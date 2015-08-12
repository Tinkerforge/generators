# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Rotary Encoder Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 236,
    'name': ('RotaryEncoder', 'rotary_encoder', 'Rotary Encoder', 'Rotary Encoder Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '360° rotary encoder with push-button',
        'de': '360° Drehgeber/Drehencoder mit Taster'
    },
    'released': True,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': ('GetCount', 'get_count'), 
'elements': [('reset', 'bool', 1, 'in'),
             ('count', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current count of the encoder. If you set reset
to true, the count is set back to 0 directly after the
current count is read.

The encoder has 24 steps per rotation

Turning the encoder to the left decrements the counter,
so a negative count is possible.
""",
'de':
"""
Gibt den aktuellen Zählerwert des Encoders zurück. Wenn
reset auf true gesetzt wird, wird der Zählerstand
direkt nach dem auslesen auf 0 zurück gesetzt.

Der Encoder hat 24 Schritte pro Umdrehung.

Wenn der Encoder nach links gedreht wird wird der Zählerwert
dekrementiert, d.h. negative Zählerwerte sind möglich.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetCountCallbackPeriod', 'set_count_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Count` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Count` is only triggered if the count has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Count` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Count` wird nur ausgelöst wenn sich der Zählerwert seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetCountCallbackPeriod', 'get_count_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetCountCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetCountCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetCountCallbackThreshold', 'set_count_callback_threshold'), 
'elements': [('option', 'char', 1, 'in', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                  ('Outside', 'outside', 'o'),
                                                                                  ('Inside', 'inside', 'i'),
                                                                                  ('Smaller', 'smaller', '<'),
                                                                                  ('Greater', 'greater', '>')])), 
             ('min', 'int32', 1, 'in'),
             ('max', 'int32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`CountReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the count is *outside* the min and max values"
 "'i'",    "Callback is triggered when the count is *inside* the min and max values"
 "'<'",    "Callback is triggered when the count is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the count is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`CountReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn der Zählerwert *außerhalb* der min und max Werte ist"
 "'i'",    "Callback wird ausgelöst wenn die Zählerwert *innerhalb* der min und max Werte ist"
 "'<'",    "Callback wird ausgelöst wenn die Zählerwert kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Zählerwert größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetCountCallbackThreshold', 'get_count_callback_threshold'), 
'elements': [('option', 'char', 1, 'out', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                   ('Outside', 'outside', 'o'),
                                                                                   ('Inside', 'inside', 'i'),
                                                                                   ('Smaller', 'smaller', '<'),
                                                                                   ('Greater', 'greater', '>')])), 
             ('min', 'int32', 1, 'out'),
             ('max', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`SetCountCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetCountCallbackThreshold`
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

* :func:`CountReached`

is triggered, if the thresholds

* :func:`SetCountCallbackThreshold`

keeps being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher der Schwellwert-Callback

* :func:`CountReached`
 
ausgelöst wird, wenn der Schwellwert 

* :func:`SetCountCallbackThreshold`
 
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
'name': ('Count', 'count'), 
'elements': [('count', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetCountCallbackPeriod`. The :word:`parameter` is the count of
the encoder.

:func:`Count` is only triggered if the count has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetCountCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist der Zählerwert des Encoders.

:func:`Count` wird nur ausgelöst wenn sich der Zähler seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('CountReached', 'count_reached'), 
'elements': [('count', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetCountCallbackThreshold` is reached.
The :word:`parameter` is the count of the encoder.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetCountCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist der Zählerwert des Encoders.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('IsPressed', 'is_pressed'), 
'elements': [('pressed', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns *true* if the button is pressed and *false* otherwise.

It is recommended to use the :func:`Pressed` and :func:`Released` callbacks
to handle the button.
""",
'de':
"""
Gibt *true* zurück wenn der Taster gedrückt ist und sonst *false*.

Es wird empfohlen die :func:`Pressed` und :func:`Released` Callbacks
zu nutzen, um den Taster programmatisch zu behandeln.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('Pressed', 'pressed'), 
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the button is pressed.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Taster gedrückt wird.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('Released', 'released'), 
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the button is released.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Taster losgelassen wird.
"""
}]
})

com['examples'].append({
'type': 'getter',
'name': 'Simple',
'values': [(('Count', 'count without reset', 'Count'), 'int32', None, None, None, None, [('bool', False)])]
})

com['examples'].append({
'type': 'callback',
'name': 'Callback',
'values': [(('Count', 'count', 'Count'), 'int32', None, None, None, None, 50)]
})
