/*
 * Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
 * Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>
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

namespace Tinkerforge
{
	public class IPConnection
	{
		internal const int RESPONSE_TIMEOUT = 2500;

		const byte BROADCAST_ADDRESS = 0;

		const byte FUNCTION_GET_STACK_ID = 255;
		const byte FUNCTION_ENUMERATE = 254;
		const byte FUNCTION_ENUMERATE_CALLBACK = 253;

		string host;
		int port;
		Socket socket;
		NetworkStream socketStream;
		Thread receiveThread;
		Thread callbackThread;
		bool receiveThreadFlag = true;
		bool callbackThreadFlag = true;
		Device pendingAddDevice = null;
		private object addDeviceLock = new object();
		Device[] devices = new Device[256];
		BlockingQueue callbackQueue = new BlockingQueue();

		public event EnumerateCallbackEventHandler EnumerateCallback;
		public delegate void EnumerateCallbackEventHandler(string uid, 
		                                       string name, 
		                                       byte stackID,
		                                       bool isNew);

		/// <summary>
		///  Creates an IP connection to the Brick Daemon with the given *host*
		///  and *port*. With the IP connection itself it is possible to enumerate the
		///  available devices. Other then that it is only used to add Bricks and
		///  Bricklets to the connection.
		///
		///  The constructor throws an System.Net.Sockets.SocketException if there
		///  is no Brick Daemon listening at the given host and port.
		/// </summary>
		public IPConnection(string host, int port) 
		{
			this.host = host;
			this.port = port;
			socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
			ConnectSocket(host, port);

			socketStream = new NetworkStream(socket);

			callbackThread = new Thread(this.CallbackLoop);
			callbackThread.Name = "Callback-Processor";
			callbackThread.Start();

			receiveThread = new Thread(this.ReceiveLoop);
			receiveThread.Name = "Brickd-Receiver";
			receiveThread.Start();
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
			while(receiveThreadFlag)
			{
				try {
					socketStream.Close();
					socket.Close();

					socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
					ConnectSocket(host, port);

					socketStream = new NetworkStream(socket);
				} catch {
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

			while(receiveThreadFlag)
			{
				int length = 0;

				try
				{
					length = socketStream.Read(pendingData, pendingLength,
					                           pendingData.Length - pendingLength);
				}
				catch(IOException e)
				{
					if (e.InnerException != null &&
					    e.InnerException is SocketException) {
						int errorCode = ((SocketException)e.InnerException).ErrorCode;

						if (errorCode == 10004) { // WSAEINTR
							continue;
						}

						if (errorCode == 10054) { // WSAECONNRESET
							if (Reconnect()) {
								continue;
							} else {
								return;
							}
						}
					}

					if (receiveThreadFlag) {
						System.Console.Error.WriteLine("Socket disconnected by Server, destroying IPConnection");
						Destroy();
					}

					return;
				}
				catch(ObjectDisposedException)
				{
					return;
				}

				pendingLength += length;

				while(true)
				{
					if(pendingLength < 4)
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
				byte[] data;
				if(!callbackQueue.TryDequeue(out data, Timeout.Infinite))
				{
					return;
				}

				byte type = GetTypeFromData(data);

				if(type == FUNCTION_ENUMERATE_CALLBACK)
				{
					ulong uid = LEConverter.ULongFrom(4, data);
					string name = LEConverter.StringFrom(12, data, 40);
					byte stackID = LEConverter.ByteFrom(52, data);
					bool isNew = LEConverter.BoolFrom(53, data);

					OnEnumerateCallback(Base58.Encode(uid), name, stackID, isNew);
				}
				else
				{
					byte stackID = GetStackIDFromData(data);
					Device device = devices[stackID];

					Device.MessageCallback callback = device.messageCallbacks[type];
					if(callback != null) 
					{
						callback(data);
					}
				}
			}
		}
		
		protected void OnEnumerateCallback(string uid, string name, byte stackID, bool isNew)
		{
			var handler = EnumerateCallback;
			if(handler != null)
				handler(uid, name, stackID, isNew);
		}

		private static byte GetStackIDFromData(byte[] data)
		{
			return data[0];
		}

		private static byte GetTypeFromData(byte[] data)
		{
			return data[1];
		}

		private static int GetLengthFromData(byte[] data)
		{
			return LEConverter.UShortFrom(2, data);
		}

		private void HandleResponse(byte[] packet)
		{
			byte functionID = GetTypeFromData(packet);

			if(functionID == FUNCTION_GET_STACK_ID)
			{
				HandleAddDevice(packet);
				return;
			}

			if(functionID == FUNCTION_ENUMERATE_CALLBACK)
			{
				HandleEnumerate(packet);
				return;
			}

			byte stackID = GetStackIDFromData(packet);
			Device device = devices[stackID];
			if(device == null)
			{
				// Response from an unknown device, ignoring it
				return;
			}

			if(functionID == device.expectedResponseFunctionID)
			{
				device.responseQueue.Enqueue(packet);
				return;
			}

			Device.MessageCallback callback = device.messageCallbacks[functionID];
			if(callback != null)
			{
				callbackQueue.Enqueue(packet);
			}

			// Response seems to be OK, but can't be handled, most likely
			// a callback without registered function
		}

		private void HandleAddDevice(byte[] packet)
		{
			if(pendingAddDevice == null)
			{
				return;
			}

			ulong uid = LEConverter.ULongFrom(4, packet);

			if(pendingAddDevice.uid == uid)
			{
				string name = LEConverter.StringFrom(15, packet, 40);
				int i = name.LastIndexOf(' ');

				if (i < 0 || name.Substring(0, i).Replace('-', ' ') != pendingAddDevice.expectedName.Replace('-', ' '))
				{
					return;
				}

				pendingAddDevice.firmwareVersion[0] = LEConverter.ByteFrom(12, packet);
				pendingAddDevice.firmwareVersion[1] = LEConverter.ByteFrom(13, packet);
				pendingAddDevice.firmwareVersion[2] = LEConverter.ByteFrom(14, packet);
				pendingAddDevice.name = name;
				pendingAddDevice.stackID = LEConverter.ByteFrom(55, packet);
				devices[pendingAddDevice.stackID] = pendingAddDevice;
				pendingAddDevice.responseQueue.Enqueue(packet);
			}
		}

		private void HandleEnumerate(byte[] packet)
		{
			callbackQueue.Enqueue(packet);
		}

		public void Write(byte[] data)
		{
			socketStream.Write(data, 0, data.Length);
		}

		/// <summary>
		///  This method registers the following delegate:
		///
		///  <code>
		///   public delegate void EnumerateCallback(string uid, string name, byte stackID, bool isNew)
		///  </code>
		///
		///  The callback receives four parameters:
		///
		///  <code>
		///   * *uid*: The UID of the device.
		///   * *name*: The name of the device (includes "Brick" or "Bricklet" and a version number).
		///   * *stackID*: The stack ID of the device (you can find out the position in a stack with this).
		///   * *isNew*: True if the device is added, false if it is removed.
		///  </code>
		///
		///  There are three different possibilities for the callback to be called.
		///  Firstly, the callback is called with all currently available devices in the
		///  IP connection (with *isNew* true). Secondly, the callback is called if
		///  a new Brick is plugged in via USB (with *isNew* true) and lastly it is
		///  called if a Brick is unplugged (with *isNew* false).
		///
		///  It should be possible to implement "plug 'n play" functionality with this
		///  (as is done in Brick Viewer).
		/// </summary>
		public void Enumerate(EnumerateCallbackEventHandler enumerateCallback) 
		{
			this.EnumerateCallback += enumerateCallback;
			byte[] data = new byte[4];
			LEConverter.To(BROADCAST_ADDRESS, 0, data);
			LEConverter.To(FUNCTION_ENUMERATE, 1, data);
			LEConverter.To((ushort)4, 2, data);
            Write(data);
		}

		/// <summary>
		///  Adds a device (Brick or Bricklet) to the IP connection. Every device
		///  has to be added to an IP connection before it can be used. Examples for
		///  this can be found in the API documentation for every Brick and Bricklet.
		/// </summary>
		public void AddDevice(Device device)
		{
			byte[] request = new byte[12];
			LEConverter.To(BROADCAST_ADDRESS, 0, request);
			LEConverter.To(FUNCTION_GET_STACK_ID, 1, request);
			LEConverter.To((ushort)12, 2, request);
			LEConverter.To(device.uid, 4, request);

			lock (addDeviceLock)
			{
				pendingAddDevice = device;

				try
				{
					Write(request);

					byte[] response;
					if(!device.responseQueue.TryDequeue(out response, RESPONSE_TIMEOUT))
					{
						throw new TimeoutException("Could not add device " + Base58.Encode(device.uid) + ", timeout");
					}

					device.ipcon = this;
				}
				finally
				{
					pendingAddDevice = null;
				}
			}
		}

		/// <summary>
		///  Joins the threads of the IP connection. The call will block until the
		///  IP connection is destroyed: <see cref="Tinkerforge.IPConnection.Destroy"/>.
		///
		///  This makes sense if you relies solely on callbacks for events or if
		///  the IP connection was created in a threads.
		///
		///  On Windows Phone this function will do nothing (since all sockets are
		///  asynchronous and there are no threads used).
		/// </summary>
		public void JoinThread()
		{
			callbackThread.Join();
			receiveThread.Join();
		}

		/// <summary>
		///  Destroys the IP connection. The socket to the Brick Daemon will be closed
		///  and the threads of the IP connection terminated.
		/// </summary>
		public void Destroy() 
		{
			// End callback thread
			callbackThreadFlag = false;
			callbackQueue.Close();

			if(Thread.CurrentThread != callbackThread)
			{
				callbackThread.Join();
			}

			// End receive thread
			receiveThreadFlag = false;
			socketStream.Close();
			socket.Close();

			if(Thread.CurrentThread != receiveThread)
			{
				receiveThread.Join();
			}
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
		internal byte[] bindingVersion = new byte[3];
		internal ulong uid = 0;
		internal byte expectedResponseFunctionID = 0;
		internal MessageCallback[] messageCallbacks = new MessageCallback[256];
		internal BlockingQueue responseQueue = new BlockingQueue();
		internal IPConnection ipcon = null;
		private object writeLock = new object();

		internal delegate int MessageCallback(byte[] data);

		public Device(string uid) 
		{
			this.uid = Base58.Decode(uid);
		}

		/// <summary>
		///  Returns the name (including the hardware version), the firmware version
		///  and the binding version of the device. The firmware and binding versions are
		///  given in arrays of size 3 with the syntax [major, minor, revision].
		/// </summary>
		public void GetVersion(out string name, out byte[] firmwareVersion, out byte[] bindingVersion)
		{
			name = this.name;
			firmwareVersion = this.firmwareVersion;
			bindingVersion = this.bindingVersion;
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

				ipcon.Write(request);

				if (!responseQueue.TryDequeue(out response, IPConnection.RESPONSE_TIMEOUT))
				{
					expectedResponseFunctionID = 0;
					throw new TimeoutException("Did not receive response in time");
				}

				expectedResponseFunctionID = 0;
			}
		}
	}

	public class Base58 {
		private const string BASE58 = "123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ";

		public static uint IndexOf(char c, string s)
		{
			for(int i = 0; i < s.Length; i++) 
			{
				if(s[i] == c) 
				{
					return (uint)i;
				}
			}

			return 0;
		}

		public static string Encode(ulong value) 
		{
			string encoded = "";
			while(value >= 58) 
			{
				ulong div = value/58;
				int mod = (int)(value % 58);
				encoded = BASE58[mod] + encoded;
				value = div;
			}
			
			encoded = BASE58[(int)value] + encoded; 
			return encoded;
		}
		
		public static ulong Decode(string encoded) 
		{
			ulong value = 0;
			ulong columnMultiplier = 1;
			for(int i = encoded.Length - 1; i >= 0; i--) 
			{
				uint column = IndexOf(encoded[i], BASE58);
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

		static public void To(ulong data, int position, byte[] array)
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

		static public void To(ulong[] data, int position, int len, byte[] array)
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

		static public void To(uint data, int position, byte[] array)
		{
			array[position + 0] = (byte)data;
			array[position + 1] = (byte)(((uint)data >> 8) & 0xFF);
			array[position + 2] = (byte)(((uint)data >> 16) & 0xFF);
			array[position + 3] = (byte)(((uint)data >> 24) & 0xFF);
		}

		static public void To(uint[] data, int position, int len, byte[] array)
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

		static public void To(ushort data, int position, byte[] array)
		{
			array[position + 0] = (byte)data;
			array[position + 1] = (byte)(((ushort)data >> 8) & 0xFF);
		}

		static public void To(ushort[] data, int position, int len, byte[] array)
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

		static public void To(sbyte data, int position, byte[] array)
		{
			array[position + 0] = (byte)data;
		}

		static public void To(sbyte[] data, int position, int len, byte[] array)
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

		static public sbyte SByteFrom(int position, byte[] array)
		{
			return (sbyte)array[position];
		}

		static public sbyte[] SByteArrayFrom(int position, byte[] array, int len) 
		{
			sbyte[] ret = new sbyte[len];

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

		static public ushort UShortFrom(int position, byte[] array)
		{
			return (ushort)((ushort)array[position + 0] << 0 | 
					        (ushort)array[position + 1] << 8 );
		}

		static public ushort[] UShortArrayFrom(int position, byte[] array, int len) 
		{
			ushort[] ret = new ushort[len];

			for(int i = 0; i < len; i++) 
			{
				ret[i] = UShortFrom(position + i*2, array);
			}

			return ret;
		}

		static public int IntFrom(int position, byte[] array) 
		{
			return (int)((uint)array[position + 0] << 0 | 
					     (uint)array[position + 1] << 8 |
					     (uint)array[position + 2] << 16 |
					     (uint)array[position + 3] << 24);
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

		static public uint UIntFrom(int position, byte[] array) 
		{
			return (uint)((uint)array[position + 0] << 0 | 
					      (uint)array[position + 1] << 8 |
					      (uint)array[position + 2] << 16 |
					      (uint)array[position + 3] << 24);
		}

		static public uint[] UIntArrayFrom(int position, byte[] array, int len) 
		{
			uint[] ret = new uint[len];

			for(int i = 0; i < len; i++) 
			{
				ret[i] = UIntFrom(position + i*4, array);
			}

			return ret;
		}

		static public long LongFrom(int position, byte[] array) 
		{
			return (long)((ulong)array[position + 0] << 0 | 
					      (ulong)array[position + 1] << 8 |
					      (ulong)array[position + 2] << 16 |
					      (ulong)array[position + 3] << 24 |
					      (ulong)array[position + 4] << 32 |
					      (ulong)array[position + 5] << 40 |
					      (ulong)array[position + 6] << 48 |
					      (ulong)array[position + 7] << 56);
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

		static public ulong ULongFrom(int position, byte[] array) 
		{
			return (ulong)((ulong)array[position + 0] << 0 | 
					       (ulong)array[position + 1] << 8 |
					       (ulong)array[position + 2] << 16 |
					       (ulong)array[position + 3] << 24 |
					       (ulong)array[position + 4] << 32 |
					       (ulong)array[position + 5] << 40 |
					       (ulong)array[position + 6] << 48 |
					       (ulong)array[position + 7] << 56);
		}

		static public ulong[] ULongArrayFrom(int position, byte[] array, int len) 
		{
			ulong[] ret = new ulong[len];

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
	internal class BlockingQueue
	{
		private bool closing;
		private readonly Queue<byte[]> queue = new Queue<byte[]>();

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

		public bool Enqueue(byte[] item)
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

		public bool TryDequeue(out byte[] value)
		{
			return TryDequeue(out value, Timeout.Infinite);
		}
		
		public bool TryDequeue(out byte[] value, int timeout)
		{
			lock(queue)
			{
				while(queue.Count == 0)
				{
					if(closing || 
					   (timeout < Timeout.Infinite) || 
					   !Monitor.Wait(queue, timeout))
					{
						value = null;
						return false;
					}
				}

				value = (byte[])queue.Dequeue();
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
