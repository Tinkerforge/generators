# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# ARINC429 Breakout Bricklet communication config

from generators.configs.commonconstants      import THRESHOLD_OPTION_CONSTANT_GROUP
from generators.configs.commonconstants      import add_callback_value_function
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
        'en': 'ARINC429 single transmitter and dual receiver',
        'de': 'ARINC429 1 Kanal Sender und 2 Kanal Empfänger'
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
'name': 'Channel',
'type': 'uint8',
'constants': [('TX',    0),    # all TX channels
              ('TX1',   1),    # TX channel 1
#             ('TX2',   2),    # provision for potential future products / common API
#             ('TX3',   3),    # ...
#             ('TX4',   4),    # ...
#             ('TX5',   5),    # ...
#             ('TX6',   6),    # ...
#             ('TX7',   7),    # ...
#             ('TX8',   8),    # ...
#             ('TX9',   9),    # ...
#             ('TX10', 10),    # ...
#             ('TX11', 11),    # ...
#             ('TX12', 12),    # ...

              ('RX',   32),    # all RX channels
              ('RX1',  33),    # RX channel 1
              ('RX2',  34)]    # RX channel 2
#             ('RX3',  35),    # provision for potential future products / common API
#             ('RX4',  36),    # ...
#             ('RX5',  37),    # ...
#             ('RX6',  38),    # ...
#             ('RX7',  39),    # ...
#             ('RX8',  40),    # ...
#             ('RX9',  41),    # ...
#             ('RX10', 42),    # ...
#             ('RX11', 43),    # ...
#             ('RX12', 44)]    # ...
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
'name': 'Status',
'type': 'uint8',
'constants': [('New',        0),  # new     frame received (or 1st frame after a timeout)
              ('Update',     1),  # updated frame received
              ('Timeout',    2),  # frame is overdue (frame data are last data received)
              ('Scheduler',  3),  # scheduler message
              ('Statistics', 4)]  # heartbeat message
})

com['constant_groups'].append({
'name': 'Scheduler Job',
'type': 'uint8',
'constants': [('Skip',        0),   # skip job        (no transmit, no dwell)
              ('Callback',    1),   # send a callback              (no dwell)
              ('Stop',        2),   # stop scheduler  (no transmit, no dwell)
              ('Jump',        3),   # jump to given job index, dwell with next return
              ('Return',      4),   # return to last Jump source   (no dwell)
              ('Dwell',       5),   # dwell only      (no transmit)
              ('Single',      6),   # send a frame once            and dwell
              ('Cyclic',      7),   # send a frame repeatedly      and dwell
              ('Retrans RX1', 8),   # send a frame received on RX1 and dwell
              ('Retrans RX2', 9)]   # send a frame received on RX2 and dwell
})

com['constant_groups'].append({
'name': 'TX Mode',
'type': 'uint8',
'constants': [('Transmit', 0), # transmit the frame / trigger a new single transmit
              ('Mute',     1)] # do not transmit the frame
})

com['packets'].append({
'type': 'function',
'name': 'Get Capabilities',
'elements': [('TX Total Scheduler Jobs', 'uint16', 1, 'out'),
             ('TX Used Scheduler Jobs',  'uint16', 1, 'out'),
             ('RX Total Frame Filters',  'uint16', 1, 'out'),
             ('RX Used Frame Filters',   'uint16', 2, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Gets the capabilities of the ARINC429 Bricklet as of the currently loaded firmware:
 * TX Total Scheduler Jobs: total number of job entries in the scheduling table.
 * TX Used Scheduler Jobs:  number of job entries that are currently in use.
 * RX Total Frame Filters:  total number of frame filters that can be defined per channel.
 * RX Used Frame Filters:   number of frame filters that are currently in use per each channel.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Heartbeat Callback Configuration',
'elements': [('Channel',             'uint8',  1, 'in', {'constant_group': 'Channel'         }),
             ('Enabled',             'bool',   1, 'in', {'default': False                    }),
             ('Value Has To Change', 'bool',   1, 'in', {'default': False                    }),
             ('Period',              'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the bricklet heartbeat callback function which reports the statistics counters for processed frames and lost frames.
The period is the period with which the :cb:`Heartbeat Message` callback is triggered periodically. A value of 0 turns the callback off.
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
'elements': [('Channel',             'uint8',  1, 'in',  {'constant_group': 'Channel'         }),
             ('Enabled',             'bool',   1, 'out', {'default': False                    }),
             ('Value Has To Change', 'bool',   1, 'out', {'default': False                    }),
             ('Period',              'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Gets the current configuration of the bricklet heartbeat callback, see :func:`Set Heartbeat Callback Configuration`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Heartbeat Message',
'elements': [('Channel',          'uint8',  1, 'out', {'constant_group': 'Channel'}),
             ('Status',           'uint8',  1, 'out', {'constant_group': 'Status' }),
             ('Seq Number',       'uint8',  1, 'out'),
             ('Timestamp',        'uint16', 1, 'out'),
             ('Frames Processed', 'uint16', 1, 'out'),
             ('Frames Lost',      'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set Heartbeat Callback Configuration`. It reports the statistics counters
for processed frames and lost frames for all TX and RX channels.
 * Channel:          channel from which this heartbeat messages originates.
 * Status:           will always be 'statistics'.
 * Seq Number:       running counter that is incremented with each callback, starting with 0 and rolling over after 255 to 1. It will restart from 0 whenever the callback is turned off and on again. This counter can be used to detect lost callbacks.
 * Timestamp:        running counter that is incremented on every millisecond, starting when the bricklet is powered up and rolling over after 65535 to 0. This counter can be used to measure the relative timing between frame receptions.
 * Frames Processed: number of Arinc429 frames that are transmitted or received on the respective channels TX, RX1 and RX2.
 * Frames Lost:      TX channel: number of Arinc429 frames that could not be transmitted due to a full transmit FIFO buffer, RX channels: number of received Arinc429 frames that could not be reported due to a full callback FIFO buffer.
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
Sets the data transmission properties of the selected channel:
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
Gets the data transmission properties of the selected channel. The channel parameter and the data returned use the same constants
as the :func:`Set Channel Configuration`,  despite that the all-channels constants CHANNEL_TX and CHANNEL_RX can not be used.
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
Sets the operating mode of the selected channel(s):
 * passive: TX channel: all transmissions are stopped and the hardware interface becomes high-Z. RX channels: all arriving frames will be discarded.
 * active:  TX channel: Arinc429 frames can be sent via the 'Write Frame Direct' function. RX channels: arriving frames will be processed according to the frame filter and callback settings.
 * run:     TX channels only: the scheduler will run and transmit frames according to the entries made in the scheduler job table.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Channel Mode',
'elements': [('Channel',   'uint8',  1, 'in',   {'constant_group': 'Channel'     }),
             ('Mode',      'uint8',  1, 'out',  {'constant_group': 'Channel Mode'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Gets the operating mode of the selected channel.  The channel parameter and the  data returned use the same constants as the
:func:`Set Channel Configuration`, despite that the all-channels constants CHANNEL_TX and CHANNEL_RX can not be used.
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
Clears all receive filters on the selected RX channel(s). The RX channels will only process those Arinc429 frames that pass the
input filtering stage. With this command, all filters are cleared, thus all incoming Arinc429 frames will be blocked from further
processing.
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
Clears a specific receive filter on the selected RX channel(s). The RX channels will only process those Arinc429 frames that pass
the input filtering stage. With this command, an Arinc429 frame matching the given parameters will be blocked by the filter.
 * Channel: selected channel.
 * Label:   label code of the filter.
 * SDI:     SDI code of the filter (SDI_SDI0 to SDI_SDI3 or SDI_DATA if SDI bits are used for data).
The function either returns 'True' if the filter was cleared or 'False' if a respective filter was not set.
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
Sets a receive filter for each label value (0-255 / 0o000-0o377) with the SDI bits set for data. Any previously existing filters will be overwritten.
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
Sets a specific receive filter on the selected channel(s):
 * Channel: selected channel.
 * Label:   label code for the filter.
 * SDI:     SDI code for the filter (SDI_SDI0 to SDI_SDI3 or SDI_DATA if SDI bits are used for data).
The function either returns 'True' if the filter was set or 'False' if a respective filter could not be created e.g. because the given combination
of label and SDI collides with an already existing filter, or because all available filters are used up (see the get_capabilities() function.
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
Queries if a filter for the given combination of label and SDI is set up or not:
 * Channel:    channel to query.
 * Label:      label code to query for.
 * SDI:        SDI usage to query for (SDI_SDI0 to SDI_SDI3 or SDI_DATA if SDI bits shall be used for data).
The function will return 'True' if the queried filter filter exists, else 'False'.
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
             ('Age',     'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Executes a direct read of an Arinc429 frame, i.e. without using the callback mechanism.
In order to be able to do a direct read of a frame with a certain label and SDI combination, a respective receive filter needs to be set up beforehand.
  * Channel: RX channel to read from.
  * Label:   label code of the frame to read. Beware that the label codes are usually given in octal notation, so make sure to use the correct notation (i.e. 0o377).
  * SDI:     SDI code of the frame to read (SDI_SDI0 to SDI_SDI3 or SDI_DATA if SDI bits are used for data).

The function return the following data:
  * Status:  returns 'True' if a respective frame was received, else 'False'.
  * Frame:   returns the complete Arinc429 frame including the label and SDI bits as a 32 bit integer. If 'parity_auto' is set for the channel, the parity bit will always come as 0. Opposite to the line transmission format, in the API functions the label code is mirrored such that the label code can directly be extracted from the frame by simply grabbing the lower 8 bits.
  * Age:     time in milliseconds since a frame matching the label & SDI combination was received last. If no frame was received so far or after a previous timeout, either 60000 or the timeout value set with the :func:`Set RX Callback Configuration` will be returned.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set RX Callback Configuration',
'elements': [('Channel',             'uint8',  1, 'in', {'constant_group': 'Channel'         }),
             ('Enabled',             'bool',   1, 'in', {'default': False                    }),
             ('Value Has To Change', 'bool',   1, 'in', {'default': False                    }),
             ('Timeout',             'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the configuration of the Arinc429 frame reception callback:
 * Channel:             selected RX channel.
 * Enabled:             select 'True' for activating the frame callbacks and 'False' for deactivating them.
 * Value Has To Change: select 'True' if callbacks shall only be sent for frames whose data have changed. With 'False' a callback will be sent on every frame reception.
 * Timeout:             time period for all frames (label and SDI combinations) on this channel.

Despite on frame reception, a callback is also generated if a frame encounters a timeout, i.e. if it is not periodically received again before
the set timeout period has expired. In order to have callbacks being generated at all, respective receive filters need to be set up.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get RX Callback Configuration',
'elements': [('Channel',             'uint8',  1, 'in',  {'constant_group': 'Channel'         }),
             ('Enabled',             'bool',   1, 'out', {'default': False                    }),
             ('Value Has To Change', 'bool',   1, 'out', {'default': False                    }),
             ('Timeout',             'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Gets the configuration of the frame reception callback, see the :func:`Set RX Callback Configuration`.
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
             ('Status',          'uint8',  1, 'out', {'constant_group': 'Status' }),
             ('Seq Number',      'uint8',  1, 'out'),
             ('Timestamp',       'uint16', 1, 'out'),
             ('Frame',           'uint32', 1, 'out'),
             ('Age',             'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered according to the configuration set by :func:`Set RX Callback Configuration`.
 * Channel:      channel from which this frame messages originates.
 * Status:       'new' signals that the frame (label + SDI combination) was received for the first time ever or again after a previous timeout. 'update' signals that a new frame was received. 'timeout' signals that the frame (label and SDI combination) encountered the timeout state.
 * Seq Number:   running counter that is incremented with each callback, starting with 0 and rolling over after 255 to 1. It will restart from 0 whenever the callback is turned off and on again. This counter can be used to detect lost callbacks.
 * Timestamp:    running counter that is incremented on every millisecond, starting when the bricklet is powered up and rolling over after 65535 to 0. This counter can be used to measure the relative timing between frame receptions.
 * Frame:        holds the complete Arinc429 frame including the label and SDI bits as a 32 bit integer. If 'parity_auto' is set for the channel, the parity bit will always come as 0. Opposite to the line transmission format, in the API functions the label code is mirrored such that the label code can directly be extracted from the frame by simply grabbing the lower 8 bits.
 * Age:          time in milliseconds since this frame (label + SDI combination) was received last. If not received for so far or after a previous timeout, 60000 or the timeout value set with the :func:`Set RX Callback Configuration` will be returned.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Write Frame Direct',
'elements': [('Channel', 'uint8',  1, 'in', {'constant_group': 'Channel'}),
             ('Frame',   'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Immediately transmits an Arinc429 frame, given that the channel is in either ACTIVE or RUN mode. If the channel is in RUN mode and frames are sent
as per programmed schedule, using this function will inject additional frames into the transmission, independent of the scheduler's activities.

 * Channel: selected transmit channel, either CHANNEL_TX or CHANNEL_TX1 can be used as there is only one TX channel.
 * frame:   complete Arinc429 frame including the label and SDI bits.

The frame needs to be passed as a 32 bit integer. Opposite to the line transmission format, in the API functions
the label code is mirrored such that the label code can directly be written 1:1 into the lower 8 bits.
Beware that the label codes are usually given in octal notation, so make sure to use the correct notation
(i.e. 0o377). If 'parity_auto' is set for the channel, the parity bit will be set (adjusted) automatically.

Between the API and the actual Arinc429 line output, there is a 32 entry deep FIFO. If frames are written via
the API and/or in combination with a running TX scheduler, the FIFO may become overfilled and subsequently
frames will get lost. Such frame losses will be indicated in the statistics data sent with the heartbeat callback.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Write Frame Scheduled',
'elements': [('Channel',     'uint8',  1, 'in', {'constant_group': 'Channel'}),
             ('Frame Index', 'uint16', 1, 'in'),
             ('Frame',       'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets or updates an Arinc429 frame that is to be transmitted via the scheduler using the scheduler job types 'Single' or 'Cyclic'.
 * Channel:     selected transmit channel, either CHANNEL_TX or CHANNEL_TX1 can be used as there is only one TX channel.
 * Frame Index: index number (0-255) that will be used in the transmit scheduler job table to refer to this frame.
 * Frame:       complete Arinc429 frame including the label and SDI bits.

The frame needs to be passed as a 32 bit integer. Opposite to the line transmission format, in the API functions
the label code is mirrored such that the label code can directly be written 1:1 into the lower 8 bits.
Beware that the label codes are usually given in octal notation, so make sure to use the correct notation
(i.e. 0o377). If 'parity_auto' is set for the channel, the parity bit will be set (adjusted) automatically.

If the frame is used by a 'single transmit' scheduler job entry, setting or updating the frame with this function
triggers also triggers the next transmission.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Clear Schedule Entries',
'elements': [('Channel',         'uint8',  1, 'in', {'constant_group': 'Channel'}),
             ('Job Index First', 'uint16', 1, 'in'),
             ('Job Index Last',  'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Clears a range of transmit scheduler job table entries:
 * Channel: selected TX channel.
 * First:   index of the first table entry to be cleared.
 * Last:    index of the last  table entry to be cleared.
To clear a single entry, set 'First' and 'Last' to the one index of the one entry to be cleared.
Clearing scheduler entries actually means they are set to the job command 'Skip'.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Schedule Entry',
'elements': [('Channel',     'uint8',  1, 'in', {'constant_group': 'Channel'}),
             ('Job Index',   'uint16', 1, 'in'),
             ('Job',         'uint8',  1, 'in', {'constant_group': 'Scheduler Job'}),
             ('Frame Index', 'uint16', 1, 'in'),
             ('Dwell Time',  'uint8',  1, 'in', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets an entry in the transmit scheduler job table:
 * Channel:     selected TX channel, either CHANNEL_TX or CHANNEL_TX1 can be used as there is only one TX channel.
 * Job Index:   index number of the job, the scheduler processes the job table in ascending order of these index numbers. The index starts with 0, see the output of the get_capabilities() function for the total number of job indexes available. In firmware 2.3.0 it is 1000.
 * Job:         activity assigned to this entry, see below.
 * Frame Index: generally, the frame assigned to this job by the 'Frame Index' used along with the :func: `Write Frame Scheduled`.
                In case of a RX1 or RX2 retransmit job, the extended label (label + SDI) of the frame to be retransmitted.
                In case of the Jump command, the Job Index at which execution shall continue.
                In case of the Callback command, this number will be sent as 'Token' code (values 0-255 only).
                In all other cases (Skip, Stop, Dwell, Return) this parameter is not used.
 * Dwell Time:  time to wait before executing the next job table entry (0-250 milliseconds).

When the scheduler is set to 'run' mode via the :func:`Set Channel Mode`, it continuously loops through the job table and executes
the assigned tasks. It starts with the job stored at job index 0.
The scheduler can execute the following activity types (jobs):
 * Skip:        the job is skipped, i.e. no frame is transmitted and no dwelling is done. The frame index and dwell time are not used.
 * Stop:        the scheduler is stopped, i.e. the channel mode is reverted from 'run' to 'active'. The frame index and dwell time are not used.
 * Jump:        the scheduler immediately continues at the Job Index position given by the Frame Index parameter. The assigned dwell time will be executed when the scheduler runs into the next Return job.
 * Return:      the scheduler immediately continues at the next Job Index position following the last Jump command. Nested Jumps are not supported. The frame index and dwell time are not used.
 * Callback:    the scheduler triggers a callback message and immediately continues with executing the next job (dwell time is not used).
 * Dwell        the scheduler executes the dwelling but does not transmit any frame. The frame index is not used.
 * Single:      the scheduler transmits the referenced frame, but only once. On subsequent executions the frame is not sent until it is renewed via the :func:`Write Frame Scheduled`, then the process repeats.
 * Cyclic:      the scheduler transmits the referenced frame and executed the dwelling on each round.
 * Retrans RX1: the scheduler retransmits a frame that was previously received on the RX1 channel. The frame to send is referenced by setting the 'Frame Index' to its extended label code, which is a 10 bit number made of the label code in the lower bits and the two SDI bits in the upper bits. If the SDI bits are used for data, set the SDI bits to zero. As long as the referenced frame was not received yet, or if it is in timeout, no frame will be sent.
 * Retrans RX2: same as before, but for frames received on the RX2 channel.

The value assigned to the 'Frame Index' parameter varies with the activity type (job):

 * Single or Cyclic: frame index as used with the :func:`Write Frame Scheduled` of the frame to transmit. Valid range: 0-255
 * Retrans RX1/RX2:  extended label (label + SDI) of the frame to re-transmit. Valid range: 0-1023
 * Callback:         arbitrary number decided by the user, it will be reported in the callback via the 'Userdata' parameter. Valid range: 0-255
 * Jump:             next job index to jump to.

The :func:`Set Schedule Entry` can be called while the TX scheduler is running, i.e. the channel mode is set to 'RUN'.
Any change will take immediate effect once the scheduler passes along and executes the changed job entry.
Every time the scheduler is started, it will begin with the job stored at job index 0.
At the end of the programmed schedule there should be a 'Jump' command back to index 0 to avoid the scheduler wasting time in processing all the remaining 'Skip' commands.
Two or more TX schedules can be pre-programmed and then selected for execution by placing - and changing as desired - a 'Jump' at index 0 that then branches to the
sequence of commands destined to be executed. This can be arranged in arbitrary ways, e.g. to create schedules with fixed and variable parts, just by using the 'Jump'
command alike a track switch in railway.

When the dwell time of a transmit command is set to zero, the respective Arinc429 frames will be transmitted back-to-back on the physical link.
Beware that there is a FIFO between the scheduler and the actual physical transmitter that is limited to 32 frames. So after latest 32 frames enqueued with zero dwell
time, the scheduler needs to be commanded to do some dwelling. How much dwelling is required can be computed by the number of back-to-back frames and the speed setting:
in high speed mode each frame takes 0.36 ms, in low speed mode 2.88 ms.
If a certain sequence of frames is to be transmitted multiple times in a schedule, this sequence just needs to be put once into the scheduler table with a 'Return'
command at its end. This way, this sequence can be called from multiple placed (job indexes) throughout the main schedule using the 'Jump' command.
Please note that this kind of calling a subroutine can not be nested, i.e. there is no return index stack, the 'Return' command always branches to the job index following
the index of the last 'Jump' command encountered. In case a dwell time > 0 is set with the 'Jump' command, this dwell time will actually be executed on encountering the
'Return' command, thus as a dwell time to be done after the execution of the subsequence that was jumped to before.

The 'Callback' command can be used to notify the application program via a callback when the scheduler passes at the respective job index. This can be used for pure
reporting / surveillance purpose, or as a means to set up a self-clocked system in which the called application program's function in return does some modification of
the programmed sequence or alike.
The scheduler can also be programmed to stop itself via the 'Stop' command, e.g. to run a pre-programmed, accurately timed single-shot sequence of frame transmissions.
Placing a' Callback' command right before the 'Stop' command will inform the application program via a callback when the sequence is done.
When using several 'Callback' commands in a schedule, each of them can be uniquely identified in the receiving application program by assigning a different 'userdata'
value to each callback command.

With the aid of the 'Retrans' commands, a frame transmission schedule can be set up whose frame timing is defined by the schedule, but whose frame's payload is taken
from the frames received via the RX1 or RX2 channel. This opens possibilities to create an autonomously operating time base corrector or re-scheduling machinery, to
zip the frames from two A429 buses onto one common bus, to create inline filers to remove certain frames (by their label & SDI code), to insert frames into a stream,
to exchange the payload of certain frames on-the-fly, and much more.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Schedule Entry',
'elements': [('Channel',     'uint8',  1, 'in',  {'constant_group': 'Channel'         }),
             ('Job Index',   'uint16', 1, 'in'),
             ('Job',         'uint8',  1, 'out', {'constant_group': 'Scheduler Job'   }),
             ('Frame Index', 'uint16', 1, 'out'),
             ('Frame',       'uint32', 1, 'out'),
             ('Dwell Time',  'uint8',  1, 'out', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Gets the definition of a transmit scheduler job table entry, refer to the :func:`Set Schedule Entry`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Restart',
'elements': [],
'since_firmware': [2, 0, 0],
'doc': ['bf', {
'en':
"""
Reverts the whole bricklet into its power-up default state.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Scheduler Message',
'elements': [('Channel',    'uint8',  1, 'in',  {'constant_group': 'Channel'}),
             ('Status',     'uint8',  1, 'out', {'constant_group': 'Status' }),
             ('Seq Number', 'uint8',  1, 'out'),
             ('Timestamp',  'uint16', 1, 'out'),
             ('Userdata',   'uint8',  1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered by the 'Callback' job in the transmit schedule.
 * Channel:          channel from which this frame messages originates, will always be 'CHANNEL_TX1'.
 * Status:           will always be 'scheduler'
 * Seq Number:       running counter that is incremented with each callback, starting with 0 and rolling over after 255 to 1. It will restart from 0 whenever the callback is turned off and on again. This counter can be used to detect lost callbacks.
 * Timestamp:        running counter that is incremented on every millisecond, starting when the bricklet is powered up and rolling over after 65535 to 0. This counter can be used to measure the relative timing between frame receptions.
 * Userdata:         8 bit number as set in the scheduler callback job
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Frame Mode',
'elements': [('Channel',     'uint8',  1, 'in', {'constant_group': 'Channel'}),
             ('Frame Index', 'uint16', 1, 'in'),
             ('Mode',        'uint8',  1, 'in', {'constant_group': 'TX Mode'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Stops / resumes the transmission of a specific frame or trigger another single-transmit. This
function only works on frames that are sent via the TX scheduler jobs 'single' and 'cyclic'.
 * Channel:     selected transmit channel, either CHANNEL_TX or CHANNEL_TX1 can be used as there is only one TX channel.
 * Frame Index: index number that will be used in the transmit scheduler job table to refer to this frame.
 * Mode :       either 'Transmit' to transmit the frame / trigger a new single transmit, or 'Mute' to stop the transmission of the frame.
""",
'de':
"""
"""
}]
})
