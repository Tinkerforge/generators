# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Distance US Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 229,
    'name': ('DistanceUS', 'distance_us', 'Distance US', 'Distance US Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures distance between 2cm and 400cm with ultrasound',
        'de': 'Misst Entfernung zwischen 2cm und 400cm mit Ultraschall'
    },
    'released': True,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetDistanceValue', 'get_distance_value'), 
'elements': [('distance', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current distance value measured by the sensor. The value has a
range of 0 to 4095. A small value corresponds to a small distance, a big
value corresponds to a big distance. The relation between the measured distance
value and the actual distance is affected by the 5V supply voltage (deviations
in the supply voltage result in deviations in the distance values) and is
non-linear (resolution is bigger at close range).

If you want to get the distance value periodically, it is recommended to
use the callback :func:`Distance` and set the period with 
:func:`SetDistanceCallbackPeriod`.
""",
'de':
"""
Gibt den aktuellen Entfernungswert zurück. Der Wert hat einen
Wertebereich von 0 bis 4095. Ein kleiner Wert entspricht einer kleinen
Entfernung, ein großer Wert entspricht einer großen Entfernung. Das Verhältnis
zwischen gemessenem Entfernungswert und wirklicher Entfernung wird durch die
5V Versorgungsspannung beeinflusst (Abweichungen der Versorgungsspannung führen
zu Abweichungen in den Entfernungswerten) und ist nicht-linear (Auflösung ist
größer im Nahbereich).

Wenn der Entfernungswert periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`Distance` zu nutzen und die Periode mit 
:func:`SetDistanceCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetDistanceCallbackPeriod', 'set_distance_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Distance` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Distance` is only triggered if the distance value has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Distance` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Distance` wird nur ausgelöst wenn sich der Entfernungswert seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetDistanceCallbackPeriod', 'get_distance_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetDistanceCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetDistanceCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetDistanceCallbackThreshold', 'set_distance_callback_threshold'), 
'elements': [('option', 'char', 1, 'in', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                  ('Outside', 'outside', 'o'),
                                                                                  ('Inside', 'inside', 'i'),
                                                                                  ('Smaller', 'smaller', '<'),
                                                                                  ('Greater', 'greater', '>')])), 
             ('min', 'int16', 1, 'in'),
             ('max', 'int16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`DistanceReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the distance value is *outside* the min and max values"
 "'i'",    "Callback is triggered when the distance value is *inside* the min and max values"
 "'<'",    "Callback is triggered when the distance value is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the distance value is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`DistanceReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn der Entfernungswert *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn der Entfernungswert *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn der Entfernungswert kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn der Entfernungswert größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetDistanceCallbackThreshold', 'get_distance_callback_threshold'), 
'elements': [('option', 'char', 1, 'out', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                   ('Outside', 'outside', 'o'),
                                                                                   ('Inside', 'inside', 'i'),
                                                                                   ('Smaller', 'smaller', '<'),
                                                                                   ('Greater', 'greater', '>')])), 
             ('min', 'int16', 1, 'out'),
             ('max', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`SetDistanceCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetDistanceCallbackThreshold`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetDebouncePeriod', 'set_debounce_period'), 
'elements': [('debounce', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the threshold callbacks

* :func:`DistanceReached`,

are triggered, if the thresholds

* :func:`SetDistanceCallbackThreshold`,

keep being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callbacks

* :func:`DistanceReached`,
 
ausgelöst werden, wenn die Schwellwerte 

* :func:`SetDistanceCallbackThreshold`,
 
weiterhin erreicht bleiben.

Der Standardwert ist 100.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetDebouncePeriod', 'get_debounce_period'), 
'elements': [('debounce', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the debounce period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Gibt die Entprellperiode zurück, wie von :func:`SetDebouncePeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('Distance', 'distance'), 
'elements': [('distance', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetDistanceCallbackPeriod`. The :word:`parameter` is the distance value
of the sensor.

:func:`Distance` is only triggered if the distance value has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetDistanceCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die Entfernungswert des Sensors.

:func:`Distance` wird nur ausgelöst wenn sich der Entfernungswert seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('DistanceReached', 'distance_reached'), 
'elements': [('distance', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetDistanceCallbackThreshold` is reached.
The :word:`parameter` is the distance value of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetDistanceCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist der Entfernungswert des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetMovingAverage', 'set_moving_average'), 
'elements': [('average', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the length of a `moving averaging <http://en.wikipedia.org/wiki/Moving_average>`__ 
for the distance value.

Setting the length to 0 will turn the averaging completely off. With less
averaging, there is more noise on the data.

The range for the averaging is 0-100.

The default value is 20.
""",
'de':
"""
Setzt die Länge eines `gleitenden Mittelwerts <http://de.wikipedia.org/wiki/Gleitender_Mittelwert>`__
für den Entfernungswert.

Wenn die Länge auf 0 gesetzt wird, ist das Averaging komplett aus. Desto kleiner
die Länge des Mittelwerts ist, desto mehr Rauschen ist auf den Daten.

Der Wertebereich liegt bei 0-100.

Der Standardwert ist 20.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetMovingAverage', 'get_moving_average'), 
'elements': [('average', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the length moving average as set by :func:`SetMovingAverage`.
""",
'de':
"""
Gibt die Länge des gleitenden Mittelwerts zurück, wie von 
:func:`SetMovingAverage` gesetzt.
"""
}]
})
