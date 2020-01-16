/*
 * Copyright (C) 2020 Matthias Bolte <matthias@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

package com.tinkerforge;

public class WrongDeviceTypeException extends TinkerforgeException {
	private static final long serialVersionUID = 1L;

	WrongDeviceTypeException() {
	}

	WrongDeviceTypeException(String message) {
		super(message);
	}

	WrongDeviceTypeException(String message, Throwable cause) {
		super(message, cause);
	}

	WrongDeviceTypeException(Throwable cause) {
		super(cause);
	}
}
