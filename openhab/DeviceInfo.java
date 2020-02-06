package org.eclipse.smarthome.binding.tinkerforge.internal.device;

import org.eclipse.smarthome.core.thing.binding.ThingHandlerService;

public class DeviceInfo {
    public final String deviceDisplayName;
    public final String deviceThingTypeName;
    public final int deviceIdentifier;
    public final Class<? extends DeviceWrapper> deviceClass;
    public final Class<? extends ThingHandlerService>  deviceActionsClass;
    public final String minimum_fw_version;
    public final boolean isCoMCU;

    public DeviceInfo(String deviceDisplayName, String deviceThingTypeName, int deviceIdentifier,
            Class<? extends DeviceWrapper> deviceClass,
            Class<? extends ThingHandlerService> deviceActionsClass,
            String minimum_fw_version,
            boolean isCoMCU) {
        this.deviceDisplayName = deviceDisplayName;
        this.deviceThingTypeName = deviceThingTypeName;
        this.deviceIdentifier = deviceIdentifier;
        this.deviceClass = deviceClass;
        this.deviceActionsClass = deviceActionsClass;
        this.minimum_fw_version = minimum_fw_version;
        this.isCoMCU = isCoMCU;
    }
}
