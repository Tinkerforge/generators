# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Moisture Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 287,
    'name': 'Moisture V2',
    'display_name': 'Moisture 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures soil moisture',
        'de': 'Misst Erdfeuchtigkeit'
    },
    'released': False,
    'documented': False,
    'packets': [],
    'examples': []
}

moisture_doc = {
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
    name      = 'Get Moisture', 
    data_name = 'Moisture',
    data_type = 'uint16',
    doc       = moisture_doc
)

