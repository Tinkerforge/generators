package org.eclipse.smarthome.binding.tinkerforge.internal.device;

public class BrickDaemonConfig {
    public String host;
    public Integer port;

    public Boolean backgroundDiscovery;
    public Integer backgroundDiscoveryInterval;

    public Boolean auth;
    public String password;
}
