#!/usr/bin/env micropython
# -*- coding: utf-8 -*-

HOST = "192.168.1.100" # Change to the IP of your PC running brickd
PORT = 4223

# For WiFi-capable boards (e.g. ESP32), connect to your network first:
#import network
#wlan = network.WLAN(network.STA_IF)
#wlan.active(True)
#wlan.connect("YOUR_SSID", "YOUR_PASSWORD")
#while not wlan.isconnected():
#    pass
#print("Connected:", wlan.ifconfig())

from ip_connection import IPConnection

# Print incoming enumeration
def cb_enumerate(uid, connected_uid, position, hardware_version, firmware_version,
                 device_identifier, enumeration_type):
    print("UID:               " + uid)
    print("Enumeration Type:  " + str(enumeration_type))

    if enumeration_type == IPConnection.ENUMERATION_TYPE_DISCONNECTED:
        print("")
        return

    print("Connected UID:     " + connected_uid)
    print("Position:          " + position)
    print("Hardware Version:  " + str(hardware_version))
    print("Firmware Version:  " + str(firmware_version))
    print("Device Identifier: " + str(device_identifier))
    print("")

# Create connection and connect to brickd
ipcon = IPConnection()
ipcon.connect(HOST, PORT)

# Register Enumerate Callback
ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE, cb_enumerate)

# Trigger Enumerate
ipcon.enumerate()

ipcon.dispatch_callbacks(-1) # Dispatch callbacks forever
