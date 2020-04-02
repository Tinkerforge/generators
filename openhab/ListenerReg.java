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

import java.util.function.Consumer;

import org.eclipse.jdt.annotation.NonNullByDefault;

/**
 * DTO used in the DeviceWrapper.
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
public class ListenerReg<T> {
    public final T listener;
    public final Consumer<T> toRemove;

    public ListenerReg(T listener, Consumer<T> toRemove) {
        this.listener = listener;
        this.toRemove = toRemove;
    }

    public void deregister() {
        toRemove.accept(listener);
    }
}
