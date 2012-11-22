# -*- coding: utf-8 -*-

# Common Brick communication config

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
""",
'de':
"""
"""
}]
})

common_packets.append({
'type': 'function',
'function_id': 243,
'name': ('Reset', 'reset'),
'elements': [],
'since_firmware': {'dc': [1, 1, 3],
                   'imu': [1, 0, 7],
                   'master': [1, 2, 1],
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
'function_id': 242,
'name': ('GetChipTemperature', 'get_chip_temperature'),
'elements': [('temperature', 'int16', 1, 'out')],
'since_firmware': {'dc': [1, 1, 3],
                   'imu': [1, 0, 7],
                   'master': [1, 2, 1],
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
