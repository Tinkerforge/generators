package com.tinkerforge;

import java.util.function.BiConsumer;

import org.eclipse.smarthome.core.types.State;

public abstract class OpenHABSensor extends Device {
    public OpenHABSensor(String uid, IPConnection ipcon) {
        super(uid, ipcon);
    }

    public abstract void initialize(Object config, BiConsumer<String, State> callbackFn) throws TinkerforgeException;

    public abstract void dispose(Object config) throws TinkerforgeException;

    public abstract Class<?> getConfigurationClass();

    public abstract State refreshValue(String value) throws TinkerforgeException;
}
