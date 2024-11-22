#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
SECRET = "My Authentication Secret!"

from tinkerforge.ip_connection import IPConnection

# Authenticate each time the connection got (re-)established
def cb_connected(connect_reason):
    if connect_reason == IPConnection.CONNECT_REASON_REQUEST:
        print("Connected by request")
    elif connect_reason == IPConnection.CONNECT_REASON_AUTO_RECONNECT:
        print("Auto-Reconnect")

    # Authenticate first...
    try:
        ipcon.authenticate(SECRET)
        print("Authentication succeeded")
    except:
        print("Could not authenticate")
        return

    # ...reenable auto reconnect mechanism, as described below...
    ipcon.set_auto_reconnect(True)

    # ...then trigger enumerate
    ipcon.enumerate()

# Print incoming enumeration
def cb_enumerate(uid, connected_uid, position, hardware_version, firmware_version,
                 device_identifier, enumeration_type):
    print("UID: " + uid + ", Enumeration Type: " + str(enumeration_type))

if __name__ == "__main__":
    # Create IPConnection
    ipcon = IPConnection()

    # Disable auto reconnect mechanism, in case we have the wrong secret.
    # If the authentication is successful, reenable it.
    ipcon.set_auto_reconnect(False)

    # Register Connected Callback
    ipcon.register_callback(IPConnection.CALLBACK_CONNECTED, cb_connected)

    # Register Enumerate Callback
    ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE, cb_enumerate)

    # Connect to brickd
    ipcon.connect(HOST, PORT)

    input("Press key to exit\n") # Use raw_input() in Python 2
    ipcon.disconnect()
