# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Unknown Bricklet communication config

com = {
    'author': 'Matthias Bolte <matthias@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': -21,
    'name': 'Unknown',
    'display_name': 'Unknown',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '',
        'de': ''
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

com['packets'].append({
'type': 'function',
'function_id': 252,
'name': 'Comcu Enumerate',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
This function is equivalent to the normal enumerate function.
It is used to trigger the initial enumeration of CoMCU-Bricklets.
See :cb:`Comcu Enumerate`.
""",
'de':
"""
Diese Funktion ist äquivalent zur normalen Enumerate-Funktion.
Sie wird verwendet, um die initiale Enumerierung von CoMCU-Bricklets auszulösen.
Siehe :cb:`Comcu Enumerate`.
"""
}]
})


com['packets'].append({
'type': 'callback',
'function_id': 253,
'name': 'Comcu Enumerate',
'elements': [('Uid', 'string', 8, 'out', {}),
             ('Connected Uid', 'string', 8, 'out', {}),
             ('Position', 'char', 1, 'out', {'range': ('0', '8')}),
             ('Hardware Version', 'uint8', 3, 'out', [{'name': 'Major'}, {'name': 'Minor'}, {'name': 'Revision'}]),
             ('Firmware Version', 'uint8', 3, 'out', [{'name': 'Major'}, {'name': 'Minor'}, {'name': 'Revision'}]),
             ('Device Identifier', 'uint16', 1, 'out', {}),
             ('Enumeration Type', 'uint8', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
This callback is equivalent to the normal enumerate callback, but will send the enumeration type CONNECTED.
See :func:`Comcu Enumerate`.
""",
'de':
"""
Dieses Callback ist äquivalent zum normalen Enumerate-Callback, gibt aber den Enumeration-Type CONNECTED zurück.
Siehe :func:`Comcu Enumerate`.
"""
}]
})
