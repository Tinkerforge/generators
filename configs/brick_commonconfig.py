# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Common Brick communication config

common_packets = []
'''
common_packets.append({
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
interference (see :func:`GetSPITFPErrorCount`) you can decrease the baudrate.

Regulatory testing is done with the default baudrate. If CE compatability
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
(siehe :func:`GetSPITFPErrorCount`) kann die Baudrate verringert werden.

EMV Tests werden mit der Standardbaudrate durchgeführt. Falls eine
CE-Kompatibilität o.ä. in der Anwendung notwendig ist empfehlen wir die Baudrate
nicht zu ändern.

Die Standardbaudrate für alle Ports ist 1400000.
"""
}]
})

common_packets.append({
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
Returns the baudrate for a given Bricklet port, see :func:`SetSPITFPBaudrate`.
""",
'de':
"""
Gibt die Baudrate für einen Bricklet Port zurück, siehe :func:`SetSPITFPBaudrate`.
"""
}]
})

# Keep function 236 empty, so we can always call "get_bootloader_mode"

common_packets.append({
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
* frameing errors and
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
'''
common_packets.append({
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
