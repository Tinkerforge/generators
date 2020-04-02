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

import org.eclipse.jdt.annotation.NonNullByDefault;

/**
 * DTO used in the TinkerforgeFirmwareProvider.
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
public class FirmwareInfo {
    public FirmwareInfo(String version, String url) {
        this.version = version;
        this.url = url;

    }

    String version;
    String url;
}
