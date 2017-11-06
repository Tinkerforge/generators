# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Motorized Linear Poti Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 267,
    'name': 'Motorized Linear Poti',
    'display_name': 'Motorized Linear Poti',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'TODO',
        'de': 'TODO'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'packets': [],
    'examples': []
}

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
    doc       = position_doc
)



com['packets'].append({
'type': 'function',
'name': 'Set Motor Position',
'elements': [('Position', 'uint16', 1, 'in'),
             ('Drive Mode', 'uint8', 1, 'in', ('Drive Mode', [('Fast', 0),
                                                              ('Smooth', 1)])),
             ('Hold Position', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the position of the potentiometer. The mororized potentiometer will
immediately start to approach the position. Depending on the choosen drive mode,
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
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Motor Position',
'elements': [('Position', 'uint16', 1, 'out'),
             ('Drive Mode', 'uint8', 1, 'out', ('Drive Mode', [('Fast', 0),
                                                               ('Smooth', 1)])),
             ('Hold Position', 'bool', 1, 'out'),
             ('Position Reached', 'bool', 1, 'out')],
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
TODO
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
TODO
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set Position Reached Callback Configuration',
'elements': [('Enabled', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Enables/Disables :cb:`Position Reached` callback.

By default the callback is enabled.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Position Reached Callback Configuration',
'elements': [('Enabled', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the position reached callback configuration 
as set by :func:`Set Position Reached Callback Configuration`.
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'callback',
'name': 'Position Reached',
'elements': [('Position', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered if a new position as set by
:func:`Set Motor Position` is reached.

The value is the current position.
""",
'de':
"""
"""
}]
})


com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Position', 'position'), [(('Position', 'Position'), 'uint16', None, None, None, (0, 100))], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Position', 'position'), [(('Position', 'Position'), 'uint16', None, None, None, (0, 100))], None, None),
              ('callback_period', ('Position', 'position'), [], 50)]
})

