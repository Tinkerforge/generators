# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Energy Monitor Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2152,
    'name': 'Energy Monitor',
    'display_name': 'Energy Monitor',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'TBD',
        'de': 'TBD'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'discontinued': False,
    'packets': [],
    'examples': []
}


com['packets'].append({
'type': 'function',
'name': 'Get Energy Data',
'elements': [('Voltage', 'int32', 1, 'out'),        # 10mV RMS
             ('Current', 'int32', 1, 'out'),        # 10mA RMS
             ('Energy', 'int32', 1, 'out'),         # 10mWh
             ('Real Power', 'int32', 1, 'out'),     # 10mW
             ('Apparent Power', 'int32', 1, 'out'), # 10mVA
             ('Reactive Power', 'int32', 1, 'out'), # 10mVAR
             ('Power Factor', 'uint16', 1, 'out'),  # 1/1000
             ('Frequency', 'uint16', 1, 'out')],    # 1/100Hz
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
frequency calculated every 6 seconds
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Reset Energy',
'elements': [],
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
'name': 'Get Waveform Low Level',
'elements': [('Waveform Chunk Offset', 'uint16', 1, 'out'),
             ('Waveform Chunk Data', 'int16', 30, 'out')],
'high_level': {'stream_out': {'name': 'Waveform', 'fixed_length': (1024-256)*2}},
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
'name': 'Set Transformer Calibration',
'elements': [('Voltage Ratio', 'uint16', 1, 'in'),
             ('Current Ratio', 'uint16', 1, 'in'),
             ('Phase Shift', 'int16', 1, 'in')],
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
'name': 'Get Transformer Calibration',
'elements': [('Voltage Ratio', 'uint16', 1, 'out'),
             ('Current Ratio', 'uint16', 1, 'out'),
             ('Phase Shift', 'int16', 1, 'out')],
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
'name': 'Calibrate Offset',
'elements': [],
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
'name': 'Set Energy Data Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period in ms is the period with which the :cb:`Energy Data`
callback is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.

The default value is (0, false).
""",
'de':
"""
Die Periode in ms ist die Periode mit der der :cb:`Energy Data`
Callback ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

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
'name': 'Get Energy Data Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set Energy Data Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set Energy Data Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Energy Data',
'elements': [('Voltage', 'int32', 1, 'out'),        # mV RMS
             ('Current', 'int32', 1, 'out'),        # mA RMS
             ('Energy', 'int32', 1, 'out'),         # 10mWh
             ('Real Power', 'int32', 1, 'out'),     # W
             ('Apparent Power', 'int32', 1, 'out'), # VA
             ('Reactive Power', 'int32', 1, 'out'), # VAR
             ('Power Factor', 'uint16', 1, 'out'),
             ('Frequency', 'uint16', 1, 'out')],    # 1/100Hz
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set Energy Data Callback Configuration`.

The :word:`parameters` are the same as :func:`Get Energy Data`.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set Energy Data Callback Configuration` gesetzten Konfiguration

Die :word:`parameters` sind der gleiche wie :func:`Get Energy Data`.
"""
}]
})
