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
		public void callback(byte data[]);
	}

	public interface EnumerateListener extends TinkerforgeListener {
		public void enumerate(String uid, String connectedUid, char position,
		                      short[] hardwareVersion, short[] firmwareVersion,
		                      int deviceIdentifier, short enumerationType);
	}

	public interface ConnectedListener extends TinkerforgeListener {
		public void connected(short connectReason);
	}

	public interface DisconnectedListener extends TinkerforgeListener {
		public void disconnected(short disconnectReason);
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

	/**
	 * Registers a listener object.
	 *
	 * @deprecated
	 * Use the add and remove listener function per listener type instead.
	 */
	@Deprecated
	public void addListener(Object object) {
		boolean knownListener = false;

		if(object instanceof EnumerateListener) {
			knownListener = true;

			if (!listenerEnumerate.contains((EnumerateListener)object)) {
				listenerEnumerate.add((EnumerateListener)object);
			}
		}

		if(object instanceof ConnectedListener) {
			knownListener = true;

			if (!listenerConnected.contains((ConnectedListener)object)) {
				listenerConnected.add((ConnectedListener)object);
			}
		}

		if(object instanceof DisconnectedListener) {
			knownListener = true;

			if (!listenerDisconnected.contains((DisconnectedListener)object)) {
				listenerDisconnected.add((DisconnectedListener)object);
			}
		}

		if(!knownListener) {
			throw new IllegalArgumentException("Unknown listener type");
		}
	}

	void callEnumerateListeners(String uid, String connectedUid, char position,
	                            short[] hardwareVersion, short[] firmwareVersion,
	                            int deviceIdentifier, short enumerationType) {
		for(IPConnection.EnumerateListener listener: listenerEnumerate) {
			listener.enumerate(uid, connectedUid, position,
			                   hardwareVersion, firmwareVersion,
			                   deviceIdentifier, enumerationType);
		}
	}

	boolean hasEnumerateListeners() {
		return !listenerEnumerate.isEmpty();
	}

	void callConnectedListeners(short connectReason) {
		for(IPConnection.ConnectedListener listener: listenerConnected) {
			listener.connected(connectReason);
		}
	}

	void callDisconnectedListeners(short disconnectReason) {
		for(IPConnection.DisconnectedListener listener: listenerDisconnected) {
			listener.disconnected(disconnectReason);
		}
	}

	void callDeviceListener(Device device, byte functionID, byte[] data) {
		if(device.callbacks[functionID] != null) {
			device.callbacks[functionID].callback(data);
		}
	}
}
