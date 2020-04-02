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

import com.tinkerforge.BrickletRemoteSwitchV2;
import com.tinkerforge.TinkerforgeException;

import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.smarthome.binding.tinkerforge.internal.device.BrickletRemoteSwitchV2Wrapper;


/**
 * Wraps the BrickletRemoteSwitcV2hWrapper implementing the RemoteSwitch interface.
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
public class BrickletRemoteSwitchV2WrapperWrapper implements RemoteSwitch {
    BrickletRemoteSwitchV2Wrapper rs;
    BrickletRemoteSwitchV2.SwitchingDoneListener listener = () -> {};

    public BrickletRemoteSwitchV2WrapperWrapper(BrickletRemoteSwitchV2Wrapper rs) {
        this.rs = rs;
    }

    @Override
    public void switchSocketA(int houseCode, int receiverCode, int switchTo) throws TinkerforgeException {
        this.rs.switchSocketA(houseCode, receiverCode, switchTo);
    }

    @Override
    public void switchSocketB(int address, int unit, int switchTo) throws TinkerforgeException {
        this.rs.switchSocketB((long) address, unit, switchTo);
    }

    @Override
    public void dimSocketB(int address, int unit, int dimValue) throws TinkerforgeException {
        this.rs.dimSocketB((int) address, unit, dimValue);
    }

    @Override
    public void switchSocketC(char systemCode, int deviceCode, int switchTo) throws TinkerforgeException {
        this.rs.switchSocketC(systemCode, deviceCode, switchTo);
    }

    @Override
    public void setRepeats(int repeats) throws TinkerforgeException {
        this.rs.setRepeats(repeats);
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
