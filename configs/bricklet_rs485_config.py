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
    'name': 'RS485',
    'display_name': 'RS485',
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
Writes a string of up to 60 characters to the RS485 interface. The string
can be binary data, ASCII or similar is not necessary.

The length of the string has to be given as an additional parameter.

The return value is the number of bytes that could be written.

See :func:`Set RS485 Configuration` for configuration possibilities
regarding baudrate, parity and so on.
""",
'de':
"""
Schreibt einen String aus bis zu 60 Zeichen auf die RS485-Schnittstelle. Der
String kann aus Binärdaten bestehen, ASCII o.ä. ist nicht notwendig.

Die Länge des Strings muss als ein zusätzlicher Parameter angegeben werden.

Der Rückgabewert ist die Anzahl der Zeichen die geschrieben werden konnten.

Siehe :func:`Set RS485 Configuration` für Konfigurationsmöglichkeiten
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
Disables the :cb:`Read Callback` callback.

By default the callback is disabled.
""",
'de':
"""
Deaktiviert den :cb:`Read Callback` Callback.

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
'name': 'Set RS485 Configuration',
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
Sets the configuration for the RS485 communication. Available options:

* Baudrate between 100 and 2000000 baud.
* Parity of none, odd or even.
* Stopbits can be 1 or 2.
* Word length of 5 to 8.
* Half- or Full-Duplex.

The default is: 115200 baud, parity none, 1 stop bit, word length 8, half duplex.
""",
'de':
"""
Setzt die Konfiguration für die RS485-Kommunikation.
Verfügbare Optionen sind:

* Baudrate zwischen 100 und YYY 2000000 Baud.
* Parität von None, Odd und Even Parity.
* Stop Bits von 1 oder 2.
* Wortlänge zwischen 5 und 8.
* Half- oder Full-Duplex.

Der Standard ist: 115200 Baud, Parität None, 1 Stop Bits, Wortlänge 8, half duplex.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get RS485 Configuration',
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
Returns the configuration as set by :func:`Set RS485 Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set RS485 Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Modbus Configuration',
'elements': [('Slave Address', 'uint8', 1, 'in'),
             ('Master Request Timeout', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the configuration for the RS485 Modbus communication. Available options:

* Slave Address to be used in Modbus slave mode.
* Master Request Timeout specifies how long the master should wait for a response from a slave in milliseconds.

""",
'de': #TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Modbus Configuration',
'elements': [('Slave Address', 'uint8', 1, 'out'),
             ('Master Request Timeout', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the configuration as set by :func:`Set Modbus Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Modbus Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Mode',
'elements': [('Mode', 'uint8', 1, 'in',('Mode', [('RS485', 0),
                                                  ('Modbus Slave RTU', 1),
                                                  ('Modbus Master RTU', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the mode of the Bricklet on which it operates.
""",
'de': #TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Mode',
'elements': [('Mode', 'uint8', 1, 'out',('Mode', [('RS485', 0),
                                                  ('Modbus Slave RTU', 1),
                                                  ('Modbus Master RTU', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the configuration as set by :func:`Set Mode`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Mode` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Apply Configuration',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
This function must be called after any configuration changes.
""",
'de': #TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Communication LED Config',
'elements': [('Config', 'uint8', 1, 'in', ('Communication LED Config', [('Off', 0),
                                                                        ('On', 1),
                                                                        ('Show Communication', 2),
                                                                        ('Show Heartbeat', 3)]))],
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
                                                                         ('Show Communication', 2),
                                                                         ('Show Heartbeat', 3)]))],
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
                                                                ('Show Error', 2),
                                                                ('Show Heartbeat', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the error LED configuration.

By default the error LED turns on if there is any error (see :cb:`Error Count`
callback). If you call this function with the SHOW ERROR option again, the LED
will turn off until the next error occurs.

You can also turn the LED permanently on/off or show a heartbeat.

If the Bricklet is in bootloader mode, the LED is off.
""",
'de':
"""
Setzt die Konfiguration der Error-LED.

Standardmäßig geht die LED an, wenn ein Error auftritt (siehe :cb:`Error Count`
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
                                                                 ('Show Error', 2),
                                                                 ('Show Heartbeat', 3)]))],
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
received through RS485 but could not yet be send to the
user, either by :func:`Read` or through :cb:`Read Callback` callback.

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
über RS485 empfangen wurden aber noch nicht über :func:`Read` oder
:cb:`Read Callback` Callback an ein Nutzerprogramm übertragen werden konnten.

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
'name': 'Enable Error Count Callback',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Enables the :cb:`Error Count` callback.

By default the callback is disabled.
""",
'de':
"""
Aktiviert den :cb:`Error Count` Callback.

Im Startzustand ist der Callback deaktiviert.
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
Disables the :cb:`Error Count` callback.

By default the callback is disabled.
""",
'de':
"""
Deaktiviert den :cb:`Error Count` Callback.

Im Startzustand ist der Callback deaktiviert.
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
Returns *true* if the :cb:`Error Count` callback is enabled,
*false* otherwise.
""",
'de':
"""
Gibt *true* zurück falls :cb:`Error Count` Callback aktiviert ist,
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
Returns the current number of overrun and parity errors.
""",
'de':
"""
Gibt die aktuelle Anzahl an Overrun und Parity Fehlern zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Modbus Common Error Count',
'elements': [('Timeout Error Count', 'uint32', 1, 'out'),
             ('Checksum Error Count', 'uint32', 1, 'out'),
             ('Frame Too Big Error Count', 'uint32', 1, 'out'),
             ('Illegal Function Error Count', 'uint32', 1, 'out'),
             ('Illegal Data Address Error Count', 'uint32', 1, 'out'),
             ('Illegal Data Value Error Count', 'uint32', 1, 'out'),
             ('Slave Device Failure Error Count', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en': # TODO: English documentation.
"""
-
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Report Exception',
'elements': [('Request ID', 'uint8', 1, 'in'),
             ('Exception Code', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en': # TODO: English documentation.
"""
-
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Answer Read Coils Request Low Level',
'elements': [('Request ID', 'uint8', 1, 'in'),
             ('Stream Total Length', 'uint16', 1, 'in'),
             ('Stream Chunk Offset', 'uint16', 1, 'in'),
             ('Stream Chunk Data', 'uint8', 59, 'in')],
'high_level': {'stream_in': {}}, # FIXME: add bitmask feature.
'since_firmware': [1, 0, 0],
'doc': ['llf', {
'en': # TODO: English documentation.
"""
-
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Read Coils',
'elements': [('Slave Address', 'uint8', 1, 'in'),
             ('Starting Address', 'uint16', 1, 'in'),
             ('Count', 'uint16', 1, 'in'),
             ('Request ID', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en': # TODO: English documentation.
"""
-
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Answer Read Holding Registers Request Low Level',
'elements': [('Request ID', 'uint8', 1, 'in'),
             ('Stream Total Length', 'uint16', 1, 'in'),
             ('Stream Chunk Offset', 'uint16', 1, 'in'),
             ('Stream Chunk Data', 'uint16', 29, 'in')],
'high_level': {'stream_in': {}}, # FIXME: add bitmask feature.
'since_firmware': [1, 0, 0],
'doc': ['llf', {
'en': # TODO: English documentation.
"""
-
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Read Holding Registers',
'elements': [('Slave Address', 'uint8', 1, 'in'),
             ('Starting Address', 'uint16', 1, 'in'),
             ('Count', 'uint16', 1, 'in'),
             ('Request ID', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en': # TODO: English documentation.
"""
-
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Answer Write Single Coil Request',
'elements': [('Request ID', 'uint8', 1, 'in'),
             ('Coil Address', 'uint16', 1, 'in'),
             ('Coil Value', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en': # TODO: English documentation.
"""
-
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Write Single Coil',
'elements': [('Slave Address', 'uint8', 1, 'in'),
             ('Coil Address', 'uint16', 1, 'in'),
             ('Coil Value', 'uint16', 1, 'in'),
             ('Request ID', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en': # TODO: English documentation.
"""
-
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Answer Write Single Register Request',
'elements': [('Request ID', 'uint8', 1, 'in'),
             ('Register Address', 'uint16', 1, 'in'),
             ('Register Value', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en': # TODO: English documentation.
"""
-
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Write Single Register',
'elements': [('Slave Address', 'uint8', 1, 'in'),
             ('Register Address', 'uint16', 1, 'in'),
             ('Register Value', 'uint16', 1, 'in'),
             ('Request ID', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en': # TODO: English documentation.
"""
-
""",
'de': # TODO: German documentation.
"""
-
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
'name': 'Error Count',
'elements': [('Overrun Error Count', 'uint32', 1, 'out'),
             ('Parity Error Count', 'uint32', 1, 'out')],
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
Er gibt die Anzahl der aufgetreten Overrun and Parity Fehler zurück.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Read Coils Request',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Starting Address', 'uint16', 1, 'out'),
             ('Count', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en': # TODO: English documentation.
"""
-
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Read Coils Response Low Level',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Exception Code', 'int8', 1, 'out'), # FIXME: add constants
             ('Stream Total Length', 'uint16', 1, 'out'),
             ('Stream Chunk Offset', 'uint16', 1, 'out'),
             ('Stream Chunk Data', 'uint8', 58, 'out')],
'high_level': {'stream_out': {}}, # FIXME: add bitmask feature
'since_firmware': [1, 0, 0],
'doc': ['llc', {
'en': # TODO: English documentation.
"""
-
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Read Holding Registers Request',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Starting Address', 'uint16', 1, 'out'),
             ('Count', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en': # TODO: English documentation.
"""
-
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Read Holding Registers Response Low Level',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Exception Code', 'int8', 1, 'out'), # FIXME: add constants
             ('Stream Total Length', 'uint16', 1, 'out'),
             ('Stream Chunk Offset', 'uint16', 1, 'out'),
             ('Stream Chunk Data', 'uint16', 29, 'out')],
'high_level': {'stream_out': {}}, # FIXME: add bitmask feature
'since_firmware': [1, 0, 0],
'doc': ['llc', {
'en': # TODO: English documentation.
"""
-
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Write Single Coil Request',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Coil Address', 'uint16', 1, 'out'),
             ('Coil Value', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en': # TODO: English documentation.
"""
-
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Write Single Coil Response',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Exception Code', 'int8', 1, 'out'), # FIXME: add constants
             ('Coil Address', 'uint16', 1, 'out'),
             ('Coil Value', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en': # TODO: English documentation.
"""
-
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Write Single Register Request',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Register Address', 'uint16', 1, 'out'),
             ('Register Value', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en': # TODO: English documentation.
"""
-
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Write Single Register Response',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Exception Code', 'int8', 1, 'out'), # FIXME: add constants
             ('Register Address', 'uint16', 1, 'out'),
             ('Register Value', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en': # TODO: English documentation.
"""
-
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})
