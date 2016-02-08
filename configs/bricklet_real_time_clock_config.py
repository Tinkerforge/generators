# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Real-Time Clock Bricklet communication config

com = {
    'author': 'Matthias Bolte <matthias@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 268,
    'name': ('Real Time Clock', 'Real-Time Clock', 'Real-Time Clock Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Battery-backed real-time clock',
        'de': 'Batteriegepufferte Echtzeituhr'
    },
    'released': False,
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
* Weekday: 1 bis 7 (Montag bis Sontag)

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
                                                         ('Sunday', 7)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current date (including weekday) and the current time of the
real-time clock with hundredths of a second resolution.
""",
'de':
"""
Gibt das aktuelle Datum (inklusive Wochentag) und die aktuelle Zeit der
Echtzeituhr mit Hundertstelsekunden Auflösung zurück.
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
Returns the offset as set by :func:`SetOffset`.
""",
'de':
"""
Gibt den Versatz zurück, wie von :func:`SetOffset` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Date Time', 'date and time'), [(('Year', 'Year'), 'uint16', None, None, None, None), (('Month', 'Month'), 'uint8', None, None, None, None), (('Day', 'Day'), 'uint8', None, None, None, None), (('Hour', 'Hour'), 'uint8', None, None, None, None), (('Minute', 'Minute'), 'uint8', None, None, None, None), (('Second', 'Second'), 'uint8', None, None, None, None), (('Centisecond', 'Centisecond'), 'uint8', None, None, None, None), (('Weekday', 'Weekday'), 'uint8', None, None, None, None)], []),
              ('getter', ('Get Timestamp', 'timestamp'), [(('Timestamp', 'Timestamp'), 'int64', None, 'ms', 'ms', None)], [])]
})
