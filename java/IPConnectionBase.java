/*
 * Copyright (C) 2012-2014 Matthias Bolte <matthias@tinkerforge.com>
 * Copyright (C) 2011-2012 Olaf Lüke <olaf@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

package com.tinkerforge;

import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;
import java.util.Hashtable;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.security.SecureRandom;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

class ReceiveThread extends Thread {
	IPConnectionBase ipcon = null;

	ReceiveThread(IPConnectionBase ipcon) {
		super("Brickd-Receiver");

		setDaemon(true);
		this.ipcon = ipcon;
	}

	@Override
	public void run() {
		byte[] pendingData = new byte[8192];
		int pendingLength = 0;
		long socketID = ipcon.socketID;

		while(ipcon.receiveFlag) {
			int length;

			try {
				length = ipcon.in.read(pendingData, pendingLength,
				                       pendingData.length - pendingLength);
			} catch(java.net.SocketException e) {
				if(ipcon.receiveFlag) {
					ipcon.handleDisconnectByPeer(IPConnectionBase.DISCONNECT_REASON_ERROR,
					                             socketID, false);
				}
				return;
			} catch(Exception e) {
				if(ipcon.receiveFlag) {
					e.printStackTrace();
				}
				return;
			}

			if(length <= 0) {
				if(ipcon.receiveFlag) {
					ipcon.handleDisconnectByPeer(IPConnectionBase.DISCONNECT_REASON_SHUTDOWN,
					                             socketID, false);
				}
				return;
			}

			pendingLength += length;

			while(ipcon.receiveFlag) {
				if(pendingLength < 8) {
					// Wait for complete header
					break;
				}

				length = IPConnectionBase.getLengthFromData(pendingData);

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

class CallbackThreadRestarter implements Thread.UncaughtExceptionHandler {
	IPConnectionBase ipcon = null;

	CallbackThreadRestarter(IPConnectionBase ipcon) {
		this.ipcon = ipcon;
	}

	@Override
	public void uncaughtException(Thread thread, Throwable exception) {
		System.err.print("Exception in thread \"" + thread.getName() + "\" ");
		exception.printStackTrace();

		ipcon.callbackThread = new CallbackThread(ipcon, ((CallbackThread)thread).callbackQueue);
		ipcon.callbackThread.start();
	}
}

class CallbackThread extends Thread {
	IPConnectionBase ipcon = null;
	LinkedBlockingQueue<IPConnectionBase.CallbackQueueObject> callbackQueue = null;
	Object mutex = new Object();
	boolean packetDispatchAllowed = false;

	CallbackThread(IPConnectionBase ipcon,
	               LinkedBlockingQueue<IPConnectionBase.CallbackQueueObject> callbackQueue) {
		super("Callback-Processor");

		setDaemon(true);
		this.ipcon = ipcon;
		this.callbackQueue = callbackQueue;
		this.setUncaughtExceptionHandler(new CallbackThreadRestarter(ipcon));
	}

	void setPacketDispatchAllowed(boolean allowed) {
		if (allowed) {
			packetDispatchAllowed = true;
		} else {
			if (Thread.currentThread() != this) {
				// FIXME: cannot lock callback mutex here because this can
				//        deadlock due to an ordering problem with the socket mutex
				/*synchronized(mutex)*/ {
					packetDispatchAllowed = false;
				}
			} else {
				packetDispatchAllowed = false;
			}
		}
	}

	void dispatchMeta(IPConnectionBase.CallbackQueueObject cqo) {
		switch(cqo.functionID) {
			case IPConnectionBase.CALLBACK_CONNECTED:
				ipcon.callConnectedListeners(cqo.parameter);

				break;

			case IPConnectionBase.CALLBACK_DISCONNECTED:
				// need to do this here, the receive loop is not allowed to
				// hold the socket mutex because this could cause a deadlock
				// with a concurrent call to the (dis-)connect function
				if(cqo.parameter != IPConnectionBase.DISCONNECT_REASON_REQUEST) {
					synchronized(ipcon.socketMutex) {
						// don't close the socket if it got disconnected or
						// reconnected in the meantime
						if (ipcon.socket != null && ipcon.socketID == cqo.socketID) {
							ipcon.disconnectProbeThread.shutdown();
							try {
								ipcon.disconnectProbeThread.join();
							} catch(InterruptedException e) {
								e.printStackTrace();
							}

							ipcon.closeSocket();
						}
					}
				}

				try {
					Thread.sleep(100);
				} catch(InterruptedException e) {
					e.printStackTrace();
				}

				ipcon.callDisconnectedListeners(cqo.parameter);

				if(cqo.parameter != IPConnectionBase.DISCONNECT_REASON_REQUEST &&
				   ipcon.autoReconnect && ipcon.autoReconnectAllowed) {
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
							} catch(InterruptedException e) {
								e.printStackTrace();
							}
						}
					}
				}

				break;
		}
	}

	void dispatchPacket(IPConnectionBase.CallbackQueueObject cqo) {
		byte functionID = IPConnectionBase.getFunctionIDFromData(cqo.packet);

		if(functionID == IPConnectionBase.CALLBACK_ENUMERATE) {
			if(ipcon.hasEnumerateListeners()) {
				int length = IPConnectionBase.getLengthFromData(cqo.packet);
				ByteBuffer bb = ByteBuffer.wrap(cqo.packet, 8, length - 8);
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
				hardwareVersion[0] = IPConnectionBase.unsignedByte(bb.get());
				hardwareVersion[1] = IPConnectionBase.unsignedByte(bb.get());
				hardwareVersion[2] = IPConnectionBase.unsignedByte(bb.get());
				short[] firmwareVersion = new short[3];
				firmwareVersion[0] = IPConnectionBase.unsignedByte(bb.get());
				firmwareVersion[1] = IPConnectionBase.unsignedByte(bb.get());
				firmwareVersion[2] = IPConnectionBase.unsignedByte(bb.get());
				int deviceIdentifier = IPConnectionBase.unsignedShort(bb.getShort());
				short enumerationType = IPConnectionBase.unsignedByte(bb.get());

				ipcon.callEnumerateListeners(uid_str, connectedUid_str, position,
				                             hardwareVersion, firmwareVersion,
				                             deviceIdentifier, enumerationType);
			}
		} else {
			long uid = IPConnectionBase.getUIDFromData(cqo.packet);
			Device device = ipcon.devices.get(uid);
			ipcon.callDeviceListener(device, functionID, cqo.packet);
		}
	}

	@Override
	public void run() {
		while(true) {
			IPConnectionBase.CallbackQueueObject cqo = null;
			try {
				cqo = callbackQueue.take();
			} catch(InterruptedException e) {
				e.printStackTrace();
				continue;
			}

			if(cqo == null) {
				continue;
			}

			// FIXME: cannot lock callback mutex here because this can
			//        deadlock due to an ordering problem with the socket mutex
			/*synchronized(mutex)*/ {
				switch(cqo.kind) {
					case IPConnectionBase.QUEUE_EXIT:
						return;

					case IPConnectionBase.QUEUE_META:
						dispatchMeta(cqo);
						break;

					case IPConnectionBase.QUEUE_PACKET:
						// don't dispatch callbacks when the receive thread isn't running
						if (packetDispatchAllowed) {
							dispatchPacket(cqo);
						}

						break;
				}
			}
		}
	}
}

// NOTE: the disconnect probe thread is not allowed to hold the socketMutex at any
//       time because it is created and joined while the socketMutex is locked
class DisconnectProbeThread extends Thread {
	IPConnectionBase ipcon = null;
	byte[] request = null;
	LinkedBlockingQueue<Boolean> queue = new LinkedBlockingQueue<Boolean>();

	final static byte FUNCTION_DISCONNECT_PROBE = (byte)128;
	final static int DISCONNECT_PROBE_INTERVAL = 5000;

	DisconnectProbeThread(IPConnectionBase ipcon) {
		super("Disconnect-Prober");

		setDaemon(true);
		this.ipcon = ipcon;
		this.request = ipcon.createRequestPacket((byte)8, FUNCTION_DISCONNECT_PROBE, null).array();
	}

	void shutdown() {
		try {
			queue.put(new Boolean(true));
		} catch(InterruptedException e) {
			e.printStackTrace();
		}
	}

	@Override
	public void run() {
		Boolean item = null;

		while (true) {
			try {
				item = queue.poll(DISCONNECT_PROBE_INTERVAL, TimeUnit.MILLISECONDS);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}

			if (item != null) {
				break;
			}

			if (ipcon.disconnectProbeFlag) {
				try {
					synchronized(ipcon.socketSendMutex) {
						ipcon.out.write(request);
					}
				} catch(java.net.SocketException e) {
					ipcon.handleDisconnectByPeer(IPConnectionBase.DISCONNECT_REASON_ERROR,
					                             ipcon.socketID, false);
					break;
				} catch(Exception e) {
					e.printStackTrace();
				}
			} else {
				ipcon.disconnectProbeFlag = true;
			}
		}
	}
}

public abstract class IPConnectionBase {
	private final static String BASE58 = "123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ";

	public final static byte FUNCTION_ENUMERATE = (byte)254;
	public final static byte CALLBACK_ENUMERATE = (byte)253;

	public final static byte CALLBACK_CONNECTED = 0;
	public final static byte CALLBACK_DISCONNECTED = 1;

	private final static int BROADCAST_UID = 0;

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

	BrickDaemon brickd = null;

	int responseTimeout = 2500;

	Hashtable<Long, Device> devices = new Hashtable<Long, Device>();
	LinkedBlockingQueue<CallbackQueueObject> callbackQueue = null;

	Object socketMutex = new Object();
	Object socketSendMutex = new Object();

	private String host;
	private int port;

	private final static int SEQUENCE_NUMBER_POS = 4;
	private int nextSequenceNumber = 0; // protected by sequenceNumberMutex
	private Object sequenceNumberMutex = new Object();

	private long nextAuthenticationNonce = 0; // protected by authenticationMutex
	private Object authenticationMutex = new Object(); // protects authentication handshake

	boolean receiveFlag = false;

	boolean autoReconnect = true;
	boolean autoReconnectAllowed = false;
	boolean autoReconnectPending = false;
	Socket socket = null; // protected by socketMutex
	long socketID = 0; // protected by socketMutex
	OutputStream out = null;
	InputStream in = null;
	ReceiveThread receiveThread = null;
	CallbackThread callbackThread = null;
	DisconnectProbeThread disconnectProbeThread = null;
	boolean disconnectProbeFlag = false;

	static class CallbackQueueObject {
		final int kind;
		final byte functionID;
		final short parameter;
		final long socketID;
		final byte[] packet;

		public CallbackQueueObject(int kind, byte functionID, short parameter,
		                           long socketID, byte[] packet) {
			this.kind = kind;
			this.functionID = functionID;
			this.parameter = parameter;
			this.socketID = socketID;
			this.packet = packet;
		}
	}

	public IPConnectionBase() {
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
	public void connect(String host, int port) throws java.net.UnknownHostException,
	                                                  java.io.IOException,
	                                                  AlreadyConnectedException {
		synchronized(socketMutex) {
			if (socket != null) {
				throw new AlreadyConnectedException("Already connected to " + this.host + ":" + this.port);
			}

			this.host = host;
			this.port = port;

			connectUnlocked(false);
		}
	}

	// NOTE: Assumes that socketMutex is locked
	void connectUnlocked(boolean isAutoReconnect) throws java.net.UnknownHostException,
	                                                     java.io.IOException {
		if(callbackThread == null) {
			callbackQueue = new LinkedBlockingQueue<CallbackQueueObject>();
			callbackThread = new CallbackThread(this, callbackQueue);
			callbackThread.start();
		}

		try {
			socket = new Socket(host, port);
			socket.setTcpNoDelay(true);
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

		++socketID;

		// create disconnect probe thread
		disconnectProbeFlag = true;
		disconnectProbeThread = new DisconnectProbeThread(this);
		disconnectProbeThread.start();

		callbackThread.setPacketDispatchAllowed(true);

		receiveFlag = true;
		receiveThread = new ReceiveThread(this);
		receiveThread.start();

		autoReconnectAllowed = false;
		autoReconnectPending = false;

		short connectReason = IPConnectionBase.CONNECT_REASON_REQUEST;
		if(isAutoReconnect) {
			connectReason = CONNECT_REASON_AUTO_RECONNECT;
		}

		try {
			callbackQueue.put(new CallbackQueueObject(QUEUE_META, CALLBACK_CONNECTED,
			                                          connectReason, 0, null));
		} catch(InterruptedException e) {
			e.printStackTrace();
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

				disconnectUnlocked();
			}

			callbackThreadTmp = callbackThread;
			callbackQueueTmp = callbackQueue;

			callbackThread = null;
			callbackQueue = null;
		}

		try {
			callbackQueueTmp.put(new CallbackQueueObject(QUEUE_META, CALLBACK_DISCONNECTED,
			                                             DISCONNECT_REASON_REQUEST, 0, null));
		} catch(InterruptedException e) {
			e.printStackTrace();
		}

		try {
			callbackQueueTmp.put(new CallbackQueueObject(QUEUE_EXIT, (byte)0,
			                                             (short)0, 0, null));
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

	void disconnectUnlocked() {
		disconnectProbeThread.shutdown();
		try {
			disconnectProbeThread.join();
		} catch(InterruptedException e) {
			e.printStackTrace();
		}

		// stop dispatching packet callbacks before ending the receive
		// thread to avoid timeout exceptions due to callback functions
		// trying to call getters
		callbackThread.setPacketDispatchAllowed(false);

		receiveFlag = false;

		closeSocket();

		if(receiveThread != null) {
			try {
				receiveThread.join();
			} catch(InterruptedException e) {
				e.printStackTrace();
			}

			receiveThread = null;
		}
	}

	/**
	 * FIXME
	 */
	public void authenticate(String secret) throws TimeoutException, NotConnectedException, CryptoException {
		synchronized(authenticationMutex) {
			if (nextAuthenticationNonce == 0) {
				byte[] seed = new SecureRandom().generateSeed(4);
				ByteBuffer bb = ByteBuffer.wrap(seed, 0, 4);

				bb.order(ByteOrder.LITTLE_ENDIAN);
				nextAuthenticationNonce = bb.getInt();
			}

			byte[] serverNonce = brickd.getAuthenticationNonce();
			byte[] clientNonce;
			ByteBuffer bb = ByteBuffer.allocate(4);

			bb.order(ByteOrder.LITTLE_ENDIAN);
			bb.putInt((int)nextAuthenticationNonce);

			clientNonce = bb.array();
			nextAuthenticationNonce = (nextAuthenticationNonce + 1) % ((long)1 << 32);

			byte[] data = new byte[serverNonce.length + clientNonce.length];

			System.arraycopy(serverNonce, 0, data, 0, serverNonce.length);
			System.arraycopy(clientNonce, 0, data, serverNonce.length, clientNonce.length);

			byte[] digest;

			try {
				Mac mac = Mac.getInstance("HmacSHA1");

				mac.init(new SecretKeySpec(secret.getBytes(), "HmacSHA1"));

				digest = mac.doFinal(data);
			} catch (Exception e) {
				throw new CryptoException("Could not generate HMAC-SHA1: " + e.getMessage(), e);
			}

			brickd.authenticate(clientNonce, digest);
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
		ByteBuffer request = createRequestPacket((byte)8, FUNCTION_ENUMERATE, null);

		sendRequest(request.array());
	}

	abstract void callEnumerateListeners(String uid, String connectedUid, char position,
	                                    short[] hardwareVersion, short[] firmwareVersion,
	                                    int deviceIdentifier, short enumerationType);
	abstract boolean hasEnumerateListeners();
	
	abstract void callConnectedListeners(short connectReason);
	
	abstract void callDisconnectedListeners(short disconnectReason);

	abstract void callDeviceListener(Device device, byte functionID, byte[] data);

	void handleResponse(byte[] packet) {
		byte functionID = getFunctionIDFromData(packet);
		short sequenceNumber = unsignedByte(getSequenceNumberFromData(packet));

		disconnectProbeFlag = false;

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
			if(device.callbacks[functionID] != null) {
				try {
					callbackQueue.put(new CallbackQueueObject(QUEUE_PACKET, (byte)0,
					                                          (short)0, 0, packet));
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

		// Response seems to be OK, but can't be handled
	}

	// NOTE: Assumes that socketMutex is locked, if disconnectImmediately is true
	void handleDisconnectByPeer(short disconnectReason, long socketID, boolean disconnectImmediately) {
		autoReconnectAllowed = true;

		if(disconnectImmediately) {
			disconnectUnlocked();
		}

		try {
			callbackQueue.put(new CallbackQueueObject(QUEUE_META, CALLBACK_DISCONNECTED,
			                                          disconnectReason, socketID, null));
		} catch(InterruptedException e) {
			e.printStackTrace();
		}
	}

	// NOTE: Assumes that socketMutex is locked
	void closeSocket() {
		if(in != null) {
			try {
				in.close();
			} catch(java.io.IOException e) {
				e.printStackTrace();
			}
		}

		if(out != null) {
			try {
				out.close();
			} catch(java.io.IOException e) {
				e.printStackTrace();
			}
		}

		if(socket != null) {
			try {
				socket.close();
			} catch(java.io.IOException e) {
				e.printStackTrace();
			}
		}

		in = null;
		out = null;
		socket = null;
	}

	static long getUIDFromData(byte[] data) {
		return (long)(data[0] & 0xFF)        | ((long)(data[1] & 0xFF) << 8) |
		      ((long)(data[2] & 0xFF) << 16) | ((long)(data[3] & 0xFF) << 24);
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

	static boolean getResponseExpectedFromData(byte[] data) {
		return ((((int)data[6]) >> 3) & 0x01) == 0x01;
	}

	static byte getErrorCodeFromData(byte[] data) {
		return (byte)((((int)data[7]) >> 6) & 0x03);
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
		return (short)((short)data & 0xFF);
	}

	static int unsignedShort(short data) {
		return (int)data & 0xFFFF;
	}

	static long unsignedInt(int data) {
		return (long)data & 0xFFFFFFFFL;
	}

	void sendRequest(byte[] request) throws NotConnectedException {
		synchronized(socketMutex) {
			if (getConnectionState() != CONNECTION_STATE_CONNECTED) {
				throw new NotConnectedException();
			}

			try {
				synchronized(socketSendMutex) {
					out.write(request);
				}
			} catch(java.net.SocketException e) {
				handleDisconnectByPeer(DISCONNECT_REASON_ERROR, 0, true);
				throw new NotConnectedException("Disconnected during send operartion: " + e.getMessage(), e);
			} catch(Exception e) {
				e.printStackTrace();
			}

			disconnectProbeFlag = false;
		}
	}

	private void handleEnumerate(byte[] packet) {
		if(hasEnumerateListeners()) {
			try {
				callbackQueue.put(new CallbackQueueObject(QUEUE_PACKET, (byte)0,
				                                          (short)0, 0, packet));
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}

	byte getNextSequenceNumber() {
		synchronized(sequenceNumberMutex) {
			int sequenceNumber = nextSequenceNumber + 1;
			nextSequenceNumber = sequenceNumber % 15;
			return (byte)sequenceNumber;
		}
	}

	ByteBuffer createRequestPacket(byte length, byte functionID, Device device) {
		int uid = BROADCAST_UID;
		byte options = 0;
		byte flags = 0;

		if (device != null) {
			uid = (int)device.uid;

			if (device.getResponseExpected(functionID)) {
				options = 8;
			}
		}

		options |= getNextSequenceNumber() << SEQUENCE_NUMBER_POS;

		ByteBuffer packet = ByteBuffer.allocate(length);

		packet.order(ByteOrder.LITTLE_ENDIAN);
		packet.putInt(uid);
		packet.put(length);
		packet.put(functionID);
		packet.put(options);
		packet.put(flags);

		return packet;
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
		long value = 0;
		long columnMultiplier = 1;

		for(int i = encoded.length() - 1; i >= 0; i--) {
			int column = BASE58.indexOf(encoded.charAt(i));

			if(column < 0) {
				throw new IllegalArgumentException("Invalid Base58 value: " + encoded);
			}

			value += column * columnMultiplier;
			columnMultiplier *= 58;
		}

		return value;
	}
}
