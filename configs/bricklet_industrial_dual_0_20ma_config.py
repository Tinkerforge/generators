# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Dual 0-20mA Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 228,
    'name': ('Industrial Dual 0 20mA', 'Industrial Dual 0-20mA', 'Industrial Dual 0-20mA Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures two DC currents between 0mA and 20mA (IEC 60381-1)',
        'de': 'Misst zwei Gleichströme zwischen 0mA und 20mA (IEC 60381-1)'
    },
    'released': True,
    'documented': True,
    'packets': [],
    'examples': []
}

com['doc'] = {
'en':
"""
Two sensors can be connected to the Bricklet. Functions that are related
directly to a sensor have a ``sensor`` parameter to specify one of the two
sensors. Valid values for the ``sensor`` parameter are 0 and 1.
""",
'de':
"""
Es können zwei Sensoren an das Bricklet angeschlossen werden. Funktionen die
sich direkt auf einen der Sensoren beziehen haben einen ``sensor`` Parameter,
um den Sensor anzugeben. Gültige Werte für den ``sensor`` Parameter sind 0
und 1.
"""
}

com['packets'].append({
'type': 'function',
'name': 'Get Current',
'elements': [('Sensor', 'uint8', 1, 'in'),
             ('Current', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current of the specified sensor (0 or 1). The value is in nA
and between 0nA and 22505322nA (22.5mA).

It is possible to detect if an IEC 60381-1 compatible sensor is connected
and if it works probably.

If the returned current is below 4mA, there is likely no sensor connected
or the sensor may be defect. If the returned current is over 20mA, there might
be a short circuit or the sensor may be defect.

If you want to get the current periodically, it is recommended to use the
callback :func:`Current` and set the period with 
:func:`SetCurrentCallbackPeriod`.
""",
'de':
"""
Gibt die gemessenen Stromstärke des angegebenen Sensors (0 oder 1) zurück. Der
Wert ist in nA und im Bereich von 0nA bis 22505322nA (22,5mA).

Es ist möglich zu erkennen ob ein IEC 60381-1-kompatibler Sensor angeschlossen
ist und ob er funktionsfähig ist.

Falls die zurückgegebene Stromstärke kleiner als 4mA ist, ist wahrscheinlich
kein Sensor angeschlossen oder der Sensor ist defekt. Falls die zurückgegebene
Stromstärke über 20mA ist, besteht entweder ein Kurzschluss oder der Sensor
ist defekt. Somit ist erkennbar ob ein Sensor angeschlossen und funktionsfähig
ist.

Wenn die Stromstärke periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`Current` zu nutzen und die Periode mit 
:func:`SetCurrentCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Current Callback Period',
'elements': [('Sensor', 'uint8', 1, 'in'),
             ('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Current` callback is triggered
periodically for the given sensor. A value of 0 turns the callback off.

:func:`Current` is only triggered if the current has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Current` Callback für den
übergebenen Sensor ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Current` wird nur ausgelöst wenn sich die Stromstärke seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0. 
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Current Callback Period',
'elements': [('Sensor', 'uint8', 1, 'in'),
             ('Period', 'uint32', 1, 'out')],
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
'name': 'Set Current Callback Threshold',
'elements': [('Sensor', 'uint8', 1, 'in'),
             ('Option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'int32', 1, 'in'),
             ('Max', 'int32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`CurrentReached` callback for the given
sensor.

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
Setzt den Schwellwert des :func:`CurrentReached` Callbacks für den übergebenen
Sensor.

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
'name': 'Get Current Callback Threshold',
'elements': [('Sensor', 'uint8', 1, 'in'),
             ('Option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'int32', 1, 'out'),
             ('Max', 'int32', 1, 'out')],
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
'name': 'Set Debounce Period',
'elements': [('Debounce', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the threshold callback

* :func:`CurrentReached`

is triggered, if the threshold

* :func:`SetCurrentCallbackThreshold`

keeps being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher der Schwellwert Callback

* :func:`CurrentReached`
 
ausgelöst werden, wenn der Schwellwert

* :func:`SetCurrentCallbackThreshold`
 
weiterhin erreicht bleibt.

Der Standardwert ist 100.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Debounce Period',
'elements': [('Debounce', 'uint32', 1, 'out')],
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
'name': 'Set Sample Rate',
'elements': [('Rate', 'uint8', 1, 'in', ('Sample Rate', [('240 SPS', 0),
                                                         ('60 SPS', 1),
                                                         ('15 SPS', 2),
                                                         ('4 SPS', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the sample rate to either 240, 60, 15 or 4 samples per second.
The resolution for the rates is 12, 14, 16 and 18 bit respectively.

.. csv-table::
 :header: "Value", "Description"
 :widths: 10, 100

 "0",    "240 samples per second, 12 bit resolution"
 "1",    "60 samples per second, 14 bit resolution"
 "2",    "15 samples per second, 16 bit resolution"
 "3",    "4 samples per second, 18 bit resolution"

The default value is 3 (4 samples per second with 18 bit resolution).
""",
'de':
"""
Setzt die Abtastrate auf 240, 60, 15 oder 4 Samples pro Sekunde.
Die Auflösung für die Raten sind 12, 14, 16 und 18 Bit respektive.

.. csv-table::
 :header: "Wert", "Beschreibung"
 :widths: 10, 100

 "0",    "240 Samples pro Sekunde, 12 Bit Auflösung"
 "1",    "60 Samples pro Sekunde, 14 Bit Auflösung"
 "2",    "15 Samples pro Sekunde, 16 Bit Auflösung"
 "3",    "4 Samples pro Sekunde, 18 Bit Auflösung"

Der Standardwert ist 3 (4 Samples pro Sekunde mit 18 Bit Auflösung).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Sample Rate',
'elements': [('Rate', 'uint8', 1, 'out', ('Sample Rate', [('240 SPS', 0),
                                                          ('60 SPS', 1),
                                                          ('15 SPS', 2),
                                                          ('4 SPS', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the sample rate as set by :func:`SetSampleRate`.
""",
'de':
"""
Gibt die Abtastrate zurück, wie von :func:`SetSampleRate`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Current',
'elements': [('Sensor', 'uint8', 1, 'out'),
             ('Current', 'int32', 1, 'out')],
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
'name': 'Current Reached',
'elements': [('Sensor', 'uint8', 1, 'out'),
             ('Current', 'int32', 1, 'out')],
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

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Current', 'current from sensor 1'), [(('Current', 'Current (Sensor 1)'), 'int32', 1000000.0, 'nA', 'mA', None)], [('uint8', 1)])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Current', 'current'), [(('Sensor', 'Sensor'), 'uint8', None, None, None, None), (('Current', 'Current'), 'int32', 1000000.0, 'nA', 'mA', None)], None, None),
              ('callback_period', ('Current', 'current (sensor 1)'), [('uint8', 1)], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('Current Reached', 'current reached'), [(('Sensor', 'Sensor'), 'uint8', None, None, None, None), (('Current', 'Current'), 'int32', 1000000.0, 'nA', 'mA', None)], None, None),
              ('callback_threshold', ('Current', 'current (sensor 1)'), [('uint8', 1)], '>', [(10, 0)])]
})
