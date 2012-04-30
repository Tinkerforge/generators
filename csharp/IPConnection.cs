using System;
using System.Collections.Generic;
using System.Threading;
using System.Net;
using System.Net.Sockets;
using System.Runtime.InteropServices;

namespace Tinkerforge
{
    public class IPConnection 
    {
		const byte BROADCAST_ADDRESS = 0;
		const byte TYPE_GET_STACK_ID = 255;
		const byte TYPE_ENUMERATE = 254;
		const byte TYPE_ENUMERATE_CALLBACK = 253;
		const byte TYPE_STACK_ENUMERATE = 252;
		const byte TYPE_ADC_CALIBRATE = 251;
		const byte TYPE_GET_ADC_CALIBRATION = 250;

#if WINDOWS_PHONE
		IPEndPoint endpoint;
		Socket socket;
#else
		NetworkStream socketStream;
		TcpClient socket;
		Thread recvThread;
		Thread callbackThread;
#endif
		bool RecvLoopFlag = true;
		Device addDev = null;
		Device[] devices = new Device[256];
		EnumerateCallback enumerateCallback = null;
		BlockingQueue callbackQueue = new BlockingQueue();

		internal const int TIMEOUT_ADD_DEVICE = 2500;
		internal const int TIMEOUT_ANSWER = 2500;

		public delegate void EnumerateCallback(string uid, 
		                                       string name, 
		                                       byte stackID,
		                                       bool isNew);

		public IPConnection(string host, int port) 
		{
#if WINDOWS_PHONE
            IPAddress ipAddress = IPAddress.Parse(host);
            endpoint = new IPEndPoint(ipAddress, port);
            socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

            SocketAsyncEventArgs args = new SocketAsyncEventArgs();
            args.UserToken = socket;
            args.RemoteEndPoint = endpoint;
            args.Completed += new EventHandler<SocketAsyncEventArgs>(IOCompleted);


            if(!socket.ConnectAsync(args))
            {
                IOCompleted(args.ConnectSocket, args);
            }
#else
			socket = new TcpClient();
			socket.Connect(host, port);

			socketStream = socket.GetStream();

			callbackThread = new Thread(this.CallbackLoop);
			callbackThread.Start();
			recvThread = new Thread(this.RecvLoop);
			recvThread.Start();
#endif
		}

#if WINDOWS_PHONE
        private void IOCompleted(object sender, SocketAsyncEventArgs e)
        {
            if(e.SocketError != SocketError.Success)
            {
                return;
            }

            switch(e.LastOperation)
            {
                case SocketAsyncOperation.Connect:
					byte[] receiveBuffer = new byte[8192];
					e.SetBuffer(receiveBuffer, 0, receiveBuffer.Length);

					if(!socket.ReceiveAsync(e))
					{
						IOCompleted(e.ConnectSocket, e);
					}


					break;
                case SocketAsyncOperation.Receive:
					HandleMessage(e.Buffer);

					if(!socket.ReceiveAsync(e))
					{
						IOCompleted(e.ConnectSocket, e);
					}

					break;
            }
        }
		
		private void WriteAsync(byte[] data)
		{
            SocketAsyncEventArgs args = new SocketAsyncEventArgs();
            args.SetBuffer(data, 0, data.Length);
            args.UserToken = socket;
            args.RemoteEndPoint = endpoint;
            args.Completed += new EventHandler<SocketAsyncEventArgs>(IOCompleted);

			socket.SendAsync(args);
		}
#else
		private void RecvLoop() 
		{
			try
			{
				while(RecvLoopFlag) 
				{
					byte[] data = new byte[8192];
					int length = socketStream.Read(data, 0, data.Length);

					string str = "";
					for(int i = 0; i < length; i++) {
						str += data[i] + " ";
					}

					int handled = 0;
					while(length != handled)
					{
						byte[] tmp = new byte[length-handled];
						Array.Copy(data, handled, tmp, 0, length - handled);
						handled += HandleMessage(tmp);
					}
				}
			}
			catch(Exception)
			{
				RecvLoopFlag = false;
				return;
			}

		}
#endif

		private void CallbackLoop()
		{
			while(RecvLoopFlag)
			{
				byte[] data;			
				if(!callbackQueue.TryDequeue(out data, Timeout.Infinite))
				{
					return;
				}

				byte type = GetTypeFromData(data);

				if(type == TYPE_ENUMERATE_CALLBACK)
				{
					ulong uid = LEConverter.ULongFrom(4, data);
					string name = LEConverter.StringFrom(12, data, 40);
					byte stackID = LEConverter.ByteFrom(52, data);
					bool isNew = LEConverter.BoolFrom(53, data);

					enumerateCallback(Base58.Encode(uid), name, stackID, isNew);
				}
				else
				{
					byte stackID = GetStackIDFromData(data);
					Device device = devices[stackID];

					Device.MessageCallback callback = device.messageCallbacks[type];
					if(callback != null && device.callbacks[type] != null) 
					{
						callback(data);
					}
				}
			}
		}

		private static byte GetStackIDFromData(byte[] data)
		{
			return data[0];
		}

		private static int GetLengthFromData(byte[] data)
		{
			return LEConverter.UShortFrom(2, data);
		}

		private static byte GetTypeFromData(byte[] data)
		{
			return data[1];
		}


		private int HandleMessage(byte[] data)
		{
			byte type = GetTypeFromData(data);
			if(type == TYPE_GET_STACK_ID) 
			{
				return HandleAddDevice(data);
			}
			else if(type == TYPE_ENUMERATE_CALLBACK)
			{
				return HandleEnumerate(data);
			}

			byte stackID = GetStackIDFromData(data);
			int length = GetLengthFromData(data);

			Device device = devices[stackID];

			if(device == null)
			{
				Console.WriteLine("Message with unknown Stack ID, discarded: "
				                  + stackID);
				return length;
			}

			if(device.answerType == type)
			{
				device.answerQueue.Enqueue(data);
				return length;
			}

			Device.MessageCallback callback = device.messageCallbacks[type];
			if(callback != null && device.callbacks[type] != null)
			{
				callbackQueue.Enqueue(data);
			}

			// Message seems to be OK, but can't be handled, most likely
			// a signal without registered callback
			return length;
		}

		private int HandleAddDevice(byte[] data)
		{
			int length = GetLengthFromData(data);

			if(addDev == null) 
			{
				return length;
			}

			ulong uid = LEConverter.ULongFrom(4, data);

			if(addDev.uid == uid) 
			{
				addDev.firmwareVersion[0] = LEConverter.ByteFrom(12, data);
				addDev.firmwareVersion[1] = LEConverter.ByteFrom(13, data);
				addDev.firmwareVersion[2] = LEConverter.ByteFrom(14, data);
				addDev.name = LEConverter.StringFrom(15, data, 40);
				addDev.stackID = LEConverter.ByteFrom(55, data);
				devices[addDev.stackID] = addDev;
				addDev.answerQueue.Enqueue(data);
				addDev = null;
			}

			return length;
		}

		private int HandleEnumerate(byte[] data)
		{
			int length = GetLengthFromData(data);
			if(enumerateCallback == null) 
			{
				return length;
			}

			callbackQueue.Enqueue(data);

			return length;
		}

        public void Write(byte[] data)
        {
#if WINDOWS_PHONE
			WriteAsync(data);
#else
            socketStream.Write(data, 0, data.Length);
#endif
        }

		public void Enumerate(EnumerateCallback enumerateCallback) 
		{
			this.enumerateCallback = enumerateCallback;
			byte[] data = new byte[4];
			LEConverter.To(BROADCAST_ADDRESS, 0, data);
			LEConverter.To(TYPE_ENUMERATE, 1, data);
			LEConverter.To((ushort)4, 2, data);
#if WINDOWS_PHONE
			WriteAsync(data);
#else
            socketStream.Write(data, 0, data.Length);
#endif
		}

		public void AddDevice(Device device) {
			byte[] data = new byte[12];
			LEConverter.To(BROADCAST_ADDRESS, 0, data);
			LEConverter.To(TYPE_GET_STACK_ID, 1, data);
			LEConverter.To((ushort)12, 2, data);
			LEConverter.To(device.uid, 4, data);

			addDev = device;
			
#if WINDOWS_PHONE
			WriteAsync(data);
#else
            socketStream.Write(data, 0, data.Length);
#endif

			byte[] tmp;
			if(!device.answerQueue.TryDequeue(out tmp, TIMEOUT_ADD_DEVICE))
			{
				throw new TimeoutException("Did not receive answer for addDevice in time");
			}

			device.ipcon = this;
		}

		public void JoinThread()
		{
#if WINDOWS_PHONE
#else
			recvThread.Join();
#endif
		}

		public void Destroy() 
		{
#if WINDOWS_PHONE
#else
			RecvLoopFlag = false;
			try 
			{
				socketStream.Close();
			}
			catch(Exception)
			{
			}
			socket.Close();
			callbackQueue.Close();
#endif
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
		internal String name;
		internal byte[] firmwareVersion = new byte[3];
		internal byte[] bindingVersion = new byte[3];
		internal ulong uid = 0;
		internal byte answerType = 0;
		internal Delegate[] callbacks = new Delegate[256];
		internal MessageCallback[] messageCallbacks = new MessageCallback[256];
		internal BlockingQueue answerQueue = new BlockingQueue();
		internal IPConnection ipcon = null;
        private object writeLock = new object();

		internal delegate int MessageCallback(byte[] data);

		public Device(string uid) 
		{
			this.uid = Base58.Decode(uid);
		}

        protected void sendOneWayMessage(byte[] data)
        {
            lock (writeLock)
            {
                ipcon.Write(data);
            }
        }

        protected void sendReturningMessage(byte[] data, byte type, out byte[] answer)
        {
            lock (writeLock)
            {
                sendOneWayMessage(data);

                answerType = type;
                if (!answerQueue.TryDequeue(out answer, IPConnection.TIMEOUT_ANSWER))
                {
                    throw new TimeoutException("Did not receive answer in time");
                }
            }
        }
	}

	public class Base58 {
		private const string BASE58 = "123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ";

		public static uint indexOf(char c, string s) 
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
				uint column = indexOf(encoded[i], BASE58);
				value += column * columnMultiplier;
				columnMultiplier *= 58;
			}
			
			return value;
		}
	}

	internal class LEConverter
	{
		static public void To(string data, int position, byte[] array)
		{
			for(int i = 0; i < Math.Min(array.Length, data.Length); i++)
			{
				array[position + i] = (byte)data[i];
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

		static public void To(long[] data, int position, byte[] array)
		{
			for(int i = 0; i < data.Length; i++)
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

		static public void To(ulong[] data, int position, byte[] array)
		{
			for(int i = 0; i < data.Length; i++)
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

		static public void To(int[] data, int position, byte[] array)
		{
			for(int i = 0; i < data.Length; i++)
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

		static public void To(uint[] data, int position, byte[] array)
		{
			for(int i = 0; i < data.Length; i++)
			{
				To(data[i], position + i, array);
			}
		}

		static public void To(short data, int position, byte[] array)
		{
			array[position + 0] = (byte)data;
			array[position + 1] = (byte)(((ushort)data >> 8) & 0xFF);
		}

		static public void To(short[] data, int position, byte[] array)
		{
			for(int i = 0; i < data.Length; i++)
			{
				To(data[i], position + i, array);
			}
		}

		static public void To(ushort data, int position, byte[] array)
		{
			array[position + 0] = (byte)data;
			array[position + 1] = (byte)(((ushort)data >> 8) & 0xFF);
		}

		static public void To(ushort[] data, int position, byte[] array)
		{
			for(int i = 0; i < data.Length; i++)
			{
				To(data[i], position + i, array);
			}
		}

		static public void To(byte data, int position, byte[] array)
		{
			array[position + 0] = (byte)data;
		}

		static public void To(byte[] data, int position, byte[] array)
		{
			for(int i = 0; i < data.Length; i++)
			{
				To(data[i], position + i, array);
			}
		}

		static public void To(sbyte data, int position, byte[] array)
		{
			array[position + 0] = (byte)data;
		}

		static public void To(sbyte[] data, int position, byte[] array)
		{
			for(int i = 0; i < data.Length; i++)
			{
				To(data[i], position + i, array);
			}
		}

		static public void To(char data, int position, byte[] array)
		{
			array[position + 0] = (byte)data;
		}

		static public void To(char[] data, int position, byte[] array)
		{
			for(int i = 0; i < data.Length; i++)
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

		static public void To(bool[] data, int position, byte[] array)
		{
			for(int i = 0; i < data.Length; i++)
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
			string s = "";
			for(int i = position; i < position + len; i++) 
			{
				if(array[i] == 0)
				{
					break;
				}
				s += (char)array[i];
			}

			return s;
		}

	}

	// There is no BlockingQueue in c# version <= 2.0, we make our own
	// to be backward compatible
	public class BlockingQueue
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

		public bool TryDequeue(out byte[] value, int timeout = Timeout.Infinite)
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
}
