# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Analog Out Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 258,
    'name': ('IndustrialAnalogOut', 'industrial_analog_out', 'Industrial Analog Out'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for output of voltage between 0 and 10V and current between 4 an 20mA',
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
Sets the voltage in mV. The possible range is 0V to 10V (0-10000).
""",
'de':
"""
Setzt die Spannung in mV. Der mögliche Bereich ist 0V bis 10V (0-10000).
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
""",
'de':
"""
"""
}]
})
