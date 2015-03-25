# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# RS232 Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 254,
    'name': ('RS232', 'rs232', 'RS232'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for RS232 communication',
    'released': False,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('Write', 'write'),
'elements': [('message', 'char', 60, 'in'),
             ('length', 'uint8', 1, 'in')],
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
'name': ('Read', 'read'),
'elements': [('message', 'char', 60, 'out'),
             ('length', 'uint8', 1, 'out')],
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
'name': ('EnableCallback', 'enable_callback'),
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
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
'name': ('DisableCallback', 'disable_callback'),
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
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
'name': ('IsCallbackEnabled', 'is_callback_enabled'),
'elements': [('enable', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
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
'name': ('SetConfiguration', 'set_configuration'),
'elements': [('baudrate', 'uint8', 1, 'in', ('Baudrate', 'baudrate', [('300', '300', 0),
                                                                      ('600', '600', 1),
                                                                      ('1200', '1200', 2),
                                                                      ('2400', '2400', 3),
                                                                      ('4800', '4800', 4),
                                                                      ('9600', '9600', 5),
                                                                      ('14400', '14400', 6),
                                                                      ('28800', '28800', 7),
                                                                      ('38400', '38400', 8),
                                                                      ('57600', '57600', 9),
                                                                      ('115200', '115200', 10),
                                                                      ('230400', '230400', 11)])),
             ('parity', 'uint8', 1, 'in', ('Parity', 'parity', [('None', 'none', 0),
                                                                ('Odd', 'odd', 1),
                                                                ('Even', 'even', 2),
                                                                ('ForcedParity1', 'forced_parity_1', 3),
                                                                ('ForcedParity0', 'forced_parity_0', 4)])),
             ('stopbits', 'uint8', 1, 'in', ('Stopbits', 'stopbits', [('1', '1', 1),
                                                                      ('2', '2', 2)])),
             ('wordlength', 'uint8', 1, 'in', ('Wordlength', 'wordlength', [('5', '5', 5),
                                                                            ('6', '6', 6),
                                                                            ('7', '7', 7),
                                                                            ('8', '8', 8)])),
             ('hardware_flowcontrol', 'uint8', 1, 'in', ('HardwareFlowcontrol', 'hardware_flowcontrol', [('Off', 'off', 0),
                                                                                                         ('On', 'on', 1)])),
             ('software_flowcontrol', 'uint8', 1, 'in', ('SoftwareFlowcontrol', 'software_flowcontrol', [('Off', 'off', 0),
                                                                                                         ('On', 'on', 1)]))],

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
'name': ('GetConfiguration', 'get_configuration'),
'elements': [('baudrate', 'uint8', 1, 'out', ('Baudrate', 'baudrate', [('300', '300', 0),
                                                                       ('600', '600', 1),
                                                                       ('1200', '1200', 2),
                                                                       ('2400', '2400', 3),
                                                                       ('4800', '4800', 4),
                                                                       ('9600', '9600', 5),
                                                                       ('14400', '14400', 6),
                                                                       ('28800', '28800', 7),
                                                                       ('38400', '38400', 8),
                                                                       ('57600', '57600', 9),
                                                                       ('115200', '115200', 10),
                                                                       ('230400', '230400', 11)])),
             ('parity', 'uint8', 1, 'out', ('Parity', 'parity', [('None', 'none', 0),
                                                                 ('Odd', 'odd', 1),
                                                                 ('Even', 'even', 2),
                                                                 ('ForcedParity1', 'forced_parity_1', 3),
                                                                 ('ForcedParity0', 'forced_parity_0', 4)])),
             ('stopbits', 'uint8', 1, 'out', ('Stopbits', 'stopbits', [('1', '1', 1),
                                                                       ('2', '2', 2)])),
             ('wordlength', 'uint8', 1, 'out', ('Wordlength', 'wordlength', [('5', '5', 5),
                                                                             ('6', '6', 6),
                                                                             ('7', '7', 7),
                                                                             ('8', '8', 8)])),
             ('hardware_flowcontrol', 'uint8', 1, 'out', ('HardwareFlowcontrol', 'hardware_flowcontrol', [('Off', 'off', 0),
                                                                                                          ('On', 'on', 1)])),
             ('software_flowcontrol', 'uint8', 1, 'out', ('SoftwareFlowcontrol', 'software_flowcontrol', [('Off', 'off', 0),
                                                                                                          ('On', 'on', 1)]))],
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
'name': ('ReadCallback', 'read_callback'),
'elements': [('message', 'char', 60, 'out'),
             ('length', 'uint8', 1, 'out')],
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
