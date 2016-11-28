# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Common Bricklet communication config

common_packets = []

common_packets.append({
'type': 'function',
'function_id': 234,
'name': 'Get SPITFP Error Count',
'elements': [('Error Count Ack Checksum', 'uint32', 1, 'out'),
             ('Error Count Message Checksum', 'uint32', 1, 'out'),
             ('Error Count Frame', 'uint32', 1, 'out'),
             ('Error Count Overflow', 'uint32', 1, 'out')],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['af', {
'en':
"""

""",
'de':
"""

"""
}]
})

common_packets.append({
'type': 'function',
'function_id': 235,
'name': 'Set Bootloader Mode',
'elements': [('Mode', 'uint8', 1, 'in'),
             ('Status', 'uint8', 1, 'out')],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['af', {
'en':
"""

""",
'de':
"""

"""
}]
})

common_packets.append({
'type': 'function',
'function_id': 236,
'name': 'Get Bootloader Mode',
'elements': [('Mode', 'uint8', 1, 'out')],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['af', {
'en':
"""

""",
'de':
"""

"""
}]
})


common_packets.append({
'type': 'function',
'function_id': 237,
'name': 'Set Write Firmware Pointer',
'elements': [('Pointer', 'uint32', 1, 'in')],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['af', {
'en':
"""

""",
'de':
"""

"""
}]
})



common_packets.append({
'type': 'function',
'function_id': 238,
'name': 'Write Firmware',
'elements': [('Data', 'uint8', 64, 'in'),
             ('Status', 'uint8', 1, 'out')],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['af', {
'en':
"""

""",
'de':
"""

"""
}]
})


common_packets.append({
'type': 'function',
'function_id': 239,
'name': 'Set Status LED Config',
'elements': [('Config', 'uint8', 1, 'in', ('Status LED Config', [('Off', 0),
                                                                 ('On', 1),
                                                                 ('Show Status', 2)]))],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['af', {
'en':
"""

""",
'de':
"""

"""
}]
})

common_packets.append({
'type': 'function',
'function_id': 240,
'name': 'Get Status LED Config',
'elements': [('Config', 'uint8', 1, 'out', ('Status LED Config', [('Off', 0),
                                                                  ('On', 1),
                                                                  ('Show Status', 2)]))],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['af', {
'en':
"""

""",
'de':
"""

"""
}]
})

common_packets.append({
'type': 'function',
'function_id': 242,
'name': 'Get Chip Temperature',
'elements': [('Temperature', 'int16', 1, 'out')],
'since_firmware': {'*': [1, 0, 0]},
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
'name': 'Reset',
'elements': [],
'since_firmware': {'*': [1, 0, 0]},
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

