# -*- coding: utf-8 -*-

# LCD 16x2 Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'version': [1, 0, 0],
    'type': 'Bricklet',
    'name': ('LCD16x2', 'lcd_16x2'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for controlling a LCD with 2 lines a 16 characters',
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('WriteLine', 'write_line'), 
'elements': [('line', 'uint8', 1, 'in'),
             ('position', 'uint8', 1, 'in'),
             ('text', 'string', 16, 'in')],
'doc': ['bm', {
'en':
"""
Writes text to a specific line (0 to 1) with a specific position 
(0 to 15). The text can have a maximum of 16 characters.

For example: (0, 5, "Hello") will write *Hello* in the middle of the
first line of the display.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('ClearDisplay', 'clear_display'), 
'elements': [],
'doc': ['bm', {
'en':
"""
Deletes all characters from the display.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('BacklightOn', 'backlight_on'), 
'elements': [],
'doc': ['bm', {
'en':
"""
Turns the backlight on.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('BacklightOff', 'backlight_off'), 
'elements': [],
'doc': ['bm', {
'en':
"""
Turns the backlight off.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('IsBacklightOn', 'is_backlight_on'), 
'elements': [('backlight', 'bool', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns true if the backlight is on and false otherwise.
""",
'de':
"""
"""
}]
})



com['packets'].append({
'type': 'function',
'name': ('SetConfig', 'set_config'), 
'elements': [('cursor', 'bool', 1, 'in'),
             ('blinking', 'bool', 1, 'in')],
'doc': ['am', {
'en':
"""
Configures if the cursor (shown as "_") should be visible and if it
should be blinking (shown as a blinking block). The cursor position
is one character behind the the last text written with 
:func:`WriteLine`.

The default is (false, false).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetConfig', 'get_config'), 
'elements': [('cursor', 'bool', 1, 'out'),
             ('blinking', 'bool', 1, 'out')],
'doc': ['am', {
'en':
"""
Returns the configuration as set by :func:`SetConfig`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('IsButtonPressed', 'is_button_pressed'), 
'elements': [('button', 'uint8', 1, 'in'),
             ('pressed', 'bool', 1, 'out')],
'doc': ['am', {
'en':
"""
Returns true if the button (0 to 2) is pressed. If you want to react
on button presses and releases it is recommended to use the
:func:`ButtonPressed` and :func:`ButtonReleased` callbacks.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('ButtonPressed', 'button_pressed'), 
'elements': [('button', 'uint8', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered when a button is pressed. The :word:`parameter` is
the number of the button (0 to 2).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('ButtonReleased', 'button_released'), 
'elements': [('button', 'uint8', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered when a button is released. The :word:`parameter` is
the number of the button (0 to 2).
""",
'de':
"""
"""
}]
})
