# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Distance IR Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2125,
    'name': 'Distance IR V2',
    'display_name': 'Distance IR 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures distance up to 150cm with infrared light',
        'de': 'Misst Entfernung bis zu 150cm mit Infrarot-Licht'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'discontinued': False,
    'packets': [],
    'examples': []
}


distance_doc = {
'en':
"""
""",
'de':
"""
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Distance',
    data_name = 'Distance',
    data_type = 'uint16',
    doc       = distance_doc
)
