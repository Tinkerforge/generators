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
'name': 'Buffer',
'type': 'uint8',
'constants': [('Anything', 0), # any        buffer (currently not used)
              ('Prio1', 1),    # priority 1 buffer
              ('Prio2', 2),    # priority 2 buffer
              ('Prio3', 3),    # priority 3 buffer
              ('FIFO',  4)]    # FIFO       buffer
})

com['constant_groups'].append({
'name': 'SDI',
'type': 'uint8',
'constants': [('Data',     0), # SD bits used for data
              ('Address',  1)] # SD bits used for label extension
})

com['constant_groups'].append({
'name': 'Parity',
'type': 'uint8',
'constants': [('Transparent', 0),  # parity bit used for data
              ('Parity',      1)]  #                 for parity
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
'constants': [('Uninit',  0),   # uninitialized
              ('Passive', 1),   # initialized, but output stage in HI-Z
              ('Active',  2),   # initialized, ready to receive / ready for direct transmit
              ('Filter',  3),   # RX channels only: active and filtering on configured labels
              ('Running', 4)]   # TX channels only: active and scheduler running
})

com['constant_groups'].append({
'name': 'Frame Status',
'type': 'uint8',
'constants': [('Timeout', 0),   # frame is overdue (frame data are last data received)
              ('Update',  1)]   # new frame received
})

com['constant_groups'].append({
'name': 'Scheduler Job',
'type': 'uint8',
'constants': [('Mute',   0),    # no     transmit
              ('Single', 1),    # single transmit (is set to mute after the transmit)
              ('Cyclic', 2)]    # cyclic transmit
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

com['packets'].append({
'type': 'function',
'name': 'Get Capabilities',
'elements': [('RX Channels',        'uint8',  1, 'out', {'range': (0, 16)}),
             ('RX Filter Frames',   'uint16', 1, 'out'),
             ('TX Channels',        'uint8',  1, 'out', {'range': (0,  8)}),
             ('TX Schedule Slots',  'uint16', 1, 'out'),
             ('TX Schedule Frames', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Get the number of RX and TX channels available on this device,
plus the max number of scheduler slots and scheduled frames.
""",
'de':
"""

"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set Heartbeat Callback Configuration',
'elements': [('Channel', 'uint8', 1, 'in', {'constant_group': 'Channel'}),
             ('Period',  'uint8', 1, 'in',  {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool',  1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period is the period with which the :cb:`Heartbeat` callback is triggered periodically.
A value of 0 turns the callback off.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Heartbeat Callback Configuration',
'elements': [('Channel', 'uint8', 1, 'in', {'constant_group': 'Channel'}),
             ('Period',  'uint8', 1, 'out',  {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool',  1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Heartbeat',
'elements': [('Channel',          'uint8',  1, 'out', {'constant_group': 'Channel'}),
             ('Sequence Number',  'uint8',  1, 'out'),
             ('Channel Mode',     'uint8',  1, 'out', {'constant_group': 'Channel Mode'}),
             ('Frames Processed', 'uint16', 1, 'out'),
             ('Frames Lost',      'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set Heartbeat Callback Configuration`.
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set Channel Configuration',
'elements': [('Channel',   'uint8',  1, 'in',  {'constant_group': 'Channel'}),
             ('Parity',    'uint8',  1, 'in',  {'constant_group': 'Parity'}),
             ('Speed',     'uint8',  1, 'in',  {'constant_group': 'Speed'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Configure the selected channel:

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
'elements': [('Channel',   'uint8',  1, 'in',  {'constant_group': 'Channel'}),
             ('Parity',    'uint8',  1, 'out',  {'constant_group': 'Parity'}),
             ('Speed',     'uint8',  1, 'out',  {'constant_group': 'Speed'})],
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
'name': 'Set Channel Mode',
'elements': [('Channel',   'uint8',  1, 'in',  {'constant_group': 'Channel'}),
             ('Mode',      'uint8',  1, 'in',  {'constant_group': 'Channel Mode'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Set the channel to active or passive mode. In passive mode, the TX channel output becomes high-Z.
This may happen while still frames are sent from the TX FIFO, effectively trashing these frames.
RX channels are not affected by this setting.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Channel Mode',
'elements': [('Channel',   'uint8',  1, 'in',  {'constant_group': 'Channel'}),
             ('Mode',      'uint8',  1, 'out',  {'constant_group': 'Channel Mode'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Set the channel to active or passive mode. In passive mode, the TX channel output becomes high-Z.
This may happen while still frames are sent from the TX FIFO, effectively trashing these frames.
RX channels are not affected by this setting.

Returns an error if:
 * the selected channel is not a valid channel,
 * the selected channel is not initialized yet,
 * the mode is neither 'active' nor 'passive'.
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
Disables the priority receive buffers of the selected channel.
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
Set the labels for the priority receive buffers of the selected channel.
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
Read the labels configured on the priority receive buffers of the selected channel.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Clear RX Labels',
'elements': [('Channel', 'uint8',  1, 'in',  {'constant_group': 'Channel'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Clear all RX label configurations for the given channel(s).
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set RX Label Configuration',
'elements': [('Channel', 'uint8',  1, 'in',  {'constant_group': 'Channel'}),
             ('Label',   'uint8',  1, 'in',),
             ('SDI',     'uint8',  1, 'in',  {'constant_group': 'SDI'}),
             ('Timeout', 'uint16', 1, 'in',  {'scale': (1, 100), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Set the function of the SDI bits and the timeout for a specific label on the selected channel.
The timeout value is in multiples of 10 ms, a timeout value of zero disables the timeout.

Returns an error if:
 * the selected channel is not a valid channel
 * the value for SDI     is not valid
 * the value for timeout is not valid (> 250)
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Get RX Label Configuration',
'elements': [('Channel', 'uint8',  1, 'in',  {'constant_group': 'Channel'}),
             ('Label',   'uint8',  1, 'in'),
             ('SDI',     'uint8',  1, 'out', {'constant_group': 'SDI'}),
             ('Timeout', 'uint16', 1, 'out', {'scale': (1, 100), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Set the function of the SDI bits and the timeout for a specific label on the selected channel.
The timeout value is in multiples of 10 ms, a timeout value of zero disables the timeout.

Returns an error if:
 * the selected channel is not a valid channel
 * the value for SDI     is not valid
 * the value for timeout is not valid (> 250)
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Read Next Frame',
'elements': [('Channel', 'uint8',  1, 'in', {'constant_group': 'Channel'}),
             ('Buffer',  'uint8',  1, 'in', {'constant_group': 'Buffer' }),
             ('Status',  'bool',  1,  'out'),
             ('Frame',   'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Do a direct read of a A429 frame from the selected receive channel and buffer.
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set Receive Frame Callback Configuration',
'elements': [('Channel',             'uint8', 1, 'in', {'constant_group': 'Channel'}),
             ('Period',              'uint8', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool',  1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Enables or disables the generation of callbacks on receiving A429 frames.

If the `value has to change`-parameter is set to TRUE, the callback is only
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
'name': 'Get Receive Frame Callback Configuration',
'elements': [('Channel',             'uint8', 1, 'in',  {'constant_group': 'Channel'}),
             ('Period',              'uint8', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool',  1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Enables or disables the generation of callbacks on receiving A429 frames.

If the `value has to change`-parameter is set to TRUE, the callback is only
triggered when the frame data have changed, else it is triggered on every
reception of a new frame.
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'callback',
'name': 'Receive Frame',
'elements': [('Channel',      'uint8',  1, 'out', {'constant_group': 'Channel'}),
             ('Buffer',       'uint8',  1, 'out', {'constant_group': 'Buffer'}),
             ('Frame Status', 'uint8',  1, 'out', {'constant_group': 'Frame Status'}),
             ('Frame',        'uint32', 1, 'out'),
             ('Age',          'uint8',  1, 'out', {'range':  (0, 250)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered according to the configuration set by :func:`Set Receive Frame Callback Configuration`.

The parameter 'Frame Status' indicates if a new frame was received, or if a timeout encountered.
The timeout can be configured with the :func:'Configure Label', default is timeout disabled.
The other :word:`parameters` are the same as with :func:`Read next Frame`.
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
Immediate write of an A429 frame to the selected transmit channel.

Returns an error if:
 * the selected channel is not a valid TX channel,
 * the selected channel is not configured yet,
 * the transmit queue   is full.
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Write Frame Scheduled',
'elements': [('Frame Index', 'uint16', 1, 'in'),
             ('Frame',       'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Set or update the value of a frame that is transmitted by the scheduler.

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
'name': 'Set Schedule Entry',
'elements': [('Channel',     'uint8',  1, 'in',  {'constant_group': 'Channel'}),
             ('Slot Index',  'uint16', 1, 'in'),
             ('Job',         'uint8',  1, 'in',  {'constant_group': 'Scheduler Job'}),
             ('Frame Index', 'uint16', 1, 'in'),
             ('Dwell Time',  'uint8',  1, 'in',  {'scale': (1, 1000), 'unit': 'Second', 'default': 10})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Program a TX schedule entry for the selected TX channel:

 * Channel:     selected TX channel
 * Slot_Index:  schedule entry
 * Job:         activity assigned to this job
 * Frame_Index: frame    assigned to this slot (by frame index)
 * Dwell_Time:   time in ms to wait before executing the next slot

Returns an error if:
 * the selected channel is not a valid TX channel,
 * the slot  index number is outside of the valid range.
 * the frame index number is outside of the valid range.
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
             ('Slot Index',  'uint16', 1, 'in'),
             ('Job',         'uint8',  1, 'out', {'constant_group': 'Scheduler Job'}),
             ('Frame Index', 'uint16', 1, 'out'),
             ('Frame',       'uint32', 1, 'out'),
             ('Dwell Time',  'uint8',  1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 10})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Read a TX schedule entry.

 * Channel:     selected TX channel
 * Slot Index:  schedule entry (0..num_tx_slots-1)
 * Job:         activity done in this job
 * Frame Index: index of the frame assigned to this slot
 * Frame:       value of the frame assigned to this slot
 * Dwell Time:  time in ms waited before the next slot is executed
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
             ('Slot Index First', 'uint16', 1, 'in'),
             ('Slot Index Last',  'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Clear a range of TX schedule entries.

 * Channel:   selected TX channel
 * First:     first schedule entry (0..num_tx_slots-1) to be cleared
 * Last:      last  schedule entry (0..num_tx_slots-1) to be cleared

Returns an error if:
 * the selected channel is not a valid TX channel,
 * the selected slot numbers are outside of the valid range,
 * the slot numbers are in wrong order (last < first)
""",
'de':
"""
"""
}]
})

