/*
 * Copyright (C) 2019 Matthias Bolte <matthias@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

package com.tinkerforge;

public class NotSupportedException extends TinkerforgeException {
	private static final long serialVersionUID = 1L;

	NotSupportedException() {
	}

	NotSupportedException(String message) {
		super(message);
	}

	NotSupportedException(String message, Throwable cause) {
		super(message, cause);
	}

	NotSupportedException(Throwable cause) {
		super(cause);
	}
}
