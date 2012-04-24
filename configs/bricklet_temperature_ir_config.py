# -*- coding: utf-8 -*-

# Temperature-IR Bricklet communication config

com = {
    'author': 'Olaf Lüke (olaf@tinkerforge.com)',
    'version': [1, 0, 0],
    'type': 'Bricklet',
    'name': ('TemperatureIR', 'temperature_ir'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for non-contact temperature sensing',
    'packets': []
}

com['packets'].append({
'type': 'method', 
'name': ('GetAmbientTemperature', 'get_ambient_temperature'), 
'elements': [('temperature', 'int16', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns the ambient temperature of the sensor. The value
has a range of -400 to 1250 and is given in °C/10,
e.g. a value of 423 means that an ambient temperature of 42.3 °C is 
measured.

If you want to get the ambient temperature periodically, it is recommended 
to use the callback :func:`AmbientTemperature` and set the period with 
:func:`SetAmbientTemperatureCallbackPeriod`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetObjectTemperature', 'get_object_temperature'), 
'elements': [('temperature', 'int16', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns the object temperature of the sensor, i.e. the temperature
of the surface of the object the sensor is aimed at. The value
has a range of -700 to 3800 and is given in °C/10,
e.g. a value of 30001 means that a temperature of 300.01 °C is measured
on the surface of the object.

The temperature of different materials is dependent on their `emissivity 
<http://en.wikipedia.org/wiki/Emissivity>`_. The emissivity of the material
can be set with :func:`SetEmissivity`.

If you want to get the object temperature periodically, it is recommended 
to use the callback :func:`ObjectTemperature` and set the period with 
:func:`SetObjectTemperatureCallbackPeriod`.
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'method', 
'name': ('SetEmissivity', 'set_emissivity'), 
'elements': [('emissivity', 'uint16', 1, 'in')],
'doc': ['am', {
'en':
"""
Sets the `emissivity <http://en.wikipedia.org/wiki/Emissivity>`_ that is 
used to calculate the surface temperature as returned by 
:func:`GetObjectTemperature`. 

The emissivity is usually given as a value between 0.0 and 1.0. A list of
emissivities of different materials can be found 
`here <http://www.infrared-thermography.com/material.htm>`_.

The parameter of :func:`SetEmissivity` has to be given with a factor of
65535 (16 bit). For example: An emissivity of 0.1 can be set with the 
value 6553, an emissivity of 0.5 with the value 32767 and so on.

 .. note::
  If you need a precise measurement for the object temperature, it is
  absolutely crucial that you also provide a precise emissivity.

The default emissivity is 1.0 (value of 65535) and the minimum emissivity the
sensor can handle is 0.1 (value of 6553).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetEmissivity', 'get_emissivity'), 
'elements': [('emissivity', 'uint16', 1, 'out')],
'doc': ['am', {
'en':
"""
Returns the emissivity as set by :func:`SetEmissivity`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('SetAmbientTemperatureCallbackPeriod', 'set_ambient_temperature_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the period in ms with which the :func:`AmbientTemperature` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`AmbientTemperature` is only triggered if the temperature has changed since the
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
'name': ('GetAmbientTemperatureCallbackPeriod', 'get_ambient_temperature_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the period as set by :func:`SetAmbientTemperatureCallbackPeriod`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('SetObjectTemperatureCallbackPeriod', 'set_object_temperature_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the period in ms with which the :func:`ObjectTemperature` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`ObjectTemperature` is only triggered if the temperature has changed since the
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
'name': ('GetObjectTemperatureCallbackPeriod', 'get_object_temperature_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the period as set by :func:`SetObjectTemperatureCallbackPeriod`.
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'method', 
'name': ('SetAmbientTemperatureCallbackThreshold', 'set_ambient_temperature_callback_threshold'), 
'elements': [('option', 'char', 1, 'in'), 
             ('min', 'int16', 1, 'in'),
             ('max', 'int16', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the thresholds for the :func:`AmbientTemperatureReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'", "Callback is turned off."
 "'o'", "Callback is triggered when the temperature is *outside* the min and max values"
 "'i'", "Callback is triggered when the temperature is *inside* the min and max values"
 "'<'", "Callback is triggered when the temperature is smaller than the min value (max is ignored)"
 "'>'", "Callback is triggered when the temperature is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetAmbientTemperatureCallbackThreshold', 'get_ambient_temperature_callback_threshold'), 
'elements': [('option', 'char', 1, 'out'), 
             ('min', 'int16', 1, 'out'),
             ('max', 'int16', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the threshold as set by :func:`SetAmbientTemperatureCallbackThreshold`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('SetObjectTemperatureCallbackThreshold', 'set_object_temperature_callback_threshold'), 
'elements': [('option', 'char', 1, 'in'), 
             ('min', 'int16', 1, 'in'),
             ('max', 'int16', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the thresholds for the :func:`ObjectTemperatureReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'", "Callback is turned off."
 "'o'", "Callback is triggered when the temperature is *outside* the min and max values"
 "'i'", "Callback is triggered when the temperature is *inside* the min and max values"
 "'<'", "Callback is triggered when the temperature is smaller than the min value (max is ignored)"
 "'>'", "Callback is triggered when the temperature is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetObjectTemperatureCallbackThreshold', 'get_object_temperature_callback_threshold'), 
'elements': [('option', 'char', 1, 'out'), 
             ('min', 'int16', 1, 'out'),
             ('max', 'int16', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the threshold as set by :func:`SetAmbientTemperatureCallbackThreshold`.
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

 :func:`AmbientTemperatureReached`, :func:`ObjectTemperatureReached`

are triggered, if the thresholds

 :func:`SetAmbientTemperatureCallbackThreshold`, :func:`SetObjectTemperatureCallbackThreshold`

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
'name': ('AmbientTemperature', 'ambient_temperature'), 
'elements': [('temperature', 'int16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetAmbientTemperatureCallbackPeriod`. The parameter is the ambient 
temperature of the sensor.

:func:`AmbientTemperature` is only triggered if the ambient temperature
has changed since the last triggering.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'signal', 
'name': ('ObjectTemperature', 'object_temperature'), 
'elements': [('temperature', 'int16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetObjectTemperatureCallbackPeriod`. The parameter is the object 
temperature of the sensor.

:func:`AmbientTemperature` is only triggered if the object temperature
has changed since the last triggering.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'signal', 
'name': ('AmbientTemperatureReached', 'ambient_temperature_reached'), 
'elements': [('temperature', 'int16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetAmbientTemperatureCallbackThreshold` is reached.
The parameter is the ambient temperature of the sensor.

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
'name': ('ObjectTemperatureReached', 'object_temperature_reached'), 
'elements': [('temperature', 'int16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetObjectTemperatureCallbackThreshold` is reached.
The parameter is the object temperature of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
"""
}]
})
