# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# ARINC429 Breakout Bricklet communication config

from generators.configs.commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from generators.configs.commonconstants import add_callback_value_function

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2160,
    'name': 'ARINC429',
    'display_name': 'ARINC429',
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
'name': 'RW Error',
'type': 'uint8',
'constants': [('OK',               0),  # Everything went OK
              ('No Write',         1),  # Write Register, but OP code is for read
              ('No Read',          2),  # Read Register, but OP code is for write
              ('Invalid OP Code',  3),  # Invalid OP code
              ('Invalid Length',   4),  # Invalid OP code
              ('SPI',              5)], # Error during SPI communication
})

com['packets'].append({
'type': 'function',
'name': 'Debug Get Discretes',
'elements': [('RX Discretes', 'uint16', 1, 'out', {'range': (0, 1023)}),
             ('TX Discretes', 'uint16', 1, 'out', {'range': (0, 3)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Debug function to read the discrete signals from the A429 chip.

RX Discretes Bit   9: MB2-1   - pending frame in RX2, PRIO 1
                   8: MB2-2   -                            2
                   7: MB2-3   -                            3
                   6: R2FLAG  -                       FIFO
                   5: R2INT   -                       FIFO
                   4: MB1-1   - pending frame in RX1, PRIO 1
                   3: MB1-2   -                            2
                   2: MB1-3   -                            3
                   1: R1FLAG  -                       FIFO
                   0: R1INT   -                       FIFO

TX Discretes Bit 2-7: unused
                   1: TFULL   - TX buffer full
                   0: TEMPTY  - TX buffer empty
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Debug Read Register Low Level',
'elements': [('OP Code', 'uint8', 1, 'in', {}),
             ('Value Length', 'uint8', 1, 'out', {}),
             ('Value Data', 'uint8', 32, 'out', {}),
             ('RW Error', 'uint8', 1, 'out',  {'constant_group': 'RW Error'})],
'high_level': {'stream_out': {'name': 'Value', 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Debug function to read from a SPI register of the A429 chip.
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Debug Write Register Low Level',
'elements': [('OP Code', 'uint8', 1, 'in', {}),
             ('Value Length', 'uint8', 1, 'in', {}),
             ('Value Data', 'uint8', 32, 'in', {}),
             ('RW Error', 'uint8', 1, 'out',  {'constant_group': 'RW Error'})],
'high_level': {'stream_in': {'name': 'Value', 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Debug function to write to a SPI register of the A429 chip.
""",
'de':
"""
"""
}]
})
