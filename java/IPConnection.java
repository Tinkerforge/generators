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
import java.util.concurrent.SynchronousQueue;
import java.util.concurrent.LinkedBlockingQueue;
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
				if(pendingLength < 4) {
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
			if(functionID == ipcon.FUNCTION_ENUMERATE_CALLBACK) {
				int length = ipcon.getLengthFromData(data);
				ByteBuffer bb = ByteBuffer.wrap(data, 4, length - 4);
				bb.order(ByteOrder.LITTLE_ENDIAN);
				long uid_num = bb.getLong();
				
				String uid = ipcon.base58Encode(uid_num);
				
				StringBuilder nameBuilder = new StringBuilder();
				for(int i = 0; i < 40; i++) {
					byte currentByte = bb.get();
					if(currentByte == 0) {
						break;
					}
					nameBuilder.append((char)currentByte);
				}
				
				short stackID = ipcon.unsignedByte(bb.get());
				boolean isNew = bb.get() != 0;
				
				ipcon.enumerateListener.enumerate(uid, nameBuilder.toString(), stackID, isNew);
			} else {
				byte stackID = ipcon.getStackIDFromData(data);
				Device device = ipcon.devices[stackID];
				if(device.callbacks[functionID] != null) {
					device.callbacks[functionID].callback(data);
				}
			}
		}
	}
}

public class IPConnection {
	private final static String BASE58 = "123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ";
	private final static byte FUNCTION_GET_STACK_ID = (byte)255;
	private final static byte FUNCTION_ENUMERATE = (byte)254;
	protected final static byte FUNCTION_ENUMERATE_CALLBACK = (byte)253;
	private final static byte FUNCTION_STACK_ENUMERATE = (byte)252;
	private final static byte FUNCTION_ADC_CALIBRATE = (byte)251;
	private final static byte FUNCTION_GET_ADC_CALIBRATION = (byte)250;

	private final static byte BROADCAST_ADDRESS = (byte)0;

	public final static int RESPONSE_TIMEOUT = 2500;

	protected Device[] devices = new Device[255];
	private Device pendingAddDevice = null;
	private Object addDeviceMutex = new Object();
	protected LinkedBlockingQueue<byte[]> callbackQueue = new LinkedBlockingQueue<byte[]>();

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
		sock = new Socket(host, port);
		out = sock.getOutputStream();
		out.flush();

		callbackThread = new CallbackThread(this);
		callbackThread.start();
		receiveThread = new ReceiveThread(this);
		receiveThread.start();
	}

	void handleResponse(byte[] packet) {
		byte functionID = getFunctionIDFromData(packet);

		if(functionID == FUNCTION_GET_STACK_ID) {
			handleAddDevice(packet);
			return;
		}

		if(functionID == FUNCTION_ENUMERATE_CALLBACK) {
			handleEnumerate(packet);
			return;
		}

		byte stackID = getStackIDFromData(packet);

		if(devices[stackID] == null) {
			// Message for an unknown device, ignoring it
			return;
		}

		Device device = devices[stackID];

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

	protected byte getStackIDFromData(byte[] data) {
		return data[0];
	}

	protected byte getFunctionIDFromData(byte[] data) {
		return data[1];
	}

	protected int getLengthFromData(byte[] data) {
		return (data[2] & 0xFF) | ((data[3] & 0xFF) << 8);
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

	public void write(Device device, ByteBuffer bb, byte functionID, boolean hasReturn) {
		try {
			device.semaphoreWrite.acquire();
		} catch(InterruptedException e) {
			e.printStackTrace();
			return;
		}

		if(hasReturn) {
			device.expectedResponseFunctionID = functionID;
		}

		try {
			out.write(bb.array());
		} catch(java.io.IOException e) {
			e.printStackTrace();
			return;
		}

		if(!hasReturn) {
			device.semaphoreWrite.release();
		}
	}

	private void handleAddDevice(byte[] packet) {
		if(pendingAddDevice == null) {
			return;
		}

		int length = getLengthFromData(packet);
		ByteBuffer bb = ByteBuffer.wrap(packet, 4, length - 4);
		bb.order(ByteOrder.LITTLE_ENDIAN);

		long uid = bb.getLong();
		if(pendingAddDevice.uid == uid) {
			pendingAddDevice.firmwareVersion[0] = IPConnection.unsignedByte(bb.get());
			pendingAddDevice.firmwareVersion[1] = IPConnection.unsignedByte(bb.get());
			pendingAddDevice.firmwareVersion[2] = IPConnection.unsignedByte(bb.get());

			String name = "";
			for(int i = 0; i < 40; i++) {
				name += (char)bb.get();
			}

			int i = name.lastIndexOf(' ');
			if (i < 0 || !name.substring(0, i).replace('-', ' ').equals(pendingAddDevice.expectedName.replace('-', ' '))) {
				return;
			}

			pendingAddDevice.name = name;
			pendingAddDevice.stackID = unsignedByte(bb.get());
			devices[pendingAddDevice.stackID] = pendingAddDevice;
			try {
				pendingAddDevice.responseQueue.put(packet);
			} catch(InterruptedException e) {
				e.printStackTrace();
			}
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

		try {
			if(in != null) {
				in.close();
			}
		} catch(java.io.IOException e) {
			e.printStackTrace();
		}

		try {
			if(out != null) {
				out.close();
			}
		} catch(java.io.IOException e) {
			e.printStackTrace();
		}

		try {
			if(sock != null) {
				sock.close();
			}
		} catch(java.io.IOException e) {
			e.printStackTrace();
		}

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
		ByteBuffer request = createRequestBuffer(BROADCAST_ADDRESS, FUNCTION_ENUMERATE, (short)4);

		this.enumerateListener = enumerateListener;

		try {
			out.write(request.array());
		}
		catch(java.io.IOException e) {
			e.printStackTrace();
		}
	}

	/**
	 * Adds a device (Brick or Bricklet) to the IP connection. Every device
	 * has to be added to an IP connection before it can be used. Examples for
	 * this can be found in the API documentation for every Brick and Bricklet.
	 */
	public void addDevice(Device device) throws IPConnection.TimeoutException {
		ByteBuffer request = createRequestBuffer(BROADCAST_ADDRESS, FUNCTION_GET_STACK_ID, (short)12);
		request.putLong(device.uid);

		synchronized(addDeviceMutex) {
			pendingAddDevice = device;

			try {
				try {
					out.write(request.array());
				}
				catch(java.io.IOException e) {
					e.printStackTrace();
				}

				byte[] response = null;
				try {
					response = pendingAddDevice.responseQueue.poll(IPConnection.RESPONSE_TIMEOUT, TimeUnit.MILLISECONDS);
					if(response == null) {
						throw new IPConnection.TimeoutException("Could not add device " + base58Encode(device.uid) + ", timeout");
					}
				} catch (InterruptedException e) {
					e.printStackTrace();
				}

				device.ipcon = this;
			} finally {
				pendingAddDevice = null;
			}
		}
	}

	static ByteBuffer createRequestBuffer(byte stackID, byte functionID, short length) {
		ByteBuffer buffer = ByteBuffer.allocate(length);

		buffer.order(ByteOrder.LITTLE_ENDIAN);
		buffer.put(stackID);
		buffer.put(functionID);
		buffer.putShort(length);

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
