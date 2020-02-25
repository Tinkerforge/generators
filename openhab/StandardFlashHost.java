package org.eclipse.smarthome.binding.tinkerforge.internal.device;

import java.util.ArrayList;
import java.util.List;

import com.tinkerforge.TinkerforgeException;

import org.eclipse.jetty.client.HttpClient;
import org.eclipse.smarthome.core.thing.binding.firmware.Firmware;
import org.eclipse.smarthome.core.thing.binding.firmware.ProgressCallback;
import org.eclipse.smarthome.core.thing.binding.firmware.ProgressStep;
public interface StandardFlashHost {
    public abstract void writeBrickletPlugin(char port, short chunkOffset, short[] chunk) throws TinkerforgeException;

    public abstract short[] readBrickletPlugin(char port, short chunkOffset) throws TinkerforgeException;

    public abstract void reset() throws TinkerforgeException;

    public default void flash(char port, Firmware firmware, ProgressCallback progressCallback, HttpClient httpClient) {
        progressCallback.defineSequence(ProgressStep.DOWNLOADING, ProgressStep.TRANSFERRING, ProgressStep.UPDATING, ProgressStep.REBOOTING);

        byte[] plugin = FlashUtils.downloadFirmware(firmware, progressCallback, httpClient);
        if(plugin == null)
            return;

        progressCallback.next();

        List<short[]> plugin_chunks = new ArrayList<>();
        int offset = 0;

        int PLUGIN_CHUNK_SIZE = 32;  //IPConnection.PLUGIN_CHUNK_SIZE
        while(offset < plugin.length) {
            short[] chunk = new short[PLUGIN_CHUNK_SIZE];
            for(int i = 0; i < Math.min(plugin.length - offset, PLUGIN_CHUNK_SIZE); ++i)
                chunk[i] = plugin[offset + i];
            plugin_chunks.add(chunk);
            offset += PLUGIN_CHUNK_SIZE;
        }

        short position = 0;
        for(short[] chunk : plugin_chunks) {
            try {
                this.writeBrickletPlugin(port, position, chunk);
            } catch (TinkerforgeException e) {
                progressCallback.failed("Failed to transfer firmware to device: {}", e.getMessage());
                return;
            }
            ++position;
            int progress = (int)(((double)position / plugin_chunks.size()) / 4);
            progressCallback.update(25 + progress);
        }

        progressCallback.next();

        position = 0;
        for(short[] chunk : plugin_chunks) {
            short[] actual;
            try {
                actual = this.readBrickletPlugin(port, position);
            } catch (TinkerforgeException e) {
                progressCallback.failed("Failed to read back transferred firmware: {}", e.getMessage());
                return;
            }
            for(int i = 0; i < Math.min(actual.length, chunk.length); ++i)
                if((byte)chunk[i] != (byte)actual[i]) {
                    progressCallback.failed("Firmware integrity check failed: Byte {} of chunk {} was {}, but expected was {}", i, position, (byte)actual[i], (byte)chunk[i]);
                    return;
                }

            ++position;
            int progress = (int)(((double)position / plugin_chunks.size()) / 4);
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
