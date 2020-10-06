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
        'device',
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

com['constant_groups'].append({
'name': 'Channel',
'type': 'uint8',
'constants': [('TX',    0),    # all TX channels
              ('TX1',   1),    # TX channel 1
              ('TX2',   2),    # provision for potential future products / common API
              ('TX3',   3),    # ...
              ('TX4',   4),    # ...
              ('TX5',   5),    # ...
              ('TX6',   6),    # ...
              ('TX7',   7),    # ...
              ('TX8',   8),    # ...
              ('TX9',   9),    # ...
              ('TX10', 10),    # ...
              ('TX11', 11),    # ...
              ('TX12', 12),    # ...

              ('RX',   32),    # all RX channels
              ('RX1',  33),    # RX channel 1
              ('RX2',  34),    # RX channel 2
              ('RX3',  35),    # provision for potential future products / common API
              ('RX4',  36),    # ...
              ('RX5',  37),    # ...
              ('RX6',  38),    # ...
              ('RX7',  39),    # ...
              ('RX8',  40),    # ...
              ('RX9',  41),    # ...
              ('RX10', 42),    # ...
              ('RX11', 43),    # ...
              ('RX12', 44)]    # ...
})

com['constant_groups'].append({
'name': 'SDI',
'type': 'uint8',
'constants': [('SDI0',     0), # SDI bits used for address extension, SDI 0
              ('SDI1',     1), # SDI bits used for address extension, SDI 0
              ('SDI2',     2), # SDI bits used for address extension, SDI 0
              ('SDI3',     3), # SDI bits used for address extension, SDI 0
              ('SDI Data', 4)] # SDI bits used for data
})

com['constant_groups'].append({
'name': 'Parity',
'type': 'uint8',
'constants': [('Parity Data', 0),  # parity bit is used for data or parity provided by user
              ('Parity Auto', 1)]  # parity bit is set automatically
})

com['constant_groups'].append({
'name': 'Speed',
'type': 'uint8',
'constants': [('HS', 0),        # high speed
              ('LS', 1)]        # low  speed
})

com['constant_groups'].append({
'name': 'Channel Mode',
'type': 'uint8',
'constants': [('Passive', 0), # initialized, but output stage in HI-Z
              ('Active',  1), # initialized, ready to receive / ready for direct transmit
              ('Run',     2)] # TX channels only: active and scheduler running
})

com['constant_groups'].append({
'name': 'Frame Status',
'type': 'uint8',
'constants': [('Update',  0),   # frame is overdue (frame data are last data received)
              ('Timeout', 1)]   # new or updated frame received
})

com['constant_groups'].append({
'name': 'Scheduler Job',
'type': 'uint8',
'constants': [('Empty',  0),    # no     transmit, no dwell
              ('Mute',   1),    # no     transmit, do dwell
              ('Single', 2),    # send frame once       and dwell
              ('Cyclic', 3)]    # send frame repeatedly and dwell
})

com['packets'].append({
'type': 'function',
'name': 'Debug Get Discretes',
'elements': [('RX Discretes', 'uint16', 1, 'out', {'range': (0, 1023)}),
             ('TX Discretes', 'uint16', 1, 'out', {'range': (0,    3)})],
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
Debug function to execute a direct SPI read access on the A429 chip.
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
Debug function to execute a direct SPI write access on the A429 chip.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Capabilities',
'elements': [('RX Channels',         'uint8',  1, 'out', {'range': (0, 16)}),
             ('RX Filter Frames',    'uint16', 1, 'out'),
             ('TX Channels',         'uint8',  1, 'out', {'range': (0,  8)}),
             ('TX Schedule Entries', 'uint16', 1, 'out'),
             ('TX Schedule Frames',  'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Get the number of RX and TX channels available on this bricklet,
along with the maximum number of available RX frame filters and
TX scheduler entries and scheduled frames.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Heartbeat Callback Configuration',
'elements': [('Period',              'uint8',  1, 'in', {'scale': (1, 60), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool',   1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Set the bricklet heartbeat which reports the statistics counter for
processed frames and lost frames.
The period is the period with which the :cb:`Heartbeat` callback
is triggered periodically. A value of 0 turns the callback off.
When 'Value Has To Change' is enabled, the heartbeat will only be
sent if there is a change in the statistics numbers.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Heartbeat Callback Configuration',
'elements': [('Period',              'uint8', 1, 'out', {'scale': (1, 60), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool',  1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Get the configuration of the bricklet heartbeat reporting the satistics counters.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Heartbeat',
'elements': [('Sequence Number',  'uint8',  1, 'out'),
             ('Frames Processed', 'uint16', 3, 'out'),
             ('Frames Lost',      'uint16', 3, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set Heartbeat Callback Configuration`. It reports the statistics counters
for processed frames and lost frames for all TX and RX channels.
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set Channel Configuration',
'elements': [('Channel', 'uint8',  1, 'in',  {'constant_group': 'Channel'}),
             ('Parity',  'uint8',  1, 'in',  {'constant_group': 'Parity' }),
             ('Speed',   'uint8',  1, 'in',  {'constant_group': 'Speed'  })],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Set the physical properties of the selected channel:
 * Channel:   channel to configure
 * Parity:    'parity' for automatic parity adjustment, 'transparent' for transparent mode
 * Speed:     'hs' for high speed (100 kbit/s), 'ls' for low speed (12.5 kbit/s)
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Channel Configuration',
'elements': [('Channel', 'uint8',  1, 'in',   {'constant_group': 'Channel'}),
             ('Parity',  'uint8',  1, 'out',  {'constant_group': 'Parity' }),
             ('Speed',   'uint8',  1, 'out',  {'constant_group': 'Speed'  })],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Get the physical properties of the selected channel.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Channel Mode',
'elements': [('Channel',   'uint8',  1, 'in',  {'constant_group': 'Channel'}),
             ('Mode',      'uint8',  1, 'in',  {'constant_group': 'Channel Mode'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Set the operating mode of the selected channel:
 * passive: the TX channel stops transmitting and becomes high-Z, the RX channel will not receive frames
 * active:  the TX channel is ready to send frames and the RX channel will receive frames
 * filtering: RX channels only - the bricklet will only forward frames that match with the set filters
 * running:   TX channels only - the scheduler will run and transmit labels according to the set schedule
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Channel Mode',
'elements': [('Channel',   'uint8',  1, 'in',   {'constant_group': 'Channel'}),
             ('Mode',      'uint8',  1, 'out',  {'constant_group': 'Channel Mode'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Get the operating mode of the selected channel.
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Clear Prio Labels',
'elements': [('Channel', 'uint8',  1, 'in', {'constant_group': 'Channel'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Disable the priority filters on the given channel(s).
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set Prio Labels',
'elements': [('Channel', 'uint8',  1, 'in',  {'constant_group': 'Channel'}),
             ('Label',   'uint8',  3, 'in',)],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Set the labels for the priority receive filters in the given channel(s).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Prio Labels',
'elements': [('Channel',      'uint8',  1, 'in',  {'constant_group': 'Channel'}),
             ('Prio Enabled', 'bool',   1, 'out'),
             ('Label',        'uint8',  3, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Read the labels configured for the priority receive filters on the selected channel.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Clear All RX Filters',
'elements': [('Channel', 'uint8',  1, 'in',  {'constant_group': 'Channel'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Clear all RX filters in the given channel(s).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Clear RX Filter',
'elements': [('Channel', 'uint8',  1, 'in',  {'constant_group': 'Channel'}),
             ('Label',   'uint8',  1, 'in'),
             ('SDI',     'uint8',  1, 'in',  {'constant_group': 'SDI'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Clear one RX filter in the given channel(s).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set RX Filter',
'elements': [('Channel', 'uint8',  1, 'in',  {'constant_group': 'Channel'}),
             ('Label',   'uint8',  1, 'in',),
             ('SDI',     'uint8',  1, 'in',  {'constant_group': 'SDI'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Set a RX filter configuration for the selected channel(s):
 * Label: Arinc429 label
 * SDI:   when set to 'Address', 4 filters will be created, one for each possible SDI value
 * Timeout: time span with no new frame received after which a timeout message will be generated.
            A timeout value of zero disables the timeout.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get RX Filter',
'elements': [('Channel',    'uint8',  1, 'in',  {'constant_group': 'Channel'}),
             ('Label',      'uint8',  1, 'in'),
             ('SDI',        'uint8',  1, 'in',  {'constant_group': 'SDI'}),
             ('Configured', 'bool',   1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Get the configuration of a RX filter.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Read Frame',
'elements': [('Channel', 'uint8',  1, 'in',  {'constant_group': 'Channel'}),
             ('Label',   'uint8',  1, 'in'),
             ('SDI',     'uint8',  1, 'in',  {'constant_group': 'SDI'}),
             ('Status',  'bool',   1, 'out'),
             ('Frame',   'uint32', 1, 'out'),
             ('Age',     'uint16', 1, 'out', {'scale': (1, 60000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Do a direct read from one of the RX channels and receive buffers. If a new frame
was received 'Status' will return as 'true', else it will have a vlaue of 'false'
and the last frame received will be repeated.
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set RX Callback Configuration',
'elements': [('Channel',             'uint8',  1, 'in', {'constant_group': 'Channel'}),
             ('Enabled',             'bool',   1, 'in', {'default': False}),
             ('Value Has To Change', 'bool',   1, 'in', {'default': False}),
             ('Timeout',             'uint16', 1, 'in', {'scale': (1, 60000), 'unit': 'Second', 'default': 1000})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Enable or disable the generation of callbacks on receiving A429 frames.
If the `value has to change` parameter is set to TRUE, the callback is only
triggered when the frame data have changed, else it is triggered on every
reception of a new frame.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get RX Callback Configuration',
'elements': [('Channel',             'uint8',  1, 'in',  {'constant_group': 'Channel'}),
             ('Enabled',             'bool',   1, 'out', {'default': False}),
             ('Value Has To Change', 'bool',   1, 'out', {'default': False}),
             ('Timeout',             'uint16', 1, 'out', {'scale': (1, 60000), 'unit': 'Second', 'default': 1000})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Get the configuration of the RX frame callback.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Frame Message',
'elements': [('Channel',         'uint8',  1, 'out', {'constant_group': 'Channel'}),
             ('Sequence Number', 'uint8',  1, 'out'),
             ('Frame Status',    'uint8',  1, 'out', {'constant_group': 'Frame Status'}),
             ('Frame',           'uint32', 1, 'out'),
             ('Age',             'uint16', 1, 'out', {'scale': (1, 60000), 'unit': 'Second'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered according to the configuration set by :func:`Set RX Callback Configuration`.
The parameter 'Frame Status' indicates if a new frame was received, or if a timeout encountered.
The timeout can be configured with the :func:'Set RX Filter', default is timeout disabled.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Write Frame Direct',
'elements': [('Channel', 'uint8',  1, 'in',  {'constant_group': 'Channel'}),
             ('Frame',   'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Do an immediate transmit of an A429 frame on the selected transmit channel.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Write Frame Scheduled',
'elements': [('Channel',     'uint8',  1, 'in',  {'constant_group': 'Channel'}),
             ('Frame Index', 'uint16', 1, 'in'),
             ('Frame',       'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Set or update a frame that is transmitted by the scheduler.
 * Frame Index: index number of the frame (the scheduler picks the frames by this index number)
 * Frame:       the A429 frame itself
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Clear Schedule Entries',
'elements': [('Channel',          'uint8',  1, 'in',  {'constant_group': 'Channel'}),
             ('Task Index First', 'uint16', 1, 'in'),
             ('Task Index Last',  'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Clear a range of TX scheduler entries.
 * Channel:   selected TX channel
 * First:     first schedule entry to be cleared
 * Last:      last  schedule entry to be cleared
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set Schedule Entry',
'elements': [('Channel',     'uint8',  1, 'in',  {'constant_group': 'Channel'}),
             ('Task Index',  'uint16', 1, 'in'),
             ('Job',         'uint8',  1, 'in',  {'constant_group': 'Scheduler Job'}),
             ('Frame Index', 'uint16', 1, 'in'),
             ('Dwell Time',  'uint8',  1, 'in',  {'scale': (1, 250), 'unit': 'Second', 'default': 10})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Set a TX scheduler entry:
 * Channel:     selected TX channel
 * Task Index:   schedule entry index
 * Job:         activity assigned to this entry
 * Frame Index: frame    assigned to this slot by frame index
 * Dwell_Time:  time to wait before executing the next job
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Get Schedule Entry',
'elements': [('Channel',     'uint8',  1, 'in',  {'constant_group': 'Channel'}),
             ('Job Index',   'uint16', 1, 'in'),
             ('Job',         'uint8',  1, 'out', {'constant_group': 'Scheduler Job'}),
             ('Frame Index', 'uint16', 1, 'out'),
             ('Frame',       'uint32', 1, 'out'),
             ('Dwell Time',  'uint8',  1, 'out', {'scale': (1, 250), 'unit': 'Second', 'default': 10})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Get a TX scheduler entry.
""",
'de':
"""
"""
}]
})
