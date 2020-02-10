# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Master Brick communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 9],
    'category': 'Brick',
    'device_identifier': 13,
    'name': 'Master',
    'display_name': 'Master',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Basis to build stacks and has 4 Bricklet ports',
        'de': 'Grundlage um Stapel zu bauen und bietet 4 Bricklet Anschlüsse'
    },
    'released': True,
    'documented': True,
    'discontinued': False,
    'features': [
        'brick_get_identity',
        'brick_status_led',
        'brick_reset',
        'brick_chip_temperature',
        'send_timeout_count',
        'eeprom_bricklet_host_4_ports',
        'comcu_bricklet_host',
        'comcu_bricklet_host_4_ports',
        'standard_bricklet_host_4_ports'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append({
'name': 'Extension Type',
'type': 'uint32',
'constants': [('Chibi', 1),
              ('RS485', 2),
              ('Wifi', 3),
              ('Ethernet', 4),
              ('Wifi2', 5)]
})

com['constant_groups'].append({
'name': 'Chibi Frequency',
'type': 'uint8',
'constants': [('OQPSK 868 MHz', 0),
              ('OQPSK 915 MHz', 1),
              ('OQPSK 780 MHz', 2),
              ('BPSK40 915 MHz', 3)]
})

com['constant_groups'].append({
'name': 'RS485 Parity',
'type': 'char',
'constants': [('None', 'n'),
              ('Even', 'e'),
              ('Odd', 'o')]
})

com['constant_groups'].append({
'name': 'Wifi Connection',
'type': 'uint8',
'constants': [('DHCP', 0),
              ('Static IP', 1),
              ('Access Point DHCP', 2),
              ('Access Point Static IP', 3),
              ('Ad Hoc DHCP', 4),
              ('Ad Hoc Static IP', 5)]
})

com['constant_groups'].append({
'name': 'Wifi Encryption',
'type': 'uint8',
'constants': [('WPA WPA2', 0),
              ('WPA Enterprise', 1),
              ('WEP', 2),
              ('No Encryption', 3)]
})

com['constant_groups'].append({
'name': 'Wifi EAP Option',
'type': 'uint8',
'constants': [('Outer Auth EAP FAST', 0),
              ('Outer Auth EAP TLS', 1),
              ('Outer Auth EAP TTLS', 2),
              ('Outer Auth EAP PEAP', 3),
              ('Inner Auth EAP MSCHAP', 0),
              ('Inner Auth EAP GTC', 4),
              ('Cert Type CA Cert', 0),
              ('Cert Type Client Cert', 8),
              ('Cert Type Private Key', 16)]
})

com['constant_groups'].append({
'name': 'Wifi State',
'type': 'uint8',
'constants': [('Disassociated', 0),
              ('Associated', 1),
              ('Associating', 2),
              ('Error', 3),
              ('Not Initialized Yet', 255)]
})

com['constant_groups'].append({
'name': 'Wifi Power Mode',
'type': 'uint8',
'constants': [('Full Speed', 0),
              ('Low Power', 1)]
})

com['constant_groups'].append({
'name': 'Wifi Domain',
'type': 'uint8',
'constants': [('Channel 1To11', 0),
              ('Channel 1To13', 1),
              ('Channel 1To14', 2)]
})

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

com['constant_groups'].append({
'name': 'Ethernet Connection',
'type': 'uint8',
'constants': [('DHCP', 0),
              ('Static IP', 1)]
})

com['constant_groups'].append({
'name': 'Connection Type',
'type': 'uint8',
'constants': [('None', 0),
              ('USB', 1),
              ('SPI Stack', 2),
              ('Chibi', 3),
              ('RS485', 4),
              ('Wifi', 5),
              ('Ethernet', 6),
              ('Wifi2', 7)]
})

com['constant_groups'].append({
'name': 'Wifi2 PHY Mode',
'type': 'uint8',
'constants': [('B', 0),
              ('G', 1),
              ('N', 2)]
})

com['constant_groups'].append({
'name': 'Wifi2 Client Status',
'type': 'uint8',
'constants': [('Idle', 0),
              ('Connecting', 1),
              ('Wrong Password', 2),
              ('No AP Found', 3),
              ('Connect Failed', 4),
              ('Got IP', 5),
              ('Unknown', 255)]
})

com['constant_groups'].append({
'name': 'Wifi2 AP Encryption',
'type': 'uint8',
'constants': [('Open', 0),
              ('WEP', 1),
              ('WPA PSK', 2),
              ('WPA2 PSK', 3),
              ('WPA WPA2 PSK', 4)]
})

com['constant_groups'].append({
'name': 'Wifi2 Mesh Status',
'type': 'uint8',
'constants': [('Disabled', 0),
              ('WIFI Connecting', 1),
              ('Got IP', 2),
              ('Mesh Local', 3),
              ('Mesh Online', 4),
              ('AP Available', 5),
              ('AP Setup', 6),
              ('Leaf Available', 7)]
})

com['packets'].append({
'type': 'function',
'name': 'Get Stack Voltage',
'elements': [('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the stack voltage. The stack voltage is the
voltage that is supplied via the stack, i.e. it is given by a
Step-Down or Step-Up Power Supply.
""",
'de':
"""
Gibt die Spannung des Stapels zurück. Diese Spannung wird über
den Stapel verteilt und kann zum Beispiel über eine Step-Down oder
Step-Up Power Supply eingespeist werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Stack Current',
'elements': [('Current', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the stack current. The stack current is the
current that is drawn via the stack, i.e. it is given by a
Step-Down or Step-Up Power Supply.
""",
'de':
"""
Gibt den Stromverbrauch des Stapels zurück. Der angegebene Strom
bezieht sich auf den Stromverbrauch der am Stapel angeschlossenen Verbraucher.
Die Speisung kann z.B. über eine Step-Down oder Step-Up Power Supply erfolgen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Extension Type',
'elements': [('Extension', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Exttype', 'uint32', 1, 'in', {'constant_group': 'Extension Type'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Writes the extension type to the EEPROM of a specified extension.
The extension is either 0 or 1 (0 is the lower one, 1 is the upper one,
if only one extension is present use 0).

Possible extension types:

.. csv-table::
 :header: "Type", "Description"
 :widths: 10, 100

 "1",    "Chibi"
 "2",    "RS485"
 "3",    "WIFI"
 "4",    "Ethernet"
 "5",    "WIFI 2.0"

The extension type is already set when bought and it can be set with the
Brick Viewer, it is unlikely that you need this function.
""",
'de':
"""
Schreibt den Typ der Extension in den EEPROM der angegebenen Extension.
Die Extension kann entweder 0 oder 1 sein (0 ist die untere, 1
die obere, wenn nur eine Extension verfügbar ist, ist 0 zu verwenden)

Mögliche Extensiontypen:

.. csv-table::
 :header: "Typ", "Beschreibung"
 :widths: 10, 100

 "1",    "Chibi"
 "2",    "RS485"
 "3",    "WIFI"
 "4",    "Ethernet"
 "5",    "WIFI 2.0"

Der Typ der Extension ist schon gesetzt beim Erwerb der Extension und kann
über den Brick Viewer gesetzt werden. Daher ist es unwahrscheinlich, dass
diese Funktion benötigt wird.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Extension Type',
'elements': [('Extension', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Exttype', 'uint32', 1, 'out', {'constant_group': 'Extension Type'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the type for a given extension as set by :func:`Set Extension Type`.
""",
'de':
"""
Gibt den Typ der angegebenen Extension zurück, wie von :func:`Set Extension Type` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is Chibi Present',
'elements': [('Present', 'bool', 1, 'out', {})],
'since_firmware': [1, 1, 0],
'doc': ['af', {
'en':
"""
Returns *true* if the Master Brick is at position 0 in the stack and a Chibi
Extension is available.
""",
'de':
"""
Gibt *true* zurück, wenn der Master Brick an Position 0 im Stapel und eine
Chibi Extension verfügbar ist.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Chibi Address',
'elements': [('Address', 'uint8', 1, 'in', {'range': (1, 255)})],
'since_firmware': [1, 1, 0],
'doc': ['af', {
'en':
"""
Sets the address belonging to the Chibi Extension.

It is possible to set the address with the Brick Viewer and it will be
saved in the EEPROM of the Chibi Extension, it does not
have to be set on every startup.
""",
'de':
"""
Setzt die zugehörige Adresse der Chibi Extension.

Es ist möglich die Adresse mit dem Brick Viewer zu setzen und diese
wird im EEPROM der Chibi Extension abgespeichert. Ein Setzen bei
jedem Start ist daher nicht notwendig.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Chibi Address',
'elements': [('Address', 'uint8', 1, 'out', {'range': (1, 255)})],
'since_firmware': [1, 1, 0],
'doc': ['af', {
'en':
"""
Returns the address as set by :func:`Set Chibi Address`.
""",
'de':
"""
Gibt die Adresse zurück, wie von :func:`Set Chibi Address` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Chibi Master Address',
'elements': [('Address', 'uint8', 1, 'in', {'range': (1, 255)})],
'since_firmware': [1, 1, 0],
'doc': ['af', {
'en':
"""
Sets the address of the Chibi Master. This address is used if the
Chibi Extension is used as slave (i.e. it does not have a USB connection).

It is possible to set the address with the Brick Viewer and it will be
saved in the EEPROM of the Chibi Extension, it does not
have to be set on every startup.
""",
'de':
"""
Setzt die Adresse des Chibi Master. Diese Adresse wird verwendet
wenn die Chibi Extension als Slave verwendet wird (z.B. wenn keine USB-Verbindung
besteht).

Es ist möglich die Adresse mit dem Brick Viewer zu setzen und diese wird im
EEPROM der Chibi Extension abgespeichert. Ein Setzen bei
jedem Start ist daher nicht notwendig.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Chibi Master Address',
'elements': [('Address', 'uint8', 1, 'out', {'range': (1, 255)})],
'since_firmware': [1, 1, 0],
'doc': ['af', {
'en':
"""
Returns the address as set by :func:`Set Chibi Master Address`.
""",
'de':
"""
Gibt die Adresse zurück, wie von :func:`Set Chibi Master Address` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Chibi Slave Address',
'elements': [('Num', 'uint8', 1, 'in', {'range': (0, 254)}),
             ('Address', 'uint8', 1, 'in')],
'since_firmware': [1, 1, 0],
'doc': ['af', {
'en':
"""
Sets up to 254 slave addresses. 0 has a
special meaning, it is used as list terminator and not allowed as normal slave
address. The address numeration (via :param:`num` parameter) has to be used
ascending from 0. For example: If you use the Chibi Extension in Master mode
(i.e. the stack has an USB connection) and you want to talk to three other
Chibi stacks with the slave addresses 17, 23, and 42, you should call with
``(0, 17)``, ``(1, 23)``, ``(2, 42)`` and ``(3, 0)``. The last call with
``(3, 0)`` is a list terminator and indicates that the Chibi slave address
list contains 3 addresses in this case.

It is possible to set the addresses with the Brick Viewer, that will take care
of correct address numeration and list termination.

The slave addresses will be saved in the EEPROM of the Chibi Extension, they
don't have to be set on every startup.
""",
'de':
"""
Setzt bis zu 254 Slave Adressen. 0 hat eine
besondere Bedeutung, sie wird zur Terminierung der Liste verwendet und ist nicht
als normale Slave Adresse erlaubt.
Die Adressnummerierung (mittels :param:`num` Parameter) muss aufsteigend ab
0 erfolgen. Beispiel: Wenn die Chibi Extension im Master Modus verwendet wird
(z.B. wenn der Stapel eine USB-Verbindung hat) und es soll mit drei weiteren
Chibi Stapeln kommuniziert werden, mit den Adressen 17, 23 und 42, sollten die
Aufrufe ``(0, 17)``, ``(1, 23)``, ``(2, 42)`` und ``(3, 0)`` sein. Der letzte
Aufruf mit ``(3, 0)`` dient der Terminierung der Liste und zeigt an, dass die
Chibi Slave Adressliste in diesem Fall 3 Einträge beinhaltet.

Es ist möglich die Adressen mit dem Brick Viewer zu setzen, dieser kümmert sich
dann um korrekte Adressnummerierung und Terminierung der Liste.

Die Slave Adresse werden im EEPROM der Chibi Extension abgespeichert. Ein
Setzen bei jedem Start ist daher nicht notwendig.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Chibi Slave Address',
'elements': [('Num', 'uint8', 1, 'in', {'range': (0, 254)}),
             ('Address', 'uint8', 1, 'out')],
'since_firmware': [1, 1, 0],
'doc': ['af', {
'en':
"""
Returns the slave address for a given :param:`num` as set by
:func:`Set Chibi Slave Address`.
""",
'de':
"""
Gibt die Slave Adresse für eine Adressnummerierung (mittels :param:`num` Parameter)
zurück, wie von :func:`Set Chibi Slave Address` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Chibi Signal Strength',
'elements': [('Signal Strength', 'uint8', 1, 'out', {'unit': 'Decibel'})],
'since_firmware': [1, 1, 0],
'doc': ['af', {
'en':
"""
Returns the signal strength in dBm. The signal strength updates every time a
packet is received.
""",
'de':
"""
Gibt die Signalstärke in dBm zurück. Die Aktualisierung der Signalstärke
wird bei jedem Empfang eines Paketes durchgeführt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Chibi Error Log',
'elements': [('Underrun', 'uint16', 1, 'out', {}),
             ('CRC Error', 'uint16', 1, 'out', {}),
             ('No Ack', 'uint16', 1, 'out', {}),
             ('Overflow', 'uint16', 1, 'out', {})],
'since_firmware': [1, 1, 0],
'doc': ['af', {
'en':
"""
Returns underrun, CRC error, no ACK and overflow error counts of the Chibi
communication. If these errors start rising, it is likely that either the
distance between two Chibi stacks is becoming too big or there are
interferences.
""",
'de':
"""
Gibt folgende Fehlerzähler der Chibi Kommunikation zurück: Underrun, CRC Fehler,
kein ACK und Overflow. Bei Anstieg dieser Fehlerzähler ist es wahrscheinlich, dass
entweder die Entfernung zwischen zwei Chibi Stapeln zu groß wird oder Störungen
vorliegen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Chibi Frequency',
'elements': [('Frequency', 'uint8', 1, 'in', {'constant_group': 'Chibi Frequency'})],
'since_firmware': [1, 1, 0],
'doc': ['af', {
'en':
"""
Sets the Chibi frequency range for the Chibi Extension. Possible values are:

.. csv-table::
 :header: "Type", "Description"
 :widths: 10, 100

 "0",    "OQPSK 868MHz (Europe)"
 "1",    "OQPSK 915MHz (US)"
 "2",    "OQPSK 780MHz (China)"
 "3",    "BPSK40 915MHz"

It is possible to set the frequency with the Brick Viewer and it will be
saved in the EEPROM of the Chibi Extension, it does not
have to be set on every startup.
""",
'de':
"""
Setzt den Chibi Frequenzbereich der Chibi Extension. Mögliche Werte sind:

.. csv-table::
 :header: "Typ", "Beschreibung"
 :widths: 10, 100

 "0",    "OQPSK 868MHz (Europe)"
 "1",    "OQPSK 915MHz (US)"
 "2",    "OQPSK 780MHz (China)"
 "3",    "BPSK40 915MHz"

Es ist möglich den Frequenzbereich mit dem Brick Viewer zu setzen und dieser wird
im EEPROM der Chibi Extension abgespeichert. Ein Setzen bei
jedem Start ist daher nicht notwendig.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Chibi Frequency',
'elements': [('Frequency', 'uint8', 1, 'out', {'constant_group': 'Chibi Frequency'})],
'since_firmware': [1, 1, 0],
'doc': ['af', {
'en':
"""
Returns the frequency value as set by :func:`Set Chibi Frequency`.
""",
'de':
"""
Gibt den Frequenzbereich zurück, wie von :func:`Set Chibi Frequency` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Chibi Channel',
'elements': [('Channel', 'uint8', 1, 'in', {'range': 'dynamic'})],
'since_firmware': [1, 1, 0],
'doc': ['af', {
'en':
"""
Sets the channel used by the Chibi Extension. Possible channels are
different for different frequencies:

.. csv-table::
 :header: "Frequency", "Possible Channels"
 :widths: 40, 60

 "OQPSK 868MHz (Europe)", "0"
 "OQPSK 915MHz (US)",     "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"
 "OQPSK 780MHz (China)",  "0, 1, 2, 3"
 "BPSK40 915MHz",         "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"

It is possible to set the channel with the Brick Viewer and it will be
saved in the EEPROM of the Chibi Extension, it does not
have to be set on every startup.
""",
'de':
"""
Setzt den verwendeten Kanal der Chibi Extension. Die möglichen Kanäle sind
abhängig vom verwendeten Frequenzbereich:

.. csv-table::
 :header: "Frequenzbereich", "Mögliche Kanäle"
 :widths: 40, 60

 "OQPSK 868MHz (Europe)", "0"
 "OQPSK 915MHz (US)",     "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"
 "OQPSK 780MHz (China)",  "0, 1, 2, 3"
 "BPSK40 915MHz",         "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"

Es ist möglich den Kanal mit dem Brick Viewer zu setzen und dieser wird
im EEPROM der Chibi Extension abgespeichert. Ein Setzen bei
jedem Start ist daher nicht notwendig.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Chibi Channel',
'elements': [('Channel', 'uint8', 1, 'out', {'range': 'dynamic'})],
'since_firmware': [1, 1, 0],
'doc': ['af', {
'en':
"""
Returns the channel as set by :func:`Set Chibi Channel`.
""",
'de':
"""
Gibt den Kanal zurück, wie von :func:`Set Chibi Channel` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is RS485 Present',
'elements': [('Present', 'bool', 1, 'out', {})],
'since_firmware': [1, 2, 0],
'doc': ['af', {
'en':
"""
Returns *true* if the Master Brick is at position 0 in the stack and a RS485
Extension is available.
""",
'de':
"""
Gibt *true* zurück, wenn der Master Brick an Position 0 im Stapel und eine
RS485 Extension verfügbar ist.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set RS485 Address',
'elements': [('Address', 'uint8', 1, 'in', {})],
'since_firmware': [1, 2, 0],
'doc': ['af', {
'en':
"""
Sets the address (0-255) belonging to the RS485 Extension.

Set to 0 if the RS485 Extension should be the RS485 Master (i.e.
connected to a PC via USB).

It is possible to set the address with the Brick Viewer and it will be
saved in the EEPROM of the RS485 Extension, it does not
have to be set on every startup.
""",
'de':
"""
Setzt die zugehörige Adresse (0-255) der RS485 Extension.

Um eine RS485 Extension als RS485 Master (z.B. verbunden mit einem PC über
USB) zu betreiben muss die Adresse auf 0 gesetzt werden.

Es ist möglich die Adresse mit dem Brick Viewer zu setzen und diese wird im
EEPROM der RS485 Extension abgespeichert. Ein Setzen bei
jedem Start ist daher nicht notwendig.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get RS485 Address',
'elements': [('Address', 'uint8', 1, 'out', {})],
'since_firmware': [1, 2, 0],
'doc': ['af', {
'en':
"""
Returns the address as set by :func:`Set RS485 Address`.
""",
'de':
"""
Gibt die Adresse zurück, wie von :func:`Set RS485 Address` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set RS485 Slave Address',
'elements': [('Num', 'uint8', 1, 'in', {}),
             ('Address', 'uint8', 1, 'in', {})],
'since_firmware': [1, 2, 0],
'doc': ['af', {
'en':
"""
Sets up to 255 slave addresses. Valid addresses are in range 1-255. 0 has a
special meaning, it is used as list terminator and not allowed as normal slave
address. The address numeration (via ``num`` parameter) has to be used
ascending from 0. For example: If you use the RS485 Extension in Master mode
(i.e. the stack has an USB connection) and you want to talk to three other
RS485 stacks with the addresses 17, 23, and 42, you should call with
``(0, 17)``, ``(1, 23)``, ``(2, 42)`` and ``(3, 0)``. The last call with
``(3, 0)`` is a list terminator and indicates that the RS485 slave address list
contains 3 addresses in this case.

It is possible to set the addresses with the Brick Viewer, that will take care
of correct address numeration and list termination.

The slave addresses will be saved in the EEPROM of the Chibi Extension, they
don't have to be set on every startup.
""",
'de':
"""
Setzt bis zu 255 Slave Adressen. Gültige Adressen sind 1-255. 0 hat eine
besondere Bedeutung, sie wird zur Terminierung der Liste verwendet und ist nicht
als normale Slave Adresse erlaubt.
Die Adressnummerierung (mittels ``num`` Parameter) muss aufsteigend ab
0 erfolgen. Beispiel: Wenn die RS485 Extension im Master Modus verwendet wird
(z.B. wenn der Stapel eine USB-Verbindung hat) und es soll mit drei weiteren
RS485 Stapeln kommuniziert werden, mit den Adressen 17, 23 und 42, sollten die
Aufrufe ``(0, 17)``, ``(1, 23)``, ``(2, 42)`` und ``(3, 0)`` sein. Der letzte
Aufruf mit ``(3, 0)`` dient der Terminierung der Liste und zeigt an, dass die
RS485 Slave Adressliste in diesem Fall 3 Einträge beinhaltet.

Es ist möglich die Adressen mit dem Brick Viewer zu setzen, dieser kümmert sich
dann um korrekte Adressnummerierung und Terminierung der Liste.

Die Slave Adresse werden im EEPROM der RS485 Extension abgespeichert. Ein
Setzen bei jedem Start ist daher nicht notwendig.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get RS485 Slave Address',
'elements': [('Num', 'uint8', 1, 'in', {}),
             ('Address', 'uint8', 1, 'out', {})],
'since_firmware': [1, 2, 0],
'doc': ['af', {
'en':
"""
Returns the slave address for a given ``num`` as set by
:func:`Set RS485 Slave Address`.
""",
'de':
"""
Gibt die Slave Adresse für eine Adressnummerierung (mittels ``num`` Parameter)
zurück, wie von :func:`Set RS485 Slave Address` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get RS485 Error Log',
'elements': [('CRC Error', 'uint16', 1, 'out', {})],
'since_firmware': [1, 2, 0],
'doc': ['af', {
'en':
"""
Returns CRC error counts of the RS485 communication.
If this counter starts rising, it is likely that the distance
between the RS485 nodes is too big or there is some kind of
interference.
""",
'de':
"""
Gibt den CRC Fehlerzähler der RS485 Kommunikation zurück. Wenn dieser Zähler
ansteigt ist es wahrscheinlich, dass der Abstand zwischen zwei RS485-Teilnehmern
zu groß ist oder es Störungen gibt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set RS485 Configuration',
'elements': [('Speed', 'uint32', 1, 'in', {'unit': 'Baud'}),
             ('Parity', 'char', 1, 'in', {'constant_group': 'RS485 Parity'}),
             ('Stopbits', 'uint8', 1, 'in', {'range': (1, 2)})],
'since_firmware': [1, 2, 0],
'doc': ['af', {
'en':
"""
Sets the configuration of the RS485 Extension. The
Master Brick will try to match the given baud rate as exactly as possible.
The maximum recommended baud rate is 2000000 (2MBd).
Possible values for parity are 'n' (none), 'e' (even) and 'o' (odd).

If your RS485 is unstable (lost messages etc.), the first thing you should
try is to decrease the speed. On very large bus (e.g. 1km), you probably
should use a value in the range of 100000 (100kBd).

The values are stored in the EEPROM and only applied on startup. That means
you have to restart the Master Brick after configuration.
""",
'de':
"""
Setzt die Schnittstellenkonfiguration der RS485 Extension.
Der Master Brick versucht die vorgegebene Baudrate so
genau wie möglich zu erreichen. Die maximale empfohlene Baudrate ist 2000000
(2MBd). Mögliche Werte für die Parität sind 'n' (keine), 'e' (gerade) und
'o' (ungerade).

Wenn die RS485 Kommunikation instabil ist (verlorene Nachrichten etc.), sollte
zuerst die Baudrate verringert werden. Sehr lange Busleitungen (z.B. 1km)
sollten möglichst Werte im Bereich von 100000 (100kBd) verwenden.

Die Werte sind im EEPROM gespeichert und werden nur beim Start angewandt. Dass
bedeutet, der Master Brick muss nach einer Konfiguration neu gestartet werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get RS485 Configuration',
'elements': [('Speed', 'uint32', 1, 'out', {'unit': 'Baud'}),
             ('Parity', 'char', 1, 'out', {'constant_group': 'RS485 Parity'}),
             ('Stopbits', 'uint8', 1, 'out', {'range': (1, 2)})],
'since_firmware': [1, 2, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set RS485 Configuration`.
""",
'de':
"""
Gibt die Schnittstellenkonfiguration zurück, wie von :func:`Set RS485 Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is Wifi Present',
'elements': [('Present', 'bool', 1, 'out', {})],
'since_firmware': [1, 2, 0],
'doc': ['af', {
'en':
"""
Returns *true* if the Master Brick is at position 0 in the stack and a WIFI
Extension is available.
""",
'de':
"""
Gibt *true* zurück, wenn der Master Brick an Position 0 im Stapel und eine
WIFI Extension verfügbar ist.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Wifi Configuration',
'elements': [('SSID', 'string', 32, 'in', {}),
             ('Connection', 'uint8', 1, 'in', {'constant_group': 'Wifi Connection'}),
             ('IP', 'uint8', 4, 'in', {}),
             ('Subnet Mask', 'uint8', 4, 'in', {}),
             ('Gateway', 'uint8', 4, 'in', {}),
             ('Port', 'uint16', 1, 'in', {'default': 4223})],
'since_firmware': [1, 3, 0],
'doc': ['af', {
'en':
"""
Sets the configuration of the WIFI Extension. The ``ssid`` can have a max length
of 32 characters. Possible values for ``connection`` are:

.. csv-table::
 :header: "Value", "Description"
 :widths: 10, 90

 "0", "DHCP"
 "1", "Static IP"
 "2", "Access Point: DHCP"
 "3", "Access Point: Static IP"
 "4", "Ad Hoc: DHCP"
 "5", "Ad Hoc: Static IP"

If you set ``connection`` to one of the static IP options then you have to
supply ``ip``, ``subnet_mask`` and ``gateway`` as an array of size 4 (first
element of the array is the least significant byte of the address). If
``connection`` is set to one of the DHCP options then ``ip``, ``subnet_mask``
and ``gateway`` are ignored, you can set them to 0.

The last parameter is the port that your program will connect to.

The values are stored in the EEPROM and only applied on startup. That means
you have to restart the Master Brick after configuration.

It is recommended to use the Brick Viewer to set the WIFI configuration.
""",
'de':
"""
Setzt die Konfiguration der WIFI Extension. Die ``ssid`` darf eine maximale
Länge von 32 Zeichen haben. Mögliche Werte für ``connection`` sind:

.. csv-table::
 :header: "Wert", "Beschreibung"
 :widths: 10, 90

 "0", "DHCP"
 "1", "Statische IP"
 "2", "Access Point: DHCP"
 "3", "Access Point: Statische IP"
 "4", "Ad Hoc: DHCP"
 "5", "Ad Hoc: Statische IP"

Wenn ``connection`` auf eine der statische IP Optionen gesetzt wird, dann müssen
``ip``, ``subnet_mask`` und ``gateway`` als ein Array der Größe 4 angegeben
werden. Dabei ist das erste Element im Array das niederwertigste Byte. Falls
``connection`` auf eine der DHCP Optionen gesetzt ist, werden ``ip``,
``subnet_mask`` und ``gateway`` ignoriert.

Der letzte Parameter ist der Port auf den das Anwendungsprogramm sich
verbindet.

Die Werte sind im EEPROM gespeichert und werden nur beim Start angewandt. Dass
bedeutet, der Master Brick muss nach einer Konfiguration neu gestartet werden.

Wir empfehlen den Brick Viewer zu verwenden, um die WIFI Extension zu
konfigurieren.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Wifi Configuration',
'elements': [('SSID', 'string', 32, 'out', {}),
             ('Connection', 'uint8', 1, 'out', {'constant_group': 'Wifi Connection'}),
             ('IP', 'uint8', 4, 'out', {}),
             ('Subnet Mask', 'uint8', 4, 'out', {}),
             ('Gateway', 'uint8', 4, 'out', {}),
             ('Port', 'uint16', 1, 'out', {'default': 4223})],
'since_firmware': [1, 3, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Wifi Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Wifi Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Wifi Encryption',
'elements': [('Encryption', 'uint8', 1, 'in', {'constant_group': 'Wifi Encryption'}),
             ('Key', 'string', 50, 'in', {}),
             ('Key Index', 'uint8', 1, 'in', {'range': (1, 4)}),
             ('EAP Options', 'uint8', 1, 'in', {'constant_group': 'Wifi EAP Option'}),
             ('CA Certificate Length', 'uint16', 1, 'in', {'unit': 'Byte', 'range': (0, 1312)}),
             ('Client Certificate Length', 'uint16', 1, 'in', {'unit': 'Byte', 'range': (0, 1312)}),
             ('Private Key Length', 'uint16', 1, 'in', {'unit': 'Byte', 'range': (0, 4320)})],
'since_firmware': [1, 3, 0],
'doc': ['af', {
'en':
"""
Sets the encryption of the WIFI Extension. The first parameter is the
type of the encryption. Possible values are:

.. csv-table::
 :header: "Value", "Description"
 :widths: 10, 90

 "0", "WPA/WPA2"
 "1", "WPA Enterprise (EAP-FAST, EAP-TLS, EAP-TTLS, PEAP)"
 "2", "WEP"
 "3", "No Encryption"

The ``key`` has a max length of 50 characters and is used if ``encryption``
is set to 0 or 2 (WPA/WPA2 or WEP). Otherwise the value is ignored.

For WPA/WPA2 the key has to be at least 8 characters long. If you want to set
a key with more than 50 characters, see :func:`Set Long Wifi Key`.

For WEP the key has to be either 10 or 26 hexadecimal digits long. It is
possible to set the WEP ``key_index`` (1-4). If you don't know your
``key_index``, it is likely 1.

If you choose WPA Enterprise as encryption, you have to set ``eap_options`` and
the length of the certificates (for other encryption types these parameters
are ignored). The certificates
themselves can be set with :func:`Set Wifi Certificate`. ``eap_options`` consist
of the outer authentication (bits 1-2), inner authentication (bit 3) and
certificate type (bits 4-5):

.. csv-table::
 :header: "Option", "Bits", "Description"
 :widths: 20, 10, 70

 "outer authentication", "1-2", "0=EAP-FAST, 1=EAP-TLS, 2=EAP-TTLS, 3=EAP-PEAP"
 "inner authentication", "3", "0=EAP-MSCHAP, 1=EAP-GTC"
 "certificate type", "4-5", "0=CA Certificate, 1=Client Certificate, 2=Private Key"

Example for EAP-TTLS + EAP-GTC + Private Key: ``option = 2 | (1 << 2) | (2 << 3)``.

The values are stored in the EEPROM and only applied on startup. That means
you have to restart the Master Brick after configuration.

It is recommended to use the Brick Viewer to set the Wi-Fi encryption.
""",
'de':
"""
Setzt die Verschlüsselung der WIFI Extension. Der erste Parameter ist der
Typ der Verschlüsselung. Mögliche Werte sind:

.. csv-table::
 :header: "Wert", "Beschreibung"
 :widths: 10, 90

 "0", "WPA/WPA2"
 "1", "WPA Enterprise (EAP-FAST, EAP-TLS, EAP-TTLS, PEAP)"
 "2", "WEP"
 "3", "Keine Verschlüsselung"

Der ``key`` hat eine maximale Länge von 50 Zeichen und wird benutzt
falls ``encryption`` auf 0 oder 2 (WPA/WPA2 oder WEP) gesetzt ist. Andernfalls
wird dieser Parameter ignoriert.

Für WPA/WPA2 muss der Schlüssel mindestens 8 Zeichen lang sein. Wenn ein
Schlüssel mit mehr als 50 Zeichen gesetzt werden soll, kann
:func:`Set Long Wifi Key` genutzt werden.

Für WEP muss der Schlüssel entweder 10 oder 26 hexadezimale Zeichen lang sein.
Es ist möglich den ``key_index`` zu setzen (1-4). Fall der ``key_index``
unbekannt ist, ist er wahrscheinlich 1.

Wenn WPA Enterprise als ``encryption`` gewählt wird, müssen ``eap_options`` und
die Länge der Zertifikate gesetzt werden. Die Zertifikate selbst können mit
:func:`Set Wifi Certificate` übertragen
werden. Die ``eap_options`` bestehen aus Outer Authentication (Bits 1-2),
Inner Authentication (Bit 3) und Certificate Type (Bits 4-5):

.. csv-table::
 :header: "Option", "Bits", "Beschreibung"
 :widths: 10, 10, 80

 "Outer Authentication", "1-2", "0=EAP-FAST, 1=EAP-TLS, 2=EAP-TTLS, 3=EAP-PEAP"
 "Inner Authentication", "3", "0=EAP-MSCHAP, 1=EAP-GTC"
 "Certificate Type", "4-5", "0=CA Certificate, 1=Client Certificate, 2=Private Key"

Beispiel für EAP-TTLS + EAP-GTC + Private Key: ``option = 2 | (1 << 2) | (2 << 3)``.

Die Werte sind im EEPROM gespeichert und werden nur beim Start angewandt.
Das bedeutet der Master Brick muss nach einer Konfiguration neu gestartet werden.

Wir empfehlen den Brick Viewer zu verwenden, um die WLAN Verschlüsselung
zu konfigurieren.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Wifi Encryption',
'elements': [('Encryption', 'uint8', 1, 'out', {'constant_group': 'Wifi Encryption'}),
             ('Key', 'string', 50, 'out', {}),
             ('Key Index', 'uint8', 1, 'out', {'range': (1, 4)}),
             ('EAP Options', 'uint8', 1, 'out', {'constant_group': 'Wifi EAP Option'}),
             ('CA Certificate Length', 'uint16', 1, 'out', {}),
             ('Client Certificate Length', 'uint16', 1, 'out', {}),
             ('Private Key Length', 'uint16', 1, 'out', {})],
'since_firmware': [1, 3, 0],
'doc': ['af', {
'en':
"""
Returns the encryption as set by :func:`Set Wifi Encryption`.

.. note::
 Since Master Brick Firmware version 2.4.4 the key is not returned anymore.
""",
'de':
"""
Gibt die Verschlüsselungseinstellungen zurück, wie von
:func:`Set Wifi Encryption` gesetzt.

.. note::
 Seit Master Brick Firmware Version 2.4.4 wird der Schlüssel nicht mehr
 zurückgegeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Wifi Status',
'elements': [('MAC Address', 'uint8', 6, 'out', {}),
             ('BSSID', 'uint8', 6, 'out', {}),
             ('Channel', 'uint8', 1, 'out', {'range': 'dynamic'}),
             ('RSSI', 'int16', 1, 'out', {}),
             ('IP', 'uint8', 4, 'out', {}),
             ('Subnet Mask', 'uint8', 4, 'out', {}),
             ('Gateway', 'uint8', 4, 'out', {}),
             ('RX Count', 'uint32', 1, 'out', {}),
             ('TX Count', 'uint32', 1, 'out', {}),
             ('State', 'uint8', 1, 'out', {'constant_group': 'Wifi State'})],
'since_firmware': [1, 3, 0],
'doc': ['af', {
'en':
"""
Returns the status of the WIFI Extension. The ``state`` is updated automatically,
all of the other parameters are updated on startup and every time
:func:`Refresh Wifi Status` is called.

Possible states are:

.. csv-table::
 :header: "State", "Description"
 :widths: 10, 90

 "0", "Disassociated"
 "1", "Associated"
 "2", "Associating"
 "3", "Error"
 "255", "Not initialized yet"
""",
'de':
"""
Gibt den Status der WIFI Extension zurück. ``state`` wird automatisch
aktualisiert, alle anderen Parameter werden nur beim Starten und nach jedem
Aufruf von :func:`Refresh Wifi Status` aktualisiert.

Mögliche Werte für *state* sind:

.. csv-table::
 :header: "State", "Beschreibung"
 :widths: 10, 90

 "0", "Getrennt"
 "1", "Verbunden"
 "2", "Verbindung wird aufgebaut"
 "3", "Fehler"
 "255", "Noch nicht initialisiert"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Refresh Wifi Status',
'elements': [],
'since_firmware': [1, 3, 0],
'doc': ['af', {
'en':
"""
Refreshes the Wi-Fi status (see :func:`Get Wifi Status`). To read the status
of the Wi-Fi module, the Master Brick has to change from data mode to
command mode and back. This transaction and the readout itself is
unfortunately time consuming. This means, that it might take some ms
until the stack with attached WIFI Extension reacts again after this
function is called.
""",
'de':
"""
Aktualisiert den WLAN Status (siehe :func:`Get Wifi Status`). Um den Status
vom WLAN Modul zu lesen, muss der Master Brick vom Datenmodus in den
Kommandomodus und wieder zurück wechseln. Dieser Wechsel und das eigentliche
Auslesen ist leider zeitaufwändig. Dass heißt, es dauert ein paar ms bis der
Stapel mit aufgesteckter WIFI Extension wieder reagiert nachdem die
Funktion aufgerufen wurde.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Wifi Certificate',
'elements': [('Index', 'uint16', 1, 'in', {'range': [(0, 1311), (10000, 11311), (20000, 24319), (0xFFFE, 0xFFFF)]}),
             ('Data', 'uint8', 32, 'in', {}),
             ('Data Length', 'uint8', 1, 'in', {'unit': 'Byte', 'range': (0, 32)})],
'since_firmware': [1, 3, 0],
'doc': ['af', {
'en':
"""
This function is used to set the certificate as well as password and username
for WPA Enterprise. To set the username use index 0xFFFF,
to set the password use index 0xFFFE. The max length of username and
password is 32.

The certificate is written in chunks of size 32 and the index is used as
the index of the chunk. ``data_length`` should nearly always be 32. Only
the last chunk can have a length that is not equal to 32.

The starting index of the CA Certificate is 0, of the Client Certificate
10000 and for the Private Key 20000. Maximum sizes are 1312, 1312 and
4320 byte respectively.

The values are stored in the EEPROM and only applied on startup. That means
you have to restart the Master Brick after uploading the certificate.

It is recommended to use the Brick Viewer to set the certificate, username
and password.
""",
'de':
"""
Diese Funktion kann benutzt werden um sowohl das Zertifikat als auch
Benutzername und Passwort für WPA Enterprise zu setzen. Für den Benutzernamen
muss Index 0xFFFF und für das Password Index 0xFFFE genutzt werden.
Die maximale Länge für beide ist 32.

Das Zertifikat wird in Chunks der Größe 32 geschrieben und der Index
gibt den Index des Chunk an. ``data_length`` sollte fast immer auf 32 gesetzt
werden. Nur beim letzten Chunk ist eine Länge ungleich 32 möglich.

Der Startindex für CA Certificate ist 0, für Client Certificate 10000 und
für Private Key 20000. Die Maximalen Dateigrößen sind jeweils 1312, 1312 und
4320 Byte.

Die Werte sind im EEPROM gespeichert und werden nur beim Start angewandt.
Das bedeutet der Master Brick muss nach einer Konfiguration neu gestartet werden.

Wir empfehlen den Brick Viewer zu verwenden, um die Zertifikate, Benutzernamen
und Passwort zu konfigurieren.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Wifi Certificate',
'elements': [('Index', 'uint16', 1, 'in', {'range': [(0, 1311), (10000, 11311), (20000, 24319), (0xFFFE, 0xFFFF)]}),
             ('Data', 'uint8', 32, 'out', {}),
             ('Data Length', 'uint8', 1, 'out', {'range': (0, 32)})],
'since_firmware': [1, 3, 0],
'doc': ['af', {
'en':
"""
Returns the certificate for a given index as set by :func:`Set Wifi Certificate`.
""",
'de':
"""
Gibt das Zertifikat für einen Index zurück, wie von
:func:`Set Wifi Certificate` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Wifi Power Mode',
'elements': [('Mode', 'uint8', 1, 'in', {'constant_group': 'Wifi Power Mode', 'default': 0})],
'since_firmware': [1, 3, 0],
'doc': ['af', {
'en':
"""
Sets the power mode of the WIFI Extension. Possible modes are:

.. csv-table::
 :header: "Mode", "Description"
 :widths: 10, 90

 "0", "Full Speed (high power consumption, high throughput)"
 "1", "Low Power (low power consumption, low throughput)"
""",
'de':
"""
Setzt den Stromsparmodus für die WIFI Extension. Mögliche Werte sind:

.. csv-table::
 :header: "Mode", "Beschreibung"
 :widths: 10, 90

 "0", "Full Speed (hoher Stromverbrauch, hoher Durchsatz)"
 "1", "Low Power (geringer Stromverbrauch, geringer Durchsatz)"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Wifi Power Mode',
'elements': [('Mode', 'uint8', 1, 'out', {'constant_group': 'Wifi Power Mode', 'default': 0})],
'since_firmware': [1, 3, 0],
'doc': ['af', {
'en':
"""
Returns the power mode as set by :func:`Set Wifi Power Mode`.
""",
'de':
"""
Gibt den Stromsparmodus zurück, wie von :func:`Set Wifi Power Mode` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Wifi Buffer Info',
'elements': [('Overflow', 'uint32', 1, 'out', {}),
             ('Low Watermark', 'uint16', 1, 'out', {'unit': 'Byte', 'range': (0, 1500)}),
             ('Used', 'uint16', 1, 'out', {'unit': 'Byte', 'range': (0, 1500)})],
'since_firmware': [1, 3, 2],
'doc': ['af', {
'en':
"""
Returns informations about the Wi-Fi receive buffer. The Wi-Fi
receive buffer has a max size of 1500 byte and if data is transfered
too fast, it might overflow.

The return values are the number of overflows, the low watermark
(i.e. the smallest number of bytes that were free in the buffer) and
the bytes that are currently used.

You should always try to keep the buffer empty, otherwise you will
have a permanent latency. A good rule of thumb is, that you can transfer
1000 messages per second without problems.

Try to not send more then 50 messages at a time without any kind of
break between them.
""",
'de':
"""
Gibt Informationen über denn WLAN Empfangsbuffer zurück. Der WLAN
Empfangsbuffer hat eine maximale Größe von 1500 Byte und falls zu viele
Daten übertragen werden, kann er überlaufen.

Die Rückgabewerte sind die Anzahl der Overflows, die Low-Watermark
(d.h. die kleinste Anzahl an Byte die je noch frei waren im Buffer) und
die Anzahl der im Moment verwendeten Bytes im Buffer.

Es sollte immer versucht werden den Buffer leer zu halten, andernfalls
ist mit einer permanenten Latenz zu rechnen. Eine gute Daumenregel ist,
nicht mehr als 1000 Nachrichten pro Sekunde zu verschicken.

Dabei sollten am besten nie mehr als 50 Nachrichten auf einmal ohne
Pausen gesendet werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Wifi Regulatory Domain',
'elements': [('Domain', 'uint8', 1, 'in', {'constant_group': 'Wifi Domain', 'default': 1})],
'since_firmware': [1, 3, 4],
'doc': ['af', {
'en':
"""
Sets the regulatory domain of the WIFI Extension. Possible domains are:

.. csv-table::
 :header: "Domain", "Description"
 :widths: 10, 90

 "0", "FCC: Channel 1-11 (N/S America, Australia, New Zealand)"
 "1", "ETSI: Channel 1-13 (Europe, Middle East, Africa)"
 "2", "TELEC: Channel 1-14 (Japan)"
""",
'de':
"""
Setzt den Geltungsbereich der WIFI Extension. Mögliche Werte sind:

.. csv-table::
 :header: "Geltungsbereich", "Beschreibung"
 :widths: 10, 90

 "0", "FCC: Kanal 1-11 (N/S Amerika, Australien, Neuseeland)"
 "1", "ETSI: Kanal 1-13 (Europa, Mittlerer Osten, Afrika)"
 "2", "TELEC: Kanal 1-14 (Japan)"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Wifi Regulatory Domain',
'elements': [('Domain', 'uint8', 1, 'out', {'constant_group': 'Wifi Domain', 'default': 1})],
'since_firmware': [1, 3, 4],
'doc': ['af', {
'en':
"""
Returns the regulatory domain as set by :func:`Set Wifi Regulatory Domain`.
""",
'de':
"""
Gibt den Geltungsbereich zurück, wie von :func:`Set Wifi Regulatory Domain` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get USB Voltage',
'elements': [('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'})],
'since_firmware': [1, 3, 5],
'doc': ['af', {
'en':
"""
Returns the USB voltage. Does not work with hardware version 2.1.
""",
'de':
"""
Gibt die USB Spannung zurück. Funktioniert nicht mit Hardware Version 2.1.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Long Wifi Key',
'elements': [('Key', 'string', 64, 'in', {})],
'since_firmware': [2, 0, 2],
'doc': ['af', {
'en':
"""
Sets a long Wi-Fi key (up to 63 chars, at least 8 chars) for WPA encryption.
This key will be used
if the key in :func:`Set Wifi Encryption` is set to "-". In the old protocol,
a payload of size 63 was not possible, so the maximum key length was 50 chars.

With the new protocol this is possible, since we didn't want to break API,
this function was added additionally.
""",
'de':
"""
Setzt einen langen WLAN Schlüssel (bis zu 63 Zeichen, mindestens 8 Zeichen) für
WPA Verschlüsselung. Dieser Schlüssel wird genutzt, wenn der Schlüssel in
:func:`Set Wifi Encryption` auf "-" gesetzt wird. Im alten Protokoll war
ein Payload der Größe 63 nicht möglich, dadurch wurde die maximale
Schlüssellänge auf 50 gesetzt.

Mit dem neuen Protokoll ist die volle
Schlüssellänge möglich. Da wir keine API brechen wollten, wurde diese
Funktion zusätzlich hinzugefügt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Long Wifi Key',
'elements': [('Key', 'string', 64, 'out', {})],
'since_firmware': [2, 0, 2],
'doc': ['af', {
'en':
"""
Returns the encryption key as set by :func:`Set Long Wifi Key`.

.. note::
 Since Master Brick firmware version 2.4.4 the key is not returned anymore.
""",
'de':
"""
Gibt den Verschlüsselungsschlüssel zurück, wie von
:func:`Set Long Wifi Key` gesetzt.

.. note::
 Seit Master Brick Firmware Version 2.4.4 wird der Schlüssel nicht mehr
 zurückgegeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Wifi Hostname',
'elements': [('Hostname', 'string', 16, 'in', {})],
'since_firmware': [2, 0, 5],
'doc': ['af', {
'en':
"""
Sets the hostname of the WIFI Extension. The hostname will be displayed
by access points as the hostname in the DHCP clients table.

Setting an empty String will restore the default hostname.
""",
'de':
"""
Setzt den Hostnamen der WIFI Extension. Der Hostname wird von
Access Points als Hostname in der DHCP Client Tabelle angezeigt.

Das Setzen eines leeren Strings stellt den voreingestellten Hostnamen
wieder her.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Wifi Hostname',
'elements': [('Hostname', 'string', 16, 'out', {})],
'since_firmware': [2, 0, 5],
'doc': ['af', {
'en':
"""
Returns the hostname as set by :func:`Set Wifi Hostname`.

An empty String means, that the default hostname is used.
""",
'de':
"""
Gibt den Hostnamen zurück, wie von :func:`Set Wifi Hostname` gesetzt.

Ein leerer String bedeutet, dass der voreingestellte Hostname
genutzt wird.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Stack Current Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Stack Current` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Stack Current` callback is only triggered if the current has changed
since the last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Stack Current` Callback ausgelöst
wird. Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Stack Current` Callback wird nur ausgelöst, wenn sich die Stromstärke
seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Stack Current Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Stack Current Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Stack Current Callback Period` gesetzt
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Stack Voltage Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Stack Voltage` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Stack Voltage` callback is only triggered if the voltage has changed
since the last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Stack Voltage` Callback ausgelöst
wird. Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Stack Voltage` Callback wird nur ausgelöst, wenn sich die Spannung seit
der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Stack Voltage Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Stack Voltage Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Stack Voltage Callback Period` gesetzt
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set USB Voltage Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`USB Voltage` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`USB Voltage` callback is only triggered if the voltage has changed
since the last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`USB Voltage` Callback ausgelöst
wird. Ein Wert von 0 deaktiviert den Callback.

Der :cb:`USB Voltage` Callback wird nur ausgelöst, wenn sich die Spannung seit
der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get USB Voltage Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set USB Voltage Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set USB Voltage Callback Period` gesetzt
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Stack Current Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Ampere', 'default': 0}),
             ('Max', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Ampere', 'default': 0})],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Stack Current Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the current is *outside* the min and max values"
 "'i'",    "Callback is triggered when the current is *inside* the min and max values"
 "'<'",    "Callback is triggered when the current is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the current is greater than the min value (max is ignored)"
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Stack Current Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn die Stromstärke *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn die Stromstärke *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn die Stromstärke kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn die Stromstärke größer als der min Wert ist (max wird ignoriert)"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Stack Current Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere', 'default': 0}),
             ('Max', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere', 'default': 0})],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Stack Current Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Stack Current Callback Threshold` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Stack Voltage Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Volt', 'default': 0}),
             ('Max', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Volt', 'default': 0})],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Stack Voltage Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the voltage is *outside* the min and max values"
 "'i'",    "Callback is triggered when the voltage is *inside* the min and max values"
 "'<'",    "Callback is triggered when the voltage is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the voltage is greater than the min value (max is ignored)"
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Stack Voltage Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn die Spannung *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn die Spannung *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn die Spannung kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn die Spannung größer als der min Wert ist (max wird ignoriert)"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Stack Voltage Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt', 'default': 0}),
             ('Max', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt', 'default': 0})],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Stack Voltage Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Stack Voltage Callback Threshold` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set USB Voltage Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Volt', 'default': 0}),
             ('Max', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Volt', 'default': 0})],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`USB Voltage Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the voltage is *outside* the min and max values"
 "'i'",    "Callback is triggered when the voltage is *inside* the min and max values"
 "'<'",    "Callback is triggered when the voltage is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the voltage is greater than the min value (max is ignored)"
""",
'de':
"""
Setzt den Schwellwert für den :cb:`USB Voltage Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn die Spannung *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn die Spannung *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn die Spannung kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn die Spannung größer als der min Wert ist (max wird ignoriert)"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get USB Voltage Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt', 'default': 0}),
             ('Max', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt', 'default': 0})],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set USB Voltage Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set USB Voltage Callback Threshold` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Debounce Period',
'elements': [('Debounce', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 100})],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Sets the period with which the threshold callbacks

* :cb:`Stack Current Reached`,
* :cb:`Stack Voltage Reached`,
* :cb:`USB Voltage Reached`

are triggered, if the thresholds

* :func:`Set Stack Current Callback Threshold`,
* :func:`Set Stack Voltage Callback Threshold`,
* :func:`Set USB Voltage Callback Threshold`

keep being reached.
""",
'de':
"""
Setzt die Periode mit welcher die Schwellwert Callbacks

* :cb:`Stack Current Reached`,
* :cb:`Stack Voltage Reached`,
* :cb:`USB Voltage Reached`

ausgelöst werden, wenn die Schwellwerte

* :func:`Set Stack Current Callback Threshold`,
* :func:`Set Stack Voltage Callback Threshold`,
* :func:`Set USB Voltage Callback Threshold`

weiterhin erreicht bleiben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Debounce Period',
'elements': [('Debounce', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 100})],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Returns the debounce period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Gibt die Entprellperiode zurück, wie von :func:`Set Debounce Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Stack Current',
'elements': [('Current', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere'})],
'since_firmware': [2, 0, 5],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Stack Current Callback Period`. The :word:`parameter` is the current
of the sensor.

The :cb:`Stack Current` callback is only triggered if the current has changed
since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Stack Current Callback Period`, ausgelöst. Der :word:`parameter` ist
die Stromstärke des Sensors.

Der :cb:`Stack Current` Callback wird nur ausgelöst, wenn sich die Stromstärke
seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Stack Voltage',
'elements': [('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'})],
'since_firmware': [2, 0, 5],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Stack Voltage Callback Period`. The :word:`parameter` is the voltage
of the sensor.

The :cb:`Stack Voltage` callback is only triggered if the voltage has changed
since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Stack Voltage Callback Period`, ausgelöst. Der :word:`parameter`
ist die Spannung des Sensors.

Der :cb:`Stack Voltage` Callback wird nur ausgelöst, wenn sich die Spannung seit
der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'USB Voltage',
'elements': [('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'})],
'since_firmware': [2, 0, 5],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set USB Voltage Callback Period`. The :word:`parameter` is the USB
voltage.

The :cb:`USB Voltage` callback is only triggered if the USB voltage has changed
since the last triggering.

Does not work with hardware version 2.1.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set USB Voltage Callback Period`, ausgelöst. Der :word:`parameter` ist
die USB Spannung.

Der :cb:`USB Voltage` Callback wird nur ausgelöst, wenn sich die USB Spannung
seit der letzten Auslösung geändert hat.

Funktioniert nicht mit Hardware Version 2.1.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Stack Current Reached',
'elements': [('Current', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere'})],
'since_firmware': [2, 0, 5],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Stack Current Callback Threshold` is reached.
The :word:`parameter` is the stack current.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Stack Current Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist der Stromverbrauch des Stapels.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Stack Voltage Reached',
'elements': [('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'})],
'since_firmware': [2, 0, 5],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Stack Voltage Callback Threshold` is reached.
The :word:`parameter` is the stack voltage.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Stack Voltage Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Spannung des Stapels.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'USB Voltage Reached',
'elements': [('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'})],
'since_firmware': [2, 0, 5],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set USB Voltage Callback Threshold` is reached.
The :word:`parameter` is the voltage of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set USB Voltage Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Spannung des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is Ethernet Present',
'elements': [('Present', 'bool', 1, 'out', {})],
'since_firmware': [2, 1, 0],
'doc': ['af', {
'en':
"""
Returns *true* if the Master Brick is at position 0 in the stack and an Ethernet
Extension is available.
""",
'de':
"""
Gibt *true* zurück, wenn der Master Brick an Position 0 im Stapel und eine
Ethernet Extension verfügbar ist.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Ethernet Configuration',
'elements': [('Connection', 'uint8', 1, 'in', {'constant_group': 'Ethernet Connection'}),
             ('IP', 'uint8', 4, 'in', {}),
             ('Subnet Mask', 'uint8', 4, 'in', {}),
             ('Gateway', 'uint8', 4, 'in', {}),
             ('Port', 'uint16', 1, 'in', {'default': 4223})],
'since_firmware': [2, 1, 0],
'doc': ['af', {
'en':
"""
Sets the configuration of the Ethernet Extension. Possible values for
``connection`` are:

.. csv-table::
 :header: "Value", "Description"
 :widths: 10, 90

 "0", "DHCP"
 "1", "Static IP"

If you set ``connection`` to static IP options then you have to supply ``ip``,
``subnet_mask`` and ``gateway`` as an array of size 4 (first element of the
array is the least significant byte of the address). If ``connection`` is set
to the DHCP options then ``ip``, ``subnet_mask`` and ``gateway`` are ignored,
you can set them to 0.

The last parameter is the port that your program will connect to.

The values are stored in the EEPROM and only applied on startup. That means
you have to restart the Master Brick after configuration.

It is recommended to use the Brick Viewer to set the Ethernet configuration.
""",
'de':
"""
Setzt die Konfiguration der Ethernet Extension. Mögliche Werte für
``connection`` sind:

.. csv-table::
 :header: "Wert", "Beschreibung"
 :widths: 10, 90

 "0", "DHCP"
 "1", "Statische IP"

Wenn ``connection`` auf die statische IP Option gesetzt wird, dann müssen
``ip``, ``subnet_mask`` und ``gateway`` als ein Array der Größe 4 angegeben
werden. Dabei ist das erste Element im Array das niederwertigste Byte. Falls
``connection`` auf die DHCP Option gesetzt ist, werden ``ip``, ``subnet_mask``
und ``gateway`` ignoriert.

Der letzte Parameter ist der Port auf den das Anwendungsprogramm sich
verbindet.

Die Werte sind im EEPROM gespeichert und werden nur beim Start angewandt.
Das bedeutet der Master Brick muss nach einer Konfiguration neu gestartet
werden.

Wir empfehlen den Brick Viewer zu verwenden, um die Ethernet Extension zu
konfigurieren.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Ethernet Configuration',
'elements': [('Connection', 'uint8', 1, 'out', {'constant_group': 'Ethernet Connection'}),
             ('IP', 'uint8', 4, 'out', {}),
             ('Subnet Mask', 'uint8', 4, 'out', {}),
             ('Gateway', 'uint8', 4, 'out', {}),
             ('Port', 'uint16', 1, 'out', {'default': 4223})],
'since_firmware': [2, 1, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Ethernet Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Ethernet Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Ethernet Status',
'elements': [('MAC Address', 'uint8', 6, 'out', {}),
             ('IP', 'uint8', 4, 'out', {}),
             ('Subnet Mask', 'uint8', 4, 'out', {}),
             ('Gateway', 'uint8', 4, 'out', {}),
             ('RX Count', 'uint32', 1, 'out', {'unit': 'Byte'}),
             ('TX Count', 'uint32', 1, 'out', {'unit': 'Byte'}),
             ('Hostname', 'string', 32, 'out', {})],
'since_firmware': [2, 1, 0],
'doc': ['af', {
'en':
"""
Returns the status of the Ethernet Extension.

``mac_address``, ``ip``, ``subnet_mask`` and ``gateway`` are given as an array.
The first element of the array is the least significant byte of the address.

``rx_count`` and ``tx_count`` are the number of bytes that have been
received/send since last restart.

``hostname`` is the currently used hostname.
""",
'de':
"""
Gibt den Status der Ethernet Extension zurück.

``mac_address``, ``ip``, ``subnet_mask`` und ``gateway`` werden als Array
übergeben. Das erste Element des Arrays ist das niederwertigste Byte.

``rx_count`` und ``tx_count`` sind die Anzahl der Bytes die seit dem letzten
Neustart empfangen/gesendet wurden.

``hostname`` ist der aktuell genutzte Hostname.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Ethernet Hostname',
'elements': [('Hostname', 'string', 32, 'in', {})],
'since_firmware': [2, 1, 0],
'doc': ['af', {
'en':
"""
Sets the hostname of the Ethernet Extension. The hostname will be displayed
by access points as the hostname in the DHCP clients table.

Setting an empty String will restore the default hostname.

The current hostname can be discovered with :func:`Get Ethernet Status`.
""",
'de':
"""
Setzt den Hostnamen der Ethernet Extension. Der Hostname wird von
Access Points als Hostname in der DHCP Client Tabelle angezeigt.

Das setzen eines leeren Strings stellt den voreingestellten Hostnamen
wieder her.

Der aktuelle Hostname kann mit :func:`Get Ethernet Status` herausgefunden werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Ethernet MAC Address',
'elements': [('MAC Address', 'uint8', 6, 'in', {})],
'since_firmware': [2, 1, 0],
'doc': ['af', {
'en':
"""
Sets the MAC address of the Ethernet Extension. The Ethernet Extension should
come configured with a valid MAC address, that is also written on a
sticker of the extension itself.

The MAC address can be read out again with :func:`Get Ethernet Status`.
""",
'de':
"""
Setzt die MAC Adresse der Ethernet Extension. Die Ethernet Extension sollte
mit einer vorkonfigurierten MAC Adresse ausgeliefert werden. Diese MAC Adresse
steht auch auf einem Aufkleber auf der Ethernet Extension.

Die MAC Adresse kann mit :func:`Get Ethernet Status` wieder ausgelesen werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Ethernet Websocket Configuration',
'elements': [('Sockets', 'uint8', 1, 'in', {'range': (0, 7), 'default': 3}),
             ('Port', 'uint16', 1, 'in', {'default': 4280})],
'since_firmware': [2, 2, 0],
'doc': ['af', {
'en':
"""
Sets the Ethernet WebSocket configuration. The first parameter sets the number of socket
connections that are reserved for WebSockets. The range is 0-7. The connections
are shared with the plain sockets. Example: If you set the connections to 3,
there will be 3 WebSocket and 4 plain socket connections available.

The second parameter is the port for the WebSocket connections. The port can
not be the same as the port for the plain socket connections.

The values are stored in the EEPROM and only applied on startup. That means
you have to restart the Master Brick after configuration.

It is recommended to use the Brick Viewer to set the Ethernet configuration.
""",
'de':
"""
Setzt die Ethernet WebSocket-Konfiguration. Der erste Parameter setzt
die Anzahl der Socket-Verbindungen die für WebSockets reserviert werden.
Der mögliche Wertebereich ist 0-7. Die Verbindungen werden zwischen den
normalen Sockets und den WebSockets aufgeteilt. Beispiel: Wenn die Socket-Verbindungen auf 3
gesetzt werden, stehen 3 WebSockets und 4 normale Sockets zur Verfügung.

Der zweite Parameter ist der Port für die WebSocket-Verbindungen. Der Port
kann nicht der gleiche sein wie der Port des normalen Sockets.

Die Werte sind im EEPROM gespeichert und werden nur beim Start angewandt.
Das bedeutet der Master Brick muss nach einer Konfiguration neu gestartet
werden.

Wir empfehlen den Brick Viewer zu verwenden, um die Ethernet Extension zu
konfigurieren.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Ethernet Websocket Configuration',
'elements': [('Sockets', 'uint8', 1, 'out', {'range': (0, 7), 'default': 3}),
             ('Port', 'uint16', 1, 'out', {'default': 4280})],
'since_firmware': [2, 2, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Ethernet Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Ethernet Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Ethernet Authentication Secret',
'elements': [('Secret', 'string', 64, 'in', {'default': ''})],
'since_firmware': [2, 2, 0],
'doc': ['af', {
'en':
"""
Sets the Ethernet authentication secret. The secret can be a string of up to 64
characters. An empty string disables the authentication.

See the :ref:`authentication tutorial <tutorial_authentication>` for more
information.

The secret is stored in the EEPROM and only applied on startup. That means
you have to restart the Master Brick after configuration.

It is recommended to use the Brick Viewer to set the Ethernet authentication secret.

The default value is an empty string (authentication disabled).
""",
'de':
"""
Setzt das Authentifizierungsgeheimnis. Das Geheimnis ist ein String aus bis zu
64 Buchstaben. Ein leerer String deaktiviert die Authentifizierung.

Für mehr Informationen zur Authentifizierung siehe das dazugehörige
:ref:`Tutorial <tutorial_authentication>`.

Das Authentifizierungsgehemnis wird im EEPROM gespeichert und nur beim Start angewandt.
Das bedeutet der Master Brick muss nach einer Konfiguration neu gestartet
werden.

Wir empfehlen den Brick Viewer zu verwenden, um die Authentifizierung der Ethernet
Extension einzurichten.

Der Standardwert ist ein leerer String (Authentifizierung deaktiviert).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Ethernet Authentication Secret',
'elements': [('Secret', 'string', 64, 'out', {'default': ''})],
'since_firmware': [2, 2, 0],
'doc': ['af', {
'en':
"""
Returns the authentication secret as set by
:func:`Set Ethernet Authentication Secret`.
""",
'de':
"""
Gibt das Authentifizierungsgeheimnis zurück, wie von
:func:`Set Ethernet Authentication Secret` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Wifi Authentication Secret',
'elements': [('Secret', 'string', 64, 'in', {'default': ''})],
'since_firmware': [2, 2, 0],
'doc': ['af', {
'en':
"""
Sets the WIFI authentication secret. The secret can be a string of up to 64
characters. An empty string disables the authentication.

See the :ref:`authentication tutorial <tutorial_authentication>` for more
information.

The secret is stored in the EEPROM and only applied on startup. That means
you have to restart the Master Brick after configuration.

It is recommended to use the Brick Viewer to set the WIFI authentication secret.

The default value is an empty string (authentication disabled).
""",
'de':
"""
Setzt das Authentifizierungsgeheimnis. Das Geheimnis ist ein String aus bis zu
64 Buchstaben. Ein leerer String deaktiviert die Authentifizierung.

Für mehr Informationen zur Authentifizierung siehe das dazugehörige
:ref:`Tutorial <tutorial_authentication>`.

Das Authentifizierungsgehemnis wird im EEPROM gespeichert und nur beim Start
angewandt. Das bedeutet der Master Brick muss nach einer Konfiguration neu
gestartet werden.

Wir empfehlen den Brick Viewer zu verwenden, um die Authentifizierung der WIFI
Extension einzurichten.

Der Standardwert ist ein leerer String (Authentifizierung deaktiviert).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Wifi Authentication Secret',
'elements': [('Secret', 'string', 64, 'out', {'default': ''})],
'since_firmware': [2, 2, 0],
'doc': ['af', {
'en':
"""
Returns the authentication secret as set by
:func:`Set Wifi Authentication Secret`.
""",
'de':
"""
Gibt das Authentifizierungsgeheimnis zurück, wie von
:func:`Set Wifi Authentication Secret` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Connection Type',
'elements': [('Connection Type', 'uint8', 1, 'out', {'constant_group': 'Connection Type'})],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Returns the type of the connection over which this function was called.
""",
'de':
"""
Gibt den Typ der Verbingung zurück, über welche diese Funktion aufgerufen wurde.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is Wifi2 Present',
'elements': [('Present', 'bool', 1, 'out', {})],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Returns *true* if the Master Brick is at position 0 in the stack and a WIFI
Extension 2.0 is available.
""",
'de':
"""
Gibt *true* zurück, wenn der Master Brick an Position 0 im Stapel und eine
WIFI Extension 2.0 verfügbar ist.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Start Wifi2 Bootloader',
'elements': [('Result', 'int8', 1, 'out', {})],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Starts the bootloader of the WIFI Extension 2.0. Returns 0 on success.
Afterwards the :func:`Write Wifi2 Serial Port` and :func:`Read Wifi2 Serial Port`
functions can be used to communicate with the bootloader to flash a new
firmware.

The bootloader should only be started over a USB connection. It cannot be
started over a WIFI2 connection, see the :func:`Get Connection Type` function.

It is recommended to use the Brick Viewer to update the firmware of the WIFI
Extension 2.0.
""",
'de':
"""
Startet den Bootloader der WIFI Extension 2.0. Gibt bei Erfolg 0 zurück.
Danach können die :func:`Write Wifi2 Serial Port` und :func:`Read Wifi2 Serial Port`
Funktionen zur Kommunikation mit dem Bootloader verwendet werden, um eine neue
Firmware zu flashen.

Der Bootloader sollte nur über eine USB Verbindung gestartet werden. Er kann
nicht über eine WIFI2 Verbindung gestartet werden, siehe die
:func:`Get Connection Type` Funktion.

Wir empfehlen den Brick Viewer zu verwenden, um die Firmware der WIFI
Extension 2.0 zu aktualisieren.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Write Wifi2 Serial Port',
'elements': [('Data', 'uint8', 60, 'in', {}),
             ('Length', 'uint8', 1, 'in', {'unit': 'Byte', 'range': (0, 60)}),
             ('Result', 'int8', 1, 'out', {})],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Writes up to 60 bytes (number of bytes to be written specified by ``length``)
to the serial port of the bootloader of the WIFI Extension 2.0. Returns 0 on
success.

Before this function can be used the bootloader has to be started using the
:func:`Start Wifi2 Bootloader` function.

It is recommended to use the Brick Viewer to update the firmware of the WIFI
Extension 2.0.
""",
'de':
"""
Schreibt bis zu 60 Bytes (Anzahl zu schreibender Bytes mit ``length`` angeben)
auf die serielle Schnittstelle des Bootloaders der WIFI Extension 2.0. Gibt
bei Erfolg 0 zurück.

Bevor diese Funktion genutzt werden kann muss der Bootloader mit der
:func:`Start Wifi2 Bootloader` Funktion gestartet werden.

Wir empfehlen den Brick Viewer zu verwenden, um die Firmware der WIFI
Extension 2.0 zu aktualisieren.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Read Wifi2 Serial Port',
'elements': [('Length', 'uint8', 1, 'in', {}),
             ('Data', 'uint8', 60, 'out', {'range': (0, 60)}),
             ('Result', 'uint8', 1, 'out', {})],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Reads up to 60 bytes (number of bytes to be read specified by ``length``)
from the serial port of the bootloader of the WIFI Extension 2.0.
Returns the number of actually read bytes.

Before this function can be used the bootloader has to be started using the
:func:`Start Wifi2 Bootloader` function.

It is recommended to use the Brick Viewer to update the firmware of the WIFI
Extension 2.0.
""",
'de':
"""
Liest bis zu 60 Bytes (Anzahl zu lesender Bytes mit ``length`` angegeben) von
der seriellen Schnittstelle des Bootloaders der WIFI Extension 2.0. Gibt die
Anzahl der wirklich gelesenen Bytes zurück.

Bevor diese Funktion genutzt werden kann muss der Bootloader mit der
:func:`Start Wifi2 Bootloader` Funktion gestartet werden.

Wir empfehlen den Brick Viewer zu verwenden, um die Firmware der WIFI
Extension 2.0 zu aktualisieren.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Wifi2 Authentication Secret',
'elements': [('Secret', 'string', 64, 'in', {})],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Sets the WIFI authentication secret. The secret can be a string of up to 64
characters. An empty string disables the authentication. The default value is
an empty string (authentication disabled).

See the :ref:`authentication tutorial <tutorial_authentication>` for more
information.

To apply configuration changes to the WIFI Extension 2.0 the
:func:`Save Wifi2 Configuration` function has to be called and the Master Brick
has to be restarted afterwards.

It is recommended to use the Brick Viewer to configure the WIFI Extension 2.0.
""",
'de':
"""
Setzt das WLAN-Authentifizierungsgeheimnis. Das Geheimnis ist ein String aus
bis zu 64 Buchstaben. Ein leerer String deaktiviert die Authentifizierung. Der
Standardwert ist ein leerer String (Authentifizierung deaktiviert).

Für mehr Informationen zur Authentifizierung siehe das dazugehörige
:ref:`Tutorial <tutorial_authentication>`.

Um Konfigurationsänderungen für die WIFI Extension 2.0 zu übernehmen muss die
:func:`Save Wifi2 Configuration` Funktion aufgerufen und der Master Brick
danach neugestartet werden.

Wir empfehlen den Brick Viewer zu verwenden, um die WIFI Extension 2.0 zu
konfigurieren.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Wifi2 Authentication Secret',
'elements': [('Secret', 'string', 64, 'out', {})],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Returns the WIFI authentication secret as set by
:func:`Set Wifi2 Authentication Secret`.
""",
'de':
"""
Gibt das WLAN-Authentifizierungsgeheimnis zurück, wie von
:func:`Set Wifi2 Authentication Secret` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Wifi2 Configuration',
'elements': [('Port', 'uint16', 1, 'in', {'default': 4223}),
             ('Websocket Port', 'uint16', 1, 'in', {'default': 4280}),
             ('Website Port', 'uint16', 1, 'in', {'default': 80}),
             ('PHY Mode', 'uint8', 1, 'in', {'constant_group': 'Wifi2 PHY Mode'}),
             ('Sleep Mode', 'uint8', 1, 'in', {}), # FIXME: constants?
             ('Website', 'uint8', 1, 'in', {})], # FIXME: constants?
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Sets the general configuration of the WIFI Extension 2.0.

The ``port`` parameter sets the port number that your programm will connect
to.

The ``websocket_port`` parameter sets the WebSocket port number that your
JavaScript programm will connect to.

The ``website_port`` parameter sets the port number for the website of the
WIFI Extension 2.0.

The ``phy_mode`` parameter sets the specific wireless network mode to be used.
Possible values are B, G and N.

The ``sleep_mode`` parameter is currently unused.

The ``website`` parameter is used to enable or disable the web interface of
the WIFI Extension 2.0, which is available from firmware version 2.0.1. Note
that, for firmware version 2.0.3 and older, to disable the the web interface
the ``website_port`` parameter must be set to 1 and greater than 1 to enable
the web interface. For firmware version 2.0.4 and later, setting this parameter
to 1 will enable the web interface and setting it to 0 will disable the web
interface.

To apply configuration changes to the WIFI Extension 2.0 the
:func:`Save Wifi2 Configuration` function has to be called and the Master Brick
has to be restarted afterwards.

It is recommended to use the Brick Viewer to configure the WIFI Extension 2.0.
""",
'de':
"""
Setzt die allgemeine Konfiguration der WIFI Extension 2.0.

Der ``port`` Parameter setzt die Portnummer auf die sich das Anwendungsprogramm
verbindet.

Der ``websocket_port`` Parameter setzt die WebSocket-Portnummer auf die sich das
JavaScript Anwendungsprogramm verbindet.

Der ``website_port`` Parameter setzt die Portnummer für die Webseite der
WIFI Extension 2.0.

Der ``phy_mode`` Parameter setzt den zu verwendenden WLAN-Modus. Mögliche Werte
sinf B, G und N.

Die ``sleep_mode`` und ``website`` Parameter werden momentan nicht verwendet.

Um Konfigurationsänderungen für die WIFI Extension 2.0 zu übernehmen muss die
:func:`Save Wifi2 Configuration` Funktion aufgerufen und der Master Brick
danach neugestartet werden.

Wir empfehlen den Brick Viewer zu verwenden, um die WIFI Extension 2.0 zu
konfigurieren.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Wifi2 Configuration',
'elements': [('Port', 'uint16', 1, 'out', {'default': 4223}),
             ('Websocket Port', 'uint16', 1, 'out', {'default': 4280}),
             ('Website Port', 'uint16', 1, 'out', {'default': 80}),
             ('PHY Mode', 'uint8', 1, 'out', {'constant_group': 'Wifi2 PHY Mode'}),
             ('Sleep Mode', 'uint8', 1, 'out', {}), # FIXME: constants?
             ('Website', 'uint8', 1, 'out', {})], # FIXME: constants?
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Returns the general configuration as set by :func:`Set Wifi2 Configuration`.
""",
'de':
"""
Gibt die allgemeine Konfiguration zurück, wie von :func:`Set Wifi2 Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Wifi2 Status',
'elements': [('Client Enabled', 'bool', 1, 'out', {}),
             ('Client Status', 'uint8', 1, 'out', {'constant_group': 'Wifi2 Client Status'}),
             ('Client IP', 'uint8', 4, 'out', {}),
             ('Client Subnet Mask', 'uint8', 4, 'out', {}),
             ('Client Gateway', 'uint8', 4, 'out', {}),
             ('Client MAC Address', 'uint8', 6, 'out', {}),
             ('Client RX Count', 'uint32', 1, 'out', {'unit': 'Byte'}),
             ('Client TX Count', 'uint32', 1, 'out', {'unit': 'Byte'}),
             ('Client RSSI', 'int8', 1, 'out', {}),
             ('AP Enabled', 'bool', 1, 'out', {}),
             ('AP IP', 'uint8', 4, 'out', {}),
             ('AP Subnet Mask', 'uint8', 4, 'out', {}),
             ('AP Gateway', 'uint8', 4, 'out', {}),
             ('AP MAC Address', 'uint8', 6, 'out', {}),
             ('AP RX Count', 'uint32', 1, 'out', {'unit': 'Byte'}),
             ('AP TX Count', 'uint32', 1, 'out', {'unit': 'Byte'}),
             ('AP Connected Count', 'uint8', 1, 'out', {})],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Returns the client and access point status of the WIFI Extension 2.0.
""",
'de':
"""
Gibt den Client und Access Point Status der WIFI Extension 2.0 zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Wifi2 Client Configuration',
'elements': [('Enable', 'bool', 1, 'in', {'default': True}),
             ('SSID', 'string', 32, 'in', {}),
             ('IP', 'uint8', 4, 'in', {}),
             ('Subnet Mask', 'uint8', 4, 'in', {}),
             ('Gateway', 'uint8', 4, 'in', {}),
             ('MAC Address', 'uint8', 6, 'in', {}),
             ('BSSID', 'uint8', 6, 'in', {})],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Sets the client specific configuration of the WIFI Extension 2.0.

The ``enable`` parameter enables or disables the client part of the
WIFI Extension 2.0.

The ``ssid`` parameter sets the SSID (up to 32 characters) of the access point
to connect to.

If the ``ip`` parameter is set to all zero then ``subnet_mask`` and ``gateway``
parameters are also set to all zero and DHCP is used for IP address configuration.
Otherwise those three parameters can be used to configure a static IP address.
The default configuration is DHCP.

If the ``mac_address`` parameter is set to all zero then the factory MAC
address is used. Otherwise this parameter can be used to set a custom MAC
address.

If the ``bssid`` parameter is set to all zero then WIFI Extension 2.0 will
connect to any access point that matches the configured SSID. Otherwise this
parameter can be used to make the WIFI Extension 2.0 only connect to an
access point if SSID and BSSID match.

To apply configuration changes to the WIFI Extension 2.0 the
:func:`Save Wifi2 Configuration` function has to be called and the Master Brick
has to be restarted afterwards.

It is recommended to use the Brick Viewer to configure the WIFI Extension 2.0.
""",
'de':
"""
Setzt die Client-spezifische Konfiguration der WIFI Extension 2.0.

Der ``enable`` Parameter aktiviert oder deaktiviert den Client-Teil der
WIFI Extension 2.0. Der Standardwert ist *true*.

Der ``ssid`` Parameter die SSID (bis zu 32 Zeichen) des Access Points zu dem
die WLAN Verbindung hergestellt werden soll.

Wenn die ``ip``, ``subnet_mask`` und ``gateway`` Parameter alle auf Null gesetzt
sind, dann wird DHCP verwendet. Andernfalls kann mit diese drei Parametern eine
statische IP Adresse eingestellt werden. Die Standardeinstellung ist DHCP.

Wenn der ``mac_address`` Parameter auf Null gesetzt ist, dann wird die
voreingestellt MAC Adresse verwendet. Andernfalls kann mit diesem Parameter
eine eigene MAC Adresse eingestellt werden.

Wenn der ``bssid`` Parameter auf Null gesetzt ist, dann verbindet sich die
WIFI Extension 2.0 mit einem Access Point wenn die eingestellt SSID
übereinstimmt. Andernfalls kann dieses Parameter verwendet werden, damit sich
die WIFI Extension 2.0 nur dann mit einem Access Point verbindet, wenn SSID
und BSSID übereinstimmen.

Um Konfigurationsänderungen für die WIFI Extension 2.0 zu übernehmen muss die
:func:`Save Wifi2 Configuration` Funktion aufgerufen und der Master Brick
danach neugestartet werden.

Wir empfehlen den Brick Viewer zu verwenden, um die WIFI Extension 2.0 zu
konfigurieren.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Wifi2 Client Configuration',
'elements': [('Enable', 'bool', 1, 'out', {'default': True}),
             ('SSID', 'string', 32, 'out', {}),
             ('IP', 'uint8', 4, 'out', {}),
             ('Subnet Mask', 'uint8', 4, 'out', {}),
             ('Gateway', 'uint8', 4, 'out', {}),
             ('MAC Address', 'uint8', 6, 'out', {}),
             ('BSSID', 'uint8', 6, 'out', {})],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Returns the client configuration as set by :func:`Set Wifi2 Client Configuration`.
""",
'de':
"""
Gibt die Client Konfiguration zurück, wie von
:func:`Set Wifi2 Client Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Wifi2 Client Hostname',
'elements': [('Hostname', 'string', 32, 'in', {})],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Sets the client hostname (up to 32 characters) of the WIFI Extension 2.0. The
hostname will be displayed by access points as the hostname in the DHCP clients
table.

To apply configuration changes to the WIFI Extension 2.0 the
:func:`Save Wifi2 Configuration` function has to be called and the Master Brick
has to be restarted afterwards.

It is recommended to use the Brick Viewer to configure the WIFI Extension 2.0.
""",
'de':
"""
Setzt den Client Hostnamen (bis zu 32 Zeichen) der WIFI Extension 2.0. Der
Hostname wird von Access Points als Hostname in der DHCP Client Tabelle angezeigt.

Um Konfigurationsänderungen für die WIFI Extension 2.0 zu übernehmen muss die
:func:`Save Wifi2 Configuration` Funktion aufgerufen und der Master Brick
danach neugestartet werden.

Wir empfehlen den Brick Viewer zu verwenden, um die WIFI Extension 2.0 zu
konfigurieren.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Wifi2 Client Hostname',
'elements': [('Hostname', 'string', 32, 'out', {})],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Returns the client hostname as set by :func:`Set Wifi2 Client Hostname`.
""",
'de':
"""
Gibt den Client Hostnamen zurück, wie von :func:`Set Wifi2 Client Hostname` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Wifi2 Client Password',
'elements': [('Password', 'string', 64, 'in', {})],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Sets the client password (up to 63 chars) for WPA/WPA2 encryption.

To apply configuration changes to the WIFI Extension 2.0 the
:func:`Save Wifi2 Configuration` function has to be called and the Master Brick
has to be restarted afterwards.

It is recommended to use the Brick Viewer to configure the WIFI Extension 2.0.
""",
'de':
"""
Setzt das Client-Passwort (bis zu 63 Zeichen) für WPA/WPA2 Verschlüsselung.

Um Konfigurationsänderungen für die WIFI Extension 2.0 zu übernehmen muss die
:func:`Save Wifi2 Configuration` Funktion aufgerufen und der Master Brick
danach neugestartet werden.

Wir empfehlen den Brick Viewer zu verwenden, um die WIFI Extension 2.0 zu
konfigurieren.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Wifi2 Client Password',
'elements': [('Password', 'string', 64, 'out', {})],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Returns the client password as set by :func:`Set Wifi2 Client Password`.

.. note::
 Since WIFI Extension 2.0 firmware version 2.1.3 the password is not
 returned anymore.
""",
'de':
"""
Gibt das Client-Passwort zurück, wie von :func:`Set Wifi2 Client Password` gesetzt.

.. note::
 Seit WIFI Extension 2.0 Firmware Version 2.1.3 wird das Passwort
 nicht mehr zurückgegeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Wifi2 AP Configuration',
'elements': [('Enable', 'bool', 1, 'in', {'default': True}),
             ('SSID', 'string', 32, 'in', {}),
             ('IP', 'uint8', 4, 'in', {'default': [0, 0, 0, 0]}),
             ('Subnet Mask', 'uint8', 4, 'in', {}),
             ('Gateway', 'uint8', 4, 'in', {}),
             ('Encryption', 'uint8', 1, 'in', {'constant_group': 'Wifi2 AP Encryption', 'default': 4}),
             ('Hidden', 'bool', 1, 'in', {'default': False}),
             ('Channel', 'uint8', 1, 'in', {'default': 1}),
             ('MAC Address', 'uint8', 6, 'in', {})],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Sets the access point specific configuration of the WIFI Extension 2.0.

The ``enable`` parameter enables or disables the access point part of the
WIFI Extension 2.0.

The ``ssid`` parameter sets the SSID (up to 32 characters) of the access point.

If the ``ip`` parameter is set to all zero then ``subnet_mask`` and ``gateway``
parameters are also set to all zero and DHCP is used for IP address configuration.
Otherwise those three parameters can be used to configure a static IP address.
The default configuration is DHCP.

The ``encryption`` parameter sets the encryption mode to be used. Possible
values are Open (no encryption), WEP or WPA/WPA2 PSK.
Use the :func:`Set Wifi2 AP Password` function to set the encryption
password.

The ``hidden`` parameter makes the access point hide or show its SSID.

The ``channel`` parameter sets the channel (1 to 13) of the access point.

If the ``mac_address`` parameter is set to all zero then the factory MAC
address is used. Otherwise this parameter can be used to set a custom MAC
address.

To apply configuration changes to the WIFI Extension 2.0 the
:func:`Save Wifi2 Configuration` function has to be called and the Master Brick
has to be restarted afterwards.

It is recommended to use the Brick Viewer to configure the WIFI Extension 2.0.
""",
'de':
"""
Setzt die Access-Point-spezifische Konfiguration der WIFI Extension 2.0.

Der ``enable`` Parameter aktiviert oder deaktiviert den Access-Point-Teil der
WIFI Extension 2.0. Der Standardwert ist *true*.

Der ``ssid`` Parameter die SSID (bis zu 32 Zeichen) des Access Points.

Wenn die ``ip``, ``subnet_mask`` und ``gateway`` Parameter alle auf Null gesetzt
sind, dann wird ein DHCP Server aktiviert. Andernfalls kann mit diese drei
Parametern eine statische IP Adresse eingestellt werden. Die Standardeinstellung
ist DHCP.

Der ``encryption`` Parameter legt den Verschlüsselungsmodus fest. Mögliche Werte
sind Open (keine  Verschlüsselung), WEP oder WPA/WPA2 PSK.
Mit der :func:`Set Wifi2 AP Password` Kann das
Verschlüsselungspasswort gesetzt werden.

Der ``hidden`` Parameter legt fest, oder der Access Point seine SSID versteckt
oder zeigt.

Der ``channel`` Parameter gibt den Kanal (1 to 13) des Access Points and.

Wenn der ``mac_address`` Parameter auf Null gesetzt ist, dann wird die
voreingestellt MAC Adresse verwendet. Andernfalls kann mit diesem Parameter
eine eigene MAC Adresse eingestellt werden.

Um Konfigurationsänderungen für die WIFI Extension 2.0 zu übernehmen muss die
:func:`Save Wifi2 Configuration` Funktion aufgerufen und der Master Brick
danach neugestartet werden.

Wir empfehlen den Brick Viewer zu verwenden, um die WIFI Extension 2.0 zu
konfigurieren.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Wifi2 AP Configuration',
'elements': [('Enable', 'bool', 1, 'out', {'default': True}),
             ('SSID', 'string', 32, 'out', {}),
             ('IP', 'uint8', 4, 'out', {'default': [0, 0, 0, 0]}),
             ('Subnet Mask', 'uint8', 4, 'out', {}),
             ('Gateway', 'uint8', 4, 'out', {}),
             ('Encryption', 'uint8', 1, 'out', {'constant_group': 'Wifi2 AP Encryption', 'default': 4}),
             ('Hidden', 'bool', 1, 'out', {'default': False}),
             ('Channel', 'uint8', 1, 'out', {'default': 1}),
             ('MAC Address', 'uint8', 6, 'out', {})],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Returns the access point configuration as set by :func:`Set Wifi2 AP Configuration`.
""",
'de':
"""
Gibt die Access-Point-Konfiguration zurück, wie von
:func:`Set Wifi2 AP Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Wifi2 AP Password',
'elements': [('Password', 'string', 64, 'in', {})],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Sets the access point password (at least 8 and up to 63 chars) for the configured encryption
mode, see :func:`Set Wifi2 AP Configuration`.

To apply configuration changes to the WIFI Extension 2.0 the
:func:`Save Wifi2 Configuration` function has to be called and the Master Brick
has to be restarted afterwards.

It is recommended to use the Brick Viewer to configure the WIFI Extension 2.0.
""",
'de':
"""
Setzt das Access-Point-Passwort (mindestens 8 und bis zu 63 Zeichen) für den eingestellten
Verschlüsselungsmodus, siehe :func:`Set Wifi2 AP Configuration`.

Um Konfigurationsänderungen für die WIFI Extension 2.0 zu übernehmen muss die
:func:`Save Wifi2 Configuration` Funktion aufgerufen und der Master Brick
danach neugestartet werden.

Wir empfehlen den Brick Viewer zu verwenden, um die WIFI Extension 2.0 zu
konfigurieren.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Wifi2 AP Password',
'elements': [('Password', 'string', 64, 'out', {})],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Returns the access point password as set by :func:`Set Wifi2 AP Password`.

.. note::
 Since WIFI Extension 2.0 firmware version 2.1.3 the password is not
 returned anymore.
""",
'de':
"""
Gibt das Access-Point-Passwort zurück, wie von :func:`Set Wifi2 AP Password` gesetzt.

.. note::
 Seit WIFI Extension 2.0 Firmware Version 2.1.3 wird das Passwort
 nicht mehr zurückgegeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Save Wifi2 Configuration',
'elements': [('Result', 'uint8', 1, 'out', {})],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
All configuration functions for the WIFI Extension 2.0 do not change the
values permanently. After configuration this function has to be called to
permanently store the values.

The values are stored in the EEPROM and only applied on startup. That means
you have to restart the Master Brick after configuration.
""",
'de':
"""
Alle Konfigurationsfunktionen der WIFI Extension 2.0 ändern die Werte nicht
dauerhaft. Nach einer Konfiguration muss diese Funktion aufgerufen werden, um
die Werte dauerhaft zu speichern.

Die Werte sind im EEPROM gespeichert und werden nur beim Start angewandt.
Das bedeutet der Master Brick muss nach einer Konfiguration neu gestartet
werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Wifi2 Firmware Version',
'elements': [('Firmware Version', 'uint8', 3, 'out',  [{'name': 'Major'}, {'name': 'Minor'}, {'name': 'Revision'}])],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Returns the current version of the WIFI Extension 2.0 firmware.
""",
'de':
"""
Gibt die aktuelle Version der WIFI Extension 2.0 Firmware zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Enable Wifi2 Status LED',
'elements': [],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Turns the green status LED of the WIFI Extension 2.0 on.
""",
'de':
"""
Aktiviert die grüne Status LED der WIFI Extension 2.0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Disable Wifi2 Status LED',
'elements': [],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Turns the green status LED of the WIFI Extension 2.0 off.
""",
'de':
"""
Deaktiviert die grüne Status LED der WIFI Extension 2.0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is Wifi2 Status LED Enabled',
'elements': [('Enabled', 'bool', 1, 'out', {})],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Returns *true* if the green status LED of the WIFI Extension 2.0 is turned on.
""",
'de':
"""
Gibt *true* zurück falls die grüne Status LED der WIFI Extension 2.0 aktiviert ist.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Wifi2 Mesh Configuration',
'elements': [('Enable', 'bool', 1, 'in', {'default': False}),
             ('Root IP', 'uint8', 4, 'in', {'default': [0, 0, 0, 0]}),
             ('Root Subnet Mask', 'uint8', 4, 'in', {}),
             ('Root Gateway', 'uint8', 4, 'in', {}),
             ('Router BSSID', 'uint8', 6, 'in', {}),
             ('Group ID', 'uint8', 6, 'in', {}),
             ('Group SSID Prefix', 'string', 16, 'in', {}),
             ('Gateway IP', 'uint8', 4, 'in', {}),
             ('Gateway Port', 'uint16', 1, 'in', {})],
'since_firmware': [2, 4, 2],
'doc': ['af', {
'en':
"""
Requires WIFI Extension 2.0 firmware 2.1.0.

Sets the mesh specific configuration of the WIFI Extension 2.0.

The ``enable`` parameter enables or disables the mesh part of the
WIFI Extension 2.0. The mesh part cannot be
enabled together with the client and access-point part.

If the ``root_ip`` parameter is set to all zero then ``root_subnet_mask``
and ``root_gateway`` parameters are also set to all zero and DHCP is used for
IP address configuration. Otherwise those three parameters can be used to
configure a static IP address. The default configuration is DHCP.

If the ``router_bssid`` parameter is set to all zero then the information is
taken from Wi-Fi scan when connecting the SSID as set by
:func:`Set Wifi2 Mesh Router SSID`. This only works if the the SSID is not hidden.
In case the router has hidden SSID this parameter must be specified, otherwise
the node will not be able to reach the mesh router.

The ``group_id`` and the ``group_ssid_prefix`` parameters identifies a
particular mesh network and nodes configured with same ``group_id`` and the
``group_ssid_prefix`` are considered to be in the same mesh network.

The ``gateway_ip`` and the ``gateway_port`` parameters specifies the location
of the brickd that supports mesh feature.

To apply configuration changes to the WIFI Extension 2.0 the
:func:`Save Wifi2 Configuration` function has to be called and the Master Brick
has to be restarted afterwards.

It is recommended to use the Brick Viewer to configure the WIFI Extension 2.0.
""",
'de':
"""
Benötigt WIFI Extension 2.0 Firmware 2.1.0.

Set die Mesh-Konfiguration der WIFI Extension 2.0.

Der ``enable`` Parameter aktiviert oder deaktiviert den Mesh-Teil der
WIFI Extension 2.0. Der Mesh-Teil kann nicht
zusammen mit dem Client- und Access-Point-Teil aktiviert werden.

Wenn die ``root_ip``, ``root_subnet_mask`` und ``root_gateway`` Parameter alle
auf Null gesetzt sind, dann wird DHCP verwendet. Andernfalls kann mit diese
drei Parametern eine statische IP Adresse eingestellt werden. Die
Standardeinstellung ist DHCP.

Wenn der ``router_bssid`` Parameter auf Null gesetzt ist, dann verbindet sich
die WIFI Extension 2.0 mit einem Access Point wenn die eingestellt SSID
übereinstimmt, siehe :func:`Set Wifi2 Mesh Router SSID`. Andernfalls kann dieses
Parameter verwendet werden, damit sich die WIFI Extension 2.0 nur dann mit
einem Access Point verbindet, wenn SSID und BSSID übereinstimmen. Die BSSID
kann auch verwendet werden, um eine Verbindung mit einer verstecken SSID
herzustellen.

Die ``group_id`` und ``group_ssid_prefix`` Parameter identifizieren in bestimmtes
Mesh-Netzwerk und alle WIFI Extension 2.0 mit der gleichen Gruppeneinstellung
gehören um gleichen Mesh-Netzwerk.

Die ``gateway_ip`` und ``gateway_port`` Parameter geben an, wie der Mesh-Gateway
(brickd) erreicht werden kann.

Um Konfigurationsänderungen für die WIFI Extension 2.0 zu übernehmen muss die
:func:`Save Wifi2 Configuration` Funktion aufgerufen und der Master Brick
danach neugestartet werden.

Wir empfehlen den Brick Viewer zu verwenden, um die WIFI Extension 2.0 zu
konfigurieren.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Wifi2 Mesh Configuration',
'elements': [('Enable', 'bool', 1, 'out', {'default': False}),
             ('Root IP', 'uint8', 4, 'out', {'default': [0, 0, 0, 0]}),
             ('Root Subnet Mask', 'uint8', 4, 'out', {}),
             ('Root Gateway', 'uint8', 4, 'out', {}),
             ('Router BSSID', 'uint8', 6, 'out', {}),
             ('Group ID', 'uint8', 6, 'out', {}),
             ('Group SSID Prefix', 'string', 16, 'out', {}),
             ('Gateway IP', 'uint8', 4, 'out', {}),
             ('Gateway Port', 'uint16', 1, 'out', {})],
'since_firmware': [2, 4, 2],
'doc': ['af', {
'en':
"""
Requires WIFI Extension 2.0 firmware 2.1.0.

Returns the mesh configuration as set by :func:`Set Wifi2 Mesh Configuration`.
""",
'de':
"""
Benötigt WIFI Extension 2.0 Firmware 2.1.0.

Gibt das Mesh Konfiguration zurück, wie von :func:`Set Wifi2 Mesh Configuration` gesetzt.
"""
}]
})

# FIXME: Espressif mesh library supports router SSID with maximum length of 31 characters at the moment
com['packets'].append({
'type': 'function',
'name': 'Set Wifi2 Mesh Router SSID',
'elements': [('SSID', 'string', 32, 'in', {})],
'since_firmware': [2, 4, 2],
'doc': ['af', {
'en':
"""
Requires WIFI Extension 2.0 firmware 2.1.0.

Sets the mesh router SSID of the WIFI Extension 2.0.
It is used to specify the mesh router to connect to.

Note that even though in the argument of this function a 32 characters long SSID
is allowed, in practice valid SSID should have a maximum of 31 characters. This
is due to a bug in the mesh library that we use in the firmware of the extension.

To apply configuration changes to the WIFI Extension 2.0 the
:func:`Save Wifi2 Configuration` function has to be called and the Master Brick
has to be restarted afterwards.

It is recommended to use the Brick Viewer to configure the WIFI Extension 2.0.
""",
'de':
"""
Benötigt WIFI Extension 2.0 Firmware 2.1.0.

Setzt die Mesh-Router-SSID der WIFI Extension 2.0. Diese wird verwendet um den
Mesh Router festzulegen.

Zu beachten ist, dass zwar 32 Zeichen als SSID übergeben werden können, aber im
Moment davon nur die ersten 31 Zeichen genutzt werden bedingt durch einen Bug
in der verwendeten Mesh-Bibliothek.

Um Konfigurationsänderungen für die WIFI Extension 2.0 zu übernehmen muss die
:func:`Save Wifi2 Configuration` Funktion aufgerufen und der Master Brick
danach neugestartet werden.

Wir empfehlen den Brick Viewer zu verwenden, um die WIFI Extension 2.0 zu
konfigurieren.
"""
}]
})

# FIXME: Espressif mesh library supports router SSID with maximum length of 31 characters at the moment
com['packets'].append({
'type': 'function',
'name': 'Get Wifi2 Mesh Router SSID',
'elements': [('SSID', 'string', 32, 'out', {})],
'since_firmware': [2, 4, 2],
'doc': ['af', {
'en':
"""
Requires WIFI Extension 2.0 firmware 2.1.0.

Returns the mesh router SSID as set by :func:`Set Wifi2 Mesh Router SSID`.
""",
'de':
"""
Benötigt WIFI Extension 2.0 Firmware 2.1.0.

Gibt das Mesh-Router-SSID zurück, wie von :func:`Set Wifi2 Mesh Router SSID` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Wifi2 Mesh Router Password',
'elements': [('Password', 'string', 64, 'in', {})],
'since_firmware': [2, 4, 2],
'doc': ['af', {
'en':
"""
Requires WIFI Extension 2.0 firmware 2.1.0.

Sets the mesh router password (up to 64 characters) for WPA/WPA2 encryption.
The password will be used to connect to the mesh router.

To apply configuration changes to the WIFI Extension 2.0 the
:func:`Save Wifi2 Configuration` function has to be called and the Master Brick
has to be restarted afterwards.

It is recommended to use the Brick Viewer to configure the WIFI Extension 2.0.
""",
'de':
"""
Benötigt WIFI Extension 2.0 Firmware 2.1.0.

Setzt das Mesh-Router-Passwort (bis zu 64 Zeichen) für WPA/WPA2 Verschlüsselung.
Das Password wird für die Verbindung zum Mesh Router verwendet.

Um Konfigurationsänderungen für die WIFI Extension 2.0 zu übernehmen muss die
:func:`Save Wifi2 Configuration` Funktion aufgerufen und der Master Brick
danach neugestartet werden.

Wir empfehlen den Brick Viewer zu verwenden, um die WIFI Extension 2.0 zu
konfigurieren.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Wifi2 Mesh Router Password',
'elements': [('Password', 'string', 64, 'out', {})],
'since_firmware': [2, 4, 2],
'doc': ['af', {
'en':
"""
Requires WIFI Extension 2.0 firmware 2.1.0.

Returns the mesh router password as set by :func:`Set Wifi2 Mesh Router Password`.
""",
'de':
"""
Benötigt WIFI Extension 2.0 Firmware 2.1.0.

Gibt das Mesh-Router-Password zurück, wie von :func:`Set Wifi2 Mesh Router Password` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Wifi2 Mesh Common Status',
'elements': [('Status', 'uint8', 1, 'out', {'constant_group': 'Wifi2 Mesh Status'}),
             ('Root Node', 'bool', 1, 'out', {}),
             ('Root Candidate', 'bool', 1, 'out', {}),
             ('Connected Nodes', 'uint16', 1, 'out', {}),
             ('RX Count', 'uint32', 1, 'out', {'unit': 'Byte'}),
             ('TX Count', 'uint32', 1, 'out', {'unit': 'Byte'})],
'since_firmware': [2, 4, 2],
'doc': ['af', {
'en':
"""
Requires WIFI Extension 2.0 firmware 2.1.0.

Returns the common mesh status of the WIFI Extension 2.0.
""",
'de':
"""
Benötigt WIFI Extension 2.0 Firmware 2.1.0.

Gibt den allgemeinen Mesh-Status der WIFI Extension 2.0 zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Wifi2 Mesh Client Status',
'elements': [('Hostname', 'string', 32, 'out', {}),
             ('IP', 'uint8', 4, 'out', {}),
             ('Subnet Mask', 'uint8', 4, 'out', {}),
             ('Gateway', 'uint8', 4, 'out', {}),
             ('MAC Address', 'uint8', 6, 'out', {})],
'since_firmware': [2, 4, 2],
'doc': ['af', {
'en':
"""
Requires WIFI Extension 2.0 firmware 2.1.0.

Returns the mesh client status of the WIFI Extension 2.0.
""",
'de':
"""
Benötigt WIFI Extension 2.0 Firmware 2.1.0.

Gibt den Mesh-Client-Status der WIFI Extension 2.0 zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Wifi2 Mesh AP Status',
'elements': [('SSID', 'string', 32, 'out', {}),
             ('IP', 'uint8', 4, 'out', {}),
             ('Subnet Mask', 'uint8', 4, 'out', {}),
             ('Gateway', 'uint8', 4, 'out', {}),
             ('MAC Address', 'uint8', 6, 'out', {})],
'since_firmware': [2, 4, 2],
'doc': ['af', {
'en':
"""
Requires WIFI Extension 2.0 firmware 2.1.0.

Returns the mesh AP status of the WIFI Extension 2.0.
""",
'de':
"""
Benötigt WIFI Extension 2.0 Firmware 2.1.0.

Gibt den Mesh-AP-Status der WIFI Extension 2.0 zurück.
"""
}]
})

com['examples'].append({
'name': 'Stack Status',
'functions': [('getter', ('Get Stack Voltage', 'stack voltage'), [(('Stack Voltage', 'Stack Voltage'), 'uint16', 1, 1000.0, 'V', None)], []),
              ('getter', ('Get Stack Current', 'stack current'), [(('Stack Current', 'Stack Current'), 'uint16', 1, 1000.0, 'A', None)], [])]
})

voltage_channel = oh_generic_old_style_channel('Stack Voltage', 'Stack Voltage', 'SmartHomeUnits.VOLT', divisor=1000.0)
voltage_channel['callbacks'][0]['transform'] = 'new QuantityType<>(voltage{divisor}, {unit})'
current_channel = oh_generic_old_style_channel('Stack Current', 'Stack Current', 'SmartHomeUnits.AMPERE', divisor=1000.0)
current_channel['callbacks'][0]['transform'] = 'new QuantityType<>(current{divisor}, {unit})'

com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'params': [],
    'channels': [voltage_channel, current_channel],
    'channel_types': [
        oh_generic_channel_type('Stack Voltage', 'Number:ElectricPotential', 'Stack Voltage',
            update_style='Callback Period',
            description='The stack voltage in V. The stack voltage is the voltage that is supplied via the stack, i.e. it is given by a Step-Down or Step-Up Power Supply.',
            read_only=True,
            pattern='%.3f %unit%'),
        oh_generic_channel_type('Stack Current', 'Number:ElectricCurrent', 'Stack Current',
            update_style='Callback Period',
            description='The stack current in A. The stack current is the current that is drawn via the stack, i.e. it is given by a Step-Down or Step-Up Power Supply.',
            read_only=True,
            pattern='%.3f %unit%'),
    ],
    'actions': [
        'Get Stack Voltage',
        'Get Stack Current',
        'Get Extension Type',

        'Is Chibi Present',
        'Get Chibi Address',
        'Get Chibi Master Address',
        'Get Chibi Slave Address',
        'Get Chibi Signal Strength',
        'Get Chibi Error Log',
        'Get Chibi Frequency',
        'Get Chibi Channel',

        'Is RS485 Present',
        'Get RS485 Address',
        'Get RS485 Slave Address',
        'Get RS485 Error Log',
        'Get RS485 Configuration',

        'Is Wifi Present',
        'Get Wifi Configuration',
        'Get Wifi Encryption',
        'Get Wifi Status',
        'Refresh Wifi Status',
        'Get Wifi Certificate',
        'Get Wifi Power Mode',
        'Get Wifi Buffer Info',
        'Get Wifi Regulatory Domain',
        'Get Long Wifi Key',
        'Get Wifi Hostname',
        'Get Wifi Authentication Secret',

        'Get USB Voltage',

        'Is Ethernet Present',
        'Get Ethernet Configuration',
        'Get Ethernet Status',
        'Get Ethernet Websocket Configuration',
        'Get Ethernet Authentication Secret',

        'Get Connection Type',

        'Is Wifi2 Present',
        'Get Wifi2 Authentication Secret',
        'Get Wifi2 Configuration',
        'Get Wifi2 Status',
        'Get Wifi2 Client Configuration',
        'Get Wifi2 Client Hostname',
        'Get Wifi2 AP Configuration',
        'Get Wifi2 Firmware Version',
        'Enable Wifi2 Status LED',
        'Disable Wifi2 Status LED',
        'Is Wifi2 Status LED Enabled',
        'Get Wifi2 Mesh Configuration',
        'Get Wifi2 Mesh Router SSID',
        'Get Wifi2 Mesh Common Status',
        'Get Wifi2 Mesh Client Status',
        'Get Wifi2 Mesh AP Status',
    ]
}
