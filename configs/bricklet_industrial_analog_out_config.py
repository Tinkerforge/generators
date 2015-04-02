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
'name': ('Enable', 'enable'), 
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
'name': ('Disable', 'disable'), 
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
'name': ('IsEnabled', 'is_enabled'), 
'elements': [('enabled', 'bool', 1, 'out')],
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
'name': ('SetVoltage', 'set_voltage'), 
'elements': [('voltage', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the voltage in mV.
""",
'de':
"""
Setzt die Spannung in mV.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetVoltage', 'get_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the voltage as set by :func:`SetVoltage`.
""",
'de':
"""
Gibt die Spannung zurück, wie von :func:`SetVoltage`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetCurrent', 'set_current'), 
'elements': [('current', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the current in µA.
""",
'de':
"""
Setzt den Strom in µA.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetCurrent', 'get_current'), 
'elements': [('current', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current as set by :func:`SetCurrent`.
""",
'de':
"""
Gibt die Spannung zurück, wie von :func:`SetCurrent`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetConfiguration', 'set_configuration'), 
'elements': [('voltage_range', 'uint8', 1, 'in', ('VoltageRange', 'voltage_range', [('0To5V', '0_to_5v', 0),
                                                                                    ('0To10V', '0_to_10v', 1)])),
             ('current_range', 'uint8', 1, 'in', ('CurrentRange', 'current_range', [('4To20mA', '4_to_20ma', 0),
                                                                                    ('0To20mA', '0_to_20ma', 1),
                                                                                    ('0To24mA', '0_to_24ma', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
TODO
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetConfiguration', 'get_configuration'), 
'elements': [('voltage_range', 'uint8', 1, 'out', ('VoltageRange', 'voltage_range', [('0To5V', '0_to_5v', 0),
                                                                                     ('0To10V', '0_to_10v', 1)])),
             ('current_range', 'uint8', 1, 'out', ('CurrentRange', 'current_range', [('4To20mA', '4_to_20ma', 0),
                                                                                     ('0To20mA', '0_to_20ma', 1),
                                                                                     ('0To24mA', '0_to_24ma', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`SetConfiguration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`SetConfiguration`
gesetzt.
"""
}]
})
