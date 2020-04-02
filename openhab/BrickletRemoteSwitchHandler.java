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

import java.util.ArrayList;
import java.util.List;
import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.function.BiFunction;
import java.util.function.Consumer;
import java.util.function.Supplier;

import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.jdt.annotation.Nullable;
import org.eclipse.jetty.client.HttpClient;
import org.eclipse.smarthome.binding.tinkerforge.internal.device.BrickletRemoteSwitchV2Wrapper;
import org.eclipse.smarthome.binding.tinkerforge.internal.device.BrickletRemoteSwitchWrapper;
import org.eclipse.smarthome.binding.tinkerforge.internal.device.DeviceWrapper;
import org.eclipse.smarthome.config.core.ConfigDescriptionRegistry;
import org.eclipse.smarthome.core.thing.Bridge;
import org.eclipse.smarthome.core.thing.Thing;
import org.eclipse.smarthome.core.thing.ThingStatus;
import org.eclipse.smarthome.core.thing.ThingStatusDetail;
import org.eclipse.smarthome.core.thing.ThingUID;
import org.eclipse.smarthome.core.thing.binding.BridgeHandler;
import org.eclipse.smarthome.core.thing.binding.ThingHandler;
import org.eclipse.smarthome.core.thing.binding.ThingHandlerService;
import org.eclipse.smarthome.core.thing.binding.builder.BridgeBuilder;
import org.eclipse.smarthome.core.thing.type.ChannelTypeRegistry;

import com.tinkerforge.BrickletRemoteSwitch;
import com.tinkerforge.BrickletRemoteSwitchV2;
import com.tinkerforge.IPConnection;
import com.tinkerforge.TimeoutException;
import com.tinkerforge.TinkerforgeException;

/**
 * Custom handler to act as bridge to remote sockets and dimmers.
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
public class BrickletRemoteSwitchHandler extends DeviceHandler implements BridgeHandler {
    private @Nullable RemoteSwitch remoteSwitch = null;

    private List<ThingHandler> childHandlers = new ArrayList<>();

    // Inserted tasks are never null, but annotating @Nullable here fixes the wrong assumption, that tasks.peek() will never return null.
    private Queue<@Nullable Task> tasks = new ConcurrentLinkedQueue<>();
    private AtomicBoolean isSwitching = new AtomicBoolean(true);
    @Nullable private ScheduledFuture<?> workFuture = null;

    public BrickletRemoteSwitchHandler(Bridge bridge, BiFunction<String, IPConnection, DeviceWrapper> deviceSupplier,
            Class<? extends ThingHandlerService> actionsClass,
            Supplier<ChannelTypeRegistry> channelTypeRegistrySupplier,
            Supplier<ConfigDescriptionRegistry> configDescriptionRegistrySupplier, @Nullable HttpClient httpClient) {
        super(bridge, deviceSupplier, actionsClass, channelTypeRegistrySupplier, configDescriptionRegistrySupplier,
                httpClient);
    }

    public void handleTimeout() {
        @Nullable Bridge bridge = getBridge();
        if (bridge == null) {
            return;
        }

        @Nullable BrickDaemonHandler brickd = (BrickDaemonHandler) (bridge.getHandler());
        if (brickd == null) {
            return;
        }

        brickd.handleTimeout(this);
    }

    @Override
    public void initialize() {
        super.initialize();
        for (ThingHandler handler : childHandlers)
            handler.initialize();
    }

    @Override
    protected void initializeDevice() {
        super.initializeDevice();
        DeviceWrapper dev = this.getDevice();
        if (dev == null) {
            return;
        }

        for (ThingHandler handler : childHandlers)
            handler.initialize();

        @Nullable ScheduledFuture<?> workFuture = this.workFuture;
        if (workFuture != null)
            workFuture.cancel(false);

        @Nullable RemoteSwitch remoteSwitch = this.remoteSwitch;
        if (remoteSwitch != null)
            remoteSwitch.removeSwitchingDoneListener();



        if (dev instanceof BrickletRemoteSwitchWrapper) {
            remoteSwitch = new BrickletRemoteSwitchWrapperWrapper((BrickletRemoteSwitchWrapper) dev);
        } else if (dev instanceof BrickletRemoteSwitchV2Wrapper) {
            remoteSwitch = new BrickletRemoteSwitchV2WrapperWrapper((BrickletRemoteSwitchV2Wrapper) dev);
        } else {
            logger.warn("Failed to initialize {}: device was of unknown type", thing.getUID().getId());
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.HANDLER_INITIALIZING_ERROR);
            return;
        }
        remoteSwitch.addSwitchingDoneListener(isSwitching);
        this.remoteSwitch = remoteSwitch;

        try {
            isSwitching.set(remoteSwitch.getSwitchingState() == BrickletRemoteSwitchWrapper.SWITCHING_STATE_BUSY);
            workFuture = scheduler.scheduleWithFixedDelay(this::work, 500, 500, TimeUnit.MILLISECONDS);
        } catch (TimeoutException e) {
            logger.debug("Failed to initialize {}: {}", thing.getUID().getId(), e.getMessage());
            handleTimeout();
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.HANDLER_INITIALIZING_ERROR);
        } catch (TinkerforgeException e) {
            logger.warn("Failed to initialize {}: {}", thing.getUID().getId(), e.getMessage());
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.HANDLER_INITIALIZING_ERROR);
        }
    }

    @Override
    public void handleRemoval() {
        @Nullable ScheduledFuture<?> workFuture = this.workFuture;
        if (workFuture != null)
            workFuture.cancel(false);
        super.handleRemoval();
    }

    public void enqueue(Task task) {
        tasks.add(task);
    }

    private void work() {
        if (isSwitching.get())
            return;

        @Nullable Task task = tasks.peek();
        if (task == null)
            return;

        isSwitching.set(true);
        tasks.poll(); // Remove peeked task.

        @Nullable RemoteSwitch remoteSwitch = this.remoteSwitch;
        if (remoteSwitch == null)
            return;

        try {
            task.task.accept(remoteSwitch);
        } catch (TinkerforgeException e) {
            task.callback.accept(false);
            handleTimeout();
            return;
        }

        task.callback.accept(true);
    }

    // BridgeHandler implementation copied over from BaseBridgeHandler.
    // This should have been an interface with default methods, e.g. a trait.

    /**
     * Finds and returns a child thing for a given UID of this bridge.
     *
     * @param uid uid of the child thing
     * @return child thing with the given uid or null if thing was not found
     */
    public @Nullable Thing getThingByUID(ThingUID uid) {
        Bridge bridge = getThing();

        List<Thing> things = bridge.getThings();

        for (Thing thing : things) {
            if (thing.getUID().equals(uid)) {
                return thing;
            }
        }

        return null;
    }

    @Override
    public Bridge getThing() {
        return (Bridge) super.getThing();
    }

    /**
     * Creates a bridge builder, which allows to modify the bridge. The method
     * {@link BaseThingHandler#updateThing(Thing)} must be called to persist the
     * changes.
     *
     * @return {@link BridgeBuilder} which builds an exact copy of the bridge (not
     *         null)
     */
    @Override
    protected BridgeBuilder editThing() {
        return BridgeBuilder.create(this.thing.getThingTypeUID(), this.thing.getUID())
                .withBridge(this.thing.getBridgeUID()).withChannels(this.thing.getChannels())
                .withConfiguration(this.thing.getConfiguration()).withLabel(this.thing.getLabel())
                .withLocation(this.thing.getLocation()).withProperties(this.thing.getProperties());
    }

    @Override
    public void childHandlerInitialized(ThingHandler childHandler, Thing childThing) {
        childHandlers.add(childHandler);
    }

    @Override
    public void childHandlerDisposed(ThingHandler childHandler, Thing childThing) {
        childHandlers.remove(childHandler);
    }
}
