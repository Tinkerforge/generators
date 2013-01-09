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
	byte[] responseExpected = new byte[256];
	byte expectedResponseFunctionID = 0;
	byte expectedResponseSequenceNumber = 0;
	private Object writeMutex = new Object();
	SynchronousQueue<byte[]> responseQueue = new SynchronousQueue<byte[]>();
	IPConnection ipcon = null;
	CallbackListener[] callbacks = new CallbackListener[256];
	Object[] listenerObjects = new Object[256];

	final static byte RESPONSE_EXPECTED_FLAG_INVALID_FUNCTION_ID = 0;
	final static byte RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE = 1;
	final static byte RESPONSE_EXPECTED_FLAG_ALWAYS_FALSE = 2;
	final static byte RESPONSE_EXPECTED_FLAG_TRUE = 3;
	final static byte RESPONSE_EXPECTED_FLAG_FALSE = 4;

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

		responseExpected[IPConnection.unsignedByte(IPConnection.FUNCTION_ENUMERATE)] = RESPONSE_EXPECTED_FLAG_FALSE;
		responseExpected[IPConnection.unsignedByte(IPConnection.FUNCTION_ADC_CALIBRATE)] = RESPONSE_EXPECTED_FLAG_FALSE;
		responseExpected[IPConnection.unsignedByte(IPConnection.FUNCTION_GET_ADC_CALIBRATION)] = RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE;
		responseExpected[IPConnection.unsignedByte(IPConnection.CALLBACK_ENUMERATE)] = RESPONSE_EXPECTED_FLAG_ALWAYS_FALSE;

		ipcon.devices.put(this.uid, this);
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
		if(this.responseExpected[IPConnection.unsignedByte(functionId)] != RESPONSE_EXPECTED_FLAG_INVALID_FUNCTION_ID &&
		   functionId < this.responseExpected.length) {
			return this.responseExpected[IPConnection.unsignedByte(functionId)] == RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE ||
			       this.responseExpected[IPConnection.unsignedByte(functionId)] == RESPONSE_EXPECTED_FLAG_TRUE;
		}

		throw new IllegalArgumentException("Invalid function ID " + functionId);
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
		if(this.responseExpected[IPConnection.unsignedByte(functionId)] == RESPONSE_EXPECTED_FLAG_INVALID_FUNCTION_ID ||
		   functionId >= this.responseExpected.length) {
			throw new IllegalArgumentException("Invalid function ID " + functionId);
		}

		if(this.responseExpected[IPConnection.unsignedByte(functionId)] == RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE ||
		   this.responseExpected[IPConnection.unsignedByte(functionId)] == RESPONSE_EXPECTED_FLAG_ALWAYS_FALSE) {
			throw new IllegalArgumentException("Response Expected flag cannot be changed for function ID " + functionId);
		}

		if(responseExpected) {
			this.responseExpected[IPConnection.unsignedByte(functionId)] = RESPONSE_EXPECTED_FLAG_TRUE;
		} else {
			this.responseExpected[IPConnection.unsignedByte(functionId)] = RESPONSE_EXPECTED_FLAG_FALSE;
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
			if(this.responseExpected[i] != RESPONSE_EXPECTED_FLAG_INVALID_FUNCTION_ID &&
		       this.responseExpected[i] != RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE &&
		       this.responseExpected[i] != RESPONSE_EXPECTED_FLAG_ALWAYS_FALSE) {
				this.responseExpected[i] = flag;
			}
		}
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
			expectedResponseSequenceNumber = IPConnection.getSequenceNumberFromData(request);

			ipcon.write(request);

			try {
				response = responseQueue.poll(ipcon.responseTimeout, TimeUnit.MILLISECONDS);
				if(response == null) {
					throw new IPConnection.TimeoutException("Did not receive response in time");
				}
			} catch (InterruptedException e) {
				e.printStackTrace();
			} finally {
				expectedResponseFunctionID = 0;
				expectedResponseSequenceNumber = 0;
			}

			byte errorCode = IPConnection.getErrorCodeFromData(response);
			switch(errorCode)
			{
				case 0:
					break;
				case 1:
					throw new java.lang.UnsupportedOperationException("Got invalid parameter for function " + functionID);
				case 2:
					throw new java.lang.UnsupportedOperationException("Function " + functionID + " is not supported");
				default:
					throw new java.lang.UnsupportedOperationException("Function " + functionID + " returned an unknown error");
			}
		}

		return response;
	}
}
