# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Rotary Poti Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from commonconstants import add_callback_value_function

from openhab_commonconfig import *
com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2140,
    'name': 'Rotary Poti V2',
    'display_name': 'Rotary Poti 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '300° rotary potentiometer',
        'de': '300° Drehpotentiometer'
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
Returns the position of the rotary potentiometer. The value is
between -150° (turned left) and 150° (turned right).
""",
'de':
"""
Gibt die Position des Drehpotentiometers zurück. Der Wertebereich ist
von -150° (links gedreht) und 150° (rechts gedreht).
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Position',
    data_name = 'Position',
    data_type = 'int16',
    doc       = position_doc,
    unit      = 'Degree',
    range_    = (-150, 150)
)

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Position', 'position'), [(('Position', 'Position'), 'int16', 1, None, '°', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Position', 'position'), [(('Position', 'Position'), 'int16', 1, None, '°', None)], None, None),
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
                    description='The position of the rotary potentiometer. The value is and between -150° (turned left) and 150° (turned right).',
                    read_only=True,
                    pattern='%d %unit%',
                    min_=-150,
                    max_=150)
    ],
    'actions': ['Get Position']
}
