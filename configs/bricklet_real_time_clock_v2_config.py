# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Real-Time Clock Bricklet 2.0 communication config

com = {
    'author': 'Matthias Bolte <matthias@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2106,
    'name': 'Real Time Clock V2',
    'display_name': 'Real-Time Clock 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Battery-backed real-time clock',
        'de': 'Batteriegepufferte Echtzeituhr'
    },
    'released': True,
    'documented': True,
    'discontinued': False,
    'features': [
        'comcu_bricklet',
        'bricklet_get_identity'
    ],
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Set Date Time',
'elements': [('Year', 'uint16', 1, 'in'),
             ('Month', 'uint8', 1, 'in'),
             ('Day', 'uint8', 1, 'in'),
             ('Hour', 'uint8', 1, 'in'),
             ('Minute', 'uint8', 1, 'in'),
             ('Second', 'uint8', 1, 'in'),
             ('Centisecond', 'uint8', 1, 'in'),
             ('Weekday', 'uint8', 1, 'in', ('Weekday', [('Monday', 1),
                                                        ('Tuesday', 2),
                                                        ('Wednesday', 3),
                                                        ('Thursday', 4),
                                                        ('Friday', 5),
                                                        ('Saturday', 6),
                                                        ('Sunday', 7)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the current date (including weekday) and the current time with hundredths
of a second resolution.

Possible value ranges:

* Year: 2000 to 2099
* Month: 1 to 12 (January to December)
* Day: 1 to 31
* Hour: 0 to 23
* Minute: 0 to 59
* Second: 0 to 59
* Centisecond: 0 to 99
* Weekday: 1 to 7 (Monday to Sunday)

If the backup battery is installed then the real-time clock keeps date and
time even if the Bricklet is not powered by a Brick.

The real-time clock handles leap year and inserts the 29th of February
accordingly. But leap seconds, time zones and daylight saving time are not
handled.
""",
'de':
"""
Setzt das aktuelle Datum (inklusive Wochentag) und die aktuelle Zeit mit
Hundertstelsekunden Auflösung.

Mögliche Wertebereiche:

* Year: 2000 bis 2099
* Month: 1 bis 12 (Januar bis Dezember)
* Day: 1 bis 31
* Hour: 0 bis 23
* Minute: 0 bis 59
* Second: 0 bis 59
* Centisecond: 0 bis 99
* Weekday: 1 bis 7 (Montag bis Sonntag)

Wenn die Backup Batterie eingebaut ist, dann behält die Echtzeituhr Datum und
Zeit auch dann, wenn kein Brick das Bricklet mit Strom versorgt.

Die Echtzeituhr behandelt Schaltjahre und fügt den 29. Februar entsprechend ein.
Schaltsekunden, Zeitzonen und die Sommerzeit werden jedoch nicht behandelt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Date Time',
'elements': [('Year', 'uint16', 1, 'out'),
             ('Month', 'uint8', 1, 'out'),
             ('Day', 'uint8', 1, 'out'),
             ('Hour', 'uint8', 1, 'out'),
             ('Minute', 'uint8', 1, 'out'),
             ('Second', 'uint8', 1, 'out'),
             ('Centisecond', 'uint8', 1, 'out'),
             ('Weekday', 'uint8', 1, 'out', ('Weekday', [('Monday', 1),
                                                         ('Tuesday', 2),
                                                         ('Wednesday', 3),
                                                         ('Thursday', 4),
                                                         ('Friday', 5),
                                                         ('Saturday', 6),
                                                         ('Sunday', 7)])),
             ('Timestamp', 'int64', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current date (including weekday) and the current time of the
real-time clock with hundredths of a second resolution.

The timestamp represents the current date and the the current time of the
real-time clock converted to milliseconds.
""",
'de':
"""
Gibt das aktuelle Datum (inklusive Wochentag) und die aktuelle Zeit der
Echtzeituhr mit Hundertstelsekunden Auflösung zurück.

Der Zeitstempel stellt das aktuelle Datum und die aktuelle Zeit der Echtzeituhr
in Millisekunden umgerechnet dar.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Timestamp',
'elements': [('Timestamp', 'int64', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current date and the time of the real-time clock converted to
milliseconds. The timestamp has an effective resolution of hundredths of a
second.
""",
'de':
"""
Gibt das aktuelle Datum und Zeit der Echtzeituhr in Millisekunden umgerechnet
zurück. Der Zeitstempel hat eine effektive Auflösung von Hundertstelsekunden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Offset',
'elements': [('Offset', 'int8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the offset the real-time clock should compensate for in 2.17 ppm steps
between -277.76 ppm (-128) and +275.59 ppm (127).

The real-time clock time can deviate from the actual time due to the frequency
deviation of its 32.768 kHz crystal. Even without compensation (factory
default) the resulting time deviation should be at most ±20 ppm (±52.6
seconds per month).

This deviation can be calculated by comparing the same duration measured by the
real-time clock (``rtc_duration``) an accurate reference clock
(``ref_duration``).

For best results the configured offset should be set to 0 ppm first and then a
duration of at least 6 hours should be measured.

The new offset (``new_offset``) can be calculated from the currently configured
offset (``current_offset``) and the measured durations as follow::

  new_offset = current_offset - round(1000000 * (rtc_duration - ref_duration) / rtc_duration / 2.17)

If you want to calculate the offset, then we recommend using the calibration
dialog in Brick Viewer, instead of doing it manually.

The offset is saved in the EEPROM of the Bricklet and only needs to be
configured once.
""",
'de':
"""
Setzt den Versatz ein, den die Echtzeituhr ausgleichen soll.
Der Versatz kann in 2,17 ppm Schritten zwischen -277,76 ppm (-128) und
+275,59 ppm (127) eingestellt werden.

Die Echtzeituhr kann von der eigentlichen Zeit abweichen, bedingt durch die
Frequenzabweichung des verbauten 32,768 kHz Quarzes. Selbst ohne Ausgleich
(Werkseinstellung) sollte die daraus entstehende Zeitabweichung höchstens
±20 ppm (±52,6 Sekunden pro Monat) betragen.

Diese Abweichung kann berechnet werden, durch Vergleich der gleichen Zeitdauer
einmal mit der Echtzeituhr (``rtc_duration``) gemessen und einmal mit einer
genauen Kontrolluhr (``ref_duration``) gemessen.

Um das beste Ergebnis zu erzielen, sollte der eingestellte Versatz zuerst auf
0 ppm gesetzt und dann eine Zeitdauer von mindestens 6 Stunden gemessen werden.

Der neue Versatz (``new_offset``) kann dann wie folgt aus dem aktuell
eingestellten Versatz (``current_offset``) und den gemessenen
Zeitdauern berechnet werden::

  new_offset = current_offset - round(1000000 * (rtc_duration - ref_duration) / rtc_duration / 2.17)

Wenn der Versatz berechnet werden soll, dann empfehlen wir den
Kalibrierungsdialog in Brick Viewer dafür zu verwenden, anstatt die Berechnung
von Hand durchzuführen.

Der Versatz wird im EEPROM des Bricklets gespeichert und muss nur einmal
gesetzt werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Offset',
'elements': [('Offset', 'int8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the offset as set by :func:`Set Offset`.
""",
'de':
"""
Gibt den Versatz zurück, wie von :func:`Set Offset` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Date Time Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :cb:`Date Time` callback is triggered
periodically. A value of 0 turns the callback off.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :cb:`Date Time` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Date Time Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Date Time Callback Configuration`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Date Time Callback Configuration`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Alarm',
'elements': [('Month', 'int8', 1, 'in', ('Alarm Match', [('Disabled', -1)])),
             ('Day', 'int8', 1, 'in', ('Alarm Match', [('Disabled', -1)])),
             ('Hour', 'int8', 1, 'in', ('Alarm Match', [('Disabled', -1)])),
             ('Minute', 'int8', 1, 'in', ('Alarm Match', [('Disabled', -1)])),
             ('Second', 'int8', 1, 'in', ('Alarm Match', [('Disabled', -1)])),
             ('Weekday', 'int8', 1, 'in', ('Alarm Match', [('Disabled', -1)])),
             ('Interval', 'int32', 1, 'in', ('Alarm Interval', [('Disabled', -1)]))],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Configures a repeatable alarm. The :cb:`Alarm` callback is triggered if the
current date and time matches the configured alarm.

Setting a parameter to -1 means that it should be disabled and doesn't take part
in the match. Setting all parameters to -1 disables the alarm completely.

For example, to make the alarm trigger every day at 7:30 AM it can be
configured as (-1, -1, 7, 30, -1, -1, -1). The hour is set to match 7 and the
minute is set to match 30. The alarm is triggered if all enabled parameters
match.

The interval has a special role. It allows to make the alarm reconfigure itself.
This is useful if you need a repeated alarm that cannot be expressed by matching
the current date and time. For example, to make the alarm trigger every 23
seconds it can be configured as (-1, -1, -1, -1, -1, -1, 23). Internally the
Bricklet will take the current date and time, add 23 seconds to it and set the
result as its alarm. The first alarm will be triggered 23 seconds after the
call. Because the interval is not -1, the Bricklet will do the same again
internally, take the current date and time, add 23 seconds to it and set that
as its alarm. This results in a repeated alarm that triggers every 23 seconds.

The interval can also be used in combination with the other parameters. For
example, configuring the alarm as (-1, -1, 7, 30, -1, -1, 300) results in an
alarm that triggers every day at 7:30 AM and is then repeated every 5 minutes.
""",
'de':
"""
Konfiguriert einen wiederholbaren Alarm. Der :cb:`Alarm` Callback wird
ausgelöst, wenn das aktuelle Datum und die aktuelle Uhrzeit mit dem
konfigurierten Alarm übereinstimmen.

Wird ein Parameter auf -1 gesetzt, dann wird es deaktiviert und nimmt nicht
am Übereinstimmungstest teil. Werden alle Parameter auf -1 gesetzt, dann ist
der Alarm vollständig deaktiviert.

Um z.B. den Alarm jeden Tag um 7:30 Uhr auszulösen kann dieser auf (-1, -1, 7,
30, -1, -1, -1) konfiguriert werden. Die Stunde ist auf 7 gesetzt und die
Minute auf 30. Der Alarm wird ausgelöst, wenn alle aktiven Parameter mit dem
aktuellen Datum und der aktuellen Zeit übereinstimmen.

Das Intervall hat eine spezielle Rolle. Wenn es nicht auf -1 gesetzt ist, dann
konfiguriert sich der Alarm nach jeder Auslösung entsprechend selbst neu. Dies
kann für wiederholende Alarme genutzt werden, die nicht durch Übereinstimmung
mit Datum und Uhrzeit abgebildet werden können. Um z.B. alle 23 Sekunden einen
Alarm auszulösen kann dieser als (-1, -1, -1, -1, -1, -1, 23) konfiguriert
werden. Intern nimmt das Bricklet das aktuelle Datum und die aktuelle Uhrzeit,
addiert 23 Sekunden und setzt das Ergebnis als Alarm. Der erste Alarm wir dann
23 Sekunden nach dem Aufruf ausgelöst werden. Da das Intervall nicht -1 ist
wird das Bricklet dann intern wieder das gleiche tun: 23 Sekunden auf das
aktuelle Datum und die aktuelle Uhrzeit addieren und das Ergebnis als Alarm
setzten. Dadurch entsteht ein sich alle 23 Sekunden wiederholender Alarm.

Das Intervall kann auch in Kombination mit den anderen Parametern verwendet
werden. Wird z.B. der Alarm auf (-1, -1, 7, 30, -1, -1, 300) konfiguriert dann
wird der Alarm jeden Tag um 7:30 Uhr ausgelöst und dann all 5 Minuten
wiederholt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Alarm',
'elements': [('Month', 'int8', 1, 'out', ('Alarm Match', [('Disabled', -1)])),
             ('Day', 'int8', 1, 'out', ('Alarm Match', [('Disabled', -1)])),
             ('Hour', 'int8', 1, 'out', ('Alarm Match', [('Disabled', -1)])),
             ('Minute', 'int8', 1, 'out', ('Alarm Match', [('Disabled', -1)])),
             ('Second', 'int8', 1, 'out', ('Alarm Match', [('Disabled', -1)])),
             ('Weekday', 'int8', 1, 'out', ('Alarm Match', [('Disabled', -1)])),
             ('Interval', 'int32', 1, 'out', ('Alarm Interval', [('Disabled', -1)]))],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the alarm configuration as set by :func:`Set Alarm`.
""",
'de':
"""
Gibt die Alarmkonfiguration zurück, wie von :func:`Set Alarm` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Date Time',
'elements': [('Year', 'uint16', 1, 'out'),
             ('Month', 'uint8', 1, 'out'),
             ('Day', 'uint8', 1, 'out'),
             ('Hour', 'uint8', 1, 'out'),
             ('Minute', 'uint8', 1, 'out'),
             ('Second', 'uint8', 1, 'out'),
             ('Centisecond', 'uint8', 1, 'out'),
             ('Weekday', 'uint8', 1, 'out', ('Weekday', [('Monday', 1),
                                                         ('Tuesday', 2),
                                                         ('Wednesday', 3),
                                                         ('Thursday', 4),
                                                         ('Friday', 5),
                                                         ('Saturday', 6),
                                                         ('Sunday', 7)])),
             ('Timestamp', 'int64', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Date Time Callback Configuration`. The :word:`parameters` are the
same as for :func:`Get Date Time`.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Date Time Callback Configuration`, ausgelöst. Die :word:`parameters` sind
die gleichen wie die von :func:`Get Date Time`.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Alarm',
'elements': [('Year', 'uint16', 1, 'out'),
             ('Month', 'uint8', 1, 'out'),
             ('Day', 'uint8', 1, 'out'),
             ('Hour', 'uint8', 1, 'out'),
             ('Minute', 'uint8', 1, 'out'),
             ('Second', 'uint8', 1, 'out'),
             ('Centisecond', 'uint8', 1, 'out'),
             ('Weekday', 'uint8', 1, 'out', ('Weekday', [('Monday', 1),
                                                         ('Tuesday', 2),
                                                         ('Wednesday', 3),
                                                         ('Thursday', 4),
                                                         ('Friday', 5),
                                                         ('Saturday', 6),
                                                         ('Sunday', 7)])),
             ('Timestamp', 'int64', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered every time the current date and time matches the
configured alarm (see :func:`Set Alarm`). The :word:`parameters` are the same
as for :func:`Get Date Time`.
""",
'de':
"""
Dieser Callback wird jedes mal ausgelöst, wenn das aktuelle Datum und die
aktuelle Uhrzeit mit dem eingestellten Alarm übereinstimmen (siehe
:func:`Set Alarm`). Die :word:`parameters` sind die gleichen wie die von
:func:`Get Date Time`.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Date Time', 'date and time'), [(('Year', 'Year'), 'uint16', 1, None, None, None), (('Month', 'Month'), 'uint8', 1, None, None, None), (('Day', 'Day'), 'uint8', 1, None, None, None), (('Hour', 'Hour'), 'uint8', 1, None, None, None), (('Minute', 'Minute'), 'uint8', 1, None, None, None), (('Second', 'Second'), 'uint8', 1, None, None, None), (('Centisecond', 'Centisecond'), 'uint8', 1, None, None, None), (('Weekday', 'Weekday'), 'uint8:constant', 1, None, None, None), (('Timestamp', 'Timestamp'), 'int64', 1, None, 'ms', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Date Time', 'date and time'), [(('Year', 'Year'), 'uint16', 1, None, None, None), (('Month', 'Month'), 'uint8', 1, None, None, None), (('Day', 'Day'), 'uint8', 1, None, None, None), (('Hour', 'Hour'), 'uint8', 1, None, None, None), (('Minute', 'Minute'), 'uint8', 1, None, None, None), (('Second', 'Second'), 'uint8', 1, None, None, None), (('Centisecond', 'Centisecond'), 'uint8', 1, None, None, None), (('Weekday', 'Weekday'), 'uint8:constant', 1, None, None, None), (('Timestamp', 'Timestamp'), 'int64', 1, None, None, None)], None, None),
              ('callback_configuration', ('Date Time', 'date and time'), [], 5000, None, None, [])]
})
