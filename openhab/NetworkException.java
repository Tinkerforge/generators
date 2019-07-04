/*
 * Copyright (C) 2017 Matthias Bolte <matthias@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

package com.tinkerforge;

public class NetworkException extends TinkerforgeException {
	private static final long serialVersionUID = 1L;

	NetworkException() {
	}

	NetworkException(String message) {
		super(message);
	}

	NetworkException(String message, Throwable cause) {
		super(message, cause);
	}

	NetworkException(Throwable cause) {
		super(cause);
	}
}
