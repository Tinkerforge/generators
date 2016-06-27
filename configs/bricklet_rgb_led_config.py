# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# RGB LED Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 271,
    'name': ('RGB LED', 'RGB LED', 'RGB LED Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Controls one RGB LED',
        'de': 'Steuert eine RGB LED'
    },
    'released': False,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Set RGB Value',
'elements': [('R', 'uint8', 1, 'in'),
             ('G', 'uint8', 1, 'in'),
             ('B', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the *rgb* value for the LED.
""",
'de':
"""
Setzt den *rgb* Wert für die LED.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get RGB Value',
'elements': [('R', 'uint8', 1, 'out'),
             ('G', 'uint8', 1, 'out'),
             ('B', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the *rgb* value of the LED as set by :func:`SetRGBValues`.
""",
'de':
"""
Gibt den *rgb* Wert der LED zurück, wie von :func:`SetRGBValue` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('setter', 'Set RGB Value', [('uint8', 0), ('uint8', 170), ('uint8', 234)], 'Set light blue color', None)]
})
