package com.tinkerforge;

import org.eclipse.smarthome.core.thing.binding.ThingHandlerService;

public class DeviceInfo {
    public final String deviceDisplayName;
    public final String deviceThingTypeName;
    public final int deviceIdentifier;
    public final Class<?> deviceClass;
    public final Class<? extends ThingHandlerService>  deviceActionsClass;

    public DeviceInfo(String deviceDisplayName, String deviceThingTypeName, int deviceIdentifier,
            Class<?> deviceClass,
            Class<? extends ThingHandlerService> deviceActionsClass) {
        this.deviceDisplayName = deviceDisplayName;
        this.deviceThingTypeName = deviceThingTypeName;
        this.deviceIdentifier = deviceIdentifier;
        this.deviceClass = deviceClass;
        this.deviceActionsClass = deviceActionsClass;
    }
}
