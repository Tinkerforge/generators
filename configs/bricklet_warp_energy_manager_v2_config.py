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
    'device_identifier': 2178,
    'name': 'WARP Energy Manager V2',
    'display_name': 'WARP Energy Manager 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Manages heat pumps, WARP Chargers and logs energy and charge data to an SD card',
        'de': 'TBD'
    },
    'released': True,
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
'name': 'Energy Meter Type',
'type': 'uint8',
'constants': [('Not Available', 0),
              ('SDM72', 1),
              ('SDM630', 2),
              ('SDM72V2', 3),
              ('SDM72CTM', 4),
              ('SDM630MCTV2', 5),
              ('DSZ15DZMOD', 6),
              ('DEM4A', 7),
              ('DMED341MID7ER', 8),
              ('DSZ16DZE', 9),
              ('WM3M4C', 10),
              ('WM3M4', 11)]
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

com['constant_groups'].append({
'name': 'Data Storage Status',
'type': 'uint8',
'constants': [('OK', 0),
              ('Not Found', 1),
              ('Busy', 2)]
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
Returns the total power (in W) and the current per phase (L1, L2, L3 in A) of
the connected energy meter.
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
'elements': [('Values Length', 'uint16', 1, 'out', {}),
             ('Values Chunk Offset', 'uint16', 1, 'out', {}),
             ('Values Chunk Data', 'float', 15, 'out', {})],
'high_level': {'stream_out': {'name': 'Values'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns all values measured by the connected energy meter. The meaning of the
values depends on the energy meter type, see :func:`Get Energy Meter State`.
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
Returns the type of the connected energy meter and the Modbus communication
error counters. The error counters are: local timeout, global timeout,
illegal function, illegal data address, illegal data value and slave device
failure.
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
'elements': [('Input', 'bool', 4, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the values of the four inputs.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set SG Ready Output',
'elements': [('Index', 'uint8', 1, 'in'),
             ('Output', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets one of the two SG Ready outputs (index 0 or 1). The SG Ready (Smart Grid
Ready) outputs can be used to control e.g. a heat pump.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get SG Ready Output',
'elements': [('Output', 'bool', 2, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the state of the two SG Ready outputs as set by
:func:`Set SG Ready Output`.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Relay Output',
'elements': [('Index', 'uint8', 1, 'in'),
             ('Output', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets one of the two relay outputs (index 0 or 1). *true* closes the relay,
*false* opens it.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Relay Output',
'elements': [('Output', 'bool', 2, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the state of the two relay outputs as set by :func:`Set Relay Output`.
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
Returns the supply voltage of the Energy Manager.
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
Returns the uptime of the Energy Manager in milliseconds.
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
'elements': [('Power', 'float', 1, 'out'),
             ('Current', 'float', 3, 'out'),
             ('Energy Meter Type', 'uint8', 1, 'out', {'constant_group': 'Energy Meter Type'}),
             ('Error Count', 'uint32', 6, 'out'),
             ('Input', 'bool', 4, 'out'),
             ('Output SG Ready', 'bool', 2, 'out'),
             ('Output Relay', 'bool', 2, 'out'),
             ('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'}),
             ('Uptime', 'uint32', 1, 'out')
],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the values of :func:`Get Energy Meter Values`,
:func:`Get Energy Meter State`, :func:`Get Input`,
:func:`Get SG Ready Output`, :func:`Get Relay Output`,
:func:`Get Input Voltage` and :func:`Get Uptime` combined in one call.
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
Returns information about the connected SD card. This includes the status of
the SD card and the LittleFS file system, the sector size and count as well as
the card type and product information.
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
             ('Flags', 'uint16', 1, 'in'), # IEC_STATE (bit 0-2) + future use
             ('Power', 'uint16', 1, 'in'), # W
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Data Status'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes a 5-minute charge data point for the wallbox with the given ID and the
given date and time to the SD card. The minute has to be a multiple of 5. The
flags contain the IEC 61851 state in bits 0-2. The power is the charging power
in W. The returned status indicates whether the data point could be queued for
writing.
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
Requests up to *Amount* 5-minute charge data points for the wallbox with the
given ID starting at the given date and time. The data points are returned
through the :cb:`SD Wallbox Data Points Low Level` callback. Only one day
(288 data points) can be requested at a time.
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
Writes a daily charge data point (the charged energy of the given day) for the
wallbox with the given ID to the SD card. The returned status indicates whether
the data point could be queued for writing.
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
Requests up to *Amount* daily charge data points for the wallbox with the
given ID starting at the given date. The data points are returned through the
:cb:`SD Wallbox Daily Data Points Low Level` callback. Only one month can be
requested at a time.
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
             ('Flags', 'uint16', 1, 'in'), #
             ('Power Grid', 'int32', 1, 'in'), # W
             ('Power General', 'int32', 6, 'in'), # W
             ('Price', 'uint32', 1, 'in'),
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Data Status'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes a 5-minute energy manager data point for the given date and time to the
SD card. The minute has to be a multiple of 5. Power Grid is the grid power in
W (positive = import, negative = export) and Power General are six additional
power values in W. The returned status indicates whether the data point could
be queued for writing.
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
Requests up to *Amount* 5-minute energy manager data points starting at the
given date and time. The data points are returned through the
:cb:`SD Energy Manager Data Points Low Level` callback. Only one day
(288 data points) can be requested at a time.
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
             ('Price', 'uint32', 1, 'in'),
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Data Status'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes a daily energy manager data point (the imported and exported energy of
the given day) to the SD card. The returned status indicates whether the data
point could be queued for writing.
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
Requests up to *Amount* daily energy manager data points starting at the given
date. The data points are returned through the
:cb:`SD Energy Manager Daily Data Points Low Level` callback. Only one month
can be requested at a time.
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
This callback is triggered by :func:`Get SD Wallbox Data Points` and returns
the requested 5-minute charge data points.
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
This callback is triggered by :func:`Get SD Wallbox Daily Data Points` and
returns the requested daily charge data points.
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
             ('Data Chunk Data', 'uint8', 34, 'out', {})],
'high_level': {'stream_out': {'name': 'Data'}},
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered by :func:`Get SD Energy Manager Data Points` and
returns the requested 5-minute energy manager data points.
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
             ('Data Chunk Data', 'uint32', 15, 'out', {})],
'high_level': {'stream_out': {'name': 'Data'}},
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered by :func:`Get SD Energy Manager Daily Data Points`
and returns the requested daily energy manager data points.
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
Formats the SD card (LittleFS file system). The password is 0x4223ABCD. All
data on the card is deleted.
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
Sets the date and time of the internal real-time clock. The day of the week is
0 for Sunday, 1 for Monday and so on.
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
Returns the date and time of the internal real-time clock as set by
:func:`Set Date Time`.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Data Storage',
'elements': [('Page', 'uint8', 1, 'in'),
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Data Storage Status'}),
             ('Data', 'uint8', 63, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the content (63 bytes) of the given storage page, see
:func:`Set Data Storage`. The status is *Not Found* if the page has not been
written yet and *Busy* while the page is being read back from the SD card.
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
Stores 63 bytes of data in the given storage page. The data is held in RAM and
written to the SD card about 10 minutes after the last change.
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
Sets the relative energy value of the energy meter to zero. This sets the
point in time from which on the relative energy meter values are counted.
""",
'de':
"""
TODO
"""
}]
})
