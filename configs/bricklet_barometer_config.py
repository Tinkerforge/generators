# -*- coding: utf-8 -*-

# Barometer Bricklet communication config

com = {
    'author': 'Matthias Bolte <matthias@tinkerforge.com>',
    'version': [1, 0, 0],
    'category': 'Bricklet',
    'name': ('Barometer', 'barometer', 'Barometer'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for sensing air pressure and altitude changes',
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetAirPressure', 'get_air_pressure'),
'elements': [('air_pressure', 'int32', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns the air pressure of the air pressure sensor. The value
has a range of 1000 to 120000 and is given in mbar/100, i.e. a value
of 100009 means that an air pressure of 1000.09 mbar is measured.

If you want to get the air pressure periodically, it is recommended to use the
callback :func:`AirPressure` and set the period with
:func:`SetAirPressureCallbackPeriod`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAltitude', 'get_altitude'),
'elements': [('altitude', 'int32', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns the relative altitude of the air pressure sensor. The value is given in
cm and represents the different between the current altitude and the reference
altitude that can be set with :func:`CalibrateAltitude`.

If you want to get the altitude periodically, it is recommended to use the
callback :func:`Altitude` and set the period with
:func:`SetAltitudeCallbackPeriod`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetTemperature', 'get_temperature'),
'elements': [('temperature', 'int16', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns the temperature of the air pressure sensor. The value
has a range of -4000 to 8500 and is given in °C/100, i.e. a value
of 2007 means that an illuminance of 20.07 °C is measured.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetAirPressureCallbackPeriod', 'set_air_pressure_callback_period'),
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the period in ms with which the :func:`AirPressure` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`AirPressure` is only triggered if the illuminance has changed since the
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
'name': ('GetAirPressureCallbackPeriod', 'get_air_pressure_callback_period'),
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the period as set by :func:`SetAirPressureCallbackPeriod`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetAltitudeCallbackPeriod', 'set_altitude_callback_period'),
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the period in ms with which the :func:`Altitude` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Altitude` is only triggered if the altitude has changed since the
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
'name': ('GetAltitudeCallbackPeriod', 'get_altitude_callback_period'),
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the period as set by :func:`SetAltitudeCallbackPeriod`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetAirPressureCallbackThreshold', 'set_air_pressure_callback_threshold'),
'elements': [('option', 'char', 1, 'in'),
             ('min', 'int32', 1, 'in'),
             ('max', 'int32', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the thresholds for the :func:`AirPressureReached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off."
 "'o'",    "Callback is triggered when the air pressure is *outside* the min and max values"
 "'i'",    "Callback is triggered when the air pressure is *inside* the min and max values"
 "'<'",    "Callback is triggered when the air pressure is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the air pressure is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAirPressureCallbackThreshold', 'get_air_pressure_callback_threshold'),
'elements': [('option', 'char', 1, 'out'),
             ('min', 'int32', 1, 'out'),
             ('max', 'int32', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the threshold as set by :func:`SetAirPressureCallbackThreshold`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetAltitudeCallbackThreshold', 'set_altitude_callback_threshold'),
'elements': [('option', 'char', 1, 'in'),
             ('min', 'int32', 1, 'in'),
             ('max', 'int32', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the thresholds for the :func:`AltitudeReached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off."
 "'o'",    "Callback is triggered when the altitude is *outside* the min and max values"
 "'i'",    "Callback is triggered when the altitude is *inside* the min and max values"
 "'<'",    "Callback is triggered when the altitude is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the altitude is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAltitudeCallbackThreshold', 'get_altitude_callback_threshold'),
'elements': [('option', 'char', 1, 'out'),
             ('min', 'int32', 1, 'out'),
             ('max', 'int32', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the threshold as set by :func:`SetAltitudeCallbackThreshold`.
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

 :func:`AirPressureReached`, :func:`AltitudeReached`, :func:`TemperatureReached`

are triggered, if the thresholds

 :func:`SetAirPressureCallbackThreshold`, :func:`SetAltitudeCallbackThreshold`, :func:`SetTemperatureCallbackThreshold`

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
'type': 'function',
'name': ('CalibrateAltitude', 'calibrate_altitude'),
'elements': [('debounce', 'uint32', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Calibrates the altitude by setting the reference altitude to the current
altitude.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('AirPressure', 'air_pressure'),
'elements': [('air_pressure', 'int32', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetAirPressureCallbackPeriod`. The :word:`parameter` is the air pressure of the
air pressure sensor.

:func:`AirPressure` is only triggered if the air pressure has changed since the
last triggering.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('Altitude', 'altitude'),
'elements': [('altitude', 'int32', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetAltitudeCallbackPeriod`. The :word:`parameter` is the altitude of the
air pressure sensor.

:func:`Illuminance` is only triggered if the altitude has changed since the
last triggering.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('AirPressureReached', 'air_pressure_reached'),
'elements': [('air_pressure', 'int32', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetAirPressureCallbackThreshold` is reached.
The :word:`parameter` is the air pressure of the air pressure sensor.

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
'name': ('AltitudeReached', 'altitude_reached'),
'elements': [('altitude', 'int32', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetAltitudeCallbackThreshold` is reached.
The :word:`parameter` is the altitude of the air pressure sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
"""
}]
})
