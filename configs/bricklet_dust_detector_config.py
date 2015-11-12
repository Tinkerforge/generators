# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Dust Detector Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 260,
    'name': ('DustDetector', 'dust_detector', 'Dust Detector', 'Dust Detector Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures dust density',
        'de': 'Misst Staubdichte'
    },
    'released': True,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': ('GetDustDensity', 'get_dust_density'), 
'elements': [('dust_density', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the dust density in µg/m³.

If you want to get the dust density periodically, it is recommended 
to use the callback :func:`DustDensity` and set the period with 
:func:`SetDustDensityCallbackPeriod`.
""",
'de':
"""
Gibt die Staubdichte in µg/m³ zurück.

Wenn die Staubdichte periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`DustDensity` zu nutzen und die Periode mit 
:func:`SetDustDensityCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetDustDensityCallbackPeriod', 'set_dust_density_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`DustDensity` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`DustDensity` is only triggered if the dust density has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`DustDensity` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`DustDensity` wird nur ausgelöst wenn sich die Staubdichte seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetDustDensityCallbackPeriod', 'get_dust_density_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetDustDensityCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetDustDensityCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetDustDensityCallbackThreshold', 'set_dust_density_callback_threshold'), 
'elements': [('option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('min', 'uint16', 1, 'in'),
             ('max', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`DustDensityReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the dust density value is *outside* the min and max values"
 "'i'",    "Callback is triggered when the dust density value is *inside* the min and max values"
 "'<'",    "Callback is triggered when the dust density value is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the dust density value is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`DustDensityReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Staubdichte *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn der Staubdichte *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn der Staubdichte kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn der Staubdichte größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetDustDensityCallbackThreshold', 'get_dust_density_callback_threshold'), 
'elements': [('option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('min', 'uint16', 1, 'out'),
             ('max', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`SetDustDensityCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetDustDensityCallbackThreshold`
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

* :func:`DustDensityReached`

is triggered, if the threshold

* :func:`SetDustDensityCallbackThreshold`

keeps being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callback

* :func:`DustDensityReached`
 
ausgelöst wird, wenn der Schwellwert 

* :func:`SetDustDensityCallbackThreshold`
 
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
'name': ('DustDensity', 'dust_density'), 
'elements': [('dust_density', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetDustDensityCallbackPeriod`. The :word:`parameter` is the 
dust density of the sensor.

:func:`DustDensity` is only triggered if the dust density value has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetDustDensityCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die Staubdichte des Sensors.

:func:`DustDensity` wird nur ausgelöst wenn sich die Staubdichte seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('DustDensityReached', 'dust_density_reached'), 
'elements': [('dust_density', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetDustDensityCallbackThreshold` is reached.
The :word:`parameter` is the dust density of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetDustDensityCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Staubdichte des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetMovingAverage', 'set_moving_average'), 
'elements': [('average', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
for the dust_density.

Setting the length to 0 will turn the averaging completely off. With less
averaging, there is more noise on the data.

The range for the averaging is 0-100.

The default value is 100.
""",
'de':
"""
Setzt die Länge eines gleitenden Mittelwerts für die Staubdichte.

Wenn die Länge auf 0 gesetzt wird, ist das Averaging komplett aus. Desto kleiner
die Länge des Mittelwerts ist, desto mehr Rauschen ist auf den Daten.

Der Wertebereich liegt bei 0-100.

Der Standardwert ist 100.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetMovingAverage', 'get_moving_average'), 
'elements': [('average', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the length moving average as set by :func:`SetMovingAverage`.
""",
'de':
"""
Gibt die Länge des gleitenden Mittelwerts zurück, wie von 
:func:`SetMovingAverage` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Dust Density', 'dust density'), [(('Dust Density', 'Dust Density'), 'uint16', None, 'µg/m³', 'µg/m³', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Dust Density', 'dust density'), [(('Dust Density', 'Dust Density'), 'uint16', None, 'µg/m³', 'µg/m³', None)], None, None),
              ('callback_period', ('Dust Density', 'dust density'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('Dust Density Reached', 'dust density reached'), [(('Dust Density', 'Dust Density'), 'uint16', None, 'µg/m³', 'µg/m³', None)], None, None),
              ('callback_threshold', ('Dust Density', 'dust density'), [], '>', [(10, 0)])]
})
