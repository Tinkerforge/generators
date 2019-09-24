package org.eclipse.smarthome.binding.tinkerforge.discovery;

import java.util.HashSet;
import java.util.Set;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;

import org.eclipse.smarthome.binding.tinkerforge.internal.handler.BrickletOutdoorWeatherHandler;
import org.eclipse.smarthome.binding.tinkerforge.internal.TinkerforgeBindingConstants;
import org.eclipse.smarthome.config.discovery.AbstractDiscoveryService;
import org.eclipse.smarthome.config.discovery.DiscoveryResultBuilder;
import org.eclipse.smarthome.core.thing.ThingTypeUID;
import org.eclipse.smarthome.core.thing.ThingUID;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.tinkerforge.IPConnection.EnumerateListener;
import com.tinkerforge.BrickletOutdoorWeather;
import com.tinkerforge.TinkerforgeException;

public class OutdoorWeatherDiscoveryService extends AbstractDiscoveryService implements TinkerforgeDiscoveryService{
    BrickletOutdoorWeather device;
    BrickletOutdoorWeatherHandler handler;
    EnumerateListener listener;
    ScheduledFuture<?> job = null;
    private final Logger logger = LoggerFactory.getLogger(OutdoorWeatherDiscoveryService.class);

    public OutdoorWeatherDiscoveryService(BrickletOutdoorWeatherHandler handler) {
        super(getSupportedDevices(), 10, true);
        this.handler = handler;
        this.device = handler.getDevice();
    }

    public static Set<ThingTypeUID> getSupportedDevices() {
        HashSet<ThingTypeUID> set = new HashSet<>();
        //set.add(TinkerforgeBindingConstants.THING_TYPE_OUTDOOR_WEATHER_SENSOR);
        set.add(TinkerforgeBindingConstants.THING_TYPE_OUTDOOR_WEATHER_STATION);
        return set;
    }

    public void activate() {
        startBackgroundDiscovery();
    }

    private void discover() {
        int[] newSensorIDs;
        int[] newStationIDs;
        try {
            newSensorIDs = this.device.getSensorIdentifiers();
            newStationIDs = this.device.getStationIdentifiers();
        } catch (TinkerforgeException e) {
            return;
        }

        for(int sensorId : newSensorIDs) {
            ThingTypeUID ttuid = TinkerforgeBindingConstants.THING_TYPE_OUTDOOR_WEATHER_SENSOR;
            ThingUID thingUid = new ThingUID(ttuid, handler.getThing().getUID(), String.valueOf(sensorId));
            thingDiscovered(DiscoveryResultBuilder.create(thingUid)
                                                  .withThingType(ttuid)
                                                  .withLabel("Sensor " + String.valueOf(sensorId))
                                                  .withBridge(handler.getThing().getUID())
                                                  .build());
        }

        for(int sensorId : newStationIDs) {
            ThingTypeUID ttuid = TinkerforgeBindingConstants.THING_TYPE_OUTDOOR_WEATHER_STATION;
            ThingUID thingUid = new ThingUID(ttuid, handler.getThing().getUID(), String.valueOf(sensorId));
            thingDiscovered(DiscoveryResultBuilder.create(thingUid)
                                                  .withThingType(ttuid)
                                                  .withLabel("Station " + String.valueOf(sensorId))
                                                  .withBridge(handler.getThing().getUID())
                                                  .build());
        }
    }

    @Override
    protected void startBackgroundDiscovery() {
        logger.debug("Start Tinkerforge outdoor weather device background discovery for outdoor weather bricklet %s", handler.getThing().getUID());
        if (job == null || job.isCancelled()) {
            job = scheduler.scheduleWithFixedDelay(this::discover, 2500, 60 * 1000, TimeUnit.MILLISECONDS);
        }
    }

    @Override
    protected void stopBackgroundDiscovery() {
        logger.debug(
                "Stop Tinkerforge outdoor weather device background discovery for outdoor weather bricklet %s", this.handler.getThing().getUID());
        if (job != null && !job.isCancelled()) {
            job.cancel(true);
            job = null;
        }
    }

    @Override
    protected void startScan() {
        this.discover();
    }

    @Override
    public Set<ThingTypeUID> getSupportedThingTypes() {
        return new HashSet<ThingTypeUID>(TinkerforgeBindingConstants.SUPPORTED_DEVICES);
    }

    @Override
    public void stopDiscovery() {
        stopBackgroundDiscovery();
    }
}
