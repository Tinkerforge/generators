package com.tinkerforge;

public class DeviceInfo {
    public final String deviceDisplayName;
    public final String deviceThingTypeName;
    public final int deviceIdentifier;
    public final Class<?> deviceClass;

    public DeviceInfo(String deviceDisplayName, String deviceThingTypeName, int deviceIdentifier,
            Class<?> deviceClass) {
        this.deviceDisplayName = deviceDisplayName;
        this.deviceThingTypeName = deviceThingTypeName;
        this.deviceIdentifier = deviceIdentifier;
        this.deviceClass = deviceClass;
    }
}
