# -*- coding: utf-8 -*-

# Dual Relay Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'version': [1, 0, 0],
    'type': 'Bricklet',
    'name': ('DualRelay', 'dual_relay'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for controlling two relays',
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('SetState', 'set_state'), 
'elements': [('relay1', 'bool', 1, 'in'),
             ('relay2', 'bool', 1, 'in')],
'doc': ['bm', {
'en':
"""
Sets the state of the relays, *true* means on and *false* means off. 
For example: (true, false) turns relay 1 on and relay 2 off.

If you just want to set one of the relays and don't know the current state
of the other relay, you can get the state with :func:`GetState`.

The default value is (false, false).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetState', 'get_state'), 
'elements': [('relay1', 'bool', 1, 'out'),
             ('relay2', 'bool', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns the state of the relays, *true* means on and *false* means off. 
""",
'de':
"""
"""
}]
})
