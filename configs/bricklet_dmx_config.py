# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# GPS Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 285,
    'name': 'DMX',
    'display_name': 'DMX',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'DMX Master and Slave',
        'de': 'DMX Master und Slave'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Set DMX Mode',
'elements': [('DMX Mode', 'uint8', 1, 'in', ('DMX Mode', [('Master', 0),
                                                          ('Slave', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Calling this sets frame number to 0
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get DMX Mode',
'elements': [('DMX Mode', 'uint8', 1, 'out', ('DMX Mode', [('Master', 0),
                                                           ('Slave', 1)]))],
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
'name': 'Write Frame Low Level',
'elements': [('Frame Length', 'uint16', 1, 'in'),
             ('Frame Chunk Offset', 'uint16', 1, 'in'),
             ('Frame Chunk Data', 'uint8', 60, 'in')],
'high_level': {'stream_in': {'name': 'Frame'}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Read Frame Low Level',
'elements': [('Frame Length', 'uint16', 1, 'out'),
             ('Frame Chunk Offset', 'uint16', 1, 'out'),
             ('Frame Chunk Data', 'uint8', 56, 'out'),
             ('Frame Number', 'uint32', 1, 'out')],
'high_level': {'stream_out': {'name': 'Frame'}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Set Frame Duration',
'elements': [('Frame Duration', 'uint16', 1, 'in')],
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
'name': 'Get Frame Duration',
'elements': [('Frame Duration', 'uint16', 1, 'out')],
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
'name': 'Draw Frame',
'elements': [],
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
'name': 'Get Frame Error Count',
'elements': [('Overrun Error Count', 'uint32', 1, 'out'),
             ('Framing Error Count', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the current number of overrun and framing errors.
""",
'de':
"""
Gibt die aktuelle Anzahl an Overrun und Framing Fehlern zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Communication LED Config',
'elements': [('Config', 'uint8', 1, 'in', ('Communication LED Config', [('Off', 0),
                                                                        ('On', 1),
                                                                        ('Show Heartbeat', 2),
                                                                        ('Show Communication', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the communication LED configuration. By default the LED shows
communication traffic, it flickers once for every 10 received data packets.

You can also turn the LED permanently on/off or show a heartbeat.

If the Bricklet is in bootloader mode, the LED is off.
""",
'de':
"""
Setzt die Konfiguration der Kommunikations-LED. Standardmäßig zeigt
die LED die Kommunikationsdatenmenge an. Sie blinkt einmal auf pro 10 empfangenen
Datenpaketen zwischen Brick und Bricklet.

Die LED kann auch permanaent an/aus gestellt werden oder einen Herzschlag anzeigen.

Wenn das Bricklet sich im Bootlodermodus befindet ist die LED aus.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Communication LED Config',
'elements': [('Config', 'uint8', 1, 'out', ('Communication LED Config', [('Off', 0),
                                                                         ('On', 1),
                                                                         ('Show Heartbeat', 2),
                                                                         ('Show Communication', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Communication LED Config`
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Communication LED Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Error LED Config',
'elements': [('Config', 'uint8', 1, 'in', ('Error LED Config', [('Off', 0),
                                                                ('On', 1),
                                                                ('Show Heartbeat', 2),
                                                                ('Show Error', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the error LED configuration.

By default the error LED turns on if there is any error (see :cb:`Get Error Count`
callback). If you call this function with the SHOW ERROR option again, the LED
will turn off until the next error occurs.

You can also turn the LED permanently on/off or show a heartbeat.

If the Bricklet is in bootloader mode, the LED is off.
""",
'de':
"""
Setzt die Konfiguration der Error-LED.

Standardmäßig geht die LED an, wenn ein Error auftritt (siehe :cb:`Get Error Count`
Callback). Wenn diese Funktion danach nochmal mit der "SHOW ERROR"-Option
aufgerufen wird, geht die LED wieder aus bis der nächste Error auftritt.

Die LED kann auch permanaent an/aus gestellt werden oder einen Herzschlag
anzeigen.

Wenn das Bricklet sich im Bootlodermodus befindet ist die LED aus.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Error LED Config',
'elements': [('Config', 'uint8', 1, 'out', ('Error LED Config', [('Off', 0),
                                                                 ('On', 1),
                                                                 ('Show Heartbeat', 2),
                                                                 ('Show Error', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Error LED Config`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Error LED Config` gesetzt.
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set Frame Callback Config',
'elements': [('Frame Started Callback Enabled', 'bool', 1, 'in'),
             ('Frame Available Callback Enabled', 'bool', 1, 'in'),
             ('Frame Callback Enabled', 'bool', 1, 'in'),
             ('Frame Error Count Callback Enabled', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
default: true,true,false
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Frame Callback Config',
'elements': [('Frame Started Callback Enabled', 'bool', 1, 'out'),
             ('Frame Available Callback Enabled', 'bool', 1, 'out'),
             ('Frame Callback Enabled', 'bool', 1, 'out'),
             ('Frame Error Count Callback Enabled', 'bool', 1, 'out')],
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
'name': 'Frame Started',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
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
'name': 'Frame Available',
'elements': [('Frame Number', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
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
'name': 'Frame Low Level',
'elements': [('Frame Length', 'uint16', 1, 'out'),
             ('Frame Chunk Offset', 'uint16', 1, 'out'),
             ('Frame Chunk Data', 'uint8', 56, 'out'),
             ('Frame Number', 'uint32', 1, 'out')],
'high_level': {'stream_out': {'name': 'Frame'}},
'since_firmware': [1, 0, 0],
'doc': ['llc', {
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
'name': 'Frame Error Count',
'elements': [('Overrun Error Count', 'uint32', 1, 'out'),
             ('Framing Error Count', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called if a new error occurs. It returns
the current overrun and framing error count.
""",
'de':
"""
Dieser Callback wird aufgerufen wenn ein neuer Fehler auftritt.
Er gibt die Anzahl der aufgetreten Overrun and Framing Fehler zurück.
"""
}]
})
