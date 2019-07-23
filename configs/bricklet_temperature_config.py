# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Temperature Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'category': 'Bricklet',
    'device_identifier': 216,
    'name': 'Temperature',
    'display_name': 'Temperature',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures ambient temperature with 0.5°C accuracy',
        'de': 'Misst Umgebungstemperatur mit 0,5°C Genauigkeit'
    },
    'released': True,
    'documented': True,
    'discontinued': False, # selling remaining stock, replaced by Temperature Bricklet 2.0
    'features': [
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

com['constant_groups'].append({
'name': 'I2C Mode',
'type': 'uint8',
'constants': [('Fast', 0),
              ('Slow', 1)]
})

com['packets'].append({
'type': 'function',
'name': 'Get Temperature',
'elements': [('Temperature', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the temperature of the sensor. The value
has a range of -2500 to 8500 and is given in °C/100,
e.g. a value of 4223 means that a temperature of 42.23 °C is measured.

If you want to get the temperature periodically, it is recommended
to use the :cb:`Temperature` callback and set the period with
:func:`Set Temperature Callback Period`.
""",
'de':
"""
Gibt die Temperatur des Sensors zurück. Der Wertebereich ist von
-2500 bis 8500 und wird in °C/100 angegeben, z.B. bedeutet
ein Wert von 4223 eine gemessene Temperatur von 42,23 °C.

Wenn die Temperatur periodisch abgefragt werden soll, wird empfohlen
den :cb:`Temperature` Callback zu nutzen und die Periode mit
:func:`Set Temperature Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Temperature Callback Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :cb:`Temperature` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Temperature` callback is only triggered if the temperature has changed
since the last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :cb:`Temperature` Callback ausgelöst
wird. Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Temperature` Callback wird nur ausgelöst wenn sich die Temperatur seit
der letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Temperature Callback Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Temperature Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Temperature Callback Period`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Temperature Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option'}),
             ('Min', 'int16', 1, 'in'),
             ('Max', 'int16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Temperature Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the temperature is *outside* the min and max values"
 "'i'",    "Callback is triggered when the temperature is *inside* the min and max values"
 "'<'",    "Callback is triggered when the temperature is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the temperature is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Temperature Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Temperatur *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn die Temperatur *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn die Temperatur kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Temperatur größer als der min Wert ist (max wird ignoriert)"

Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Temperature Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option'}),
             ('Min', 'int16', 1, 'out'),
             ('Max', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Temperature Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Temperature Callback Threshold`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Debounce Period',
'elements': [('Debounce', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the threshold callback

* :cb:`Temperature Reached`

is triggered, if the threshold

* :func:`Set Temperature Callback Threshold`

keeps being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callback

* :cb:`Temperature Reached`

ausgelöst wird, wenn der Schwellwert

* :func:`Set Temperature Callback Threshold`

weiterhin erreicht bleibt.

Der Standardwert ist 100.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Debounce Period',
'elements': [('Debounce', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the debounce period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Gibt die Entprellperiode zurück, wie von :func:`Set Debounce Period`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Temperature',
'elements': [('Temperature', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Temperature Callback Period`. The :word:`parameter` is the
temperature of the sensor.

The :cb:`Temperature` callback is only triggered if the temperature has changed
since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Temperature Callback Period`,
ausgelöst. Der :word:`parameter` ist die Temperatur des Sensors.

Der :cb:`Temperature` Callback wird nur ausgelöst wenn sich die Temperatur seit
der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Temperature Reached',
'elements': [('Temperature', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Temperature Callback Threshold` is reached.
The :word:`parameter` is the temperature of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von
:func:`Set Temperature Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Temperatur des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set I2C Mode',
'elements': [('Mode', 'uint8', 1, 'in', {'constant_group': 'I2C Mode'})],
'since_firmware': [2, 0, 1],
'doc': ['af', {
'en':
"""
Sets the I2C mode. Possible modes are:

* 0: Fast (400kHz, default)
* 1: Slow (100kHz)

If you have problems with obvious outliers in the
Temperature Bricklet measurements, they may be caused by EMI issues.
In this case it may be helpful to lower the I2C speed.

It is however not recommended to lower the I2C speed in applications where
a high throughput needs to be achieved.
""",
'de':
"""
Setzt den I2C Modus. Mögliche Modi sind:

* 0: Fast (400kHz, Standard)
* 1: Slow (100kHz)

Wenn Probleme mit offensichtlichen Ausreißern in den
Temperature Bricklet Messungen auftreten, können diese eventuell aufgrund
von elektromagnetischen Störungen sein. In diesem Fall kann es helfen
die I2C Geschwindigkeit zu verringern.

Falls in einem System ein hoher Durchsatz an Nachrichten erwünscht ist,
sollte die I2C Geschwindigkeit allerdings nicht verringert werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get I2C Mode',
'elements': [('Mode', 'uint8', 1, 'out', {'constant_group': 'I2C Mode'})],
'since_firmware': [2, 0, 1],
'doc': ['af', {
'en':
"""
Returns the I2C mode as set by :func:`Set I2C Mode`.
""",
'de':
"""
Gibt den I2C Modus zurück, wie von :func:`Set I2C Mode` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Temperature', 'temperature'), [(('Temperature', 'Temperature'), 'int16', 1, 100.0, '°C', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Temperature', 'temperature'), [(('Temperature', 'Temperature'), 'int16', 1, 100.0, '°C', None)], None, None),
              ('callback_period', ('Temperature', 'temperature'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('Temperature Reached', 'temperature reached'), [(('Temperature', 'Temperature'), 'int16', 1, 100.0, '°C', None)], None, 'It is too hot, we need air conditioning!'),
              ('callback_threshold', ('Temperature', 'temperature'), [], '>', [(30, 0)])]
})
