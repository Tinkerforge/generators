# -*- coding: utf-8 -*-

# Linear Poti Bricklet communication config

com = {
    'author': 'Olaf Lüke (olaf@tinkerforge.com)',
    'version': [1, 0, 0],
    'type': 'Bricklet',
    'name': ('DistanceIR', 'distance_ir'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for sensing distance via infrared',
    'packets': []
}

com['packets'].append({
'type': 'method', 
'name': ('GetDistance', 'get_distance'), 
'elements': [('distance', 'uint16', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns the distance of the sensor. The value is in mm and
between TODO

If you want to get the distance periodically, it is recommended to use the
callback :func:`Distance` and set the period with 
:func:`SetDistanceCallbackPeriod`.
""",
'de':
"""
"""
}]
})



com['packets'].append({
'type': 'method', 
'name': ('GetAnalogValue', 'get_analog_value'), 
'elements': [('value', 'uint16', 1, 'out')],
'doc': ['am', {
'en':
"""
Returns the value as read by a 12 bit analog to digital converter.
The value is between 0 and 4095.

 .. note::
  The value returned by :func:`GetDistance` is averaged over several samples
  to yield less noise, while :func:`GetAnalogValue` gives back raw
  unfiltered analog values. The only reason to use :func:`GetAnalogValue` is,
  if you need the full resolution of the analog to digital converter.

If you want the analog value periodically, it is recommended to use the 
callback :func:`AnalogValue` and set the period with 
:func:`SetAnalogValueCallbackPeriod`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('SetSamplingPoint', 'set_sampling_point'), 
'elements': [('position', 'uint8', 1, 'in'),
             ('distance', 'uint16',1, 'in')],
'doc': ['am', {
'en':
"""
Sets a sampling point value to a specific position of the lookup table.
The lookup table is comprised of 128 equidistant analog values with
corresponding distances.

If you measure a distance of 50cm at the analog value 2048, you have
shoud call this function with (64, 5000). The utilized analog to digital
converter has a resolution of 12 bit. With 128 sampling points on the
whole range, this means that every sampling point has a size of 32
analog values. Thus the analog value 2048 has the corresponding sampling
point 64 = 2048/32.

Sampling points are saved on the eeprom of the Distance-IR Bricklet and
loaded again on startup.

 .. note::
  An easy way to calibrate the sampling points of the Distace-IR Bricklet is
  implemented in brickv. If you want to calibrate your Bricklet it is
  highly recommended to use this implementation. 

""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetSamplingPoint', 'get_sampling_point'), 
'elements': [('position', 'uint8', 1, 'in'),
             ('distance', 'uint16',1, 'out')],
'doc': ['am', {
'en':
"""
Returns the distance to a sampling point position as set by
:func:`SetSamplingPoint`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('SetDistanceCallbackPeriod', 'set_distance_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the period in ms with which the :func:`Distance` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Distance` is only triggered if the distance has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetDistanceCallbackPeriod', 'get_distance_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the period as set by :func:`SetDistanceCallbackPeriod`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('SetAnalogValueCallbackPeriod', 'set_analog_value_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the period in ms with which the :func:`AnalogValue` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`AnalogValue` is only triggered if the analog value has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetAnalogValueCallbackPeriod', 'get_analog_value_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the period as set by :func:`SetAnalogValueCallbackPeriod`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('SetDistanceCallbackThreshold', 'set_distance_callback_threshold'), 
'elements': [('option', 'char', 1, 'in'), 
             ('min', 'int16', 1, 'in'),
             ('max', 'int16', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the thresholds for the :func:`DistanceReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'", "Callback is turned off."
 "'o'", "Callback is triggered when the distance is *outside* the min and max values"
 "'i'", "Callback is triggered when the distance is *inside* the min and max values"
 "'<'", "Callback is triggered when the distance is smaller than the min value (max is ignored)"
 "'>'", "Callback is triggered when the distance is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetDistanceCallbackThreshold', 'get_distance_callback_threshold'), 
'elements': [('option', 'char', 1, 'out'), 
             ('min', 'int16', 1, 'out'),
             ('max', 'int16', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the threshold as set by :func:`SetDistanceCallbackThreshold`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('SetAnalogValueCallbackThreshold', 'set_analog_value_callback_threshold'), 
'elements': [('option', 'char', 1, 'in'), 
             ('min', 'uint16', 1, 'in'),
             ('max', 'uint16', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the thresholds for the :func:`AnalogValueReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'", "Callback is turned off."
 "'o'", "Callback is triggered when the distance is *outside* the min and max values"
 "'i'", "Callback is triggered when the distance is *inside* the min and max values"
 "'<'", "Callback is triggered when the distance is smaller than the min value (max is ignored)"
 "'>'", "Callback is triggered when the distance is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetAnalogValueCallbackThreshold', 'get_analog_value_callback_threshold'), 
'elements': [('option', 'char', 1, 'out'), 
             ('min', 'uint16', 1, 'out'),
             ('max', 'uint16', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the threshold as set by :func:`SetAnalogValueCallbackThreshold`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('SetDebouncePeriod', 'set_debounce_period'), 
'elements': [('debounce', 'uint32', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the period in ms with which the threshold callbacks

 :func:`DistanceReached`, :func:`AnalogValueReached`

are triggered, if the thresholds

 :func:`SetDistanceCallbackThreshold`, :func:`SetAnalogValueCallbackThreshold`

keep beeing reached.

The default value is 100.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetDebouncePeriod', 'get_debounce_period'), 
'elements': [('debounce', 'uint32', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the debounce period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'signal', 
'name': ('Distance', 'distance'), 
'elements': [('distance', 'uint16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetDistanceCallbackPeriod`. The parameter is the distance of the
sensor.

:func:`Distance` is only triggered if the distance has changed since the
last triggering.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'signal', 
'name': ('AnalogValue', 'analog_value'), 
'elements': [('value', 'uint16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetAnalogValueCallbackPeriod`. The parameter is the analog value of the
sensor.

:func:`AnalogValue` is only triggered if the distance has changed since the
last triggering.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'signal', 
'name': ('DistanceReached', 'distance_reached'), 
'elements': [('distance', 'uint16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetDistanceCallbackThreshold` is reached.
The parameter is the distance of the sensor.

If the threshold keeps beeing reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'signal', 
'name': ('AnalogValueReached', 'analog_value_reached'), 
'elements': [('value', 'uint16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetAnalogValueCallbackThreshold` is reached.
The parameter is the analog value of the sensor.

If the threshold keeps beeing reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
"""
}]
})
