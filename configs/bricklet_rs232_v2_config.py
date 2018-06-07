# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# RS232 Bricklet 2.0 communication config

com = {
    'author': 'Ishraq Ibne Ashraf <ishraq@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2108,
    'name': 'RS232 V2',
    'display_name': 'RS232 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Communicates with RS232 devices',
        'de': 'Kommuniziert mit RS232 Geräten'
    },
    'comcu': True,
    'released': True,
    'documented': False,
    'discontinued': False,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Write Low Level',
'elements': [('Message Length', 'uint16', 1, 'in'),
             ('Message Chunk Offset', 'uint16', 1, 'in'),
             ('Message Chunk Data', 'char', 60, 'in'),
             ('Message Chunk Written', 'uint8', 1, 'out')],
'high_level': {'stream_in': {'name': 'Message', 'short_write': True}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes characters to the RS232 interface. The characters can be binary data,
ASCII or similar is not necessary.

The return value is the number of characters that were written.

See :func:`Set Configuration` for configuration possibilities
regarding baud rate, parity and so on.
""",
'de':
"""
Schreibt Zeichen auf die RS232-Schnittstelle. Die Zeichen können Binärdaten
sein, ASCII o.ä. ist nicht notwendig.

Der Rückgabewert ist die Anzahl der Zeichen die geschrieben wurden.

Siehe :func:`Set Configuration` für Konfigurationsmöglichkeiten
bezüglich Baudrate, Parität usw.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Read Low Level',
'elements': [('Length', 'uint16', 1, 'in'),
             ('Message Length', 'uint16', 1, 'out'),
             ('Message Chunk Offset', 'uint16', 1, 'out'),
             ('Message Chunk Data', 'char', 60, 'out')],
'high_level': {'stream_out': {'name': 'Message'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns up to *length* characters from receive buffer.

Instead of polling with this function, you can also use
callbacks. But note that this function will return available
data only when the read callback is disabled.
See :func:`Enable Read Callback` and :cb:`Read` callback.
""",
'de':
"""
Gibt bis zu *length* Zeichen aus dem Empfangsbuffer zurück.

Anstatt mit dieser Funktion zu pollen, ist es auch möglich
Callbacks zu nutzen. Diese Funktion gibt nur Daten zurück wenn
der Read-Callback nicht aktiv ist.
Siehe :func:`Enable Read Callback` und :cb:`Read` Callback.
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
Enables the :cb:`Read` callback.

By default the callback is disabled.
""",
'de':
"""
Aktiviert den :cb:`Read` Callback.

Im Startzustand ist der Callback deaktiviert.
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
Disables the :cb:`Read` callback.

By default the callback is disabled.
""",
'de':
"""
Deaktiviert den :cb:`Read` Callback.

Im Startzustand ist der Callback deaktiviert.
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
Returns *true* if the :cb:`Read` callback is enabled,
*false* otherwise.
""",
'de':
"""
Gibt *true* zurück falls :cb:`Read` Callback aktiviert ist,
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
             ('Flowcontrol', 'uint8', 1, 'in', ('Flowcontrol', [('Off', 0),
                                                                ('Software', 1),
                                                                ('Hardware', 2)]))],

'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the configuration for the RS232 communication. Available options:

* Baud rate between 100 and 2000000 baud.
* Parity of none, odd or even.
* Stop bits can be 1 or 2.
* Word length of 5 to 8.
* Flow control can be off, software or hardware.

The default is: 115200 baud, parity none, 1 stop bit, word length 8.
""",
'de':
"""
Setzt die Konfiguration für die RS232-Kommunikation.
Verfügbare Optionen sind:

* Baudrate zwischen 100 und 2000000 Baud.
* Parität von None, Odd und Even.
* Stopp-Bits von 1 oder 2.
* Wortlänge zwischen 5 und 8.
* Flow Control kann aus, Software oder Hardware sein.

Der Standard ist: 115200 Baud, Parität None, 1 Stop Bits, Wortlänge 8.
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
             ('Flowcontrol', 'uint8', 1, 'out', ('Flowcontrol', [('Off', 0),
                                                                 ('Software', 1),
                                                                 ('Hardware', 2)]))],
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
'type': 'function',
'name': 'Set Buffer Config',
'elements': [('Send Buffer Size', 'uint16', 1, 'in'),
             ('Receive Buffer Size', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the send and receive buffer size in byte. In sum there is
10240 byte (10kb) buffer available and the minimum buffer size
is 1024 byte (1kb) for both.

The current buffer content is lost if this function is called.

The send buffer holds data that is given by :func:`Write` and
can not be written yet. The receive buffer holds data that is
received through RS232 but could not yet be send to the
user, either by :func:`Read` or through :cb:`Read` callback.

The default configuration is 5120 byte (5kb) per buffer.
""",
'de':
"""
Setzt die Größe des Senden- und Empfangsbuffers. In Summe können
die Buffer eine Größe von 10240 Byte (10kb) haben, die Minimumalgröße
ist 1024 byte (1kb) für beide.

Der aktuelle Bufferinhalt geht bei einem Aufruf dieser Funktion verloren.

Der Sendenbuffer hält die Daten welche über :func:`Write` übergeben und noch
nicht geschrieben werden konnten. Der Empfangsbuffer hält Daten welche
über RS232 empfangen wurden aber noch nicht über :func:`Read` oder
:cb:`Read` Callback an ein Nutzerprogramm übertragen werden konnten.

Die Standardkonfiguration ist 5120 Byte (5kb) pro Buffer.
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
Returns the buffer configuration as set by :func:`Set Buffer Config`.
""",
'de':
"""
Gibt die Buffer-Konfiguration zurück, wie von :func:`Set Buffer Config` gesetzt.
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
Returns the currently used bytes for the send and received buffer.

See :func:`Set Buffer Config` for buffer size configuration.
""",
'de':
"""
Gibt die aktuell genutzten Bytes des Sende- und Empfangsbuffers zurück.

Siehe :func:`Set Buffer Config` zur Konfiguration der Buffergrößen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Error Count',
'elements': [('Error Count Overrun', 'uint32', 1, 'out'),
             ('Error Count Parity', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the current number of overrun and parity errors.
""",
'de':
"""
Gibt die aktuelle Anzahl an Overrun und Parity Fehlern zurück.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Read Low Level',
'elements': [('Message Length', 'uint16', 1, 'out'),
             ('Message Chunk Offset', 'uint16', 1, 'out'),
             ('Message Chunk Data', 'char', 60, 'out')],
'high_level': {'stream_out': {'name': 'Message'}},
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called if new data is available.

To enable this callback, use :func:`Enable Read Callback`.
""",
'de':
"""
Dieser Callback wird aufgerufen wenn neue Daten zur Verfügung stehen.

Dieser Callback kann durch :func:`Enable Read Callback` aktiviert werden.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Error Count',
'elements': [('Error Count Overrun', 'uint32', 1, 'out'),
             ('Error Count Parity', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called if a new error occurs. It returns
the current overrun and parity error count.
""",
'de':
"""
Dieser Callback wird aufgerufen wenn ein neuer Fehler auftritt.
Er gibt die Anzahl der aufgetreten Overrun und Parity Fehler zurück.
"""
}]
})

com['examples'].append({
'name': 'Loopback',
'description': 'For this example connect the RX pin to the TX pin on the same Bricklet',
'functions': [('callback', ('Read', 'read'), [(('Message', 'Message'), 'char', -65535, None, None, None)], None, None), # FIXME: wrong message type
              ('setter', 'Enable Read Callback', [], 'Enable read callback', None)],
'incomplete': True # because of special logic and callback with array parameter
})
