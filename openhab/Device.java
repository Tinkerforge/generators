/*
 * Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
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

import org.eclipse.smarthome.config.core.ConfigDescription;
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

	/**
	 * Creates the device object with the unique device ID \c uid and adds
	 * it to the IPConnection \c ipcon.
	 */
	public Device(String uid, IPConnection ipcon) {
		super(uid, ipcon);

		ipcon.devices.put(this.uid, this); // FIXME: use weakref here
	}

    public abstract Identity getIdentity() throws TinkerforgeException;

    public abstract void initialize(Object config, BiConsumer<String, State> updateStateFn, BiConsumer<String, String> triggerChannelFn) throws TinkerforgeException;

    public abstract void dispose(Object config) throws TinkerforgeException;

    public abstract Class<?> getConfigurationClass();

    public abstract void refreshValue(String value, BiConsumer<String, State> updateStateFn, BiConsumer<String, String> triggerChannelFn) throws TinkerforgeException;

    public abstract void handleCommand(Object config, String channel, Command command) throws TinkerforgeException;

    public abstract List<String> getEnabledChannels(Object config);

    /*public abstract ThingType getThingType(ThingTypeUID thingTypeUID);

    public abstract ChannelType getChannelType(ChannelTypeUID channelTypeUID);

    public abstract ConfigDescription getConfigDescription(URI uri);*/
}
