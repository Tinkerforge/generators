# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Analog Out Bricklet 3.0 communication config

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2115,
    'name': 'Analog Out V3',
    'display_name': 'Analog Out 3.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Generates configurable DC voltage between 0V and 12V',
        'de': 'Erzeugt konfigurierbare Gleichspannung zwischen 0V und 12V'
    },
    'released': True,
    'documented': True,
    'discontinued': False,
    'features': [
        'device',
        'comcu_bricklet',
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Set Output Voltage',
'elements': [('Voltage', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Volt', 'range': (0, 12000), 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the voltage.
""",
'de':
"""
Setzt die Spannung.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Output Voltage',
'elements': [('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt', 'range': (0, 12000), 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the voltage as set by :func:`Set Output Voltage`.
""",
'de':
"""
Gibt die Spannung zurück, wie von :func:`Set Output Voltage` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Input Voltage',
'elements': [('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt', 'range': (0, 15000)})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the input voltage.
""",
'de':
"""
Gibt die Eingangsspannung zurück.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('setter', 'Set Output Voltage', [('uint16', 3300)], 'Set output voltage to 3.3V', None)]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'channels': [{
            'id': 'Input Voltage',
            'type': 'Input Voltage',
            'getters': [{
                'packet': 'Get {title_words}',
                'element': 'Voltage',
                'packet_params': [],
                'transform': 'new {number_type}(value{divisor}{unit})'}],

        }, {
            'id': 'Output Voltage',
            'type': 'Output Voltage',
            'getters': [{
                'packet': 'Get {title_words}',
                'element': 'Voltage',
                'packet_params': [],
                'transform': 'new {number_type}(value{divisor}{unit})'}],
            'setters':[{
                'packet': 'Set {title_words}',
                'element': 'Voltage',
                'packet_params': ['(int)Math.round(cmd.doubleValue(){divisor})'],
                'command_type': 'Number',
            }],
        }
    ],
   'channel_types': [
        oh_generic_channel_type('Input Voltage', 'Number', {'en': 'Input Voltage', 'de': 'Eingangspannung'},
                    update_style=None,
                    description={'en': 'The input voltage', 'de': 'Die Ausgangsspannung'}),
         oh_generic_channel_type('Output Voltage', 'Number', {'en': 'Output Voltage', 'de': 'Ausgangspannung'},
                    update_style=None,
                    description={'en': 'The output voltage. The possible range is 0V to 12V',
                                 'de': 'Die Ausgangsspannung. Der mögliche Wertebereich ist 0V bis 12V.'})
    ],
    'actions': [{'fn': 'Set Output Voltage', 'refreshs': ['Output Voltage']}, 'Get Output Voltage', 'Get Input Voltage']
}
