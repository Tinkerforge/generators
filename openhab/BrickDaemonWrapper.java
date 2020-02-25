/*
 * Copyright (C) 2012-2014 Matthias Bolte <matthias@tinkerforge.com>
 * Copyright (C) 2011-2012 Olaf Lüke <olaf@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

package org.eclipse.smarthome.binding.tinkerforge.internal.device;

import java.math.BigDecimal;
import java.net.URI;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.function.BiConsumer;
import java.util.function.Consumer;
import java.util.function.Function;

import com.tinkerforge.Device.Identity;
import com.tinkerforge.IPConnection;
import com.tinkerforge.TinkerforgeException;

import org.eclipse.smarthome.config.core.ConfigDescription;
import org.eclipse.smarthome.config.core.ConfigDescriptionBuilder;
import org.eclipse.smarthome.config.core.ConfigDescriptionParameterBuilder;
import org.eclipse.smarthome.config.core.Configuration;
import org.eclipse.smarthome.config.core.ConfigDescriptionParameter.Type;
import org.eclipse.smarthome.core.thing.ThingTypeUID;
import org.eclipse.smarthome.core.thing.binding.BaseThingHandler;
import org.eclipse.smarthome.core.thing.type.ChannelType;
import org.eclipse.smarthome.core.thing.type.ChannelTypeUID;
import org.eclipse.smarthome.core.thing.type.ThingType;
import org.eclipse.smarthome.core.thing.type.ThingTypeBuilder;
import org.eclipse.smarthome.core.types.Command;
import org.eclipse.smarthome.core.types.State;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class BrickDaemonWrapper implements DeviceWrapper {
    public final static DeviceInfo DEVICE_INFO = new DeviceInfo("Brick Daemon", "brickd", -1, BrickDaemonWrapper.class,
            DefaultActions.class, "2.0.0", false);

    private final static Logger logger = LoggerFactory.getLogger(BrickDaemonWrapper.class);

    public BrickDaemonWrapper(String uid, IPConnection ipcon) {
        super();
    }

    private List<ScheduledFuture<?>> manualChannelUpdates = new ArrayList<ScheduledFuture<?>>();
    private List<ListenerReg> listenerRegs = new ArrayList<ListenerReg>();

    public void cancelManualUpdates() {
        manualChannelUpdates.forEach(f -> f.cancel(true));
    }

    public <T> T reg(T listener, Consumer<T> toRemove) {
        listenerRegs.add(new ListenerReg<T>(listener, toRemove));
        return listener;
    }

    @Override
    public void initialize(org.eclipse.smarthome.config.core.Configuration config,
            Function<String, org.eclipse.smarthome.config.core.Configuration> getChannelConfigFn,
            BiConsumer<String, org.eclipse.smarthome.core.types.State> updateStateFn,
            BiConsumer<String, String> triggerChannelFn, ScheduledExecutorService scheduler, BaseThingHandler handler)
            throws TinkerforgeException {
    }

    @Override
    public void dispose(Configuration config) throws TinkerforgeException {
        listenerRegs.forEach(reg -> reg.toRemove.accept(reg.listener));
    }

    @Override
    public void refreshValue(String value, Configuration config, Configuration channelConfig,
            BiConsumer<String, State> updateStateFn, BiConsumer<String, String> triggerChannelFn)
            throws TinkerforgeException {
        return;
    }

    @Override
    public List<SetterRefresh> handleCommand(Configuration config, Configuration channelConfig, String channel,
            Command command) throws TinkerforgeException {
        return Collections.emptyList();
    }

    @Override
    public List<String> getEnabledChannels(Configuration config) throws TinkerforgeException {
        return new ArrayList<>();
    }

    public static ThingType getThingType(ThingTypeUID thingTypeUID) {
        return ThingTypeBuilder.instance(thingTypeUID, "Brick Daemon").isListed(true)
                .withDescription("A connection to a Brick Daemon, Ethernet Extension or WIFI Extension.")
                .withConfigDescriptionURI(URI.create("thing-type:tinkerforge:brickd")).buildBridge();
    }

    public static ChannelType getChannelType(ChannelTypeUID channelTypeUID) {
        return null;
    }

    public static ConfigDescription getConfigDescription(URI uri) {
        switch (uri.toASCIIString()) {
        case "thing-type:tinkerforge:brickd":
            return ConfigDescriptionBuilder.create(uri).withParameters(Arrays.asList(
                    ConfigDescriptionParameterBuilder.create("host", Type.TEXT).withLabel("Brick Daemon Hostname/IP")
                            .withDescription(
                                    "The IP/hostname of the Brick Daemon, Ethernet Extension or WIFI Extension.")
                            .withContext("network-address").withAdvanced(false).withDefault("localhost").build(),
                    ConfigDescriptionParameterBuilder.create("port", Type.INTEGER).withLabel("Brick Daemon Port")
                            .withDescription(
                                    "The port is optional, if none is provided, the standard port 4223 is used.")
                            .withContext("network-address").withAdvanced(false).withDefault("4223")
                            .withMinimum(BigDecimal.valueOf(1)).withMaximum(BigDecimal.valueOf(65535))
                            .withStepSize(BigDecimal.valueOf(1)).build(),
                    ConfigDescriptionParameterBuilder.create("auth", Type.BOOLEAN).withLabel("Use authentication")
                            .withDescription("Use authentication when connecting to the Brick Daemon.")
                            .withAdvanced(true).withDefault("false").build(),
                    ConfigDescriptionParameterBuilder.create("password", Type.TEXT).withLabel("Password")
                            .withDescription("The password to use for authenticating.").withContext("password")
                            .withAdvanced(true).build(),
                    ConfigDescriptionParameterBuilder.create("enableBackgroundDiscovery", Type.BOOLEAN)
                            .withLabel("Enable Background Discovery")
                            .withDescription(
                                    "This will check periodically for new devices attached to the Brick Daemon, Ethernet Extension or WIFI Extension.")
                            .withAdvanced(true).withDefault("true").build(),
                    ConfigDescriptionParameterBuilder.create("backgroundDiscoveryInterval", Type.DECIMAL)
                            .withLabel("Background Discovery Interval")
                            .withDescription("Minutes to wait between Background Discovery Scans.").withAdvanced(true)
                            .withDefault("10.0").withUnit("min").build()))
                    .build();
        }
        logger.debug("Unknown config description URI {}", uri);
        return null;
    }

    @Override
    public Identity getIdentity() throws TinkerforgeException {
        return null;
    }
}
