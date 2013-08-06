# -*- coding: utf-8 -*-

# Tilt Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 239,
    'name': ('Tilt', 'tilt', 'Tilt'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for sensing inclination changes',
    'released': False,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetTiltState', 'get_tilt_state'),
'elements': [('state', 'uint8', 1, 'out', ('TiltState', 'tilt_state', [('Closed', 'closed', 0),
                                                                       ('Open', 'open', 1)]))],
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
'name': ('TiltStateChanged', 'tilt_state_changed'), 
'elements': [('state', 'uint8', 1, 'out', ('TiltState', 'tilt_state', [('Closed', 'closed', 0),
                                                                       ('Open', 'open', 1)]))],
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
