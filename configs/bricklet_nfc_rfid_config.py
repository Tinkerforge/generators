# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Heart Rate Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 245,
    'name': ('NFCRFID', 'nfc_rfid', 'NFC/RFID'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device that can read and write NFC and RFID tags',
    'released': False,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('ReadPassiveTargetID', 'read_passive_target_id'), 
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
'name': ('GetPassiveTargetID', 'get_passive_target_id'), 
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
'name': ('AuthenticatePageMifareClassic', 'authenticate_page_mifare_classic'), 
'elements': [('page', 'uint8', 1, 'in'),
             ('key_number', 'uint8', 1, 'in'),
             ('key', 'uint8', 7, 'in'),
             ('tid', 'uint8', 4, 'in')],
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
'name': ('WritePageMifareClassic', 'write_page_mifare_classic'), 
'elements': [('page', 'uint8', 1, 'in'),
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
'name': ('WritePageType1', 'write_page_type1'), 
'elements': [('page', 'uint8', 1, 'in'),
             ('data', 'uint8', 8, 'in')],
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
'name': ('WritePageType2', 'write_page_type2'), 
'elements': [('page', 'uint8', 1, 'in'),
             ('data', 'uint8', 4, 'in')],
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
'name': ('ReadPage', 'read_page'), 
'elements': [('target_type', 'uint8', 1, 'in'),
             ('page', 'uint8', 1, 'in')],
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
'name': ('GetPageMifareClassic', 'get_page_mifare_classic'), 
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
'type': 'function',
'name': ('GetPageType1', 'get_page_mifare_classic'), 
'elements': [('data', 'uint8', 8, 'out')],
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
'name': ('GetPageType2', 'get_page_mifare_classic'), 
'elements': [('data', 'uint8', 4, 'out')],
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
'name': ('NewPassiveTargetID', 'new_passive_target_id'), 
'elements': [('target_type', 'uint8', 1, 'out'),
             ('tid_length', 'uint16', 1, 'out'),
             ('tid', 'uint8', 7, 'out')],
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

com['packets'].append({
'type': 'function',
'name': ('StateChanged', 'state_changed'), 
'elements': [('state', 'uint8', 1, 'out'),
             ('error', 'uint16', 1, 'out')],
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

