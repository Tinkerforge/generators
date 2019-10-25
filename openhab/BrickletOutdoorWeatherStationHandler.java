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

import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.jdt.annotation.Nullable;
import org.eclipse.smarthome.binding.tinkerforge.internal.TinkerforgeChannelTypeProvider;
import org.eclipse.smarthome.binding.tinkerforge.internal.TinkerforgeThingTypeProvider;
import org.eclipse.smarthome.config.core.Configuration;
import org.eclipse.smarthome.core.thing.Bridge;
import org.eclipse.smarthome.core.thing.Channel;
import org.eclipse.smarthome.core.thing.ChannelUID;
import org.eclipse.smarthome.core.thing.CommonTriggerEvents;
import org.eclipse.smarthome.core.thing.Thing;
import org.eclipse.smarthome.core.thing.ThingRegistry;
import org.eclipse.smarthome.core.thing.ThingStatus;
import org.eclipse.smarthome.core.thing.ThingStatusDetail;
import org.eclipse.smarthome.core.thing.ThingStatusInfo;
import org.eclipse.smarthome.core.thing.binding.BaseThingHandler;
import org.eclipse.smarthome.core.thing.binding.builder.ChannelBuilder;
import org.eclipse.smarthome.core.thing.type.ChannelDefinition;
import org.eclipse.smarthome.core.thing.type.ChannelType;
import org.eclipse.smarthome.core.thing.type.ThingType;
import org.eclipse.smarthome.core.types.Command;
import org.eclipse.smarthome.core.types.RefreshType;
import org.eclipse.smarthome.core.types.State;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.function.BiFunction;
import java.util.stream.Collectors;

import com.tinkerforge.BrickletOutdoorWeather;
import com.tinkerforge.BrickletOutdoorWeatherStation;
import com.tinkerforge.Device;
import com.tinkerforge.IPConnection;
import com.tinkerforge.TinkerforgeException;
import com.tinkerforge.Device.SetterRefresh;
import com.tinkerforge.IPConnection.EnumerateListener;

/**
 * The {@link BrickletOutdoorWeatherStationHandler} is responsible for handling
 * commands, which are sent to one of the channels.
 *
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
public class BrickletOutdoorWeatherStationHandler extends BaseThingHandler {
    private final Logger logger = LoggerFactory.getLogger(BrickletOutdoorWeatherStationHandler.class);

    private boolean wasInitialized = false;

    private @Nullable BrickletOutdoorWeatherStation device;

    public BrickletOutdoorWeatherStationHandler(Thing thing) {
        super(thing);
    }

    @Override
    public void initialize() {
        String id = thing.getUID().getId();
        Bridge bridge = getBridge();
        if (bridge == null) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.CONFIGURATION_ERROR, "Bridge not found.");
            return;
        }
        BrickletOutdoorWeatherHandler outdoorWeatherHandler = ((BrickletOutdoorWeatherHandler) bridge.getHandler());
        device = new BrickletOutdoorWeatherStation(Integer.valueOf(id), outdoorWeatherHandler.getDevice());
        configureChannels();

        if (this.getBridge().getStatus() == ThingStatus.ONLINE) {
            initializeDevice();
        } else {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.BRIDGE_OFFLINE);
        }
    }

    private Configuration getChannelConfiguration(String channelID) {
        return getThing().getChannel(channelID).getConfiguration();
    }

    private void initializeDevice() {
        String id = thing.getUID().getId();
        Bridge bridge = getBridge();
        if (bridge == null) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.BRIDGE_UNINITIALIZED);
            return;
        }
        BrickletOutdoorWeatherHandler outdoorWeatherHandler = ((BrickletOutdoorWeatherHandler) bridge.getHandler());
        device = new BrickletOutdoorWeatherStation(Integer.valueOf(id), outdoorWeatherHandler.getDevice());
        device.initialize(getConfig(), this::getChannelConfiguration, this::updateState, this::triggerChannel);

        updateStatus(ThingStatus.ONLINE, ThingStatusDetail.NONE);

        this.getThing().getChannels().forEach(c -> handleCommand(c.getUID(), RefreshType.REFRESH));
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

    private void refreshValue(String channelId, Configuration channelConfig) {
        try {
            device.refreshValue(channelId, getConfig(), channelConfig, this::updateState, this::triggerChannel);
            updateStatus(ThingStatus.ONLINE);
        } catch (TinkerforgeException e) {
            ((BrickletOutdoorWeatherHandler)getBridge()).handleTimeout();
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.COMMUNICATION_ERROR);
        }
    }

    @Override
    public void handleCommand(ChannelUID channelUID, Command command) {
        if (this.getBridge().getStatus() == ThingStatus.OFFLINE) {
            // updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.BRIDGE_OFFLINE);
            return;
        }

        try {
            if (command instanceof RefreshType) {
                refreshValue(channelUID.getId(), getThing().getChannel(channelUID).getConfiguration());
            } else {
                List<SetterRefresh> refreshs = device.handleCommand(getConfig(),
                        getThing().getChannel(channelUID).getConfiguration(), channelUID.getId(), command);
                refreshs.forEach(r -> scheduler.schedule(
                        () -> refreshValue(r.channel, getThing().getChannel(r.channel).getConfiguration()), r.delay,
                        TimeUnit.MILLISECONDS));
            }
        } catch (TinkerforgeException e) {
            ((BrickletOutdoorWeatherHandler)getBridge()).handleTimeout();
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.COMMUNICATION_ERROR);
        }
    }

    private Channel buildChannel(ThingType tt, ChannelDefinition def) {
        ChannelType ct = TinkerforgeChannelTypeProvider.getChannelTypeStatic(def.getChannelTypeUID(), null);

        ChannelBuilder builder = ChannelBuilder
                .create(new ChannelUID(getThing().getUID(), def.getId()), ct.getItemType())
                .withAutoUpdatePolicy(def.getAutoUpdatePolicy()).withProperties(def.getProperties())
                .withType(def.getChannelTypeUID());

        String desc = def.getDescription();
        if (desc != null) {
            builder.withDescription(desc);
        }
        String label = def.getLabel();
        if (label != null) {
            builder.withLabel(label);
        }

        return builder.build();
    }

    private void configureChannels() {
        List<String> enabledChannelNames = new ArrayList<>();
        try {
            enabledChannelNames = device.getEnabledChannels(getConfig());
        } catch (TinkerforgeException e) {
            ((BrickletOutdoorWeatherHandler)getBridge()).handleTimeout();
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.COMMUNICATION_ERROR);
        }

        ThingType tt = TinkerforgeThingTypeProvider.getThingTypeStatic(this.getThing().getThingTypeUID(), null);

        List<Channel> enabledChannels = new ArrayList<>();
        for (String s : enabledChannelNames) {
            ChannelUID cuid = new ChannelUID(getThing().getUID(), s);
            ChannelDefinition def = tt.getChannelDefinitions().stream().filter(d -> d.getId().equals(cuid.getId()))
                    .findFirst().get();
            Channel newChannel = buildChannel(tt, def);

            Channel existingChannel = this.thing.getChannel(newChannel.getUID());
            if (existingChannel != null)
                newChannel = ChannelBuilder.create(newChannel).withConfiguration(existingChannel.getConfiguration())
                        .build();

            enabledChannels.add(newChannel);
        }

        updateThing(editThing().withChannels(enabledChannels).build());
    }
}
