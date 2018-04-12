# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Barometer Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

com = {
    'author': 'Ishraq Ibne Ashraf <ishraq@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2117,
    'name': 'Barometer V2',
    'display_name': 'Barometer 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures air pressure and altitude changes',
        'de': 'Misst Luftdruck und Höhenänderungen'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'discontinued': False,
    'packets': [],
    'examples': []
}

air_pressure_doc = {
'en':
"""

""",
'de':
"""

"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Air Pressure',
    data_name = 'Air Pressure',
    data_type = 'int32',
    doc       = air_pressure_doc
)

altitude_doc = {
'en':
"""

""",
'de':
"""

"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Altitude',
    data_name = 'Altitude',
    data_type = 'int32',
    doc       = altitude_doc
)

com['packets'].append({
'type': 'function',
'name': 'Get Temperature',
'elements': [('Temperature', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""

""",
'de':
"""

"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Moving Average Configuration',
'elements': [('Moving Average Length Air Pressure', 'uint16', 1, 'in'),
             ('Moving Average Length Temperature', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
for the air pressure and temperature.

Setting the length to 1 will turn the averaging off. With less
averaging, there is more noise on the data.

The range for the averaging is 1-1000. The default value is 100.
""",
'de':
"""
Setzt die Länge eines `gleitenden Mittelwerts <https://de.wikipedia.org/wiki/Gleitender_Mittelwert>`__
für die Luftfeuchtigkeit und Temperatur.

Wenn die Länge auf 1 gesetzt wird, ist die Mittelwertbildung deaktiviert.
Desto kürzer die Länge des Mittelwerts ist, desto mehr Rauschen ist auf den Daten.

Der Wertebereich liegt bei 1-1000. Der Standardwert ist 100.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Moving Average Configuration',
'elements': [('Moving Average Length Air Pressure', 'uint16', 1, 'out'),
             ('Moving Average Length Temperature', 'uint16', 1, 'out')],

'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the moving average configuration as set by :func:`Set Moving Average Configuration`.
""",
'de':
"""
Gibt die Moving Average-Konfiguration zurück, wie von :func:`Set Moving Average Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Reference Air Pressure',
'elements': [('Air Pressure', 'int32', 1, 'in')],
'since_firmware': [1, 1, 0],
'doc': ['bf', {
'en':
"""
Sets the reference air pressure in mbar/1000 for the altitude calculation.
Valid values are between 10000 and 1200000.
Setting the reference to the current air pressure results in a calculated
altitude of 0cm. Passing 0 is a shortcut for passing the current air pressure as
reference.

Well known reference values are the Q codes
`QNH <https://en.wikipedia.org/wiki/QNH>`__ and
`QFE <https://en.wikipedia.org/wiki/Mean_sea_level_pressure#Mean_sea_level_pressure>`__
used in aviation.

The default value is 1013.25mbar.
""",
'de':
"""
Setzt den Referenzluftdruck in mbar/1000 für die Höhenberechnung.
Gültige Werte liegen zwischen 10000 und 1200000. Wenn der
aktuelle Luftdruckwert als Referenz übergeben wird dann gibt die Höhenberechnung
0cm aus. Als Abkürzung kann auch 0 übergeben werden, dadurch wird der
Referenzluftdruck intern auf den aktuellen Luftdruckwert gesetzt.

Wohl bekannte Referenzluftdruckwerte, die in der Luftfahrt verwendet werden, sind
`QNH <https://de.wikipedia.org/wiki/Barometrische_H%C3%B6henmessung_in_der_Luftfahrt#QNH>`__ und
`QFE <https://de.wikipedia.org/wiki/Barometrische_H%C3%B6henmessung_in_der_Luftfahrt#QFE>`__
aus dem Q-Schlüssel.

Der Standardwert ist 1013,25mbar.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Reference Air Pressure',
'elements': [('Air Pressure', 'int32', 1, 'out')],
'since_firmware': [1, 1, 0],
'doc': ['bf', {
'en':
"""
Returns the reference air pressure as set by :func:`Set Reference Air Pressure`.
""",
'de':
"""
Gibt den Referenzluftdruckwert zurück, wie von :func:`Set Reference Air Pressure`
gesetzt.
"""
}]
})
