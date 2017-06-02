/*
 * Copyright (C) 2017 Matthias Bolte <matthias@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

package com.tinkerforge;

public class StreamOutOfSyncException extends TinkerforgeException {
	private static final long serialVersionUID = 1L;

	StreamOutOfSyncException() {
	}

	StreamOutOfSyncException(String message) {
		super(message);
	}

	StreamOutOfSyncException(String message, Throwable cause) {
		super(message, cause);
	}

	StreamOutOfSyncException(Throwable cause) {
		super(cause);
	}
}
