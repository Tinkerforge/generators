# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# GPS Bricklet 3.0 communication config

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2171,
    'name': 'GPS V3',
    'display_name': 'GPS 3.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Determine position, velocity and altitude using GPS',
        'de': 'Bestimmt Position, Geschwindigkeit und Höhe mittels GPS'
    },
    'released': True,
    'documented': True,
    'discontinued': False,
    'features': [
        'device',
        'comcu_bricklet',
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append({
'name': 'Restart Type',
'type': 'uint8',
'constants': [('Hot Start', 0),
              ('Warm Start', 1),
              ('Cold Start', 2),
              ('Factory Reset', 3)]
})

com['constant_groups'].append({
'name': 'Satellite System',
'type': 'uint8',
'constants': [('GPS', 0),
              ('GLONASS', 1),
              ('Galileo', 2)]
})

com['constant_groups'].append({
'name': 'Fix',
'type': 'uint8',
'constants': [('No Fix', 1),
              ('2D Fix', 2),
              ('3D Fix', 3)]
})

com['constant_groups'].append({
'name': 'Fix LED Config',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Show Heartbeat', 2),
              ('Show Fix', 3),
              ('Show PPS', 4)]
})

com['constant_groups'].append({
'name': 'SBAS',
'type': 'uint8',
'constants': [('Enabled', 0),
              ('Disabled', 1)]
})

com['packets'].append({
'type': 'function',
'name': 'Get Coordinates',
'elements': [('Latitude', 'uint32', 1, 'out', {'scale': (1, 10**6), 'unit': 'Degree', 'range': (0, 90*10**6)}),
             ('NS', 'char', 1, 'out', {'range': [('N', 'N'), ('S', 'S')]}),
             ('Longitude', 'uint32', 1, 'out', {'scale': (1, 10**6), 'unit': 'Degree', 'range': (0, 180*10**6)}),
             ('EW', 'char', 1, 'out', {'range': [('E', 'E'), ('W', 'W')]})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the GPS coordinates. Latitude and longitude are given in the
``DD.dddddd°`` format, the value 57123468 means 57.123468°.
The parameter ``ns`` and ``ew`` are the cardinal directions for
latitude and longitude. Possible values for ``ns`` and ``ew`` are 'N', 'S', 'E'
and 'W' (north, south, east and west).

This data is only valid if there is currently a fix as indicated by
:func:`Get Status`.
""",
'de':
"""
Gibt die GPS Koordinaten zurück. Breitengrad und Längengrad werden im Format
``DD.dddddd°`` angegeben, der Wert 57123468 bedeutet 57,123468°.
Die Parameter ``ns`` und ``ew`` sind Himmelsrichtungen für
Breiten- und Längengrad. Mögliche Werte für ``ns`` und ``ew`` sind 'N', 'S', 'E'
und 'W' (Nord, Süd, Ost, West).

Diese Daten sind nur gültig wenn ein Fix vorhanden ist (siehe :func:`Get Status`).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Status',
'elements': [('Has Fix', 'bool', 1, 'out', {}),
             ('Satellites View', 'uint8', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns if a fix is currently available as well as the number of
satellites that are in view.

There is also a :ref:`green LED <gps_v2_bricklet_fix_led>` on the Bricklet that
indicates the fix status.
""",
'de':
"""
Gibt zurück ob ein GPS Fix besteht sowie die Anzahl der sichtbaren Satelliten.

Auf dem Bricklet ist eine :ref:`green LED <gps_v2_bricklet_fix_led>`, die den
Fix-Status anzeigt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Altitude',
'elements': [('Altitude', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Meter'}),
             ('Geoidal Separation', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Meter'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current altitude and corresponding geoidal separation.

This data is only valid if there is currently a fix as indicated by
:func:`Get Status`.
""",
'de':
"""
Gibt die aktuelle Höhe und die dazu gehörige Geoidal Separation zurück.

Diese Daten sind nur gültig wenn ein Fix vorhanden ist (siehe :func:`Get Status`).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Motion',
'elements': [('Course', 'uint32', 1, 'out', {'scale': (1, 100), 'unit': 'Degree', 'range': (0, 36000)}),
             ('Speed', 'uint32', 1, 'out', {'scale': (1, 100), 'unit': 'Kilometer Per Hour'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current course and speed. A course of 0° means the Bricklet is
traveling north bound and 90° means it is traveling east bound.

Please note that this only returns useful values if an actual movement
is present.

This data is only valid if there is currently a fix as indicated by
:func:`Get Status`.
""",
'de':
"""
Gibt die aktuelle Richtung und Geschwindigkeit zurück. Eine
Richtung von 0° bedeutet eine Bewegung des Bricklets nach Norden und 90°
einer Bewegung nach Osten.

Dabei ist zu beachten: Diese Funktion liefert nur nützlich Werte wenn
auch tatsächlich eine Bewegung stattfindet.

Diese Daten sind nur gültig wenn ein Fix vorhanden ist (siehe :func:`Get Status`).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Date Time',
'elements': [('Date', 'uint32', 1, 'out', {'range': (10100, 311299)}),
             ('Time', 'uint32', 1, 'out', {'range': (0, 235959999)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current date and time. The date is
given in the format ``ddmmyy`` and the time is given
in the format ``hhmmss.sss``. For example, 140713 means
14.07.13 as date and 195923568 means 19:59:23.568 as time.
""",
'de':
"""
Gibt das aktuelle Datum und die aktuelle Zeit zurück. Das Datum ist
im Format ``ddmmyy`` und die Zeit im Format ``hhmmss.sss`` angegeben. Zum
Beispiel, 140713 bedeutet 14.07.13 als Datum und 195923568 bedeutet
19:59:23.568 als Zeit.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Restart',
'elements': [('Restart Type', 'uint8', 1, 'in', {'constant_group': 'Restart Type'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Restarts the GPS Bricklet, the following restart types are available:

.. csv-table::
 :header: "Value", "Description"
 :widths: 10, 100

 "0", "Hot start (use all available data in the NV store)"
 "1", "Warm start (don't use ephemeris at restart)"
 "2", "Cold start (don't use time, position, almanacs and ephemeris at restart)"
 "3", "Factory reset (clear all system/user configurations at restart)"
""",
'de':
"""
Startet das GPS Bricklet neu. Die folgenden Neustart-Typen stehen zur
Verfügung:

.. csv-table::
 :header: "Wert", "Beschreibung"
 :widths: 10, 100

 "0", "Hot Start (alle verfügbaren Daten im NV-Speicher werden weiter genutzt)"
 "1", "Warm Start (Ephemerisdaten werden verworfen)"
 "2", "Cold Start (Zeit-, Position-, Almanach- und Ephemerisdaten werden verworfen)"
 "3", "Factory Reset (Alle System/User Einstellungen werden verworfen)"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Satellite System Status Low Level',
'elements': [('Satellite System', 'uint8', 1, 'in', {'constant_group': 'Satellite System'}),
             ('Satellite Numbers Length', 'uint8', 1, 'out', {'range': (0, 12)}),
             ('Satellite Numbers Data', 'uint8', 12, 'out', {}),
             ('Fix', 'uint8', 1, 'out', {'constant_group': 'Fix'}),
             ('PDOP', 'uint16', 1, 'out', {'scale': (1, 100)}),
             ('HDOP', 'uint16', 1, 'out', {'scale': (1, 100)}),
             ('VDOP', 'uint16', 1, 'out', {'scale': (1, 100)})],
'high_level': {'stream_out': {'name': 'Satellite Numbers', 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the

* satellite numbers list (up to 12 items)
* fix value,
* PDOP value,
* HDOP value and
* VDOP value

for a given satellite system. Currently GPS, GLONASS and Galileo are supported.

The GPS and GLONASS satellites have unique numbers and the satellite list gives
the numbers of the satellites that are currently utilized. The number 0 is not
a valid satellite number and can be ignored in the list.
""",
'de':
"""
Gibt die

* Liste der Satellitennummern (bis zu 12 Elemente),
* Fix-Wert,
* PDOP-Wert,
* HDOP-Wert and
* VDOP-Wert zurück.

für ein gegebenes Satellitensystem zurück. Aktuell werden GPS, GLONASS und Galileo
unterstützt.

Die Satelliten haben eindeutige Nummern and die Satellitenliste
gibt die Nummer der Satelliten die aktuell benutzt werden. Die Nummer 0 ist
keine gültige Satellitennummer und kann ignoriert werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Satellite Status',
'elements': [('Satellite System', 'uint8', 1, 'in', {'constant_group': 'Satellite System'}),
             ('Satellite Number', 'uint8', 1, 'in', {'range': (1, 32)}),
             ('Elevation', 'int16', 1, 'out', {'unit': 'Degree', 'range': (0, 90)}),
             ('Azimuth', 'int16', 1, 'out', {'unit': 'Degree', 'range': (0, 359)}),
             ('SNR', 'int16', 1, 'out', {'unit': 'Decibel', 'range': (0, 99)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current elevation, azimuth and SNR for a given satellite and satellite system.

The available satellite numbers are:

* GPS: 1-32
* GLONASS: 65-96
* Galileo: 301-332

""",
'de':
"""
Gibt die aktuellen Werte von Elevation, Azimutwinkel und SNR
für einen gegebenen Satelliten und ein gegebenes Satellitensystem zurück.

Die Satellitennummern teilen sich wie folgt auf:

* GPS: 1-32
* GLONASS: 65-96
* Galileo: 301-332

"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Fix LED Config',
'elements': [('Config', 'uint8', 1, 'in', {'constant_group': 'Fix LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the fix LED configuration. By default the LED shows if
the Bricklet got a GPS fix yet. If a fix is established the LED turns on.
If there is no fix then the LED is turned off.

You can also turn the LED permanently on/off, show a heartbeat or let it blink
in sync with the PPS (pulse per second) output of the GPS module.

If the Bricklet is in bootloader mode, the LED is off.
""",
'de':
"""
Setzt die Konfiguration der Fix-LED. Standardmäßig zeigt
die LED an ob ein GPS-Fix besteht. Wenn ein Fix da ist, geht die LED an. Wenn
kein Fix da ist, geht die LED aus.

Die LED kann auch permanent an/aus gestellt werden, einen Herzschlag anzeigen
oder im Rhythmus des PPS (Puls pro Sekunde) Ausgangs des GPS Moduls blinken.

Wenn das Bricklet sich im Bootloadermodus befindet ist die LED aus.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Fix LED Config',
'elements': [('Config', 'uint8', 1, 'out', {'constant_group': 'Fix LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Fix LED Config`
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Fix LED Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Coordinates Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Coordinates` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Coordinates` callback is only triggered if the coordinates changed
since the last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Coordinates` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Coordinates` Callback wird nur ausgelöst, wenn sich die Koordinaten seit der
letzten Auslösung geändert haben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Coordinates Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Coordinates Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Coordinates Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Status Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Status` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Status` callback is only triggered if the status changed since the
last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Status` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Status` Callback wird nur ausgelöst, wenn sich der Status seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Status Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Status Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Status Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Altitude Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Altitude` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Altitude` callback is only triggered if the altitude changed since the
last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Altitude` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Altitude` Callback wird nur ausgelöst, wenn sich die Höhe seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Altitude Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Altitude Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Altitude Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Motion Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Motion` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Motion` callback is only triggered if the motion changed since the
last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Motion` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Motion` Callback wird nur ausgelöst, wenn sich die Bewegung seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Motion Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Motion Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Motion Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Date Time Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Date Time` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Date Time` callback is only triggered if the date or time changed
since the last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Date Time` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Date Time` Callback wird nur ausgelöst, wenn sich das Datum oder die
Zeit seit der letzten Auslösung geändert haben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Date Time Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Date Time Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Date Time Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Pulse Per Second',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered precisely once per second,
see `PPS <https://en.wikipedia.org/wiki/Pulse-per-second_signal>`__.

The precision of two subsequent pulses will be skewed because
of the latency in the USB/RS485/Ethernet connection. But in the
long run this will be very precise. For example a count of
3600 pulses will take exactly 1 hour.
""",
'de':
"""
Dieser Callback wird  präzise einmal pro sekunde ausgeführt,
siehe `PPS <https://de.wikipedia.org/wiki/Puls_pro_Sekunde>`__.

Die Präzision von zwei direkt aufeinander folgenden Pulsen
kann auf Grund von Latenzen in der USB/RS485/Ethernet-Verbindung
verzerrt sein. Langfristig ist dies allerdings weiterhin sehr
präzise. Zum Beispiel wird eine Zählung von 3600 Pulsen exakt
eine Stund dauern.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Coordinates',
'elements': [('Latitude', 'uint32', 1, 'out', {'scale': (1, 10**6), 'unit': 'Degree', 'range': (0, 90*10**6)}),
             ('NS', 'char', 1, 'out', {'range': [('N', 'N'), ('S', 'S')]}),
             ('Longitude', 'uint32', 1, 'out', {'scale': (1, 10**6), 'unit': 'Degree', 'range': (0, 180*10**6)}),
             ('EW', 'char', 1, 'out', {'range': [('E', 'E'), ('W', 'W')]})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Coordinates Callback Period`. The parameters are the same
as for :func:`Get Coordinates`.

The :cb:`Coordinates` callback is only triggered if the coordinates changed
since the last triggering and if there is currently a fix as indicated by
:func:`Get Status`.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Coordinates Callback Period`, ausgelöst. Die Parameter sind die
gleichen wie die von :func:`Get Coordinates`.

Der :cb:`Coordinates` Callback wird nur ausgelöst, wenn sich die
Koordinaten seit der letzten Auslösung geändert haben und ein Fix vorhanden
ist (siehe :func:`Get Status`).
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Status',
'elements': [('Has Fix', 'bool', 1, 'out', {}),
             ('Satellites View', 'uint8', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Status Callback Period`. The parameters are the same
as for :func:`Get Status`.

The :cb:`Status` callback is only triggered if the status changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Status Callback Period`, ausgelöst. Die Parameter sind die
gleichen wie die von :func:`Get Status`.

Der :cb:`Status` Callback wird nur ausgelöst, wenn sich der
Status seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Altitude',
'elements': [('Altitude', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Meter'}),
             ('Geoidal Separation', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Meter'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Altitude Callback Period`. The parameters are the same
as for :func:`Get Altitude`.

The :cb:`Altitude` callback is only triggered if the altitude changed since the
last triggering and if there is currently a fix as indicated by
:func:`Get Status`.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Altitude Callback Period`, ausgelöst. Die Parameter sind die
gleichen wie die von :func:`Get Altitude`.

Der :cb:`Altitude` Callback wird nur ausgelöst, wenn sich die
Höhe seit der letzten Auslösung geändert hat und ein Fix vorhanden
ist (siehe :func:`Get Status`).
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Motion',
'elements': [('Course', 'uint32', 1, 'out', {'scale': (1, 100), 'unit': 'Degree', 'range': (0, 36000)}),
             ('Speed', 'uint32', 1, 'out', {'scale': (1, 100), 'unit': 'Kilometer Per Hour'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Motion Callback Period`. The parameters are the same
as for :func:`Get Motion`.

The :cb:`Motion` callback is only triggered if the motion changed since the
last triggering and if there is currently a fix as indicated by
:func:`Get Status`.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Motion Callback Period`, ausgelöst. Die Parameter sind die
gleichen wie die von :func:`Get Motion`.

Der :cb:`Motion` Callback wird nur ausgelöst, wenn sich die
Bewegung seit der letzten Auslösung geändert hat und ein Fix vorhanden
ist (siehe :func:`Get Status`).
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Date Time',
'elements': [('Date', 'uint32', 1, 'out', {'range': (10100, 311299)}),
             ('Time', 'uint32', 1, 'out', {'range': (0, 235959999)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Date Time Callback Period`. The parameters are the same
as for :func:`Get Date Time`.

The :cb:`Date Time` callback is only triggered if the date or time changed
since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Date Time Callback Period`, ausgelöst. Die Parameter sind die
gleichen wie die von :func:`Get Date Time`.

Der :cb:`Date Time` Callback wird nur ausgelöst, wenn sich das Datum oder die
Zeit seit der letzten Auslösung geändert haben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set SBAS Config',
'elements': [('SBAS Config', 'uint8', 1, 'in', {'constant_group': 'SBAS', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
If `SBAS <https://en.wikipedia.org/wiki/GNSS_augmentation#Satellite-based_augmentation_system>`__ is enabled,
the position accuracy increases (if SBAS satellites are in view),
but the update rate is limited to 5Hz. With SBAS disabled the update rate is increased to 10Hz.
""",
'de':
"""
Wenn `SBAS <https://de.wikipedia.org/wiki/Satellite_Based_Augmentation_System>`__ aktiviert ist,
erhöht sich die Positionsgenauigkeit der GPS Daten falls SBAS Satelliten zu sehen sind.
Die Aktualisierungsrate der GPS Daten beträgt 5Hz falls SBAS aktiviert ist und 10Hz falls SBAS deaktiviert ist.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get SBAS Config',
'elements': [('SBAS Config', 'uint8', 1, 'out', {'constant_group': 'SBAS', 'default': 0})],

'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the SBAS configuration as set by :func:`Set SBAS Config`
""",
'de':
"""
Gibt die SBAS-Konfiguration zurück, wie von :func:`Set SBAS Config` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Coordinates', 'coordinates'), [(('Latitude', 'Latitude'), 'uint32', 1, 1000000.0, '°', None), (('NS', 'N/S'), 'char', 1, None, None, None), (('Longitude', 'Longitude'), 'uint32', 1, 1000000.0, '°', None), (('EW', 'E/W'), 'char', 1, None, None, None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Coordinates', 'coordinates'), [(('Latitude', 'Latitude'), 'uint32', 1, 1000000.0, '°', None), (('NS', 'N/S'), 'char', 1, None, None, None), (('Longitude', 'Longitude'), 'uint32', 1, 1000000.0, '°', None), (('EW', 'E/W'), 'char', 1, None, None, None)], None, None),
              ('callback_period', ('Coordinates', 'coordinates'), [], 1000)]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports() + oh_generic_trigger_channel_imports() +
                ['org.eclipse.smarthome.core.library.types.StringType',
                 'org.eclipse.smarthome.core.library.types.PointType',
                 'org.eclipse.smarthome.core.library.types.DateTimeType',
                 'org.eclipse.smarthome.core.library.types.OpenClosedType',
                 'java.time.ZoneId'],
    'param_groups': oh_generic_channel_param_groups(),
    'params': [{
            'packet': 'Set Fix LED Config',
            'element': 'Config',

            'name': 'Fix LED Config',
            'type': 'integer',
            'label': {'en': 'Fix LED', 'de': 'Fix-LED'},
            'description': {'en': 'The fix LED configuration. By default the LED shows if the Bricklet got a GPS fix yet. If a fix is established the LED turns on. If there is no fix then the LED is turned off.\n\nYou can also turn the LED permanently on/off, show a heartbeat or let it blink in sync with the PPS (pulse per second) output of the GPS module.\n\nIf the Bricklet is in bootloader mode, the LED is off.',
                            'de': 'Die Konfiguration der Fix-LED. Standardmäßig zeigt die LED an ob ein GPS-Fix besteht. Wenn ein Fix da ist, geht die LED an. Wenn kein Fix da ist, geht die LED aus.\n\nDie LED kann auch permanent an/aus gestellt werden, einen Herzschlag anzeigen oder im Rhythmus des PPS (Puls pro Sekunde) Ausgangs des GPS Moduls blinken.\n\nWenn das Bricklet sich im Bootloadermodus befindet ist die LED aus.'}
        }, {
            'packet': 'Set SBAS Config',
            'element': 'SBAS Config',

            'name': 'Enable SBAS',
            'type': 'boolean',
            'default': 'true',
            'label': {'en': 'SBAS', 'de': 'SBAS'},
            'description': {'en': 'If SBAS is enabled, the position accuracy increases (if SBAS satellites are in view), but the update rate is limited to 5Hz. With SBAS disabled the update rate is increased to 10Hz.',
                            'de': 'Wenn SBAS aktiviert ist, erhöht sich die Positionsgenauigkeit der GPS Daten falls SBAS Satelliten zu sehen sind. Die Aktualisierungsrate der GPS Daten beträgt 5Hz falls SBAS aktiviert ist und 10Hz falls SBAS deaktiviert ist.'},
        },
        update_interval('Set Status Callback Period', 'Period', 'Status', 'the status'),
        update_interval('Set Altitude Callback Period', 'Period', 'Altitude', 'the altitude and geodial separation'),
        update_interval('Set Motion Callback Period', 'Period', 'Motion', 'the course and speed')],
    'init_code': """this.setFixLEDConfig(cfg.fixLEDConfig);
        this.setSBASConfig(cfg.enableSBAS ? 0 : 1);
        this.setStatusCallbackPeriod(cfg.statusUpdateInterval);
        this.setAltitudeCallbackPeriod(cfg.altitudeUpdateInterval);
        this.setMotionCallbackPeriod(cfg.motionUpdateInterval);""",
    'dispose_code': """this.setStatusCallbackPeriod(0);
        this.setAltitudeCallbackPeriod(0);
        this.setMotionCallbackPeriod(0);""",
    'channels': [
        {
            'id': 'Location',
            'type': 'Coordinates',
            'callbacks': [{
                'packet': 'Coordinates',
                'transform': "new PointType(new DecimalType(latitude / 1000000.0 * (ns == 'N' ? 1 : -1)), new DecimalType(longitude / 1000000.0 * (ew == 'E' ? 1 : -1)))"}],
            'init_code': 'this.setCoordinatesCallbackPeriod(channelCfg.updateInterval);',
            'dispose_code': 'this.setCoordinatesCallbackPeriod(0);'
        }, {
            'id': 'Fix',
            'type': 'Fix',

            'getters': [{
                'packet': 'Get Status',
                'element': 'Has Fix',
                'packet_params': [],
                'transform': "value.hasFix ? OpenClosedType.CLOSED : OpenClosedType.OPEN"}],

            'callbacks': [{
                'packet': 'Status',
                'element': 'Has Fix',
                'transform': "hasFix ? OpenClosedType.CLOSED : OpenClosedType.OPEN"}],

        }, {
            'id': 'Satellites In View',
            'type': 'Satellites In View',

            'getters': [{
                'packet': 'Get Status',
                'element': 'Satellites View',
                'packet_params': [],
                'transform': "new DecimalType(value.satellitesView)"}],

            'callbacks': [{
                'packet': 'Status',
                'element': 'Satellites View',
                'transform': "new DecimalType(satellitesView)"}],

        },  {
            'id': 'Altitude',
            'type': 'Altitude',

            'getters': [{
                'packet': 'Get Altitude',
                'element': '{title_words}',
                'packet_params': [],
                'transform': "new {number_type}(value.altitude{divisor}{unit})"}],

            'callbacks': [{
                'packet': 'Altitude',
                'element': '{title_words}',
                'transform': "new {number_type}(altitude{divisor}{unit})"}],

        },  {
            'id': 'Geoidal Separation',
            'type': 'Geoidal Separation',

            'getters': [{
                'packet': 'Get Altitude',
                'element': '{title_words}',
                'packet_params': [],
                'transform': "new {number_type}(value.geoidalSeparation{divisor}{unit})"}],

            'callbacks': [{
                'packet': 'Altitude',
                'element': '{title_words}',
                'transform': "new {number_type}(geoidalSeparation{divisor}{unit})"}],

        },  {
            'id': 'Course',
            'type': 'Course',

            'getters': [{
                'packet': 'Get Motion',
                'element': '{title_words}',
                'packet_params': [],
                'transform': "new {number_type}(value.course{divisor}{unit})"}],

            'callbacks': [{
                'packet': 'Motion',
                'element': '{title_words}',
                'transform': "new {number_type}(course{divisor}{unit})"}],

        },  {
            'id': 'Speed',
            'type': 'Speed',

            'getters': [{
                'packet': 'Get Motion',
                'element': '{title_words}',
                'packet_params': [],
                'transform': "new {number_type}(value.speed{divisor}{unit})"}],

            'callbacks': [{
                'packet': 'Motion',
                'element': '{title_words}',
                'transform': "new {number_type}(speed{divisor}{unit})"}],

        },  {
            'id': 'Date Time',
            'type': 'Date Time',

            'getters': [{
                'packet': 'Get Date Time',
                'packet_params': [],
                'transform': 'new DateTimeType(Helper.parseGPSDateTime(value.date, value.time).withZoneSameInstant(ZoneId.systemDefault()))'}],

            'callbacks': [{
                'packet': 'Date Time',
                'transform': "new DateTimeType(Helper.parseGPSDateTime(date, time).withZoneSameInstant(ZoneId.systemDefault()))"}],

            'init_code': 'this.setDateTimeCallbackPeriod(channelCfg.updateInterval);',
            'dispose_code': 'this.setDateTimeCallbackPeriod(0);'
        }, {
            'id': 'Pulse Per Second',
            'type': 'system.trigger',

            'label': 'Pulse Per Second',
            'description': 'This channel is triggered precisely once per second, see `PPS <https://en.wikipedia.org/wiki/Pulse-per-second_signal>`__.\n\nThe precision of two subsequent pulses will be skewed because of the latency in the USB/RS485/Ethernet connection. But in the long run this will be very precise. For example a count of 3600 pulses will take exactly 1 hour.',

            'callbacks': [{
                'packet': 'Pulse Per Second',
                'transform': '""'}],
        }, {
            'id': 'Restart',
            'type': 'Restart',

            'setters': [{
                'packet': 'Restart',
                'packet_params': ['Integer.valueOf(cmd.toString())'],
                'command_type': "StringType"
            }],

        }
    ],
    'channel_types': [
       oh_generic_channel_type('Coordinates', 'Location', {'en': 'Location', 'de': 'Standort'},
                    update_style='Callback Period',
                    description={'en': 'The location as determined by the bricklet.',
                                 'de': 'Der vom Bricklet ermittelte Standort'}),
        oh_generic_channel_type('Fix', 'Contact', {'en': 'Fix', 'de': 'Fix'},
                    update_style=None,
                    description={'en': 'The current fix status',
                                 'de': 'Der aktuelle Fix-Status'}),
        oh_generic_channel_type('Satellites In View', 'Number', {'en': 'Satellites In View', 'de': 'Sichtbare Satelliten'},
                    update_style=None,
                    description={'en': 'The number of satellites that are in view.',
                                 'de': 'Die Anzahl der derzeit sichtbaren Satelliten.'}),
        oh_generic_channel_type('Altitude', 'Number', {'en': 'Altitude', 'de': 'Höhe'},
                    update_style=None,
                    description={'en': 'The measured altitude', 'de': 'Die gemessene Höhe'}),
        oh_generic_channel_type('Geoidal Separation', 'Number', {'en': 'Geoidal Separation', 'de': 'Geoidal Separation'},
                    update_style=None,
                    description={'en': 'The geoidal separation corresponding to the current altitude',
                                 'de': "Die 'Geoidal Separation' zur aktuellen Höhe."}),
        oh_generic_channel_type('Course', 'Number', {'en': 'Course', 'de': 'Kurs'},
                    update_style=None,
                    description={'en': 'The current course. A course of 0° means the Bricklet is traveling north bound and 90° means it is traveling east bound. Please note that this only returns useful values if an actual movement is present.',
                                 'de': 'Eine Richtung von 0° bedeutet eine Bewegung des Bricklets nach Norden und 90° einer Bewegung nach Osten. Dabei ist zu beachten: Diese Funktion liefert nur nützlich Werte wenn auch tatsächlich eine Bewegung stattfindet.'}),
        oh_generic_channel_type('Speed', 'Number', {'en': 'Speed', 'de': 'Geschwindigkeit'},
                    update_style=None,
                    description={'en': 'The current speed. Please note that this only returns useful values if an actual movement is present.',
                                 'de': 'Die aktuelle Geschwindigkeit. Dabei ist zu beachten: Diese Funktion liefert nur nützlich Werte wenn auch tatsächlich eine Bewegung stattfindet.'}),
        oh_generic_channel_type('Date Time', 'DateTime', {'en': 'Date Time', 'de': 'Datum und Uhrzeit'},
                    update_style='Callback Period',
                    description={'en': 'The current date and time.',
                                 'de': 'Das aktuelle Datum und die aktuelle Uhrzeit'}),
        oh_generic_channel_type('Restart', 'String', {'en': 'Restart', 'de': 'Neustart'},
                    update_style=None,
                    description={'en': "Restarts the GPS Bricklet, the following restart types are available:<ul><li>Hot start (use all available data in the NV store)</li><li>Warm start (don't use ephemeris at restart)</li><li>Cold start (don't use time, position, almanacs and ephemeris at restart)</li><li>Factory reset (clear all system/user configurations at restart)</li></ul>",
                                 'de': "Startet das GPS Bricklet neu. Die folgenden Neustart-Typen stehen zur Verfügung:<ul><li>Hot Start (alle verfügbaren Daten im NV-Speicher werden weiter genutzt)</li><li>Warm Start (Ephemerisdaten werden verworfen)</li><li>Cold Start (Zeit-, Position-, Almanach- und Ephemerisdaten werden verworfen)</li><li>Factory Reset (Alle System/User Einstellungen werden verworfen)</li></ul>"},
                    command_options=[('Hot Start', '0'),
                                     ('Warm Start', '1'),
                                     ('Cold Start', '2'),
                                     ('Factory reset', '3')])
    ],
    'actions': ['Get Coordinates', 'Get Status', 'Get Altitude', 'Get Motion', 'Get Date Time', 'Get Satellite System Status', 'Get Satellite Status', 'Restart', 'Get Fix LED Config', 'Get SBAS Config']
}
