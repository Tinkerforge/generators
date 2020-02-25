package org.eclipse.smarthome.binding.tinkerforge.internal.device;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.Callable;
import java.util.concurrent.ScheduledExecutorService;
import java.util.function.BiConsumer;
import java.util.function.Consumer;
import java.util.function.Function;

import com.tinkerforge.TinkerforgeException;
import com.tinkerforge.Device.Identity;

import org.eclipse.smarthome.config.core.Configuration;
import org.eclipse.smarthome.core.types.State;
import org.eclipse.smarthome.core.types.Command;
import org.eclipse.smarthome.core.thing.binding.BaseThingHandler;


public interface DeviceWrapper {
    public class SetterRefresh {
        public final String channel;
        public final long delay;

        public SetterRefresh(String channel, long delay) {
            this.channel = channel;
            this.delay = delay;
        }
    }

    public class ListenerReg<T> {
        public final T listener;
        public final Consumer<T> toRemove;

        public ListenerReg(T listener, Consumer<T> toRemove) {
            this.listener = listener;
            this.toRemove = toRemove;
        }
    }

    public abstract void cancelManualUpdates();

    public abstract <T> T reg(T listener, Consumer<T> toRemove);

    public abstract void initialize(Configuration config, Function<String, Configuration> getChannelConfigFn, BiConsumer<String, State> updateStateFn, BiConsumer<String, String> triggerChannelFn, ScheduledExecutorService scheduler, BaseThingHandler handler) throws TinkerforgeException;

    public abstract void dispose(Configuration config) throws TinkerforgeException;

    public abstract void refreshValue(String value, Configuration config, Configuration channelConfig, BiConsumer<String, State> updateStateFn, BiConsumer<String, String> triggerChannelFn) throws TinkerforgeException;

    public abstract List<SetterRefresh> handleCommand(Configuration config, Configuration channelConfig, String channel, Command command) throws TinkerforgeException;

    public abstract List<String> getEnabledChannels(Configuration config) throws TinkerforgeException;

    public abstract Identity getIdentity() throws TinkerforgeException;
}
