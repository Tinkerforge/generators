# -*- coding: utf-8 -*-

# Common communication config

common_packets = []

common_packets.append({
'type': 'function',
'function_id': 243,
'name': ('Reset', 'reset'),
'elements': [],
'doc': ['am', {
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
'doc': ['am', {
'en':
"""
Returns the temperature in °C/10 as measured inside the microcontroller. The
value returned is not the ambient temperature!

The temperature has an accuracy of +-15%. Practically it is only useful as
an indicator for temperature changes.
""",
'de':
"""
Gibt die Temperatur in °C/10, gemessen im Microcontroller, aus. Der Rückgabewert
ist nicht die Umgebungstemperatur.

Die Genauigkeit der Temperatur beträgt +-15%. Daher beschränkt sich der praktische
Nutzen auf die Indikation von Temperaturveränderungen.
"""
}]
})
