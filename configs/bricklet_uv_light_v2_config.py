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

uv_type_a_doc = {
'en':
"""
Returns the UV light type A intensity of the sensor, the intensity is given
in µW/cm².

If you want to get the intensity periodically, it is recommended to use the
:cb:`UV Type A` callback and set the period with
:func:`Set UV Type A Callback Configuration`.
""",
'de':
"""
Gibt die UV-Licht Type A Intensität des Sensors zurück. Die Intensität wird
in der Einheit µW/cm² gegeben.

Wenn die Intensität periodisch abgefragt werden soll, wird empfohlen
den :cb:`UV Type A` Callback zu nutzen und die Periode mit
:func:`Set UV Type A Callback Configuration` vorzugeben.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get UV Type A',
    data_name = 'UV Type A',
    data_type = 'uint32',
    doc       = uv_type_a_doc
)

uv_type_b_doc = {
'en':
"""
Returns the UV light type B intensity of the sensor, the intensity is given
in µW/cm².

If you want to get the intensity periodically, it is recommended to use the
:cb:`UV Type B` callback and set the period with
:func:`Set UV Type B Callback Configuration`.
""",
'de':
"""
Gibt die UV-Licht Type B Intensität des Sensors zurück. Die Intensität wird
in der Einheit µW/cm² gegeben.

Wenn die Intensität periodisch abgefragt werden soll, wird empfohlen
den :cb:`UV Type B` Callback zu nutzen und die Periode mit
:func:`Set UV Type B Callback Configuration` vorzugeben.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get UV Type B',
    data_name = 'UV Type B',
    data_type = 'uint32',
    doc       = uv_type_b_doc
)
