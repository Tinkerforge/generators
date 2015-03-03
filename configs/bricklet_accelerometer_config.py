# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Accelerometer Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 250,
    'name': ('Accelerometer', 'accelerometer', 'Accelerometer'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for sensing acceleration in three axis',
    'released': False,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetAcceleration', 'get_acceleration'), 
'elements': [('x', 'int16', 1, 'out'),
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO

If you want to get the acceleration periodically, it is recommended 
to use the callback :func:`Acceleration` and set the period with 
:func:`SetAccelerationCallbackPeriod`.
""",
'de':
"""
TODO

Wenn die Farbe periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`Acceleration` zu nutzen und die Periode mit 
:func:`SetAccelerationCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetAccelerationCallbackPeriod', 'set_acceleration_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Acceleration` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Acceleration` is only triggered if the acceleration has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Acceleration` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Acceleration` wird nur ausgelöst wenn sich die Acceleration seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAccelerationCallbackPeriod', 'get_acceleration_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetAccelerationCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetAccelerationCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetAccelerationCallbackThreshold', 'set_acceleration_callback_threshold'), 
'elements': [('option', 'char', 1, 'in', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                  ('Outside', 'outside', 'o'),
                                                                                  ('Inside', 'inside', 'i'),
                                                                                  ('Smaller', 'smaller', '<'),
                                                                                  ('Greater', 'greater', '>')])), 
             ('min_x', 'int16', 1, 'in'),
             ('max_x', 'int16', 1, 'in'),
             ('min_y', 'int16', 1, 'in'),
             ('max_y', 'int16', 1, 'in'),
             ('min_z', 'int16', 1, 'in'),
             ('max_z', 'int16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`AccelerationReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the temperature is *outside* the min and max values"
 "'i'",    "Callback is triggered when the temperature is *inside* the min and max values"
 "'<'",    "Callback is triggered when the temperature is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the temperature is greater than the min value (max is ignored)"

The default value is ('x', 0, 0, 0, 0, 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`AccelerationReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Temperatur *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn die Temperatur *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn die Temperatur kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Temperatur größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0, 0, 0, 0, 0, 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAccelerationCallbackThreshold', 'get_acceleration_callback_threshold'), 
'elements': [('option', 'char', 1, 'out', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                   ('Outside', 'outside', 'o'),
                                                                                   ('Inside', 'inside', 'i'),
                                                                                   ('Smaller', 'smaller', '<'),
                                                                                   ('Greater', 'greater', '>')])), 
             ('min_x', 'int16', 1, 'out'),
             ('max_x', 'int16', 1, 'out'),
             ('min_y', 'int16', 1, 'out'),
             ('max_y', 'int16', 1, 'out'),
             ('min_z', 'int16', 1, 'out'),
             ('max_z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`SetAccelerationCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetAccelerationCallbackThreshold`
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

* :func:`AccelerationReached`

is triggered, if the threshold

* :func:`SetAccelerationCallbackThreshold`

keeps being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callback

* :func:`AccelerationReached`
 
ausgelöst wird, wenn der Schwellwert 

* :func:`SetAccelerationCallbackThreshold`
 
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
'name': ('GetTemperature', 'get_temperature'), 
'elements': [('temperature', 'int8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the temperature of the accelerometer in °C.
""",
'de':
"""
Gibt die Temperatur des Beschleunigungssensors in °C zurück.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('Acceleration', 'acceleration'), 
'elements': [('x', 'int16', 1, 'out'),
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
TODO

:func:`Acceleration` is only triggered if the acceleration has changed since the
last triggering.
""",
'de':
"""
TODO

:func:`Acceleration` wird nur ausgelöst wenn sich die Farbe seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('AccelerationReached', 'acceleration_reached'), 
'elements': [('x', 'int16', 1, 'out'),
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
TODO

:func:`Acceleration` is only triggered if the acceleration has changed since the
last triggering.
""",
'de':
"""
TODO

:func:`Acceleration` wird nur ausgelöst wenn sich die Farbe seit der
letzten Auslösung geändert hat.
"""
}]
})

