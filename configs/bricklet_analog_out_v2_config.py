# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Analog Out Bricklet 2.0 communication config

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 256,
    'name': 'Analog Out V2',
    'display_name': 'Analog Out 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Generates configurable DC voltage between 0V and 12V',
        'de': 'Erzeugt konfigurierbare Gleichspannung zwischen 0V und 12V'
    },
    'released': True,
    'documented': True,
    'discontinued': False, # selling remaining stock, replaced by Analog Out Bricklet 3.0
    'features': [
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Set Output Voltage',
'elements': [('Voltage', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the voltage in mV. The possible range is 0V to 12V (0-12000).
""",
'de':
"""
Setzt die Spannung in mV. Der mögliche Bereich ist 0V bis 12V (0-12000).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Output Voltage',
'elements': [('Voltage', 'uint16', 1, 'out')],
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
'elements': [('Voltage', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the input voltage in mV.
""",
'de':
"""
Gibt die Eingangsspannung in mV zurück.
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
                'packet_params': [],
                'transform': 'new QuantityType<>(value{divisor}, {unit})'}],

            'java_unit': 'SmartHomeUnits.VOLT',
            'divisor': 1000.0,
            'is_trigger_channel': False
        }, {
            'id': 'Output Voltage',
            'type': 'Output Voltage',
            'getters': [{
                'packet': 'Get {title_words}',
                'packet_params': [],
                'transform': 'new QuantityType<>(value{divisor}, {unit})'}],
            'setters':[{
                'packet': 'Set {title_words}',
                'packet_params': ['(int)Math.round(cmd.doubleValue() * 1000.0)'],
            }],
            'setter_command_type': 'QuantityType',

            'java_unit': 'SmartHomeUnits.VOLT',
            'divisor': 1000.0,
            'is_trigger_channel': False
        }
    ],
    'channel_types': [
        oh_generic_channel_type('Input Voltage', 'Number:ElectricPotential', 'Input Voltage',
                     description='The input voltage',
                     read_only=True,
                     pattern='%.3f %unit%',
                     min_=0,
                     max_=15),
         oh_generic_channel_type('Output Voltage', 'Number:ElectricPotential', 'Output Voltage',
                     description='The output voltage. The possible range is 0V to 12V',
                     pattern='%.3f %unit%',
                     min_=0,
                     max_=12)
    ]
}
