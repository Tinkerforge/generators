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
package org.eclipse.smarthome.binding.tinkerforge.discovery;

import java.util.Date;
import java.util.HashSet;
import java.util.Optional;
import java.util.Set;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;

import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.jdt.annotation.Nullable;
import org.eclipse.smarthome.binding.tinkerforge.internal.TinkerforgeBindingConstants;
import org.eclipse.smarthome.binding.tinkerforge.internal.device.DeviceWrapperFactory;
import org.eclipse.smarthome.binding.tinkerforge.internal.handler.BrickDaemonHandler;
import org.eclipse.smarthome.config.discovery.AbstractDiscoveryService;
import org.eclipse.smarthome.config.discovery.DiscoveryResult;
import org.eclipse.smarthome.config.discovery.DiscoveryResultBuilder;
import org.eclipse.smarthome.core.thing.Thing;
import org.eclipse.smarthome.core.thing.ThingTypeUID;
import org.eclipse.smarthome.core.thing.ThingUID;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.tinkerforge.IPConnection.EnumerateListener;
import com.tinkerforge.IPConnectionBase;
import com.tinkerforge.NotConnectedException;

@NonNullByDefault
public class BrickDaemonDiscoveryService extends AbstractDiscoveryService {
    private BrickDaemonHandler handler;
    private EnumerateListener listener;
    private @Nullable ScheduledFuture<?> job = null;
    private final Logger logger = LoggerFactory.getLogger(BrickDaemonDiscoveryService.class);

    public BrickDaemonDiscoveryService(BrickDaemonHandler handler) {
        super(new HashSet<>(TinkerforgeBindingConstants.SUPPORTED_DEVICES), 10, true);
        this.handler = handler;
        this.listener = this::listenerFn;
    }

    private void listenerFn(String uid, String connectedUid, char position, short[] hardwareVersion,
            short[] firmwareVersion, int deviceIdentifier, short enumerationType) {
        if (enumerationType == IPConnectionBase.ENUMERATION_TYPE_DISCONNECTED) {
            return;
        }

        Optional<ThingTypeUID> opt = null;
        try {
            opt = TinkerforgeBindingConstants.SUPPORTED_DEVICES
                    .stream()
                    .filter(ttuid -> ttuid.getId().equals(
                            DeviceWrapperFactory.getDeviceInfo(deviceIdentifier).deviceThingTypeName)).findFirst();
        } catch (IllegalArgumentException e) { // DeviceWrapperFactory throws if the deviceIdentifier is
                                               // unknown.
            logger.debug("Discovered unknown device {} with UID {} connected to {} at port {}.", deviceIdentifier, uid,
                    connectedUid, position);
            return;
        }
        if (!opt.isPresent()) {
            logger.debug("Discovered unknown device {} with UID {} connected to {} at port {}.", deviceIdentifier, uid,
                    connectedUid, position);
            return;
        }

        ThingTypeUID ttuid = opt.get();

        ThingUID thingUid = new ThingUID(ttuid, uid);

        String fwVersion = firmwareVersion[0] + "." + firmwareVersion[1] + "." + firmwareVersion[2];
        String hwVersion = hardwareVersion[0] + "." + hardwareVersion[1] + "." + hardwareVersion[2];

        DiscoveryResult result = DiscoveryResultBuilder.create(thingUid).withThingType(ttuid).withLabel(uid)
                .withBridge(handler.getThing().getUID()).withProperty(Thing.PROPERTY_FIRMWARE_VERSION, fwVersion)
                .withProperty(Thing.PROPERTY_HARDWARE_VERSION, hwVersion)
                .withProperty(Thing.PROPERTY_VENDOR, "Tinkerforge GmbH")
                .withProperty(Thing.PROPERTY_SERIAL_NUMBER, uid)
                .withProperty(Thing.PROPERTY_MODEL_ID, deviceIdentifier).build();
        thingDiscovered(result);
    }

    public void activate() {
        this.handler.addEnumerateListener(this.listener);
        startBackgroundDiscovery();
    }

    @Override
    public void deactivate() {
        this.handler.removeEnumerateListener(this.listener);
    }

    @Override
    protected void startBackgroundDiscovery() {
        logger.debug("Start Tinkerforge device background discovery for Brick Daemon {}", this.handler.getThing()
                .getUID());
        @Nullable ScheduledFuture<?> job = this.job;
        if (job == null || job.isCancelled()) {
            this.job = scheduler.scheduleWithFixedDelay(() -> {
                try {
                    long scanStart = new Date().getTime();
                    logger.debug("Enumerating devices for Brick Daemon {}.", this.handler.getThing().getUID());
                    handler.enumerate();
                    scheduler.schedule(() -> removeOlderResults(scanStart, handler.getThing().getUID()), 2500, TimeUnit.MILLISECONDS);
                } catch (NotConnectedException e) {
                    logger.debug("Brick Daemon {} currently not connected.", this.handler.getThing().getUID());
                }
            }, 2500, 10 * 60 * 1000, TimeUnit.MILLISECONDS);
        }
    }

    @Override
    protected void stopBackgroundDiscovery() {
        logger.debug("Stop Tinkerforge device background discovery for Brick Daemon "
                + this.handler.getThing().getUID());
        @Nullable ScheduledFuture<?> job = this.job;
        if (job != null && !job.isCancelled()) {
            job.cancel(true);
            this.job = null;
        }
    }

    @Override
    protected void startScan() {
        try {
            logger.debug("Enumerating devices for Brick Daemon {}.", this.handler.getThing().getUID());
            handler.enumerate();
        } catch (NotConnectedException e) {
            logger.debug("Brick Daemon {} currently not connected.", this.handler.getThing().getUID());
        }
    }

    @Override
    protected synchronized void stopScan() {
        super.stopScan();
        removeOlderResults(getTimestampOfLastScan(), handler.getThing().getUID());
    }

    @Override
    public Set<ThingTypeUID> getSupportedThingTypes() {
        return new HashSet<ThingTypeUID>(TinkerforgeBindingConstants.SUPPORTED_DEVICES);
    }

    public void stopDiscovery() {
        stopBackgroundDiscovery();
        deactivate();
    }
}
