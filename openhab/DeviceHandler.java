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
import org.eclipse.smarthome.core.thing.binding.ThingHandlerService;
import org.eclipse.smarthome.core.thing.binding.builder.ChannelBuilder;
import org.eclipse.smarthome.core.thing.type.ChannelDefinition;
import org.eclipse.smarthome.core.thing.type.ChannelType;
import org.eclipse.smarthome.core.thing.type.ChannelTypeRegistry;
import org.eclipse.smarthome.core.thing.type.ThingType;
import org.eclipse.smarthome.core.types.Command;
import org.eclipse.smarthome.core.types.RefreshType;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.function.BiFunction;
import java.util.function.Supplier;
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

    private Class<? extends ThingHandlerService> actionsClass;

    private Supplier<ChannelTypeRegistry> channelTypeRegistrySupplier;

    public DeviceHandler(Thing thing, BiFunction<String, IPConnection, Device> deviceSupplier,
            Class<? extends ThingHandlerService> actionsClass,
            Supplier<ChannelTypeRegistry> channelTypeRegistrySupplier) {
        super(thing);

        this.deviceSupplier = deviceSupplier;
        this.actionsClass = actionsClass;
        this.channelTypeRegistrySupplier = channelTypeRegistrySupplier;
    }

	public @Nullable Device getDevice() {
		return device;
    }


    public boolean checkReachablity() {
        try {
            logger.debug("Checking reachability of {}", thing.getUID().getId());
            getDevice().getIdentity();
            logger.debug("Done checking reachability of {}", thing.getUID().getId());

            // Initialize will set the status itself if the configuration succeeds.
            if(!thing.getStatus().equals(ThingStatus.INITIALIZING))
                updateStatus(ThingStatus.ONLINE, ThingStatusDetail.NONE);
            return true;
        } catch(TinkerforgeException e) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.COMMUNICATION_ERROR, "Device is unreachable.");
            logger.debug("Failed checking reachability of {}: {}", thing.getUID().getId(), e.getMessage());
            return false;
        }
    }

    private void enumerateListener(String uid, String connectedUid, char position, short[] hardwareVersion,
    short[] firmwareVersion, int deviceIdentifier, short enumerationType) {
        String id = thing.getUID().getId();

        if (!uid.equals(id)) {
            return;
        }

        switch(enumerationType) {
            case IPConnection.ENUMERATION_TYPE_AVAILABLE:
                break;
            case IPConnection.ENUMERATION_TYPE_CONNECTED:
                initializeDevice();
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

        BrickDaemonHandler brickd = (BrickDaemonHandler) (getBridge().getHandler());
        if (!wasInitialized)
        {
            brickd.addEnumerateListener(this::enumerateListener);
        }
        wasInitialized = true;

        com.tinkerforge.IPConnection ipcon = brickd.ipcon;

        String id = thing.getUID().getId();
        device = deviceSupplier.apply(id, ipcon);

        configureChannels();

        if(this.getBridge().getStatus() == ThingStatus.ONLINE) {
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
        if (bridge == null)
        {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.BRIDGE_UNINITIALIZED);
            return;
        }
        BrickDaemonHandler brickd = (BrickDaemonHandler) (bridge.getHandler());
        com.tinkerforge.IPConnection ipcon = brickd.ipcon;
        device = deviceSupplier.apply(id, ipcon);

        if(!checkReachablity()) {
            return;
        }

        try {
            device.initialize(getConfig(), this::getChannelConfiguration, this::updateState, this::triggerChannel);
        }
        catch (TinkerforgeException e) {
            brickd.handleTimeout(this);
            return;
        }
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

    private void refreshValue(String channelId, Configuration channelConfig) {
        try {
            device.refreshValue(channelId, getConfig(), channelConfig, this::updateState, this::triggerChannel);
        } catch (TinkerforgeException e) {
            ((BrickDaemonHandler)(getBridge().getHandler())).handleTimeout(this);
        }
    }

    @Override
    public void handleCommand(ChannelUID channelUID, Command command) {
        if (this.getBridge().getStatus() == ThingStatus.OFFLINE) {
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
            ((BrickDaemonHandler)(getBridge().getHandler())).handleTimeout(this);
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

    private Channel buildChannel(ThingType tt, ChannelDefinition def){
        ChannelType ct = TinkerforgeChannelTypeProvider.getChannelTypeStatic(def.getChannelTypeUID(), null);
        if(ct == null) {
            ChannelTypeRegistry reg = channelTypeRegistrySupplier.get();
            if(reg == null) {
                logger.warn("Could not get build channel {}: ChannelTypeRegistry not found.", def.getId());
                return null;
            }
            ct = reg.getChannelType(def.getChannelTypeUID());
        }
        ChannelBuilder builder = ChannelBuilder.create(new ChannelUID(getThing().getUID(), def.getId()), ct.getItemType())
                                               .withAutoUpdatePolicy(def.getAutoUpdatePolicy())
                                               .withProperties(def.getProperties())
                                               .withType(def.getChannelTypeUID())
                                               .withKind(ct.getKind());

        String desc = def.getDescription();
        if(desc != null) {
            builder.withDescription(desc);
        }
        String label = def.getLabel();
        if(label != null) {
            builder.withLabel(label);
        }

        return builder.build();
    }

    private void configureChannels() {
        List<String> enabledChannelNames = new ArrayList<>();
        try {
            enabledChannelNames = device.getEnabledChannels(getConfig());
        }
        catch(TinkerforgeException e) {
            ((BrickDaemonHandler)(getBridge().getHandler())).handleTimeout(this);
        }

        ThingType tt = TinkerforgeThingTypeProvider.getThingTypeStatic(this.getThing().getThingTypeUID(), null);

        List<Channel> enabledChannels = new ArrayList<>();
        for(String s : enabledChannelNames) {
            ChannelUID cuid = new ChannelUID(getThing().getUID(), s);
            ChannelDefinition def = tt.getChannelDefinitions().stream().filter(d -> d.getId().equals(cuid.getId())).findFirst().get();
            Channel newChannel = buildChannel(tt, def);

            Channel existingChannel = this.thing.getChannel(newChannel.getUID());
            if(existingChannel != null)
                newChannel = ChannelBuilder.create(newChannel).withConfiguration(existingChannel.getConfiguration()).build();

            enabledChannels.add(newChannel);
        }

        updateThing(editThing().withChannels(enabledChannels).build());
    }

    @Override
    public Collection<Class<? extends ThingHandlerService>> getServices() {
        return Collections.singletonList(actionsClass);
    }
}
