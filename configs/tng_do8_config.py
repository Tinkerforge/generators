# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# TNG DO8 communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'TNG',
    'device_identifier': 202,
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
'name': 'Set Value',
'elements': [('Timestamp', 'uint64', 1, 'in', {'scale': (1, 10**6), 'unit': 'Second'}),
             ('Value', 'bool', 8, 'in', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the output value of all four channels. A value of *true* or *false* outputs
logic 1 or logic 0 respectively on the corresponding channel.
""",
'de':
"""
Setzt den Zustand aller vier Kanäle. Der Wert *true* bzw. *false* erzeugen
logisch 1 bzw. logisch 0 auf dem entsprechenden Kanal.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('setter', 'Set Value', [('bool', [True, False, True, False, True, False, True, False])], None, None)]
})
