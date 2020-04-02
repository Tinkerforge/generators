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
package org.eclipse.smarthome.binding.tinkerforge.internal;

import java.lang.reflect.Method;
import java.net.URI;
import java.util.Collection;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;
import java.util.stream.Collectors;

import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.jdt.annotation.Nullable;
import org.eclipse.smarthome.binding.tinkerforge.internal.device.DeviceInfo;
import org.eclipse.smarthome.binding.tinkerforge.internal.device.DeviceWrapperFactory;
import org.eclipse.smarthome.config.core.ConfigDescription;
import org.eclipse.smarthome.config.core.ConfigDescriptionProvider;
import org.eclipse.smarthome.core.thing.ThingTypeUID;
import org.osgi.service.component.annotations.Component;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Dynamically provides config descriptions based on the generated device wrappers.
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
@Component(service = { TinkerforgeConfigDescriptionProvider.class, ConfigDescriptionProvider.class }, immediate = true)
public class TinkerforgeConfigDescriptionProvider implements ConfigDescriptionProvider {

    private final Map<URI, ConfigDescription> configDescriptionCache = new HashMap<>();

    private static final Logger logger = LoggerFactory.getLogger(TinkerforgeConfigDescriptionProvider.class);

    @Override
    public Collection<ConfigDescription> getConfigDescriptions(@Nullable Locale locale) {
        return TinkerforgeBindingConstants.SUPPORTED_CONFIG_DESCRIPTIONS.keySet().stream()
                .map(uri -> getConfigDescription(uri, locale)).filter(cd -> cd != null)
                .map(cd -> Utils.assertNonNull(cd)).collect(Collectors.toList());
    }

    @Override
    public @Nullable ConfigDescription getConfigDescription(URI uri, @Nullable Locale locale) {
        if (configDescriptionCache.containsKey(uri)) {
            return configDescriptionCache.get(uri);
        }

        ThingTypeUID thingTypeUID = null;
        DeviceInfo info = null;
        ConfigDescription result = null;

        try {
            thingTypeUID = TinkerforgeBindingConstants.SUPPORTED_CONFIG_DESCRIPTIONS.get(uri);
            info = DeviceWrapperFactory.getDeviceInfo(thingTypeUID.getId());
        } catch (Exception e) {
            logger.debug("Could not find device info for configDescriptionURI {}: {}.", uri, e.getMessage());
            return null;
        }

        try {
            Method m = info.deviceClass.getMethod("getConfigDescription", URI.class);
            result = (ConfigDescription) m.invoke(null, uri);
        } catch (Exception e) {
            logger.debug("Could not find config description for configDescriptionURI {} of device {}: {}.", uri,
                    info.deviceDisplayName, e.getMessage());
            return null;
        }

        configDescriptionCache.put(uri, result);
        return result;
    }

}
