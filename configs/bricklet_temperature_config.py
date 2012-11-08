# -*- coding: utf-8 -*-

# Temperature Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [1, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 216,
    'name': ('Temperature', 'temperature', 'Temperature'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for sensing Temperature',
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetTemperature', 'get_temperature'), 
'elements': [('temperature', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the temperature of the sensor. The value
has a range of -2500 to 8500 and is given in °C/100,
e.g. a value of 4223 means that a temperature of 42.23 °C is measured.

If you want to get the temperature periodically, it is recommended 
to use the callback :func:`Temperature` and set the period with 
:func:`SetTemperatureCallbackPeriod`.
""",
'de':
"""
Gibt die Temperatur des Sensors zurück. Der Wertebereich ist von
-2500 bis 8500 und wird in °C/100 angegeben, z.B. bedeutet 
ein Wert von 4223 eine gemessene Temperatur von 42,23 °C.

Wenn die Temperatur periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`Temperature` zu nutzen und die Periode mit 
:func:`SetTemperatureCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetTemperatureCallbackPeriod', 'set_temperature_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Temperature` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Temperature` is only triggered if the temperature has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Temperature` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Temperature` wird nur ausgelöst wenn sich die Temperatur seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetTemperatureCallbackPeriod', 'get_temperature_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetTemperatureCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetTemperatureCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetTemperatureCallbackThreshold', 'set_temperature_callback_threshold'), 
'elements': [('option', 'char', 1, 'in'), 
             ('min', 'int16', 1, 'in'),
             ('max', 'int16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`TemperatureReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the temperature is *outside* the min and max values"
 "'i'",    "Callback is triggered when the temperature is *inside* the min and max values"
 "'<'",    "Callback is triggered when the temperature is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the temperature is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`TemperatureReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Temperatur *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn die Temperatur *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn die Temperatur kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Temperatur größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetTemperatureCallbackThreshold', 'get_temperature_callback_threshold'), 
'elements': [('option', 'char', 1, 'out'), 
             ('min', 'int16', 1, 'out'),
             ('max', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`SetTemperatureCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetTemperatureCallbackThreshold`
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

 :func:`TemperatureReached`

is triggered, if the threshold

 :func:`SetTemperatureCallbackThreshold`

keeps being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callback

 :func:`TemperatureReached`
 
ausgelöst wird, wenn der Schwellwert 

 :func:`SetTemperatureCallbackThreshold`
 
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
'name': ('Temperature', 'temperature'), 
'elements': [('temperature', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetTemperatureCallbackPeriod`. The :word:`parameter` is the temperature
of the sensor.

:func:`Temperature` is only triggered if the temperature has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetTemperatureCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die Temperatur des Sensors.

:func:`Temperature` wird nur ausgelöst wenn sich die Temperatur seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('TemperatureReached', 'temperature_reached'), 
'elements': [('temperature', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetTemperatureCallbackThreshold` is reached.
The :word:`parameter` is the temperature of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetTemperatureCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Temperatur des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})
