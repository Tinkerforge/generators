# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Air Quality Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 297,
    'name': 'Air Quality',
    'display_name': 'Air Quality',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures relative IAQ index, temperature, humidity and air pressure',
        'de': 'Misst IAQ Index, Temperatur, relative Luftfeuchtigkeit und Luftdruck'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'discontinued': False,
    'packets': [],
    'examples': []
}

IAQ_CONSTANT = ('Accuracy', [('Unreliable', 0),
                             ('Low',  1),
                             ('Medium',  2),
                             ('High',  3)])

com['packets'].append({
'type': 'function',
'name': 'Get All Values',
'elements': [('IAQ Index', 'int32', 1, 'out'),
             ('IAQ Index Accuracy', 'uint8', 1, 'out', IAQ_CONSTANT),
             ('Temperature', 'int32', 1, 'out'),
             ('Humidity', 'int32', 1, 'out'),
             ('Air Pressure', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Temperature Offset',
'elements': [('Offset', 'int32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets a temperature offset in 1/100°C. A offset of 10 will decrease the temperature
by 0.1°C.

If you install this Bricklet into an enclosure and you want to measure the ambient
temperature, you may have to decrease the measured temperature by some value to
include for the error because of the heating inside of the enclosure.

We would recommend that you leave the parts in the enclosure running for at least
24 hours such that a temperature equilibrium can be reached. After that you can measure
the temperature directly outside of enclosure and set the difference as offset.

This temperature difference is used to calculate the correct ambient humidity and
also for the in air quality measurements. If the precision of the measurements is
important to you we recommend that you set this value.
""",
'de':
"""
TBD
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Temperature Offset',
'elements': [('Offset', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the temperature offset as set by
:func:`Set Temperature Offset`.
""",
'de':
"""
Gibt den Temperatur-Offset zurück, wie mittels
:func:`Set Temperature Offset` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set All Values Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period in ms is the period with which the :cb:`All Values`
callback is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after at least one of the values has changed. If the values didn't 
change within the period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.

The default value is (0, false).
""",
'de':
"""
Die Periode in ms ist die Periode mit der der :cb:`All Values`
Callback ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn sich mindest ein Wert im Vergleich zum letzten mal geändert
hat. Ändert sich kein Wert innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn ein Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen der Werte.

Der Standardwert ist (0, false).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get All Values Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set All Values Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set All Values Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'All Values',
'elements': [('IAQ Index', 'int32', 1, 'out'),
             ('IAQ Index Accuracy', 'uint8', 1, 'out', IAQ_CONSTANT),
             ('Temperature', 'int32', 1, 'out'),
             ('Humidity', 'int32', 1, 'out'),
             ('Air Pressure', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set All Values Callback Configuration`.

The `parameters` are the same as :func:`Get All Values`.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set All Values Callback Configuration` gesetzten Konfiguration

Die `parameters` sind der gleiche wie :func:`Get All Values`.
"""
}]
})

iaq_index_doc = {
'en':
"""
TBD
""",
'de':
"""
TBD
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get IAQ Index',
    data_name = 'IAQ Index',
    data_type = 'int32',
    doc       = iaq_index_doc
)

temperature_doc = {
'en':
"""
TBD
""",
'de':
"""
TBD
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Temperature',
    data_name = 'Temperature',
    data_type = 'int32',
    doc       = temperature_doc
)

humidity_doc = {
'en':
"""
TBD
""",
'de':
"""
TBD
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Humidity',
    data_name = 'Humidity',
    data_type = 'int32',
    doc       = humidity_doc
)

air_pressure_doc = {
'en':
"""
TBD
""",
'de':
"""
TBD
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Air Pressure',
    data_name = 'Air Pressure',
    data_type = 'int32',
    doc       = air_pressure_doc
)

