# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# RGB LED Button Bricklet communication config

from commonconstants import *

com = {
    'author': 'Bastian Nordmeyer <bastian@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 282,
    'name': 'RGB LED Button',
    'display_name': 'RGB LED Button',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Push button with built-in RGB LED',
        'de': 'Taster mit eingebauter RGB LED'
    },
    'released': True,
    'documented': True,
    'discontinued': False,
    'features': [
        'comcu_bricklet',
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append({
'name': 'Button State',
'type': 'uint8',
'constants': [('Pressed', 0),
              ('Released', 1)]
})

com['packets'].append({
'type': 'function',
'name': 'Set Color',
'elements': [('Red', 'uint8', 1, 'in'),
             ('Green', 'uint8', 1, 'in'),
             ('Blue', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the color of the LED.

By default the LED is off (0, 0, 0).
""",
'de':
"""
Setzt die LED-Farbe.

Standardmäßig ist die LED aus (0, 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Color',
'elements': [('Red', 'uint8', 1, 'out'),
             ('Green', 'uint8', 1, 'out'),
             ('Blue', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the LED color as set by :func:`Set Color`.
""",
'de':
"""
Gibt die LED-Farbe zurück, wie von :func:`Set Color` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Button State',
'elements': [('State', 'uint8', 1, 'out', {'constant_group': 'Button State'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current state of the button (either pressed or released).
""",
'de':
"""
Gibt den aktuellen Zustand des Knopfes zurück (entweder gedrückt oder nicht gedrückt).
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Button State Changed',
'elements': [('State', 'uint8', 1, 'out', {'constant_group': 'Button State'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered every time the button state changes from pressed to
released or from released to pressed.

The :word:`parameter` is the current state of the button.
""",
'de':
"""
Dieser Callback wird jedes mal ausgelöst, wenn sich der Zustand es Knopfes ändert
von gedrückt zu nicht gedrückt oder anders herum

Das :word:`parameter` ist der aktuelle Zustand des Knopfes.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Color Calibration',
'elements': [('Red', 'uint8', 1, 'in'),
             ('Green', 'uint8', 1, 'in'),
             ('Blue', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets a color calibration. Some colors appear brighter then others,
so a calibration may be necessary for nice uniform colors.

The values range from 0% to 100%.

The calibration is saved in flash. You don't need to call this
function on every startup.

Default value is (100, 100, 55).
""",
'de':
"""
Setzt die Farbwert-Kalibrierung. Einige Farben erscheinen heller als andere,
daher kann eine Kalibrierung nötig sein um gleichmäßige Farben zu erzielen.

Der Wertebereich ist 0% bis 100%

Die Kalibrierung wird im Flash des Bricklets gespeichert und muss daher nicht
bei jedem Start erneut vorgenommen werden.

Standardwert ist (100, 100, 55).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Color Calibration',
'elements': [('Red', 'uint8', 1, 'out'),
             ('Green', 'uint8', 1, 'out'),
             ('Blue', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the color calibration as set by :func:`Set Color Calibration`.
""",
'de':
"""
Gibt die Farbwert-Kalibrierung zurück, wie von :func:`Set Color Calibration` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple Button',
'functions': [('getter', ('Get Button State', 'button state'), [(('State', 'State'), 'uint8:constant', 1, None, None, None)], [])]
})

com['examples'].append({
'name': 'Simple Color',
'functions': [('setter', 'Set Color', [('uint8', 0), ('uint8', 170), ('uint8', 234)], 'Set light blue color', None)]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Button State Changed', 'button state changed'), [(('State', 'State'), 'uint8:constant', 1, None, None, None)], None, None)]
})

def percent_type_to_int(name):
    return '(int)({}.doubleValue() * 255.0 / 100.0)'.format(name)

com['openhab'] = {
    'imports': oh_generic_trigger_channel_imports() + ['org.eclipse.smarthome.core.library.types.HSBType'],
    'channels': [{
            'id': 'Color',
            'type': 'Color',

            'setters': [{
                'packet': 'Set {title_words}',
                'packet_params': [percent_type_to_int('cmd.getRed()'), percent_type_to_int('cmd.getGreen()'), percent_type_to_int('cmd.getBlue()'),]}],
            'setter_command_type': "HSBType",

            'getters': [{
                'packet': 'Get {title_words}',
                'transform': 'HSBType.fromRGB(value.red, value.green, value.blue)'}],
        },
        {
            'id': 'Button',
            'label': 'Button',
            'type': 'system.rawbutton',
            'getters': [{
                'packet': 'Get Button State',
                'transform': 'value == BrickletRGBLEDButton.BUTTON_STATE_PRESSED ? CommonTriggerEvents.PRESSED : CommonTriggerEvents.RELEASED'}],

            'callbacks': [{
                'packet': 'Button State Changed',
                'transform': 'state == BrickletRGBLEDButton.BUTTON_STATE_PRESSED ? CommonTriggerEvents.PRESSED : CommonTriggerEvents.RELEASED'}],

            'is_trigger_channel': True
        }
    ],
    'channel_types': [
        oh_generic_channel_type('Color', 'Color', 'LED Color',
                     read_only=False)
    ]
}
