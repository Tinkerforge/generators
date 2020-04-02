/**
 * Copyright (c) 2010-2020 Contributors to the openHAB project
 *
 * See the NOTICE file(s) distributed with this work for additional
 * information.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0
 *
 * SPDX-License-Identifier: EPL-2.0
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

import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.jdt.annotation.Nullable;
import org.eclipse.smarthome.binding.tinkerforge.internal.TinkerforgeBindingConstants;
import org.eclipse.smarthome.binding.tinkerforge.internal.handler.BrickletRemoteSwitchHandler;
import org.eclipse.smarthome.binding.tinkerforge.internal.handler.Task;
import org.eclipse.smarthome.config.core.ConfigDescription;
import org.eclipse.smarthome.config.core.ConfigDescriptionBuilder;
import org.eclipse.smarthome.config.core.ConfigDescriptionParameter.Type;
import org.eclipse.smarthome.config.core.ConfigDescriptionParameterBuilder;
import org.eclipse.smarthome.config.core.Configuration;
import org.eclipse.smarthome.core.library.types.StringType;
import org.eclipse.smarthome.core.thing.ThingTypeUID;
import org.eclipse.smarthome.core.thing.binding.BaseThingHandler;
import org.eclipse.smarthome.core.thing.type.ChannelDefinitionBuilder;
import org.eclipse.smarthome.core.thing.type.ChannelType;
import org.eclipse.smarthome.core.thing.type.ChannelTypeBuilder;
import org.eclipse.smarthome.core.thing.type.ChannelTypeUID;
import org.eclipse.smarthome.core.thing.type.ThingType;
import org.eclipse.smarthome.core.thing.type.ThingTypeBuilder;
import org.eclipse.smarthome.core.types.Command;
import org.eclipse.smarthome.core.types.CommandDescriptionBuilder;
import org.eclipse.smarthome.core.types.CommandOption;
import org.eclipse.smarthome.core.types.State;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.tinkerforge.Device.Identity;
import com.tinkerforge.TinkerforgeException;

/**
 * Fake device modelling a remote socket type A controlled by a remote switch bricklet.
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
public class RemoteSocketTypeA implements DeviceWrapper {
    public RemoteSocketTypeA(BrickletRemoteSwitchHandler handler) {
        this.handler = handler;
    }

    private List<ScheduledFuture<?>> manualChannelUpdates = new ArrayList<>();
    private List<ListenerReg<?>> listenerRegs = new ArrayList<>();

    public void cancelManualUpdates() {
        manualChannelUpdates.forEach(f -> f.cancel(true));
    }

    public <T> T reg(T listener, Consumer<T> toRemove) {
        listenerRegs.add(new ListenerReg<T>(listener, toRemove));
        return listener;
    }

    @Override
    public void dispose(Configuration config) throws TinkerforgeException {
        listenerRegs.forEach(ListenerReg::deregister);
    }

    private final BrickletRemoteSwitchHandler handler;

    public final static int DEVICE_IDENTIFIER = -235;
    public final static String DEVICE_DISPLAY_NAME = "Remote Socket Type A";

    public final static DeviceInfo DEVICE_INFO = new DeviceInfo(DEVICE_DISPLAY_NAME, "remotesockettypea",
            DEVICE_IDENTIFIER, RemoteSocketTypeA.class, DefaultActions.class, "1.0.0", false);

    private final Logger logger = LoggerFactory.getLogger(RemoteSocketTypeA.class);
    private final static Logger static_logger = LoggerFactory.getLogger(RemoteSocketTypeA.class);

    public List<String> getEnabledChannels(org.eclipse.smarthome.config.core.Configuration config)
            throws TinkerforgeException {
        return Arrays.asList("RemoteSocketTypeACommand");
    }

    public static @Nullable ChannelType getChannelType(ChannelTypeUID channelTypeUID) {
        switch (channelTypeUID.getId()) {
            case "RemoteSocketTypeACommand":
                return ChannelTypeBuilder
                        .state(new ChannelTypeUID("tinkerforge", "RemoteSocketTypeACommand"), "Command", "String")
                        .withConfigDescriptionURI(URI.create("channel-type:tinkerforge:RemoteSocketTypeACommand"))
                        .withCommandDescription(
                                CommandDescriptionBuilder.create()
                                        .withCommandOption(new CommandOption("ON", "Switch On"))
                                        .withCommandOption(new CommandOption("OFF", "Switch Off")).build()).build();
            default:
                static_logger.debug("Unknown channel type ID {}", channelTypeUID.getId());
                break;
        }

        return null;
    }

    public static ThingType getThingType(ThingTypeUID thingTypeUID) {
        return ThingTypeBuilder
                .instance(thingTypeUID, "Tinkerforge Remote Socket Type A")
                .isListed(true)
                .withSupportedBridgeTypeUIDs(
                        Arrays.asList(TinkerforgeBindingConstants.THING_TYPE_BRICKLET_REMOTE_SWITCH.toString(),
                                TinkerforgeBindingConstants.THING_TYPE_BRICKLET_REMOTE_SWITCH_V2.toString()))
                .withConfigDescriptionURI(URI.create("thing-type:tinkerforge:" + thingTypeUID.getId()))
                .withDescription(
                        "Remote controlled mains switch (type A) for Remote Switch Bricklet or Remote Switch Bricklet 2.0")
                .withChannelDefinitions(
                        Arrays.asList(new ChannelDefinitionBuilder("RemoteSocketTypeACommand", new ChannelTypeUID(
                                "tinkerforge", "RemoteSocketTypeACommand")).withLabel("Command").build())).build();
    }

    public static @Nullable ConfigDescription getConfigDescription(URI uri) {
        switch (uri.toASCIIString()) {
            case "thing-type:tinkerforge:remotesockettypea":
                return ConfigDescriptionBuilder
                        .create(uri)
                        .withParameters(
                                Arrays.asList(
                                        ConfigDescriptionParameterBuilder.create("houseCode", Type.INTEGER)
                                                .withDefault("0")
                                                .withDescription("The house code of the remote socket to control.")
                                                .withMinimum(BigDecimal.valueOf(0)).withMaximum(BigDecimal.valueOf(31))
                                                .build(),
                                        ConfigDescriptionParameterBuilder.create("receiverCode", Type.INTEGER)
                                                .withDefault("0")
                                                .withDescription("The receiver code of the remote socket to control.")
                                                .withMinimum(BigDecimal.valueOf(0)).withMaximum(BigDecimal.valueOf(31))
                                                .build(),
                                        ConfigDescriptionParameterBuilder
                                                .create("repeats", Type.INTEGER)
                                                .withDefault("5")
                                                .withDescription(
                                                        "Sets the number of times the code is sent when of the socket is toggled. The repeats basically correspond to the amount of time that a button of the remote is pressed.")
                                                .withMinimum(BigDecimal.valueOf(0))
                                                .withMaximum(BigDecimal.valueOf(255)).build())).build();
            case "channel-type:tinkerforge:RemoteSocketTypeACommand":
                return ConfigDescriptionBuilder.create(uri).build();
            default:
                static_logger.debug("Unknown config description URI {}", uri.toASCIIString());
                break;
        }
        return null;
    }

    public void refreshValue(String value, org.eclipse.smarthome.config.core.Configuration config,
            org.eclipse.smarthome.config.core.Configuration channelConfig,
            BiConsumer<String, org.eclipse.smarthome.core.types.State> updateStateFn,
            BiConsumer<String, String> triggerChannelFn) throws TinkerforgeException {
        switch (value) {
            case "RemoteSocketTypeACommand":
                break;
            default:
                logger.warn("Refresh for unknown channel {}", value);
                break;
        }
    }

    public List<SetterRefresh> handleCommand(org.eclipse.smarthome.config.core.Configuration config,
            org.eclipse.smarthome.config.core.Configuration channelConfig, String channel, Command command)
            throws TinkerforgeException {
        List<SetterRefresh> result = Collections.emptyList();
        RemoteSocketTypeAConfig cfg = (RemoteSocketTypeAConfig) config.as(RemoteSocketTypeAConfig.class);
        switch (channel) {
            case "RemoteSocketTypeACommand":
                if (command instanceof StringType) {
                    StringType cmd = (StringType) command;
                    handler.enqueue(new Task(rs -> {
                        rs.setRepeats(cfg.repeats);
                        rs.switchSocketA(cfg.houseCode, cfg.receiverCode, cmd.toString().equals("ON") ? 1 : 0);
                    }, success -> {
                        if (!success)
                            logger.warn("House {} Receiver {} command {} failed", cfg.houseCode, cfg.receiverCode,
                                    cmd.toString());
                    }));
                }

                else {
                    logger.warn("Command type {} not supported for channel {}. Please use one of StringType.", command
                            .getClass().getName(), channel);
                }

                break;
            default:
                logger.warn("Command for unknown channel {}", channel);
        }
        return result;
    }

    @Override
    public void initialize(Configuration config, Function<String, Configuration> getChannelConfigFn,
            BiConsumer<String, State> updateStateFn, BiConsumer<String, String> triggerChannelFn,
            ScheduledExecutorService scheduler, BaseThingHandler handler) throws TinkerforgeException {

    }

    @Override
    public Identity getIdentity() throws TinkerforgeException {
        return new Identity();
    }
}
