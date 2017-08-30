# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# RGB LED Button Bricklet communication config

com = {
    'author': 'Bastian Nordmeyer <bastian@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 282,
    'name': 'RGB LED Button',
    'display_name': 'RGB LED Button',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'RGB LED Button',
        'de': 'RGB LED Button'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Set Color',
'elements': [('Red', 'uint8', 1, 'in'),
             ('Green', 'uint8', 1, 'in'),
             ('Blue', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
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
'name': 'Get Color',
'elements': [('Red', 'uint8', 1, 'out'),
             ('Green', 'uint8', 1, 'out'),
             ('Blue', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
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
'name': 'Get Button State',
'elements': [('State', 'uint8', 1, 'out', ('Button State', [('Pressed', 0),
                                                            ('Released', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
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
'name': 'Button State Changed',
'elements': [('State', 'uint8', 1, 'out', ('Button State', [('Pressed', 0),
                                                            ('Released', 1)]))],
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

com['packets'].append({
'type': 'function',
'name': 'Set Color Calibration',
'elements': [('Red', 'uint8', 1, 'in'),
             ('Green', 'uint8', 1, 'in'),
             ('Blue', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TOOD:
range 0-100%

Is saved in flash, don't call every time.

default: 100, 100, 55
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Color Calibration',
'elements': [('Red', 'uint8', 1, 'out'),
             ('Green', 'uint8', 1, 'out'),
             ('Blue', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the *rgb* value calibrationas set by :func:`Set Color Calibration`.
""",
'de':
"""
Gibt die *rgb* Wert Kalibrierung zurück, wie von :func:`Set Color Calibration` gesetzt.
"""
}]
})
