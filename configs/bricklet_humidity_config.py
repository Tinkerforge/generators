# -*- coding: utf-8 -*-

# Humidity Bricklet communication config

com = {
    'author': 'Olaf Lüke (olaf@tinkerforge.com)',
    'version': '1.0',
    'type': 'Bricklet',
    'name': ('Humidity', 'humidity'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for sensing Humidity',
    'packets': []
}

com['packets'].append({
'type': 'method', 
'name': ('GetHumidity', 'get_humidity'), 
'elements': [('humidity', 'uint16', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns the humidity of the sensor. The value
has a range of 0 to 1000 and is given in %RH/10 (Relative Humidity), 
i.e. a value of 421 means that a humidity of 42.1 %RH is measured.

If you want to get the humidity periodically, it is recommended to use the
callback :func:`Humidity` and set the period with 
:func:`SetHumidityCallbackPeriod`.
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
  The value returned by :func:`GetHumidity` is averaged over several samples
  to yield less noise, while :func:`GetAnalogValue` gives back raw
  unfiltered analog values. The returned humidity value is calibrated for
  room temperatures, if you use the sensor in extreme cold or extreme
  warm enviroments, you might want to calculate the humidity from
  the analog value yourself. See the HIH 5030 datasheet (TODO: link).

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
'name': ('SetHumidityCallbackPeriod', 'set_humidity_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the period in ms with which the :func:`Humidity` callback is called 
periodically. A value of 0 turns the callback off.

:func:`Humidity` is only called if the humidity has changed since the
last call.

The default value is 0.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetHumidityCallbackPeriod', 'get_humidity_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the period as set by :func:`SetHumidityCallbackPeriod`.
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
Sets the period in ms with which the :func:`AnalogValue` callback is called 
periodically. A value of 0 turns the callback off.

:func:`AnalogValue` is only called if the analog value has changed since the
last call.

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
'name': ('SetHumidityCallbackThreshold', 'set_humidity_callback_threshold'), 
'elements': [('option', 'char', 1, 'in'), 
             ('min', 'int16', 1, 'in'),
             ('max', 'int16', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the thresholds for the :func:`HumidityReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'", "Callback is turned off."
 "'o'", "Callback is called when the humidity is *outside* the min and max values"
 "'i'", "Callback is called when the humidity is *inside* the min and max values"
 "'<'", "Callback is called when the humidity is smaller than the min value (max is ignored)"
 "'>'", "Callback is called when the humidity is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetHumidityCallbackThreshold', 'get_humidity_callback_threshold'), 
'elements': [('option', 'char', 1, 'out'), 
             ('min', 'int16', 1, 'out'),
             ('max', 'int16', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the threshold as set by :func:`SetHumidityCallbackThreshold`.
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
 "'o'", "Callback is called when the humidity is *outside* the min and max values"
 "'i'", "Callback is called when the humidity is *inside* the min and max values"
 "'<'", "Callback is called when the humidity is smaller than the min value (max is ignored)"
 "'>'", "Callback is called when the humidity is greater than the min value (max is ignored)"

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

 :func:`HumidityReached`, :func:`AnalogValueReached`

are called, if the thresholds 

 :func:`SetHumidityCallbackThreshold`, :func:`SetAnalogValueCallbackThreshold`

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
'name': ('Humidity', 'humidity'), 
'elements': [('humidity', 'uint16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is called periodically with the period that is set by 
:func:`SetHumidityCallbackPeriod`. The parameter is the humidity of the
sensor.

:func:`Humidity` is only called if the humidity has changed since the
last call.
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
This callback is called periodically with the period that is set by 
:func:`SetAnalogValueCallbackPeriod`. The parameter is the analog value of the
sensor.

:func:`AnalogValue` is only called if the humidity has changed since the
last call.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'signal', 
'name': ('HumidityReached', 'humidity_reached'), 
'elements': [('humidity', 'uint16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is called when the threshold as set by
:func:`SetHumidityCallbackThreshold` is reached.
The parameter is the humidity of the sensor.

If the threshold keeps beeing reached, the callback is called periodically 
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
This callback is called when the threshold as set by
:func:`SetAnalogValueCallbackThreshold` is reached.
The parameter is the analog value of the sensor.

If the threshold keeps beeing reached, the callback is called periodically 
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
"""
}]
})
