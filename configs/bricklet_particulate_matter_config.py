# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Particulate Matter Bricklet communication config

com = {
    'author': 'Matthias Bolte <matthias@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2110,
    'name': 'Particulate Matter',
    'display_name': 'Particulate Matter',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'TBD',
        'de': 'TBD'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'discontinued': False,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Get PM Concentration',
'elements': [('PM10', 'uint16', 1, 'out'),
             ('PM25', 'uint16', 1, 'out'),
             ('PM100', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the particulate matter concentration in µg/m³, broken down as:

* PM\ :sub:`1.0`\ ,
* PM\ :sub:`2.5`\  and
* PM\ :sub:`10.0`\ .

If the sensor is disabled (see :func:`Set Enable`) then the last known good
values from the sensor are return.
""",
'de':
"""
Gibt die Feinstaub-Konzentration in µg/m³ zurück, augeschlüsselt nach:

* PM\ :sub:`1.0`\ ,
* PM\ :sub:`2.5`\  und
* PM\ :sub:`10.0`\ .

Wenn der Sensor deaktiviert ist (siehe :func:`Set Enable`), dann wird weiterhin
der letzte Sensorwert zurückgegeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get PM Count',
'elements': [('Greater03um', 'uint16', 1, 'out'),
             ('Greater05um', 'uint16', 1, 'out'),
             ('Greater10um', 'uint16', 1, 'out'),
             ('Greater25um', 'uint16', 1, 'out'),
             ('Greater50um', 'uint16', 1, 'out'),
             ('Greater100um', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the number of particulates in 100 ml of air, broken down by their
diameter:

* greater 0.3µm,
* greater 0.5µm,
* greater 1.0µm,
* greater 2.5µm,
* greater 5.0µm and
* greater 10.0µm.

If the sensor is disabled (see :func:`Set Enable`) then the last known good
value from the sensor is return.
""",
'de':
"""
Gibt die Anzahl der Feinstaub-Teilchen in 100ml Luft zurück, augeschlüsselt
nach deren Durchmesser:

* größer 0,3µm,
* größer 0,5µm,
* größer 1,0µm,
* größer 2,5µm,
* größer 5,0µm und
* größer 10,0µm.

Wenn der Sensor deaktiviert ist (siehe :func:`Set Enable`), dann wird weiterhin
der letzte Sensorwert zurückgegeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Enable',
'elements': [('Enable', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Enables/Disables the fan and the laser diode of the sensors. The sensor is
enabled by default.

The sensor takes about 30 after it is enabled to settle and produce stable
values.
""",
'de':
"""
Aktiviert/deaktiviert den Lüfter und die Laserdiode des Sensors. Der Sensor
ist standardmäßig aktiv.

Der Sensor benötigt ca. 30 Sekunden nach der Aktivierung um sich einzuschwingen
und stabile Werte zu produzieren.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Enable',
'elements': [('Enable', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the state of the sensor as set by :func:`Set Enable`.
""",
'de':
"""
Gibt den Zustand des Sensors zurück, wie von :func:`Set Enable` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Sensor Info',
'elements': [('Sensor Version', 'uint8', 1, 'out'),
             ('Last Error Code', 'uint8', 1, 'out'),
             ('Framing Error Count', 'uint8', 1, 'out'),
             ('Checksum Error Count', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns information about the sensor:

* the sensor version number,
* the last error code reported by the sensor (0 means no error) and
* the number of framing and checksum errors that occurred in the communication
  with the sensor.
""",
'de':
"""
Gibt Informationen über den Sensor zurück:

* die Versionsnummer des Sensors,
* den letzten Fehlercode den der Sensor gemeldet (0 bedeute kein Fehler) hat,
* die Anzahl der Framing und Prüfsummenfehler die in der Kommunikation mit dem
  Sensor aufgetreten sind.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set PM Concentration Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period in ms is the period with which the :cb:`PM Concentration`
callback is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.

The default value is (0, false).
""",
'de':
"""
Die Periode in ms ist die Periode mit der der :cb:`PM Concentration`
Callback ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn der Wert sich im Vergleich zum letzten mal geändert
hat. Ändert der Wert sich nicht innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen des Werts.

Der Standardwert ist (0, false).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get PM Concentration Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set PM Concentration Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set PM Concentration Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set PM Count Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period in ms is the period with which the :cb:`PM Count` callback
is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.

The default value is (0, false).
""",
'de':
"""
Die Periode in ms ist die Periode mit der der :cb:`PM Count` Callback
ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn der Wert sich im Vergleich zum letzten mal geändert
hat. Ändert der Wert sich nicht innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen des Werts.

Der Standardwert ist (0, false).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get PM Count Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set PM Count Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set PM Count Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'PM Concentration',
'elements': [('PM10', 'uint16', 1, 'out'),
             ('PM25', 'uint16', 1, 'out'),
             ('PM100', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set PM Concentration Callback Configuration`.

The `parameters` are the same as :func:`Get PM Concentration`.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set PM Concentration Callback Configuration` gesetzten Konfiguration

Die `parameters` sind der gleiche wie :func:`Get PM Concentration`.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'PM Count',
'elements': [('Greater03um', 'uint16', 1, 'out'),
             ('Greater05um', 'uint16', 1, 'out'),
             ('Greater10um', 'uint16', 1, 'out'),
             ('Greater25um', 'uint16', 1, 'out'),
             ('Greater50um', 'uint16', 1, 'out'),
             ('Greater100um', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set PM Count Callback Configuration`.

The `parameters` are the same as :func:`Get PM Count`.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set PM Count Callback Configuration` gesetzten Konfiguration

Die `parameters` sind der gleiche wie :func:`Get PM Count`.
"""
}]
})
