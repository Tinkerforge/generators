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

import java.util.ArrayList;
import java.util.List;

import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.jetty.client.HttpClient;
import org.eclipse.smarthome.core.thing.binding.firmware.Firmware;
import org.eclipse.smarthome.core.thing.binding.firmware.ProgressCallback;
import org.eclipse.smarthome.core.thing.binding.firmware.ProgressStep;

import com.tinkerforge.TinkerforgeException;

/**
 * Implemented by bricks that support flashing standard (i.e. non-CoMCU) bricklets.
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
public interface StandardFlashHost {
    public abstract void writeBrickletPlugin(char port, short chunkOffset, short[] chunk) throws TinkerforgeException;

    public abstract short[] readBrickletPlugin(char port, short chunkOffset) throws TinkerforgeException;

    public abstract void reset() throws TinkerforgeException;

    public default void flash(char port, Firmware firmware, ProgressCallback progressCallback, HttpClient httpClient) {
        progressCallback.defineSequence(ProgressStep.DOWNLOADING, ProgressStep.TRANSFERRING, ProgressStep.UPDATING,
                ProgressStep.REBOOTING);

        byte[] plugin = FlashUtils.downloadFirmware(firmware, progressCallback, httpClient);
        if (plugin == null)
            return;

        progressCallback.next();

        List<short[]> pluginChunks = new ArrayList<>();
        int offset = 0;

        final int pluginChunkSize = 32;
        while (offset < plugin.length) {
            short[] chunk = new short[pluginChunkSize];
            for (int i = 0; i < Math.min(plugin.length - offset, pluginChunkSize); ++i)
                chunk[i] = plugin[offset + i];
            pluginChunks.add(chunk);
            offset += pluginChunkSize;
        }

        short position = 0;
        for (short[] chunk : pluginChunks) {
            try {
                this.writeBrickletPlugin(port, position, chunk);
            } catch (TinkerforgeException e) {
                progressCallback.failed("Failed to transfer firmware to device: {}", e.getMessage());
                return;
            }
            ++position;
            int progress = (int) (((double) position / pluginChunks.size()) / 4);
            progressCallback.update(25 + progress);
        }

        progressCallback.next();

        position = 0;
        for (short[] chunk : pluginChunks) {
            short[] actual;
            try {
                actual = this.readBrickletPlugin(port, position);
            } catch (TinkerforgeException e) {
                progressCallback.failed("Failed to read back transferred firmware: {}", e.getMessage());
                return;
            }
            for (int i = 0; i < Math.min(actual.length, chunk.length); ++i)
                if ((byte) chunk[i] != (byte) actual[i]) {
                    progressCallback.failed(
                            "Firmware integrity check failed: Byte {} of chunk {} was {}, but expected was {}", i,
                            position, (byte) actual[i], (byte) chunk[i]);
                    return;
                }

            ++position;
            int progress = (int) (((double) position / pluginChunks.size()) / 4);
            progressCallback.update(25 + progress);
        }
        progressCallback.next();

        try {
            this.reset();
        } catch (TinkerforgeException e) {
            progressCallback.failed("Failed to reset brick: {}", e.getMessage());
            return;
        }
        progressCallback.update(100);

        progressCallback.success();
    }
}
