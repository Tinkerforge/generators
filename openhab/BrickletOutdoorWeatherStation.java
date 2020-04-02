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
import org.eclipse.smarthome.core.library.types.OnOffType;
import org.eclipse.smarthome.core.library.types.QuantityType;
import org.eclipse.smarthome.core.library.types.StringType;
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

import com.tinkerforge.BrickletOutdoorWeather.StationData;
import com.tinkerforge.BrickletOutdoorWeather.StationDataListener;
import com.tinkerforge.Device.Identity;
import com.tinkerforge.TinkerforgeException;

/**
 * Fake device modelling an outdoor weather station.
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
public class BrickletOutdoorWeatherStation implements DeviceWrapper {
    public BrickletOutdoorWeatherStation(BrickletOutdoorWeatherWrapper bricklet) {
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
    public @Nullable StationDataListener listener = null;

    public static final int DEVICE_IDENTIFIER = -288;
    public static final String DEVICE_DISPLAY_NAME = "Outdoor Weather Station";

    public static final DeviceInfo DEVICE_INFO = new DeviceInfo(DEVICE_DISPLAY_NAME, "outdoorweatherstation",
            DEVICE_IDENTIFIER, BrickletOutdoorWeatherStation.class, DefaultActions.class, "1.0.0", false);

    private final Logger logger = LoggerFactory.getLogger(BrickletOutdoorWeatherStation.class);
    private static final Logger static_logger = LoggerFactory.getLogger(BrickletOutdoorWeatherStation.class);

    public void initialize(Configuration config, Function<String, Configuration> getChannelConfigFn,
            BiConsumer<String, State> updateStateFn, BiConsumer<String, String> triggerChannelFn,
            ScheduledExecutorService scheduler, BaseThingHandler handler) {
        BrickletOutdoorWeatherStationConfig cfg = (BrickletOutdoorWeatherStationConfig) config
                .as(BrickletOutdoorWeatherStationConfig.class);
        listener = (int identifier, int temperature, int humidity, long windSpeed, long gustSpeed, long rain,
                int windDirection, boolean batteryLow) -> {
            if (identifier != cfg.stationID)
                return;
            updateStateFn.accept("OutdoorWeatherStationTemperature", new QuantityType<>(temperature / 10.0,
                    SIUnits.CELSIUS));
            updateStateFn.accept("OutdoorWeatherStationHumidity", new QuantityType<>(humidity, SmartHomeUnits.PERCENT));
            updateStateFn.accept("OutdoorWeatherStationWindSpeed", new QuantityType<>(windSpeed / 10.0,
                    SmartHomeUnits.METRE_PER_SECOND));
            updateStateFn.accept("OutdoorWeatherStationGustSpeed", new QuantityType<>(gustSpeed / 10.0,
                    SmartHomeUnits.METRE_PER_SECOND));
            updateStateFn.accept("OutdoorWeatherStationRainFall", new QuantityType<>(rain / 10000.0, SIUnits.METRE));
            updateStateFn.accept("OutdoorWeatherStationWindDirection", new StringType(
                    getWindDirectionName(windDirection)));
            updateStateFn.accept("OutdoorWeatherStationBatteryLow", batteryLow ? OnOffType.ON : OnOffType.OFF);
            updateStateFn.accept("OutdoorWeatherStationLastChange", new DateTimeType(getAbsoluteTime(0)));
        };
        bricklet.addStationDataListener(listener);
    }

    public List<String> getEnabledChannels(org.eclipse.smarthome.config.core.Configuration config)
            throws TinkerforgeException {
        return Arrays.asList("OutdoorWeatherStationTemperature", "OutdoorWeatherStationHumidity",
                "OutdoorWeatherStationWindSpeed", "OutdoorWeatherStationGustSpeed", "OutdoorWeatherStationRainFall",
                "OutdoorWeatherStationWindDirection", "OutdoorWeatherStationBatteryLow",
                "OutdoorWeatherStationLastChange");
    }

    public static @Nullable ChannelType getChannelType(ChannelTypeUID channelTypeUID) {
        switch (channelTypeUID.getId()) {
            case "OutdoorWeatherStationTemperature":
                return ChannelTypeBuilder
                        .state(new ChannelTypeUID("tinkerforge", "OutdoorWeatherStationTemperature"), "Temperature",
                                "Number:Temperature")
                        .withConfigDescriptionURI(
                                URI.create("channel-type:tinkerforge:OutdoorWeatherStationTemperature"))
                        .withDescription("Last received temperature")
                        .withStateDescription(
                                StateDescriptionFragmentBuilder.create().withPattern("%.1f %unit%").withReadOnly(true)
                                        .build().toStateDescription()).build();
            case "OutdoorWeatherStationHumidity":
                return ChannelTypeBuilder
                        .state(new ChannelTypeUID("tinkerforge", "OutdoorWeatherStationHumidity"), "Humidity",
                                "Number:Dimensionless")
                        .withConfigDescriptionURI(URI.create("channel-type:tinkerforge:OutdoorWeatherStationHumidity"))
                        .withDescription("Last received humidity")
                        .withStateDescription(
                                StateDescriptionFragmentBuilder.create().withPattern("%d %%").withReadOnly(true)
                                        .build().toStateDescription()).build();
            case "OutdoorWeatherStationWindSpeed":
                return ChannelTypeBuilder
                        .state(new ChannelTypeUID("tinkerforge", "OutdoorWeatherStationWindSpeed"), "Wind Speed",
                                "Number:Speed")
                        .withConfigDescriptionURI(URI.create("channel-type:tinkerforge:OutdoorWeatherStationWindSpeed"))
                        .withDescription("Last received wind speed")
                        .withStateDescription(
                                StateDescriptionFragmentBuilder.create().withPattern("%.1f %unit%").withReadOnly(true)
                                        .build().toStateDescription()).build();
            case "OutdoorWeatherStationGustSpeed":
                return ChannelTypeBuilder
                        .state(new ChannelTypeUID("tinkerforge", "OutdoorWeatherStationGustSpeed"), "Gust Speed",
                                "Number:Speed")
                        .withConfigDescriptionURI(URI.create("channel-type:tinkerforge:OutdoorWeatherStationGustSpeed"))
                        .withDescription("Last received gust speed")
                        .withStateDescription(
                                StateDescriptionFragmentBuilder.create().withPattern("%.1f %unit%").withReadOnly(true)
                                        .build().toStateDescription()).build();
            case "OutdoorWeatherStationRainFall":
                return ChannelTypeBuilder
                        .state(new ChannelTypeUID("tinkerforge", "OutdoorWeatherStationRainFall"), "Rain Fall",
                                "Number:Length")
                        .withConfigDescriptionURI(URI.create("channel-type:tinkerforge:OutdoorWeatherStationRainFall"))
                        .withDescription("Last received rain fall.")
                        .withStateDescription(
                                StateDescriptionFragmentBuilder.create().withPattern("%.4f %unit%").withReadOnly(true)
                                        .build().toStateDescription()).build();
            case "OutdoorWeatherStationWindDirection":
                return ChannelTypeBuilder
                        .state(new ChannelTypeUID("tinkerforge", "OutdoorWeatherStationWindDirection"),
                                "Wind Direction", "String")
                        .withConfigDescriptionURI(
                                URI.create("channel-type:tinkerforge:OutdoorWeatherStationWindDirection"))
                        .withDescription("Last received wind direction")
                        .withStateDescription(
                                StateDescriptionFragmentBuilder.create().withReadOnly(true).build()
                                        .toStateDescription()).build();
            case "OutdoorWeatherStationBatteryLow":
                return ChannelTypeBuilder
                        .state(new ChannelTypeUID("tinkerforge", "OutdoorWeatherStationBatteryLow"), "Battery Low",
                                "Switch")
                        .withConfigDescriptionURI(
                                URI.create("channel-type:tinkerforge:OutdoorWeatherStationBatteryLow"))
                        .withDescription("Enabled if battery is low.")
                        .withStateDescription(
                                StateDescriptionFragmentBuilder.create().withReadOnly(true).build()
                                        .toStateDescription()).build();
            case "OutdoorWeatherStationLastChange":
                return ChannelTypeBuilder
                        .state(new ChannelTypeUID("tinkerforge", "OutdoorWeatherStationLastChange"), "Last Change",
                                "DateTime")
                        .withConfigDescriptionURI(
                                URI.create("channel-type:tinkerforge:OutdoorWeatherStationLastChange"))
                        .withDescription(
                                "Time when the last data was received from the station. The station sends data every 45 to 60 seconds.")
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
                .instance(thingTypeUID, "Tinkerforge Outdoor Weather Station WS-6147.")
                .isListed(true)
                .withSupportedBridgeTypeUIDs(
                        Arrays.asList(TinkerforgeBindingConstants.THING_TYPE_BRICKLET_OUTDOOR_WEATHER.toString()))
                .withConfigDescriptionURI(URI.create("thing-type:tinkerforge:" + thingTypeUID.getId()))
                .withDescription("Weather Station connected to an Outdoor Weather Bricklet")
                .withChannelDefinitions(
                        Arrays.asList(
                                new ChannelDefinitionBuilder("OutdoorWeatherStationTemperature", new ChannelTypeUID(
                                        "tinkerforge", "OutdoorWeatherStationTemperature")).withLabel("Temperature")
                                        .build(),
                                new ChannelDefinitionBuilder("OutdoorWeatherStationHumidity", new ChannelTypeUID(
                                        "tinkerforge", "OutdoorWeatherStationHumidity")).withLabel("Humidity").build(),
                                new ChannelDefinitionBuilder("OutdoorWeatherStationWindSpeed", new ChannelTypeUID(
                                        "tinkerforge", "OutdoorWeatherStationWindSpeed")).withLabel("Wind Speed")
                                        .build(),
                                new ChannelDefinitionBuilder("OutdoorWeatherStationGustSpeed", new ChannelTypeUID(
                                        "tinkerforge", "OutdoorWeatherStationGustSpeed")).withLabel("Gust Speed")
                                        .build(),
                                new ChannelDefinitionBuilder("OutdoorWeatherStationRainFall", new ChannelTypeUID(
                                        "tinkerforge", "OutdoorWeatherStationRainFall")).withLabel("Rain Fall").build(),
                                new ChannelDefinitionBuilder("OutdoorWeatherStationWindDirection", new ChannelTypeUID(
                                        "tinkerforge", "OutdoorWeatherStationWindDirection")).withLabel(
                                        "Wind Direction").build(), new ChannelDefinitionBuilder(
                                        "OutdoorWeatherStationBatteryLow", new ChannelTypeUID("tinkerforge",
                                                "OutdoorWeatherStationBatteryLow")).withLabel("Battery Low").build(),
                                new ChannelDefinitionBuilder("OutdoorWeatherStationLastChange", new ChannelTypeUID(
                                        "tinkerforge", "OutdoorWeatherStationLastChange")).withLabel("Last Change")
                                        .build())).build();
    }

    public static @Nullable ConfigDescription getConfigDescription(URI uri) {
        switch (uri.toASCIIString()) {
            case "thing-type:tinkerforge:outdoorweatherstation":
                return ConfigDescriptionBuilder
                        .create(uri)
                        .withParameters(
                                Arrays.asList(ConfigDescriptionParameterBuilder
                                        .create("stationID", Type.INTEGER)
                                        .withDefault("0")
                                        .withDescription(
                                                "The ID of the station to query. Each station gives itself a random identifier on startup. The Outdoor Weather Bricklet reports available IDs.")
                                        .withMinimum(BigDecimal.valueOf(0)).withMaximum(BigDecimal.valueOf(255))
                                        .build())).build();
            case "channel-type:tinkerforge:OutdoorWeatherStationTemperature":
            case "channel-type:tinkerforge:OutdoorWeatherStationHumidity":
            case "channel-type:tinkerforge:OutdoorWeatherStationWindSpeed":
            case "channel-type:tinkerforge:OutdoorWeatherStationGustSpeed":
            case "channel-type:tinkerforge:OutdoorWeatherStationRainFall":
            case "channel-type:tinkerforge:OutdoorWeatherStationWindDirection":
            case "channel-type:tinkerforge:OutdoorWeatherStationBatteryLow":
            case "channel-type:tinkerforge:OutdoorWeatherStationLastChange":
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
        BrickletOutdoorWeatherStationConfig cfg = (BrickletOutdoorWeatherStationConfig) config
                .as(BrickletOutdoorWeatherStationConfig.class);
        switch (value) {
            case "OutdoorWeatherStationTemperature":
                updateStateFn.accept(value,
                        transformOutdoorWeatherTemperatureGetter0(bricklet.getStationData(cfg.stationID)));
                break;
            case "OutdoorWeatherStationHumidity":
                updateStateFn.accept(value,
                        transformOutdoorWeatherHumidityGetter0(bricklet.getStationData(cfg.stationID)));
                break;
            case "OutdoorWeatherStationWindSpeed":
                updateStateFn.accept(value,
                        transformOutdoorWeatherWindSpeedGetter0(bricklet.getStationData(cfg.stationID)));
                break;
            case "OutdoorWeatherStationGustSpeed":
                updateStateFn.accept(value,
                        transformOutdoorWeatherGustSpeedGetter0(bricklet.getStationData(cfg.stationID)));
                break;
            case "OutdoorWeatherStationRainFall":
                updateStateFn.accept(value,
                        transformOutdoorWeatherRainFallGetter0(bricklet.getStationData(cfg.stationID)));
                break;
            case "OutdoorWeatherStationWindDirection":
                updateStateFn.accept(value,
                        transformOutdoorWeatherWindDirectionGetter0(bricklet.getStationData(cfg.stationID)));
                break;
            case "OutdoorWeatherStationBatteryLow":
                updateStateFn.accept(value,
                        transformOutdoorWeatherBatteryLowGetter0(bricklet.getStationData(cfg.stationID)));
                break;
            case "OutdoorWeatherStationLastChange":
                updateStateFn.accept(value,
                        transformOutdoorWeatherLastChangeGetter0(bricklet.getStationData(cfg.stationID)));
                break;
            default:
                logger.warn("Refresh for unknown channel {}", value);
                break;
        }
    }

    public String getWindDirectionName(int windDirection) {
        String[] windDirections = new String[] { "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW",
                "WSW", "W", "WNW", "NW", "NNW" };

        if (windDirection >= 0 && windDirection < windDirections.length) {
            return windDirections[windDirection];
        } else if (windDirection == 255) {
            return "Unknown (Station Error)";
        } else {
            return "Unknown (" + windDirection + ")";
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

    private org.eclipse.smarthome.core.types.State transformOutdoorWeatherTemperatureGetter0(StationData value) {
        return new QuantityType<>(value.temperature / 10.0, SIUnits.CELSIUS);
    }

    private org.eclipse.smarthome.core.types.State transformOutdoorWeatherHumidityGetter0(StationData value) {
        return new QuantityType<>(value.humidity, SmartHomeUnits.PERCENT);
    }

    private org.eclipse.smarthome.core.types.State transformOutdoorWeatherWindSpeedGetter0(StationData value) {
        return new QuantityType<>(value.windSpeed / 10.0, SmartHomeUnits.METRE_PER_SECOND);
    }

    private org.eclipse.smarthome.core.types.State transformOutdoorWeatherGustSpeedGetter0(StationData value) {
        return new QuantityType<>(value.gustSpeed / 10.0, SmartHomeUnits.METRE_PER_SECOND);
    }

    private org.eclipse.smarthome.core.types.State transformOutdoorWeatherRainFallGetter0(StationData value) {
        return new QuantityType<>(value.rain / 10000.0, SIUnits.METRE);
    }

    private org.eclipse.smarthome.core.types.State transformOutdoorWeatherWindDirectionGetter0(StationData value) {
        return new StringType(getWindDirectionName(value.windDirection));
    }

    private org.eclipse.smarthome.core.types.State transformOutdoorWeatherBatteryLowGetter0(StationData value) {
        return value.batteryLow ? OnOffType.ON : OnOffType.OFF;
    }

    private org.eclipse.smarthome.core.types.State transformOutdoorWeatherLastChangeGetter0(StationData value) {
        return new DateTimeType(getAbsoluteTime(value.lastChange));
    }

    @Override
    public Identity getIdentity() throws TinkerforgeException {
        return new Identity();
    }
}
