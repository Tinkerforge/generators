# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# HAT Zero Brick communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Brick',
    'device_identifier': 112,
    'name': 'HAT Zero',
    'display_name': 'HAT Zero',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'HAT for Raspberry Pi Zero with 4 Bricklets ports',
        'de': 'HAT für Raspberry Pi Zero mit 4 Bricklet-Ports'
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
'name': 'Get USB Voltage',
'elements': [('Voltage', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the USB supply voltage of the Raspberry Pi in mV.
""",
'de':
"""
Gibt die USB-Versorgungsspannung des Raspberry Pi in mV zurück.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get USB Voltage', 'voltage'), [(('Voltage', 'Voltage'), 'uint16', 1, 1000.0, 'V', None)], [])]
})
