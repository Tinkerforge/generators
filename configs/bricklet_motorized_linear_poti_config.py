# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Motorized Linear Poti Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from commonconstants import add_callback_value_function

from openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 267,
    'name': 'Motorized Linear Poti',
    'display_name': 'Motorized Linear Poti',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Motorized Linear Potentiometer',
        'de': 'Motorisiertes Linearpotentiometer'
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

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

com['constant_groups'].append({
'name': 'Drive Mode',
'type': 'uint8',
'constants': [('Fast', 0),
              ('Smooth', 1)]
})

position_doc = {
'en':
"""
Returns the position of the linear potentiometer. The value is
between 0 (slider down) and 100 (slider up).
""",
'de':
"""
Gibt die Position des Linearpotentiometers zurück. Der Wertebereich
ist von 0 (Schieberegler unten) und 100 (Schieberegler oben).
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Position',
    data_name = 'Position',
    data_type = 'uint16',
    doc       = position_doc,
    range_    = (0, 100)
)

com['packets'].append({
'type': 'function',
'name': 'Set Motor Position',
'elements': [('Position', 'uint16', 1, 'in', {'range': (0, 100)}),
             ('Drive Mode', 'uint8', 1, 'in', {'constant_group': 'Drive Mode'}),
             ('Hold Position', 'bool', 1, 'in', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the position of the potentiometer. The motorized potentiometer will
immediately start to approach the position. Depending on the chosen drive mode,
the position will either be reached as fast as possible or in a slow but smooth
motion.

The position has to be between 0 (slider down) and 100 (slider up).

If you set the hold position parameter to true, the position will automatically
be retained. If a user changes the position of the potentiometer, it will
automatically drive back to the original set point.

If the hold position parameter is set to false, the potentiometer can be changed
again by the user as soon as the set point was reached once.
""",
'de':
"""
Setzt die Position des Potentiometers. Nach Aufruf der Funktion wird das Potentiometer
sofort diese Position anfahren. Abhängig von dem gewählten *Drive Mode* wird die Position
entweder so schnell wie möglich angefahren oder langsam dafür aber gleichmäßig (smooth).

Die Position kann zwischen 0 (Regler unten) und 100 (Regler oben) festgelegt werden.

Wenn der *Hold Position* Parameter auf True gesetzt wird, wird die Position automatisch
gehalten. Wenn ein Nutzer die Position ändert, fährt das Potentiometer die alte Position
anschließend wieder an.

Wenn der *Hold Position* Parameter auf False gesetzt wird, kann die Position vom Nutzer
geändert werden, nachdem die Sollposition erreicht wurde.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Motor Position',
'elements': [('Position', 'uint16', 1, 'out', {'range': (0, 100)}),
             ('Drive Mode', 'uint8', 1, 'out', {'constant_group': 'Drive Mode'}),
             ('Hold Position', 'bool', 1, 'out', {}),
             ('Position Reached', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the last motor position as set by :func:`Set Motor Position`. This is not
the current position (use :func:`Get Position` to get the current position). This
is the last used set point and configuration.

The position reached parameter is true if the position has been reached at one point.
The position may have been changed again in the meantime by the user.
""",
'de':
"""
Gibt die letzte Motor Position, die mittels :func:`Set Motor Position` gesetzt wurde
zurück. Dies ist nicht die aktuelle Position des Potentiometers (dafür ist
:func:`Get Position` gedacht). Zusätzlich wird die letzte Konfiguration zurückgegeben.

Der *Position Reached* Parameter ist True, wenn der letzte Sollwert (Motor Position)
erreicht wurde. Die reale Position könnte sich seitdem jedoch geändert haben.
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
Starts a calibration procedure. The potentiometer will be driven to the extreme
points to calibrate the potentiometer.

The calibration is saved in flash, it does not have to be called on every start up.

The Motorized Linear Poti Bricklet is already factory-calibrated during
testing at Tinkerforge.
""",
'de':
"""
Startet die Kalibrierung. Das Potentiometer fährt dabei die Extrempunkte an.

Die Kalibrierung wird im internen Flash gespeichert und muss nicht bei jedem
Start neu durchgeführt werden.

Das Motorized Linear Poti Bricklet wird von Tinkerforge während des Funktionstests
kalibriert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Position Reached Callback Configuration',
'elements': [('Enabled', 'bool', 1, 'in', {'default': True})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Enables/Disables :cb:`Position Reached` callback.
""",
'de':
"""
Aktiviert/Deaktiviert den :cb:`Position Reached` Callback.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Position Reached Callback Configuration',
'elements': [('Enabled', 'bool', 1, 'out', {'default': True})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the :cb:`Position Reached` callback configuration
as set by :func:`Set Position Reached Callback Configuration`.
""",
'de':
"""
Gibt die :cb:`Position Reached` Callback Konfiguration zurück, wie von
:func:`Set Position Reached Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Position Reached',
'elements': [('Position', 'uint16', 1, 'out', {'range': (0, 100)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered if a new position as set by
:func:`Set Motor Position` is reached.

The :word:`parameter` is the current position.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn die mittels
:func:`Set Motor Position` gesetzte Position erreicht wird.

Der :word:`parameter` ist die aktuelle Position.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Position', 'position'), [(('Position', 'Position'), 'uint16', 1, None, None, (0, 100))], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Position', 'position'), [(('Position', 'Position'), 'uint16', 1, None, None, (0, 100))], None, None),
              ('callback_configuration', ('Position', 'position'), [], 50, False, 'x', [(0, 0)])]
})

com['examples'].append({
'name': 'Motor',
'functions': [('callback', ('Position Reached', 'position reached'), [(('Position', 'Position'), 'uint16', 1, None, None, (0, 100))], None, None),
              ('setter', 'Set Motor Position', [('uint16', 50), ('uint8:constant', 1), ('bool', False)], 'Move slider smooth to the middle', None)]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports() + oh_generic_trigger_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'channels': [
        oh_generic_channel('Position', 'Position'),
        {
            'id': 'Motor Position',
            'label': 'Motor Position',
            'description': 'The motor position of the potentiometer. The motorized potentiometer will immediately start to approach the position. Depending on the chosen drive mode, the position will either be reached as fast as possible or in a slow but smooth motion.<br/><br/>The position has to be between 0 (slider down) and 100 (slider up).',
            'type': 'Motor Position',

            'getters': [{
                'packet': 'Get {title_words}',
                'element': 'Position',
                'packet_params': [],
                'transform': 'new {number_type}(value.position{divisor}{unit})'}],

            'setters': [{
                'packet': 'Set {title_words}',
                'element': 'Position',
                'packet_params': ['cmd.intValue(){divisor}', 'channelCfg.smoothDriveMode ? 1 : 0', 'channelCfg.holdPosition'],
                'command_type': 'Number',
            }],
        }, {
            'id': 'Position Reached',
            'type': 'system.trigger',

            'label': 'Position Reached',
            'description': 'This channel is triggered if a new position as set by the Motor Position Channel is reached.',

            'callbacks': [{
                'packet': 'Position Reached',
                'transform': '""'}],
        },
    ],
    'channel_types': [
        oh_generic_channel_type('Position', 'Number', 'Position',
                    update_style='Callback Configuration',
                    description='The position of the linear potentiometer. The value is between 0 (slider down) and 100 (slider up).'),
        oh_generic_channel_type('Motor Position', 'Number', 'Motor Position',
                    update_style=None,
                    description='The motor position of the potentiometer. The value is between 0 (slider down) and 100 (slider up).',
                    params=[{
                        'packet': 'Set Motor Position',
                        'element': 'Drive Mode',

                        'name': 'Smooth Drive Mode',
                        'type': 'boolean',
                        'default': 'false',

                        'label': 'Smooth Drive Mode',
                        'description': ' Depending on the chosen drive mode, the position will either be reached as fast as possible or in a slow but smooth motion.',
                    }, {
                        'packet': 'Set Motor Position',
                        'element': 'Hold Position',

                        'name': 'Hold Position',
                        'type': 'boolean',
                        'default': 'false',

                        'label': 'Hold Position',
                        'description': 'If you enable the hold position flag, the position will automatically be retained. If a user changes the position of the potentiometer, it will automatically drive back to the original set point.<br/><br/>If the hold position flag disabled, the potentiometer can be changed again by the user as soon as the set point was reached once.',
                    }])
    ],
    'actions': ['Get Position', {'fn': 'Set Motor Position', 'refreshs': ['Motor Position']}, 'Get Motor Position']
}
