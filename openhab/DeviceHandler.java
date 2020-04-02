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
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.TimeUnit;
import java.util.function.BiFunction;
import java.util.function.Supplier;

import org.eclipse.jdt.annotation.NonNull;
import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.jdt.annotation.Nullable;
import org.eclipse.jetty.client.HttpClient;
import org.openhab.binding.tinkerforge.internal.TinkerforgeBindingConstants;
import org.openhab.binding.tinkerforge.internal.TinkerforgeThingTypeProvider;
import org.openhab.binding.tinkerforge.internal.Utils;
import org.openhab.binding.tinkerforge.internal.device.CoMCUFlashable;
import org.openhab.binding.tinkerforge.internal.device.DeviceWrapper;
import org.openhab.binding.tinkerforge.internal.device.SetterRefresh;
import org.openhab.binding.tinkerforge.internal.device.DeviceWrapperFactory;
import org.openhab.binding.tinkerforge.internal.device.Helper;
import org.openhab.binding.tinkerforge.internal.device.StandardFlashHost;
import org.openhab.binding.tinkerforge.internal.device.StandardFlashable;
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
import org.eclipse.smarthome.core.thing.binding.ThingHandler;
import org.eclipse.smarthome.core.thing.binding.ThingHandlerService;
import org.eclipse.smarthome.core.thing.binding.builder.ChannelBuilder;
import org.eclipse.smarthome.core.thing.binding.firmware.Firmware;
import org.eclipse.smarthome.core.thing.binding.firmware.FirmwareUpdateHandler;
import org.eclipse.smarthome.core.thing.binding.firmware.ProgressCallback;
import org.eclipse.smarthome.core.thing.type.ChannelDefinition;
import org.eclipse.smarthome.core.thing.type.ChannelTypeRegistry;
import org.eclipse.smarthome.core.thing.type.ThingType;
import org.eclipse.smarthome.core.types.Command;
import org.eclipse.smarthome.core.types.RefreshType;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.tinkerforge.BrickMaster;
import com.tinkerforge.Device.Identity;
import com.tinkerforge.IPConnection;
import com.tinkerforge.IPConnection.EnumerateListener;
import com.tinkerforge.TimeoutException;
import com.tinkerforge.TinkerforgeException;

/**
 * Handles communication with a brick or bricklet.
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
public class DeviceHandler extends BaseThingHandler implements FirmwareUpdateHandler {
    protected final Logger logger = LoggerFactory.getLogger(DeviceHandler.class);

    private boolean wasInitialized = false;

    private @Nullable DeviceWrapper device;

    private final BiFunction<String, IPConnection, DeviceWrapper> deviceSupplier;

    private Class<? extends ThingHandlerService> actionsClass;
    private Supplier<ChannelTypeRegistry> channelTypeRegistrySupplier;
    private Supplier<ConfigDescriptionRegistry> configDescriptionRegistrySupplier;
    private EnumerateListener enumerateListener;
    private @Nullable HttpClient httpClient;

    public DeviceHandler(Thing thing, BiFunction<String, IPConnection, DeviceWrapper> deviceSupplier,
            Class<? extends ThingHandlerService> actionsClass,
            Supplier<ChannelTypeRegistry> channelTypeRegistrySupplier,
            Supplier<ConfigDescriptionRegistry> configDescriptionRegistrySupplier, @Nullable HttpClient httpClient) {
        super(thing);

        this.deviceSupplier = deviceSupplier;
        this.actionsClass = actionsClass;
        this.channelTypeRegistrySupplier = channelTypeRegistrySupplier;
        this.configDescriptionRegistrySupplier = configDescriptionRegistrySupplier;
        this.httpClient = httpClient;
        this.enumerateListener = this::enumerateListenerFn;
    }

    public @Nullable DeviceWrapper getDevice() {
        return device;
    }

    public boolean checkReachablity() {
        try {
            logger.debug("Checking reachability of {}", thing.getUID().getId());
            @Nullable DeviceWrapper dev = device;
            if (dev == null) {
                return false;
            }

            Identity id = dev.getIdentity();
            boolean isInBootloader = dev instanceof CoMCUFlashable
                    && ((CoMCUFlashable) dev).getBootloaderMode() != CoMCUFlashable.BOOTLOADER_MODE_FIRMWARE;
            if (!isInBootloader) {
                logger.debug("{} is not in bootloader mode.", thing.getUID().getId());
                String fwVersion = id.firmwareVersion[0] + "." + id.firmwareVersion[1] + "." + id.firmwareVersion[2];
                this.getThing().setProperty(Thing.PROPERTY_FIRMWARE_VERSION, fwVersion);
            } else {
                logger.debug("{} is in bootloader mode.", thing.getUID().getId());
            }
            logger.debug("Done checking reachability of {}", thing.getUID().getId());

            // Initialize will set the status itself if the configuration succeeds.
            if (!thing.getStatus().equals(ThingStatus.ONLINE)) {
                logger.debug("{} was not already online. Reinitializing", thing.getUID().getId());
                initializeDevice();
            } else {
                logger.debug("{} was already online. Will not reinitialize.", thing.getUID().getId());
            }
            return true;
        } catch (TinkerforgeException e) {
            logger.debug("Failed checking reachability of {}: {}", thing.getUID().getId(), e.getMessage());
            return false;
        }
    }

    public void reachabilityCheckFailed() {
        updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.COMMUNICATION_ERROR, "Device is unreachable.");
    }

    private void enumerateListenerFn(String uid, String connectedUid, char position, short[] hardwareVersion,
            short[] firmwareVersion, int deviceIdentifier, short enumerationType) {
        String id = thing.getUID().getId();
        if (!uid.equals(id)) {
            return;
        }

        String hwVersion = firmwareVersion[0] + "." + firmwareVersion[1] + "." + firmwareVersion[2];
        String fwVersion = firmwareVersion[0] + "." + firmwareVersion[1] + "." + firmwareVersion[2];
        logger.debug("Enumeration {}, {}, {}, {}, {}, {}, {}", uid, connectedUid, position, hwVersion, fwVersion,
                device, enumerationType);

        if (enumerationType == IPConnection.ENUMERATION_TYPE_DISCONNECTED) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.NONE, "Device was unplugged.");
            return;
        }
        this.getThing().setProperty(Thing.PROPERTY_FIRMWARE_VERSION, fwVersion);

        if (enumerationType == IPConnection.ENUMERATION_TYPE_CONNECTED) {
            initializeDevice();
        }
    }

    @Override
    public void initialize() {
        logger.debug("Initializing handler for {}", thing.getUID().getId());
        @Nullable Bridge bridge = getBridge();
        if (bridge == null) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.CONFIGURATION_ERROR, "Bridge not found.");
            return;
        }

        BrickDaemonHandler brickd = (BrickDaemonHandler) (bridge.getHandler());
        if (brickd == null) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.CONFIGURATION_ERROR, "Bridge handler not found.");
            return;
        }
        if (!wasInitialized) {
            logger.debug("Adding enumerate listener for {}", thing.getUID().getId());
            brickd.addEnumerateListener(enumerateListener);
        }
        wasInitialized = true;

        com.tinkerforge.IPConnection ipcon = brickd.ipcon;

        String id = thing.getUID().getId();
        if (device != null) {
            logger.debug("Removing old manual update handler for {}", thing.getUID().getId());
            Utils.assertNonNull(device).cancelManualUpdates();
        }
        device = deviceSupplier.apply(id, ipcon);

        boolean success = configureChannels();
        if (!success) {
            logger.debug("Failed to configure channels for {}", thing.getUID().getId());
            return;
        }

        if (bridge.getStatus() == ThingStatus.ONLINE) {
            initializeDevice();
        } else {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.BRIDGE_OFFLINE);
        }
    }

    private Configuration getChannelConfiguration(String channelID) {
        @Nullable Channel c = getThing().getChannel(channelID);
        if (c == null) {
            throw new IllegalArgumentException(String.format("Channel %s not found", channelID));
        }
        return c.getConfiguration();
    }


    protected void initializeDevice() {
        String id = thing.getUID().getId();
        logger.debug("Initializing {}", id);
        Bridge bridge = getBridge();
        if (bridge == null) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.BRIDGE_UNINITIALIZED, "Bridge not found.");
            return;
        }
        BrickDaemonHandler brickd = (BrickDaemonHandler) (bridge.getHandler());
        if (brickd == null) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.BRIDGE_UNINITIALIZED, "Bridge handler not found.");
            return;
        }
        com.tinkerforge.IPConnection ipcon = brickd.ipcon;
        if (device != null) {
            logger.debug("Removing old manual update handler for {}", thing.getUID().getId());
            Utils.assertNonNull(device).cancelManualUpdates();
        }
        DeviceWrapper dev = deviceSupplier.apply(id, ipcon);
        this.device = dev;

        try {
            if (dev instanceof CoMCUFlashable
                    && ((CoMCUFlashable) dev).getBootloaderMode() != CoMCUFlashable.BOOTLOADER_MODE_FIRMWARE) {
                updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.NONE,
                        "Device is in bootloader mode. Please flash a suitable firmware.");
                this.getThing().setProperty(Thing.PROPERTY_FIRMWARE_VERSION, "0.0.0");
                return;
            }

            short[] fw = dev.getIdentity().firmwareVersion;
            String minFWString = getThing().getProperties().getOrDefault(
                    TinkerforgeBindingConstants.PROPERTY_MINIMUM_FIRMWARE_VERSION, "2.0.0");
            String[] splt = minFWString.split("\\.");
            short[] minFW = { Short.parseShort(splt[0]), Short.parseShort(splt[1]), Short.parseShort(splt[2]) };
            if (Helper.compareFWs(fw, minFW) < 0) {
                updateStatus(
                        ThingStatus.OFFLINE,
                        ThingStatusDetail.NONE,
                        String.format(
                                "Device firmware %d.%d.%d is older than the minimum required version %s. Please update the firmware.",
                                fw[0], fw[1], fw[2], minFWString));
                return;
            }

            dev.initialize(getConfig(), this::getChannelConfiguration, this::updateState, this::triggerChannel,
                    scheduler, this);
            logger.debug("Initialized {}", thing.getUID().getId());
        } catch (TimeoutException e) {
            logger.debug("Failed to initialize {}: {}", thing.getUID().getId(), e.getMessage());
            reportTimeout();
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.HANDLER_INITIALIZING_ERROR, e.getMessage());
            return;
        } catch (TinkerforgeException e) {
            logger.warn("Failed to initialize {}: {}", thing.getUID().getId(), e.getMessage());
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.HANDLER_INITIALIZING_ERROR, e.getMessage());
            return;
        }
        updateStatus(ThingStatus.ONLINE, ThingStatusDetail.NONE);
        logger.debug("Refreshing channels of {}", thing.getUID().getId());
        this.getThing().getChannels().stream().filter(c -> !Utils.assertNonNull(c.getChannelTypeUID()).toString().startsWith("system"))
                .forEach(c -> handleCommand(c.getUID(), RefreshType.REFRESH));
    }

    @Override
    public Configuration getConfig() {
        return super.getConfig();
    }

    @Override
    public void bridgeStatusChanged(ThingStatusInfo bridgeStatusInfo) {
        if (bridgeStatusInfo.getStatus() == ThingStatus.ONLINE) {
            logger.debug("Bridge of {} went online", thing.getUID().getId());
            initializeDevice();
        } else if (bridgeStatusInfo.getStatus() == ThingStatus.OFFLINE) {
            logger.debug("Bridge of {} went offline", thing.getUID().getId());
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.BRIDGE_OFFLINE);
        }
    }

    private void refreshValue(String channelId, Configuration channelConfig) {
        try {
            @Nullable DeviceWrapper dev = device;
            if (dev == null) {
                return;
            }
            dev.refreshValue(channelId, getConfig(), channelConfig, this::updateState, this::triggerChannel);
        } catch (TimeoutException e) {
            logger.debug("Failed to refresh value for {}: {}", channelId, e.getMessage());
            reportTimeout();
        } catch (TinkerforgeException e) {
            logger.warn("Failed to refresh value for {}: {}", channelId, e.getMessage());
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
        try {
            if (command instanceof RefreshType) {
                refreshValue(channelUID.getId(), channel.getConfiguration());
            } else {
                @Nullable DeviceWrapper dev = device;
                if (dev == null) {
                    return;
                }
                List<SetterRefresh> refreshs = dev.handleCommand(getConfig(), channel.getConfiguration(), channelUID.getId(), command);
                refreshs.forEach(r -> scheduler.schedule(
                        () -> refreshValue(r.channel, Utils.assertNonNull(getThing().getChannel(r.channel)).getConfiguration()), r.delay,
                        TimeUnit.MILLISECONDS));
            }
        } catch (TimeoutException e) {
            logger.debug("Failed to send command {} to channel {}: {}", command.toFullString(), channelUID.toString(), e.getMessage());
            reportTimeout();
        } catch (TinkerforgeException e) {
            logger.warn("Failed to send command {} to channel {}: {}", command.toFullString(), channelUID.toString(), e.getMessage());
        }
    }

    @Override
    public void handleRemoval() {
        logger.debug("Removing {}", thing.getUID().getId());
        try {
            @Nullable DeviceWrapper dev = device;
            if (dev != null) {
                dev.cancelManualUpdates();
                @Nullable Bridge bridge = getBridge();
                if (bridge != null) {
                    BrickDaemonHandler brickd = (BrickDaemonHandler) (bridge.getHandler());
                    if (brickd != null)
                        brickd.removeEnumerateListener(enumerateListener);
                }

                dev.dispose(getConfig());
            }
            logger.debug("Removed {}", thing.getUID().getId());

        } catch (TinkerforgeException e) {
        }
        updateStatus(ThingStatus.REMOVED);
    }


    private void reportTimeout() {
        @Nullable Bridge bridge = getBridge();
        if (bridge == null) {
            return;
        }

        @Nullable BrickDaemonHandler brickd = (BrickDaemonHandler) (bridge.getHandler());
        if (brickd == null) {
            return;
        }

        brickd.handleTimeout(this);
    }

    private boolean configureChannels() {
        List<String> enabledChannelNames = new ArrayList<>();
        try {
            enabledChannelNames = Utils.assertNonNull(device).getEnabledChannels(getConfig());
        } catch (TimeoutException e) {
            logger.debug("Failed to get enabled channels for device {}: {}", this.getThing().getUID().toString(), e.getMessage());
            reportTimeout();
            return false;
        } catch (TinkerforgeException e) {
            logger.warn("Failed to get enabled channels for device {}: {}", this.getThing().getUID().toString(), e.getMessage());
            return false;
        }

        ThingType tt = TinkerforgeThingTypeProvider.getThingTypeStatic(this.getThing().getThingTypeUID(), null);
        if(tt == null) {
            logger.warn("Failed to get thing type for device {}", this.getThing().getUID().toString());
            return false;
        }

        List<Channel> enabledChannels = new ArrayList<>();
        for (String s : enabledChannelNames) {
            ChannelUID cuid = new ChannelUID(getThing().getUID(), s);
            ChannelDefinition def = tt.getChannelDefinitions().stream().filter(d -> d.getId().equals(cuid.getId()))
                    .findFirst().get();
            Channel newChannel = Utils.buildChannel(tt, getThing().getUID(), def, channelTypeRegistrySupplier.get(), configDescriptionRegistrySupplier.get(), logger);

            Channel existingChannel = Utils.assertNonNull(this.thing.getChannel(newChannel.getUID()));

            newChannel = ChannelBuilder.create(newChannel).withConfiguration(existingChannel.getConfiguration()).build();

            enabledChannels.add(newChannel);
        }

        updateThing(editThing().withChannels(enabledChannels).build());
        return true;
    }

    @Override
    public Collection<Class<? extends ThingHandlerService>> getServices() {
        return Collections.singletonList(actionsClass);
    }

    @Override
    public void updateFirmware(Firmware firmware, ProgressCallback progressCallback) {
        @Nullable Bridge bridge = getBridge();
        if (bridge == null) {
            progressCallback.failed("Bridge not found.");
            return;
        }

        @Nullable BrickDaemonHandler brickd = (BrickDaemonHandler) (bridge.getHandler());
        if (brickd == null) {
            progressCallback.failed("Bridge handler not found.");
            return;
        }

        @Nullable DeviceWrapper dev = this.device;
        if (dev == null) {
            progressCallback.failed("Device not found.");
            return;
        }

        if (dev instanceof CoMCUFlashable) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.FIRMWARE_UPDATING, "Firmware is updating");

            CoMCUFlashable flashable = (CoMCUFlashable) dev;
            flashable.flash(firmware, progressCallback, Utils.assertNonNull(this.httpClient));

            updateStatus(ThingStatus.ONLINE);
            return;
        }

        if (dev instanceof StandardFlashable) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.FIRMWARE_UPDATING, "Firmware is updating");

            Identity id;
            try {
                id = dev.getIdentity();
            } catch (TinkerforgeException e) {
                progressCallback.failed("Failed to get device identity: {}", e.getMessage());
                reportTimeout();
                return;
            }
            String hostUID = id.connectedUid;

            ThingHandler hostHandler = brickd.getChildHandler(hostUID);

            DeviceWrapper hostDevice;
            if (hostHandler != null)
                hostDevice = ((DeviceHandler) hostHandler).getDevice();
            else {
                IPConnection ipcon = brickd.ipcon;
                Identity hostId;
                try {
                    hostId = new BrickMaster(hostUID, ipcon).getIdentity();
                } catch (TinkerforgeException e) {
                    progressCallback.failed("Failed to get host identity: {}", e.getMessage());
                    reportTimeout();
                    return;
                }
                try {
                    hostDevice = DeviceWrapperFactory.createDevice(hostId.deviceIdentifier, hostUID, ipcon);
                } catch (Exception e) {
                    progressCallback.failed("Failed to create host device wrapper: {}", e.getMessage());
                    return;
                }
            }

            if (!(hostDevice instanceof StandardFlashHost)) {
                progressCallback.failed("Device is connected to host that does not implement StandardFlashHost");
                return;
            }

            ((StandardFlashHost) hostDevice).flash(id.position, firmware, progressCallback, Utils.assertNonNull(this.httpClient));
        }
    }

    @Override
    public void cancel() {
        // not needed for now
    }

    @Override
    public boolean isUpdateExecutable() {
        @Nullable Bridge bridge = getBridge();
        boolean bridgeReachable = bridge != null && bridge.getStatus() == ThingStatus.ONLINE;
        boolean updateSchemeSupported = this.device instanceof CoMCUFlashable
                || this.device instanceof StandardFlashable;
        boolean thingReachable = getThing().getStatusInfo().getStatusDetail() != ThingStatusDetail.COMMUNICATION_ERROR;

        return this.httpClient != null && bridgeReachable && thingReachable && updateSchemeSupported;
    }
}
