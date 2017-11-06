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
Sets the color of the LED.

By default the LED is off (0, 0, 0).
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
Returns the LED color as set by :func:`Set Color`.
""",
'de':
"""
Gibt die LED-Farbe zurück, wie von :func:`Set Color` gesetzt.
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
Returns the current state of the button (either pressed or released).
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
This callback is triggered every time the button state changes from pressed to released
or from released to pressed.

The parameter `state` is the current state of the button.
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
'doc': ['af', {
'en':
"""
Sets a color calibration. Some colors appear brighter then others,
so a calibration may be necessary for nice uniform colors.

The values range from 0-100%.

The calibration is saved in flash. You don't need to call this
function on every startup.

Default values: (100, 100, 55).
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
Returns the color calibration as set by :func:`Set Color Calibration`.
""",
'de':
"""
Gibt die Farbwert-Kalibrierung zurück, wie von :func:`Set Color Calibration` gesetzt.
"""
}]
})
