# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Common Bricklet communication config

common_packets = []

common_packets.append({
'type': 'function',
'function_id': 234,
'name': 'Get SPITFP Error Count',
'elements': [('Error Count Ack Checksum', 'uint32', 1, 'out'),
             ('Error Count Message Checksum', 'uint32', 1, 'out'),
             ('Error Count Frame', 'uint32', 1, 'out'),
             ('Error Count Overflow', 'uint32', 1, 'out')],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['af', {
'en':
"""
Returns the error count for the communication between Brick and Bricklet.

The errors are divided into

* ack checksum errors,
* message checksum errors,
* frameing errors and
* overflow errors.

The errors counts are for errors that occur on the Bricklet side. All
Bricks have a similar function that returns the errors on the Brick side.
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

Die Fehlerzähler sind für Fehler die auf der Seite des Bricklets auftreten.
Jedes Bricklet hat eine ähnliche Funktion welche die Fehler auf Brickseite
ausgibt.
"""
}]
})

common_packets.append({
'type': 'function',
'function_id': 235,
'name': 'Set Bootloader Mode',
'elements': [('Mode', 'uint8', 1, 'in', ('Bootloader Mode', [('Bootloader', 0),
                                                             ('Firmware', 1),
                                                             ('Bootloader Wait For Reboot', 2),
                                                             ('Firmware Wait For Reboot', 3),
                                                             ('Firmware Wait For Erase And Reboot', 4)])),
             ('Status', 'uint8', 1, 'out', ('Bootloader Status', [('OK', 0),
                                                                  ('Invalid Mode', 1),
                                                                  ('No Change', 2),
                                                                  ('Entry Function Not Present', 3),
                                                                  ('Device Identifier Incorrect', 4),
                                                                  ('CRC Mismatch', 5)]))],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['af', {
'en':
"""
Sets the bootloader mode and returns the status after the requested
mode change was instigated.

You can change from bootloader mode to firmware mode and vice versa. A change
from bootloader mode to firmware mode will only take place if the entry function,
device identifier und crc are present and correct.

This function is used by Brick Viewer during flashing. It should not be
necessary to call it in a normal user program.
""",
'de':
"""
Setzt den Bootloader-Modus und gibt den Status zurück nachdem die 
Modusänderungsanfrage bearbeitet wurde.

Mit dieser Funktion ist es möglich vom Bootloader- in den Firmware-Modus zu
wechseln und umgekehrt. Ein Welchsel vom Bootlodaer- in der den Firmware-Modus
ist nur möglich wenn Entry-Funktion, Device Identifier und CRC vorhanden und
korrekt sind.

Diese Funktion wird vom Brick Viewer während des flashens benutzt. In einem
normalem Nutzerprogramm sollte diese Funktion nicht benötigt werden.
"""
}]
})

common_packets.append({
'type': 'function',
'function_id': 236,
'name': 'Get Bootloader Mode',
'elements': [('Mode', 'uint8', 1, 'out', ('Bootloader Mode', [('Bootloader', 0),
                                                              ('Firmware', 1),
                                                              ('Bootloader Wait For Reboot', 2),
                                                              ('Firmware Wait For Reboot', 3),
                                                              ('Firmware Wait For Erase And Reboot', 4)]))],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['af', {
'en':
"""
Returns the current bootloader mode, see :func:`SetBootloaderMode`.
""",
'de':
"""
Gibt den aktuellen Bootloader-Modus zurück, siehe :func:`SetBootloaderMode`.
"""
}]
})


common_packets.append({
'type': 'function',
'function_id': 237,
'name': 'Set Write Firmware Pointer',
'elements': [('Pointer', 'uint32', 1, 'in')],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['af', {
'en':
"""
Sets the firmware pointer for func:`WriteFirmware`. The pointer has
to be increased by chunks of size 64. The data is written to flash
every 4 chunks (which equals to one page of size 256).

This function is used by Brick Viewer during flashing. It should not be
necessary to call it in a normal user program.
""",
'de':
"""
Setzt den Firmware-Pointer für func:`WriteFirmware`. Der Pointer
muss um je 64 Byte erhöht werden. Die Daten werden alle 4 Datenblöcke
in den Flash geschrieben (4 Datenblöcke entsprechen einer Page mit 256 Byte).

Diese Funktion wird vom Brick Viewer während des flashens benutzt. In einem
normalem Nutzerprogramm sollte diese Funktion nicht benötigt werden.
"""
}]
})



common_packets.append({
'type': 'function',
'function_id': 238,
'name': 'Write Firmware',
'elements': [('Data', 'uint8', 64, 'in'),
             ('Status', 'uint8', 1, 'out')],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['af', {
'en':
"""
Writes 64 Bytes of firmware at the position as written by 
:func:`SetWriteFirmwarePointer` before. The firmware is written
to flash every 4 chunks.

You can only write firmware in bootloader mode.

This function is used by Brick Viewer during flashing. It should not be
necessary to call it in a normal user program.
""",
'de':
"""
Schreibt 64 Bytes Firmware an die Position die vorher von
:func:`SetWriteFirmwarePointer` gesetzt wurde. Die Firmware wird
alle 4 Datenblöcke in den Flash geschrieben.

Eine Firmware kann nur im Bootloader-Mode geschrieben werden.

Diese Funktion wird vom Brick Viewer während des flashens benutzt. In einem
normalem Nutzerprogramm sollte diese Funktion nicht benötigt werden.
"""
}]
})


common_packets.append({
'type': 'function',
'function_id': 239,
'name': 'Set Status LED Config',
'elements': [('Config', 'uint8', 1, 'in', ('Status LED Config', [('Off', 0),
                                                                 ('On', 1),
                                                                 ('Show Status', 2),
                                                                 ('Show Heartbeat', 3)]))],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['af', {
'en':
"""
Sets the status LED configuration. By default the LED shows
communication traffic between Brick and Bricklet, it flickers once 
for every 10 received data packets.

You can also turn the LED permanently on/off or show a heartbeat.

If the Bricklet is in bootloader mode, the LED is will show heartbeat by default.
""",
'de':
"""
Setzt die Konfiguration der Status-LED. Standardmäßig zeigt
die LED die Kommunikationsdatenmenge an. Sie blinkt einmal auf pro 10 empfangenen
Datenpaketen zwischen Brick und Bricklet.

Die LED kann auch permanaent an/aus gestellt werden oder einen Herzschlag anzeigen.

Wenn das Bricklet sich im Bootlodermodus befindet ist die LED aus.
"""
}]
})

common_packets.append({
'type': 'function',
'function_id': 240,
'name': 'Get Status LED Config',
'elements': [('Config', 'uint8', 1, 'out', ('Status LED Config', [('Off', 0),
                                                                  ('On', 1),
                                                                  ('Show Status', 2),
                                                                  ('Show Heartbeat', 3)]))],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`SetStatusLEDConfig`
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`SetStatusLEDConfig` gesetzt.
"""
}]
})

common_packets.append({
'type': 'function',
'function_id': 242,
'name': 'Get Chip Temperature',
'elements': [('Temperature', 'int16', 1, 'out')],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['af', {
'en':
"""
Returns the temperature in °C as measured inside the microcontroller. The
value returned is not the ambient temperature!

The temperature is only proportional to the real temperature and it has bad
accuracy. Practically it is only useful as an indicator for
temperature changes.
""",
'de':
"""
Gibt die Temperatur in °C, gemessen im Mikrocontroller, aus. Der
Rückgabewert ist nicht die Umgebungstemperatur.

Die Temperatur ist lediglich proportional zur echten Temperatur und hat eine
hohe Ungenauigkeit. Daher beschränkt sich der praktische Nutzen auf die
Indikation von Temperaturveränderungen.
"""
}]
})


common_packets.append({
'type': 'function',
'function_id': 243,
'name': 'Reset',
'elements': [],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['af', {
'en':
"""
Calling this function will reset the Bricklet. All configurations
will be lost.

After a reset you have to create new device objects,
calling functions on the existing ones will result in
undefined behavior!
""",
'de':
"""
Ein Aufruf dieser Funktion setzt das Bricklet zurück. Nach einem
neustart sind alle Konfiguration verloren.

Nach dem Zurücksetzen ist es notwendig neue Objekte zu erzeugen,
Funktionsaufrufe auf bestehende führt zu undefiniertem Verhalten.
"""
}]
})

common_packets.append({
'type': 'function',
'function_id': 248,
'name': 'Write UID',
'elements': [('UID', 'uint32', 1, 'in')],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['af', {
'en':
"""
Writes a new UID into flash. If you want to set a new UID
you have to decode the Base58 encoded UID string into an
integer first.

We recommend that you use Brick Viewer to change the UID.
""",
'de':
"""
Schreibt eine neue UID in den Flash. Die UID muss zuerst
vom Base58 encodierten String in einen Integer decodiert
werden.

Wir empfehlen die Nutzung des Brick Viewers zum ändern
der UID.
"""
}]
})

common_packets.append({
'type': 'function',
'function_id': 249,
'name': 'Read UID',
'elements': [('UID', 'uint32', 1, 'out')],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['af', {
'en':
"""
Returns the current UID as an integer. Encode as
Base58 to get the usual string version.
""",
'de':
"""
Gibt die aktuelle UID als Integer zurück. Dieser Integer
kann als Base58 encodiert werden um an den üblichen
UID-String zu gelangen.
"""
}]
})
