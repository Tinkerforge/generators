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

com['packets'].append({
'type': 'function',
'name': 'Set Sleep Mode',
'elements': [('Power Off Delay', 'uint32', 1, 'in'),
             ('Power Off Duration', 'uint32', 1, 'in'),
             ('Raspberry Pi Off', 'bool', 1, 'in'),
             ('Bricklets Off', 'bool', 1, 'in'),
             ('Enable Sleep Indicator', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Enable Sleep Indicator => status led blinks in 1s interval => ~0.3mA
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Sleep Mode',
'elements': [('Power Off Delay', 'uint32', 1, 'out'),
             ('Power Off Duration', 'uint32', 1, 'out'),
             ('Raspberry Pi Off', 'bool', 1, 'out'),
             ('Bricklets Off', 'bool', 1, 'out'),
             ('Enable Sleep Indicator', 'bool', 1, 'out')],
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
'name': 'Set Bricklet Power',
'elements': [('Bricklet Power', 'bool', 1, 'in')],
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
'name': 'Get Bricklet Power',
'elements': [('Bricklet Power', 'bool', 1, 'out')],
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
'elements': [('Voltage USB', 'uint16', 1, 'out'),
             ('Voltage DC', 'uint16', 1, 'out')],
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
