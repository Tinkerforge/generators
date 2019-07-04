/*
 * Copyright (C) 2012-2014 Matthias Bolte <matthias@tinkerforge.com>
 * Copyright (C) 2011-2012 Olaf Lüke <olaf@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

package com.tinkerforge;

public class NotConnectedException extends TinkerforgeException {
	private static final long serialVersionUID = 1L;

	NotConnectedException() {
	}

	NotConnectedException(String message) {
		super(message);
	}

	NotConnectedException(String message, Throwable cause) {
		super(message, cause);
	}

	NotConnectedException(Throwable cause) {
		super(cause);
	}
}
