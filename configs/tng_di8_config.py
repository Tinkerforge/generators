# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# TNG DI8 communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'TNG',
    'device_identifier': 201,
    'name': 'DI8',
    'display_name': 'DI8',
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

CONSTANT_CHANNEL = ('Channel', [('0', 0),
                                ('1', 1),
                                ('2', 2),
                                ('3', 3),
                                ('4', 4),
                                ('5', 5),
                                ('6', 6),
                                ('7', 7)])

com['packets'].append({
'type': 'function',
'name': 'Get Value',
'elements': [('Timestamp', 'uint64', 1, 'out'),
             ('Value', 'bool', 8, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the input value as bools, *true* refers to high and *false* refers to low.
""",
'de':
"""
Gibt die Eingangswerte als Bools zurück, *true* bedeutet logisch 1 und *false* logisch 0.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Value', 'value'), [(('Value', ['Channel 0', 'Channel 1', 'Channel 2', 'Channel 3', 'Channel 4', 'Channel 5', 'Channel 6', 'Channel 7']), 'bool', 8, None, None, None)], [])]
})
