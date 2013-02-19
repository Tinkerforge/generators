# -*- coding: utf-8 -*-

# Master Brick communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'category': 'Brick',
    'device_identifier': 13,
    'name': ('Master', 'master', 'Master'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for controlling Stacks and four Bricklets',
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetStackVoltage', 'get_stack_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')], 
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
'name': ('GetStackCurrent', 'get_stack_current'), 
'elements': [('current', 'uint16', 1, 'out')], 
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
'name': ('SetExtensionType', 'set_extension_type'), 
'elements': [('extension', 'uint8', 1, 'in'),
             ('exttype', 'uint32', 1, 'in', ('ExtensionType', 'extension_type', [('Chibi', 'chibi', 1),
                                                                                 ('RS485', 'rs485', 2),
                                                                                 ('Wifi', 'wifi', 3),
                                                                                 ('Ethernet', 'ethernet', 4)]))], 
'since_firmware': [1, 0, 0],
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
 "3",    "WIFI"
 "4",    "Ethernet"

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
 :widths: 10, 100
 
 "1",    "Chibi"
 "2",    "RS485"
 "3",    "WIFI"
 "4",    "Ethernet"

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
             ('exttype', 'uint32', 1, 'out', ('ExtensionType', 'extension_type', [('Chibi', 'chibi', 1),
                                                                                  ('RS485', 'rs485', 2),
                                                                                  ('Wifi', 'wifi', 3),
                                                                                  ('Ethernet', 'ethernet', 4)]))],
'since_firmware': [1, 0, 0],
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
'since_firmware': [1, 1, 0],
'doc': ['af', {
'en':
"""
Returns *true* if a Chibi Extension is available to be used by the Master.
""",
'de':
"""
Gibt zurück ob eine Chibi Extension zur Nutzung durch den Master verfügbar ist.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetChibiAddress', 'set_chibi_address'), 
'elements': [('address', 'uint8', 1, 'in')], 
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
jedem Hochfahren ist daher nicht notwendig.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetChibiAddress', 'get_chibi_address'), 
'elements': [('address', 'uint8', 1, 'out')], 
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
'name': ('SetChibiMasterAddress', 'set_chibi_master_address'), 
'elements': [('address', 'uint8', 1, 'in')], 
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
jedem Hochfahren ist daher nicht notwendig.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetChibiMasterAddress', 'get_chibi_master_address'), 
'elements': [('address', 'uint8', 1, 'out')], 
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
'name': ('SetChibiSlaveAddress', 'set_chibi_slave_address'), 
'elements': [('num', 'uint8', 1, 'in'),
             ('address', 'uint8', 1, 'in')], 
'since_firmware': [1, 1, 0],
'doc': ['af', {
'en':
"""
Sets up to 254 slave addresses. Valid addresses are in range 1-255. 0 has a
special meaning, it is used as list terminator and not allowed as normal slave
address. The address numeration (via num parameter) has to be used
ascending from 0. For example: If you use the Chibi Extension in Master mode
(i.e. the stack has an USB connection) and you want to talk to three other
Chibi stacks with the slave addresses 17, 23, and 42, you should call with
"(0, 17), (1, 23), (2, 42) and (3, 0)". The last call with "(3, 0)" is a list
terminator and indicates that the Chibi slave address list contains 3 addresses
in this case.

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
Die Adressnummerierung (mittels num Parameter) muss aufsteigend ab
0 erfolgen. Beispiel: Wenn die Chibi Extension im Master Modus verwendet wird
(z.B. wenn der Stapel eine USB-Verbindung hat) und es soll mit drei weiteren
Chibi Stapeln kommuniziert werden, mit den Adressen 17, 23 und 42, sollten die
Aufrufe "(0, 17), (1, 23), (2, 42) und (3, 0)" sein. Der letzte Aufruf mit
"(3, 0)" dient der Terminierung der Liste und zeigt an, dass die Chibi Slave
Adressliste in diesem Fall 3 Einträge beinhaltet.

Es ist möglich die Adressen mit dem Brick Viewer zu setzen, dieser kümmert sich
dann um korrekte Adressnummerierung und Terminierung der Liste.

Die Slave Adresse werden im EEPROM der RS485 Extension abgespeichert. Ein
Setzen bei jedem Hochfahren ist daher nicht notwendig.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetChibiSlaveAddress', 'get_chibi_slave_address'), 
'elements': [('num', 'uint8', 1, 'in'),
             ('address', 'uint8', 1, 'out')], 
'since_firmware': [1, 1, 0],
'doc': ['af', {
'en':
"""
Returns the slave address for a given num as set by 
:func:`SetChibiSlaveAddress`.
""",
'de':
"""
Gibt die Slave Adresse für eine Adressnummerierung (mittels num Parameter) zurück,
wie von :func:`SetChibiSlaveAddress` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetChibiSignalStrength', 'get_chibi_signal_strength'), 
'elements': [('signal_strength', 'uint8', 1, 'out')], 
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
'name': ('GetChibiErrorLog', 'get_chibi_error_log'), 
'elements': [('underrun', 'uint16', 1, 'out'),
             ('crc_error', 'uint16', 1, 'out'),
             ('no_ack', 'uint16', 1, 'out'),
             ('overflow', 'uint16', 1, 'out')], 
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
'name': ('SetChibiFrequency', 'set_chibi_frequency'), 
'elements': [('frequency', 'uint8', 1, 'in', ('ChibiFrequency', 'chibi_frequency', [('OQPSK868MHz', 'oqpsk_868_mhz', 0),
                                                                                    ('OQPSK915MHz', 'oqpsk_915_mhz', 1),
                                                                                    ('OQPSK780MHz', 'oqpsk_780_mhz', 2),
                                                                                    ('BPSK40915MHz', 'bpsk40_915_mhz', 3)]))],
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
jedem Hochfahren ist daher nicht notwendig.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetChibiFrequency', 'get_chibi_frequency'), 
'elements': [('frequency', 'uint8', 1, 'out', ('ChibiFrequency', 'chibi_frequency', [('OQPSK868MHz', 'oqpsk_868_mhz', 0),
                                                                                     ('OQPSK915MHz', 'oqpsk_915_mhz', 1),
                                                                                     ('OQPSK780MHz', 'oqpsk_780_mhz', 2),
                                                                                     ('BPSK40915MHz', 'bpsk40_915_mhz', 3)]))],
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
'name': ('SetChibiChannel', 'set_chibi_channel'), 
'elements': [('channel', 'uint8', 1, 'in')], 
'since_firmware': [1, 1, 0],
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
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetChibiChannel', 'get_chibi_channel'), 
'elements': [('channel', 'uint8', 1, 'out')], 
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
'name': ('IsRS485Present', 'is_rs485_present'), 
'elements': [('present', 'bool', 1, 'out')], 
'since_firmware': [1, 2, 0],
'doc': ['af', {
'en':
"""
Returns *true* if a RS485 Extension is available to be used by the Master.
""",
'de':
"""
Gibt zurück ob eine RS485 Extension zur Nutzung durch den Master verfügbar ist.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('SetRS485Address', 'set_rs485_address'), 
'elements': [('address', 'uint8', 1, 'in')], 
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
jedem Hochfahren ist daher nicht notwendig.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('GetRS485Address', 'get_rs485_address'), 
'elements': [('address', 'uint8', 1, 'out')], 
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
'name': ('SetRS485SlaveAddress', 'set_rs485_slave_address'),
'elements': [('num', 'uint8', 1, 'in'),
             ('address', 'uint8', 1, 'in')], 
'since_firmware': [1, 2, 0],
'doc': ['af', {
'en':
"""
Sets up to 255 slave addresses. Valid addresses are in range 1-255. 0 has a
special meaning, it is used as list terminator and not allowed as normal slave
address. The address numeration (via num parameter) has to be used
ascending from 0. For example: If you use the RS485 Extension in Master mode
(i.e. the stack has an USB connection) and you want to talk to three other
RS485 stacks with the addresses 17, 23, and 42, you should call with "(0, 17),
(1, 23), (2, 42) and (3, 0)". The last call with "(3, 0)" is a list terminator
and indicates that the RS485 slave address list contains 3 addresses in this
case.

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
Die Adressnummerierung (mittels num Parameter) muss aufsteigend ab
0 erfolgen. Beispiel: Wenn die RS485 Extension im Master Modus verwendet wird
(z.B. wenn der Stapel eine USB-Verbindung hat) und es soll mit drei weiteren
RS485 Stapeln kommuniziert werden, mit den Adressen 17, 23 und 42, sollten die
Aufrufe "(0, 17), (1, 23), (2, 42) und (3, 0)" sein. Der letzte Aufruf mit
"(3, 0)" dient der Terminierung der Liste und zeigt an, dass die RS485 Slave
Adressliste in diesem Fall 3 Einträge beinhaltet.

Es ist möglich die Adressen mit dem Brick Viewer zu setzen, dieser kümmert sich
dann um korrekte Adressnummerierung und Terminierung der Liste.

Die Slave Adresse werden im EEPROM der RS485 Extension abgespeichert. Ein
Setzen bei jedem Hochfahren ist daher nicht notwendig.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('GetRS485SlaveAddress', 'get_rs485_slave_address'), 
'elements': [('num', 'uint8', 1, 'in'),
             ('address', 'uint8', 1, 'out')], 
'since_firmware': [1, 2, 0],
'doc': ['af', {
'en':
"""
Returns the slave address for a given num as set by 
:func:`SetRS485SlaveAddress`.
""",
'de':
"""
Gibt die Slave Adresse für eine Adressnummerierung (mittels num Parameter) zurück,
wie von :func:`SetRS485SlaveAddress` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('GetRS485ErrorLog', 'get_rs485_error_log'), 
'elements': [('crc_error', 'uint16', 1, 'out')], 
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
'name': ('SetRS485Configuration', 'set_rs485_configuration'), 
'elements': [('speed', 'uint32', 1, 'in'),
             ('parity', 'char', 1, 'in', ('RS485Parity', 'rs485_parity', [('None', 'none', 'n'),
                                                                          ('Even', 'even', 'e'),
                                                                          ('Odd', 'odd', 'o')])),
             ('stopbits', 'uint8', 1, 'in')], 
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
genau wie möglich zu erreichen. Die maximale empfohlene Baudrate ist 2000000 (2Mbit/s).
Mögliche Werte für die Parität sind 'n' (keine), 'e' (gerade) und 'o' (ungerade).
Mögliche Werte für Stoppbits sind 1 und 2.

Wenn die RS485 Kommunikation instabil ist (verlorene Nachrichten etc.), sollte zuerst
die Baudrate verringert werden. Sehr lange Busleitungen (z.B. 1km) sollten möglichst
Werte im Bereich von 100000 (100kbit/s) verwenden.

Die Werte sind im EEPROM gespeichert und werden nur beim Hochfahren angewandt.
Das bedeutet der Master Brick muss nach einer Konfiguration neugestartet werden.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('GetRS485Configuration', 'get_rs485_configuration'), 
'elements': [('speed', 'uint32', 1, 'out'),
             ('parity', 'char', 1, 'out', ('RS485Parity', 'rs485_parity', [('None', 'none', 'n'),
                                                                           ('Even', 'even', 'e'),
                                                                           ('Odd', 'odd', 'o')])),
             ('stopbits', 'uint8', 1, 'out')], 
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
'name': ('IsWifiPresent', 'is_wifi_present'), 
'elements': [('present', 'bool', 1, 'out')], 
'since_firmware': [1, 2, 0],
'doc': ['af', {
'en':
"""
Returns *true* if a WIFI Extension is available to be used by the Master.
""",
'de':
"""
Gibt zurück ob eine WIFI Extension zur Nutzung durch den Master verfügbar ist.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('SetWifiConfiguration', 'set_wifi_configuration'), 
'elements': [('ssid', 'string', 32, 'in'),
             ('connection', 'uint8', 1, 'in', ('WifiConnection', 'wifi_connection', [('DHCP', 'dhcp', 0),
                                                                                     ('StaticIP', 'static_ip', 1),
                                                                                     ('AccessPointDHCP', 'access_point_dhcp', 2),
                                                                                     ('AccessPointStaticIP', 'access_point_static_ip', 3),
                                                                                     ('AdHocDHCP', 'ad_hoc_dhcp', 4),
                                                                                     ('AdHocStaticIP', 'ad_hoc_static_ip', 5)])),
             ('ip', 'uint8', 4, 'in'),
             ('subnet_mask', 'uint8', 4, 'in'),
             ('gateway', 'uint8', 4, 'in'),
             ('port', 'uint16', 1, 'in')], 
'since_firmware': [1, 3, 0],
'doc': ['af', {
'en':
"""
Sets the configuration of the WIFI Extension. The *ssid* can have a max length
of 32 characters. Possible values for *connection* are:

.. csv-table::
 :header: "Value", "Description"
 :widths: 10, 90

 "0", "DHCP"
 "1", "Static IP"
 "2", "Access Point: DHCP"
 "3", "Access Point: Static IP"
 "4", "Ad Hoc: DHCP"
 "5", "Ad Hoc: Static IP"

If you set *connection* to one of the static IP options then you have to supply
*ip*, *subnet_mask* and *gateway* as an array of size 4 (first element of the
array is the least significant byte of the address). If *connection* is set to
one of the DHCP options then *ip*, *subnet_mask* and *gateway* are ignored, you
can set them to 0.

The last parameter is the port that your program will connect to. The
default port, that is used by brickd, is 4223.

The values are stored in the EEPROM and only applied on startup. That means
you have to restart the Master Brick after configuration.

It is recommended to use the Brick Viewer to set the WIFI configuration.
""",
'de':
"""
Setzt die Konfiguration der WIFI Extension. Die *ssid* darf eine maximale
Länge von 32 Zeichen haben. Mögliche Werte für *connection* sind:

.. csv-table::
 :header: "Wert", "Beschreibung"
 :widths: 10, 90

 "0", "DHCP"
 "1", "Statische IP"
 "2", "Access Point: DHCP"
 "3", "Access Point: Statische IP"
 "4", "Ad Hoc: DHCP"
 "5", "Ad Hoc: Statische IP"

Wenn *connection* auf eine der statische IP Optionen gesetzt wird, dann müssen
*ip*, *subnet_mask* und *gateway* als ein Array der größe 4 angegeben werden.
Dabei ist das erste Element im Array das niederwertigste Byte. Falls
*connection* auf eine der DHCP Optionen gesetzt ist, werden *ip*, *subnet_mask*
und *gateway* ignoriert.

Der letzte Parameter ist der port auf den das Anwendungsprogramm sich
verbindet. Der Standardport von brickd ist 4223.

Die Werte sind im EEPROM gespeichert und werden nur beim Hochfahren angewandt.
Das bedeutet der Master Brick muss nach einer Konfiguration neugestartet werden.

Wir empfehlen die Brick Viewer zu nutzen um die WIFI Extension zu
konfigurieren.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('GetWifiConfiguration', 'get_wifi_configuration'), 
'elements': [('ssid', 'string', 32, 'out'),
             ('connection', 'uint8', 1, 'out', ('WifiConnection', 'wifi_connection', [('DHCP', 'dhcp', 0),
                                                                                      ('StaticIP', 'static_ip', 1),
                                                                                      ('AccessPointDHCP', 'access_point_dhcp', 2),
                                                                                      ('AccessPointStaticIP', 'access_point_static_ip', 3),
                                                                                      ('AdHocDHCP', 'ad_hoc_dhcp', 4),
                                                                                      ('AdHocStaticIP', 'ad_hoc_static_ip', 5)])),
             ('ip', 'uint8', 4, 'out'),
             ('subnet_mask', 'uint8', 4, 'out'),
             ('gateway', 'uint8', 4, 'out'),
             ('port', 'uint16', 1, 'out')], 
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
'name': ('SetWifiEncryption', 'set_wifi_encryption'), 
'elements': [('encryption', 'uint8', 1, 'in', ('WifiEncryption', 'wifi_encryption', [('WPAWPA2', 'wpa_wpa2', 0),
                                                                                     ('WPAEnterprise', 'wpa_enterprise', 1),
                                                                                     ('WEP', 'wep', 2),
                                                                                     ('NoEncryption', 'no_encryption', 3)])),
             ('key', 'string', 50, 'in'),
             ('key_index', 'uint8', 1, 'in'),
             ('eap_options', 'uint8', 1, 'in', ('WifiEAPOption', 'wifi_eap_option', [('OuterAuthEAPFAST', 'outer_auth_eap_fast', 0),
                                                                                     ('OuterAuthEAPTLS', 'outer_auth_eap_tls', 1),
                                                                                     ('OuterAuthEAPTTLS', 'outer_auth_eap_ttls', 2),
                                                                                     ('OuterAuthEAPPEAP', 'outer_auth_eap_peap', 3),
                                                                                     ('InnerAuthEAPMSCHAP', 'inner_auth_eap_mschap', 0),
                                                                                     ('InnerAuthEAPGTC', 'inner_auth_eap_gtc', 4),
                                                                                     ('CertTypeCACert', 'cert_type_ca_cert', 0),
                                                                                     ('CertTypeClientCert', 'cert_type_client_cert', 8),
                                                                                     ('CertTypePrivateKey', 'cert_type_private_key', 16)])),
             ('ca_certificate_length', 'uint16', 1, 'in'), 
             ('client_certificate_length', 'uint16', 1, 'in'), 
             ('private_key_length', 'uint16', 1, 'in')], 
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

The key has a max length of 50 characters and is used if encryption
is set to 0 or 2 (WPA/WPA2 or WEP). Otherwise the value is ignored.

For WPA/WPA2 the key has to be at least 8 characters long. If you want to set
a key with more than 50 characters, see :func:`SetLongWifiKey`.

For WEP the key has to be either 10 or 26 hexdecimal digits long. It is
possible to set the WEP key index (1-4). If you don't know your key index,
it is likely 1.

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

Key hat eine maximale Länge von 50 Zeichen und wird benutzt falls
encryption auf 0 oder 2 (WPA/WPA2 oder WEP) gesetzt ist. Andernfalls wird key
ignoriert.

Für WPA/WPA2 muss der Schlüssel mindestens 8 Zeichen lang sein. Wenn ein Schlüssel
mit mehr als 50 Zeichen gesetzt werden soll, kann :func:`SetLongWifiKey`
genutzt werden.

Für WEP muss der Schlüssel entweder 10 oder 26 hexadezimale Zeichen lang sein.
Es ist möglich den key index zu setzen (1-4). Fall der key index unbekannt ist,
ist er wahrscheinlich 1.

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
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('GetWifiEncryption', 'get_wifi_encryption'), 
'elements': [('encryption', 'uint8', 1, 'out', ('WifiEncryption', 'wifi_encryption', [('WPAWPA2', 'wpa_wpa2', 0),
                                                                                      ('WPAEnterprise', 'wpa_enterprise', 1),
                                                                                      ('WEP', 'wep', 2),
                                                                                      ('NoEncryption', 'no_encryption', 3)])),
             ('key', 'string', 50, 'out'),
             ('key_index', 'uint8', 1, 'out'),
             ('eap_options', 'uint8', 1, 'out', ('WifiEAPOption', 'wifi_eap_option', [('OuterAuthEAPFAST', 'outer_auth_eap_fast', 0),
                                                                                      ('OuterAuthEAPTLS', 'outer_auth_eap_tls', 1),
                                                                                      ('OuterAuthEAPTTLS', 'outer_auth_eap_ttls', 2),
                                                                                      ('OuterAuthEAPPEAP', 'outer_auth_eap_peap', 3),
                                                                                      ('InnerAuthEAPMSCHAP', 'inner_auth_eap_mschap', 0),
                                                                                      ('InnerAuthEAPGTC', 'inner_auth_eap_gtc', 4),
                                                                                      ('CertTypeCACert', 'cert_type_ca_cert', 0),
                                                                                      ('CertTypeClientCert', 'cert_type_client_cert', 8),
                                                                                      ('CertTypePrivateKey', 'cert_type_private_key', 16)])),
             ('ca_certificate_length', 'uint16', 1, 'out'), 
             ('client_certificate_length', 'uint16', 1, 'out'), 
             ('private_key_length', 'uint16', 1, 'out')], 
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
             ('state', 'uint8', 1, 'out', ('WifiState', 'wifi_state', [('Disassociated', 'disassociated', 0),
                                                                       ('Associated', 'associated', 1),
                                                                       ('Associating', 'associating', 2),
                                                                       ('Error', 'error', 3),
                                                                       ('NotInitializedYet', 'not_initialized_yet', 255)]))],
'since_firmware': [1, 3, 0],
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
""",
'de':
"""
Gibt den Status der WIFI Extension zurück. State wird automatisch aktualisiert,
alle anderen Parameter werden nur beim Starten und nach jedem Aufruf von
:func:`RefreshWifiStatus` aktualisiert.

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
'name': ('RefreshWifiStatus', 'refresh_wifi_status'), 
'elements': [],
'since_firmware': [1, 3, 0],
'doc': ['af', {
'en':
"""
Refreshes the WIFI status (see :func:`GetWifiStatus`). To read the status
of the WIFI module, the Master Brick has to change from data mode to
command mode and back. This transaction and the readout itself is
unfortunately time consuming. This means, that it might take some ms
until the stack with attached WIFI Extensions reacts again after this
function is called.
""",
'de':
"""
Aktualisiert den WIFI Status (siehe :func:`GetWifiStatus`). Um den Status
vom WIFI Modul zu lesen, muss der Master Brick vom Datenmodus in den
Kommandomodus und wieder zurück wechseln. Dieser Wechsel und das eigentliche
Auslesen ist leider zeitaufwändig. Dass heißt, es dauert ein paar ms bis der
Stapel mit aufgesteckter WIFI Extension wieder reagiert nachdem die
Funktion aufgerufen wurde.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('SetWifiCertificate', 'set_wifi_certificate'), 
'elements': [('index', 'uint16', 1, 'in'),
             ('data', 'uint8', 32, 'in'),
             ('data_length', 'uint8', 1, 'in')], 
'since_firmware': [1, 3, 0],
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
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('GetWifiCertificate', 'get_wifi_certificate'), 
'elements': [('index', 'uint16', 1, 'in'),
             ('data', 'uint8', 32, 'out'),
             ('data_length', 'uint8', 1, 'out')], 
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
'name': ('SetWifiPowerMode', 'set_wifi_power_mode'),
'elements': [('mode', 'uint8', 1, 'in', ('WifiPowerMode', 'wifi_power_mode', [('FullSpeed', 'full_speed', 0),
                                                                              ('LowPower', 'low_power', 1)]))],
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
'name': ('GetWifiPowerMode', 'get_wifi_power_mode'), 
'elements': [('mode', 'uint8', 1, 'out', ('WifiPowerMode', 'wifi_power_mode', [('FullSpeed', 'full_speed', 0),
                                                                               ('LowPower', 'low_power', 1)]))],
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
'name': ('GetWifiBufferInfo', 'get_wifi_buffer_info'), 
'elements': [('overflow', 'uint32', 1, 'out'),
             ('low_watermark', 'uint16', 1, 'out'),
             ('used', 'uint16', 1, 'out')],
'since_firmware': [1, 3, 2],
'doc': ['af', {
'en':
"""
Returns informations about the WIFI receive buffer. The WIFI
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
Gibt Informationen über denn WIFI Empfangsbuffer zurück. Der WIFI
Empfangsbuffer hat eine maximale Größe von 1500 Byte und falls zuviele
Daten übertragen werden, kann er überlaufen.

Die Rückgabewerte sind die anzahl der Oveflows, die low watermark
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
'name': ('SetWifiRegulatoryDomain', 'set_wifi_regulatory_domain'), 
'elements': [('domain', 'uint8', 1, 'in', ('WifiDoamin', 'wifi_domain', [('Channel1To11', 'channel_1to11', 0),
                                                                         ('Channel1To13', 'channel_1to13', 1),
                                                                         ('Channel1To14', 'channel_1to14', 2)]))],
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
'name': ('GetWifiRegulatoryDomain', 'get_wifi_regulatory_domain'), 
'elements': [('domain', 'uint8', 1, 'out', ('WifiDoamin', 'wifi_domain', [('Channel1To11', 'channel_1to11', 0),
                                                                          ('Channel1To13', 'channel_1to13', 1),
                                                                          ('Channel1To14', 'channel_1to14', 2)]))],
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
'name': ('GetUSBVoltage', 'get_usb_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')], 
'since_firmware': [1, 3, 5],
'doc': ['af', {
'en':
"""
Returns the USB voltage in mV.
""",
'de':
"""
Gibt die USB Spannung in mV zurück.
"""
}]
})

com['packets'].append({
'type': 'function', 
'name': ('SetLongWifiKey', 'set_long_wifi_key'), 
'elements': [('key', 'string', 64, 'in')],
'since_firmware': [2, 0, 2],
'doc': ['af', {
'en':
"""
Sets a long WIFI key (up to 63 chars, at least 8 chars) for WPA encryption.
This key will be used
if the key in :func:`SetWifiEncryption` is set to "-". In the old protocol,
a payload of size 63 was not possible, so the maximum key length was 50 chars.

With the new protocol this is possible, since we didn't want to break API,
this function was added additionally.
""",
'de':
"""
Setzt einen langen WIFI Schlüssel (bis zu 63 Zeichen, mindestens 8 Zeichen) für
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
'name': ('GetLongWifiKey', 'get_long_wifi_key'), 
'elements': [('key', 'string', 64, 'out')],
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
'name': ('SetWifiHostname', 'set_wifi_hostname'), 
'elements': [('hostname', 'string', 16, 'in')],
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
'name': ('GetWifiHostname', 'get_wifi_hostname'), 
'elements': [('hostname', 'string', 16, 'out')],
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
'name': ('SetStackCurrentCallbackPeriod', 'set_stack_current_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
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
'name': ('GetStackCurrentCallbackPeriod', 'get_stack_current_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
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
'name': ('SetStackVoltageCallbackPeriod', 'set_stack_voltage_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
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
'name': ('GetStackVoltageCallbackPeriod', 'get_stack_voltage_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
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
'name': ('SetUSBVoltageCallbackPeriod', 'set_usb_voltage_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
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
'name': ('GetUSBVoltageCallbackPeriod', 'get_usb_voltage_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
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
'name': ('SetStackCurrentCallbackThreshold', 'set_stack_current_callback_threshold'), 
'elements': [('option', 'char', 1, 'in', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                  ('Outside', 'outside', 'o'),
                                                                                  ('Inside', 'inside', 'i'),
                                                                                  ('Smaller', 'smaller', '<'),
                                                                                  ('Greater', 'greater', '>')])), 
             ('min', 'uint16', 1, 'in'),
             ('max', 'uint16', 1, 'in')],
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
'name': ('GetStackCurrentCallbackThreshold', 'get_stack_current_callback_threshold'), 
'elements': [('option', 'char', 1, 'out', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                   ('Outside', 'outside', 'o'),
                                                                                   ('Inside', 'inside', 'i'),
                                                                                   ('Smaller', 'smaller', '<'),
                                                                                   ('Greater', 'greater', '>')])), 
             ('min', 'uint16', 1, 'out'),
             ('max', 'uint16', 1, 'out')],
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
'name': ('SetStackVoltageCallbackThreshold', 'set_stack_voltage_callback_threshold'), 
'elements': [('option', 'char', 1, 'in', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                  ('Outside', 'outside', 'o'),
                                                                                  ('Inside', 'inside', 'i'),
                                                                                  ('Smaller', 'smaller', '<'),
                                                                                  ('Greater', 'greater', '>')])), 
             ('min', 'uint16', 1, 'in'),
             ('max', 'uint16', 1, 'in')],
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
'name': ('GetStackVoltageCallbackThreshold', 'get_stack_voltage_callback_threshold'), 
'elements': [('option', 'char', 1, 'out', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                   ('Outside', 'outside', 'o'),
                                                                                   ('Inside', 'inside', 'i'),
                                                                                   ('Smaller', 'smaller', '<'),
                                                                                   ('Greater', 'greater', '>')])), 
             ('min', 'uint16', 1, 'out'),
             ('max', 'uint16', 1, 'out')],
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
'name': ('SetUSBVoltageCallbackThreshold', 'set_usb_voltage_callback_threshold'), 
'elements': [('option', 'char', 1, 'in', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                  ('Outside', 'outside', 'o'),
                                                                                  ('Inside', 'inside', 'i'),
                                                                                  ('Smaller', 'smaller', '<'),
                                                                                  ('Greater', 'greater', '>')])), 
             ('min', 'uint16', 1, 'in'),
             ('max', 'uint16', 1, 'in')],
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
'name': ('GetUSBVoltageCallbackThreshold', 'get_usb_voltage_callback_threshold'), 
'elements': [('option', 'char', 1, 'out', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                   ('Outside', 'outside', 'o'),
                                                                                   ('Inside', 'inside', 'i'),
                                                                                   ('Smaller', 'smaller', '<'),
                                                                                   ('Greater', 'greater', '>')])), 
             ('min', 'uint16', 1, 'out'),
             ('max', 'uint16', 1, 'out')],
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
'name': ('SetDebouncePeriod', 'set_debounce_period'), 
'elements': [('debounce', 'uint32', 1, 'in')],
'since_firmware': [2, 0, 5],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the threshold callbacks

 :func:`StackCurrentReached`, :func:`StackVoltageReached`, :func:`USBVoltageReached`

are triggered, if the thresholds

 :func:`SetStackCurrentCallbackThreshold`, :func:`SetStackVoltageCallbackThreshold`, :func:`SetUSBVoltageCallbackThreshold`

keep being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callbacks

 :func:`StackCurrentReached`, :func:`StackVoltageReached`, :func:`USBVoltageReached`
 
ausgelöst werden, wenn die Schwellwerte 

 :func:`SetStackCurrentCallbackThreshold`, :func:`SetStackVoltageCallbackThreshold`, :func:`SetUSBVoltageCallbackThreshold`
 
weiterhin erreicht bleiben.

Der Standardwert ist 100.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetDebouncePeriod', 'get_debounce_period'), 
'elements': [('debounce', 'uint32', 1, 'out')],
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
'name': ('StackCurrent', 'stack_current'), 
'elements': [('current', 'uint16', 1, 'out')],
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
'name': ('StackVoltage', 'stack_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')],
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
'name': ('USBVoltage', 'usb_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')],
'since_firmware': [2, 0, 5],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetUSBVoltageCallbackPeriod`. The :word:`parameter` is the voltage of the
sensor.

:func:`USBVoltage` is only triggered if the voltage has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetUSBVoltageCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die Spannung des Sensors.

:func:`USBVoltage` wird nur ausgelöst wenn sich die Spannung seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('StackCurrentReached', 'stack_current_reached'), 
'elements': [('current', 'uint16', 1, 'out')],
'since_firmware': [2, 0, 5],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetStackCurrentCallbackThreshold` is reached.
The :word:`parameter` is the current of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetStackCurrentCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Stromstärke des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('StackVoltageReached', 'stack_voltage_reached'), 
'elements': [('voltage', 'uint16', 1, 'out')],
'since_firmware': [2, 0, 5],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetStackVoltageCallbackThreshold` is reached.
The :word:`parameter` is the voltage of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetStackVoltageCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Spannung des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('USBVoltageReached', 'usb_voltage_reached'), 
'elements': [('voltage', 'uint16', 1, 'out')],
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
