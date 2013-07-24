# -*- coding: utf-8 -*-

# Water Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 240,
    'name': ('Water', 'water', 'Water'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for sensing water amount (rainfall etc)',
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetWaterValue', 'get_water_value'), 
'elements': [('water', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
If you want to get the water amount value periodically, it is recommended 
to use the callback :func:`Water` and set the period with 
:func:`SetWaterCallbackPeriod`.
""",
'de':
"""
Wenn der Wassermengenwert periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`Water` zu nutzen und die Periode mit 
:func:`SetWaterCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetWaterCallbackPeriod', 'set_water_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Water` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Water` is only triggered if the water amount value has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Water` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Water` wird nur ausgelöst wenn sich der Wassermengenwert seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetWaterCallbackPeriod', 'get_water_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetWaterCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetWaterCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetWaterCallbackThreshold', 'set_water_callback_threshold'), 
'elements': [('option', 'char', 1, 'in', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                  ('Outside', 'outside', 'o'),
                                                                                  ('Inside', 'inside', 'i'),
                                                                                  ('Smaller', 'smaller', '<'),
                                                                                  ('Greater', 'greater', '>')])), 
             ('min', 'uint16', 1, 'in'),
             ('max', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`WaterReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the water amount value is *outside* the min and max values"
 "'i'",    "Callback is triggered when the water amount value is *inside* the min and max values"
 "'<'",    "Callback is triggered when the water amount value is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the water amount value is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`WaterReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn der Wassermengenwert *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn der Wassermengenwert *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn der Wassermengenwert kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn der Wassermengenwert größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetWaterCallbackThreshold', 'get_water_callback_threshold'), 
'elements': [('option', 'char', 1, 'out', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                   ('Outside', 'outside', 'o'),
                                                                                   ('Inside', 'inside', 'i'),
                                                                                   ('Smaller', 'smaller', '<'),
                                                                                   ('Greater', 'greater', '>')])), 
             ('min', 'uint16', 1, 'out'),
             ('max', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`SetWaterCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetWaterCallbackThreshold`
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

* :func:`WaterReached`

is triggered, if the threshold

* :func:`SetWaterCallbackThreshold`

keeps being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callback

* :func:`WaterReached`
 
ausgelöst wird, wenn der Schwellwert 

* :func:`SetWaterCallbackThreshold`
 
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
'type': 'callback',
'name': ('Water', 'water'), 
'elements': [('water', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetWaterCallbackPeriod`. The :word:`parameter` is the water amount value
of the sensor.

:func:`Water` is only triggered if the water amount value has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetWaterCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist der Wassermengenwert des Sensors.

:func:`Water` wird nur ausgelöst wenn sich der Wassermengenwert seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('WaterReached', 'water_reached'), 
'elements': [('water', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetWaterCallbackThreshold` is reached.
The :word:`parameter` is the water amount value of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetWaterCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Wassermengenwert des Sensors.

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
TODO

Max value: 100
""",
'de':
"""
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
""",
'de':
"""
"""
}]
})
