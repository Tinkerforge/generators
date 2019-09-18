# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# NO2 Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2155,
    'name': 'Gas',
    'display_name': 'Gas',
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
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

com['constant_groups'].append({
'name': 'Gas Type',
'type': 'uint8',
'constants': [('CO',     0),
              ('EtOH',   1),
              ('H2S',    2),
              ('SO2',    3),
              ('NO2',    4),
              ('O3',     5),
              ('IAQ',    6),
              ('RESP',   7),
              ('O3 NO2', 8)]
})

com['packets'].append({
'type': 'function',
'name': 'Get Values',
'elements': [('Gas Concentration', 'int32', 1, 'out'),  # always PPB?
             ('Temperature', 'int16', 1, 'out'),        # 1/100 °C
             ('Humidity', 'uint16', 1, 'out'),          # 1/100 %RH
             ('Gas Type', 'uint8', 1, 'out', {'constant_group': 'Gas Type'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
# MAX 4 SPS
""",
'de':
"""

"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get ADC Count',
'elements': [('ADC Count', 'uint32', 1, 'out')],
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


com['packets'].append({
'type': 'function',
'name': 'Set Calibration',
'elements': [('ADC Count Zero', 'uint32', 1, 'in'),
             ('Temperature Zero', 'int16', 1, 'in'),       # 1/100 °C
             ('Humidity Zero', 'int16', 1, 'in'),          # 1/100 %RH
             ('Compensation Zero Low', 'int32', 1, 'in'),  # 1/1000
             ('Compensation Zero High', 'int32', 1, 'in'), # 1/1000
             ('PPM Span', 'uint32', 1, 'in'),              # 1/100
             ('ADC Count Span', 'uint32', 1, 'in'),
             ('Temperature Span', 'int16', 1, 'in'),       # 1/100 °C
             ('Humidity Span', 'int16', 1, 'in'),          # 1/100 %RH
             ('Compensation Span Low', 'int32', 1, 'in'),  # 1/1000 
             ('Compensation Span High', 'int32', 1, 'in'), # 1/1000
             ('Temperature Offset', 'int16', 1, 'in'),     # 1/100 °C
             ('Humidity Offset', 'int16', 1, 'in'),        # 1/100 %RH
             ('Gas Type', 'uint8', 1, 'in', {'constant_group': 'Gas Type'}),
             ('Sensitivity', 'int32', 1, 'in')],           # 1/100 nA/PPM
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

com['packets'].append({
'type': 'function',
'name': 'Get Calibration',
'elements': [('ADC Count Zero', 'uint32', 1, 'out'),
             ('Temperature Zero', 'int16', 1, 'out'),       # 1/100 °C
             ('Humidity Zero', 'int16', 1, 'out'),          # 1/100 %RH
             ('Compensation Zero Low', 'int32', 1, 'out'),  # 1/1000
             ('Compensation Zero High', 'int32', 1, 'out'), # 1/1000
             ('PPM Span', 'uint32', 1, 'out'),              # 1/100
             ('ADC Count Span', 'uint32', 1, 'out'),
             ('Temperature Span', 'int16', 1, 'out'),       # 1/100 °C
             ('Humidity Span', 'int16', 1, 'out'),          # 1/100 %RH
             ('Compensation Span Low', 'int32', 1, 'out'),  # 1/1000 
             ('Compensation Span High', 'int32', 1, 'out'), # 1/1000
             ('Temperature Offset', 'int16', 1, 'out'),     # 1/100 °C
             ('Humidity Offset', 'int16', 1, 'out'),        # 1/100 %RH
             ('Gas Type', 'uint8', 1, 'out', {'constant_group': 'Gas Type'}),
             ('Sensitivity', 'int32', 1, 'out')],           # 1/100 nA/PPM
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

com['packets'].append({
'type': 'function',
'name': 'Set Values Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period in ms is the period with which the :cb:`Values`
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
Die Periode in ms ist die Periode mit der der :cb:`Values`
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
'name': 'Get Values Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set Values Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set Values Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Values',
'elements': [('Gas Concentration', 'int32', 1, 'out'),
             ('Temperature', 'int16', 1, 'out'),
             ('Humidity', 'uint16', 1, 'out'),
             ('Gas Type', 'uint8', 1, 'out', {'constant_group': 'Gas Type'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set Values Callback Configuration`.

The :word:`parameters` are the same as :func:`Get Values`.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set Values Callback Configuration` gesetzten Konfiguration

Die :word:`parameters` sind der gleiche wie :func:`Get Values`.
"""
}]
})
