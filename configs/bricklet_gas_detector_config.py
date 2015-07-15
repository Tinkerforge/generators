# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Gas Detector Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 252,
    'name': ('GasDetector', 'gas_detector', 'Gas Detector', 'Gas Detector Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures concentration of different gases',
        'de': 'Misst Konzentration verschiedener Gase'
    },
    'released': False,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetValue', 'get_value'), 
'elements': [('value', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns a value between 0 and 4095. 

See `here <TODO>`__ for more information about the measurements.

If you want to get the value periodically, it is recommended 
to use the callback :func:`Value` and set the period with 
:func:`SetValueCallbackPeriod`.
""",
'de':
"""
Gibt einen Wert zwischen 0 und 4095 zurück.

Siehe `hier <TODO>`__ für mehr Informationen zu den Messwerten.

Wenn der Wert periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`Value` zu nutzen und die Periode mit 
:func:`SetValueCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetValueCallbackPeriod', 'set_value_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Value` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Value` is only triggered if the value value has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Value` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Value` wird nur ausgelöst wenn sich der Wert seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetValueCallbackPeriod', 'get_value_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetValueCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetValueCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetValueCallbackThreshold', 'set_value_callback_threshold'), 
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
Sets the thresholds for the :func:`ValueReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the value value is *outside* the min and max values"
 "'i'",    "Callback is triggered when the value value is *inside* the min and max values"
 "'<'",    "Callback is triggered when the value value is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the value value is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`ValueReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn der Wert *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn der Wert *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn der Wert kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn der Wert größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetValueCallbackThreshold', 'get_value_callback_threshold'), 
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
Returns the threshold as set by :func:`SetValueCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetValueCallbackThreshold`
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

* :func:`ValueReached`

is triggered, if the threshold

* :func:`SetValueCallbackThreshold`

keeps being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callback

* :func:`ValueReached`
 
ausgelöst wird, wenn der Schwellwert 

* :func:`SetValueCallbackThreshold`
 
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
'type': 'function',
'name': ('SetMovingAverage', 'set_moving_average'), 
'elements': [('average', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
for the measured value.

Setting the length to 1 will turn the averaging off. With less
averaging, there is more noise on the data.

The range for the averaging is 1-100.

The default value is 100.
""",
'de':
"""
Setzt die Länge eines `gleitenden Mittelwerts <https://de.wikipedia.org/wiki/Gleitender_Mittelwert>`__
für den gemessenen Wert.

Wenn die Länge auf 1 gesetzt wird, ist das Averaging aus. Desto kleiner
die Länge des Mittelwerts ist, desto mehr Rauschen ist auf den Daten.

Der Wertebereich liegt bei 1-100.

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

com['packets'].append({
'type': 'function',
'name': ('SetDetectorType', 'set_detector_type'), 
'elements': [('detector_type', 'uint8', 1, 'in', ('DetectorType', 'detector_type', [('0', '0', 0),
                                                                                    ('1', '1', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the detector type.

The following types are currently supported.

* Type 0: MQ2 and MQ5
* Type 1: MQ3

The detector type is written to the EEPROM of the Bricklet, so it only has
to be set once.

You can use the Brick Viewer to set the detector type, so you likely
don't need to use this function in your source code.

The default detector type is 0.
""",
'de':
"""
Setzt den Detektortyp

Die folgenden Typen werden aktuell unterstützt:

* Typ 0: MQ2 und MQ5
* Typ 1: MQ3

Der Detektortyp wird in das EEPROM des Bricklets geschrieben und muss
daher nur einmal gesetzt werden.

Wir empfehlen den Typ des Detektors im Brick Viewer zu setzen anstatt
diese Funktion zu nutzen.

Der standard Detektortyp ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetDetectorType', 'get_detector_type'), 
'elements': [('detector_type', 'uint8', 1, 'out', ('DetectorType', 'detector_type', [('0', '0', 0),
                                                                                     ('1', '1', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the detector type as set by :func:`SetDetectorType`.
""",
'de':
"""
Gibt den Detektortyp zurück, wie von :func:`SetDetectorType` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('HeaterOn', 'heater_on'), 
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Turns the internal heater on.
""",
'de':
"""
Aktiviert die interne Heizung.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('HeaterOff', 'heater_off'), 
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Turns the internal heater off.
""",
'de':
"""
Deaktiviert die interne Heizung.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('IsHeaterOn', 'is_heater_on'), 
'elements': [('heater', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns *true* if the heater is on, *false* otherwise.
""",
'de':
"""
Gibt *true* zurück wenn die interne Heizung aktiviert ist, *false* sonst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('Value', 'value'), 
'elements': [('value', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetValueCallbackPeriod`. The :word:`parameter` is the value value
of the sensor.

:func:`Value` is only triggered if the value has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetValueCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist der Wert.

:func:`Value` wird nur ausgelöst wenn sich der Wert seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('ValueReached', 'value_reached'), 
'elements': [('value', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetValueCallbackThreshold` is reached.
The :word:`parameter` is the value of the detector.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetValueCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist der Wert des Detektors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})
