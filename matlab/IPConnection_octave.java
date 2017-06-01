/*
 * Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
 * Copyright (C) 2014 Matthias Bolte <matthias@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

package com.tinkerforge;

import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import java.io.File;
import java.io.InputStream;
import java.io.FileOutputStream;
import org.octave.Octave;
import org.octave.OctaveReference;

public class IPConnection extends IPConnectionBase {
	List<OctaveReference> listenerEnumerate = new CopyOnWriteArrayList<OctaveReference>();
	List<OctaveReference> listenerConnected = new CopyOnWriteArrayList<OctaveReference>();
	List<OctaveReference> listenerDisconnected = new CopyOnWriteArrayList<OctaveReference>();

	static private boolean haveOctaveInvokeWrapper = false;

	static {
		// check if JNI is working for Octave
		boolean okay = true;

		try {
			Octave.needThreadedInvokation();
		} catch (UnsatisfiedLinkError e) {
			okay = false;
		}

		// if not, work around the UnsatisfiedLinkError
		if (!okay) {
			String suffix = System.getProperty("os.name").toLowerCase() + "-" + System.getProperty("os.arch").toLowerCase();
			InputStream input;

			try {
				if(suffix.startsWith("windows")) {
					suffix = "windows-" + System.getProperty("os.arch").toLowerCase();
					input = IPConnection.class.getResourceAsStream("/com/tinkerforge/liboctaveinvokewrapper-" + suffix + ".dll");
				} else if(suffix.startsWith("mac")) {
					suffix = "mac-" + System.getProperty("os.arch").toLowerCase();
					input = IPConnection.class.getResourceAsStream("/com/tinkerforge/liboctaveinvokewrapper-" + suffix + ".dynlib");
				} else {
					input = IPConnection.class.getResourceAsStream("/com/tinkerforge/liboctaveinvokewrapper-" + suffix + ".so");
				}
			} catch (Exception e) {
				input = null;
			}

			if (input != null) {
				try {
					File tmp;
					if(suffix.startsWith("windows")) {
						tmp = File.createTempFile("liboctaveinvokewrapper-" + suffix, ".dll");
					} else if(suffix.startsWith("mac")) {
						tmp = File.createTempFile("liboctaveinvokewrapper-" + suffix, ".dynlib");
					} else {
						tmp = File.createTempFile("liboctaveinvokewrapper-" + suffix, ".so");
					}
					tmp.deleteOnExit();

					FileOutputStream output = new FileOutputStream(tmp);
					byte[] buffer = new byte[1024];
					int readBytes;

					try {
						while ((readBytes = input.read(buffer)) != -1) {
							output.write(buffer, 0, readBytes);
						}
					} finally {
						output.close();
					}

					System.load(tmp.getAbsolutePath());

					haveOctaveInvokeWrapper = true;
				} catch (Exception e) {
					e.printStackTrace(); // FIXME
				} finally {
					try {
						input.close();
					} catch (Exception e) {
						e.printStackTrace(); // FIXME
					}
				}
			}
		}
	}

	public native static void doOctaveInvokeWrapper(int id, Object[] args);

	public static void doOctaveInvoke(OctaveReference reference, Object[] args) {
		if (haveOctaveInvokeWrapper) {
			doOctaveInvokeWrapper(reference.getID(), args);
		} else {
			reference.invoke(args);
		}
	}

	interface DeviceCallbackListener {
		public void callback(Device device, byte data[]);
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

	public class ConnectedCallbackData extends java.util.EventObject {
		private static final long serialVersionUID = 1L;

		public short connectReason;

		public ConnectedCallbackData(IPConnection ipcon, short connectReason) {
			super(ipcon);

			this.connectReason = connectReason;
		}
	}

	public class DisconnectedCallbackData extends java.util.EventObject {
		private static final long serialVersionUID = 1L;

		public short disconnectReason;

		public DisconnectedCallbackData(IPConnection ipcon, short disconnectReason) {
			super(ipcon);

			this.disconnectReason = disconnectReason;
		}
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
	public void addEnumerateCallback(OctaveReference listener) {
		listenerEnumerate.add(listener);
	}

	/**
	 * Removes a Enumerate listener.
	 */
	public void removeEnumerateCallback(OctaveReference listener) {
		listenerEnumerate.remove(listener);
	}

	/**
	 * Adds a Connected listener.
	 */
	public void addConnectedCallback(OctaveReference listener) {
		listenerConnected.add(listener);
	}

	/**
	 * Removes a Connected listener.
	 */
	public void removeConnectedCallback(OctaveReference listener) {
		listenerConnected.remove(listener);
	}

	/**
	 * Adds a Disconnected listener.
	 */
	public void addDisconnectedCallback(OctaveReference listener) {
		listenerDisconnected.add(listener);
	}

	/**
	 * Removes a Disconnected listener.
	 */
	public void removeDisconnectedCallback(OctaveReference listener) {
		listenerDisconnected.remove(listener);
	}

	@Override
	protected void callEnumerateListeners(String uid, String connectedUid, char position,
	                                      short[] hardwareVersion, short[] firmwareVersion,
	                                      int deviceIdentifier, short enumerationType) {
		for (OctaveReference listener: listenerEnumerate) {
			doOctaveInvoke(listener, new Object[]{new EnumerateCallbackData(this, uid, connectedUid, position,
			                                                                hardwareVersion, firmwareVersion,
			                                                                deviceIdentifier, enumerationType)});
		}
	}

	@Override
	protected boolean hasEnumerateListeners() {
		return !listenerEnumerate.isEmpty();
	}

	@Override
	protected void callConnectedListeners(short connectReason) {
		for (OctaveReference listener: listenerConnected) {
			doOctaveInvoke(listener, new Object[]{new ConnectedCallbackData(this, connectReason)});
		}
	}

	@Override
	protected void callDisconnectedListeners(short disconnectReason) {
		for (OctaveReference listener: listenerDisconnected) {
			doOctaveInvoke(listener, new Object[]{new DisconnectedCallbackData(this, disconnectReason)});
		}
	}

	@Override
	protected void callDeviceListener(Device device, byte functionID, byte[] data) {
		if(device.callbacks[functionID] != null) {
			device.callbacks[functionID].callback(device, data);
		}
	}
}
