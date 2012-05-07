/*
 * Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
 * Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted.
 */

package com.tinkerforge;

import java.util.concurrent.Semaphore;
import java.util.concurrent.SynchronousQueue;

public abstract class Device {
	long uid = (long)0;
	short stackID = (short)0;
	String name = null;
	short[] firmwareVersion = new short[3];
	short[] bindingVersion = new short[3];
	byte answerType = (byte)0;
	Semaphore semaphoreAnswer = new Semaphore(1, true);
	Semaphore semaphoreWrite = new Semaphore(1, true);
	SynchronousQueue<byte[]> answerQueue = new SynchronousQueue<byte[]>();

	IPConnection ipcon = null;

	CallbackListener[] callbacks = new CallbackListener[255];
	Object[] listenerObjects = new Object[255];

	interface CallbackListener {
		public void callback(byte data[]);
	}

	public Device(String uid) {
		try {
			semaphoreAnswer.acquire();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}

		this.uid = IPConnection.base58Decode(uid);
	}
}
