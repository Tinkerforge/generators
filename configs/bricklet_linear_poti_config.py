# -*- coding: utf-8 -*-

# Linear Poti Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'version': [1, 0, 0],
    'category': 'Bricklet',
    'name': ('LinearPoti', 'linear_poti', 'Linear Poti'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for sensing Linear Potentiometer input',
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetPosition', 'get_position'), 
'elements': [('position', 'uint16', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns the position of the Linear Potentiometer. The value is  
between 0 (slider down) and 100 (slider up).

If you want to get the position periodically, it is recommended to use the
callback :func:`Position` and set the period with 
:func:`SetPositionCallbackPeriod`.
""",
'de':
"""
Gibt die Position des Linearpotentionmeters zurück. Der Wertebereich
ist von 0 (Schieberegler unten) und 100 (Schieberegler oben).

Wenn die Position periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`Position` zu nutzen und die Periode mit 
:func:`SetPositionCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAnalogValue', 'get_analog_value'), 
'elements': [('value', 'uint16', 1, 'out')],
'doc': ['am', {
'en':
"""
Returns the value as read by a 12 bit analog to digital converter.
The value is between 0 and 4095.

.. note::
 The value returned by :func:`GetPosition` is averaged over several samples
 to yield less noise, while :func:`GetAnalogValue` gives back raw
 unfiltered analog values. The only reason to use :func:`GetAnalogValue` is,
 if you need the full resolution of the analog to digital converter.

If you want the analog value periodically, it is recommended to use the 
callback :func:`AnalogValue` and set the period with 
:func:`SetAnalogValueCallbackPeriod`.
""",
'de':
"""
Gibt den Wert, wie vom 12 bit Analog-Digital-Wandler gelesen, zurück. Der 
Wertebereich ist 0 bis 4095.

.. note::
 Der von :func:`GetPosition` zurückgegebene Wert ist über mehrere
 Messwerte gemittelt um das Rauschen zu vermindern, während :func:`GetAnalogValue`
 unverarbeitete Analogwerte zurückgibt. Der einzige Grund :func:`GetAnalogValue`
 zu nutzen, ist die volle Auflösung des Analog-Digital-Wandlers zu erhalten.
 
Wenn der Analogwert periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`AnalogValue` zu nutzen und die Periode mit 
:func:`SetAnalogValueCallbackPeriod` vorzugeben.
"""
}]
})


com['packets'].append({
'type': 'function',
'name': ('SetPositionCallbackPeriod', 'set_position_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the period in ms with which the :func:`Position` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Position` is only triggered if the position has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Position` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Position` wird nur ausgelöst wenn sich die Position seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetPositionCallbackPeriod', 'get_position_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the period as set by :func:`SetPositionCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetPositionCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetAnalogValueCallbackPeriod', 'set_analog_value_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the period in ms with which the :func:`AnalogValue` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`AnalogValue` is only triggered if the analog value has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`AnalogValue` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`AnalogValue` wird nur ausgelöst wenn sich der Analogwert seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAnalogValueCallbackPeriod', 'get_analog_value_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the period as set by :func:`SetAnalogValueCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetAnalogValueCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetPositionCallbackThreshold', 'set_position_callback_threshold'), 
'elements': [('option', 'char', 1, 'in'), 
             ('min', 'int16', 1, 'in'),
             ('max', 'int16', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the thresholds for the :func:`PositionReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off."
 "'o'",    "Callback is triggered when the position is *outside* the min and max values"
 "'i'",    "Callback is triggered when the position is *inside* the min and max values"
 "'<'",    "Callback is triggered when the position is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the position is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`PositionReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Position *ausserhalb* der min und max Werte ist"
 "'i'",    "Callback wird ausgelöst wenn die Position *innerhalb* der min und max Werte ist"
 "'<'",    "Callback wird ausgelöst wenn die Position kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Position größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetPositionCallbackThreshold', 'get_position_callback_threshold'), 
'elements': [('option', 'char', 1, 'out'), 
             ('min', 'int16', 1, 'out'),
             ('max', 'int16', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the threshold as set by :func:`SetPositionCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetPositionCallbackThreshold`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetAnalogValueCallbackThreshold', 'set_analog_value_callback_threshold'), 
'elements': [('option', 'char', 1, 'in'), 
             ('min', 'uint16', 1, 'in'),
             ('max', 'uint16', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the thresholds for the :func:`AnalogValueReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off."
 "'o'",    "Callback is triggered when the analog value is *outside* the min and max values"
 "'i'",    "Callback is triggered when the analog value is *inside* the min and max values"
 "'<'",    "Callback is triggered when the analog value is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the analog value is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`AnalogValueReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn der Analogwert *ausserhalb* der min und max Werte ist"
 "'i'",    "Callback wird ausgelöst wenn der Analogwert *innerhalb* der min und max Werte ist"
 "'<'",    "Callback wird ausgelöst wenn der Analogwert kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn der Analogwert größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAnalogValueCallbackThreshold', 'get_analog_value_callback_threshold'), 
'elements': [('option', 'char', 1, 'out'), 
             ('min', 'uint16', 1, 'out'),
             ('max', 'uint16', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the threshold as set by :func:`SetAnalogValueCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetAnalogValueCallbackThreshold`
gesetzt.
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

 :func:`PositionReached`, :func:`AnalogValueReached`

are triggered, if the thresholds

 :func:`SetPositionCallbackThreshold`, :func:`SetAnalogValueCallbackThreshold`

keep being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callbacks

 :func:`PositionReached`, :func:`AnalogValueReached`
 
ausgelöst werden, wenn die Schwellwerte 

 :func:`SetPositionCallbackThreshold`, :func:`SetAnalogValueCallbackThreshold`
 
weiterhin erreicht bleiben.

Der Standardwert ist 100.
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
Gibt die Entprellperiode zurück, wie von :func:`SetDebouncePeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('Position', 'position'), 
'elements': [('position', 'uint16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetPositionCallbackPeriod`. The :word:`parameter` is the position of the
Linear Potentiometer.

:func:`Position` is only triggered if the position has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetPositionCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die Position des Linearpotentiometers.

:func:`Position` wird nur ausgelöst wenn sich die Position seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('AnalogValue', 'analog_value'), 
'elements': [('value', 'uint16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetAnalogValueCallbackPeriod`. The :word:`parameter` is the analog value of the
Linear Potentiometer.

:func:`AnalogValue` is only triggered if the position has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetAnalogValueCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist der Analogwert des Linearpotentiometers.

:func:`AnalogValue` wird nur ausgelöst wenn sich der Analogwert seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('PositionReached', 'position_reached'), 
'elements': [('position', 'uint16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetPositionCallbackThreshold` is reached.
The :word:`parameter` is the position of the Linear Potentiometer.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetPositionCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Position des Linearpotentionmeters.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('AnalogValueReached', 'analog_value_reached'), 
'elements': [('value', 'uint16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetAnalogValueCallbackThreshold` is reached.
The :word:`parameter` is the analog value of the Linear Potentiometer.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetAnalogValueCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist der Analogwert des Linearpotentiometers.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})
