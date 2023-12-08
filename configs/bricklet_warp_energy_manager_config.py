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
    'device_identifier': 2169,
    'name': 'WARP Energy Manager',
    'display_name': 'WARP Energy Manager',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'TBD',
        'de': 'TBD'
    },
    'released': False,
    'documented': False,
    'discontinued': False,
    'esp32_firmware': 'energy_manager',
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
'name': 'Energy Meter Type',
'type': 'uint8',
'constants': [('Not Available', 0),
              ('SDM72', 1),
              ('SDM630', 2),
              ('SDM72V2', 3),
              ('SDM72CTM', 4),
              ('SDM630MCTV2', 5),
              ('DSZ15DZMOD', 6),
              ('DEM4A', 7)]
})

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
'name': 'LED Pattern',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Blinking', 2),
              ('Breathing', 3)]
})

com['packets'].append({
'type': 'function',
'name': 'Set Contactor',
'elements': [('Contactor Value', 'bool', 1, 'in', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TBD
""",
'de':
"""
TBD
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Contactor',
'elements': [('Contactor Value', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TBD
""",
'de':
"""
TBD
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set RGB Value',
'elements': [('R', 'uint8', 1, 'in', {}),
             ('G', 'uint8', 1, 'in', {}),
             ('B', 'uint8', 1, 'in', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the *r*, *g* and *b* values for the LED.
""",
'de':
"""
Setzt die *r*, *g* und *b* Werte für die LED.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get RGB Value',
'elements': [('R', 'uint8', 1, 'out', {}),
             ('G', 'uint8', 1, 'out', {}),
             ('B', 'uint8', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the *r*, *g* and *b* values of the LED as set by :func:`Set RGB Value`.
""",
'de':
"""
Gibt die *r*, *g* und *b* Werte der LED zurück, wie von :func:`Set RGB Value` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Energy Meter Values',
'elements': [('Power', 'float', 1, 'out'),
             ('Current', 'float', 3, 'out')],
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
'name': 'Get Energy Meter Detailed Values Low Level',
'elements': [('Values Chunk Offset', 'uint16', 1, 'out', {}),
             ('Values Chunk Data', 'float', 15, 'out', {})],
'high_level': {'stream_out': {'name': 'Values', 'fixed_length': 88}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TBD
""",
'de':
"""
TBD
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Energy Meter State',
'elements': [('Energy Meter Type', 'uint8', 1, 'out', {'constant_group': 'Energy Meter Type'}),
             ('Error Count', 'uint32', 6, 'out')], # local timeout, global timeout, illigal function, illegal data address, illegal data value, slave device failure
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
'name': 'Get Input',
'elements': [('Input', 'bool', 2, 'out')],
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
'name': 'Set Output',
'elements': [('Output', 'bool', 1, 'in')],
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
'name': 'Get Output',
'elements': [('Output', 'bool', 1, 'out')],
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
'name': 'Get Input Voltage',
'elements': [('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'})],
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
'name': 'Get State',
'elements': [('Contactor Check State', 'uint8', 1, 'out')],
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

com['packets'].append({
'type': 'function',
'name': 'Get All Data 1',
'elements': [('Contactor Value', 'bool', 1, 'out', {}),
             ('R', 'uint8', 1, 'out', {}),
             ('G', 'uint8', 1, 'out', {}),
             ('B', 'uint8', 1, 'out', {}),
             ('Power', 'float', 1, 'out'),
             ('Current', 'float', 3, 'out'),
             ('Energy Meter Type', 'uint8', 1, 'out', {'constant_group': 'Energy Meter Type'}),
             ('Error Count', 'uint32', 6, 'out'),
             ('Input', 'bool', 2, 'out'),
             ('Output', 'bool', 1, 'out'),
             ('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'}),
             ('Contactor Check State', 'uint8', 1, 'out'),
             ('Uptime', 'uint32', 1, 'out')
],
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
'type': 'function',
'name': 'Set SD Wallbox Data Point',
'elements': [('Wallbox ID', 'uint32', 1, 'in'),
             ('Year', 'uint8', 1, 'in'), # base 2000
             ('Month', 'uint8', 1, 'in', {'range': (1, 12)}),
             ('Day', 'uint8', 1, 'in', {'range': (1, 31)}),
             ('Hour', 'uint8', 1, 'in', {'range': (0, 23)}),
             ('Minute', 'uint8', 1, 'in', {'range': (0, 55)}), # 5 minute interval (0, 5, .., 50, 55)
             ('Flags', 'uint8', 1, 'in'), # IEC_STATE (bit 0-2) + future use
             ('Power', 'uint16', 1, 'in'), # W
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Data Status'})],
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

# Triggers SD Wallbox Data callback
# Only access one day at a time! 
com['packets'].append({
'type': 'function',
'name': 'Get SD Wallbox Data Points',
'elements': [('Wallbox ID', 'uint32', 1, 'in'),
             ('Year', 'uint8', 1, 'in'), # base 2000
             ('Month', 'uint8', 1, 'in', {'range': (1, 12)}),
             ('Day', 'uint8', 1, 'in', {'range': (1, 31)}),
             ('Hour', 'uint8', 1, 'in', {'range': (0, 23)}),
             ('Minute', 'uint8', 1, 'in', {'range': (0, 55)}), # 5 minute interval (0, 5, .., 50, 55)
             ('Amount', 'uint16', 1, 'in'), # 288 for one day
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Data Status'})],
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
'name': 'Set SD Wallbox Daily Data Point',
'elements': [('Wallbox ID', 'uint32', 1, 'in'),
             ('Year', 'uint8', 1, 'in'), # base 2000
             ('Month', 'uint8', 1, 'in', {'range': (1, 12)}),
             ('Day', 'uint8', 1, 'in', {'range': (1, 31)}),
             ('Energy', 'uint32', 1, 'in'),
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Data Status'})],
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

# Triggers SD Wallbox Daily Data callback
# Only access one month at a time! 
com['packets'].append({
'type': 'function',
'name': 'Get SD Wallbox Daily Data Points',
'elements': [('Wallbox ID', 'uint32', 1, 'in'),
             ('Year', 'uint8', 1, 'in'), # base 2000
             ('Month', 'uint8', 1, 'in', {'range': (1, 12)}),
             ('Day', 'uint8', 1, 'in', {'range': (1, 31)}),
             ('Amount', 'uint8', 1, 'in'),
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Data Status'})],
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
'name': 'Set SD Energy Manager Data Point',
'elements': [('Year', 'uint8', 1, 'in'), # base 2000
             ('Month', 'uint8', 1, 'in', {'range': (1, 12)}),
             ('Day', 'uint8', 1, 'in', {'range': (1, 31)}),
             ('Hour', 'uint8', 1, 'in', {'range': (0, 23)}),
             ('Minute', 'uint8', 1, 'in', {'range': (0, 55)}), # 5 minute interval (0, 5, .., 50, 55)
             ('Flags', 'uint8', 1, 'in'), #
             ('Power Grid', 'int32', 1, 'in'), # W
             ('Power General', 'int32', 6, 'in'), # W
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Data Status'})],
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

# Triggers SD Energy Manager Data callback
# Only access one day at a time! 
com['packets'].append({
'type': 'function',
'name': 'Get SD Energy Manager Data Points',
'elements': [('Year', 'uint8', 1, 'in'), # base 2000
             ('Month', 'uint8', 1, 'in', {'range': (1, 12)}),
             ('Day', 'uint8', 1, 'in', {'range': (1, 31)}),
             ('Hour', 'uint8', 1, 'in', {'range': (0, 23)}),
             ('Minute', 'uint8', 1, 'in', {'range': (0, 55)}), # 5 minute interval (0, 5, .., 50, 55)
             ('Amount', 'uint16', 1, 'in'), # 288 for one day
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Data Status'})],
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
'name': 'Set SD Energy Manager Daily Data Point',
'elements': [('Year', 'uint8', 1, 'in'), # base 2000
             ('Month', 'uint8', 1, 'in', {'range': (1, 12)}),
             ('Day', 'uint8', 1, 'in', {'range': (1, 31)}),
             ('Energy Grid In', 'uint32', 1, 'in'),
             ('Energy Grid Out', 'uint32', 1, 'in'),
             ('Energy General In', 'uint32', 6, 'in'),
             ('Energy General Out', 'uint32', 6, 'in'),
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Data Status'})],
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

# Triggers SD Energy Manager Daily Data callback
# Only access one month at a time! 
com['packets'].append({
'type': 'function',
'name': 'Get SD Energy Manager Daily Data Points',
'elements': [('Year', 'uint8', 1, 'in'), # base 2000
             ('Month', 'uint8', 1, 'in', {'range': (1, 12)}),
             ('Day', 'uint8', 1, 'in', {'range': (1, 31)}),
             ('Amount', 'uint8', 1, 'in'),
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Data Status'})],
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
'name': 'SD Wallbox Data Points Low Level',
'elements': [('Data Length', 'uint16', 1, 'out', {}),
             ('Data Chunk Offset', 'uint16', 1, 'out', {}),
             ('Data Chunk Data', 'uint8', 60, 'out', {})],
'high_level': {'stream_out': {'name': 'Data'}},
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

com['packets'].append({
'type': 'callback',
'name': 'SD Wallbox Daily Data Points Low Level',
'elements': [('Data Length', 'uint16', 1, 'out', {}),
             ('Data Chunk Offset', 'uint16', 1, 'out', {}),
             ('Data Chunk Data', 'uint32', 15, 'out', {})],
'high_level': {'stream_out': {'name': 'Data'}},
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

com['packets'].append({
'type': 'callback',
'name': 'SD Energy Manager Data Points Low Level',
'elements': [('Data Length', 'uint16', 1, 'out', {}),
             ('Data Chunk Offset', 'uint16', 1, 'out', {}),
             ('Data Chunk Data', 'uint8', 58, 'out', {})],
'high_level': {'stream_out': {'name': 'Data'}},
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

com['packets'].append({
'type': 'callback',
'name': 'SD Energy Manager Daily Data Points Low Level',
'elements': [('Data Length', 'uint16', 1, 'out', {}),
             ('Data Chunk Offset', 'uint16', 1, 'out', {}),
             ('Data Chunk Data', 'uint32', 14, 'out', {})],
'high_level': {'stream_out': {'name': 'Data'}},
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

com['packets'].append({
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
'name': 'Set LED State',
'elements': [('Pattern', 'uint8', 1, 'in'),
             ('Hue', 'uint16', 1, 'in')],
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
'name': 'Get LED State',
'elements': [('Pattern', 'uint8', 1, 'out'),
             ('Hue', 'uint16', 1, 'out')],
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
'name': 'Get Data Storage',
'elements': [('Page', 'uint8', 1, 'in'),
             ('Data', 'uint8', 63, 'out')],
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
'name': 'Set Data Storage',
'elements': [('Page', 'uint8', 1, 'in'),
             ('Data', 'uint8', 63, 'in')],
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
'name': 'Reset Energy Meter Relative Energy',
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
