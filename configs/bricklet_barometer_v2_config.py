# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Barometer Bricklet 2.0 communication config

from generators.configs.commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from generators.configs.commonconstants import add_callback_value_function

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Ishraq Ibne Ashraf <ishraq@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2117,
    'name': 'Barometer V2',
    'display_name': 'Barometer 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures air pressure and altitude changes',
        'de': 'Misst Luftdruck und Höhenänderungen'
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

com['constant_groups'].append({
'name': 'Data Rate',
'type': 'uint8',
'constants': [('Off', 0),
              ('1Hz', 1),
              ('10Hz', 2),
              ('25Hz', 3),
              ('50Hz', 4),
              ('75Hz', 5)]
})

com['constant_groups'].append({
'name': 'Low Pass Filter',
'type': 'uint8',
'constants': [('Off', 0),
              ('1 9th', 1),
              ('1 20th', 2)]
})

air_pressure_doc = {
'en':
"""
Returns the measured air pressure.
""",
'de':
"""
Gibt den Luftdruck des Luftdrucksensors zurück.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Air Pressure',
    data_name = 'Air Pressure',
    data_type = 'int32',
    doc       = air_pressure_doc,
    scale     = (1, 1000),
    unit      = 'Hectopascal',
    range_    = (260000, 1260000)
)

altitude_doc = {
'en':
"""
Returns the relative altitude of the air pressure sensor. The value
is calculated based on the difference between the
current air pressure and the reference air pressure that can be set
with :func:`Set Reference Air Pressure`.
""",
'de':
"""
Gibt die relative Höhe des Luftdrucksensors zurück. Der Wert
wird auf Basis der Differenz zwischen dem aktuellen
Luftdruck und dem Referenzluftdruck berechnet, welcher mit
:func:`Set Reference Air Pressure` gesetzt werden kann.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Altitude',
    data_name = 'Altitude',
    data_type = 'int32',
    doc       = altitude_doc,
    unit      = 'Meter',
    scale     = (1, 1000)
)

temperature_doc = {
'en':
"""
Returns the temperature of the air pressure sensor.

This temperature is used internally for temperature compensation
of the air pressure measurement. It is not as accurate as the
temperature measured by the :ref:`temperature_v2_bricklet` or the
:ref:`temperature_ir_v2_bricklet`.
""",
'de':
"""
Gibt die Temperatur des Luftdrucksensors zurück.

Diese Temperatur wird intern zur Temperaturkompensation der
Luftdruckmessung verwendet. Sie ist nicht so genau wie die
Temperatur die vom :ref:`temperature_v2_bricklet` oder dem
:ref:`temperature_ir_v2_bricklet` gemessen wird.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Temperature',
    data_name = 'Temperature',
    data_type = 'int32',
    doc       = temperature_doc,
    scale     = (1, 100),
    unit      = 'Degree Celsius',
    range_    = (-4000, 8500)
)

com['packets'].append({
'type': 'function',
'name': 'Set Moving Average Configuration',
'elements': [('Moving Average Length Air Pressure', 'uint16', 1, 'in', {'range': (1, 1000), 'default': 100}),
             ('Moving Average Length Temperature', 'uint16', 1, 'in', {'range': (1, 1000), 'default': 100})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
for the air pressure and temperature measurements.

Setting the length to 1 will turn the averaging off. With less
averaging, there is more noise on the data.

If you want to do long term measurements the longest moving average will give
the cleanest results.
""",
'de':
"""
Setzt die Länge eines `gleitenden Mittelwerts <https://de.wikipedia.org/wiki/Gleitender_Mittelwert>`__
für die Luftdruck- und Temperaturmessung.

Wenn die Länge auf 1 gesetzt wird, ist die Mittelwertbildung deaktiviert.
Je kürzer die Länge des Mittelwerts ist, desto mehr Rauschen ist auf den Daten.

Bei Langzeitmessungen gibt ein langer Mittelwert die saubersten Resultate.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Moving Average Configuration',
'elements': [('Moving Average Length Air Pressure', 'uint16', 1, 'out', {'range': (1, 1000), 'default': 100}),
             ('Moving Average Length Temperature', 'uint16', 1, 'out', {'range': (1, 1000), 'default': 100})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the moving average configuration as set by
:func:`Set Moving Average Configuration`.
""",
'de':
"""
Gibt die Moving Average-Konfiguration zurück, wie von
:func:`Set Moving Average Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Reference Air Pressure',
'elements': [('Air Pressure', 'int32', 1, 'in', {'scale': (1, 1000), 'unit': 'Hectopascal', 'range': [(0, 0), (260000, 1260000)], 'default': 1013250})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the reference air pressure for the altitude calculation.
Setting the reference to the
current air pressure results in a calculated altitude of 0mm. Passing 0 is
a shortcut for passing the current air pressure as reference.

Well known reference values are the Q codes
`QNH <https://en.wikipedia.org/wiki/QNH>`__ and
`QFE <https://en.wikipedia.org/wiki/Mean_sea_level_pressure#Mean_sea_level_pressure>`__
used in aviation.
""",
'de':
"""
Setzt den Referenzluftdruck für die Höhenberechnung.
Wenn der aktuelle
Luftdruckwert als Referenz übergeben wird dann gibt die Höhenberechnung
0mm aus. Als Abkürzung kann auch 0 übergeben werden, dadurch wird der
Referenzluftdruck intern auf den aktuellen Luftdruckwert gesetzt.

Wohl bekannte Referenzluftdruckwerte, die in der Luftfahrt verwendet werden, sind
`QNH <https://de.wikipedia.org/wiki/Barometrische_H%C3%B6henmessung_in_der_Luftfahrt#QNH>`__ und
`QFE <https://de.wikipedia.org/wiki/Barometrische_H%C3%B6henmessung_in_der_Luftfahrt#QFE>`__
aus dem Q-Schlüssel.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Reference Air Pressure',
'elements': [('Air Pressure', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Hectopascal', 'range': [(260000, 1260000)], 'default': 1013250})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the reference air pressure as set by :func:`Set Reference Air Pressure`.
""",
'de':
"""
Gibt den Referenzluftdruckwert zurück, wie von :func:`Set Reference Air Pressure` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Calibration',
'elements': [('Measured Air Pressure', 'int32', 1, 'in', {'scale': (1, 1000), 'unit': 'Hectopascal', 'range': [(0, 0), (260000, 1260000)]}),
             ('Actual Air Pressure', 'int32', 1, 'in', {'scale': (1, 1000), 'unit': 'Hectopascal', 'range': [(0, 0), (260000, 1260000)]})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the one point calibration (OPC) values for the air pressure measurement.

Before the Bricklet can be calibrated any previous calibration has to be removed
by setting ``measured air pressure`` and ``actual air pressure`` to 0.

Then the current air pressure has to be measured using the Bricklet
(``measured air pressure``) and with an accurate reference barometer
(``actual air pressure``) at the same time and passed to this function.

After proper calibration the air pressure measurement can achieve an accuracy
up to 0.2 hPa.

The calibration is saved in the EEPROM of the Bricklet and only needs to be
configured once.
""",
'de':
"""
Setzt den One Point Calibration (OPC) Werte für die Luftdruckmessung.

Bevor das Bricklet kalibriert werden kann muss die möglicherweise vorhandene
Kalibierung gelöschet werden, dazu muss ``Measured Air Pressure`` und
``Actual Air Pressure`` auf 0 gesetzt werden.

Dann muss der aktuelle Luftdruck gleichzeitig mit dem Bricklet
(``Measured Air Pressure``) und einem genauen Referenzbarometer
(``Actual Air Pressure``) gemessen und die Werte an diese Funktion
übergeben werden.

Nach einer ordentlichen Kalibrierung kann der Luftdruck mit bis zu 0,2 hPa
Genauigkeit gemessen werden

Die Kalibrierung wird im EEPROM des Bricklets gespeichert und muss nur einmal
gesetzt werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Calibration',
'elements': [('Measured Air Pressure', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Hectopascal', 'range': [(0, 0), (260000, 1260000)]}),
             ('Actual Air Pressure', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Hectopascal', 'range': [(0, 0), (260000, 1260000)]})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the air pressure one point calibration values as set by
:func:`Set Calibration`.
""",
'de':
"""
Gibt die Luftdruck One Point Calibration Werte zurück, wie von
:func:`Set Calibration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Sensor Configuration',
'elements': [('Data Rate', 'uint8', 1, 'in', {'constant_group': 'Data Rate', 'default': 4}),
             ('Air Pressure Low Pass Filter', 'uint8', 1, 'in', {'constant_group': 'Low Pass Filter', 'default': 1})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Configures the data rate and air pressure low pass filter. The low pass filter
cut-off frequency (if enabled) can be set to 1/9th or 1/20th of the configure
data rate to decrease the noise on the air pressure data.

The low pass filter configuration only applies to the air pressure measurement.
There is no low pass filter for the temperature measurement.

A higher data rate will result in a less precise temperature because of
self-heating of the sensor. If the accuracy of the temperature reading is
important to you, we would recommend the 1Hz data rate.
""",
'de':
"""
Konfiguriert die Datenrate und den Luftdrucktiefpassfilter. Die Grenzfrequenz des
Tiefpassfilters (falls aktiviert) kann auf 1/9 oder 1/20 der eingestellten
Datenrate gesetzt werden, um das Rauschen auf den Luftdruckdaten zu verringert.

Die Tiefpassfiltereinstellung gilt nur für die Luftdruckmessung. Es gibt keinen
Tiefpassfilter für die Temperaturmessung.

Eine Verringerung der Datenrate oder des Wertebereichs verringert auch
automatisch das Rauschen auf den Daten. Eine hohe Datenrate erhöht zusätzlich
die Selbsterhitzung des Sensors. Wenn eine hohe Temperaturgenauigkeit
wichtig ist empfehlen wir eine Datenrate von 1Hz.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Sensor Configuration',
'elements': [('Data Rate', 'uint8', 1, 'out', {'constant_group': 'Data Rate', 'default': 4}),
             ('Air Pressure Low Pass Filter', 'uint8', 1, 'out', {'constant_group': 'Low Pass Filter', 'default': 1})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the sensor configuration as set by :func:`Set Sensor Configuration`.
""",
'de':
"""
Gibt die Sensor-Konfiguration zurück, wie von :func:`Set Sensor Configuration` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Air Pressure', 'air pressure'), [(('Air Pressure', 'Air Pressure'), 'int32', 1, 1000.0, 'hPa', None)], []),
              ('getter', ('Get Altitude', 'altitude'), [(('Altitude', 'Altitude'), 'int32', 1, 1000.0, 'm', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Air Pressure', 'air pressure'), [(('Air Pressure', 'Air Pressure'), 'int32', 1, 1000.0, 'hPa', None)], None, None),
              ('callback_configuration', ('Air Pressure', 'air pressure'), [], 1000, False, 'x', [(0, 0)])]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('callback', ('Air Pressure', 'air pressure'), [(('Air Pressure', 'Air Pressure'), 'int32', 1, 1000.0, 'hPa', None)], None, 'Enjoy the potentially good weather!'),
              ('callback_configuration', ('Air Pressure', 'air pressure'), [], 1000, False, '>', [(1025, 0)])]
})


com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups() +  [{
        'name': 'average',
        'label': 'Averaging',
        'description': {'en': 'The length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__ for the air pressure and temperature measurements.\n\nSetting the length to 1 will turn the averaging off. With less averaging, there is more noise on the data.\n\nIf you want to do long term measurements the longest moving average will give the cleanest results.',
                        'de': 'Die Länge eines `gleitenden Mittelwerts <https://de.wikipedia.org/wiki/Gleitender_Mittelwert>`__ für die Luftdruck- und Temperaturmessung.\n\nWenn die Länge auf 1 gesetzt wird, ist die Mittelwertbildung deaktiviert. Je kürzer die Länge des Mittelwerts ist, desto mehr Rauschen ist auf den Daten.\n\nBei Langzeitmessungen gibt ein langer Mittelwert die saubersten Resultate.'},
        'advanced': 'true'
    }],
    'params': [
        {
            'packet': 'Set Moving Average Configuration',
            'element': 'Moving Average Length Air Pressure',

            'name': 'Air Pressure Moving Average Length',
            'type': 'integer',
            'label': 'Air Pressure Moving Average Length',
            'description': {'en': 'The length of a moving averaging for the air pressure.',
                            'de': 'Die Länge eines gleitenden Mittelwerts für den Luftdruck.'},
            'groupName': 'average'
        }, {
            'packet':'Set Moving Average Configuration',
            'element': 'Moving Average Length Temperature',

            'name': 'Temperature Moving Average Length',
            'type': 'integer',
            'label': 'Temperature Moving Average Length',
            'description': {'en': 'The length of a moving averaging for the temperature.',
                            'de': 'Die Länge eines gleitenden Mittelwerts für die Temperatur.'},
            'groupName': 'average'
        }, {
            'packet': 'Set Reference Air Pressure',
            'element': 'Air Pressure',

            'name': 'Reference Air Pressure',
            'type': 'decimal',
            'min': 260, # Disallow 0 intentionally.

            'label': 'Reference Air Pressure',
            'description': {'en': 'The reference air pressure in hPa for the altitude calculation. Setting the reference to the current air pressure results in a calculated altitude of 0 m.',
                            'de': 'Der Referenzluftdruck für die Höhenberechnung. Wenn der aktuelle Luftdruckwert als Referenz übergeben wird, dann gibt die Höhenberechnung 0m aus.'}
        }, {
            'packet': 'Set Sensor Configuration',
            'element': 'Data Rate',

            'name': 'Data Rate',
            'type': 'integer',
            'label': 'Data Rate',
            'description': {'en': "Configures the data rate. A higher data rate will result in a less precise temperature because of self-heating of the sensor. If the accuracy of the temperature reading is important to you, we would recommend the 1Hz data rate.",
                            'de': 'Konfiguriert die Datenrate. Eine Verringerung der Datenrate oder des Wertebereichs verringert auch automatisch das Rauschen auf den Daten. Eine hohe Datenrate erhöht zusätzlich die Selbsterhitzung des Sensors. Wenn eine hohe Temperaturgenauigkeit wichtig ist empfehlen wir eine Datenrate von 1Hz.'},
        }, {
            'packet': 'Set Sensor Configuration',
            'element': 'Air Pressure Low Pass Filter',

            'name': 'Air Pressure Low Pass Filter',
            'type': 'integer',
            'options': [({'en': 'Off', 'de': 'Aus'}, 0),
                        ({'en': '1/9th', 'de': '1/9'}, 1),
                        ({'en': '1/20th', 'de': '1/20'}, 2)],
            'limit_to_options': 'true',
            'label': 'Air Pressure Low Pass Filter',
            'description': {'en': "Configures the air pressure low pass filter. The low pass filter cut-off frequency (if enabled) can be set to 1/9th or 1/20th of the configure data rate to decrease the noise on the air pressure data.",
                            'de': "Konfiguriert den Luftdrucktiefpassfilter. Die Grenzfrequenz des Tiefpassfilters (falls aktiviert) kann auf 1/9 oder 1/20 der eingestellten Datenrate gesetzt werden, um das Rauschen auf den Luftdruckdaten zu verringert.\n\nDie Tiefpassfiltereinstellung gilt nur für die Luftdruckmessung. Es gibt keinen Tiefpassfilter für die Temperaturmessung."}
        },
    ],
    'init_code': """this.setReferenceAirPressure(cfg.referenceAirPressure.multiply(new BigDecimal(1000)).intValue());
this.setMovingAverageConfiguration(cfg.airPressureMovingAverageLength, cfg.temperatureMovingAverageLength);
this.setSensorConfiguration(cfg.dataRate, cfg.airPressureLowPassFilter);""",
    'channels': [
        oh_generic_channel('Air Pressure', 'Air Pressure', 'SmartHomeUnits.BAR', divisor=1000000.0),
        oh_generic_channel('Altitude', 'Altitude'),
        oh_generic_channel('Temperature', 'Temperature'),
    ],
    'channel_types': [
        oh_generic_channel_type('Air Pressure', 'Number:Pressure', {'en': 'Air Pressure', 'de': 'Luftdruck'},
                    update_style='Callback Configuration',
                    description={'en': 'The measured air pressure', 'de': 'Der gemessene Luftdruck'}),
        oh_generic_channel_type('Altitude', 'Number', {'en': 'Altitude', 'de': 'Höhe'},
                    update_style='Callback Configuration',
                    description={'en': 'The relative altitude. The value is calculated based on the difference between the current air pressure and the reference air pressure.',
                                 'de': 'Die relative Höhe. Der Wert wird auf Basis der Differenz zwischen dem aktuellen Luftdruck und dem Referenzluftdruck berechnet.'}),
        oh_generic_channel_type('Temperature', 'Number', 'Temperature',
                    update_style='Callback Configuration',
                    description={'en': 'The measured temperature', 'de': 'Die gemessene Temperatur'}),
    ],
    'actions': ['Get Air Pressure', 'Get Altitude', 'Get Temperature', 'Get Moving Average Configuration', 'Get Reference Air Pressure']
}
