/*
 * Copyright (C) 2013 Matthias Bolte <matthias@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted.
 */

package com.tinkerforge;

public class TinkerforgeException extends Exception {
	private static final long serialVersionUID = 1L;

	TinkerforgeException() {
	}

	TinkerforgeException(String message) {
		super(message);
	}

	TinkerforgeException(Throwable cause) {
		super(cause);
	}
}
