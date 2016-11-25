# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# GPS Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 277,
    'name': ('RS485', 'RS485', 'RS485 Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Communicates with RS485 devices with full- or half-duplex',
        'de': 'Kommuniziert mit RS485 Geräten mit voll- oder halb-duplex'
    },
    'has_comcu': True,
    'released': False,
    'documented': False,
    'packets': [],
    'examples': []
}


com['packets'].append({
'type': 'function',
'name': 'Write',
'elements': [('Message', 'char', 60, 'in'),
             ('Length', 'uint8', 1, 'in'),
             ('Written', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes a string of up to 60 characters to the RS232 interface. The string
can be binary data, ASCII or similar is not necessary.

The length of the string has to be given as an additional parameter.

The return value is the number of bytes that could be written.

See :func:`SetConfiguration` for configuration possibilities
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
'name': 'Read',
'elements': [('Message', 'char', 60, 'out'),
             ('Length', 'uint8', 1, 'out')],
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

Anstatt mit dieser Funktion zu pollen, ist es auch möglich
Callbacks zu nutzen. Siehe :func:`EnableReadCallback` und
:func:`ReadCallback`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Enable Read Callback',
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
'name': 'Disable Read Callback',
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
'name': 'Is Read Callback Enabled',
'elements': [('Enabled', 'bool', 1, 'out')],
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
'name': 'Set Configuration',
'elements': [('Baudrate', 'uint32', 1, 'in'),
             ('Parity', 'uint8', 1, 'in', ('Parity', [('None', 0),
                                                      ('Odd', 1),
                                                      ('Even', 2)])),
             ('Stopbits', 'uint8', 1, 'in', ('Stopbits', [('1', 1),
                                                          ('2', 2)])),
             ('Wordlength', 'uint8', 1, 'in', ('Wordlength', [('5', 5),
                                                              ('6', 6),
                                                              ('7', 7),
                                                              ('8', 8)])),
             ('Duplex', 'uint8', 1, 'in', ('Duplex', [('Half', 0),
                                                      ('Full', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the configuration for the RS232 communication. Available options:

TODO: Baudrate 100 to 48000000*1023/(1024*16.0) = 2997070

* Baudrate between XXX and YYY baud.
* Parity of none, odd or even.
* Stopbits can be 1 or 2.
* Word length of 5 to 8.
* Duplex TODO

The default is: 115200 baud, parity none, 1 stop bit, word length 8, half duplex.
""",
'de':
"""
Setzt die Konfiguration für die RS232-Kommunikation.
Verfügbare Optionen sind:

* Baudrate zwischen XXX und YYY Baud.
* Parität von None, Odd und Even Parity.
* Stop Bits von 1 oder 2.
* Wortlänge zwischen 5 und 8.
* Hard-/Software Flow Control kann je an oder aus sein.

Der Standard ist: 115200 Baud, Parität None, 1 Stop Bits, Wortlänge 8, half duplex.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Baudrate', 'uint32', 1, 'out'),
             ('Parity', 'uint8', 1, 'out', ('Parity', [('None', 0),
                                                       ('Odd', 1),
                                                       ('Even', 2)])),
             ('Stopbits', 'uint8', 1, 'out', ('Stopbits', [('1', 1),
                                                           ('2', 2)])),
             ('Wordlength', 'uint8', 1, 'out', ('Wordlength', [('5', 5),
                                                               ('6', 6),
                                                               ('7', 7),
                                                               ('8', 8)])),
             ('Duplex', 'uint8', 1, 'out', ('Duplex', [('Half', 0),
                                                       ('Full', 1)]))],
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
'type': 'function',
'name': 'Set Communication LED Config',
'elements': [('Config', 'uint8', 1, 'in', ('Communication LED Config', [('Off', 0),
                                                                        ('On', 1),
                                                                        ('Show Communication', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
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
'name': 'Get Communication LED Config',
'elements': [('Config', 'uint8', 1, 'out', ('Communication LED Config', [('Off', 0),
                                                                         ('On', 1),
                                                                         ('Show Communication', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
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
'name': 'Set Error LED Config',
'elements': [('Config', 'uint8', 1, 'in', ('Error LED Config', [('Off', 0),
                                                                ('On', 1),
                                                                ('Show Error', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
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
'name': 'Get Error LED Config',
'elements': [('Config', 'uint8', 1, 'out', ('Error LED Config', [('Off', 0),
                                                                 ('On', 1),
                                                                 ('Show Error', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
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
'name': 'Set Buffer Config',
'elements': [('Send Buffer Size', 'uint16', 1, 'in'),
             ('Receive Buffer Size', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Current buffer content is lost if called

Sum = X, min for both = 1024
default = 50/50
""",
'de':
"""

"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Buffer Config',
'elements': [('Send Buffer Size', 'uint16', 1, 'out'),
             ('Receive Buffer Size', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sum = X, min for both = 1024
default = 50/50
""",
'de':
"""

"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Buffer Status',
'elements': [('Send Buffer Used', 'uint16', 1, 'out'),
             ('Receive Buffer Used', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Used bytes of send/receive buffer
""",
'de':
"""

"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Enable Error Count Callback',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Enables the :func:`ErrorCountCallback`.

By default the callback is disabled.
""",
'de':
"""
Aktiviert den :func:`ErrorCountCallback`.

Im Startzustand ist der Callback deaktiviert
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Disable Error Count Callback',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Disables the :func:`ErrorCountCallback`.

By default the callback is disabled.
""",
'de':
"""
Deaktiviert den :func:`ErrorCountCallback`.

Im Startzustand ist der Callback deaktiviert
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is Error Count Callback Enabled',
'elements': [('Enabled', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns *true* if the :func:`ErrorCountCallback` is enabled,
*false* otherwise.
""",
'de':
"""
Gibt *true* zurück falls :func:`ErrorCountCallback` aktiviert ist, 
*false* sonst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Error Count',
'elements': [('Overrun Error Count', 'uint32', 1, 'out'),
             ('Parity Error Count', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
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
'name': 'Read Callback',
'elements': [('Message', 'char', 60, 'out'),
             ('Length', 'uint8', 1, 'out')],
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

com['packets'].append({
'type': 'callback',
'name': 'Error Count Callback',
'elements': [('Overrun Error Count', 'uint32', 1, 'out'),
             ('Parity Error Count', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called if a new error occurs. It has a 
Possible errors are overrun and parity error.
""",
'de':
"""
Dieser Callback wird aufgerufen wenn ein Fehler auftritt.
Mögliche Fehler sind Overrun-, Parity- oder Framing-Fehler.
"""
}]
})

