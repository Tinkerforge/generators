/*
 * Copyright (C) 2014 Matthias Bolte <matthias@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

package com.tinkerforge;

public class CryptoException extends TinkerforgeException {
	private static final long serialVersionUID = 1L;

	CryptoException() {
	}

	CryptoException(String message) {
		super(message);
	}

	CryptoException(String message, Throwable cause) {
		super(message, cause);
	}

	CryptoException(Throwable cause) {
		super(cause);
	}
}
