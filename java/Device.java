/*
 * Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
 * Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted.
 */

package com.tinkerforge;

import java.util.Arrays;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;

public abstract class Device {
	long uid = (long)0;
	short[] apiVersion = new short[3];
	byte[] responseExpected = new byte[256];
	byte expectedResponseFunctionID = 0; // protected by requestMutex
	byte expectedResponseSequenceNumber = 0; // protected by requestMutex
	private Object requestMutex = new Object();
	LinkedBlockingQueue<byte[]> responseQueue = new LinkedBlockingQueue<byte[]>();
	IPConnection ipcon = null;
	CallbackListener[] callbacks = new CallbackListener[256];

	final static byte RESPONSE_EXPECTED_FLAG_INVALID_FUNCTION_ID = 0;
	final static byte RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE = 1;
	final static byte RESPONSE_EXPECTED_FLAG_ALWAYS_FALSE = 2;
	final static byte RESPONSE_EXPECTED_FLAG_TRUE = 3;
	final static byte RESPONSE_EXPECTED_FLAG_FALSE = 4;

	public class Identity {
		public String uid;
		public String connectedUid;
		public char position;
		public short[] hardwareVersion = new short[3];
		public short[] firmwareVersion = new short[3];
		public int deviceIdentifier;

		public String toString() {
			return "[" + "uid = " + uid + ", " + "connectedUid = " + connectedUid + ", " +
			       "position = " + position + ", " + "hardwareVersion = " + Arrays.toString(hardwareVersion) + ", " +
			       "firmwareVersion = " + Arrays.toString(firmwareVersion) + ", " +
			       "deviceIdentifier = " + deviceIdentifier + "]";
		}
	}

	interface CallbackListener {
		public void callback(byte data[]);
	}

	/**
	 * Creates the device object with the unique device ID \c uid and adds
	 * it to the IPConnection \c ipcon.
	 */
	public Device(String uid, IPConnection ipcon) {
		long uidTmp = IPConnection.base58Decode(uid);
        if(uidTmp > 0xFFFFFFFFL) {
            // convert from 64bit to 32bit
            long value1 = uidTmp & 0xFFFFFFFFL;
            long value2 = (uidTmp >> 32) & 0xFFFFFFFFL;

            uidTmp  = (value1 & 0x00000FFFL);
            uidTmp |= (value1 & 0x0F000000L) >> 12;
            uidTmp |= (value2 & 0x0000003FL) << 16;
            uidTmp |= (value2 & 0x000F0000L) << 6;
            uidTmp |= (value2 & 0x3F000000L) << 2;
		}

		this.uid   = uidTmp;
		this.ipcon = ipcon;

		for(int i = 0; i < responseExpected.length; i++) {
			responseExpected[i] = RESPONSE_EXPECTED_FLAG_INVALID_FUNCTION_ID;
		}

		responseExpected[IPConnection.unsignedByte(IPConnection.FUNCTION_ENUMERATE)] = RESPONSE_EXPECTED_FLAG_ALWAYS_FALSE;
		responseExpected[IPConnection.unsignedByte(IPConnection.CALLBACK_ENUMERATE)] = RESPONSE_EXPECTED_FLAG_ALWAYS_FALSE;

		ipcon.devices.put(this.uid, this); // FIXME: use weakref here
	}

	public Identity getIdentity() throws TimeoutException, NotConnectedException {
		return null;
	}

	/**
	 * Returns the API version (major, minor, revision) of the bindings for
	 * this device.
	 */
	public short[] getAPIVersion() {
		return apiVersion;
	}

	/**
	 * Returns the response expected flag for the function specified by the
	 * \c functionId parameter. It is *true* if the function is expected to
	 * send a response, *false* otherwise.
	 *
	 * For getter functions this is enabled by default and cannot be disabled,
	 * because those functions will always send a response. For callback
	 * configuration functions it is enabled by default too, but can be
	 * disabled via the SetResponseExpected function. For setter functions it
	 * is disabled by default and can be enabled.
	 *
	 * Enabling the response expected flag for a setter function allows to
	 * detect timeouts and other error conditions calls of this setter as well.
	 * The device will then send a response for this purpose. If this flag is
	 * disabled for a setter function then no response is send and errors are
	 * silently ignored, because they cannot be detected.
	 */
	public boolean getResponseExpected(byte functionId) {
		byte flag = responseExpected[IPConnection.unsignedByte(functionId)];

		if(flag == RESPONSE_EXPECTED_FLAG_INVALID_FUNCTION_ID) {
			throw new IllegalArgumentException("Invalid function ID " + functionId);
		}

		return flag == RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE ||
		       flag == RESPONSE_EXPECTED_FLAG_TRUE;
	}

	/**
	 * Changes the response expected flag of the function specified by
	 * the \c functionId parameter. This flag can only be changed for setter
	 * (default value: *false*) and callback configuration functions
	 * (default value: *true*). For getter functions it is always enabled
	 * and callbacks it is always disabled.
	 *
	 * Enabling the response expected flag for a setter function allows to
	 * detect timeouts and other error conditions calls of this setter as
	 * well. The device will then send a response for this purpose. If this
	 * flag is disabled for a setter function then no response is send and
	 * errors are silently ignored, because they cannot be detected.
	 */
	public void setResponseExpected(byte functionId, boolean responseExpected) {
		int index = IPConnection.unsignedByte(functionId);
		byte flag = this.responseExpected[index];

		if(flag == RESPONSE_EXPECTED_FLAG_INVALID_FUNCTION_ID) {
			throw new IllegalArgumentException("Invalid function ID " + functionId);
		}

		if(flag == RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE ||
		   flag == RESPONSE_EXPECTED_FLAG_ALWAYS_FALSE) {
			throw new IllegalArgumentException("Response Expected flag cannot be changed for function ID " + functionId);
		}

		if(responseExpected) {
			this.responseExpected[index] = RESPONSE_EXPECTED_FLAG_TRUE;
		} else {
			this.responseExpected[index] = RESPONSE_EXPECTED_FLAG_FALSE;
		}
	}

	/**
	 * Changes the response expected flag for all setter and callback
	 * configuration functions of this device at once.
	 */
	public void setResponseExpectedAll(boolean responseExpected) {
		byte flag = RESPONSE_EXPECTED_FLAG_FALSE;
		if(responseExpected) {
			flag = RESPONSE_EXPECTED_FLAG_TRUE;
		}

		for(int i = 0; i < this.responseExpected.length; i++) {
			if(this.responseExpected[i] == RESPONSE_EXPECTED_FLAG_TRUE ||
			   this.responseExpected[i] == RESPONSE_EXPECTED_FLAG_FALSE) {
				this.responseExpected[i] = flag;
			}
		}
	}

	byte[] sendRequest(byte[] request) throws TimeoutException, NotConnectedException {
		byte[] response = null;

		if (IPConnection.getResponseExpectedFromData(request)) {
			byte functionID = IPConnection.getFunctionIDFromData(request);

			synchronized(requestMutex) {
				expectedResponseFunctionID = functionID;
				expectedResponseSequenceNumber = IPConnection.getSequenceNumberFromData(request);

				try {
					ipcon.sendRequest(request);

					while(true) {
						response = null;

						try {
							response = responseQueue.poll(ipcon.responseTimeout, TimeUnit.MILLISECONDS);
						} catch (InterruptedException e) {
							e.printStackTrace();
						}

						if(response == null) {
							throw new TimeoutException("Did not receive response in time for function ID " + functionID);
						}

						if(expectedResponseFunctionID == IPConnection.getFunctionIDFromData(response) &&
						   expectedResponseSequenceNumber == IPConnection.getSequenceNumberFromData(response)) {
							// ignore old responses that arrived after the timeout expired, but before setting
							// expectedResponseFunctionID and expectedResponseSequenceNumber back to 0
							break;
						}
					}
				} finally {
					expectedResponseFunctionID = 0;
					expectedResponseSequenceNumber = 0;
				}
			}

			byte errorCode = IPConnection.getErrorCodeFromData(response);
			switch(errorCode) {
				case 0:
					break;
				case 1:
					throw new UnsupportedOperationException("Got invalid parameter for function ID " + functionID);
				case 2:
					throw new UnsupportedOperationException("Function ID " + functionID + " is not supported");
				default:
					throw new UnsupportedOperationException("Function ID " + functionID + " returned an unknown error");
			}
		} else {
			ipcon.sendRequest(request);
		}

		return response;
	}
}
