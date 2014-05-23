# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# NFC/RFID Bricklet communication config

STATE_IDLE_MASK = (1 << 7)
STATE_ERROR_MASK = ((1 << 7) | (1 << 6))

STATE_INITIALIZATION = 0
STATE_IDLE = STATE_IDLE_MASK
STATE_ERROR = STATE_ERROR_MASK
STATE_REQUEST_TAG_ID = 2
STATE_REQUEST_TAG_ID_READY = STATE_IDLE_MASK | STATE_REQUEST_TAG_ID
STATE_REQUEST_TAG_ID_ERROR = STATE_ERROR_MASK | STATE_REQUEST_TAG_ID
STATE_AUTHENTICATING_MIFARE_CLASSIC_PAGE = 3
STATE_AUTHENTICATING_MIFARE_CLASSIC_PAGE_READY = STATE_IDLE_MASK | STATE_AUTHENTICATING_MIFARE_CLASSIC_PAGE
STATE_AUTHENTICATING_MIFARE_CLASSIC_PAGE_ERROR = STATE_ERROR_MASK | STATE_AUTHENTICATING_MIFARE_CLASSIC_PAGE
STATE_WRITE_PAGE = 4
STATE_WRITE_PAGE_READY = STATE_IDLE_MASK | STATE_WRITE_PAGE
STATE_WRITE_PAGE_ERROR = STATE_ERROR_MASK | STATE_WRITE_PAGE
STATE_REQUEST_PAGE = 5
STATE_REQUEST_PAGE_READY = STATE_IDLE_MASK | STATE_REQUEST_PAGE
STATE_REQUEST_PAGE_ERROR = STATE_ERROR_MASK | STATE_REQUEST_PAGE

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
'elements': [('tag_type', 'uint8', 1, 'in', ('TagType', 'tag_type', [('MifareClassic', 'mifare_classic', 0),
                                                                     ('Type1', 'type1', 1),
                                                                     ('Type2', 'type2', 2)]))],
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
'elements': [('tag_type', 'uint8', 1, 'out', ('TagType', 'tag_type', [('MifareClassic', 'mifare_classic', 0),
                                                                      ('Type1', 'type1', 1),
                                                                      ('Type2', 'type2', 2)])),
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
'elements': [('state', 'uint8', 1, 'out', ('State', 'state', [('Initialization', 'initialization', STATE_INITIALIZATION),
                                                              ('Idle', 'idle', STATE_IDLE),
                                                              ('Error', 'error', STATE_ERROR),
                                                              ('RequestTagID', 'request_tag_id', STATE_REQUEST_TAG_ID),
                                                              ('RequestTagIDReady', 'request_tag_id_ready', STATE_REQUEST_TAG_ID_READY),
                                                              ('RequestTagIDError', 'request_tag_id_error', STATE_REQUEST_TAG_ID_ERROR),
                                                              ('AuthenticatingMifareClassicPage', 'authenticating_mifare_classic_page', STATE_AUTHENTICATING_MIFARE_CLASSIC_PAGE),
                                                              ('AuthenticatingMifareClassicPageReady', 'authenticating_mifare_classic_page_ready', STATE_AUTHENTICATING_MIFARE_CLASSIC_PAGE_READY),
                                                              ('AuthenticatingMifareClassicPageError', 'authenticating_mifare_classic_page_error', STATE_AUTHENTICATING_MIFARE_CLASSIC_PAGE_ERROR),
                                                              ('WritePage', 'write_page', STATE_WRITE_PAGE),
                                                              ('WritePageReady', 'write_page_ready', STATE_WRITE_PAGE_READY),
                                                              ('WritePageError', 'write_page_error', STATE_WRITE_PAGE_ERROR),
                                                              ('RequestPage', 'request_page', STATE_REQUEST_PAGE),
                                                              ('RequestPageReady', 'request_page_ready', STATE_REQUEST_PAGE_READY),
                                                              ('RequestPageError', 'request_page_error', STATE_REQUEST_PAGE_ERROR)])),
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
             ('key_number', 'uint8', 1, 'in', ('Key', 'key', [('A', 'a', 0),
                                                              ('B', 'b', 1)])),
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
'elements': [('state', 'uint8', 1, 'out', ('State', 'state', [('Initialization', 'initialization', STATE_INITIALIZATION),
                                                              ('Idle', 'idle', STATE_IDLE),
                                                              ('Error', 'error', STATE_ERROR),
                                                              ('RequestTagID', 'request_tag_id', STATE_REQUEST_TAG_ID),
                                                              ('RequestTagIDReady', 'request_tag_id_ready', STATE_REQUEST_TAG_ID_READY),
                                                              ('RequestTagIDError', 'request_tag_id_error', STATE_REQUEST_TAG_ID_ERROR),
                                                              ('AuthenticatingMifareClassicPage', 'authenticating_mifare_classic_page', STATE_AUTHENTICATING_MIFARE_CLASSIC_PAGE),
                                                              ('AuthenticatingMifareClassicPageReady', 'authenticating_mifare_classic_page_ready', STATE_AUTHENTICATING_MIFARE_CLASSIC_PAGE_READY),
                                                              ('AuthenticatingMifareClassicPageError', 'authenticating_mifare_classic_page_error', STATE_AUTHENTICATING_MIFARE_CLASSIC_PAGE_ERROR),
                                                              ('WritePage', 'write_page', STATE_WRITE_PAGE),
                                                              ('WritePageReady', 'write_page_ready', STATE_WRITE_PAGE_READY),
                                                              ('WritePageError', 'write_page_error', STATE_WRITE_PAGE_ERROR),
                                                              ('RequestPage', 'request_page', STATE_REQUEST_PAGE),
                                                              ('RequestPageReady', 'request_page_ready', STATE_REQUEST_PAGE_READY),
                                                              ('RequestPageError', 'request_page_error', STATE_REQUEST_PAGE_ERROR)])),
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

