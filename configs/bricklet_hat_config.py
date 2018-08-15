# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# HAT Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2126,
    'name': 'HAT',
    'display_name': 'HAT',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '',
        'de': ''
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'discontinued': False,
    'packets': [],
    'examples': []
}

WEEKDAY = ('Weekday', [('Monday', 1),
                       ('Tuesday', 2),
                       ('Wednesday', 3),
                       ('Thursday', 4),
                       ('Friday', 5),
                       ('Saturday', 6),
                       ('Sunday', 7)])

com['packets'].append({
'type': 'function',
'name': 'Get Battery Statistics',
'elements': [('Battery Connected', 'bool', 1, 'out'),
             ('Capacity Full', 'int32', 1, 'out'),
             ('Capacity Nominal', 'int32', 1, 'out'),
             ('Capacity Remaining', 'int32', 1, 'out'),
             ('Percentage Charge', 'int32', 1, 'out'),
             ('Time To Empty', 'int32', 1, 'out'),
             ('Time To Full', 'int32', 1, 'out'),
             ('Voltage Battery', 'int32', 1, 'out'),
             ('Voltage USB', 'int32', 1, 'out'),
             ('Voltage DC', 'int32', 1, 'out'),
             ('Current Flow', 'int32', 1, 'out'),
             ('Temperature Battery', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set Power Off',
'elements': [('Power Off Delay', 'uint32', 1, 'in'),
             ('Power Off Duration', 'uint32', 1, 'in'),
             ('Raspberry Pi Off', 'bool', 1, 'in'),
             ('Bricklets Off', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Power Off',
'elements': [('Power Off Delay', 'uint32', 1, 'out'),
             ('Power Off Duration', 'uint32', 1, 'out'),
             ('Raspberry Pi Off', 'bool', 1, 'out'),
             ('Bricklets Off', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set Time',
'elements': [('Year', 'uint16', 1, 'in'),
             ('Month', 'uint8', 1, 'in'),
             ('Day', 'uint8', 1, 'in'),
             ('Hour', 'uint8', 1, 'in'),
             ('Minute', 'uint8', 1, 'in'),
             ('Second', 'uint8', 1, 'in'),
             ('Weekday', 'uint8', 1, 'in', WEEKDAY)],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Time',
'elements': [('Year', 'uint16', 1, 'out'),
             ('Month', 'uint8', 1, 'out'),
             ('Day', 'uint8', 1, 'out'),
             ('Hour', 'uint8', 1, 'out'),
             ('Minute', 'uint8', 1, 'out'),
             ('Second', 'uint8', 1, 'out'),
             ('Weekday', 'uint8', 1, 'out', WEEKDAY)],
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
