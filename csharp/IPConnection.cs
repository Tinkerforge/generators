/*
 * Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
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

[assembly:CLSCompliant(true)] 
namespace Tinkerforge
{
	public class IPConnection
	{
		public int responseTimeout = 2500;

		const byte BROADCAST_ADDRESS = 0;

		public const byte FUNCTION_ENUMERATE = 254;
		public const byte FUNCTION_ADC_CALIBRATE = 251;
		public const byte FUNCTION_GET_ADC_CALIBRATION = 250;

		public const byte CALLBACK_ENUMERATE = 253;

		internal const int CALLBACK_CONNECTED = 0;
		internal const int CALLBACK_DISCONNECTED = 1;
		internal const int CALLBACK_AUTHENTICATION_ERROR = 2;

		private const long BROADCAST_UID = (long)0;

		// enumeration_type parameter to the enumerate callback
		public const short ENUMERATION_TYPE_AVAILABLE = 0;
		public const short ENUMERATION_TYPE_CONNECTED = 1;
		public const short ENUMERATION_TYPE_DISCONNECTED = 2;

		// connect_reason parameter to the connected callback
		internal const int CONNECT_REASON_REQUEST = 0;
		internal const int CONNECT_REASON_AUTO_RECONNECT = 1;

		// disconnect_reason parameter to the disconnected callback
		internal const int DISCONNECT_REASON_REQUEST = 0;
		internal const int DISCONNECT_REASON_ERROR = 1;
		internal const int DISCONNECT_REASON_SHUTDOWN = 2;

		// returned by get_connection_state
		internal const int CONNECTION_STATE_DISCONNECTED = 0;
		internal const int CONNECTION_STATE_CONNECTED = 1;
		internal const int CONNECTION_STATE_PENDING = 2; // auto-reconnect in process

		internal const int QUEUE_EXIT = 0;
	    internal const int QUEUE_META = 1;
    	internal const int QUEUE_PACKET = 2;

		internal int nextSequenceMumber = 1;

		internal readonly object socketLock = new object();
		private object writeLock = new object();

		internal bool autoReconnectAllowed = false;
		internal bool autoReconnectPending = false;
		internal bool autoReconnect = true;

		string host;
		int port;
		Socket socket;
		NetworkStream socketStream;
		BinaryWriter socketWriter;
		BinaryReader socketReader;
		Thread receiveThread;
		Thread callbackThread;
		bool receiveFlag = true;
		bool callbackThreadFlag = true;
		internal Dictionary<long, Device> devices = new Dictionary<long, Device>();
		BlockingQueue<CallbackQueueObject> callbackQueue = null;

		public event EnumerateEventHandler EnumerateCallback;
		public delegate void EnumerateEventHandler(object sender, string UID, string connectedUID, char position, short[] hardwareVersion, short[] firmwareVersion, int deviceIdentifier, short enumerationType);
		public event ConnectedEventHandler Connected;
		public delegate void ConnectedEventHandler(object sender, int reason);
		public event DisconnectedEventHandler Disconnected;
		public delegate void DisconnectedEventHandler(object sender, int reason);

		public class CallbackQueueObject 
		{
			public int kind; 
			public byte[] data; 
			public CallbackQueueObject(int kind, byte[] data) 
			{ 
				this.kind = kind; 
				this.data = data; 
			} 
		}

		/// <summary>
		///  Creates an IP connection to the Brick Daemon with the given *host*
		///  and *port*. With the IP connection itself it is possible to enumerate the
		///  available devices. Other then that it is only used to add Bricks and
		///  Bricklets to the connection.
		///
		///  The constructor throws an System.Net.Sockets.SocketException if there
		///  is no Brick Daemon listening at the given host and port.
		/// </summary>
		public IPConnection() 
		{
		}

		public void Connect(string host, int port)
		{
			lock(socketLock)
			{
				this.host = host;
				this.port = port;

				ConnectUnlocked(false);
			}
		}

		void ConnectUnlocked(bool isAutoReconnect)
		{
			if(callbackThread == null)
			{
				callbackThread = new Thread(this.CallbackLoop);
				callbackQueue = new BlockingQueue<CallbackQueueObject>();
				callbackThread.IsBackground = true;
				callbackThread.Name = "Callback-Processor";
				callbackThread.Start();
			}

			socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
			ConnectSocket(host, port);

			socketStream = new NetworkStream(socket);
			socketWriter = new BinaryWriter(socketStream);
			socketReader = new BinaryReader(socketStream);

			if(receiveThread == null)
			{
				receiveThread = new Thread(this.ReceiveLoop);
				receiveThread.IsBackground = true;
				receiveThread.Name = "Brickd-Receiver";
				receiveThread.Start();
			}

			int connectReason = IPConnection.CONNECT_REASON_REQUEST;
			if(isAutoReconnect) 
			{
				connectReason = CONNECT_REASON_AUTO_RECONNECT;
			}
			
			autoReconnectAllowed = false;
			autoReconnectPending = false;

			byte[] data_ = new byte[8];
			LEConverter.To((int)CALLBACK_CONNECTED, 0, data_);
			LEConverter.To((int)connectReason, 4, data_);

			callbackQueue.Enqueue(new CallbackQueueObject(QUEUE_META, data_));
		}

		public void Disconnect() 
		{
			Thread callbackThreadTmp = null;
			BlockingQueue<CallbackQueueObject> callbackQueueTmp = null;

			lock(socketLock) 
			{
				autoReconnectAllowed = false;

				if(autoReconnectPending) 
				{
					autoReconnectPending = false;
				} else 
				{
					if(socket == null) 
					{
						// FIXME: throw not-connected exception
						return;
					}

					receiveFlag = false;

					if(socket != null) 
					{
						socket.Close();
						socket = null;
					}

					if(receiveThread != null) 
					{
						receiveThread.Join();
					}

					receiveThread = null;
				}

				callbackThreadTmp = callbackThread;
				callbackQueueTmp = callbackQueue;

				callbackThread = null;
				callbackQueue = null;
			}

			byte[] data_ = new byte[8];
			LEConverter.To((int)CALLBACK_DISCONNECTED, 0, data_);
			LEConverter.To((int)DISCONNECT_REASON_REQUEST, 4, data_);

			callbackQueueTmp.Enqueue(new CallbackQueueObject(QUEUE_META, data_));
			callbackQueueTmp.Enqueue(new CallbackQueueObject(QUEUE_EXIT, null));

			if(Thread.CurrentThread != callbackThreadTmp) 
			{
				callbackThreadTmp.Join();
			}
		}

		public byte GetConnectionState() 
		{
			if(socket != null) 
			{
				return CONNECTION_STATE_CONNECTED;
			}

			if(autoReconnectPending) 
			{
				return IPConnection.CONNECTION_STATE_PENDING;
			}

			return IPConnection.CONNECTION_STATE_DISCONNECTED;
		}

		public void SetAutoReconnect(bool autoReconnect) 
		{
			this.autoReconnect = autoReconnect;

			if(!autoReconnect) 
			{
				autoReconnectAllowed = false;
			}
		}

		public bool GetAutoReconnect() 
		{
			return autoReconnect;
		}

		public void SetTimeout(int timeout) 
		{
			if(timeout < 0) 
			{
				throw new ArgumentOutOfRangeException("Timeout cannot be negative");
			}

			responseTimeout = timeout;
		}

		public int GetTimeout() 
		{
			return responseTimeout;
		}

		
		internal int GetNextSequenceNumber()
		{
			int sequenceNumber = nextSequenceMumber;
			nextSequenceMumber = (nextSequenceMumber + 1) % 15;
			return sequenceNumber + 1;
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
            bool connectPending = Socket.ConnectAsync(args);

            if(connectPending)
            {
                connectedEvent.WaitOne();
            }
            if(!connectPending || args.SocketError != SocketError.Success)
            {
                throw new IOException(string.Format("Could not connect: {0}", args.SocketError));
            }
#else
            socket.Connect(host, port);
#endif
        }

		private bool Reconnect()
		{
			while(receiveFlag)
			{
				try 
				{
					socketStream.Close();
					socket.Close();

					socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
					ConnectSocket(host, port);

					socketStream = new NetworkStream(socket);
					socketWriter = new BinaryWriter(socketStream);
					socketReader = new BinaryReader(socketStream);
				} 
				catch 
				{
					Thread.Sleep(500);
					continue;
				}

				return true;
			}

			return false;
		}

		private void ReceiveLoop()
		{
			byte[] pendingData = new byte[8192];
			int pendingLength = 0;

			while(receiveFlag)
			{
				int length = 0;

				try
				{
					length = socketReader.Read(pendingData, pendingLength,
					                           pendingData.Length - pendingLength);
				}
				catch(IOException e)
				{
					if(e.InnerException != null &&
					   e.InnerException is SocketException) 
					{
						byte[] data_ = new byte[8];
						LEConverter.To((int)CALLBACK_DISCONNECTED, 0, data_);
						LEConverter.To((int)DISCONNECT_REASON_ERROR, 4, data_);

						callbackQueue.Enqueue(new CallbackQueueObject(QUEUE_META, data_));
					}
					else
					{
						receiveFlag = false;
					}

					return;
				}
				catch(ObjectDisposedException)
				{
					receiveFlag = false;
					return;
				}

				if(length == 0)
				{
					if(receiveFlag)
					{
						autoReconnectAllowed = true;
						receiveFlag = false;

						byte[] data_ = new byte[8];
						LEConverter.To((int)CALLBACK_DISCONNECTED, 0, data_);
						LEConverter.To((int)DISCONNECT_REASON_SHUTDOWN, 4, data_);

						callbackQueue.Enqueue(new CallbackQueueObject(QUEUE_META, data_));
					}
				}

				pendingLength += length;

				while(true)
				{
					if(pendingLength < 8)
					{
						// Wait for complete header
						break;
					}

					length = GetLengthFromData(pendingData);

					if(pendingLength < length)
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

		private void CallbackLoop()
		{
			while(callbackThreadFlag)
			{
				CallbackQueueObject cqo;
				if(!callbackQueue.TryDequeue(out cqo, Timeout.Infinite))
				{
					continue;
				}

				if(cqo == null)
				{
					continue;
				}

				byte fid = GetFunctionIdFromData(cqo.data);
				long uid = GetUIDFromData(cqo.data);

				switch(cqo.kind)
				{
					case IPConnection.QUEUE_EXIT:
						return;

					case IPConnection.QUEUE_META:
						int mid = LEConverter.IntFrom(0, cqo.data);
						int parameter = LEConverter.IntFrom(4, cqo.data);
				
						switch(mid)
						{
							case IPConnection.CALLBACK_CONNECTED:
								var handler = Connected;
								if(handler != null)
								{
									handler(this, parameter);
								}
								break;

							case IPConnection.CALLBACK_DISCONNECTED:
								lock(socketLock)
								{
									if(socket != null)
									{
										socket.Close();
									}
								}

								Thread.Sleep(100);

								var disconHandler = Disconnected;
								if(disconHandler != null)
								{
									disconHandler(this, parameter);
								}

								if(parameter != DISCONNECT_REASON_REQUEST && autoReconnect && autoReconnectAllowed)
								{
									autoReconnectPending = true;
									bool retry = true;
									while(retry)
									{
										retry = false;
										lock(socketLock)
										{
											if(autoReconnectAllowed && socket == null)
											{
												try
												{
													ConnectUnlocked(true);
												}
												catch(Exception)
												{
													retry = true;
												}
											}
											else
											{
												autoReconnectPending = false;
											}
										}

										if(retry)
										{
											Thread.Sleep(100);
										}
									}
								}

								break;
						}
						break;


					case IPConnection.QUEUE_PACKET:
						if (!callbackThreadFlag) {
							return;
						}

						if(fid == CALLBACK_ENUMERATE)
						{
							var enumHandler = EnumerateCallback;
							if(enumHandler != null)
							{
								string UID = LEConverter.StringFrom(8, cqo.data, 8);
								string connectedUID = LEConverter.StringFrom(16, cqo.data, 8);
								char position = (char)LEConverter.CharFrom(24, cqo.data);
								short[] hardwareVersion = new short[3];
								hardwareVersion[0] = LEConverter.ByteFrom(25, cqo.data);
								hardwareVersion[1] = LEConverter.ByteFrom(26, cqo.data);
								hardwareVersion[2] = LEConverter.ByteFrom(27, cqo.data);
								short[] firmwareVersion = new short[3];
								firmwareVersion[0] = LEConverter.ByteFrom(28, cqo.data);
								firmwareVersion[1] = LEConverter.ByteFrom(29, cqo.data);
								firmwareVersion[2] = LEConverter.ByteFrom(30, cqo.data);
								int deviceIdentifier = LEConverter.ShortFrom(31, cqo.data);
								short enumerationType = LEConverter.ByteFrom(33, cqo.data);

								enumHandler(this, UID, connectedUID, position, hardwareVersion, firmwareVersion, deviceIdentifier, enumerationType);
							}
						}
						else
						{
							if(devices.ContainsKey(uid))
							{
								Device device = devices[uid];
								Device.MessageCallback callback = device.messageCallbacks[fid];
								if(callback != null) 
								{
									callback(cqo.data);
								}
							}
						}
						break;
				}
			}
		}


		private static byte GetFunctionIdFromData(byte[] data)
		{
			return data[5];
		}

		private static int GetLengthFromData(byte[] data)
		{
			return data[4];
		}

		internal static long GetUIDFromData(byte[] data)
		{
			return (long)(((long)data[0]) & 0xFF) | (long)((((long)data[1]) & 0xFF) << 8) | (long)((((long)data[2]) & 0xFF) << 16) | (long)((((long)data[3]) & 0xFF) << 24);
		}

		private static byte GetSequenceNumberFromData(byte[] data) {
			return (byte)((((int)data[6]) >> 4) & 0x0F);
		}

		internal static byte GetErrorCodeFromData(byte[] data) {
			return (byte)(((int)(data[7] >> 6)) & 0x03);
		}

		private void HandleResponse(byte[] packet)
		{
			byte functionID = GetFunctionIdFromData(packet);

			if(functionID == CALLBACK_ENUMERATE)
			{
				HandleEnumerate(packet);
				return;
			}

			long uid = GetUIDFromData(packet);

			if(!devices.ContainsKey(uid))
			{
				// Response from an unknown device, ignoring it
				return;
			}

			Device device = devices[uid];

			byte sequenceNumber = GetSequenceNumberFromData(packet);

			if(functionID == device.expectedResponseFunctionID && sequenceNumber == device.expectedResponseSequenceNumber)
			{
				device.responseQueue.Enqueue(packet);
				return;
			}

			Device.MessageCallback callback = device.messageCallbacks[functionID];
			if(callback != null)
			{
				callbackQueue.Enqueue(new CallbackQueueObject(QUEUE_PACKET, packet));
			}

			// Response seems to be OK, but can't be handled, most likely
			// a callback without registered function
		}

		private void HandleEnumerate(byte[] packet)
		{
			callbackQueue.Enqueue(new CallbackQueueObject(QUEUE_PACKET, packet));
		}

		public void Write(byte[] data)
		{
			lock(writeLock)
			{
				socketWriter.Write(data, 0, data.Length);
			}
		}

		public void Enumerate() 
		{
			byte[] data_ = new byte[8];
			LEConverter.To((byte)0, 0, data_);
			LEConverter.To((byte)8, 4, data_);
			LEConverter.To(CALLBACK_ENUMERATE, 5, data_);
			LEConverter.To((byte)((GetNextSequenceNumber() << 4)), 6, data_);
			LEConverter.To((byte)0, 7, data_);
            Write(data_);
		}
	}

	public class TimeoutException : Exception
	{
		public TimeoutException(string message) : base(message)
		{
		}
	}

	public abstract class Device
	{
		internal byte stackID = 0;
		internal String expectedName;
		internal String name;
		internal byte[] firmwareVersion = new byte[3];
		internal short[] bindingVersion = new short[3];
		internal ResponseExpectedFlag[] responseExpected = new ResponseExpectedFlag[256];
		internal long uid = 0;
		internal byte expectedResponseFunctionID = 0;
		internal byte expectedResponseSequenceNumber = 0;
		internal MessageCallback[] messageCallbacks = new MessageCallback[256];
		internal BlockingQueue<byte[]> responseQueue = new BlockingQueue<byte[]>();
		internal IPConnection ipcon = null;

		internal enum ResponseExpectedFlag 
		{
			INVALID_FUNCTION_ID = 0,
			ALWAYS_TRUE = 1,
			ALWAYS_FALSE = 2,
			TRUE = 3,
			FALSE = 4
		}

		private object writeLock = new object();

		internal delegate void MessageCallback(byte[] data);

		public Device(string uid, IPConnection ipcon) 
		{
			long uidTmp = Base58.Decode(uid);
			if(uidTmp > 0xFFFFFFFFL) 
			{
				// convert from 64bit to 32bit
				long value1 = uidTmp & 0xFFFFFFFFL;
				long value2 = (uidTmp >> 32) & 0xFFFFFFFFL;

				uidTmp  = (value1 & 0x3F000000L) << 2;
				uidTmp |= (value1 & 0x000F0000L) << 6;
				uidTmp |= (value1 & 0x0000003FL) << 16;
				uidTmp |= (value2 & 0x0F000000L) >> 12;
				uidTmp |= (value2 & 0x00000FFFL);
			}

			this.uid = uidTmp;
			this.ipcon = ipcon;


			for(int i = 0; i < responseExpected.Length; i++) 
			{
				responseExpected[i] = ResponseExpectedFlag.INVALID_FUNCTION_ID;
			}

			responseExpected[IPConnection.FUNCTION_ENUMERATE]            = ResponseExpectedFlag.FALSE;
			responseExpected[IPConnection.FUNCTION_ADC_CALIBRATE]        = ResponseExpectedFlag.FALSE;
			responseExpected[IPConnection.FUNCTION_GET_ADC_CALIBRATION]  = ResponseExpectedFlag.ALWAYS_TRUE;
			responseExpected[IPConnection.CALLBACK_ENUMERATE]            = ResponseExpectedFlag.ALWAYS_FALSE;
			responseExpected[IPConnection.CALLBACK_CONNECTED]            = ResponseExpectedFlag.ALWAYS_FALSE;
			responseExpected[IPConnection.CALLBACK_DISCONNECTED]         = ResponseExpectedFlag.ALWAYS_FALSE;
			responseExpected[IPConnection.CALLBACK_AUTHENTICATION_ERROR] = ResponseExpectedFlag.ALWAYS_FALSE;

			ipcon.devices[this.uid] = this;
		}

		/// <summary>
		///  Returns the name (including the hardware version), the firmware version
		///  and the binding version of the device. The firmware and binding versions are
		///  given in arrays of size 3 with the syntax [major, minor, revision].
		/// </summary>
		public short[] GetAPIVersion()
		{
			return bindingVersion;
		}

		public void SetResponseExpected(int functionId, bool responseExpected) 
		{
			if(this.responseExpected[functionId] == ResponseExpectedFlag.INVALID_FUNCTION_ID ||
			   functionId >= this.responseExpected.Length) 
			{
				throw new ArgumentOutOfRangeException("Invalid function ID " + functionId);
			}

			if(this.responseExpected[functionId] == ResponseExpectedFlag.ALWAYS_TRUE ||
			   this.responseExpected[functionId] == ResponseExpectedFlag.ALWAYS_FALSE) 
			{
				throw new ArgumentOutOfRangeException("Response Expected flag cannot be changed for function ID " + functionId);
			}

			if(responseExpected)
			{
				this.responseExpected[functionId] = ResponseExpectedFlag.TRUE;
			} else
			{
				this.responseExpected[functionId] = ResponseExpectedFlag.FALSE;
			}
		}

		public bool GetResponseExpected(byte functionId)
		{
			if(this.responseExpected[functionId] != ResponseExpectedFlag.INVALID_FUNCTION_ID &&
			   functionId < this.responseExpected.Length)
			{
				return this.responseExpected[functionId] == ResponseExpectedFlag.ALWAYS_TRUE || 
					   this.responseExpected[functionId] == ResponseExpectedFlag.TRUE;
			}
				
			throw new ArgumentOutOfRangeException("Invalid function ID " + functionId);
		}

		public void SetResponseExpectedAll(bool responseExpected)
		{
			ResponseExpectedFlag flag = ResponseExpectedFlag.TRUE;
			if(responseExpected)
			{
				flag = ResponseExpectedFlag.FALSE;
			}

			for(int i = 0; i < this.responseExpected.Length; i++)
			{
				if(this.responseExpected[i] != ResponseExpectedFlag.INVALID_FUNCTION_ID &&
				   this.responseExpected[i] != ResponseExpectedFlag.ALWAYS_TRUE &&
				   this.responseExpected[i] != ResponseExpectedFlag.ALWAYS_FALSE) {
					this.responseExpected[i] = flag;
				}
			}
		}


		protected byte[] MakePacketHeader(byte length, byte fid)
		{
			byte[] packet = new byte[length];
			LEConverter.To((long)this.uid, 0, packet);
			LEConverter.To((byte)length, 4, packet);
			LEConverter.To((byte)fid, 5, packet);
			if(responseExpected[fid] == ResponseExpectedFlag.ALWAYS_TRUE || responseExpected[fid] == ResponseExpectedFlag.TRUE) 
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

		protected void SendRequestNoResponse(byte[] request)
		{
			lock (writeLock)
			{
				ipcon.Write(request);
			}
		}

		protected void SendRequestExpectResponse(byte[] request, byte functionID, out byte[] response)
		{
			lock (writeLock)
			{
				expectedResponseFunctionID = functionID;
				expectedResponseSequenceNumber = (byte)((request[6] >> 4) & 0xF);

				ipcon.Write(request);

				if (!responseQueue.TryDequeue(out response, ipcon.responseTimeout))
				{
					expectedResponseFunctionID = 0;
					throw new TimeoutException("Did not receive response in time");
				}

				expectedResponseFunctionID = 0;
				expectedResponseSequenceNumber = 0;

				byte errorCode = IPConnection.GetErrorCodeFromData(response);
				switch(errorCode)
				{
					case 0:
						break;
					case 1:
						throw new NotSupportedException("Got invalid parameter for function " + functionID);
					case 2:
						throw new NotSupportedException("Function " + functionID + " is not supported");
					default:
						throw new NotSupportedException("Function " + functionID + " returned an unknown error");
				}
			}
		}
	}

	public class Base58 {
		private const string BASE58 = "123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ";

		public static int IndexOf(char c, string s)
		{
			for(int i = 0; i < s.Length; i++) 
			{
				if(s[i] == c) 
				{
					return i;
				}
			}

			return 0;
		}

		public static string Encode(long value) 
		{
			string encoded = "";
			while(value >= 58) 
			{
				long div = value/58;
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
			for(int i = encoded.Length - 1; i >= 0; i--) 
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
			for(int i = 0; i < Math.Min(len, data.Length); i++)
			{
				array[position + i] = (byte)data[i];
			}

			for(int i = Math.Min(len, data.Length); i < len; i++)
			{
				array[position + i] = 0;
			}
		}

		static public void To(long data, int position, byte[] array)
		{
			array[position + 0] = (byte)data;
			array[position + 1] = (byte)(((ulong)data >> 8) & 0xFF);
			array[position + 2] = (byte)(((ulong)data >> 16) & 0xFF);
			array[position + 3] = (byte)(((ulong)data >> 24) & 0xFF);
			array[position + 4] = (byte)(((ulong)data >> 32) & 0xFF);
			array[position + 5] = (byte)(((ulong)data >> 40) & 0xFF);
			array[position + 6] = (byte)(((ulong)data >> 48) & 0xFF);
			array[position + 7] = (byte)(((ulong)data >> 56) & 0xFF);
		}

		static public void To(long[] data, int position, int len, byte[] array)
		{
			for(int i = 0; i < len; i++)
			{
				To(data[i], position + i, array);
			}
		}

		static public void To(int data, int position, byte[] array)
		{
			array[position + 0] = (byte)data;
			array[position + 1] = (byte)(((uint)data >> 8) & 0xFF);
			array[position + 2] = (byte)(((uint)data >> 16) & 0xFF);
			array[position + 3] = (byte)(((uint)data >> 24) & 0xFF);
		}

		static public void To(int[] data, int position, int len, byte[] array)
		{
			for(int i = 0; i < len; i++)
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
			for(int i = 0; i < len; i++)
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
			for(int i = 0; i < len; i++)
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
			for(int i = 0; i < len; i++)
			{
				To(data[i], position + i, array);
			}
		}

		static public void To(bool data, int position, byte[] array)
		{
			if(data)
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
			for(int i = 0; i < len; i++)
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

			for(int i = 0; i < len; i++) 
			{
				ret[i] = BoolFrom(position + i*1, array);
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

			for(int i = 0; i < len; i++) 
			{
				ret[i] = CharFrom(position + i*1, array);
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

			for(int i = 0; i < len; i++) 
			{
				ret[i] = SByteFrom(position + i*1, array);
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

			for(int i = 0; i < len; i++) 
			{
				ret[i] = ByteFrom(position + i*1, array);
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

			for(int i = 0; i < len; i++) 
			{
				ret[i] = ShortFrom(position + i*2, array);
			}

			return ret;
		}

		static public int UShortFrom(int position, byte[] array)
		{
			return (int)((int)array[position + 0] << 0 | 
					     (int)array[position + 1] << 8 );
		}

		static public int[] UShortArrayFrom(int position, byte[] array, int len) 
		{
			int[] ret = new int[len];

			for(int i = 0; i < len; i++) 
			{
				ret[i] = UShortFrom(position + i*2, array);
			}

			return ret;
		}

		static public int IntFrom(int position, byte[] array) 
		{
			return (int)((int)array[position + 0] << 0 | 
					     (int)array[position + 1] << 8 |
					     (int)array[position + 2] << 16 |
					     (int)array[position + 3] << 24);
		}

		static public int[] IntArrayFrom(int position, byte[] array, int len) 
		{
			int[] ret = new int[len];

			for(int i = 0; i < len; i++) 
			{
				ret[i] = IntFrom(position + i*4, array);
			}

			return ret;
		}

		static public long UIntFrom(int position, byte[] array) 
		{
			return (long)((long)array[position + 0] << 0 | 
					      (long)array[position + 1] << 8 |
					      (long)array[position + 2] << 16 |
					      (long)array[position + 3] << 24);
		}

		static public long[] UIntArrayFrom(int position, byte[] array, int len) 
		{
			long[] ret = new long[len];

			for(int i = 0; i < len; i++) 
			{
				ret[i] = UIntFrom(position + i*4, array);
			}

			return ret;
		}

		static public long LongFrom(int position, byte[] array) 
		{
			return (long)((long)array[position + 0] << 0 | 
					      (long)array[position + 1] << 8 |
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

			for(int i = 0; i < len; i++) 
			{
				ret[i] = LongFrom(position + i*8, array);
			}

			return ret;
		}

		static public long ULongFrom(int position, byte[] array) 
		{
			return (long)((long)array[position + 0] << 0 | 
					      (long)array[position + 1] << 8 |
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

			for(int i = 0; i < len; i++) 
			{
				ret[i] = ULongFrom(position + i*8, array);
			}

			return ret;
		}

		static public float FloatFrom(int position, byte[] array) 
		{
			// We need Little Endian 
			if(BitConverter.IsLittleEndian)
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

			for(int i = 0; i < len; i++) 
			{
				ret[i] = FloatFrom(position + i*4, array);
			}

			return ret;
		}

		static public string StringFrom(int position, byte[] array, int len) 
		{
			StringBuilder sb = new StringBuilder(len);
			for(int i = position; i < position + len; i++) 
			{
				if(array[i] == 0)
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
				lock(queue)
				{
					return queue.Count;
				}
			}
		}

		public BlockingQueue()
		{
			lock(queue)
			{
				closing = false;
				Monitor.PulseAll(queue);
			}
		}

		public bool Enqueue(T item)
		{
			lock (queue)
			{
				if(closing || null == item)
				{
					return false;
				}

				queue.Enqueue(item);

				if(queue.Count == 1)
				{
					// wake up any blocked dequeue
					Monitor.PulseAll(queue);
				}

				return true;
			}
		}

		public void Close()
		{
			lock(queue)
			{
				if(!closing)
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
			lock(queue)
			{
				while(queue.Count == 0)
				{
					if(closing || 
					   (timeout < Timeout.Infinite) || 
					   !Monitor.Wait(queue, timeout))
					{
						value = default (T);
						return false;
					}
				}

				value = (T)queue.Dequeue();
				return true;
			}
		}

		public void Clear()
		{
			lock(queue)
			{
				queue.Clear();
				Monitor.Pulse(queue);
			}
		}
	}
#if WINDOWS_PHONE
    class NetworkStream : Stream
    {
        private Socket socket;

        private BlockingQueue ReceiveQueue = new BlockingQueue();
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
            if (e.SocketError != SocketError.Success)
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

        public override int Read(byte[] buffer, int offset, int count)
        {
            int readLength;
            lock (readLock)
            {
                if (ImmediateReadBuffer == null)
                {
                    ReceiveQueue.TryDequeue(out ImmediateReadBuffer);
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
