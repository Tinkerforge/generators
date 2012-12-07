/*
 * Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
 * Copyright (C) 2011-2012 Olaf Lüke <olaf@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file, 
 * with or without modification, are permitted.
 */

package com.tinkerforge;

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
		setDaemon(true);
		this.ipcon = ipcon;
	}

	public void run() {
		byte[] pendingData = new byte[8192];
		int pendingLength = 0;

		try {
			ipcon.in = ipcon.socket.getInputStream();
		} catch(java.io.IOException e) {
			e.printStackTrace();
			return;
		}

		while(ipcon.receiveFlag) {
			int length;

			try {
				length = ipcon.in.read(pendingData, pendingLength,
				                       pendingData.length - pendingLength);
			} catch(java.net.SocketException e) {
				ipcon.autoReconnectAllowed = true;
				ipcon.receiveFlag = false;
				ByteBuffer bb = ByteBuffer.allocate(8);
				bb.putInt(ipcon.CALLBACK_DISCONNECTED);
				bb.putInt(ipcon.DISCONNECT_REASON_ERROR);

				try {
					ipcon.callbackQueue.put(new IPConnection.CallbackQueueObject(ipcon.QUEUE_META, bb.array()));
				} catch(java.lang.InterruptedException e2) {
				}
				return;
			} catch(java.io.IOException e) {
				if(ipcon.receiveFlag) {
					ipcon.receiveFlag = false;
					e.printStackTrace();
				}
				return;
			}

			if(length == 0 || length == -1) {
				if(ipcon.receiveFlag) {
					ipcon.autoReconnectAllowed = true;
					ipcon.receiveFlag = false;
					ByteBuffer bb = ByteBuffer.allocate(8);
					bb.putInt(ipcon.CALLBACK_DISCONNECTED);

					if(length == 0) {
						bb.putInt(ipcon.DISCONNECT_REASON_SHUTDOWN);
					} else {
						bb.putInt(ipcon.DISCONNECT_REASON_ERROR);
					}

					try {
						ipcon.callbackQueue.put(new IPConnection.CallbackQueueObject(ipcon.QUEUE_META, bb.array()));
					} catch(java.lang.InterruptedException e2) {
					}
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
		setDaemon(true);
		this.ipcon = ipcon;
	}

	public void run() {
		while(ipcon.callbackThreadFlag) {
			IPConnection.CallbackQueueObject cqo = null;
			try {
				cqo = ipcon.callbackQueue.take();
			} catch(InterruptedException e) {
				e.printStackTrace();
				continue;
			}

			if(cqo == null) {
				continue;
			}

			switch(cqo.kind) {
				case IPConnection.QUEUE_EXIT: {
					return;
				}

				case IPConnection.QUEUE_META: {
					ByteBuffer bb = ByteBuffer.wrap(cqo.data, 0, 8);
					bb.order(ByteOrder.LITTLE_ENDIAN);

					int functionId = bb.getInt();
					int parameter = bb.getInt();
					
					switch(functionId) {
						case IPConnection.CALLBACK_CONNECTED:
							if(ipcon.connectedListener != null) {
								ipcon.connectedListener.connected(parameter);
							}

							break;

						case IPConnection.CALLBACK_DISCONNECTED:
							synchronized(ipcon.socketMutex) {
								try {
									if(ipcon.socket != null) {
										ipcon.socket.close();
										ipcon.socket = null;
									}
								} catch(java.io.IOException e) {
									e.printStackTrace();
								}
							}

							try {
								Thread.sleep(100);
							} catch(java.lang.InterruptedException e) {
								e.printStackTrace();
							}

							if(ipcon.disconnectedListener != null) {
								ipcon.disconnectedListener.disconnected(parameter);
							}

							if(parameter != IPConnection.DISCONNECT_REASON_REQUEST && ipcon.autoReconnect && ipcon.autoReconnectAllowed) {
								ipcon.autoReconnectPending = true;
								boolean retry = true;

								while(retry) {
									retry = false;

									synchronized(ipcon.socketMutex) {
										if(ipcon.autoReconnectAllowed && ipcon.socket == null) {
											try {
												ipcon.connectUnlocked(true);
											} catch(Exception e) {
												retry = true;
											}
										} else {
											ipcon.autoReconnectPending = true;
										}
									}

									if(retry) {
										try {
											Thread.sleep(100);
										} catch(java.lang.InterruptedException e) {
											e.printStackTrace();
										}
									}
								}
							}

							break;
					}

					break;
				}

				case IPConnection.QUEUE_PACKET: {
					if (!ipcon.callbackThreadFlag) {
						return;
					}

					byte functionID = ipcon.getFunctionIDFromData(cqo.data);
					if(functionID == IPConnection.CALLBACK_ENUMERATE) {
						if(ipcon.enumerateListener != null) {
							int length = ipcon.getLengthFromData(cqo.data);
							ByteBuffer bb = ByteBuffer.wrap(cqo.data, 8, length - 8);
							bb.order(ByteOrder.LITTLE_ENDIAN);
							String UID = "";
							for(int i = 0; i < 8; i++) {
								char c = (char)bb.get();
								if(c != '\0') {
									UID += c;
								}
							}
							String connectedUID = "";
							for(int i = 0; i < 8; i++) {
								char c = (char)bb.get();
								if(c != '\0') {
									connectedUID += c;
								}
							}
							char position = (char)bb.get();
							short[] hardwareVersion = new short[3];
							hardwareVersion[0] = ipcon.unsignedByte(bb.get());
							hardwareVersion[1] = ipcon.unsignedByte(bb.get());
							hardwareVersion[2] = ipcon.unsignedByte(bb.get());
							short[] firmwareVersion = new short[3];
							firmwareVersion[0] = ipcon.unsignedByte(bb.get());
							firmwareVersion[1] = ipcon.unsignedByte(bb.get());
							firmwareVersion[2] = ipcon.unsignedByte(bb.get());
							int deviceIdentifier = ipcon.unsignedShort(bb.getShort());
							short enumerationType = ipcon.unsignedByte(bb.get());

							ipcon.enumerateListener.enumerate(UID, connectedUID, position, hardwareVersion, firmwareVersion, deviceIdentifier, enumerationType);
						}
					} else {
						long uid = ipcon.getUIDFromData(cqo.data);
						Device device = ipcon.devices.get(uid);
						if(device.callbacks[functionID] != null) {
							device.callbacks[functionID].callback(cqo.data);
						}
					}
					
					break;
				}
			}
		}
	}
}

public class IPConnection {
	private final static String BASE58 = "123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ";

	public final static byte FUNCTION_ENUMERATE = (byte)254;
	public final static byte FUNCTION_ADC_CALIBRATE = (byte)251;
	public final static byte FUNCTION_GET_ADC_CALIBRATION = (byte)250;
	public final static byte CALLBACK_ENUMERATE = (byte)253;

	public final static byte CALLBACK_CONNECTED = (byte)0;
	public final static byte CALLBACK_DISCONNECTED = (byte)1;
	public final static byte CALLBACK_AUTHENTICATION_ERROR = (byte)2;

	private final static long BROADCAST_UID = (long)0;

	// enumeration_type parameter to the enumerate callback
    public final static short ENUMERATION_TYPE_AVAILABLE = 0;
    public final static short ENUMERATION_TYPE_CONNECTED = 1;
    public final static short ENUMERATION_TYPE_DISCONNECTED = 2;

    // connect_reason parameter to the connected callback
    public final static int CONNECT_REASON_REQUEST = 0;
    public final static int CONNECT_REASON_AUTO_RECONNECT = 1;

    // disconnect_reason parameter to the disconnected callback
    public final static int DISCONNECT_REASON_REQUEST = 0;
    public final static int DISCONNECT_REASON_ERROR = 1;
    public final static int DISCONNECT_REASON_SHUTDOWN = 2;

    // returned by get_connection_state
    public final static int CONNECTION_STATE_DISCONNECTED = 0;
    public final static int CONNECTION_STATE_CONNECTED = 1;
    public final static int CONNECTION_STATE_PENDING = 2; // auto-reconnect in process

    protected final static int QUEUE_EXIT = 0;
    protected final static int QUEUE_META = 1;
    protected final static int QUEUE_PACKET = 2;

	protected int response_timeout = 2500;

	protected Hashtable<Long, Device> devices = new Hashtable<Long, Device>();
	protected LinkedBlockingQueue<CallbackQueueObject> callbackQueue = null;

	protected Object socketMutex = new Object();
	private Object sequenceNumberMutex = new Object();

	private String host;
	private int port;

	protected final static int SEQENCE_NUMBER_POS = 4;
	protected byte nextSequenceNumber = 1;

	boolean receiveFlag = false;
	boolean callbackThreadFlag = false;

	boolean autoReconnect = true;
	boolean autoReconnectAllowed = false;
	boolean autoReconnectPending = false;
	Socket socket = null;
	OutputStream out = null;
	InputStream in = null;
	protected EnumerateListener enumerateListener = null;
	protected ConnectedListener connectedListener = null;
	protected DisconnectedListener disconnectedListener = null;
	ReceiveThread receiveThread = null;
	CallbackThread callbackThread = null;

	public static class CallbackQueueObject {
 		public final int kind; 
  		public final byte[] data; 
  		public CallbackQueueObject(int kind, byte[] data) { 
    		this.kind = kind; 
    		this.data = data; 
  		} 
	}

	public static class TimeoutException extends Exception {
		private static final long serialVersionUID = 1L;

		TimeoutException(String string) {
			super(string);
		}
	}

	public interface EnumerateListener {
		public void enumerate(String UID, String connectedUID, char position, short[] hardwareVersion, short[] firmwareVersion, int deviceIdentifier, short enumerationType);
	}

	public interface ConnectedListener {
		public void connected(int reason);
	}

	public interface DisconnectedListener {
		public void disconnected(int reason);
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
	public IPConnection() {

	}

	public void addListener(Object o) {
		if(o instanceof EnumerateListener) {
			enumerateListener = (EnumerateListener)o;
		} else if(o instanceof ConnectedListener) {
			connectedListener = (ConnectedListener)o;
		} else if(o instanceof DisconnectedListener) {
			disconnectedListener = (DisconnectedListener)o;
		}
	}

	public void connect(String host, int port) throws java.net.UnknownHostException, java.io.IOException {
		synchronized(socketMutex) {
			this.host = host;
			this.port = port;

			try {
				connectUnlocked(false);
			} catch(java.io.IOException e) {
				throw(e);
			}
		}
	}

	void connectUnlocked(boolean isAutoReconnect) throws java.net.UnknownHostException, java.io.IOException {
		if(callbackThread == null) {
			callbackQueue = new LinkedBlockingQueue<CallbackQueueObject>();
			callbackThread = new CallbackThread(this);
			callbackThreadFlag = true;
			callbackThread.start();
		}

		if(socket == null) {
			try {
				socket = new Socket(host, port);
				out = socket.getOutputStream();
				out.flush();
			} catch(java.io.IOException e) {
				socket = null;
				out = null;
				throw(e);
			}
		}

		if(receiveThread == null) {
			receiveThread = new ReceiveThread(this);
			receiveFlag = true;
			receiveThread.start();
		}

		int connectReason = IPConnection.CONNECT_REASON_REQUEST;
		if(isAutoReconnect) {
			connectReason = CONNECT_REASON_AUTO_RECONNECT;
		}
		
		autoReconnectAllowed = false;
		autoReconnectPending = false;

		ByteBuffer bb = ByteBuffer.allocate(8);
		bb.putInt(CALLBACK_CONNECTED);
		bb.putInt(connectReason);

		try {
			callbackQueue.put(new CallbackQueueObject(QUEUE_META, bb.array()));
		} catch(java.lang.InterruptedException e) {
		}
	}

	public void disconnect() {
		CallbackThread callbackThreadTmp = null;
		LinkedBlockingQueue<CallbackQueueObject> callbackQueueTmp = null;

		synchronized(socketMutex) {
			autoReconnectAllowed = false;

			if(autoReconnectPending) {
				autoReconnectPending = false;
			} else {
				if(socket == null) {
					// FIXME: throw not-connected exception
					return;
				}

				receiveFlag = false;

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
					if(socket != null) {
						socket.close();
						socket = null;
					}
				} catch(java.io.IOException e) {
					e.printStackTrace();
				}

				if(receiveThread != null) {
					try {
						receiveThread.join();
					} catch(java.lang.InterruptedException e) {
						e.printStackTrace();
					}
				}

				receiveThread = null;
			}

			callbackThreadTmp = callbackThread;
			callbackQueueTmp = callbackQueue;

			callbackThread = null;
			callbackQueue = null;
		}

		ByteBuffer bb = ByteBuffer.allocate(8);
		bb.putInt(CALLBACK_DISCONNECTED);
		bb.putInt(DISCONNECT_REASON_REQUEST);

		try {
			callbackQueueTmp.put(new CallbackQueueObject(QUEUE_META, bb.array()));
		} catch(InterruptedException e) {
			e.printStackTrace();
		}

		try {
			callbackQueueTmp.put(new CallbackQueueObject(QUEUE_EXIT, null));
		} catch(InterruptedException e) {
			e.printStackTrace();
		}

		if(Thread.currentThread() != callbackThreadTmp) {
			try {
				callbackThreadTmp.join();
			} catch(InterruptedException e) {
				e.printStackTrace();
			}
		}
	}

	public byte getConnectionState() {
		if(socket != null) {
			return CONNECTION_STATE_CONNECTED;
		}

		if(autoReconnectPending) {
			return IPConnection.CONNECTION_STATE_PENDING;
		}

		return IPConnection.CONNECTION_STATE_DISCONNECTED;
	}

	public void setAutoReconnect(boolean autoReconnect) {
		this.autoReconnect = autoReconnect;

		if(!autoReconnect) {
			autoReconnectAllowed = false;
		}
	}

	public boolean getAutoReconnect() {
		return autoReconnect;
	}

	public void setTimeout(int timeout) {
		if(timeout < 0) {
			throw new IllegalArgumentException("Timeout cannot be negative");
		}

		response_timeout = timeout;
	}

	public int getTimeout() {
		return response_timeout;
	}

	void handleResponse(byte[] packet) {
		byte functionID = getFunctionIDFromData(packet);
		short sequenceNumber = unsignedByte(getSequenceNumberFromData(packet));

		if(functionID == CALLBACK_ENUMERATE && sequenceNumber == 0) {
			handleEnumerate(packet);
			return;
		}

		long uid = getUIDFromData(packet);

		if(!devices.containsKey(uid)) {
			// Message for an unknown device, ignoring it
			return;
		}

		Device device = devices.get(uid);

		if(functionID == device.expectedResponseFunctionID &&
		   sequenceNumber == device.expectedResponseSequenceNumber) {
			try {
				device.responseQueue.put(packet);
			} catch(InterruptedException e) {
				e.printStackTrace();
			}
			return;
		}
		
		if(device.callbacks[functionID] != null && sequenceNumber == 0 && device.listenerObjects[functionID] != null) {
			try {
				callbackQueue.put(new CallbackQueueObject(QUEUE_PACKET, packet));
			} catch(InterruptedException e) {
				e.printStackTrace();
			}
		}

		// Response seems to be OK, but can't be handled, most likely
		// a callback without registered listener
	}

	protected static long getUIDFromData(byte[] data) {
		return (long)(data[0] & 0xFF) | ((long)(data[1] & 0xFF) << 8) | ((long)(data[2] & 0xFF) << 16) | ((long)(data[3] & 0xFF) << 24);
	}

	protected static byte getLengthFromData(byte[] data) {
		return data[4];
	}

	protected static byte getFunctionIDFromData(byte[] data) {
		return data[5];
	}

	protected static byte getSequenceNumberFromData(byte[] data) {
		return (byte)((((int)data[6]) >> 4) & 0x0F);
	}

	protected static byte getErrorCodeFromData(byte[] data) {
		return (byte)(((int)(data[7] >> 6)) & 0x03);
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

	public void write(byte[] data) {
		try {
			out.write(data);
		} catch(java.io.IOException e) {
			e.printStackTrace();
			return;
		}
	}

	private void handleEnumerate(byte[] packet) {
		synchronized(socketMutex) {
			if(enumerateListener != null) {
				try {
					callbackQueue.put(new IPConnection.CallbackQueueObject(QUEUE_PACKET, packet));
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
			}
		}
	}

	/**
	 * This method registers the following listener:
	 *
	 * \code
	 * public class IPConnection.EnumerateListener() {
	 *   public void enumerate(String UID, String connectedUID, char position, short[3] hardwareVersion, short[3] firmwareVersion, int device_identifier, short enumerationType)
	 * }
	 * \endcode
	 *
	 * The listener receives four parameters:
	 *
	 * - \c uid: The UID of the device.
	 * - \c connectedUID: UID where the device is connected to. For a Bricklet this will be a UID of the Brick where it is connected to. For a Brick it will be the UID of the bottom Master Brick in the stack. For the bottom Master Brick in a Stack this will be “1”. With this information it is possible to reconstruct the complete network topology. 
	 * - \c position: Position in stack. For Bricks: ‘0’ - ‘8’ (position in stack). For Bricklets: ‘a’ - ‘d’ (position on Brick).
	 * - \c hardwareVersion: Major, minor and release number for hardware version.
	 * - \c firmwareVersion: Major, minor and release number for firmware version.
	 * - \c device_identifier: A number that represents the Brick, instead of the name of the Brick (easier to parse).
	 * - \c enumerationType: Type of enumeration
	 *
	 * Possible enumerate types:
     *
	 * ENUMERATION_TYPE_AVAILABLE (0): Device is available (enumeration triggered by user).
     * ENUMERATION_TYPE_CONNECTED (1): Device is newly connected (automatically send by Brick after establishing a communication connection). This indicates that the device has potentially lost its previous configuration and needs to be reconfigured.
     * ENUMERATION_TYPE_DISCONNECTED (2): Device is disconnected (only possible for USB connection).
	 *
	 * It should be possible to implement "plug 'n play" functionality with this
	 * (as is done in Brick Viewer).
	 */
	public void enumerate() {
		synchronized(socketMutex) {
			ByteBuffer request = createRequestBuffer(BROADCAST_UID, (byte)8, FUNCTION_ENUMERATE, (byte)0, (byte)0);

			try {
				out.write(request.array());
			} catch(java.io.IOException e) {
				e.printStackTrace();
			}
		}
	}

	ByteBuffer createRequestBuffer(long uid, byte length, int functionID, byte options, byte flags) {
		synchronized(sequenceNumberMutex) {
			options |= nextSequenceNumber << SEQENCE_NUMBER_POS;

			nextSequenceNumber++;
			if(nextSequenceNumber == 0 || nextSequenceNumber > 15) {
				nextSequenceNumber = 1;
			}
		}

		ByteBuffer buffer = ByteBuffer.allocate(length);

		buffer.order(ByteOrder.LITTLE_ENDIAN);
		buffer.putInt((int)uid);
		buffer.put(length);
		buffer.put((byte)functionID);
		buffer.put(options);
		buffer.put(flags);

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
