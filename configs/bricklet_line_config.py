# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Line Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 241,
    'name': ('Line', 'Line', 'Line Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures reflectivity of a surface',
        'de': 'Misst Reflektivität einer Oberfläche'
    },
    'released': True,
    'documented': True,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Get Reflectivity',
'elements': [('Reflectivity', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the currently measured reflectivity. The reflectivity is
a value between 0 (not reflective) and 4095 (very reflective).

Usually black has a low reflectivity while white has a high
reflectivity.

If you want to get the reflectivity periodically, it is recommended 
to use the callback :func:`Reflectivity` and set the period with 
:func:`SetReflectivityCallbackPeriod`.
""",
'de':
"""
Gibt die aktuell gemessene Reflektivität zurück. Die Reflektivität
ist ein Wert zwischen 0 (nicht reflektiv) und 4095 (sehr reflektiv).

Normalerweise hat schwarz eine geringe Reflektivität während
weiß eine hohe Reflektivität hat.

Wenn die Reflektivität periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`Reflectivity` zu nutzen und die Periode mit 
:func:`SetReflectivityCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Reflectivity Callback Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Reflectivity` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Reflectivity` is only triggered if the reflectivity has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Reflectivity` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Reflectivity` wird nur ausgelöst wenn sich die Reflektivität seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Reflectivity Callback Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetReflectivityCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetReflectivityCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Reflectivity Callback Threshold',
'elements': [('Option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint16', 1, 'in'),
             ('Max', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`ReflectivityReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the reflectivity is *outside* the min and max values"
 "'i'",    "Callback is triggered when the reflectivity is *inside* the min and max values"
 "'<'",    "Callback is triggered when the reflectivity is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the reflectivity is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`ReflectivityReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Reflektivität *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn die Reflektivität *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn die Reflektivität kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Reflektivität größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Reflectivity Callback Threshold',
'elements': [('Option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint16', 1, 'out'),
             ('Max', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`SetReflectivityCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetReflectivityCallbackThreshold`
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
Sets the period in ms with which the threshold callback

* :func:`ReflectivityReached`

is triggered, if the threshold

* :func:`SetReflectivityCallbackThreshold`

keeps being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callback

* :func:`ReflectivityReached`
 
ausgelöst wird, wenn der Schwellwert 

* :func:`SetReflectivityCallbackThreshold`
 
weiterhin erreicht bleibt.

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
'name': 'Reflectivity',
'elements': [('Reflectivity', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetReflectivityCallbackPeriod`. The :word:`parameter` is the reflectivity
of the sensor.

:func:`Reflectivity` is only triggered if the reflectivity has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetReflectivityCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die Reflektivität des Sensors.

:func:`Reflectivity` wird nur ausgelöst wenn sich die Reflektivität seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Reflectivity Reached',
'elements': [('Reflectivity', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetReflectivityCallbackThreshold` is reached.
The :word:`parameter` is the reflectivity of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetReflectivityCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Reflektivität des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Reflectivity', 'reflectivity'), [(('Reflectivity', 'Reflectivity'), 'uint16', None, None, None, None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Reflectivity', 'reflectivity'), [(('Reflectivity', 'Reflectivity'), 'uint16', None, None, None, None)], None, None),
              ('callback_period', ('Reflectivity', 'reflectivity'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 1000),
              ('callback', ('Reflectivity Reached', 'reflectivity reached'), [(('Reflectivity', 'Reflectivity'), 'uint16', None, None, None, None)], None, None),
              ('callback_threshold', ('Reflectivity', 'reflectivity'), [], '>', [(2000, 0)])]
})
