
package org.eclipse.smarthome.binding.tinkerforge.internal.device;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.time.ZonedDateTime;
import java.util.ArrayList;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.Arrays;
import java.util.List;
import java.net.URI;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.function.Consumer;
import java.util.function.Function;
import org.eclipse.smarthome.binding.tinkerforge.internal.device.DeviceWrapper.SetterRefresh;

import com.tinkerforge.Device.Identity;
import com.tinkerforge.TinkerforgeException;

import java.util.function.BiConsumer;
import org.eclipse.smarthome.config.core.Configuration;
import org.eclipse.smarthome.config.core.ConfigDescription;
import org.eclipse.smarthome.config.core.ConfigDescriptionBuilder;
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
import org.eclipse.smarthome.core.thing.binding.BaseThingHandler;
import org.eclipse.smarthome.core.thing.type.ChannelDefinitionBuilder;
import org.eclipse.smarthome.core.thing.type.ChannelType;
import org.eclipse.smarthome.core.thing.type.ChannelTypeBuilder;
import org.eclipse.smarthome.core.thing.type.ChannelTypeUID;
import org.eclipse.smarthome.core.thing.type.ThingType;
import org.eclipse.smarthome.core.thing.type.ThingTypeBuilder;
import org.eclipse.smarthome.core.types.StateDescriptionFragmentBuilder;
import org.eclipse.smarthome.binding.tinkerforge.internal.TinkerforgeBindingConstants;
import org.eclipse.smarthome.binding.tinkerforge.internal.handler.BrickletRemoteSwitchHandler;
import org.eclipse.smarthome.binding.tinkerforge.internal.handler.BrickletRemoteSwitchHandler.Task;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.eclipse.smarthome.core.library.types.DateTimeType;
import org.eclipse.smarthome.core.library.types.OnOffType;
import org.eclipse.smarthome.core.library.types.QuantityType;
import org.eclipse.smarthome.core.library.types.StringType;
import org.eclipse.smarthome.core.library.unit.MetricPrefix;
import org.eclipse.smarthome.core.library.unit.SIUnits;
import org.eclipse.smarthome.core.library.unit.SmartHomeUnits;

public class RemoteSocketTypeB implements DeviceWrapper {
    public RemoteSocketTypeB(BrickletRemoteSwitchHandler handler) {
        this.handler = handler;
    }

    private List<ScheduledFuture<?>> manualChannelUpdates = new ArrayList<ScheduledFuture<?>>();
    private List<ListenerReg> listenerRegs = new ArrayList<ListenerReg>();

    public void cancelManualUpdates() {
        manualChannelUpdates.forEach(f -> f.cancel(true));
    }

    public <T> T reg(T listener, Consumer<T> toRemove) {
        listenerRegs.add(new ListenerReg<T>(listener, toRemove));
        return listener;
    }

    @Override
    public void dispose(Configuration config) throws TinkerforgeException {
        listenerRegs.forEach(reg -> reg.toRemove.accept(reg.listener));
    }

    private final BrickletRemoteSwitchHandler handler;

    public final static int DEVICE_IDENTIFIER = -235;
    public final static String DEVICE_DISPLAY_NAME = "Remote Socket Type B";

    public final static DeviceInfo DEVICE_INFO = new DeviceInfo(DEVICE_DISPLAY_NAME, "remotesockettypeb",
            DEVICE_IDENTIFIER, RemoteSocketTypeB.class, DefaultActions.class, "1.0.0", false);

    private final Logger logger = LoggerFactory.getLogger(RemoteSocketTypeB.class);
    private final static Logger static_logger = LoggerFactory.getLogger(RemoteSocketTypeB.class);

    public List<String> getEnabledChannels(org.eclipse.smarthome.config.core.Configuration config)
            throws TinkerforgeException {
        return Arrays.asList("RemoteSocketTypeBCommand");
    }

    public static ChannelType getChannelType(ChannelTypeUID channelTypeUID) {
        switch (channelTypeUID.getId()) {
        case "RemoteSocketTypeBCommand":
            return ChannelTypeBuilder
                    .state(new ChannelTypeUID("tinkerforge", "RemoteSocketTypeBCommand"), "Command", "String")
                    .withConfigDescriptionURI(URI.create("channel-type:tinkerforge:RemoteSocketTypeBCommand"))
                    .withCommandDescription(
                            CommandDescriptionBuilder.create().withCommandOption(new CommandOption("ON", "Switch On"))
                                    .withCommandOption(new CommandOption("OFF", "Switch Off")).build())
                    .build();
        default:
            static_logger.debug("Unknown channel type ID {}", channelTypeUID.getId());
            break;
        }

        return null;
    }

    public static ThingType getThingType(ThingTypeUID thingTypeUID) {
        return ThingTypeBuilder.instance(thingTypeUID, "Tinkerforge Remote Socket Type B").isListed(true)
                .withSupportedBridgeTypeUIDs(
                        Arrays.asList(TinkerforgeBindingConstants.THING_TYPE_BRICKLET_REMOTE_SWITCH.toString(),
                                TinkerforgeBindingConstants.THING_TYPE_BRICKLET_REMOTE_SWITCH_V2.toString()))
                .withConfigDescriptionURI(URI.create("thing-type:tinkerforge:" + thingTypeUID.getId()))
                .withDescription(
                        "Remote controlled mains switch (Type B) for Remote Switch Bricklet or Remote Switch Bricklet 2.0")
                .withChannelDefinitions(Arrays.asList(new ChannelDefinitionBuilder("RemoteSocketTypeBCommand",
                        new ChannelTypeUID("tinkerforge", "RemoteSocketTypeBCommand")).withLabel("Command").build()))
                .build();
    }

    public static ConfigDescription getConfigDescription(URI uri) {
        switch (uri.toASCIIString()) {
        case "thing-type:tinkerforge:remotesockettypeb":
            return ConfigDescriptionBuilder.create(uri).withParameters(Arrays.asList(
                    ConfigDescriptionParameterBuilder.create("address", Type.INTEGER).withDefault("0")
                            .withDescription("The address of the remote socket to control.")
                            .withMinimum(BigDecimal.valueOf(0)).withMaximum(BigDecimal.valueOf(67108863)).build(),
                    ConfigDescriptionParameterBuilder.create("unit", Type.INTEGER).withDefault("0")
                            .withDescription("The unit of the remote socket to control.")
                            .withMinimum(BigDecimal.valueOf(0)).withMaximum(BigDecimal.valueOf(15)).build(),
                    ConfigDescriptionParameterBuilder.create("repeats", Type.INTEGER).withDefault("5").withDescription(
                            "Sets the number of times the code is sent when of the socket is toggled. The repeats basically correspond to the amount of time that a button of the remote is pressed.")
                            .withMinimum(BigDecimal.valueOf(0)).withMaximum(BigDecimal.valueOf(255)).build()))
                    .build();
        case "channel-type:tinkerforge:RemoteSocketTypeBCommand":
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
        RemoteSocketTypeBConfig cfg = (RemoteSocketTypeBConfig) config.as(RemoteSocketTypeBConfig.class);
        switch (value) {
        case "RemoteSocketTypeBCommand":
            break;
        default:
            logger.warn("Refresh for unknown channel {}", value);
            break;
        }
    }

    public List<SetterRefresh> handleCommand(org.eclipse.smarthome.config.core.Configuration config,
            org.eclipse.smarthome.config.core.Configuration channelConfig, String channel, Command command)
            throws TinkerforgeException {
        List<SetterRefresh> result = Collections.emptyList();
        RemoteSocketTypeBConfig cfg = (RemoteSocketTypeBConfig) config.as(RemoteSocketTypeBConfig.class);
        switch (channel) {
        case "RemoteSocketTypeBCommand":
            if (command instanceof StringType) {
                StringType cmd = (StringType) command;
                handler.enqueue(new Task(rs -> {
                    rs.setRepeats(cfg.repeats);
                    rs.switchSocketB(cfg.address, cfg.unit, cmd.toString().equals("ON") ? 1 : 0);
                }, success -> {
                    if (!success)
                        logger.warn("Address {} Unit {} command {} failed", cfg.address, cfg.unit, cmd.toString());
                }));
            }

            else {
                logger.warn("Command type {} not supported for channel {}. Please use one of StringType.",
                        command.getClass().getName(), channel);
            }

            break;
        default:
            logger.warn("Command for unknown channel {}", channel);
        }
        return result;
    }

    @Override
    public void initialize(Configuration config, Function<String, Configuration> getChannelConfigFn,
            BiConsumer<String, State> updateStateFn, BiConsumer<String, String> triggerChannelFn,
            ScheduledExecutorService scheduler, BaseThingHandler handler) throws TinkerforgeException {
        // TODO Auto-generated method stub

    }

    @Override
    public Identity getIdentity() throws TinkerforgeException {
        // TODO Auto-generated method stub
        return null;
    }
}
