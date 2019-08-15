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
import org.eclipse.smarthome.config.core.Configuration;
import org.eclipse.smarthome.core.thing.Bridge;
import org.eclipse.smarthome.core.thing.Channel;
import org.eclipse.smarthome.core.thing.ChannelUID;
import org.eclipse.smarthome.core.thing.CommonTriggerEvents;
import org.eclipse.smarthome.core.thing.Thing;
import org.eclipse.smarthome.core.thing.ThingStatus;
import org.eclipse.smarthome.core.thing.ThingStatusDetail;
import org.eclipse.smarthome.core.thing.ThingStatusInfo;
import org.eclipse.smarthome.core.thing.binding.BaseThingHandler;
import org.eclipse.smarthome.core.types.Command;
import org.eclipse.smarthome.core.types.RefreshType;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.function.BiFunction;
import java.util.stream.Collectors;

import com.tinkerforge.Device;
import com.tinkerforge.IPConnection;
import com.tinkerforge.TinkerforgeException;
import com.tinkerforge.Device.SetterRefresh;
import com.tinkerforge.IPConnection.EnumerateListener;


/**
 * The {@link DeviceHandler} is responsible for handling commands,
 * which are sent to one of the channels.
 *
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
public class DeviceHandler extends BaseThingHandler {

    private final Logger logger = LoggerFactory.getLogger(DeviceHandler.class);

    private boolean wasInitialized = false;

    @Nullable
    private Device device;

    private final BiFunction<String, IPConnection, Device> deviceSupplier;

    private List<Channel> channels;

    public DeviceHandler(Thing thing, BiFunction<String, IPConnection, Device> deviceSupplier) {
        super(thing);
        channels = new ArrayList<Channel>(thing.getChannels());
        System.out.println("Constructing " + thing.getUID().getAsString());
        this.deviceSupplier = deviceSupplier;
    }

    private void enumerateListener(String uid, String connectedUid, char position, short[] hardwareVersion,
    short[] firmwareVersion, int deviceIdentifier, short enumerationType) {
        String id = thing.getUID().getId();

        if (uid.equals(id)) {
            return;
        }

        switch(enumerationType) {
            case IPConnection.ENUMERATION_TYPE_AVAILABLE:
                break;
            case IPConnection.ENUMERATION_TYPE_CONNECTED:
                initialize_device();
                break;
            case IPConnection.ENUMERATION_TYPE_DISCONNECTED:
                updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.NONE, "Device was unplugged.");
                break;
        }
    }

    @Override
    public void initialize() {
        if (getBridge() == null) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.CONFIGURATION_ERROR, "Bridge not found.");
            return;
        }
        BrickDaemonHandler brickd = ((BrickDaemonHandler) getBridge().getHandler());
        if (!wasInitialized)
        {
            brickd.addEnumerateListener(this::enumerateListener);
        }

        com.tinkerforge.IPConnection ipcon = brickd.ipcon;

        String id = thing.getUID().getId();
        device = deviceSupplier.apply(id, ipcon);

        if (!wasInitialized) {
            configureChannels();
        }
        wasInitialized = true;

        if(this.getBridge().getStatus() == ThingStatus.ONLINE) {
            initialize_device();
        } else {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.BRIDGE_OFFLINE);
        }
    }

    private Configuration getChannelConfiguration(String channelID) {
        return getThing().getChannel(channelID).getConfiguration();
    }

    private void initialize_device() {
        String id = thing.getUID().getId();
        Bridge bridge = getBridge();
        if (bridge == null)
        {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.BRIDGE_UNINITIALIZED);
            return;
        }
        BrickDaemonHandler brickd = ((BrickDaemonHandler) bridge.getHandler());
        com.tinkerforge.IPConnection ipcon = brickd.ipcon;
        device = deviceSupplier.apply(id, ipcon);

        try {
            device.initialize(getConfig(), this::getChannelConfiguration, this::updateState, this::triggerChannel);
        }
        catch (TinkerforgeException e) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.COMMUNICATION_ERROR);
            return;
        }
        updateStatus(ThingStatus.ONLINE, ThingStatusDetail.NONE);

        this.getThing().getChannels().forEach(c -> handleCommand(c.getUID(), RefreshType.REFRESH));
    }

    @Override
    public void bridgeStatusChanged(ThingStatusInfo bridgeStatusInfo) {
        if (bridgeStatusInfo.getStatus() == ThingStatus.ONLINE) {
            initialize_device();
        } else if (bridgeStatusInfo.getStatus() == ThingStatus.OFFLINE) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.BRIDGE_OFFLINE);
        }
    }

    private void refreshValue(String channelId, Configuration channelConfig) {
        try {
            System.out.println("Refreshing " + channelId);
            device.refreshValue(channelId, getConfig(), channelConfig, this::updateState, this::triggerChannel);
        } catch (TinkerforgeException e) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.COMMUNICATION_ERROR);
        }
    }

    @Override
    public void handleCommand(ChannelUID channelUID, Command command) {
        if (this.getBridge().getStatus() == ThingStatus.OFFLINE) {
            //updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.BRIDGE_OFFLINE);
            return;
        }

        try {
            if (command instanceof RefreshType) {
                refreshValue(channelUID.getId(), getThing().getChannel(channelUID).getConfiguration());
            }
            else {
                List<SetterRefresh> refreshs = device.handleCommand(getConfig(), getThing().getChannel(channelUID).getConfiguration(), channelUID.getId(), command);
                refreshs.forEach(r -> scheduler.schedule(() -> refreshValue(r.channel, getThing().getChannel(r.channel).getConfiguration()), r.delay, TimeUnit.MILLISECONDS));
            }
        } catch (TinkerforgeException e) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.COMMUNICATION_ERROR);
        }
    }

    @Override
    public void handleRemoval() {
        try {
            if (device != null) {
                device.dispose(getConfig());
            }
            updateStatus(ThingStatus.REMOVED);
        } catch (TinkerforgeException e) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.COMMUNICATION_ERROR);
        }
    }

    private void configureChannels() {
        List<String> enabledChannelNames = device.getEnabledChannels(getConfig());

        List<Channel> enabledChannels = enabledChannelNames.stream()
                                                           .map(s -> new ChannelUID(getThing().getUID(), s))
                                                           .map(cuid -> channels.stream().filter(c -> c.getUID().equals(cuid)).findFirst().get())
                                                           .collect(Collectors.toList());
        updateThing(editThing().withChannels(enabledChannels).build());
    }

    @Override
    public void handleConfigurationUpdate(Map<String, Object> configurationParameters) {
        super.handleConfigurationUpdate(configurationParameters);
        configureChannels();
    }
}
