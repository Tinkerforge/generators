# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# CO2 Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 262,
    'name': ('CO2', 'co2', 'CO2', 'CO2 Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures CO2 concentration in ppm',
        'de': 'Misst CO2-Konzentration in ppm'
    },
    'released': False,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetCO2Concentration', 'get_co2_concentration'),
'elements': [('co2_concentration', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the measured CO2 concentration. The value is in 
`ppm (parts per million) <https://en.wikipedia.org/wiki/Parts-per_notation>`__
and between 0 to TBD.

If you want to get the CO2 concentration periodically, it is recommended to use the
callback :func:`CO2Concentration` and set the period with
:func:`SetCO2ConcentrationCallbackPeriod`.
""",
'de':
"""
Gibt die gemessene CO2-Konzentration zurück. Der Wert ist in
`ppm (Teile pro Million) <https://de.wikipedia.org/wiki/Parts_per_million>`__
und im Bereich von 0 bis TBD.

Wenn die Spannung periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`CO2Concentration` zu nutzen und die Periode mit
:func:`SetCO2ConcentrationCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetCO2ConcentrationCallbackPeriod', 'set_co2_concentration_callback_period'),
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`CO2Concentration` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`CO2Concentration` is only triggered if the co2_concentration has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`CO2Concentration` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`CO2Concentration` wird nur ausgelöst wenn sich die Spannung seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetCO2ConcentrationCallbackPeriod', 'get_co2_concentration_callback_period'),
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetCO2ConcentrationCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetCO2ConcentrationCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetCO2ConcentrationCallbackThreshold', 'set_co2_concentration_callback_threshold'),
'elements': [('option', 'char', 1, 'in', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                  ('Outside', 'outside', 'o'),
                                                                                  ('Inside', 'inside', 'i'),
                                                                                  ('Smaller', 'smaller', '<'),
                                                                                  ('Greater', 'greater', '>')])),
             ('min', 'int16', 1, 'in'),
             ('max', 'int16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`CO2ConcentrationReached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the co2_concentration is *outside* the min and max values"
 "'i'",    "Callback is triggered when the co2_concentration is *inside* the min and max values"
 "'<'",    "Callback is triggered when the co2_concentration is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the co2_concentration is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`CO2ConcentrationReached` Callback.

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
'name': ('GetCO2ConcentrationCallbackThreshold', 'get_co2_concentration_callback_threshold'),
'elements': [('option', 'char', 1, 'out', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                   ('Outside', 'outside', 'o'),
                                                                                   ('Inside', 'inside', 'i'),
                                                                                   ('Smaller', 'smaller', '<'),
                                                                                   ('Greater', 'greater', '>')])),
             ('min', 'int16', 1, 'out'),
             ('max', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`SetCO2ConcentrationCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetCO2ConcentrationCallbackThreshold`
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

* :func:`CO2ConcentrationReached`,

are triggered, if the thresholds

* :func:`SetCO2ConcentrationCallbackThreshold`,

keep being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callbacks

* :func:`CO2ConcentrationReached`,

ausgelöst werden, wenn die Schwellwerte

* :func:`SetCO2ConcentrationCallbackThreshold`,

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
'name': ('CO2Concentration', 'co2_concentration'),
'elements': [('co2_concentration', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetCO2ConcentrationCallbackPeriod`. The :word:`parameter` is the co2 concentration of the
sensor.

:func:`CO2Concentration` is only triggered if the co2 concentration has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetCO2ConcentrationCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die gemessene CO2-Konzentration des Sensors.

:func:`CO2Concentration` wird nur ausgelöst wenn sich die CO2-Konzentration seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('CO2ConcentrationReached', 'co2_concentration_reached'),
'elements': [('co2_concentration', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetCO2ConcentrationCallbackThreshold` is reached.
The :word:`parameter` is the CO2 concentration.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von
:func:`SetCO2ConcentrationCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die gemessene CO2-Konzentration.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})
