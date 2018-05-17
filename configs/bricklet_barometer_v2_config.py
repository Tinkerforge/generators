# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Barometer Bricklet 2.0 communication config

# TODO: Documentation and examples.

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
Returns the measured air pressure. The value has a range of
260000 to 1260000 and is given in mbar/1000, i.e. a value of
1001092 means that an air pressure of 1001.092 mbar is measured.
""",
'de':
"""
Gibt den Luftdruck des Luftdrucksensors zurück. Der Wertbereich
geht von 260000 bis 1260000 und ist in mbar/1000 angegeben, d.h.
bei einem Wert von 1001092 wurde ein Luftdruck von 1001,092 mbar
gemessen.
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
Returns the relative altitude of the air pressure sensor. The value
is given in mm and is calculated based on the difference between the
current air pressure and the reference air pressure that can be set
with :func:`Set Reference Air Pressure`.
""",
'de':
"""
Gibt die relative Höhe des Luftdrucksensors zurück. Der Wert ist in
mm angegeben und wird auf Basis der Differenz zwischen dem aktuellen
Luftdruck und dem Referenzluftdruck berechnet, welcher mit
:func:`Set Reference Air Pressure` gesetzt werden kann.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Altitude',
    data_name = 'Altitude',
    data_type = 'int32',
    doc       = altitude_doc
)

temperature_doc = {
'en':
"""
Returns the temperature of the air pressure sensor. The value
has a range of -4000 to 8500 and is given in °C/100, i.e. a value
of 2007 means that a temperature of 20.07 °C is measured.

This temperature is used internally for temperature compensation
of the air pressure measurement. It is not as accurate as the
temperature measured by the :ref:`temperature_bricklet` or the
:ref:`temperature_ir_bricklet`.
""",
'de':
"""
Gibt die Temperatur des Luftdrucksensors zurück. Der Wertbereich
ist von -4000 bis 8500 und ist in °C/100 angegeben, d.h. bei
einem Wert von 2007 wurde eine Temperatur von 20,07 °C gemessen.

Diese Temperatur wird intern zur Temperaturkompensation der
Luftdruckmessung verwendet. Sie ist nicht so genau wie die
Temperatur die vom :ref:`temperature_bricklet` oder dem
:ref:`temperature_ir_bricklet` gemessen wird.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Temperature',
    data_name = 'Temperature',
    data_type = 'int32',
    doc       = temperature_doc
)

com['packets'].append({
'type': 'function',
'name': 'Set Moving Average Configuration',
'elements': [('Moving Average Length Air Pressure', 'uint16', 1, 'in'),
             ('Moving Average Length Altitude', 'uint16', 1, 'in'),
             ('Moving Average Length Temperature', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
for the air pressure, altitude and temperature.

Setting the length to 1 will turn the averaging off. With less
averaging, there is more noise on the data.

The range for the averaging is 1-1000.

If you want to do long term measurements the longest moving average will give
the cleanest results.

The default value is 100.
""",
'de':
"""
Setzt die Länge eines `gleitenden Mittelwerts <https://de.wikipedia.org/wiki/Gleitender_Mittelwert>`__
für die Luftfeuchtigkeit und Temperatur.

Wenn die Länge auf 1 gesetzt wird, ist die Mittelwertbildung deaktiviert.
Desto kürzer die Länge des Mittelwerts ist, desto mehr Rauschen ist auf den Daten.

Der Wertebereich liegt bei 1-1000.

Bei Langzeitmessungen gibt ein langer Mittelwert die saubersten Resultate.

Der Standardwert ist 100.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Moving Average Configuration',
'elements': [('Moving Average Length Air Pressure', 'uint16', 1, 'out'),
             ('Moving Average Length Altitude', 'uint16', 1, 'out'),
             ('Moving Average Length Temperature', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the moving average configuration as set by
:func:`Set Moving Average Configuration`.
""",
'de':
"""
Gibt die Moving Average-Konfiguration zurück, wie von
:func:`Set Moving Average Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Reference Air Pressure',
'elements': [('Air Pressure', 'int32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the reference air pressure in mbar/1000 for the altitude calculation.
Valid values are between 260000 and 1260000. Setting the reference to the
current air pressure results in a calculated altitude of 0mm. Passing 0 is
a shortcut for passing the current air pressure as reference.

Well known reference values are the Q codes
`QNH <https://en.wikipedia.org/wiki/QNH>`__ and
`QFE <https://en.wikipedia.org/wiki/Mean_sea_level_pressure#Mean_sea_level_pressure>`__
used in aviation.

The default value is 1013.25mbar.
""",
'de':
"""
Setzt den Referenzluftdruck in mbar/1000 für die Höhenberechnung.
Gültige Werte liegen zwischen 260000 und 1260000. Wenn der aktuelle
Luftdruckwert als Referenz übergeben wird dann gibt die Höhenberechnung
0mm aus. Als Abkürzung kann auch 0 übergeben werden, dadurch wird der
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
'since_firmware': [1, 0, 0],
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

com['packets'].append({
'type': 'function',
'name': 'Set Calibration',
'elements': [('Measured Air Pressure', 'int32', 1, 'in'),
             ('Reference Air Pressure', 'int32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets one point air pressure offset calibration value. The offset
is the difference between currently measured air pressure by the
sensor and the air pressure measured by an accurate reference
barometer in mbar/1000. The values has a range of 260000 to 1260000.

After calibration the air pressure measurements will achieve accuracy
of about 0.1 mbar.
""",
'de':
"""

"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Calibration',
'elements': [('Measured Air Pressure', 'int32', 1, 'out'),
             ('Reference Air Pressure', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the air pressure offset values as set by :func:`Set Calibration`.
""",
'de':
"""
Gibt den Luftdruck offset werte zurück, wie von :func:`Set Calibration`
gesetzt.
"""
}]
})
