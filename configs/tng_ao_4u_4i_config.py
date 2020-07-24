# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# TNG DI8 communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'TNG',
    'device_identifier': 206,
    'name': 'AO 4U 4I',
    'display_name': 'AO 4U 4I',
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
             ('Voltages', 'int32', 4, 'in', {}),
             ('Currents', 'int32', 4, 'in', {})],
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
'name': 'Get Values',
'elements': [('Timestamp', 'uint64', 1, 'out', {'scale': (1, 10**6), 'unit': 'Second'}),
             ('Voltages', 'int32', 4, 'out', {}),
             ('Currents', 'int32', 4, 'out', {})],
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
'name': 'Set Voltages',
'elements': [('Timestamp', 'uint64', 1, 'in', {'scale': (1, 10**6), 'unit': 'Second'}),
             ('Voltages', 'int32', 4, 'in', {})],
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
'name': 'Get Voltages',
'elements': [('Timestamp', 'uint64', 1, 'out', {'scale': (1, 10**6), 'unit': 'Second'}),
             ('Voltages', 'int32', 4, 'out', {})],
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
'name': 'Set Currents',
'elements': [('Timestamp', 'uint64', 1, 'in', {'scale': (1, 10**6), 'unit': 'Second'}),
             ('Currents', 'int32', 4, 'in', {})],
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
'name': 'Get Currents',
'elements': [('Timestamp', 'uint64', 1, 'out', {'scale': (1, 10**6), 'unit': 'Second'}),
             ('Currents', 'int32', 4, 'out', {})],
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
'name': 'Set Selected Voltage',
'elements': [('Channel', 'uint8', 1, 'in', {}),
             ('Timestamp', 'uint64', 1, 'in', {'scale': (1, 10**6), 'unit': 'Second'}),
             ('Voltage', 'int32', 1, 'in', {})],
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
'name': 'Get Selected Voltage',
'elements': [('Channel', 'uint8', 1, 'in', {}),
             ('Timestamp', 'uint64', 1, 'out', {'scale': (1, 10**6), 'unit': 'Second'}),
             ('Voltage', 'int32', 1, 'out', {})],
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
'name': 'Set Selected Current',
'elements': [('Channel', 'uint8', 1, 'in', {}),
             ('Timestamp', 'uint64', 1, 'in', {'scale': (1, 10**6), 'unit': 'Second'}),
             ('Current', 'int32', 1, 'in', {})],
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
'name': 'Get Selected Current',
'elements': [('Channel', 'uint8', 1, 'in', {}),
             ('Timestamp', 'uint64', 1, 'out', {'scale': (1, 10**6), 'unit': 'Second'}),
             ('Current', 'int32', 1, 'out', {})],
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
'functions': [('getter', ('Get Values', 'values'), [(('Values', ['Channel 0', 'Channel 1', 'Channel 2', 'Channel 3', 'Channel 4', 'Channel 5', 'Channel 6', 'Channel 7']), 'bool', 8, None, None, None)], [])]
})
