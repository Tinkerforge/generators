/*
 * Copyright (C) 2020 Matthias Bolte <matthias@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

package com.tinkerforge;

public class WrongResponseLengthException extends TinkerforgeException {
	private static final long serialVersionUID = 1L;

	WrongResponseLengthException() {
	}

	WrongResponseLengthException(String message) {
		super(message);
	}

	WrongResponseLengthException(String message, Throwable cause) {
		super(message, cause);
	}

	WrongResponseLengthException(Throwable cause) {
		super(cause);
	}
}
