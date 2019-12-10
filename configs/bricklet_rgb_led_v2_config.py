# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# RGB LED Bricklet 2.0 communication config

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2127,
    'name': 'RGB LED V2',
    'display_name': 'RGB LED 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Controls one RGB LED',
        'de': 'Steuert eine RGB LED'
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

com['packets'].append({
'type': 'function',
'name': 'Set RGB Value',
'elements': [('R', 'uint8', 1, 'in', {}),
             ('G', 'uint8', 1, 'in', {}),
             ('B', 'uint8', 1, 'in', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the *r*, *g* and *b* values for the LED.
""",
'de':
"""
Setzt die *r*, *g* und *b* Werte für die LED.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get RGB Value',
'elements': [('R', 'uint8', 1, 'out', {}),
             ('G', 'uint8', 1, 'out', {}),
             ('B', 'uint8', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the *r*, *g* and *b* values of the LED as set by :func:`Set RGB Value`.
""",
'de':
"""
Gibt die *r*, *g* und *b* Werte der LED zurück, wie von :func:`Set RGB Value` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('setter', 'Set RGB Value', [('uint8', 0), ('uint8', 170), ('uint8', 234)], 'Set light blue color', None)]
})

def percent_type_to_int(name):
    return '(int)({}.doubleValue() * 255.0 / 100.0)'.format(name)

com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.HSBType'],
    'param_groups': oh_generic_channel_param_groups(),
    'channels': [{
            'id': 'Color',
            'type': 'Color',

            'setters': [{
                'packet': 'Set RGB Value',
                'packet_params': [percent_type_to_int('cmd.getRed()'), percent_type_to_int('cmd.getGreen()'), percent_type_to_int('cmd.getBlue()'),]}],
            'setter_command_type': "HSBType",

            'getters': [{
                'packet': 'Get RGB Value',
                'transform': 'HSBType.fromRGB(value.r, value.g, value.b)'}],
        }
    ],
    'channel_types': [
        oh_generic_channel_type('Color', 'Color', 'LED Color', description='The color of the LED.',
                    update_style=None,
                    read_only=False)
    ],
    'actions': ['Get RGB Value']
}
