# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Voltage/Current Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 227,
    'name': ('VoltageCurrent', 'voltage_current', 'Voltage/Current', 'Voltage/Current Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for high precision sensing of voltage and current',
    'released': True,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetCurrent', 'get_current'), 
'elements': [('current', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current. The value is in mA
and between -20000mA and 20000mA.

If you want to get the current periodically, it is recommended to use the
callback :func:`Current` and set the period with 
:func:`SetCurrentCallbackPeriod`.
""",
'de':
"""
Gibt die gemessenen Stromstärke zurück. Der Wert ist in mA und im
Bereich von -20000mA bis 20000mA.

Wenn die Stromstärke periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`Current` zu nutzen und die Periode mit 
:func:`SetCurrentCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetVoltage', 'get_voltage'), 
'elements': [('voltage', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the voltage. The value is in mV
and between 0mV and 36000mV.

If you want to get the voltage periodically, it is recommended to use the
callback :func:`Voltage` and set the period with 
:func:`SetVoltageCallbackPeriod`.
""",
'de':
"""
Gibt die gemessenen Spannung zurück. Der Wert ist in mV und im
Bereich von 0mV bis 36000mV.

Wenn die Stromstärke periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`Voltage` zu nutzen und die Periode mit 
:func:`SetVoltageCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetPower', 'get_power'), 
'elements': [('power', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the power. The value is in mW
and between 0mV and 720000mW.

If you want to get the power periodically, it is recommended to use the
callback :func:`Power` and set the period with 
:func:`SetPowerCallbackPeriod`.
""",
'de':
"""
Gibt die gemessenen Leistung zurück. Der Wert ist in mW und im
Bereich von 0mW bis 720000mW.

Wenn die Leistung periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`Power` zu nutzen und die Periode mit 
:func:`SetPowerCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetConfiguration', 'set_configuration'), 
'elements': [('averaging', 'uint8', 1, 'in', ('Averaging', 'averaging', [('1', '1', 0),
                                                                         ('4', '4', 1),
                                                                         ('16', '16', 2),
                                                                         ('64', '64', 3),
                                                                         ('128', '128', 4),
                                                                         ('256', '256', 5),
                                                                         ('512', '512', 6),
                                                                         ('1024', '1024', 7)])),
             ('voltage_conversion_time', 'uint8', 1, 'in'),
             ('current_conversion_time', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the configuration of the Voltage/Current Bricklet. It is
possible to configure number of averages as well as
voltage and current conversion time.

Averaging:

.. csv-table::
 :header: "Value", "Number of Averages"
 :widths: 20, 20

 "0",    "1"
 "1",    "4"
 "2",    "16"
 "3",    "64"
 "4",    "128"
 "5",    "256"
 "6",    "512"
 ">=7",  "1024"

Voltage/Current conversion:

.. csv-table::
 :header: "Value", "Conversion time"
 :widths: 20, 20

 "0",    "140µs"
 "1",    "204µs"
 "2",    "332µs"
 "3",    "588µs"
 "4",    "1.1ms"
 "5",    "2.116ms"
 "6",    "4.156ms"
 ">=7",  "8.244ms"

The default values are 3, 4 and 4 (64, 1.1ms, 1.1ms) for averaging, voltage 
conversion and current conversion.
""",
'de':
"""
Setzt die Konfiguration des Voltage/Current Bricklet. Es ist
möglich die Anzahl für die Durchschnittsbildung, und die 
Wandlungszeit für Spannung und Stromstärke zu definieren.

Durchschnittsbildung:

.. csv-table::
 :header: "Wert", "Anzahl"
 :widths: 20, 20

 "0",    "1"
 "1",    "4"
 "2",    "16"
 "3",    "64"
 "4",    "128"
 "5",    "256"
 "6",    "512"
 ">=7",  "1024"

Wandlungszeit für Spannung/Stromstärke:

.. csv-table::
 :header: "Wert", "Wandlungszeit"
 :widths: 20, 20

 "0",    "140µs"
 "1",    "204µs"
 "2",    "332µs"
 "3",    "588µs"
 "4",    "1.1ms"
 "5",    "2.116ms"
 "6",    "4.156ms"
 ">=7",  "8.244ms"

Die Standardwerte sind 3, 4 und 4 (64, 1.1ms, 1.1ms) für die
Durchschnittsbildung und die Spannungs/Stromstärkenwandlungszeit.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetConfiguration', 'get_configuration'), 
'elements': [('averaging', 'uint8', 1, 'out', ('Averaging', 'averaging', [('1', '1', 0),
                                                                          ('4', '4', 1),
                                                                          ('16', '16', 2),
                                                                          ('64', '64', 3),
                                                                          ('128', '128', 4),
                                                                          ('256', '256', 5),
                                                                          ('512', '512', 6),
                                                                          ('1024', '1024', 7)])),
             ('voltage_conversion_time', 'uint8', 1, 'out'),
             ('current_conversion_time', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the configuration as set by :func:`SetConfiguration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`SetConfiguration`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetCalibration', 'set_calibration'), 
'elements': [('gain_multiplier', 'uint16', 1, 'in'),
             ('gain_divisor', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Since the shunt resistor that is used to measure the current is not
perfectly precise, it needs to be calibrated by a multiplier and
divisor if a very precise reading is needed.

For example, if you are expecting a measurement of 1000mA and you
are measuring 1023mA, you can calibrate the Voltage/Current Bricklet 
by setting the multiplier to 1000 and the divisor to 1023.
""",
'de':
"""
Da der Shunt-Widerstand über den die Stromstärke gemessen wird keine
perfekte Genauigkeit hat, ist es nötig einen Multiplikator und
einen Divisor zu setzen falls sehr genaue Messwerte nötig sind.

Zum Beispiel: Wenn eine Messung von 1000mA erwartet wird, das
Voltage/Current Bricklet aber 1023mA zurück gibt, sollte 
der Multiplikator auf 1000 und der Divisor auf 1023 gesetzt
werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetCalibration', 'get_calibration'), 
'elements': [('gain_multiplier', 'uint16', 1, 'out'),
             ('gain_divisor', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the calibration as set by :func:`SetCalibration`.
""",
'de':
"""
Gibt die Kalibrierung zurück, wie von :func:`SetCalibration`
gesetzt.
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
gesetzt
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetVoltageCallbackPeriod', 'set_voltage_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Voltage` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Voltage` is only triggered if the voltage has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Voltage` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Voltage` wird nur ausgelöst wenn sich die Spannung seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetVoltageCallbackPeriod', 'get_voltage_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetVoltageCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetVoltageCallbackPeriod`
gesetzt
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetPowerCallbackPeriod', 'set_power_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Power` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Power` is only triggered if the power has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Power` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Power` wird nur ausgelöst wenn sich die Leistung seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetPowerCallbackPeriod', 'get_power_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`GetPowerCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`GetPowerCallbackPeriod`
gesetzt
"""
}]
})


com['packets'].append({
'type': 'function',
'name': ('SetCurrentCallbackThreshold', 'set_current_callback_threshold'), 
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
'name': ('SetVoltageCallbackThreshold', 'set_voltage_callback_threshold'), 
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
Sets the thresholds for the :func:`VoltageReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the voltage is *outside* the min and max values"
 "'i'",    "Callback is triggered when the voltage is *inside* the min and max values"
 "'<'",    "Callback is triggered when the voltage is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the voltage is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`VoltageReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Spannung *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn die Spannung *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn die Spannung kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Spannung größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetVoltageCallbackThreshold', 'get_voltage_callback_threshold'), 
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
Returns the threshold as set by :func:`SetVoltageCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetVoltageCallbackThreshold`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetPowerCallbackThreshold', 'set_power_callback_threshold'), 
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
Sets the thresholds for the :func:`PowerReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the power is *outside* the min and max values"
 "'i'",    "Callback is triggered when the power is *inside* the min and max values"
 "'<'",    "Callback is triggered when the power is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the power is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`PowerReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Leistung *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn die Leistung *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn die Leistung kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Leistung größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetPowerCallbackThreshold', 'get_power_callback_threshold'), 
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
Returns the threshold as set by :func:`SetPowerCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetPowerCallbackThreshold`
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

* :func:`CurrentReached`,
* :func:`VoltageReached`,
* :func:`PowerReached`

are triggered, if the thresholds

* :func:`SetCurrentCallbackThreshold`,
* :func:`SetVoltageCallbackThreshold`,
* :func:`SetPowerCallbackThreshold`

keep being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callbacks

* :func:`CurrentReached`,
* :func:`VoltageReached`,
* :func:`PowerReached`
 
ausgelöst werden, wenn die Schwellwerte 

* :func:`SetCurrentCallbackThreshold`,
* :func:`SetVoltageCallbackThreshold`,
* :func:`SetPowerCallbackThreshold`
 
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
'elements': [('current', 'int32', 1, 'out')],
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
'name': ('Voltage', 'voltage'), 
'elements': [('voltage', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetVoltageCallbackPeriod`. The :word:`parameter` is the voltage of the
sensor.

:func:`Voltage` is only triggered if the voltage has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetVoltageCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die Spannung des Sensors.

:func:`Voltage` wird nur ausgelöst wenn sich die Spannung seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('Power', 'power'), 
'elements': [('power', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetPowerCallbackPeriod`. The :word:`parameter` is the power of the
sensor.

:func:`Power` is only triggered if the power has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetPowerCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die Leistung des Sensors.

:func:`Power` wird nur ausgelöst wenn sich die Leistung seit der
letzten Auslösung geändert hat.
"""
}]
})


com['packets'].append({
'type': 'callback',
'name': ('CurrentReached', 'current_reached'), 
'elements': [('current', 'int32', 1, 'out')],
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
'name': ('VoltageReached', 'voltage_reached'), 
'elements': [('voltage', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetVoltageCallbackThreshold` is reached.
The :word:`parameter` is the voltage of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetVoltageCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Spannung des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('PowerReached', 'power_reached'), 
'elements': [('power', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetPowerCallbackThreshold` is reached.
The :word:`parameter` is the power of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetPowerCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Spannung des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

