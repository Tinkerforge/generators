#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223

from tinkerforge.ip_connection import IPConnection

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

if __name__ == "__main__":
    # Create connection and connect to brickd
    ipcon = IPConnection()
    ipcon.connect(HOST, PORT)

    # Register Enumerate Callback
    ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE, cb_enumerate)

    # Trigger Enumerate
    ipcon.enumerate()

    raw_input("Press key to exit\n") # Use input() in Python 3
    ipcon.disconnect()
