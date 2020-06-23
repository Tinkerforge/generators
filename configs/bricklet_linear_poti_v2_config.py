# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Linear Poti Bricklet 2.0 communication config

from generators.configs.commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from generators.configs.commonconstants import add_callback_value_function

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2139,
    'name': 'Linear Poti V2',
    'display_name': 'Linear Poti 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '59mm linear potentiometer',
        'de': '59mm Linearpotentiometer'
    },
    'released': True,
    'documented': True,
    'discontinued': False,
    'features': [
        'comcu_bricklet',
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

position_doc = {
'en':
"""
Returns the position of the linear potentiometer. The value is
between 0 (slider down) and 100 (slider up).
""",
'de':
"""
Gibt die Position des Linearpotentiometers zurück. Der Wertebereich
ist von 0 (Schieberegler unten) und 100 (Schieberegler oben).
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Position',
    data_name = 'Position',
    data_type = 'uint8',
    doc       = position_doc,
    range_    = (0, 100)
)

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Position', 'position'), [(('Position', 'Position'), 'uint8', 1, None, '°', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Position', 'position'), [(('Position', 'Position'), 'uint8', 1, None, '°', None)], None, None),
              ('callback_configuration', ('Position', 'position'), [], 250, False, 'x', [(0, 0)])]
})


com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'channels': [
        oh_generic_channel('Position', 'Position')
    ],
    'channel_types': [
        oh_generic_channel_type('Position', 'Number', 'Position',
                    update_style='Callback Configuration',
                    description='The position of the linear potentiometer. The value is between 0 (slider down) and 100 (slider up).')
    ],
    'actions': ['Get Position']
}
