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
package org.openhab.binding.tinkerforge.internal.device;

import java.util.List;
import java.util.concurrent.ScheduledExecutorService;
import java.util.function.BiConsumer;
import java.util.function.Consumer;
import java.util.function.Function;

import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.smarthome.config.core.Configuration;
import org.eclipse.smarthome.core.thing.binding.BaseThingHandler;
import org.eclipse.smarthome.core.types.Command;
import org.eclipse.smarthome.core.types.State;

import com.tinkerforge.Device.Identity;
import com.tinkerforge.TinkerforgeException;

/**
 * Implemented by classes to wrap a device of the Java Bindings.
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
public interface DeviceWrapper {
    public abstract void cancelManualUpdates();

    public abstract <T> T reg(T listener, Consumer<T> toRemove);

    public abstract void initialize(Configuration config, Function<String, Configuration> getChannelConfigFn,
            BiConsumer<String, State> updateStateFn, BiConsumer<String, String> triggerChannelFn,
            ScheduledExecutorService scheduler, BaseThingHandler handler) throws TinkerforgeException;

    public abstract void dispose(Configuration config) throws TinkerforgeException;

    public abstract void refreshValue(String value, Configuration config, Configuration channelConfig,
            BiConsumer<String, State> updateStateFn, BiConsumer<String, String> triggerChannelFn)
            throws TinkerforgeException;

    public abstract List<SetterRefresh> handleCommand(Configuration config, Configuration channelConfig,
            String channel, Command command) throws TinkerforgeException;

    public abstract List<String> getEnabledChannels(Configuration config) throws TinkerforgeException;

    public abstract Identity getIdentity() throws TinkerforgeException;
}
