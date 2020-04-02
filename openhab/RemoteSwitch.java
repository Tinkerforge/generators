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

import java.util.concurrent.atomic.AtomicBoolean;

import com.tinkerforge.TinkerforgeException;

import org.eclipse.jdt.annotation.NonNullByDefault;

/**
 * Abstracts common usage of remote switch bricklets.
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
public interface RemoteSwitch {
    void switchSocketA(int houseCode, int receiverCode, int switchTo) throws TinkerforgeException;

    void switchSocketB(int address, int unit, int switchTo) throws TinkerforgeException;

    void dimSocketB(int address, int unit, int dimValue) throws TinkerforgeException;

    void switchSocketC(char systemCode, int deviceCode, int switchTo) throws TinkerforgeException;

    void setRepeats(int repeats) throws TinkerforgeException;

    int getSwitchingState() throws TinkerforgeException;

    void addSwitchingDoneListener(AtomicBoolean isSwitching);

    void removeSwitchingDoneListener();
}
