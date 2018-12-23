# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Air Quality Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 297,
    'name': 'Air Quality',
    'display_name': 'Air Quality',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures IAQ index, temperature, humidity and air pressure',
        'de': 'Misst IAQ Index, Temperatur, relative Luftfeuchtigkeit und Luftdruck'
    },
    'comcu': True,
    'released': True,
    'documented': True,
    'discontinued': False,
    'packets': [],
    'examples': []
}

IAQ_CONSTANT = ('Accuracy', [('Unreliable', 0),
                             ('Low',  1),
                             ('Medium',  2),
                             ('High',  3)])

com['packets'].append({
'type': 'function',
'name': 'Get All Values',
'elements': [('IAQ Index', 'int32', 1, 'out'),
             ('IAQ Index Accuracy', 'uint8', 1, 'out', IAQ_CONSTANT),
             ('Temperature', 'int32', 1, 'out'),
             ('Humidity', 'int32', 1, 'out'),
             ('Air Pressure', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns all values measured by the Air Quality Bricklet. The values are
IAQ (Indoor Air Quality) Index, IAQ Index Accuracy, Temperature, Humidity and
Air Pressure.

.. image:: /Images/Misc/bricklet_air_quality_iaq_index.png
   :scale: 100 %
   :alt: Air Quality Index description
   :align: center
   :target: ../../_images/Misc/bricklet_air_quality_iaq_index.png

The values have these ranges and units:

* IAQ Index: 0 to 500, higher value means greater level of air pollution
* IAQ Index Accuracy: 0 = unreliable to 3 = high
* Temperature: in steps of 0.01 °C
* Humidity: in steps of 0.01 %RH
* Air Pressure: in steps of 0.01 mbar
""",
'de':
"""
Gibt alle Werte zurück, die das Air Quality Bricklet misst. Diese Werte umfassen:
IAQ (Indoor Air Quality = Innenraumluftqualität) Index, IAQ Index Genauigkeit,
Temperatur, Luftfeuchte und Luftdruck.

.. image:: /Images/Misc/bricklet_air_quality_iaq_index.png
   :scale: 100 %
   :alt: Air Quality Index description
   :align: center
   :target: ../../_images/Misc/bricklet_air_quality_iaq_index.png

Die Werte haben diese Bereiche und Einheiten:

* IAQ Index: 0 bis 500, ein höhere Werte bedeutet eine stärkere Luftverschmutzung
* IAQ Index Genauigkeit: 0 = unzuverlässig bis 3 = hoch
* Temperatur: in 0,01 °C Schritten
* Luftfeuchte: in 0,01 %RH Schritten
* Luftdruck: in 0,01 mbar Schritten
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Temperature Offset',
'elements': [('Offset', 'int32', 1, 'in')],
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
IAQ index measurements. In case the Bricklet is installed in an enclosure, we
recommend to measure and set the temperature offset to imporve the accuracy of
the measurements.
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

Dieses Temperatur-Offset geht in die Berechnung der Luftfeuchte und des IAQ Index
mit ein. Um die Genauigkeit der Messwerte innerhalb eines Gehäuses zu verbessern
sollte der Temperatur-Offset unbedingt bestimmt und eingestellt werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Temperature Offset',
'elements': [('Offset', 'int32', 1, 'out')],
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
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period in ms is the period with which the :cb:`All Values`
callback is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after at least one of the values has changed. If the values didn't
change within the period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.

The default value is (0, false).
""",
'de':
"""
Die Periode in ms ist die Periode mit der der :cb:`All Values`
Callback ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn sich mindestens ein Wert im Vergleich zum letzten mal geändert
hat. Ändert sich kein Wert innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn ein Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen der Werte.

Der Standardwert ist (0, false).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get All Values Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
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
'elements': [('IAQ Index', 'int32', 1, 'out'),
             ('IAQ Index Accuracy', 'uint8', 1, 'out', IAQ_CONSTANT),
             ('Temperature', 'int32', 1, 'out'),
             ('Humidity', 'int32', 1, 'out'),
             ('Air Pressure', 'int32', 1, 'out')],
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

Die :word:`parameters` sind der gleiche wie :func:`Get All Values`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get IAQ Index',
'elements': [('IAQ Index', 'int32', 1, 'out'),
             ('IAQ Index Accuracy', 'uint8', 1, 'out', IAQ_CONSTANT)],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the IAQ index and accuracy. The IAQ index goes from
0 to 500. The higher the IAQ index, the greater the level of air pollution.

.. image:: /Images/Misc/bricklet_air_quality_iaq_index.png
   :scale: 100 %
   :alt: IAQ index description
   :align: center
   :target: ../../_images/Misc/bricklet_air_quality_iaq_index.png

If you want to get the value periodically, it is recommended to use the
:cb:`IAQ Index` callback. You can set the callback configuration
with :func:`Set IAQ Index Callback Configuration`.
""",
'de':
"""
Gibt den IAQ Index und dessen Genaugkeit zurück. Der IAQ Index hate einen
Wertebereich von 0 bis 500, ein höhere Werte bedeutet eine stärkere
Luftverschmutzung.

.. image:: /Images/Misc/bricklet_air_quality_iaq_index.png
   :scale: 100 %
   :alt: IAQ Index Beschreibung
   :align: center
   :target: ../../_images/Misc/bricklet_air_quality_iaq_index.png

Wenn der Wert periodisch benötigt wird, kann auch der :cb:`IAQ Index` Callback
verwendet werden. Der Callback wird mit der Funktion
:func:`Set IAQ Index Callback Configuration` konfiguriert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set IAQ Index Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period in ms is the period with which the :cb:`IAQ Index`
callback is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after at least one of the values has changed. If the values didn't
change within the period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.

The default value is (0, false).
""",
'de':
"""
Die Periode in ms ist die Periode mit der der :cb:`IAQ Index`
Callback ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn sich mindestens ein Wert im Vergleich zum letzten mal
geändert hat. Ändert sich kein Wert innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn ein Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen der Werte.

Der Standardwert ist (0, false).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get IAQ Index Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set IAQ Index Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set IAQ Index Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'IAQ Index',
'elements': [('IAQ Index', 'int32', 1, 'out'),
             ('IAQ Index Accuracy', 'uint8', 1, 'out', IAQ_CONSTANT)],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set IAQ Index Callback Configuration`.

The :word:`parameters` are the same as :func:`Get IAQ Index`.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set IAQ Index Callback Configuration` gesetzten Konfiguration

Die :word:`parameters` sind die gleichen wie :func:`Get IAQ Index`.
"""
}]
})

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
    data_type = 'int32',
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
    data_type = 'int32',
    doc       = humidity_doc
)

air_pressure_doc = {
'en':
"""
Returns air pressure in steps of 0.01 mbar.
""",
'de':
"""
Gibt den Luftdruck in 0,01 mbar Schritten zurück.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Air Pressure',
    data_name = 'Air Pressure',
    data_type = 'int32',
    doc       = air_pressure_doc
)

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get All Values', 'all values'), [(('IAQ Index', 'IAQ Index'), 'int32', 1, None, None, None), (('IAQ Index Accuracy', 'IAQ Index Accuracy'), 'uint8:constant', 1, None, None, None), (('Temperature', 'Temperature'), 'int32', 1, 100.0, '°C', None), (('Humidity', 'Humidity'), 'int32', 1, 100.0, '%RH', None), (('Air Pressure', 'Air Pressure'), 'int32', 1, 100.0, 'mbar', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('All Values', 'all values'), [(('IAQ Index', 'IAQ Index'), 'int32', 1, None, None, None), (('IAQ Index Accuracy', 'IAQ Index Accuracy'), 'uint8:constant', 1, None, None, None), (('Temperature', 'Temperature'), 'int32', 1, 100.0, '°C', None), (('Humidity', 'Humidity'), 'int32', 1, 100.0, '%RH', None), (('Air Pressure', 'Air Pressure'), 'int32', 1, 100.0, 'mbar', None)], None, None),
              ('callback_configuration', ('All Values', 'all values'), [], 1000, False, None, [])]
})
