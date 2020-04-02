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
package org.eclipse.smarthome.binding.tinkerforge.internal.handler;

import org.eclipse.jdt.annotation.NonNullByDefault;

import com.tinkerforge.TinkerforgeException;
/**
 * Works like a normal consumer but supports throwing (checked) TinkerforgeExceptions.
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
@FunctionalInterface
public interface CheckedConsumer<T> {
    void accept(T t) throws TinkerforgeException;
}
