# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Joystick Bricklet 2.0 communication config

from openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2138,
    'name': 'Joystick V2',
    'display_name': 'Joystick 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '2-axis joystick with push-button',
        'de': '2-Achsen Joystick mit Taster'
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

com['packets'].append({
'type': 'function',
'name': 'Get Position',
'elements': [('X', 'int16', 1, 'out', {'range': (-100, 100)}),
             ('Y', 'int16', 1, 'out', {'range': (-100, 100)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the position of the joystick. The middle position of the joystick is x=0, y=0.
The returned values are averaged and calibrated (see :func:`Calibrate`).

If you want to get the position periodically, it is recommended to use the
:cb:`Position` callback and set the period with
:func:`Set Position Callback Configuration`.
""",
'de':
"""
Gibt die Position des Joystick zurück. Die Mittelposition des Joysticks ist x=0, y=0.
Die zurückgegebenen Werte sind gemittelt und kalibriert (siehe :func:`Calibrate`).

Wenn die Position periodisch abgefragt werden sollen, wird empfohlen
den :cb:`Position` Callback zu nutzen und die Periode mit
:func:`Set Position Callback Configuration` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is Pressed',
'elements': [('Pressed', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns *true* if the button is pressed and *false* otherwise.

If you want to get the press-state periodically, it is recommended to use the
:cb:`Pressed` callback and set the period with
:func:`Set Pressed Callback Configuration`.
""",
'de':
"""
Gibt *true* zurück wenn die Taste gedrückt ist und sonst *false*.

Wenn der Tastendruck periodisch abgefragt werden sollen, wird empfohlen
den :cb:`Pressed` Callback zu nutzen und die Periode mit
:func:`Set Pressed Callback Configuration` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Calibrate',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Calibrates the middle position of the joystick. If your Joystick Bricklet 2.0
does not return x=0 and y=0 in the middle position, call this function
while the joystick is standing still in the middle position.

The resulting calibration will be saved in non-volatile memory,
thus you only have to calibrate it once.
""",
'de':
"""
Kalibriert die Mittelposition des Joysticks. Sollte der Joystick Bricklet 2.0
nicht x=0 und y=0 in der Mittelposition zurückgeben, kann diese Funktion
aufgerufen werden wenn der Joystick sich unbewegt in der Mittelposition befindet.

Die resultierende Kalibrierung wird in nicht-flüchtigem Speicher gespeichert,
somit ist die Kalibrierung nur einmalig notwendig.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Position Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period is the period with which the :cb:`Position`
callback is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after at least one of the values has changed. If the values didn't
change within the period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.
""",
'de':
"""
Die Periode ist die Periode mit der der :cb:`Position`
Callback ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf true gesetzt wird, wird der
Callback nur ausgelöst, wenn sich mindestens ein Wert im Vergleich zum letzten mal geändert
hat. Ändert sich kein Wert innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn ein Wert sich das nächste mal ändert.

Wird der Parameter auf false gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen der Werte.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Position Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set Position Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set Position Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Position',
'elements': [('X', 'int16', 1, 'out', {'range': (-100, 100)}),
             ('Y', 'int16', 1, 'out', {'range': (-100, 100)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set Position Callback Configuration`.

The :word:`parameters` are the same as with :func:`Get Position`.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set Position Callback Configuration` gesetzten Konfiguration

Die :word:`parameters` sind die gleichen wie bei :func:`Get Position`.
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set Pressed Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period is the period with which the :cb:`Pressed`
callback is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after at least one of the values has changed. If the values didn't
change within the period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.
""",
'de':
"""
Die Periode ist die Periode mit der der :cb:`Pressed`
Callback ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf true gesetzt wird, wird der
Callback nur ausgelöst, wenn sich mindestens ein Wert im Vergleich zum letzten mal geändert
hat. Ändert sich kein Wert innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn ein Wert sich das nächste mal ändert.

Wird der Parameter auf false gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen der Werte.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Pressed Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set Pressed Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set Pressed Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Pressed',
'elements': [('Pressed', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set Pressed Callback Configuration`.

The :word:`parameters` are the same as with :func:`Is Pressed`.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set Pressed Callback Configuration` gesetzten Konfiguration

Der :word:`parameters` ist der gleiche wie bei :func:`Is Pressed`.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Position', 'position'), [(('X', 'Position [X]'), 'int16', 1, None, None, None), (('Y', 'Position [Y]'), 'int16', 1, None, None, None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Pressed', 'pressed'), [(('Pressed', 'Pressed'), 'bool', 1, None, None, None)], None, None),
              ('callback_configuration', ('Pressed', 'pressed'), [], 10, True, None, [])]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports() + oh_generic_trigger_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'params': [
        update_interval('Set Position Callback Configuration', 'Period', 'Position', 'X and Y position')
    ],
    'init_code':"""this.setPositionCallbackConfiguration(cfg.positionUpdateInterval, true);""",
    'dispose_code': """this.setPositionCallbackConfiguration(0, true);""",
    'channels': [{
            'id': 'Position {}'.format(axis),
            'type': 'Position',
            'label': 'Position {}'.format(axis),

            'getters': [{
                'packet': 'Get Position',
                'element': axis,
                'packet_params': [],
                'transform': 'new QuantityType<>(value.{}{{divisor}}, {{unit}})'.format(axis.lower())}],

            'callbacks': [{
                'packet': 'Position',
                'transform': 'new QuantityType<>({}{{divisor}}, {{unit}})'.format(axis.lower())}],

            'is_trigger_channel': False
        } for axis in ['X', 'Y']] + [{
            'id': 'Pressed',
            'label': 'Pressed',
            'description': 'Triggers if the button is pressed or released',
            'type': 'system.rawbutton',
            'getters': [{
                'packet': 'Is Pressed',
                'element': 'Pressed',
                'transform': 'value ? CommonTriggerEvents.PRESSED : CommonTriggerEvents.RELEASED'}],

            'callbacks': [{
                'packet': 'Pressed',
                'element': 'Pressed',
                'transform': 'pressed ? CommonTriggerEvents.PRESSED : CommonTriggerEvents.RELEASED'}],

            'is_trigger_channel': True,
            'init_code': """this.setPressedCallbackConfiguration(10, true);"""
        },
    ],
    'channel_types': [
        oh_generic_channel_type('Position', 'Number', 'Position',
                    update_style=None,
                    description='The position of the joystick. The value ranges between -100 and 100 for both axis. The middle position of the joystick is x=0, y=0. The returned values are averaged and calibrated.',
                    read_only=True,
                    pattern='%d %unit%',
                    min_=-100,
                    max_=100)
    ],
    'actions': ['Get Position', 'Is Pressed']
}
