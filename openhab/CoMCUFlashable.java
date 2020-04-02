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
package org.openhab.binding.tinkerforge.internal.device;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.stream.IntStream;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.jetty.client.HttpClient;
import org.eclipse.smarthome.core.thing.binding.firmware.Firmware;
import org.eclipse.smarthome.core.thing.binding.firmware.ProgressCallback;
import org.eclipse.smarthome.core.thing.binding.firmware.ProgressStep;

import com.tinkerforge.TinkerforgeException;

/**
 * Used to flash CoMCU bricklets.
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
public interface CoMCUFlashable {
    public static final int BOOTLOADER_MODE_BOOTLOADER = 0;
    public static final int BOOTLOADER_MODE_FIRMWARE = 1;
    public static final int BOOTLOADER_MODE_BOOTLOADER_WAIT_FOR_REBOOT = 2;
    public static final int BOOTLOADER_MODE_FIRMWARE_WAIT_FOR_REBOOT = 3;
    public static final int BOOTLOADER_MODE_FIRMWARE_WAIT_FOR_ERASE_AND_REBOOT = 4;
    public static final int BOOTLOADER_STATUS_OK = 0;
    public static final int BOOTLOADER_STATUS_INVALID_MODE = 1;
    public static final int BOOTLOADER_STATUS_NO_CHANGE = 2;
    public static final int BOOTLOADER_STATUS_ENTRY_FUNCTION_NOT_PRESENT = 3;
    public static final int BOOTLOADER_STATUS_DEVICE_IDENTIFIER_INCORRECT = 4;
    public static final int BOOTLOADER_STATUS_CRC_MISMATCH = 5;

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

        byte[] pluginData = null;
        try {
            while ((file = zf.getNextEntry()) != null) {
                if (file.getName().endsWith("firmware.bin")) {
                    long size = file.getSize();
                    if (size > 4 << 20) // Useful upper bound? 4MB for now...
                        return;
                    // pluginData = new byte[(int)size];
                    byte[] buffer = new byte[1024];
                    ByteArrayOutputStream outStream = new ByteArrayOutputStream();
                    int read = 0;
                    while ((read = zf.read(buffer)) >= 0) {
                        outStream.write(buffer, 0, read);
                    }
                    pluginData = outStream.toByteArray();
                    break;
                }
            }
        } catch (IOException e) {
            progressCallback.failed("Failed to update: zip file contained no firmware");
            return;
        }
        if (pluginData == null)
            return;

        plugin = pluginData;
        int regularPluginUpto = -1;
        for (int i = plugin.length - 13; i >= 4; --i) {
            if (plugin[i] == 0x12 && plugin[i - 1] == 0x34 && plugin[i - 2] == 0x56 && plugin[i - 3] == 0x78) {
                regularPluginUpto = i;
                break;
            }
        }

        if (regularPluginUpto == -1)
            return;

        progressCallback.next();
        progressCallback.update(33);
        try {
            CoMCUHelper.flashComcuPlugin(plugin, this, regularPluginUpto);
        } catch (TinkerforgeException e) {
            progressCallback.failed("Failed to flash: {}", e.getMessage());
            return;
        }

        progressCallback.next();

        int modeRet;
        try {
            modeRet = this.setBootloaderMode(CoMCUFlashable.BOOTLOADER_MODE_FIRMWARE);
        } catch (TinkerforgeException e) {
            progressCallback.failed("Failed to reboot into firmware: {}", e.getMessage());
            return;
        }
        if (modeRet != 0 && modeRet != 2) {
            // report error
            if (modeRet != 5) {
                progressCallback.failed("Failed to reboot into firmware: Set bootloader mode returned {}", modeRet);
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

/**
 * Helper functions for CoMCU flashing
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
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

    static void flashComcuPlugin(byte[] plugin, CoMCUFlashable bricklet, int regularPluginUpto)
            throws TinkerforgeException {
        bricklet.setBootloaderMode(CoMCUFlashable.BOOTLOADER_MODE_BOOTLOADER);
        waitForBootloaderMode(bricklet, CoMCUFlashable.BOOTLOADER_MODE_BOOTLOADER);

        int numPackets = plugin.length / 64;
        int[] indexList;
        if (regularPluginUpto >= (plugin.length - 64 * 4))
            indexList = IntStream.range(0, numPackets).toArray();
        else {
            int packetUpto = ((regularPluginUpto / 256) + 1) * 4;
            indexList = IntStream.concat(IntStream.range(0, packetUpto),
                    IntStream.of(numPackets - 4, numPackets - 3, numPackets - 2, numPackets - 1)).toArray();
        }

        int[] chunk = new int[64];

        for (int position : indexList) {
            int start = position * 64;

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
