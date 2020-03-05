# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Real-Time Clock Bricklet communication config

from openhab_commonconfig import *

com = {
    'author': 'Matthias Bolte <matthias@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'category': 'Bricklet',
    'device_identifier': 268,
    'name': 'Real Time Clock',
    'display_name': 'Real-Time Clock',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Battery-backed real-time clock',
        'de': 'Batteriegepufferte Echtzeituhr'
    },
    'released': True,
    'documented': True,
    'discontinued': False, # selling remaining stock, replaced by Real-Time Clock Bricklet 2.0
    'features': [
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append({
'name': 'Weekday',
'type': 'uint8',
'constants': [('Monday', 1),
              ('Tuesday', 2),
              ('Wednesday', 3),
              ('Thursday', 4),
              ('Friday', 5),
              ('Saturday', 6),
              ('Sunday', 7)]
})

com['constant_groups'].append({
'name': 'Alarm Match',
'type': 'int8',
'constants': [('Disabled', -1)]
})

com['constant_groups'].append({
'name': 'Alarm Interval',
'type': 'int32',
'constants': [('Disabled', -1)]
})

com['packets'].append({
'type': 'function',
'name': 'Set Date Time',
'elements': [('Year', 'uint16', 1, 'in', {'range': (2000, 2099)}),
             ('Month', 'uint8', 1, 'in', {'range': (1, 12)}),
             ('Day', 'uint8', 1, 'in', {'range': (1, 31)}),
             ('Hour', 'uint8', 1, 'in', {'range': (0, 23)}),
             ('Minute', 'uint8', 1, 'in', {'range': (0, 59)}),
             ('Second', 'uint8', 1, 'in', {'range': (0, 59)}),
             ('Centisecond', 'uint8', 1, 'in', {'range': (0, 99)}),
             ('Weekday', 'uint8', 1, 'in', {'constant_group': 'Weekday'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the current date (including weekday) and the current time.

If the backup battery is installed then the real-time clock keeps date and
time even if the Bricklet is not powered by a Brick.

The real-time clock handles leap year and inserts the 29th of February
accordingly. But leap seconds, time zones and daylight saving time are not
handled.
""",
'de':
"""
Setzt das aktuelle Datum (inklusive Wochentag).

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
'elements': [('Year', 'uint16', 1, 'out', {'range': (2000, 2099)}),
             ('Month', 'uint8', 1, 'out', {'range': (1, 12)}),
             ('Day', 'uint8', 1, 'out', {'range': (1, 31)}),
             ('Hour', 'uint8', 1, 'out', {'range': (0, 23)}),
             ('Minute', 'uint8', 1, 'out', {'range': (0, 59)}),
             ('Second', 'uint8', 1, 'out', {'range': (0, 59)}),
             ('Centisecond', 'uint8', 1, 'out', {'range': (0, 99)}),
             ('Weekday', 'uint8', 1, 'out', {'constant_group': 'Weekday'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current date (including weekday) and the current time of the
real-time clock.
""",
'de':
"""
Gibt das aktuelle Datum (inklusive Wochentag) und die aktuelle Zeit der
Echtzeituhr zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Timestamp',
'elements': [('Timestamp', 'int64', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current date and the time of the real-time clock.
The timestamp has an effective resolution of hundredths of a
second and is an offset to 2000-01-01 00:00:00.000.
""",
'de':
"""
Gibt das aktuelle Datum und Zeit der Echtzeituhr.
Der Zeitstempel hat eine effektive Auflösung von Hundertstelsekunden
und ist der Versatz zum 01.01.2000 00:00:00,000.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Offset',
'elements': [('Offset', 'int8', 1, 'in', {'scale': (217, 100), 'unit': 'Parts Per Million'})],
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
'elements': [('Offset', 'int8', 1, 'out', {'scale': (217, 100), 'unit': 'Parts Per Million'})],
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
'name': 'Set Date Time Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [2, 0, 1],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Date Time` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Date Time` Callback is only triggered if the date or time changed
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
'since_firmware': [2, 0, 1],
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
'type': 'function',
'name': 'Set Alarm',
'elements': [('Month', 'int8', 1, 'in', {'range': [(-1, -1), (1, 12)], 'constant_group': 'Alarm Match'}),
             ('Day', 'int8', 1, 'in', {'range': [(-1, -1), (1, 31)], 'constant_group': 'Alarm Match'}),
             ('Hour', 'int8', 1, 'in', {'range': [(-1, -1), (0, 23)], 'constant_group': 'Alarm Match'}),
             ('Minute', 'int8', 1, 'in', {'range': [(-1, -1), (0, 59)], 'constant_group': 'Alarm Match'}),
             ('Second', 'int8', 1, 'in', {'range': [(-1, -1), (0, 59)], 'constant_group': 'Alarm Match'}),
             ('Weekday', 'int8', 1, 'in', {'range': [(-1, -1), (1, 7)], 'constant_group': 'Alarm Match'}),
             ('Interval', 'int32', 1, 'in', {'range': [(-1, -1), (1, None)], 'unit': 'Second', 'constant_group': 'Alarm Interval'})],
'since_firmware': [2, 0, 1],
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
'elements': [('Month', 'int8', 1, 'out', {'range': [(-1, -1), (1, 12)], 'constant_group': 'Alarm Match'}),
             ('Day', 'int8', 1, 'out', {'range': [(-1, -1), (1, 31)], 'constant_group': 'Alarm Match'}),
             ('Hour', 'int8', 1, 'out', {'range': [(-1, -1), (0, 23)], 'constant_group': 'Alarm Match'}),
             ('Minute', 'int8', 1, 'out', {'range': [(-1, -1), (0, 59)], 'constant_group': 'Alarm Match'}),
             ('Second', 'int8', 1, 'out', {'range': [(-1, -1), (0, 59)], 'constant_group': 'Alarm Match'}),
             ('Weekday', 'int8', 1, 'out', {'range': [(-1, -1), (1, 7)], 'constant_group': 'Alarm Match'}),
             ('Interval', 'int32', 1, 'out', {'range': [(-1, -1), (1, None)], 'unit': 'Second', 'constant_group': 'Alarm Interval'})],
'since_firmware': [2, 0, 1],
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
'elements': [('Year', 'uint16', 1, 'out', {'range': (2000, 2099)}),
             ('Month', 'uint8', 1, 'out', {'range': (1, 12)}),
             ('Day', 'uint8', 1, 'out', {'range': (1, 31)}),
             ('Hour', 'uint8', 1, 'out', {'range': (0, 23)}),
             ('Minute', 'uint8', 1, 'out', {'range': (0, 59)}),
             ('Second', 'uint8', 1, 'out', {'range': (0, 59)}),
             ('Centisecond', 'uint8', 1, 'out', {'range': (0, 99)}),
             ('Weekday', 'uint8', 1, 'out', {'constant_group': 'Weekday'}),
             ('Timestamp', 'int64', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [2, 0, 1],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Date Time Callback Period`. The :word:`parameters` are the same
as for :func:`Get Date Time` and :func:`Get Timestamp` combined.

The :cb:`Date Time` callback is only triggered if the date or time changed
since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Date Time Callback Period`, ausgelöst. Die :word:`parameters` sind
die gleichen wie die von :func:`Get Date Time` und :func:`Get Timestamp`
kombiniert.

Der :cb:`Date Time` Callback wird nur ausgelöst, wenn sich das Datum oder die
Zeit seit der letzten Auslösung geändert haben.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Alarm',
'elements': [('Year', 'uint16', 1, 'out', {'range': (2000, 2099)}),
             ('Month', 'uint8', 1, 'out', {'range': (1, 12)}),
             ('Day', 'uint8', 1, 'out', {'range': (1, 31)}),
             ('Hour', 'uint8', 1, 'out', {'range': (0, 23)}),
             ('Minute', 'uint8', 1, 'out', {'range': (0, 59)}),
             ('Second', 'uint8', 1, 'out', {'range': (0, 59)}),
             ('Centisecond', 'uint8', 1, 'out', {'range': (0, 99)}),
             ('Weekday', 'uint8', 1, 'out', {'constant_group': 'Weekday'}),
             ('Timestamp', 'int64', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [2, 0, 1],
'doc': ['c', {
'en':
"""
This callback is triggered every time the current date and time matches the
configured alarm (see :func:`Set Alarm`). The :word:`parameters` are the same
as for :func:`Get Date Time` and :func:`Get Timestamp` combined.
""",
'de':
"""
Dieser Callback wird jedes mal ausgelöst, wenn das aktuelle Datum und die
aktuelle Uhrzeit mit dem eingestellten Alarm übereinstimmen (siehe
:func:`Set Alarm`). Die :word:`parameters` sind die gleichen wie die von
:func:`Get Date Time` und :func:`Get Timestamp` kombiniert.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Date Time', 'date and time'), [(('Year', 'Year'), 'uint16', 1, None, None, None), (('Month', 'Month'), 'uint8', 1, None, None, None), (('Day', 'Day'), 'uint8', 1, None, None, None), (('Hour', 'Hour'), 'uint8', 1, None, None, None), (('Minute', 'Minute'), 'uint8', 1, None, None, None), (('Second', 'Second'), 'uint8', 1, None, None, None), (('Centisecond', 'Centisecond'), 'uint8', 1, None, None, None), (('Weekday', 'Weekday'), 'uint8:constant', 1, None, None, None)], []),
              ('getter', ('Get Timestamp', 'timestamp'), [(('Timestamp', 'Timestamp'), 'int64', 1, None, 'ms', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Date Time', 'date and time'), [(('Year', 'Year'), 'uint16', 1, None, None, None), (('Month', 'Month'), 'uint8', 1, None, None, None), (('Day', 'Day'), 'uint8', 1, None, None, None), (('Hour', 'Hour'), 'uint8', 1, None, None, None), (('Minute', 'Minute'), 'uint8', 1, None, None, None), (('Second', 'Second'), 'uint8', 1, None, None, None), (('Centisecond', 'Centisecond'), 'uint8', 1, None, None, None), (('Weekday', 'Weekday'), 'uint8:constant', 1, None, None, None), (('Timestamp', 'Timestamp'), 'int64', 1, None, None, None)], None, None),
              ('callback_period', ('Date Time', 'date and time'), [], 5000)]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports() + oh_generic_trigger_channel_imports() + ['java.time.ZonedDateTime', 'java.time.ZoneId', 'org.eclipse.smarthome.core.library.types.DateTimeType'],
    'param_groups': oh_generic_channel_param_groups(),
    'params': [
        update_interval('Set Date Time Callback Period', 'Period', 'Date Time', 'the date time and timestamp'),
    ],
    'init_code':"""this.setDateTimeCallbackPeriod(cfg.dateTimeUpdateInterval);""",
    'dispose_code': """this.setDateTimeCallbackPeriod(0);""",
    'channels': [
        {
            'id': 'Date Time',
            'label': 'Date Time',
            'type': 'Date Time',
            'getters': [{
                'packet': 'Get Date Time',
                'transform': 'new DateTimeType(ZonedDateTime.of(value.year, value.month, value.day, value.hour, value.minute, value.second, value.centisecond * 10 * 1000 * 1000, ZoneId.of("UTC")).withZoneSameInstant(ZoneId.systemDefault()))'}],

            'setters': [{
                'packet': 'Set Date Time',
                'packet_params': ['cmd.getZonedDateTime().withZoneSameInstant(ZoneId.of("UTC")).getYear()',
                                        '(short)cmd.getZonedDateTime().withZoneSameInstant(ZoneId.of("UTC")).getMonth().getValue()',
                                        '(short)cmd.getZonedDateTime().withZoneSameInstant(ZoneId.of("UTC")).getDayOfMonth()',
                                        '(short)cmd.getZonedDateTime().withZoneSameInstant(ZoneId.of("UTC")).getHour()',
                                        '(short)cmd.getZonedDateTime().withZoneSameInstant(ZoneId.of("UTC")).getMinute()',
                                        '(short)cmd.getZonedDateTime().withZoneSameInstant(ZoneId.of("UTC")).getSecond()',
                                        '(short)(cmd.getZonedDateTime().withZoneSameInstant(ZoneId.of("UTC")).getNano() / 1000 / 1000 / 10)',
                                        '(short)cmd.getZonedDateTime().withZoneSameInstant(ZoneId.of("UTC")).getDayOfWeek().getValue()'],
                'command_type': 'DateTimeType'
            }],


            'callbacks': [{
                'packet': 'Date Time',
                'transform': 'new DateTimeType(ZonedDateTime.of(year, month, day, hour, minute, second, centisecond * 10 * 1000 * 1000, ZoneId.of("UTC")).withZoneSameInstant(ZoneId.systemDefault()))'}]

        }, {
            'id': 'Timestamp',
            'label': 'Timestamp',
            'type': 'Timestamp',
            'java_unit': 'SmartHomeUnits.SECOND',
            'divisor': 1000.0,
            'getters': [{
                'packet': 'Get Timestamp',
                'transform': 'new QuantityType<>(value{divisor}, {unit})'}],

            'callbacks': [{
                'packet': 'Date Time',
                'transform': 'new QuantityType<>(timestamp{divisor}, {unit})'}]
        }, {
            'id': 'Alarm Triggered',
            'label': 'Alarm Triggered',
            'description': 'This listener is triggered every time the current date and time matches the configured alarm (see the setAlarm action).',
            'type': 'system.trigger',
            'callbacks': [{
                'packet': 'Alarm',
                'transform': 'CommonTriggerEvents.PRESSED'
            }],
            'is_trigger_channel': True
        }
    ],
    'channel_types': [
        oh_generic_channel_type('Date Time', 'DateTime', 'Date Time',
                    update_style=None,
                    description="The real-time clock handles leap year and inserts the 29th of February accordingly. But leap seconds are not handled. The time is stored as UTC on the clock and converted into your system's timezone when accessed by OpenHAB."),
        oh_generic_channel_type('Timestamp', 'Number:Time', 'Timestamp',
                    update_style=None,
                    description="the current date and the time of the real-time clock converted to seconds. The timestamp has an effective resolution of hundredths of a second.",
                    read_only=True,
                    pattern='%.2f %unit%')
    ],
    'actions': [{'fn': 'Set Date Time', 'refreshs': ['Date Time']}, 'Get Date Time', 'Get Timestamp', 'Get Offset', 'Set Alarm', 'Get Alarm']
}
