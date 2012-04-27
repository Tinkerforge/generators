# -*- coding: utf-8 -*-

# Joystick Bricklet communication config

com = {
    'author': 'Olaf Lüke (olaf@tinkerforge.com)',
    'version': [1, 0, 0],
    'type': 'Bricklet',
    'name': ('Joystick', 'joystick'),
    'manufacturer': 'Tinkerforge',
    'description': 'Dual-Axis Joystick with Button',
    'packets': []
}

com['packets'].append({
'type': 'method', 
'name': ('GetPosition', 'get_position'), 
'elements': [('x', 'int16', 1, 'out'),
             ('y', 'int16', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns the position of the Joystick. The value ranges between -100 and
100 for both axis. The middle position of the joystick is x=0, y=0. The
returned values are averaged and calibrated (see :func:`Calibrate`).

If you want to get the position periodically, it is recommended to use the
callback :func:`Position` and set the period with 
:func:`SetPositionCallbackPeriod`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('IsPressed', 'is_pressed'), 
'elements': [('pressed', 'bool', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns true if the button is pressed and false otherwise.

It is recommended to use the :func:`Pressed` and :func:`Released` callbacks
to handle the button.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetAnalogValue', 'get_analog_value'), 
'elements': [('x', 'uint16', 1, 'out'),
             ('y', 'uint16', 1, 'out')],
'doc': ['am', {
'en':
"""
Returns the values as read by a 12 bit analog to digital converter.
The values are between 0 and 4095 for both axis.

 .. note::
  The values returned by :func:`GetPosition` are averaged over several samples
  to yield less noise, while :func:`GetAnalogValue` gives back raw
  unfiltered analog values. The only reason to use :func:`GetAnalogValue` is,
  if you need the full resolution of the analog to digital converter.

If you want the analog values periodically, it is recommended to use the 
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
'name': ('Calibrate', 'calibrate'), 
'elements': [],
'doc': ['am', {
'en':
"""
Calibrates the middle position of the Joystick. If your Joystick Bricklet
does not return x=0 and y=0 in the middle position, call this function
while the Joystick is standing still in the middle position.

The resulting calibration will be saved on the EEPROM of the Joystick
Bricklet, thus you only have to calibrate it once.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('SetPositionCallbackPeriod', 'set_position_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the period in ms with which the :func:`Position` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Position` is only triggered if the position has changed since the
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
'name': ('GetPositionCallbackPeriod', 'get_position_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the period as set by :func:`SetPositionCallbackPeriod`.
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
'name': ('SetPositionCallbackThreshold', 'set_position_callback_threshold'), 
'elements': [('option', 'char', 1, 'in'), 
             ('min_x', 'int16', 1, 'in'),
             ('max_x', 'int16', 1, 'in'),
             ('min_y', 'int16', 1, 'in'),
             ('max_y', 'int16', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the thresholds for the :func:`PositionReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'", "Callback is turned off."
 "'o'", "Callback is triggered when the position is *outside* the min and max values"
 "'i'", "Callback is triggered when the position is *inside* the min and max values"
 "'<'", "Callback is triggered when the position is smaller than the min value (max is ignored)"
 "'>'", "Callback is triggered when the position is greater than the min value (max is ignored)"

The default value is ('x', 0, 0, 0, 0).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetPositionCallbackThreshold', 'get_position_callback_threshold'), 
'elements': [('option', 'char', 1, 'out'), 
             ('min_x', 'int16', 1, 'out'),
             ('max_x', 'int16', 1, 'out'),
             ('min_y', 'int16', 1, 'out'),
             ('max_y', 'int16', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the threshold as set by :func:`SetPositionCallbackThreshold`.
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
             ('min_x', 'uint16', 1, 'in'),
             ('max_x', 'uint16', 1, 'in'),
             ('min_y', 'uint16', 1, 'in'),
             ('max_y', 'uint16', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the thresholds for the :func:`AnalogValueReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'", "Callback is turned off."
 "'o'", "Callback is triggered when the position is *outside* the min and max values"
 "'i'", "Callback is triggered when the position is *inside* the min and max values"
 "'<'", "Callback is triggered when the position is smaller than the min value (max is ignored)"
 "'>'", "Callback is triggered when the position is greater than the min value (max is ignored)"

The default value is ('x', 0, 0, 0, 0).
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
             ('min_x', 'uint16', 1, 'out'),
             ('max_x', 'uint16', 1, 'out'),
             ('min_y', 'uint16', 1, 'out'),
             ('max_y', 'uint16', 1, 'out')],
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

 :func:`PositionReached`, :func:`AnalogValueReached`

are triggered, if the thresholds

 :func:`SetPositionCallbackThreshold`, :func:`SetAnalogValueCallbackThreshold`

keep being reached.

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
'name': ('Position', 'position'), 
'elements': [('x', 'int16', 1, 'out'),
             ('y', 'int16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetPositionCallbackPeriod`. The parameter is the position of the
Joystick.

:func:`Position` is only triggered if the position has changed since the
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
'elements': [('x', 'uint16', 1, 'out'),
             ('y', 'uint16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetAnalogValueCallbackPeriod`. The parameters are the analog values
of the Joystick.

:func:`AnalogValue` is only triggered if the value has changed since the
last triggering.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'signal', 
'name': ('PositionReached', 'position_reached'), 
'elements': [('x', 'int16', 1, 'out'),
             ('y', 'int16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetPositionCallbackThreshold` is reached.
The parameter is the position of the Joystick.

If the threshold keeps being reached, the callback is triggered periodically
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
'elements': [('x', 'uint16', 1, 'out'),
             ('y', 'uint16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetAnalogValueCallbackThreshold` is reached.
The parameters are the analog values of the Joystick.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'signal', 
'name': ('Pressed', 'pressed'), 
'elements': [],
'doc': ['c', {
'en':
"""
This callback is triggered when the button is pressed.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'signal', 
'name': ('Released', 'released'), 
'elements': [],
'doc': ['c', {
'en':
"""
This callback is triggered when the button is released.
""",
'de':
"""
"""
}]
})
