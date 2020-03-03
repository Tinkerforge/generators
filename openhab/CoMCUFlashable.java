package org.eclipse.smarthome.binding.tinkerforge.internal.device;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.stream.IntStream;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

import org.eclipse.jetty.client.HttpClient;
import org.eclipse.smarthome.core.thing.binding.firmware.Firmware;
import org.eclipse.smarthome.core.thing.binding.firmware.ProgressCallback;
import org.eclipse.smarthome.core.thing.binding.firmware.ProgressStep;

import com.tinkerforge.TinkerforgeException;

public interface CoMCUFlashable {
    public final static int BOOTLOADER_MODE_BOOTLOADER = 0;
    public final static int BOOTLOADER_MODE_FIRMWARE = 1;
    public final static int BOOTLOADER_MODE_BOOTLOADER_WAIT_FOR_REBOOT = 2;
    public final static int BOOTLOADER_MODE_FIRMWARE_WAIT_FOR_REBOOT = 3;
    public final static int BOOTLOADER_MODE_FIRMWARE_WAIT_FOR_ERASE_AND_REBOOT = 4;
    public final static int BOOTLOADER_STATUS_OK = 0;
    public final static int BOOTLOADER_STATUS_INVALID_MODE = 1;
    public final static int BOOTLOADER_STATUS_NO_CHANGE = 2;
    public final static int BOOTLOADER_STATUS_ENTRY_FUNCTION_NOT_PRESENT = 3;
    public final static int BOOTLOADER_STATUS_DEVICE_IDENTIFIER_INCORRECT = 4;
    public final static int BOOTLOADER_STATUS_CRC_MISMATCH = 5;

    public abstract int setBootloaderMode(int mode) throws TinkerforgeException;

    public abstract int getBootloaderMode() throws TinkerforgeException;

    public abstract void setWriteFirmwarePointer(long pointer) throws TinkerforgeException;

    public abstract int writeFirmware(int[] chunk) throws TinkerforgeException;

    public default void flash(Firmware firmware, ProgressCallback progressCallback, HttpClient httpClient) {
        progressCallback.defineSequence(ProgressStep.DOWNLOADING, ProgressStep.UPDATING, ProgressStep.REBOOTING);

        byte[] plugin = FlashUtils.downloadFirmware(firmware, progressCallback, httpClient);
        if (plugin == null)
            return;

        ZipInputStream zf = new ZipInputStream(new ByteArrayInputStream(plugin));
        ZipEntry file = null;

        byte[] plugin_data = null;
        try {
            while ((file = zf.getNextEntry()) != null) {
                if (file.getName().endsWith("firmware.bin")) {
                    long size = file.getSize();
                    if (size > 4 << 20) // TODO: Useful upper bound? 4MB for now...
                        return;
                    // plugin_data = new byte[(int)size];
                    byte[] buffer = new byte[1024];
                    ByteArrayOutputStream outStream = new ByteArrayOutputStream();
                    int read = 0;
                    while ((read = zf.read(buffer)) >= 0) {
                        outStream.write(buffer, 0, read);
                    }
                    plugin_data = outStream.toByteArray();
                    break;
                }
            }
        } catch (IOException e) {
            progressCallback.failed("Failed to update: zip file contained no firmware");
            return;
        }
        if (plugin_data == null)
            return;

        plugin = plugin_data;
        int regular_plugin_upto = -1;
        for (int i = plugin.length - 13; i >= 4; --i) {
            if (plugin[i] == 0x12 && plugin[i - 1] == 0x34 && plugin[i - 2] == 0x56 && plugin[i - 3] == 0x78) {
                regular_plugin_upto = i;
                break;
            }
        }

        if (regular_plugin_upto == -1)
            return;

        progressCallback.next();
        progressCallback.update(33);
        try {
            CoMCUHelper.flashComcuPlugin(plugin, this, regular_plugin_upto);
        } catch (TinkerforgeException e) {
            progressCallback.failed("Failed to flash: {}", e.getMessage());
            return;
        }

        progressCallback.next();

        int mode_ret;
        try {
            mode_ret = this.setBootloaderMode(CoMCUFlashable.BOOTLOADER_MODE_FIRMWARE);
        } catch (TinkerforgeException e) {
            progressCallback.failed("Failed to reboot into firmware: {}", e.getMessage());
            return;
        }
        if (mode_ret != 0 && mode_ret != 2) {
            // report error
            if (mode_ret != 5) {
                progressCallback.failed("Failed to reboot into firmware: Set bootloader mode returned {}", mode_ret);
                return;
            }

            try {
                CoMCUHelper.flashComcuPlugin(plugin, this, plugin.length);
            } catch (TinkerforgeException e) {
                progressCallback.failed("Failed to flash (second try): {}", e.getMessage());
                return;
            }
        }
        progressCallback.update(66);
        try {
            CoMCUHelper.waitForBootloaderMode(this, CoMCUFlashable.BOOTLOADER_MODE_FIRMWARE);
        } catch (TinkerforgeException e) {
            progressCallback.failed("Failed to wait for reboot into firmware: {}", e.getMessage());
            return;
        }
        progressCallback.update(100);
        progressCallback.success();
    }
}

class CoMCUHelper {
    static void waitForBootloaderMode(CoMCUFlashable bricklet, int mode) throws TinkerforgeException {
        int counter = 0;
        while (true) {
            if (bricklet.getBootloaderMode() == mode)
                break;

            if (counter == 40)
                return;

            try {
                Thread.sleep(250);
            } catch (InterruptedException e) {
            }
            ++counter;
        }
    }

    static void flashComcuPlugin(byte[] plugin, CoMCUFlashable bricklet, int regular_plugin_upto)
            throws TinkerforgeException {
        bricklet.setBootloaderMode(CoMCUFlashable.BOOTLOADER_MODE_BOOTLOADER);
        waitForBootloaderMode(bricklet, CoMCUFlashable.BOOTLOADER_MODE_BOOTLOADER);

        int num_packets = plugin.length / 64;
        int[] index_list;
        if (regular_plugin_upto >= (plugin.length - 64 * 4))
            index_list = IntStream.range(0, num_packets).toArray();
        else {
            int packet_up_to = ((regular_plugin_upto / 256) + 1) * 4;
            index_list = IntStream.concat(IntStream.range(0, packet_up_to),
                    IntStream.of(num_packets - 4, num_packets - 3, num_packets - 2, num_packets - 1)).toArray();
        }

        int[] chunk = new int[64];

        for (int position : index_list) {
            int start = position * 64;
            int end = (position + 1) * 64;

            for (int i = 0; i < 64; ++i)
                chunk[i] = plugin[start + i];

            try {
                bricklet.setWriteFirmwarePointer(start);
                bricklet.writeFirmware(chunk);
            } catch (Exception e) {
                try {
                    bricklet.setWriteFirmwarePointer(start);
                    bricklet.writeFirmware(chunk);
                } catch (Exception e1) {
                    return;
                }
            }
        }
    }
}
