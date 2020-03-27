package org.eclipse.smarthome.binding.tinkerforge.internal;

import java.math.BigDecimal;
import java.net.URI;

import org.eclipse.jdt.annotation.NonNull;
import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.jdt.annotation.Nullable;
import org.eclipse.smarthome.config.core.ConfigDescription;
import org.eclipse.smarthome.config.core.ConfigDescriptionParameter;
import org.eclipse.smarthome.config.core.ConfigDescriptionParameter.Type;
import org.eclipse.smarthome.config.core.ConfigDescriptionRegistry;
import org.eclipse.smarthome.config.core.Configuration;
import org.eclipse.smarthome.core.thing.Channel;
import org.eclipse.smarthome.core.thing.ChannelUID;
import org.eclipse.smarthome.core.thing.ThingUID;
import org.eclipse.smarthome.core.thing.binding.builder.ChannelBuilder;
import org.eclipse.smarthome.core.thing.type.ChannelDefinition;
import org.eclipse.smarthome.core.thing.type.ChannelType;
import org.eclipse.smarthome.core.thing.type.ChannelTypeRegistry;
import org.eclipse.smarthome.core.thing.type.ThingType;
import org.slf4j.Logger;

@NonNullByDefault
public class Utils {
    public static @NonNull <T> T assertNonNull(@Nullable T value) {
        StackTraceElement e = Thread.currentThread().getStackTrace()[1];
        if (value == null) throw new AssertionError(String.format("Value was asserted to be non-null, but was null: %s:%s", e.getFileName(), e.getLineNumber()));
        return value;
    }

    public static Channel buildChannel(ThingType tt, ThingUID tuid, ChannelDefinition def, ChannelTypeRegistry chanTypeReg, ConfigDescriptionRegistry confDescReg, Logger logger) {
        ChannelType ct = TinkerforgeChannelTypeProvider.getChannelTypeStatic(def.getChannelTypeUID(), null);
        if (ct == null) {
            ct = Utils.assertNonNull(chanTypeReg.getChannelType(def.getChannelTypeUID()));
        }
        ChannelBuilder builder = ChannelBuilder
                .create(new ChannelUID(tuid, def.getId()), ct.getItemType())
                .withAutoUpdatePolicy(def.getAutoUpdatePolicy()).withProperties(def.getProperties())
                .withType(def.getChannelTypeUID()).withKind(ct.getKind());

        String desc = def.getDescription();
        if (desc != null) {
            builder = builder.withDescription(desc);
        }
        String label = def.getLabel();
        if (label != null) {
            builder = builder.withLabel(label);
        }

        // Initialize channel configuration with default-values
        URI confDescURI = ct.getConfigDescriptionURI();
        if (confDescURI == null) {
            return builder.build();
        }

        ConfigDescription cd = confDescReg.getConfigDescription(confDescURI);
        if (cd == null) {
            return builder.build();
        }

        Configuration config = new Configuration();
        for (ConfigDescriptionParameter param : cd.getParameters()) {
            String defaultValue = param.getDefault();
            if (defaultValue == null) {
                continue;
            }

            Object value = getDefaultValueAsCorrectType(param.getType(), defaultValue, logger);
            if (value == null) {
                continue;
            }

            config.put(param.getName(), value);
        }
        builder = builder.withConfiguration(config);

        return builder.build();
    }

    public static @Nullable Object getDefaultValueAsCorrectType(Type parameterType, String defaultValue, Logger logger) {
        try {
            switch (parameterType) {
                case TEXT:
                    return defaultValue;
                case BOOLEAN:
                    return Boolean.parseBoolean(defaultValue);
                case INTEGER:
                    return new BigDecimal(defaultValue);
                case DECIMAL:
                    return new BigDecimal(defaultValue);
                default:
                    return null;
            }
        } catch (NumberFormatException ex) {
            logger.warn("Could not parse default value '{}' as type '{}': {}", defaultValue, parameterType,
                    ex.getMessage(), ex);
            return null;
        }
    }
}
