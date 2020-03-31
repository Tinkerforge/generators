/*
 * Copyright (C) 2012-2015, 2017, 2020 Matthias Bolte <matthias@tinkerforge.com>
 * Copyright (C) 2011-2012 Olaf Lüke <olaf@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

using System;
using System.Collections.Generic;
using System.Threading;
using System.Net;
using System.Net.Sockets;
using System.Runtime.InteropServices;
using System.IO;
using System.Text;
using System.Reflection;
#if WINDOWS_UWP || WINDOWS_UAP
using System.Runtime.InteropServices.WindowsRuntime;
using System.Threading.Tasks;
using Windows.Foundation;
using Windows.Foundation.Collections;
using Windows.ApplicationModel.AppService;
using Windows.Security.Cryptography;
using Windows.Security.Cryptography.Core;
#else
using System.Security.Cryptography;
#endif

[assembly: CLSCompliant(true)]
namespace Tinkerforge
{
	/// <summary>
	///  The IPConnection creates a TCP/IP connection to the Brick Daemon.
	/// </summary>
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

		internal static Dictionary<int, string> deviceDisplayNames = new Dictionary<int, string>();

		// enumeration_type parameter to the enumerate callback
		/// <summary>
		///  Device is available (enumeration triggered by user: Enumerate()).
		///  This enumeration type can occur multiple times for the same device.
		/// </summary>
		public const short ENUMERATION_TYPE_AVAILABLE = 0;

		/// <summary>
		///  Device is newly connected (automatically send by Brick after
		///  establishing a communication connection). This indicates that the
		///  device has potentially lost its previous configuration and needs
		///  to be reconfigured.
		/// </summary>
		public const short ENUMERATION_TYPE_CONNECTED = 1;

		/// <summary>
		///  Device is disconnected (only possible for USB connection). In this
		///  case only uid and enumerationType are valid.
		/// </summary>
		public const short ENUMERATION_TYPE_DISCONNECTED = 2;

		// connect_reason parameter to the connected callback
		/// <summary>
		///  Connection established after request from user.
		/// </summary>
		public const short CONNECT_REASON_REQUEST = 0;

		/// <summary>
		///  Connection after auto-reconnect.
		/// </summary>
		public const short CONNECT_REASON_AUTO_RECONNECT = 1;

		// disconnect_reason parameter to the disconnected callback
		/// <summary>
		///  Disconnect was requested by user.
		/// </summary>
		public const short DISCONNECT_REASON_REQUEST = 0;

		/// <summary>
		///  Disconnect because of an unresolvable error.
		/// </summary>
		public const short DISCONNECT_REASON_ERROR = 1;

		/// <summary>
		///  Disconnect initiated by Brick Daemon or WIFI/Ethernet Extension.
		/// </summary>
		public const short DISCONNECT_REASON_SHUTDOWN = 2;

		// returned by get_connection_state
		/// <summary>
		///  No connection is established.
		/// </summary>
		public const short CONNECTION_STATE_DISCONNECTED = 0;

		/// <summary>
		///  A connection to the Brick Daemon or the WIFI/Ethernet Extension is
		///  established.
		/// </summary>
		public const short CONNECTION_STATE_CONNECTED = 1;

		/// <summary>
		///  IP Connection is currently trying to connect.
		/// </summary>
		public const short CONNECTION_STATE_PENDING = 2; // auto-reconnect in process

		internal const int QUEUE_EXIT = 0;
		internal const int QUEUE_META = 1;
		internal const int QUEUE_PACKET = 2;

		internal int nextSequenceNumber = 0; // protected by sequenceNumberLock
		private object sequenceNumberLock = new object();

		private uint nextAuthenticationNonce = 0; // protected by authenticationLock
		private object authenticationLock = new object(); // protects authentication handshake

		internal bool autoReconnectAllowed = false;
		internal bool autoReconnectPending = false;
		internal bool autoReconnect = true;

#if !(WINDOWS_UWP || WINDOWS_UAP)
		private static RNGCryptoServiceProvider randomGenerator = null; // protected by randomGeneratorLock
		private static object randomGeneratorLock = new object();
#endif

		internal BrickDaemon brickd = null;

		string host;
		int port;
		ISocketWrapper socket = null; // protected by socketLock
		internal object socketLock = new object();
		internal object socketWriteLock = new object(); // used to synchronize write access to socket
		long socketID = 0; // protected by socketLock
		Thread receiveThread = null;
		bool receiveFlag = true;
		CallbackContext callback = null;
		internal Dictionary<int, Device> devices = new Dictionary<int, Device>();
		internal object replaceLock = new object(); // used to synchronize replacements in the devices dictionary
		BlockingQueue<bool> waiter = new BlockingQueue<bool>();

		bool disconnectProbeFlag = false;
		BlockingQueue<bool> disconnectProbeQueue = null;
		Thread disconnectProbeThread = null;

		/// <summary>
		/// </summary>
		public event EnumerateEventHandler EnumerateCallback;
		/// <summary>
		/// </summary>
		public delegate void EnumerateEventHandler(IPConnection sender, string uid, string connectedUid,
		                                           char position, short[] hardwareVersion, short[] firmwareVersion,
		                                           int deviceIdentifier, short enumerationType);

		/// <summary>
		/// </summary>
		public event ConnectedEventHandler ConnectedCallback;
		/// <summary>
		/// </summary>
		public delegate void ConnectedEventHandler(IPConnection sender, short connectReason);

		/// <summary>
		/// </summary>
		public event ConnectedEventHandler Connected // for backward compatibility
		{
			add { ConnectedCallback += value; }
			remove { ConnectedCallback -= value; }
		}

		/// <summary>
		/// </summary>
		public event DisconnectedEventHandler DisconnectedCallback;
		/// <summary>
		/// </summary>
		public delegate void DisconnectedEventHandler(IPConnection sender, short disconnectReason);

		/// <summary>
		/// </summary>
		public event DisconnectedEventHandler Disconnected // for backward compatibility
		{
			add { DisconnectedCallback += value; }
			remove { DisconnectedCallback -= value; }
		}

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

		static IPConnection()
		{
			Type[] types = typeof(Device).Assembly.GetTypes();

			foreach (Type type in types)
			{
				if (type.BaseType != typeof(Device) || type == typeof(BrickDaemon))
				{
					continue;
				}

				FieldInfo deviceIdentifierInfo = type.GetField("DEVICE_IDENTIFIER", BindingFlags.Public | BindingFlags.Static);
				int deviceIdentifier = (int)deviceIdentifierInfo.GetValue(null);
				FieldInfo deviceDisplayNameInfo = type.GetField("DEVICE_DISPLAY_NAME", BindingFlags.Public | BindingFlags.Static);
				string deviceDisplayName = (string)deviceDisplayNameInfo.GetValue(null);

				deviceDisplayNames[deviceIdentifier] = deviceDisplayName;
			}
		}

		internal static string GetDeviceDisplayName(int deviceIdentifier)
		{
			string deviceDisplayName;

			if (!deviceDisplayNames.TryGetValue(deviceIdentifier, out deviceDisplayName))
			{
				deviceDisplayName = "Unknown Device [" + deviceIdentifier + "]";
			}

			return deviceDisplayName;
		}

		/// <summary>
		///  Creates an IP Connection object that can be used to enumerate the
		///  available devices. It is also required for the constructor of
		///  Bricks and Bricklets.
		/// </summary>
		public IPConnection()
		{
			brickd = new BrickDaemon("2", this);
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

		// NOTE: assumes that socket is null and socketLock is locked
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

#if WINDOWS_UWP || WINDOWS_UAP
			if (host == "localhost" || host == "127.0.0.1")
			{
				socket = new AppServiceWrapper();
			}
			else
			{
				socket = new SocketWrapper(host, port);
			}
#else
			socket = new SocketWrapper(host, port);
#endif

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

		// NOTE: assumes that socket is not null and socketLock is locked
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

			socket.Close();
			socket = null;

			if (receiveThread != null)
			{
				receiveThread.Join();
				receiveThread = null;
			}
		}

		/// <summary>
		///  Performs an authentication handshake with the connected Brick Daemon or
		///  WIFI/Ethernet Extension. If the handshake succeeds the connection switches
		///  from non-authenticated to authenticated state and communication can
		///  continue as normal. If the handshake fails then the connection gets closed.
		///  Authentication can fail if the wrong secret was used or if authentication
		///  is not enabled at all on the Brick Daemon or the WIFI/Ethernet Extension.
		///
		///  For more information about authentication see
		///  https://www.tinkerforge.com/en/doc/Tutorials/Tutorial_Authentication/Tutorial.html
		/// </summary>
		public void Authenticate(string secret)
		{
			for (int i = 0; i < secret.Length; ++i)
			{
				if (secret[i] > 0x7f)
				{
					throw new ArgumentException("Authentication secret contains non-ASCII characters.");
				}
			}

			lock (authenticationLock)
			{
				if (nextAuthenticationNonce == 0)
				{
#if WINDOWS_UWP || WINDOWS_UAP
					nextAuthenticationNonce = CryptographicBuffer.GenerateRandomNumber();
#else
					lock (randomGeneratorLock)
					{
						if (randomGenerator == null)
						{
							randomGenerator = new RNGCryptoServiceProvider();
						}

						try
						{
							byte[] randomNumber = new byte[4];

							randomGenerator.GetBytes(randomNumber);

							nextAuthenticationNonce = (uint)LEConverter.IntFrom(0, randomNumber);
						}
						catch (CryptographicException)
						{
							ulong milliseconds = (ulong)DateTime.Now.Ticks / (ulong)TimeSpan.TicksPerMillisecond;
							ulong seconds = milliseconds / 1000;
							ulong remainder = milliseconds % 1000;
							ulong pid = (ulong)System.Diagnostics.Process.GetCurrentProcess().Id;

							nextAuthenticationNonce = (uint)((seconds << 26 | seconds >> 6) + remainder + pid); // overflow is intended
						}
					}
#endif
				}

				byte[] serverNonce = brickd.GetAuthenticationNonce();
				byte[] clientNonce = new byte[4];

				LEConverter.To((int)nextAuthenticationNonce++, 0, clientNonce);

				byte[] data = new byte[serverNonce.Length + clientNonce.Length];

				System.Buffer.BlockCopy(serverNonce, 0, data, 0, serverNonce.Length);
				System.Buffer.BlockCopy(clientNonce, 0, data, serverNonce.Length, clientNonce.Length);

#if WINDOWS_UWP || WINDOWS_UAP
				MacAlgorithmProvider hmac = MacAlgorithmProvider.OpenAlgorithm("HMAC_SHA1");
				CryptographicKey key = hmac.CreateKey(Encoding.ASCII.GetBytes(secret).AsBuffer());
				byte[] digest = CryptographicEngine.Sign(key, data.AsBuffer()).ToArray();
#else
				HMACSHA1 hmac = new HMACSHA1(Encoding.ASCII.GetBytes(secret));
				byte[] digest = hmac.ComputeHash(data);
#endif

				brickd.Authenticate(clientNonce, digest);
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

		private void ReceiveLoop(long localSocketID)
		{
			byte[] pendingData = new byte[8192];
			int pendingLength = 0;

			while (receiveFlag)
			{
				int length = 0;

				try
				{
					length = socket.Read(pendingData, pendingLength, pendingData.Length - pendingLength);
				}
				catch (IOException e)
				{
					if (e.InnerException != null && e.InnerException is SocketException)
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
						return;
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
					var handler = ConnectedCallback;
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
								socket.Close();
								socket = null;
							}
						}
					}

					Thread.Sleep(100);

					var disconHandler = DisconnectedCallback;

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
					if (cqo.packet.Length != 34)
					{
						return; // silently ignoring callback with wrong length
					}

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
				Device device;

				if (devices.TryGetValue(uid, out device))
				{
					Device.CallbackWrapper wrapper = device.callbackWrappers[fid];

					if (wrapper != null)
					{
						try
						{
							device.CheckValidity();
						}
						catch (TinkerforgeException)
						{
							return; // silently ignoring callback for invalid device
						}

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
						lock (socketWriteLock)
						{
							socket.Write(request, 0, request.Length);
						}
					}
					catch (IOException e)
					{
						if (e.InnerException != null && e.InnerException is SocketException)
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
			Device device;

			if (!devices.TryGetValue(uid, out device))
			{
				return; // Response from an unknown device, ignoring it
			}

			if (sequenceNumber == 0)
			{
				if (device.callbackWrappers[functionID] != null)
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

		internal void SendRequest(byte[] request)
		{
			lock (socketLock)
			{
				if (GetConnectionState() != CONNECTION_STATE_CONNECTED)
				{
					throw new NotConnectedException();
				}

				try
				{
					lock (socketWriteLock)
					{
						socket.Write(request, 0, request.Length);
					}
				}
				catch (IOException e)
				{
					if (e.InnerException != null && e.InnerException is SocketException)
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
			lock (replaceLock)
			{
				Device replacedDevice;

				if (devices.TryGetValue((int)device.internalUID, out replacedDevice))
				{
					replacedDevice.replaced = true;
				}

				devices[(int)device.internalUID] = device; // TODO: Dictionary might use UID directly as key; FIXME: might use weakref here
			}
		}
	}

	/// <summary>
	///  Base class for all Tinkerforge exceptions.
	/// </summary>
	public class TinkerforgeException : Exception
	{
		/// <summary>
		/// </summary>
		public TinkerforgeException()
		{
		}

		/// <summary>
		/// </summary>
		public TinkerforgeException(string message) : base(message)
		{
		}
	}

	/// <summary>
	///  Used to report timeout errors.
	/// </summary>
	public class TimeoutException : TinkerforgeException
	{
		/// <summary>
		/// </summary>
		public TimeoutException(string message) : base(message)
		{
		}
	}

	/// <summary>
	///  Used to report if <see cref="Tinkerforge.IPConnection.Connect"/> is
	///  called on an already connected IPConnection.
	/// </summary>
	public class AlreadyConnectedException : TinkerforgeException
	{
		/// <summary>
		/// </summary>
		public AlreadyConnectedException(string message) : base(message)
		{
		}
	}

	/// <summary>
	///  Used to report if a method is called on an unconnected IPConnection
	///  that requires a connected IPConnection.
	/// </summary>
	public class NotConnectedException : TinkerforgeException
	{
		/// <summary>
		/// </summary>
		public NotConnectedException()
		{
		}
	}

	/// <summary>
	///  Used to report if a method was called with an invalid parameter.
	/// </summary>
	public class InvalidParameterException : TinkerforgeException
	{
		/// <summary>
		/// </summary>
		public InvalidParameterException(string message) : base(message)
		{
		}
	}

	/// <summary>
	///  Used to report if not supported method was called.
	/// </summary>
	public class NotSupportedException : TinkerforgeException
	{
		/// <summary>
		/// </summary>
		public NotSupportedException(string message) : base(message)
		{
		}
	}

	/// <summary>
	///  Used to report if device responds with an unknown error code.
	/// </summary>
	public class UnknownErrorCodeException : TinkerforgeException
	{
		/// <summary>
		/// </summary>
		public UnknownErrorCodeException(string message) : base(message)
		{
		}
	}

	/// <summary>
	///  Used to report if a stream method call hit an out-of-sync condition.
	/// </summary>
	public class StreamOutOfSyncException : TinkerforgeException
	{
		/// <summary>
		/// </summary>
		public StreamOutOfSyncException(string message) : base(message)
		{
		}
	}

	/// <summary>
	///  Used to report if the API bindings device class does not match the
	///  device identifier.
	/// </summary>
	public class WrongDeviceTypeException : TinkerforgeException
	{
		/// <summary>
		/// </summary>
		public WrongDeviceTypeException(string message) : base(message)
		{
		}
	}

	/// <summary>
	///  Used to report if the device object got replaced by other device
	///  object and does no longer receive responses.
	/// </summary>
	public class DeviceReplacedException : TinkerforgeException
	{
		/// <summary>
		/// </summary>
		public DeviceReplacedException()
		{
		}
	}

	/// <summary>
	///  Used to report if a response does not have the expected length.
	/// </summary>
	public class WrongResponseLengthException : TinkerforgeException
	{
		/// <summary>
		/// </summary>
		public WrongResponseLengthException(string message) : base(message)
		{
		}
	}

	/// <summary>
	/// </summary>
	public struct UID
	{
		private string StringRepresentation;
		private int IntRepresentation;

		/// <summary>
		/// </summary>
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

			if (uidTmp == 0) {
				throw new ArgumentOutOfRangeException("UID '" + uid + "' is empty or maps to zero");
			}

			IntRepresentation = (int)uidTmp;
		}

		/// <summary>
		/// </summary>
		public int ToInt()
		{
			return IntRepresentation;
		}

		/// <summary>
		/// </summary>
		public static explicit operator int(UID uid)
		{
			return uid.ToInt();
		}

		/// <summary>
		/// </summary>
		public override string ToString()
		{
			return StringRepresentation;
		}
	}

	/// <summary>
	///  Base class for all Tinkerforge Brick and Bricklet classes.
	/// </summary>
	public abstract class Device
	{
		internal bool replaced;
		internal int deviceIdentifier;
		internal string deviceDisplayName;
		internal object deviceIdentifierLock = new object();
		internal DeviceIdentifierCheck deviceIdentifierCheck = DeviceIdentifierCheck.PENDING; // protected by deviceIdentifierLock
		internal string wrongDeviceDisplayName = "?"; // protected by deviceIdentifierLock
		internal short[] apiVersion = new short[3];
		internal ResponseExpectedFlag[] responseExpected = new ResponseExpectedFlag[256];
		internal byte expectedResponseFunctionID = 0; // protected by requestLock
		internal byte expectedResponseSequenceNumber = 0; // protected by requestLock
		internal CallbackWrapper[] callbackWrappers = new CallbackWrapper[256];
		internal HighLevelCallback[] highLevelCallbacks = new HighLevelCallback[256];
		internal BlockingQueue<byte[]> responseQueue = new BlockingQueue<byte[]>();
		internal IPConnection ipcon = null;
		internal object requestLock = new object();
		internal UID internalUID;
		internal object streamLock = new object();

		/// <summary>
		/// </summary>
		public string UID
		{
			get
			{
				return internalUID.ToString();
			}
		}

		internal enum DeviceIdentifierCheck
		{
			PENDING = 0,
			MATCH = 1,
			MISMATCH = 2
		}

		internal enum ResponseExpectedFlag
		{
			INVALID_FUNCTION_ID = 0,
			ALWAYS_TRUE = 1, // getter
			TRUE = 2, // setter
			FALSE = 3 // setter, default
		}

		internal delegate void CallbackWrapper(byte[] data);

		/// <summary>
		///  Creates the device object with the unique device ID *uid* and adds
		///  it to the IPConnection *ipcon*.
		/// </summary>
		public Device(string uid, IPConnection ipcon, int deviceIdentifier, string deviceDisplayName)
		{
			internalUID = new UID(uid);
			this.ipcon = ipcon;
			this.deviceIdentifier = deviceIdentifier;
			this.deviceDisplayName = deviceDisplayName;

			for (int i = 0; i < responseExpected.Length; i++)
			{
				responseExpected[i] = ResponseExpectedFlag.INVALID_FUNCTION_ID;
			}
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
		///  too, but can be disabled via the SetResponseExpected function.
		///  For setter functions it is disabled by default and can be enabled.
		///
		///  Enabling the response expected flag for a setter function allows
		///  to detect timeouts and other error conditions calls of this setter
		///  as well. The device will then send a response for this purpose.
		///  If this flag is disabled for a setter function then no response
		///  is sent and errors are silently ignored, because they cannot be
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
		///  always enabled.
		///
		///  Enabling the response expected flag for a setter function allows
		///  to detect timeouts and other error conditions calls of this setter
		///  as well. The device will then send a response for this purpose.
		///  If this flag is disabled for a setter function then no response
		///  is sent and errors are silently ignored, because they cannot be
		///  detected.
		/// </summary>
		public void SetResponseExpected(byte functionId, bool responseExpected)
		{
			ResponseExpectedFlag flag = this.responseExpected[functionId];

			if (flag == ResponseExpectedFlag.INVALID_FUNCTION_ID)
			{
				throw new ArgumentException("Invalid function ID " + functionId);
			}

			if (flag == ResponseExpectedFlag.ALWAYS_TRUE)
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

		/// <summary>
		///  Returns the UID, the UID where the Brick/Bricklet is connected to,
		///  the position, the hardware and firmware version as well as the
		///  device identifier.
		/// </summary>
		public abstract void GetIdentity(out string uid, out string connectedUid, out char position,
		                                 out byte[] hardwareVersion, out byte[] firmwareVersion,
		                                 out int deviceIdentifier);

		internal byte[] CreateRequestPacket(byte length, byte fid)
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

		internal byte[] SendRequest(byte[] request, int expectedResponseLength)
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
						if (expectedResponseLength == 0)
						{
							// setter with response-expected enabled
							expectedResponseLength = 8;
						}

						if (response.Length != expectedResponseLength)
						{
							throw new WrongResponseLengthException("Expected response of " + expectedResponseLength + " byte for function ID " + functionID + ", got " + response.Length + " byte instead");
						}

						break;

					case 1:
						throw new InvalidParameterException("Got invalid parameter for function ID " + functionID);

					case 2:
						throw new NotSupportedException("Function ID " + functionID + " is not supported");

					default:
						throw new UnknownErrorCodeException("Function ID " + functionID + " returned an unknown error");
				}
			}
			else
			{
				ipcon.SendRequest(request);
			}

			return response;
		}

		internal void CheckValidity()
		{
			if (replaced)
			{
				throw new DeviceReplacedException();
			}

			if (deviceIdentifierCheck == DeviceIdentifierCheck.MATCH)
			{
				return;
			}

			lock (deviceIdentifierLock)
			{
				if (deviceIdentifierCheck == DeviceIdentifierCheck.PENDING)
				{
					byte[] request = CreateRequestPacket(8, 255); // GetIdentity
					byte[] response = SendRequest(request, 33);
					int deviceIdentifier = LEConverter.UShortFrom(31, response);

					if (deviceIdentifier == this.deviceIdentifier)
					{
						deviceIdentifierCheck = DeviceIdentifierCheck.MATCH;
					}
					else
					{
						deviceIdentifierCheck = DeviceIdentifierCheck.MISMATCH;
						wrongDeviceDisplayName = IPConnection.GetDeviceDisplayName(deviceIdentifier);
					}
				}

				if (deviceIdentifierCheck == DeviceIdentifierCheck.MISMATCH)
				{
					throw new WrongDeviceTypeException("UID " + UID + " belongs to a " + wrongDeviceDisplayName +
					                                   " instead of the expected " + deviceDisplayName);
				}
			}
		}
	}

	internal class HighLevelCallback
	{
		internal object data = null;
		internal int length = 0;
	}

	internal class BrickDaemon : Device
	{
		public const byte FUNCTION_GET_AUTHENTICATION_NONCE = 1;
		public const byte FUNCTION_AUTHENTICATE = 2;

		public BrickDaemon(string uid, IPConnection ipcon) : base(uid, ipcon, 0, "Brick Daemon")
		{
			apiVersion[0] = 2;
			apiVersion[1] = 0;
			apiVersion[2] = 0;

			responseExpected[FUNCTION_GET_AUTHENTICATION_NONCE] = ResponseExpectedFlag.ALWAYS_TRUE;
			responseExpected[FUNCTION_AUTHENTICATE] = ResponseExpectedFlag.TRUE;

			ipcon.AddDevice(this);
		}

		public byte[] GetAuthenticationNonce()
		{
			byte[] request = CreateRequestPacket(8, FUNCTION_GET_AUTHENTICATION_NONCE);
			byte[] response = SendRequest(request, 12);

			return LEConverter.ByteArrayFrom(8, response, 4);
		}

		public void Authenticate(byte[] clientNonce, byte[] digest)
		{
			byte[] request = CreateRequestPacket(32, FUNCTION_AUTHENTICATE);

			LEConverter.To(clientNonce, 8, 4, request);
			LEConverter.To(digest, 12, 20, request);

			SendRequest(request, 0);
		}

		public override void GetIdentity(out string uid, out string connectedUid, out char position,
		                                 out byte[] hardwareVersion, out byte[] firmwareVersion,
		                                 out int deviceIdentifier)
		{
			uid = "";
			connectedUid = "";
			position = '0';
			hardwareVersion = new byte[0];
			firmwareVersion = new byte[0];
			deviceIdentifier = 0;
		}
	}

	internal class Base58
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

			return -1;
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

				if (column < 0)
				{
					throw new ArgumentOutOfRangeException("UID '" + encoded + "' contains invalid character");
				}

				try
				{
					checked
					{
						value += column * columnMultiplier;
					}
				}
				catch (OverflowException)
				{
					throw new ArgumentOutOfRangeException("UID '" + encoded + "' is too big");
				}

				try
				{
					checked
					{
						columnMultiplier *= 58;
					}
				}
				catch (OverflowException)
				{
					if (i > 0) {
						throw new ArgumentOutOfRangeException("UID '" + encoded + "' is too big");
					}
				}
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
				ret[i] = (array[position + i / 8] & (1 << (i % 8))) != 0;
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
				ret[i] = CharFrom(position + i, array);
			}

			return ret;
		}

		static public short SByteFrom(int position, byte[] array)
		{
			return (short)((array[position] & 0x7F) - (array[position] & 0x80));
		}

		static public short[] SByteArrayFrom(int position, byte[] array, int len)
		{
			short[] ret = new short[len];

			for (int i = 0; i < len; i++)
			{
				ret[i] = SByteFrom(position + i, array);
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
				ret[i] = ByteFrom(position + i, array);
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

	// There is no BlockingQueue in C# version <= 2.0, we make our own
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

	internal interface ISocketWrapper
	{
		void Close();

		int Read(byte[] buffer, int offset, int count);

		void Write(byte[] buffer, int offset, int count);
	}

	internal class SocketWrapper : ISocketWrapper
	{
		private Socket socket = null;
		private NetworkStream stream = null;

		public SocketWrapper(String host, int port)
		{
			socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
			socket.NoDelay = true;

#if WINDOWS_PHONE || WINDOWS_UWP || WINDOWS_UAP
			SocketAsyncEventArgs args = new SocketAsyncEventArgs();
			args.RemoteEndPoint = new DnsEndPoint(host, port);

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

			stream = new NetworkStream(socket);
		}

		public void Close()
		{
			stream.Close();
#if WINDOWS_UWP || WINDOWS_UAP
			stream.Dispose();
#endif

			socket.Shutdown(SocketShutdown.Both);

#if WINDOWS_UWP || WINDOWS_UAP
			socket.Dispose();
#else
			socket.Close();
#endif
		}

		public int Read(byte[] buffer, int offset, int count)
		{
			return stream.Read(buffer, offset, count);
		}

		public void Write(byte[] buffer, int offset, int count)
		{
			stream.Write(buffer, offset, count);
		}
	}

#if WINDOWS_UWP || WINDOWS_UAP
	internal class AppServiceWrapper : ISocketWrapper
	{
		private AppServiceConnection conn = null;

		private object readLock = new object();
		private BlockingQueue<byte[]> receiveQueue = new BlockingQueue<byte[]>();
		private byte[] immediateReadBuffer;
		private int immediateReadOffset;

		private object writeLock = new object();

		public AppServiceWrapper()
		{
			conn = new AppServiceConnection();
			conn.RequestReceived += RequestReceived;
			conn.ServiceClosed += ServiceClosed;
			conn.AppServiceName = "com.tinkerforge.brickd";
			conn.PackageFamilyName = "brickd_3cmbwa9ky1nvw";

			Task<AppServiceConnectionStatus> task = conn.OpenAsync().AsTask();

			task.Wait();

			AppServiceConnectionStatus status = task.Result;

			if (status != AppServiceConnectionStatus.Success)
			{
				throw new IOException(string.Format("Could not connect: {0}", status));
			}

			// FIXME: wait for initial handshake message
		}

		public void Close()
		{
			// make Read() report an socket error
			byte[] buffer = new byte[0];
			receiveQueue.Enqueue(buffer);

			conn.Dispose();
		}

		public int Read(byte[] buffer, int offset, int count)
		{
			int readLength;

			lock (readLock)
			{
				if (immediateReadBuffer == null)
				{
					receiveQueue.TryDequeue(out immediateReadBuffer);

					if (immediateReadBuffer.Length == 0)
					{
						throw new IOException("Read failure", new SocketException(10004 /* WSAEINTR */));
					}
				}

				readLength = Math.Min(count, immediateReadBuffer.Length - immediateReadOffset);
				Array.Copy(immediateReadBuffer, immediateReadOffset, buffer, offset, readLength);
				immediateReadOffset += readLength;

				if (immediateReadOffset == immediateReadBuffer.Length)
				{
					immediateReadBuffer = null;
					immediateReadOffset = 0;
				}
			}

			return readLength;
		}

		public void Write(byte[] buffer, int offset, int count)
		{
			ValueSet request = new ValueSet();
			byte[] data = new byte[count];

			Array.Copy(buffer, offset, data, 0, count);
			request.Add("data", data);

			lock (writeLock)
			{
				Task<AppServiceResponse> task = conn.SendMessageAsync(request).AsTask();

				task.Wait(); // FIXME: look at response status?
			}
		}

		private void RequestReceived(AppServiceConnection sender, AppServiceRequestReceivedEventArgs args)
		{
			AppServiceDeferral deferral = args.GetDeferral();

			try
			{
				byte[] data = (byte[])args.Request.Message["data"];
				byte[] buffer = new byte[data.Length];
				Array.Copy(data, buffer, data.Length);

				receiveQueue.Enqueue(buffer);

				Task<AppServiceResponseStatus> task = args.Request.SendResponseAsync(new ValueSet()).AsTask();

				task.Wait(); // FIXME: look at response status?
			}
			finally
			{
				deferral.Complete();
			}
		}

		private void ServiceClosed(AppServiceConnection sender, AppServiceClosedEventArgs args)
		{
			// FIXME: look at args.Status?

			// make Read() report an socket error
			byte[] buffer = new byte[0];
			receiveQueue.Enqueue(buffer);
		}
	}
#endif

#if WINDOWS_PHONE || WINDOWS_UWP || WINDOWS_UAP
	internal class NetworkStream : Stream
	{
		private Socket socket;

		private object readLock = new object();
		private BlockingQueue<byte[]> receiveQueue = new BlockingQueue<byte[]>();
		private byte[] immediateReadBuffer;
		private int immediateReadOffset;

		private object writeLock = new object();
		private AutoResetEvent writeCompleteEvent = new AutoResetEvent(false);

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
			// stream is always flushed
		}

		public NetworkStream(Socket socket)
		{
			this.socket = socket;

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
				receiveQueue.Enqueue(buffer);

				return;
			}
			else if (e.SocketError != SocketError.Success)
			{
				// TODO: error handling
			}

			switch (e.LastOperation)
			{
				case SocketAsyncOperation.Receive:
					if (e.BytesTransferred == 0)
					{
						break; // TODO: error handling
					}

					byte[] receiveBuffer = new byte[e.BytesTransferred];
					Array.Copy(e.Buffer, receiveBuffer, e.BytesTransferred);
					receiveQueue.Enqueue(receiveBuffer);

					if (!socket.ReceiveAsync(e))
					{
						// TODO: error handling
					}

					break;

				case SocketAsyncOperation.Send:
					writeCompleteEvent.Set();
					break;

				default:
					break; // TODO: error handling
			}
		}

#if WINDOWS_PHONE
		public override void Close()
		{
			base.Close();
#else
		public void Close()
		{
#endif
			// make Read() report an socket error
			byte[] buffer = new byte[0];
			receiveQueue.Enqueue(buffer);
		}

		public override int Read(byte[] buffer, int offset, int count)
		{
			int readLength;

			lock (readLock)
			{
				if (immediateReadBuffer == null)
				{
					receiveQueue.TryDequeue(out immediateReadBuffer);

					if (immediateReadBuffer.Length == 0)
					{
						throw new IOException("Read failure", new SocketException(10004 /* WSAEINTR */));
					}
				}

				readLength = Math.Min(count, immediateReadBuffer.Length - immediateReadOffset);
				Array.Copy(immediateReadBuffer, immediateReadOffset, buffer, offset, readLength);
				immediateReadOffset += readLength;

				if (immediateReadOffset == immediateReadBuffer.Length)
				{
					immediateReadBuffer = null;
					immediateReadOffset = 0;
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

				writeCompleteEvent.WaitOne();
			}
		}

		public override long Seek(long offset, SeekOrigin origin)
		{
			throw new System.NotSupportedException();
		}

		public override void SetLength(long value)
		{
			throw new System.NotSupportedException();
		}

		public override long Position
		{
			get
			{
				throw new System.NotSupportedException();
			}
			set
			{
				throw new System.NotSupportedException();
			}
		}

		public override long Length
		{
			get { throw new System.NotSupportedException(); }
		}
	}
#endif

#if WINDOWS_UWP || WINDOWS_UAP
	internal delegate void ThreadStart();

	internal class Thread
	{
		internal bool IsBackground;
		internal string Name;
		private ThreadStart function;
		private Task task;
		private static ThreadLocal<Thread> current = new ThreadLocal<Thread>();

		public Thread(ThreadStart function)
		{
			this.function = function;
		}

		public static Thread CurrentThread { get { return current.Value; } }

		internal static void Sleep(int millisecondsTimeout)
		{
			Task.Delay(millisecondsTimeout).Wait();
		}

		internal void Join()
		{
			task.Wait();
		}

		internal void Start()
		{
			task = new Task(() =>
			{
				current.Value = this;
				function.Invoke();
			});

			task.Start();
		}
	}
#endif
}
