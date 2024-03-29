# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Common Device communication config

from copy import deepcopy

common_constant_groups = []

common_constant_groups.append({
'feature': 'send_timeout_count',
'name': 'Communication Method',
'type': 'uint8',
'constants': [('None', 0),
              ('USB', 1),
              ('SPI Stack', 2),
              ('Chibi', 3),
              ('RS485', 4),
              ('WIFI', 5),
              ('Ethernet', 6),
              ('WIFI V2', 7)]
})

common_constant_groups.append({
'feature': 'comcu_bricklet',
'name': 'Bootloader Mode',
'type': 'uint8',
'constants': [('Bootloader', 0),
              ('Firmware', 1),
              ('Bootloader Wait For Reboot', 2),
              ('Firmware Wait For Reboot', 3),
              ('Firmware Wait For Erase And Reboot', 4)]
})

common_constant_groups.append({
'feature': 'comcu_bricklet',
'name': 'Bootloader Status',
'type': 'uint8',
'constants': [('OK', 0),
              ('Invalid Mode', 1),
              ('No Change', 2),
              ('Entry Function Not Present', 3),
              ('Device Identifier Incorrect', 4),
              ('CRC Mismatch', 5)]
})

common_constant_groups.append({
'feature': 'comcu_bricklet',
'name': 'Status LED Config',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Show Heartbeat', 2),
              ('Show Status', 3)]
})

common_constant_groups.append({
'feature': 'tng',
'name': 'Copy Status',
'type': 'uint8',
'constants': [('OK', 0),
              ('Device Identifier Incorrect', 1),
              ('Magic Number Incorrect', 2),
              ('Length Malformed', 3),
              ('CRC Mismatch', 4)]
})

common_packets = []

common_packets.append({
'is_virtual': True, # function without a corresponding TCP/IP packet
'feature': 'device',
'type': 'function',
'function_id': -1,
'name': 'Get API Version',
'elements': [('API Version', 'uint8', 3, 'out', [{'name': 'Major'}, {'name': 'Minor'}, {'name': 'Revision'}])],
'since_firmware': None,
'doc': ['vf', {
'en':
"""
Returns the version of the API definition implemented
by this API bindings. This is neither the release version of this API bindings
nor does it tell you anything about the represented Brick or Bricklet.
""",
'de':
"""
Gibt die Version der API Definition zurück, die diese
API Bindings implementieren. Dies ist weder die Release-Version dieser API
Bindings noch gibt es in irgendeiner Weise Auskunft über den oder das
repräsentierte(n) Brick oder Bricklet.
"""
}]
})

common_packets.append({
'is_virtual': True, # function without a corresponding TCP/IP packet
'feature': 'device',
'type': 'function',
'function_id': -1,
'name': 'Get Response Expected',
'elements': [('Function Id', 'uint8', 1, 'in', {'constant_group': 'Function'}),
             ('Response Expected', 'bool', 1, 'out', {})],
'since_firmware': None,
'doc': ['vf', {
'en':
"""
Returns the response expected flag for the function specified by the function
ID parameter. It is *true* if the function is expected to send a response,
*false* otherwise.

For getter functions this is enabled by default and cannot be disabled,
because those functions will always send a response. For callback configuration
functions it is enabled by default too, but can be disabled by
:func:`Set Response Expected`. For setter functions it is disabled by default
and can be enabled.

Enabling the response expected flag for a setter function allows to detect
timeouts and other error conditions calls of this setter as well. The
device will then send a response for this purpose. If this flag is disabled for
a setter function then no response is sent and errors are silently ignored,
because they cannot be detected.
""",
'de':
"""
Gibt das Response-Expected-Flag für die Funktion mit der angegebenen Funktions
IDs zurück. Es ist *true* falls für die Funktion beim Aufruf eine Antwort
erwartet wird, *false* andernfalls.

Für Getter-Funktionen ist diese Flag immer gesetzt und kann nicht entfernt
werden, da diese Funktionen immer eine Antwort senden. Für
Konfigurationsfunktionen für Callbacks ist es standardmäßig gesetzt, kann aber
entfernt werden mittels :func:`Set Response Expected`. Für Setter-Funktionen ist
es standardmäßig nicht gesetzt, kann aber gesetzt werden.

Wenn das Response-Expected-Flag für eine Setter-Funktion gesetzt ist, können
Timeouts und andere Fehlerfälle auch für Aufrufe dieser Setter-Funktion
detektiert werden. Das Gerät sendet dann eine Antwort extra für diesen Zweck.
Wenn das Flag für eine Setter-Funktion nicht gesetzt ist, dann wird keine
Antwort vom Gerät gesendet und Fehler werden stillschweigend ignoriert, da sie
nicht detektiert werden können.
"""
}]
})

common_packets.append({
'is_virtual': True, # function without a corresponding TCP/IP packet
'feature': 'device',
'type': 'function',
'function_id': -1,
'name': 'Set Response Expected',
'elements': [('Function Id', 'uint8', 1, 'in', {'constant_group': 'Function'}),
             ('Response Expected', 'bool', 1, 'in', {})],
'since_firmware': None,
'doc': ['vf', {
'en':
"""
Changes the response expected flag of the function specified by the
function ID parameter. This flag can only be changed for setter (default value:
*false*) and callback configuration functions (default value: *true*). For
getter functions it is always enabled.

Enabling the response expected flag for a setter function allows to detect
timeouts and other error conditions calls of this setter as well. The
device will then send a response for this purpose. If this flag is disabled for
a setter function then no response is sent and errors are silently ignored,
because they cannot be detected.
""",
'de':
"""
Ändert das Response-Expected-Flag für die Funktion mit der angegebenen Funktion
IDs. Diese Flag kann nur für Setter-Funktionen (Standardwert: *false*) und
Konfigurationsfunktionen für Callbacks (Standardwert: *true*) geändert werden.
Für Getter-Funktionen ist das Flag immer gesetzt.

Wenn das Response-Expected-Flag für eine Setter-Funktion gesetzt ist, können
Timeouts und andere Fehlerfälle auch für Aufrufe dieser Setter-Funktion
detektiert werden. Das Gerät sendet dann eine Antwort extra für diesen Zweck.
Wenn das Flag für eine Setter-Funktion nicht gesetzt ist, dann wird keine
Antwort vom Gerät gesendet und Fehler werden stillschweigend ignoriert, da sie
nicht detektiert werden können.
"""
}]
})

common_packets.append({
'is_virtual': True, # function without a corresponding TCP/IP packet
'feature': 'device',
'type': 'function',
'function_id': -1,
'name': 'Set Response Expected All',
'elements': [('Response Expected', 'bool', 1, 'in', {})],
'since_firmware': None,
'doc': ['vf', {
'en':
"""
Changes the response expected flag for all setter and callback configuration
functions of this device at once.
""",
'de':
"""
Ändert das Response-Expected-Flag für alle Setter-Funktionen und
Konfigurationsfunktionen für Callbacks diese Gerätes.
"""
}]
})

common_packets.append({
'feature': 'comcu_bricklet_host',
'type': 'function',
'function_id': 231,
'name': 'Set SPITFP Baudrate Config',
'elements': [('Enable Dynamic Baudrate', 'bool', 1, 'in', {'default': True}),
             ('Minimum Dynamic Baudrate', 'uint32', 1, 'in', {'unit': 'Baud', 'range': (400000, 2000000), 'default': 400000})],
'since_firmware': {'*': [2, 0, 0],
                   'DC': [2, 3, 5],
                   'IMU': [2, 3, 5],
                   'IMU V2': [2, 0, 10],
                   'Master': [2, 4, 6],
                   'Servo': [2, 3, 4],
                   'Silent Stepper': [2, 0, 4],
                   'Stepper': [2, 3, 6]},
'doc': ['af', {
'en':
"""
The SPITF protocol can be used with a dynamic baudrate. If the dynamic baudrate is
enabled, the Brick will try to adapt the baudrate for the communication
between Bricks and Bricklets according to the amount of data that is transferred.

The baudrate will be increased exponentially if lots of data is sent/received and
decreased linearly if little data is sent/received.

This lowers the baudrate in applications where little data is transferred (e.g.
a weather station) and increases the robustness. If there is lots of data to transfer
(e.g. Thermal Imaging Bricklet) it automatically increases the baudrate as needed.

In cases where some data has to transferred as fast as possible every few seconds
(e.g. RS485 Bricklet with a high baudrate but small payload) you may want to turn
the dynamic baudrate off to get the highest possible performance.

The maximum value of the baudrate can be set per port with the function
:func:`Set SPITFP Baudrate`. If the dynamic baudrate is disabled, the baudrate
as set by :func:`Set SPITFP Baudrate` will be used statically.
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
"""
}]
})

common_packets.append({
'feature': 'comcu_bricklet_host',
'type': 'function',
'function_id': 232,
'name': 'Get SPITFP Baudrate Config',
'elements': [('Enable Dynamic Baudrate', 'bool', 1, 'out', {'default': True}),
             ('Minimum Dynamic Baudrate', 'uint32', 1, 'out', {'unit': 'Baud', 'range': (400000, 2000000), 'default': 400000})],
'since_firmware': {'*': [2, 0, 0],
                   'DC': [2, 3, 5],
                   'IMU': [2, 3, 5],
                   'IMU V2': [2, 0, 10],
                   'Master': [2, 4, 6],
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
'elements': [('Communication Method', 'uint8', 1, 'in', {'constant_group': 'Communication Method'}),
             ('Timeout Count', 'uint32', 1, 'out', {})],
'since_firmware': {'*': [2, 0, 0],
                   'DC': [2, 3, 3],
                   'IMU': [2, 3, 3],
                   'IMU V2': [2, 0, 7],
                   'Master': [2, 4, 3],
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

set_spitfp_baudrate = {
    'feature': 'comcu_bricklet_host',
    'type': 'function',
    'function_id': 234,
    'name': 'Set SPITFP Baudrate',
    'elements': [('Bricklet Port', 'char', 1, 'in', {}),
                 ('Baudrate', 'uint32', 1, 'in', {'unit': 'Baud', 'range': (400000, 2000000), 'default': 1400000})],
    'since_firmware': {'*': [2, 0, 0],
                       'DC': [2, 3, 3],
                       'IMU': [2, 3, 3],
                       'IMU V2': [2, 0, 5],
                       'Master': [2, 4, 3],
                       'Servo': [2, 3, 2],
                       'Stepper': [2, 3, 3]},
    'doc': ['af', {
    'en':
    """
Sets the baudrate for a specific Bricklet port.

If you want to increase the throughput of Bricklets you can increase
the baudrate. If you get a high error count because of high
interference (see :func:`Get SPITFP Error Count`) you can decrease the
baudrate.

If the dynamic baudrate feature is enabled, the baudrate set by this
function corresponds to the maximum baudrate (see :func:`Set SPITFP Baudrate Config`).

Regulatory testing is done with the default baudrate. If CE compatibility
or similar is necessary in your applications we recommend to not change
the baudrate.
""",
    'de':
    """
Setzt die Baudrate eines spezifischen Bricklet Ports .

Für einen höheren Durchsatz der Bricklets kann die Baudrate erhöht werden.
Wenn der Fehlerzähler auf Grund von lokaler Störeinstrahlung hoch ist
(siehe :func:`Get SPITFP Error Count`) kann die Baudrate verringert werden.

Wenn das Feature der dynamische Baudrate aktiviert ist, setzt diese Funktion
die maximale Baudrate (siehe :func:`Set SPITFP Baudrate Config`).

EMV Tests werden mit der Standardbaudrate durchgeführt. Falls eine
CE-Kompatibilität o.ä. in der Anwendung notwendig ist empfehlen wir die
Baudrate nicht zu ändern.
"""
    }]
}

get_spitfp_baudrate = {
    'feature': 'comcu_bricklet_host',
    'type': 'function',
    'function_id': 235,
    'name': 'Get SPITFP Baudrate',
    'elements': [('Bricklet Port', 'char', 1, 'in', {}),
                 ('Baudrate', 'uint32', 1, 'out', {'unit': 'Baud', 'range': (400000, 2000000), 'default': 1400000})],
    'since_firmware': {'*': [2, 0, 0],
                       'DC': [2, 3, 3],
                       'IMU': [2, 3, 3],
                       'IMU V2': [2, 0, 5],
                       'Master': [2, 4, 3],
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
}

get_spitfp_error_count = {
    'feature': 'comcu_bricklet_host',
    'type': 'function',
    'function_id': 237,
    'name': 'Get SPITFP Error Count',
    'elements': [('Bricklet Port', 'char', 1, 'in', {}),
                 ('Error Count ACK Checksum', 'uint32', 1, 'out', {}),
                 ('Error Count Message Checksum', 'uint32', 1, 'out', {}),
                 ('Error Count Frame', 'uint32', 1, 'out', {}),
                 ('Error Count Overflow', 'uint32', 1, 'out', {})],
    'since_firmware': {'*': [2, 0, 0],
                       'DC': [2, 3, 3],
                       'IMU': [2, 3, 3],
                       'IMU V2': [2, 0, 5],
                       'Master': [2, 4, 3],
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
}

get_protocol1_bricklet_name = {
'feature': 'eeprom_bricklet_host',
'type': 'function',
'function_id': 241,
'name': 'Get Protocol1 Bricklet Name',
'elements': [('Port', 'char', 1, 'in', {}),
             ('Protocol Version', 'uint8', 1, 'out', {}),
             ('Firmware Version', 'uint8', 3, 'out', [{'name': 'Major'}, {'name': 'Minor'}, {'name': 'Revision'}]),
             ('Name', 'string', 40, 'out', {})],
'since_firmware': {'*': [2, 0, 0],
                   'DC': [2, 0, 0],
                   'IMU': [2, 0, 0],
                   'Master': [2, 0, 0],
                   'Servo': [2, 0, 0],
                   'Stepper': [2, 0, 0]},
'doc': ['if', {
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
}

write_bricklet_plugin = {
'feature': 'eeprom_bricklet_host',
'type': 'function',
'function_id': 246,
'name': 'Write Bricklet Plugin',
'elements': [('Port', 'char', 1, 'in', {}),
             ('Offset', 'uint8', 1, 'in', {}),
             ('Chunk', 'uint8', 32, 'in', {})],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['if', {
'en':
"""
Writes 32 bytes of firmware to the bricklet attached at the given port.
The bytes are written to the position offset * 32.

This function is used by Brick Viewer during flashing. It should not be
necessary to call it in a normal user program.
""",
'de':
"""
Schreibt 32 Bytes Firmware auf das Bricklet, dass am gegebenen Port angeschlossen ist.
Die Bytes werden an die Position offset * 32 geschrieben.

Diese Funktion wird vom Brick Viewer während des Flashens benutzt. In einem
normalem Nutzerprogramm sollte diese Funktion nicht benötigt werden.
"""
}]
}

read_bricklet_plugin = {
'feature': 'eeprom_bricklet_host',
'type': 'function',
'function_id': 247,
'name': 'Read Bricklet Plugin',
'elements': [('Port', 'char', 1, 'in', {}),
             ('Offset', 'uint8', 1, 'in', {}),
             ('Chunk', 'uint8', 32, 'out', {})],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['if', {
'en':
"""
Reads 32 bytes of firmware from the bricklet attached at the given port.
The bytes are read starting at the position offset * 32.

This function is used by Brick Viewer during flashing. It should not be
necessary to call it in a normal user program.
""",
'de':
"""
Liest 32 Bytes Firmware vom Bricklet, dass am gegebenen Port angeschlossen ist.
Die Bytes werden ab der Position offset * 32 gelesen.

Diese Funktion wird vom Brick Viewer während des Flashens benutzt. In einem
normalem Nutzerprogramm sollte diese Funktion nicht benötigt werden.
"""
}]
}

for i in [2, 4]:
    for blueprint in [set_spitfp_baudrate,
                      get_spitfp_baudrate,
                      get_spitfp_error_count,
                      get_protocol1_bricklet_name,
                      write_bricklet_plugin,
                      read_bricklet_plugin]:
        pkt = deepcopy(blueprint)
        pkt['feature'] += '_{}_ports'.format(i)
        pkt['elements'][0][4]['range'] = ('a', chr(ord('a') + i - 1))

        common_packets.append(pkt)

common_packets.append({
'feature': 'comcu_bricklet',
'type': 'function',
'function_id': 234,
'name': 'Get SPITFP Error Count',
'elements': [('Error Count Ack Checksum', 'uint32', 1, 'out', {}),
             ('Error Count Message Checksum', 'uint32', 1, 'out', {}),
             ('Error Count Frame', 'uint32', 1, 'out', {}),
             ('Error Count Overflow', 'uint32', 1, 'out', {})],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['af', {
'en':
"""
Returns the error count for the communication between Brick and Bricklet.

The errors are divided into

* ACK checksum errors,
* message checksum errors,
* framing errors and
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
Jedes Brick hat eine ähnliche Funktion welche die Fehler auf Brickseite
ausgibt.
"""
}]
})

common_packets.append({
'feature': 'tng',
'type': 'function',
'function_id': 234,
'name': 'Get Timestamp',
'elements': [('Timestamp', 'uint64', 1, 'out', {'scale': (1, 10**6), 'unit': 'Second'})],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['af', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

common_packets.append({
'feature': 'comcu_bricklet',
'type': 'function',
'function_id': 235,
'name': 'Set Bootloader Mode',
'elements': [('Mode', 'uint8', 1, 'in', {'constant_group': 'Bootloader Mode'}),
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Bootloader Status'})],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['if', {
'en':
"""
Sets the bootloader mode and returns the status after the requested
mode change was instigated.

You can change from bootloader mode to firmware mode and vice versa. A change
from bootloader mode to firmware mode will only take place if the entry function,
device identifier and CRC are present and correct.

This function is used by Brick Viewer during flashing. It should not be
necessary to call it in a normal user program.
""",
'de':
"""
Setzt den Bootloader-Modus und gibt den Status zurück nachdem die
Modusänderungsanfrage bearbeitet wurde.

Mit dieser Funktion ist es möglich vom Bootloader- in den Firmware-Modus zu
wechseln und umgekehrt. Ein Welchsel vom Bootloader- in der den Firmware-Modus
ist nur möglich wenn Entry-Funktion, Device Identifier und CRC vorhanden und
korrekt sind.

Diese Funktion wird vom Brick Viewer während des Flashens benutzt. In einem
normalem Nutzerprogramm sollte diese Funktion nicht benötigt werden.
"""
}]
})

common_packets.append({
'feature': 'tng',
'type': 'function',
'function_id': 235,
'name': 'Copy Firmware',
'elements': [('Status', 'uint8', 1, 'out', {'constant_group': 'Copy Status'})],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['if', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

# function 236 must never be used for anything else than "Get Bootloader Mode"
# to allow for calling function 236 without knowing anything about the device
# and either calling "Get Bootloader Mode" or getting a non-supported error.
common_packets.append({
'feature': 'comcu_bricklet',
'type': 'function',
'function_id': 236,
'name': 'Get Bootloader Mode',
'elements': [('Mode', 'uint8', 1, 'out', {'constant_group': 'Bootloader Mode'})],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['if', {
'en':
"""
Returns the current bootloader mode, see :func:`Set Bootloader Mode`.
""",
'de':
"""
Gibt den aktuellen Bootloader-Modus zurück, siehe :func:`Set Bootloader Mode`.
"""
}]
})

common_packets.append({
'feature': 'tng',
'type': 'function',
'function_id': 237,
'name': 'Set Write Firmware Pointer',
'elements': [('Pointer', 'uint32', 1, 'in', {'unit': 'Byte'})],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['if', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

common_packets.append({
'feature': 'comcu_bricklet',
'type': 'function',
'function_id': 237,
'name': 'Set Write Firmware Pointer',
'elements': [('Pointer', 'uint32', 1, 'in', {'unit': 'Byte'})],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['if', {
'en':
"""
Sets the firmware pointer for :func:`Write Firmware`. The pointer has
to be increased by chunks of size 64. The data is written to flash
every 4 chunks (which equals to one page of size 256).

This function is used by Brick Viewer during flashing. It should not be
necessary to call it in a normal user program.
""",
'de':
"""
Setzt den Firmware-Pointer für :func:`Write Firmware`. Der Pointer
muss um je 64 Byte erhöht werden. Die Daten werden alle 4 Datenblöcke
in den Flash geschrieben (4 Datenblöcke entsprechen einer Page mit 256 Byte).

Diese Funktion wird vom Brick Viewer während des Flashens benutzt. In einem
normalem Nutzerprogramm sollte diese Funktion nicht benötigt werden.
"""
}]
})

common_packets.append({
'feature': 'brick_status_led',
'type': 'function',
'function_id': 238,
'name': 'Enable Status LED',
'elements': [],
'since_firmware': {'*': [2, 0, 0],
                   'DC': [2, 3, 1],
                   'IMU': [2, 3, 1],
                   'Master': [2, 3, 2],
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
'feature': 'tng',
'type': 'function',
'function_id': 238,
'name': 'Write Firmware',
'elements': [('Data', 'uint8', 64, 'in', {}),
             ('Status', 'uint8', 1, 'out', {})],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['if', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

common_packets.append({
'feature': 'comcu_bricklet',
'type': 'function',
'function_id': 238,
'name': 'Write Firmware',
'elements': [('Data', 'uint8', 64, 'in', {}),
             ('Status', 'uint8', 1, 'out', {})],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['if', {
'en':
"""
Writes 64 Bytes of firmware at the position as written by
:func:`Set Write Firmware Pointer` before. The firmware is written
to flash every 4 chunks.

You can only write firmware in bootloader mode.

This function is used by Brick Viewer during flashing. It should not be
necessary to call it in a normal user program.
""",
'de':
"""
Schreibt 64 Bytes Firmware an die Position die vorher von
:func:`Set Write Firmware Pointer` gesetzt wurde. Die Firmware wird
alle 4 Datenblöcke in den Flash geschrieben.

Eine Firmware kann nur im Bootloader-Mode geschrieben werden.

Diese Funktion wird vom Brick Viewer während des Flashens benutzt. In einem
normalem Nutzerprogramm sollte diese Funktion nicht benötigt werden.
"""
}]
})

common_packets.append({
'feature': 'brick_status_led',
'type': 'function',
'function_id': 239,
'name': 'Disable Status LED',
'elements': [],
'since_firmware': {'*': [2, 0, 0],
                   'DC': [2, 3, 1],
                   'IMU': [2, 3, 1],
                   'Master': [2, 3, 2],
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
'feature': 'comcu_bricklet',
'type': 'function',
'function_id': 239,
'name': 'Set Status LED Config',
'elements': [('Config', 'uint8', 1, 'in', {'constant_group': 'Status LED Config', 'default': 3})],
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

Die LED kann auch permanent an/aus gestellt werden oder einen Herzschlag anzeigen.

Wenn das Bricklet sich im Bootlodermodus befindet ist die LED aus.
"""
}]
})

common_packets.append({
'feature': 'brick_status_led',
'type': 'function',
'function_id': 240,
'name': 'Is Status LED Enabled',
'elements': [('Enabled', 'bool', 1, 'out', {'default': True})],
'since_firmware': {'*': [2, 0, 0],
                   'DC': [2, 3, 1],
                   'IMU': [2, 3, 1],
                   'Master': [2, 3, 2],
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
'feature': 'comcu_bricklet',
'type': 'function',
'function_id': 240,
'name': 'Get Status LED Config',
'elements': [('Config', 'uint8', 1, 'out', {'constant_group': 'Status LED Config', 'default': 3})],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Status LED Config`
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Status LED Config` gesetzt.
"""
}]
})

common_packets.append({
'feature': 'brick_chip_temperature',
'type': 'function',
'function_id': 242,
'name': 'Get Chip Temperature',
'elements': [('Temperature', 'int16', 1, 'out', {'scale': (1, 10), 'unit': 'Degree Celsius'})],
'since_firmware': {'*': [2, 0, 0],
                   'DC': [1, 1, 3],
                   'IMU': [1, 0, 7],
                   'Master': [1, 2, 1],
                   'Servo': [1, 1, 3],
                   'Stepper': [1, 1, 4]},
'doc': ['af', {
'en':
"""
Returns the temperature as measured inside the microcontroller. The
value returned is not the ambient temperature!

The temperature is only proportional to the real temperature and it has an
accuracy of ±15%. Practically it is only useful as an indicator for
temperature changes.
""",
'de':
"""
Gibt die Temperatur, gemessen im Mikrocontroller, aus. Der
Rückgabewert ist nicht die Umgebungstemperatur.

Die Temperatur ist lediglich proportional zur echten Temperatur und hat eine
Genauigkeit von ±15%. Daher beschränkt sich der praktische Nutzen auf die
Indikation von Temperaturveränderungen.
"""
}]
})

common_packets.append({
'feature': 'comcu_bricklet',
'type': 'function',
'function_id': 242,
'name': 'Get Chip Temperature',
'elements': [('Temperature', 'int16', 1, 'out', {'unit': 'Degree Celsius'})],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['af', {
'en':
"""
Returns the temperature as measured inside the microcontroller. The
value returned is not the ambient temperature!

The temperature is only proportional to the real temperature and it has bad
accuracy. Practically it is only useful as an indicator for
temperature changes.
""",
'de':
"""
Gibt die Temperatur, gemessen im Mikrocontroller, aus. Der
Rückgabewert ist nicht die Umgebungstemperatur.

Die Temperatur ist lediglich proportional zur echten Temperatur und hat eine
hohe Ungenauigkeit. Daher beschränkt sich der praktische Nutzen auf die
Indikation von Temperaturveränderungen.
"""
}]
})

common_packets.append({
'feature': 'brick_reset',
'type': 'function',
'function_id': 243,
'name': 'Reset',
'elements': [],
'since_firmware': {'*': [2, 0, 0],
                   'DC': [1, 1, 3],
                   'IMU': [1, 0, 7],
                   'Master': [1, 2, 1],
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
'feature': 'comcu_bricklet',
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
Neustart sind alle Konfiguration verloren.

Nach dem Zurücksetzen ist es notwendig neue Objekte zu erzeugen,
Funktionsaufrufe auf bestehenden führen zu undefiniertem Verhalten.
"""
}]
})

common_packets.append({
'feature': 'tng',
'type': 'function',
'function_id': 243,
'name': 'Reset',
'elements': [],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['af', {
'en':
"""
Calling this function will reset the TNG module. All configurations
will be lost.

After a reset you have to create new device objects,
calling functions on the existing ones will result in
undefined behavior!
""",
'de':
"""
Ein Aufruf dieser Funktion setzt das TNG-Modul zurück. Nach einem
Neustart sind alle Konfiguration verloren.

Nach dem Zurücksetzen ist es notwendig neue Objekte zu erzeugen,
Funktionsaufrufe auf bestehenden führen zu undefiniertem Verhalten.
"""
}]
})

common_packets.append({
'feature': 'comcu_bricklet',
'type': 'function',
'function_id': 248,
'name': 'Write UID',
'elements': [('UID', 'uint32', 1, 'in', {})],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['if', {
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
'feature': 'tng',
'type': 'function',
'function_id': 248,
'name': 'Write UID',
'elements': [('UID', 'uint32', 1, 'in', {})],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['if', {
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
'feature': 'comcu_bricklet',
'type': 'function',
'function_id': 249,
'name': 'Read UID',
'elements': [('UID', 'uint32', 1, 'out', {})],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['if', {
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

common_packets.append({
'feature': 'tng',
'type': 'function',
'function_id': 249,
'name': 'Read UID',
'elements': [('UID', 'uint32', 1, 'out', {})],
'since_firmware': {'*': [1, 0, 0]},
'doc': ['if', {
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

# function 255 must never be used for anything else than "Get Identity" to allow
# for calling function 255 without knowing anything about the device.
common_packets.append({
'feature': 'tng',
'type': 'function',
'function_id': 255,
'name': 'Get Identity',
'elements': [('Uid', 'string', 8, 'out', {}),
             ('Connected Uid', 'string', 8, 'out', {}),
             ('Position', 'char', 1, 'out', {'range': ('0', '8')}), # TODO: TNG Position?
             ('Hardware Version', 'uint8', 3, 'out', [{'name': 'Major'}, {'name': 'Minor'}, {'name': 'Revision'}]),
             ('Firmware Version', 'uint8', 3, 'out', [{'name': 'Major'}, {'name': 'Minor'}, {'name': 'Revision'}]),
             ('Device Identifier', 'uint16', 1, 'out', {})],
'since_firmware': {'*': [1, 0, 0]},
'prototype_in_device': True,
'doc': ['af', {
'en':
"""
Returns the UID, the UID where the Brick is connected to,
the position, the hardware and firmware version as well as the
device identifier.

The position is the position in the stack from '0' (bottom) to '8' (top).

The device identifier numbers can be found :ref:`here <device_identifier>`.
|device_identifier_constant|
""",
'de':
"""
Gibt die UID, die UID zu der der Brick verbunden ist, die
Position, die Hard- und Firmware Version sowie den Device Identifier
zurück.

Die Position ist die Position im Stack von '0' (unterster Brick) bis '8' (oberster Brick).

Eine Liste der Device Identifier Werte ist :ref:`hier <device_identifier>` zu
finden. |device_identifier_constant|
"""
}]
})

# function 255 must never be used for anything else than "Get Identity" to allow
# for calling function 255 without knowing anything about the device.
common_packets.append({
'feature': 'brick_get_identity',
'type': 'function',
'function_id': 255,
'name': 'Get Identity',
'elements': [('Uid', 'string', 8, 'out', {}),
             ('Connected Uid', 'string', 8, 'out', {}),
             ('Position', 'char', 1, 'out', {'range': ('0', '8')}),
             ('Hardware Version', 'uint8', 3, 'out', [{'name': 'Major'}, {'name': 'Minor'}, {'name': 'Revision'}]),
             ('Firmware Version', 'uint8', 3, 'out', [{'name': 'Major'}, {'name': 'Minor'}, {'name': 'Revision'}]),
             ('Device Identifier', 'uint16', 1, 'out', {})],
'since_firmware': {'*': [1, 0, 0]},
'prototype_in_device': True,
'doc': ['af', {
'en':
"""
Returns the UID, the UID where the Brick is connected to,
the position, the hardware and firmware version as well as the
device identifier.

The position is the position in the stack from '0' (bottom) to '8' (top).

The device identifier numbers can be found :ref:`here <device_identifier>`.
|device_identifier_constant|
""",
'de':
"""
Gibt die UID, die UID zu der der Brick verbunden ist, die
Position, die Hard- und Firmware Version sowie den Device Identifier
zurück.

Die Position ist die Position im Stack von '0' (unterster Brick) bis '8' (oberster Brick).

Eine Liste der Device Identifier Werte ist :ref:`hier <device_identifier>` zu
finden. |device_identifier_constant|
"""
}]
})

# function 255 must never be used for anything else than "Get Identity" to allow
# for calling function 255 without knowing anything about the device.
common_packets.append({
'feature': 'bricklet_get_identity',
'type': 'function',
'function_id': 255,
'name': 'Get Identity',
'elements': [('Uid', 'string', 8, 'out', {}),
             ('Connected Uid', 'string', 8, 'out', {}),
             ('Position', 'char', 1, 'out', {'range': [('a', 'h'), ('z', 'z')]}),
             ('Hardware Version', 'uint8', 3, 'out', [{'name': 'Major'}, {'name': 'Minor'}, {'name': 'Revision'}]),
             ('Firmware Version', 'uint8', 3, 'out', [{'name': 'Major'}, {'name': 'Minor'}, {'name': 'Revision'}]),
             ('Device Identifier', 'uint16', 1, 'out', {})],
'since_firmware': {'*': [1, 0, 0]},
'prototype_in_device': True,
'doc': ['af', {
'en':
"""
Returns the UID, the UID where the Bricklet is connected to,
the position, the hardware and firmware version as well as the
device identifier.

The position can be 'a', 'b', 'c', 'd', 'e', 'f', 'g' or 'h' (Bricklet Port).
A Bricklet connected to an :ref:`Isolator Bricklet <isolator_bricklet>` is always at
position 'z'.

The device identifier numbers can be found :ref:`here <device_identifier>`.
|device_identifier_constant|
""",
'de':
"""
Gibt die UID, die UID zu der das Bricklet verbunden ist, die
Position, die Hard- und Firmware Version sowie den Device Identifier
zurück.

Die Position ist 'a', 'b', 'c', 'd', 'e', 'f', 'g' oder 'h' (Bricklet Anschluss).
Ein Bricklet hinter einem :ref:`Isolator Bricklet <isolator_bricklet>` ist immer an
Position 'z'.

Eine Liste der Device Identifier Werte ist :ref:`hier <device_identifier>` zu
finden. |device_identifier_constant|
"""
}]
})

# function 255 must never be used for anything else than "Get Identity" to allow
# for calling function 255 without knowing anything about the device.
common_packets.append({
'feature': 'hat_get_identity',
'type': 'function',
'function_id': 255,
'name': 'Get Identity',
'elements': [('Uid', 'string', 8, 'out', {}),
             ('Connected Uid', 'string', 8, 'out', {}),
             ('Position', 'char', 1, 'out', {'range': [('i', 'i')]}),
             ('Hardware Version', 'uint8', 3, 'out', [{'name': 'Major'}, {'name': 'Minor'}, {'name': 'Revision'}]),
             ('Firmware Version', 'uint8', 3, 'out', [{'name': 'Major'}, {'name': 'Minor'}, {'name': 'Revision'}]),
             ('Device Identifier', 'uint16', 1, 'out', {})],
'since_firmware': {'*': [1, 0, 0]},
'prototype_in_device': True,
'doc': ['af', {
'en':
"""
Returns the UID, the UID where the HAT is connected to
(typically '0' as the HAT is the root device in the topology),
the position, the hardware and firmware version as well as the
device identifier.

The HAT (Zero) Brick is always at position 'i'.

The device identifier numbers can be found :ref:`here <device_identifier>`.
|device_identifier_constant|
""",
'de':
"""
Gibt die UID, die UID zu der das HAT verbunden ist
(typischerweise '0' da das HAT das Wurzelgerät der Topologie ist), die
Position, die Hard- und Firmware Version sowie den Device Identifier
zurück.

Der HAT (Zero) Brick ist immer an Position 'i'.

Eine Liste der Device Identifier Werte ist :ref:`hier <device_identifier>` zu
finden. |device_identifier_constant|
"""
}]
})

def openhab_spitfp_baudrate(port):
    return {
        'packet': 'Set SPITFP Baudrate',
        'element': 'Baudrate',

        'name': 'SPITFP Baudrate Port {}'.format(port),
        'type': 'integer',
        'default': 1400000,
        'min': 400000,
        'max': 2000000,

        'label': '(Maximum) SPITFP Baudrate Port {}'.format(port),
        'description': 'The baudrate for Bricklet port {}.\n\nIf you want to increase the throughput of Bricklets you can increase the baudrate. If you get a high error count because of high interference you can decrease the baudrate.\n\nIf the dynamic baudrate feature is enabled, this is the maximum baudrate.\n\nRegulatory testing is done with the default baudrate. If CE compatibility or similar is necessary in your applications we recommend to not change the baudrate.'.format(port),
    }

common_openhab = {
    'bricklet_get_identity': {
        'actions': ['Get Identity']
    },

    'brick_get_identity': {
        'actions': ['Get Identity']
    },

    'comcu_bricklet': {
        'actions': ['Read UID', 'Get Chip Temperature', 'Get Status LED Config', 'Get SPITFP Error Count', 'Reset'],
        'params': [{
            'packet': 'Set Status LED Config',
            'element': 'Config',

            'name': 'Status LED Config',
            'type': 'integer',
            'options': [('Off', 0),
                        ('On', 1),
                        ('Show Heartbeat', 2),
                        ('Show Status', 3)],
            'limit_to_options': 'true',
            'default': 3,
            'label': 'Status LED Configuration',
            'description': 'The status LED configuration. By default the LED shows communication traffic between Brick and Bricklet, it flickers once for every 10 received data packets.\n\nYou can also turn the LED permanently on/off or show a heartbeat.\n\nIf the Bricklet is in bootloader mode, the LED is will show heartbeat by default.'
        }],
        'init_code': 'this.setStatusLEDConfig(cfg.statusLEDConfig);'
    },

    'brick_chip_temperature': {
        'actions': ['Get Chip Temperature']
    },

    'brick_status_led': {
        'actions': ['Is Status LED Enabled'],
        'params': [{
            'virtual': True,

            'name': 'Status LED Config',
            'type': 'boolean',
            'default': 'true',
            'label': 'Status LED Configuration',
            'description': 'The status LED is the blue LED next to the USB connector. If enabled is is on and it flickers if data is transfered. If disabled it is always off.'
        }],
        'init_code': """if(cfg.statusLEDConfig) {
                this.enableStatusLED();
            } else {
                this.disableStatusLED();
            }"""
    },

    'eeprom_bricklet_host': {
        'actions': ['Get Protocol1 Bricklet Name']
    },

    'comcu_bricklet_host_2_ports': {
        'actions': ['Get SPITFP Error Count', 'Get SPITFP Baudrate'],
        'params': [
            openhab_spitfp_baudrate('A'),
            openhab_spitfp_baudrate('B'),
        ],
        'init_code': """this.setSPITFPBaudrate('a', cfg.spitfpBaudratePortA);
            this.setSPITFPBaudrate('b', cfg.spitfpBaudratePortB);"""
    },

    'comcu_bricklet_host_4_ports': {
        'actions': ['Get SPITFP Error Count', 'Get SPITFP Baudrate'],
        'params': [
            openhab_spitfp_baudrate('A'),
            openhab_spitfp_baudrate('B'),
            openhab_spitfp_baudrate('C'),
            openhab_spitfp_baudrate('D'),
        ],
        'init_code': """this.setSPITFPBaudrate('a', cfg.spitfpBaudratePortA);
            this.setSPITFPBaudrate('b', cfg.spitfpBaudratePortB);
            this.setSPITFPBaudrate('c', cfg.spitfpBaudratePortC);
            this.setSPITFPBaudrate('d', cfg.spitfpBaudratePortD);"""
    },

    'comcu_bricklet_host': {
        'actions': ['Get SPITFP Baudrate Config'],
        'params': [{
            'packet': 'Set SPITFP Baudrate Config',
            'element': 'Enable Dynamic Baudrate',

            'name': 'SPITFP Enable Dynamic Baudrate',
            'type': 'boolean',
            'default': 'true',
            'label': 'SPITFP Enable Dynamic Baudrate',
            'description': 'The SPITF protocol can be used with a dynamic baudrate. If the dynamic baudrate is enabled, the Brick will try to adapt the baudrate for the communication between Bricks and Bricklets according to the amount of data that is transferred.\n\nThe baudrate will be increased exponentially if lots of data is sent/received and decreased linearly if little data is sent/received.\n\nThis lowers the baudrate in applications where little data is transferred (e.g. a weather station) and increases the robustness. If there is lots of data to transfer (e.g. Thermal Imaging Bricklet) it automatically increases the baudrate as needed.\n\nIn cases where some data has to transferred as fast as possible every few seconds (e.g. RS485 Bricklet with a high baudrate but small payload) you may want to turn the dynamic baudrate off to get the highest possible performance.\n\nThe maximum value of the baudrate can be set per port. If the dynamic baudrate is disabled, the maximum baudrate will be used statically.'
        }, {
            'packet': 'Set SPITFP Baudrate Config',
            'element': 'Minimum Dynamic Baudrate',

            'name': 'SPITFP Minimum Dynamic Baudrate',
            'type': 'integer',
            'default': 400000,
            'min': 400000,
            'max': 2000000,

            'label': 'SPITFP Minimum Dynamic Baudrate',
            'description': 'See SPITFP Enable Dynamic Baudrate',
        }],
        'init_code': """this.setSPITFPBaudrateConfig(cfg.spitfpEnableDynamicBaudrate, cfg.spitfpMinimumDynamicBaudrate);"""
    },

    'send_timeout_count': {
        'actions': ['Get Send Timeout Count']
    },

    'tng': {
        'actions': ['Get Timestamp']
    }
}
