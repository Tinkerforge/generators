# -*- coding: utf-8 -*-

# Current12 Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 23,
    'name': ('Current12', 'current12', 'Current12'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for sensing current of up to 12.5A',
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetCurrent', 'get_current'), 
'elements': [('current', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current of the sensor. The value is in mA
and between -12500mA and 12500mA.

If you want to get the current periodically, it is recommended to use the
callback :func:`Current` and set the period with 
:func:`SetCurrentCallbackPeriod`.
""",
'de':
"""
Gibt die gemessenen Stromstärke des Sensors zurück. Der Wert ist in mA und im
Bereich von -12500mA bis 12500mA.

Wenn die Stromstärke periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`Current` zu nutzen und die Periode mit 
:func:`SetCurrentCallbackPeriod` vorzugeben.
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
Calibrates the 0 value of the sensor. You have to call this function
when there is no current present. 

The zero point of the current sensor
is depending on the exact properties of the analog-to-digital converter,
the length of the Bricklet cable and the temperature. Thus, if you change
the Brick or the environment in which the Bricklet is used, you might
have to recalibrate.

The resulting calibration will be saved on the EEPROM of the Current
Bricklet.
""",
'de':
"""
Kalibriert den Nullwert des Sensors. Diese Funktion muss aufgerufen werden, 
wenn kein Strom fließt.

Der Nullwert des Stromsensors ist abhängig von den exakten Eigenschaften des
Analog-Digital-Wandlers, der Länge des Brickletkabels und der Temperatur. Daher ist es,
bei Wechsel des Brick oder bei Veränderung der Umgebung in welcher das Bricklet genutzt wird,
ratsam erneut zu kalibrieren.

Die resultierende Kalibrierung wird in den EEPROM des Current Bricklet gespeichert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('IsOverCurrent', 'is_over_current'), 
'elements': [('over', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns *true* if more than 12.5A were measured.

.. note::
 To reset this value you have to power cycle the Bricklet.
""",
'de':
"""
Gibt *true* zurück wenn mehr als 12,5A gemessen wurden.

.. note::
 Um diesen Wert zurückzusetzen ist ein Aus- und Wiedereinschalten des Bricklet
 notwendig.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAnalogValue', 'get_analog_value'), 
'elements': [('value', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the value as read by a 12-bit analog-to-digital converter.
The value is between 0 and 4095.

.. note::
 The value returned by :func:`GetCurrent` is averaged over several samples
 to yield less noise, while :func:`GetAnalogValue` gives back raw
 unfiltered analog values. The only reason to use :func:`GetAnalogValue` is,
 if you need the full resolution of the analog-to-digital converter.

If you want the analog value periodically, it is recommended to use the 
callback :func:`AnalogValue` and set the period with 
:func:`SetAnalogValueCallbackPeriod`.
""",
'de':
"""
Gibt den Wert, wie vom 12-Bit Analog-Digital-Wandler gelesen, zurück. Der
Wertebereich ist 0 bis 4095.

.. note::
 Der von :func:`GetCurrent` zurückgegebene Wert ist über mehrere
 Messwerte gemittelt um das Rauschen zu vermindern, während :func:`GetAnalogValue`
 unverarbeitete Analogwerte zurück gibt. Der einzige Grund :func:`GetAnalogValue`
 zu nutzen, ist die volle Auflösung des Analog-Digital-Wandlers zu erhalten.
 
Wenn der Analogwert periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`AnalogValue` zu nutzen und die Periode mit 
:func:`SetAnalogValueCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetCurrentCallbackPeriod', 'set_current_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Current` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Current` is only triggered if the current has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Current` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Current` wird nur ausgelöst wenn sich die Stromstärke seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0. 
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetCurrentCallbackPeriod', 'get_current_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetCurrentCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetCurrentCallbackPeriod`
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
'name': ('SetCurrentCallbackThreshold', 'set_current_callback_threshold'), 
'elements': [('option', 'char', 1, 'in'), 
             ('min', 'int16', 1, 'in'),
             ('max', 'int16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`CurrentReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the current is *outside* the min and max values"
 "'i'",    "Callback is triggered when the current is *inside* the min and max values"
 "'<'",    "Callback is triggered when the current is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the current is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`CurrentReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Stromstärke *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn die Stromstärke *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn die Stromstärke kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Stromstärke größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetCurrentCallbackThreshold', 'get_current_callback_threshold'), 
'elements': [('option', 'char', 1, 'out'), 
             ('min', 'int16', 1, 'out'),
             ('max', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`SetCurrentCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetCurrentCallbackThreshold`
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
 "'o'",    "Callback wird ausgelöst wenn der Analogwert *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn der Analogwert *innerhalb* des min und max Wertes ist"
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

 :func:`CurrentReached`, :func:`AnalogValueReached`

are triggered, if the thresholds

 :func:`SetCurrentCallbackThreshold`, :func:`SetAnalogValueCallbackThreshold`

keep being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callbacks

 :func:`CurrentReached`, :func:`AnalogValueReached`
 
ausgelöst werden, wenn die Schwellwerte 

 :func:`SetCurrentCallbackThreshold`, :func:`SetAnalogValueCallbackThreshold`
 
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
'name': ('Current', 'current'), 
'elements': [('current', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetCurrentCallbackPeriod`. The :word:`parameter` is the current of the
sensor.

:func:`Current` is only triggered if the current has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetCurrentCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die Stromstärke des Sensors.

:func:`Current` wird nur ausgelöst wenn sich die Stromstärke seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('AnalogValue', 'analog_value'), 
'elements': [('value', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetAnalogValueCallbackPeriod`. The :word:`parameter` is the analog value
of the sensor.

:func:`AnalogValue` is only triggered if the current has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetAnalogValueCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist der Analogwert des Umgebungslichtsensors.

:func:`AnalogValue` wird nur ausgelöst wenn sich der Analogwert seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('CurrentReached', 'current_reached'), 
'elements': [('current', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetCurrentCallbackThreshold` is reached.
The :word:`parameter` is the current of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetCurrentCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Stromstärke des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('AnalogValueReached', 'analog_value_reached'), 
'elements': [('value', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetAnalogValueCallbackThreshold` is reached.
The :word:`parameter` is the analog value of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetAnalogValueCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist der Analogwert des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('OverCurrent', 'over_current'), 
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when an over current is measured
(see :func:`IsOverCurrent`).
""",
'de':
"""
Dieser Callback wird ausgelöst wenn ein Überstrom gemessen wurde
(siehe :func:`IsOverCurrent`).
"""
}]
})
