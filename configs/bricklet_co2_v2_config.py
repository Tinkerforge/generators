# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# CO2 Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from commonconstants import add_callback_value_function

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
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
'elements': [('CO2 Concentration', 'uint16', 1, 'out'),
             ('Temperature', 'int16', 1, 'out'),
             ('Humidity', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns all values measured by the CO2 Bricklet 2.0. The values are
CO2 concentration (in ppm), temperature (in 0.01 °C)
and humidity (in 0.01 %RH).

If you want to get the values periodically, it is recommended to use the
:cb:`All Values` callback. You can set the callback configuration
with :func:`Set All Values Callback Configuration`.
""",
'de':
"""
Gibt alle Werte zurück, die das CO2 Bricklet 2.0 misst. Diese Werte umfassen:
CO2-Konzentration (in ppm), Temperatur (in 0,01 °C) und
Luftfeuchte (in 0,01 %RH).

Wenn der Wert periodisch benötigt wird, kann auch der :cb:`All Values` Callback
verwendet werden. Der Callback wird mit der Funktion
:func:`Set All Values Callback Configuration` konfiguriert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Air Pressure',
'elements': [('Air Pressure', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
The CO2 concentration (among other things) depends on the ambient air pressure.

To increase the accuracy of the CO2 Bricklet 2.0 you can set the current air pressure.
You use the :ref:`Barometer Bricklet 2.0 <barometer_v2_bricklet>` or the
:ref:`Air Quality Bricklet <air_quality_bricklet>` to get the current air pressure.

The expected unit of the ambient air pressure value is mbar.

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

Die erwartete Einheit des Umgebungs-Luftdrucks ist mbar.

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
'elements': [('Air Pressure', 'uint16', 1, 'out')],
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
'elements': [('Offset', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets a temperature offset with resolution 1/100°C. A offset of 10 will decrease
the measured temperature by 0.1°C.

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
Setzt ein Temperatur-Offset mit Auflösung 1/100°C. Ein Offset von 10 verringert
die gemessene Temperatur um 0,1°C.

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
'elements': [('Offset', 'uint16', 1, 'out')],
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
'elements': [('Period', 'uint32', 1, 'in', {'factor': 1000, 'unit': 'Second', 'default': 0}),
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
'elements': [('Period', 'uint32', 1, 'out', {'divisor': 1000, 'unit': 'Second', 'default': 0}),
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
'elements': [('CO2 Concentration', 'uint16', 1, 'out'),
             ('Temperature', 'int16', 1, 'out'),
             ('Humidity', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set All Values Callback Configuration`.

The :word:`parameters` are the same as :func:`Get All Values`.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set All Values Callback Configuration` gesetzten Konfiguration

Die :word:`parameters` sind die gleichen wie :func:`Get All Values`.
"""
}]
})

co2_concentration_doc = {
'en':
"""
Returns CO2 concentration in ppm.
""",
'de':
"""
Gibt die CO2-Konzentration in ppm zurück.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get CO2 Concentration',
    data_name = 'CO2 Concentration',
    data_type = 'uint16',
    doc       = co2_concentration_doc
)

temperature_doc = {
'en':
"""
Returns temperature in steps of 0.01 °C.
""",
'de':
"""
Gibt die Temperatur in 0,01 °C Schritten zurück.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Temperature',
    data_name = 'Temperature',
    data_type = 'int16',
    doc       = temperature_doc
)

humidity_doc = {
'en':
"""
Returns relative humidity in steps of 0.01 %RH.
""",
'de':
"""
Gibt die relative Luftfeuchtigkeit in 0,01 %RH Schritten zurück.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Humidity',
    data_name = 'Humidity',
    data_type = 'uint16',
    doc       = humidity_doc
)

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
        oh_generic_channel('CO2 Concentration', 'Concentration', 'SmartHomeUnits.PARTS_PER_MILLION'),
        oh_generic_channel('Temperature', 'Temperature', 'SIUnits.CELSIUS', divisor=100.0),
        oh_generic_channel('Humidity', 'Humidity', 'SmartHomeUnits.PERCENT', divisor=100.0),
        {
            'id': 'Air Pressure',
            'type': 'Air Pressure',
            'getters': [{
                'packet': 'Get {title_words}',
                'packet_params': [],
                'transform': 'new QuantityType<>(value{divisor}, {unit})'}],

            'setters': [{
                'packet': 'Set {title_words}',
                'packet_params': ['(int)Math.round(cmd.doubleValue() * 1000.0)']
            }],
            'setter_command_type': 'Number',

            'java_unit': 'SmartHomeUnits.BAR',
            'divisor': 1000.0,
            'is_trigger_channel': False
        }
    ],
    'channel_types': [
        oh_generic_channel_type('Concentration', 'Number:Dimensionless', 'CO2 Concentration',
                    description='The measured CO2 concentration.',
                    read_only=True,
                    pattern='%d %unit%'),
        oh_generic_channel_type('Temperature', 'Number:Temperature', 'Temperature',
                    description='The measured temperature.',
                    read_only=True,
                    pattern='%.2f %unit%'),
        oh_generic_channel_type('Humidity', 'Number:Dimensionless', 'Humidity',
                    description='The measured humidity.',
                    read_only=True,
                    pattern='%.2f %unit%'),
        oh_generic_channel_type('Air Pressure', 'Number:Pressure', 'Air Pressure',
                    description='The CO2 concentration (among other things) depends on the ambient air pressure. To increase the accuracy of the CO2 Bricklet 2.0 you can set the current air pressure. You use the Barometer Bricklet 2.0 or the Air Quality Bricklet to get the current air pressure. The expected unit of the ambient air pressure value is bar. By default air pressure compensation is disabled. Once you set a value it will be used for compensation. You can turn the compensation off again by setting the value to 0. It is sufficient to update the value every few minutes.',
                    pattern='%.3f %unit%')
    ],
    'actions': ['Get All Values', 'Get Air Pressure', 'Get Temperature Offset', 'Get CO2 Concentration', 'Get Temperature', 'Get Humidity']
}
