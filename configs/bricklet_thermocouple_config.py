# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Thermocouple Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 266,
    'name': 'Thermocouple',
    'display_name': 'Thermocouple',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures temperature with thermocouples',
        'de': 'Misst Temperatur mit Thermoelementen'
    },
    'released': True,
    'documented': True,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Get Temperature',
'elements': [('Temperature', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the temperature of the thermocouple. The value is given in °C/100,
e.g. a value of 4223 means that a temperature of 42.23 °C is measured.

If you want to get the temperature periodically, it is recommended 
to use the :cb:`Temperature` callback and set the period with
:func:`Set Temperature Callback Period`.
""",
'de':
"""
Gibt die Temperatur des Thermoelements zurück. Der Wert wird in °C/100 
angegeben, z.B. bedeutet ein Wert von 4223 eine gemessene Temperatur von 
42,23 °C.

Wenn die Temperatur periodisch abgefragt werden soll, wird empfohlen
den :cb:`Temperature` Callback zu nutzen und die Periode mit
:func:`Set Temperature Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Temperature Callback Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :cb:`Temperature` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Temperature` callback is only triggered if the temperature has changed
since the last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :cb:`Temperature` Callback ausgelöst
wird. Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Temperature` Callback wird nur ausgelöst wenn sich die Temperatur seit
der letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Temperature Callback Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Temperature Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Temperature Callback Period`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Temperature Callback Threshold',
'elements': [('Option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'int32', 1, 'in'),
             ('Max', 'int32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Temperature Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the temperature is *outside* the min and max values"
 "'i'",    "Callback is triggered when the temperature is *inside* the min and max values"
 "'<'",    "Callback is triggered when the temperature is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the temperature is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Temperature Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Temperatur *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn die Temperatur *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn die Temperatur kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Temperatur größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Temperature Callback Threshold',
'elements': [('Option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'int32', 1, 'out'),
             ('Max', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Temperature Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Temperature Callback Threshold`
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

* :cb:`Temperature Reached`

is triggered, if the threshold

* :func:`Set Temperature Callback Threshold`

keeps being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callback

* :cb:`Temperature Reached`
 
ausgelöst wird, wenn der Schwellwert 

* :func:`Set Temperature Callback Threshold`
 
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
Returns the debounce period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Gibt die Entprellperiode zurück, wie von :func:`Set Debounce Period`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Temperature',
'elements': [('Temperature', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Temperature Callback Period`. The :word:`parameter` is the
temperature of the thermocouple.

The :cb:`Temperature` callback is only triggered if the temperature has
changed since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Temperature Callback Period`, ausgelöst. Der :word:`parameter` ist
die Temperatur des Thermoelements.

Der :cb:`Temperature` Callback wird nur ausgelöst wenn sich die Temperatur seit
der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Temperature Reached',
'elements': [('Temperature', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Temperature Callback Threshold` is reached.
The :word:`parameter` is the temperature of the thermocouple.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`Set Temperature Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Temperatur des Thermoelements.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('Averaging', 'uint8', 1, 'in', ('Averaging', [('1', 1),
                                                            ('2', 2),
                                                            ('4', 4),
                                                            ('8', 8),
                                                            ('16', 16)])),
             ('Thermocouple Type', 'uint8', 1, 'in', ('Type', [('B', 0),
                                                               ('E', 1),
                                                               ('J', 2),
                                                               ('K', 3),
                                                               ('N', 4),
                                                               ('R', 5),
                                                               ('S', 6),
                                                               ('T', 7),
                                                               ('G8', 8),
                                                               ('G32', 9)])),
             ('Filter', 'uint8', 1, 'in', ('Filter Option', [('50Hz', 0),
                                                             ('60Hz', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
You can configure averaging size, thermocouple type and frequency
filtering.

Available averaging sizes are 1, 2, 4, 8 and 16 samples.

As thermocouple type you can use B, E, J, K, N, R, S and T. If you have a
different thermocouple or a custom thermocouple you can also use
G8 and G32. With these types the returned value will not be in °C/100,
it will be calculated by the following formulas:

* G8: ``value = 8 * 1.6 * 2^17 * Vin``
* G32: ``value = 32 * 1.6 * 2^17 * Vin``

where Vin is the thermocouple input voltage.

The frequency filter can be either configured to 50Hz or to 60Hz. You should
configure it according to your utility frequency.

The conversion time depends on the averaging and filter configuration, it can
be calculated as follows:

* 60Hz: ``time = 82 + (samples - 1) * 16.67``
* 50Hz: ``time = 98 + (samples - 1) * 20``

The default configuration is 16 samples, K type and 50Hz.
""",
'de':
"""
Konfiguriert werden können Averaging-Größe, Thermoelement-Typ und
Frequenz-Filterung.

Mögliche Averaging-Größen sind 1, 2, 4, 8 und 16 Samples.

Als Thermoelement-Typ stehen B, E, J, K, N, R, S und T zur Verfügung.
Falls ein anderes Thermoelement benutzt werden soll, können G8 und G32
genutzt werden. Mit diesen Typen wird der Wert nicht in °C/100 zurückgegeben
sondern er wird durch folgende Formeln bestimmt:

* G8: ``Wert = 8 * 1.6 * 2^17 * Vin``
* G32: ``Wert = 32 * 1.6 * 2^17 * Vin``

dabei ist Vin die Eingangsspannung des Thermoelements.

Der Frequenz-Filter kann auf 50Hz und 60Hz konfiguriert werden. Er sollte
abhängig von der lokalen Netzfrequenz gewählt werden.

Die Konvertierungszeit ist abhängig von der Averaging-Größe und der
Frequenz-Filter-Konfiguration. Sie kann wie folgt bestimmt werden:

* 60Hz: ``Zeit = 82 + (Samples - 1) * 16.67``
* 50Hz: ``Zeit = 98 + (Samples - 1) * 20``

Die Standardkonfiguration ist 16 Samples, Typ K und 50Hz.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Averaging', 'uint8', 1, 'out', ('Averaging', [('1', 1),
                                                             ('2', 2),
                                                             ('4', 4),
                                                             ('8', 8),
                                                             ('16', 16)])),
             ('Thermocouple Type', 'uint8', 1, 'out', ('Type', [('B', 0),
                                                                ('E', 1),
                                                                ('J', 2),
                                                                ('K', 3),
                                                                ('N', 4),
                                                                ('R', 5),
                                                                ('S', 6),
                                                                ('T', 7),
                                                                ('G8', 8),
                                                                ('G32', 9)])),
             ('Filter', 'uint8', 1, 'out', ('Filter Option', [('50Hz', 0),
                                                              ('60Hz', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Error State',
'elements': [('Over Under', 'bool', 1, 'out'),
             ('Open Circuit', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the current error state. There are two possible errors:

* Over/Under Voltage and
* Open Circuit.

Over/Under Voltage happens for voltages below 0V or above 3.3V. In this case
it is very likely that your thermocouple is defective. An Open Circuit error
indicates that there is no thermocouple connected.

You can use the func:`ErrorState` callback to automatically get triggered
when the error state changes.
""",
'de':
"""
Gibt den aktuellen Error-Status zurück. Es gibt zwei mögliche Status:

* Over/Under Voltage und
* Open Circuit.

Over/Under Voltage bei Spannungen unter 0V oder über 3.3V ausgelöst. In diesem
Fall ist mit hoher Wahrscheinlichkeit das Thermoelement defekt. Ein
Open Circuit-Error deutet darauf hin, das kein Thermoelement angeschlossen
ist.

Der func:`ErrorState` Callback wird automatisch jedes mal ausgelöst wenn sich
der Error-Status ändert.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Error State',
'elements': [('Over Under', 'bool', 1, 'out'),
             ('Open Circuit', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This Callback is triggered every time the error state changes 
(see func:`GetErrorStatus`).
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Error-Status sich verändert
(siehe func:`GetErrorStatus`).
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Temperature', 'temperature'), [(('Temperature', 'Temperature'), 'int32', 100.0, '°C/100', '°C', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Temperature', 'temperature'), [(('Temperature', 'Temperature'), 'int32', 100.0, '°C/100', '°C', None)], None, None),
              ('callback_period', ('Temperature', 'temperature'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('Temperature Reached', 'temperature reached'), [(('Temperature', 'Temperature'), 'int32', 100.0, '°C/100', '°C', None)], None, None),
              ('callback_threshold', ('Temperature', 'temperature'), [], '>', [(30, 0)])]
})
