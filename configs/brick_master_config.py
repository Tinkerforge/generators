# -*- coding: utf-8 -*-

# Master Brick communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'version': [1, 3, 0],
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
The maximum recommended baud rate is 2000000 (2Mbit/s).
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
genau wie möglich zu erreichen. Die maximale empfohlene Baudrate ist 2000000 (2Mbit/s).
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

com['packets'].append({
'type': 'function', 
'name': ('IsWifiPresent', 'is_wifi_present'), 
'elements': [('present', 'bool', 1, 'out')], 
'doc': ['af', {
'en':
"""
Returns *true* if a WIFI Extension is available to be used by the Master.

.. versionadded:: 1.2.0
""",
'de':
"""
Gibt zurück ob eine WIFI Extension zur Nutzung durch den Master verfügbar ist.

.. versionadded:: 1.2.0
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('SetWifiConfiguration', 'set_wifi_configuration'), 
'elements': [('ssid', 'string', 32, 'in'),
             ('connection', 'uint8', 1, 'in'),
             ('ip', 'uint8', 4, 'in'),
             ('subnet_mask', 'uint8', 4, 'in'),
             ('gateway', 'uint8', 4, 'in'),
             ('port', 'uint16', 1, 'in')], 
'doc': ['af', {
'en':
"""
Sets the configuration of the WIFI Extension. The ssid can have a max length
of 32 characters, the connection is either 0 for DHCP or 1 for static IP.

If you set connection to 1, you have to supply ip, subnet mask and gateway
as an array of size 4 (first element of the array is the least significant
byte of the address). If connection is set to 0 ip, subnet mask and gateway
are ignored, you can set them to 0.

The last parameter is the port that your program will connect to. The
default port, that is used by brickd, is 4223.

The values are stored in the EEPROM and only applied on startup. That means
you have to restart the Master Brick after configuration.

It is recommended to use the Brick Viewer to set the WIFI configuration.

.. versionadded:: 1.3.0
""",
'de':
"""
Setzt die Konfiguration der WIFI Extension. Die ssid darf eine maximale
Länge von 32 Zeichen haben, die connection ist entweder 0 für DHCP oder
1 für eine statische IP.

Wenn die connection auf 1 gesetzt wird, müssen ip, subnet mask und gateway
als ein Array der größe 4 angegeben werden. Dabei ist das erste Element
im Array das niederwertigste Byte. Falls die connection auf 0 gesetzt ist,
werden ip, subnet mask und gateway ignoriert.

Der letzte Parameter ist der port auf den das Anwendungsprogramm sich
verbindet. Der Standardport von brickd ist 4223.

Die Werte sind im EEPROM gespeichert und werden nur beim Hochfahren angewandt.
Das bedeutet der Master Brick muss nach einer Konfiguration neugestartet werden.

Wir empfehlen die Brick Viewer zu nutzen um die WIFI Extension zu
konfigurieren.

.. versionadded:: 1.3.0
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('GetWifiConfiguration', 'get_wifi_configuration'), 
'elements': [('ssid', 'string', 32, 'out'),
             ('connection', 'uint8', 1, 'out'),
             ('ip', 'uint8', 4, 'out'),
             ('subnet_mask', 'uint8', 4, 'out'),
             ('gateway', 'uint8', 4, 'out'),
             ('port', 'uint16', 1, 'out')], 
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`SetWifiConfiguration`.

.. versionadded:: 1.3.0
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`SetWifiConfiguration`
gesetzt.

.. versionadded:: 1.3.0
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('SetWifiEncryption', 'set_wifi_encryption'), 
'elements': [('encryption', 'uint8', 1, 'in'),
             ('key', 'string', 50, 'in'),
             ('key_index', 'uint8', 1, 'in'),
             ('eap_options', 'uint8', 1, 'in'),
             ('ca_certificate_length', 'uint16', 1, 'in'), 
             ('client_certificate_length', 'uint16', 1, 'in'), 
             ('private_key_length', 'uint16', 1, 'in')], 
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
 "3", "Open Network"

The key has a max length of 50 characters and is used if encryption
is set to 0 or 2 (WPA or WEP). Otherwise the value is ignored.
For WEP it is possible to set the key index (1-4). If you don't know your
key index, it is likely 1.

If you choose WPA Enterprise as encryption, you have to set eap options and
the length of the certificates (for other encryption types these paramters
are ignored). The certificate length are given in byte and the certificates
themself can be set with  :func:`SetWifiCertificate`. Eap options consist of 
the outer authentication (bits 1-2), inner authentication (bit 3) and 
certificate type (bits 4-5):

.. csv-table::
 :header: "Option", "Bits", "Description"
 :widths: 10, 10, 80

 "outer auth", "1-2", "0=EAP-FAST, 1=EAP-TLS, 2=EAP-TTLS, 3=EAP-PEAP"
 "inner auth", "3", "0=EAP-MSCHAP, 1=EAP-GTC"
 "cert type", "4-5", "0=CA Certificate, 1=Client Certificate, 2=Private Key"

Example for EAP-TTLS + EAP-GTC + Private Key: option = 2 | (1 << 2) | (2 << 3).

The values are stored in the EEPROM and only applied on startup. That means
you have to restart the Master Brick after configuration.

It is recommended to use the Brick Viewer to set the WIFI encryption.

.. versionadded:: 1.3.0
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
 "3", "Offenes Netzwerk"

Key hat eine maximale Länge von 50 Zeichen und wird benutzt falls
encryption auf 0 oder 2 (WPA oder WEP) gesetzt ist. Andernfalls wird key
ignoriert. Für WEP gibt es die Möglichkeit den key index zu setzen
(1-4). Fall der key index unbekannt ist, ist er wahrscheinlich 1.

Wenn WPA Enterprise als encryption gewählt wird, müssen eap options und
die Länge der Zertifikate gesetzt werden. Die Länge wird in Byte angegeben
und die Zertifikate selbst können mit :func:`SetWifiCertificate` übertragen
werden. Die eap options bestehen aus outer authentication (Bits 1-2), 
inner authentication (Bit 3) und certificate type (bits 4-5):

.. csv-table::
 :header: "Option", "Bits", "Beschreibung"
 :widths: 10, 10, 80

 "outer auth", "1-2", "0=EAP-FAST, 1=EAP-TLS, 2=EAP-TTLS, 3=EAP-PEAP"
 "inner auth", "3", "0=EAP-MSCHAP, 1=EAP-GTC"
 "cert type", "4-5", "0=CA Certificate, 1=Client Certificate, 2=Private Key"

Beispiel für EAP-TTLS + EAP-GTC + Private Key: option = 2 | (1 << 2) | (2 << 3).

Die Werte sind im EEPROM gespeichert und werden nur beim Hochfahren angewandt.
Das bedeutet der Master Brick muss nach einer Konfiguration neugestartet werden.

Wir empfehlen die Brick Viewer zu nutzen um die WIFI Extension Verschlüsselung
zu konfigurieren.

.. versionadded:: 1.3.0
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('GetWifiEncryption', 'get_wifi_encryption'), 
'elements': [('encryption', 'uint8', 1, 'out'),
             ('key', 'string', 50, 'out'),
             ('key_index', 'uint8', 1, 'out'),
             ('eap_options', 'uint8', 1, 'out'),
             ('ca_certificate_length', 'uint16', 1, 'out'), 
             ('client_certificate_length', 'uint16', 1, 'out'), 
             ('private_key_length', 'uint16', 1, 'out')], 
'doc': ['af', {
'en':
"""
Returns the encryption as set by :func:`SetWifiEncryption`.

.. versionadded:: 1.3.0
""",
'de':
"""
Gibt die Verschlüsselungseinstellungen zurück, wie von 
:func:`SetWifiEncryption` gesetzt.

.. versionadded:: 1.3.0
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('GetWifiStatus', 'get_wifi_status'), 
'elements': [('mac_address', 'uint8', 6, 'out'),
             ('bssid', 'uint8', 6, 'out'),
             ('channel', 'uint8', 1, 'out'),
             ('rssi', 'int16', 1, 'out'),
             ('ip', 'uint8', 4, 'out'),
             ('subnet_mask', 'uint8', 4, 'out'),
             ('gateway', 'uint8', 4, 'out'),
             ('rx_count', 'uint32', 1, 'out'),
             ('tx_count', 'uint32', 1, 'out'),
             ('state', 'uint8', 1, 'out')],
'doc': ['af', {
'en':
"""
Returns the status of the WIFI Extension. The state is updated automatically,
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

.. versionadded:: 1.3.0
""",
'de':
"""
Gibt den Status der WIFI Extension zurück. State wird automatisch aktualisiert,
alle anderen Parameter werden nur beim Starten und nach jedem Aufruf von
:func:`RefreshWifiStatus` aktualisiert.

Mögliche Werte für state sind:

.. csv-table::
 :header: "State", "Beschreibung"
 :widths: 10, 90

 "0", "Getrennt"
 "1", "Verbunden"
 "2", "Am Verbinden"
 "3", "Error"
 "255", "Noch nicht initialisiert"


.. versionadded:: 1.3.0
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('RefreshWifiStatus', 'refresh_wifi_status'), 
'elements': [],
'doc': ['af', {
'en':
"""
Refreshes the WIFI status (see :func:`GetWifiStatus`). To read the status
of the WIFI module, the Master Brick has to change from data mode to
command mode and back. This transaction and the readout itself is
unfortunately time consuming. This means, that it might take some ms
until the stack with attached WIFI Extensions reacts again after this
function is called.

.. versionadded:: 1.3.0
""",
'de':
"""
Aktualisiert den WIFI Status (siehe :func:`GetWifiStatus`). Um den Status
vom WIFI Modul zu lesen, muss der Master Brick vom Datenmodus in den
Kommandomodus und wieder zurück wechseln. Dieser Wechsel und das eigentliche
Auslesen ist leider zeitaufwändig. Dass heißt, es dauert ein paar ms bis der
Stapel mit aufgesteckter WIFI Extension wieder reagiert nachdem die
Funktion aufgerufen wurde.

.. versionadded:: 1.3.0
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('SetWifiCertificate', 'set_wifi_certificate'), 
'elements': [('index', 'uint16', 1, 'in'),
             ('data', 'string', 32, 'in'),
             ('data_length', 'uint8', 1, 'in')], 
'doc': ['af', {
'en':
"""
This function is used to set the certificate as well as password and username
for WPA Enterprise. To set the username use index 0xFFFF,
to set the password use index 0xFFFE. The max length of username and 
password is 32.

The certificate is written in chunks of size 32 and the index is used as
the index of the chunk. The data length should nearly always be 32. Only
the last chunk can have a length that is not equal to 32.

The starting index of the CA Certificate is 0, of the Client Certificate
10000 and for the Private Key 20000. Maximum sizes are 1312, 1312 and
4320 byte respectively.

The values are stored in the EEPROM and only applied on startup. That means
you have to restart the Master Brick after uploading the certificate.

It is recommended to use the Brick Viewer to set the certificate, username
and password.

.. versionadded:: 1.3.0
""",
'de':
"""
Diese Funktion kann benutzt werden um sowohl das Zertifikat als auch
Benutzername und Passwort für WPA Enterprise zu setzen. Für den Benutzernamen
muss Index 0xFFFF und für das Password Index 0xFFFE genutzt werden.
Die maximale Länge für beide ist 32.

Das Zertifikat wird in Chunks der Größe 32 geschrieben und der Index
gibt den Index des Chunk an. Data length sollte fast immer auf 32 gesetzt
werden. Nur beim letzten Chunk ist eine Länge ungleich 32 möglich.

Der Startindex für CA Certificate ist 0, für Client Certificate 10000 und
für Private Key 20000. Die Maximalen Dateigrößen sind jeweils 1312, 1312 und 
4320 Byte.

Die Werte sind im EEPROM gespeichert und werden nur beim Hochfahren angewandt.
Das bedeutet der Master Brick muss nach einer Konfiguration neugestartet werden.

Wir empfehlen die Brick Viewer zu nutzen um die WIFI Extension Verschlüsselung
zu konfigurieren.

.. versionadded:: 1.3.0
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('GetWifiCertificate', 'get_wifi_certificate'), 
'elements': [('index', 'uint16', 1, 'in'),
             ('data', 'string', 32, 'out'),
             ('data_length', 'uint8', 1, 'out')], 
'doc': ['af', {
'en':
"""
Returns the certificate for a given index as set by :func:`SetWifiCertificate`.

.. versionadded:: 1.3.0
""",
'de':
"""
Gibt das Zertifikat für einen Index zurück, wie von 
:func:`SetWifiCertificate` gesetzt.

.. versionadded:: 1.3.0
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('SetWifiPowerMode', 'set_wifi_power_mode'), 
'elements': [('mode', 'uint8', 1, 'in')], 
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

.. versionadded:: 1.3.0
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

.. versionadded:: 1.3.0
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('GetWifiPowerMode', 'get_wifi_power_mode'), 
'elements': [('mode', 'uint8', 1, 'out')], 
'doc': ['af', {
'en':
"""
Returns the power mode as set by :func:`SetWifiPowerMode`.

.. versionadded:: 1.3.0
""",
'de':
"""
Gibt den Stromsparmodus zurück, wie von :func:`SetWifiPowerMode` gesetzt.

.. versionadded:: 1.3.0
"""
}]
})
