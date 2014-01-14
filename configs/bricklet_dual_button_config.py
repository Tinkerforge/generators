# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Dual Button Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 230,
    'name': ('DualButton', 'dual_button', 'Dual Button'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device with two buttons and two LEDs',
    'released': True,
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

* 0 = AutoToggleOn: Enables auto toggle with initially enabled LED.
* 1 = AutoToggleOff: Activates auto toggle with initially disabled LED.
* 2 = On: Enables LED (auto toggle is disabled).
* 3 = Off: Disables LED (auto toggle is disabled).

In auto toggle mode the LED is toggled automatically at each press of a button.

If you just want to set one of the LEDs and don't know the current state
of the other LED, you can get the state with :func:`GetLEDState` or you
can use :func:`SetSelectedLEDState`.

The default value is (1, 1).
""",
'de':
"""
Setzt den Zustand der LEDs. Möglich Zustände sind:

* 0 = AutoToggleOn: Aktiviert Auto-Toggle und anfänglich aktiviert LED
* 1 = AutoToggleOff: Aktiviert Auto-Toggle und anfänglich deaktiviert LED.
* 2 = On: Aktiviert LED (Auto-Toggle is deaktiviert).
* 3 = Off: Deaktiviert LED (Auto-Toggle is deaktiviert).

Im Auto-Toggle Modus wechselt die LED automatisch zwischen aus und an bei jedem
Tasterdruck.

Wenn nur eine der LEDs gesetzt werden soll und der aktuelle Zustand der anderen LED
nicht bekannt ist, dann kann der Zustand mit :func:`GetLEDState` ausgelesen werden oder
es kann :func:`SetSelectedLEDState` genutzt werden.

Der Standardwert ist (1, 1).
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
Returns the current state for both buttons. Possible states are:

* 0 = pressed
* 1 = released
""",
'de':
"""
Gibt den aktuellen Zustand beider Taster zurück. Mögliche
Zustände sind:

* 0 = pressed (gedrückt)
* 1 = released (losgelassen)
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

Possible states for buttons are:

* 0 = pressed
* 1 = released

Possible states for LEDs are:

* 0 = AutoToggleOn: Auto toggle enabled and LED on.
* 1 = AutoToggleOff: Auto toggle enabled and LED off.
* 2 = On: LED on (auto toggle is disabled).
* 3 = Off: LED off (auto toggle is disabled).
""",
'de':
"""
Dieser Callback wird aufgerufen wenn einer der Taster gedrückt wird.

Mögliche Zustände der Taster sind:

* 0 = pressed (gedrückt)
* 1 = released (losgelassen)

Mögliche Zustände der LEDs sind:

* 0 = AutoToggleOn: Auto-Toggle aktiv und LED an.
* 1 = AutoToggleOff: Auto-Toggle aktiv und LED aus.
* 2 = On: Aktiviert LED (Auto-Toggle ist deaktiviert).
* 3 = Off: Deaktiviert LED (Auto-Toggle ist deaktiviert).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetSelectedLEDState', 'set_selected_led_state'), 
'elements': [('led', 'uint8', 1, 'in', ('LED', 'led', [('Left', 'left', 0),
                                                       ('Right', 'right', 1)])),
             ('state', 'uint8', 1, 'in', ('LEDState', 'led_state', [('AutoToggleOn', 'auto_toggle_on', 0),
                                                                    ('AutoToggleOff', 'auto_toggle_off', 1),
                                                                    ('On', 'on', 2),
                                                                    ('Off', 'off', 3)])),
],
'since_firmware': [2, 0, 0],
'doc': ['af', {
'en':
"""
Sets the state of the selected LED (0 or 1). 

The other LED remains untouched.
""",
'de':
"""
Setzt den Zustand der selektierten LED (0 oder 1).

Die andere LED bleibt unangetastet.
"""
}]
})
