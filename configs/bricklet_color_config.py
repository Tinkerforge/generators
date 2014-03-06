# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Color Bricklet communication config

com = {
    'author': 'Ishraq Ibne Ashraf <ishraq@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 243,
    'name': ('Color', 'color', 'Color'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for measuring color(RGB value) of objects',
    'released': False,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetColor', 'get_color'), 
'elements': [('r', 'uint16', 1, 'out'),
             ('g', 'uint16', 1, 'out'),
             ('b', 'uint16', 1, 'out'),
             ('c', 'uint16', 1, 'out')],
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
'name': ('SetColorCallbackPeriod', 'set_color_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
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
'name': ('GetColorCallbackPeriod', 'get_color_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
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
'name': ('SetColorCallbackThreshold', 'set_color_callback_threshold'), 
'elements': [('option', 'char', 1, 'in', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                  ('Outside', 'outside', 'o'),
                                                                                  ('Inside', 'inside', 'i'),
                                                                                  ('Smaller', 'smaller', '<'),
                                                                                  ('Greater', 'greater', '>')])), 
             ('min_r', 'uint16', 1, 'in'),
             ('max_r', 'uint16', 1, 'in'),
             ('min_g', 'uint16', 1, 'in'),
             ('max_g', 'uint16', 1, 'in'),
             ('min_b', 'uint16', 1, 'in'),
             ('max_b', 'uint16', 1, 'in'),
             ('min_c', 'uint16', 1, 'in'),
             ('max_c', 'uint16', 1, 'in')],
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
'name': ('GetColorCallbackThreshold', 'get_color_callback_threshold'), 
'elements': [('option', 'char', 1, 'out', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                   ('Outside', 'outside', 'o'),
                                                                                   ('Inside', 'inside', 'i'),
                                                                                   ('Smaller', 'smaller', '<'),
                                                                                   ('Greater', 'greater', '>')])), 
             ('min_r', 'uint16', 1, 'out'),
             ('max_r', 'uint16', 1, 'out'),
             ('min_g', 'uint16', 1, 'out'),
             ('max_g', 'uint16', 1, 'out'),
             ('min_b', 'uint16', 1, 'out'),
             ('max_b', 'uint16', 1, 'out'),
             ('min_c', 'uint16', 1, 'out'),
             ('max_c', 'uint16', 1, 'out')],
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
'name': ('SetDebouncePeriod', 'set_debounce_period'), 
'elements': [('debounce', 'uint32', 1, 'in')],
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
'name': ('GetDebouncePeriod', 'get_debounce_period'), 
'elements': [('debounce', 'uint32', 1, 'out')],
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
'name': ('Color', 'color'), 
'elements': [('r', 'uint16', 1, 'out'),
             ('g', 'uint16', 1, 'out'),
             ('b', 'uint16', 1, 'out'),
             ('c', 'uint16', 1, 'out')],
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
'name': ('ColorReached', 'color_reached'), 
'elements': [('r', 'uint16', 1, 'out'),
             ('g', 'uint16', 1, 'out'),
             ('b', 'uint16', 1, 'out'),
             ('c', 'uint16', 1, 'out')],
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
'name': ('LightOn', 'light_on'), 
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Turns the LED on.
""",
'de':
"""
Aktiviert die LED.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('LightOff', 'light_off'), 
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Turns the LED off.
""",
'de':
"""
Deaktiviert die LED.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('IsLightOn', 'is_light_on'), 
'elements': [('light', 'uint8', 1, 'out', ('Light', 'light', [('On', 'on', 0),
                                                              ('Off', 'off', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns *true* if the backlight is on and *false* otherwise.
""",
'de':
"""
Gibt *true* zurück wenn die LED aktiv ist, sonst *false*.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetConfig', 'set_config'), 
'elements': [('gain', 'uint8', 1, 'in', ('Gain', 'gain', [('1x', '1x', 0x0),
                                                          ('4x', '4x', 0x1),
                                                          ('16x', '16x', 0x2),
                                                          ('60x', '60x', 0x3)])),
             ('integration_time', 'uint8', 1, 'in', ('IntegrationTime', 'integration_time', [('2ms', '2ms', 0xFF),
                                                                                             ('24ms', '24ms', 0xF6),
                                                                                             ('101ms', '101ms', 0xD5),
                                                                                             ('154ms', '154ms', 0xC0),
                                                                                             ('700ms', '700ms', 0x00)]))],
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
'name': ('GetConfig', 'get_config'), 
'elements': [('gain', 'uint8', 1, 'out', ('Gain', 'gain', [('1x', '1x', 0x0),
                                                            ('4x', '4x', 0x1),
                                                            ('16x', '16x', 0x2),
                                                            ('60x', '60x', 0x3)])),
             ('integration_time', 'uint8', 1, 'out', ('IntegrationTime', 'integration_time', [('2ms', '2ms', 0xFF),
                                                                                              ('24ms', '24ms', 0xF6),
                                                                                              ('101ms', '101ms', 0xD5),
                                                                                              ('154ms', '154ms', 0xC0),
                                                                                              ('700ms', '700ms', 0x00)]))],
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

