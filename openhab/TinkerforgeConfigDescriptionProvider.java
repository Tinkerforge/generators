package org.eclipse.smarthome.binding.tinkerforge.internal;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.net.URI;
import java.util.Collection;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;
import java.util.stream.Collectors;

import com.tinkerforge.DeviceFactory;
import com.tinkerforge.DeviceInfo;

import org.eclipse.jdt.annotation.Nullable;
import org.eclipse.smarthome.config.core.ConfigDescription;
import org.eclipse.smarthome.config.core.ConfigDescriptionParameterBuilder;
import org.eclipse.smarthome.config.core.ConfigDescriptionProvider;
import org.eclipse.smarthome.config.core.FilterCriteria;
import org.eclipse.smarthome.config.core.ParameterOption;
import org.eclipse.smarthome.config.core.ConfigDescriptionParameter.Type;
import org.eclipse.smarthome.core.thing.ThingTypeUID;
import org.osgi.service.component.annotations.Component;

@Component(service = { TinkerforgeConfigDescriptionProvider.class, ConfigDescriptionProvider.class }, immediate = true)
public class TinkerforgeConfigDescriptionProvider implements ConfigDescriptionProvider {

    private final Map<URI, ConfigDescription> configDescriptionCache = new HashMap<>();

    @Override
    public Collection<ConfigDescription> getConfigDescriptions(@Nullable Locale locale) {
        return TinkerforgeBindingConstants.SUPPORTED_CONFIG_DESCRIPTIONS.keySet().stream().map(uri -> getConfigDescription(uri, locale)).collect(Collectors.toList());
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
            info = DeviceFactory.getDeviceInfo(thingTypeUID.getId());
        }
        catch (Exception e) {
            //e.printStackTrace();
            System.out.println("ConfigDescription meta-info search failed:" + thingTypeUID + " uri " + uri);
            return null;
        }

        try {
            Method m = info.deviceClass.getMethod("getConfigDescription", URI.class);
            result = (ConfigDescription) m.invoke(null, uri);
        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
            System.out.println("ConfigDescription creation failed");
            return null;
        }

        configDescriptionCache.put(uri, result);
        return result;
    }

}
