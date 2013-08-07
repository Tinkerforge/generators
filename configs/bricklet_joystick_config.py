# -*- coding: utf-8 -*-

# Joystick Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 210,
    'name': ('Joystick', 'joystick', 'Joystick'),
    'manufacturer': 'Tinkerforge',
    'description': 'Dual-Axis Joystick with Button',
    'released': True,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetPosition', 'get_position'), 
'elements': [('x', 'int16', 1, 'out'),
             ('y', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the position of the Joystick. The value ranges between -100 and
100 for both axis. The middle position of the joystick is x=0, y=0. The
returned values are averaged and calibrated (see :func:`Calibrate`).

If you want to get the position periodically, it is recommended to use the
callback :func:`Position` and set the period with 
:func:`SetPositionCallbackPeriod`.
""",
'de':
"""
Gibt die Position des Joystick zurück. Der Wertebereich ist von -100 bis
100 für beide Achsen. Die Mittelposition des Joysticks ist x=0, y=0.
Die zurückgegebenen Werte sind gemittelt und kalibriert (siehe :func:`Calibrate`).

Wenn die Position periodisch abgefragt werden sollen, wird empfohlen
den Callback :func:`Position` zu nutzen und die Periode mit 
:func:`SetPositionCallbackPeriod` vorzugeben.
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
Gibt *true* zurück wenn die Taste gedrückt ist und sonst *false*.

Es wird empfohlen die :func:`Pressed` und :func:`Released` Callbacks
zu nutzen, um die Taste programmatisch zu behandeln.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAnalogValue', 'get_analog_value'), 
'elements': [('x', 'uint16', 1, 'out'),
             ('y', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the values as read by a 12-bit analog-to-digital converter.
The values are between 0 and 4095 for both axis.

.. note::
 The values returned by :func:`GetPosition` are averaged over several samples
 to yield less noise, while :func:`GetAnalogValue` gives back raw
 unfiltered analog values. The only reason to use :func:`GetAnalogValue` is,
 if you need the full resolution of the analog-to-digital converter.

If you want the analog values periodically, it is recommended to use the 
callback :func:`AnalogValue` and set the period with 
:func:`SetAnalogValueCallbackPeriod`.
""",
'de':
"""
Gibt den Wert, wie vom 12-Bit Analog-Digital-Wandler gelesen, zurück. Der
Wertebereich ist 0 bis 4095.

.. note::
 Der von :func:`GetPosition` zurückgegebene Wert ist über mehrere
 Messwerte gemittelt um das Rauschen zu vermindern, während :func:`GetAnalogValue`
 unverarbeitete Analogwerte zurück gibt. Der einzige Grund :func:`GetAnalogValue`
 zu nutzen, ist die volle Auflösung des Analog-Digital-Wandlers zu erhalten.
 
Wenn die Analogwerte periodisch abgefragt werden sollen, wird empfohlen
den Callback :func:`AnalogValue` zu nutzen und die Periode mit 
:func:`SetAnalogValueCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('Calibrate', 'calibrate'), 
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Calibrates the middle position of the Joystick. If your Joystick Bricklet
does not return x=0 and y=0 in the middle position, call this function
while the Joystick is standing still in the middle position.

The resulting calibration will be saved on the EEPROM of the Joystick
Bricklet, thus you only have to calibrate it once.
""",
'de':
"""
Kalibriert die Mittelposition des Joysticks. Sollte der Joystick Bricklet
nicht x=0 und y=0 in der Mittelposition zurückgeben, kann diese Funktion
aufgerufen werden wenn der Joystick sich unbewegt in der Mittelposition befindet.

Die resultierende Kalibrierung wird in den EEPROM des Joystick Bricklet gespeichert,
somit ist die Kalibrierung nur einmalig notwendig.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetPositionCallbackPeriod', 'set_position_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
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
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
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
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`AnalogValue` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`AnalogValue` is only triggered if the analog values have changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`AnalogValue` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`AnalogValue` wird nur ausgelöst wenn sich die Analogwerte seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAnalogValueCallbackPeriod', 'get_analog_value_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
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
'elements': [('option', 'char', 1, 'in', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                  ('Outside', 'outside', 'o'),
                                                                                  ('Inside', 'inside', 'i'),
                                                                                  ('Smaller', 'smaller', '<'),
                                                                                  ('Greater', 'greater', '>')])), 
             ('min_x', 'int16', 1, 'in'),
             ('max_x', 'int16', 1, 'in'),
             ('min_y', 'int16', 1, 'in'),
             ('max_y', 'int16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`PositionReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the position is *outside* the min and max values"
 "'i'",    "Callback is triggered when the position is *inside* the min and max values"
 "'<'",    "Callback is triggered when the position is smaller than the min values (max is ignored)"
 "'>'",    "Callback is triggered when the position is greater than the min values (max is ignored)"

The default value is ('x', 0, 0, 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`PositionReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Position *außerhalb* der min und max Werte ist"
 "'i'",    "Callback wird ausgelöst wenn die Position *innerhalb* der min und max Werte ist"
 "'<'",    "Callback wird ausgelöst wenn die Position kleiner als die min Werte ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Position größer als die min Werte ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0, 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetPositionCallbackThreshold', 'get_position_callback_threshold'), 
'elements': [('option', 'char', 1, 'out', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                   ('Outside', 'outside', 'o'),
                                                                                   ('Inside', 'inside', 'i'),
                                                                                   ('Smaller', 'smaller', '<'),
                                                                                   ('Greater', 'greater', '>')])), 
             ('min_x', 'int16', 1, 'out'),
             ('max_x', 'int16', 1, 'out'),
             ('min_y', 'int16', 1, 'out'),
             ('max_y', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
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
'elements': [('option', 'char', 1, 'in', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                  ('Outside', 'outside', 'o'),
                                                                                  ('Inside', 'inside', 'i'),
                                                                                  ('Smaller', 'smaller', '<'),
                                                                                  ('Greater', 'greater', '>')])), 
             ('min_x', 'uint16', 1, 'in'),
             ('max_x', 'uint16', 1, 'in'),
             ('min_y', 'uint16', 1, 'in'),
             ('max_y', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`AnalogValueReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the analog values are *outside* the min and max values"
 "'i'",    "Callback is triggered when the analog values are *inside* the min and max values"
 "'<'",    "Callback is triggered when the analog values are smaller than the min values (max is ignored)"
 "'>'",    "Callback is triggered when the analog values are greater than the min values (max is ignored)"

The default value is ('x', 0, 0, 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`AnalogValueReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Analogwerte *außerhalb* der min und max Werte ist"
 "'i'",    "Callback wird ausgelöst wenn die Analogwerte *innerhalb* der min und max Werte ist"
 "'<'",    "Callback wird ausgelöst wenn die Analogwerte kleiner als die min Werte ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Analogwerte größer als die min Werte ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0, 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAnalogValueCallbackThreshold', 'get_analog_value_callback_threshold'), 
'elements': [('option', 'char', 1, 'out', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                   ('Outside', 'outside', 'o'),
                                                                                   ('Inside', 'inside', 'i'),
                                                                                   ('Smaller', 'smaller', '<'),
                                                                                   ('Greater', 'greater', '>')])), 
             ('min_x', 'uint16', 1, 'out'),
             ('max_x', 'uint16', 1, 'out'),
             ('min_y', 'uint16', 1, 'out'),
             ('max_y', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
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
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the threshold callbacks

* :func:`PositionReached`,
* :func:`AnalogValueReached`

are triggered, if the thresholds

* :func:`SetPositionCallbackThreshold`,
* :func:`SetAnalogValueCallbackThreshold`

keep being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callbacks

* :func:`PositionReached`,
* :func:`AnalogValueReached`
 
ausgelöst werden, wenn die Schwellwerte 

* :func:`SetPositionCallbackThreshold`,
* :func:`SetAnalogValueCallbackThreshold`
 
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
'name': ('Position', 'position'), 
'elements': [('x', 'int16', 1, 'out'),
             ('y', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetPositionCallbackPeriod`. The :word:`parameter` is the position of the
Joystick.

:func:`Position` is only triggered if the position has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetPositionCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die Position des Joysticks.

:func:`Position` wird nur ausgelöst wenn sich der Strom seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('AnalogValue', 'analog_value'), 
'elements': [('x', 'uint16', 1, 'out'),
             ('y', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetAnalogValueCallbackPeriod`. The :word:`parameters` are the analog values
of the Joystick.

:func:`AnalogValue` is only triggered if the values have changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetAnalogValueCallbackPeriod`,
ausgelöst. Der :word:`parameter` sind die Analogwerte des Joysticks.

:func:`AnalogValue` wird nur ausgelöst wenn sich die Analogwerte seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('PositionReached', 'position_reached'), 
'elements': [('x', 'int16', 1, 'out'),
             ('y', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetPositionCallbackThreshold` is reached.
The :word:`parameters` are the position of the Joystick.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetPositionCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Position des Joysticks.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('AnalogValueReached', 'analog_value_reached'), 
'elements': [('x', 'uint16', 1, 'out'),
             ('y', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetAnalogValueCallbackThreshold` is reached.
The :word:`parameters` are the analog values of the Joystick.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetAnalogValueCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` sind die Analogwerte des Joystick.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
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
Dieser Callback wird ausgelöst wenn die Taste gedrückt wird.
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
Dieser Callback wird ausgelöst wenn die Taste losgelassen wird.
"""
}]
})
