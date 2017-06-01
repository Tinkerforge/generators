# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Motorized Linear Poti Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 267,
    'name': 'Motorized Linear Poti',
    'display_name': 'Motorized Linear Poti',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'TODO',
        'de': 'TODO'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'packets': [],
    'examples': []
}

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
    data_type = 'uint16',
    doc       = position_doc
)



com['packets'].append({
'type': 'function',
'name': 'Set Motor Position',
'elements': [('Position', 'uint16', 1, 'in'),
             ('Drive Mode', 'uint8', 1, 'in', ('Drive Mode', [('Fast', 0),
                                                              ('Smooth', 1)])),
             ('Hold Position', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Motor Position',
'elements': [('Position', 'uint16', 1, 'out'),
             ('Drive Mode', 'uint8', 1, 'out', ('Drive Mode', [('Fast', 0),
                                                               ('Smooth', 1)])),
             ('Hold Position', 'bool', 1, 'out'),
             ('Position Reached', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Calibrate',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set Position Reached Callback Configuration',
'elements': [('Enabled', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
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
'name': 'Get Position Reached Callback Configuration',
'elements': [('Enabled', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'callback',
'name': 'Position Reached',
'elements': [('Position', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
""",
'de':
"""
"""
}]
})


com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Position', 'position'), [(('Position', 'Position'), 'uint16', None, None, None, (0, 100))], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Position', 'position'), [(('Position', 'Position'), 'uint16', None, None, None, (0, 100))], None, None),
              ('callback_period', ('Position', 'position'), [], 50)]
})

