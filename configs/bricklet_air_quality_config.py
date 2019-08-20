# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Air Quality Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from commonconstants import add_callback_value_function

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'category': 'Bricklet',
    'device_identifier': 297,
    'name': 'Air Quality',
    'display_name': 'Air Quality',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures IAQ index, temperature, humidity and air pressure',
        'de': 'Misst IAQ Index, Temperatur, relative Luftfeuchtigkeit und Luftdruck'
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

com['constant_groups'].append({
'name': 'Accuracy',
'type': 'uint8',
'constants': [('Unreliable', 0),
              ('Low',  1),
              ('Medium',  2),
              ('High',  3)]
})

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

com['constant_groups'].append({
'name': 'Duration',
'type': 'uint8',
'constants': [('4 Days', 0),
              ('28 Days', 1)]
})

com['packets'].append({
'type': 'function',
'name': 'Get All Values',
'elements': [('IAQ Index', 'int32', 1, 'out'),
             ('IAQ Index Accuracy', 'uint8', 1, 'out', {'constant_group': 'Accuracy'}),
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
             ('IAQ Index Accuracy', 'uint8', 1, 'out', {'constant_group': 'Accuracy'}),
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
             ('IAQ Index Accuracy', 'uint8', 1, 'out', {'constant_group': 'Accuracy'})],
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
             ('IAQ Index Accuracy', 'uint8', 1, 'out', {'constant_group': 'Accuracy'})],
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

com['packets'].append({
'type': 'function',
'name': 'Remove Calibration',
'elements': [],
'since_firmware': [2, 0, 3],
'doc': ['af', {
'en':
"""
Deletes the calibration from flash. After you call this function,
you need to power cycle the Air Quality Bricklet.

On the next power up the Bricklet will start a new calibration, as
if it was started for the very first time.

The calibration is based on the data of the last four days, so it takes
four days until a full calibration is re-established.
""",
'de':
"""
Löscht die Kalibrierung auf dem Flash. Nach dem diese Funktion aufgerufen wird
muss das Air Quality Bricklet vom Strom getrennt werden.

Beim nächsten starten des Bricklet wird eine komplett neue Kalibrierung
gestartet, wie beim allerersten Starten des Bricklets.

Die Kalibrierung basiert auf den Daten der letzten vier Tage, daher dauert
es vier Tage bis eine volle Kalibrierung wieder hergestellt ist.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Background Calibration Duration',
'elements': [('Duration', 'uint8', 1, 'in', {'constant_group': 'Duration'})],
'since_firmware': [2, 0, 3],
'doc': ['af', {
'en':
"""
The Air Quality Bricklet uses an automatic background calibration mechanism to
calculate the IAQ Index. This calibration mechanism considers a history of
measured data. The duration of this history can be configured to either be
4 days or 28 days.

If you keep the Bricklet mostly at one place and it does not get moved around
to different environments, we recommend that you use a duration of 28 days.

If you change the duration, the current calibration will be discarded and
the calibration will start from beginning again. The configuration of the
duration is saved in flash, so you should only have to call this function
once in the lifetime of the Bricklet.

The Bricklet has to be power cycled after this function is called
for a duration change to take effect.

Before firmware version 2.0.3 this was not configurable and the duration was
4 days.

The default value (since firmware version 2.0.3) is 28 days.
""",
'de':
"""
Das Air Quality Bricklet nutzt eine automatische Hintergrundkalibrierung um
den IAQ-Index zu bestimmen. Der Kalibrierungsmechanismus nutzt eine Historie
von gemessenen Werte. Die Länge dieser Historie kann zwischen 4 und 28 Tagen
konfiguriert werden.

Wenn das Bricklet hauptsächlich am gleichen Ort bleibt und die Umgebung nicht
oft verändert wird, empfehlen wir eine Länge von 28 Tagen zu verwenden.

Wenn die Länge geändert wird,wird die aktuelle Kalibrierung verworfen und die
Kalibrierung beginnt von vorne. Die Konfiguration der Länge wird im Flash
gespeichert, diese Funktion sollte also nur einmal in der Lebenszeit des
Bricklets aufgerufen werden müssen.

Eine Änderung der Kalibrierungslänge wird beim nächsten Start des Bricklets
übernommen.

Vor Firmware-Version 2.0.3 war die Hintergrundkalibrierungslänge 4 Tage und
nicht konfigurierbare.

Der Standardwert (seit Firmware-Version 2.0.3) beträgt 28 Tage.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Background Calibration Duration',
'elements': [('Duration', 'uint8', 1, 'out', {'constant_group': 'Duration'})],
'since_firmware': [2, 0, 3],
'doc': ['af', {
'en':
"""
Returns the background calibration duration as set by
:func:`Set Background Calibration Duration`.
""",
'de':
"""
Gibt die Länge der Hintergrundkalibrierung zurück, wie von
:func:`Set Background Calibration Duration` gesetzt.
"""
}]
})



com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get All Values', 'all values'), [(('IAQ Index', 'IAQ Index'), 'int32', 1, None, None, None), (('IAQ Index Accuracy', 'IAQ Index Accuracy'), 'uint8:constant', 1, None, None, None), (('Temperature', 'Temperature'), 'int32', 1, 100.0, '°C', None), (('Humidity', 'Humidity'), 'int32', 1, 100.0, '%RH', None), (('Air Pressure', 'Air Pressure'), 'int32', 1, 100.0, 'mbar', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('All Values', 'all values'), [(('IAQ Index', 'IAQ Index'), 'int32', 1, None, None, None), (('IAQ Index Accuracy', 'IAQ Index Accuracy'), 'uint8:constant', 1, None, None, None), (('Temperature', 'Temperature'), 'int32', 1, 100.0, '°C', None), (('Humidity', 'Humidity'), 'int32', 1, 100.0, '%RH', None), (('Air Pressure', 'Air Pressure'), 'int32', 1, 100.0, 'mbar', None)], None, None),
              ('callback_configuration', ('All Values', 'all values'), [], 1000, False, None, [])]
})



com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'params': [{
            'name': 'Temperature Offset',
            'type': 'decimal',
            'default': 0,
            'min': 0,
            'max': 100,

            'label': 'Temperature Offset',
            'description': 'If you install this Bricklet into an enclosure and you want to measure the ambient temperature, you may have to decrease the measured temperature by some value to compensate for the error because of the heating inside of the enclosure.<br/><br/>We recommend that you leave the parts in the enclosure running for at least 24 hours such that a temperature equilibrium can be reached. After that you can measure the temperature directly outside of enclosure and set the difference as offset.<br/><br/>This temperature offset is used to calculate the relative humidity and IAQ index measurements. In case the Bricklet is installed in an enclosure, we recommend to measure and set the temperature offset to imporve the accuracy of the measurements.'
        }
    ],
    'init_code': """this.setTemperatureOffset((int)(cfg.temperatureOffset.doubleValue() * 100.0f));""",
    'channels': [
        oh_generic_channel('Humidity', 'Humidity', 'SmartHomeUnits.PERCENT', divisor=100.0),
        oh_generic_channel('Temperature', 'Temperature', 'SIUnits.CELSIUS', divisor=100.0),
        oh_generic_channel('Air Pressure', 'Air Pressure', 'SmartHomeUnits.MILLIBAR', divisor=100.0),
        {
            'id': 'IAQ Index',
            'type': 'IAQ Index',
            'init_code':"""this.set{camel}CallbackConfiguration(channelCfg.updateInterval, true);""",
            'dispose_code': """this.set{camel}CallbackConfiguration(0, true);""",
            'getters': [{
                'packet': 'Get {title_words}',
                'packet_params': [],
                'transform': 'new QuantityType<>(value.iaqIndex{divisor}, {unit})'}],

            'callbacks': [{
                'packet': '{title_words}',
                'transform': 'new QuantityType<>(iaqIndex{divisor}, {unit})'}],

            'java_unit': 'SmartHomeUnits.ONE',
            'divisor': 1,
            'is_trigger_channel': False
        },{
            'id': 'IAQ Index Accuracy',
            'type': 'IAQ Index Accuracy',
            'init_code':"""this.setIAQIndexCallbackConfiguration(channelCfg.updateInterval, true);""",
            'dispose_code': """this.setIAQIndexCallbackConfiguration(0, true);""",
            'getters': [{
                'packet': 'Get IAQ Index',
                'packet_params': [],
                'transform': 'new QuantityType<>(value.iaqIndexAccuracy{divisor}, {unit})'}],

            'callbacks': [{
                'packet': 'IAQ Index',
                'transform': 'new QuantityType<>(iaqIndexAccuracy{divisor}, {unit})',
                'filter': 'true'}],

            'java_unit': 'SmartHomeUnits.ONE',
            'divisor': 1,
            'is_trigger_channel': False
        }
    ],
    'channel_types': [
        oh_generic_channel_type('Humidity', 'Number:Dimensionless', 'Humidity',
                     description='Measured relative humidity',
                     read_only=True,
                     pattern='%.2f %%',
                     min_=0,
                     max_=100),
        oh_generic_channel_type('Temperature', 'Number:Temperature', 'Temperature',
                     description='Measured temperature',
                     read_only=True,
                     pattern='%.2f %unit%',
                     min_=-40,
                     max_=85),
        oh_generic_channel_type('Air Pressure', 'Number:Pressure', 'Air Pressure',
                     description='Measured air pressure',
                     read_only=True,
                     pattern='%.2f %unit%',
                     min_=300,
                     max_=1100),
        oh_generic_channel_type('IAQ Index', 'Number:Dimensionless', 'IAQ Index',
                     description='The IAQ index goes from 0 to 500. The higher the IAQ index, the greater the level of air pollution.',
                     read_only=True,
                     pattern='%d',
                     min_=0,
                     max_=500),
        oh_generic_channel_type('IAQ Index Accuracy', 'Number:Dimensionless', 'IAQ Index Accuracy',
                     description="The Bricklet is building a database of measurements and uses this data to do an automatic background calibration and calculate an accurate IAQ index over time. It will take a few days until the IAQ index has a high reliability.<br/><br/>The IAQ accuracy is reflects the current state of the background calibration process.<br/><br/>    Accuracy 0: The Bricklet was just started and the sensor is stabilizing.<br/>    Accuracy 1: The background history is uncertain. This typically means the gas sensor data was too stable for the calibration algorithm to clearly define its references.<br/>    Accuracy 2: The Bricklet found new calibration data and is currently calibrating.<br/>    Accuracy 3: The Bricklets is calibrated successfully.<br/><br/>The effective duration of the calibration process depends on the stimuli observed by the sensor. An IAQ accuracy going back and fourth between 2 and 3 is expected, the Bricklet is recalibrating itself.<br/><br/>The Bricklet saves the current database of values and calculated coefficients every 12 hours in its internal flash memory. If the Bricklet loses power it will not take as long to receive reliable data again.<br/><br/>Starting with firmware version 2.0.3 the automatic background calibration considers 28 days of data. We recommend that you run the Bricklet for 28 full days before you consider the data as completely reliable. It is possible to reduce the calibration window to 4 days with the API.<br/><br/><br/>Note<br/><br/>The currently released firmware (2.0.4) does not save the calibration every 12 hours. We had to disable this because of a bug in the proprietary load/save mechanism that we can't fix. We will release a new firmware that has this enabled again as soon as this bug is fixed.",
                     read_only=True,
                     pattern='%d',
                     min_=0,
                     max_=500),
    ]
}
