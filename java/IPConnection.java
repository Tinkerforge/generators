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

class RecvLoopThread extends Thread {
	IPConnection ipcon = null;

	RecvLoopThread(IPConnection ipcon) {
		this.ipcon = ipcon;
	}

	public void run() {
		byte[] data = new byte[8192];
		
		try {
			ipcon.in = ipcon.sock.getInputStream();
		}
		catch(java.io.IOException e) {
			e.printStackTrace();
		}

		while(ipcon.recvLoopFlag) {
			try {
				int length = ipcon.in.read(data, 0, 8192);
				if(length == 0) {
					if(ipcon.recvLoopFlag) {
						System.err.println("Socket disconnected by Server, destroying ipcon");
						ipcon.destroy();
					}
					return;
				} else if(length == -1) {
					if(ipcon.recvLoopFlag) {
						System.err.println("Socket disconnected by Server, destroying ipcon");
						ipcon.destroy();
					}
					return;
				}
				
				int handled = 0;
				while(length != handled) {
					// Copy data, otherwise callback data might be overwritten
					byte[] tmp = new byte[length-handled];
					System.arraycopy(data, handled, tmp, 0, length - handled);
					
					handled += ipcon.handleMessage(tmp);
				}
			} 
			catch(java.io.IOException e) {
				return;
			}
		}
	}
}


class CallbackLoopThread extends Thread {
	IPConnection ipcon = null;

	CallbackLoopThread(IPConnection ipcon) {
		this.ipcon = ipcon;
	}

	public void run() {
		while(ipcon.recvLoopFlag) {
			byte[] data = null;
			try {
				data = ipcon.callbackQueue.take();
			} catch (InterruptedException e) {
				e.printStackTrace();
				continue;
			}

		
			byte type = ipcon.getTypeFromData(data);
			if(type == ipcon.TYPE_ENUMERATE_CALLBACK) {
				int length = ipcon.getLengthFromData(data);
				ByteBuffer bb = ByteBuffer.wrap(data, 4, length - 4);
				bb.order(ByteOrder.LITTLE_ENDIAN);
				long uid_num = bb.getLong();
				
				String uid = ipcon.base58Encode(uid_num);
				
				String name = new String();
				for(int i = 0; i < 40; i++) {
					name += (char)bb.get();
				}
				
				short stackID = ipcon.unsignedByte(bb.get());
				boolean isNew = bb.get() != 0;
				
				ipcon.enumerateListener.enumerate(uid, name, stackID, isNew);
			} else {
				byte stackID = ipcon.getStackIDFromData(data);
				Device device = ipcon.devices[stackID];
				if(device.callbacks[type] != null) {
					device.callbacks[type].callback(data);
				}
			}
		}
	}
}

public class IPConnection {
	private final static String BASE58 = new String("123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ");
    private final static byte TYPE_GET_STACK_ID = (byte)255;
    private final static byte TYPE_ENUMERATE = (byte)254;
    protected final static byte TYPE_ENUMERATE_CALLBACK = (byte)253;
    private final static byte TYPE_STACK_ENUMERATE = (byte)252;
    private final static byte TYPE_ADC_CALIBRATE = (byte)251;
    private final static byte TYPE_GET_ADC_CALIBRATION = (byte)250;

    private final static byte BROADCAST_ADDRESS = (byte)0;
    private final static short ENUMERATE_LENGTH = (short)4;
    private final static short GET_STACK_ID_LENGTH = (short)12;
    
    public final static int TIMEOUT_ADD_DEVICE = 2500;
    public final static int TIMEOUT_ANSWER = 2500;
    
    protected Device[] devices = new Device[255];
    private Device addDevice = null;
	protected LinkedBlockingQueue<byte[]> callbackQueue = new LinkedBlockingQueue<byte[]>();

    boolean recvLoopFlag = true;
	Socket sock = null;
	OutputStream out = null;
	InputStream in = null;
	protected EnumerateListener enumerateListener = null;
	RecvLoopThread recvLoopThread = null;
	CallbackLoopThread callbackLoopThread = null;

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

		callbackLoopThread = new CallbackLoopThread(this);
		callbackLoopThread.start();
		recvLoopThread = new RecvLoopThread(this);
		recvLoopThread.start();
	}
	
	int handleMessage(byte[] data) {
		byte type = getTypeFromData(data);
		
		if(type == TYPE_GET_STACK_ID) {
			return handleAddDevice(data);
		} else if(type == TYPE_ENUMERATE_CALLBACK) {
			return handleEnumerate(data);
		}
		
		byte stackID = getStackIDFromData(data);
		int length = getLengthFromData(data);
		
		if(devices[stackID] == null) {
			// Message for an unknown device, ignoring it
			return length;
		}
		
		Device device = devices[stackID];
		
		if(device.answerType == type) {
			try {
				device.answerQueue.put(data);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			return length;
		}
		
		if(device.callbacks[type] != null && device.listenerObjects[type] != null) {
			try {
				callbackQueue.put(data);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}

		// Message seems to be OK, but can't be handled, most likely
		// a callback without registered function
		return length;
	}
	
	protected byte getStackIDFromData(byte[] data) {
		return data[0];
	}
	
	protected byte getTypeFromData(byte[] data) {
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
			recvLoopThread.join();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	
	public void write(Device device, ByteBuffer bb, byte type, boolean hasReturn) {
		try {
			device.semaphoreWrite.acquire();
		} catch (InterruptedException e) {
			e.printStackTrace();
			return;
		}
		
		if(hasReturn) {
			device.answerType = type;
		}
		
		try {
			out.write(bb.array());
		}
		catch(java.io.IOException e) {
			e.printStackTrace();
			return;
		}
		
		if(!hasReturn) {
			device.semaphoreWrite.release();
		}
		
	}
	
	private int handleAddDevice(byte[] data) {
		int length = getLengthFromData(data);
		
		if(addDevice == null) {
			return length;
		}
		
		ByteBuffer bb = ByteBuffer.wrap(data, 4, length - 4);
		bb.order(ByteOrder.LITTLE_ENDIAN);


		long uid = bb.getLong();
		if(addDevice.uid == uid) {

			addDevice.firmwareVersion[0] = IPConnection.unsignedByte(bb.get());
			addDevice.firmwareVersion[1] = IPConnection.unsignedByte(bb.get());
			addDevice.firmwareVersion[2] = IPConnection.unsignedByte(bb.get());

			addDevice.name = new String("");
			for(int i = 0; i < 40; i++) {
				addDevice.name += (char)bb.get();
			}

			addDevice.stackID = unsignedByte(bb.get());
			devices[addDevice.stackID] = addDevice;
			addDevice.semaphoreAnswer.release();
			addDevice = null;
		}
		
		return length;
	}
	
	private int handleEnumerate(byte[] data) {
		int length = getLengthFromData(data);
		
		if(enumerateListener == null) {
			return length;
		}

		try {
			callbackQueue.put(data);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}

		
		return length;
	}

	public void destroy() {
		recvLoopFlag = false;
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
		ByteBuffer bb = ByteBuffer.allocate(4);
		bb.order(ByteOrder.LITTLE_ENDIAN);
		bb.put(BROADCAST_ADDRESS);
		bb.put(TYPE_ENUMERATE);
		bb.putShort(ENUMERATE_LENGTH);

		this.enumerateListener = enumerateListener;
		
		try {
			out.write(bb.array());
		}
		catch(java.io.IOException e) {
			e.printStackTrace();
		}
	}

	public void addDevice(Device device) throws IPConnection.TimeoutException {
		ByteBuffer bb = ByteBuffer.allocate(12);
		bb.order(ByteOrder.LITTLE_ENDIAN);
		bb.put(BROADCAST_ADDRESS);
		bb.put(TYPE_GET_STACK_ID);
		bb.putShort(GET_STACK_ID_LENGTH);
		bb.putLong(device.uid);
		
		addDevice = device;
		
		try {
			out.write(bb.array());
		}
		catch(java.io.IOException e) {
			e.printStackTrace();
		}

		try {
			if(!addDevice.semaphoreAnswer.tryAcquire(TIMEOUT_ADD_DEVICE, TimeUnit.MILLISECONDS)) {
				throw new IPConnection.TimeoutException("Did not receive answer for addDevice in time");
			}
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		
		device.ipcon = this;
	}
	
	public static String base58Encode(long value) {
		String encoded = new String("");
		while(value >= 58) {
			long div = value/58;
			int mod = (int)(value % 58);
			encoded = BASE58.charAt(mod) + encoded;
			value = div;
		}
		
		encoded = BASE58.charAt((int)value) + encoded; 
		return encoded;
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
