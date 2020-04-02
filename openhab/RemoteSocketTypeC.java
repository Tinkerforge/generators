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
import org.eclipse.smarthome.config.core.ParameterOption;
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
 * Fake device modelling a remote socket type C controlled by a remote switch bricklet.
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
public class RemoteSocketTypeC implements DeviceWrapper {
    public RemoteSocketTypeC(BrickletRemoteSwitchHandler handler) {
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

    public static final int DEVICE_IDENTIFIER = -235;
    public static final String DEVICE_DISPLAY_NAME = "Remote Socket Type C";

    public static final DeviceInfo DEVICE_INFO = new DeviceInfo(DEVICE_DISPLAY_NAME, "remotesockettypec",
            DEVICE_IDENTIFIER, RemoteSocketTypeC.class, DefaultActions.class, "1.0.0", false);

    private final Logger logger = LoggerFactory.getLogger(RemoteSocketTypeC.class);

    public List<String> getEnabledChannels(org.eclipse.smarthome.config.core.Configuration config)
            throws TinkerforgeException {
        return Arrays.asList("RemoteSocketTypeCCommand");
    }

    public static @Nullable ChannelType getChannelType(ChannelTypeUID channelTypeUID) {
        switch (channelTypeUID.getId()) {
            case "RemoteSocketTypeCCommand":
                return ChannelTypeBuilder
                        .state(new ChannelTypeUID("tinkerforge", "RemoteSocketTypeCCommand"), "Command", "String")
                        .withConfigDescriptionURI(URI.create("channel-type:tinkerforge:RemoteSocketTypeCCommand"))
                        .withCommandDescription(
                                CommandDescriptionBuilder.create()
                                        .withCommandOption(new CommandOption("ON", "Switch On"))
                                        .withCommandOption(new CommandOption("OFF", "Switch Off")).build()).build();
            default:
                break;
        }

        return null;
    }

    public static ThingType getThingType(ThingTypeUID thingTypeUID) {
        return ThingTypeBuilder
                .instance(thingTypeUID, "Tinkerforge Remote Socket Type C")
                .isListed(true)
                .withSupportedBridgeTypeUIDs(
                        Arrays.asList(TinkerforgeBindingConstants.THING_TYPE_BRICKLET_REMOTE_SWITCH.toString(),
                                TinkerforgeBindingConstants.THING_TYPE_BRICKLET_REMOTE_SWITCH_V2.toString()))
                .withConfigDescriptionURI(URI.create("thing-type:tinkerforge:" + thingTypeUID.getId()))
                .withDescription(
                        "Remote controlled mains switch (Type C) for Remote Switch Bricklet or Remote Switch Bricklet 2.0")
                .withChannelDefinitions(
                        Arrays.asList(new ChannelDefinitionBuilder("RemoteSocketTypeCCommand", new ChannelTypeUID(
                                "tinkerforge", "RemoteSocketTypeCCommand")).withLabel("Command").build())).build();
    }

    public static @Nullable ConfigDescription getConfigDescription(URI uri) {
        switch (uri.toASCIIString()) {
            case "thing-type:tinkerforge:remotesockettypec":
                return ConfigDescriptionBuilder
                        .create(uri)
                        .withParameters(
                                Arrays.asList(
                                        ConfigDescriptionParameterBuilder
                                                .create("systemCode", Type.TEXT)
                                                .withDefault("A")
                                                .withDescription("The system code of the remote socket to control.")
                                                .withOptions(
                                                        Arrays.asList(new ParameterOption("A", "A"),
                                                                new ParameterOption("B", "B"), new ParameterOption("C",
                                                                        "C"), new ParameterOption("D", "D"),
                                                                new ParameterOption("E", "E"), new ParameterOption("F",
                                                                        "F"), new ParameterOption("G", "G"),
                                                                new ParameterOption("H", "H"), new ParameterOption("I",
                                                                        "I"), new ParameterOption("J", "J"),
                                                                new ParameterOption("K", "K"), new ParameterOption("L",
                                                                        "L"), new ParameterOption("M", "M"),
                                                                new ParameterOption("N", "N"), new ParameterOption("O",
                                                                        "O"), new ParameterOption("P", "P"))).build(),
                                        ConfigDescriptionParameterBuilder.create("deviceCode", Type.INTEGER)
                                                .withDefault("1")
                                                .withDescription("The device code of the remote socket to control.")
                                                .withMinimum(BigDecimal.valueOf(1)).withMaximum(BigDecimal.valueOf(16))
                                                .build(),
                                        ConfigDescriptionParameterBuilder
                                                .create("repeats", Type.INTEGER)
                                                .withDefault("5")
                                                .withDescription(
                                                        "Sets the number of times the code is sent when of the socket is toggled. The repeats basically correspond to the amount of time that a button of the remote is pressed.")
                                                .withMinimum(BigDecimal.valueOf(0))
                                                .withMaximum(BigDecimal.valueOf(255)).build())).build();
            case "channel-type:tinkerforge:RemoteSocketTypeCCommand":
                return ConfigDescriptionBuilder.create(uri).build();
            default:
                break;
        }
        return null;
    }

    public void refreshValue(String value, org.eclipse.smarthome.config.core.Configuration config,
            org.eclipse.smarthome.config.core.Configuration channelConfig,
            BiConsumer<String, org.eclipse.smarthome.core.types.State> updateStateFn,
            BiConsumer<String, String> triggerChannelFn) throws TinkerforgeException {
        switch (value) {
            case "RemoteSocketTypeCCommand":
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
        RemoteSocketTypeCConfig cfg = (RemoteSocketTypeCConfig) config.as(RemoteSocketTypeCConfig.class);
        switch (channel) {
            case "RemoteSocketTypeCCommand":
                if (command instanceof StringType) {
                    StringType cmd = (StringType) command;
                    handler.enqueue(new Task(
                            rs -> {
                                rs.setRepeats(cfg.repeats);
                                rs.switchSocketC(cfg.systemCode.charAt(0), cfg.deviceCode,
                                        cmd.toString().equals("ON") ? 1 : 0);
                            }, success -> {
                                if (!success)
                                    logger.warn("Address {} Unit {} command {} failed", cfg.systemCode.charAt(0),
                                            cfg.deviceCode, cmd.toString());
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
