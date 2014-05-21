# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# NFC/RFID Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 246,
    'name': ('NFCRFID', 'nfc_rfid', 'NFC/RFID'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device that can read and write NFC and RFID tags',
    'released': False,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('RequestTagID', 'request_tag_id'), 
'elements': [('target_type', 'uint8', 1, 'in')],
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
'name': ('GetTagID', 'get_tag_id'), 
'elements': [('target_type', 'uint8', 1, 'out'),
             ('tid_length', 'uint16', 1, 'out'),
             ('tid', 'uint8', 7, 'out')],
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
'name': ('GetState', 'get_state'), 
'elements': [('state', 'uint8', 1, 'out'),
             ('idle', 'bool', 1, 'out')],
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
'name': ('AuthenticateMifareClassicPage', 'authenticate_mifare_classic_page'), 
'elements': [('page', 'uint16', 1, 'in'),
             ('key_number', 'uint8', 1, 'in'),
             ('key', 'uint8', 6, 'in')],
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
'name': ('WritePage', 'write_page'), 
'elements': [('page', 'uint16', 1, 'in'),
             ('data', 'uint8', 16, 'in')],
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
'name': ('RequestPage', 'request_page'), 
'elements': [('page', 'uint16', 1, 'in')],
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
'name': ('GetPage', 'get_page'), 
'elements': [('data', 'uint8', 16, 'out')],
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
'type': 'callback',
'name': ('StateChanged', 'state_changed'), 
'elements': [('state', 'uint8', 1, 'out'),
             ('idle', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
""",
'de':
"""
"""
}]
})

