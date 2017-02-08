# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# GPS Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 278,
    'name': 'Thermal Imaging',
    'display_name': 'Thermal Imaging',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '60x80 pixel thermal imaging camera',
        'de': '60x80 Pixel Wärmebildkamera'
    },
    'has_comcu': True,
    'released': False,
    'documented': False,
    'packets': [],
    'examples': []
}


com['packets'].append({
'type': 'function',
'name': 'Set Callback Config',
'elements': [('Callback Config', 'uint8', 1, 'in')],
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
'name': 'Get Callback Config',
'elements': [('Callback Config', 'uint8', 1, 'out')],
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
'name': 'Grey Scale Image Low Level',
'elements': [('Stream Chunk Offset', 'uint16', 1, 'out'),
             ('Stream Chunk Data', 'uint8', 62, 'out')],
'high_level': {'stream_out': {'fixed_total_length': 60*80}},
'since_firmware': [1, 0, 0],
'doc': ['llc', {
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
'name': 'Temperature Image Low Level',
'elements': [('Stream Chunk Offset', 'uint16', 1, 'out'),
             ('Stream Chunk Data', 'uint16', 31, 'out')],
'high_level': {'stream_out': {'fixed_total_length': 60*80}},
'since_firmware': [1, 0, 0],
'doc': ['llc', {
'en':
"""
""",
'de':
"""
"""
}]
})

