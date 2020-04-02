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

/**
 * DTO used in the generated device wrappers.
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
public class SetterRefresh {
    public final String channel;
    public final long delay;

    public SetterRefresh(String channel, long delay) {
        this.channel = channel;
        this.delay = delay;
    }
}
