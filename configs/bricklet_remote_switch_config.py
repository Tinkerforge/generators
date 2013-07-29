# -*- coding: utf-8 -*-

# Remote Switch Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 235,
    'name': ('RemoteSwitch', 'remote_switch', 'Remote Switch'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device that controls mains switches remotely',
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('SwitchSocket', 'switch_socket'), 
'elements': [('house_code', 'uint8', 1, 'in'),
             ('receiver_code', 'uint8', 1, 'in'),
             ('switch_to', 'uint8', 1, 'in', ('SwitchTo', 'switch_to', [('Off', 'off', 0),
                                                                        ('On', 'on', 1)]))],
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
'name': ('GetSwitchingState', 'get_switching_state'), 
'elements': [('state', 'uint8', 1, 'out', ('SwitchingState', 'SwitchingState', [('Ready', 'ready', 0),
                                                                                ('Busy', 'busy', 1)]))],
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
'name': ('SwitchingDone', 'switching_done'), 
'elements': [],
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
'name': ('SetTries', 'set_tries'), 
'elements': [('tries', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
The default value is 5.
""",
'de':
"""
Der Standardwert ist 5.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetTries', 'get_tries'), 
'elements': [('tries', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the number of tries as set by :func:`SetTries`. 
""",
'de':
"""
Gibt die Anzahl der Versuche zurück, wie von :func:`SetTries` gesetzt.
"""
}]
})
