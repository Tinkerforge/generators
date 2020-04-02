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

import com.tinkerforge.BrickletRemoteSwitch;
import com.tinkerforge.TinkerforgeException;

import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.smarthome.binding.tinkerforge.internal.device.BrickletRemoteSwitchWrapper;


/**
 * Wraps the BrickletRemoteSwitchWrapper implementing the RemoteSwitch interface.
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
public class BrickletRemoteSwitchWrapperWrapper implements RemoteSwitch {
    BrickletRemoteSwitchWrapper rs;
    BrickletRemoteSwitch.SwitchingDoneListener listener = () -> {};

    public BrickletRemoteSwitchWrapperWrapper(BrickletRemoteSwitchWrapper rs) {
        this.rs = rs;
    }

    @Override
    public void switchSocketA(int houseCode, int receiverCode, int switchTo) throws TinkerforgeException {
        this.rs.switchSocketA((short) houseCode, (short) receiverCode, (short) switchTo);
    }

    @Override
    public void switchSocketB(int address, int unit, int switchTo) throws TinkerforgeException {
        this.rs.switchSocketB((long) address, (short) unit, (short) switchTo);
    }

    @Override
    public void dimSocketB(int address, int unit, int dimValue) throws TinkerforgeException {
        this.rs.dimSocketB((int) address, (short) unit, (short) dimValue);
    }

    @Override
    public void switchSocketC(char systemCode, int deviceCode, int switchTo) throws TinkerforgeException {
        this.rs.switchSocketC(systemCode, (short) deviceCode, (short) switchTo);
    }

    @Override
    public void setRepeats(int repeats) throws TinkerforgeException {
        this.rs.setRepeats((short) repeats);
    }

    @Override
    public int getSwitchingState() throws TinkerforgeException {
        return this.rs.getSwitchingState();
    }

        @Override
        public void addSwitchingDoneListener(AtomicBoolean isSwitching) {
            listener = () -> isSwitching.set(false);
            this.rs.addSwitchingDoneListener(listener);
        }

        @Override
        public void removeSwitchingDoneListener() {
            this.rs.removeSwitchingDoneListener(listener);
        }
    }
