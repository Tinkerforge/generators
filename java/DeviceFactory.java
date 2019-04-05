/*
 * Copyright (C) 2018 Matthias Bolte <matthias@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

package com.tinkerforge;

import java.util.Hashtable;
import java.util.ServiceLoader;

public class DeviceFactory {
	private static Hashtable<Integer, DeviceProvider> deviceProviders = new Hashtable<Integer, DeviceProvider>();

	static {
		for (DeviceProvider deviceProvider: ServiceLoader.load(DeviceProvider.class)) {
			deviceProviders.put(deviceProvider.getDeviceIdentifier(), deviceProvider);
		}
	}

	private static DeviceProvider getDeviceProvider(int deviceIdentifier) {
		DeviceProvider deviceProvider = deviceProviders.get(deviceIdentifier);

		if (deviceProvider == null) {
			throw new IllegalArgumentException("Unknown device identifier: " + deviceIdentifier);
		}

		return deviceProvider;
	}

	public static Class<? extends Device> getDeviceClass(int deviceIdentifier) {
		return getDeviceProvider(deviceIdentifier).getDeviceClass();
	}

	public static String getDeviceDisplayName(int deviceIdentifier) {
		return getDeviceProvider(deviceIdentifier).getDeviceDisplayName();
	}

	public static Device createDevice(int deviceIdentifier, String uid, IPConnection ipcon) throws Exception {
		return getDeviceClass(deviceIdentifier).getConstructor(String.class, IPConnection.class).newInstance(uid, ipcon);
	}
}
