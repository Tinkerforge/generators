# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# RS232 Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 254,
    'name': ('RS232', 'rs232', 'RS232'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for RS232 communication',
    'released': False,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('Write', 'write'),
'elements': [('message', 'char', 60, 'in'),
             ('length', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('Read', 'read'),
'elements': [('message', 'char', 60, 'out'),
             ('length', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('EnableCallback', 'enable_callback'),
'elements': [('enable', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('IsCallbackEnabled', 'is_callback_enabled'),
'elements': [('enable', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetConfiguration', 'set_configuration'),
'elements': [('speed', 'uint32', 1, 'in'),
             ('parity', 'char', 1, 'in'),
             ('stopbits', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetConfiguration', 'get_configuration'),
'elements': [('speed', 'uint32', 1, 'in'),
             ('parity', 'char', 1, 'in'),
             ('stopbits', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

