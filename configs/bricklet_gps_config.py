# -*- coding: utf-8 -*-

# GPS Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [1, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 222,
    'name': ('GPS', 'gps', 'GPS'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for receiving GPS position',
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetCoordinates', 'get_coordinates'),
'elements': [('latitude', 'uint32', 1, 'out'),
             ('ns', 'char', 1, 'out'),
             ('longitude', 'uint32', 1, 'out'),
             ('ew', 'char', 1, 'out'),
             ('pdop', 'uint16', 1, 'out'),
             ('hdop', 'uint16', 1, 'out'),
             ('vdop', 'uint16', 1, 'out'),
             ('epe', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the GPS coordinates. Latitude and longitude are given in the
DD.dddddd° format, the value 57123468 means 57.123468°.
The parameter ns and ew are the cardinal directions for
latitude and logitude. Possible values for ns and ew are 'N', 'S', 'E'
and 'W' (north, south, east and west).

PDOP, HDOP and VDOP are the dilution of precision (DOP) values. They specify
the additional multiplicative effect of GPS satellite geometry on GPS 
precision. See 
`here <http://en.wikipedia.org/wiki/Dilution_of_precision_(GPS)>`__
for more information. The values are give in hundreths.

EPE is the "Estimated Position Error". The EPE is given in cm. This is not the
absolute maximum error, it is the error with a specific confidence. See
`here <http://www.nps.gov/gis/gps/WhatisEPE.html>`__ for more information.

This data is only valid if there is currently a fix as indicated by
:func:`GetStatus`.
""",
'de':
"""
Gibt die GPS Koordinaten zurück. Breitengrad und Längengrad werden im Format
DD.dddddd° ausgegeben, der Wert 57123468 bedeutet 57,123468°.
Die Parameter ns und ew sind Himmelsrichtungen für
Breiten- und Längengrad. Mögliche Werte für ns und ew sind 'N', 'S', 'E'
und 'W' (Nord, Süd, Ost, West).

PDOP, HDOP und VDOP sind die "dilution of precision" (DOP) Werte. Sie
spezifizieren die zusätzlichen multiplikativen Effekte von der GPS
Satellitengeometrie auf die GPS-Präzision.
`hier <http://en.wikipedia.org/wiki/Dilution_of_precision_(GPS)>`__ gibt
es mehr Informationen dazu. Die Werte werden in Hunderstel gegeben.

EPE ist der "Estimated Position Error". Der EPE wird in cm gegeben.
Dies ist nicht der absolut maximale Fehler, es ist der Fehler mit einer
spezifischen Konfidenz. Siehe 
`hier <http://www.nps.gov/gis/gps/WhatisEPE.html>`__ für mehr Informationen.

Diese Daten sind nur gültig wenn ein Fix vorhanden ist (siehe :func:`GetStatus`).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetStatus', 'get_status'),
'elements': [('fix', 'uint8', 1, 'out'),
             ('satellites_view', 'uint8', 1, 'out'),
             ('satellites_used', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current fix status, the number of satellites that are in view and
the number of satellites that are currently used.

Possible fix status values can be:

.. csv-table::
 :header: "Value", "Description"
 :widths: 10, 100

 "1", "No Fix"
 "2", "2D Fix"
 "3", "3D Fix"
""",
'de':
"""
Gibt den aktuellen Fix-Status, die Anzahl der sichtbaren Satelliten und die
Anzahl der im Moment benutzten Satelliten zurück.

Mögliche Fix-Status Werte sind:

.. csv-table::
 :header: "Wert", "Beschreibung"
 :widths: 10, 100

 "1", "Kein Fix"
 "2", "2D Fix"
 "3", "3D Fix"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAltitude', 'get_altitude'),
'elements': [('altitude', 'uint32', 1, 'out'),
             ('geoidal_separation', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current altitude and corresponding geoidal separation.

Both values are given in cm.

This data is only valid if there is currently a fix as indicated by
:func:`GetStatus`.
""",
'de':
"""
Gibt die aktuelle Höhe und die dazu gehörige "Geoidal Seperation"
zurück.

Beide Werte werden in cm angegeben.

Diese Daten sind nur gültig wenn ein Fix vorhanden ist (siehe :func:`GetStatus`).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetMotion', 'get_motion'),
'elements': [('course', 'uint32', 1, 'out'),
             ('speed', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current course and speed. Course is given in hundreths degree
and speed is given in hundreths km/h. A course of 0° means the Bricklet is
traveling north bound and 90° means it is traveling east bound.

Please note that this only returns useful values if an actual movement
is present.

This data is only valid if there is currently a fix as indicated by
:func:`GetStatus`.
""",
'de':
"""
Gibt die aktuelle Richtung und Geschwindigkeit zurück. Die Richtung wird
in hundestel Grad und die Geschwindigkeit in hunderstel km/h gegben. Eine
Richtung von 0° bedeutet eine Bewegung des Bricklets nach Norden und 90°
einer Bewegung nach Osten.

Dabei ist zu beachten: Diese Funktion liefert nur nützlich Werte wenn
auch tatsächlich eine Bewegung stattfindet.

Diese Daten sind nur gültig wenn ein Fix vorhanden ist (siehe :func:`GetStatus`).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetDateTime', 'get_date_time'),
'elements': [('date', 'uint32', 1, 'out'),
             ('time', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current date and time. The date is
given in the format ddmmyy and the time is given
in the format hhmmss.sss
""",
'de':
"""
Gibt das aktuelle Datum un die Aktuelle Zeit zurück. Das Datum ist
im Format ddmmyy und die Zeit im Format hhmmss.sss gegeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('Restart', 'restart'),
'elements': [('restart_type', 'uint8', 1, 'in')],
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
'name': ('SetCoordinatesCallbackPeriod', 'set_coordinates_callback_period'),
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Coordinates` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Coordinates` is only triggered if the coordinates changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Coordinates` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Coordinates` wird nur ausgelöst wenn sich die Koordinaten seit der
letzten Auslösung geändert haben.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetCoordinatesCallbackPeriod', 'get_coordinates_callback_period'),
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetCoordinatesCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetCoordinatesCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetStatusCallbackPeriod', 'set_status_callback_period'),
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Status` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Status` is only triggered if the status changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Status` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Status` wird nur ausgelöst wenn sich der Status seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetStatusCallbackPeriod', 'get_status_callback_period'),
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetStatusCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetStatusCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetAltitudeCallbackPeriod', 'set_altitude_callback_period'),
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Altitude` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Altitude` is only triggered if the altitude changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Altitude` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Altitude` wird nur ausgelöst wenn sich die Höhe seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAltitudeCallbackPeriod', 'get_altitude_callback_period'),
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetAltitudeCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetAltitudeCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetDateTimeCallbackPeriod', 'set_date_time_callback_period'),
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`DateTime` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`DateTime` is only triggered if the date or time changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`DateTime` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`DateTime` wird nur ausgelöst wenn sich das Datum oder die Zeit seit der
letzten Auslösung geändert haben.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetDateTimeCallbackPeriod', 'get_date_time_callback_period'),
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetDateTimeCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetDateTimeCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetMotionCallbackPeriod', 'set_motion_callback_period'),
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Motion` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Motion` is only triggered if the motion changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Motion` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Motion` wird nur ausgelöst wenn sich die Bewegung seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetMotionCallbackPeriod', 'get_motion_callback_period'),
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetMotionCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetMotionCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('Coordinates', 'coordinates'),
'elements': [('latitude', 'uint32', 1, 'out'),
             ('ns', 'char', 1, 'out'),
             ('longitude', 'uint32', 1, 'out'),
             ('ew', 'char', 1, 'out'),
             ('pdop', 'uint16', 1, 'out'),
             ('hdop', 'uint16', 1, 'out'),
             ('vdop', 'uint16', 1, 'out'),
             ('epe', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetCoordinatesCallbackPeriod`. The parameters are the same
as for :func:`GetCoordinates`.

:func:`Coordinates` is only triggered if the coordinates changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit 
:func:`SetCoordinatesCallbackPeriod`, ausgelöst. Die Parameter sind die 
gleichen wie die von :func:`GetCoordinates`.

:func:`SetCoordinatesCallbackPeriod` wird nur ausgelöst wenn sich die 
Koordinaten seit der letzten Auslösung geändert haben.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('Status', 'status'),
'elements': [('fix', 'uint8', 1, 'out'),
             ('satellites_view', 'uint8', 1, 'out'),
             ('satellites_used', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetStatusCallbackPeriod`. The parameters are the same
as for :func:`GetStatus`.

:func:`Status` is only triggered if the status changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit 
:func:`SetStatusCallbackPeriod`, ausgelöst. Die Parameter sind die 
gleichen wie die von :func:`GetStatus`.

:func:`Status` wird nur ausgelöst wenn sich der 
Status seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('Altitude', 'altitude'),
'elements': [('altitude', 'uint32', 1, 'out'),
             ('geoidal_separation', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetAltitudeCallbackPeriod`. The parameters are the same
as for :func:`GetAltitude`.

:func:`Altitude` is only triggered if the altitude changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit 
:func:`SetAltitudeCallbackPeriod`, ausgelöst. Die Parameter sind die 
gleichen wie die von :func:`GetAltitude`.

:func:`Altitude` wird nur ausgelöst wenn sich die 
Höhe seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('Motion', 'motion'),
'elements': [('course', 'uint32', 1, 'out'),
             ('speed', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetMotionCallbackPeriod`. The parameters are the same
as for :func:`GetMotion`.

:func:`Motion` is only triggered if the motion changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit 
:func:`SetMotionCallbackPeriod`, ausgelöst. Die Parameter sind die 
gleichen wie die von :func:`GetMotion`.

:func:`Motion` wird nur ausgelöst wenn sich die 
Bewegung seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('DateTime', 'date_time'),
'elements': [('date', 'uint32', 1, 'out'),
             ('time', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetDateTimeCallbackPeriod`. The parameters are the same
as for :func:`GetDateTime`.

:func:`DateTime` is only triggered if the date or time changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit 
:func:`SetDateTimeCallbackPeriod`, ausgelöst. Die Parameter sind die 
gleichen wie die von :func:`GetDateTime`.

:func:`DateTime` wird nur ausgelöst wenn sich das Datum oder die Zeit 
seit der letzten Auslösung geändert haben.
"""
}]
})
