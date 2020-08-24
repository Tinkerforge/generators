# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# One Wire Bricklet communication config

from generators.configs.openhab_commonconfig import *

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
    'released': True,
    'documented': True,
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
'name': 'Status',
'type': 'uint8',
'constants': [('OK', 0),
              ('Busy', 1),
              ('No Presence', 2),
              ('Timeout', 3),
              ('Error', 4)]
})

com['constant_groups'].append({
'name': 'Communication LED Config',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Show Heartbeat', 2),
              ('Show Communication', 3)]
})

com['packets'].append({
'type': 'function',
'name': 'Search Bus Low Level',
'elements': [('Identifier Length', 'uint16', 1, 'out', {'range': (0, 64)}),
             ('Identifier Chunk Offset', 'uint16', 1, 'out', {}),
             ('Identifier Chunk Data', 'uint64', 7, 'out', {}),
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Status'})],
'high_level': {'stream_out': {'name': 'Identifier'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns a list of up to 64 identifiers of the connected 1-Wire devices.
Each identifier is 64-bit and consists of 8-bit family code, 48-bit ID and
8-bit CRC.

To get these identifiers the Bricklet runs the
`SEARCH ROM algorithm <https://www.maximintegrated.com/en/app-notes/index.mvp/id/187>`__,
as defined by Maxim.
""",
'de':
"""
Gibt eine Liste mit bis zu 64 Identifiern von angeschlossenen 1-Wire Geräten
zurück. Jeder Identifier ist 64-Bit und besteht aus 8-Bit Familien-Code,
48-Bit ID und 8-Bit CRC.

Um diese Liste zu erhalten führt das Bricklet den
`SEARCH ROM Algorithmus <https://www.maximintegrated.com/en/app-notes/index.mvp/id/187>`__
von Maxim aus.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Reset Bus',
'elements': [('Status', 'uint8', 1, 'out', {'constant_group': 'Status'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Resets the bus with the 1-Wire reset operation.
""",
'de':
"""
Setzt den Bus mit einer 1-Wire Reset Operation zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Write',
'elements': [('Data', 'uint8', 1, 'in', {}),
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Status'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes a byte of data to the 1-Wire bus.
""",
'de':
"""
Schreibt ein Byte an Daten auf den 1-Wire Bus.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Read',
'elements': [('Data', 'uint8', 1, 'out', {}),
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Status'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Reads a byte of data from the 1-Wire bus.
""",
'de':
"""
Liest ein Byte an Daten vom 1-Wire Bus.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Write Command',
'elements': [('Identifier', 'uint64', 1, 'in', {}),
             ('Command', 'uint8', 1, 'in', {}),
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Status'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes a command to the 1-Wire device with the given identifier. You can obtain
the identifier by calling :func:`Search Bus`. The MATCH ROM operation is used to
write the command.

If you only have one device connected or want to broadcast to all devices
you can set the identifier to 0. In this case the SKIP ROM operation is used to
write the command.
""",
'de':
"""
Sendet einen Befehl an das 1-Wire Gerät mit der angegebenen Identifier. Die
Liste der Identifier können mittels :func:`Search Bus` ermittelt werden. Die
MATCH ROM Operation wird verwendet, um den Befehl zu übertragen.

Wenn nur ein Gerät angeschlossen ist, oder der Befehl an alle Geräte gesendet
werden soll kann als Identifier 0 verwendet werden. Dann wird die SKIP ROM
Operation verwendet, um den Befehl zu übertragen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Communication LED Config',
'elements': [('Config', 'uint8', 1, 'in', {'constant_group': 'Communication LED Config', 'default': 3})],
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

Wenn das Bricklet sich im Bootloadermodus befindet ist die LED aus.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Communication LED Config',
'elements': [('Config', 'uint8', 1, 'out', {'constant_group': 'Communication LED Config', 'default': 3})],
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
    ow.write(0x7F) # CONFIGURATION: 12-bit mode

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
              ('setter', 'Write', [('uint8', 0x7F)], None, 'CONFIGURATION: 12-bit mode'),
              ('loop_header', 10, 'Read temperature 10 times'),
              ('setter', 'Write Command', [('uint64', 0), ('uint8', 0x44)], None, 'CONVERT T (start temperature conversion)'),
              ('sleep', 1000, None, 'Wait for conversion to finish'),
              ('setter', 'Write Command', [('uint64', 0), ('uint8', 0xBE)], None, 'READ SCRATCHPAD'),
              # TODO: Add getter for temperature values (see above)
              ('loop_footer',)],
'incomplete': True # because of special print logic
})

com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'params': [{
        'packet': 'Set Communication LED Config',
        'element': 'Config',

        'name': 'Communication LED Config',
        'type': 'integer',
        'label': 'Communication LED Config',
        'description': "The communication LED configuration. By default the LED shows 1-wire communication traffic by flickering. You can also turn the LED permanently on/off or show a heartbeat.",
    }],
    'init_code': """this.setCommunicationLEDConfig(cfg.communicationLEDConfig);""",
    'channels': [],
    'channel_types': [],
    'actions': ['Search Bus', 'Reset Bus', 'Write', 'Read', 'Write Command', 'Get Communication LED Config']
}
