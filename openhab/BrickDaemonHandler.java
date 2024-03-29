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
package org.openhab.binding.tinkerforge.internal.handler;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.concurrent.Callable;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Future;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;
import java.util.function.Consumer;
import java.util.function.Predicate;
import java.util.stream.Collectors;

import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.jdt.annotation.Nullable;
import org.eclipse.smarthome.core.thing.Bridge;
import org.eclipse.smarthome.core.thing.ChannelUID;
import org.eclipse.smarthome.core.thing.Thing;
import org.eclipse.smarthome.core.thing.ThingStatus;
import org.eclipse.smarthome.core.thing.ThingStatusDetail;
import org.eclipse.smarthome.core.thing.binding.BaseBridgeHandler;
import org.eclipse.smarthome.core.thing.binding.ThingHandler;
import org.eclipse.smarthome.core.types.Command;
import org.openhab.binding.tinkerforge.discovery.BrickDaemonDiscoveryService;
import org.openhab.binding.tinkerforge.internal.Utils;
import org.openhab.binding.tinkerforge.internal.device.BrickDaemonConfig;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.tinkerforge.AlreadyConnectedException;
import com.tinkerforge.IPConnection;
import com.tinkerforge.IPConnection.DisconnectedListener;
import com.tinkerforge.IPConnection.EnumerateListener;
import com.tinkerforge.NetworkException;
import com.tinkerforge.NotConnectedException;
import com.tinkerforge.TimeoutException;
import com.tinkerforge.TinkerforgeException;

/**
 * Handles communication with Brick Daemons.
 *
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
public class BrickDaemonHandler extends BaseBridgeHandler {
    public IPConnection ipcon;
    private Consumer<BrickDaemonDiscoveryService> registerFn;
    private Consumer<BrickDaemonDiscoveryService> deregisterFn;
    private @Nullable BrickDaemonDiscoveryService discoveryService;
    private @Nullable ScheduledFuture<?> connectFuture;
    private @Nullable ScheduledFuture<?> heartbeatFuture;
    private DisconnectedListener disconnectedListener;

    private final Logger logger = LoggerFactory.getLogger(BrickDaemonHandler.class);
    private static final int FIRST_RECONNECT_INTERVAL_SECS = 10;
    private static final int MAX_RECONNECT_INTERVAL_SECS = 600;

    private static final int FIRST_HEARTBEAT_INTERVAL_SECS = 10;
    private static final int HEARTBEAT_INTERVAL_SECS = 90;

    private static final int ALL_PACKETS_LOST_THRESHOLD = 5;
    private final Map<String, ThingHandler> childHandlers = new ConcurrentHashMap<>();

    private final Object isRequestedHeartbeatRunningLock = new Object();
    private boolean isRequestedHeartbeatRunning = false;

    public BrickDaemonHandler(Bridge bridge, Consumer<BrickDaemonDiscoveryService> registerFn,
            Consumer<BrickDaemonDiscoveryService> deregisterFn) {
        super(bridge);
        this.registerFn = registerFn;
        this.deregisterFn = deregisterFn;
        ipcon = new IPConnection();
        // attemptReconnect implements a custom auto reconnect mechanism
        ipcon.setAutoReconnect(false);

        disconnectedListener = reason -> {
            updateStatus(ThingStatus.OFFLINE);
            this.stopDiscoveryService();
            attemptReconnect(FIRST_RECONNECT_INTERVAL_SECS);
        };
    }

    @Override
    public void handleCommand(ChannelUID channelUID, Command command) {
    }

    private List<ReachabilityResult> checkReachability(Predicate<? super Thing> filter) {
        List<DeviceHandler> handlers = getThing().getThings().stream().filter(filter)
                .map(t -> (DeviceHandler) t.getHandler()).filter(h -> h != null) // If checkReachability is called fast
                                                                                 // enough, some things don't have a
                                                                                 // handler yet.
                .collect(Collectors.toList());
        List<Callable<ReachabilityResult>> tasks = handlers.stream()
                .map(h -> (Callable<ReachabilityResult>) (() -> new ReachabilityResult(h.checkReachablity(), h)))
                .collect(Collectors.toList());

        List<Future<ReachabilityResult>> futures = new ArrayList<>();
        try {
            futures = scheduler.invokeAll(tasks);
        } catch (InterruptedException e) {
            return handlers.stream().map(h -> new ReachabilityResult(false, h)).collect(Collectors.toList());
        }

        List<ReachabilityResult> result = new ArrayList<>();
        for (int i = 0; i < handlers.size(); ++i) {
            try {
                result.add(futures.get(i).get(3, TimeUnit.SECONDS));
            } catch (InterruptedException | ExecutionException | java.util.concurrent.TimeoutException e) {
                result.add(new ReachabilityResult(false, handlers.get(i)));
            }
        }
        return result;
    }

    private void attemptReconnect(int reconnectInterval) {
        logger.trace("Attempting to reconnect...");
        this.dispose();
        this.connect();
        if (!thing.getStatus().equals(ThingStatus.ONLINE)) {
            final int newReconnectInterval = Math.min(MAX_RECONNECT_INTERVAL_SECS, reconnectInterval * 2);
            logger.trace("Failed to reconnect. Will try again in {} seconds.", newReconnectInterval);
            connectFuture = scheduler.schedule(() -> this.attemptReconnect(newReconnectInterval), newReconnectInterval,
                    TimeUnit.SECONDS);
        } else {
            logger.trace("Reconnected");
        }
    }

    public void handleTimeout(DeviceHandler handler) {
        logger.trace("Timeout for device {}", handler.getThing().getUID());

        // Make sure only one timeout triggers a heartbeat.
        // Otherwise, all timeouts can spawn a heartbeat, that
        // will give the scheduler a task per device
        // If we are unlucky with the scheduling, all
        // threads start running the heartbeat method, leaving
        // no tasks to run the tasks spawned by a heartbeat
        // This then blocks all thing handling threads forever.
        synchronized(isRequestedHeartbeatRunningLock) {
            if (isRequestedHeartbeatRunning)
                return;
            isRequestedHeartbeatRunning = true;
        }

        if (heartbeatFuture != null)
            Utils.assertNonNull(heartbeatFuture).cancel(false);
        // Replace canceled heartbeat with one, that will run immediately
        heartbeatFuture = scheduler.scheduleWithFixedDelay(this::heartbeat, 0, HEARTBEAT_INTERVAL_SECS,
                TimeUnit.SECONDS);
    }

    private synchronized void startDiscoveryService() {
        if (discoveryService != null) {
            return;
        }
        BrickDaemonDiscoveryService discoveryService = new BrickDaemonDiscoveryService(this);
        this.discoveryService = discoveryService;
        discoveryService.activate();
        registerFn.accept(discoveryService);
    }

    private synchronized void stopDiscoveryService() {
        BrickDaemonDiscoveryService discoveryService = this.discoveryService;
        if (discoveryService != null) {
            discoveryService.deactivate();
            deregisterFn.accept(discoveryService);
            this.discoveryService = null;
        }
    }

    private boolean none(List<ReachabilityResult> lst) {
        return !lst.stream().anyMatch(r -> r.reachable);
    }


    private void heartbeat() {
        if (thing.getStatus().equals(ThingStatus.OFFLINE)) {
            synchronized(isRequestedHeartbeatRunningLock) {
                isRequestedHeartbeatRunning = false;
            }
            return;
        }

        int allPacketsLost = 0;
        List<ReachabilityResult> reachabilityResults = new ArrayList<>();
        while (allPacketsLost < ALL_PACKETS_LOST_THRESHOLD) {
            List<ReachabilityResult> reachable = this.checkReachability(thing -> true);
            reachabilityResults.addAll(reachable);
            // Only assume lost connection if at least one device was checked
            if (none(reachable) && reachable.size() > 0) {
                ++allPacketsLost;
            } else {
                break;
            }
        }

        Map<DeviceHandler, List<ReachabilityResult>> map = reachabilityResults.stream().collect(
                Collectors.groupingBy(r -> r.handler));
        for (Entry<DeviceHandler, List<ReachabilityResult>> entry : map.entrySet()) {
            if (none(entry.getValue())) {
                entry.getKey().reachabilityCheckFailed();
            }
        }

        if (allPacketsLost >= ALL_PACKETS_LOST_THRESHOLD) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.COMMUNICATION_ERROR,
                    "Connection lost. Trying to reconnect.");
            attemptReconnect(FIRST_RECONNECT_INTERVAL_SECS);
        }

        synchronized(isRequestedHeartbeatRunningLock) {
            isRequestedHeartbeatRunning = false;
        }
    }

    private void connect() {
        ipcon.removeDisconnectedListener(disconnectedListener);

        BrickDaemonConfig cfg = getConfigAs(BrickDaemonConfig.class);

        try {
            ipcon.connect(cfg.host, cfg.port);
        } catch (NetworkException e) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.COMMUNICATION_ERROR,
                    "Could not connect: " + e.getLocalizedMessage());
            return;
        } catch (AlreadyConnectedException e) {
            logger.trace("Tried to connect to {}:{} but was already connected.", cfg.host, cfg.port);
        }

        if (cfg.auth) {
            try {
                ipcon.authenticate(cfg.password);
            } catch (TimeoutException e) {
                updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.CONFIGURATION_ERROR, "Could not authenticate (maybe the password was wrong?): " + e.getLocalizedMessage());
                return;
            } catch (TinkerforgeException e) {
                updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.COMMUNICATION_ERROR, "Could not authenticate: " + e.getLocalizedMessage());
                return;
            }
        }

        ipcon.addDisconnectedListener(disconnectedListener);

        this.startDiscoveryService();

        heartbeatFuture = scheduler.scheduleWithFixedDelay(this::heartbeat, FIRST_HEARTBEAT_INTERVAL_SECS,
                HEARTBEAT_INTERVAL_SECS, TimeUnit.SECONDS);

        updateStatus(ThingStatus.ONLINE);
    }

    @Override
    public void initialize() {
        // The framework requires you to return from this method quickly. Also, before
        // leaving this method a thing
        // status from one of ONLINE, OFFLINE or UNKNOWN must be set. This might already
        // be the real thing status in
        // case you can decide it directly.
        // In case you can not decide the thing status directly (e.g. for long running
        // connection handshake using WAN
        // access or similar) you should set status UNKNOWN here and then decide the
        // real status asynchronously in the
        // background.

        // set the thing status to UNKNOWN temporarily and let the background task
        // decide for the real status.
        // the framework is then able to reuse the resources from the thing handler
        // initialization.
        // we set this upfront to reliably check status updates in unit tests.
        updateStatus(ThingStatus.UNKNOWN);
        connectFuture = scheduler.schedule(() -> this.attemptReconnect(FIRST_RECONNECT_INTERVAL_SECS), 0,
                TimeUnit.SECONDS);
    }

    public void enumerate() throws NotConnectedException {
        try {
            ipcon.enumerate();
        } catch (NotConnectedException e) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.COMMUNICATION_ERROR,
                    "Could not enumerate: Not connected.");
        }
    }

    public void addEnumerateListener(EnumerateListener listener) {
        ipcon.addEnumerateListener(listener);
    }

    public void removeEnumerateListener(EnumerateListener listener) {
        ipcon.removeEnumerateListener(listener);
    }

    @Override
    public void handleRemoval() {
        this.dispose();
        super.handleRemoval();
    }

    @Override
    public void dispose() {
        try {
            if (connectFuture != null)
                Utils.assertNonNull(connectFuture).cancel(false);
            if (heartbeatFuture != null)
                Utils.assertNonNull(heartbeatFuture).cancel(false);
            ipcon.removeDisconnectedListener(disconnectedListener);
            this.stopDiscoveryService();
            ipcon.disconnect();
        } catch (NotConnectedException e) {
        }
    }

    @Override
    public void childHandlerInitialized(ThingHandler childHandler, Thing childThing) {
        super.childHandlerInitialized(childHandler, childThing);
        childHandlers.put(childThing.getUID().getId(), childHandler);
    }

    @Override
    public void childHandlerDisposed(ThingHandler childHandler, Thing childThing) {
        super.childHandlerDisposed(childHandler, childThing);
        childHandlers.remove(childThing.getUID().getId());
    }

    public @Nullable ThingHandler getChildHandler(String uid) {
        return childHandlers.get(uid);
    }
}
