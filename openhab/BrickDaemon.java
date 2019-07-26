/*
 * Copyright (C) 2012-2014 Matthias Bolte <matthias@tinkerforge.com>
 * Copyright (C) 2011-2012 Olaf Lüke <olaf@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

package com.tinkerforge;

import java.math.BigDecimal;
import java.net.URI;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.function.BiConsumer;
import java.util.function.Function;

import org.eclipse.smarthome.config.core.ConfigDescription;
import org.eclipse.smarthome.config.core.ConfigDescriptionParameterBuilder;
import org.eclipse.smarthome.config.core.Configuration;
import org.eclipse.smarthome.config.core.ConfigDescriptionParameter.Type;
import org.eclipse.smarthome.core.thing.ThingTypeUID;
import org.eclipse.smarthome.core.thing.type.ChannelType;
import org.eclipse.smarthome.core.thing.type.ChannelTypeUID;
import org.eclipse.smarthome.core.thing.type.ThingType;
import org.eclipse.smarthome.core.thing.type.ThingTypeBuilder;
import org.eclipse.smarthome.core.types.Command;
import org.eclipse.smarthome.core.types.State;

public class BrickDaemon extends Device {
	public final static int DEVICE_IDENTIFIER = -1;
	public final static String DEVICE_DISPLAY_NAME = "Brick Daemon";

    public final static DeviceInfo DEVICE_INFO = new DeviceInfo(DEVICE_DISPLAY_NAME, "brickd", DEVICE_IDENTIFIER, BrickDaemon.class);

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
    public void initialize(Configuration config, Function<String, Configuration> channelConfigFn, BiConsumer<String, State> updateStateFn, BiConsumer<String, String> triggerChannelFn) throws TinkerforgeException {}

    @Override
    public void dispose(Configuration config) throws TinkerforgeException {}

    @Override
    public void refreshValue(String value, BiConsumer<String, State> updateStateFn,
            BiConsumer<String, String> triggerChannelFn) throws TinkerforgeException {
        throw new NotSupportedException();
    }

    @Override
    public void handleCommand(Configuration config, Configuration channelConfig, String channel, Command command) throws TinkerforgeException {

    }

    @Override
    public List<String> getEnabledChannels(Configuration config) {
        return new ArrayList<>();
    }

    public static ThingType getThingType(ThingTypeUID thingTypeUID) {
        return ThingTypeBuilder.instance(thingTypeUID, "Brick Daemon")
                               .isListed(true)
                               .withDescription("A connection to a Brick Daemon, Ethernet Extension or WIFI Extension.")
                               .withConfigDescriptionURI(URI.create("thing-type:tinkerforge:brickd"))
                               .buildBridge();
    }

    public static ChannelType getChannelType(ChannelTypeUID channelTypeUID) {
        return null;
    }

    public static ConfigDescription getConfigDescription(URI uri) {
        switch(uri.toASCIIString()) {
            case "thing-type:tinkerforge:brickd":
                return new ConfigDescription(uri, Arrays.asList(
                    ConfigDescriptionParameterBuilder.create("host", Type.TEXT)
                                                     .withLabel("Brick Daemon Hostname/IP")
                                                     .withDescription("The IP/hostname of the Brick Daemon, Ethernet Extension or WIFI Extension.")
                                                     .withContext("network-address")
                                                     .withAdvanced(false)
                                                     .withDefault("localhost")
                                                     .build(),
                    ConfigDescriptionParameterBuilder.create("port", Type.INTEGER)
                                                     .withLabel("Brick Daemon Port")
                                                     .withDescription("The port is optional, if none is provided, the standard port 4223 is used.")
                                                     .withContext("network-address")
                                                     .withAdvanced(false)
                                                     .withDefault("4223")
                                                     .withMinimum(BigDecimal.valueOf(1))
                                                     .withMaximum(BigDecimal.valueOf(65535))
                                                     .withStepSize(BigDecimal.valueOf(1))
                                                     .build(),
                    ConfigDescriptionParameterBuilder.create("enableReconnect", Type.BOOLEAN)
                                                     .withLabel("Enable reconnects")
                                                     .withDescription("Enable reattempting to connect to the Brick Daemon instance if the connection could not be established.")
                                                     .withAdvanced(true)
                                                     .withDefault("true")
                                                     .build(),
                    ConfigDescriptionParameterBuilder.create("reconnectInterval", Type.DECIMAL)
                                                     .withLabel("Reconnect Interval")
                                                     .withDescription("Seconds to wait between attempts to connect.")
                                                     .withAdvanced(true)
                                                     .withDefault("10.0")
                                                     .withUnit("s")
                                                     .build(),
                    ConfigDescriptionParameterBuilder.create("auth", Type.BOOLEAN)
                                                     .withLabel("Use authentication")
                                                     .withDescription("Use authentication when connecting to the Brick Daemon.")
                                                     .withAdvanced(true)
                                                     .withDefault("false")
                                                     .build(),
                    ConfigDescriptionParameterBuilder.create("password", Type.TEXT)
                                                     .withLabel("Password")
                                                     .withDescription("The password to use for authenticating.")
                                                     .withContext("password")
                                                     .withAdvanced(true)
                                                     .build(),
                    ConfigDescriptionParameterBuilder.create("enableBackgroundDiscovery", Type.BOOLEAN)
                                                     .withLabel("Enable Background Discovery")
                                                     .withDescription("This will check periodically for new devices attached to the Brick Daemon, Ethernet Extension or WIFI Extension.")
                                                     .withAdvanced(true)
                                                     .withDefault("true")
                                                     .build(),
                    ConfigDescriptionParameterBuilder.create("backgroundDiscoveryInterval", Type.DECIMAL)
                                                     .withLabel("Background Discovery Interval")
                                                     .withDescription("Minutes to wait between Background Discovery Scans.")
                                                     .withAdvanced(true)
                                                     .withDefault("10.0")
                                                     .withUnit("min")
                                                     .build()
                ));
        }
        return null;
    }
}
