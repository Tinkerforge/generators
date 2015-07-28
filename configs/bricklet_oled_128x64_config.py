# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# OLED 128x64 Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 263,
    'name': ('OLED128x64', 'oled_128x64', 'OLED 128x64', 'OLED 128x64 Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '1.3" OLED with 128x64 pixels',
        'de': '1.3" OLED mit 128x64 Pixel'
    },
    'released': False,
    'packets': []
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
             ('text', 'string', 26, 'in')],
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
