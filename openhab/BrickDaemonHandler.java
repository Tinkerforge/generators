package org.eclipse.smarthome.binding.tinkerforge.internal.handler;

import org.eclipse.jdt.annotation.NonNull;
import org.eclipse.jdt.annotation.Nullable;
import org.eclipse.smarthome.binding.tinkerforge.discovery.BrickDaemonDiscoveryService;
import org.eclipse.smarthome.core.thing.Bridge;
import org.eclipse.smarthome.core.thing.ChannelUID;
import org.eclipse.smarthome.core.thing.Thing;
import org.eclipse.smarthome.core.thing.ThingStatus;
import org.eclipse.smarthome.core.thing.ThingStatusDetail;
import org.eclipse.smarthome.core.thing.binding.BaseBridgeHandler;
import org.eclipse.smarthome.core.thing.binding.ThingHandler;
import org.eclipse.smarthome.core.types.Command;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

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

import com.tinkerforge.AlreadyConnectedException;
import org.eclipse.smarthome.binding.tinkerforge.internal.device.BrickDaemonConfig;
import com.tinkerforge.IPConnection;
import com.tinkerforge.IPConnection.DisconnectedListener;
import com.tinkerforge.IPConnection.EnumerateListener;
import com.tinkerforge.NetworkException;
import com.tinkerforge.NotConnectedException;
import com.tinkerforge.TimeoutException;
import com.tinkerforge.TinkerforgeException;

public class BrickDaemonHandler extends BaseBridgeHandler {
    public IPConnection ipcon;
    private Consumer<BrickDaemonDiscoveryService> registerFn;
    private Consumer<BrickDaemonDiscoveryService> deregisterFn;
    private BrickDaemonDiscoveryService discoveryService;
    @Nullable
    private ScheduledFuture<?> connectFuture;
    private ScheduledFuture<?> heartbeatFuture;
    private DisconnectedListener disconnectedListener;

    private final Logger logger = LoggerFactory.getLogger(BrickDaemonHandler.class);
    private final int FIRST_RECONNECT_INTERVAL_SECS = 10;
    private final int MAX_RECONNECT_INTERVAL_SECS = 600;

    private final int FIRST_HEARTBEAT_INTERVAL_SECS = 10;
    private final int HEARTBEAT_INTERVAL_SECS = 90;

    private final int ALL_PACKETS_LOST_THRESHOLD = 5;
    private final Map<String, ThingHandler> childHandlers = new ConcurrentHashMap<>();

    public BrickDaemonHandler(Bridge bridge, Consumer<BrickDaemonDiscoveryService> registerFn,
            Consumer<BrickDaemonDiscoveryService> deregisterFn) {
        super(bridge);
        this.registerFn = registerFn;
        this.deregisterFn = deregisterFn;
        ipcon = new IPConnection();
        // attemptReconnect implements a custom auto reconnect mechanism
        ipcon.setAutoReconnect(false);
    }

    @Override
    public void handleCommand(@NonNull ChannelUID channelUID, @NonNull Command command) {

    }

    private class ReachabilityResult {
        Boolean reachable;
        DeviceHandler handler;
        ReachabilityResult(Boolean reachable, DeviceHandler handler) {
            this.reachable = reachable;
            this.handler = handler;
        }
    }

    private List<ReachabilityResult> checkReachability(Predicate<? super Thing> filter) {
        List<DeviceHandler> handlers = getThing().getThings()
                                                 .stream()
                                                 .filter(filter)
                                                 .map(t -> (DeviceHandler) t.getHandler())
                                                 .filter(h -> h != null) // If checkReachability is called fast enough, some things don't have a handler yet.
                                                 .collect(Collectors.toList());
        List<Callable<ReachabilityResult>> tasks = handlers.stream().map(h -> (Callable<ReachabilityResult>)(() -> new ReachabilityResult(h.checkReachablity(), h))).collect(Collectors.toList());

        List<Future<ReachabilityResult>> futures = new ArrayList<>();
        try {
            futures = scheduler.invokeAll(tasks);
        } catch (InterruptedException e) {
            return handlers.stream().map(h -> new ReachabilityResult(false, h)).collect(Collectors.toList());
        }

        List<ReachabilityResult> result = new ArrayList<>();
        for(int i = 0; i < handlers.size(); ++i){
            try {
                result.add(futures.get(i).get());
            } catch (InterruptedException | ExecutionException e) {
                result.add(new ReachabilityResult(false, handlers.get(i)));
            }
        }
        return result;
    }

    private void attemptReconnect(int reconnectInterval) {
        logger.trace("Attempting to reconnect...");
        this.dispose();
        this.connect();
        if(!thing.getStatus().equals(ThingStatus.ONLINE))
        {
            final int newReconnectInterval = Math.min(MAX_RECONNECT_INTERVAL_SECS, reconnectInterval * 2);
            logger.trace("Failed to reconnect. Will try again in {} seconds.", newReconnectInterval);
            connectFuture = scheduler.schedule(() -> this.attemptReconnect(newReconnectInterval), newReconnectInterval, TimeUnit.SECONDS);
        } else {
            logger.trace("Reconnected");
        }
    }

    public void handleTimeout(DeviceHandler handler) {
        logger.trace("Timeout for device {}", handler.getThing().getUID());
        if(heartbeatFuture != null)
            heartbeatFuture.cancel(false);
        // Replace canceled heartbeat with one, that will run immediately
        heartbeatFuture = scheduler.scheduleWithFixedDelay(this::heartbeat, 0, HEARTBEAT_INTERVAL_SECS, TimeUnit.SECONDS);
    }

    private synchronized void startDiscoveryService() {
        if (discoveryService != null) {
            return;
        }
        discoveryService = new BrickDaemonDiscoveryService(this);
        discoveryService.activate();
        registerFn.accept(discoveryService);
    }

    private synchronized void stopDiscoveryService() {
        if (discoveryService != null) {
            discoveryService.deactivate();
            deregisterFn.accept(discoveryService);
            discoveryService = null;
        }
    }

    private boolean none(List<ReachabilityResult> lst) {
        return !lst.stream().anyMatch(r -> r.reachable);
    }

    private void heartbeat() {
        if(thing.getStatus().equals(ThingStatus.OFFLINE))
            return;

        int allPacketsLost = 0;
        List<ReachabilityResult> reachabilityResults = new ArrayList<>();
        while(allPacketsLost < ALL_PACKETS_LOST_THRESHOLD) {
            List<ReachabilityResult> reachable = this.checkReachability(thing -> true);
            reachabilityResults.addAll(reachable);
            //Only assume lost connection if there are devices that can have been checked
            if(none(reachable) && reachable.size() > 0) {
                ++allPacketsLost;
            } else {
                break;
            }
        }

        Map<DeviceHandler, List<ReachabilityResult>> map = reachabilityResults.stream().collect(Collectors.groupingBy(r -> r.handler));
        for(Entry<DeviceHandler, List<ReachabilityResult>> entry : map.entrySet()) {
            if (none(entry.getValue())) {
                entry.getKey().reachabilityCheckFailed();
            }
        }

        if (allPacketsLost >= ALL_PACKETS_LOST_THRESHOLD) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.COMMUNICATION_ERROR,
                        "Connection lost. Trying to reconnect.");
            attemptReconnect(FIRST_RECONNECT_INTERVAL_SECS);
        }
    }

    private void connect() {
        if(disconnectedListener != null)
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
            } catch (TinkerforgeException e) {
                if (e instanceof TimeoutException) {
                    updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.CONFIGURATION_ERROR,
                                "Could not authenticate (maybe the password was wrong?): " + e.getLocalizedMessage());
                }
                else {
                    updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.COMMUNICATION_ERROR,
                                "Could not authenticate: " + e.getLocalizedMessage());
                }
                return;
            }
        }

        disconnectedListener = reason -> {
            updateStatus(ThingStatus.OFFLINE);
            this.stopDiscoveryService();
            attemptReconnect(FIRST_RECONNECT_INTERVAL_SECS);
        };

        ipcon.addDisconnectedListener(disconnectedListener);

        this.startDiscoveryService();

        heartbeatFuture = scheduler.scheduleWithFixedDelay(this::heartbeat, FIRST_HEARTBEAT_INTERVAL_SECS, HEARTBEAT_INTERVAL_SECS, TimeUnit.SECONDS);

        updateStatus(ThingStatus.ONLINE);
    }

    @Override
    public void initialize() {
        // The framework requires you to return from this method quickly. Also, before leaving this method a thing
        // status from one of ONLINE, OFFLINE or UNKNOWN must be set. This might already be the real thing status in
        // case you can decide it directly.
        // In case you can not decide the thing status directly (e.g. for long running connection handshake using WAN
        // access or similar) you should set status UNKNOWN here and then decide the real status asynchronously in the
        // background.

        // set the thing status to UNKNOWN temporarily and let the background task decide for the real status.
        // the framework is then able to reuse the resources from the thing handler initialization.
        // we set this upfront to reliably check status updates in unit tests.
        updateStatus(ThingStatus.UNKNOWN);
        connectFuture = scheduler.schedule(() -> this.attemptReconnect(FIRST_RECONNECT_INTERVAL_SECS), 0, TimeUnit.SECONDS);
    }

    public void enumerate() throws NotConnectedException {
        try {
            ipcon.enumerate();
        }
        catch (NotConnectedException e) {
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
                connectFuture.cancel(false);
            if (heartbeatFuture != null)
                heartbeatFuture.cancel(false);
            if (disconnectedListener != null)
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

    public ThingHandler getChildHandler(String uid) {
        return childHandlers.getOrDefault(uid, null);
    }
}
