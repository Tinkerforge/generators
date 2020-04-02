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
package org.openhab.binding.tinkerforge.internal;

import java.lang.reflect.Method;
import java.util.Collection;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;
import java.util.stream.Collectors;

import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.jdt.annotation.Nullable;
import org.openhab.binding.tinkerforge.internal.device.DeviceInfo;
import org.openhab.binding.tinkerforge.internal.device.DeviceWrapperFactory;
import org.eclipse.smarthome.core.thing.ThingTypeUID;
import org.eclipse.smarthome.core.thing.binding.ThingTypeProvider;
import org.eclipse.smarthome.core.thing.type.ThingType;
import org.osgi.service.component.annotations.Component;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Dynamically provides thing types based on the generated device wrappers.
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
@Component(service = ThingTypeProvider.class, immediate = true)
public class TinkerforgeThingTypeProvider implements ThingTypeProvider {

    private static final Map<ThingTypeUID, ThingType> THING_TYPE_CACHE = new HashMap<>();
    private static final Logger LOGGER = LoggerFactory.getLogger(TinkerforgeThingTypeProvider.class);

    @Override
    public Collection<ThingType> getThingTypes(@Nullable Locale locale) {
        return TinkerforgeBindingConstants.SUPPORTED_DEVICES.stream().map(uid -> getThingType(uid, locale))
                .filter(tt -> tt != null).map(tt -> Utils.assertNonNull(tt)).collect(Collectors.toList());
    }

    @Override
    public @Nullable ThingType getThingType(ThingTypeUID thingTypeUID, @Nullable Locale locale) {
        return getThingTypeStatic(thingTypeUID, locale);
    }

    public static @Nullable ThingType getThingTypeStatic(ThingTypeUID thingTypeUID, @Nullable Locale locale) {
        if (THING_TYPE_CACHE.containsKey(thingTypeUID)) {
            return THING_TYPE_CACHE.get(thingTypeUID);
        }

        DeviceInfo info = null;
        try {
            info = DeviceWrapperFactory.getDeviceInfo(thingTypeUID.getId());
        } catch (Exception e) {
            LOGGER.debug("Could not find device info for thingTypeUID {}: {}.", thingTypeUID, e.getMessage());
            return null;
        }
        ThingType result;
        try {
            Method m = info.deviceClass.getMethod("getThingType", ThingTypeUID.class);
            result = (ThingType) m.invoke(null, thingTypeUID);
        } catch (Exception e) {
            LOGGER.debug("Could not find thing type for thingTypeUID {} of device {}: {}.", thingTypeUID,
                    info.deviceDisplayName, e.getMessage());
            return null;
        }

        THING_TYPE_CACHE.put(thingTypeUID, result);
        return result;
    }
}
