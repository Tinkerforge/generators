# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# WARP ESP32 Ethernet 2.0 Co communication config

from generators.configs.commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from generators.configs.commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2184,
    'name': 'WARP ESP32 Ethernet V2 Co',
    'display_name': 'WARP ESP32 Ethernet 2.0 Co',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'TBD',
        'de': 'TBD'
    },
    'released': False,
    'documented': False,
    'discontinued': False,
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
'name': 'Data Status',
'type': 'uint8',
'constants': [('OK', 0),
              ('SD Error', 1),
              ('LFS Error', 2),
              ('Queue Full', 3),
              ('Date Out Of Range', 4)]
})

com['constant_groups'].append({
'name': 'Format Status',
'type': 'uint8',
'constants': [('OK', 0),
              ('Password Error', 1),
              ('Format Error', 2)]
})

com['constant_groups'].append({
'name': 'LED State',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Auto', 2)]
})

com['packets'].append({
'type': 'function',
'name': 'Set LED',
'elements': [('State', 'uint8', 1, 'in', {'constant_group': 'LED State'})],
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
'name': 'Get LED',
'elements': [('State', 'uint8', 1, 'out', {'constant_group': 'LED State'})],
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
'name': 'Get Temperature',
'elements': [('Temperature', 'int16', 1, 'out')], # Returns 0 in EVSE V2
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
'name': 'Set Date Time',
'elements': [('Seconds', 'uint8', 1, 'in', {'range': (0, 59)}),
             ('Minutes', 'uint8', 1, 'in', {'range': (0, 59)}),
             ('Hours', 'uint8', 1, 'in', {'range': (0, 23)}),
             ('Days', 'uint8', 1, 'in', {'range': (0, 31)}),
             ('Days Of Week', 'uint8', 1, 'in', {'range': (0, 6)}), # 0 = Sunday, 1 = Monday, ...
             ('Month', 'uint8', 1, 'in', {'range': (0, 11)}),
             ('Year', 'uint16', 1, 'in')],
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
'name': 'Get Date Time',
'elements': [('Seconds', 'uint8', 1, 'out', {'range': (0, 59)}),
             ('Minutes', 'uint8', 1, 'out', {'range': (0, 59)}),
             ('Hours', 'uint8', 1, 'out', {'range': (0, 23)}),
             ('Days', 'uint8', 1, 'out', {'range': (0, 31)}),
             ('Days Of Week', 'uint8', 1, 'out', {'range': (0, 6)}), # 0 = Sunday, 1 = Monday, ...
             ('Month', 'uint8', 1, 'out', {'range': (0, 11)}),
             ('Year', 'uint16', 1, 'out')],
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
'name': 'Get Uptime',
'elements': [('Uptime', 'uint32', 1, 'out')],
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

com['packets'].append({ # unused
'type': 'function',
'name': 'Format SD',
'elements': [('Password', 'uint32', 1, 'in'), # Password: 0x4223ABCD
             ('Format Status', 'uint8', 1, 'out', {'constant_group': 'Format Status'})],
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

com['packets'].append({ # unused
'type': 'function',
'name': 'Get SD Information',
'elements': [('SD Status', 'uint32', 1, 'out'),
             ('LFS Status', 'uint32', 1, 'out'),
             ('Sector Size', 'uint16', 1, 'out'),
             ('Sector Count', 'uint32', 1, 'out'),
             ('Card Type', 'uint32', 1, 'out'),
             ('Product Rev', 'uint8', 1, 'out'),
             ('Product Name', 'char', 5, 'out'),
             ('Manufacturer ID', 'uint8', 1, 'out')],
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
'type': 'callback',
'name': 'RMMI Interrupt',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
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
