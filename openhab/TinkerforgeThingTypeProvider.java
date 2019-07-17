package org.eclipse.smarthome.binding.tinkerforge.internal;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.stream.Collectors;

import com.tinkerforge.BrickDaemon;
import com.tinkerforge.DeviceFactory;
import com.tinkerforge.DeviceInfo;

import org.eclipse.jdt.annotation.Nullable;
import org.eclipse.smarthome.core.thing.ThingTypeUID;
import org.eclipse.smarthome.core.thing.binding.ThingTypeProvider;
import org.eclipse.smarthome.core.thing.type.ThingType;
import org.eclipse.smarthome.core.thing.type.ThingTypeBuilder;
import org.osgi.service.component.annotations.Component;

@Component(service = ThingTypeProvider.class, immediate = true)
public class TinkerforgeThingTypeProvider implements ThingTypeProvider {

    private static final Map<ThingTypeUID, ThingType> thingTypeCache = new HashMap<>();

    @Override
    public Collection<ThingType> getThingTypes(@Nullable Locale locale) {
        return TinkerforgeBindingConstants.SUPPORTED_DEVICES.stream().map(uid -> getThingType(uid, locale))
                .collect(Collectors.toList());
    }

    @Override
    public @Nullable ThingType getThingType(ThingTypeUID thingTypeUID, @Nullable Locale locale) {
        return getThingTypeStatic(thingTypeUID, locale);
    }

    public static @Nullable ThingType getThingTypeStatic(ThingTypeUID thingTypeUID, @Nullable Locale locale) {
        if (thingTypeCache.containsKey(thingTypeUID)) {
            System.out.println("Cache hit for " + thingTypeUID);
            return thingTypeCache.get(thingTypeUID);
        }

        DeviceInfo info = null;
        try {
            info = DeviceFactory.getDeviceInfo(thingTypeUID.getId());
        }
        catch (Exception e) {
            System.out.println("ThingType meta data retrival failed");
            return null;
        }
        ThingType result;
        try {
            Method m = info.deviceClass.getMethod("getThingType", ThingTypeUID.class);
            result = (ThingType) m.invoke(null, thingTypeUID);
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("ThingType creation failed");
            return null;
        }

        thingTypeCache.put(thingTypeUID, result);
        System.out.println("Cache miss for " + thingTypeUID);
        return result;
    }
}
