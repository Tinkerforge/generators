package org.eclipse.smarthome.binding.tinkerforge.internal.device;

import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.jdt.annotation.Nullable;
import org.eclipse.smarthome.binding.tinkerforge.internal.handler.DeviceHandler;
import org.eclipse.smarthome.core.thing.binding.ThingActions;
import org.eclipse.smarthome.core.thing.binding.ThingActionsScope;
import org.eclipse.smarthome.core.thing.binding.ThingHandler;

@ThingActionsScope(name = "tinkerforge")
@NonNullByDefault
public class DefaultActions implements ThingActions {

    private @Nullable DeviceHandler handler;

    @Override
    public void setThingHandler(@Nullable ThingHandler handler) { this.handler = (DeviceHandler) handler; }

    @Override
    public @Nullable ThingHandler getThingHandler() { return handler; }
}

