# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# OLED 64x48 Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 264,
    'name': ('OLED64x48', 'oled_64x48', 'OLED 64x48', 'OLED 64x48 Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '0.66" OLED with 64x48 pixels',
        'de': '0,66" OLED mit 64x48 Pixel'
    },
    'released': False,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': ('Write', 'write'), 
'elements': [('data', 'uint8', 64, 'in')],
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
'name': ('NewWindow', 'new_window'), 
'elements': [('column_from', 'uint8', 1, 'in'),
             ('column_to', 'uint8', 1, 'in'),
             ('row_from', 'uint8', 1, 'in'),
             ('row_to', 'uint8', 1, 'in')],
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
'name': ('ClearDisplay', 'clear_display'), 
'elements': [],
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
'name': ('SetDisplayConfiguration', 'set_display_configuration'), 
'elements': [('contrast', 'uint8', 1, 'in'),
             ('invert', 'bool', 1, 'in')],
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
'name': ('GetDisplayConfiguration', 'get_display_configuration'), 
'elements': [('contrast', 'uint8', 1, 'out'),
             ('invert', 'bool', 1, 'out')],
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
'name': ('WriteLine', 'write_line'), 
'elements': [('line', 'uint8', 1, 'in'),
             ('position', 'uint8', 1, 'in'),
             ('text', 'string', 13, 'in')],
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

com['examples'].append({
'name': 'Hello World',
'functions': [('setter', 'Clear Display', [], 'Clear display', None),
              ('setter', 'Write Line', [('uint8', 0), ('uint8', 0), ('string', 'Hello World')], 'Write "Hello World" starting from upper left corner of the screen', None)]
})

com['examples'].append({
'name': 'Pixel Matrix',
'functions': [('setter', 'Clear Display', [], 'Clear display', None)],
'incomplete': True # because of special logic
})
