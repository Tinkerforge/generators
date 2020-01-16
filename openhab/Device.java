/*
 * Copyright (C) 2012-2013, 2020 Matthias Bolte <matthias@tinkerforge.com>
 * Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

package com.tinkerforge;

import java.net.URI;
import java.util.Arrays;
import java.util.List;
import java.util.function.BiConsumer;
import java.util.function.Function;

import org.eclipse.smarthome.config.core.ConfigDescription;
import org.eclipse.smarthome.config.core.Configuration;
import org.eclipse.smarthome.core.types.State;
import org.eclipse.smarthome.core.types.Command;
import org.eclipse.smarthome.core.thing.ThingTypeUID;
import org.eclipse.smarthome.core.thing.type.ChannelType;
import org.eclipse.smarthome.core.thing.type.ChannelTypeUID;
import org.eclipse.smarthome.core.thing.type.ThingType;

public abstract class Device extends DeviceBase {
	public class Identity {
		public String uid;
		public String connectedUid;
		public char position;
		public short[] hardwareVersion = new short[3];
		public short[] firmwareVersion = new short[3];
		public int deviceIdentifier;

		public String toString() {
			return "[" + "uid = " + uid + ", " + "connectedUid = " + connectedUid + ", " +
			       "position = " + position + ", " + "hardwareVersion = " + Arrays.toString(hardwareVersion) + ", " +
			       "firmwareVersion = " + Arrays.toString(firmwareVersion) + ", " +
			       "deviceIdentifier = " + deviceIdentifier + "]";
		}
    }

    public class SetterRefresh {
        public final String channel;
        public final long delay;

        public SetterRefresh(String channel, long delay) {
            this.channel = channel;
            this.delay = delay;
        }
    }

	/**
	 * Creates the device object with the unique device ID \c uid and adds
	 * it to the IPConnection \c ipcon.
	 */
	public Device(String uid, IPConnection ipcon) {
		super(uid, ipcon);

		ipcon.devices.put(this.uidNumber, this); // FIXME: use weakref here
	}

    public abstract Identity getIdentity() throws TinkerforgeException;

    public abstract void initialize(Configuration config, Function<String, Configuration> getChannelConfigFn, BiConsumer<String, State> updateStateFn, BiConsumer<String, String> triggerChannelFn) throws TinkerforgeException;

    public abstract void dispose(Configuration config) throws TinkerforgeException;

    public abstract void refreshValue(String value, Configuration config, Configuration channelConfig, BiConsumer<String, State> updateStateFn, BiConsumer<String, String> triggerChannelFn) throws TinkerforgeException;

    public abstract List<SetterRefresh> handleCommand(Configuration config, Configuration channelConfig, String channel, Command command) throws TinkerforgeException;

    public abstract List<String> getEnabledChannels(Configuration config) throws TinkerforgeException;

    /*public abstract ThingType getThingType(ThingTypeUID thingTypeUID);

    public abstract ChannelType getChannelType(ChannelTypeUID channelTypeUID);

    public abstract ConfigDescription getConfigDescription(URI uri);*/
}
