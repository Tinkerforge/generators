/*
 * Copyright (C) 2013-2014 Matthias Bolte <matthias@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

package com.tinkerforge;

public class TinkerforgeException extends Exception {
	private static final long serialVersionUID = 1L;

	TinkerforgeException() {
	}

	TinkerforgeException(String message) {
		super(message);
	}

	TinkerforgeException(String message, Throwable cause) {
		super(message, cause);
	}

	TinkerforgeException(Throwable cause) {
		super(cause);
	}
}
