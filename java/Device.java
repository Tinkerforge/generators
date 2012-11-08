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
	short[] apiVersion = new short[3];
	byte expectedResponseFunctionID = (byte)0;
	private Object writeMutex = new Object();
	SynchronousQueue<byte[]> responseQueue = new SynchronousQueue<byte[]>();
	IPConnection ipcon = null;
	CallbackListener[] callbacks = new CallbackListener[255];
	Object[] listenerObjects = new Object[255];

	interface CallbackListener {
		public void callback(byte data[]);
	}

	public Device(String uid, IPConnection ipcon) {
		// FIXME: convert from uint64_t to uint32_t
		this.uid = IPConnection.base58Decode(uid);
		this.ipcon = ipcon;
	}

	/**
	 * Returns API version [major, minor, revision] used for this device.
	 */
	public short[] getAPIVersion() {
		return apiVersion;
	}

	void sendRequestNoResponse(byte[] request) {
		synchronized(writeMutex) {
			ipcon.write(request);
		}
	}

	byte[] sendRequestExpectResponse(byte[] request, byte functionID) throws IPConnection.TimeoutException {
		byte[] response = null;

		synchronized(writeMutex) {
			expectedResponseFunctionID = functionID;

			ipcon.write(request);

			try {
				response = responseQueue.poll(IPConnection.RESPONSE_TIMEOUT, TimeUnit.MILLISECONDS);
				if(response == null) {
					throw new IPConnection.TimeoutException("Did not receive response in time");
				}
			} catch (InterruptedException e) {
				e.printStackTrace();
			} finally {
				expectedResponseFunctionID = 0;
			}
		}

		return response;
	}
}
