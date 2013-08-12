# -*- coding: utf-8 -*-

# Hall Effect Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 240,
    'name': ('HallEffect', 'hall_effect', 'Hall Effect'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device that detects presence of magnetic field via hall effect',
    'released': False,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetValue', 'get_value'),
'elements': [('value', 'bool', 1, 'out')],
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
'name': ('GetEdgeCount', 'get_edge_count'),
'elements': [('reset_counter', 'bool', 1, 'in'),
             ('count', 'uint32', 1, 'out')],
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
'name': ('SetEdgeCountConfig', 'set_edge_count_config'),
'elements': [('edge_type', 'uint8', 1, 'in'),
             ('debounce', 'uint8', 1, 'in')],
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
'name': ('GetEdgeCountConfig', 'get_edge_count_config'),
'elements': [('edge_type', 'uint8', 1, 'out'),
             ('debounce', 'uint8', 1, 'out')],
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
'name': ('SetEdgeInterrupt', 'set_edge_interrupt'),
'elements': [('count', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Interrupt every count edges
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetEdgeInterrupt', 'get_edge_interrupt'),
'elements': [('count', 'uint32', 1, 'out')],
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
'name': ('SetEdgeCountCallbackPeriod', 'set_edge_count_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`EdgeCount` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`EdgeCount` is only triggered if the edge count has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`EdgeCount` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`EdgeCount` wird nur ausgelöst wenn sich die Flankenzählung seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetEdgeCountCallbackPeriod', 'get_edge_count_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetEdgeCountCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetEdgeCountCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('EdgeInterrupt', 'edge_interrupt'),
'elements': [('count', 'uint32', 1, 'out'),
             ('value', 'bool', 1, 'out')],
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
'type': 'callback',
'name': ('EdgeCount', 'edge_count'), 
'elements': [('count', 'uint32', 1, 'out'),
             ('value', 'bool', 1, 'out')],
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
