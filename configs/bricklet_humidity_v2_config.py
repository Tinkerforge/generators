# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Humidity Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 283,
    'name': 'Humidity V2',
    'display_name': 'Humidity 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures relative humidity',
        'de': 'Misst relative Luftfeuchtigkeit'
    },
    'comcu': True,
    'released': True,
    'documented': True,
    'packets': [],
    'examples': []
}

humidity_doc = {
'en':
"""
Returns the humidity measured by the sensor. The value
has a range of 0 to 10000 and is given in %RH/100 (Relative Humidity),
i.e. a value of 4223 means that a humidity of 42.23 %RH is measured.
""",
'de':
"""
Gibt die gemessene Luftfeuchtigkeit des Sensors zurück. Der Wertebereich ist von
0 bis 10000 und wird in %RH/100 angegeben (relative Luftfeuchtigkeit), z.B. bedeutet
ein Wert von 4223 eine gemessene Luftfeuchtigkeit von 42,23 %RH.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Humidity',
    data_name = 'Humidity',
    data_type = 'uint16',
    doc       = humidity_doc
)

temperature_doc = {
'en':
"""
Returns the temperature measured by the sensor. The value
has a range of -4000 to 16500 and is given in °C/100,
i.e. a value of 3200 means that a temperature of 32.00 °C is measured.
""",
'de':
"""
Gibt die gemessene Temperatur des Sensors zurück. Der Wertebereich ist von
-4000 bis 16500 und wird in °C/100 angegeben, z.B. bedeutet
ein Wert von 3200 eine gemessene Temperatur von 32,00 °C.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Temperature',
    data_name = 'Temperature',
    data_type = 'int16',
    doc       = temperature_doc
)

HEATER_CONFIG_CONSTANT = ('Heater Config', [('Disabled', 0),
                                            ('Enabled',  1)])

com['packets'].append({
'type': 'function',
'name': 'Set Heater Configuration',
'elements': [('Heater Config', 'uint8', 1, 'in', HEATER_CONFIG_CONSTANT)],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Enables/disables the heater. The heater can be used to dry the sensor in
extremely wet conditions.

By default the heater is disabled.
""",
'de':
"""
Aktiviert/deaktiviert das Heizelement. Das Heizelement kann genutzt werden
um den Sensor bei extremer Feuchtigkeit zu trocknen.

Standardmäßig ist das Heizelement deaktiviert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Heater Configuration',
'elements': [('Heater Config', 'uint8', 1, 'out', HEATER_CONFIG_CONSTANT)],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the heater configuration as set by :func:`Set Heater Configuration`.
""",
'de':
"""
Gibt die Heizelement-Konfiguration zurück, wie von :func:`Set Heater Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Moving Average Configuration',
'elements': [('Moving Average Length Humidity', 'uint16', 1, 'in'),
             ('Moving Average Length Temperature', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
for the humidity and temperature.

Setting the length to 1 will turn the averaging off. With less
averaging, there is more noise on the data.

The range for the averaging is 1-1000.

New data is gathered every 50ms. With a moving average of length 1000 the resulting
averaging window has a length of 50s. If you want to do long term measurements the longest
moving average will give the cleanest results.

The default value is 100.
""",
'de':
"""
Setzt die Länge eines `gleitenden Mittelwerts <https://de.wikipedia.org/wiki/Gleitender_Mittelwert>`__
für die Luftfeuchtigkeit und Temperatur.

Wenn die Länge auf 1 gesetzt wird, ist die Mittelwertbildung deaktiviert.
Desto kürzer die Länge des Mittelwerts ist, desto mehr Rauschen ist auf den Daten.

Der Wertebereich liegt bei 1-1000.

Einer neue Wert wird alle 50ms gemessen. Mit einer Mittelwerts-Länge von 1000 hat das
resultierende gleitende Fenster eine Zeitspanne von 50s. Bei Langzeitmessungen gibt
ein langer Mittelwert die saubersten Resultate.

Der Standardwert ist 100.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Moving Average Configuration',
'elements': [('Moving Average Length Humidity', 'uint16', 1, 'out'),
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

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Humidity', 'humidity'), [(('Humidity', 'Humidity'), 'uint16', 100.0, '%RH/100', '%RH', None)], [])]
})
