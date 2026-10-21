#!/usr/bin/env micropython
# -*- coding: utf-8 -*-

HOST = "192.168.1.100" # Change to the IP of your PC running brickd
PORT = 4223
SECRET = "My Authentication Secret!"

# For WiFi-capable boards (e.g. ESP32), connect to your network first:
#import network
#wlan = network.WLAN(network.STA_IF)
#wlan.active(True)
#wlan.connect("YOUR_SSID", "YOUR_PASSWORD")
#while not wlan.isconnected():
#    pass
#print("Connected:", wlan.ifconfig())

# NOTE: Authentication requires the hmac module. If your MicroPython build
# does not include it, install it first:
#   import mip
#   mip.install("hmac")

from ip_connection import IPConnection

# Authenticate each time the connection got established
def cb_connected(connect_reason):
    if connect_reason == IPConnection.CONNECT_REASON_REQUEST:
        print("Connected by request")

    # Authenticate first...
    try:
        ipcon.authenticate(SECRET)
        print("Authentication succeeded")
    except:
        print("Could not authenticate")
        return

    # ...then trigger enumerate
    ipcon.enumerate()

# Print incoming enumeration
def cb_enumerate(uid, connected_uid, position, hardware_version, firmware_version,
                 device_identifier, enumeration_type):
    print("UID: " + uid + ", Enumeration Type: " + str(enumeration_type))

# Create IPConnection
ipcon = IPConnection()

# Register Connected Callback
ipcon.register_callback(IPConnection.CALLBACK_CONNECTED, cb_connected)

# Register Enumerate Callback
ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE, cb_enumerate)

# Connect to brickd
ipcon.connect(HOST, PORT)

ipcon.dispatch_callbacks(-1) # Dispatch callbacks forever
