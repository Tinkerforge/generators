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
package org.eclipse.smarthome.binding.tinkerforge.internal;

import java.util.Collections;
import java.util.HashSet;
import java.util.Locale;
import java.util.Optional;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.jdt.annotation.Nullable;
import org.eclipse.jetty.client.HttpClient;
import org.eclipse.jetty.client.api.Result;
import org.eclipse.jetty.client.util.BufferingResponseListener;
import org.eclipse.smarthome.binding.tinkerforge.internal.device.DeviceWrapperFactory;
import org.eclipse.smarthome.core.common.ThreadPoolManager;
import org.eclipse.smarthome.core.thing.Thing;
import org.eclipse.smarthome.core.thing.ThingTypeUID;
import org.eclipse.smarthome.core.thing.binding.firmware.Firmware;
import org.eclipse.smarthome.core.thing.binding.firmware.FirmwareBuilder;
import org.eclipse.smarthome.core.thing.firmware.FirmwareProvider;
import org.eclipse.smarthome.io.net.http.HttpClientFactory;
import org.osgi.service.component.annotations.Component;
import org.osgi.service.component.annotations.Reference;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@NonNullByDefault
@Component(service = FirmwareProvider.class)
public class TinkerforgeFirmwareProvider implements FirmwareProvider {
    private @Nullable HttpClient httpClient;

    private final Logger logger = LoggerFactory.getLogger(TinkerforgeFirmwareProvider.class);

    private class FirmwareInfo {
        public FirmwareInfo(String version, String url) {
            this.version = version;
            this.url = url;

        }

        String version;
        String url;
    }

    private final ConcurrentMap<String, @Nullable FirmwareInfo> latestVersions = new ConcurrentHashMap<>();

    protected final ScheduledExecutorService scheduler = ThreadPoolManager.getScheduledPool("tinkerforge-firmware");

    @Override
    public @Nullable Firmware getFirmware(Thing thing, String version) {
        return getFirmware(thing, version, null);
    }

    @Override
    public @Nullable Firmware getFirmware(Thing thing, String version, @Nullable Locale locale) {
        Optional<Firmware> opt = Utils.assertNonNull(getFirmwares(thing, locale)).stream().filter(fw -> fw.getVersion().equals(version)).findFirst();
        //.getOrDefault(null) conflicts with the null annotations.
        if(opt.isPresent())
            return opt.get();
        return null;
    }

    @Override
    public @Nullable Set<Firmware> getFirmwares(Thing thing) {
        return getFirmwares(thing, null);
    }

    @Override
    public @Nullable Set<Firmware> getFirmwares(Thing thing, @Nullable Locale locale) {
        Set<Firmware> result = new HashSet<>();
        String id = thing.getThingTypeUID().getId();
        @Nullable FirmwareInfo info = latestVersions.get(id);
        if (info != null)
            result.add(buildFirmware(thing.getThingTypeUID(), info.version, info.url));
        return result;

    }

    private Firmware buildFirmware(ThingTypeUID ttuid, String version, String url) {
        return FirmwareBuilder.create(ttuid, version).withVendor("Tinkerforge GmbH")
                .withProperties(Collections.singletonMap(TinkerforgeBindingConstants.PROPERTY_FIRMWARE_URL, url))
                .build();
    }

    private void parseLatestVersions(String latestVersionsText) {
        for (String line : latestVersionsText.split("\n")) {
            boolean isBrick = line.startsWith("bricks:");
            boolean isBricklet = line.startsWith("bricklets:");
            boolean isExtension = line.startsWith("extensions:");
            if (!(isBrick || isBricklet || isExtension))
                continue;

            String[] splt = line.split(":");
            String deviceType = splt[0].substring(0, splt[0].length() - 1);
            String deviceName = splt[1];
            String thingName = deviceType + deviceName.replace("_", "");

            if (deviceName.equals("hat") || deviceName.equals("hat_zero"))
                thingName = "brick" + deviceName.replace("_", "");

            if (deviceName.contains("lcd_20x4_v1"))
                thingName = deviceType + "lcd20x4";

            String version = splt[2];
            boolean isCoMCU = isExtension || DeviceWrapperFactory.getDeviceInfo(thingName).isCoMCU;
            String urlString = String.format("https://download.tinkerforge.com/firmwares/%s/%s/%s_%s_firmware_%s.%s",
                    deviceType + 's', deviceName, deviceType, deviceName, version.replace(".", "_"), isCoMCU ? "zbin"
                            : "bin");

            latestVersions.put(thingName, new FirmwareInfo(version, urlString));
        }
    }

    private void getLatestVersions() {
        @Nullable HttpClient httpClient = this.httpClient;
        if (httpClient == null)
            return;

        httpClient.newRequest("https://download.tinkerforge.com/latest_versions.txt").send(
                new BufferingResponseListener() {
                    @Override
                    public void onComplete(@Nullable Result result) {
                        if (Utils.assertNonNull(result).isSucceeded()) {
                            parseLatestVersions(getContentAsString());
                            scheduler.schedule(() -> getLatestVersions(), 1, TimeUnit.HOURS);
                        } else {
                            logger.info("Failed to download latest versions: {}", Utils.assertNonNull(result).getFailure().toString());
                            scheduler.schedule(() -> getLatestVersions(), 5, TimeUnit.MINUTES);
                        }
                    }
                });
    }

    @Reference
    protected void setHttpClientFactory(HttpClientFactory httpClientFactory) {
        this.httpClient = httpClientFactory.createHttpClient("tinkerforge");
        try {
            Utils.assertNonNull(this.httpClient).start();
        } catch (Exception e) {
            logger.info("Failed to start HTTP Client: {}", e.getMessage());
            return;
        }
        getLatestVersions();
    }

    protected void unsetHttpClientFactory(HttpClientFactory httpClientFactory) {
        try {
            Utils.assertNonNull(this.httpClient).stop();
        } catch (Exception e) {
            logger.info("Failed to stop HTTP Client: {}", e.getMessage());
        }
        this.httpClient = null;
    }
}
