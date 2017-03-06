# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# RS485 Bricklet communication config

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

* Slave Address: Address to be used as the Modbus slave address in Modbus slave mode. Valid Modbus slave address range is 0 to 247.
* Master Request Timeout: Specifies how long the master should wait for a response from a slave in milliseconds when in Modbus master mode.

The default is: Slave Address = 1 and Master Request Timeout = 1000 milliseconds or 1 second.
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
Sets the mode of the Bricklet in which it operates. Available options:

* RS485: Switches the operating mode of the bricklet to RS485 mode.
* Modbus Slave RTU: Switches the operating mode of the bricklet to Modbus Slave RTU mode.
* Modbus Master RTU. Switches the operating mode of the bricklet to Modbus Master RTU mode.

The default is: RS485 mode.
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
'en':
"""
Returns the current number of errors occurred in Modbus mode.

* Timeout Error Count: Number of timeouts occurred.
* Checksum Error Count: Number of failures due to Modbus frame CRC16 checksum mismatch.
* Frame Too Big Error Count: Number of times frames were rejected because they exceeded maximum Modbus frame size which is 256 bytes.
* Illegal Function Error Count: Number of errors when an unimplemented or illegal function is requested. This corresponds to Modbus exception code 1.
* Illegal Data Address Error Count: Number of errors due to invalid data address. This corresponds to Modbus exception code 2.
* Illegal Data Value Error Count: Number of errors due to invalid data value. This corresponds to Modbus exception code 3.
* Slave Device Failure Error Count: Number of errors occurred on the slave device which were unrecoverable. This corresponds to Modbus exception code 4.

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
'en':
"""
In Modbus slave mode this function can be used to report a modbus exception for
a Modbus master request.

* Request ID: Request ID of the request received by the slave.
* Exception Code: Modbus exception code to report to the Modbus master.
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
'en':
"""
In Modbus slave mode this function can be used to answer a master request to
read coils.

* Request ID: Request ID of the corresponding request that is being answered.
* Data: Data that is to be sent to the Modbus master for the corresponding request.

This function must be called from the :cb:`Modbus Read Coils Request` callback
with the Request ID as provided by the argument of the callback.
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
'en':
"""
In Modbus master mode this function can be used to read coils from a slave.

* Slave Address: Address of the target Modbus slave.
* Starting Address: Starting address of the read.
* Count: Number of coils to read.

Upon success the function will return a non-zero request ID which will represent
the current request initiated by the Modbus master. In case of failure the returned
request ID will be 0.

When successful this function will also invoke the :cb:`Modbus Read Coils Response`
callback. In this callback the Request ID provided by the callback argument must be
matched with the Request ID returned from this function to verify that the callback
is indeed for a particular request.
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
'en':
"""
In Modbus slave mode this function can be used to answer a master request to
read holding registers.

* Request ID: Request ID of the corresponding request that is being answered.
* Data: Data that is to be sent to the Modbus master for the corresponding request.

This function must be called from the :cb:`Modbus Read Holding Registers Request`
callback with the Request ID as provided by the argument of the callback.
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
'en':
"""
In Modbus master mode this function can be used to read holding registers from a slave.

* Slave Address: Address of the target Modbus slave.
* Starting Address: Starting address of the read.
* Count: Number of holding registers to read.

Upon success the function will return a non-zero request ID which will represent
the current request initiated by the Modbus master. In case of failure the returned
request ID will be 0.

When successful this function will also invoke the :cb:`Modbus Read Holding Registers Response`
callback. In this callback the Request ID provided by the callback argument must be matched
with the Request ID returned from this function to verify that the callback is indeed for a
particular request.
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
'en':
"""
In Modbus slave mode this function can be used to answer a master request to
write a single coil.

* Request ID: Request ID of the corresponding request that is being answered.
* Coil Address: Address of the coil to write.
* Coil Value: Value to be written.

This function must be called from the :cb:`Modbus Write Single Coil Request`
callback with the Request ID, Coil Address and Coil Value as provided by the
arguments of the callback.
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
'en':
"""
In Modbus master mode this function can be used to write a single coil of a slave.

* Slave Address: Address of the target Modbus slave.
* Coil Address: Address of the coil.
* Coil Value: Value to be written.

Upon success the function will return a non-zero request ID which will represent
the current request initiated by the Modbus master. In case of failure the returned
request ID will be 0.

When successful this function will also invoke the :cb:`Modbus Write Single Coil Response`
callback. In this callback the Request ID provided by the callback argument must be matched
with the Request ID returned from this function to verify that the callback is indeed for a
particular request.
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
'en':
"""
In Modbus slave mode this function can be used to answer a master request to
write a single register.

* Request ID: Request ID of the corresponding request that is being answered.
* Register Address: Address of the register to write.
* Register Value: Value to be written.

This function must be called from the :cb:`Modbus Write Single Register Request`
callback with the Request ID, Register Address and Register Value as provided by
the arguments of the callback.
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
'en':
"""
In Modbus master mode this function can be used to write a single register of a
slave.

* Slave Address: Address of the target Modbus slave.
* Register Address: Address of the register.
* Register Value: Value to be written.

Upon success the function will return a non-zero request ID which will represent
the current request initiated by the Modbus master. In case of failure the returned
request ID will be 0.

When successful this function will also invoke the :cb:`Modbus Write Single Register Response`
callback. In this callback the Request ID provided by the callback argument must be matched
with the Request ID returned from this function to verify that the callback is indeed for a
particular request.
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Answer Write Multiple Coils Request',
'elements': [('Request ID', 'uint8', 1, 'in'),
             ('Starting Address', 'uint16', 1, 'in'),
             ('Count', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
In Modbus slave mode this function can be used to answer a master request to
write multiple coils.

* Request ID: Request ID of the corresponding request that is being answered.
* Starting Address: Starting address of the write.
* Count: Number of coils to write.

This function must be called from the :cb:`Modbus Write Multiple Coils Request`
callback with the Request ID, Starting Address and Count as provided by the
arguments of the callback.
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Write Multiple Coils Low Level',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Slave Address', 'uint8', 1, 'in'),
             ('Starting Address', 'uint16', 1, 'in'),
             ('Count', 'uint16', 1, 'in'),
             ('Stream Total Length', 'uint16', 1, 'in'),
             ('Stream Chunk Offset', 'uint16', 1, 'in'),
             ('Stream Chunk Data', 'uint8', 54, 'in')],
'high_level': {'stream_in': {}}, # FIXME: add bitmask feature.
'since_firmware': [1, 0, 0],
'doc': ['llf', {
'en':
"""
In Modbus master mode this function can be used to write multiple coils of a slave.

* Slave Address: Address of the target Modbus slave.
* Starting Address: Starting address of the write.
* Count: Number of coils to write.

Upon success the function will return a non-zero request ID which will represent
the current request initiated by the Modbus master. In case of failure the returned
request ID will be 0.

When successful this function will also invoke the :cb:`Modbus Write Multiple Coils Response`
callback. In this callback the Request ID provided by the callback argument must be matched
with the Request ID returned from this function to verify that the callback is indeed for a
particular request.
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Answer Write Multiple Registers Request',
'elements': [('Request ID', 'uint8', 1, 'in'),
             ('Starting Address', 'uint16', 1, 'in'),
             ('Count', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
In Modbus slave mode this function can be used to answer a master request to
write multiple registers.

* Request ID: Request ID of the corresponding request that is being answered.
* Starting Address: Starting address of the write.
* Count: Number of registers to write.

This function must be called from the :cb:`Modbus Write Multiple Registers Request`
callback with the Request ID, Starting Address and Count as provided by the
arguments of the callback.
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Write Multiple Registers Low Level',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Slave Address', 'uint8', 1, 'in'),
             ('Starting Address', 'uint16', 1, 'in'),
             ('Count', 'uint16', 1, 'in'),
             ('Stream Total Length', 'uint16', 1, 'in'),
             ('Stream Chunk Offset', 'uint16', 1, 'in'),
             ('Stream Chunk Data', 'uint16', 27, 'in')],
'high_level': {'stream_in': {}}, # FIXME: add bitmask feature.
'since_firmware': [1, 0, 0],
'doc': ['llf', {
'en':
"""
In Modbus master mode this function can be used to write multiple registers of a slave.

* Slave Address: Address of the target Modbus slave.
* Starting Address: Starting Address of the write.
* Count: Number of registers to write.

Upon success the function will return a non-zero request ID which will represent
the current request initiated by the Modbus master. In case of failure the returned
request ID will be 0.

When successful this function will also invoke the :cb:`Modbus Write Multiple Registers Response`
callback. In this callback the Request ID provided by the callback argument must be matched
with the Request ID returned from this function to verify that the callback is indeed for a
particular request.
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Answer Read Discrete Inputs Request Low Level',
'elements': [('Request ID', 'uint8', 1, 'in'),
             ('Stream Total Length', 'uint16', 1, 'in'),
             ('Stream Chunk Offset', 'uint16', 1, 'in'),
             ('Stream Chunk Data', 'uint8', 59, 'in')],
'high_level': {'stream_in': {}}, # FIXME: add bitmask feature.
'since_firmware': [1, 0, 0],
'doc': ['llf', {
'en':
"""
In Modbus slave mode this function can be used to answer a master request to
read discrete inputs.

* Request ID: Request ID of the corresponding request that is being answered.
* Data: Data that is to be sent to the Modbus master for the corresponding request.

This function must be called from the :cb:`Modbus Read Discrete Inputs Request`
callback with the Request ID as provided by the argument of the callback.
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Read Discrete Inputs',
'elements': [('Slave Address', 'uint8', 1, 'in'),
             ('Starting Address', 'uint16', 1, 'in'),
             ('Count', 'uint16', 1, 'in'),
             ('Request ID', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
In Modbus master mode this function can be used to read discrete inputs from a slave.

* Slave Address: Address of the target Modbus slave.
* Starting Address: Starting address of the read.
* Count: Number of discrete inputs to read.

Upon success the function will return a non-zero request ID which will represent
the current request initiated by the Modbus master. In case of failure the returned
request ID will be 0.

When successful this function will also invoke the :cb:`Modbus Read Discrete Inputs Response`
callback. In this callback the Request ID provided by the callback argument must be matched
with the Request ID returned from this function to verify that the callback is indeed for a
particular request.
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Answer Read Input Registers Request Low Level',
'elements': [('Request ID', 'uint8', 1, 'in'),
             ('Stream Total Length', 'uint16', 1, 'in'),
             ('Stream Chunk Offset', 'uint16', 1, 'in'),
             ('Stream Chunk Data', 'uint16', 29, 'in')],
'high_level': {'stream_in': {}}, # FIXME: add bitmask feature.
'since_firmware': [1, 0, 0],
'doc': ['llf', {
'en':
"""
In Modbus slave mode this function can be used to answer a master request to
read input registers.

* Request ID: Request ID of the corresponding request that is being answered.
* Data: Data that is to be sent to the Modbus master for the corresponding request.

This function must be called from the :cb:`Modbus Read Input Registers Request` callback
with the Request ID as provided by the argument of the callback.
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Read Input Registers',
'elements': [('Slave Address', 'uint8', 1, 'in'),
             ('Starting Address', 'uint16', 1, 'in'),
             ('Count', 'uint16', 1, 'in'),
             ('Request ID', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
In Modbus master mode this function can be used to read input registers from a slave.

* Slave Address: Address of the target Modbus slave.
* Starting Address: Starting address of the read.
* Count: Number of input registers to read.

Upon success the function will return a non-zero request ID which will represent
the current request initiated by the Modbus master. In case of failure the returned
request ID will be 0.

When successful this function will also invoke the :cb:`Modbus Read Input Registers Response`
callback. In this callback the Request ID provided by the callback argument must be matched
with the Request ID returned from this function to verify that the callback is indeed for a
particular request.
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
'en':
"""
This callback is called only in Modbus slave mode when the slave receives a
valid request from a Modbus master to read coils. The :word:`parameters` are
request ID of the request, the starting address and the number of coils to
be read as received by the request.
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
'en':
"""
This callback is called only in Modbus master mode when the master receives a
valid response of a request to read coils. The :word:`parameters` are request ID
of the request, exception code of the response and the data as received by the
response. Any non-zero exception code indicates a problem. If the exception code
is greater than zero then the number represents a Modbus exception code. If it is
less than zero then it represents other errors. For example, -1 indicates that
the request timedout or that the master did not receive any valid response of the
request within the master request timeout period as set by
:func:`Set Modbus Configuration`.
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
'en':
"""
This callback is called only in Modbus slave mode when the slave receives a
valid request from a Modbus master to read holding registers. The :word:`parameters`
are request ID of the request, the starting address and the number of holding
registers to be read as received by the request.
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
'en':
"""
This callback is called only in Modbus master mode when the master receives a
valid response of a request to read holding registers. The :word:`parameters` are
request ID of the request, exception code of the response and the data as received
by the response. Any non-zero exception code indicates a problem. If the exception
code is greater than zero then the number represents a Modbus exception code. If
it is less than zero then it represents other errors. For example, -1 indicates that
the request timedout or that the master did not receive any valid response of the
request within the master request timeout period as set by
:func:`Set Modbus Configuration`.
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
'en':
"""
This callback is called only in Modbus slave mode when the slave receives a
valid request from a Modbus master to write a single coil. The :word:`parameters`
are request ID of the request, the coil address and the value of coil to be
written as received by the request.
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
'en':
"""
This callback is called only in Modbus master mode when the master receives a
valid response of a request to write a single coil. The :word:`parameters` are
request ID of the request, exception code of the response, coil address and coil
value as received by the response. Any non-zero exception code indicates a problem.
If the exception code is greater than zero then the number represents a Modbus
exception code. If it is less than zero then it represents other errors. For
example, -1 indicates that the request timedout or that the master did not receive
any valid response of the request within the master request timeout period as set
by :func:`Set Modbus Configuration`.
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
'en':
"""
This callback is called only in Modbus slave mode when the slave receives a
valid request from a Modbus master to write a single register. The :word:`parameters`
are request ID of the request, the register address and the register value to
be written as received by the request.
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
'en':
"""
This callback is called only in Modbus master mode when the master receives a
valid response of a request to write a single register. The :word:`parameters` are
request ID of the request, exception code of the response, register address and
the register value as received by the response. Any non-zero exception code
indicates a problem. If the exception code is greater than zero then the number
represents a Modbus exception code. If it is less than zero then it represents
other errors. For example, -1 indicates that the request timedout or that the
master did not receive any valid response of the request within the master request
timeout period as set by :func:`Set Modbus Configuration`.
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Write Multiple Coils Request Low Level',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Starting Address', 'uint16', 1, 'out'),
             ('Count', 'uint16', 1, 'out'),
             ('Stream Total Length', 'uint16', 1, 'out'),
             ('Stream Chunk Offset', 'uint16', 1, 'out'),
             ('Stream Chunk Data', 'uint8', 55, 'out')],
'high_level': {'stream_out': {}}, # FIXME: add bitmask feature
'since_firmware': [1, 0, 0],
'doc': ['llc', {
'en':
"""
This callback is called only in Modbus slave mode when the slave receives a
valid request from a Modbus master to write multiple coils. The :word:`parameters`
are request ID of the request, the starting address, the number of coils to
be written and the data to be written as received by the request.
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Write Multiple Coils Response',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Exception Code', 'int8', 1, 'out'), # FIXME: add constants
             ('Starting Address', 'uint16', 1, 'out'),
             ('Count', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called only in Modbus master mode when the master receives a
valid response of a request to read holding registers. The :word:`parameters` are
request ID of the request, exception code of the response, starting address and
number of coils to write as received by the response. Any non-zero exception code
indicates a problem. If the exception code is greater than zero then the number
represents a Modbus exception code. If it is less than zero then it represents
other errors. For example, -1 indicates that the request timedout or that the
master did not receive any valid response of the request within the master request
timeout period as set by :func:`Set Modbus Configuration`.
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Write Multiple Registers Request Low Level',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Starting Address', 'uint16', 1, 'out'),
             ('Count', 'uint16', 1, 'out'),
             ('Stream Total Length', 'uint16', 1, 'out'),
             ('Stream Chunk Offset', 'uint16', 1, 'out'),
             ('Stream Chunk Data', 'uint16', 27, 'out')],
'high_level': {'stream_out': {}}, # FIXME: add bitmask feature
'since_firmware': [1, 0, 0],
'doc': ['llc', {
'en':
"""
This callback is called only in Modbus slave mode when the slave receives a
valid request from a Modbus master to write multiple registers. The :word:`parameters`
are request ID of the request, the starting address, the number of registers to
be written and the data to be written as received by the request.
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Write Multiple Registers Response',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Exception Code', 'int8', 1, 'out'), # FIXME: add constants
             ('Starting Address', 'uint16', 1, 'out'),
             ('Count', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called only in Modbus master mode when the master receives a
valid response of a request to write multiple registers. The :word:`parameters`
are request ID of the request, exception code of the response, starting address
and the number of registers to be written as received by the response. Any non-zero
exception code indicates a problem. If the exception code is greater than zero then
the number represents a Modbus exception code. If it is less than zero then it
represents other errors. For example, -1 indicates that the request timedout or
that the master did not receive any valid response of the request within the master
request timeout period as set by :func:`Set Modbus Configuration`.
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Read Discrete Inputs Request',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Starting Address', 'uint16', 1, 'out'),
             ('Count', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called only in Modbus slave mode when the slave receives a
valid request from a Modbus master to read discrete inputs. The :word:`parameters`
are request ID of the request, the starting address and the number of discrete
inputs to be read as received by the request.
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Read Discrete Inputs Response Low Level',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Exception Code', 'int8', 1, 'out'), # FIXME: add constants
             ('Stream Total Length', 'uint16', 1, 'out'),
             ('Stream Chunk Offset', 'uint16', 1, 'out'),
             ('Stream Chunk Data', 'uint8', 58, 'out')],
'high_level': {'stream_out': {}}, # FIXME: add bitmask feature
'since_firmware': [1, 0, 0],
'doc': ['llc', {
'en':
"""
This callback is called only in Modbus master mode when the master receives a
valid response of a request to read discrete inputs. The :word:`parameters` are
request ID of the request, exception code of the response and the data as received
by the response. Any non-zero exception code indicates a problem. If the exception
code is greater than zero then the number represents a Modbus exception code. If
it is less than zero then it represents other errors. For example, -1 indicates that
the request timedout or that the master did not receive any valid response of the
request within the master request timeout period as set by
:func:`Set Modbus Configuration`.
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Read Input Registers Request',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Starting Address', 'uint16', 1, 'out'),
             ('Count', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called only in Modbus slave mode when the slave receives a
valid request from a Modbus master to read input registers. The :word:`parameters`
are request ID of the request, the starting address and the number of input
registers to be read as received by the request.
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Read Input Registers Response Low Level',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Exception Code', 'int8', 1, 'out'), # FIXME: add constants
             ('Stream Total Length', 'uint16', 1, 'out'),
             ('Stream Chunk Offset', 'uint16', 1, 'out'),
             ('Stream Chunk Data', 'uint16', 29, 'out')],
'high_level': {'stream_out': {}}, # FIXME: add bitmask feature
'since_firmware': [1, 0, 0],
'doc': ['llc', {
'en':
"""
This callback is called only in Modbus master mode when the master receives a
valid response of a request to read input registers. The :word:`parameters` are
request ID of the request, exception code of the response and the data as received
by the response. Any non-zero exception code indicates a problem. If the exception
code is greater than zero then the number represents a Modbus exception code. If
it is less than zero then it represents other errors. For example, -1 indicates that
the request timedout or that the master did not receive any valid response of the
request within the master request timeout period as set by
:func:`Set Modbus Configuration`.
""",
'de': # TODO: German documentation.
"""
-
"""
}]
})
