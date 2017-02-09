# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Common Bricklet communication config

common_packets = []

common_packets.append({
'type': 'function',
'function_id': 255,
'name': 'Get Identity',
'elements': [('Uid', 'string', 8, 'out'),
             ('Connected Uid', 'string', 8, 'out'),
             ('Position', 'char', 1, 'out'),
             ('Hardware Version', 'uint8', 3, 'out'),
             ('Firmware Version', 'uint8', 3, 'out'),
             ('Device Identifier', 'uint16', 1, 'out')],
'since_firmware': {'*': [2, 0, 0]},
'prototype_in_device': True,
'doc': ['af', {
'en':
"""
Returns the UID, the UID where the Bricklet is connected to,
the position, the hardware and firmware version as well as the
device identifier.

The position can be 'a', 'b', 'c' or 'd'.

The device identifier numbers can be found :ref:`here <device_identifier>`.
|device_identifier_constant|
""",
'de':
"""
Gibt die UID, die UID zu der das Bricklet verbunden ist, die
Position, die Hard- und Firmware Version sowie den Device Identifier
zurück.

Die Position kann 'a', 'b', 'c' oder 'd' sein.

Eine Liste der Device Identifier Werte ist :ref:`hier <device_identifier>` zu
finden. |device_identifier_constant|
"""
}]
})
