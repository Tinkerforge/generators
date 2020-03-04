package org.eclipse.smarthome.binding.tinkerforge.internal.device;

import java.math.BigDecimal;

public class BrickDaemonConfig {
    public String host = "localhost";
    public Integer port = 4223;

    public Boolean backgroundDiscovery = true;
    public BigDecimal backgroundDiscoveryInterval = BigDecimal.valueOf(10.0);

    public Boolean auth = false;
    public String password = "";
}
