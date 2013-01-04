# -*- coding: utf-8 -*-

# Common Bricklet communication config

common_packets = []

common_packets.append({
'type': 'function',
'function_id': 255,
'name': ('GetIdentity', 'get_identity'),
'elements': [('uid', 'string', 8, 'out'),
             ('connected_uid', 'string', 8, 'out'),
             ('position', 'char', 1, 'out'),
             ('hardware_version', 'uint8', 3, 'out'),
             ('firmware_version', 'uint8', 3, 'out'),
             ('device_identifier', 'uint16', 1, 'out')],
'since_firmware': {'*': [2, 0, 0]},
'doc': ['af', {
'en':
"""
Returns the UID, the UID where the Bricklet is connected to, 
the position, the hardware and firmware version as well as the
device identifier.

The position can be 'a', 'b', 'c' or 'd'.

The device identifiers are:

.. csv-table::
 :header: "Device Identifier", "Device Name"
 :widths: 30, 100

 "11", "Brick DC"
 "12", "Brick Debug"
 "13", "Brick Master"
 "14", "Brick Servo"
 "15", "Brick Stepper"
 "16", "Brick IMU"
 "", ""
 "21", "Bricklet Ambient Light"
 "22", "Bricklet Breakout"
 "23", "Bricklet Current12"
 "24", "Bricklet Current25"
 "25", "Bricklet Distance IR"
 "26", "Bricklet Dual Relay"
 "27", "Bricklet Humidity"
 "28", "Bricklet IO-16"
 "29", "Bricklet IO-4"
 "210", "Bricklet Joystick"
 "211", "Bricklet LCD 16x2"
 "212", "Bricklet LCD 20x4"
 "213", "Bricklet Linear Poti"
 "214", "Bricklet Piezo Buzzer"
 "215", "Bricklet Rotary Poti"
 "216", "Bricklet Temperature"
 "217", "Bricklet Temperature IR"
 "218", "Bricklet Voltage"
 "219", "Bricklet Analog In"
 "220", "Bricklet Analog Out"
 "221", "Bricklet Barometer"
 "222", "Bricklet GPS"
 "223", "Bricklet Industrial Digital In 4"
 "224", "Bricklet Industrial Digital Out 4"
 "225", "Bricklet Industrial Quad Relay"
 "226", "Bricklet PTC"
 "227", "Bricklet Voltage/Current"
""",
'de':
"""
Gibt die UID, die UID zu der das Bricklet verbunden ist, die
Position, die Hard- und Firmware Version sowie den Device Identifier
zurück.

Die Position kann 'a', 'b', 'c' oder 'd' sein.

Die Device Identifiers sind:

.. csv-table::
 :header: "Device Identifier", "Device Name"
 :widths: 30, 100

 "11", "Brick DC"
 "13", "Brick Master"
 "14", "Brick Servo"
 "15", "Brick Stepper"
 "16", "Brick IMU"
 "", ""
 "21", "Bricklet Ambient Light"
 "23", "Bricklet Current12"
 "24", "Bricklet Current25"
 "25", "Bricklet Distance IR"
 "26", "Bricklet Dual Relay"
 "27", "Bricklet Humidity"
 "28", "Bricklet IO-16"
 "29", "Bricklet IO-4"
 "210", "Bricklet Joystick"
 "211", "Bricklet LCD 16x2"
 "212", "Bricklet LCD 20x4"
 "213", "Bricklet Linear Poti"
 "214", "Bricklet Piezo Buzzer"
 "215", "Bricklet Rotary Poti"
 "216", "Bricklet Temperature"
 "217", "Bricklet Temperature IR"
 "218", "Bricklet Voltage"
 "219", "Bricklet Analog In"
 "220", "Bricklet Analog Out"
 "221", "Bricklet Barometer"
 "222", "Bricklet GPS"
 "223", "Bricklet Industrial Digital In 4"
 "224", "Bricklet Industrial Digital Out 4"
 "225", "Bricklet Industrial Quad Relay"
 "226", "Bricklet PTC"
 "227", "Bricklet Voltage/Current"
"""
}]
})
