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
import java.util.function.BiFunction;
import java.util.function.Supplier;

import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.jdt.annotation.Nullable;
import org.eclipse.jetty.client.HttpClient;
import org.openhab.binding.tinkerforge.internal.device.BrickletOutdoorWeatherWrapper;
import org.openhab.binding.tinkerforge.internal.device.DeviceWrapper;
import org.eclipse.smarthome.config.core.ConfigDescriptionRegistry;
import org.eclipse.smarthome.core.thing.Bridge;
import org.eclipse.smarthome.core.thing.Thing;
import org.eclipse.smarthome.core.thing.ThingStatus;
import org.eclipse.smarthome.core.thing.ThingUID;
import org.eclipse.smarthome.core.thing.binding.BridgeHandler;
import org.eclipse.smarthome.core.thing.binding.ThingHandler;
import org.eclipse.smarthome.core.thing.binding.ThingHandlerService;
import org.eclipse.smarthome.core.thing.binding.builder.BridgeBuilder;
import org.eclipse.smarthome.core.thing.type.ChannelTypeRegistry;

import com.tinkerforge.IPConnection;

/**
 * Custom handler to act as bridge to outdoor weather stations and sensors.
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
public class BrickletOutdoorWeatherHandler extends DeviceHandler implements BridgeHandler {
    private List<ThingHandler> childHandlers = new ArrayList<>();

    public BrickletOutdoorWeatherHandler(Bridge bridge, BiFunction<String, IPConnection, DeviceWrapper> deviceSupplier,
            Class<? extends ThingHandlerService> actionsClass,
            Supplier<ChannelTypeRegistry> channelTypeRegistrySupplier,
            Supplier<ConfigDescriptionRegistry> configDescriptionRegistrySupplier, @Nullable HttpClient httpClient) {
        super(bridge, deviceSupplier, actionsClass, channelTypeRegistrySupplier, configDescriptionRegistrySupplier,
                httpClient);
    }

    public @Nullable BrickletOutdoorWeatherWrapper getDevice() {
        return (BrickletOutdoorWeatherWrapper) super.getDevice();
    }

    public void handleTimeout() {
        @Nullable
        Bridge b = this.getBridge();
        if (b == null) {
            return;
        }

        @Nullable
        BrickDaemonHandler handler = (@Nullable BrickDaemonHandler) b.getHandler();
        if (handler == null) {
            return;
        }
        handler.handleTimeout(this);
    }

    @Override
    public void initialize() {
        @Nullable
        BrickletOutdoorWeatherWrapper dev = this.getDevice();
        if (dev != null)
            dev.cancelManualUpdates();
        super.initialize();
        if (this.getThing().getStatus() == ThingStatus.ONLINE) {
            for (ThingHandler handler : childHandlers)
                handler.initialize();
        }
    }

    @Override
    protected void initializeDevice() {
        @Nullable
        BrickletOutdoorWeatherWrapper dev = this.getDevice();
        if (dev != null)
            dev.cancelManualUpdates();
        super.initializeDevice();
        for (ThingHandler handler : childHandlers)
            handler.initialize();
    }

    // BridgeHandler implementation copied over from BaseBridgeHandler.
    // This should have been an interface with default methods, e.g. a trait.

    /**
     * Finds and returns a child thing for a given UID of this bridge.
     *
     * @param uid uid of the child thing
     * @return child thing with the given uid or null if thing was not found
     */
    public @Nullable Thing getThingByUID(ThingUID uid) {
        Bridge bridge = getThing();

        List<Thing> things = bridge.getThings();

        for (Thing thing : things) {
            if (thing.getUID().equals(uid)) {
                return thing;
            }
        }

        return null;
    }

    @Override
    public Bridge getThing() {
        return (Bridge) super.getThing();
    }

    /**
     * Creates a bridge builder, which allows to modify the bridge. The method
     * {@link BaseThingHandler#updateThing(Thing)} must be called to persist the
     * changes.
     *
     * @return {@link BridgeBuilder} which builds an exact copy of the bridge (not
     *         null)
     */
    @Override
    protected BridgeBuilder editThing() {
        return BridgeBuilder.create(this.thing.getThingTypeUID(), this.thing.getUID())
                .withBridge(this.thing.getBridgeUID()).withChannels(this.thing.getChannels())
                .withConfiguration(this.thing.getConfiguration()).withLabel(this.thing.getLabel())
                .withLocation(this.thing.getLocation()).withProperties(this.thing.getProperties());
    }

    @Override
    public void childHandlerInitialized(ThingHandler childHandler, Thing childThing) {
        childHandlers.add(childHandler);
    }

    @Override
    public void childHandlerDisposed(ThingHandler childHandler, Thing childThing) {
        childHandlers.remove(childHandler);
    }
}
