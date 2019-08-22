# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Compass Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2153,
    'name': 'Compass',
    'display_name': 'Compass',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '3-axis compass with 0.1mG (milli Gauss) and 0.1° resolution',
        'de': '3-Achsen Kompass mit 0,1mG (Milligauß) und 0,1° Auflösung'
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
'constants': [('100Hz', 0),
              ('200Hz', 1),
              ('400Hz', 2),
              ('600Hz', 3)]
})

heading_doc = {
'en':
"""
Returns the heading in 1/10 degree (north = 0 degree, east = 90 degree).

Alternatively you can use :func:`Get Magnetic Flux Density` and calculate the
heading with ``heading = atan2(y, x) * 180 / PI``.
""",
'de':
"""
Gibt die Richtung in 1/10 Grad zurück (Norden = 0 Grad, Osten = 90 Grad).

Alternativ kann die Funktion :func:`Get Magnetic Flux Density` genutzt werden um
die Richtung per ``heading = atan2(y, x) * 180 / PI`` zu bestimmen.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Heading',
    data_name = 'Heading',
    data_type = 'int16',
    doc       = heading_doc
)

com['packets'].append({
'type': 'function',
'name': 'Get Magnetic Flux Density',
'elements': [('X', 'int32', 1, 'out'),
             ('Y', 'int32', 1, 'out'),
             ('Z', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the `magnetic flux density (magnetic induction) <https://en.wikipedia.org/wiki/Magnetic_flux>`__
for all three axis in 1/10 `mG (milli Gauss) <https://en.wikipedia.org/wiki/Gauss_(unit)>`__.

If you want to get the value periodically, it is recommended to use the
:cb:`Magnetic Flux Density` callback. You can set the callback configuration
with :func:`Set Magnetic Flux Density Callback Configuration`.
""",
'de':
"""
Gibt die `magnetische Flussdichte (magnetische Induktion) <https://de.wikipedia.org/wiki/Magnetische_Flussdichte>`__
für alle drei Achsen in 1/10 `mG (Milligauß) <https://de.wikipedia.org/wiki/Gau%C3%9F_(Einheit)>`__ zurück.

Wenn der Wert periodisch benötigt wird, kann auch der :cb:`Magnetic Flux Density` Callback
verwendet werden. Der Callback wird mit der Funktion
:func:`Set Magnetic Flux Density Callback Configuration` konfiguriert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Magnetic Flux Density Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period in ms is the period with which the :cb:`Magnetic Flux Density` callback
is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.

The default value is (0, false).
""",
'de':
"""
Die Periode in ms ist die Periode mit der der :cb:`Magnetic Flux Density` Callback
ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn der Wert sich im Vergleich zum letzten mal geändert
hat. Ändert der Wert sich nicht innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen des Werts.

Der Standardwert ist (0, false).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Magnetic Flux Density Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set Magnetic Flux Density Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set Magnetic Flux Density Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Magnetic Flux Density',
'elements': [('X', 'int32', 1, 'out'),
             ('Y', 'int32', 1, 'out'),
             ('Z', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set Magnetic Flux Density Callback Configuration`.

The :word:`parameters` are the same as :func:`Get Magnetic Flux Density`.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set Magnetic Flux Density Callback Configuration` gesetzten Konfiguration

Die :word:`parameters` sind der gleichen wie :func:`Get Magnetic Flux Density`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('Data Rate', 'uint8', 1, 'in', {'constant_group': 'Data Rate'}),
             ('Background Calibration', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Configures the data rate and background calibration.

* Data Rate: Sets the data rate that is used by the magnetometer.
  The lower the data rate, the lower is the noise on the data.
* Background Calibration: Set to *true* to enable the background
  calibration and *false* to turn it off. If the background calibration
  is enabled the sensing polarity is flipped once per second to automatically
  calculate and remove offset that is caused by temperature changes.
  This polarity flipping takes about 20ms. This means that once a second
  you will not get new data for a period of 20ms. We highly recommend that
  you keep the background calibration enabled and only disable it if the 20ms
  off-time is a problem in your application.

Default values: Data rate of 100Hz and background calibration enabled.
""",
'de':
"""
Konfiguriert die Datenrate und Hintergrundkalibrierung:

* Data Rate: Setzt die Datenrate des eingesetzten Magnetometers.
  Je niedriger die Datenrate ist, desto weniger Rauschen befindet sich auf den Daten.
* Background Calibration: Aktiviert die automatische Hintergrundkalibrierung, wenn
  auf *true* gesetzt. Wenn die Hintergrundkalibrierung aktiviert ist, ändert
  das Bricklet einmal pro Sekunde die Erfassungspolarität, um damit automatisch
  temperaturabhängige Offsets zu entfernen. Das Ändern der Polarität dauert ungefähr
  20ms. Daher werden einmal pro Sekunde für 20ms keine neuen Daten generiert, wenn
  die Kalibrierung aktiviert ist. Wir empfehlen die Kalibrierung nur zu deaktivieren,
  falls diese 20ms Auszeit ein großes Problem in der Anwendung des Bricklets darstellen.

Standardwerte: Datenrate 100Hz und Hintergrundkalibrierung aktiviert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Data Rate', 'uint8', 1, 'out', {'constant_group': 'Data Rate',}),
             ('Background Calibration', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the configuration as set by :func:`Set Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Calibration',
'elements': [('Offset', 'int16', 3, 'in'),
             ('Gain', 'int16', 3, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets offset and gain for each of the three axes.

The Bricklet is factory calibrated. If you want to re-calibrate the
Bricklet we recommend that you do the calibration through Brick Viewer.

The calibration is saved in non-volatile memory and only has to be
done once.
""",
'de':
"""
Setzt Offset und Gain für alle drei Achsen.

Das Bricklet ist ab Werk kalibriert. Wenn eine Rekalibrierung durchgeführt
werden soll, empfehlen wir dafür den Brick Viewer zu nutzen.

Die Kalibrierung wird in nicht-flüchtigem Speicher gespeichert und muss
nur einmal durchgeführt werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Calibration',
'elements': [('Offset', 'int16', 3, 'out'),
             ('Gain', 'int16', 3, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the calibration parameters as set by :func:`Set Calibration`.
""",
'de':
"""
Gibt die Kalibrierungsparameter zurück, wie von :func:`Set Calibration` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Heading', 'heading'), [(('Heading', 'Heading'), 'int16', 1, 10.0, '°', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Heading', 'heading'), [(('Heading', 'Heading'), 'int16', 1, 10.0, '°', None)], None, None),
              ('callback_configuration', ('Heading', 'heading'), [], 100, False, 'x', [(0, 0)])]
})
