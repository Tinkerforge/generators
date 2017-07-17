# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# RS485 Bricklet communication config

EXCEPTION_CODE_CONSTANTS =  ('Exception Code', [('Timeout', -1),
                                                ('Success', 0),
                                                ('Illegal Function', 1),
                                                ('Illegal Data Address', 2),
                                                ('Illegal Data Value', 3),
                                                ('Slave Device Failure', 4),
                                                ('Acknowledge', 5),
                                                ('Slave Device Busy', 6),
                                                ('Memory Parity Error', 8),
                                                ('Gateway Path Unavailable', 10),
                                                ('Gateway Target Device Failed To Respond', 11)])

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 277,
    'name': 'RS485',
    'display_name': 'RS485',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Communicates with RS485/Modbus devices with full- or half-duplex',
        'de': 'Kommuniziert mit RS485/Modbus Geräten mit voll- oder halb-duplex'
    },
    'comcu': True,
    'released': False,
    'documented': False,
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
'doc': ['llf', {
'en':
"""
Writes characters to the RS485 interface. The characters can be binary data,
ASCII or similar is not necessary.

The return value is the number of characters that were written.

See :func:`Set RS485 Configuration` for configuration possibilities
regarding baudrate, parity and so on.
""",
'de':
"""
Schreibt Zeichen auf die RS485-Schnittstelle. Die Zeichen können Binärdaten
sein, ASCII o.ä. ist nicht notwendig.

Der Rückgabewert ist die Anzahl der Zeichen die geschrieben wurden.

Siehe :func:`Set RS485 Configuration` für Konfigurationsmöglichkeiten
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
'doc': ['llf', {
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
der Read-Callback nich aktiv ist.
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

* Slave Address: Address to be used as the Modbus slave address in Modbus slave mode. Valid Modbus slave address range is 1 to 247.
* Master Request Timeout: Specifies how long the master should wait for a response from a slave in milliseconds when in Modbus master mode.

The default is: Slave Address = 1 and Master Request Timeout = 1000 milliseconds (1 second).
""",
'de':
"""
Setzt die Konfiguration für die RS485 Modbus Kommunikation. Verfügbare Optionen:

* Slave Address: Addresse die vom Modbus-Slave im Modbus-Slave Modus genutzt wird. Der gültige Adressbereich ist 1 bis 247.
* Master Request Timeout: Spezifiziert wie lange der Modbus-Master auf eine Antwort von einem Modbus-Slave wartet. Die Angabe ist in Millisekunden.

Die Standardwerte sind Slave Address = 1 und Master Request Timeout = 1000 Millisekunden (1 Sekunde).
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
                                                 ('Modbus Master RTU', 1),
                                                 ('Modbus Slave RTU', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the mode of the Bricklet in which it operates. Available options are

* RS485,
* Modbus Master RTU and
* Modbus Slave RTU.

The default is: RS485 mode.
""",
'de':
"""
Setzt den Modus des Bricklets. Verfügbare Optionen sind

* RS485,
* Modbus Master RTU und
* Modbus Slave RTU.

Der Standardmodus ist RS485.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Mode',
'elements': [('Mode', 'uint8', 1, 'out',('Mode', [('RS485', 0),
                                                  ('Modbus Master RTU', 1),
                                                  ('Modbus Slave RTU', 2)]))],
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
über RS485 empfangen wurden aber noch nicht über :func:`Read` oder
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
'de':
"""
Gibt die aktuelle Fehleranzahl für verschiedene Fehlerarten Modbus-Modus zurück.

* Timeout Error Count: Anzahl Timeouts.
* Checksum Error Count: Anzahl von Modbus CRC16 Checksummen-Fehlern.
* Frame Too Big Error Count: Anzahl von verworfenen Frames auf Grund einer zu großen Frame Größe (maximal 256 Byte).
* Illegal Function Error Count: Anzahl der Anfragen von nicht-implementierten oder illegalen Funktionen. Entsprocht Modbus Exception Code 1.
* Illegal Data Address Error Count: Anzahl der Anfragen mit ungütiger Adresse. Entspricht Modbus Exception Code 2.
* Illegal Data Value Error Count: Anzahl der Anfragen mit ungültigem Datenwert. Entspricht Modbus Exception Code 3.
* Slave Device Failure Error Count: Anzahl der nicht-behebaren Fehler eines Slaves. Entspricht Modbus Exception Code 4.

"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Slave Report Exception',
'elements': [('Request ID', 'uint8', 1, 'in'),
             ('Exception Code', 'int8', 1, 'in', EXCEPTION_CODE_CONSTANTS)],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
In Modbus slave mode this function can be used to report a Modbus exception for
a Modbus master request.

* Request ID: Request ID of the request received by the slave.
* Exception Code: Modbus exception code to report to the Modbus master.
""",
'de':
"""
Im Modbus-Slave Modus kann diese Funktion genutzt werden um eine Modbus Exception
auf eine Modbus-Master Anfrage zurückzugeben.

* Request ID: Request ID einer Anfrage eines Slaves.
* Exception Code: Modbus Exception Code für den Modbus Master.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Slave Answer Read Coils Request Low Level',
'elements': [('Request ID', 'uint8', 1, 'in'),
             ('Coils Length', 'uint16', 1, 'in'),
             ('Coils Chunk Offset', 'uint16', 1, 'in'),
             ('Coils Chunk Data', 'bool', 472, 'in')],
'high_level': {'stream_in': {'name': 'Coils'}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
'en':
"""
In Modbus slave mode this function can be used to answer a master request to
read coils.

* Request ID: Request ID of the corresponding request that is being answered.
* Coils: Data that is to be sent to the Modbus master for the corresponding request.

This function must be called from the :cb:`Modbus Slave Read Coils Request` callback
with the Request ID as provided by the argument of the callback.
""",
'de':
"""
Im Modbus-Slave Modus kann diese Funktion genutzt werden un eine Read Coils-Anfrage
eines Modbus-Masters zu beantworten.

* Request ID: Request ID der zu beantwortenden Anfrage.
* Coils: Daten die zum Modbus-Master gesendet werden sollen.

Diese Funktion muss vom :cb:`Modbus Slave Read Coils Request` Callback mit der
Request ID des Callbacks aufgerufen werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Master Read Coils',
'elements': [('Slave Address', 'uint8', 1, 'in'),
             ('Starting Address', 'uint32', 1, 'in'),
             ('Count', 'uint16', 1, 'in'),
             ('Request ID', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
In Modbus master mode this function can be used to read coils from a slave. This
function creates a Modbus function code 1 request.

* Slave Address: Address of the target Modbus slave.
* Starting Address: Starting address of the read.
* Count: Number of coils to read.

Upon success the function will return a non-zero request ID which will represent
the current request initiated by the Modbus master. In case of failure the returned
request ID will be 0.

When successful this function will also invoke the :cb:`Modbus Master Read Coils Response`
callback. In this callback the Request ID provided by the callback argument must be
matched with the Request ID returned from this function to verify that the callback
is indeed for a particular request.
""",
'de':
"""
Im Modbus-Master Modus kann diese Funktion genutzt werden um Coils vom Slave zu lesen.

* Slave Addresss: Adresse des Modbus-Slave
* Starting Address: Startadresse der Leseoperation
* Count: Anzahl der zu lesenden Coils.

Nach erfolgreichen ausführen der Leseoperation gibt diese funktion eine Request ID
zurück die nicht Null ist. Im Falle eines Fehlers wird eine Null als Request ID
zurückgegeben.

Falls kein Fehler auftritt, wird auch der :cb:`Modbus Master Read Coils Response` Callback
aufgerufen. In diesem Callback wird einer Request ID übergeben. Falls der Callback
eine Antwortet auf diese Anfrage ist, stimmt die Request ID mit der in dieser Funktion
zurückgegeben Request ID überein.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Slave Answer Read Holding Registers Request Low Level',
'elements': [('Request ID', 'uint8', 1, 'in'),
             ('Holding Registers Length', 'uint16', 1, 'in'),
             ('Holding Registers Chunk Offset', 'uint16', 1, 'in'),
             ('Holding Registers Chunk Data', 'uint16', 29, 'in')],
'high_level': {'stream_in': {'name': 'Holding Registers'}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
'en':
"""
In Modbus slave mode this function can be used to answer a master request to
read holding registers.

* Request ID: Request ID of the corresponding request that is being answered.
* Holding Registers: Data that is to be sent to the Modbus master for the corresponding request.

This function must be called from the :cb:`Modbus Slave Read Holding Registers Request`
callback with the Request ID as provided by the argument of the callback.
""",
'de':
"""
Im Modbus-Slave Modus kann diese Funktion genutzt werden un eine ``Read Holding Registers``-Anfrage
eines Modbus-Masters zu beantworten.

* Request ID: Request ID der zu beantwortenden Anfrage.
* Holding Registers: Daten die zum Modbus-Master gesendet werden sollen.

Diese Funktion muss vom :cb:`Modbus Slave Read Holding Registers Request` Callback mit der
Request ID des Callbacks aufgerufen werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Master Read Holding Registers',
'elements': [('Slave Address', 'uint8', 1, 'in'),
             ('Starting Address', 'uint32', 1, 'in'),
             ('Count', 'uint16', 1, 'in'),
             ('Request ID', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
In Modbus master mode this function can be used to read holding registers from a slave.
This function creates a Modbus function code 3 request.

* Slave Address: Address of the target Modbus slave.
* Starting Address: Starting address of the read.
* Count: Number of holding registers to read.

Upon success the function will return a non-zero request ID which will represent
the current request initiated by the Modbus master. In case of failure the returned
request ID will be 0.

When successful this function will also invoke the :cb:`Modbus Master Read Holding Registers Response`
callback. In this callback the Request ID provided by the callback argument must be matched
with the Request ID returned from this function to verify that the callback is indeed for a
particular request.
""",
'de':
"""
Im Modbus-Master Modus kann diese Funktion genutzt werden un eine Read Holding Register-Anfrage
an einen Modbus-Slave zu senden (Modbus Funktionscode 3).

* Slave Address: Addresse des anzusprechenden Modbus-Slave.
* Starting Address: Startadresse der Leseeoperation.
* Count: Anzahl der zu schreibenden Register.

Falls kein Fehler auftritt, wird auch der :cb:`Modbus Master Read Holding Registers Response` Callback
aufgerufen. In diesem Callback wird einer Request ID übergeben. Falls der Callback
eine Antwortet auf diese Anfrage ist, stimmt die Request ID mit der in dieser Funktion
zurückgegeben Request ID überein.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Slave Answer Write Single Coil Request',
'elements': [('Request ID', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
In Modbus slave mode this function can be used to answer a master request to
write a single coil.

* Request ID: Request ID of the corresponding request that is being answered.

This function must be called from the :cb:`Modbus Slave Write Single Coil Request`
callback with the Request ID as provided by the arguments of the callback.
""",
'de':
"""
Im Modbus-Slave Modus kann diese Funktion genutzt werden un eine Read Single Coil-Anfrage
eines Modbus-Masters zu beantworten.

* Request ID: Request ID der zu beantwortenden Anfrage.

Diese Funktion muss vom :cb:`Modbus Slave Write Single Coil Request` Callback mit der
Request ID des Callbacks aufgerufen werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Master Write Single Coil',
'elements': [('Slave Address', 'uint8', 1, 'in'),
             ('Coil Address', 'uint32', 1, 'in'),
             ('Coil Value', 'bool', 1, 'in'),
             ('Request ID', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
In Modbus master mode this function can be used to write a single coil of a slave.
This function creates a Modbus function code 5 request.

* Slave Address: Address of the target Modbus slave.
* Coil Address: Address of the coil.
* Coil Value: Value to be written.

Upon success the function will return a non-zero request ID which will represent
the current request initiated by the Modbus master. In case of failure the returned
request ID will be 0.

When successful this function will also invoke the :cb:`Modbus Master Write Single Coil Response`
callback. In this callback the Request ID provided by the callback argument must be matched
with the Request ID returned from this function to verify that the callback is indeed for a
particular request.
""",
'de':
"""
Im Modbus-Master Modus kann diese Funktion genutzt werden un eine einzelne Coil eines
Modbus-Slave zu schreiben (Modbus Funktionscode 5).

* Slave Address: Addresse des anzusprechenden Modbus-Slave.
* Coil Address: Adresse der Coil
* Coil Value: Zu schreibender Wert

Falls kein Fehler auftritt, wird auch der :cb:`Modbus Master Read Holding Registers Response` Callback
aufgerufen. In diesem Callback wird einer Request ID übergeben. Falls der Callback
eine Antwort auf diese Anfrage ist, stimmt die Request ID mit der in dieser Funktion
zurückgegeben Request ID überein.

Im Fehlerfall ist die Request ID 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Slave Answer Write Single Register Request',
'elements': [('Request ID', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
In Modbus slave mode this function can be used to answer a master request to
write a single register.

* Request ID: Request ID of the corresponding request that is being answered.

This function must be called from the :cb:`Modbus Slave Write Single Register Request`
callback with the Request ID, Register Address and Register Value as provided by
the arguments of the callback.
""",
'de':
"""
Im Modbus-Slave Modus kann diese Funktion genutzt werden un eine Write Single Register-Anfrage
eines Modbus-Masters zu beantworten.

* Request ID: Request ID der zu beantwortenden Anfrage.

Diese Funktion muss vom :cb:`Modbus Slave Write Single Register Request` Callback mit der
Request ID des Callbacks aufgerufen werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Master Write Single Register',
'elements': [('Slave Address', 'uint8', 1, 'in'),
             ('Register Address', 'uint32', 1, 'in'),
             ('Register Value', 'uint16', 1, 'in'),
             ('Request ID', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
In Modbus master mode this function can be used to write a single register of a
slave. This function creates a Modbus function code 6 request.

* Slave Address: Address of the target Modbus slave.
* Register Address: Address of the register.
* Register Value: Value to be written.

Upon success the function will return a non-zero request ID which will represent
the current request initiated by the Modbus master. In case of failure the returned
request ID will be 0.

When successful this function will also invoke the :cb:`Modbus Master Write Single Register Response`
callback. In this callback the Request ID provided by the callback argument must be matched
with the Request ID returned from this function to verify that the callback is indeed for a
particular request.
""",
'de':
"""
Im Modbus-Master Modus kann diese Funktion genutzt werden un ein einzelnes Register eines
Modbus-Slave zu schreiben (Modbus Funktionscode 6).

* Slave Address: Addresse des anzusprechenden Modbus-Slave.
* Register Address: Adresse des Registers
* Register Value: Zu schreibender Wert

Falls kein Fehler auftritt, wird auch der :cb:`Modbus Master Write Single Register Response` Callback
aufgerufen. In diesem Callback wird einer Request ID übergeben. Falls der Callback
eine Antwort auf diese Anfrage ist, stimmt die Request ID mit der in dieser Funktion
zurückgegeben Request ID überein.

Im Fehlerfall ist die Request ID 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Slave Answer Write Multiple Coils Request',
'elements': [('Request ID', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
In Modbus slave mode this function can be used to answer a master request to
write multiple coils.

* Request ID: Request ID of the corresponding request that is being answered.

This function must be called from the :cb:`Modbus Slave Write Multiple Coils Request`
callback with the Request ID of the callback.
""",
'de':
"""
Im Modbus-Slave Modus kann diese Funktion genutzt werden un eine Write Multiple Coils-Anfrage
eines Modbus-Masters zu beantworten.

* Request ID: Request ID der zu beantwortenden Anfrage.

Diese Funktion muss vom :cb:`Modbus Slave Write Multiple Coils Request` Callback mit der
Request ID des Callbacks aufgerufen werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Master Write Multiple Coils Low Level',
'elements': [('Slave Address', 'uint8', 1, 'in'),
             ('Starting Address', 'uint32', 1, 'in'),
             ('Coils Length', 'uint16', 1, 'in'),
             ('Coils Chunk Offset', 'uint16', 1, 'in'),
             ('Coils Chunk Data', 'bool', 440, 'in'),
             ('Request ID', 'uint8', 1, 'out')],
'high_level': {'stream_in': {'name': 'Coils'}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
'en':
"""
In Modbus master mode this function can be used to write multiple coils of a slave.
This function creates a Modbus function code 15 request.

* Slave Address: Address of the target Modbus slave.
* Starting Address: Starting address of the write.

Upon success the function will return a non-zero request ID which will represent
the current request initiated by the Modbus master. In case of failure the returned
request ID will be 0.

When successful this function will also invoke the :cb:`Modbus Master Write Multiple Coils Response`
callback. In this callback the Request ID provided by the callback argument must be matched
with the Request ID returned from this function to verify that the callback is indeed for a
particular request.
""",
'de':
"""
Im Modbus-Master Modus kann diese Funktion genutzt werden un eine mehrere Coils eines
Modbus-Slave zu schreiben (Modbus Funktionscode 15).

* Slave Address: Addresse des anzusprechenden Modbus-Slave.
* Starting Address: Startadresse der Schreibeoperation

Falls kein Fehler auftritt, wird auch der :cb:`Modbus Master Write Multiple Coils Response` Callback
aufgerufen. In diesem Callback wird einer Request ID übergeben. Falls der Callback
eine Antwort auf diese Anfrage ist, stimmt die Request ID mit der in dieser Funktion
zurückgegeben Request ID überein.

Im Fehlerfall ist die Request ID 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Slave Answer Write Multiple Registers Request',
'elements': [('Request ID', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
In Modbus slave mode this function can be used to answer a master request to
write multiple registers.

* Request ID: Request ID of the corresponding request that is being answered.

This function must be called from the :cb:`Modbus Slave Write Multiple Registers Request`
callback with the Request ID of the callback.
""",
'de':
"""
Im Modbus-Slave Modus kann diese Funktion genutzt werden un eine Write Multiple Register-Anfrage
eines Modbus-Masters zu beantworten.

* Request ID: Request ID der zu beantwortenden Anfrage.

Diese Funktion muss vom :cb:`Modbus Slave Write Multiple Registers Request` Callback mit der
Request ID des Callbacks aufgerufen werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Master Write Multiple Registers Low Level',
'elements': [('Slave Address', 'uint8', 1, 'in'),
             ('Starting Address', 'uint32', 1, 'in'),
             ('Registers Length', 'uint16', 1, 'in'),
             ('Registers Chunk Offset', 'uint16', 1, 'in'),
             ('Registers Chunk Data', 'uint16', 27, 'in'),
             ('Request ID', 'uint8', 1, 'out')],
'high_level': {'stream_in': {'name': 'Registers'}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
'en':
"""
In Modbus master mode this function can be used to write multiple registers of a slave.
This function creates a Modbus function code 16 request.

* Slave Address: Address of the target Modbus slave.
* Starting Address: Starting Address of the write.

Upon success the function will return a non-zero request ID which will represent
the current request initiated by the Modbus master. In case of failure the returned
request ID will be 0.

When successful this function will also invoke the :cb:`Modbus Master Write Multiple Registers Response`
callback. In this callback the Request ID provided by the callback argument must be matched
with the Request ID returned from this function to verify that the callback is indeed for a
particular request.
""",
'de':
"""
Im Modbus-Master Modus kann diese Funktion genutzt werden un eine mehrere Register eines
Modbus-Slave zu schreiben (Modbus Funktionscode 16).

* Slave Address: Addresse des anzusprechenden Modbus-Slave.
* Starting Address: Startadresse der Schreibeoperation

Falls kein Fehler auftritt, wird auch der :cb:`Modbus Master Write Multiple Registers Response` Callback
aufgerufen. In diesem Callback wird einer Request ID übergeben. Falls der Callback
eine Antwort auf diese Anfrage ist, stimmt die Request ID mit der in dieser Funktion
zurückgegeben Request ID überein.

Im Fehlerfall ist die Request ID 0.

"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Slave Answer Read Discrete Inputs Request Low Level',
'elements': [('Request ID', 'uint8', 1, 'in'),
             ('Discrete Inputs Length', 'uint16', 1, 'in'),
             ('Discrete Inputs Chunk Offset', 'uint16', 1, 'in'),
             ('Discrete Inputs Chunk Data', 'bool', 472, 'in')],
'high_level': {'stream_in': {'name': 'Discrete Inputs'}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
'en':
"""
In Modbus slave mode this function can be used to answer a master request to
read discrete inputs.

* Request ID: Request ID of the corresponding request that is being answered.
* Discrete Inputs: Data that is to be sent to the Modbus master for the corresponding request.

This function must be called from the :cb:`Modbus Slave Read Discrete Inputs Request`
callback with the Request ID as provided by the argument of the callback.
""",
'de':
"""
Im Modbus-Slave Modus kann diese Funktion genutzt werden un eine ``Read Discrete Inputs``-Anfrage
eines Modbus-Masters zu beantworten.

* Request ID: Request ID der zu beantwortenden Anfrage.
* Discrete Inputs: Daten die zum Modbus-Master gesendet werden sollen.

Diese Funktion muss vom :cb:`Modbus Slave Read Discrete Inputs Request` Callback mit der
Request ID des Callbacks aufgerufen werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Master Read Discrete Inputs',
'elements': [('Slave Address', 'uint8', 1, 'in'),
             ('Starting Address', 'uint32', 1, 'in'),
             ('Count', 'uint16', 1, 'in'),
             ('Request ID', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
In Modbus master mode this function can be used to read discrete inputs from a slave.
This function creates a Modbus function code 2 request.

* Slave Address: Address of the target Modbus slave.
* Starting Address: Starting address of the read.
* Count: Number of discrete inputs to read.

Upon success the function will return a non-zero request ID which will represent
the current request initiated by the Modbus master. In case of failure the returned
request ID will be 0.

When successful this function will also invoke the :cb:`Modbus Master Read Discrete Inputs Response`
callback. In this callback the Request ID provided by the callback argument must be matched
with the Request ID returned from this function to verify that the callback is indeed for a
particular request.
""",
'de':
"""
Im Modbus-Master Modus kann diese Funktion genutzt werden un eine Read Discrete Inputs-Anfrage
an einen Modbus-Slave zu senden (Modbus Funktionscode 2).

* Slave Address: Addresse des anzusprechenden Modbus-Slave.
* Starting Address: Startadresse der Leseeoperation.
* Count: Anzahl der zu lesenden Register.

Falls kein Fehler auftritt, wird auch der :cb:`Modbus Master Read Discrete Inputs Response` Callback
aufgerufen. In diesem Callback wird einer Request ID übergeben. Falls der Callback
eine Antwortet auf diese Anfrage ist, stimmt die Request ID mit der in dieser Funktion
zurückgegeben Request ID überein.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Slave Answer Read Input Registers Request Low Level',
'elements': [('Request ID', 'uint8', 1, 'in'),
             ('Input Registers Length', 'uint16', 1, 'in'),
             ('Input Registers Chunk Offset', 'uint16', 1, 'in'),
             ('Input Registers Chunk Data', 'uint16', 29, 'in')],
'high_level': {'stream_in': {'name': 'Input Registers'}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
'en':
"""
In Modbus slave mode this function can be used to answer a master request to
read input registers.

* Request ID: Request ID of the corresponding request that is being answered.
* Input Registers: Data that is to be sent to the Modbus master for the corresponding request.

This function must be called from the :cb:`Modbus Slave Read Input Registers Request` callback
with the Request ID as provided by the argument of the callback.
""",
'de':
"""
Im Modbus-Slave Modus kann diese Funktion genutzt werden un eine ``Read Input``-Anfrage
eines Modbus-Masters zu beantworten.

* Request ID: Request ID der zu beantwortenden Anfrage.
* Input Registers: Daten die zum Modbus-Master gesendet werden sollen.

Diese Funktion muss vom :cb:`Modbus Slave Read Input Registers Request` Callback mit der
Request ID des Callbacks aufgerufen werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Modbus Master Read Input Registers',
'elements': [('Slave Address', 'uint8', 1, 'in'),
             ('Starting Address', 'uint32', 1, 'in'),
             ('Count', 'uint16', 1, 'in'),
             ('Request ID', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
In Modbus master mode this function can be used to read input registers from a slave.
This function creates a Modbus function code 4 request.

* Slave Address: Address of the target Modbus slave.
* Starting Address: Starting address of the read.
* Count: Number of input registers to read.

Upon success the function will return a non-zero request ID which will represent
the current request initiated by the Modbus master. In case of failure the returned
request ID will be 0.

When successful this function will also invoke the :cb:`Modbus Master Read Input Registers Response`
callback. In this callback the Request ID provided by the callback argument must be matched
with the Request ID returned from this function to verify that the callback is indeed for a
particular request.
""",
'de':
"""
Im Modbus-Master Modus kann diese Funktion genutzt werden un eine Read Input-Anfrage
an einen Modbus-Slave zu senden (Modbus Funktionscode 4).

* Slave Address: Addresse des anzusprechenden Modbus-Slave.
* Starting Address: Startadresse der Leseeoperation.
* Count: Anzahl der zu lesenden Register.

Falls kein Fehler auftritt, wird auch der :cb:`Modbus Master Read Input Registers Response` Callback
aufgerufen. In diesem Callback wird einer Request ID übergeben. Falls der Callback
eine Antwortet auf diese Anfrage ist, stimmt die Request ID mit der in dieser Funktion
zurückgegeben Request ID überein.
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
'doc': ['llc', {
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
'name': 'Modbus Slave Read Coils Request',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Starting Address', 'uint32', 1, 'out'),
             ('Count', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called only in Modbus slave mode when the slave receives a
valid request from a Modbus master to read coils. The :word:`parameters` are
request ID of the request, the starting address and the number of coils to
be read as received by the request.

To send a response of this request use :func:`Modbus Slave Answer Read Coils Request`.
""",
'de':
"""
Dieser Callback wird im Modbus-Slave Modus aufgerufen, wenn der Slave eine
gültige Anfrage eines Masters zum lesen von Coils erhält. Die :word:`parameters`
sind die Request ID der Anfrage, die Startadresse und die Anzahl der zu lesenden
Coils.

Eine Antwort auf diese Anfrage kann mit der Funktion
:func:`Modbus Slave Answer Read Coils Request` gesendet werden.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Master Read Coils Response Low Level',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Exception Code', 'int8', 1, 'out', EXCEPTION_CODE_CONSTANTS),
             ('Coils Length', 'uint16', 1, 'out'),
             ('Coils Chunk Offset', 'uint16', 1, 'out'),
             ('Coils Chunk Data', 'bool', 464, 'out')],
'high_level': {'stream_out': {'name': 'Coils'}},
'since_firmware': [1, 0, 0],
'doc': ['llc', {
'en':
"""
This callback is called only in Modbus master mode when the master receives a
valid response of a request to read coils.

The :word:`parameters` are request ID
of the request, exception code of the response and the data as received by the
response.

Any non-zero exception code indicates a problem. If the exception code
is greater than zero then the number represents a Modbus exception code. If it is
less than zero then it represents other errors. For example, -1 indicates that
the request timed out or that the master did not receive any valid response of the
request within the master request timeout period as set by
:func:`Set Modbus Configuration`.
""",
'de':
"""
Dieser Callback wird im Modbus-Master Modus aufgerufen, wenn der Master eine
gültige Antwort auf eine Read Coils-Anfrage zurück bekommt.

Die :word:`parameters` sind die Request ID der Anfrage, der Exception Code der
Antwort und die empfangenen Daten.

Ein Exception Code der nicht Null ist, beschreibt einen Fehler. Wenn die Zahl größer Null ist,
entspricht der Code dem Modbus Exception Code. Wenn die Zahl kleiner Null ist,
ist ein anderer Fehler aufgetreten. Ein Wert von -1 bedeutet, dass es einen
Timeout bei der Anfrage gab. Die Länge dieses Timeouts kann per
:func:`Set Modbus Configuration` gesetzt werden.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Slave Read Holding Registers Request',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Starting Address', 'uint32', 1, 'out'),
             ('Count', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called only in Modbus slave mode when the slave receives a
valid request from a Modbus master to read holding registers. The :word:`parameters`
are request ID of the request, the starting address and the number of holding
registers to be read as received by the request.

To send a response of this request use :func:`Modbus Slave Answer Read Holding Registers Request`.
""",
'de':
"""
Dieser Callback wird im Modbus-Slave Modus aufgerufen, wenn der Slave eine
gültige Anfrage eines Masters zum lesen von Holding Registern erhält. Die :word:`parameters`
sind die Request ID der Anfrage, die Startadresse und die Anzahl der zu lesenden
Register.

Eine Antwort auf diese Anfrage kann mit der Funktion
:func:`Modbus Slave Answer Read Holding Registers Request` gesendet werden.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Master Read Holding Registers Response Low Level',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Exception Code', 'int8', 1, 'out', EXCEPTION_CODE_CONSTANTS),
             ('Holding Registers Length', 'uint16', 1, 'out'),
             ('Holding Registers Chunk Offset', 'uint16', 1, 'out'),
             ('Holding Registers Chunk Data', 'uint16', 29, 'out')],
'high_level': {'stream_out': {'name': 'Holding Registers'}},
'since_firmware': [1, 0, 0],
'doc': ['llc', {
'en':
"""
This callback is called only in Modbus master mode when the master receives a
valid response of a request to read holding registers.

The :word:`parameters` are
request ID of the request, exception code of the response and the data as received
by the response.

Any non-zero exception code indicates a problem. If the exception
code is greater than zero then the number represents a Modbus exception code. If
it is less than zero then it represents other errors. For example, -1 indicates that
the request timed out or that the master did not receive any valid response of the
request within the master request timeout period as set by
:func:`Set Modbus Configuration`.
""",
'de':
"""
Dieser Callback wird im Modbus-Master Modus aufgerufen, wenn der Master eine
gültige Antwort auf eine Read Holding Registers-Anfrage zurück bekommt.

Die :word:`parameters` sind die Request ID der Anfrage, der Exception Code der
Antwort und die empfangenen Daten.

Ein Exception Code der nicht Null ist, beschreibt einen Fehler. Wenn die Zahl größer Null ist,
entspricht der Code dem Modbus Exception Code. Wenn die Zahl kleiner Null ist,
ist ein anderer Fehler aufgetreten. Ein Wert von -1 bedeutet, dass es einen
Timeout bei der Anfrage gab. Die Länge dieses Timeouts kann per
:func:`Set Modbus Configuration` gesetzt werden.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Slave Write Single Coil Request',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Coil Address', 'uint32', 1, 'out'),
             ('Coil Value', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called only in Modbus slave mode when the slave receives a
valid request from a Modbus master to write a single coil. The :word:`parameters`
are request ID of the request, the coil address and the value of coil to be
written as received by the request.

To send a response of this request use :func:`Modbus Slave Answer Write Single Coil Request`.
""",
'de':
"""
Dieser Callback wird im Modbus-Slave Modus aufgerufen, wenn der Slave eine
gültige Anfrage eines Masters zum schreiben einer einzelnen Coil erhält. Die :word:`parameters`
sind die Request ID der Anfrage, die Adresse der Coil und der Wert der zu schreibenen
Coil.

Eine Antwort auf diese Anfrage kann mit der Funktion
:func:`Modbus Slave Answer Write Single Coil Request` gesendet werden.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Master Write Single Coil Response',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Exception Code', 'int8', 1, 'out', EXCEPTION_CODE_CONSTANTS)],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called only in Modbus master mode when the master receives a
valid response of a request to write a single coil.

The :word:`parameters` are
request ID of the request and exception code of the response.

Any non-zero exception code indicates a problem.
If the exception code is greater than zero then the number represents a Modbus
exception code. If it is less than zero then it represents other errors. For
example, -1 indicates that the request timed out or that the master did not receive
any valid response of the request within the master request timeout period as set
by :func:`Set Modbus Configuration`.
""",
'de':
"""
Dieser Callback wird im Modbus-Master Modus aufgerufen, wenn der Master eine
gültige Antwort auf eine Write Single Coil-Anfrage zurück bekommt.

Die :word:`parameters` sind die Request ID der Anfrage und der Exception Code der
Antwort.

Ein Exception Code der nicht Null ist, beschreibt einen Fehler. Wenn die Zahl größer Null ist,
entspricht der Code dem Modbus Exception Code. Wenn die Zahl kleiner Null ist,
ist ein anderer Fehler aufgetreten. Ein Wert von -1 bedeutet, dass es einen
Timeout bei der Anfrage gab. Die Länge dieses Timeouts kann per
:func:`Set Modbus Configuration` gesetzt werden.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Slave Write Single Register Request',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Register Address', 'uint32', 1, 'out'),
             ('Register Value', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called only in Modbus slave mode when the slave receives a
valid request from a Modbus master to write a single register. The :word:`parameters`
are request ID of the request, the register address and the register value to
be written as received by the request.

To send a response of this request use :func:`Modbus Slave Answer Write Single Register Request`.
""",
'de':
"""
Dieser Callback wird im Modbus-Slave Modus aufgerufen, wenn der Slave eine
gültige Anfrage eines Masters zum schreiben einer einzelnen Registers erhält. Die :word:`parameters`
sind die Request ID der Anfrage, die Adresse des Registers und der Wert des zuschreibenen
Registers.

Eine Antwort auf diese Anfrage kann mit der Funktion
:func:`Modbus Slave Answer Write Single Register Request` gesendet werden.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Master Write Single Register Response',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Exception Code', 'int8', 1, 'out', EXCEPTION_CODE_CONSTANTS)],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called only in Modbus master mode when the master receives a
valid response of a request to write a single register.

The :word:`parameters` are
request ID of the request and exception code of the response.

Any non-zero exception code
indicates a problem. If the exception code is greater than zero then the number
represents a Modbus exception code. If it is less than zero then it represents
other errors. For example, -1 indicates that the request timed out or that the
master did not receive any valid response of the request within the master request
timeout period as set by :func:`Set Modbus Configuration`.
""",
'de':
"""
Dieser Callback wird im Modbus-Master Modus aufgerufen, wenn der Master eine
gültige Antwort auf eine Write Single Register-Anfrage zurück bekommt.

Die :word:`parameters` sind die Request ID der Anfrage und der Exception Code der
Antwort.

Ein Exception Code der nicht Null ist, beschreibt einen Fehler. Wenn die Zahl größer Null ist,
entspricht der Code dem Modbus Exception Code. Wenn die Zahl kleiner Null ist,
ist ein anderer Fehler aufgetreten. Ein Wert von -1 bedeutet, dass es einen
Timeout bei der Anfrage gab. Die Länge dieses Timeouts kann per
:func:`Set Modbus Configuration` gesetzt werden.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Slave Write Multiple Coils Request Low Level',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Starting Address', 'uint32', 1, 'out'),
             ('Coils Length', 'uint16', 1, 'out'),
             ('Coils Chunk Offset', 'uint16', 1, 'out'),
             ('Coils Chunk Data', 'bool', 440, 'out')],
'high_level': {'stream_out': {'name': 'Coils'}},
'since_firmware': [1, 0, 0],
'doc': ['llc', {
'en':
"""
This callback is called only in Modbus slave mode when the slave receives a
valid request from a Modbus master to write multiple coils. The :word:`parameters`
are request ID of the request, the starting address and the data to be written as
received by the request.

To send a response of this request use :func:`Modbus Slave Answer Write Multiple Coils Request`.
""",
'de':
"""
Dieser Callback wird im Modbus-Slave Modus aufgerufen, wenn der Slave eine
gültige Anfrage eines Masters zum schreiben einer mehrerer Coils erhält. Die :word:`parameters`
sind die Request ID der Anfrage, die Startadresse der Coils und die zu schreibenen Daten.

Eine Antwort auf diese Anfrage kann mit der Funktion
:func:`Modbus Slave Answer Write Multiple Coils Request` gesendet werden.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Master Write Multiple Coils Response',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Exception Code', 'int8', 1, 'out', EXCEPTION_CODE_CONSTANTS)],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called only in Modbus master mode when the master receives a
valid response of a request to read coils.

The :word:`parameters` are
request ID of the request and exception code of the response.

Any non-zero exception code
indicates a problem. If the exception code is greater than zero then the number
represents a Modbus exception code. If it is less than zero then it represents
other errors. For example, -1 indicates that the request timedout or that the
master did not receive any valid response of the request within the master request
timeout period as set by :func:`Set Modbus Configuration`.
""",
'de':
"""
Dieser Callback wird im Modbus-Master Modus aufgerufen, wenn der Master eine
gültige Antwort auf eine Write Multiple Coils-Anfrage zurück bekommt.

Die :word:`parameters` sind die Request ID der Anfrage und der Exception Code der
Antwort.

Ein Exception Code der nicht Null ist, beschreibt einen Fehler. Wenn die Zahl größer Null ist,
entspricht der Code dem Modbus Exception Code. Wenn die Zahl kleiner Null ist,
ist ein anderer Fehler aufgetreten. Ein Wert von -1 bedeutet, dass es einen
Timeout bei der Anfrage gab. Die Länge dieses Timeouts kann per
:func:`Set Modbus Configuration` gesetzt werden.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Slave Write Multiple Registers Request Low Level',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Starting Address', 'uint32', 1, 'out'),
             ('Registers Length', 'uint16', 1, 'out'),
             ('Registers Chunk Offset', 'uint16', 1, 'out'),
             ('Registers Chunk Data', 'uint16', 27, 'out')],
'high_level': {'stream_out': {'name': 'Registers'}},
'since_firmware': [1, 0, 0],
'doc': ['llc', {
'en':
"""
This callback is called only in Modbus slave mode when the slave receives a
valid request from a Modbus master to write multiple registers. The :word:`parameters`
are request ID of the request, the starting address and the data to be written as
received by the request.

To send a response of this request use :func:`Modbus Slave Answer Write Multiple Registers Request`.
""",
'de':
"""
Dieser Callback wird im Modbus-Slave Modus aufgerufen, wenn der Slave eine
gültige Anfrage eines Masters zum schreiben einer mehrerer Register erhält. Die :word:`parameters`
sind die Request ID der Anfrage, die Startadresse der Register und die zu schreibenen Daten.

Eine Antwort auf diese Anfrage kann mit der Funktion
:func:`Modbus Slave Answer Write Multiple Registers Request` gesendet werden.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Master Write Multiple Registers Response',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Exception Code', 'int8', 1, 'out', EXCEPTION_CODE_CONSTANTS)],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called only in Modbus master mode when the master receives a
valid response of a request to write multiple registers.

The :word:`parameters`
are request ID of the request and exception code of the response.

Any non-zero
exception code indicates a problem. If the exception code is greater than zero then
the number represents a Modbus exception code. If it is less than zero then it
represents other errors. For example, -1 indicates that the request timedout or
that the master did not receive any valid response of the request within the master
request timeout period as set by :func:`Set Modbus Configuration`.
""",
'de':
"""
Dieser Callback wird im Modbus-Master Modus aufgerufen, wenn der Master eine
gültige Antwort auf eine Write Multiple Register-Anfrage zurück bekommt.

Die :word:`parameters` sind die Request ID der Anfrage und der Exception Code der
Antwort.

Ein Exception Code der nicht Null ist, beschreibt einen Fehler. Wenn die Zahl größer Null ist,
entspricht der Code dem Modbus Exception Code. Wenn die Zahl kleiner Null ist,
ist ein anderer Fehler aufgetreten. Ein Wert von -1 bedeutet, dass es einen
Timeout bei der Anfrage gab. Die Länge dieses Timeouts kann per
:func:`Set Modbus Configuration` gesetzt werden.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Slave Read Discrete Inputs Request',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Starting Address', 'uint32', 1, 'out'),
             ('Count', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called only in Modbus slave mode when the slave receives a
valid request from a Modbus master to read discrete inputs. The :word:`parameters`
are request ID of the request, the starting address and the number of discrete
inputs to be read as received by the request.

To send a response of this request use :func:`Modbus Slave Answer Read Discrete Inputs Request`.
""",
'de':
"""
Dieser Callback wird im Modbus-Slave Modus aufgerufen, wenn der Slave eine
gültige Anfrage eines Masters zum lesen von Discrete Inputs erhält. Die :word:`parameters`
sind die Request ID der Anfrage, die Startadresse und die Anzahl der zu lesenden
Discrete Inputs.

Eine Antwort auf diese Anfrage kann mit der Funktion
:func:`Modbus Slave Answer Read Discrete Inputs Request` gesendet werden.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Master Read Discrete Inputs Response Low Level',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Exception Code', 'int8', 1, 'out', EXCEPTION_CODE_CONSTANTS),
             ('Discrete Inputs Length', 'uint16', 1, 'out'),
             ('Discrete Inputs Chunk Offset', 'uint16', 1, 'out'),
             ('Discrete Inputs Chunk Data', 'bool', 464, 'out')],
'high_level': {'stream_out': {'name': 'Discrete Inputs'}},
'since_firmware': [1, 0, 0],
'doc': ['llc', {
'en':
"""
This callback is called only in Modbus master mode when the master receives a
valid response of a request to read discrete inputs.

The :word:`parameters` are
request ID of the request, exception code of the response and the data as received
by the response.

Any non-zero exception code indicates a problem. If the exception
code is greater than zero then the number represents a Modbus exception code. If
it is less than zero then it represents other errors. For example, -1 indicates that
the request timedout or that the master did not receive any valid response of the
request within the master request timeout period as set by
:func:`Set Modbus Configuration`.
""",
'de':
"""
Dieser Callback wird im Modbus-Master Modus aufgerufen, wenn der Master eine
gültige Antwort auf eine Read Discrete Inputs-Anfrage zurück bekommt.

Die :word:`parameters` sind die Request ID der Anfrage, der Exception Code der
Antwort und die empfangenen Daten.

Ein Exception Code der nicht Null ist, beschreibt einen Fehler. Wenn die Zahl größer Null ist,
entspricht der Code dem Modbus Exception Code. Wenn die Zahl kleiner Null ist,
ist ein anderer Fehler aufgetreten. Ein Wert von -1 bedeutet, dass es einen
Timeout bei der Anfrage gab. Die Länge dieses Timeouts kann per
:func:`Set Modbus Configuration` gesetzt werden.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Slave Read Input Registers Request',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Starting Address', 'uint32', 1, 'out'),
             ('Count', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called only in Modbus slave mode when the slave receives a
valid request from a Modbus master to read input registers. The :word:`parameters`
are request ID of the request, the starting address and the number of input
registers to be read as received by the request.

To send a response of this request use :func:`Modbus Slave Answer Read Input Registers Request`.
""",
'de':
"""
Dieser Callback wird im Modbus-Slave Modus aufgerufen, wenn der Slave eine
gültige Anfrage eines Masters zum lesen von Input Registern erhält. Die :word:`parameters`
sind die Request ID der Anfrage, die Startadresse und die Anzahl der zu lesenden
Register.

Eine Antwort auf diese Anfrage kann mit der Funktion
:func:`Modbus Slave Answer Read Input Registers Request` gesendet werden.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Modbus Master Read Input Registers Response Low Level',
'elements': [('Request ID', 'uint8', 1, 'out'),
             ('Exception Code', 'int8', 1, 'out', EXCEPTION_CODE_CONSTANTS),
             ('Input Registers Length', 'uint16', 1, 'out'),
             ('Input Registers Chunk Offset', 'uint16', 1, 'out'),
             ('Input Registers Chunk Data', 'uint16', 29, 'out')],
'high_level': {'stream_out': {'name': 'Input Registers'}},
'since_firmware': [1, 0, 0],
'doc': ['llc', {
'en':
"""
This callback is called only in Modbus master mode when the master receives a
valid response of a request to read input registers.

The :word:`parameters` are
request ID of the request, exception code of the response and the data as received
by the response.

Any non-zero exception code indicates a problem. If the exception
code is greater than zero then the number represents a Modbus exception code. If
it is less than zero then it represents other errors. For example, -1 indicates that
the request timedout or that the master did not receive any valid response of the
request within the master request timeout period as set by
:func:`Set Modbus Configuration`.
""",
'de':
"""
Dieser Callback wird im Modbus-Master Modus aufgerufen, wenn der Master eine
gültige Antwort auf eine Read Input Registers-Anfrage zurück bekommt.

Die :word:`parameters` sind die Request ID der Anfrage, der Exception Code der
Antwort und die empfangenen Daten.

Ein Exception Code der nicht Null ist, beschreibt einen Fehler. Wenn die Zahl größer Null ist,
entspricht der Code dem Modbus Exception Code. Wenn die Zahl kleiner Null ist,
ist ein anderer Fehler aufgetreten. Ein Wert von -1 bedeutet, dass es einen
Timeout bei der Anfrage gab. Die Länge dieses Timeouts kann per
:func:`Set Modbus Configuration` gesetzt werden.
"""
}]
})

com['examples'].append({
'name': 'Loopback',
'description': 'For this example connect the RX+/- pins to TX+/- pins on the same Bricklet\nand configure the DIP switch on the Bricklet to full-duplex mode',
'functions': [('callback', ('Read', 'read'), [(('Message', 'Message'), 'char', None, None, None, None)], None, None), # FIXME: wrong message type
              ('setter', 'Enable Read Callback', [], 'Enable read callback', None)],
'incomplete': True # because of special logic and callback with array parameter
})

com['examples'].append({
'name': 'Modbus Master',
'functions': [('setter', 'Set Mode', [('uint8:constant', 1)], 'Set operating mode to Modbus RTU master', None),
              ('setter', 'Set Modbus Configuration', [('uint8', 1), ('uint32', 1000)], 'Modbus specific configuration:\n- slave address = 1 (unused in master mode)\n- master request timeout = 1000ms', None),
              ('callback', ('Modbus Master Write Single Register Response', 'Modbus master write single register response'), [(('Request ID', 'Request ID'), 'uint8', None, None, None, None), (('Exception Code', 'Exception Code'), 'int8', None, None, None, None)], None, None),
              ('setter', 'Modbus Master Write Single Register', [('uint8', 17), ('uint32', 42), ('uint16', 65535)], 'Write 65535 to register 42 of slave 17', None)],
'incomplete': True # because of special callback logic and missing return value handling of the write call
})

com['examples'].append({
'name': 'Modbus Slave',
'functions': [('setter', 'Set Mode', [('uint8:constant', 2)], 'Set operating mode to Modbus RTU slave', None),
              ('setter', 'Set Modbus Configuration', [('uint8', 17), ('uint32', 0)], 'Modbus specific configuration:\n- slave address = 17\n- master request timeout = 0ms (unused in slave mode)', None),
              ('callback', ('Modbus Slave Write Single Register Request', 'Modbus slave write single register request'), [(('Request ID', 'Request ID'), 'uint8', None, None, None, None), (('Register Address', 'Register Address'), 'uint32', None, None, None, None), (('Register Value', 'Register Value'), 'uint16', None, None, None, None)], None, None)],
'incomplete': True # because of special callback logic
})
