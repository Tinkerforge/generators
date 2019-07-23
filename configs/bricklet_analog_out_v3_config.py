# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Analog Out Bricklet 3.0 communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2115,
    'name': 'Analog Out V3',
    'display_name': 'Analog Out 3.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Generates configurable DC voltage between 0V and 12V',
        'de': 'Erzeugt konfigurierbare Gleichspannung zwischen 0V und 12V'
    },
    'released': True,
    'documented': True,
    'discontinued': False,
    'features': [
        'comcu_bricklet',
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Set Output Voltage',
'elements': [('Voltage', 'uint16', 1, 'in')],
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
'name': 'Get Output Voltage',
'elements': [('Voltage', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the voltage as set by :func:`Set Output Voltage`.
""",
'de':
"""
Gibt die Spannung zurück, wie von :func:`Set Output Voltage` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Input Voltage',
'elements': [('Voltage', 'uint16', 1, 'out')],
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

com['examples'].append({
'name': 'Simple',
'functions': [('setter', 'Set Output Voltage', [('uint16', 3300)], 'Set output voltage to 3.3V', None)]
})
