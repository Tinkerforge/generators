# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# One Wire Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2123,
    'name': 'One Wire',
    'display_name': 'One Wire',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Communicates with up 64 1-Wire devices',
        'de': 'Kommuniziert mit bis zu 64 1-Wire Geräten'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'discontinued': False,
    'packets': [],
    'examples': []
}

ONE_WIRE_STATUS = ('Status', [('OK', 0),
                              ('Busy', 1),
                              ('No Presence', 2),
                              ('Timeout', 3),
                              ('Error', 4)])

com['packets'].append({
'type': 'function',
'name': 'Search Bus Low Level',
'elements': [('Identifier Length', 'uint16', 1, 'out'),
             ('Identifier Chunk Offset', 'uint16', 1, 'out'),
             ('Identifier Chunk Data', 'uint64', 7, 'out'),
             ('Status', 'uint8', 1, 'out', ONE_WIRE_STATUS)],
'high_level': {'stream_out': {'name': 'Identifier'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns a list of up to 64 Identifiers of the connected 1-Wire devices. 
Each identifier has 64 bits and consists of 8 bit family code, 48 bit ID and
8 bit CRC.

To get these Identifiers the Bricklet runs the SEARCH ROM algorithm, as 
`defined by maxim <https://www.maximintegrated.com/en/app-notes/index.mvp/id/187>`__.
""",
'de':
"""

"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Reset Bus',
'elements': [('Status', 'uint8', 1, 'out', ONE_WIRE_STATUS)],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Resets the bus with the 1-Wire reset operation.
""",
'de':
"""

"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Write',
'elements': [('Data', 'uint8', 1, 'in'),
             ('Status', 'uint8', 1, 'out', ONE_WIRE_STATUS)],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes a byte of data to the 1-Wire bus.
""",
'de':
"""

"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Read',
'elements': [('Data', 'uint8', 1, 'out'),
             ('Status', 'uint8', 1, 'out', ONE_WIRE_STATUS)],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Reads a byte of data from the 1-Wire bus.
""",
'de':
"""

"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Write Command',
'elements': [('Identifier', 'uint64', 1, 'in'),
             ('Command', 'uint8', 1, 'in'),
             ('Status', 'uint8', 1, 'out', ONE_WIRE_STATUS)],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes a command to the 1-Wire device with the given identifier. You can obain
the identifier by calling :func:`Search Bus`. The MATCH ROM operation is used to
write the command

If you only have one device connected you can set the identifier to 0. In this case
the SKIP ROM command is used to write the command.
""",
'de':
"""

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
Sets the communication LED configuration. By default the LED shows 1-wire
communication traffic by flickering.

You can also turn the LED permanently on/off or show a heartbeat.

If the Bricklet is in bootloader mode, the LED is off.
""",
'de':
"""
Setzt die Konfiguration der Kommunikations-LED. Standardmäßig zeigt
die LED die 1-Wire Kommunikation durch Aufblinken an.

Die LED kann auch permanent an/aus gestellt werden oder einen Herzschlag anzeigen.

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

"""
    ow.write_command(0, 0x4E) # WRITE SCRATCHPAD
    ow.write(0x00) # ALARM H (unused)
    ow.write(0x00) # ALARM L (unused)
    ow.write(0x7F) # COFIGURATION: 12 bit mode

    while True:
        ow.write_command(0, 0x44) # CONVERT T (start temperature conversion)
        time.sleep(1) # Wait for conversion to finish

        ow.write_command(0, 0xBE) # READ SCRATCHPAD

        t_low = ow.read().data
        t_high = ow.read().data
        print('Temperature: {0} °C'.format((t_low | (t_high << 8))/16.0))
"""
com['examples'].append({
'name': 'Read DS18B20 Temperature',
'functions': [('setter', 'Write Command', [('uint64', 0), ('uint8', 0x4E)], None, 'WRITE SCRATCHPAD'),
              ('setter', 'Write', [('uint8', 0x00)], None, 'ALARM H (unused)'),
              ('setter', 'Write', [('uint8', 0x00)], None, 'ALARM L (unused)'),
              ('setter', 'Write', [('uint8', 0x7F)], None, 'CONFIGURATION: 12 bit mode'),
              ('loop_header', 10, 'Read temperature 10 times'),
              ('setter', 'Write Command', [('uint64', 0), ('uint8', 0x44)], None, 'CONVERT T (start temperature conversion)'),
              ('sleep', 1000, None, 'Wait for conversion to finish'),
              ('setter', 'Write Command', [('uint64', 0), ('uint8', 0xBE)], None, 'READ SCRATCHPAD'),
              # TODO: Add getter for temperature values (see above)
              ('loop_footer',)],
'incomplete': True # because of special print logic
})
