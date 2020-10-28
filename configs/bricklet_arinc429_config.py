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
'constants': [('OK',               0),  # everything went OK
              ('No Write',         1),  # write register, but OP code is for read
              ('No Read',          2),  # read  register, but OP code is for write
              ('Invalid OP Code',  3),  # invalid OP code
              ('Invalid Length',   4),  # invalid length of OP code argument
              ('SPI',              5)], # error during SPI communication
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
'constants': [('SDI0', 0),     # SDI bits used for address extension, SDI 0
              ('SDI1', 1),     # SDI bits used for address extension, SDI 0
              ('SDI2', 2),     # SDI bits used for address extension, SDI 0
              ('SDI3', 3),     # SDI bits used for address extension, SDI 0
              ('Data', 4)]     # SDI bits used for data
})

com['constant_groups'].append({
'name': 'Parity',
'type': 'uint8',
'constants': [('Data', 0),     # parity bit is used for data or parity provided by user
              ('Auto', 1)]     # parity bit is set automatically
})

com['constant_groups'].append({
'name': 'Speed',
'type': 'uint8',
'constants': [('HS', 0),       # high speed
              ('LS', 1)]       # low  speed
})

com['constant_groups'].append({
'name': 'Channel Mode',
'type': 'uint8',
'constants': [('Passive', 0),  # initialized, but output stage in HI-Z
              ('Active',  1),  # initialized, ready to receive / ready for direct transmit
              ('Run',     2)]  # TX channels only: active and scheduler running
})

com['constant_groups'].append({
'name': 'Frame Status',
'type': 'uint8',
'constants': [('Update',  0),  # frame is overdue (frame data are last data received)
              ('Timeout', 1)]  # new or updated frame received
})

com['constant_groups'].append({
'name': 'Scheduler Job',
'type': 'uint8',
'constants': [('Skip',        0),   # no transmit, no   dwell
              ('Dwell',       1),   # no transmit, only dwell
              ('Single',      2),   # send a frame once            and dwell
              ('Cyclic',      3),   # send a frame repeatedly      and dwell
              ('Retrans RX1', 4),   # send a frame received on RX1 and dwell
              ('Retrans RX2', 5)]   # send a frame received on RX1 and dwell
})

com['constant_groups'].append({
'name': 'A429 Mode',
'type': 'uint8',
'constants': [('Normal',  0),  # normal RX/TX operations
              ('Debug',   1)]  # high-level FW functions stopped
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
Low-level debug function to read the discrete signals from the A429 chip.
RX Discretes Bit   9: MB2-1   - pending frame in RX2, PRIO 1 mailbox
                   8: MB2-2   -                            2 mailbox
                   7: MB2-3   -                            3 mailbox
                   6: R2FLAG  -                       FIFO
                   5: R2INT   -                       FIFO (pulse only)
                   4: MB1-1   - pending frame in RX1, PRIO 1 mailbox
                   3: MB1-2   -                            2 mailbox
                   2: MB1-3   -                            3 mailbox
                   1: R1FLAG  -                       FIFO
                   0: R1INT   -                       FIFO (pulse only)
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
'elements': [('OP Code',      'uint8', 1,  'in',  {}),
             ('Value Length', 'uint8', 1,  'out', {}),
             ('Value Data',   'uint8', 32, 'out', {}),
             ('RW Error',     'uint8', 1,  'out',  {'constant_group': 'RW Error'})],
'high_level': {'stream_out': {'name': 'Value', 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Low-level debug function to execute a direct SPI read access on the A429 chip.
 * OP Code:      code number of the SPI read command
 * Value Length: number of bytes read
 * Value Data:   data bytes read
 * RW Error:     'OK' if the read access was successful, else error code
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Debug Write Register Low Level',
'elements': [('OP Code',      'uint8', 1,  'in', {}),
             ('Value Length', 'uint8', 1,  'in', {}),
             ('Value Data',   'uint8', 32, 'in', {}),
             ('RW Error',     'uint8', 1,  'out',  {'constant_group': 'RW Error'})],
'high_level': {'stream_in': {'name': 'Value', 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Low-level debug function to execute a direct SPI write access on the A429 chip.
 * OP Code:      code number of the SPI read command
 * Value Length: number of bytes to write
 * Value Data:   data bytes to write
 * RW Error:     'OK' if the write access was successful, else error code
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Capabilities',
'elements': [('TX Total Scheduler Tasks', 'uint16', 1, 'out'),
             ('TX Used Scheduler Tasks',  'uint16', 1, 'out'),
             ('RX Total Frame Filters',   'uint16', 1, 'out'),
             ('RX Used Frame Filters',    'uint16', 2, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Get the TX and RX capabilities and their current usage:
 * TX Total Scheduler Tasks: total number of task entries in the scheduling table.
 * TX Used Scheduler Tasks:  number of task entries that are currently in use.
 * RX Total Frame Filters:   total number of frame filters that can be defined per channel.
 * RX Used Frame Filters:    number of frame filters that are currently in use per each channel.
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
Set the bricklet heartbeat which reports the statistics counters for processed frames and lost frames.
The period is the period with which the :cb:`Heartbeat` callback is triggered periodically. A value of 0 turns the callback off.
When 'Value Has To Change' is enabled, the heartbeat will only be sent if there is a change in the statistics numbers.
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
Get the configuration of the bricklet heartbeat reporting the statistics counters.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Heartbeat',
'elements': [('Seq Number',       'uint8',  1, 'out'),
             ('Timestamp',        'uint16', 1, 'out'),
             ('Frames Processed', 'uint16', 3, 'out'),
             ('Frames Lost',      'uint16', 3, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set Heartbeat Callback Configuration`. It reports the statistics counters
for processed frames and lost frames for all TX and RX channels.
 * Seq Number:       running counter that is incremented with each callback, starting with 0 and rolling over after 255 to 1. It will restart from 0 whenever the heartbeat is turned off and on again. This counter can be used to detect lost callbacks.
 * Timestamp:        running counter that is incremented on every millisecond, starting when the bricklet is powered up and rolling over after 65535 to 0. This counter can be used to measure the relative timing between events.
 * Frames Processed: number of Arinc429 frames that are transmitted or received on the respective channels TX, RX1 and RX2.
 * Frames Lost:      TX channel: number of Arinc429 frames that could not be transmitted due to a full transmit buffer, RX channels: number of received Arinc429 frames that could not be reported due to a full callback buffer.
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
Set the data transmission properties of the selected channel:
 * Channel: channel to configure
 * Parity:  'parity_auto' for automatic parity adjustment, 'parity_data' for parity bit supplied by the application or if used for data.
 * Speed:   'speed_hs' for high speed mode (100 kbit/s), 'speed_ls' for low speed mode (12.5 kbit/s).
When parity set to 'parity_auto', frames received with a parity error will be counted in the lost frames counter but discarded otherwise.
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
Get the data transmission properties of the selected channel.
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
 * passive: TX channel: all transmissions are stopped and the hardware interface becomes high-Z. RX channels: all arriving frames will be discarded.
 * active:  TX channel: Arinc429 frames can be sent via the 'Write Frame Direct' function. RX channels: arriving frames will be processed according to the frame filter and callback settings.
 * run:     TX channels only: the scheduler will run and transmit frames according to the entries made in the scheduler task table.
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
'name': 'Clear All RX Filters',
'elements': [('Channel', 'uint8',  1, 'in',  {'constant_group': 'Channel'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Clear all receive filters on the selected RX channel.
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
             ('SDI',     'uint8',  1, 'in',  {'constant_group': 'SDI'}),
             ('Success', 'bool',   1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Clear one receive filter on the selected RX channel.
 * Channel: selected channel.
 * Label:   label code of the filter.
 * SDI:     SDI code of the filter (SDI_SDI0 to SDI_SDI3 or SDI_DATA if SDI bits are used for data).
 * Success: returns 'True' if the filter was cleared or 'False' if a respective filter was not set.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set RX Standard Filters',
'elements': [('Channel', 'uint8',  1, 'in',  {'constant_group': 'Channel'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Set a receive filter for each label value (0-255) with SDI bits set for data. Any previously existing filters will be overwritten.
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
             ('SDI',     'uint8',  1, 'in',  {'constant_group': 'SDI'}),
             ('Success', 'bool',   1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Set a receive filter on the selected channel:
 * Channel: selected channel.
 * Label:   label code for the filter.
 * SDI:     SDI code for the filter (SDI_SDI0 to SDI_SDI3 or SDI_DATA if SDI bits are used for data).
 * Success: returns 'True' if the filter was set or 'False' if a respective filter could not be set up (e.g. because label + SDI collides with an already existing filter or all available filters are used up).
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
Query if a specific filter is set up or not:
 * Channel:    channel to query.
 * Label:      label code to query for.
 * SDI:        SDI usage to query for (SDI_SDI0 to SDI_SDI3 or SDI_DATA if SDI bits shall be used for data).
 * Configured: returns 'True' if the inquired filter exists, else 'False'.
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
             ('Age',     'uint16', 1, 'out', {'scale': (1, 60000), 'unit': 'Second', 'default': 0})],  # TODO 1 - 60.000 milli-seconds
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Direct read of an Arinc429 frame, i.e. without using the callback mechanism.
In order to be able to do a direct read of a frame with a certain label and SDI combination, a respective receive filter needs to be set up beforehand.
 * Channel: RX channel to read from.
 * Label:   label code of the frame to read.
 * SDI:     SDI code of the frame to read (SDI_SDI0 to SDI_SDI3 or SDI_DATA if SDI bits are used for data).
 * Status:  returns 'True' if a respective frame was received, else 'False'.
 * Frame:   returns the complete Arinc429 frame including the label and SDI bits. If 'parity_auto' is set for the channel, the parity bit will always come as 0.
 * Age:     time in milliseconds since this frame (label + SDI combination) was received last. If not received for so far or after a previous timeout, 60000 or the timeout value set with the 'Set RX Callback Configuration' function will be returned.
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
             ('Timeout',             'uint16', 1, 'in', {'scale': (1, 60000), 'unit': 'Second', 'default': 1000})],   # TODO 1 - 60.000 milli-seconds
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Set the configuration of the Arinc429 frame reception callback:
 * Channel:             selected RX channel.
 * Enabled:             select 'True' for activating the frame callbacks and 'False' for deactivating them.
 * Value Has To Change: select 'True' if callbacks shall only be sent for frames whose data have changed. With 'False' a callback will be sent on every frame reception.
 * Timeout:             time period for all frames (label and SDI combinations) on this channel.

Despite on frame reception, a callback is also generated if a frame encounters a timeout, i.e. if it is not periodically received again before the set timeout period has expired.
In order to have callbacks being generated at all, respective receive filters need to be set up.
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
             ('Timeout',             'uint16', 1, 'out', {'scale': (1, 60000), 'unit': 'Second', 'default': 1000})],  # TODO 1 - 60.000 milli-seconds
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Get the configuration of the frame reception callback.
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
             ('Seq Number',      'uint8',  1, 'out'),
             ('Timestamp',       'uint16', 1, 'out'),
             ('Frame Status',    'uint8',  1, 'out', {'constant_group': 'Frame Status'}),
             ('Frame',           'uint32', 1, 'out'),
             ('Age',             'uint16', 1, 'out', {'scale': (1, 60000), 'unit': 'Second'})],  # TODO 1 - 60.000 milli-seconds
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered according to the configuration set by :func:`Set RX Callback Configuration`.
 * Channel:      RX channel on which the frame was received.
 * Seq Number:   running counter that is incremented with each callback, starting with 0 and rolling over after 255 to 1. It will restart from 0 whenever the callback is turned off and on again. This counter can be used to detect lost callbacks.
 * Timestamp:    running counter that is incremented on every millisecond, starting when the bricklet is powered up and rolling over after 65535 to 0. This counter can be used to measure the relative timing between frame receptions.
 * Frame Status: 'update' signals that a new frame (new data) was received, whereas 'timeout' signals that the frame (label and SDI combination) encountered the timeout state.
 * Frame:        the complete Arinc429 frame including the label and SDI bits. If 'parity_auto' is set for the channel, the parity bit will always come as 0.
 * Age:          time in milliseconds since this frame (label + SDI combination) was received last. If not received for so far or after a previous timeout, 60000 or the timeout value set with the 'Set RX Callback Configuration' function will be returned.

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
Immediately transmit an Arinc429 frame:
 * Channel: selected transmit channel.
 * frame:   complete Arinc429 frame including the label and SDI bits. If 'parity_auto' is set for the channel, the parity bit will be set (adjusted) automatically.
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
Set or update an Arinc429 frame that is transmitted by the scheduler using the task types 'Single' and 'Cyclic'.
 * Channel:     selected transmit channel.
 * Frame Index: index number that will be used in the transmit scheduler task table to refer to this frame.
 * frame:       complete Arinc429 frame including the label and SDI bits. If 'parity_auto' is set for the channel, the parity bit will be set (adjusted) automatically.
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
Clear a range of transmit scheduler task table entries:
 * Channel: selected TX channel.
 * First:   index of the first table entry to be cleared.
 * Last:    index of the last  table entry to be cleared.
To clear a single entry, set 'First' and 'Last' to the one index of the one entry to be cleared.
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
             ('Dwell Time',  'uint8',  1, 'in',  {'scale': (1, 250), 'unit': 'Second', 'default': 10})],  # TODO 1 - 250 milli-seconds
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Set an entry in the transmit scheduler task table:
 * Channel:     selected TX channel
 * Task Index:  index number of the task, the scheduler processes the task table in ascending order of these index numbers.
 * Job:         activity assigned to this entry, see below.
 * Frame Index: frame assigned to this task, either the 'Frame Index' used along with the :func: `Write Frame Scheduled` or the extended label (label + SDI) in case of RX1/RX2 retransmits.
 * Dwell Time:  time to wait before executing the next task table entry (0-250 milliseconds).

When the scheduler is set to 'run' mode via the :func:`Set Channel Mode`, it continuously loops through the task table and executes the assigned tasks.
It starts with the task stored at task index 0.
The scheduler can execute the following activity types (jobs):
 * Skip:        the task is skipped, i.e. no frame is transmitted and no dwelling is done. The frame index and dwell time are not used.
 * Dwell        the scheduler executes the dwelling but does not transmit any frame. The frame index is not used.
 * Single:      the scheduler transmits the referenced frame, but only once. On subsequent executions the frame is not sent until it is renewed via the :func:`Write Frame Scheduled`, then the process repeats.
 * Cyclic:      the scheduler transmits the referenced frame and executed the dwelling on each round.
 * Retrans RX1: the scheduler retransmits a frame that was previously received on the RX1 channel. The frame to send is referenced by setting the 'Frame Index' to its extended label code, which is a 10 bit number made of the label code in the lower bits and the two SDI bits in the upper bits. If the SDI bits are used for data, set the SDI bits to zero. As long as the referenced frame was not received yet, or if it is in timeout, no frame will be sent.
 * Retrans RX2: same as before, but for frames received on the RX2 channel.
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
             ('Task Index',  'uint16', 1, 'in'),
             ('Job',         'uint8',  1, 'out', {'constant_group': 'Scheduler Job'}),
             ('Frame Index', 'uint16', 1, 'out'),
             ('Frame',       'uint32', 1, 'out'),
             ('Dwell Time',  'uint8',  1, 'out', {'scale': (1, 250), 'unit': 'Second', 'default': 10})],   # TODO 1 - 250 milli-seconds
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Get a transmit scheduler task table entry.
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Reset A429',
'elements': [('Mode', 'uint8', 1, 'in', {'constant_group': 'A429 Mode', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Reset the A429 bricklet. The bricklet will restart in the selected mode:
 * 'Normal': normal operating mode with all high-level Arinc429 frame processing being executed.
 * 'Debug':  debug mode with all high-level processing suspended, for use in conjunction with the low-level debug functions.
""",
'de':
"""
"""
}]
})

