# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# PTC Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2101,
    'name': 'PTC V2',
    'display_name': 'PTC 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Reads temperatures from Pt100 und Pt1000 sensors',
        'de': 'Liest Temperaturen von Pt100 und Pt1000 Sensoren'
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
'name': 'Filter Option',
'type': 'uint8',
'constants': [('50Hz', 0),
              ('60Hz', 1)]
})

com['constant_groups'].append({
'name': 'Wire Mode',
'type': 'uint8',
'constants': [('2', 2),
              ('3', 3),
              ('4', 4)]
})

temperature_doc = {
'en':
"""
Returns the temperature of the connected sensor. The value
has a range of -246 to 849 °C and is given in °C/100,
e.g. a value of 4223 means that a temperature of 42.23 °C is measured.
""",
'de':
"""
Gibt die Temperatur des verbundenen Sensors zurück. Der Wertebereich ist von
-246 bis 849 °C und wird in °C/100 angegeben, z.B. bedeutet
ein Wert von 4223 eine gemessene Temperatur von 42,23 °C.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Temperature',
    data_name = 'Temperature',
    data_type = 'int32',
    doc       = temperature_doc
)

resistance_doc = {
'en':
"""
Returns the value as measured by the MAX31865 precision delta-sigma ADC.

The value can be converted with the following formulas:

* Pt100:  resistance = (value * 390) / 32768
* Pt1000: resistance = (value * 3900) / 32768
""",
'de':
"""
Gibt den Wert zurück, wie vom "MAX31865 Präzisions-Delta-Sigma ADC" berechnet.

Der Wert kann mit den folgenden Formeln in einen Widerstand konvertiert werden:

* Pt100:  Widerstand = (Wert * 390) / 32768
* Pt1000: Widerstand = (Wert * 3900) / 32768
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Resistance',
    data_name = 'Resistance',
    data_type = 'int32',
    doc       = resistance_doc
)

com['packets'].append({
'type': 'function',
'name': 'Set Noise Rejection Filter',
'elements': [('Filter', 'uint8', 1, 'in', {'constant_group': 'Filter Option'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the noise rejection filter to either 50Hz (0) or 60Hz (1).
Noise from 50Hz or 60Hz power sources (including
harmonics of the AC power's fundamental frequency) is
attenuated by 82dB.

Default value is 0 = 50Hz.
""",
'de':
"""
Setzt den Entstörfilter auf 50Hz (0) oder 60Hz (1).
Störungen von 50Hz oder 60Hz Stromquellen (inklusive
Oberwellen der Stromquellen-Grundfrequenz) werden
um 82dB abgeschwächt.

Der Standardwert ist 0 = 50Hz.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Noise Rejection Filter',
'elements': [('Filter', 'uint8', 1, 'out', {'constant_group': 'Filter Option'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the noise rejection filter option as set by
:func:`Set Noise Rejection Filter`
""",
'de':
"""
Gibt die Einstellung des Entstörfilters zurück, wie von
:func:`Set Noise Rejection Filter` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is Sensor Connected',
'elements': [('Connected', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns *true* if the sensor is connected correctly.

If this function
returns *false*, there is either no Pt100 or Pt1000 sensor connected,
the sensor is connected incorrectly or the sensor itself is faulty.

If you want to get the status automatically, it is recommended to use the
:cb:`Sensor Connected` callback. You can set the callback configuration
with :func:`Set Sensor Connected Callback Configuration`.
""",
'de':
"""
Gibt *true* zurück wenn ein Sensor korrekt verbunden ist.

Falls diese Funktion *false* zurück gibt, ist entweder kein
Pt100 oder Pt1000 Sensor verbunden, der Sensor ist inkorrekt
verbunden oder der Sensor selbst ist fehlerhaft.

Zum automatischen übertragen des Status kann auch der
:cb:`Sensor Connected` Callback verwendet werden.
Der Callback wird mit der Funktion
:func:`Set Sensor Connected Callback Configuration` konfiguriert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Wire Mode',
'elements': [('Mode', 'uint8', 1, 'in', {'constant_group': 'Wire Mode'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the wire mode of the sensor. Possible values are 2, 3 and 4 which
correspond to 2-, 3- and 4-wire sensors. The value has to match the jumper
configuration on the Bricklet.

The default value is 2 = 2-wire.
""",
'de':
"""
Stellt die Leiter-Konfiguration des Sensors ein. Mögliche Werte sind 2, 3 und
4, dies entspricht 2-, 3- und 4-Leiter-Sensoren. Der Wert muss er
Jumper-Konfiguration am Bricklet entsprechen.

Der Standardwert ist 2 = 2-Leiter.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Wire Mode',
'elements': [('Mode', 'uint8', 1, 'out', {'constant_group': 'Wire Mode'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the wire mode as set by :func:`Set Wire Mode`
""",
'de':
"""
Gibt die Leiter-Konfiguration zurück, wie von :func:`Set Wire Mode` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Moving Average Configuration',
'elements': [('Moving Average Length Resistance', 'uint16', 1, 'in'),
             ('Moving Average Length Temperature', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
for the resistance and temperature.

Setting the length to 1 will turn the averaging off. With less
averaging, there is more noise on the data.

The range for the averaging is 1-1000.

New data is gathered every 20ms. With a moving average of length 1000 the resulting
averaging window has a length of 20s. If you want to do long term measurements the longest
moving average will give the cleanest results.

The default value is 1 for resistance and 40 for temperature. The default values match
the non-changeable averaging settings of the old PTC Bricklet 1.0
""",
'de':
"""
Setzt die Länge eines `gleitenden Mittelwerts <https://de.wikipedia.org/wiki/Gleitender_Mittelwert>`__
für den Widerstand und die Temperatur.

Wenn die Länge auf 1 gesetzt wird, ist die Mittelwertbildung deaktiviert.
Je kürzer die Länge des Mittelwerts ist, desto mehr Rauschen ist auf den Daten.

Der Wertebereich liegt bei 1-1000.

Einer neue Wert wird alle 20ms gemessen. Mit einer Mittelwerts-Länge von 1000 hat das
resultierende gleitende Fenster eine Zeitspanne von 20s. Bei Langzeitmessungen gibt
ein langer Mittelwert die saubersten Resultate.

Der Standardwert ist 1 für den Widerstand und 40 für die Temperatur. Die Standardwerte entsprechen
den nicht-änderbaren Mittelwert-Einstellungen des alten PTC Bricklet 1.0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Moving Average Configuration',
'elements': [('Moving Average Length Resistance', 'uint16', 1, 'out'),
             ('Moving Average Length Temperature', 'uint16', 1, 'out')],

'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the moving average configuration as set by :func:`Set Moving Average Configuration`.
""",
'de':
"""
Gibt die Moving Average-Konfiguration zurück, wie von :func:`Set Moving Average Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Sensor Connected Callback Configuration',
'elements': [('Enabled', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
If you enable this callback, the :cb:`Sensor Connected` callback is triggered
every time a Pt sensor is connected/disconnected.

By default this callback is disabled.
""",
'de':
"""
Wenn dieser Callback aktiviert ist, wird der :cb:`Sensor Connected` Callback
jedes mal ausgelöst, wenn ein Pt-Sensor verbunden/getrennt wird.

Standardmäßig ist dieser Callback deaktiviert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Sensor Connected Callback Configuration',
'elements': [('Enabled', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the configuration as set by :func:`Set Sensor Connected Callback Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Sensor Connected Callback Configuration`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Sensor Connected',
'elements': [('Connected', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set Sensor Connected Callback Configuration`.

The :word:`parameter` is the same as :func:`Is Sensor Connected`.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set Sensor Connected Callback Configuration` gesetzten Konfiguration

Der :word:`parameter` ist der gleiche wie bei :func:`Is Sensor Connected`.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Temperature', 'temperature'), [(('Temperature', 'Temperature'), 'int32', 1, 100.0, '°C', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Temperature', 'temperature'), [(('Temperature', 'Temperature'), 'int32', 1, 100.0, '°C', None)], None, None),
              ('callback_configuration', ('Temperature', 'temperature'), [], 1000, False, 'x', [(0, 0)])]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('callback', ('Temperature', 'temperature'), [(('Temperature', 'Temperature'), 'int32', 1, 100.0, '°C', None)], None, None),
              ('callback_configuration', ('Temperature', 'temperature'), [], 1000, False, '>', [(30, 0)])]
})
