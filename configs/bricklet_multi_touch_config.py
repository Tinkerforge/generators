# -*- coding: utf-8 -*-

# Multi Touch Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 234,
    'name': ('MultiTouch', 'multi_touch', 'Multi Touch'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device with 12 touch sensors',
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetTouchState', 'get_touch_state'), 
'elements': [('state', 'uint16', 1, 'out')],
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
'name': ('TouchState', 'touch_state'), 
'elements': [('state', 'uint16', 1, 'out')],
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
