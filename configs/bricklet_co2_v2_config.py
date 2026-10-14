# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# CO2 Bricklet 2.0 communication config

from generators.configs.commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from generators.configs.commonconstants import add_callback_value_function

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'category': 'Bricklet',
    'device_identifier': 2147,
    'name': 'CO2 V2',
    'display_name': 'CO2 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures CO2 concentration, temperature and humidity',
        'de': 'Misst CO2-Konzentration, Temperatur und Luftfeuchte'
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

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

com['packets'].append({
'type': 'function',
'name': 'Get All Values',
'elements': [('CO2 Concentration', 'uint16', 1, 'out', {'unit': 'Parts Per Million', 'range': (0, 40000)}),
             ('Temperature', 'int16', 1, 'out', {'scale': (1, 100), 'unit': 'Degree Celsius', 'range': (-4000, 12000)}),
             ('Humidity', 'uint16', 1, 'out', {'scale': (1, 100), 'unit': 'Percent Relative Humidity', 'range': (0, 10000)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns all values measured by the CO2 Bricklet 2.0.

If you want to get the values periodically, it is recommended to use the
:cb:`All Values` callback. You can set the callback configuration
with :func:`Set All Values Callback Configuration`.

.. note::
 The sensor is able to messure up to 120 °C. However it is only specified up to 70 °C.
 Exposing the Bricklet to higher temperatures might result in permanent damage.
""",
'de':
"""
Gibt alle Werte zurück, die das CO2 Bricklet 2.0 misst.

Wenn der Wert periodisch benötigt wird, kann auch der :cb:`All Values` Callback
verwendet werden. Der Callback wird mit der Funktion
:func:`Set All Values Callback Configuration` konfiguriert.

.. note::
 Der Sensor kann bis zu 120 °C messen, ist aber nur bis 70 °C spezifiziert.
 Das Bricklet kann permanent beschädigt werden, falls es höheren Temperaturen ausgesetzt wird.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Air Pressure',
'elements': [('Air Pressure', 'uint16', 1, 'in', {'unit': 'Hectopascal', 'range': [(0, 0), (700, 1200)], 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
The CO2 concentration depends (among other things) on the ambient air pressure.

To increase the accuracy of the CO2 Bricklet 2.0 you can set the current air pressure.
You use the :ref:`Barometer Bricklet 2.0 <barometer_v2_bricklet>` or the
:ref:`Air Quality Bricklet <air_quality_bricklet>` to get the current air pressure.

By default air pressure compensation is disabled. Once you set a value it
will be used for compensation. You can turn the compensation off again by
setting the value to 0.

It is sufficient to update the value every few minutes.
""",
'de':
"""
Die CO2-Konzentration hängt (unter anderem) vom Umgebungs-Luftdruck ab.

Um die Genauigkeit des CO2 Bricklet 2.0 zu verbessern ist es möglich den aktuellen
Luftdruck zu setzen. Dazu kann das :ref:`Barometer Bricklet 2.0 <barometer_v2_bricklet>`
oder auch das :ref:`Air Quality Bricklet <air_quality_bricklet>` genutzt werden.

Standardmäßig ist die Luftdruck-Kompensation deaktiviert. Sobald ein Wert gesetzt
wird, wird dieser zur Kompensation verwendet. Die Kompensation kann wieder
ausgestellt werden in dem der Wert zurück auf 0 gesetzt wird.

Es ist hinreichend den Wert alle paar Minuten zu aktualisieren.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Air Pressure',
'elements': [('Air Pressure', 'uint16', 1, 'out', {'unit': 'Hectopascal', 'range': [(0, 0), (700, 1200)], 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the ambient air pressure as set by :func:`Set Air Pressure`.
""",
'de':
"""
Gibt den Umgebungs-Luftdruch zurück, wie von :func:`Set Air Pressure` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Temperature Offset',
'elements': [('Offset', 'uint16', 1, 'in', {'scale': (1, 100), 'unit': 'Degree Celsius'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets a temperature offset. A offset of 10 will decrease
the measured temperature by 0.1 °C.

If you install this Bricklet into an enclosure and you want to measure the ambient
temperature, you may have to decrease the measured temperature by some value to
compensate for the error because of the heating inside of the enclosure.

We recommend that you leave the parts in the enclosure running for at least
24 hours such that a temperature equilibrium can be reached. After that you can measure
the temperature directly outside of enclosure and set the difference as offset.

This temperature offset is used to calculate the relative humidity and
CO2 concentration. In case the Bricklet is installed in an enclosure, we
recommend to measure and set the temperature offset to improve the accuracy of
the measurements.

It is sufficient to set the temperature offset once. The offset is saved in
non-volatile memory and is applied again after a power loss.
""",
'de':
"""
Setzt ein Temperatur-Offset. Ein Offset von 10 verringert
die gemessene Temperatur um 0,1 °C.

Wenn das Bricklet in einem Gehäuse verbaut wird, aber die Umgebungstemperatur
außerhalb des Gehäuses gemessen werden soll, dann muss vom gemessenen Temperatur
ein bestimmter Wert abgezogen werden, um den Messfehler durch das Aufheizen des
Gehäuses zu kompensieren.

Wir empfehlen den Messaufbau im Gehäuse mindestens 24 Stunden laufen zu lassen,
damit sich ein Temperaturgleichgewicht einstellt. Danach muss die Temperatur
außerhalb des Gehäuses gemessen werden und die Differenz zur Temperatur innerhalb
des Gehäuses als Offset eingestellt werden.

Dieses Temperatur-Offset geht in die Berechnung der Luftfeuchte und der
CO2-Konzentration mit ein. Um die Genauigkeit der Messwerte innerhalb eines
Gehäuses zu verbessern sollte der Temperatur-Offset bestimmt und
eingestellt werden.

Es ist hinreichend den Temperatur-Offset einmal zu setzen. Der Offset wird
in einem nicht-flüchtigen Speicher gespeichert und auch nach einem
Neustart wieder angewendet.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Temperature Offset',
'elements': [('Offset', 'uint16', 1, 'out', {'scale': (1, 100), 'unit': 'Degree Celsius'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the temperature offset as set by
:func:`Set Temperature Offset`.
""",
'de':
"""
Gibt das Temperatur-Offset zurück, wie mittels
:func:`Set Temperature Offset` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set All Values Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period is the period with which the :cb:`All Values`
callback is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after at least one of the values has changed. If the values didn't
change within the period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.
""",
'de':
"""
Die Periode ist die Periode mit der der :cb:`All Values`
Callback ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf true gesetzt wird, wird der
Callback nur ausgelöst, wenn sich mindestens ein Wert im Vergleich zum letzten mal geändert
hat. Ändert sich kein Wert innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn ein Wert sich das nächste mal ändert.

Wird der Parameter auf false gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen der Werte.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get All Values Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set All Values Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set All Values Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'All Values',
'elements': [('CO2 Concentration', 'uint16', 1, 'out', {'unit': 'Parts Per Million', 'range': (0, 40000)}),
             ('Temperature', 'int16', 1, 'out', {'scale': (1, 100), 'unit': 'Degree Celsius', 'range': (-4000, 12000)}),
             ('Humidity', 'uint16', 1, 'out', {'scale': (1, 100), 'unit': 'Percent Relative Humidity', 'range': (0, 10000)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set All Values Callback Configuration`.

The :word:`parameters` are the same as :func:`Get All Values`.

.. note::
 The sensor is able to messure up to 120 °C. However it is only specified up to 70 °C.
 Exposing the Bricklet to higher temperatures might result in permanent damage.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set All Values Callback Configuration` gesetzten Konfiguration

Die :word:`parameters` sind die gleichen wie :func:`Get All Values`.

.. note::
 Der Sensor kann bis zu 120 °C messen, ist aber nur bis 70 °C spezifiziert.
 Das Bricklet kann permanent beschädigt werden, falls es höheren Temperaturen ausgesetzt wird.
"""
}]
})

co2_concentration_doc = {
'en':
"""
Returns CO2 concentration.
""",
'de':
"""
Gibt die CO2-Konzentration zurück.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get CO2 Concentration',
    data_name = 'CO2 Concentration',
    data_type = 'uint16',
    doc       = co2_concentration_doc,
    unit      = 'Parts Per Million',
    range_    = (0, 40000)
)

temperature_doc = {
'en':
"""
Returns temperature.

.. note::
 The sensor is able to messure up to 120 °C. However it is only specified up to 70 °C.
 Exposing the Bricklet to higher temperatures might result in permanent damage.
""",
'de':
"""
Gibt die Temperatur zurück.

.. note::
 Der Sensor kann bis zu 120 °C messen, ist aber nur bis 70 °C spezifiziert.
 Das Bricklet kann permanent beschädigt werden, falls es höheren Temperaturen ausgesetzt wird.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Temperature',
    data_name = 'Temperature',
    data_type = 'int16',
    doc       = temperature_doc,
    scale     = (1, 100),
    unit      = 'Degree Celsius',
    range_    = (-4000, 12000)
)

humidity_doc = {
'en':
"""
Returns relative humidity.
""",
'de':
"""
Gibt die relative Luftfeuchtigkeit zurück.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Humidity',
    data_name = 'Humidity',
    data_type = 'uint16',
    doc       = humidity_doc,
    scale     = (1, 100),
    unit      = 'Percent Relative Humidity',
    range_    = (0, 10000)
)

com['packets'].append({
'type': 'function',
'name': 'Set Automatic Self Calibration',
'elements': [('Enabled', 'bool', 1, 'in', {'default': True})],
'since_firmware': [2, 0, 4],
'doc': ['af', {
'en':
"""
Enables/disables the automatic self-calibration (ASC) of the CO2 sensor.

If ASC is enabled the sensor continuously recalibrates itself. For this to work
the sensor has to be exposed to fresh air for at least one hour every day. The first
time ASC is enabled, the sensor needs at least 7 days of uninterrupted operation to
find its initial calibration parameters.

If the Bricklet is used in an environment where it does not regularly see fresh
air (for example in a living room or bedroom), ASC can result in wrong
CO2 concentration measurements over time. In this case we recommend to disable ASC
and to recalibrate the sensor with :func:`Set Forced Recalibration` instead.

Disabling ASC does not discard the calibration that was found so far. It stays in
use until it is replaced by :func:`Set Forced Recalibration` or by a new
calibration found by ASC.

The setting is saved in flash and applied again after a power loss.

By default ASC is enabled. Before firmware version 2.0.4 ASC was always enabled
and could not be disabled.
""",
'de':
"""
Aktiviert/deaktiviert die automatische Selbstkalibrierung (ASC) des CO2-Sensors.

Bei aktivierter ASC kalibriert sich der Sensor fortlaufend selbst. Dazu muss der
Sensor jeden Tag für mindestens eine Stunde Frischluft ausgesetzt sein. Wird ASC
zum ersten Mal aktiviert, benötigt der Sensor mindestens 7 Tage ununterbrochenen
Betrieb, um seine initialen Kalibrierungsparameter zu bestimmen.

Wird das Bricklet in einer Umgebung eingesetzt, in der es nicht regelmäßig
Frischluft ausgesetzt ist (zum Beispiel in einem Wohn- oder Schlafzimmer), kann ASC
mit der Zeit zu falschen CO2-Messwerten führen. In diesem Fall empfehlen wir ASC
zu deaktivieren und den Sensor stattdessen mittels :func:`Set Forced Recalibration`
zu kalibrieren.

Das Deaktivieren von ASC verwirft nicht die bisher bestimmte Kalibrierung. Diese
bleibt aktiv, bis sie durch :func:`Set Forced Recalibration` oder durch eine neue
von ASC bestimmte Kalibrierung ersetzt wird.

Die Einstellung wird im Flash gespeichert und nach einem Neustart wieder angewendet.

Standardmäßig ist ASC aktiviert. Vor Firmware-Version 2.0.4 war ASC immer aktiviert
und konnte nicht deaktiviert werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Automatic Self Calibration',
'elements': [('Enabled', 'bool', 1, 'out', {'default': True})],
'since_firmware': [2, 0, 4],
'doc': ['af', {
'en':
"""
Returns the automatic self-calibration configuration as set by
:func:`Set Automatic Self Calibration`.
""",
'de':
"""
Gibt die Konfiguration der automatischen Selbstkalibrierung zurück, wie mittels
:func:`Set Automatic Self Calibration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Forced Recalibration',
'elements': [('CO2 Concentration', 'uint16', 1, 'in', {'unit': 'Parts Per Million', 'range': (400, 2000)})],
'since_firmware': [2, 0, 4],
'doc': ['af', {
'en':
"""
Recalibrates the CO2 sensor with a known reference CO2 concentration
(forced recalibration, FRC).

For best results, operate the Bricklet in a stable environment with a known
CO2 concentration close to the sensor, for example next to a calibrated
reference instrument.

The sensor has to measure continuously for at least two minutes before the
recalibration is applied. If this function is called within the first two
minutes after the Bricklet was started, the recalibration is applied automatically
as soon as the two minutes have passed.

The recalibration is saved permanently in the sensor and stays in use after a
power loss.

A forced recalibration replaces the calibration found by the automatic
self-calibration (ASC) and vice versa. If you want to use forced recalibration,
we recommend to disable ASC with :func:`Set Automatic Self Calibration` first.
Otherwise the recalibration may later be overwritten by ASC.

The reference CO2 concentration of the most recent recalibration can be read
back with :func:`Get Forced Recalibration`.
""",
'de':
"""
Kalibriert den CO2-Sensor anhand einer bekannten Referenz-CO2-Konzentration neu
(Forced Recalibration, FRC).

Für beste Ergebnisse sollte das Bricklet in einer stabilen Umgebung mit bekannter
CO2-Konzentration in der Nähe des Sensors betrieben werden, zum Beispiel neben
einem kalibrierten Referenzmessgerät.

Der Sensor muss mindestens zwei Minuten kontinuierlich gemessen haben, bevor die
Neukalibrierung angewendet wird. Wird diese Funktion innerhalb der ersten zwei
Minuten nach dem Start des Bricklets aufgerufen, so wird die Neukalibrierung
automatisch angewendet, sobald die zwei Minuten vergangen sind.

Die Neukalibrierung wird dauerhaft im Sensor gespeichert und bleibt auch nach
einem Neustart aktiv.

Eine Forced Recalibration ersetzt die von der automatischen Selbstkalibrierung
(ASC) bestimmte Kalibrierung und umgekehrt. Soll Forced Recalibration genutzt
werden, empfehlen wir ASC vorher mittels :func:`Set Automatic Self Calibration`
zu deaktivieren. Ansonsten kann die Neukalibrierung später durch ASC
überschrieben werden.

Die Referenz-CO2-Konzentration der letzten Neukalibrierung kann mittels
:func:`Get Forced Recalibration` ausgelesen werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Forced Recalibration',
'elements': [('CO2 Concentration', 'uint16', 1, 'out', {'unit': 'Parts Per Million', 'range': (400, 2000), 'default': 400})],
'since_firmware': [2, 0, 4],
'doc': ['af', {
'en':
"""
Returns the reference CO2 concentration of the most recent forced recalibration
as reported by the CO2 sensor.

The value is updated as soon as the recalibration set by
:func:`Set Forced Recalibration` has been applied (see the two minute
waiting period described there).

The sensor only keeps this value in volatile memory. After a power loss
400 ppm (the default reference value of the sensor) is returned, even though
the recalibration itself is saved permanently in the sensor and stays in use.
""",
'de':
"""
Gibt die Referenz-CO2-Konzentration der letzten Forced Recalibration zurück,
wie vom CO2-Sensor gemeldet.

Der Wert wird aktualisiert, sobald die mittels :func:`Set Forced Recalibration`
gesetzte Neukalibrierung angewendet wurde (siehe die dort beschriebene
Wartezeit von zwei Minuten).

Der Sensor hält diesen Wert nur in flüchtigem Speicher. Nach einem Neustart
werden 400 ppm (der Standard-Referenzwert des Sensors) zurückgegeben, obwohl die
Neukalibrierung selbst dauerhaft im Sensor gespeichert ist und aktiv bleibt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get All Values', 'all values'), [(('CO2 Concentration', 'CO2 Concentration'), 'uint16', 1, None, 'ppm', None), (('Temperature', 'Temperature'), 'int16', 1, 100.0, '°C', None), (('Humidity', 'Humidity'), 'uint16', 1, 100.0, '%RH', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('All Values', 'all values'), [(('CO2 Concentration', 'CO2 Concentration'), 'uint16', 1, None, 'ppm', None), (('Temperature', 'Temperature'), 'int16', 1, 100.0, '°C', None), (('Humidity', 'Humidity'), 'uint16', 1, 100.0, '%RH', None)], None, None),
              ('callback_configuration', ('All Values', 'all values'), [], 1000, False, None, [])]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'channels': [
        oh_generic_channel('CO2 Concentration', 'CO2 Concentration'),
        oh_generic_channel('Temperature', 'Temperature'),
        oh_generic_channel('Humidity', 'Humidity'),
        {
            'id': 'Air Pressure',
            'type': 'Air Pressure',
            'getters': [{
                'packet': 'Get {title_words}',
                'element': '{title_words}',
                'packet_params': [],
                'transform': 'new {number_type}(value{divisor}{unit})'}],

            'setters': [{
                'packet': 'Set {title_words}',
                'element': '{title_words}',
                'packet_params': ['(int)Math.round(cmd.doubleValue(){divisor})'],
                'command_type': 'Number',
            }],

            'java_unit': 'SmartHomeUnits.BAR',
            'divisor': 1000.0,
        }
    ],
    'channel_types': [
        oh_generic_channel_type('CO2 Concentration', 'Number', {'en': 'CO2 Concentration', 'de': 'CO2-Konzentration'},
                    update_style='Callback Configuration',
                    description={'en': 'The measured CO2 concentration.',
                                 'de': 'Die gemessene CO2-Konzentration.'}),
        oh_generic_channel_type('Temperature', 'Number', {'en': 'Temperature', 'de': 'Temperatur'},
                    update_style='Callback Configuration',
                    description={'en': 'The measured temperature.',
                                 'de': 'Die gemessene Temperatur.'}),
        oh_generic_channel_type('Humidity', 'Number', 'Humidity',
                    update_style='Callback Configuration',
                    description={'en': 'The measured humidity.',
                                 'de': 'Die gemessene Luftfeuchtigkeit.'}),
        oh_generic_channel_type('Air Pressure', 'Number:Pressure', {'en': 'Air Pressure', 'de': 'Luftdruck'},
                    update_style=None,
                    description={'en': 'The CO2 concentration (among other things) depends on the ambient air pressure. To increase the accuracy of the CO2 Bricklet 2.0 you can set the current air pressure. You use the Barometer Bricklet 2.0 or the Air Quality Bricklet to get the current air pressure. The expected unit of the ambient air pressure value is bar. By default air pressure compensation is disabled. Once you set a value it will be used for compensation. You can turn the compensation off again by setting the value to 0. It is sufficient to update the value every few minutes.',
                                 'de': 'Die CO2-Konzentration hängt (unter anderem) vom Umgebungs-Luftdruck ab.\n\nUm die Genauigkeit des CO2 Bricklet 2.0 zu verbessern ist es möglich den aktuellen Luftdruck zu setzen. Dazu kann das Barometer Bricklet 2.0 oder auch das Air Quality Bricklet genutzt werden.\n\nStandardmäßig ist die Luftdruck-Kompensation deaktiviert. Sobald ein Wert gesetzt wird, wird dieser zur Kompensation verwendet. Die Kompensation kann wieder ausgestellt werden in dem der Wert zurück auf 0 gesetzt wird.\n\nEs ist hinreichend den Wert alle paar Minuten zu aktualisieren.'})
    ],
    'actions': ['Get All Values', {'fn': 'Set Air Pressure', 'refreshs': ['Air Pressure']}, 'Get Air Pressure', 'Get Temperature Offset', 'Get CO2 Concentration', 'Get Temperature', 'Get Humidity']
}
