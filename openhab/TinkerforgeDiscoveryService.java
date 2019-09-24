package org.eclipse.smarthome.binding.tinkerforge.discovery;

import org.eclipse.smarthome.config.discovery.DiscoveryService;

public interface TinkerforgeDiscoveryService extends DiscoveryService {
    public void stopDiscovery();
}
