/*
 * Copyright (C) 2018 Matthias Bolte <matthias@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

package com.tinkerforge;

public interface DeviceProvider {
	public int getDeviceIdentifier();
	public String getDeviceDisplayName();
	public Class<? extends Device> getDeviceClass();
}
