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
    'comcu': True,
    'released': False,
    'documented': False,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Get High Contrast Image Low Level',
'elements': [('Image Chunk Offset', 'uint16', 1, 'out'),
             ('Image Chunk Data', 'uint8', 62, 'out')],
'high_level': {'stream_out': {'name': 'Image', 'fixed_total_length': 80*60}},
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
'name': 'Get Temperature Image Low Level',
'elements': [('Image Chunk Offset', 'uint16', 1, 'out'),
             ('Image Chunk Data', 'uint16', 31, 'out')],
'high_level': {'stream_out': {'name': 'Image', 'fixed_total_length': 80*60}},
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
'elements': [('Spotmeter Statistics', 'uint16', 4, 'out'), # mean, max, min, pixel count
             ('Temperatures', 'uint16', 4, 'out'), # focal plain array, focal plain array at last ffc, housing, housing at last ffc 
             ('Resolution', 'uint8', 1, 'out', ('Resolution', [('0 To 6553 Kelvin', 0),
                                                              ('0 To 655 Kelvin', 1)])),
             ('Status', 'uint16', 1, 'out') # Lots of status bits # FIXME: convert to bools or add constants
],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Status:
* bit 0: FFC desired
* bit 1-2: FFC never commanded, FFC imminent, FFC in progress, FFC complete
* bit 3: AGC State
* bit 4: Shutter lockout
* bit 5: Overtemp shut down imminent
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
'name': 'Set High Contrast Config',
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
'name': 'Get High Contrast Config',
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
'name': 'Set Image Transfer Config',
'elements': [('Config', 'uint8', 1, 'in', ('Data Transfer', [('Manual High Contrast Image', 0),
                                                             ('Manual Temperature Image', 1),
                                                             ('Callback High Contrast Image', 2),
                                                             ('Callback Temperature Image', 3)]))],
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
'name': 'Get Image Transfer Config',
'elements': [('Config', 'uint8', 1, 'out', ('Data Transfer', [('Manual High Contrast Image', 0),
                                                              ('Manual Temperature Image', 1),
                                                              ('Callback High Contrast Image', 2),
                                                              ('Callback Temperature Image', 3)]))],
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
'name': 'High Contrast Image Low Level',
'elements': [('Image Chunk Offset', 'uint16', 1, 'out'),
             ('Image Chunk Data', 'uint8', 62, 'out')],
'high_level': {'stream_out': {'name': 'Image', 'fixed_total_length': 80*60}},
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
'elements': [('Image Chunk Offset', 'uint16', 1, 'out'),
             ('Image Chunk Data', 'uint16', 31, 'out')],
'high_level': {'stream_out': {'name': 'Image', 'fixed_total_length': 80*60}},
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

