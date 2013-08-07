# -*- coding: utf-8 -*-

# Tilt Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 239,
    'name': ('Tilt', 'tilt', 'Tilt'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for sensing tilt and vibration',
    'released': False,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetTiltState', 'get_tilt_state'),
'elements': [('state', 'uint8', 1, 'out', ('TiltState', 'tilt_state', [('Closed', 'closed', 0),
                                                                       ('Open', 'open', 1),
                                                                       ('ClosedVibrating', 'closed_vibrating', 2)]))],
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
'name': ('EnableTiltStateCallback', 'enable_tilt_state_callback'),
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
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
'name': ('DisableTiltStateCallback', 'disable_tilt_state_callback'),
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
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
'name': ('IsTiltStateCallbackEnabled', 'is_tilt_state_callback_enabled'),
'elements': [('enabled', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
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
'name': ('TiltState', 'tilt_state'), 
'elements': [('state', 'uint8', 1, 'out', ('TiltState', 'tilt_state', [('Closed', 'closed', 0),
                                                                       ('Open', 'open', 1),
                                                                       ('ClosedVibrating', 'closed_vibrating', 2)]))],
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
