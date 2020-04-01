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
package org.eclipse.smarthome.binding.tinkerforge.internal.device;

import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.smarthome.core.thing.binding.ThingHandlerService;

/**
 * DTO containing information about a brick or bricklet
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
public class DeviceInfo {
    public final String deviceDisplayName;
    public final String deviceThingTypeName;
    public final int deviceIdentifier;
    public final Class<? extends DeviceWrapper> deviceClass;
    public final Class<? extends ThingHandlerService> deviceActionsClass;
    public final String minimum_fw_version;
    public final boolean isCoMCU;

    public DeviceInfo(String deviceDisplayName, String deviceThingTypeName, int deviceIdentifier,
            Class<? extends DeviceWrapper> deviceClass, Class<? extends ThingHandlerService> deviceActionsClass,
            String minimum_fw_version, boolean isCoMCU) {
        this.deviceDisplayName = deviceDisplayName;
        this.deviceThingTypeName = deviceThingTypeName;
        this.deviceIdentifier = deviceIdentifier;
        this.deviceClass = deviceClass;
        this.deviceActionsClass = deviceActionsClass;
        this.minimum_fw_version = minimum_fw_version;
        this.isCoMCU = isCoMCU;
    }
}
