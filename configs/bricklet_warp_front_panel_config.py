# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Energy Monitor Bricklet communication config

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2179,
    'name': 'WARP Front Panel',
    'display_name': 'WARP Front Panel',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'TBD',
        'de': 'TBD'
    },
    'released': False,
    'documented': False,
    'discontinued': False,
    'esp32_firmware': 'energy_manager_v2',
    'features': [
        'device',
        'comcu_bricklet',
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append({
'name': 'Flash Status',
'type': 'uint8',
'constants': [('OK', 0),
              ('Busy', 1)]
})

# Page = 256 Byte of 64 Byte Subpages
# Sector = 4096 Byte

com['packets'].append({
'type': 'function',
'name': 'Set Flash Index',
'elements': [('Page Index', 'uint32', 1, 'in'),
             ('Sub Page Index', 'uint8', 1, 'in')],
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
'name': 'Get Flash Index',
'elements': [('Page Index', 'uint32', 1, 'out'),
             ('Sub Page Index', 'uint8', 1, 'out')],
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
'name': 'Set Flash Data', # Uses current Index and increments it by 1
'elements': [('Data', 'uint8', 64, 'in'),
             ('Next Page Index', 'uint32', 1, 'out'),
             ('Next Sub Page Index', 'uint8', 1, 'out'),
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Flash Status'})],
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
'name': 'Erase Flash Sector',
'elements': [('Sector Index', 'uint16', 1, 'in'),
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Flash Status'})],
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
'name': 'Erase Flash',
'elements': [('Status', 'uint8', 1, 'out', {'constant_group': 'Flash Status'})],
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
'name': 'Set Status Bar',
'elements': [('Ethernet Status', 'uint32', 1, 'in'),
             ('WIFI Status', 'uint32', 1, 'in'),
             ('Hours', 'uint8', 1, 'in'),
             ('Minutes', 'uint8', 1, 'in'),
             ('Seconds', 'uint8', 1, 'in')],
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
'name': 'Get Status Bar',
'elements': [('Ethernet Status', 'uint32', 1, 'out'),
             ('WIFI Status', 'uint32', 1, 'out'),
             ('Hours', 'uint8', 1, 'out'),
             ('Minutes', 'uint8', 1, 'out'),
             ('Seconds', 'uint8', 1, 'out')],
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
'name': 'Set Display Page Index',
'elements': [('Page Index', 'uint32', 1, 'in')],
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
'name': 'Get Display Page Index',
'elements': [('Page Index', 'uint32', 1, 'out')],
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
'name': 'Set Display Front Page Icon',
'elements': [('Icon Index', 'uint32', 1, 'in'),
             ('Active', 'bool', 1, 'in'),
             ('Sprite Index', 'uint32', 1, 'in'),
             ('Text 1', 'char', 10, 'in'),
             ('Font Index 1', 'uint8', 1, 'in'),
             ('Text 2', 'char', 10, 'in'),
             ('Font Index 2', 'uint8', 1, 'in')],
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
'name': 'Get Display Front Page Icon',
'elements': [('Icon Index', 'uint32', 1, 'in'),
             ('Active', 'bool', 1, 'out'),
             ('Sprite Index', 'uint32', 1, 'out'),
             ('Text 1', 'char', 10, 'out'),
             ('Font Index 1', 'uint8', 1, 'out'),
             ('Text 2', 'char', 10, 'out'),
             ('Font Index 2', 'uint8', 1, 'out')],
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
