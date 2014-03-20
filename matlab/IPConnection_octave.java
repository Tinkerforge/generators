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
import org.octave.Octave;

public class IPConnection extends IPConnectionBase {
	List<String> listenerEnumerate = new CopyOnWriteArrayList<String>();
	List<String> listenerConnected = new CopyOnWriteArrayList<String>();
	List<String> listenerDisconnected = new CopyOnWriteArrayList<String>();

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
	public void addEnumerateListener(String listener) {
		listenerEnumerate.add(listener);
	}

	/**
	 * Removes a Enumerate listener.
	 */
	public void removeEnumerateListener(String listener) {
		listenerEnumerate.remove(listener);
	}

	/**
	 * Adds a Connected listener.
	 */
	public void addConnectedListener(String listener) {
		listenerConnected.add(listener);
	}

	/**
	 * Removes a Connected listener.
	 */
	public void removeConnectedListener(String listener) {
		listenerConnected.remove(listener);
	}

	/**
	 * Adds a Disconnected listener.
	 */
	public void addDisconnectedListener(String listener) {
		listenerDisconnected.add(listener);
	}

	/**
	 * Removes a Disconnected listener.
	 */
	public void removeDisconnectedListener(String listener) {
		listenerDisconnected.remove(listener);
	}

	/**
	 * Registers a listener object.
	 *
	 * @deprecated
	 * Use the add and remove listener function per listener type instead.
	 */
	@Deprecated
	/*public void addListener(Object object) {
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
	}*/

	void callEnumerateListeners(String uid, String connectedUid, char position,
	                            short[] hardwareVersion, short[] firmwareVersion,
	                            int deviceIdentifier, short enumerationType) {
		for(String listener: listenerEnumerate) {
            Octave.call(listener,
                        new Object[]{uid, connectedUid, position,
                                     hardwareVersion, firmwareVersion,
                                     deviceIdentifier, enumerationType},
                        new Object[]{});
		}
	}

	boolean hasEnumerateListeners() {
		return !listenerEnumerate.isEmpty();
	}

	void callConnectedListeners(short connectReason) {
		for(String listener: listenerConnected) {
			Octave.call(listener, new Object[]{connectReason}, new Object[]{});
		}
	}

	void callDisconnectedListeners(short disconnectReason) {
		for(String listener: listenerDisconnected) {
            Octave.call(listener, new Object[]{disconnectReason}, new Object[]{});
		}
	}

	void callDeviceListener(Device device, byte functionID, byte[] data) {
		if(device.callbacks[functionID] != null) {
			device.callbacks[functionID].callback(data);
		}
	}
}
