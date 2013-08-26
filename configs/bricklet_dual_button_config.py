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
'elements': [('led_l', 'uint8', 1, 'in', ('LEDState', 'led_state', [('AutoToggleOn', 'auto_toggle_on', 0),
                                                                    ('AutoToggleOff', 'auto_toggle_off', 1),
                                                                    ('On', 'on', 2),
                                                                    ('Off', 'off', 3)])),
             ('led_r', 'uint8', 1, 'in', ('LEDState', 'led_state', [('AutoToggleOn', 'auto_toggle_on', 0),
                                                                    ('AutoToggleOff', 'auto_toggle_off', 1),
                                                                    ('On', 'on', 2),
                                                                    ('Off', 'off', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the state of the LEDs. Possible states are:

* AutoToggleOn: Enables auto toggle with enabled LED.
* AutoToggleOff: Activates auto toggle with disabled LED.
* On: Enables LED (auto toggle is disabled).
* Off: Disables LED (auto toggle is disabled).

In auto toggle mode the LED is toggled automatically whenever the
button is pressed.
""",
'de':
"""
Setzt den Zustand der LEDs. Möglich Zustände sind:

* AutoToggleOn: Aktiviert auto toggle und aktiviert LED
* AutoToggleOff: Aktiviert auto toggle und deaktiviert LED.
* On: Aktiviert LED (auto toggle is deaktiviert).
* Off: Deaktiviert LED (auto toggle is deaktiviert).

Im auto toggle Modus wechselt die LED automatisch zwischen
aus und an wenn der Taster gedrückt wird.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetLEDState', 'get_led_state'), 
'elements': [('led_l', 'uint8', 1, 'out', ('LEDState', 'led_state', [('AutoToggleOn', 'auto_toggle_on', 0),
                                                                     ('AutoToggleOff', 'auto_toggle_off', 1),
                                                                     ('On', 'on', 2),
                                                                     ('Off', 'off', 3)])),
             ('led_r', 'uint8', 1, 'out', ('LEDState', 'led_state', [('AutoToggleOn', 'auto_toggle_on', 0),
                                                                     ('AutoToggleOff', 'auto_toggle_off', 1),
                                                                     ('On', 'on', 2),
                                                                     ('Off', 'off', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current state of the LEDs, as set by :func:`SetLEDState`.
""",
'de':
"""
Gibt den aktuellen Zustand der LEDs zurück, wie von :func:`SetLEDState` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetButtonState', 'get_button_state'), 
'elements': [('button_l', 'uint8', 1, 'out', ('ButtonState', 'button_state', [('Pressed', 'pressed', 0),
                                                                             ('Released', 'released', 1)])),
             ('button_r', 'uint8', 1, 'out', ('ButtonState', 'button_state', [('Pressed', 'pressed', 0),
                                                                             ('Released', 'released', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current state for both buttons. Possible states are
pressed and released.
""",
'de':
"""
Gibt den aktuellen Zustand beider Taster zurück. Mögliche
Zustände sind pressed (gedrückt) und released (losgelassen).
"""
}]
})


com['packets'].append({
'type': 'callback',
'name': ('StateChanged', 'state_changed'), 
'elements': [('button_l', 'uint8', 1, 'out', ('ButtonState', 'button_state', [('Pressed', 'pressed', 0),
                                                                             ('Released', 'released', 1)])),
             ('button_r', 'uint8', 1, 'out', ('ButtonState', 'button_state', [('Pressed', 'pressed', 0),
                                                                             ('Released', 'released', 1)])),
             ('led_l', 'uint8', 1, 'out', ('LEDState', 'led_state', [('AutoToggleOn', 'auto_toggle_on', 0),
                                                                    ('AutoToggleOff', 'auto_toggle_off', 1),
                                                                    ('On', 'on', 2),
                                                                    ('Off', 'off', 3)])),
             ('led_r', 'uint8', 1, 'out', ('LEDState', 'led_state', [('AutoToggleOn', 'auto_toggle_on', 0),
                                                                    ('AutoToggleOff', 'auto_toggle_off', 1),
                                                                    ('On', 'on', 2),
                                                                    ('Off', 'off', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called whenever a button is pressed. 

Possible states for buttons are pressed and released.

Possible states for leds are:

* AutoToggleOn: Auto toggle enabled and LED on.
* AutoToggleOff: Auto toggle emabled and LED off.
* On: LED on (auto toggle ist disabled).
* Off: LED off (auto toggle ist disabled).
""",
'de':
"""
Dieser Callback wird aufgerufen wenn einer der Taster gedrückt wird.

Mögliche Zustände der Taster sind pressed (gedrückt) und 
released (losgelassen).

Mögliche Zustände der LEDs sind:

* AutoToggleOn: Auto toggle aktiv und LED an.
* AutoToggleOff: Auto toggle aktiv und LED aus.
* On: Aktiviert LED (auto toggle ist deaktiviert).
* Off: Deaktiviert LED (auto toggle ist deaktiviert).
"""
}]
})
