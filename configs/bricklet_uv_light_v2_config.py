# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# UV Light Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

# TODO: Examples.

com = {
    'author': 'Ishraq Ibne Ashraf <ishraq@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2118,
    'name': 'UV Light V2',
    'display_name': 'UV Light 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures UV light',
        'de': 'Misst UV-Licht'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'discontinued': False,
    'packets': [],
    'examples': []
}

uv_light_doc = {
'en':
"""
Returns the UV light intensity of the sensor, the intensity is given
in µW/cm².

To get UV Index you have to divide the value by 250. For example, a UV Light
intensity of 500µW/cm² is equivalent to an UV Index of 2.

If you want to get the intensity periodically, it is recommended to use the
:cb:`UV Light` callback and set the period with
:func:`Set UV Light Callback Configuration`.
""",
'de':
"""
Gibt die UV-Licht-Intensität des Sensors zurück. Die Intensität wird
in der Einheit µW/cm² gegeben.

Die Intensität kann einfach durch 250 geteilt werden um den UV Index zu
bestimmen. Beispiel: Eine UV-Licht-Intensität von 500µW/cm² entspricht
einem UV Index von 2.

Wenn die Intensität periodisch abgefragt werden soll, wird empfohlen
den :cb:`UV Light` Callback zu nutzen und die Periode mit
:func:`Set UV Light Callback Configuration` vorzugeben.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get UV Light',
    data_name = 'UV Light',
    data_type = 'uint32',
    doc       = uv_light_doc
)

'''
com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get UV Light', 'UV light'), [(('UV Light', 'UV Light'), 'uint32', 1, None, 'µW/cm²', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('UV Light', 'UV light'), [(('UV Light', 'UV Light'), 'uint32', 1, None, 'µW/cm²', None)], None, None),
              ('callback_period', ('UV Light', 'UV light'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('UV Light Reached', 'UV light reached'), [(('UV Light', 'UV Light'), 'uint32', 1, None, 'µW/cm²', None)], None, 'UV Index > 3. Use sunscreen!'),
              ('callback_threshold', ('UV Light', 'UV light'), [], '>', [(250*3, 0)])]
})
'''
