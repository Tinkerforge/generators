#!/usr/bin/env python3

HOST = "localhost"
PORT = 5555
UID = "CTV1" # Change XYZ to the UID of your Common Test Bricklet

from ip_connection import IPConnection
from bricklet_common_test import BrickletCommonTest

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    ct = BrickletCommonTest(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    for set_value in range(-128, 128):
        ct.set_int8_value(set_value)
        get_value = ct.get_int8_value()

        if get_value != set_value:
            print("Int8 Value:", get_value, "!=", set_value)
        else:
            print("Int8 Value:", get_value)

    input("Press key to exit\n") # Use raw_input() in Python 2
    ipcon.disconnect()
