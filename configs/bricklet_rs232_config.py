# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# RS232 Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 2],
    'category': 'Bricklet',
    'device_identifier': 254,
    'name': 'RS232',
    'display_name': 'RS232',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Communicates with RS232 devices',
        'de': 'Kommuniziert mit RS232 Geräten'
    },
    'released': True,
    'documented': True,
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

See :func:`Set Configuration` for configuration possibilities
regarding baudrate, parity and so on.
""",
'de':
"""
Schreibt einen String aus bis zu 60 Zeichen auf die RS232-Schnittstelle. Der
String kann aus Binärdaten bestehen, ASCII o.ä. ist nicht notwendig.

Die Länge des Strings muss als ein zusätzlicher Parameter angegeben werden.

Der Rückgabewert ist die Anzahl der Zeichen die geschrieben werden konnten.

Siehe :func:`Set Configuration` für Konfigurationsmöglichkeiten
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
callbacks. See :func:`Enable Read Callback` and :cb:`Read Callback` callback.
""",
'de':
"""
Gibt die aktuell gespeicherte Nachricht zurück. Die maximale Länge
beträgt 60. Wenn die Länge als 0 gegeben wird, waren keine
neuen Daten verfügbar.

Anstatt mit dieser Funktion zu pollen, ist es auch möglich
Callbacks zu nutzen. Siehe :func:`Enable Read Callback` und
:cb:`Read Callback` Callback.
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
Enables the :cb:`Read Callback` callback.

By default the callback is disabled.
""",
'de':
"""
Aktiviert den :cb:`Read Callback` Callback.

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
Disables the :cb:`Read Callback` callback.

By default the callback is disabled.
""",
'de':
"""
Deaktiviert den :cb:`Read Callback` Callback.

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
Returns *true* if the :cb:`Read Callback` callback is enabled,
*false* otherwise.
""",
'de':
"""
Gibt *true* zurück falls :cb:`Read Callback` Callback aktiviert ist,
*false* sonst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('Baudrate', 'uint8', 1, 'in', ('Baudrate', [('300', 0),
                                                          ('600', 1),
                                                          ('1200', 2),
                                                          ('2400', 3),
                                                          ('4800', 4),
                                                          ('9600', 5),
                                                          ('14400', 6),
                                                          ('19200', 7),
                                                          ('28800', 8),
                                                          ('38400', 9),
                                                          ('57600', 10),
                                                          ('115200', 11),
                                                          ('230400', 12)])),
             ('Parity', 'uint8', 1, 'in', ('Parity', [('None', 0),
                                                      ('Odd', 1),
                                                      ('Even', 2),
                                                      ('Forced Parity 1', 3),
                                                      ('Forced Parity 0', 4)])),
             ('Stopbits', 'uint8', 1, 'in', ('Stopbits', [('1', 1),
                                                          ('2', 2)])),
             ('Wordlength', 'uint8', 1, 'in', ('Wordlength', [('5', 5),
                                                              ('6', 6),
                                                              ('7', 7),
                                                              ('8', 8)])),
             ('Hardware Flowcontrol', 'uint8', 1, 'in', ('Hardware Flowcontrol', [('Off', 0),
                                                                                  ('On', 1)])),
             ('Software Flowcontrol', 'uint8', 1, 'in', ('Software Flowcontrol', [('Off', 0),
                                                                                  ('On', 1)]))],

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
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Baudrate', 'uint8', 1, 'out', ('Baudrate', [('300', 0),
                                                           ('600', 1),
                                                           ('1200', 2),
                                                           ('2400', 3),
                                                           ('4800', 4),
                                                           ('9600', 5),
                                                           ('14400', 6),
                                                           ('19200', 7),
                                                           ('28800', 8),
                                                           ('38400', 9),
                                                           ('57600', 10),
                                                           ('115200', 11),
                                                           ('230400', 12)])),
             ('Parity', 'uint8', 1, 'out', ('Parity', [('None', 0),
                                                       ('Odd', 1),
                                                       ('Even', 2),
                                                       ('Forced Parity 1', 3),
                                                       ('Forced Parity 0', 4)])),
             ('Stopbits', 'uint8', 1, 'out', ('Stopbits', [('1', 1),
                                                           ('2', 2)])),
             ('Wordlength', 'uint8', 1, 'out', ('Wordlength', [('5', 5),
                                                               ('6', 6),
                                                               ('7', 7),
                                                               ('8', 8)])),
             ('Hardware Flowcontrol', 'uint8', 1, 'out', ('Hardware Flowcontrol', [('Off', 0),
                                                                                   ('On', 1)])),
             ('Software Flowcontrol', 'uint8', 1, 'out', ('Software Flowcontrol', [('Off', 0),
                                                                                   ('On', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the configuration as set by :func:`Set Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Configuration` gesetzt.
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

To enable this callback, use :func:`Enable Read Callback`.
""",
'de':
"""
Dieser Callback wird aufgerufen wenn neue Daten zur Verfügung stehen.
Die Nachricht hat eine Maximalgröße von 60 Zeichen. Die Länge
der Nachricht wird zusätzlich übergeben.

Dieser Callback kann durch :func:`Enable Read Callback` aktiviert werden.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Error Callback',
'elements': [('Error', 'uint8', 1, 'out', ('Error', [('Overrun', 1),
                                                     ('Parity', 2),
                                                     ('Framing', 4)]))],
'since_firmware': [2, 0, 1],
'doc': ['c', {
'en':
"""
This callback is called if an error occurs.
Possible errors are overrun, parity or framing error.
""",
'de':
"""
Dieser Callback wird aufgerufen wenn ein Fehler auftritt.
Mögliche Fehler sind Overrun-, Parity- oder Framing-Fehler.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Break Condition',
'elements': [('Break Time', 'uint16', 1, 'in')],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Sets a break condition (the TX output is forced to a logic 0 state).
The parameter sets the hold-time of the break condition (in ms).
""",
'de':
"""
Setzt eine Break Condition (die TX-Ausgabe wird fest of logisch 0 gezwungen).
Der Parameter setzt die Haltezeit der Break Condition (in ms).
"""
}]
})

com['examples'].append({
'name': 'Loopback',
'functions': [('setter', 'Enable Read Callback', [], 'Enable read callback', None)],
'incomplete': True # because of special logic and callback with array parameter
})
