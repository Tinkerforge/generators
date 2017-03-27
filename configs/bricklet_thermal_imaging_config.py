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
'name': 'Get Image Low Level',
'elements': [('Stream Chunk Offset', 'uint16', 1, 'out'),
             ('Stream Chunk Data', 'uint8', 62, 'out')],
'high_level': {'stream_out': {'fixed_total_length': 60*80}},
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
'name': 'Get Raw Image Low Level',
'elements': [('Stream Chunk Offset', 'uint16', 1, 'out'),
             ('Stream Chunk Data', 'uint16', 31, 'out')],
'high_level': {'stream_out': {'fixed_total_length': 60*80}},
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
'name': 'Get Statistics',
'elements': [('Video Scene Statistics', 'uint16', 4, 'out'), # mean, max, min, pixel count
             ('Spotmeter Statistics', 'uint16', 4, 'out'), # mean, max, min, pixel count
             ('Temperatures', 'uint16', 8, 'out'), # focal plain array, focal plain array at last ffc, housing, housing at last ffc, background, atmospheric, window, window reflected, 
             ('Status', 'uint16', 1, 'out') # Lots of status bits

#             ('Window Reflection', 'uint16', 1, 'out'), # ?
#             ('Window Transmission', 'uint16', 1, 'out'), # ?
#             ('Atmospheric Transmission', 'uint16', 1, 'out'), # ?
],
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
'name': 'Set Resolution',
'elements': [('Resolution', 'uint8', 1, 'in', ('Resolution', [('0 To 6553 Kelvin', 0),
                                                              ('0 To 655 Kelvin', 1)]))],
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
'name': 'Get Resolution',
'elements': [('Resolution', 'uint8', 1, 'out', ('Resolution', [('0 To 6553 Kelvin', 0),
                                                               ('0 To 655 Kelvin', 1)]))],
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
'name': 'Set Spotmeter Config',
'elements': [('Region Of Interest', 'uint8', 4, 'in')],
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
'name': 'Get Spotmeter Config',
'elements': [('Region Of Interest', 'uint8', 4, 'out')],
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
'name': 'Set Automatic Gain Control Config',
'elements': [('Region Of Interest', 'uint8', 4, 'in'),
             ('Dampening Factor', 'uint16', 1, 'in'),
             ('Clip Limit', 'uint16', 2, 'in'),
             ('Empty Counts', 'uint16', 1, 'in')],
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
'name': 'Get Automatic Gain Control Config',
'elements': [('Region Of Interest', 'uint8', 4, 'out'),
             ('Dampening Factor', 'uint16', 1, 'out'),
             ('Clip Limit', 'uint16', 2, 'out'),
             ('Empty Counts', 'uint16', 1, 'out')],
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
'name': 'Set Callback Config',
'elements': [('Callback Config', 'uint8', 1, 'in', ('Callback Config', [('Callback Off', 0),
                                                                        ('Callback Image', 1),
                                                                        ('Callback Raw Image', 2)]))],
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
'elements': [('Callback Config', 'uint8', 1, 'out', ('Callback Config', [('Callback Off', 0),
                                                                         ('Callback Image', 1),
                                                                         ('Callback Raw Image', 2)]))],
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
'name': 'Image Low Level',
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
'name': 'Raw Image Low Level',
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

