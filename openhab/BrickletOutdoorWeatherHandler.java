package org.eclipse.smarthome.binding.tinkerforge.internal.handler;

import java.util.ArrayList;
import java.util.List;
import java.util.function.BiFunction;
import java.util.function.Consumer;
import java.util.function.Supplier;

import com.tinkerforge.BrickletOutdoorWeather;
import com.tinkerforge.DefaultActions;
import com.tinkerforge.Device;
import com.tinkerforge.IPConnection;

import org.eclipse.jdt.annotation.Nullable;
import org.eclipse.smarthome.config.core.ConfigDescriptionRegistry;
import org.eclipse.smarthome.core.thing.Bridge;
import org.eclipse.smarthome.core.thing.Thing;
import org.eclipse.smarthome.core.thing.ThingUID;
import org.eclipse.smarthome.core.thing.binding.BridgeHandler;
import org.eclipse.smarthome.core.thing.binding.ThingHandler;
import org.eclipse.smarthome.core.thing.binding.builder.BridgeBuilder;
import org.eclipse.smarthome.core.thing.type.ChannelTypeRegistry;

public class BrickletOutdoorWeatherHandler extends DeviceHandler implements BridgeHandler {
    private List<ThingHandler> childHandlers = new ArrayList<>();

    public BrickletOutdoorWeatherHandler(
        Bridge bridge,
        BiFunction<String, IPConnection, Device> deviceSupplier,
        Supplier<ChannelTypeRegistry> channelTypeRegistrySupplier,
        Supplier<ConfigDescriptionRegistry> configDescriptionRegistrySupplier) {
        super(bridge, deviceSupplier, DefaultActions.class, channelTypeRegistrySupplier, configDescriptionRegistrySupplier);
    }

    public @Nullable BrickletOutdoorWeather getDevice() {
        return (BrickletOutdoorWeather)super.getDevice();
    }

    public void handleTimeout() {
        ((BrickDaemonHandler)(this.getBridge().getHandler())).handleTimeout(this);
    }

    @Override
    public void initialize() {
        super.initialize();
        for(ThingHandler handler : childHandlers)
            handler.initialize();
    }

    @Override
    protected void initializeDevice() {
        super.initializeDevice();
        for(ThingHandler handler : childHandlers)
            handler.initialize();
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
     * {@link BaseThingHandler#updateThing(Thing)} must be called to persist the changes.
     *
     * @return {@link BridgeBuilder} which builds an exact copy of the bridge (not null)
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
