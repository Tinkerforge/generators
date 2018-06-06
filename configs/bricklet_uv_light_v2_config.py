# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# UV Light Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

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

uva_light_doc = {
'en':
"""
Returns the UVA light intensity of the sensor, the intensity is given
in µW/cm².

UVA light index (UVAI) can be calculated as:
UVAI = ((UVA * 2) / 9) * 0.01

If you want to get the intensity periodically, it is recommended to use the
:cb:`UVA Light` callback and set the period with
:func:`Set UVA Light Callback Configuration`.
""",
'de':
"""
Gibt die UVA Licht Intensität des Sensors zurück. Die Intensität wird
in der Einheit µW/cm² gegeben.

Der UVA Licht Index (UVAI) kann wie folgt berechnet werden:
UVAI = ((UVA * 2) / 9) * 0.01

Wenn die Intensität periodisch abgefragt werden soll, wird empfohlen
den :cb:`UVA Light` Callback zu nutzen und die Periode mit
:func:`Set UVA Light Callback Configuration` vorzugeben.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get UVA Light',
    data_name = 'UVA Light',
    data_type = 'uint32',
    doc       = uva_light_doc
)

uvb_light_doc = {
'en':
"""
Returns the UVB light intensity of the sensor, the intensity is given
in µW/cm².

UVB light index (UVBI) can be calculated as:
UVBI = ((UVB * 4) / 8) * 0.01

If you want to get the intensity periodically, it is recommended to use the
:cb:`UVB Light` callback and set the period with
:func:`Set UVB Light Callback Configuration`.
""",
'de':
"""
Gibt die UVB Licht Intensität des Sensors zurück. Die Intensität wird
in der Einheit µW/cm² gegeben.

Der UVB Licht Index (UVBI) kann wie folgt berechnet werden:
UVBI = ((UVB * 4) / 8) * 0.01

Wenn die Intensität periodisch abgefragt werden soll, wird empfohlen
den :cb:`UVB Light` Callback zu nutzen und die Periode mit
:func:`Set UVB Light Callback Configuration` vorzugeben.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get UVB Light',
    data_name = 'UVB Light',
    data_type = 'uint32',
    doc       = uvb_light_doc
)
