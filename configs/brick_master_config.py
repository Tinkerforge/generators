# -*- coding: utf-8 -*-

# Servo Brick communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'version': [1, 1, 0],
    'type': 'Brick',
    'name': ('Master', 'master'),
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

 "1", "Chibi"
 "2", "RS485"

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
Sets up to 256 slave addresses. The address numeration has to be used 
ascending from 0. For example: If you use the Chibi Extension in Master mode
(i.e. the stack has an USB connection) and you want to talk to three other
Chibi stacks with the IDs 17, 23, and 42, you should call with "(0, 17),
(1, 23) and (2, 42)".

It is possible to set the addresses with the Brick Viewer and it will be 
saved in the EEPROM of the Chibi Extension, they don't
have to be set on every startup.
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

 "0", "OQPSK 868Mhz (Europe)"
 "1", "OQPSK 915Mhz (US)"
 "2", "OQPSK 780Mhz (China)"
 "3", "BPSK40 915Mhz"

It is possible to set the frequency with the Brick Viewer and it will be 
saved in the EEPROM of the Chibi Extension, it does not
have to be set on every startup.
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
 :header: "Frequency", "Possible Channels"
 :widths: 40, 60

 "OQPSK 868Mhz (Europe)", "0"
 "OQPSK 915Mhz (US)", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"
 "OQPSK 780Mhz (China)", "0, 1, 2, 3"
 "BPSK40 915Mhz", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"

It is possible to set the frequency with the Brick Viewer and it will be 
saved in the EEPROM of the Chibi Extension, it does not
have to be set on every startup.
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
""",
'de':
"""
"""
}]
})
