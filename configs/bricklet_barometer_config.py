# -*- coding: utf-8 -*-

# Barometer Bricklet communication config

com = {
    'author': 'Matthias Bolte <matthias@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 221,
    'name': ('Barometer', 'barometer', 'Barometer'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for sensing air pressure and altitude changes',
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetAirPressure', 'get_air_pressure'),
'elements': [('air_pressure', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the air pressure of the air pressure sensor. The value
has a range of 10000 to 1200000 and is given in mbar/1000, i.e. a value
of 1001092 means that an air pressure of 1001.092 mbar is measured.

If you want to get the air pressure periodically, it is recommended to use the
callback :func:`AirPressure` and set the period with
:func:`SetAirPressureCallbackPeriod`.
""",
'de':
"""
Gibt den Luftdruck des Luftdrucksensors zurück. Der Wertbereich
geht von 10000 bis 1200000 und ist in mbar/1000 angegeben, d.h. bei einem Wert von
1001092 wurde ein Luftdruck von 1001,092 mbar gemessen.

Wenn der Luftdruck periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`AirPressure` zu nutzen und die Periode mit 
:func:`SetAirPressureCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAltitude', 'get_altitude'),
'elements': [('altitude', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the relative altitude of the air pressure sensor. The value is given in
cm and is calculated based on the difference between the current air pressure
and the reference air pressure that can be set with :func:`SetReferenceAirPressure`.

If you want to get the altitude periodically, it is recommended to use the
callback :func:`Altitude` and set the period with
:func:`SetAltitudeCallbackPeriod`.
""",
'de':
"""
Gibt die relative Höhe des Luftdrucksensors zurück. Der Wert ist in cm angegeben
und wird auf Basis der Differenz zwischen dem aktuellen Luftdruck und dem
Referenzluftdruck berechnet, welcher mit :func:`SetReferenceAirPressure` gesetzt
werden kann.

Wenn die Höhe periodisch abgefragt werden soll, wird empfohlen den Callback
:func:`Altitude` zu nutzen und die Periode mit :func:`SetAltitudeCallbackPeriod`
vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetAirPressureCallbackPeriod', 'set_air_pressure_callback_period'),
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`AirPressure` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`AirPressure` is only triggered if the air pressure has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`AirPressure` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`AirPressure` wird nur ausgelöst wenn sich der Luftdruck seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAirPressureCallbackPeriod', 'get_air_pressure_callback_period'),
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetAirPressureCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetAirPressureCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetAltitudeCallbackPeriod', 'set_altitude_callback_period'),
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Altitude` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Altitude` is only triggered if the altitude has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Altitude` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Altitude` wird nur ausgelöst wenn sich Höhe seit der letzten Auslösung
geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAltitudeCallbackPeriod', 'get_altitude_callback_period'),
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetAltitudeCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetAltitudeCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetAirPressureCallbackThreshold', 'set_air_pressure_callback_threshold'),
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
Sets the thresholds for the :func:`AirPressureReached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the air pressure is *outside* the min and max values"
 "'i'",    "Callback is triggered when the air pressure is *inside* the min and max values"
 "'<'",    "Callback is triggered when the air pressure is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the air pressure is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`AirPressureReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn der Luftdruck *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn der Luftdruck *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn der Luftdruck kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn der Luftdruck größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAirPressureCallbackThreshold', 'get_air_pressure_callback_threshold'),
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
Returns the threshold as set by :func:`SetAirPressureCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetAirPressureCallbackThreshold`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetAltitudeCallbackThreshold', 'set_altitude_callback_threshold'),
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
Sets the thresholds for the :func:`AltitudeReached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the altitude is *outside* the min and max values"
 "'i'",    "Callback is triggered when the altitude is *inside* the min and max values"
 "'<'",    "Callback is triggered when the altitude is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the altitude is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`AltitudeReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Höhe *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn die Höhe *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn die Höhe kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Höhe größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAltitudeCallbackThreshold', 'get_altitude_callback_threshold'),
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
Returns the threshold as set by :func:`SetAltitudeCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetAltitudeCallbackThreshold`
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

 :func:`AirPressureReached`, :func:`AltitudeReached`

are triggered, if the thresholds

 :func:`SetAirPressureCallbackThreshold`, :func:`SetAltitudeCallbackThreshold`

keep being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callbacks

 :func:`AirPressureReached`, :func:`AltitudeReached`
 
ausgelöst werden, wenn die Schwellwerte 

 :func:`SetAirPressureCallbackThreshold`, :func:`SetAltitudeCallbackThreshold`
 
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
'type': 'function',
'name': ('SetReferenceAirPressure', 'set_reference_air_pressure'),
'elements': [('air_pressure', 'int32', 1, 'in')],
'since_firmware': [1, 1, 0],
'doc': ['bf', {
'en':
"""
Sets the reference air pressure in mbar/1000 for the altitude calculation.
Setting the reference to the current air pressure results in a calculated
altitude of 0cm. Passing 0 is a shortcut for passing the current air pressure as
reference.

Well known reference values are the Q codes
`QNH <http://en.wikipedia.org/wiki/QNH>`__ and
`QFE <http://en.wikipedia.org/wiki/Mean_sea_level_pressure#Mean_sea_level_pressure>`__
used in aviation.

The default value is 1013.25mbar.
""",
'de':
"""
Setzt den Referenzluftdruck in mbar/1000 für die Höhenberechnung. Wenn der
aktuelle Luftdruckwert als Referenz übergeben wird dann gibt die Höhenberechnung
0cm aus. Als Abkürzung kann auch 0 übergeben werden, dadurch wird der
Referenzluftdruck intern auf den aktuellen Luftdruckwert gesetzt.

Wohl bekannte Referenzluftdruckwerte, die in der Luftfahrt verwendet werden, sind
`QNH <http://de.wikipedia.org/wiki/Barometrische_H%C3%B6henmessung_in_der_Luftfahrt#QNH>`__ und
`QFE <http://de.wikipedia.org/wiki/Barometrische_H%C3%B6henmessung_in_der_Luftfahrt#QFE>`__
aus dem Q-Schlüssel.

Der Standardwert ist 1013,25mbar.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetChipTemperature', 'get_chip_temperature'),
'elements': [('temperature', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the temperature of the air pressure sensor. The value
has a range of -4000 to 8500 and is given in °C/100, i.e. a value
of 2007 means that a temperature of 20.07 °C is measured.

This temperature is used internally for temperature compensation of the air
pressure measurement. It is not as accurate as the temperature measured by the
:ref:`temperature_bricklet` or the :ref:`temperature_ir_bricklet`.
""",
'de':
"""
Gibt die Temperatur des Luftdrucksensors zurück. Der Wertbereich
ist von -4000 bis 8500 und ist in °C/100 angegeben, d.h. bei einem Wert von
2007 wurde eine Temperatur von 20,07 °C gemessen.

Diese Temperatur wird intern zur Temperaturkompensation der Luftdruckmessung
verwendet. Sie ist nicht so genau wie die Temperatur die vom
:ref:`temperature_bricklet` oder dem :ref:`temperature_ir_bricklet` gemessen
wird.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('AirPressure', 'air_pressure'),
'elements': [('air_pressure', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetAirPressureCallbackPeriod`. The :word:`parameter` is the air pressure of the
air pressure sensor.

:func:`AirPressure` is only triggered if the air pressure has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetAirPressureCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist der Luftdruck des Luftdrucksensors.

:func:`AirPressure` wird nur ausgelöst wenn sich der Luftdruck seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('Altitude', 'altitude'),
'elements': [('altitude', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetAltitudeCallbackPeriod`. The :word:`parameter` is the altitude of the
air pressure sensor.

:func:`Altitude` is only triggered if the altitude has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetAltitudeCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die Höhe des Luftdrucksensors.

:func:`Altitude` wird nur ausgelöst wenn sich die Höhe seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('AirPressureReached', 'air_pressure_reached'),
'elements': [('air_pressure', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetAirPressureCallbackThreshold` is reached.
The :word:`parameter` is the air pressure of the air pressure sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetAirPressureCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist der Luftdruck des Luftdrucksensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('AltitudeReached', 'altitude_reached'),
'elements': [('altitude', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetAltitudeCallbackThreshold` is reached.
The :word:`parameter` is the altitude of the air pressure sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetAltitudeCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Höhe des Luftdrucksensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetReferenceAirPressure', 'get_reference_air_pressure'),
'elements': [('air_pressure', 'int32', 1, 'out')],
'since_firmware': [1, 1, 0],
'doc': ['bf', {
'en':
"""
Returns the reference air pressure as set by :func:`SetReferenceAirPressure`.
""",
'de':
"""
Gibt den Referenzluftdruckwert zurück, wie von :func:`SetReferenceAirPressure`
gesetzt.
"""
}]
})
