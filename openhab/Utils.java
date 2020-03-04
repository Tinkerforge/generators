package org.eclipse.smarthome.binding.tinkerforge.internal;

import org.eclipse.jdt.annotation.NonNull;
import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.jdt.annotation.Nullable;

@NonNullByDefault
public class Utils {
    public static @NonNull <T> T assertNonNull(@Nullable T value) {
        StackTraceElement e = Thread.currentThread().getStackTrace()[1];
        if (value == null) throw new AssertionError(String.format("Value was asserted to be non-null, but was null: %s:%s", e.getFileName(), e.getLineNumber()));
        return value;
    }
}
