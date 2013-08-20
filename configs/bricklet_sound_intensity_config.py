# -*- coding: utf-8 -*-

# Sound Intensity Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 238,
    'name': ('SoundIntensity', 'sound_intensity', 'Sound Intensity'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for sensing sound intensity',
    'released': False,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetIntensity', 'get_intensity'), 
'elements': [('intensity', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetIntensityCallbackPeriod', 'set_intensity_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Intensity` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Intensity` is only triggered if the intensity has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Intensity` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Intensity` wird nur ausgelöst wenn sich die Intensität seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetIntensityCallbackPeriod', 'get_intensity_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetIntensityCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetIntensityCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetIntensityCallbackThreshold', 'set_intensity_callback_threshold'), 
'elements': [('option', 'char', 1, 'in', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                  ('Outside', 'outside', 'o'),
                                                                                  ('Inside', 'inside', 'i'),
                                                                                  ('Smaller', 'smaller', '<'),
                                                                                  ('Greater', 'greater', '>')])), 
             ('min', 'uint16', 1, 'in'),
             ('max', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`IntensityReached` callback. 

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
Setzt den Schwellwert für den :func:`IntensityReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Intensität *außerhalb* der min und max Werte ist"
 "'i'",    "Callback wird ausgelöst wenn die Intensität *innerhalb* der min und max Werte ist"
 "'<'",    "Callback wird ausgelöst wenn die Intensität kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Intensität größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetIntensityCallbackThreshold', 'get_intensity_callback_threshold'), 
'elements': [('option', 'char', 1, 'out', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                   ('Outside', 'outside', 'o'),
                                                                                   ('Inside', 'inside', 'i'),
                                                                                   ('Smaller', 'smaller', '<'),
                                                                                   ('Greater', 'greater', '>')])), 
             ('min', 'uint16', 1, 'out'),
             ('max', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`SetIntensityCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetIntensityCallbackThreshold`
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

* :func:`IntensityReached`

is triggered, if the thresholds

* :func:`SetIntensityCallbackThreshold`

keeps being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher der Schwellwert-Callback

* :func:`IntensityReached`
 
ausgelöst wird, wenn der Schwellwert 

* :func:`SetIntensityCallbackThreshold`
 
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
'name': ('Intensity', 'intensity'), 
'elements': [('intensity', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetIntensityCallbackPeriod`. The :word:`parameter` is the intensity of
the encoder.

:func:`Intensity` is only triggered if the intensity has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetIntensityCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist gemessene Schallintensität.

:func:`Intensity` wird nur ausgelöst wenn sich die Intensität seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('IntensityReached', 'intensity_reached'), 
'elements': [('intensity', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetIntensityCallbackThreshold` is reached.
The :word:`parameter` is the intensity of the encoder.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetIntensityCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die gemessene Schallintensität.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

