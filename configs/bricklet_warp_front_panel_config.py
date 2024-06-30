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

# Page = 256 Byte of 64 Byte Subpages
# Sector = 4096 Byte

com['packets'].append({
'type': 'function',
'name': 'Set EEPROM Index',
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
'name': 'Get EEPROM Index',
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
'name': 'Set EEPROM Data', # Uses current Index and increments it by 1
'elements': [('Data', 'uint8', 64, 'in'),
             ('Next Page Index', 'uint32', 1, 'out'),
             ('Next Sub Page Index', 'uint8', 1, 'out')],
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
'name': 'Get EEPROM Data',
'elements': [('Data', 'uint8', 64, 'out')],
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
'name': 'Erase EEPROM Sector',
'elements': [('Sector Index', 'uint16', 1, 'in')],
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
'name': 'Erase EEPROM',
'elements': [],
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
