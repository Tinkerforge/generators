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
        'en': 'Battery backed real-time clock',
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
Gitb das aktuelle Datum (inklusive Wochentag) und die aktuelle Zeit der
Echtzeituhr mit Hundertstelsekunden Auflösung zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Timestamp',
'elements': [('Milliseconds', 'int64', 1, 'out')],
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
Gitb das aktuelle Datum und Zeit der Echtzeituhr in Millisekunden umgerechnet
zurück. Der Zeitstempel hat eine effektive Auflösung von Hundertstelsekunden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Correction Offset',
'elements': [('Offset', 'int8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the correction offset for the real-time clock in 2.17 ppm steps between
-277.76 ppm (-128) and +275.59 ppm (127).

The real-time clock time can deviate from the actual time due to the frequency
deviation of its 32.768 kHz crystal. Without correction (factory default) the
time deviation should less than ±20 ppm (±1.728 seconds per day).

This deviation can be calculated by comparing the same duration measured by the
real-time clock (``rtc_duration``) an accurate reference clock
(``ref_duration``). For best results the offset should be set to 0 ppm first
and then a duration of at least 6 hours should be measured.

The new correction offset can be calculated as follow::

  offset = round(1000000 * (ref_duration - rtc_duration) / rtc_duration / 2.17)

If you want to apply an offset correction, then we recommend using the
calibration dialog in Brick Viewer, instead of doing it manually.
""",
'de':
"""
Setzt den Korrekturversatz für die Echtzeituhr in 2,17 ppm Schritten zwischen
-277,76 ppm (-128) und +275,59 ppm (127).

Die Echtzeituhr kann von der eigentlichen Zeit abweichen, bedingt durch die
Frequenzabweichung des verbauten 32,768 kHz Quarzes. Ohne Korrektur
(Werkseinstellung) sollte die Zeitabweichung weniger als ±20 ppm (±1,728
Sekunden pro Tag) betragen.

Diese Abweichung kann berechnet werden, durch Vergleich der gleichen Zeitdauer
einmal mit der Echtzeituhr (``rtc_duration``) gemessen und einmal mit einer
genauen Kontrolluhr (``ref_duration``) gemessen. Um das beste Ergebnis zu
erzielen, sollte der Korrekturversatz zuerst auf 0 ppm gesetzt und dann eine
Zeitdauer von mindestens 6 Stunden gemessen werden.

Der neue Korrekturversatz kann dann wie folgt berechnet werden::

  offset = round(1000000 * (ref_duration - rtc_duration) / rtc_duration / 2.17)

Wenn eine Korrekturversatz berechnet werden soll, dann empfehlen wir den
Kalibrierungsdialog in Brick Viewer dafür zu verwenden, anstatt die Berechnung
von Hand durchzuführen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Correction Offset',
'elements': [('Offset', 'int8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the correction offset as set by :func:`SetCorrectionOffset`.
""",
'de':
"""
Gibt den Korrekturversatz zurück, wie von :func:`SetCorrectionOffset` gesetzt.
"""
}]
})
