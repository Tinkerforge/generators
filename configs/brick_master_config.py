# -*- coding: utf-8 -*-

# Master Brick communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'version': [1, 2, 1],
    'category': 'Brick',
    'name': ('Master', 'master', 'Master'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for controlling Stacks and four Bricklets',
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetStackVoltage', 'get_stack_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')], 
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
'name': ('GetStackCurrent', 'get_stack_current'), 
'elements': [('current', 'uint16', 1, 'out')], 
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
'name': ('SetExtensionType', 'set_extension_type'), 
'elements': [('extension', 'uint8', 1, 'in'),
             ('exttype', 'uint32', 1, 'in')], 
'doc': ['af', {
'en':
"""
Writes the extension type to the EEPROM of a specified extension. 
The extension is either 0 or 1 (0 is the on the bottom, 1 is the on on top, 
if only one extension is present use 0).

Possible extension types:

.. csv-table::
 :header: "Type", "Description"
 :widths: 10, 100

 "1",    "Chibi"
 "2",    "RS485"

The extension type is already set when bought and it can be set with the 
Brick Viewer, it is unlikely that you need this function.

The value will be saved in the EEPROM of the Chibi Extension, it does not
have to be set on every startup.
""",
'de':
"""
Schreibt den Typ der Extension in den EEPROM der angegebenen Extension.
Die Extension kann entweder 0 oder 1 sein (0 ist an der Unterseite, 1
auf der Oberseite, wenn nur eine Extension verfügbar ist, ist 0 zu verwenden)

Mögliche Extensiontypen:

.. csv-table::
 :header: "Typ", "Beschreibung"
 :widths: 10,100
 
 "1",    "Chibi"
 "2",    "RS485"

Der Typ der Extension ist schon gesetzt beim Erwerb der Extension und kann über den
Brick Viewer gesetzt werden. Daher ist es unwahrscheinlich, dass diese Funktion benötigt
wird.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetExtensionType', 'get_extension_type'), 
'elements': [('extension', 'uint8', 1, 'in'),
             ('exttype', 'uint32', 1, 'out')], 
'doc': ['af', {
'en':
"""
Returns the extension type for a given extension as set by 
:func:`SetExtensionType`.
""",
'de':
"""
Gibt den Extensiontyp der angegebenen Extension zurück,
wie von :func:`SetExtensionType` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('IsChibiPresent', 'is_chibi_present'), 
'elements': [('present', 'bool', 1, 'out')], 
'doc': ['af', {
'en':
"""
Returns *true* if a Chibi Extension is available to be used by the Master.

.. versionadded:: 1.1.0
""",
'de':
"""
Gibt zurück ob eine Chibi Extension zur Nutzung durch den Master verfügbar ist.

.. versionadded:: 1.1.0
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetChibiAddress', 'set_chibi_address'), 
'elements': [('address', 'uint8', 1, 'in')], 
'doc': ['af', {
'en':
"""
Sets the address (1-255) belonging to the Chibi Extension.

It is possible to set the address with the Brick Viewer and it will be 
saved in the EEPROM of the Chibi Extension, it does not
have to be set on every startup.

.. versionadded:: 1.1.0
""",
'de':
"""
Setzt die zugehörige Adresse (1-255) der Chibi Extension.

Es ist möglich die Adresse mit dem Brick Viewer zu setzen und diese
wird im EEPROM der Chibi Extension abgespeichert. Ein Setzen bei
jedem Hochfahren ist daher nicht notwendig.

.. versionadded:: 1.1.0
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetChibiAddress', 'get_chibi_address'), 
'elements': [('address', 'uint8', 1, 'out')], 
'doc': ['af', {
'en':
"""
Returns the address as set by :func:`SetChibiAddress`.

.. versionadded:: 1.1.0
""",
'de':
"""
Gibt die Adresse zurück, wie von :func:`SetChibiAddress` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetChibiMasterAddress', 'set_chibi_master_address'), 
'elements': [('address', 'uint8', 1, 'in')], 
'doc': ['af', {
'en':
"""
Sets the address (1-255) of the Chibi Master. This address is used if the
Chibi Extension is used as slave (i.e. it does not have a USB connection).

It is possible to set the address with the Brick Viewer and it will be 
saved in the EEPROM of the Chibi Extension, it does not
have to be set on every startup.

.. versionadded:: 1.1.0
""",
'de':
"""
Setzt die Adresse (1-255) des Chibi Master. Diese Adresse wird verwendet
wenn die Chibi Extension als Slave verwendet wird (z.B. wenn keine USB-Verbindung
besteht).

Es ist möglich die Adresse mit dem Brick Viewer zu setzen und diese wird im
EEPROM der Chibi Extension abgespeichert. Ein Setzen bei
jedem Hochfahren ist daher nicht notwendig.

.. versionadded:: 1.1.0
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetChibiMasterAddress', 'get_chibi_master_address'), 
'elements': [('address', 'uint8', 1, 'out')], 
'doc': ['af', {
'en':
"""
Returns the address as set by :func:`SetChibiMasterAddress`.

.. versionadded:: 1.1.0
""",
'de':
"""
Gibt die Adresse zurück, wie von :func:`SetChibiMasterAddress` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetChibiSlaveAddress', 'set_chibi_slave_address'), 
'elements': [('num', 'uint8', 1, 'in'),
             ('address', 'uint8', 1, 'in')], 
'doc': ['af', {
'en':
"""
Sets up to 254 slave addresses. Valid addresses are in range 1-255.
The address numeration (via num parameter) has to be used
ascending from 0. For example: If you use the Chibi Extension in Master mode
(i.e. the stack has an USB connection) and you want to talk to three other
Chibi stacks with the slave addresses 17, 23, and 42, you should call with "(0, 17),
(1, 23) and (2, 42)".

It is possible to set the addresses with the Brick Viewer and it will be 
saved in the EEPROM of the Chibi Extension, they don't
have to be set on every startup.

.. versionadded:: 1.1.0
""",
'de':
"""
Setzt bis zu 254 Slave Adressen. Gültige Adressen sind 1-255.
Die Adressnummerierung (mittels num Parameter) muss aufsteigend ab
0 erfolgen. Beispiel: Wenn die Chibi Extension im Master Modus verwendet wird
(z.B. wenn der Stapel eine USB-Verbindung hat) und es soll mit drei weiteren
Chibi Stapeln kommuniziert werden, mit den Adressen 17, 23 und 42, sollten die
Aufrufe "(0, 17), (1, 23) und (2, 42)" sein.

Es ist möglich die Adressen mit dem Brick Viewer zu setzen und diese werden
im EEPROM der Chibi Extension abgespeichert. Ein Setzen bei
jedem Hochfahren ist daher nicht notwendig.

.. versionadded:: 1.1.0
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetChibiSlaveAddress', 'get_chibi_slave_address'), 
'elements': [('num', 'uint8', 1, 'in'),
             ('address', 'uint8', 1, 'out')], 
'doc': ['af', {
'en':
"""
Returns the slave address for a given num as set by 
:func:`SetChibiSlaveAddress`.

.. versionadded:: 1.1.0
""",
'de':
"""
Gibt die Slave Adresse für eine Adressnummerierung (mittels num Parameter) zurück,
wie von :func:`SetChibiSlaveAddress` gesetzt.

.. versionadded:: 1.1.0
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetChibiSignalStrength', 'get_chibi_signal_strength'), 
'elements': [('signal_strength', 'uint8', 1, 'out')], 
'doc': ['af', {
'en':
"""
Returns the signal strength in dBm. The signal strength updates every time a
packet is received.

.. versionadded:: 1.1.0
""",
'de':
"""
Gibt die Signalstärke in dBm zurück. Die Aktualisierung der Signalstärke
wird bei jedem Empfang eines Paketes durchgeführt.

.. versionadded:: 1.1.0
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetChibiErrorLog', 'get_chibi_error_log'), 
'elements': [('underrun', 'uint16', 1, 'out'),
             ('crc_error', 'uint16', 1, 'out'),
             ('no_ack', 'uint16', 1, 'out'),
             ('overflow', 'uint16', 1, 'out')], 
'doc': ['af', {
'en':
"""
Returns underrun, CRC error, no ACK and overflow error counts of the Chibi
communication. If these errors start rising, it is likely that either the
distance between two Chibi stacks is becoming too big or there are
interferences.

.. versionadded:: 1.1.0
""",
'de':
"""
Gibt folgende Fehlerzähler der Chibi Kommunikation zurück: Underrun, CRC Fehler,
kein ACK und Overflow. Bei Anstieg dieser Fehlerzähler ist es wahrscheinlich, dass
entweder die Entfernung zwischen zwei Chibi Stapeln zu groß wird oder Störungen
vorliegen.

.. versionadded:: 1.1.0
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetChibiFrequency', 'set_chibi_frequency'), 
'elements': [('frequency', 'uint8', 1, 'in')], 
'doc': ['af', {
'en':
"""
Sets the Chibi frequency range for the Chibi Extension. Possible values are:

.. csv-table::
 :header: "Type", "Description"
 :widths: 10, 100

 "0",    "OQPSK 868Mhz (Europe)"
 "1",    "OQPSK 915Mhz (US)"
 "2",    "OQPSK 780Mhz (China)"
 "3",    "BPSK40 915Mhz"

It is possible to set the frequency with the Brick Viewer and it will be 
saved in the EEPROM of the Chibi Extension, it does not
have to be set on every startup.

.. versionadded:: 1.1.0
""",
'de':
"""
Setzt den Chibi Frequenzbereich der Chibi Extension. Mögliche Werte sind:

.. csv-table::
 :header: "Typ", "Beschreibung"
 :widths: 10, 100

 "0",    "OQPSK 868Mhz (Europe)"
 "1",    "OQPSK 915Mhz (US)"
 "2",    "OQPSK 780Mhz (China)"
 "3",    "BPSK40 915Mhz"
 
Es ist möglich den Frequenzbereich mit dem Brick Viewer zu setzen und dieser wird
im EEPROM der Chibi Extension abgespeichert. Ein Setzen bei
jedem Hochfahren ist daher nicht notwendig.

.. versionadded:: 1.1.0
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetChibiFrequency', 'get_chibi_frequency'), 
'elements': [('frequency', 'uint8', 1, 'out')], 
'doc': ['af', {
'en':
"""
Returns the frequency value as set by :func:`SetChibiFrequency`.

.. versionadded:: 1.1.0
""",
'de':
"""
Gibt den Frequenzbereich zurück, wie von :func:`SetChibiFrequency` gesetzt.

.. versionadded:: 1.1.0
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetChibiChannel', 'set_chibi_channel'), 
'elements': [('channel', 'uint8', 1, 'in')], 
'doc': ['af', {
'en':
"""
Sets the channel used by the Chibi Extension. Possible channels are
different for different frequencies:

.. csv-table::
 :header: "Frequency",             "Possible Channels"
 :widths: 40, 60

 "OQPSK 868Mhz (Europe)", "0"
 "OQPSK 915Mhz (US)",     "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"
 "OQPSK 780Mhz (China)",  "0, 1, 2, 3"
 "BPSK40 915Mhz",         "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"

It is possible to set the channel with the Brick Viewer and it will be 
saved in the EEPROM of the Chibi Extension, it does not
have to be set on every startup.

.. versionadded:: 1.1.0
""",
'de':
"""
Setzt den verwendeten Kanal der Chibi Extension. Die möglichen Kanäle sind
abhängig vom verwendeten Frequenzbereich:

.. csv-table::
 :header: "Frequenzbereich",             "Mögliche Kanäle"
 :widths: 40, 60

 "OQPSK 868Mhz (Europe)", "0"
 "OQPSK 915Mhz (US)",     "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"
 "OQPSK 780Mhz (China)",  "0, 1, 2, 3"
 "BPSK40 915Mhz",         "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"
 
Es ist möglich den Kanal mit dem Brick Viewer zu setzen und dieser wird
im EEPROM der Chibi Extension abgespeichert. Ein Setzen bei
jedem Hochfahren ist daher nicht notwendig.

.. versionadded:: 1.1.0
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetChibiChannel', 'get_chibi_channel'), 
'elements': [('channel', 'uint8', 1, 'out')], 
'doc': ['af', {
'en':
"""
Returns the channel as set by :func:`SetChibiChannel`.

.. versionadded:: 1.1.0
""",
'de':
"""
Gibt den Kanal zurück, wie von :func:`SetChibiChannel` gesetzt.

.. versionadded:: 1.1.0
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('IsRS485Present', 'is_rs485_present'), 
'elements': [('present', 'bool', 1, 'out')], 
'doc': ['af', {
'en':
"""
Returns *true* if a RS485 Extension is available to be used by the Master.

.. versionadded:: 1.2.0
""",
'de':
"""
Gibt zurück ob eine RS485 Extension zur Nutzung durch den Master verfügbar ist.

.. versionadded:: 1.2.0
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('SetRS485Address', 'set_rs485_address'), 
'elements': [('address', 'uint8', 1, 'in')], 
'doc': ['af', {
'en':
"""
Sets the address (1-255) belonging to the RS485 Extension.

Set to 0 if the RS485 Extension should be the RS485 Master (i.e.
connected to a PC via USB).

It is possible to set the address with the Brick Viewer and it will be 
saved in the EEPROM of the RS485 Extension, it does not
have to be set on every startup.

.. versionadded:: 1.2.0
""",
'de':
"""
Setzt die zugehörige Adresse (1-255) der RS485 Extension.

Um eine RS485 Extension als RS485 Master (z.B. verbunden mit einem PC über
USB) zu betreiben muss die Adresse auf 0 gesetzt werden.

Es ist möglich die Adresse mit dem Brick Viewer zu setzen und diese wird im
EEPROM der RS485 Extension abgespeichert. Ein Setzen bei
jedem Hochfahren ist daher nicht notwendig.

.. versionadded:: 1.2.0
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('GetRS485Address', 'get_rs485_address'), 
'elements': [('address', 'uint8', 1, 'out')], 
'doc': ['af', {
'en':
"""
Returns the address as set by :func:`SetRS485Address`.

.. versionadded:: 1.2.0
""",
'de':
"""
Gibt die Adresse zurück, wie von :func:`SetRS485Address` gesetzt.

.. versionadded:: 1.2.0
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('SetRS485SlaveAddress', 'set_rs485_slave_address'),
'elements': [('num', 'uint8', 1, 'in'),
             ('address', 'uint8', 1, 'in')], 
'doc': ['af', {
'en':
"""
Sets up to 255 slave addresses. Valid addresses are in range 1-255.
The address numeration (via num parameter) has to be used
ascending from 0. For example: If you use the RS485 Extension in Master mode
(i.e. the stack has an USB connection) and you want to talk to three other
RS485 stacks with the IDs 17, 23, and 42, you should call with "(0, 17),
(1, 23) and (2, 42)".

It is possible to set the addresses with the Brick Viewer and it will be 
saved in the EEPROM of the RS485 Extension, they don't
have to be set on every startup.

.. versionadded:: 1.2.0
""",
'de':
"""
Setzt bis zu 255 Slave Adressen. Gültige Adressen sind 1-255.
Die Adressnummerierung (mittels num Parameter) muss aufsteigend ab
0 erfolgen. Beispiel: Wenn die RS485 Extension im Master Modus verwendet wird
(z.B. wenn der Stapel eine USB-Verbindung hat) und es soll mit drei weiteren
RS485 Stapeln kommuniziert werden, mit den Adressen 17, 23 und 42, sollten die
Aufrufe "(0, 17), (1, 23) und (2, 42)" sein.

Es ist möglich die Adressen mit dem Brick Viewer zu setzen und diese werden
im EEPROM der RS485 Extension abgespeichert. Ein Setzen bei
jedem Hochfahren ist daher nicht notwendig.

.. versionadded:: 1.2.0
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('GetRS485SlaveAddress', 'get_rs485_slave_address'), 
'elements': [('num', 'uint8', 1, 'in'),
             ('address', 'uint8', 1, 'out')], 
'doc': ['af', {
'en':
"""
Returns the slave address for a given num as set by 
:func:`SetRS485SlaveAddress`.

.. versionadded:: 1.2.0
""",
'de':
"""
Gibt die Slave Adresse für eine Adressnummerierung (mittels num Parameter) zurück,
wie von :func:`SetRS485SlaveAddress` gesetzt.

.. versionadded:: 1.2.0
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('GetRS485ErrorLog', 'get_rs485_error_log'), 
'elements': [('crc_error', 'uint16', 1, 'out')], 
'doc': ['af', {
'en':
"""
Returns CRC error counts of the RS485 communication.
If this counter starts rising, it is likely that the distance
between the RS485 nodes is too big or there is some kind of
interference.

.. versionadded:: 1.2.0
""",
'de':
"""
Gibt den CRC Fehlerzähler der RS485 Kommunikation zurück. Wenn dieser Zähler
ansteigt ist es wahrscheinlich, dass der Abstand zwischen zwei RS485-Teilnehmern
zu groß ist oder es Störungen gibt.

.. versionadded:: 1.2.0
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('SetRS485Configuration', 'set_rs485_configuration'), 
'elements': [('speed', 'uint32', 1, 'in'),
             ('parity', 'char', 1, 'in'),
             ('stopbits', 'uint8', 1, 'in')], 
'doc': ['af', {
'en':
"""
Sets the configuration of the RS485 Extension. Speed is given in baud. The
Master Brick will try to match the given baud rate as exactly as possible.
The maximum recommended baud rate is 2000000 (2Mbit).
Possible values for parity are 'n' (none), 'e' (even) and 'o' (odd).
Possible values for stop bits are 1 and 2.

If your RS485 is unstable (lost messages etc), the first thing you should
try is to decrease the speed. On very large bus (e.g. 1km), you probably
should use a value in the range of 100khz.

The values are stored in the EEPROM and only applied on startup. That means
you have to restart the Master Brick after configuration.

.. versionadded:: 1.2.0
""",
'de':
"""
Setzt die Schnittstellenkonfiguration der RS485 Extension. Die Geschwindigkeit
wird in Baud angegeben. Der Master Brick versucht die vorgegebene Baudrate so
genau wie möglich zu erreichen. Die maximale empfohlene Baudrate ist 2000000 (2Mbit).
Mögliche Werte für die Parität sind 'n' (keine), 'e' (gerade) und 'o' (ungerade).
Mögliche Werte für Stoppbits sind 1 und 2.

Wenn die RS485 Kommunikation instabil ist (verlorene Nachrichten etc.), sollte zuerst
die Baudrate verringert werden. Sehr lange Busleitungen (z.B. 1km) sollten möglichst
Werte im Bereich von 100000 verwenden.

Die Werte sind im EEPROM gespeichert und werden nur beim Hochfahren angewandt.
Das bedeutet der Master Brick muss nach einer Konfiguration neugestartet werden.

.. versionadded:: 1.2.0
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('GetRS485Configuration', 'get_rs485_configuration'), 
'elements': [('speed', 'uint32', 1, 'out'),
             ('parity', 'char', 1, 'out'),
             ('stopbits', 'uint8', 1, 'out')], 
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`SetRS485Configuration`.

.. versionadded:: 1.2.0
""",
'de':
"""
Gibt die Schnittstellenkonfiguration zurück, wie von :func:`SetRS485Configuration`
gesetzt.

.. versionadded:: 1.2.0
"""
}]
})
