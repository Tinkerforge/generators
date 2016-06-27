# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Master Brick communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 4],
    'category': 'Brick',
    'device_identifier': 13,
    'name': ('Master', 'Master', 'Master Brick'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Basis to build stacks and has 4 Bricklet ports',
        'de': 'Grundlage um Stapel zu bauen und bietet 4 Bricklet Anschlüsse'
    },
    'released': True,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Get Stack Voltage',
'elements': [('Voltage', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the stack voltage in mV. The stack voltage is the
voltage that is supplied via the stack, i.e. it is given by a 
Step-Down or Step-Up Power Supply.
""",
'de':
"""
Gibt die Spannung des Stapels in mV zurück. Diese Spannung wird über
den Stapel verteilt und kann zum Beispiel über eine Step-Down oder
Step-Up Power Supply eingespeist werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Stack Current',
'elements': [('Current', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the stack current in mA. The stack current is the
current that is drawn via the stack, i.e. it is given by a
Step-Down or Step-Up Power Supply.
""",
'de':
"""
Gibt den Stromverbrauch des Stapels in mA zurück. Der angegebene Strom
bezieht sich auf den Stromverbrauch der am Stapel angeschlossenen Verbraucher.
Die Speisung kann z.B. über eine Step-Down oder Step-Up Power Supply erfolgen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Extension Type',
'elements': [('Extension', 'uint8', 1, 'in'),
             ('Exttype', 'uint32', 1, 'in', ('Extension Type', [('Chibi', 1),
                                                                ('RS485', 2),
                                                                ('Wifi', 3),
                                                                ('Ethernet', 4),
                                                                ('Wifi2', 5)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Writes the extension type to the EEPROM of a specified extension. 
The extension is either 0 or 1 (0 is the on the bottom, 1 is the one on top,
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
Die Extension kann entweder 0 oder 1 sein (0 ist an der Unterseite, 1
auf der Oberseite, wenn nur eine Extension verfügbar ist, ist 0 zu verwenden)

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
'elements': [('Extension', 'uint8', 1, 'in'),
             ('Exttype', 'uint32', 1, 'out', ('Extension Type', [('Chibi', 1),
                                                                 ('RS485', 2),
                                                                 ('Wifi', 3),
                                                                 ('Ethernet', 4),
                                                                 ('Wifi2', 5)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the type for a given extension as set by :func:`SetExtensionType`.
""",
'de':
"""
Gibt den Typ der angegebenen Extension zurück, wie von :func:`SetExtensionType`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is Chibi Present',
'elements': [('Present', 'bool', 1, 'out')],
'since_firmware': [1, 1, 0],
'doc': ['af', {
'en':
"""
Returns *true* if a Chibi Extension is available to be used by the Master Brick.
""",
'de':
"""
Gibt zurück ob eine Chibi Extension zur Nutzung durch den Master Brick
verfügbar ist.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Chibi Address',
'elements': [('Address', 'uint8', 1, 'in')],
'since_firmware': [1, 1, 0],
'doc': ['af', {
'en':
"""
Sets the address (1-255) belonging to the Chibi Extension.

It is possible to set the address with the Brick Viewer and it will be 
saved in the EEPROM of the Chibi Extension, it does not
have to be set on every startup.
""",
'de':
"""
Setzt die zugehörige Adresse (1-255) der Chibi Extension.

Es ist möglich die Adresse mit dem Brick Viewer zu setzen und diese
wird im EEPROM der Chibi Extension abgespeichert. Ein Setzen bei
jedem Start ist daher nicht notwendig.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Chibi Address',
'elements': [('Address', 'uint8', 1, 'out')],
'since_firmware': [1, 1, 0],
'doc': ['af', {
'en':
"""
Returns the address as set by :func:`SetChibiAddress`.
""",
'de':
"""
Gibt die Adresse zurück, wie von :func:`SetChibiAddress` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Chibi Master Address',
'elements': [('Address', 'uint8', 1, 'in')],
'since_firmware': [1, 1, 0],
'doc': ['af', {
'en':
"""
Sets the address (1-255) of the Chibi Master. This address is used if the
Chibi Extension is used as slave (i.e. it does not have a USB connection).

It is possible to set the address with the Brick Viewer and it will be 
saved in the EEPROM of the Chibi Extension, it does not
have to be set on every startup.
""",
'de':
"""
Setzt die Adresse (1-255) des Chibi Master. Diese Adresse wird verwendet
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
'elements': [('Address', 'uint8', 1, 'out')],
'since_firmware': [1, 1, 0],
'doc': ['af', {
'en':
"""
Returns the address as set by :func:`SetChibiMasterAddress`.
""",
'de':
"""
Gibt die Adresse zurück, wie von :func:`SetChibiMasterAddress` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Chibi Slave Address',
'elements': [('Num', 'uint8', 1, 'in'),
             ('Address', 'uint8', 1, 'in')],
'since_firmware': [1, 1, 0],
'doc': ['af', {
'en':
"""
Sets up to 254 slave addresses. Valid addresses are in range 1-255. 0 has a
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
Setzt bis zu 254 Slave Adressen. Gültige Adressen sind 1-255. 0 hat eine
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
'elements': [('Num', 'uint8', 1, 'in'),
             ('Address', 'uint8', 1, 'out')],
'since_firmware': [1, 1, 0],
'doc': ['af', {
'en':
"""
Returns the slave address for a given :param:`num` as set by
:func:`SetChibiSlaveAddress`.
""",
'de':
"""
Gibt die Slave Adresse für eine Adressnummerierung (mittels :param:`num` Parameter)
zurück, wie von :func:`SetChibiSlaveAddress` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Chibi Signal Strength',
'elements': [('Signal Strength', 'uint8', 1, 'out')],
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
'elements': [('Underrun', 'uint16', 1, 'out'),
             ('CRC Error', 'uint16', 1, 'out'),
             ('No Ack', 'uint16', 1, 'out'),
             ('Overflow', 'uint16', 1, 'out')],
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
'elements': [('Frequency', 'uint8', 1, 'in', ('Chibi Frequency', [('OQPSK 868 MHz', 0),
                                                                  ('OQPSK 915 MHz', 1),
                                                                  ('OQPSK 780 MHz', 2),
                                                                  ('BPSK40 915 MHz', 3)]))],
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
'elements': [('Frequency', 'uint8', 1, 'out', ('Chibi Frequency', [('OQPSK 868 MHz', 0),
                                                                   ('OQPSK 915 MHz', 1),
                                                                   ('OQPSK 780 MHz', 2),
                                                                   ('BPSK40 915 MHz', 3)]))],
'since_firmware': [1, 1, 0],
'doc': ['af', {
'en':
"""
Returns the frequency value as set by :func:`SetChibiFrequency`.
""",
'de':
"""
Gibt den Frequenzbereich zurück, wie von :func:`SetChibiFrequency` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Chibi Channel',
'elements': [('Channel', 'uint8', 1, 'in')],
'since_firmware': [1, 1, 0],
'doc': ['af', {
'en':
"""
Sets the channel used by the Chibi Extension. Possible channels are
different for different frequencies:

.. csv-table::
 :header: "Frequency",             "Possible Channels"
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
 :header: "Frequenzbereich",             "Mögliche Kanäle"
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
'elements': [('Channel', 'uint8', 1, 'out')],
'since_firmware': [1, 1, 0],
'doc': ['af', {
'en':
"""
Returns the channel as set by :func:`SetChibiChannel`.
""",
'de':
"""
Gibt den Kanal zurück, wie von :func:`SetChibiChannel` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Is RS485 Present',
'elements': [('Present', 'bool', 1, 'out')],
'since_firmware': [1, 2, 0],
'doc': ['af', {
'en':
"""
Returns *true* if a RS485 Extension is available to be used by the Master Brick.
""",
'de':
"""
Gibt zurück ob eine RS485 Extension zur Nutzung durch den Master Brick
verfügbar ist.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Set RS485 Address',
'elements': [('Address', 'uint8', 1, 'in')],
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
'elements': [('Address', 'uint8', 1, 'out')],
'since_firmware': [1, 2, 0],
'doc': ['af', {
'en':
"""
Returns the address as set by :func:`SetRS485Address`.
""",
'de':
"""
Gibt die Adresse zurück, wie von :func:`SetRS485Address` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Set RS485 Slave Address',
'elements': [('Num', 'uint8', 1, 'in'),
             ('Address', 'uint8', 1, 'in')],
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
'elements': [('Num', 'uint8', 1, 'in'),
             ('Address', 'uint8', 1, 'out')],
'since_firmware': [1, 2, 0],
'doc': ['af', {
'en':
"""
Returns the slave address for a given ``num`` as set by
:func:`SetRS485SlaveAddress`.
""",
'de':
"""
Gibt die Slave Adresse für eine Adressnummerierung (mittels ``num`` Parameter)
zurück, wie von :func:`SetRS485SlaveAddress` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Get RS485 Error Log',
'elements': [('CRC Error', 'uint16', 1, 'out')],
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
'elements': [('Speed', 'uint32', 1, 'in'),
             ('Parity', 'char', 1, 'in', ('RS485 Parity', [('None', 'n'),
                                                           ('Even', 'e'),
                                                           ('Odd', 'o')])),
             ('Stopbits', 'uint8', 1, 'in')],
'since_firmware': [1, 2, 0],
'doc': ['af', {
'en':
"""
Sets the configuration of the RS485 Extension. Speed is given in baud. The
Master Brick will try to match the given baud rate as exactly as possible.
The maximum recommended baud rate is 2000000 (2Mbit/s).
Possible values for parity are 'n' (none), 'e' (even) and 'o' (odd).
Possible values for stop bits are 1 and 2.

If your RS485 is unstable (lost messages etc.), the first thing you should
try is to decrease the speed. On very large bus (e.g. 1km), you probably
should use a value in the range of 100000 (100kbit/s).

The values are stored in the EEPROM and only applied on startup. That means
you have to restart the Master Brick after configuration.
""",
'de':
"""
Setzt die Schnittstellenkonfiguration der RS485 Extension. Die Geschwindigkeit
wird in Baud angegeben. Der Master Brick versucht die vorgegebene Baudrate so
genau wie möglich zu erreichen. Die maximale empfohlene Baudrate ist 2000000
(2Mbit/s). Mögliche Werte für die Parität sind 'n' (keine), 'e' (gerade) und
'o' (ungerade). Mögliche Werte für Stoppbits sind 1 und 2.

Wenn die RS485 Kommunikation instabil ist (verlorene Nachrichten etc.), sollte
zuerst die Baudrate verringert werden. Sehr lange Busleitungen (z.B. 1km)
sollten möglichst Werte im Bereich von 100000 (100kbit/s) verwenden.

Die Werte sind im EEPROM gespeichert und werden nur beim Start angewandt. Dass
bedeutet, der Master Brick muss nach einer Konfiguration neu gestartet werden.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Get RS485 Configuration',
'elements': [('Speed', 'uint32', 1, 'out'),
             ('Parity', 'char', 1, 'out', ('RS485 Parity', [('None', 'n'),
                                                            ('Even', 'e'),
                                                            ('Odd', 'o')])),
             ('Stopbits', 'uint8', 1, 'out')],
'since_firmware': [1, 2, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`SetRS485Configuration`.
""",
'de':
"""
Gibt die Schnittstellenkonfiguration zurück, wie von :func:`SetRS485Configuration`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Is Wifi Present',
'elements': [('Present', 'bool', 1, 'out')],
'since_firmware': [1, 2, 0],
'doc': ['af', {
'en':
"""
Returns *true* if a WIFI Extension is available to be used by the Master Brick.
""",
'de':
"""
Gibt zurück ob eine WIFI Extension zur Nutzung durch den Master Brick verfügbar
ist.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Set Wifi Configuration',
'elements': [('SSID', 'string', 32, 'in'),
             ('Connection', 'uint8', 1, 'in', ('Wifi Connection', [('DHCP', 0),
                                                                   ('Static IP', 1),
                                                                   ('Access Point DHCP', 2),
                                                                   ('Access Point Static IP', 3),
                                                                   ('Ad Hoc DHCP', 4),
                                                                   ('Ad Hoc Static IP', 5)])),
             ('IP', 'uint8', 4, 'in'),
             ('Subnet Mask', 'uint8', 4, 'in'),
             ('Gateway', 'uint8', 4, 'in'),
             ('Port', 'uint16', 1, 'in')],
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

The last parameter is the port that your program will connect to. The
default port, that is used by brickd, is 4223.

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
verbindet. Der Standardport von brickd ist 4223.

Die Werte sind im EEPROM gespeichert und werden nur beim Start angewandt. Dass
bedeutet, der Master Brick muss nach einer Konfiguration neu gestartet werden.

Wir empfehlen den Brick Viewer zu nutzen um die WIFI Extension zu
konfigurieren.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Get Wifi Configuration',
'elements': [('SSID', 'string', 32, 'out'),
             ('Connection', 'uint8', 1, 'out', ('Wifi Connection', [('DHCP', 0),
                                                                    ('Static IP', 1),
                                                                    ('Access Point DHCP', 2),
                                                                    ('Access Point Static IP', 3),
                                                                    ('Ad Hoc DHCP', 4),
                                                                    ('Ad Hoc Static IP', 5)])),
             ('IP', 'uint8', 4, 'out'),
             ('Subnet Mask', 'uint8', 4, 'out'),
             ('Gateway', 'uint8', 4, 'out'),
             ('Port', 'uint16', 1, 'out')],
'since_firmware': [1, 3, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`SetWifiConfiguration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`SetWifiConfiguration`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Set Wifi Encryption',
'elements': [('Encryption', 'uint8', 1, 'in', ('Wifi Encryption', [('WPA WPA2', 0),
                                                                   ('WPA Enterprise', 1),
                                                                   ('WEP', 2),
                                                                   ('No Encryption', 3)])),
             ('Key', 'string', 50, 'in'),
             ('Key Index', 'uint8', 1, 'in'),
             ('EAP Options', 'uint8', 1, 'in', ('Wifi EAP Option', [('Outer Auth EAP FAST', 0),
                                                                    ('Outer Auth EAP TLS', 1),
                                                                    ('Outer Auth EAP TTLS', 2),
                                                                    ('Outer Auth EAP PEAP', 3),
                                                                    ('Inner Auth EAP MSCHAP', 0),
                                                                    ('Inner Auth EAP GTC', 4),
                                                                    ('Cert Type CA Cert', 0),
                                                                    ('Cert Type Client Cert', 8),
                                                                    ('Cert Type Private Key', 16)])),
             ('CA Certificate Length', 'uint16', 1, 'in'),
             ('Client Certificate Length', 'uint16', 1, 'in'),
             ('Private Key Length', 'uint16', 1, 'in')],
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
a key with more than 50 characters, see :func:`SetLongWifiKey`.

For WEP the key has to be either 10 or 26 hexadecimal digits long. It is
possible to set the WEP ``key_index`` (1-4). If you don't know your
``key_index``, it is likely 1.

If you choose WPA Enterprise as encryption, you have to set ``eap_options`` and
the length of the certificates (for other encryption types these parameters
are ignored). The certificate length are given in byte and the certificates
themselves can be set with :func:`SetWifiCertificate`. ``eap_options`` consist
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
:func:`SetLongWifiKey` genutzt werden.

Für WEP muss der Schlüssel entweder 10 oder 26 hexadezimale Zeichen lang sein.
Es ist möglich den ``key_index`` zu setzen (1-4). Fall der ``key_index``
unbekannt ist, ist er wahrscheinlich 1.

Wenn WPA Enterprise als ``encryption`` gewählt wird, müssen ``eap_options`` und
die Länge der Zertifikate gesetzt werden. Die Länge wird in Byte angegeben
und die Zertifikate selbst können mit :func:`SetWifiCertificate` übertragen
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

Wir empfehlen den Brick Viewer zu nutzen um die WLAN Verschlüsselung
zu konfigurieren.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Get Wifi Encryption',
'elements': [('Encryption', 'uint8', 1, 'out', ('Wifi Encryption', [('WPA WPA2', 0),
                                                                    ('WPA Enterprise', 1),
                                                                    ('WEP', 2),
                                                                    ('No Encryption', 3)])),
             ('Key', 'string', 50, 'out'),
             ('Key Index', 'uint8', 1, 'out'),
             ('EAP Options', 'uint8', 1, 'out', ('Wifi EAP Option', [('Outer Auth EAP FAST', 0),
                                                                     ('Outer Auth EAP TLS', 1),
                                                                     ('Outer Auth EAP TTLS', 2),
                                                                     ('Outer Auth EAP PEAP', 3),
                                                                     ('Inner Auth EAP MSCHAP', 0),
                                                                     ('Inner Auth EAP GTC', 4),
                                                                     ('Cert Type CA Cert', 0),
                                                                     ('Cert Type Client Cert', 8),
                                                                     ('Cert Type Private Key', 16)])),
             ('CA Certificate Length', 'uint16', 1, 'out'),
             ('Client Certificate Length', 'uint16', 1, 'out'),
             ('Private Key Length', 'uint16', 1, 'out')],
'since_firmware': [1, 3, 0],
'doc': ['af', {
'en':
"""
Returns the encryption as set by :func:`SetWifiEncryption`.
""",
'de':
"""
Gibt die Verschlüsselungseinstellungen zurück, wie von 
:func:`SetWifiEncryption` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Get Wifi Status',
'elements': [('MAC Address', 'uint8', 6, 'out'),
             ('BSSID', 'uint8', 6, 'out'),
             ('Channel', 'uint8', 1, 'out'),
             ('RSSI', 'int16', 1, 'out'),
             ('IP', 'uint8', 4, 'out'),
             ('Subnet Mask', 'uint8', 4, 'out'),
             ('Gateway', 'uint8', 4, 'out'),
             ('RX Count', 'uint32', 1, 'out'),
             ('TX Count', 'uint32', 1, 'out'),
             ('State', 'uint8', 1, 'out', ('Wifi State', [('Disassociated', 0),
                                                          ('Associated', 1),
                                                          ('Associating', 2),
                                                          ('Error', 3),
                                                          ('Not Initialized Yet', 255)]))],
'since_firmware': [1, 3, 0],
'doc': ['af', {
'en':
"""
Returns the status of the WIFI Extension. The ``state`` is updated automatically,
all of the other parameters are updated on startup and every time
:func:`RefreshWifiStatus` is called.

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
Aufruf von :func:`RefreshWifiStatus` aktualisiert.

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
Refreshes the Wi-Fi status (see :func:`GetWifiStatus`). To read the status
of the Wi-Fi module, the Master Brick has to change from data mode to
command mode and back. This transaction and the readout itself is
unfortunately time consuming. This means, that it might take some ms
until the stack with attached WIFI Extension reacts again after this
function is called.
""",
'de':
"""
Aktualisiert den WLAN Status (siehe :func:`GetWifiStatus`). Um den Status
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
'elements': [('Index', 'uint16', 1, 'in'),
             ('Data', 'uint8', 32, 'in'),
             ('Data Length', 'uint8', 1, 'in')],
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

Wir empfehlen den Brick Viewer zu nutzen um die WIFI Extension Verschlüsselung
zu konfigurieren.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Get Wifi Certificate',
'elements': [('Index', 'uint16', 1, 'in'),
             ('Data', 'uint8', 32, 'out'),
             ('Data Length', 'uint8', 1, 'out')],
'since_firmware': [1, 3, 0],
'doc': ['af', {
'en':
"""
Returns the certificate for a given index as set by :func:`SetWifiCertificate`.
""",
'de':
"""
Gibt das Zertifikat für einen Index zurück, wie von 
:func:`SetWifiCertificate` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Set Wifi Power Mode',
'elements': [('Mode', 'uint8', 1, 'in', ('Wifi Power Mode', [('Full Speed', 0),
                                                             ('Low Power', 1)]))],
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

The default value is 0 (Full Speed).
""",
'de':
"""
Setzt den Stromsparmodus für die WIFI Extension. Mögliche Werte sind:

.. csv-table::
 :header: "Mode", "Beschreibung"
 :widths: 10, 90

 "0", "Full Speed (hoher Stromverbrauch, hoher Durchsatz)"
 "1", "Low Power (geringer Stromverbrauch, geringer Durchsatz)"

Der Standardwert ist 0 (Full Speed).
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Get Wifi Power Mode',
'elements': [('Mode', 'uint8', 1, 'out', ('Wifi Power Mode', [('Full Speed', 0),
                                                              ('Low Power', 1)]))],
'since_firmware': [1, 3, 0],
'doc': ['af', {
'en':
"""
Returns the power mode as set by :func:`SetWifiPowerMode`.
""",
'de':
"""
Gibt den Stromsparmodus zurück, wie von :func:`SetWifiPowerMode` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Get Wifi Buffer Info',
'elements': [('Overflow', 'uint32', 1, 'out'),
             ('Low Watermark', 'uint16', 1, 'out'),
             ('Used', 'uint16', 1, 'out')],
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
'elements': [('Domain', 'uint8', 1, 'in', ('Wifi Domain', [('Channel 1To11', 0),
                                                           ('Channel 1To13', 1),
                                                           ('Channel 1To14', 2)]))],
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

The default value is 1 (ETSI).
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

Der Standardwert ist 1 (ETSI).
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Get Wifi Regulatory Domain',
'elements': [('Domain', 'uint8', 1, 'out', ('Wifi Domain', [('Channel 1To11', 0),
                                                            ('Channel 1To13', 1),
                                                            ('Channel 1To14', 2)]))],
'since_firmware': [1, 3, 4],
'doc': ['af', {
'en':
"""
Returns the regulatory domain as set by :func:`SetWifiRegulatoryDomain`.
""",
'de':
"""
Gibt den Geltungsbereich zurück, wie von :func:`SetWifiRegulatoryDomain` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get USB Voltage',
'elements': [('Voltage', 'uint16', 1, 'out')],
'since_firmware': [1, 3, 5],
'doc': ['af', {
'en':
"""
Returns the USB voltage in mV. Does not work with hardware version 2.1.
""",
'de':
"""
Gibt die USB Spannung in mV zurück. Funktioniert nicht mit Hardware Version 2.1.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Set Long Wifi Key',
'elements': [('Key', 'string', 64, 'in')],
'since_firmware': [2, 0, 2],
'doc': ['af', {
'en':
"""
Sets a long Wi-Fi key (up to 63 chars, at least 8 chars) for WPA encryption.
This key will be used
if the key in :func:`SetWifiEncryption` is set to "-". In the old protocol,
a payload of size 63 was not possible, so the maximum key length was 50 chars.

With the new protocol this is possible, since we didn't want to break API,
this function was added additionally.
""",
'de':
"""
Setzt einen langen WLAN Schlüssel (bis zu 63 Zeichen, mindestens 8 Zeichen) für
WPA Verschlüsselung. Dieser Schlüssel wird genutzt, wenn der Schlüssel in
:func:`SetWifiEncryption` auf "-" gesetzt wird. Im alten Protokoll war
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
'elements': [('Key', 'string', 64, 'out')],
'since_firmware': [2, 0, 2],
'doc': ['af', {
'en':
"""
Returns the encryption key as set by :func:`SetLongWifiKey`.
""",
'de':
"""
Gibt den Verschlüsselungsschlüssel zurück, wie von 
:func:`SetLongWifiKey` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Set Wifi Hostname',
'elements': [('Hostname', 'string', 16, 'in')],
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
Access Points als Hostname in der DHCP-Client Tabelle angezeigt.

Das setzen eines leeren Strings stellt den voreingestellten Hostnamen
wieder her.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Get Wifi Hostname',
'elements': [('Hostname', 'string', 16, 'out')],
'since_firmware': [2, 0, 5],
'doc': ['af', {
'en':
"""
Returns the hostname as set by :func:`GetWifiHostname`.

An empty String means, that the default hostname is used.
""",
'de':
"""
Gibt den Hostnamen zurück, wie von :func:`GetWifiHostname` gesetzt.

Ein leerer String bedeutet, dass der voreingestellte Hostname
genutzt wird.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Stack Current Callback Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`StackCurrent` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`StackCurrent` is only triggered if the current has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`StackCurrent` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`StackCurrent` wird nur ausgelöst wenn sich die Stromstärke seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Stack Current Callback Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetCurrentCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetCurrentCallbackPeriod`
gesetzt
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Stack Voltage Callback Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`StackVoltage` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`StackVoltage` is only triggered if the voltage has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`StackVoltage` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`StackVoltage` wird nur ausgelöst wenn sich die Spannung seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Stack Voltage Callback Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetStackVoltageCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetStackVoltageCallbackPeriod`
gesetzt
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set USB Voltage Callback Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`USBVoltage` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`USBVoltage` is only triggered if the voltage has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`USBVoltage` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`USBVoltage` wird nur ausgelöst wenn sich die Spannung seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get USB Voltage Callback Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetUSBVoltageCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetUSBVoltageCallbackPeriod`
gesetzt
"""
}]
})



com['packets'].append({
'type': 'function',
'name': 'Set Stack Current Callback Threshold',
'elements': [('Option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint16', 1, 'in'),
             ('Max', 'uint16', 1, 'in')],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`StackCurrentReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the current is *outside* the min and max values"
 "'i'",    "Callback is triggered when the current is *inside* the min and max values"
 "'<'",    "Callback is triggered when the current is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the current is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`StackCurrentReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Stromstärke *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn die Stromstärke *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn die Stromstärke kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Stromstärke größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Stack Current Callback Threshold',
'elements': [('Option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint16', 1, 'out'),
             ('Max', 'uint16', 1, 'out')],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`SetStackCurrentCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetStackCurrentCallbackThreshold`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Stack Voltage Callback Threshold',
'elements': [('Option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint16', 1, 'in'),
             ('Max', 'uint16', 1, 'in')],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`StackStackVoltageReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the voltage is *outside* the min and max values"
 "'i'",    "Callback is triggered when the voltage is *inside* the min and max values"
 "'<'",    "Callback is triggered when the voltage is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the voltage is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`StackVoltageReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Spannung *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn die Spannung *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn die Spannung kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Spannung größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Stack Voltage Callback Threshold',
'elements': [('Option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint16', 1, 'out'),
             ('Max', 'uint16', 1, 'out')],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`SetStackVoltageCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetStackVoltageCallbackThreshold`
gesetzt.
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set USB Voltage Callback Threshold',
'elements': [('Option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint16', 1, 'in'),
             ('Max', 'uint16', 1, 'in')],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`USBVoltageReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the voltage is *outside* the min and max values"
 "'i'",    "Callback is triggered when the voltage is *inside* the min and max values"
 "'<'",    "Callback is triggered when the voltage is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the voltage is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`USBVoltageReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Spannung *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn die Spannung *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn die Spannung kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Spannung größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get USB Voltage Callback Threshold',
'elements': [('Option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint16', 1, 'out'),
             ('Max', 'uint16', 1, 'out')],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`SetUSBVoltageCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetUSBVoltageCallbackThreshold`
gesetzt.
"""
}]
})



com['packets'].append({
'type': 'function',
'name': 'Set Debounce Period',
'elements': [('Debounce', 'uint32', 1, 'in')],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the threshold callbacks

* :func:`StackCurrentReached`,
* :func:`StackVoltageReached`,
* :func:`USBVoltageReached`

are triggered, if the thresholds

* :func:`SetStackCurrentCallbackThreshold`,
* :func:`SetStackVoltageCallbackThreshold`,
* :func:`SetUSBVoltageCallbackThreshold`

keep being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callbacks

* :func:`StackCurrentReached`,
* :func:`StackVoltageReached`,
* :func:`USBVoltageReached`
 
ausgelöst werden, wenn die Schwellwerte 

* :func:`SetStackCurrentCallbackThreshold`,
* :func:`SetStackVoltageCallbackThreshold`,
* :func:`SetUSBVoltageCallbackThreshold`
 
weiterhin erreicht bleiben.

Der Standardwert ist 100.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Debounce Period',
'elements': [('Debounce', 'uint32', 1, 'out')],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Returns the debounce period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Gibt die Entprellperiode zurück, wie von :func:`SetDebouncePeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Stack Current',
'elements': [('Current', 'uint16', 1, 'out')],
'since_firmware': [2, 0, 5],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetStackCurrentCallbackPeriod`. The :word:`parameter` is the current of the
sensor.

:func:`StackCurrent` is only triggered if the current has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetStackCurrentCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die Stromstärke des Sensors.

:func:`StackCurrent` wird nur ausgelöst wenn sich die Stromstärke seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Stack Voltage',
'elements': [('Voltage', 'uint16', 1, 'out')],
'since_firmware': [2, 0, 5],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetStackVoltageCallbackPeriod`. The :word:`parameter` is the voltage of the
sensor.

:func:`StackVoltage` is only triggered if the voltage has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetStackVoltageCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die Spannung des Sensors.

:func:`StackVoltage` wird nur ausgelöst wenn sich die Spannung seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'USB Voltage',
'elements': [('Voltage', 'uint16', 1, 'out')],
'since_firmware': [2, 0, 5],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetUSBVoltageCallbackPeriod`. The :word:`parameter` is the USB voltage
in mV.

:func:`USBVoltage` is only triggered if the USB voltage has changed since the
last triggering.

Does not work with hardware version 2.1.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetUSBVoltageCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die USB Spannung in mV.

:func:`USBVoltage` wird nur ausgelöst wenn sich die USB Spannung seit der
letzten Auslösung geändert hat.

Funktioniert nicht mit Hardware Version 2.1.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Stack Current Reached',
'elements': [('Current', 'uint16', 1, 'out')],
'since_firmware': [2, 0, 5],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetStackCurrentCallbackThreshold` is reached.
The :word:`parameter` is the stack current in mA.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetStackCurrentCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist der Stromverbrauch des Stapels in mA.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Stack Voltage Reached',
'elements': [('Voltage', 'uint16', 1, 'out')],
'since_firmware': [2, 0, 5],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetStackVoltageCallbackThreshold` is reached.
The :word:`parameter` is the stack voltage in mV.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetStackVoltageCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Spannung des Stapels in mV.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'USB Voltage Reached',
'elements': [('Voltage', 'uint16', 1, 'out')],
'since_firmware': [2, 0, 5],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetUSBVoltageCallbackThreshold` is reached.
The :word:`parameter` is the voltage of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetUSBVoltageCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Spannung des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Is Ethernet Present',
'elements': [('Present', 'bool', 1, 'out')],
'since_firmware': [2, 1, 0],
'doc': ['af', {
'en':
"""
Returns *true* if a Ethernet Extension is available to be used by the Master
Brick.
""",
'de':
"""
Gibt zurück ob eine Ethernet Extension zur Nutzung durch den Master Brick
verfügbar ist.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Set Ethernet Configuration',
'elements': [('Connection', 'uint8', 1, 'in', ('Ethernet Connection', [('DHCP', 0),
                                                                       ('Static IP', 1)])),
             ('IP', 'uint8', 4, 'in'),
             ('Subnet Mask', 'uint8', 4, 'in'),
             ('Gateway', 'uint8', 4, 'in'),
             ('Port', 'uint16', 1, 'in')],
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

The last parameter is the port that your program will connect to. The
default port, that is used by brickd, is 4223.

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
verbindet. Der Standardport von brickd ist 4223.

Die Werte sind im EEPROM gespeichert und werden nur beim Start angewandt.
Das bedeutet der Master Brick muss nach einer Konfiguration neu gestartet
werden.

Wir empfehlen den Brick Viewer zu nutzen um die Ethernet Extension zu
konfigurieren.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Get Ethernet Configuration',
'elements': [('Connection', 'uint8', 1, 'out', ('Ethernet Connection', [('DHCP', 0),
                                                                        ('Static IP', 1)])),
             ('IP', 'uint8', 4, 'out'),
             ('Subnet Mask', 'uint8', 4, 'out'),
             ('Gateway', 'uint8', 4, 'out'),
             ('Port', 'uint16', 1, 'out')],
'since_firmware': [2, 1, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`SetEthernetConfiguration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`SetEthernetConfiguration`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Get Ethernet Status',
'elements': [('MAC Address', 'uint8', 6, 'out'),
             ('IP', 'uint8', 4, 'out'),
             ('Subnet Mask', 'uint8', 4, 'out'),
             ('Gateway', 'uint8', 4, 'out'),
             ('RX Count', 'uint32', 1, 'out'),
             ('TX Count', 'uint32', 1, 'out'),
             ('Hostname', 'string', 32, 'out')],
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
'elements': [('Hostname', 'string', 32, 'in')],
'since_firmware': [2, 1, 0],
'doc': ['af', {
'en':
"""
Sets the hostname of the Ethernet Extension. The hostname will be displayed 
by access points as the hostname in the DHCP clients table.

Setting an empty String will restore the default hostname.

The current hostname can be discovered with :func:`GetEthernetStatus`.
""",
'de':
"""
Setzt den Hostnamen der Ethernet Extension. Der Hostname wird von
Access Points als Hostname in der DHCP-Client Tabelle angezeigt.

Das setzen eines leeren Strings stellt den voreingestellten Hostnamen
wieder her.

Der aktuelle Hostname kann mit :func:`GetEthernetStatus` herausgefunden werden.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Set Ethernet MAC Address',
'elements': [('MAC Address', 'uint8', 6, 'in')],
'since_firmware': [2, 1, 0],
'doc': ['af', {
'en':
"""
Sets the MAC address of the Ethernet Extension. The Ethernet Extension should
come configured with a valid MAC address, that is also written on a
sticker of the extension itself.

The MAC address can be read out again with :func:`GetEthernetStatus`.
""",
'de':
"""
Setzt die MAC Adresse der Ethernet Extension. Die Ethernet Extension sollte
mit einer vorkonfigurierten MAC Adresse ausgeliefert werden. Diese MAC Adresse
steht auch auf einem Aufkleber auf der Ethernet Extension.

Die MAC Adresse kann mit :func:`GetEthernetStatus` wieder ausgelesen werden.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Set Ethernet Websocket Configuration',
'elements': [('Sockets', 'uint8', 1, 'in'),
             ('Port', 'uint16', 1, 'in')],
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

The default values are 3 for the socket connections and 4280 for the port.
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

Wir empfehlen den Brick Viewer zu nutzen um die Ethernet Extension zu
konfigurieren.

Die Standardwerte sind 3 für die Anzahl der Socket-Verbindungen und
4280 für den Port.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Get Ethernet Websocket Configuration',
'elements': [('Sockets', 'uint8', 1, 'out'),
             ('Port', 'uint16', 1, 'out')],
'since_firmware': [2, 2, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`SetEthernetConfiguration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`SetEthernetConfiguration`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Set Ethernet Authentication Secret',
'elements': [('Secret', 'string', 64, 'in')],
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

Wir empfehlen den Brick Viewer zu nutzen um die Authentifizierung der Ethernet
Extension einzurichten.

Der Standardwert ist ein leerer String (Authentifizierung deaktiviert).
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Get Ethernet Authentication Secret',
'elements': [('Secret', 'string', 64, 'out')],
'since_firmware': [2, 2, 0],
'doc': ['af', {
'en':
"""
Returns the authentication secret as set by :func:`SetEthernetAuthenticationSecret`.
""",
'de':
"""
Gibt das Authentifizierungsgeheimnis zurück, wie von
:func:`SetEthernetAuthenticationSecret` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Set Wifi Authentication Secret',
'elements': [('Secret', 'string', 64, 'in')],
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

Wir empfehlen den Brick Viewer zu nutzen um die Authentifizierung der WIFI 
Extension einzurichten.

Der Standardwert ist ein leerer String (Authentifizierung deaktiviert).
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Get Wifi Authentication Secret',
'elements': [('Secret', 'string', 64, 'out')],
'since_firmware': [2, 2, 0],
'doc': ['af', {
'en':
"""
Returns the authentication secret as set by :func:`SetWifiAuthenticationSecret`.
""",
'de':
"""
Gibt das Authentifizierungsgeheimnis zurück, wie von
:func:`SetWifiAuthenticationSecret` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Get Connection Type',
'elements': [('Connection Type', 'uint8', 1, 'out', ('Connection Type', [('None', 0),
                                                                         ('USB', 1),
                                                                         ('SPI Stack', 2),
                                                                         ('Chibi', 3),
                                                                         ('RS485', 4),
                                                                         ('Wifi', 5),
                                                                         ('Ethernet', 6),
                                                                         ('Wifi2', 7)]))],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Is Wifi2 Present',
'elements': [('Present', 'bool', 1, 'out')],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Returns *true* if a WIFI Extension 2.0 is available to be used by the Master
Brick.
""",
'de':
"""
Gibt zurück ob eine WIFI Extension 2.0 zur Nutzung durch den Master Brick
verfügbar ist.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Start Wifi2 Bootloader',
'elements': [('Result', 'int8', 1, 'out')],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Write Wifi2 Flash',
'elements': [('Data', 'uint8', 60, 'in'),
             ('Length', 'uint8', 1, 'in'),
             ('Result', 'int8', 1, 'out')],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Read Wifi2 Flash',
'elements': [('Length', 'uint8', 1, 'in'),
             ('Data', 'uint8', 60, 'out'),
             ('Result', 'uint8', 1, 'out')],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Set Wifi2 Authentication Secret',
'elements': [('Secret', 'string', 64, 'in')],
'since_firmware': [2, 4, 0],
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

Wir empfehlen den Brick Viewer zu nutzen um die Authentifizierung der WIFI 
Extension einzurichten.

Der Standardwert ist ein leerer String (Authentifizierung deaktiviert).
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Get Wifi2 Authentication Secret',
'elements': [('Secret', 'string', 64, 'out')],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Returns the authentication secret as set by :func:`SetWifi2AuthenticationSecret`.
""",
'de':
"""
Gibt das Authentifizierungsgeheimnis zurück, wie von
:func:`SetWifi2AuthenticationSecret` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Set Wifi2 Configuration',
'elements': [('Port', 'uint16', 1, 'in'),
             ('Websocket Port', 'uint16', 1, 'in'),
             ('Website Port', 'uint16', 1, 'in'),
             ('PHY Mode', 'uint8', 1, 'in', ('Wifi2 PHY Mode', [('B', 0),
                                                                ('G', 1),
                                                                ('N', 2)])),
             ('Sleep Mode', 'uint8', 1, 'in'), # FIXME: constants?
             ('Website', 'uint8', 1, 'in')], # FIXME: constants?
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Get Wifi2 Configuration',
'elements': [('Port', 'uint16', 1, 'out'),
             ('Websocket Port', 'uint16', 1, 'out'),
             ('Website Port', 'uint16', 1, 'out'),
             ('PHY Mode', 'uint8', 1, 'out', ('Wifi2 PHY Mode', [('B', 0),
                                                                 ('G', 1),
                                                                 ('N', 2)])),
             ('Sleep Mode', 'uint8', 1, 'out'), # FIXME: constants?
             ('Website', 'uint8', 1, 'out')], # FIXME: constants?
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Get Wifi2 Status',
'elements': [('Client Enabled', 'bool', 1, 'out'),
             ('Client Status', 'uint8', 1, 'out', ('Wifi2 Client Status', [('Idle', 0),
                                                                           ('Connecting', 1),
                                                                           ('Wrong Password', 2),
                                                                           ('No AP Found', 3),
                                                                           ('Connect Failed', 4),
                                                                           ('Got IP', 5)])),
             ('Client IP', 'uint8', 4, 'out'),
             ('Client Subnet Mask', 'uint8', 4, 'out'),
             ('Client Gateway', 'uint8', 4, 'out'),
             ('Client MAC Address', 'uint8', 6, 'out'),
             ('Client RX Count', 'uint32', 1, 'out'),
             ('Client TX Count', 'uint32', 1, 'out'),
             ('Client RSSI', 'int8', 1, 'out'),
             ('AP Enabled', 'bool', 1, 'out'),
             ('AP IP', 'uint8', 4, 'out'),
             ('AP Subnet Mask', 'uint8', 4, 'out'),
             ('AP Gateway', 'uint8', 4, 'out'),
             ('AP MAC Address', 'uint8', 6, 'out'),
             ('AP RX Count', 'uint32', 1, 'out'),
             ('AP TX Count', 'uint32', 1, 'out'),
             ('AP Connected Count', 'uint8', 1, 'out')],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Set Wifi2 Client Configuration',
'elements': [('Enable', 'bool', 1, 'in'),
             ('SSID', 'string', 32, 'in'),
             ('IP', 'uint8', 4, 'in'),
             ('Subnet Mask', 'uint8', 4, 'in'),
             ('Gateway', 'uint8', 4, 'in'),
             ('MAC Address', 'uint8', 6, 'in'),
             ('BSSID', 'uint8', 6, 'in')],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Get Wifi2 Client Configuration',
'elements': [('Enable', 'bool', 1, 'out'),
             ('SSID', 'string', 32, 'out'),
             ('IP', 'uint8', 4, 'out'),
             ('Subnet Mask', 'uint8', 4, 'out'),
             ('Gateway', 'uint8', 4, 'out'),
             ('MAC Address', 'uint8', 6, 'out'),
             ('BSSID', 'uint8', 6, 'out')],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Set Wifi2 Client Hostname',
'elements': [('Hostname', 'string', 32, 'in')],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Get Wifi2 Client Hostname',
'elements': [('Hostname', 'string', 32, 'out')],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Set Wifi2 Client Password',
'elements': [('Password', 'string', 64, 'in')],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Get Wifi2 Client Password',
'elements': [('Password', 'string', 64, 'out')],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Set Wifi2 AP Configuration',
'elements': [('Enable', 'bool', 1, 'in'),
             ('SSID', 'string', 32, 'in'),
             ('IP', 'uint8', 4, 'in'),
             ('Subnet Mask', 'uint8', 4, 'in'),
             ('Gateway', 'uint8', 4, 'in'),
             ('Encryption', 'uint8', 1, 'in', ('Wifi2 AP Encryption', [('No Encryption', 0),
                                                                       ('WEP', 1),
                                                                       ('WPA PSK', 2),
                                                                       ('WPA2 PSK', 3),
                                                                       ('WPA WPA2 PSK', 4)])),
             ('Hidden', 'bool', 1, 'in'),
             ('Channel', 'uint8', 1, 'in'),
             ('MAC Address', 'uint8', 6, 'in')],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Get Wifi2 AP Configuration',
'elements': [('Enable', 'bool', 1, 'out'),
             ('SSID', 'string', 32, 'out'),
             ('IP', 'uint8', 4, 'out'),
             ('Subnet Mask', 'uint8', 4, 'out'),
             ('Gateway', 'uint8', 4, 'out'),
             ('Encryption', 'uint8', 1, 'out', ('Wifi2 AP Encryption', [('No Encryption', 0),
                                                                        ('WEP', 1),
                                                                        ('WPA PSK', 2),
                                                                        ('WPA2 PSK', 3),
                                                                        ('WPA WPA2 PSK', 4)])),
             ('Hidden', 'bool', 1, 'out'),
             ('Channel', 'uint8', 1, 'out'),
             ('MAC Address', 'uint8', 6, 'out')],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Set Wifi2 AP Password',
'elements': [('Password', 'string', 64, 'in')],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Get Wifi2 AP Password',
'elements': [('Password', 'string', 64, 'out')],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Save Wifi2 Configuration',
'elements': [('Result', 'uint8', 1, 'out')],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Call this function to actually save configuration
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': 'Get Wifi2 Firmware Version',
'elements': [('Firmware Version', 'uint8', 3, 'out')],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Returns the current version of the WIFI Extension 2.0 firmware (major, minor, revision).
""",
'de':
"""
Gibt die aktuelle Version der WIFI Extension 2.0 Firmware zurück (major, minor, revision).
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
'elements': [('Enabled', 'bool', 1, 'out')],
'since_firmware': [2, 4, 0],
'doc': ['af', {
'en':
"""
Returns *True* if the green status LED of the WIFI Extension 2.0 is turned on.
""",
'de':
"""
Gibt *True* zurück falls die grüne Status LED der WIFI Extension 2.0 aktiviert ist.
"""
}]
})

com['examples'].append({
'name': 'Stack Status',
'functions': [('getter', ('Get Stack Voltage', 'stack voltage'), [(('Stack Voltage', 'Stack Voltage'), 'uint16', 1000.0, 'mV', 'V', None)], []),
              ('getter', ('Get Stack Current', 'stack current'), [(('Stack Current', 'Stack Current'), 'uint16', 1000.0, 'mA', 'A', None)], [])]
})
