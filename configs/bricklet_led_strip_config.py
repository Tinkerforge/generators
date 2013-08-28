# -*- coding: utf-8 -*-

# LED Strip Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 231,
    'name': ('LEDStrip', 'led_strip', 'LED Strip'),
    'manufacturer': 'Tinkerforge',
    'description': 'TODO',
    'released': False,
    'packets': []
}


com['packets'].append({
'type': 'function',
'name': ('SetRGBValues', 'set_rgb_values'), 
'elements': [('index', 'uint16', 1, 'in'),
             ('length', 'uint8', 1, 'in'),
             ('r', 'uint8', 16, 'in'),
             ('g', 'uint8', 16, 'in'),
             ('b', 'uint8', 16, 'in')],
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
'name': ('GetRGBValues', 'get_rgb_values'), 
'elements': [('index', 'uint16', 1, 'in'),
             ('length', 'uint8', 1, 'in'),
             ('r', 'uint8', 16, 'out'),
             ('g', 'uint8', 16, 'out'),
             ('b', 'uint8', 16, 'out')],
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
'name': ('SetFrameDuration', 'set_frame_duration'), 
'elements': [('duration', 'uint16', 1, 'in')],
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
'name': ('GetFrameDuration', 'get_frame_duration'), 
'elements': [('duration', 'uint16', 1, 'out')],
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
'name': ('GetSupplyVoltage', 'get_supply_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')],
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
'name': ('FrameRendered', 'frame_rendered'), 
'elements': [('length', 'uint16', 1, 'out')],
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

