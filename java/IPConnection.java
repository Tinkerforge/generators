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

		while(ipcon.receiveFlag) {
			int length;

			try {
				length = ipcon.in.read(pendingData, pendingLength,
				                       pendingData.length - pendingLength);
			} catch(java.net.SocketException e) {
				if(ipcon.receiveFlag) {
					ipcon.autoReconnectAllowed = true;
					ipcon.receiveFlag = false;
					ByteBuffer bb = ByteBuffer.allocate(3);
					bb.order(ByteOrder.LITTLE_ENDIAN);
					bb.put(IPConnection.CALLBACK_DISCONNECTED);
					bb.putShort(IPConnection.DISCONNECT_REASON_ERROR);

					try {
						ipcon.callbackQueue.put(new IPConnection.CallbackQueueObject(ipcon.QUEUE_META, bb.array()));
					} catch(java.lang.InterruptedException e2) {
					}
				}
				return;
			} catch(java.io.IOException e) {
				if(ipcon.receiveFlag) {
					ipcon.receiveFlag = false;
					e.printStackTrace();
				}
				return;
			}

			if(length <= 0) {
				if(ipcon.receiveFlag) {
					ipcon.autoReconnectAllowed = true;
					ipcon.receiveFlag = false;
					ByteBuffer bb = ByteBuffer.allocate(8);
					bb.order(ByteOrder.LITTLE_ENDIAN);
					bb.put(IPConnection.CALLBACK_DISCONNECTED);
					bb.putShort(IPConnection.DISCONNECT_REASON_SHUTDOWN);

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
	LinkedBlockingQueue<IPConnection.CallbackQueueObject> callbackQueue = null;

	CallbackThread(IPConnection ipcon,
	               LinkedBlockingQueue<IPConnection.CallbackQueueObject> callbackQueue) {
		setDaemon(true);
		this.ipcon = ipcon;
		this.callbackQueue = callbackQueue;
	}

	public void run() {
		while(true) {
			IPConnection.CallbackQueueObject cqo = null;
			try {
				cqo = callbackQueue.take();
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
					ByteBuffer bb = ByteBuffer.wrap(cqo.data, 0, 3);
					bb.order(ByteOrder.LITTLE_ENDIAN);

					byte id = bb.get();
					short parameter = bb.getShort();

					switch(id) {
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
								ipcon.disconnectedListener.disconnected((short)parameter);
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
					if (!ipcon.receiveFlag) {
						// don't dispatch callbacks when the receive thread isn't running
						continue;
					}

					byte functionID = ipcon.getFunctionIDFromData(cqo.data);
					if(functionID == IPConnection.CALLBACK_ENUMERATE) {
						if(ipcon.enumerateListener != null) {
							int length = ipcon.getLengthFromData(cqo.data);
							ByteBuffer bb = ByteBuffer.wrap(cqo.data, 8, length - 8);
							bb.order(ByteOrder.LITTLE_ENDIAN);
							String uid_str = "";
							for(int i = 0; i < 8; i++) {
								char c = (char)bb.get();
								if(c != '\0') {
									uid_str += c;
								}
							}
							String connectedUid_str = "";
							for(int i = 0; i < 8; i++) {
								char c = (char)bb.get();
								if(c != '\0') {
									connectedUid_str += c;
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

							ipcon.enumerateListener.enumerate(uid_str, connectedUid_str, position,
							                                  hardwareVersion, firmwareVersion,
							                                  deviceIdentifier, enumerationType);
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
	public final static short CONNECT_REASON_REQUEST = 0;
	public final static short CONNECT_REASON_AUTO_RECONNECT = 1;

	// disconnect_reason parameter to the disconnected callback
	public final static short DISCONNECT_REASON_REQUEST = 0;
	public final static short DISCONNECT_REASON_ERROR = 1;
	public final static short DISCONNECT_REASON_SHUTDOWN = 2;

	// returned by get_connection_state
	public final static short CONNECTION_STATE_DISCONNECTED = 0;
	public final static short CONNECTION_STATE_CONNECTED = 1;
	public final static short CONNECTION_STATE_PENDING = 2; // auto-reconnect in process

	final static int QUEUE_EXIT = 0;
	final static int QUEUE_META = 1;
	final static int QUEUE_PACKET = 2;

	int responseTimeout = 2500;

	Hashtable<Long, Device> devices = new Hashtable<Long, Device>();
	LinkedBlockingQueue<CallbackQueueObject> callbackQueue = null;

	Object socketMutex = new Object();
	private Object sequenceNumberMutex = new Object();

	private String host;
	private int port;

	private final static int SEQENCE_NUMBER_POS = 4;
	private byte nextSequenceNumber = 1;

	boolean receiveFlag = false;

	boolean autoReconnect = true;
	boolean autoReconnectAllowed = false;
	boolean autoReconnectPending = false;
	Socket socket = null;
	OutputStream out = null;
	InputStream in = null;
	EnumerateListener enumerateListener = null;
	ConnectedListener connectedListener = null;
	DisconnectedListener disconnectedListener = null;
	ReceiveThread receiveThread = null;
	CallbackThread callbackThread = null;

	static class CallbackQueueObject {
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

	public static class AlreadyConnectedException extends Exception {
		private static final long serialVersionUID = 1L;

		AlreadyConnectedException(String string) {
			super(string);
		}
	}

	public static class NotConnectedException extends Exception {
		private static final long serialVersionUID = 1L;

		NotConnectedException() {
		}
	}

	public interface EnumerateListener {
		public void enumerate(String uid, String connectedUid, char position,
		                      short[] hardwareVersion, short[] firmwareVersion,
		                      int deviceIdentifier, short enumerationType);
	}

	public interface ConnectedListener {
		public void connected(short disconnectReason);
	}

	public interface DisconnectedListener {
		public void disconnected(short disconnectReason);
	}

	/**
	 * Creates an IP Connection object that can be used to enumerate the available
	 * devices. It is also required for the constructor of Bricks and Bricklets.
	 */
	public IPConnection() {
	}

	/**
	 * Creates a TCP/IP connection to the given \c host and \c port. The host
	 * and port can point to a Brick Daemon or to a WIFI/Ethernet Extension.
	 *
	 * Devices can only be controlled when the connection was established
	 * successfully.
	 *
	 * Blocks until the connection is established and throws an exception if
	 * there is no Brick Daemon or WIFI/Ethernet Extension listening at the
	 * given host and port.
	 */
	public void connect(String host, int port) throws java.net.UnknownHostException, java.io.IOException, AlreadyConnectedException {
		synchronized(socketMutex) {
			if (socket != null) {
				throw new AlreadyConnectedException("Already connected to " + this.host + ":" + this.port);
			}

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
			callbackThread = new CallbackThread(this, callbackQueue);
			callbackThread.start();
		}

		try {
			socket = new Socket(host, port);
			in = socket.getInputStream();
			out = socket.getOutputStream();
			out.flush();
		} catch(java.net.UnknownHostException e) {
			socket = null;
			in = null;
			out = null;
			throw(e);
		} catch(java.io.IOException e) {
			socket = null;
			in = null;
			out = null;
			throw(e);
		}

		receiveFlag = true;
		receiveThread = new ReceiveThread(this);
		receiveThread.start();

		autoReconnectAllowed = false;
		autoReconnectPending = false;

		short connectReason = IPConnection.CONNECT_REASON_REQUEST;
		if(isAutoReconnect) {
			connectReason = CONNECT_REASON_AUTO_RECONNECT;
		}

		ByteBuffer bb = ByteBuffer.allocate(3);
		bb.order(ByteOrder.LITTLE_ENDIAN);
		bb.put(CALLBACK_CONNECTED);
		bb.putShort(connectReason);

		try {
			callbackQueue.put(new CallbackQueueObject(QUEUE_META, bb.array()));
		} catch(java.lang.InterruptedException e) {
		}
	}

	/**
	 * Disconnects the TCP/IP connection from the Brick Daemon or the
	 * WIFI/Ethernet Extension.
	 */
	public void disconnect() throws NotConnectedException {
		CallbackThread callbackThreadTmp = null;
		LinkedBlockingQueue<CallbackQueueObject> callbackQueueTmp = null;

		synchronized(socketMutex) {
			autoReconnectAllowed = false;

			if(autoReconnectPending) {
				autoReconnectPending = false;
			} else {
				if(socket == null) {
					throw new NotConnectedException();
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

		ByteBuffer bb = ByteBuffer.allocate(3);
		bb.order(ByteOrder.LITTLE_ENDIAN);
		bb.put(CALLBACK_DISCONNECTED);
		bb.putShort(DISCONNECT_REASON_REQUEST);

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

	/**
	 * Can return the following states:
	 *
	 * - CONNECTION_STATE_DISCONNECTED: No connection is established.
	 * - CONNECTION_STATE_CONNECTED: A connection to the Brick Daemon or
	 *   the WIFI/Ethernet Extension is established.
	 * - CONNECTION_STATE_PENDING: IP Connection is currently trying to
	 *   connect.
	 */
	public short getConnectionState() {
		if(socket != null) {
			return CONNECTION_STATE_CONNECTED;
		}

		if(autoReconnectPending) {
			return CONNECTION_STATE_PENDING;
		}

		return CONNECTION_STATE_DISCONNECTED;
	}

	/**
	 * Enables or disables auto-reconnect. If auto-reconnect is enabled,
	 * the IP Connection will try to reconnect to the previously given
	 * host and port, if the connection is lost.
	 *
	 * Default value is *true*.
	 */
	public void setAutoReconnect(boolean autoReconnect) {
		this.autoReconnect = autoReconnect;

		if(!autoReconnect) {
			autoReconnectAllowed = false;
		}
	}

	/**
	 * Returns *true* if auto-reconnect is enabled, *false* otherwise.
	 */
	public boolean getAutoReconnect() {
		return autoReconnect;
	}

	/**
	 * Sets the timeout in milliseconds for getters and for setters for which the
	 * response expected flag is activated.
	 *
	 * Default timeout is 2500.
	 */
	public void setTimeout(int timeout) {
		if(timeout < 0) {
			throw new IllegalArgumentException("Timeout cannot be negative");
		}

		responseTimeout = timeout;
	}

	/**
	 * Returns the timeout as set by setTimeout.
	 */
	public int getTimeout() {
		return responseTimeout;
	}

	/**
	 * Broadcasts an enumerate request. All devices will respond with an enumerate
	 * callback.
	 */
	public void enumerate() throws NotConnectedException {
		synchronized(socketMutex) {
			if(socket == null) {
				throw new NotConnectedException();
			}

			ByteBuffer request = createRequestBuffer(BROADCAST_UID, (byte)8, FUNCTION_ENUMERATE, (byte)0, (byte)0);

			write(request.array());
		}
	}

	/**
	 * Registers a listener object.
	 */
	public void addListener(Object object) {
		if(object instanceof EnumerateListener) {
			enumerateListener = (EnumerateListener)object;
		} else if(object instanceof ConnectedListener) {
			connectedListener = (ConnectedListener)object;
		} else if(object instanceof DisconnectedListener) {
			disconnectedListener = (DisconnectedListener)object;
		} else {
			throw new IllegalArgumentException("Unknown listener type");
		}
	}

	void handleResponse(byte[] packet) {
		byte functionID = getFunctionIDFromData(packet);
		short sequenceNumber = unsignedByte(getSequenceNumberFromData(packet));

		if(sequenceNumber == 0 && functionID == CALLBACK_ENUMERATE) {
			handleEnumerate(packet);
			return;
		}

		long uid = getUIDFromData(packet);

		if(!devices.containsKey(uid)) {
			// Message for an unknown device, ignoring it
			return;
		}

		Device device = devices.get(uid);

		if(sequenceNumber == 0) {
			if(device.callbacks[functionID] != null && device.listenerObjects[functionID] != null) {
				try {
					callbackQueue.put(new CallbackQueueObject(QUEUE_PACKET, packet));
				} catch(InterruptedException e) {
					e.printStackTrace();
				}
			}

			return;
		}

		if(functionID == device.expectedResponseFunctionID &&
		   sequenceNumber == device.expectedResponseSequenceNumber) {
			try {
				device.responseQueue.put(packet);
			} catch(InterruptedException e) {
				e.printStackTrace();
			}
			return;
		}

		// Response seems to be OK, but can't be handled, most likely
		// a callback without registered listener
	}

	static long getUIDFromData(byte[] data) {
		return (long)(data[0] & 0xFF) | ((long)(data[1] & 0xFF) << 8) | ((long)(data[2] & 0xFF) << 16) | ((long)(data[3] & 0xFF) << 24);
	}

	static byte getLengthFromData(byte[] data) {
		return data[4];
	}

	static byte getFunctionIDFromData(byte[] data) {
		return data[5];
	}

	static byte getSequenceNumberFromData(byte[] data) {
		return (byte)((((int)data[6]) >> 4) & 0x0F);
	}

	static byte getErrorCodeFromData(byte[] data) {
		return (byte)(((int)(data[7] >> 6)) & 0x03);
	}

	static String string(ByteBuffer buffer, int length) {
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

	static short unsignedByte(byte data) {
		return (short)(data & 0xFF);
	}

	static int unsignedShort(short data) {
		return (int)(data & 0xFFFF);
	}

	static long unsignedInt(int data) {
		return (long)(((long)data) & 0xFFFFFFFF);
	}

	void write(byte[] data) {
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
				callbackQueue.put(new IPConnection.CallbackQueueObject(QUEUE_PACKET, packet));
			} catch (InterruptedException e) {
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

	static String base58Encode(long value) {
		String encoded = "";

		while(value >= 58) {
			long div = value / 58;
			int mod = (int)(value % 58);
			encoded = BASE58.charAt(mod) + encoded;
			value = div;
		}

		return BASE58.charAt((int)value) + encoded;
	}

	static long base58Decode(String encoded) {
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
