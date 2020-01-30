/*
 * Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
 * Copyright (C) 2012-2013, 2019-2020 Matthias Bolte <matthias@tinkerforge.com>
 * Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

package com.tinkerforge;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.Arrays;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;

public abstract class DeviceBase {
	final static byte DEVICE_IDENTIFIER_CHECK_PENDING = 0;
	final static byte DEVICE_IDENTIFIER_CHECK_MATCH = 1;
	final static byte DEVICE_IDENTIFIER_CHECK_MISMATCH = 2;

	final static byte RESPONSE_EXPECTED_FLAG_INVALID_FUNCTION_ID = 0;
	final static byte RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE = 1; // getter
	final static byte RESPONSE_EXPECTED_FLAG_TRUE = 2; // setter
	final static byte RESPONSE_EXPECTED_FLAG_FALSE = 3; // setter, default

	long uidNumber;
	String uidString;
	int deviceIdentifier;
	String deviceDisplayName;
	Object deviceIdentifierMutex = new Object();
	byte deviceIdentifierCheck = DEVICE_IDENTIFIER_CHECK_PENDING; // protected by deviceIdentifierMutex
	String wrongDeviceDisplayName = "?"; // protected by deviceIdentifierMutex
	short[] apiVersion = new short[3];
	byte[] responseExpected = new byte[256];
	byte expectedResponseFunctionID = 0; // protected by requestMutex
	byte expectedResponseSequenceNumber = 0; // protected by requestMutex
	Object requestMutex = new Object();
	LinkedBlockingQueue<byte[]> responseQueue = new LinkedBlockingQueue<byte[]>();
	IPConnection ipcon = null;
	IPConnection.DeviceCallbackListener[] callbacks = new IPConnection.DeviceCallbackListener[256];
	IPConnection.DeviceHighLevelCallback[] highLevelCallbacks = new IPConnection.DeviceHighLevelCallback[256];
	Object streamMutex = new Object();

	public DeviceBase(String uid, IPConnection ipcon) {
		long uidNumber = IPConnection.base58Decode(uid);

		if (uidNumber > 0xFFFFFFFFL) {
			// convert from 64bit to 32bit
			long value1 = uidNumber & 0xFFFFFFFFL;
			long value2 = (uidNumber >> 32) & 0xFFFFFFFFL;

			uidNumber  = (value1 & 0x00000FFFL);
			uidNumber |= (value1 & 0x0F000000L) >> 12;
			uidNumber |= (value2 & 0x0000003FL) << 16;
			uidNumber |= (value2 & 0x000F0000L) << 6;
			uidNumber |= (value2 & 0x3F000000L) << 2;
		}

		if (uidNumber == 0) {
			throw new IllegalArgumentException("UID '" + uid + "' is empty or maps to zero");
		}

		this.uidNumber = uidNumber;
		this.uidString = uid;
		this.ipcon = ipcon;

		for (int i = 0; i < responseExpected.length; i++) {
			responseExpected[i] = RESPONSE_EXPECTED_FLAG_INVALID_FUNCTION_ID;
		}
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
	 * disabled for a setter function then no response is sent and errors are
	 * silently ignored, because they cannot be detected.
	 */
	public boolean getResponseExpected(byte functionId) {
		byte flag = responseExpected[IPConnection.unsignedByte(functionId)];

		if (flag == RESPONSE_EXPECTED_FLAG_INVALID_FUNCTION_ID) {
			throw new IllegalArgumentException("Invalid function ID " + functionId);
		}

		return flag == RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE ||
		       flag == RESPONSE_EXPECTED_FLAG_TRUE;
	}

	/**
	 * Changes the response expected flag of the function specified by
	 * the \c functionId parameter. This flag can only be changed for setter
	 * (default value: *false*) and callback configuration functions
	 * (default value: *true*). For getter functions it is always enabled.
	 *
	 * Enabling the response expected flag for a setter function allows to
	 * detect timeouts and other error conditions calls of this setter as
	 * well. The device will then send a response for this purpose. If this
	 * flag is disabled for a setter function then no response is sent and
	 * errors are silently ignored, because they cannot be detected.
	 */
	public void setResponseExpected(byte functionId, boolean responseExpected) {
		int index = IPConnection.unsignedByte(functionId);
		byte flag = this.responseExpected[index];

		if (flag == RESPONSE_EXPECTED_FLAG_INVALID_FUNCTION_ID) {
			throw new IllegalArgumentException("Invalid function ID " + functionId);
		}

		if (flag == RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE) {
			throw new IllegalArgumentException("Response Expected flag cannot be changed for function ID " + functionId);
		}

		if (responseExpected) {
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

		if (responseExpected) {
			flag = RESPONSE_EXPECTED_FLAG_TRUE;
		}

		for (int i = 0; i < this.responseExpected.length; i++) {
			if (this.responseExpected[i] == RESPONSE_EXPECTED_FLAG_TRUE ||
			    this.responseExpected[i] == RESPONSE_EXPECTED_FLAG_FALSE) {
				this.responseExpected[i] = flag;
			}
		}
	}

	void checkDeviceIdentifier() throws TinkerforgeException {
		if (deviceIdentifierCheck == DEVICE_IDENTIFIER_CHECK_MATCH) {
			return;
		}

		synchronized (deviceIdentifierMutex) {
			if (deviceIdentifierCheck == DEVICE_IDENTIFIER_CHECK_PENDING) {
				ByteBuffer bb = ipcon.createRequestPacket((byte)8, (byte)255, this); // getIdentity
				byte[] response = sendRequest(bb.array());

				bb = ByteBuffer.wrap(response, 31, response.length - 31);
				bb.order(ByteOrder.LITTLE_ENDIAN);

				int deviceIdentifier = IPConnection.unsignedShort(bb.getShort());

				if (deviceIdentifier == this.deviceIdentifier) {
					deviceIdentifierCheck = DEVICE_IDENTIFIER_CHECK_MATCH;
				} else {
					deviceIdentifierCheck = DEVICE_IDENTIFIER_CHECK_MISMATCH;

					try {
						wrongDeviceDisplayName = DeviceFactory.getDeviceDisplayName(deviceIdentifier);
					} catch (IllegalArgumentException e) {
						wrongDeviceDisplayName = "Unknown Device [" + deviceIdentifier + "]";
					}
				}
			}

			if (deviceIdentifierCheck == DEVICE_IDENTIFIER_CHECK_MISMATCH) {
				throw new WrongDeviceTypeException("UID " + uidString + " belongs to a " + wrongDeviceDisplayName +
				                                   " instead of the expected " + deviceDisplayName);
			}
		}
	}

	byte[] sendRequest(byte[] request) throws TinkerforgeException {
		byte[] response = null;

		if (IPConnection.getResponseExpectedFromData(request)) {
			byte functionID = IPConnection.getFunctionIDFromData(request);

			synchronized (requestMutex) {
				expectedResponseFunctionID = functionID;
				expectedResponseSequenceNumber = IPConnection.getSequenceNumberFromData(request);

				try {
					ipcon.sendRequest(request);

					while (true) {
						response = null;

						try {
							response = responseQueue.poll(ipcon.responseTimeout, TimeUnit.MILLISECONDS);
						} catch (InterruptedException e) {
							e.printStackTrace();
						}

						if (response == null) {
							throw new TimeoutException("Did not receive response in time for function ID " + functionID);
						}

						if (expectedResponseFunctionID == IPConnection.getFunctionIDFromData(response) &&
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

			switch (errorCode) {
				case 0:
					break;
				case 1:
					throw new InvalidParameterException("Got invalid parameter for function ID " + functionID);
				case 2:
					throw new NotSupportedException("Function ID " + functionID + " is not supported");
				default:
					throw new UnknownErrorCodeException("Function ID " + functionID + " returned an unknown error");
			}
		} else {
			ipcon.sendRequest(request);
		}

		return response;
	}
}
