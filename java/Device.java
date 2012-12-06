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

	public Device(String uid, IPConnection ipcon) {
		long uidTmp = IPConnection.base58Decode(uid);
        if(uidTmp > 0xFFFFFFFFL) {
            // convert from 64bit to 32bit
            long value1 = uidTmp & 0xFFFFFFFFL;
            long value2 = (uidTmp >> 32) & 0xFFFFFFFFL;

            uidTmp  = (value1 & 0x3F000000L) << 2;
            uidTmp |= (value1 & 0x000F0000L) << 6;
            uidTmp |= (value1 & 0x0000003FL) << 16;
            uidTmp |= (value2 & 0x0F000000L) >> 12;
            uidTmp |= (value2 & 0x00000FFFL);
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
	 * Returns API version [major, minor, revision] used for this device.
	 */
	public short[] getAPIVersion() {
		return apiVersion;
	}

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

	public boolean getResponseExpected(byte functionId) {
		if(this.responseExpected[IPConnection.unsignedByte(functionId)] != RESPONSE_EXPECTED_FLAG_INVALID_FUNCTION_ID &&
		   functionId < this.responseExpected.length) {
			return this.responseExpected[IPConnection.unsignedByte(functionId)] == RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE || 
			       this.responseExpected[IPConnection.unsignedByte(functionId)] == RESPONSE_EXPECTED_FLAG_TRUE;
		}

		throw new IllegalArgumentException("Invalid function ID " + functionId);
	}

	public void setResponseExpectedAll(boolean responseExpected) {
		byte flag = RESPONSE_EXPECTED_FLAG_TRUE;
		if(responseExpected) {
			flag = RESPONSE_EXPECTED_FLAG_FALSE;
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
				response = responseQueue.poll(ipcon.response_timeout, TimeUnit.MILLISECONDS);
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
