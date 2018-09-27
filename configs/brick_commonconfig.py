# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Common Brick communication config

common_packets = []

common_packets.append({
'feature': 'bricklet_comcu',
'type': 'function',
'function_id': 231,
'name': 'Set SPITFP Baudrate Config',
'elements': [('Enable Dynamic Baudrate', 'bool', 1, 'in'),
             ('Minimum Dynamic Baudrate', 'uint32', 1, 'in')],
'since_firmware': {'*': [2, 0, 0],
                   'DC': [2, 3, 5],
                   'IMU': [2, 3, 5],
                   'IMU V2': [2, 0, 10],
                   'Master': [2, 4, 6],
                   'RED': None,
                   'Servo': [2, 3, 4],
                   'Silent Stepper': [2, 0, 4],
                   'Stepper': [2, 3, 6]},
'doc': ['af', {
'en':
"""
The SPITF protocol can be used with a dynamic baudrate. If the dynamic baudrate is
enabled, the Brick will try to adapt the baudrate for the communication
between Bricks and Bricklets according to the amount of data that is transferred.

The baudrate will be increased exponentially if lots of data is send/received and
decreased linearly if little data is send/received.

This lowers the baudrate in applications where little data is transferred (e.g.
a weather station) and increases the robustness. If there is lots of data to transfer
(e.g. Thermal Imaging Bricklet) it automatically increases the baudrate as needed.

In cases where some data has to transferred as fast as possible every few seconds
(e.g. RS485 Bricklet with a high baudrate but small payload) you may want to turn
the dynamic baudrate off to get the highest possible performance.

The maximum value of the baudrate can be set per port with the function
:func:`Set SPITFP Baudrate`. If the dynamic baudrate is disabled, the baudrate
as set by :func:`Set SPITFP Baudrate` will be used statically.

The minimum dynamic baudrate has a value range of 400000 to 2000000 baud.

By default dynamic baudrate is enabled and the minimum dynamic baudrate is 400000.
""",
'de':
"""
Das SPITF-Protokoll kann mit einer dynamischen Baudrate genutzt werden. Wenn die dynamische
Baudrate aktiviert ist, versucht der Brick die Baudrate anhand des Datenaufkommens
zwischen Brick und Bricklet anzupassen.

Die Baudrate wird exponentiell erhöht wenn viele Daten gesendet/empfangen werden
und linear verringert wenn wenig Daten gesendet/empfangen werden.

Diese Vorgehensweise verringert die Baudrate in Anwendungen wo nur wenig Daten
ausgetauscht werden müssen (z.B. eine Wetterstation) und erhöht die Robustheit.
Wenn immer viele Daten ausgetauscht werden (z.B. Thermal Imaging Bricklet), wird
die Baudrate automatisch erhöht.

In Fällen wo wenige Daten all paar Sekunden so schnell wie Möglich übertragen werden
sollen (z.B. RS485 Bricklet mit hoher Baudrate aber kleinem Payload) kann die
dynamische Baudrate zum maximieren der Performance ausgestellt werden.

Die maximale Baudrate kann pro Port mit der Funktion :func:`Set SPITFP Baudrate`.
gesetzt werden. Falls die dynamische Baudrate nicht aktiviert ist, wird die Baudrate
wie von :func:`Set SPITFP Baudrate` gesetzt statisch verwendet.

Die minimale dynamische Baudrate hat einen Wertebereich von 400000 bis 2000000 Baud.

Standardmäßig ist die dynamische Baudrate aktiviert und die minimale dynamische Baudrate ist 400000.
"""
}]
})

common_packets.append({
'feature': 'bricklet_comcu',
'type': 'function',
'function_id': 232,
'name': 'Get SPITFP Baudrate Config',
'elements': [('Enable Dynamic Baudrate', 'bool', 1, 'out'),
             ('Minimum Dynamic Baudrate', 'uint32', 1, 'out')],
'since_firmware': {'*': [2, 0, 0],
                   'DC': [2, 3, 5],
                   'IMU': [2, 3, 5],
                   'IMU V2': [2, 0, 10],
                   'Master': [2, 4, 6],
                   'RED': None,
                   'Servo': [2, 3, 4],
                   'Silent Stepper': [2, 0, 4],
                   'Stepper': [2, 3, 6]},
'doc': ['af', {
'en':
"""
Returns the baudrate config, see :func:`Set SPITFP Baudrate Config`.
""",
'de':
"""
Gibt die Baudratenkonfiguration zurück, siehe :func:`Set SPITFP Baudrate Config`.
"""
}]
})

common_packets.append({
'feature': 'send_timeout_count',
'type': 'function',
'function_id': 233,
'name': 'Get Send Timeout Count',
'elements': [('Communication Method', 'uint8', 1, 'in', ('Communication Method', [('None', 0),
                                                                                  ('USB', 1),
                                                                                  ('SPI Stack', 2),
                                                                                  ('Chibi', 3),
                                                                                  ('RS485', 4),
                                                                                  ('WIFI', 5),
                                                                                  ('Ethernet', 6),
                                                                                  ('WIFI V2', 7)])),
             ('Timeout Count', 'uint32', 1, 'out')],
'since_firmware': {'*': [2, 0, 0],
                   'DC': [2, 3, 3],
                   'IMU': [2, 3, 3],
                   'IMU V2': [2, 0, 7],
                   'Master': [2, 4, 3],
                   'RED': None,
                   'Servo': [2, 3, 2],
                   'Stepper': [2, 3, 4]},
'doc': ['af', {
'en':
"""
Returns the timeout count for the different communication methods.

The methods 0-2 are available for all Bricks, 3-7 only for Master Bricks.

This function is mostly used for debugging during development, in normal operation
the counters should nearly always stay at 0.
""",
'de':
"""
Gibt den Timeout-Zähler für die verschiedenen Kommunikationsmöglichkeiten zurück

Die Kommunikationsmöglichkeiten 0-2 stehen auf allen Bricks zur verfügung, 3-7 nur auf Master Bricks.

Diese Funktion ist hauptsächlich zum debuggen während der Entwicklung gedacht.
Im normalen Betrieb sollten alle Zähler fast immer auf 0 stehen bleiben.
"""
}]
})

common_packets.append({
'feature': 'bricklet_comcu',
'type': 'function',
'function_id': 234,
'name': 'Set SPITFP Baudrate',
'elements': [('Bricklet Port', 'char', 1, 'in'),
             ('Baudrate', 'uint32', 1, 'in')],
'since_firmware': {'*': [2, 0, 0],
                   'DC': [2, 3, 3],
                   'IMU': [2, 3, 3],
                   'IMU V2': [2, 0, 5],
                   'Master': [2, 4, 3],
                   'RED': None,
                   'Servo': [2, 3, 2],
                   'Stepper': [2, 3, 3]},
'doc': ['af', {
'en':
"""
Sets the baudrate for a specific Bricklet port ('a' - 'd'). The
baudrate can be in the range 400000 to 2000000.

If you want to increase the throughput of Bricklets you can increase
the baudrate. If you get a high error count because of high
interference (see :func:`Get SPITFP Error Count`) you can decrease the
baudrate.

If the dynamic baudrate feature is enabled, the baudrate set by this
function corresponds to the maximum baudrate (see :func:`Set SPITFP Baudrate Config`).

Regulatory testing is done with the default baudrate. If CE compatibility
or similar is necessary in you applications we recommend to not change
the baudrate.

The default baudrate for all ports is 1400000.
""",
'de':
"""
Setzt die Baudrate eines spezifischen Bricklet Ports ('a' - 'd'). Die
Baudrate hat einen möglichen Wertebereich von 400000 bis 2000000.

Für einen höheren Durchsatz der Bricklets kann die Baudrate erhöht werden.
Wenn der Fehlerzähler auf Grund von lokaler Störeinstrahlung hoch ist
(siehe :func:`Get SPITFP Error Count`) kann die Baudrate verringert werden.

Wenn das Feature der dynamische Baudrate aktiviert ist, setzt diese Funktion
die maximale Baudrate (siehe :func:`Set SPITFP Baudrate Config`).

EMV Tests werden mit der Standardbaudrate durchgeführt. Falls eine
CE-Kompatibilität o.ä. in der Anwendung notwendig ist empfehlen wir die
Baudrate nicht zu ändern.

Die Standardbaudrate für alle Ports ist 1400000.
"""
}]
})

common_packets.append({
'feature': 'bricklet_comcu',
'type': 'function',
'function_id': 235,
'name': 'Get SPITFP Baudrate',
'elements': [('Bricklet Port', 'char', 1, 'in'),
             ('Baudrate', 'uint32', 1, 'out')],
'since_firmware': {'*': [2, 0, 0],
                   'DC': [2, 3, 3],
                   'IMU': [2, 3, 3],
                   'IMU V2': [2, 0, 5],
                   'Master': [2, 4, 3],
                   'RED': None,
                   'Servo': [2, 3, 2],
                   'Stepper': [2, 3, 3]},
'doc': ['af', {
'en':
"""
Returns the baudrate for a given Bricklet port, see :func:`Set SPITFP Baudrate`.
""",
'de':
"""
Gibt die Baudrate für einen Bricklet Port zurück, siehe
:func:`Set SPITFP Baudrate`.
"""
}]
})

# Keep function 236 empty, so we can always call "get_bootloader_mode"

common_packets.append({
'feature': 'bricklet_comcu',
'type': 'function',
'function_id': 237,
'name': 'Get SPITFP Error Count',
'elements': [('Bricklet Port', 'char', 1, 'in'),
             ('Error Count ACK Checksum', 'uint32', 1, 'out'),
             ('Error Count Message Checksum', 'uint32', 1, 'out'),
             ('Error Count Frame', 'uint32', 1, 'out'),
             ('Error Count Overflow', 'uint32', 1, 'out')],
'since_firmware': {'*': [2, 0, 0],
                   'DC': [2, 3, 3],
                   'IMU': [2, 3, 3],
                   'IMU V2': [2, 0, 5],
                   'Master': [2, 4, 3],
                   'RED': None,
                   'Servo': [2, 3, 2],
                   'Stepper': [2, 3, 3]},
'doc': ['af', {
'en':
"""
Returns the error count for the communication between Brick and Bricklet.

The errors are divided into

* ACK checksum errors,
* message checksum errors,
* framing errors and
* overflow errors.

The errors counts are for errors that occur on the Brick side. All
Bricklets have a similar function that returns the errors on the Bricklet side.
""",
'de':
"""
Gibt die Anzahl der Fehler die während der Kommunikation zwischen Brick und
Bricklet aufgetreten sind zurück.

Die Fehler sind aufgeteilt in

* ACK-Checksummen Fehler,
* Message-Checksummen Fehler,
* Framing Fehler und
* Overflow Fehler.

Die Fehlerzähler sind für Fehler die auf der Seite des Bricks auftreten.
Jedes Bricklet hat eine ähnliche Funktion welche die Fehler auf Brickletseite
ausgibt.
"""
}]
})
common_packets.append({
'feature': 'status_led',
'type': 'function',
'function_id': 238,
'name': 'Enable Status LED',
'elements': [],
'since_firmware': {'*': [2, 0, 0],
                   'DC': [2, 3, 1],
                   'IMU': [2, 3, 1],
                   'Master': [2, 3, 2],
                   'RED': None,
                   'Servo': [2, 3, 1],
                   'Stepper': [2, 3, 1]},
'doc': ['af', {
'en':
"""
Enables the status LED.

The status LED is the blue LED next to the USB connector. If enabled is is
on and it flickers if data is transfered. If disabled it is always off.

The default state is enabled.
""",
'de':
"""
Aktiviert die Status LED.

Die Status LED ist die blaue LED neben dem USB-Stecker. Wenn diese aktiviert
ist, ist sie an und sie flackert wenn Daten transferiert werden. Wenn sie
deaktiviert ist, ist sie immer aus.

Der Standardzustand ist aktiviert.
"""
}]
})

common_packets.append({
'feature': 'status_led',
'type': 'function',
'function_id': 239,
'name': 'Disable Status LED',
'elements': [],
'since_firmware': {'*': [2, 0, 0],
                   'DC': [2, 3, 1],
                   'IMU': [2, 3, 1],
                   'Master': [2, 3, 2],
                   'RED': None,
                   'Servo': [2, 3, 1],
                   'Stepper': [2, 3, 1]},
'doc': ['af', {
'en':
"""
Disables the status LED.

The status LED is the blue LED next to the USB connector. If enabled is is
on and it flickers if data is transfered. If disabled it is always off.

The default state is enabled.
""",
'de':
"""
Deaktiviert die Status LED.

Die Status LED ist die blaue LED neben dem USB-Stecker. Wenn diese aktiviert
ist, ist sie an und sie flackert wenn Daten transferiert werden. Wenn sie
deaktiviert ist, ist sie immer aus.

Der Standardzustand ist aktiviert.
"""
}]
})

common_packets.append({
'feature': 'status_led',
'type': 'function',
'function_id': 240,
'name': 'Is Status LED Enabled',
'elements': [('Enabled', 'bool', 1, 'out')],
'since_firmware': {'*': [2, 0, 0],
                   'DC': [2, 3, 1],
                   'IMU': [2, 3, 1],
                   'Master': [2, 3, 2],
                   'RED': None,
                   'Servo': [2, 3, 1],
                   'Stepper': [2, 3, 1]},
'doc': ['af', {
'en':
"""
Returns *true* if the status LED is enabled, *false* otherwise.
""",
'de':
"""
Gibt *true* zurück wenn die Status LED aktiviert ist, *false* sonst.
"""
}]
})

common_packets.append({
'feature': 'bricklet_eeprom',
'type': 'function',
'function_id': 241,
'name': 'Get Protocol1 Bricklet Name',
'elements': [('Port', 'char', 1, 'in'),
             ('Protocol Version', 'uint8', 1, 'out'),
             ('Firmware Version', 'uint8', 3, 'out'),
             ('Name', 'string', 40, 'out')],
'since_firmware': {'*': [2, 0, 0],
                   'DC': [2, 0, 0],
                   'IMU': [2, 0, 0],
                   'Master': [2, 0, 0],
                   'RED': None,
                   'Servo': [2, 0, 0],
                   'Stepper': [2, 0, 0]},
'doc': ['af', {
'en':
"""
Returns the firmware and protocol version and the name of the Bricklet for a
given port.

This functions sole purpose is to allow automatic flashing of v1.x.y Bricklet
plugins.
""",
'de':
"""
Gibt die Firmware und Protokoll Version und den Namen des Bricklets für einen
gegebenen Port zurück.

Der einzige Zweck dieser Funktion ist es, automatischen Flashen von Bricklet
v1.x.y Plugins zu ermöglichen.
"""
}]
})

common_packets.append({
'feature': 'chip_temperature',
'type': 'function',
'function_id': 242,
'name': 'Get Chip Temperature',
'elements': [('Temperature', 'int16', 1, 'out')],
'since_firmware': {'*': [2, 0, 0],
                   'DC': [1, 1, 3],
                   'IMU': [1, 0, 7],
                   'Master': [1, 2, 1],
                   'RED': None,
                   'Servo': [1, 1, 3],
                   'Stepper': [1, 1, 4]},
'doc': ['af', {
'en':
"""
Returns the temperature in °C/10 as measured inside the microcontroller. The
value returned is not the ambient temperature!

The temperature is only proportional to the real temperature and it has an
accuracy of +-15%. Practically it is only useful as an indicator for
temperature changes.
""",
'de':
"""
Gibt die Temperatur in °C/10, gemessen im Mikrocontroller, aus. Der
Rückgabewert ist nicht die Umgebungstemperatur.

Die Temperatur ist lediglich proportional zur echten Temperatur und hat eine
Genauigkeit von +-15%. Daher beschränkt sich der praktische Nutzen auf die
Indikation von Temperaturveränderungen.
"""
}]
})

common_packets.append({
'type': 'function',
'function_id': 243,
'name': 'Reset',
'elements': [],
'since_firmware': {'*': [2, 0, 0],
                   'DC': [1, 1, 3],
                   'IMU': [1, 0, 7],
                   'Master': [1, 2, 1],
                   'RED': None,
                   'Servo': [1, 1, 3],
                   'Stepper': [1, 1, 4]},
'doc': ['af', {
'en':
"""
Calling this function will reset the Brick. Calling this function
on a Brick inside of a stack will reset the whole stack.

After a reset you have to create new device objects,
calling functions on the existing ones will result in
undefined behavior!
""",
'de':
"""
Ein Aufruf dieser Funktion setzt den Brick zurück. Befindet sich der Brick
innerhalb eines Stapels wird der gesamte Stapel zurück gesetzt.

Nach dem Zurücksetzen ist es notwendig neue Geräteobjekte zu erzeugen,
Funktionsaufrufe auf bestehende führt zu undefiniertem Verhalten.
"""
}]
})

common_packets.append({
'type': 'function',
'function_id': 255,
'name': 'Get Identity',
'elements': [('Uid', 'string', 8, 'out'),
             ('Connected Uid', 'string', 8, 'out'),
             ('Position', 'char', 1, 'out'),
             ('Hardware Version', 'uint8', 3, 'out'),
             ('Firmware Version', 'uint8', 3, 'out'),
             ('Device Identifier', 'uint16', 1, 'out')],
'since_firmware': {'*': [2, 0, 0]},
'prototype_in_device': True,
'doc': ['af', {
'en':
"""
Returns the UID, the UID where the Brick is connected to,
the position, the hardware and firmware version as well as the
device identifier.

The position can be '0'-'8' (stack position).

The device identifier numbers can be found :ref:`here <device_identifier>`.
|device_identifier_constant|
""",
'de':
"""
Gibt die UID, die UID zu der der Brick verbunden ist, die
Position, die Hard- und Firmware Version sowie den Device Identifier
zurück.

Die Position kann '0'-'8' (Stack Position) sein.

Eine Liste der Device Identifier Werte ist :ref:`hier <device_identifier>` zu
finden. |device_identifier_constant|
"""
}]
})
