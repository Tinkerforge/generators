# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Color Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2153,
    'name': 'Compass',
    'display_name': 'Compass',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'TBD',
        'de': 'TBD'
    },
    'released': False,
    'documented': False,
    'discontinued': False,
    'features': [
        'comcu_bricklet',
        'bricklet_get_identity'
    ],
    'packets': [],
    'examples': []
}

heading_doc = {
'en':
"""
""",
'de':
"""
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Heading',
    data_name = 'Heading',
    data_type = 'int16',
    doc       = heading_doc
)

com['packets'].append({
'type': 'function',
'name': 'Get Magnetic Flux Density',
'elements': [('X', 'int32', 1, 'out'),
             ('Y', 'int32', 1, 'out'),
             ('Z', 'int32', 1, 'out')],
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
'name': 'Set Magnetic Flux Density Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period in ms is the period with which the :cb:`Magnetic Flux Density` callback
is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.

The default value is (0, false).
""",
'de':
"""
Die Periode in ms ist die Periode mit der der :cb:`Magnetic Flux Density` Callback
ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn der Wert sich im Vergleich zum letzten mal geändert
hat. Ändert der Wert sich nicht innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen des Werts.

Der Standardwert ist (0, false).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Magnetic Flux Density Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set Magnetic Flux Density Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set Magnetic Flux Density Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Magnetic Flux Density',
'elements': [('X', 'int32', 1, 'out'),
             ('Y', 'int32', 1, 'out'),
             ('Z', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set Magnetic Flux Density Callback Configuration`.

The :word:`parameters` are the same as :func:`Get Magnetic Flux Density`.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set Magnetic Flux Density Callback Configuration` gesetzten Konfiguration

Die :word:`Parameter` sind der gleichen wie :func:`Get Magnetic Flux Density`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('Data Rate', 'uint8', 1, 'in', ('Data Rate', [('100Hz', 0),
                                                            ('200Hz', 1),
                                                            ('400Hz', 2),
                                                            ('600Hz', 3)])),
             ('Background Calibration', 'bool', 1, 'in')],
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
'name': 'Get Configuration',
'elements': [('Data Rate', 'uint8', 1, 'out', ('Data Rate', [('100Hz', 0),
                                                             ('200Hz', 1),
                                                             ('400Hz', 2),
                                                             ('600Hz', 3)])),
             ('Background Calibration', 'bool', 1, 'out')],
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
'name': 'Set Calibration',
'elements': [('Offset', 'int16', 3, 'in'),
             ('Multiplier', 'int16', 3, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
saved in non-volatile memory

""",
'de':
"""

"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Calibration',
'elements': [('Offset', 'int16', 3, 'out'),
             ('Multiplier', 'int16', 3, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""

""",
'de':
"""

"""
}]
})
