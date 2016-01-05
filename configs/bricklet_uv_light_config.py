# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# UV Light Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 265,
    'name': ('UV Light', 'UV Light', 'UV Light Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures UV Light',
        'de': 'Misst UV Light'
    },
    'released': False,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Get UV Light',
'elements': [('UV Light', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the UV Light intensity of the sensor, the intensity is given 
in µW/cm².

To get UV Index you have to divide the value by 250. For example, a UV Light
intensity of 500µW/cm² is equivalent to an UV Index of 2.

If you want to get the intensity periodically, it is recommended to use the
callback :func:`UVLight` and set the period with 
:func:`SetUVLightCallbackPeriod`.
""",
'de':
"""
Gibt die UV-Licht-Intensität des Sensors zurück. Die Intensität wird
in der Einheit µW/cm² gegeben.

Die Intensität kann einfach durch 250 geteilt werden um den UV Index zu
bestimmen. Beispiel: Eine UV-Lich-Intensität von 500µW/cm² entspricht
einem UV Index von 2.

Wenn die Intensität periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`UVLight` zu nutzen und die Periode mit 
:func:`SetUVLightCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set UV Light Callback Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`UVLight` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`UVLight` is only triggered if the intensity has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`UVLight` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`UVLight` wird nur ausgelöst wenn sich die Intensität seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get UV Light Callback Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetUVLightCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetUVLightCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set UV Light Callback Threshold', 
'elements': [('Option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint32', 1, 'in'),
             ('Max', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`UVLightReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the intensity is *outside* the min and max values"
 "'i'",    "Callback is triggered when the intensity is *inside* the min and max values"
 "'<'",    "Callback is triggered when the intensity is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the intensity is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`UVLightReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Intensität *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn die Intensität *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn die Intensität kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn dieIntensität  größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get UV Light Callback Threshold',
'elements': [('Option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint32', 1, 'out'),
             ('Max', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`SetUVLightCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetUVLightCallbackThreshold`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Debounce Period',
'elements': [('Debounce', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the threshold callbacks

* :func:`UVLightReached`,

are triggered, if the thresholds

* :func:`SetUVLightCallbackThreshold`,

keep being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callbacks

* :func:`UVLightReached`,
 
ausgelöst werden, wenn die Schwellwerte 

* :func:`SetUVLightCallbackThreshold`,
 
weiterhin erreicht bleiben.

Der Standardwert ist 100.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Debounce Period',
'elements': [('Debounce', 'uint32', 1, 'out')],
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
'name': 'UV Light',
'elements': [('UV Light', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetUVLightCallbackPeriod`. The :word:`parameter` is the UV Light 
intensity of the sensor.

:func:`UVLight` is only triggered if the intensity has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetUVLightCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die UV-Licht-Intensität des Sensors.

:func:`UVLight` wird nur ausgelöst wenn sich die Intensität seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'UV Light Reached',
'elements': [('UV Light', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetUVLightCallbackThreshold` is reached.
The :word:`parameter` is the UV Light intensity of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetUVLightCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die UV-Licht-Intensität des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get UV Light', 'UV light'), [(('UV Light', 'UV Light'), 'uint32', None, 'µW/cm²', 'µW/cm²', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('UV Light', 'UV light'), [(('UV Light', 'UV Light'), 'uint32', None, 'µW/cm²', 'µW/cm²', None)], None, None),
              ('callback_period', ('UV Light', 'UV light'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('UV Light Reached', 'UV light reached'), [(('UV Light', 'UV Light'), 'uint32', None, 'µW/cm²', 'µW/cm²', None)], None, 'UV Index > 3. Use sunscreen!'),
              ('callback_threshold', ('UV Light', 'UV light'), [], '>', [(250*3, 0)])]
})
