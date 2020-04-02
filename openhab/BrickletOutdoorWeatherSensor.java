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
package org.eclipse.smarthome.binding.tinkerforge.internal.device;

import java.math.BigDecimal;
import java.net.URI;
import java.time.ZonedDateTime;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.function.BiConsumer;
import java.util.function.Consumer;
import java.util.function.Function;

import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.jdt.annotation.Nullable;
import org.eclipse.smarthome.binding.tinkerforge.internal.TinkerforgeBindingConstants;
import org.eclipse.smarthome.config.core.ConfigDescription;
import org.eclipse.smarthome.config.core.ConfigDescriptionBuilder;
import org.eclipse.smarthome.config.core.ConfigDescriptionParameter.Type;
import org.eclipse.smarthome.config.core.ConfigDescriptionParameterBuilder;
import org.eclipse.smarthome.config.core.Configuration;
import org.eclipse.smarthome.core.library.types.DateTimeType;
import org.eclipse.smarthome.core.library.types.QuantityType;
import org.eclipse.smarthome.core.library.unit.SIUnits;
import org.eclipse.smarthome.core.library.unit.SmartHomeUnits;
import org.eclipse.smarthome.core.thing.ThingTypeUID;
import org.eclipse.smarthome.core.thing.binding.BaseThingHandler;
import org.eclipse.smarthome.core.thing.type.ChannelDefinitionBuilder;
import org.eclipse.smarthome.core.thing.type.ChannelType;
import org.eclipse.smarthome.core.thing.type.ChannelTypeBuilder;
import org.eclipse.smarthome.core.thing.type.ChannelTypeUID;
import org.eclipse.smarthome.core.thing.type.ThingType;
import org.eclipse.smarthome.core.thing.type.ThingTypeBuilder;
import org.eclipse.smarthome.core.types.Command;
import org.eclipse.smarthome.core.types.State;
import org.eclipse.smarthome.core.types.StateDescriptionFragmentBuilder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.tinkerforge.BrickletOutdoorWeather.SensorData;
import com.tinkerforge.BrickletOutdoorWeather.SensorDataListener;
import com.tinkerforge.Device.Identity;
import com.tinkerforge.TinkerforgeException;

/**
 * Fake device modelling an outdoor weather sensor.
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
public class BrickletOutdoorWeatherSensor implements DeviceWrapper {
    public BrickletOutdoorWeatherSensor(BrickletOutdoorWeatherWrapper bricklet) {
        this.bricklet = bricklet;
    }

    private List<ScheduledFuture<?>> manualChannelUpdates = new ArrayList<>();
    private List<ListenerReg<?>> listenerRegs = new ArrayList<>();

    public void cancelManualUpdates() {
        manualChannelUpdates.forEach(f -> f.cancel(true));
    }

    public <T> T reg(T listener, Consumer<T> toRemove) {
        listenerRegs.add(new ListenerReg<T>(listener, toRemove));
        return listener;
    }

    @Override
    public void dispose(Configuration config) throws TinkerforgeException {
        listenerRegs.forEach(ListenerReg::deregister);
    }

    private final BrickletOutdoorWeatherWrapper bricklet;
    public @Nullable SensorDataListener listener = null;

    public static final int DEVICE_IDENTIFIER = -288;
    public static final String DEVICE_DISPLAY_NAME = "Outdoor Weather Sensor";

    public static final DeviceInfo DEVICE_INFO = new DeviceInfo(DEVICE_DISPLAY_NAME, "outdoorweathersensor",
            DEVICE_IDENTIFIER, BrickletOutdoorWeatherSensor.class, DefaultActions.class, "1.0.0", false);

    private final Logger logger = LoggerFactory.getLogger(BrickletOutdoorWeatherSensor.class);
    private static final Logger static_logger = LoggerFactory.getLogger(BrickletOutdoorWeatherSensor.class);

    public void initialize(Configuration config, Function<String, Configuration> getChannelConfigFn,
            BiConsumer<String, State> updateStateFn, BiConsumer<String, String> triggerChannelFn,
            ScheduledExecutorService scheduler, BaseThingHandler handler) {
        BrickletOutdoorWeatherSensorConfig cfg = (BrickletOutdoorWeatherSensorConfig) config
                .as(BrickletOutdoorWeatherSensorConfig.class);
        listener = (int identifier, int temperature, int humidity) -> {
            if (identifier != cfg.sensorID)
                return;
            updateStateFn.accept("OutdoorWeatherSensorTemperature", new QuantityType<>(temperature / 10.0,
                    SIUnits.CELSIUS));
            updateStateFn.accept("OutdoorWeatherSensorHumidity", new QuantityType<>(humidity, SmartHomeUnits.PERCENT));
            updateStateFn.accept("OutdoorWeatherSensorLastChange", new DateTimeType(getAbsoluteTime(0)));
        };
        bricklet.addSensorDataListener(listener);
    }

    public List<String> getEnabledChannels(org.eclipse.smarthome.config.core.Configuration config)
            throws TinkerforgeException {
        return Arrays.asList("OutdoorWeatherSensorTemperature", "OutdoorWeatherSensorHumidity",
                "OutdoorWeatherSensorLastChange");
    }

    public static @Nullable ChannelType getChannelType(ChannelTypeUID channelTypeUID) {
        switch (channelTypeUID.getId()) {
            case "OutdoorWeatherSensorTemperature":
                return ChannelTypeBuilder
                        .state(new ChannelTypeUID("tinkerforge", "OutdoorWeatherSensorTemperature"), "Temperature",
                                "Number:Temperature")
                        .withConfigDescriptionURI(
                                URI.create("channel-type:tinkerforge:OutdoorWeatherSensorTemperature"))
                        .withDescription("Last received temperature")
                        .withStateDescription(
                                StateDescriptionFragmentBuilder.create().withPattern("%.1f %unit%").withReadOnly(true)
                                        .build().toStateDescription()).build();
            case "OutdoorWeatherSensorHumidity":
                return ChannelTypeBuilder
                        .state(new ChannelTypeUID("tinkerforge", "OutdoorWeatherSensorHumidity"), "Humidity",
                                "Number:Dimensionless")
                        .withConfigDescriptionURI(URI.create("channel-type:tinkerforge:OutdoorWeatherSensorHumidity"))
                        .withDescription("Last received humidity")
                        .withStateDescription(
                                StateDescriptionFragmentBuilder.create().withPattern("%d %%").withReadOnly(true)
                                        .build().toStateDescription()).build();
            case "OutdoorWeatherSensorLastChange":
                return ChannelTypeBuilder
                        .state(new ChannelTypeUID("tinkerforge", "OutdoorWeatherSensorLastChange"), "Last Change",
                                "DateTime")
                        .withConfigDescriptionURI(URI.create("channel-type:tinkerforge:OutdoorWeatherSensorLastChange"))
                        .withDescription(
                                "Time when the last data was received from the sensor. The sensor sends data every 45 to 60 seconds.")
                        .withStateDescription(
                                StateDescriptionFragmentBuilder.create().withReadOnly(true).build()
                                        .toStateDescription()).build();
            default:
                static_logger.debug("Unknown channel type ID {}", channelTypeUID.getId());
                break;
        }

        return null;
    }

    public static ThingType getThingType(ThingTypeUID thingTypeUID) {
        return ThingTypeBuilder
                .instance(thingTypeUID, "Tinkerforge Outdoor Weather Temperature/Humidity Sensor TH-6148 ")
                .isListed(true)
                .withSupportedBridgeTypeUIDs(
                        Arrays.asList(TinkerforgeBindingConstants.THING_TYPE_BRICKLET_OUTDOOR_WEATHER.toString()))
                .withConfigDescriptionURI(URI.create("thing-type:tinkerforge:" + thingTypeUID.getId()))
                .withDescription("Weather sensor connected to an Outdoor Weather Bricklet")
                .withChannelDefinitions(
                        Arrays.asList(
                                new ChannelDefinitionBuilder("OutdoorWeatherSensorTemperature", new ChannelTypeUID(
                                        "tinkerforge", "OutdoorWeatherSensorTemperature")).withLabel("Temperature")
                                        .build(),
                                new ChannelDefinitionBuilder("OutdoorWeatherSensorHumidity", new ChannelTypeUID(
                                        "tinkerforge", "OutdoorWeatherSensorHumidity")).withLabel("Humidity").build(),
                                new ChannelDefinitionBuilder("OutdoorWeatherSensorLastChange", new ChannelTypeUID(
                                        "tinkerforge", "OutdoorWeatherSensorLastChange")).withLabel("Last Change")
                                        .build())).build();
    }

    public static @Nullable ConfigDescription getConfigDescription(URI uri) {
        switch (uri.toASCIIString()) {
            case "thing-type:tinkerforge:outdoorweathersensor":
                return ConfigDescriptionBuilder
                        .create(uri)
                        .withParameters(
                                Arrays.asList(ConfigDescriptionParameterBuilder
                                        .create("sensorID", Type.INTEGER)
                                        .withDefault("0")
                                        .withDescription(
                                                "The ID of the sensor to query. Each sensor gives itself a random identifier on startup. The Outdoor Weather Bricklet reports available IDs.")
                                        .withMinimum(BigDecimal.valueOf(0)).withMaximum(BigDecimal.valueOf(255))
                                        .build())).build();
            case "channel-type:tinkerforge:OutdoorWeatherSensorTemperature":
            case "channel-type:tinkerforge:OutdoorWeatherSensorHumidity":
            case "channel-type:tinkerforge:OutdoorWeatherSensorLastChange":
                return ConfigDescriptionBuilder.create(uri).build();
            default:
                static_logger.debug("Unknown config description URI {}", uri.toASCIIString());
                break;
        }
        return null;
    }

    public void refreshValue(String value, org.eclipse.smarthome.config.core.Configuration config,
            org.eclipse.smarthome.config.core.Configuration channelConfig,
            BiConsumer<String, org.eclipse.smarthome.core.types.State> updateStateFn,
            BiConsumer<String, String> triggerChannelFn) throws TinkerforgeException {
        BrickletOutdoorWeatherSensorConfig cfg = (BrickletOutdoorWeatherSensorConfig) config
                .as(BrickletOutdoorWeatherSensorConfig.class);
        switch (value) {
            case "OutdoorWeatherSensorTemperature":
                updateStateFn.accept(value,
                        transformOutdoorWeatherTemperatureGetter0(bricklet.getSensorData(cfg.sensorID)));
                break;
            case "OutdoorWeatherSensorHumidity":
                updateStateFn.accept(value,
                        transformOutdoorWeatherHumidityGetter0(bricklet.getSensorData(cfg.sensorID)));
                break;
            case "OutdoorWeatherSensorLastChange":
                updateStateFn.accept(value,
                        transformOutdoorWeatherLastChangeGetter0(bricklet.getSensorData(cfg.sensorID)));
                break;
            default:
                logger.warn("Refresh for unknown channel {}", value);
                break;
        }
    }

    public ZonedDateTime getAbsoluteTime(int offset) {
        return ZonedDateTime.now().minusSeconds(offset);
    }

    public List<SetterRefresh> handleCommand(org.eclipse.smarthome.config.core.Configuration config,
            org.eclipse.smarthome.config.core.Configuration channelConfig, String channel, Command command)
            throws TinkerforgeException {
        List<SetterRefresh> result = Collections.emptyList();
        switch (channel) {
            default:
                logger.warn("Command for unknown channel {}", channel);
        }
        return result;
    }

    private org.eclipse.smarthome.core.types.State transformOutdoorWeatherTemperatureGetter0(SensorData value) {
        return new QuantityType<>(value.temperature / 10.0, SIUnits.CELSIUS);
    }

    private org.eclipse.smarthome.core.types.State transformOutdoorWeatherHumidityGetter0(SensorData value) {
        return new QuantityType<>(value.humidity, SmartHomeUnits.PERCENT);
    }

    private org.eclipse.smarthome.core.types.State transformOutdoorWeatherLastChangeGetter0(SensorData value) {
        return new DateTimeType(getAbsoluteTime(value.lastChange));
    }

    @Override
    public Identity getIdentity() throws TinkerforgeException {
        return new Identity();
    }
}
