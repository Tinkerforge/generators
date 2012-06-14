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

		while(ipcon.threadRunFlag) {
			int length;

			try {
				length = ipcon.in.read(pendingData, pendingLength,
				                       pendingData.length - pendingLength);
			} catch(java.io.IOException e) {
				if(ipcon.threadRunFlag) {
					e.printStackTrace();
				}
				return;
			}

			if(length == 0 || length == -1) {
				if(ipcon.threadRunFlag) {
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
		while(ipcon.threadRunFlag) {
			byte[] data = null;
			try {
				data = ipcon.callbackQueue.take();
			} catch(InterruptedException e) {
				e.printStackTrace();
				continue;
			}

			if (!ipcon.threadRunFlag) {
				return;
			}

			byte functionID = ipcon.getFunctionIDFromData(data);
			if(functionID == ipcon.FUNCTION_ENUMERATE_CALLBACK) {
				int length = ipcon.getLengthFromData(data);
				ByteBuffer bb = ByteBuffer.wrap(data, 4, length - 4);
				bb.order(ByteOrder.LITTLE_ENDIAN);
				long uid_num = bb.getLong();
				
				String uid = ipcon.base58Encode(uid_num);
				
				String name = "";
				for(int i = 0; i < 40; i++) {
					name += (char)bb.get();
				}
				
				short stackID = ipcon.unsignedByte(bb.get());
				boolean isNew = bb.get() != 0;
				
				ipcon.enumerateListener.enumerate(uid, name, stackID, isNew);
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
	protected LinkedBlockingQueue<byte[]> callbackQueue = new LinkedBlockingQueue<byte[]>();

	boolean threadRunFlag = true;
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

	public void joinThread() {
		try {
			receiveThread.join();
			callbackThread.join();
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
			pendingAddDevice = null;
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

	public void destroy() {
		threadRunFlag = false;

		try {
			callbackQueue.put(new byte[1]);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}

		try {
			if(in != null) {
				in.close();
			}
		}
		catch(java.io.IOException e) {
			e.printStackTrace();
		}

		try {
			if(out != null) {
				out.close();
			}
		}
		catch(java.io.IOException e) {
			e.printStackTrace();
		}

		try {
			if(sock != null) {
				sock.close();
			}
		}
		catch(java.io.IOException e) {
			e.printStackTrace();
		}
	}

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

	public void addDevice(Device device) throws IPConnection.TimeoutException {
		ByteBuffer request = createRequestBuffer(BROADCAST_ADDRESS, FUNCTION_GET_STACK_ID, (short)12);
		request.putLong(device.uid);

		pendingAddDevice = device;

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
