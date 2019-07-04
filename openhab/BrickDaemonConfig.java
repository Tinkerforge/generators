package com.tinkerforge;

public class BrickDaemonConfig {
    public String host;
    public Integer port;

    public Boolean enableReconnect;
    public Integer reconnectInterval;

    public Boolean backgroundDiscovery;
    public Integer backgroundDiscoveryInterval;

    public Boolean auth;
    public String password;
}
