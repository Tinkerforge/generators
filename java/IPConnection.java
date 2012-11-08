/*
 * Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
 * Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file, 
 * with or without modification, are permitted.
 */

package com.tinkerforge;

import java.util.concurrent.Semaphore;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.Hashtable;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

class ReceiveThread extends Thread {
	IPConnection ipcon = null;

	ReceiveThread(IPConnection ipcon) {
		this.ipcon = ipcon;
	}

	public void run() {
		byte[] pendingData = new byte[8192];
		int pendingLength = 0;

		try {
			ipcon.in = ipcon.sock.getInputStream();
		} catch(java.io.IOException e) {
			e.printStackTrace();
			return;
		}

		while(ipcon.receiveThreadFlag) {
			int length;

			try {
				length = ipcon.in.read(pendingData, pendingLength,
				                       pendingData.length - pendingLength);
			} catch(java.net.SocketException e) {
				if(ipcon.reconnect()) {
					continue;
				} else {
					return;
				}
			} catch(java.io.IOException e) {
				if(ipcon.receiveThreadFlag) {
					e.printStackTrace();
				}
				return;
			}

			if(length == 0 || length == -1) {
				if(ipcon.receiveThreadFlag) {
					System.err.println("Socket disconnected by Server, destroying IPConnection");
					ipcon.destroy();
				}
				return;
			}

			pendingLength += length;

			while(true) {
				if(pendingLength < 8) {
					// Wait for complete header
					break;
				}

				length = ipcon.getLengthFromData(pendingData);

				if(pendingLength < length) {
					// Wait for complete packet
					break;
				}

				byte[] packet = new byte[length];

				System.arraycopy(pendingData, 0, packet, 0, length);
				System.arraycopy(pendingData, length, pendingData, 0, pendingLength - length);
				pendingLength -= length;
				ipcon.handleResponse(packet);
			}
		}
	}
}


class CallbackThread extends Thread {
	IPConnection ipcon = null;

	CallbackThread(IPConnection ipcon) {
		this.ipcon = ipcon;
	}

	public void run() {
		while(ipcon.callbackThreadFlag) {
			byte[] data = null;
			try {
				data = ipcon.callbackQueue.take();
			} catch(InterruptedException e) {
				e.printStackTrace();
				continue;
			}

			if (!ipcon.callbackThreadFlag) {
				return;
			}

			byte functionID = ipcon.getFunctionIDFromData(data);
			if(functionID == ipcon.CALLBACK_ENUMERATE) {
				int length = ipcon.getLengthFromData(data);
				ByteBuffer bb = ByteBuffer.wrap(data, 4, length - 4);
				bb.order(ByteOrder.LITTLE_ENDIAN);
				String uid = ipcon.base58Encode(bb.getLong());
				String name = ipcon.string(bb, 40);
				short stackID = ipcon.unsignedByte(bb.get());
				boolean isNew = bb.get() != 0;

				ipcon.enumerateListener.enumerate(uid, name, stackID, isNew);
			} else {
				long uid = ipcon.getUIDFromData(data);
				Device device = ipcon.devices.get(uid);
				if(device.callbacks[functionID] != null) {
					device.callbacks[functionID].callback(data);
				}
			}
		}
	}
}

public class IPConnection {
	private final static String BASE58 = "123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ";
	private final static byte FUNCTION_GET_IDENTITY = (byte)255;
	private final static byte FUNCTION_ENUMERATE = (byte)254;
	protected final static byte CALLBACK_ENUMERATE = (byte)253;

	private final static long BROADCAST_UID = (long)0;

	public final static int RESPONSE_TIMEOUT = 2500;

	protected Hashtable<Long, Device> devices = new Hashtable<Long, Device>();
	protected LinkedBlockingQueue<byte[]> callbackQueue = new LinkedBlockingQueue<byte[]>();

	private String host;
	private int port;

	boolean receiveThreadFlag = true;
	boolean callbackThreadFlag = true;
	Socket sock = null;
	OutputStream out = null;
	InputStream in = null;
	protected EnumerateListener enumerateListener = null;
	ReceiveThread receiveThread = null;
	CallbackThread callbackThread = null;

	public static class TimeoutException extends Exception {
		private static final long serialVersionUID = 1L;

		TimeoutException(String string) {
			super(string);
		}
	}

	public interface EnumerateListener {
		public void enumerate(String uid, String name, short stackID, boolean isNew);
	}

	/**
	 * Creates an IP connection to the Brick Daemon with the given \c host
	 * and \c port. With the IP connection itself it is possible to enumerate the
	 * available devices. Other then that it is only used to add Bricks and
	 * Bricklets to the connection.
	 *
	 * The constructor throws an IOException if there is no Brick Daemon
	 * listening at the given host and port.
	 */
	public IPConnection(String host, int port) throws java.io.IOException {
		this.host = host;
		this.port = port;

		sock = new Socket(host, port);
		out = sock.getOutputStream();
		out.flush();

		callbackThread = new CallbackThread(this);
		callbackThread.start();
		receiveThread = new ReceiveThread(this);
		receiveThread.start();
	}

	void disconnect() {
		try {
			if(in != null) {
				in.close();
				in = null;
			}
		} catch(java.io.IOException e) {
			e.printStackTrace();
		}

		try {
			if(out != null) {
				out.close();
				out = null;
			}
		} catch(java.io.IOException e) {
			e.printStackTrace();
		}

		try {
			if(sock != null) {
				sock.close();
				sock = null;
			}
		} catch(java.io.IOException e) {
			e.printStackTrace();
		}
	}

	boolean reconnect() {
		disconnect();

		while(receiveThreadFlag) {
			try {
				sock = new Socket(this.host, this.port);
				out = sock.getOutputStream();
				out.flush();
				in = sock.getInputStream();
			} catch(java.io.IOException e1) {
				disconnect();
				try {
					Thread.sleep(500);
				} catch(InterruptedException e2) {
					e2.printStackTrace();
				}
				continue;
			}

			return true;
		}

		return false;
	}

	void handleResponse(byte[] packet) {
		byte functionID = getFunctionIDFromData(packet);

		if(functionID == CALLBACK_ENUMERATE) {
			handleEnumerate(packet);
			return;
		}

		long uid = getUIDFromData(packet);

		if(!devices.contains(uid)) {
			// Message for an unknown device, ignoring it
			return;
		}

		Device device = devices.get(uid);

		if(functionID == device.expectedResponseFunctionID) {
			try {
				device.responseQueue.put(packet);
			} catch(InterruptedException e) {
				e.printStackTrace();
			}
			return;
		}
		
		if(device.callbacks[functionID] != null && device.listenerObjects[functionID] != null) {
			try {
				callbackQueue.put(packet);
			} catch(InterruptedException e) {
				e.printStackTrace();
			}
		}

		// Response seems to be OK, but can't be handled, most likely
		// a callback without registered listener
	}

	protected long getUIDFromData(byte[] data) {
		return (long)(data[0] & 0xFF) | (long)((data[1] & 0xFF) << 8) | (long)((data[2] & 0xFF) << 16) | (long)((data[3] & 0xFF) << 24);
	}

	protected byte getLengthFromData(byte[] data) {
		return data[4];
	}

	protected byte getFunctionIDFromData(byte[] data) {
		return data[5];
	}

	public static String string(ByteBuffer buffer, int length) {
		StringBuilder builder = new StringBuilder(length);
		int i = 0;

		while(i < length) {
			char c = (char)buffer.get();
			++i;

			if (c == 0) {
				break;
			}

			builder.append(c);
		}

		while(i < length) {
			buffer.get();
			++i;
		}

		return builder.toString();
	}

	public static short unsignedByte(byte data) {
		return (short)(data & 0xFF);
	}

	public static int unsignedShort(short data) {
		return (int)(data & 0xFFFF);
	}

	public static long unsignedInt(int data) {
		return (long)(((long)data) & 0xFFFFFFFF);
	}

	/**
	 * Joins the threads of the IP connection. The call will block until the
	 * IP connection is destroyed: {@link com.tinkerforge.IPConnection.destroy}.
	 *
	 * This makes sense if you relies solely on callbacks for events or if
	 * the IP connection was created in a threads.
	 */
	public void joinThread() {
		try {
			callbackThread.join();
			receiveThread.join();
		} catch(InterruptedException e) {
			e.printStackTrace();
		}
	}

	public void write(byte[] data) {
		try {
			out.write(data);
		} catch(java.io.IOException e) {
			e.printStackTrace();
			return;
		}
	}

	private void handleEnumerate(byte[] packet) {
		if(enumerateListener != null) {
			try {
				callbackQueue.put(packet);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}

	/**
	 * Destroys the IP connection. The socket to the Brick Daemon will be closed
	 * and the threads of the IP connection terminated.
	 */
	public void destroy() {
		// End callback thread
		callbackThreadFlag = false;

		try {
			callbackQueue.put(new byte[1]); // Unblock callback thread
		} catch (InterruptedException e) {
			e.printStackTrace();
		}

		if (Thread.currentThread() != callbackThread) {
			try {
				callbackThread.join();
			} catch(InterruptedException e) {
				e.printStackTrace();
			}
		}

		// End receive thread
		receiveThreadFlag = false;

		disconnect();

		if (Thread.currentThread() != receiveThread) {
			try {
				receiveThread.join();
			} catch(InterruptedException e) {
				e.printStackTrace();
			}
		}
	}

	/**
	 * This method registers the following listener:
	 *
	 * \code
	 * public class IPConnection.EnumerateListener() {
	 *   public void enumerate(String uid, String name, short stackID, boolean isNew)
	 * }
	 * \endcode
	 *
	 * The listener receives four parameters:
	 *
	 * - \c uid: The UID of the device.
	 * - \c name: The name of the device (includes "Brick" or "Bricklet" and a version number).
	 * - \c stackID: The stack ID of the device (you can find out the position in a stack with this).
	 * - \c isNew: True if the device is added, false if it is removed.
	 *
	 * There are three different possibilities for the listener to be called.
	 * Firstly, the listener is called with all currently available devices in the
	 * IP connection (with \c isNew true). Secondly, the listener is called if
	 * a new Brick is plugged in via USB (with \c isNew true) and lastly it is
	 * called if a Brick is unplugged (with \c isNew false).
	 *
	 * It should be possible to implement "plug 'n play" functionality with this
	 * (as is done in Brick Viewer).
	 */
	public void enumerate(EnumerateListener enumerateListener) {
		ByteBuffer request = createRequestBuffer(BROADCAST_UID, (byte)8, FUNCTION_ENUMERATE);

		this.enumerateListener = enumerateListener;

		try {
			out.write(request.array());
		}
		catch(java.io.IOException e) {
			e.printStackTrace();
		}
	}

	static ByteBuffer createRequestBuffer(long uid, byte length, byte functionID) {
		ByteBuffer buffer = ByteBuffer.allocate(length);

		buffer.order(ByteOrder.LITTLE_ENDIAN);
		buffer.putInt((int)uid);
		buffer.put(length);
		buffer.put(functionID);

		return buffer;
	}

	public static String base58Encode(long value) {
		String encoded = "";

		while(value >= 58) {
			long div = value / 58;
			int mod = (int)(value % 58);
			encoded = BASE58.charAt(mod) + encoded;
			value = div;
		}

		return BASE58.charAt((int)value) + encoded;
	}

	public static long base58Decode(String encoded) {
		long value = (long)0;
		long columnMultiplier = (long)1;

		for(int i = encoded.length() - 1; i >= 0; i--) {
			int column = BASE58.indexOf(encoded.charAt(i));
			value += column * columnMultiplier;
			columnMultiplier *= 58;
		}

		return value;
	}
}
