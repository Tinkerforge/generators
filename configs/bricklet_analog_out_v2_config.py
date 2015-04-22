# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Analog Out Bricklet 2.0 communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 256,
    'name': ('AnalogOutV2', 'analog_out_v2', 'Analog Out 2.0', 'Analog Out Bricklet 2.0'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for output of voltage between 0 and 12V',
    'released': False,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('SetOutputVoltage', 'set_output_voltage'), 
'elements': [('voltage', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the voltage in mV. The possible range is 0V to 12V (0-12000).
""",
'de':
"""
Setzt die Spannung in mV. Der mögliche Bereich ist 0V bis 12V (0-12000).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetOutputVoltage', 'get_output_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the voltage as set by :func:`SetOutputVoltage`.
""",
'de':
"""
Gibt die Spannung zurück, wie von :func:`SetOutputVoltage`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetInputVoltage', 'get_input_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the input voltage in mV.
""",
'de':
"""
Gibt die Eingangsspannung in mV zurück.
"""
}]
})
