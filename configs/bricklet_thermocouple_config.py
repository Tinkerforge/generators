# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Thermocouple Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 266,
    'name': ('Thermocouple', 'thermocouple', 'Thermocouple', 'Thermocouple Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures temperature with thermocouples',
        'de': 'Misst Temperatur mit Thermoelementen'
    },
    'released': False,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': ('GetTemperature', 'get_temperature'), 
'elements': [('temperature', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
""",
'de':
"""
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
""",
'de':
"""
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
'elements': [('option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('min', 'int32', 1, 'in'),
             ('max', 'int32', 1, 'in')],
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
'elements': [('option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('min', 'int32', 1, 'out'),
             ('max', 'int32', 1, 'out')],
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

* :func:`TemperatureReached`

is triggered, if the threshold

* :func:`SetTemperatureCallbackThreshold`

keeps being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callback

* :func:`TemperatureReached`
 
ausgelöst wird, wenn der Schwellwert 

* :func:`SetTemperatureCallbackThreshold`
 
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
'elements': [('temperature', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetThermocoupleCallbackPeriod`. The :word:`parameter` is the temperature
of the thermocouple.

:func:`Temperature` is only triggered if the temperature has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetTemperatureCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die Temperatur des Thermoelements.

:func:`Temperature` wird nur ausgelöst wenn sich die Temperatur seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('TemperatureReached', 'temperature_reached'), 
'elements': [('temperature', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetTemperatureCallbackThreshold` is reached.
The :word:`parameter` is the temperature of the thermocouple.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetTemperatureCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Temperatur des Thermoelements.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetConfiguration', 'set_configuration'), 
'elements': [('averaging', 'uint8', 1, 'in', ('Averaging', 'averaging', [('1', '1', 1),
                                                                         ('2', '2', 2),
                                                                         ('4', '4', 4),
                                                                         ('8', '8', 8),
                                                                         ('16', '16', 16)])),
             ('thermocouple_type', 'uint8', 1, 'in', ('Type', 'type', [('B', 'b', 0),
                                                                       ('E', 'e', 1),
                                                                       ('J', 'j', 2),
                                                                       ('K', 'k', 3),
                                                                       ('N', 'n', 4),
                                                                       ('R', 'r', 5),
                                                                       ('S', 's', 6),
                                                                       ('T', 't', 7),
                                                                       ('G8', 'g8', 8),
                                                                       ('G32', 'g32', 9)])),
             ('filter', 'uint8', 1, 'in', ('FilterOption', 'filter_option', [('50Hz', '50hz', 0),
                                                                             ('60Hz', '60hz', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Conversion time in ms 60Hz: 82 + (samples-1)*16.67
                      50Hz: 98 + (samples-1)*20

G8:  Gain = 8,  value = 8  x 1.6 x 2^17 x V_in
G32: Gain = 32, value = 32 x 1.6 x 2^17 x V_in

where V_in = thermocouple input voltage

Default: 16, K, 50Hz
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetConfiguration', 'get_configuration'),
'elements': [('averaging', 'uint8', 1, 'out', ('Averaging', 'averaging', [('1', '1', 1),
                                                                          ('2', '2', 2),
                                                                          ('4', '4', 4),
                                                                          ('8', '8', 8),
                                                                          ('16', '16', 16)])),
             ('thermocouple_type', 'uint8', 1, 'out', ('Type', 'type', [('B', 'b', 0),
                                                                        ('E', 'e', 1),
                                                                        ('J', 'j', 2),
                                                                        ('K', 'k', 3),
                                                                        ('N', 'n', 4),
                                                                        ('R', 'r', 5),
                                                                        ('S', 's', 6),
                                                                        ('T', 't', 7),
                                                                        ('G8', 'g8', 8),
                                                                        ('G32', 'g32', 9)])),
             ('filter', 'uint8', 1, 'out', ('FilterOption', 'filter_option', [('50Hz', '50hz', 0),
                                                                              ('60Hz', '60hz', 1)]))],
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

com['packets'].append({
'type': 'function',
'name': ('GetErrorState', 'get_error_state'),
'elements': [('over_under', 'bool', 1, 'out'),
             ('open_circuit', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
* Returns current error state
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('ErrorState', 'error_state'), 
'elements': [('over_under', 'bool', 1, 'out'),
             ('open_circuit', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
* Called every time the error state changes
""",
'de':
"""
"""
}]
})

com['examples'].append({
'type': 'getter',
'name': 'Simple',
'values': [(('Temperature', 'temperature', 'Temperature'), 'int32', 100.0, '°C/100', '°C', None, [])]
})

com['examples'].append({
'type': 'callback',
'name': 'Callback',
'values': [(('Temperature', 'temperature', 'Temperature'), 'int32', 100.0, '°C/100', '°C', None, 1000)]
})

com['examples'].append({
'type': 'threshold',
'name': 'Threshold',
'values': [(('Temperature', 'temperature', 'Temperature'), 'int32', 100.0, '°C/100', '°C', 10000, '>', 30, 0, 'It is too hot, we need air conditioning!')]
})
