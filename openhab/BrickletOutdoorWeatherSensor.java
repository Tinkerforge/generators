
package com.tinkerforge;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.time.ZonedDateTime;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.Arrays;
import java.util.List;
import java.net.URI;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.function.Function;

import com.tinkerforge.BrickletOutdoorWeather.SensorData;
import com.tinkerforge.Device.SetterRefresh;

import java.util.function.BiConsumer;
import org.eclipse.smarthome.config.core.Configuration;
import org.eclipse.smarthome.config.core.ConfigDescription;
import org.eclipse.smarthome.config.core.ConfigDescriptionParameter.Type;
import org.eclipse.smarthome.config.core.ConfigDescriptionParameterBuilder;
import org.eclipse.smarthome.config.core.ConfigDescriptionParameterGroup;
import org.eclipse.smarthome.config.core.ParameterOption;
import org.eclipse.smarthome.core.types.State;
import org.eclipse.smarthome.core.types.StateOption;
import org.eclipse.smarthome.core.types.Command;
import org.eclipse.smarthome.core.types.CommandDescriptionBuilder;
import org.eclipse.smarthome.core.types.CommandOption;
import org.eclipse.smarthome.core.thing.ThingTypeUID;
import org.eclipse.smarthome.core.thing.type.ChannelDefinitionBuilder;
import org.eclipse.smarthome.core.thing.type.ChannelType;
import org.eclipse.smarthome.core.thing.type.ChannelTypeBuilder;
import org.eclipse.smarthome.core.thing.type.ChannelTypeUID;
import org.eclipse.smarthome.core.thing.type.ThingType;
import org.eclipse.smarthome.core.thing.type.ThingTypeBuilder;
import org.eclipse.smarthome.core.types.StateDescriptionFragmentBuilder;
import org.eclipse.smarthome.binding.tinkerforge.internal.TinkerforgeBindingConstants;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.eclipse.smarthome.core.library.types.DateTimeType;
import org.eclipse.smarthome.core.library.types.OnOffType;
import org.eclipse.smarthome.core.library.types.QuantityType;
import org.eclipse.smarthome.core.library.types.StringType;
import org.eclipse.smarthome.core.library.unit.MetricPrefix;
import org.eclipse.smarthome.core.library.unit.SIUnits;
import org.eclipse.smarthome.core.library.unit.SmartHomeUnits;


public class BrickletOutdoorWeatherSensor {
    public BrickletOutdoorWeatherSensor(int id, BrickletOutdoorWeather bricklet) {
        this.id = id;
        this.bricklet = bricklet;
    }

    private final int id;
    private final BrickletOutdoorWeather bricklet;

    public final static int DEVICE_IDENTIFIER = -288;
    public final static String DEVICE_DISPLAY_NAME = "Outdoor Weather Sensor";

    public final static DeviceInfo DEVICE_INFO = new DeviceInfo(DEVICE_DISPLAY_NAME, "outdoorweathersensor",
            DEVICE_IDENTIFIER, BrickletOutdoorWeatherSensor.class);

    private final Logger logger = LoggerFactory.getLogger(BrickletOutdoorWeather.class);
    private final static Logger static_logger = LoggerFactory.getLogger(BrickletOutdoorWeather.class);

    public void initialize(org.eclipse.smarthome.config.core.Configuration config, Function<String, org.eclipse.smarthome.config.core.Configuration> getChannelConfigFn, BiConsumer<String, org.eclipse.smarthome.core.types.State> updateStateFn, BiConsumer<String, String> triggerChannelFn) {
        bricklet.addSensorDataListener((int identifier, int temperature, int humidity) -> {
            if(identifier != this.id)
                return;
            updateStateFn.accept("OutdoorWeatherSensorTemperature",   new QuantityType<>(temperature / 10.0, SIUnits.CELSIUS));
            updateStateFn.accept("OutdoorWeatherSensorHumidity",      new QuantityType<>(humidity, SmartHomeUnits.PERCENT));
            updateStateFn.accept("OutdoorWeatherSensorLastChange",    new DateTimeType(getAbsoluteTime(0)));
        });
    }

    public List<String> getEnabledChannels(org.eclipse.smarthome.config.core.Configuration config)
            throws TinkerforgeException {
        return Arrays.asList("OutdoorWeatherSensorTemperature",
                             "OutdoorWeatherSensorHumidity",
                             "OutdoorWeatherSensorLastChange");
    }

    public static ChannelType getChannelType(ChannelTypeUID channelTypeUID) {
        switch (channelTypeUID.getId()) {
        case "OutdoorWeatherSensorTemperature":
            return ChannelTypeBuilder
                    .state(new ChannelTypeUID("tinkerforge", "OutdoorWeatherSensorTemperature"), "Temperature",
                            "Number:Temperature")
                    .withConfigDescriptionURI(URI.create("channel-type:tinkerforge:OutdoorWeatherSensorTemperature"))
                    .withDescription("Last received temperature").withStateDescription(StateDescriptionFragmentBuilder
                            .create().withPattern("%.1f %unit%").withReadOnly(true).build().toStateDescription())
                    .build();
        case "OutdoorWeatherSensorHumidity":
            return ChannelTypeBuilder
                    .state(new ChannelTypeUID("tinkerforge", "OutdoorWeatherSensorHumidity"), "Humidity",
                            "Number:Dimensionless")
                    .withConfigDescriptionURI(URI.create("channel-type:tinkerforge:OutdoorWeatherSensorHumidity"))
                    .withDescription("Last received humidity").withStateDescription(StateDescriptionFragmentBuilder
                            .create().withPattern("%d %%").withReadOnly(true).build().toStateDescription())
                    .build();
        case "OutdoorWeatherSensorLastChange":
            return ChannelTypeBuilder
                    .state(new ChannelTypeUID("tinkerforge", "OutdoorWeatherSensorLastChange"), "Last Change", "DateTime")
                    .withConfigDescriptionURI(URI.create("channel-type:tinkerforge:OutdoorWeatherSensorLastChange"))
                    .withDescription("Time when the last data was received from the sensor.")
                    .withStateDescription(
                            StateDescriptionFragmentBuilder.create().withReadOnly(true).build().toStateDescription())
                    .build();
        default:
            static_logger.debug("Unknown channel type ID {}", channelTypeUID.getId());
            break;
        }

        return null;
    }

    public static ThingType getThingType(ThingTypeUID thingTypeUID) {
        return ThingTypeBuilder.instance(thingTypeUID, "Tinkerforge Outdoor Weather Temperature/Humidity Sensor TH-6148 ").isListed(false)
                .withSupportedBridgeTypeUIDs(Arrays.asList(TinkerforgeBindingConstants.THING_TYPE_OUTDOOR_WEATHER.getId()))
                .withConfigDescriptionURI(URI.create("thing-type:tinkerforge:" + thingTypeUID.getId()))
                .withDescription("Weather sensor connected to an Outdoor Weather Bricklet")
                .withChannelDefinitions(Arrays.asList(
                        new ChannelDefinitionBuilder("OutdoorWeatherSensorTemperature",
                                new ChannelTypeUID("tinkerforge", "OutdoorWeatherSensorTemperature")).withLabel("Temperature").build(),
                        new ChannelDefinitionBuilder("OutdoorWeatherSensorHumidity",
                                new ChannelTypeUID("tinkerforge", "OutdoorWeatherSensorHumidity")).withLabel("Humidity").build(),
                        new ChannelDefinitionBuilder("OutdoorWeatherSensorLastChange",
                                new ChannelTypeUID("tinkerforge", "OutdoorWeatherSensorLastChange")).withLabel("Last Change").build()))
                .build();
    }

    public static ConfigDescription getConfigDescription(URI uri) {
        switch (uri.toASCIIString()) {
        case "thing-type:tinkerforge:outdoorweathersensor":
        case "channel-type:tinkerforge:OutdoorWeatherSensorTemperature":
        case "channel-type:tinkerforge:OutdoorWeatherSensorHumidity":
        case "channel-type:tinkerforge:OutdoorWeatherSensorLastChange":
            return new ConfigDescription(uri, Arrays.asList());
        default:
            static_logger.debug("Unknown config description URI {}", uri.toASCIIString());
            break;
        }
        return null;
    }


    public void refreshValue(String value, org.eclipse.smarthome.config.core.Configuration config, org.eclipse.smarthome.config.core.Configuration channelConfig, BiConsumer<String, org.eclipse.smarthome.core.types.State> updateStateFn, BiConsumer<String, String> triggerChannelFn) throws TinkerforgeException {
        switch(value) {
            case "OutdoorWeatherSensorTemperature":
                updateStateFn.accept(value, transformOutdoorWeatherTemperatureGetter0(bricklet.getSensorData(this.id)));
                break;
            case "OutdoorWeatherSensorHumidity":
                updateStateFn.accept(value, transformOutdoorWeatherHumidityGetter0(bricklet.getSensorData(this.id)));
                break;
            case "OutdoorWeatherSensorLastChange":
                updateStateFn.accept(value, transformOutdoorWeatherLastChangeGetter0(bricklet.getSensorData(this.id)));
                break;
            default:
                logger.warn("Refresh for unknown channel {}", value);
                break;
        }
    }

    public ZonedDateTime getAbsoluteTime(int offset) {
        return ZonedDateTime.now().minusSeconds(offset);
    }

    public List<SetterRefresh> handleCommand(org.eclipse.smarthome.config.core.Configuration config, org.eclipse.smarthome.config.core.Configuration channelConfig, String channel, Command command) throws TinkerforgeException {
        List<SetterRefresh> result = Collections.emptyList();
        switch(channel) {

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
}
