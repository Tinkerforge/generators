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
package org.eclipse.smarthome.binding.tinkerforge.internal;

import static org.eclipse.smarthome.binding.tinkerforge.internal.TinkerforgeBindingConstants.*;

import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Hashtable;
import java.util.Map;
import java.util.Set;

import com.tinkerforge.DeviceFactory;
import com.tinkerforge.Device;
import com.tinkerforge.IPConnection;

import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.jdt.annotation.Nullable;
import org.eclipse.smarthome.binding.tinkerforge.discovery.BrickDaemonDiscoveryService;
import org.eclipse.smarthome.binding.tinkerforge.discovery.TinkerforgeDiscoveryService;
import org.eclipse.smarthome.binding.tinkerforge.internal.handler.BrickDaemonHandler;
import org.eclipse.smarthome.binding.tinkerforge.internal.handler.BrickletOutdoorWeatherHandler;
import org.eclipse.smarthome.binding.tinkerforge.internal.handler.BrickletOutdoorWeatherSensorHandler;
import org.eclipse.smarthome.binding.tinkerforge.internal.handler.BrickletOutdoorWeatherStationHandler;
import org.eclipse.smarthome.binding.tinkerforge.internal.handler.BrickletRemoteSwitchHandler;
import org.eclipse.smarthome.binding.tinkerforge.internal.handler.DeviceHandler;
import org.eclipse.smarthome.binding.tinkerforge.internal.handler.RemoteDimmerTypeBHandler;
import org.eclipse.smarthome.binding.tinkerforge.internal.handler.RemoteSocketTypeAHandler;
import org.eclipse.smarthome.binding.tinkerforge.internal.handler.RemoteSocketTypeBHandler;
import org.eclipse.smarthome.binding.tinkerforge.internal.handler.RemoteSocketTypeCHandler;
import org.eclipse.smarthome.config.core.ConfigDescriptionRegistry;
import org.eclipse.smarthome.config.discovery.DiscoveryService;
import org.eclipse.smarthome.core.thing.Bridge;
import org.eclipse.smarthome.core.thing.Thing;
import org.eclipse.smarthome.core.thing.ThingTypeUID;
import org.eclipse.smarthome.core.thing.ThingUID;
import org.eclipse.smarthome.core.thing.binding.BaseThingHandlerFactory;
import org.eclipse.smarthome.core.thing.binding.ThingHandler;
import org.eclipse.smarthome.core.thing.binding.ThingHandlerFactory;
import org.eclipse.smarthome.core.thing.type.ChannelTypeRegistry;
import org.osgi.framework.ServiceRegistration;
import org.osgi.service.component.annotations.Component;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * The {@link TinkerforgeHandlerFactory} is responsible for creating things and thing
 * handlers.
 *
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
@Component(configurationPid = "binding.tinkerforge", service = ThingHandlerFactory.class)
public class TinkerforgeHandlerFactory extends BaseThingHandlerFactory {
    private final Map<TinkerforgeDiscoveryService, @Nullable ServiceRegistration<?>> discoveryServiceRegs = new HashMap<>();

    private final Logger logger = LoggerFactory.getLogger(TinkerforgeChannelTypeProvider.class);

    @Override
    public boolean supportsThingType(ThingTypeUID thingTypeUID) {
        return TinkerforgeBindingConstants.SUPPORTED_DEVICES.contains(thingTypeUID);
    }

    private @Nullable Device createDevice(String thingName, String uid, IPConnection ipcon) {
        try {
            return (Device)DeviceFactory.createDevice(thingName, uid, ipcon);
        }
        catch(Exception e) {
            logger.warn("Could not create device {} with uid {}: {}.", thingName, uid, e);
            return null;
        }
    }

    @Override
    protected @Nullable ThingHandler createHandler(Thing thing) {
        ThingTypeUID thingTypeUID = thing.getThingTypeUID();
        if (thingTypeUID.equals(THING_TYPE_BRICK_DAEMON)) {
            assert (thing instanceof Bridge);
            return new BrickDaemonHandler((Bridge) thing, this::registerBrickDaemonDiscoveryService, this::deregisterBrickDaemonDiscoveryService);
        } else if (thingTypeUID.equals(THING_TYPE_BRICKLET_OUTDOOR_WEATHER)) {
            assert (thing instanceof Bridge);
            return new BrickletOutdoorWeatherHandler((Bridge) thing,
                                                     (String uid, IPConnection ipcon) -> createDevice(thingTypeUID.getId(), uid, ipcon),
                                                     () -> this.bundleContext.getService(this.bundleContext.getServiceReference(ChannelTypeRegistry.class)),
                                                     () -> this.bundleContext.getService(this.bundleContext.getServiceReference(ConfigDescriptionRegistry.class)));
        } else if (thingTypeUID.equals(THING_TYPE_BRICKLET_REMOTE_SWITCH) || thingTypeUID.equals(THING_TYPE_BRICKLET_REMOTE_SWITCH_V2)) {
            assert (thing instanceof Bridge);
            return new BrickletRemoteSwitchHandler((Bridge) thing,
                                                     (String uid, IPConnection ipcon) -> createDevice(thingTypeUID.getId(), uid, ipcon),
                                                     () -> this.bundleContext.getService(this.bundleContext.getServiceReference(ChannelTypeRegistry.class)),
                                                     () -> this.bundleContext.getService(this.bundleContext.getServiceReference(ConfigDescriptionRegistry.class)));
        } else if (thingTypeUID.equals(THING_TYPE_OUTDOOR_WEATHER_STATION)) {
            return new BrickletOutdoorWeatherStationHandler(thing);
        } else if (thingTypeUID.equals(THING_TYPE_OUTDOOR_WEATHER_SENSOR)) {
            return new BrickletOutdoorWeatherSensorHandler(thing);
        } else if (thingTypeUID.equals(THING_TYPE_REMOTE_SOCKET_TYPE_A)) {
            return new RemoteSocketTypeAHandler(thing);
        } else if (thingTypeUID.equals(THING_TYPE_REMOTE_SOCKET_TYPE_B)) {
            return new RemoteSocketTypeBHandler(thing);
        } else if (thingTypeUID.equals(THING_TYPE_REMOTE_SOCKET_TYPE_C)) {
            return new RemoteSocketTypeCHandler(thing);
        } else if (thingTypeUID.equals(THING_TYPE_REMOTE_DIMMER_TYPE_B)) {
            return new RemoteDimmerTypeBHandler(thing);
        }

        String thingName = thingTypeUID.getId();
        return new DeviceHandler(thing,
                                (String uid, IPConnection ipcon) -> createDevice(thingName, uid, ipcon),
                                DeviceFactory.getDeviceInfo(thingName).deviceActionsClass,
                                () -> this.bundleContext.getService(this.bundleContext.getServiceReference(ChannelTypeRegistry.class)),
                                () -> this.bundleContext.getService(this.bundleContext.getServiceReference(ConfigDescriptionRegistry.class)));
    }

    private synchronized void registerBrickDaemonDiscoveryService(TinkerforgeDiscoveryService service) {
        this.discoveryServiceRegs.put(service, bundleContext.registerService(DiscoveryService.class.getName(), service, new Hashtable<String, Object>()));
    }

    private synchronized void deregisterBrickDaemonDiscoveryService(TinkerforgeDiscoveryService service) {
        ServiceRegistration<?> serviceReg = this.discoveryServiceRegs.remove(service);
        if (serviceReg != null) {
            // remove discovery service, if bridge handler is removed
            serviceReg.unregister();
            if (service != null) {
                service.stopDiscovery();
            }
        }
    }

   /* @Override
    protected synchronized void removeHandler(ThingHandler thingHandler) {
        if (thingHandler instanceof BrickDaemonHandler) {
            ServiceRegistration<?> serviceReg = this.discoveryServiceRegs.remove(thingHandler.getThing().getUID());
            if (serviceReg != null) {
                // remove discovery service, if bridge handler is removed
                BrickDaemonDiscoveryService service = (BrickDaemonDiscoveryService) bundleContext
                        .getService(serviceReg.getReference());
                serviceReg.unregister();
                if (service != null) {
                    service.deactivate();
                }
            }
        }
    }*/
}
