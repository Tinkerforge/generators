# -*- coding: utf-8 -*-

# Rotary Poti Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'version': [1, 0, 0],
    'type': 'Bricklet',
    'name': ('Current25', 'current25'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for sensing current of up to 25A',
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetCurrent', 'get_current'), 
'elements': [('current', 'int16', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns the current of the sensor. The value is in mA
and between -25000mA and 25000mA.

If you want to get the current periodically, it is recommended to use the
callback :func:`Current` and set the period with 
:func:`SetCurrentCallbackPeriod`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('Calibrate', 'calibrate'), 
'elements': [],
'doc': ['am', {
'en':
"""
Calibrates the 0 value of the sensor. You have to call this function
when there is no current present. 

The zero point of the current sensor
is depending on the exact properties of the analog to digital converter,
the length of the Bricklet cable and the temperature. Thus, if you change
the Brick or the environment in which the Bricklet is used, you might
have to recalibrate.

The resulting calibration will be saved on the EEPROM of the Current
Bricklet.
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'function',
'name': ('IsOverCurrent', 'is_over_current'), 
'elements': [('over', 'bool', 1, 'out')],
'doc': ['am', {
'en':
"""
Returns true if more than 25A were measured.

 .. note::
  To reset this value you have to power cycle the Bricklet.

""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'function',
'name': ('GetAnalogValue', 'get_analog_value'), 
'elements': [('value', 'uint16', 1, 'out')],
'doc': ['am', {
'en':
"""
Returns the value as read by a 12 bit analog to digital converter.
The value is between 0 and 4095.

 .. note::
  The value returned by :func:`GetCurrent` is averaged over several samples
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
'type': 'function',
'name': ('SetCurrentCallbackPeriod', 'set_current_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the period in ms with which the :func:`Current` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Current` is only triggered if the current has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetCurrentCallbackPeriod', 'get_current_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the period as set by :func:`SetCurrentCallbackPeriod`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
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
'type': 'function',
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
'type': 'function',
'name': ('SetCurrentCallbackThreshold', 'set_current_callback_threshold'), 
'elements': [('option', 'char', 1, 'in'), 
             ('min', 'int16', 1, 'in'),
             ('max', 'int16', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the thresholds for the :func:`CurrentReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'", "Callback is turned off."
 "'o'", "Callback is triggered when the current is *outside* the min and max values"
 "'i'", "Callback is triggered when the current is *inside* the min and max values"
 "'<'", "Callback is triggered when the current is smaller than the min value (max is ignored)"
 "'>'", "Callback is triggered when the current is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetCurrentCallbackThreshold', 'get_current_callback_threshold'), 
'elements': [('option', 'char', 1, 'out'), 
             ('min', 'int16', 1, 'out'),
             ('max', 'int16', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the threshold as set by :func:`SetCurrentCallbackThreshold`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
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
 "'o'", "Callback is triggered when the current is *outside* the min and max values"
 "'i'", "Callback is triggered when the current is *inside* the min and max values"
 "'<'", "Callback is triggered when the current is smaller than the min value (max is ignored)"
 "'>'", "Callback is triggered when the current is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
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
'type': 'function',
'name': ('SetDebouncePeriod', 'set_debounce_period'), 
'elements': [('debounce', 'uint32', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the period in ms with which the threshold callbacks

 :func:`CurrentReached`, :func:`AnalogValueReached`

are triggered, if the thresholds

 :func:`SetCurrentCallbackThreshold`, :func:`SetAnalogValueCallbackThreshold`

keep being reached.

The default value is 100.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
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
'type': 'callback',
'name': ('Current', 'current'), 
'elements': [('current', 'int16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetCurrentCallbackPeriod`. The :word:`parameter` is the current of the
sensor.

:func:`Current` is only triggered if the current has changed since the
last triggering.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('AnalogValue', 'analog_value'), 
'elements': [('value', 'uint16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetAnalogValueCallbackPeriod`. The :word:`parameter` is the analog value of the
sensor.

:func:`AnalogValue` is only triggered if the current has changed since the
last triggering.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('CurrentReached', 'current_reached'), 
'elements': [('current', 'int16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetCurrentCallbackThreshold` is reached.
The :word:`parameter` is the current of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('AnalogValueReached', 'analog_value_reached'), 
'elements': [('value', 'uint16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetAnalogValueCallbackThreshold` is reached.
The :word:`parameter` is the analog value of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('OverCurrent', 'over_current'), 
'elements': [],
'doc': ['c', {
'en':
"""
This callback is triggered when an over current is measured
(see :func:`IsOverCurrent`).
""",
'de':
"""
"""
}]
})
