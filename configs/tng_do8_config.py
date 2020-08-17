# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# TNG DO8 communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'TNG',
    'device_identifier': 205,
    'name': 'DO8',
    'display_name': 'DO8',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'TBD',
        'de': 'TBD'
    },
    'released': False,
    'documented': False,
    'discontinued': False,
    'features': [
        'tng'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Set Values',
'elements': [('Timestamp', 'uint64', 1, 'in', {'scale': (1, 10**6), 'unit': 'Second'}),
             ('Values', 'bool', 8, 'in', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
timestamp = 0 => now
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Values',
'elements': [('Timestamp', 'uint64', 1, 'out', {'scale': (1, 10**6), 'unit': 'Second'}),
             ('Values', 'bool', 8, 'out', {})],
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
'name': 'Set Selected Value',
'elements': [('Channel', 'uint8', 1, 'in', {}),
             ('Timestamp', 'uint64', 1, 'in', {'scale': (1, 10**6), 'unit': 'Second'}),
             ('Value', 'bool', 8, 'in', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
timestamp = 0 => now
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Selected Value',
'elements': [('Channel', 'uint8', 1, 'in', {}),
             ('Timestamp', 'uint64', 1, 'out', {'scale': (1, 10**6), 'unit': 'Second'}),
             ('Value', 'bool', 1, 'out', {})],
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
'name': 'Simple',
'functions': [('setter', 'Set Values', [('uint64', 0), ('bool', [True, False, True, False, True, False, True, False])], None, None)]
})
