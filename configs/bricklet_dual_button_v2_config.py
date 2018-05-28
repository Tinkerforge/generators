# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Dual Button Bricklet 2.0 communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2119,
    'name': 'Dual Button V2',
    'display_name': 'Dual Button 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Two tactile buttons with built-in blue LEDs',
        'de': 'Zwei Taster mit eingebauten blauen LEDs'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'discontinued': False,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Set LED State',
'elements': [('LED L', 'uint8', 1, 'in', ('LED State', [('Auto Toggle On', 0),
                                                        ('Auto Toggle Off', 1),
                                                        ('On', 2),
                                                        ('Off', 3)])),
             ('LED R', 'uint8', 1, 'in', ('LED State', [('Auto Toggle On', 0),
                                                        ('Auto Toggle Off', 1),
                                                        ('On', 2),
                                                        ('Off', 3)]))],
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
of the other LED, you can get the state with :func:`Get LED State` or you
can use :func:`Set Selected LED State`.

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
nicht bekannt ist, dann kann der Zustand mit :func:`Get LED State` ausgelesen werden oder
es kann :func:`Set Selected LED State` genutzt werden.

Der Standardwert ist (1, 1).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get LED State',
'elements': [('LED L', 'uint8', 1, 'out', ('LED State', [('Auto Toggle On', 0),
                                                         ('Auto Toggle Off', 1),
                                                         ('On', 2),
                                                         ('Off', 3)])),
             ('LED R', 'uint8', 1, 'out', ('LED State', [('Auto Toggle On', 0),
                                                         ('Auto Toggle Off', 1),
                                                         ('On', 2),
                                                         ('Off', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current state of the LEDs, as set by :func:`Set LED State`.
""",
'de':
"""
Gibt den aktuellen Zustand der LEDs zurück, wie von :func:`Set LED State` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Button State',
'elements': [('Button L', 'uint8', 1, 'out', ('Button State', [('Pressed', 0),
                                                               ('Released', 1)])),
             ('Button R', 'uint8', 1, 'out', ('Button State', [('Pressed', 0),
                                                               ('Released', 1)]))],
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
'name': 'State Changed',
'elements': [('Button L', 'uint8', 1, 'out', ('Button State', [('Pressed', 0),
                                                               ('Released', 1)])),
             ('Button R', 'uint8', 1, 'out', ('Button State', [('Pressed', 0),
                                                               ('Released', 1)])),
             ('LED L', 'uint8', 1, 'out', ('LED State', [('Auto Toggle On', 0),
                                                         ('Auto Toggle Off', 1),
                                                         ('On', 2),
                                                         ('Off', 3)])),
             ('LED R', 'uint8', 1, 'out', ('LED State', [('Auto Toggle On', 0),
                                                         ('Auto Toggle Off', 1),
                                                         ('On', 2),
                                                         ('Off', 3)]))],
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

This callback can be enabled with :func:`Set State Changed Callback Configuration`.
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

Dieser Callback kann über :func:`Set State Changed Callback Configuration` aktiviert werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Selected LED State',
'elements': [('LED', 'uint8', 1, 'in', ('LED', [('Left', 0),
                                                ('Right', 1)])),
             ('State', 'uint8', 1, 'in', ('LED State', [('Auto Toggle On', 0),
                                                        ('Auto Toggle Off', 1),
                                                        ('On', 2),
                                                        ('Off', 3)])),
],
'since_firmware': [1, 0, 0],
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



com['packets'].append({
'type': 'function',
'name': 'Set State Changed Callback Configuration',
'elements': [('Enabled', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
If you enable this callback, the :cb:`State Changed` callback is triggered
every time a button is pressed/released

By default this callback is disabled.
""",
'de':
"""
Wenn dieser Callback aktiviert ist, wird der :cb:`State Changed` Callback
jedes mal ausgelöst wenn ein Taster gedrückt/losgelassen wird.

Standardmäßig ist dieser Callback deaktiviert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get State Changed Callback Configuration',
'elements': [('Enabled', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the configuration as set by :func:`Set State Changed Callback Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set State Changed Callback Configuration`
gesetzt.
"""
}]
})


com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('State Changed', 'state changed'), [(('Button L', 'Left Button'), 'uint8:constant', 1, None, None, None), (('Button R', 'Right Button'), 'uint8:constant', 1, None, None, None), (('LED L', None), 'uint8', 1, None, None, None), (('LED R', None), 'uint8', 1, None, None, None)], None, None)]
})
