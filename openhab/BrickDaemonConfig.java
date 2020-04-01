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

import java.math.BigDecimal;

import org.eclipse.jdt.annotation.NonNullByDefault;

@NonNullByDefault
public class BrickDaemonConfig {
    public String host = "localhost";
    public Integer port = 4223;

    public Boolean backgroundDiscovery = true;
    public BigDecimal backgroundDiscoveryInterval = BigDecimal.valueOf(10.0);

    public Boolean auth = false;
    public String password = "";
}
