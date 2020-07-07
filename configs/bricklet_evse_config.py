# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# EVSE Bricklet communication config

from generators.configs.commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from generators.configs.commonconstants import add_callback_value_function
from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2159,
    'name': 'EVSE',
    'display_name': 'EVSE',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'TBD',
        'de': 'TBD'
    },
    'released': False,
    'documented': False,
    'discontinued': False,
    'features': [
        'comcu_bricklet',
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append({
'name': 'IEC61851 State',
'type': 'uint8',
'constants': [('A', 0),
              ('B', 1),
              ('C', 2),
              ('D', 3),
              ('EF', 4)]
})

com['constant_groups'].append({
'name': 'LED State',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Blinking', 2),
              ('Breathing', 3)]
})

com['constant_groups'].append({
'name': 'Contactor State',
'type': 'uint8',
'constants': [('AC1 NLive AC2 NLive', 0),
              ('AC1 Live AC2 NLive', 1),
              ('AC1 NLive AC2 Live', 2),
              ('AC1 Live AC2 Live', 3)]
})

com['constant_groups'].append({
'name': 'Lock State',
'type': 'uint8',
'constants': [('Init', 0),
              ('Open', 1),
              ('Closing', 2),
              ('Close', 3),
              ('Opening', 4),
              ('Error', 5)]
})

com['constant_groups'].append({
'name': 'Jumper Configuration',
'type': 'uint8',
'constants': [('6A', 0),
              ('10A', 1),
              ('13A', 2),
              ('16A', 3),
              ('20A', 4),
              ('25A', 5),
              ('32A', 6),
              ('Software', 7),
              ('Unconfigured', 8)]
})

com['packets'].append({
'type': 'function',
'name': 'Get State',
'elements': [('IEC61851 State', 'uint8', 1, 'out', {'constant_group': 'IEC61851 State'}),
             ('LED State', 'uint8', 1, 'out', {'constant_group': 'LED State'}),
             ('Resistance', 'uint32', 2, 'out'),
             ('CP PWM Duty Cycle', 'uint16', 1, 'out'),
             ('Contactor State', 'uint8', 1, 'out', {'constant_group': 'Contactor State'}),
             ('Contactor Error', 'uint8', 1, 'out'),
             ('GPIO', 'bool', 4, 'out'),
             ('Lock State', 'uint8', 1, 'out', {'constant_group': 'Lock State'}),
             ('Jumper Configuration', 'uint8', 1, 'out', {'constant_group': 'Jumper Configuration'}),
             ('Has Lock Switch', 'bool', 1, 'out'),
             ('Uptime', 'uint32', 1, 'out')],
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
'name': 'Set Low Level Output',
'elements': [('Low Level Mode Enabled', 'bool', 1, 'in'),
             ('CP Duty Cycle', 'uint16', 1, 'in'), # 1 khz
             ('Motor Direction', 'bool', 1, 'in'),
             ('Motor Duty Cycle', 'uint16', 1, 'in'),
             ('Relay Enabled', 'uint16', 1, 'in'), # Monoflop
             ('Password', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
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
'name': 'Get Low Level Status',
'elements': [('Low Level Mode Enabled', 'bool', 1, 'out'),
             ('CP Duty Cycle', 'uint16', 1, 'out'),
             ('Motor Direction', 'uint16', 1, 'out'),
             ('Motor Duty Cycle', 'uint16', 1, 'out'),
             ('Relay Enabled', 'uint16', 1, 'out'),
             ('CP Voltage', 'int16', 1, 'out'), # mV
             ('PP Voltage', 'int16', 1, 'out'), # mv
             ('AC Input', 'bool', 2, 'out'),
             ('GP Input', 'bool', 1, 'out'),
             ('Motor Fault', 'bool', 1, 'out'),
             ('Motor Switch', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
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

