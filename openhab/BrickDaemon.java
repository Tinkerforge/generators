/*
 * Copyright (C) 2012-2014 Matthias Bolte <matthias@tinkerforge.com>
 * Copyright (C) 2011-2012 Olaf Lüke <olaf@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

package com.tinkerforge;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.function.BiConsumer;


import org.eclipse.smarthome.core.types.Command;
import org.eclipse.smarthome.core.types.State;

class BrickDaemon extends Device {
	public final static byte FUNCTION_GET_AUTHENTICATION_NONCE = (byte)1;
	public final static byte FUNCTION_AUTHENTICATE = (byte)2;

	public BrickDaemon(String uid, IPConnection ipcon) {
		super(uid, ipcon);

		apiVersion[0] = 2;
		apiVersion[1] = 0;
		apiVersion[2] = 0;

		responseExpected[IPConnection.unsignedByte(FUNCTION_GET_AUTHENTICATION_NONCE)] = RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE;
		responseExpected[IPConnection.unsignedByte(FUNCTION_AUTHENTICATE)] = RESPONSE_EXPECTED_FLAG_TRUE;
	}

	public byte[] getAuthenticationNonce() throws TinkerforgeException {
		ByteBuffer bb = ipcon.createRequestPacket((byte)8, FUNCTION_GET_AUTHENTICATION_NONCE, this);

		byte[] response = sendRequest(bb.array());

		bb = ByteBuffer.wrap(response, 8, response.length - 8);
		bb.order(ByteOrder.LITTLE_ENDIAN);

		byte[] server_nonce = new byte[4];

		for (int i = 0; i < 4; i++) {
			server_nonce[i] = bb.get();
		}

		return server_nonce;
	}

	public void authenticate(byte[] client_nonce, byte[] digest) throws TinkerforgeException {
		ByteBuffer bb = ipcon.createRequestPacket((byte)32, FUNCTION_AUTHENTICATE, this);

		for (int i = 0; i < 4; i++) {
			bb.put(client_nonce[i]);
		}

		for (int i = 0; i < 20; i++) {
			bb.put(digest[i]);
		}

		sendRequest(bb.array());
	}

	public Identity getIdentity() throws TinkerforgeException {
		return null;
    }

    @Override
    public void initialize(Object config, BiConsumer<String, State> updateStateFn, BiConsumer<String, String> triggerChannelFn) throws TinkerforgeException {}

    @Override
    public void dispose(Object config) throws TinkerforgeException {}

    @Override
    public Class<?> getConfigurationClass() {
        return BrickDaemonConfig.class;
    }

    @Override
    public void refreshValue(String value, BiConsumer<String, State> updateStateFn,
            BiConsumer<String, String> triggerChannelFn) throws TinkerforgeException {
        throw new NotSupportedException();
    }

    @Override
    public void handleCommand(String channel, Command command) {

    }
}
