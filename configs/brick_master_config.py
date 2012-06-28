# -*- coding: utf-8 -*-

# Master Brick communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'version': [1, 2, 0],
    'category': 'Brick',
    'name': ('Master', 'master', 'Master'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for controlling Stacks and four Bricklets',
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetStackVoltage', 'get_stack_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')], 
'doc': ['bm', {
'en':
"""
Returns the stack voltage in mV. The stack voltage is the
voltage that is supplied via the stack, i.e. it is given by a 
Step-Down or Step-Up Power Supply.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetStackCurrent', 'get_stack_current'), 
'elements': [('current', 'uint16', 1, 'out')], 
'doc': ['bm', {
'en':
"""
Returns the stack current in mA. The stack current is the
current that is drawn via the stack, i.e. it is given by a
Step-Down or Step-Up Power Supply.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetExtensionType', 'set_extension_type'), 
'elements': [('extension', 'uint8', 1, 'in'),
             ('exttype', 'uint32', 1, 'in')], 
'doc': ['am', {
'en':
"""
Writes the extension type to the EEPROM of a specified extension. 
The extension is either 0 or 1 (0 is the on the bottom, 1 is the on on top, 
if only one extension is present use 0).

Possible extension types:

.. csv-table::
 :header: "Type", "Description"
 :widths: 10, 100

 "1",    "Chibi"
 "2",    "RS485"

The extension type is already set when bought and it can be set with the 
Brick Viewer, it is unlikely that you need this function.

The value will be saved in the EEPROM of the Chibi Extension, it does not
have to be set on every startup.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetExtensionType', 'get_extension_type'), 
'elements': [('extension', 'uint8', 1, 'in'),
             ('exttype', 'uint32', 1, 'out')], 
'doc': ['am', {
'en':
"""
Returns the extension type for a given extension as set by 
:func:`SetExtensionType`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('IsChibiPresent', 'is_chibi_present'), 
'elements': [('present', 'bool', 1, 'out')], 
'doc': ['am', {
'en':
"""
Returns true if a Chibi Extension is available to be used by the Master.

.. versionadded:: 1.1.0
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetChibiAddress', 'set_chibi_address'), 
'elements': [('address', 'uint8', 1, 'in')], 
'doc': ['am', {
'en':
"""
Sets the address (1-255) belonging to the Chibi Extension.

It is possible to set the address with the Brick Viewer and it will be 
saved in the EEPROM of the Chibi Extension, it does not
have to be set on every startup.

.. versionadded:: 1.1.0
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetChibiAddress', 'get_chibi_address'), 
'elements': [('address', 'uint8', 1, 'out')], 
'doc': ['am', {
'en':
"""
Returns the address as set by :func:`SetChibiAddress`.

.. versionadded:: 1.1.0
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetChibiMasterAddress', 'set_chibi_master_address'), 
'elements': [('address', 'uint8', 1, 'in')], 
'doc': ['am', {
'en':
"""
Sets the address (1-255) of the Chibi Master. This address is used if the
Chibi Extension is used as slave (i.e. it does not have a USB connection).

It is possible to set the address with the Brick Viewer and it will be 
saved in the EEPROM of the Chibi Extension, it does not
have to be set on every startup.

.. versionadded:: 1.1.0
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetChibiMasterAddress', 'get_chibi_master_address'), 
'elements': [('address', 'uint8', 1, 'out')], 
'doc': ['am', {
'en':
"""
Returns the address as set by :func:`SetChibiMasterAddress`.

.. versionadded:: 1.1.0
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetChibiSlaveAddress', 'set_chibi_slave_address'), 
'elements': [('num', 'uint8', 1, 'in'),
             ('address', 'uint8', 1, 'in')], 
'doc': ['am', {
'en':
"""
Sets up to 255 slave addresses. The address numeration has to be used
ascending from 0. For example: If you use the Chibi Extension in Master mode
(i.e. the stack has an USB connection) and you want to talk to three other
Chibi stacks with the IDs 17, 23, and 42, you should call with "(0, 17),
(1, 23) and (2, 42)".

It is possible to set the addresses with the Brick Viewer and it will be 
saved in the EEPROM of the Chibi Extension, they don't
have to be set on every startup.

.. versionadded:: 1.1.0
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetChibiSlaveAddress', 'get_chibi_slave_address'), 
'elements': [('num', 'uint8', 1, 'in'),
             ('address', 'uint8', 1, 'out')], 
'doc': ['am', {
'en':
"""
Returns the slave address for a given num as set by 
:func:`SetChibiSlaveAddress`.

.. versionadded:: 1.1.0
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetChibiSignalStrength', 'get_chibi_signal_strength'), 
'elements': [('signal_strength', 'uint8', 1, 'out')], 
'doc': ['am', {
'en':
"""
Returns the signal strength in dBm. The signal strength updates every time a
packet is received.

.. versionadded:: 1.1.0
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetChibiErrorLog', 'get_chibi_error_log'), 
'elements': [('underrun', 'uint16', 1, 'out'),
             ('crc_error', 'uint16', 1, 'out'),
             ('no_ack', 'uint16', 1, 'out'),
             ('overflow', 'uint16', 1, 'out')], 
'doc': ['am', {
'en':
"""
Returns underrun, CRC error, no ACK and overflow error counts of the Chibi
communication. If these errors start rising, it is likely that either the
distance between two Chibi stacks is becoming too big or there are
interferences.

.. versionadded:: 1.1.0
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetChibiFrequency', 'set_chibi_frequency'), 
'elements': [('frequency', 'uint8', 1, 'in')], 
'doc': ['am', {
'en':
"""
Sets the Chibi frequency range for the Chibi Extension. Possible values are:

.. csv-table::
 :header: "Type", "Description"
 :widths: 10, 100

 "0",    "OQPSK 868Mhz (Europe)"
 "1",    "OQPSK 915Mhz (US)"
 "2",    "OQPSK 780Mhz (China)"
 "3",    "BPSK40 915Mhz"

It is possible to set the frequency with the Brick Viewer and it will be 
saved in the EEPROM of the Chibi Extension, it does not
have to be set on every startup.

.. versionadded:: 1.1.0
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetChibiFrequency', 'get_chibi_frequency'), 
'elements': [('frequency', 'uint8', 1, 'out')], 
'doc': ['am', {
'en':
"""
Returns the frequency value as set by :func:`SetChibiFrequency`.

.. versionadded:: 1.1.0
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetChibiChannel', 'set_chibi_channel'), 
'elements': [('channel', 'uint8', 1, 'in')], 
'doc': ['am', {
'en':
"""
Sets the channel used by the Chibi Extension. Possible channels are
different for different frequencies:

.. csv-table::
 :header: "Frequency",             "Possible Channels"
 :widths: 40, 60

 "OQPSK 868Mhz (Europe)", "0"
 "OQPSK 915Mhz (US)",     "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"
 "OQPSK 780Mhz (China)",  "0, 1, 2, 3"
 "BPSK40 915Mhz",         "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"

It is possible to set the frequency with the Brick Viewer and it will be 
saved in the EEPROM of the Chibi Extension, it does not
have to be set on every startup.

.. versionadded:: 1.1.0
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetChibiChannel', 'get_chibi_channel'), 
'elements': [('channel', 'uint8', 1, 'out')], 
'doc': ['am', {
'en':
"""
Returns the channel as set by :func:`SetChibiChannel`.

.. versionadded:: 1.1.0
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('IsRS485Present', 'is_rs485_present'), 
'elements': [('present', 'bool', 1, 'out')], 
'doc': ['am', {
'en':
"""
Returns true if a RS485 Extension is available to be used by the Master.

.. versionadded:: 1.2.0
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('SetRS485Address', 'set_rs485_address'), 
'elements': [('address', 'uint8', 1, 'in')], 
'doc': ['am', {
'en':
"""
Sets the address (1-255) belonging to the RS485 Extension.

Set to 0 if the RS485 Extension should be the RS485 Master (i.e.
connected to a PC via USB).

It is possible to set the address with the Brick Viewer and it will be 
saved in the EEPROM of the RS485 Extension, it does not
have to be set on every startup.

.. versionadded:: 1.2.0
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('GetRS485Address', 'get_rs485_address'), 
'elements': [('address', 'uint8', 1, 'out')], 
'doc': ['am', {
'en':
"""
Returns the address as set by :func:`SetRS485Address`.

.. versionadded:: 1.2.0
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('SetRS485SlaveAddress', 'set_rs485_slave_address'),
'elements': [('num', 'uint8', 1, 'in'),
             ('address', 'uint8', 1, 'in')], 
'doc': ['am', {
'en':
"""
Sets up to 255 slave addresses. The address numeration has to be used
ascending from 0. For example: If you use the RS485 Extension in Master mode
(i.e. the stack has an USB connection) and you want to talk to three other
RS485 stacks with the IDs 17, 23, and 42, you should call with "(0, 17),
(1, 23) and (2, 42)".

It is possible to set the addresses with the Brick Viewer and it will be 
saved in the EEPROM of the RS485 Extension, they don't
have to be set on every startup.

.. versionadded:: 1.2.0
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('GetRS485SlaveAddress', 'get_rs485_slave_address'), 
'elements': [('num', 'uint8', 1, 'in'),
             ('address', 'uint8', 1, 'out')], 
'doc': ['am', {
'en':
"""
Returns the slave address for a given num as set by 
:func:`SetRS485SlaveAddress`.

.. versionadded:: 1.2.0
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('GetRS485ErrorLog', 'get_rs485_error_log'), 
'elements': [('crc_error', 'uint16', 1, 'out')], 
'doc': ['am', {
'en':
"""
Returns CRC error counts of the RS485 communication.
If this counter starts rising, it is likely that the distance
between the RS485 nodes is too big or there is some kind of
interference.

.. versionadded:: 1.2.0
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('SetRS485Configuration', 'set_rs485_configuration'), 
'elements': [('speed', 'uint32', 1, 'in'),
             ('parity', 'char', 1, 'in'),
             ('stopbits', 'uint8', 1, 'in')], 
'doc': ['am', {
'en':
"""
Sets the configuration of the RS485 extension. Speed is given in baud. The
Master Brick will try to match the given baud rate as exactly as possible.
The maximum recommended baud rate is 2000000 (2Mbit).
Possible values for parity are 'n' (none), 'e' (even) and 'o' (odd).
Possible values for stopbits are 1 and 2.

If your RS485 is unstable (lost messages etc), the first thing you should
try is to decrease the speed. On very large bus (e.g. 1km), you probably
should use a value in the range of 100khz.

The values are stored in the EEPROM and only applied on startup. That means
you have to restart the Master Brick after configuration.

.. versionadded:: 1.2.0
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('GetRS485Configuration', 'get_rs485_configuration'), 
'elements': [('speed', 'uint32', 1, 'out'),
             ('parity', 'char', 1, 'out'),
             ('stopbits', 'uint8', 1, 'out')], 
'doc': ['am', {
'en':
"""
Returns the configuration as set by :func:`SetRS485Configuration`.

.. versionadded:: 1.2.0
""",
'de':
"""
"""
}]
})
