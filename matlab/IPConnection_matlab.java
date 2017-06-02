/*
 * Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

package com.tinkerforge;

import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

public class IPConnection extends IPConnectionBase {
	List<EnumerateListener> listenerEnumerate = new CopyOnWriteArrayList<EnumerateListener>();
	List<ConnectedListener> listenerConnected = new CopyOnWriteArrayList<ConnectedListener>();
	List<DisconnectedListener> listenerDisconnected = new CopyOnWriteArrayList<DisconnectedListener>();

	interface DeviceCallbackListener {
		public void callback(Device device, byte[] packet);
	}

	public class EnumerateCallbackData extends java.util.EventObject {
		private static final long serialVersionUID = 1L;

		public String uid;
		public String connectedUid;
		public char position;
		public short[] hardwareVersion;
		public short[] firmwareVersion;
		public int deviceIdentifier;
		public short enumerationType;

		public EnumerateCallbackData(IPConnection ipcon,
		                             String uid, String connectedUid, char position,
		                             short[] hardwareVersion, short[] firmwareVersion,
		                             int deviceIdentifier, short enumerationType) {
			super(ipcon);

			this.uid = uid;
			this.connectedUid = connectedUid;
			this.position = position;
			this.hardwareVersion = hardwareVersion;
			this.firmwareVersion = firmwareVersion;
			this.deviceIdentifier = deviceIdentifier;
			this.enumerationType = enumerationType;
		}
	}

	public interface EnumerateListener extends TinkerforgeListener {
		public void enumerate(EnumerateCallbackData data);
	}

	public class ConnectedCallbackData extends java.util.EventObject {
		private static final long serialVersionUID = 1L;

		public short connectReason;

		public ConnectedCallbackData(IPConnection ipcon, short connectReason) {
			super(ipcon);

			this.connectReason = connectReason;
		}
	}

	public interface ConnectedListener extends TinkerforgeListener {
		public void connected(ConnectedCallbackData data);
	}

	public class DisconnectedCallbackData extends java.util.EventObject {
		private static final long serialVersionUID = 1L;

		public short disconnectReason;

		public DisconnectedCallbackData(IPConnection ipcon, short disconnectReason) {
			super(ipcon);

			this.disconnectReason = disconnectReason;
		}
	}

	public interface DisconnectedListener extends TinkerforgeListener {
		public void disconnected(DisconnectedCallbackData data);
	}

	/**
	 * Creates an IP Connection object that can be used to enumerate the available
	 * devices. It is also required for the constructor of Bricks and Bricklets.
	 */
	public IPConnection() {
		brickd = new BrickDaemon("2", this);
	}

	/**
	 * Adds a Enumerate listener.
	 */
	public void addEnumerateListener(EnumerateListener listener) {
		listenerEnumerate.add(listener);
	}

	/**
	 * Removes a Enumerate listener.
	 */
	public void removeEnumerateListener(EnumerateListener listener) {
		listenerEnumerate.remove(listener);
	}

	/**
	 * Adds a Connected listener.
	 */
	public void addConnectedListener(ConnectedListener listener) {
		listenerConnected.add(listener);
	}

	/**
	 * Removes a Connected listener.
	 */
	public void removeConnectedListener(ConnectedListener listener) {
		listenerConnected.remove(listener);
	}

	/**
	 * Adds a Disconnected listener.
	 */
	public void addDisconnectedListener(DisconnectedListener listener) {
		listenerDisconnected.add(listener);
	}

	/**
	 * Removes a Disconnected listener.
	 */
	public void removeDisconnectedListener(DisconnectedListener listener) {
		listenerDisconnected.remove(listener);
	}

	@Override
	protected void callEnumerateListeners(String uid, String connectedUid, char position,
	                                      short[] hardwareVersion, short[] firmwareVersion,
	                                      int deviceIdentifier, short enumerationType) {
		for (IPConnection.EnumerateListener listener: listenerEnumerate) {
			listener.enumerate(new EnumerateCallbackData(this, uid, connectedUid, position,
			                                             hardwareVersion, firmwareVersion,
			                                             deviceIdentifier, enumerationType));
		}
	}

	@Override
	protected boolean hasEnumerateListeners() {
		return !listenerEnumerate.isEmpty();
	}

	@Override
	protected void callConnectedListeners(short connectReason) {
		for (IPConnection.ConnectedListener listener: listenerConnected) {
			listener.connected(new ConnectedCallbackData(this, connectReason));
		}
	}

	@Override
	protected void callDisconnectedListeners(final short disconnectReason) {
		for (IPConnection.DisconnectedListener listener: listenerDisconnected) {
			listener.disconnected(new DisconnectedCallbackData(this, disconnectReason));
		}
	}

	@Override
	protected void callDeviceListener(final Device device, final byte functionID, byte[] packet) {
		if (device.callbacks[functionID] != null) {
			device.callbacks[functionID].callback(device, packet);
		}
	}
}
