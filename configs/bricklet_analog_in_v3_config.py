# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Analog In 3.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 295,
    'name': 'Analog In V3',
    'display_name': 'Analog In 3.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '',
        'de': ''
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'packets': [],
    'examples': []
}

OVERSAMPLING = ('Oversampling', [('32', 0),
                                 ('64', 1),
                                 ('128', 2),
                                 ('256', 3),
                                 ('512', 4),
                                 ('1024', 5),
                                 ('2048', 6),
                                 ('4096', 7),
                                 ('8192', 8),
                                 ('16384', 9)])


voltage_doc = {
'en':
"""
Returns the measured voltage. The value is in mV and
between 0V and 42V. The resolution is approximately 10mV to 1mV.


TODO: oversampling...

""",
'de':
"""

"""
}

add_callback_value_function(
    packets   = com['packets'], 
    name      = 'Get Voltage', 
    data_name = 'Voltage',
    data_type = 'uint16',
    doc       = voltage_doc
)

com['packets'].append({
'type': 'function',
'name': 'Set Oversampling',
'elements': [('Oversampling', 'uint8', 1, 'in', OVERSAMPLING)],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""

One 12bit sample taken every 17.5us:

*32x    -> 0.56ms
*16384x -> 286ms

uses moving average principle (new value every 1ms)
TODO
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Oversampling',
'elements': [('Oversampling', 'uint8', 1, 'out', OVERSAMPLING)],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Calibration',
'elements': [('Offset', 'int16', 1, 'in'),
             ('Multiplier', 'uint16', 1, 'in'),
             ('Divisor', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Calibrated Value = (Value + Offset)*Muliplier/Divisor

Hint: Use Brick Viewer
TODO
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Calibration',
'elements': [('Offset', 'int16', 1, 'out'),
             ('Multiplier', 'uint16', 1, 'out'),
             ('Divisor', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
TODO
""",
'de':
"""
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Voltage', 'voltage'), [(('Voltage', 'Voltage'), 'uint16', 1, 1000.0, 'mV', 'V', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Voltage', 'voltage'), [(('Voltage', 'Voltage'), 'uint16', 1, 1000.0, 'mV', 'V', None)], None, None),
              ('callback_configuration', ('Voltage', 'voltage'), [], 1000, 'x', [(0, 0)])]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('Voltage', 'voltage'), [(('Voltage', 'Voltage'), 'uint16', 1, 1000.0, 'mV', 'V', None)], None, None),
              ('callback_configuration', ('Voltage', 'voltage'), [], 1000, 'o', [(5, 0)])]
})
