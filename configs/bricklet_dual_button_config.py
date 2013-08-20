# -*- coding: utf-8 -*-

# Dual Button Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 230,
    'name': ('DualButton', 'dual_button', 'Dual Button'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device with two buttons and two LEDs',
    'released': False,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('SetLEDState', 'set_led_state'), 
'elements': [('led1', 'uint8', 1, 'in', ('LEDState', 'led_state', [('AutoToggleOn', 'auto_toggle_on', 0),
                                                                   ('AutoToggleOff', 'auto_toggle_off', 1),
                                                                   ('On', 'on', 2),
                                                                   ('Off', 'off', 3)])),
             ('led2', 'uint8', 1, 'in', ('LEDState', 'led_state', [('AutoToggleOn', 'auto_toggle_on', 0),
                                                                   ('AutoToggleOff', 'auto_toggle_off', 1),
                                                                   ('On', 'on', 2),
                                                                   ('Off', 'off', 3)]))],
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
'name': ('GetLEDState', 'get_led_state'), 
'elements': [('led1', 'uint8', 1, 'out', ('LEDState', 'led_state', [('AutoToggleOn', 'auto_toggle_on', 0),
                                                                    ('AutoToggleOff', 'auto_toggle_off', 1),
                                                                    ('On', 'on', 2),
                                                                    ('Off', 'off', 3)])),
             ('led2', 'uint8', 1, 'out', ('LEDState', 'led_state', [('AutoToggleOn', 'auto_toggle_on', 0),
                                                                    ('AutoToggleOff', 'auto_toggle_off', 1),
                                                                    ('On', 'on', 2),
                                                                    ('Off', 'off', 3)]))],
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
'name': ('GetButtonState', 'get_button_state'), 
'elements': [('button1', 'uint8', 1, 'out', ('ButtonState', 'button_state', [('Pressed', 'pressed', 0),
                                                                             ('Released', 'released', 1)])),
             ('button2', 'uint8', 1, 'out', ('ButtonState', 'button_state', [('Pressed', 'pressed', 0),
                                                                             ('Released', 'released', 1)]))],
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
'elements': [('button1', 'uint8', 1, 'out', ('ButtonState', 'button_state', [('Pressed', 'pressed', 0),
                                                                             ('Released', 'released', 1)])),
             ('button2', 'uint8', 1, 'out', ('ButtonState', 'button_state', [('Pressed', 'pressed', 0),
                                                                             ('Released', 'released', 1)])),
             ('led1', 'uint8', 1, 'out', ('LEDState', 'led_state', [('AutoToggleOn', 'auto_toggle_on', 0),
                                                                    ('AutoToggleOff', 'auto_toggle_off', 1),
                                                                    ('On', 'on', 2),
                                                                    ('Off', 'off', 3)])),
             ('led2', 'uint8', 1, 'out', ('LEDState', 'led_state', [('AutoToggleOn', 'auto_toggle_on', 0),
                                                                    ('AutoToggleOff', 'auto_toggle_off', 1),
                                                                    ('On', 'on', 2),
                                                                    ('Off', 'off', 3)]))],
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
