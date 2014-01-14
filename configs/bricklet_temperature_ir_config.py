# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Temperature-IR Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 217,
    'name': ('TemperatureIR', 'temperature_ir', 'Temperature IR'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for non-contact temperature sensing',
    'released': True,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetAmbientTemperature', 'get_ambient_temperature'), 
'elements': [('temperature', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
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
Gibt die Umgebungstemperatur des Sensors zurück. Der Wertebereich ist von
-400 bis 1250 und wird in °C/10 angegeben, z.B. bedeutet 
ein Wert von 423 eine gemessene Umgebungstemperatur von 42,3 °C.

Wenn die Umgebungstemperatur periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`AmbientTemperature` zu nutzen und die Periode mit 
:func:`SetAmbientTemperatureCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetObjectTemperature', 'get_object_temperature'), 
'elements': [('temperature', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the object temperature of the sensor, i.e. the temperature
of the surface of the object the sensor is aimed at. The value
has a range of -700 to 3800 and is given in °C/10,
e.g. a value of 3001 means that a temperature of 300.1 °C is measured
on the surface of the object.

The temperature of different materials is dependent on their `emissivity 
<http://en.wikipedia.org/wiki/Emissivity>`__. The emissivity of the material
can be set with :func:`SetEmissivity`.

If you want to get the object temperature periodically, it is recommended 
to use the callback :func:`ObjectTemperature` and set the period with 
:func:`SetObjectTemperatureCallbackPeriod`.
""",
'de':
"""
Gibt die Objekttemperatur des Sensors zurück, z.B. die Temperatur
der Oberfläche auf welche der Sensor zielt. Der Wertebereich ist von
-700 bis 3800 und wird in °C/10 angegeben, z.B. bedeutet 
ein Wert von 3001 eine gemessene Temperatur von 300,1 °C auf der Oberfläche
des Objektes.

Die Temperatur von unterschiedlichen Materialien ist abhängig von ihrem `Emissionsgrad
<http://de.wikipedia.org/wiki/Emissionsgrad>`__. Der Emissionsgrad des Materials kann mit
:func:`SetEmissivity` gesetzt werden.

Wenn die Objekttemperatur periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`ObjectTemperature` zu nutzen und die Periode mit 
:func:`SetObjectTemperatureCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetEmissivity', 'set_emissivity'), 
'elements': [('emissivity', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the `emissivity <http://en.wikipedia.org/wiki/Emissivity>`__ that is
used to calculate the surface temperature as returned by 
:func:`GetObjectTemperature`. 

The emissivity is usually given as a value between 0.0 and 1.0. A list of
emissivities of different materials can be found 
`here <http://www.infrared-thermography.com/material.htm>`__.

The parameter of :func:`SetEmissivity` has to be given with a factor of
65535 (16-bit). For example: An emissivity of 0.1 can be set with the
value 6553, an emissivity of 0.5 with the value 32767 and so on.

.. note::
 If you need a precise measurement for the object temperature, it is
 absolutely crucial that you also provide a precise emissivity.

The default emissivity is 1.0 (value of 65535) and the minimum emissivity the
sensor can handle is 0.1 (value of 6553).
""",
'de':
"""
Setzt den `Emissionsgrad <http://de.wikipedia.org/wiki/Emissionsgrad>`__,
welcher zur Berechnung der Oberflächentemperatur benutzt wird, wie von
:func:`GetObjectTemperature` zurückgegeben.

Der Emissionsgrad wird normalerweise als Wert zwischen 0,0 und 1,0 angegeben.
Eine Liste von Emissionsgraden unterschiedlicher Materialien ist
`hier <http://www.infrared-thermography.com/material.htm>`__ zu finden.

Der Parameter von :func:`SetEmissivity` muss mit eine Faktor von 65535 (16-Bit)
vorgegeben werden. Beispiel: Ein Emissionsgrad von 0,1 kann mit dem Wert
6553 gesetzt werden, ein Emissionsgrad von 0,5 mit dem Wert 32767 und so weiter.

.. note::
 Wenn eine exakte Messung der Objekttemperatur notwendig ist, ist es entscheidend
 eine exakten Emissionsgrad anzugeben.
 
Der Standard Emissionsgrad ist 1,0 (Wert von 65535) und der minimale
Emissionsgrad welcher der Sensor verarbeiten kann ist 0,1 (Wert von 6553).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetEmissivity', 'get_emissivity'), 
'elements': [('emissivity', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the emissivity as set by :func:`SetEmissivity`.
""",
'de':
"""
Gibt den Emissionsgrad zurück, wie von :func:`SetEmissivity` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetAmbientTemperatureCallbackPeriod', 'set_ambient_temperature_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
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
Setzt die Periode in ms mit welcher der :func:`AmbientTemperature` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`AmbientTemperature` wird nur ausgelöst wenn sich die Temperatur seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAmbientTemperatureCallbackPeriod', 'get_ambient_temperature_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetAmbientTemperatureCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetAmbientTemperatureCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetObjectTemperatureCallbackPeriod', 'set_object_temperature_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
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
Setzt die Periode in ms mit welcher der :func:`ObjectTemperature` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`ObjectTemperature` wird nur ausgelöst wenn sich die Temperatur seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetObjectTemperatureCallbackPeriod', 'get_object_temperature_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetObjectTemperatureCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetObjectTemperatureCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetAmbientTemperatureCallbackThreshold', 'set_ambient_temperature_callback_threshold'), 
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
Sets the thresholds for the :func:`AmbientTemperatureReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the ambient temperature is *outside* the min and max values"
 "'i'",    "Callback is triggered when the ambient temperature is *inside* the min and max values"
 "'<'",    "Callback is triggered when the ambient temperature is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the ambient temperature is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`AmbientTemperatureReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Umgebungstemperatur *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn die Umgebungstemperatur *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn die Umgebungstemperatur kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Umgebungstemperatur größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAmbientTemperatureCallbackThreshold', 'get_ambient_temperature_callback_threshold'), 
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
Returns the threshold as set by :func:`SetAmbientTemperatureCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetAmbientTemperatureCallbackThreshold`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetObjectTemperatureCallbackThreshold', 'set_object_temperature_callback_threshold'), 
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
Sets the thresholds for the :func:`ObjectTemperatureReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the object temperature is *outside* the min and max values"
 "'i'",    "Callback is triggered when the object temperature is *inside* the min and max values"
 "'<'",    "Callback is triggered when the object temperature is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the object temperature is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`ObjectTemperatureReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Objekttemperatur *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn die Objekttemperatur *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn die Objekttemperatur kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Objekttemperatur größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetObjectTemperatureCallbackThreshold', 'get_object_temperature_callback_threshold'), 
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
Returns the threshold as set by :func:`SetObjectTemperatureCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetObjectTemperatureCallbackThreshold`
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
Sets the period in ms with which the threshold callbacks

* :func:`AmbientTemperatureReached`,
* :func:`ObjectTemperatureReached`

are triggered, if the thresholds

* :func:`SetAmbientTemperatureCallbackThreshold`,
* :func:`SetObjectTemperatureCallbackThreshold`

keep being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callbacks

* :func:`AmbientTemperatureReached`,
* :func:`ObjectTemperatureReached`
 
ausgelöst werden, wenn die Schwellwerte 

* :func:`SetAmbientTemperatureCallbackThreshold`,
* :func:`SetObjectTemperatureCallbackThreshold`
 
weiterhin erreicht bleiben.

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
'name': ('AmbientTemperature', 'ambient_temperature'), 
'elements': [('temperature', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetAmbientTemperatureCallbackPeriod`. The :word:`parameter` is the ambient
temperature of the sensor.

:func:`AmbientTemperature` is only triggered if the ambient temperature
has changed since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetAmbientTemperatureCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die Temperatur des Sensors.

:func:`AmbientTemperature` wird nur ausgelöst wenn sich die Temperatur seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('ObjectTemperature', 'object_temperature'), 
'elements': [('temperature', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetObjectTemperatureCallbackPeriod`. The :word:`parameter` is the object
temperature of the sensor.

:func:`ObjectTemperature` is only triggered if the object temperature
has changed since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetObjectTemperatureCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die Objekttemperatur des Sensors.

:func:`ObjectTemperature` wird nur ausgelöst wenn sich die Objekttemperatur seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('AmbientTemperatureReached', 'ambient_temperature_reached'), 
'elements': [('temperature', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetAmbientTemperatureCallbackThreshold` is reached.
The :word:`parameter` is the ambient temperature of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetAmbientTemperatureCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Umgebungstemperatur des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('ObjectTemperatureReached', 'object_temperature_reached'), 
'elements': [('temperature', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetObjectTemperatureCallbackThreshold` is reached.
The :word:`parameter` is the object temperature of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetObjectTemperatureCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Objekttemperatur des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})
