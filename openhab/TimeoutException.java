/*
 * Copyright (C) 2012-2014 Matthias Bolte <matthias@tinkerforge.com>
 * Copyright (C) 2011-2012 Olaf Lüke <olaf@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

package com.tinkerforge;

public class TimeoutException extends TinkerforgeException {
	private static final long serialVersionUID = 1L;

	TimeoutException() {
	}

	TimeoutException(String message) {
		super(message);
	}

	TimeoutException(String message, Throwable cause) {
		super(message, cause);
	}

	TimeoutException(Throwable cause) {
		super(cause);
	}
}
