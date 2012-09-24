/*
 * Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
 * Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted.
 */

package com.tinkerforge;

import java.util.concurrent.SynchronousQueue;
import java.util.concurrent.TimeUnit;

public abstract class Device {
	long uid = (long)0;
	short stackID = (short)0;
	String expectedName = null;
	String name = null;
	short[] firmwareVersion = new short[3];
	short[] bindingVersion = new short[3];
	byte expectedResponseFunctionID = (byte)0;
	private Object writeMutex = new Object();
	SynchronousQueue<byte[]> responseQueue = new SynchronousQueue<byte[]>();

	IPConnection ipcon = null;

	CallbackListener[] callbacks = new CallbackListener[255];
	Object[] listenerObjects = new Object[255];

	interface CallbackListener {
		public void callback(byte data[]);
	}

	public class Version {
		public String name = null;
		public short[] firmwareVersion = new short[3];
		public short[] bindingVersion = new short[3];

		public String toString() {
			return "[" + "name = " + name + ", " + "firmwareVersion = " +
			       firmwareVersion + ", " + "bindingVersion = " + bindingVersion + "]";
		}
	}

	public Device(String uid) {
		this.uid = IPConnection.base58Decode(uid);
	}

	/**
	 * Returns the name (including the hardware version), the firmware version
	 * and the binding version of the device. The firmware and binding versions
	 * are given in arrays of size 3 with the syntax [major, minor, revision].
	 *
	 * The returned object has the public member variables String name,
	 * short[3] firmwareVersion and short[3] bindingVersion.
	 */
	public Version getVersion() {
		Version version = new Version();
		version.name = name;
		version.firmwareVersion[0] = firmwareVersion[0];
		version.firmwareVersion[1] = firmwareVersion[1];
		version.firmwareVersion[2] = firmwareVersion[2];
		version.bindingVersion[0] = bindingVersion[0];
		version.bindingVersion[1] = bindingVersion[1];
		version.bindingVersion[2] = bindingVersion[2];

		return version;
	}

	void sendRequestNoResponse(byte[] request)
	{
		synchronized(writeMutex)
		{
			ipcon.write(request);
		}
	}

	byte[] sendRequestExpectResponse(byte[] request, byte functionID) throws IPConnection.TimeoutException
	{
		byte[] response = null;

		synchronized(writeMutex)
		{
			ipcon.write(request);

			expectedResponseFunctionID = functionID;

			try {
				response = responseQueue.poll(IPConnection.RESPONSE_TIMEOUT, TimeUnit.MILLISECONDS);
				if(response == null) {
					throw new IPConnection.TimeoutException("Did not receive response in time");
				}
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}

		return response;
	}
}
