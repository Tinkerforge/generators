# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Common Brick communication config

common_packets = []

common_packets.append({
'type': 'function',
'function_id': 241,
'name': ('GetProtocol1BrickletName', 'get_protocol1_bricklet_name'), 
'elements': [('port', 'char', 1, 'in'),
             ('protocol_version', 'uint8', 1, 'out'),
             ('firmware_version', 'uint8', 3, 'out'),
             ('name', 'string', 40, 'out')], 
'since_firmware': {'*': [2, 0, 0],
                   'dc': [2, 0, 0],
                   'imu': [2, 0, 0],
                   'master': [2, 0, 0],
                   'red': None,
                   'servo': [2, 0, 0],
                   'stepper': [2, 0, 0]},
'doc': ['af', {
'en':
"""
Returns the firmware and protocol version and the name of the Bricklet for a
given port.

This functions sole purpose is to allow automatic flashing of v1.x.y Bricklet
plugins.
""",
'de':
"""
Gibt die Firmware und Protokoll Version und den Namen des Bricklets für einen
gegebenen Port zurück.

Der einzige Zweck dieser Funktion ist es, automatischen Flashen von Bricklet
v1.x.y Plugins zu ermöglichen.
"""
}]
})

common_packets.append({
'type': 'function',
'function_id': 242,
'name': ('GetChipTemperature', 'get_chip_temperature'),
'elements': [('temperature', 'int16', 1, 'out')],
'since_firmware': {'*': [2, 0, 0],
                   'dc': [1, 1, 3],
                   'imu': [1, 0, 7],
                   'master': [1, 2, 1],
                   'red': None,
                   'servo': [1, 1, 3],
                   'stepper': [1, 1, 4]},
'doc': ['af', {
'en':
"""
Returns the temperature in °C/10 as measured inside the microcontroller. The
value returned is not the ambient temperature!

The temperature is only proportional to the real temperature and it has an
accuracy of +-15%. Practically it is only useful as an indicator for
temperature changes.
""",
'de':
"""
Gibt die Temperatur in °C/10, gemessen im Mikrocontroller, aus. Der
Rückgabewert ist nicht die Umgebungstemperatur.

Die Temperatur ist lediglich proportional zur echten Temperatur und hat eine
Genauigkeit von +-15%. Daher beschränkt sich der praktische Nutzen auf die
Indikation von Temperaturveränderungen.
"""
}]
})

common_packets.append({
'type': 'function',
'function_id': 243,
'name': ('Reset', 'reset'),
'elements': [],
'since_firmware': {'*': [2, 0, 0],
                   'dc': [1, 1, 3],
                   'imu': [1, 0, 7],
                   'master': [1, 2, 1],
                   'red': None,
                   'servo': [1, 1, 3],
                   'stepper': [1, 1, 4]},
'doc': ['af', {
'en':
"""
Calling this function will reset the Brick. Calling this function
on a Brick inside of a stack will reset the whole stack.

After a reset you have to create new device objects,
calling functions on the existing ones will result in
undefined behavior!
""",
'de':
"""
Ein Aufruf dieser Funktion setzt den Brick zurück. Befindet sich der Brick
innerhalb eines Stapels wird der gesamte Stapel zurück gesetzt.

Nach dem Zurücksetzen ist es notwendig neue Geräteobjekte zu erzeugen,
Funktionsaufrufe auf bestehende führt zu undefiniertem Verhalten.
"""
}]
})

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
'prototype_in_device': True,
'doc': ['af', {
'en':
"""
Returns the UID, the UID where the Brick is connected to, 
the position, the hardware and firmware version as well as the
device identifier.

The position can be '0'-'8' (stack position).

The device identifier numbers can be found :ref:`here <device_identifier>`.
|device_identifier_constant|
""",
'de':
"""
Gibt die UID, die UID zu der der Brick verbunden ist, die
Position, die Hard- und Firmware Version sowie den Device Identifier
zurück.

Die Position kann '0'-'8' (Stack Position) sein.

Eine Liste der Device Identifier Werte ist :ref:`hier <device_identifier>` zu
finden. |device_identifier_constant|
"""
}]
})
