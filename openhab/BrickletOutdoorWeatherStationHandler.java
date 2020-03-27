/**
 * Copyright (c) 2014,2019 Contributors to the Eclipse Foundation
 *
 * See the NOTICE file(s) distributed with this work for additional
 * information regarding copyright ownership.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0
 *
 * SPDX-License-Identifier: EPL-2.0
 */
package org.eclipse.smarthome.binding.tinkerforge.internal.handler;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;
import java.util.function.Supplier;

import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.jdt.annotation.Nullable;
import org.eclipse.smarthome.binding.tinkerforge.internal.TinkerforgeThingTypeProvider;
import org.eclipse.smarthome.binding.tinkerforge.internal.Utils;
import org.eclipse.smarthome.binding.tinkerforge.internal.device.BrickletOutdoorWeatherStation;
import org.eclipse.smarthome.binding.tinkerforge.internal.device.DeviceWrapper.SetterRefresh;
import org.eclipse.smarthome.config.core.ConfigDescriptionRegistry;
import org.eclipse.smarthome.config.core.Configuration;
import org.eclipse.smarthome.core.thing.Bridge;
import org.eclipse.smarthome.core.thing.Channel;
import org.eclipse.smarthome.core.thing.ChannelUID;
import org.eclipse.smarthome.core.thing.Thing;
import org.eclipse.smarthome.core.thing.ThingStatus;
import org.eclipse.smarthome.core.thing.ThingStatusDetail;
import org.eclipse.smarthome.core.thing.ThingStatusInfo;
import org.eclipse.smarthome.core.thing.binding.BaseThingHandler;
import org.eclipse.smarthome.core.thing.binding.builder.ChannelBuilder;
import org.eclipse.smarthome.core.thing.type.ChannelDefinition;
import org.eclipse.smarthome.core.thing.type.ChannelTypeRegistry;
import org.eclipse.smarthome.core.thing.type.ThingType;
import org.eclipse.smarthome.core.types.Command;
import org.eclipse.smarthome.core.types.RefreshType;
import org.eclipse.smarthome.core.types.State;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.tinkerforge.TimeoutException;
import com.tinkerforge.TinkerforgeException;

/**
 * The {@link BrickletOutdoorWeatherStationHandler} is responsible for handling
 * commands, which are sent to one of the channels.
 *
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
public class BrickletOutdoorWeatherStationHandler extends BaseThingHandler {
    private final Logger logger = LoggerFactory.getLogger(BrickletOutdoorWeatherStationHandler.class);

    private @Nullable BrickletOutdoorWeatherStation device;

    private Supplier<ChannelTypeRegistry> channelTypeRegistrySupplier;
    private Supplier<ConfigDescriptionRegistry> configDescriptionRegistrySupplier;

    public BrickletOutdoorWeatherStationHandler(Thing thing,
            Supplier<ChannelTypeRegistry> channelTypeRegistrySupplier,
            Supplier<ConfigDescriptionRegistry> configDescriptionRegistrySupplier) {
        super(thing);
        this.channelTypeRegistrySupplier = channelTypeRegistrySupplier;
        this.configDescriptionRegistrySupplier = configDescriptionRegistrySupplier;
    }

    @Override
    public void initialize() {
        logger.debug("Initializing outdoor weather station handler {}", thing.getUID().getId());
        Bridge bridge = getBridge();
        if (bridge == null) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.CONFIGURATION_ERROR, "Bridge not found.");
            return;
        }
        @Nullable BrickletOutdoorWeatherHandler outdoorWeatherHandler = ((BrickletOutdoorWeatherHandler) bridge.getHandler());
        if (outdoorWeatherHandler == null) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.BRIDGE_UNINITIALIZED, "Bridge handler not found.");
            return;
        }

        if (device != null) {
            Utils.assertNonNull(outdoorWeatherHandler.getDevice()).removeStationDataListener(Utils.assertNonNull(device).listener);
            logger.debug("Removed old outdoor weather station {} handler", thing.getUID().getId());
        }
        device = new BrickletOutdoorWeatherStation(Utils.assertNonNull(outdoorWeatherHandler.getDevice()));
        configureChannels();

        if (bridge.getStatus() == ThingStatus.ONLINE) {
            initializeDevice();
            logger.debug("Initialized outdoor weather station handler {}", thing.getUID().getId());
        } else {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.BRIDGE_OFFLINE);
            logger.debug("Bridge of outdoor weather station {} offline", thing.getUID().getId());
        }
    }

    private Configuration getChannelConfiguration(String channelID) {
        @Nullable Channel c = getThing().getChannel(channelID);
        if (c == null) {
            throw new IllegalArgumentException(String.format("Channel %s not found", channelID));
        }
        return c.getConfiguration();
    }

    private void initializeDevice() {
        logger.debug("Initializing outdoor weather station {}", thing.getUID().getId());
        Bridge bridge = getBridge();
        if (bridge == null) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.BRIDGE_UNINITIALIZED);
            return;
        }

        @Nullable BrickletOutdoorWeatherHandler outdoorWeatherHandler = ((BrickletOutdoorWeatherHandler) bridge.getHandler());
        if (outdoorWeatherHandler == null) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.BRIDGE_UNINITIALIZED, "Bridge handler not found.");
            return;
        }

        BrickletOutdoorWeatherStation dev = device;
        if (dev != null)
            Utils.assertNonNull(outdoorWeatherHandler.getDevice()).removeStationDataListener(dev.listener);

        dev = new BrickletOutdoorWeatherStation(Utils.assertNonNull(outdoorWeatherHandler.getDevice()));
        this.device = dev;
        dev.initialize(getConfig(), this::getChannelConfiguration, this::updateState, this::triggerChannel,
                scheduler, this);
        logger.debug("Initialized outdoor weather station {}", thing.getUID().getId());
        updateStatus(ThingStatus.ONLINE, ThingStatusDetail.NONE);

        this.getThing().getChannels().stream().filter(c -> !Utils.assertNonNull(c.getChannelTypeUID()).toString().startsWith("system"))
                .forEach(c -> handleCommand(c.getUID(), RefreshType.REFRESH));
    }

    @Override
    public void bridgeStatusChanged(ThingStatusInfo bridgeStatusInfo) {
        if (bridgeStatusInfo.getStatus() == ThingStatus.ONLINE) {
            initializeDevice();
        } else if (bridgeStatusInfo.getStatus() == ThingStatus.OFFLINE) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.BRIDGE_OFFLINE);
        }
    }

    @Override
    protected void updateState(String channelID, State state) {
        super.updateState(channelID, state);
        updateStatus(ThingStatus.ONLINE);
    }

    @Override
    protected void triggerChannel(String channelID, String event) {
        super.triggerChannel(channelID, event);
        updateStatus(ThingStatus.ONLINE);
    }

    private void reportTimeout() {
        @Nullable Bridge bridge = getBridge();
        if (bridge == null) {
            return;
        }

        @Nullable BrickletOutdoorWeatherHandler handler = (BrickletOutdoorWeatherHandler) (bridge.getHandler());
        if (handler == null) {
            return;
        }

        handler.handleTimeout();
    }

    private void refreshValue(String channelId, Configuration channelConfig) {
        try {
            @Nullable BrickletOutdoorWeatherStation dev = this.device;
            if (dev == null) {
                return;
            }
            dev.refreshValue(channelId, getConfig(), channelConfig, this::updateState, this::triggerChannel);
            updateStatus(ThingStatus.ONLINE);
        } catch (TinkerforgeException e) {
            if (e instanceof TimeoutException) {
                logger.debug("Failed to refresh value for {}: {}", channelId, e.getMessage());
                reportTimeout();
            } else {
                logger.warn("Failed to refresh value for {}: {}", channelId, e.getMessage());
            }
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.COMMUNICATION_ERROR);
        }
    }

    @Override
    public void handleCommand(ChannelUID channelUID, Command command) {
        @Nullable Bridge bridge = this.getBridge();
        if (bridge == null) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.CONFIGURATION_ERROR, "Bridge not found.");
            return;
        }
        if (bridge.getStatus() == ThingStatus.OFFLINE) {
            return;
        }

        @Nullable Channel channel = getThing().getChannel(channelUID);
        if (channel == null) {
            logger.info("Received command {} for unknown channel {}.", command.toFullString(),
                        channelUID.toString());
            return;
        }

        try {
            if (command instanceof RefreshType) {
                refreshValue(channelUID.getId(), channel.getConfiguration());
            } else {
                @Nullable BrickletOutdoorWeatherStation dev = device;
                if (dev == null) {
                    return;
                }
                List<SetterRefresh> refreshs = dev.handleCommand(getConfig(), channel
                        .getConfiguration(), channelUID.getId(), command);
                refreshs.forEach(r -> scheduler.schedule(
                        () -> refreshValue(r.channel, Utils.assertNonNull(getThing().getChannel(r.channel)).getConfiguration()), r.delay,
                        TimeUnit.MILLISECONDS));
            }
        } catch (TinkerforgeException e) {
            if (e instanceof TimeoutException) {
                logger.debug("Failed to send command {} to channel {}: {}", command.toFullString(),
                        channelUID.toString(), e.getMessage());
                reportTimeout();
            } else {
                logger.warn("Failed to send command {} to channel {}: {}", command.toFullString(),
                        channelUID.toString(), e.getMessage());
            }
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.COMMUNICATION_ERROR);
        }
    }

    private void configureChannels() {
        List<String> enabledChannelNames = new ArrayList<>();
        try {
            enabledChannelNames = Utils.assertNonNull(device).getEnabledChannels(getConfig());
        } catch (TinkerforgeException e) {
            if (e instanceof TimeoutException) {
                logger.debug("Failed to get enabled channels for device {}: {}", this.getThing().getUID().toString(),
                        e.getMessage());
                reportTimeout();
            } else {
                logger.warn("Failed to get enabled channels for device {}: {}", this.getThing().getUID().toString(),
                        e.getMessage());
            }
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.COMMUNICATION_ERROR);
        }

        ThingType tt = TinkerforgeThingTypeProvider.getThingTypeStatic(this.getThing().getThingTypeUID(), null);
        if(tt == null) {
            logger.warn("Failed to get thing type for device {}", this.getThing().getUID().toString());
            return;
        }

        List<Channel> enabledChannels = new ArrayList<>();
        for (String s : enabledChannelNames) {
            ChannelUID cuid = new ChannelUID(getThing().getUID(), s);
            ChannelDefinition def = tt.getChannelDefinitions().stream().filter(d -> d.getId().equals(cuid.getId()))
                    .findFirst().get();
            Channel newChannel = Utils.buildChannel(tt, getThing().getUID(), def, channelTypeRegistrySupplier.get(), configDescriptionRegistrySupplier.get(), logger);

            Channel existingChannel = this.thing.getChannel(newChannel.getUID());
            if (existingChannel != null)
                newChannel = ChannelBuilder.create(newChannel).withConfiguration(existingChannel.getConfiguration())
                        .build();

            enabledChannels.add(newChannel);
        }

        updateThing(editThing().withChannels(enabledChannels).build());
    }
}
