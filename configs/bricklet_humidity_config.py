# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Humidity Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'api_version_extra': 1, # +1 for "Break API to fix threshold min/max type mismatch [59d13f6]"
    'category': 'Bricklet',
    'device_identifier': 27,
    'name': 'Humidity',
    'display_name': 'Humidity',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures relative humidity',
        'de': 'Misst relative Luftfeuchtigkeit'
    },
    'released': True,
    'documented': True,
    'discontinued': True,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Get Humidity',
'elements': [('Humidity', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the humidity of the sensor. The value
has a range of 0 to 1000 and is given in %RH/10 (Relative Humidity),
i.e. a value of 421 means that a humidity of 42.1 %RH is measured.

If you want to get the humidity periodically, it is recommended to use the
:cb:`Humidity` callback and set the period with
:func:`Set Humidity Callback Period`.
""",
'de':
"""
Gibt die gemessene Luftfeuchtigkeit des Sensors zurück. Der Wertebereich ist von
0 bis 1000 und wird in %RH/10 angegeben (relative Luftfeuchtigkeit), z.B. bedeutet
ein Wert von 421 eine gemessene Luftfeuchtigkeit von 42,1 %RH.

Wenn die Luftfeuchtigkeit periodisch abgefragt werden soll, wird empfohlen
den :cb:`Humidity` Callback zu nutzen und die Periode mit
:func:`Set Humidity Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Analog Value',
'elements': [('Value', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the value as read by a 12-bit analog-to-digital converter.
The value is between 0 and 4095.

.. note::
 The value returned by :func:`Get Humidity` is averaged over several samples
 to yield less noise, while :func:`Get Analog Value` gives back raw
 unfiltered analog values. The returned humidity value is calibrated for
 room temperatures, if you use the sensor in extreme cold or extreme
 warm environments, you might want to calculate the humidity from
 the analog value yourself. See the `HIH 5030 datasheet
 <https://github.com/Tinkerforge/humidity-bricklet/raw/master/datasheets/hih-5030.pdf>`__.

If you want the analog value periodically, it is recommended to use the
:cb:`Analog Value` callback and set the period with
:func:`Set Analog Value Callback Period`.
""",
'de':
"""
Gibt den Wert, wie vom 12-Bit Analog-Digital-Wandler gelesen, zurück. Der
Wertebereich ist 0 bis 4095.

.. note::
 Der von :func:`Get Humidity` zurückgegebene Wert ist über mehrere
 Messwerte gemittelt um das Rauschen zu vermindern, während :func:`Get Analog Value`
 unverarbeitete Analogwerte zurück gibt. Der zurückgegebene Luftfeuchtigkeitswert
 ist auf Raumtemperatur kalibriert, d.h. wenn der Sensor in sehr kalten oder
 warmen Umgebungen verwendet wird, ist es ratsam den Luftfeuchtigkeitswert
 direkt aus den Analogwerten zu berechnen. Siehe hierzu das `HIH 5030 Datenblatt
 <https://github.com/Tinkerforge/humidity-bricklet/raw/master/datasheets/hih-5030.pdf>`__.

Wenn der Analogwert periodisch abgefragt werden soll, wird empfohlen
den :cb:`Analog Value` Callback zu nutzen und die Periode mit
:func:`Set Analog Value Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Humidity Callback Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :cb:`Humidity` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Humidity` callback is only triggered if the humidity has changed
since the last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :cb:`Humidity` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Humidity` Callback wird nur ausgelöst wenn sich die Luftfeuchtigkeit
seit der letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Humidity Callback Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Humidity Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Humidity Callback Period`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Analog Value Callback Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :cb:`Analog Value` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Analog Value` callback is only triggered if the analog value has
changed since the last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :cb:`Analog Value` Callback ausgelöst
wird. Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Analog Value` Callback wird nur ausgelöst wenn sich der Analogwert
seit der letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Analog Value Callback Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Analog Value Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Analog Value Callback Period`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Humidity Callback Threshold',
'elements': [('Option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint16', 1, 'in'),
             ('Max', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Humidity Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the humidity is *outside* the min and max values"
 "'i'",    "Callback is triggered when the humidity is *inside* the min and max values"
 "'<'",    "Callback is triggered when the humidity is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the humidity is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Humidity Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Luftfeuchtigkeit *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn die Luftfeuchtigkeit *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn die Luftfeuchtigkeit kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Luftfeuchtigkeit größer als der min Wert ist (max wird ignoriert)"

Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Humidity Callback Threshold',
'elements': [('Option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint16', 1, 'out'),
             ('Max', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Humidity Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Humidity Callback Threshold`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Analog Value Callback Threshold',
'elements': [('Option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint16', 1, 'in'),
             ('Max', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Analog Value Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the analog value is *outside* the min and max values"
 "'i'",    "Callback is triggered when the analog value is *inside* the min and max values"
 "'<'",    "Callback is triggered when the analog value is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the analog value is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Analog Value Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn der Analogwert *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn der Analogwert *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn der Analogwert kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn der Analogwert größer als der min Wert ist (max wird ignoriert)"

Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Analog Value Callback Threshold',
'elements': [('Option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint16', 1, 'out'),
             ('Max', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Analog Value Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Analog Value Callback Threshold`
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
Sets the period in ms with which the threshold callbacks

* :cb:`Humidity Reached`,
* :cb:`Analog Value Reached`

are triggered, if the thresholds

* :func:`Set Humidity Callback Threshold`,
* :func:`Set Analog Value Callback Threshold`

keep being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callbacks

* :cb:`Humidity Reached`,
* :cb:`Analog Value Reached`

ausgelöst werden, wenn die Schwellwerte

* :func:`Set Humidity Callback Threshold`,
* :func:`Set Analog Value Callback Threshold`

weiterhin erreicht bleiben.

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
'name': 'Humidity',
'elements': [('Humidity', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Humidity Callback Period`. The :word:`parameter` is the humidity of
the sensor.

The :cb:`Humidity` callback is only triggered if the humidity has changed since
the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Humidity Callback Period`,
ausgelöst. Der :word:`parameter` ist die Luftfeuchtigkeit des Sensors.

Der :cb:`Humidity` Callback wird nur ausgelöst wenn sich die Luftfeuchtigkeit
seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Analog Value',
'elements': [('Value', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Analog Value Callback Period`. The :word:`parameter` is the analog
value of the sensor.

The :cb:`Analog Value` callback is only triggered if the humidity has changed
since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Analog Value Callback Period`,
ausgelöst. Der :word:`parameter` ist der Analogwert des Sensors.

:cb:`Analog Value` Callback wird nur ausgelöst wenn sich der Analogwert seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Humidity Reached',
'elements': [('Humidity', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Humidity Callback Threshold` is reached.
The :word:`parameter` is the humidity of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von
:func:`Set Humidity Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Luftfeuchtigkeit des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Analog Value Reached',
'elements': [('Value', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Analog Value Callback Threshold` is reached.
The :word:`parameter` is the analog value of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von
:func:`Set Analog Value Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist der Analogwert des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Humidity', 'humidity'), [(('Humidity', 'Humidity'), 'uint16', 1, 10.0, '%RH', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Humidity', 'humidity'), [(('Humidity', 'Humidity'), 'uint16', 1, 10.0, '%RH', None)], None, None),
              ('callback_period', ('Humidity', 'humidity'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('Humidity Reached', 'humidity reached'), [(('Humidity', 'Humidity'), 'uint16', 1, 10.0, '%RH', None)], None, 'Recommended humiditiy for human comfort is 30 to 60 %RH.'),
              ('callback_threshold', ('Humidity', 'humidity'), [], 'o', [(30, 60)])]
})
