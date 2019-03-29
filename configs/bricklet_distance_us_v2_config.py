# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Distance US Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 299,
    'name': 'Distance US V2',
    'display_name': 'Distance US 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '',
        'de': ''
    },
    'released': False, # FIXME: update Distance US Bricklet (1.0) replacement recommendation, once this Bricklet is released
    'documented': False,
    'discontinued': False,
    'features': [
        'comcu_bricklet',
        'bricklet_get_identity'
    ],
    'packets': [],
    'examples': []
}

distance_doc = {
'en':
"""
Returns the distance in cm.
""",
'de':
"""
Gibt die Distanz in cm zurück.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Distance',
    data_name = 'Distance',
    data_type = 'uint16',
    doc       = distance_doc
)

