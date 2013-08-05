# -*- coding: utf-8 -*-

# Segment Display 4x7 Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 237,
    'name': ('SegmentDisplay4x7', 'segment_display_4x7', 'Segment Display 4x7'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for controling four 7-segment displays',
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('SetSegments', 'set_segments'), 
'elements': [('segments', 'uint8', 4, 'in'),
             ('brightness', 'uint8', 1, 'in'),
             ('clock_points', 'bool', 1, 'in')],
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
'name': ('GetSegments', 'get_segments'), 
'elements': [('segments', 'uint8', 4, 'out'),
             ('brightness', 'uint8', 1, 'out'),
             ('clock_points', 'bool', 1, 'out')],
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
