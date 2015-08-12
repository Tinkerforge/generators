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
    'name': ('RS232', 'rs232', 'RS232', 'RS232 Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Communicates with RS232 devices',
        'de': 'Kommuniziert mit RS232 Geräten'
    },
    'released': True,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': ('Write', 'write'),
'elements': [('message', 'char', 60, 'in'),
             ('length', 'uint8', 1, 'in'),
             ('written', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes a string of up to 60 characters to the RS232 interface. The string
can be binary data, ASCII or similar is not necessary.

The length of the string has to be given as an additional parameter.

The return value is the number of bytes that could be written.

See :func:`SetConfigurations` for configuration possibilities
regarding baudrate, parity and so on.
""",
'de':
"""
Schreibt einen String aus bis zu 60 Zeichen auf die RS232-Schnittstelle. Der
String kann aus Binärdaten bestehen, ASCII o.ä. ist nicht notwendig.

Die Länge des Strings muss als ein zusätzlicher Parameter angegeben werden.

Der Rückgabewert ist die Anzahl der Zeichen die geschrieben werden konnten.

Siehe :func:`SetConfiguration` für Konfigurationsmöglichkeiten
bezüglich Baudrate, Parität usw.
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
Returns the currently buffered message. The maximum length
of message is 60. If the length is given as 0, there was no
new data available.

Instead of polling with this function, you can also use
callbacks. See :func:`EnableReadCallback` and :func:`ReadCallback`.
""",
'de':
"""
Gibt die aktuell gespeicherte Nachricht zurück. Die maximale Länge
beträgt 60. Wenn die Länge als 0 gegeben wird, waren keine
neuen Daten verfügbar.

Anstatt zu mit dieser Funktion zu pollen, ist es auch möglich
Callbacks zu nutzen. Siehe :func:`EnableReadCallback` und
:func:`DisableReadCallback`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('EnableReadCallback', 'enable_read_callback'),
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Enables the :func:`ReadCallback`.

By default the callback is disabled.
""",
'de':
"""
Aktiviert den :func:`ReadCallback`.

Im Startzustand ist der Callback deaktiviert
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('DisableReadCallback', 'disable_read_callback'),
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Disables the :func:`ReadCallback`.

By default the callback is disabled.
""",
'de':
"""
Deaktiviert den :func:`ReadCallback`.

Im Startzustand ist der Callback deaktiviert
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('IsReadCallbackEnabled', 'is_read_callback_enabled'),
'elements': [('enabled', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns *true* if the :func:`ReadCallback` is enabled,
*false* otherwise.
""",
'de':
"""
Gibt *true* zurück falls :func:`ReadCallback` aktiviert ist, 
*false* sonst.
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
                                                                      ('19200', '19200', 7),
                                                                      ('28800', '28800', 8),
                                                                      ('38400', '38400', 9),
                                                                      ('57600', '57600', 10),
                                                                      ('115200', '115200', 11),
                                                                      ('230400', '230400', 12)])),
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
Sets the configuration for the RS232 communication. Available options:

* Baudrate between 300 and 230400 baud.
* Parity of none, odd, even or forced parity.
* Stopbits can be 1 or 2.
* Word length of 5 to 8.
* Hard-/Software flow control can each be on or off.

The default is: 115200 baud, parity none, 1 stop bit, word length 8, hard-/software flow control off.

.. note::
 The currently released Bindings have a off-by-one in the baudrate constants.
 Please use the actual number and not the constant. The bug will be fixed
 with the next Binding release.
""",
'de':
"""
Setzt die Konfiguration für die RS232-Kommunikation.
Verfügbare Optionen sind:

* Baudrate zwischen 300 und 230400 Baud.
* Parität von None, Odd, Even und Forced Parity.
* Stop Bits von 1 oder 2.
* Wortlänge zwischen 5 und 8.
* Hard-/Software Flow Control kann je an oder aus sein.

Der Standard ist: 115200 Baud, Parität None, 1 Stop Bits, Wortlänge 8, Hard-/Software Flow Control aus.

.. note::
 Die aktuell veröffentlichen Bindings haben einen "off-by-one" in den
 Baudraten-Kostanten. Aktuell kann nur die eigentliche Zahl genutzt werden
 und nicht die vordefinierte Konstante. Dieser Bug wird mit dem nächsten
 Binding-Release gefixt.
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
                                                                       ('19200', '19200', 7),
                                                                       ('28800', '28800', 8),
                                                                       ('38400', '38400', 9),
                                                                       ('57600', '57600', 10),
                                                                       ('115200', '115200', 11),
                                                                       ('230400', '230400', 12)])),
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
Returns the configuration as set by :func:`SetConfiguration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`SetConfiguration` gesetzt.
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
This callback is called if new data is available. The message has
a maximum size of 60 characters. The actual length of the message
is given in addition.

To enable this callback, use :func:`EnableReadCallback`.
""",
'de':
"""
Dieser Callback wird aufgerufen wenn neue Daten zur Verfügung stehen.
Die Nachricht hat eine Maximalgröße von 60 Zeichen. Die Länge
der Nachricht wird zusätzlich übergeben.

Dieser Callback kann durch :func:`EnableReadCallback` aktiviert werden.
"""
}]
})

com['examples'].append({
'type': 'skeleton',
'name': 'Loopback'
})
