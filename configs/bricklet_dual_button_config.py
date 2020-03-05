# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Dual Button Bricklet communication config

from openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 230,
    'name': 'Dual Button',
    'display_name': 'Dual Button',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Two tactile buttons with built-in blue LEDs',
        'de': 'Zwei Taster mit eingebauten blauen LEDs'
    },
    'released': True,
    'documented': True,
    'discontinued': False, # selling remaining stock, replaced by Dual Button Bricklet 2.0
    'features': [
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append({
'name': 'LED State',
'type': 'uint8',
'constants': [('Auto Toggle On', 0),
              ('Auto Toggle Off', 1),
              ('On', 2),
              ('Off', 3)]
})

com['constant_groups'].append({
'name': 'Button State',
'type': 'uint8',
'constants': [('Pressed', 0),
              ('Released', 1)]
})

com['constant_groups'].append({
'name': 'LED',
'type': 'uint8',
'constants': [('Left', 0),
              ('Right', 1)]
})

com['packets'].append({
'type': 'function',
'name': 'Set LED State',
'elements': [('LED L', 'uint8', 1, 'in', {'constant_group': 'LED State', 'default': 1}),
             ('LED R', 'uint8', 1, 'in', {'constant_group': 'LED State', 'default': 1})],
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
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get LED State',
'elements': [('LED L', 'uint8', 1, 'out', {'constant_group': 'LED State', 'default': 1}),
             ('LED R', 'uint8', 1, 'out', {'constant_group': 'LED State', 'default': 1})],
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
'elements': [('Button L', 'uint8', 1, 'out', {'constant_group': 'Button State'}),
             ('Button R', 'uint8', 1, 'out', {'constant_group': 'Button State'})],
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
'elements': [('Button L', 'uint8', 1, 'out', {'constant_group': 'Button State'}),
             ('Button R', 'uint8', 1, 'out', {'constant_group': 'Button State'}),
             ('LED L', 'uint8', 1, 'out', {'constant_group': 'LED State'}),
             ('LED R', 'uint8', 1, 'out', {'constant_group': 'LED State'})],
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
'name': 'Set Selected LED State',
'elements': [('LED', 'uint8', 1, 'in', {'constant_group': 'LED'}),
             ('State', 'uint8', 1, 'in', {'constant_group': 'LED State'}),
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

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('State Changed', 'state changed'), [(('Button L', 'Left Button'), 'uint8:constant', 1, None, None, None), (('Button R', 'Right Button'), 'uint8:constant', 1, None, None, None), (('LED L', None), 'uint8:constant', 1, None, None, None), (('LED R', None), 'uint8:constant', 1, None, None, None)], None, None)]
})


com['openhab'] = {
    'imports': oh_generic_trigger_channel_imports() + oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.OnOffType'],
    'params': [
        {
            'packet': 'Set LED State',
            'element': 'LED L',

            'name': 'Left LED State',
            'type': 'integer',
            'default': 1,

            'label': 'Left LED State',
            'description': """<ul><li>Auto Toggle - Default On: Enables auto toggle. LED initially enabled</li><li>Auto Toggle - Default Off: Enables auto toggle. LED initially disabled</li><li>Channel - Default On: Creates a control channel. LED initially enabled.</li><li>Channel - Default Off: Creates a control channel. LED initially disabled.</li></ul>""",
            'options':  [('Auto Toggle - Default On', 0),
                         ('Auto Toggle - Default Off', 1),
                         ('Channel - Default On', 2),
                         ('Channel - Default Off', 3)],
        },
        {
            'packet': 'Set LED State',
            'element': 'LED R',

            'name': 'Right LED State',
            'type': 'integer',
            'default': 1,

            'label': 'Right LED State',
            'description': """<ul><li>Auto Toggle - Default On: Enables auto toggle. LED initially enabled</li><li>Auto Toggle - Default Off: Enables auto toggle. LED initially disabled</li><li>Channel - Default On: Creates a control channel. LED initially enabled.</li><li>Channel - Default Off: Creates a control channel. LED initially disabled.</li></ul>""",
            'options': [('Auto Toggle - Default On', 0),
                        ('Auto Toggle - Default Off', 1),
                        ('Channel - Default On', 2),
                        ('Channel - Default Off', 3)],
        }
    ],
    'init_code': 'this.setLEDState(cfg.leftLEDState.shortValue(), cfg.rightLEDState.shortValue());',
    'channels': [
        {
            'id': 'Left Button',
            'label': 'Left Button',
            'description': 'This channel triggers if the right button is pressed or released',
            'type': 'system.rawbutton',
            'getters': [{
                'packet': 'Get Button State',
                'transform': 'value.buttonL == BrickletDualButton.BUTTON_STATE_PRESSED ? CommonTriggerEvents.PRESSED : CommonTriggerEvents.RELEASED'}],

            'callbacks': [{
                'packet': 'State Changed',
                'transform': 'buttonL == BrickletDualButton.BUTTON_STATE_PRESSED ? CommonTriggerEvents.PRESSED : CommonTriggerEvents.RELEASED'}],

            'is_trigger_channel': True
        },
        {
            'id': 'Right Button',
            'label': 'Right Button',
            'description': 'This channel triggers if the right button is pressed or released',
            'type': 'system.rawbutton',
            'getters': [{
                'packet': 'Get Button State',
                'transform': 'value.buttonR == BrickletDualButton.BUTTON_STATE_PRESSED ? CommonTriggerEvents.PRESSED : CommonTriggerEvents.RELEASED'}],

            'callbacks': [{
                'packet': 'State Changed',
                'transform': 'buttonR == BrickletDualButton.BUTTON_STATE_PRESSED ? CommonTriggerEvents.PRESSED : CommonTriggerEvents.RELEASED'}],

            'is_trigger_channel': True
        }, {
            'id': 'Left LED',
            'label': 'Left LED',
            'type': 'Left LED',

            'predicate': 'cfg.leftLEDState > 1',

            'getters': [{
                'packet': 'Get LED State',
                'transform': 'value.ledL == BrickletDualButton.LED_STATE_ON ? OnOffType.ON : OnOffType.OFF'}],

            'setters': [{
                'packet': 'Set Selected LED State',
                'packet_params': ['BrickletDualButton.LED_LEFT', 'cmd == OnOffType.ON? BrickletDualButton.LED_STATE_ON : BrickletDualButton.LED_STATE_OFF'],
                'command_type': 'OnOffType'
            }],

        }, {
            'id': 'Right LED',
            'label': 'Right LED',
            'type': 'Right LED',

            'predicate': 'cfg.rightLEDState > 1',

            'getters': [{
                'packet': 'Get LED State',
                'transform': 'value.ledR == BrickletDualButton.LED_STATE_ON ? OnOffType.ON : OnOffType.OFF'}],

            'setters': [{
                'packet': 'Set Selected LED State',
                'packet_params': ['BrickletDualButton.LED_RIGHT', 'cmd == OnOffType.ON? BrickletDualButton.LED_STATE_ON : BrickletDualButton.LED_STATE_OFF'],
                'command_type': 'OnOffType'
            }],

        },
    ],
    'channel_types': [
        oh_generic_channel_type('Left LED', 'Switch', 'Left LED',
                    update_style=None,
                    description='Controls the left LED.'),
        oh_generic_channel_type('Right LED', 'Switch', 'Right LED',
                    update_style=None,
                    description='Controls the right LED.'),
    ],
    'actions': ['Get LED State', 'Get Button State']
}
