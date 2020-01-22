
package org.eclipse.smarthome.binding.tinkerforge.internal;

import java.util.HashSet;
import java.util.Locale;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

import org.eclipse.jdt.annotation.Nullable;
import org.eclipse.jetty.client.HttpClient;
import org.eclipse.jetty.client.api.Result;
import org.eclipse.jetty.client.util.BufferingResponseListener;
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

@Component(service = FirmwareProvider.class)
public class TinkerforgeFirmwareProvider implements FirmwareProvider {
    private HttpClient httpClient;

    private final Logger logger = LoggerFactory.getLogger(TinkerforgeChannelTypeProvider.class);

    private final ConcurrentMap<String, String> latestVersions = new ConcurrentHashMap<>();

    protected final ScheduledExecutorService scheduler = ThreadPoolManager.getScheduledPool("tinkerforge-firmware");

    @Override
    public Firmware getFirmware(Thing thing, String version) {
        return getFirmware(thing, version, null);
    }

    @Nullable
    @Override
    public Firmware getFirmware(Thing thing, String version, @Nullable Locale locale) {
        return getFirmwares(thing, locale).stream().filter(fw -> fw.getVersion().equals(version)).findFirst().orElseGet(() -> null);
    }

    @Override
    public Set<Firmware> getFirmwares(Thing thing) {
        return getFirmwares(thing, null);
    }

    @Override
    public Set<Firmware> getFirmwares(Thing thing, Locale locale) {
        Set<Firmware> result = new HashSet<>();
        result.add(buildFirmware(thing.getThingTypeUID(), thing.getProperties().get(TinkerforgeBindingConstants.PROPERTY_MINIMUM_FIRMWARE_VERSION)));
        String id = thing.getThingTypeUID().getId();
        String version = latestVersions.get(id);
        if (version != null)
            result.add(buildFirmware(thing.getThingTypeUID(), version));
        return result;

    }

    private Firmware buildFirmware(ThingTypeUID ttuid, String version) {
        return FirmwareBuilder.create(ttuid, version)
                              .withVendor("Tinkerforge GmbH")
                              .build();
    }

    private void parseLatestVersions(String latestVersionsText) {
        for(String line : latestVersionsText.split("\n")) {
            if (!(line.startsWith("bricks:") || line.startsWith("bricklets:") || line.startsWith("extensions:")))
                continue;

            String[] splt = line.split(":");
            String deviceName = splt[0].substring(0, splt[0].length() - 1) + splt[1].replace("_", "");
            latestVersions.put(deviceName, splt[2]);
        }
    }

    private void getLatestVersions() {
        if (this.httpClient == null)
            return;

        this.httpClient
            .newRequest("https://download.tinkerforge.com/latest_versions.txt")
            .send(new BufferingResponseListener() {
                @Override
                public void onComplete(Result result) {
                    if (result.isSucceeded()) {
                        parseLatestVersions(getContentAsString());
                        scheduler.schedule(() -> getLatestVersions(), 1, TimeUnit.HOURS);
                    } else {
                        logger.info("Failed to download latest versions: {}", result.getFailure().getMessage());
                        scheduler.schedule(() -> getLatestVersions(), 5, TimeUnit.MINUTES);
                    }
                }
            });
    }

    @Reference
    protected void setHttpClientFactory(HttpClientFactory httpClientFactory) {
        this.httpClient = httpClientFactory.createHttpClient("tinkerforge");
        try {
            this.httpClient.start();
        } catch (Exception e) {
            logger.info("Failed to start HTTP Client: {}", e.getMessage());
            return;
        }
        getLatestVersions();
    }

    protected void unsetHttpClientFactory(HttpClientFactory httpClientFactory) {
        try {
            this.httpClient.stop();
        } catch (Exception e) {
            logger.info("Failed to stop HTTP Client: {}", e.getMessage());
        }
        this.httpClient = null;
    }
}
