# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Load Cell Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 253,
    'name': ('LoadCell', 'load_cell', 'Load Cell', 'Load Cell Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for measuring weight with a load cell',
    'released': False,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetWeight', 'get_weight'), 
'elements': [('weight', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO

If you want to get the weight periodically, it is recommended 
to use the callback :func:`Weight` and set the period with 
:func:`SetWeightCallbackPeriod`.
""",
'de':
"""
TODO

Wenn das Gewicht periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`Weight` zu nutzen und die Periode mit 
:func:`SetWeightCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetWeightCallbackPeriod', 'set_weight_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Weight` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Weight` is only triggered if the weight has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Weight` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Weight` wird nur ausgelöst wenn sich das Gewicht seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetWeightCallbackPeriod', 'get_weight_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetWeightCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetWeightCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetWeightCallbackThreshold', 'set_weight_callback_threshold'), 
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
Sets the thresholds for the :func:`WeightReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the weight is *outside* the min and max values"
 "'i'",    "Callback is triggered when the weight is *inside* the min and max values"
 "'<'",    "Callback is triggered when the weight is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the weight is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`WeightReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn das Gewicht *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn das Gewicht *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn das Gewicht kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn das Gewicht größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetWeightCallbackThreshold', 'get_weight_callback_threshold'), 
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
Returns the threshold as set by :func:`SetWeightCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetWeightCallbackThreshold`
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
Sets the period in ms with which the threshold callback

* :func:`WeightReached`

is triggered, if the threshold

* :func:`SetWeightCallbackThreshold`

keeps being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callback

* :func:`WeightReached`
 
ausgelöst wird, wenn der Schwellwert 

* :func:`SetWeightCallbackThreshold`
 
weiterhin erreicht bleibt.

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
'type': 'function',
'name': ('SetMovingAverage', 'set_moving_average'), 
'elements': [('average', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the length of a `moving averaging <http://en.wikipedia.org/wiki/Moving_average>`__ 
for the value value.

Setting the length to 1 will turn the averaging off. With less
averaging, there is more noise on the data.

The range for the averaging is 1-40.

The default value is 4.
""",
'de':
"""
Setzt die Länge eines gleitenden Mittelwerts für den Wert.

Wenn die Länge auf 1 gesetzt wird, ist das Averaging aus. Desto kleiner
die Länge des Mittelwerts ist, desto mehr Rauschen ist auf den Daten.

Der Wertebereich liegt bei 1-40.

Der Standardwert ist 4.
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

com['packets'].append({
'type': 'function',
'name': ('LEDOn', 'led_on'), 
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('LEDOff', 'led_off'), 
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('IsLEDOn', 'is_led_on'), 
'elements': [('value', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'function',
'name': ('Calibrate', 'calibrate'), 
'elements': [('weight', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
* 0   = set zero point
* > 0 = set gain
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetConfiguration', 'set_configuration'), 
'elements': [('rate', 'uint8', 1, 'in'),
             ('gain', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetConfiguration', 'get_configuration'), 
'elements': [('rate', 'uint8', 1, 'out'),
             ('gain', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
rate: 0 = 10Hz
rate: 1 = 80Hz
gain: 0 = +-3.3*0.5V/128
gain: 1 = +-3.3*0.5V/64
gain: 2 = +-3.3*0.5V/32
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('Weight', 'weight'), 
'elements': [('weight', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetWeightCallbackPeriod`. The :word:`parameter` is the weight
as measured by the load cell.

:func:`Weight` is only triggered if the weight has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetWeightCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist das Gewicht wie von der Wägezelle gemessen.

:func:`Weight` wird nur ausgelöst wenn sich das Gewicht seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('WeightReached', 'weight_reached'), 
'elements': [('weight', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetWeightCallbackThreshold` is reached.
The :word:`parameter` is the weight as measured by the load cell.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetWeightCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist das Gewicht wie von der Wägezelle gemessen.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})
