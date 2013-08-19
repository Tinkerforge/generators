/*
 * Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
 * Copyright (C) 2011-2012 Olaf Lüke <olaf@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted.
 */

using System;
using System.Collections.Generic;
using System.Threading;
using System.Net;
using System.Net.Sockets;
using System.Runtime.InteropServices;
using System.IO;
using System.Text;

[assembly: CLSCompliant(true)]
namespace Tinkerforge
{
	public class IPConnection
	{
		internal int responseTimeout = 2500;

		internal const byte FUNCTION_DISCONNECT_PROBE = 128;
		internal const byte FUNCTION_ENUMERATE = 254;

		internal const byte CALLBACK_ENUMERATE = 253;

		internal const int CALLBACK_CONNECTED = 0;
		internal const int CALLBACK_DISCONNECTED = 1;

		internal const long BROADCAST_UID = (long)0;

		internal const int DISCONNECT_PROBE_INTERVAL = 5000;

		// enumeration_type parameter to the enumerate callback
		public const short ENUMERATION_TYPE_AVAILABLE = 0;
		public const short ENUMERATION_TYPE_CONNECTED = 1;
		public const short ENUMERATION_TYPE_DISCONNECTED = 2;

		// connect_reason parameter to the connected callback
		public const short CONNECT_REASON_REQUEST = 0;
		public const short CONNECT_REASON_AUTO_RECONNECT = 1;

		// disconnect_reason parameter to the disconnected callback
		public const short DISCONNECT_REASON_REQUEST = 0;
		public const short DISCONNECT_REASON_ERROR = 1;
		public const short DISCONNECT_REASON_SHUTDOWN = 2;

		// returned by get_connection_state
		public const short CONNECTION_STATE_DISCONNECTED = 0;
		public const short CONNECTION_STATE_CONNECTED = 1;
		public const short CONNECTION_STATE_PENDING = 2; // auto-reconnect in process

		internal const int QUEUE_EXIT = 0;
		internal const int QUEUE_META = 1;
		internal const int QUEUE_PACKET = 2;

		internal int nextSequenceNumber = 0; // protected by sequenceNumberLock
		private object sequenceNumberLock = new object();

		internal bool autoReconnectAllowed = false;
		internal bool autoReconnectPending = false;
		internal bool autoReconnect = true;

		string host;
		int port;
		Socket socket = null;
		internal object socketLock = new object();
		NetworkStream socketStream = null; // protected by socketLock
		internal object socketStreamSendLock = new object(); // used to synchronize send access to socketStream
		long socketID = 0; // protected by socketLock
		Thread receiveThread = null;
		bool receiveFlag = true;
		CallbackContext callback = null;
		internal Dictionary<int, Device> devices = new Dictionary<int, Device>();
		BlockingQueue<bool> waiter = new BlockingQueue<bool>();

		bool disconnectProbeFlag = false;
		BlockingQueue<bool> disconnectProbeQueue = null;
		Thread disconnectProbeThread = null;

		public event EnumerateEventHandler EnumerateCallback;
		public delegate void EnumerateEventHandler(IPConnection sender, string uid, string connectedUid,
		                                           char position, short[] hardwareVersion, short[] firmwareVersion,
		                                           int deviceIdentifier, short enumerationType);
		public event ConnectedEventHandler Connected;
		public delegate void ConnectedEventHandler(IPConnection sender, short connectReason);
		public event DisconnectedEventHandler Disconnected;
		public delegate void DisconnectedEventHandler(IPConnection sender, short disconnectReason);

		class CallbackQueueObject
		{
			public int kind;
			public byte functionID;
			public short parameter;
			public long socketID;
			public byte[] packet;

			public CallbackQueueObject(int kind, byte functionID, short parameter, long socketID, byte[] packet)
			{
				this.kind = kind;
				this.functionID = functionID;
				this.parameter = parameter;
				this.socketID = socketID;
				this.packet = packet;
			}
		}

		class CallbackContext
		{
			public Thread thread = null;
			public BlockingQueue<CallbackQueueObject> queue = null;
			public object lock_ = null;
			public bool packetDispatchAllowed = false;
		}

		/// <summary>
		///  Creates an IP Connection object that can be used to enumerate the
		///  available devices. It is also required for the constructor of
		///  Bricks and Bricklets.
		/// </summary>
		public IPConnection()
		{
		}

		/// <summary>
		///  Creates a TCP/IP connection to the given *host* and *port*.
		///  The host and port can point to a Brick Daemon or to a WIFI/Ethernet
		///  Extension.
		///
		///  Devices can only be controlled when the connection was established
		///  successfully.
		///
		///  Blocks until the connection is established and throws an exception
		///  if there is no Brick Daemon or WIFI/Ethernet Extension listening
		///  at the given host and port.
		/// </summary>
		public void Connect(string host, int port)
		{
			lock (socketLock)
			{
				if (socket != null)
				{
					throw new AlreadyConnectedException("Already connected to " + this.host + ":" + this.port);
				}

				this.host = host;
				this.port = port;

				ConnectUnlocked(false);
			}
		}

		// NOTE: assumes that socketLock is locked
		private void ConnectUnlocked(bool isAutoReconnect)
		{
			if (callback == null)
			{
				callback = new CallbackContext();
				callback.packetDispatchAllowed = false;
				callback.queue = new BlockingQueue<CallbackQueueObject>();
				callback.lock_ = new object();
				callback.thread = new Thread(delegate() { this.CallbackLoop(callback); });
				callback.thread.IsBackground = true;
				callback.thread.Name = "Callback-Processor";
				callback.thread.Start();
			}

			try
			{
				socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
				socket.NoDelay = true;
				ConnectSocket(host, port);
			}
			catch (Exception)
			{
				if (socket != null)
				{
					socket.Close();
					socket = null;
				}
				throw;
			}

			socketStream = new NetworkStream(socket);
			++socketID;

			// create disconnect probe thread
			disconnectProbeFlag = true;
			disconnectProbeQueue = new BlockingQueue<bool>();
			disconnectProbeThread = new Thread(delegate() { this.DisconnectProbeLoop(disconnectProbeQueue); });
			disconnectProbeThread.IsBackground = true;
			disconnectProbeThread.Name = "Disconnect-Prober";
			disconnectProbeThread.Start();

			callback.packetDispatchAllowed = true;

			receiveFlag = true;

			receiveThread = new Thread(delegate() { this.ReceiveLoop(socketID); });
			receiveThread.IsBackground = true;
			receiveThread.Name = "Brickd-Receiver";
			receiveThread.Start();

			autoReconnectAllowed = false;
			autoReconnectPending = false;

			short connectReason = IPConnection.CONNECT_REASON_REQUEST;
			if (isAutoReconnect)
			{
				connectReason = CONNECT_REASON_AUTO_RECONNECT;
			}

			callback.queue.Enqueue(new CallbackQueueObject(QUEUE_META, CALLBACK_CONNECTED,
			                                               connectReason, 0, null));
		}

		/// <summary>
		///  Disconnects the TCP/IP connection from the Brick Daemon or the
		///  WIFI/Ethernet Extension.
		/// </summary>
		public void Disconnect()
		{
			CallbackContext localCallback = null;

			lock (socketLock)
			{
				autoReconnectAllowed = false;

				if (autoReconnectPending)
				{
					autoReconnectPending = false;
				}
				else
				{
					if (socket == null)
					{
						throw new NotConnectedException();
					}

					DisconnectUnlocked();
				}

				localCallback = callback;
				callback = null;
			}

			localCallback.queue.Enqueue(new CallbackQueueObject(QUEUE_META, CALLBACK_DISCONNECTED,
			                                                    DISCONNECT_REASON_REQUEST, 0, null));
			localCallback.queue.Enqueue(new CallbackQueueObject(QUEUE_EXIT, 0, 0, 0, null));

			if (Thread.CurrentThread != localCallback.thread)
			{
				localCallback.thread.Join();
			}
		}

		// NOTE: assumes that socketLock is locked
		private void DisconnectUnlocked()
		{
			// destroy disconnect probe thread
			disconnectProbeQueue.Enqueue(true);
			disconnectProbeThread.Join();
			disconnectProbeThread = null;

			// stop dispatching packet callbacks before ending the receive
			// thread to avoid timeout exceptions due to callback functions
			// trying to call getters
			if (Thread.CurrentThread != callback.thread)
			{
				// FIXME: cannot lock callback lock here because this can
				//        deadlock due to an ordering problem with the socket lock
				//lock (callback.lock_)
				{
					callback.packetDispatchAllowed = false;
				}
			}
			else
			{
				callback.packetDispatchAllowed = false;
			}

			receiveFlag = false;

			socketStream.Close();
			socket.Shutdown(SocketShutdown.Both);
			socket.Close();

			socketStream = null;
			socket = null;

			if (receiveThread != null)
			{
				receiveThread.Join();
				receiveThread = null;
			}
		}

		/// <summary>
		///  Can return the following states:
		///
		///  - CONNECTION_STATE_DISCONNECTED: No connection is established.
		///  - CONNECTION_STATE_CONNECTED: A connection to the Brick Daemon or
		///    the WIFI/Ethernet Extension  is established.
		///  - CONNECTION_STATE_PENDING: IP Connection is currently trying to
		///    connect.
		/// </summary>
		public short GetConnectionState()
		{
			if (socket != null)
			{
				return CONNECTION_STATE_CONNECTED;
			}

			if (autoReconnectPending)
			{
				return CONNECTION_STATE_PENDING;
			}

			return CONNECTION_STATE_DISCONNECTED;
		}

		/// <summary>
		///  Enables or disables auto-reconnect. If auto-reconnect is enabled,
		///  the IP Connection will try to reconnect to the previously given
		///  host and port, if the connection is lost.
		///
		///  Default value is *true*.
		/// </summary>
		public void SetAutoReconnect(bool autoReconnect)
		{
			this.autoReconnect = autoReconnect;

			if (!autoReconnect)
			{
				autoReconnectAllowed = false;
			}
		}

		/// <summary>
		///  Returns *true* if auto-reconnect is enabled, *false* otherwise.
		/// </summary>
		public bool GetAutoReconnect()
		{
			return autoReconnect;
		}

		/// <summary>
		///  Sets the timeout in milliseconds for getters and for setters for
		///  which the response expected flag is activated.
		///
		///  Default timeout is 2500.
		/// </summary>
		public void SetTimeout(int timeout)
		{
			if (timeout < 0)
			{
				throw new ArgumentOutOfRangeException("Timeout cannot be negative");
			}

			responseTimeout = timeout;
		}

		/// <summary>
		///  Returns the timeout as set by SetTimeout.
		/// </summary>
		public int GetTimeout()
		{
			return responseTimeout;
		}

		/// <summary>
		///  Broadcasts an enumerate request. All devices will respond with an
		///  enumerate callback.
		/// </summary>
		public void Enumerate()
		{
			byte[] request = new byte[8];
			LEConverter.To((byte)0, 0, request);
			LEConverter.To((byte)8, 4, request);
			LEConverter.To(FUNCTION_ENUMERATE, 5, request);
			LEConverter.To((byte)((GetNextSequenceNumber() << 4)), 6, request);
			LEConverter.To((byte)0, 7, request);

			SendRequest(request);
		}

		/// <summary>
		///  Stops the current thread until Unwait is called.
		///
		///  This is useful if you rely solely on callbacks for events, if you
		///  want to wait for a specific callback or if the IP Connection was
		///  created in a thread.
		///
		///  Wait and Unwait act in the same way as "acquire" and "release" of
		///  a semaphore.
		/// </summary>
		public void Wait()
		{
			bool value;

			waiter.TryDequeue(out value);
		}

		/// <summary>
		///  Unwaits the thread previously stopped by Wait.
		///
		///  Wait and Unwait act in the same way as "acquire" and "release" of
		///  a semaphore.
		/// </summary>
		public void Unwait()
		{
			waiter.Enqueue(true);
		}

		internal int GetNextSequenceNumber()
		{
			int currentSequenceNumber;
			lock (sequenceNumberLock)
			{
				currentSequenceNumber = nextSequenceNumber + 1;
				nextSequenceNumber = currentSequenceNumber % 15;
			}
			return currentSequenceNumber;
		}

		private void ConnectSocket(string host, int port)
		{
#if WINDOWS_PHONE
			IPAddress ipAddress = IPAddress.Parse(host);
			var endpoint = new IPEndPoint(ipAddress, port);

			SocketAsyncEventArgs args = new SocketAsyncEventArgs();
			args.RemoteEndPoint = endpoint;

			AutoResetEvent connectedEvent = new AutoResetEvent(false);
			args.Completed += new EventHandler<SocketAsyncEventArgs>((o, e) => { connectedEvent.Set(); });
			bool connectPending = socket.ConnectAsync(args);

			if (connectPending)
			{
				connectedEvent.WaitOne();
			}
			if (!connectPending || args.SocketError != SocketError.Success)
			{
				throw new IOException(string.Format("Could not connect: {0}", args.SocketError));
			}
#else
			socket.Connect(host, port);
#endif
		}

		private void ReceiveLoop(long localSocketID)
		{
			byte[] pendingData = new byte[8192];
			int pendingLength = 0;

			while (receiveFlag)
			{
				int length = 0;

				try
				{
					length = socketStream.Read(pendingData, pendingLength,
					                           pendingData.Length - pendingLength);
				}
				catch (IOException e)
				{
					if (e.InnerException != null &&
					    e.InnerException is SocketException)
					{
						if (receiveFlag)
						{
							HandleDisconnectByPeer(DISCONNECT_REASON_ERROR, localSocketID, false);
						}
					}

					return;
				}
				catch (ObjectDisposedException)
				{
					return;
				}
				catch (NullReferenceException)
				{
					return;
				}

				if (length == 0)
				{
					if (receiveFlag)
					{
						HandleDisconnectByPeer(DISCONNECT_REASON_SHUTDOWN, localSocketID, false);
					}
				}

				pendingLength += length;

				while (receiveFlag)
				{
					if (pendingLength < 8)
					{
						// Wait for complete header
						break;
					}

					length = GetLengthFromData(pendingData);

					if (pendingLength < length)
					{
						// Wait for complete packet
						break;
					}

					byte[] packet = new byte[length];

					Array.Copy(pendingData, 0, packet, 0, length);
					Array.Copy(pendingData, length, pendingData, 0, pendingLength - length);
					pendingLength -= length;
					HandleResponse(packet);
				}
			}
		}

		private void DispatchMeta(CallbackQueueObject cqo)
		{
			switch (cqo.functionID)
			{
				case IPConnection.CALLBACK_CONNECTED:
					var handler = Connected;
					if (handler != null)
					{
						handler(this, cqo.parameter);
					}
					break;

				case IPConnection.CALLBACK_DISCONNECTED:
					if (cqo.parameter != DISCONNECT_REASON_REQUEST)
					{
						// need to do this here, the receive loop is not allowed to
						// hold the socket lock because this could cause a deadlock
						// with a concurrent call to the (dis-)connect function
						lock (socketLock)
						{
							// don't close the socket if it got disconnected or
							// reconnected in the meantime
							if (socket != null && socketID == cqo.socketID)
							{
								// destroy disconnect probe thread
								disconnectProbeQueue.Enqueue(true);
								disconnectProbeThread.Join();
								disconnectProbeThread = null;

								// destroy socket
								socketStream.Close();
								socket.Close();

								socketStream = null;
								socket = null;
							}
						}
					}

					Thread.Sleep(100);

					var disconHandler = Disconnected;
					if (disconHandler != null)
					{
						disconHandler(this, cqo.parameter);
					}

					if (cqo.parameter != DISCONNECT_REASON_REQUEST &&
					    autoReconnect && autoReconnectAllowed)
					{
						autoReconnectPending = true;
						bool retry = true;
						while (retry)
						{
							retry = false;
							lock (socketLock)
							{
								if (autoReconnectAllowed && socket == null)
								{
									try
									{
										ConnectUnlocked(true);
									}
									catch (Exception)
									{
										retry = true;
									}
								}
								else
								{
									autoReconnectPending = false;
								}
							}

							if (retry)
							{
								Thread.Sleep(100);
							}
						}
					}

					break;
			}
		}

		private void DispatchPacket(CallbackQueueObject cqo)
		{
			byte fid = GetFunctionIDFromData(cqo.packet);

			if (fid == CALLBACK_ENUMERATE)
			{
				var enumHandler = EnumerateCallback;
				if (enumHandler != null)
				{
					string uid_str = LEConverter.StringFrom(8, cqo.packet, 8);
					string connectedUid_str = LEConverter.StringFrom(16, cqo.packet, 8);
					char position = (char)LEConverter.CharFrom(24, cqo.packet);
					short[] hardwareVersion = new short[3];
					hardwareVersion[0] = LEConverter.ByteFrom(25, cqo.packet);
					hardwareVersion[1] = LEConverter.ByteFrom(26, cqo.packet);
					hardwareVersion[2] = LEConverter.ByteFrom(27, cqo.packet);
					short[] firmwareVersion = new short[3];
					firmwareVersion[0] = LEConverter.ByteFrom(28, cqo.packet);
					firmwareVersion[1] = LEConverter.ByteFrom(29, cqo.packet);
					firmwareVersion[2] = LEConverter.ByteFrom(30, cqo.packet);
					int deviceIdentifier = LEConverter.ShortFrom(31, cqo.packet);
					short enumerationType = LEConverter.ByteFrom(33, cqo.packet);

					enumHandler(this, uid_str, connectedUid_str, position, hardwareVersion,
					            firmwareVersion, deviceIdentifier, enumerationType);
				}
			}
			else
			{
				int uid = GetUIDFromData(cqo.packet);

				if (devices.ContainsKey(uid))
				{
					Device device = devices[uid];
					Device.CallbackWrapper wrapper = device.callbackWrappers[fid];
					if (wrapper != null)
					{
						wrapper(cqo.packet);
					}
				}
			}
		}

		private void CallbackLoop(CallbackContext localCallback)
		{
			while (true)
			{
				CallbackQueueObject cqo;
				if (!localCallback.queue.TryDequeue(out cqo, Timeout.Infinite))
				{
					continue;
				}

				if (cqo == null)
				{
					continue;
				}

				// FIXME: cannot lock callback lock here because this can
				//        deadlock due to an ordering problem with the socket lock
				//lock (localCallback.lock_)
				{
					switch (cqo.kind)
					{
						case IPConnection.QUEUE_EXIT:
							return;

						case IPConnection.QUEUE_META:
							DispatchMeta(cqo);
							break;

						case IPConnection.QUEUE_PACKET:
							// don't dispatch callbacks when the receive thread isn't running
							if (localCallback.packetDispatchAllowed)
							{
								DispatchPacket(cqo);
							}

							break;
					}
				}
			}
		}

		// NOTE: the disconnect probe loop is not allowed to hold the socketLock at any
		//       time because it is created and joined while the socketLock is locked
		private void DisconnectProbeLoop(BlockingQueue<bool> localDisconnectProbeQueue)
		{
			byte[] request = new byte[8];
			LEConverter.To((byte)0, 0, request);
			LEConverter.To((byte)8, 4, request);
			LEConverter.To(FUNCTION_DISCONNECT_PROBE, 5, request);
			LEConverter.To((byte)((GetNextSequenceNumber() << 4)), 6, request);
			LEConverter.To((byte)0, 7, request);

			bool response;
			while (true)
			{
				if (localDisconnectProbeQueue.TryDequeue(out response, DISCONNECT_PROBE_INTERVAL))
				{
					break;
				}

				if (disconnectProbeFlag)
				{
					try
					{
						lock (socketStreamSendLock)
						{
							socketStream.Write(request, 0, request.Length);
						}
					}
					catch (IOException e)
					{
						if (e.InnerException != null &&
						    e.InnerException is SocketException)
						{
							HandleDisconnectByPeer(DISCONNECT_REASON_ERROR, socketID, false);
							break;
						}
					}
				}
				else
				{
					disconnectProbeFlag = true;
				}
			}
		}

		internal static byte GetFunctionIDFromData(byte[] data)
		{
			return data[5];
		}

		internal static int GetLengthFromData(byte[] data)
		{
			return data[4];
		}

		internal static int GetUIDFromData(byte[] data)
		{
			return LEConverter.IntFrom(0, data);
		}

		internal static byte GetSequenceNumberFromData(byte[] data)
		{
			return (byte)((((int)data[6]) >> 4) & 0x0F);
		}

		internal static bool GetResponseExpectedFromData(byte[] data)
		{
			return (((int)(data[6]) >> 3) & 0x01) == 0x01;
		}

		internal static byte GetErrorCodeFromData(byte[] data)
		{
			return (byte)(((int)(data[7] >> 6)) & 0x03);
		}

		// NOTE: assumes that socketLock is locked if disconnectImmediately is true
		private void HandleDisconnectByPeer(short disconnectReason, long socketID,
		                                    bool disconnectImmediately)
		{
			autoReconnectAllowed = true;

			if (disconnectImmediately)
			{
				DisconnectUnlocked();
			}

			callback.queue.Enqueue(new CallbackQueueObject(QUEUE_META, CALLBACK_DISCONNECTED,
			                                               disconnectReason, socketID, null));
		}

		private void HandleResponse(byte[] packet)
		{
			byte functionID = GetFunctionIDFromData(packet);
			byte sequenceNumber = GetSequenceNumberFromData(packet);

			disconnectProbeFlag = false;

			if (sequenceNumber == 0 && functionID == CALLBACK_ENUMERATE)
			{
				callback.queue.Enqueue(new CallbackQueueObject(QUEUE_PACKET, 0, 0, 0, packet));
				return;
			}

			int uid = GetUIDFromData(packet);

			if (!devices.ContainsKey(uid))
			{
				// Response from an unknown device, ignoring it
				return;
			}

			Device device = devices[uid];

			if (sequenceNumber == 0)
			{
				Device.CallbackWrapper wrapper = device.callbackWrappers[functionID];

				if (wrapper != null)
				{
					callback.queue.Enqueue(new CallbackQueueObject(QUEUE_PACKET, 0, 0, 0, packet));
				}

				return;
			}

			if (functionID == device.expectedResponseFunctionID &&
			    sequenceNumber == device.expectedResponseSequenceNumber)
			{
				device.responseQueue.Enqueue(packet);
				return;
			}

			// Response seems to be OK, but can't be handled
		}

		public void SendRequest(byte[] request)
		{
			lock (socketLock)
			{
				if (GetConnectionState() != IPConnection.CONNECTION_STATE_CONNECTED)
				{
					throw new NotConnectedException();
				}

				try
				{
					lock (socketStreamSendLock)
					{
						socketStream.Write(request, 0, request.Length);
					}
				}
				catch (IOException e)
				{
					if (e.InnerException != null &&
					    e.InnerException is SocketException)
					{
						HandleDisconnectByPeer(DISCONNECT_REASON_ERROR, socketID, true);
						throw new NotConnectedException();
					}
				}

				disconnectProbeFlag = false;
			}
		}

		internal void AddDevice(Device device)
		{
			devices[(int)device.internalUID] = device; // TODO: Dictionary might use UID directly as key; FIXME: might use weakref here
		}
	}

	public class TinkerforgeException : Exception
	{
		public TinkerforgeException()
		{
		}

		public TinkerforgeException(string message)
			: base(message)
		{
		}
	}

	public class TimeoutException : TinkerforgeException
	{
		public TimeoutException(string message)
			: base(message)
		{
		}
	}

	public class AlreadyConnectedException : TinkerforgeException
	{
		public AlreadyConnectedException(string message)
			: base(message)
		{
		}
	}

	public class NotConnectedException : TinkerforgeException
	{
		public NotConnectedException()
		{
		}
	}

	public struct UID
	{
		private string StringRepresentation;
		private int IntRepresentation;

		public UID(string uid)
		{
			StringRepresentation = uid;
			long uidTmp = Base58.Decode(uid);
			if (uidTmp > 0xFFFFFFFFL)
			{
				// convert from 64bit to 32bit
				long value1 = uidTmp & 0xFFFFFFFFL;
				long value2 = (uidTmp >> 32) & 0xFFFFFFFFL;

				uidTmp  = (value1 & 0x00000FFFL);
				uidTmp |= (value1 & 0x0F000000L) >> 12;
				uidTmp |= (value2 & 0x0000003FL) << 16;
				uidTmp |= (value2 & 0x000F0000L) << 6;
				uidTmp |= (value2 & 0x3F000000L) << 2;
			}

			IntRepresentation = (int)uidTmp;
		}

		public int ToInt()
		{
			return IntRepresentation;
		}

		public static explicit operator int(UID uid)
		{
			return uid.ToInt();
		}

		public override string ToString()
		{
			return StringRepresentation;
		}
	}

	public abstract class Device
	{
		internal byte stackID = 0;
		internal short[] apiVersion = new short[3];
		internal ResponseExpectedFlag[] responseExpected = new ResponseExpectedFlag[256];
		internal byte expectedResponseFunctionID = 0; // protected by requestLock
		internal byte expectedResponseSequenceNumber = 0; // protected by requestLock
		internal CallbackWrapper[] callbackWrappers = new CallbackWrapper[256];
		internal BlockingQueue<byte[]> responseQueue = new BlockingQueue<byte[]>();
		internal IPConnection ipcon = null;
		internal object requestLock = new object();
		internal UID internalUID;

		public string UID
		{
			get
			{
				return internalUID.ToString();
			}
		}

		internal enum ResponseExpectedFlag
		{
			INVALID_FUNCTION_ID = 0,
			ALWAYS_TRUE = 1,
			ALWAYS_FALSE = 2,
			TRUE = 3,
			FALSE = 4
		}

		internal delegate void CallbackWrapper(byte[] data);

		/// <summary>
		///  Creates the device objectwith the unique device ID *uid* and adds
		///  it to the IPConnection *ipcon*.
		/// </summary>
		public Device(string uid, IPConnection ipcon)
		{
			internalUID = new UID(uid);
			this.ipcon = ipcon;

			for (int i = 0; i < responseExpected.Length; i++)
			{
				responseExpected[i] = ResponseExpectedFlag.INVALID_FUNCTION_ID;
			}

			responseExpected[IPConnection.FUNCTION_ENUMERATE] = ResponseExpectedFlag.ALWAYS_FALSE;
			responseExpected[IPConnection.CALLBACK_ENUMERATE] = ResponseExpectedFlag.ALWAYS_FALSE;

			ipcon.AddDevice(this);
		}

		/// <summary>
		///  Returns the API version (major, minor, revision) of the bindings
		///  for this device.
		/// </summary>
		public short[] GetAPIVersion()
		{
			return apiVersion;
		}

		/// <summary>
		///  Returns the response expected flag for the function specified
		///  by the *functionId* parameter. It is *true* if the function is
		///  expected to send a response, *false* otherwise.
		///
		///  For getter functions this is enabled by default and cannot be
		///  disabled, because those functions will always send a response.
		///  For callback configuration functions it is enabled by default
		///  too, but can be disabled via the setResponseExpected function.
		///  For setter functions it is disabled by default and can be enabled.
		///
		///  Enabling the response expected flag for a setter function allows
		///  to detect timeouts and other error conditions calls of this setter
		///  as well. The device will then send a response for this purpose.
		///  If this flag is disabled for a setter function then no response
		///  is send and errors are silently ignored, because they cannot be
		///  detected.
		/// </summary>
		public bool GetResponseExpected(byte functionId)
		{
			ResponseExpectedFlag flag = this.responseExpected[functionId];

			if (flag == ResponseExpectedFlag.INVALID_FUNCTION_ID)
			{
				throw new ArgumentException("Invalid function ID " + functionId);
			}

			return flag == ResponseExpectedFlag.ALWAYS_TRUE ||
			       flag == ResponseExpectedFlag.TRUE;
		}

		/// <summary>
		///  Changes the response expected flag of the function specified
		///  by the function ID parameter. This flag can only be changed
		///  for setter (default value: *false*) and callback configuration
		///  functions (default value: *true*). For getter functions it is
		///  always enabled and callbacks it is always disabled.
		///
		///  Enabling the response expected flag for a setter function allows
		///  to detect timeouts and other error conditions calls of this setter
		///  as well. The device will then send a response for this purpose.
		///  If this flag is disabled for a setter function then no response
		///  is send and errors are silently ignored, because they cannot be
		///  detected.
		/// </summary>
		public void SetResponseExpected(byte functionId, bool responseExpected)
		{
			ResponseExpectedFlag flag = this.responseExpected[functionId];

			if (flag == ResponseExpectedFlag.INVALID_FUNCTION_ID)
			{
				throw new ArgumentException("Invalid function ID " + functionId);
			}

			if (flag == ResponseExpectedFlag.ALWAYS_TRUE ||
			    flag == ResponseExpectedFlag.ALWAYS_FALSE)
			{
				throw new ArgumentException("Response Expected flag cannot be changed for function ID " + functionId);
			}

			if (responseExpected)
			{
				this.responseExpected[functionId] = ResponseExpectedFlag.TRUE;
			}
			else
			{
				this.responseExpected[functionId] = ResponseExpectedFlag.FALSE;
			}
		}

		/// <summary>
		///  Changes the response expected flag for all setter and callback
		///  configuration functions of this device at once.
		/// </summary>
		public void SetResponseExpectedAll(bool responseExpected)
		{
			ResponseExpectedFlag flag = ResponseExpectedFlag.FALSE;

			if (responseExpected)
			{
				flag = ResponseExpectedFlag.TRUE;
			}

			for (int i = 0; i < this.responseExpected.Length; i++)
			{
				if (this.responseExpected[i] == ResponseExpectedFlag.TRUE ||
				    this.responseExpected[i] == ResponseExpectedFlag.FALSE)
				{
					this.responseExpected[i] = flag;
				}
			}
		}

		public abstract void GetIdentity(out string uid, out string connectedUid, out char position,
		                                 out byte[] hardwareVersion, out byte[] firmwareVersion,
		                                 out int deviceIdentifier);

		protected byte[] CreateRequestPacket(byte length, byte fid)
		{
			byte[] packet = new byte[length];
			LEConverter.To((int)this.internalUID, 0, packet);
			LEConverter.To((byte)length, 4, packet);
			LEConverter.To((byte)fid, 5, packet);
			if (GetResponseExpected(fid))
			{
				LEConverter.To((byte)((1 << 3) | (ipcon.GetNextSequenceNumber() << 4)), 6, packet);
			}
			else
			{
				LEConverter.To((byte)((ipcon.GetNextSequenceNumber() << 4)), 6, packet);
			}
			LEConverter.To((byte)0, 7, packet);

			return packet;
		}

		protected byte[] SendRequest(byte[] request)
		{
			byte[] response = null;

			if (IPConnection.GetResponseExpectedFromData(request))
			{
				byte functionID = IPConnection.GetFunctionIDFromData(request);

				lock (requestLock)
				{
					expectedResponseFunctionID = functionID;
					expectedResponseSequenceNumber = IPConnection.GetSequenceNumberFromData(request);

					try
					{
						ipcon.SendRequest(request);

						while (true)
						{
							if (!responseQueue.TryDequeue(out response, ipcon.responseTimeout))
							{
								throw new TimeoutException("Did not receive response in time for function ID " + functionID);
							}

							if (expectedResponseFunctionID == IPConnection.GetFunctionIDFromData(response) &&
							    expectedResponseSequenceNumber == IPConnection.GetSequenceNumberFromData(response))
							{
								// ignore old responses that arrived after the timeout expired, but before setting
								// expectedResponseFunctionID and expectedResponseSequenceNumber back to 0
								break;
							}
						}
					}
					finally
					{
						expectedResponseFunctionID = 0;
						expectedResponseSequenceNumber = 0;
					}
				}

				byte errorCode = IPConnection.GetErrorCodeFromData(response);

				switch (errorCode)
				{
					case 0:
						break;
					case 1:
						throw new NotSupportedException("Got invalid parameter for function ID " + functionID);
					case 2:
						throw new NotSupportedException("Function ID " + functionID + " is not supported");
					default:
						throw new NotSupportedException("Function ID " + functionID + " returned an unknown error");
				}
			}
			else
			{
				ipcon.SendRequest(request);
			}

			return response;
		}
	}

	public class Base58
	{
		private const string BASE58 = "123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ";

		public static int IndexOf(char c, string s)
		{
			for (int i = 0; i < s.Length; i++)
			{
				if (s[i] == c)
				{
					return i;
				}
			}

			return 0;
		}

		public static string Encode(long value)
		{
			string encoded = "";
			while (value >= 58)
			{
				long div = value / 58;
				int mod = (int)(value % 58);
				encoded = BASE58[mod] + encoded;
				value = div;
			}

			encoded = BASE58[(int)value] + encoded;
			return encoded;
		}

		public static long Decode(string encoded)
		{
			long value = 0;
			long columnMultiplier = 1;
			for (int i = encoded.Length - 1; i >= 0; i--)
			{
				int column = IndexOf(encoded[i], BASE58);
				value += column * columnMultiplier;
				columnMultiplier *= 58;
			}

			return value;
		}
	}

	internal class LEConverter
	{
		static public void To(string data, int position, int len, byte[] array)
		{
			for (int i = 0; i < Math.Min(len, data.Length); i++)
			{
				array[position + i] = (byte)data[i];
			}

			for (int i = Math.Min(len, data.Length); i < len; i++)
			{
				array[position + i] = 0;
			}
		}

		static public void To(long data, int position, byte[] array)
		{
			array[position + 0] = (byte)data;
			array[position + 1] = (byte)(((ulong)data >>  8) & 0xFF);
			array[position + 2] = (byte)(((ulong)data >> 16) & 0xFF);
			array[position + 3] = (byte)(((ulong)data >> 24) & 0xFF);
			array[position + 4] = (byte)(((ulong)data >> 32) & 0xFF);
			array[position + 5] = (byte)(((ulong)data >> 40) & 0xFF);
			array[position + 6] = (byte)(((ulong)data >> 48) & 0xFF);
			array[position + 7] = (byte)(((ulong)data >> 56) & 0xFF);
		}

		static public void To(long[] data, int position, int len, byte[] array)
		{
			for (int i = 0; i < len; i++)
			{
				To(data[i], position + i, array);
			}
		}

		static public void To(int data, int position, byte[] array)
		{
			array[position + 0] = (byte)data;
			array[position + 1] = (byte)(((uint)data >>  8) & 0xFF);
			array[position + 2] = (byte)(((uint)data >> 16) & 0xFF);
			array[position + 3] = (byte)(((uint)data >> 24) & 0xFF);
		}

		static public void To(int[] data, int position, int len, byte[] array)
		{
			for (int i = 0; i < len; i++)
			{
				To(data[i], position + i, array);
			}
		}

		static public void To(short data, int position, byte[] array)
		{
			array[position + 0] = (byte)data;
			array[position + 1] = (byte)(((ushort)data >> 8) & 0xFF);
		}

		static public void To(short[] data, int position, int len, byte[] array)
		{
			for (int i = 0; i < len; i++)
			{
				To(data[i], position + i, array);
			}
		}

		static public void To(byte data, int position, byte[] array)
		{
			array[position + 0] = (byte)data;
		}

		static public void To(byte[] data, int position, int len, byte[] array)
		{
			for (int i = 0; i < len; i++)
			{
				To(data[i], position + i, array);
			}
		}

		static public void To(char data, int position, byte[] array)
		{
			array[position + 0] = (byte)data;
		}

		static public void To(char[] data, int position, int len, byte[] array)
		{
			for (int i = 0; i < len; i++)
			{
				To(data[i], position + i, array);
			}
		}

		static public void To(bool data, int position, byte[] array)
		{
			if (data)
			{
				array[position + 0] = 1;
			}
			else
			{
				array[position + 0] = 0;
			}
		}

		static public void To(bool[] data, int position, int len, byte[] array)
		{
			for (int i = 0; i < len; i++)
			{
				To(data[i], position + i, array);
			}
		}

		static public bool BoolFrom(int position, byte[] array)
		{
			return array[position] != 0;
		}

		static public bool[] BoolArrayFrom(int position, byte[] array, int len)
		{
			bool[] ret = new bool[len];

			for (int i = 0; i < len; i++)
			{
				ret[i] = BoolFrom(position + i * 1, array);
			}

			return ret;
		}

		static public char CharFrom(int position, byte[] array)
		{
			return (char)array[position];
		}

		static public char[] CharArrayFrom(int position, byte[] array, int len)
		{
			char[] ret = new char[len];

			for (int i = 0; i < len; i++)
			{
				ret[i] = CharFrom(position + i * 1, array);
			}

			return ret;
		}

		static public short SByteFrom(int position, byte[] array)
		{
			return (short)array[position];
		}

		static public short[] SByteArrayFrom(int position, byte[] array, int len)
		{
			short[] ret = new short[len];

			for (int i = 0; i < len; i++)
			{
				ret[i] = SByteFrom(position + i * 1, array);
			}

			return ret;
		}

		static public byte ByteFrom(int position, byte[] array)
		{
			return (byte)array[position];
		}

		static public byte[] ByteArrayFrom(int position, byte[] array, int len)
		{
			byte[] ret = new byte[len];

			for (int i = 0; i < len; i++)
			{
				ret[i] = ByteFrom(position + i * 1, array);
			}

			return ret;
		}

		static public short ShortFrom(int position, byte[] array)
		{
			return (short)((ushort)array[position + 0] << 0 |
			               (ushort)array[position + 1] << 8);
		}

		static public short[] ShortArrayFrom(int position, byte[] array, int len)
		{
			short[] ret = new short[len];

			for (int i = 0; i < len; i++)
			{
				ret[i] = ShortFrom(position + i * 2, array);
			}

			return ret;
		}

		static public int UShortFrom(int position, byte[] array)
		{
			return (int)((int)array[position + 0] << 0 |
			             (int)array[position + 1] << 8);
		}

		static public int[] UShortArrayFrom(int position, byte[] array, int len)
		{
			int[] ret = new int[len];

			for (int i = 0; i < len; i++)
			{
				ret[i] = UShortFrom(position + i * 2, array);
			}

			return ret;
		}

		static public int IntFrom(int position, byte[] array)
		{
			return (int)((int)array[position + 0] <<  0 |
			             (int)array[position + 1] <<  8 |
			             (int)array[position + 2] << 16 |
			             (int)array[position + 3] << 24);
		}

		static public int[] IntArrayFrom(int position, byte[] array, int len)
		{
			int[] ret = new int[len];

			for (int i = 0; i < len; i++)
			{
				ret[i] = IntFrom(position + i * 4, array);
			}

			return ret;
		}

		static public long UIntFrom(int position, byte[] array)
		{
			return (long)((long)array[position + 0] <<  0 |
			              (long)array[position + 1] <<  8 |
			              (long)array[position + 2] << 16 |
			              (long)array[position + 3] << 24);
		}

		static public long[] UIntArrayFrom(int position, byte[] array, int len)
		{
			long[] ret = new long[len];

			for (int i = 0; i < len; i++)
			{
				ret[i] = UIntFrom(position + i * 4, array);
			}

			return ret;
		}

		static public long LongFrom(int position, byte[] array)
		{
			return (long)((long)array[position + 0] <<  0 |
			              (long)array[position + 1] <<  8 |
			              (long)array[position + 2] << 16 |
			              (long)array[position + 3] << 24 |
			              (long)array[position + 4] << 32 |
			              (long)array[position + 5] << 40 |
			              (long)array[position + 6] << 48 |
			              (long)array[position + 7] << 56);
		}

		static public long[] LongArrayFrom(int position, byte[] array, int len)
		{
			long[] ret = new long[len];

			for (int i = 0; i < len; i++)
			{
				ret[i] = LongFrom(position + i * 8, array);
			}

			return ret;
		}

		static public long ULongFrom(int position, byte[] array)
		{
			return (long)((long)array[position + 0] <<  0 |
			              (long)array[position + 1] <<  8 |
			              (long)array[position + 2] << 16 |
			              (long)array[position + 3] << 24 |
			              (long)array[position + 4] << 32 |
			              (long)array[position + 5] << 40 |
			              (long)array[position + 6] << 48 |
			              (long)array[position + 7] << 56);
		}

		static public long[] ULongArrayFrom(int position, byte[] array, int len)
		{
			long[] ret = new long[len];

			for (int i = 0; i < len; i++)
			{
				ret[i] = ULongFrom(position + i * 8, array);
			}

			return ret;
		}

		static public float FloatFrom(int position, byte[] array)
		{
			// We need Little Endian
			if (BitConverter.IsLittleEndian)
			{
				return BitConverter.ToSingle(array, position);
			}
			else
			{
				byte[] array_tmp = new byte[4];
				array_tmp[3] = array[position + 0];
				array_tmp[2] = array[position + 1];
				array_tmp[1] = array[position + 2];
				array_tmp[0] = array[position + 3];
				return BitConverter.ToSingle(array_tmp, 0);
			}
		}

		static public float[] FloatArrayFrom(int position, byte[] array, int len)
		{
			float[] ret = new float[len];

			for (int i = 0; i < len; i++)
			{
				ret[i] = FloatFrom(position + i * 4, array);
			}

			return ret;
		}

		static public string StringFrom(int position, byte[] array, int len)
		{
			StringBuilder sb = new StringBuilder(len);
			for (int i = position; i < position + len; i++)
			{
				if (array[i] == 0)
				{
					break;
				}
				sb.Append((char)array[i]);
			}

			return sb.ToString();
		}
	}

	// There is no BlockingQueue in c# version <= 2.0, we make our own
	// to be backward compatible
	internal class BlockingQueue<T>
	{
		private bool closing;
		private readonly Queue<T> queue = new Queue<T>();

		public int Count
		{
			get
			{
				lock (queue)
				{
					return queue.Count;
				}
			}
		}

		public BlockingQueue()
		{
			lock (queue)
			{
				closing = false;
				Monitor.PulseAll(queue);
			}
		}

		public bool Enqueue(T item)
		{
			lock (queue)
			{
				if (closing || null == item)
				{
					return false;
				}

				queue.Enqueue(item);

				if (queue.Count == 1)
				{
					// wake up any blocked dequeue
					Monitor.PulseAll(queue);
				}

				return true;
			}
		}

		public void Close()
		{
			lock (queue)
			{
				if (!closing)
				{
					closing = true;
					queue.Clear();
					Monitor.PulseAll(queue);
				}
			}
		}

		public bool TryDequeue(out T value)
		{
			return TryDequeue(out value, Timeout.Infinite);
		}

		public bool TryDequeue(out T value, int timeout)
		{
			lock (queue)
			{
				while (queue.Count == 0)
				{
					if (closing ||
					   (timeout < Timeout.Infinite) ||
					   !Monitor.Wait(queue, timeout))
					{
						value = default(T);
						return false;
					}
				}

				value = (T)queue.Dequeue();
				return true;
			}
		}

		public void Clear()
		{
			lock (queue)
			{
				queue.Clear();
				Monitor.Pulse(queue);
			}
		}
	}
#if WINDOWS_PHONE
	internal class NetworkStream : Stream
	{
		private Socket socket;

		private BlockingQueue<byte[]> ReceiveQueue = new BlockingQueue<byte[]>();
		private byte[] ImmediateReadBuffer;
		private int ImmediateReadOffset;

		private object readLock = new object();
		private object writeLock = new object();
		private AutoResetEvent WriteCompleteEvent = new AutoResetEvent(false);

		public override bool CanRead
		{
			get { return true; }
		}

		public override bool CanSeek
		{
			get { return false; }
		}

		public override bool CanWrite
		{
			get { return true; }
		}

		public override void Flush()
		{
			//stream is always flushed
		}

		public NetworkStream(Socket sock)
		{
			socket = sock;
			SocketAsyncEventArgs args = new SocketAsyncEventArgs();
			byte[] buffer = new byte[8192];
			args.SetBuffer(buffer, 0, buffer.Length);
			args.Completed += OnIOCompletion;
			if (!socket.ReceiveAsync(args))
			{
				throw new IOException(string.Format("Could not initialize NetworkStream: {0}", args.SocketError));
			}
		}

		private void OnIOCompletion(object sender, SocketAsyncEventArgs e)
		{
			if (e.SocketError == SocketError.OperationAborted)
			{
				// make Read() report an socket error
				byte[] buffer = new byte[0];
				ReceiveQueue.Enqueue(buffer);
				return;
			}
			else if (e.SocketError != SocketError.Success)
			{
				//TODO: error handling
			}

			switch (e.LastOperation)
			{
				case SocketAsyncOperation.Receive:
					if (e.BytesTransferred == 0)
					{
						//TODO: error handling
						break;
					}
					byte[] receiveBuffer = new byte[e.BytesTransferred];
					Array.Copy(e.Buffer, receiveBuffer, e.BytesTransferred);
					ReceiveQueue.Enqueue(receiveBuffer);
					if (!socket.ReceiveAsync(e))
					{
						//TODO: error handling
					}
					break;
				case SocketAsyncOperation.Send:
					WriteCompleteEvent.Set();
					break;
				default:
					break; //TODO: error handling
			}
		}

		public override void Close()
		{
			base.Close();

			// make Read() report an socket error
			byte[] buffer = new byte[0];
			ReceiveQueue.Enqueue(buffer);
		}

		public override int Read(byte[] buffer, int offset, int count)
		{
			int readLength;
			lock (readLock)
			{
				if (ImmediateReadBuffer == null)
				{
					ReceiveQueue.TryDequeue(out ImmediateReadBuffer);

					if (ImmediateReadBuffer.Length == 0)
					{
						throw new IOException("Read failure", new SocketException(10004 /* WSAEINTR */));
					}
				}

				readLength = Math.Min(count, ImmediateReadBuffer.Length - ImmediateReadOffset);
				Array.Copy(ImmediateReadBuffer, ImmediateReadOffset, buffer, offset, readLength);

				ImmediateReadOffset += readLength;
				if (ImmediateReadOffset == ImmediateReadBuffer.Length)
				{
					ImmediateReadBuffer = null;
					ImmediateReadOffset = 0;
				}
			}
			return readLength;
		}

		public override void Write(byte[] buffer, int offset, int count)
		{
			lock (writeLock)
			{
				SocketAsyncEventArgs args = new SocketAsyncEventArgs();
				args.SetBuffer(buffer, offset, count);
				args.Completed += OnIOCompletion;
				if (!socket.SendAsync(args))
				{
					throw new IOException(string.Format("Could not write on NetworkStream: {0}", args.SocketError));
				}
				WriteCompleteEvent.WaitOne();
			}
		}

		public override long Seek(long offset, SeekOrigin origin)
		{
			throw new NotSupportedException();
		}

		public override void SetLength(long value)
		{
			throw new NotSupportedException();
		}

		public override long Position
		{
			get
			{
				throw new NotSupportedException();
			}
			set
			{
				throw new NotSupportedException();
			}
		}

		public override long Length
		{
			get { throw new NotSupportedException(); }
		}
	}
#endif
}
