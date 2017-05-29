# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Humidity Bricklet communication config

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
    'released': False,
    'documented': False,
    'packets': [],
    'examples': []
}

humidity_doc = {
'en':
"""
Returns the humidity of the sensor. The value
has a range of 0 to 1000 and is given in %RH/10 (Relative Humidity),
i.e. a value of 421 means that a humidity of 42.1 %RH is measured.
""",
'de':
"""
Gibt die gemessene Luftfeuchtigkeit des Sensors zurück. Der Wertebereich ist von
0 bis 1000 und wird in %RH/10 angegeben (relative Luftfeuchtigkeit), z.B. bedeutet
ein Wert von 421 eine gemessene Luftfeuchtigkeit von 42,1 %RH.
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
TODO
""",
'de':
"""
TODO
"""
}

add_callback_value_function(
    packets   = com['packets'], 
    name      = 'Get Temperature', 
    data_name = 'Temperature',
    data_type = 'uint16',
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
""",
'de':
"""
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
""",
'de':
"""
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
""",
'de':
"""
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
""",
'de':
"""
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Humidity', 'humidity'), [(('Humidity', 'Humidity'), 'uint16', 10.0, '%RH/10', '%RH', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Humidity', 'humidity'), [(('Humidity', 'Humidity'), 'uint16', 10.0, '%RH/10', '%RH', None)], None, None),
              ('callback_period', ('Humidity', 'humidity'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('Humidity Reached', 'humidity reached'), [(('Humidity', 'Humidity'), 'uint16', 10.0, '%RH/10', '%RH', None)], None, 'Recommended humiditiy for human comfort is 30 to 60 %RH.'),
              ('callback_threshold', ('Humidity', 'humidity'), [], 'o', [(30, 60)])]
})
