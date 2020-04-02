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
package org.openhab.binding.tinkerforge.internal.handler;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;
import java.util.function.Function;
import java.util.function.Supplier;

import org.eclipse.jdt.annotation.NonNull;
import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.jdt.annotation.Nullable;
import org.openhab.binding.tinkerforge.internal.TinkerforgeThingTypeProvider;
import org.openhab.binding.tinkerforge.internal.Utils;
import org.openhab.binding.tinkerforge.internal.device.DeviceWrapper;
import org.openhab.binding.tinkerforge.internal.device.SetterRefresh;
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
 * Custom handler controlling any supported remote socket or dimmer.
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
public class RemoteSwitchDeviceHandler extends BaseThingHandler {
    private final Logger logger = LoggerFactory.getLogger(RemoteSwitchDeviceHandler.class);

    private @Nullable DeviceWrapper device;
    private Function<BrickletRemoteSwitchHandler,DeviceWrapper> deviceSupplier;
    private Supplier<ChannelTypeRegistry> channelTypeRegistrySupplier;
    private Supplier<ConfigDescriptionRegistry> configDescriptionRegistrySupplier;

    public RemoteSwitchDeviceHandler(Thing thing, Function<BrickletRemoteSwitchHandler, DeviceWrapper> deviceSupplier,
            Supplier<ChannelTypeRegistry> channelTypeRegistrySupplier,
            Supplier<ConfigDescriptionRegistry> configDescriptionRegistrySupplier) {
        super(thing);
        this.deviceSupplier = deviceSupplier;
        this.channelTypeRegistrySupplier = channelTypeRegistrySupplier;
        this.configDescriptionRegistrySupplier = configDescriptionRegistrySupplier;
    }

    @Override
    public void initialize() {
        Bridge bridge = getBridge();
        if (bridge == null) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.BRIDGE_UNINITIALIZED, "Bridge not found.");
            return;
        }

        BrickletRemoteSwitchHandler handler = ((BrickletRemoteSwitchHandler) bridge.getHandler());
        if (handler == null) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.BRIDGE_UNINITIALIZED, "Bridge handler not found.");
            return;
        }

        device = deviceSupplier.apply(handler);
        configureChannels();

        if (bridge.getStatus() == ThingStatus.ONLINE) {
            initializeDevice();
        } else {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.BRIDGE_OFFLINE);
        }
    }

    private void initializeDevice() {
        Bridge bridge = getBridge();
        if (bridge == null) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.BRIDGE_UNINITIALIZED);
            return;
        }
        BrickletRemoteSwitchHandler handler = ((BrickletRemoteSwitchHandler) bridge.getHandler());
        if (handler == null) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.BRIDGE_UNINITIALIZED, "Bridge handler not found.");
            return;
        }

        device = deviceSupplier.apply(handler);

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

        @Nullable BrickletRemoteSwitchHandler handler = (BrickletRemoteSwitchHandler) (bridge.getHandler());
        if (handler == null) {
            return;
        }

        handler.handleTimeout();
    }

    private void refreshValue(String channelId, Configuration channelConfig) {
        try {
            @Nullable DeviceWrapper dev = device;
            if (dev == null) {
                return;
            }
            dev.refreshValue(channelId, getConfig(), channelConfig, this::updateState, this::triggerChannel);
            updateStatus(ThingStatus.ONLINE);
        } catch (TimeoutException e) {
            logger.debug("Failed to refresh value for {}: {}", channelId, e.getMessage());
            reportTimeout();
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.COMMUNICATION_ERROR);
        } catch (TinkerforgeException e) {
            logger.warn("Failed to refresh value for {}: {}", channelId, e.getMessage());
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.COMMUNICATION_ERROR);
        }
    }

    @Override
    public void handleCommand(ChannelUID channelUID, Command command) {
        @Nullable Channel channel = getThing().getChannel(channelUID);
        if (channel == null) {
            logger.info("Received command {} for unknown channel {}.", command.toFullString(),
                        channelUID.toString());
            return;
        }

        @Nullable Bridge bridge = getBridge();
        if (bridge == null) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.CONFIGURATION_ERROR, "Bridge not found.");
            return;
        }

        if (bridge.getStatus() == ThingStatus.OFFLINE) {
            // updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.BRIDGE_OFFLINE);
            return;
        }

        try {
            if (command instanceof RefreshType) {
                refreshValue(channelUID.getId(), channel.getConfiguration());
            } else {
                @Nullable DeviceWrapper dev = device;
                if (dev == null) {
                    return;
                }
                List<SetterRefresh> refreshs = dev.handleCommand(getConfig(), channel
                        .getConfiguration(), channelUID.getId(), command);
                refreshs.forEach(r -> scheduler.schedule(
                        () -> refreshValue(r.channel, Utils.assertNonNull(getThing().getChannel(r.channel)).getConfiguration()), r.delay,
                        TimeUnit.MILLISECONDS));
            }
        } catch (TimeoutException e) {
            logger.debug("Failed to send command {} to channel {}: {}", command.toFullString(), channelUID.toString(), e.getMessage());
            reportTimeout();
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.COMMUNICATION_ERROR);
        } catch (TinkerforgeException e) {
            logger.warn("Failed to send command {} to channel {}: {}", command.toFullString(), channelUID.toString(), e.getMessage());
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.COMMUNICATION_ERROR);
        }
    }

    private void configureChannels() {
        List<String> enabledChannelNames = new ArrayList<>();
        try {
            enabledChannelNames = Utils.assertNonNull(device).getEnabledChannels(getConfig());
        } catch (TimeoutException e) {
            logger.debug("Failed to get enabled channels for device {}: {}", this.getThing().getUID().toString(), e.getMessage());
            reportTimeout();
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.COMMUNICATION_ERROR);
        } catch (TinkerforgeException e) {
            logger.warn("Failed to get enabled channels for device {}: {}", this.getThing().getUID().toString(), e.getMessage());
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
