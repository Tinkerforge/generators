# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Barometer Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

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
    'comcu': True,
    'released': True,
    'documented': True,
    'discontinued': False,
    'packets': [],
    'examples': []
}

air_pressure_doc = {
'en':
"""
Returns the measured air pressure. The value has a range of
260000 to 1260000 and is given in mbar/1000, i.e. a value of
1001092 means that an air pressure of 1001.092 mbar is measured.
""",
'de':
"""
Gibt den Luftdruck des Luftdrucksensors zurück. Der Wertbereich
geht von 260000 bis 1260000 und ist in mbar/1000 angegeben, d.h.
bei einem Wert von 1001092 wurde ein Luftdruck von 1001,092 mbar
gemessen.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Air Pressure',
    data_name = 'Air Pressure',
    data_type = 'int32',
    doc       = air_pressure_doc
)

altitude_doc = {
'en':
"""
Returns the relative altitude of the air pressure sensor. The value
is given in mm and is calculated based on the difference between the
current air pressure and the reference air pressure that can be set
with :func:`Set Reference Air Pressure`.
""",
'de':
"""
Gibt die relative Höhe des Luftdrucksensors zurück. Der Wert ist in
mm angegeben und wird auf Basis der Differenz zwischen dem aktuellen
Luftdruck und dem Referenzluftdruck berechnet, welcher mit
:func:`Set Reference Air Pressure` gesetzt werden kann.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Altitude',
    data_name = 'Altitude',
    data_type = 'int32',
    doc       = altitude_doc
)

temperature_doc = {
'en':
"""
Returns the temperature of the air pressure sensor. The value
has a range of -4000 to 8500 and is given in °C/100, i.e. a value
of 2007 means that a temperature of 20.07 °C is measured.

This temperature is used internally for temperature compensation
of the air pressure measurement. It is not as accurate as the
temperature measured by the :ref:`temperature_v2_bricklet` or the
:ref:`temperature_ir_v2_bricklet`.
""",
'de':
"""
Gibt die Temperatur des Luftdrucksensors zurück. Der Wertbereich
ist von -4000 bis 8500 und ist in °C/100 angegeben, d.h. bei
einem Wert von 2007 wurde eine Temperatur von 20,07 °C gemessen.

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
    doc       = temperature_doc
)

com['packets'].append({
'type': 'function',
'name': 'Set Moving Average Configuration',
'elements': [('Moving Average Length Air Pressure', 'uint16', 1, 'in'),
             ('Moving Average Length Temperature', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
for the air pressure and temperature measurements.

Setting the length to 1 will turn the averaging off. With less
averaging, there is more noise on the data.

The range for the averaging is 1-1000.

If you want to do long term measurements the longest moving average will give
the cleanest results.

The default value is 100.
""",
'de':
"""
Setzt die Länge eines `gleitenden Mittelwerts <https://de.wikipedia.org/wiki/Gleitender_Mittelwert>`__
für die Luftdruck- und Temperaturmessung.

Wenn die Länge auf 1 gesetzt wird, ist die Mittelwertbildung deaktiviert.
Desto kürzer die Länge des Mittelwerts ist, desto mehr Rauschen ist auf den Daten.

Der Wertebereich liegt bei 1-1000.

Bei Langzeitmessungen gibt ein langer Mittelwert die saubersten Resultate.

Der Standardwert ist 100.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Moving Average Configuration',
'elements': [('Moving Average Length Air Pressure', 'uint16', 1, 'out'),
             ('Moving Average Length Temperature', 'uint16', 1, 'out')],
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
'elements': [('Air Pressure', 'int32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the reference air pressure in mbar/1000 for the altitude calculation.
Valid values are between 260000 and 1260000. Setting the reference to the
current air pressure results in a calculated altitude of 0mm. Passing 0 is
a shortcut for passing the current air pressure as reference.

Well known reference values are the Q codes
`QNH <https://en.wikipedia.org/wiki/QNH>`__ and
`QFE <https://en.wikipedia.org/wiki/Mean_sea_level_pressure#Mean_sea_level_pressure>`__
used in aviation.

The default value is 1013.25mbar.
""",
'de':
"""
Setzt den Referenzluftdruck in mbar/1000 für die Höhenberechnung.
Gültige Werte liegen zwischen 260000 und 1260000. Wenn der aktuelle
Luftdruckwert als Referenz übergeben wird dann gibt die Höhenberechnung
0mm aus. Als Abkürzung kann auch 0 übergeben werden, dadurch wird der
Referenzluftdruck intern auf den aktuellen Luftdruckwert gesetzt.

Wohl bekannte Referenzluftdruckwerte, die in der Luftfahrt verwendet werden, sind
`QNH <https://de.wikipedia.org/wiki/Barometrische_H%C3%B6henmessung_in_der_Luftfahrt#QNH>`__ und
`QFE <https://de.wikipedia.org/wiki/Barometrische_H%C3%B6henmessung_in_der_Luftfahrt#QFE>`__
aus dem Q-Schlüssel.

Der Standardwert ist 1013,25mbar.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Reference Air Pressure',
'elements': [('Air Pressure', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the reference air pressure as set by :func:`Set Reference Air Pressure`.
""",
'de':
"""
Gibt den Referenzluftdruckwert zurück, wie von :func:`Set Reference Air Pressure`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Calibration',
'elements': [('Measured Air Pressure', 'int32', 1, 'in'),
             ('Actual Air Pressure', 'int32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the one point calibration (OPC) values for the air pressure measurement.

Before the Bricklet can be calibrated any previous calibration has to be removed
by setting ``measured air pressure`` and ``actual air pressure`` to 0.

Then the current air pressure has to be measured using the Bricklet
(``measured air pressure``) and with and accurate reference barometer
(``actual air pressure``) at the same time and passed to this function in
mbar/1000.

After proper calibration the air pressure measurement can achieve an accuracy
up to 0.2 mbar.

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
(``Actual Air Pressure``) gemessen und die Werte in mbar/1000 an diese Funktion
übergeben werden.

Nach einer ordentlichen Kalibrierung kann der Luftdruck mit bis zu 0,2 mbar
Genauigkeit gemessen werden

Die Kalibrierung wird im EEPROM des Bricklets gespeichert und muss nur einmal
gesetzt werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Calibration',
'elements': [('Measured Air Pressure', 'int32', 1, 'out'),
             ('Actual Air Pressure', 'int32', 1, 'out')],
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
'elements': [('Data Rate', 'uint8', 1, 'in', ('Data Rate', [('Off', 0),
                                                            ('1Hz', 1),
                                                            ('10Hz', 2),
                                                            ('25Hz', 3),
                                                            ('50Hz', 4),
                                                            ('75Hz', 5)])),
             ('Air Pressure Low Pass Filter', 'uint8', 1, 'in', ('Low Pass Filter', [('Off', 0),
                                                                                     ('1 9th', 1),
                                                                                     ('1 20th', 2)]))],
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

The default values are 50Hz data rate and 1/9th low pass filter.
""",
'de':
"""
Konfiguriert die Datenrate und de Luftdrucktiefpassfilter. Die Grenzfrequenz des
Tiefpassfilters (falls aktiviert) kann auf 1/9tel oder 1/20stel der eingestellten
Datenrate gesetzt werden, um das Rauschen auf den Luftdruckdaten zu verringert.

Die Tiefpassfiltereinstellung gilt nur für die Luftdruckmessung. Es gibt keinen
Tiefpassfilter für die Temperaturmessung.

Eine Verringerung der Datenrate oder des Wertebereichs verringert auch
automatisch das Rauschen auf den Daten. Eine hohe Datenrate erhöht zusätzlich
die Selbsterhitzung des Sensors. Wenn eine hohe Temperaturgenauigkeit
wichtig ist empfehlen wir eine Datenrate von 1Hz.

Die Standardwerte sind 50Hz Datenrate und 1/9tel Tiefpassfilter.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Sensor Configuration',
'elements': [('Data Rate', 'uint8', 1, 'out', ('Data Rate', [('Off', 0),
                                                             ('1Hz', 1),
                                                             ('10Hz', 2),
                                                             ('25Hz', 3),
                                                             ('50Hz', 4),
                                                             ('75Hz', 5)])),
             ('Air Pressure Low Pass Filter', 'uint8', 1, 'out', ('Low Pass Filter', [('Off', 0),
                                                                                      ('1 9th', 1),
                                                                                      ('1 20th', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the sensor configuration as set by :func:`Set Sensor Configuration`.
""",
'de':
"""
Gibt die Sensor-Konfiguration zurück, wie von :func:`Set Sensor Configuration`
gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Air Pressure', 'air pressure'), [(('Air Pressure', 'Air Pressure'), 'int32', 1, 1000.0, 'mbar', None)], []),
              ('getter', ('Get Altitude', 'altitude'), [(('Altitude', 'Altitude'), 'int32', 1, 1000.0, 'm', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Air Pressure', 'air pressure'), [(('Air Pressure', 'Air Pressure'), 'int32', 1, 1000.0, 'mbar', None)], None, None),
              ('callback_configuration', ('Air Pressure', 'air pressure'), [], 1000, False, 'x', [(0, 0)])]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('callback', ('Air Pressure', 'air pressure'), [(('Air Pressure', 'Air Pressure'), 'int32', 1, 1000.0, 'mbar', None)], None, 'Enjoy the potentially good weather!'),
              ('callback_configuration', ('Air Pressure', 'air pressure'), [], 1000, False, '>', [(1025, 0)])]
})
