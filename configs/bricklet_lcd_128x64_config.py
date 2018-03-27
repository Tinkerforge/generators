# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# LCD 128x64 Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 298,
    'name': 'LCD 128x64',
    'display_name': 'LCD 128x64',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'LCD with 128x64 pixel',
        'de': 'LCD mit 128x64 Pixel'
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
'name': 'Write Pixels Low Level',
'elements': [('Column Start', 'uint8', 1, 'in'),
             ('Row Start', 'uint8', 1, 'in'),
             ('Column End', 'uint8', 1, 'in'),
             ('Row End', 'uint8', 1, 'in'),
             ('Pixels Length', 'uint16', 1, 'in'),
             ('Pixels Chunk Offset', 'uint16', 1, 'in'),
             ('Pixels Chunk Data', 'bool', 56*8, 'in')],
'high_level': {'stream_in': {'name': 'Pixels'}},
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
'name': 'Clear Display',
'elements': [],
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
'name': 'Set Display Configuration',
'elements': [('Contrast', 'uint8', 1, 'in'),
             ('Backlight', 'uint8', 1, 'in'),
             ('Invert', 'bool', 1, 'in'),
             ('Automatic Draw', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the configuration of the display.

You can set a contrast value from 0 to 63, a backlight intensity value
from 0 to 100 and you can invert the color (black/white) of the display.

The default values are contrast 21, backlight intensity 100, inverting off
and automatic draw on.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Display Configuration',
'elements': [('Contrast', 'uint8', 1, 'out'),
             ('Backlight', 'uint8', 1, 'out'),
             ('Invert', 'bool', 1, 'out'),
             ('Automatic Draw', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Display Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Display Configuration`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Write Line',
'elements': [('Line', 'uint8', 1, 'in'),
             ('Position', 'uint8', 1, 'in'),
             ('Text', 'string', 22, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO: 22 chars because of space between char? or 26 chars and no space?


Writes text to a specific line (0 to 7) with a specific position
(0 to 25). The text can have a maximum of 26 characters.

For example: (1, 10, "Hello") will write *Hello* in the middle of the
second line of the display.

The display uses a special 5x7 pixel charset. You can view the characters
of the charset in Brick Viewer.
""",
'de':
"""
Schreibt einen Text in die angegebene Zeile (0 bis 7) mit einer vorgegebenen
Position (0 bis 25). Der Text kann maximal 26 Zeichen lang sein.

Beispiel: (1, 10, "Hallo") schreibt *Hallo* in die Mitte der zweiten Zeile
des Displays.

Das Display nutzt einen speziellen 5x7 Pixel Zeichensatz. Der Zeichensatz
kann mit Hilfe von Brick Viewer angezeigt werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Draw Buffered Frame',
'elements': [('Force Complete Redraw', 'bool', 1, 'in')],
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
'name': 'Get Touch Position',
'elements': [('Pressure', 'uint16', 1, 'out'),
             ('X', 'uint16', 1, 'out'),
             ('Y', 'uint16', 1, 'out'),
             ('Age', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
pressure = 0 => no touch
TBD
""",
'de':
"""
TBD
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set Touch Position Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period in ms is the period with which the :cb:`Touch Position` callback
is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.

The default value is (0, false).
""",
'de':
"""
Die Periode in ms ist die Periode mit der der :cb:`Touch Position` Callback
ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn der Wert sich im Vergleich zum letzten mal geändert
hat. Ändert der Wert sich nicht innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen des Werts.

Der Standardwert ist (0, false).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Touch Position Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set Touch Position Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set Touch Position Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Touch Position',
'elements': [('Pressure', 'uint16', 1, 'out'),
             ('X', 'uint16', 1, 'out'),
             ('Y', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
TBD
""",
'de':
"""
TBD
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Touch Gesture',
'elements': [('Gesture', 'uint8', 1, 'out', ('Gesture', [('Left To Right', 0),
                                                         ('Right To Left', 1),
                                                         ('Top To Bottom', 2),
                                                         ('Bottom To Top', 3)])),
             ('Duration', 'uint32', 1, 'out'),
             ('X Start', 'uint16', 1, 'out'),
             ('Y Start', 'uint16', 1, 'out'),
             ('X End', 'uint16', 1, 'out'),
             ('Y End', 'uint16', 1, 'out'),
             ('Age', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TBD
""",
'de':
"""
TBD
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set Touch Gesture Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period in ms is the period with which the :cb:`Touch Gesture` callback
is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.

The default value is (0, false).
""",
'de':
"""
Die Periode in ms ist die Periode mit der der :cb:`Touch Gesture` Callback
ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn der Wert sich im Vergleich zum letzten mal geändert
hat. Ändert der Wert sich nicht innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen des Werts.

Der Standardwert ist (0, false).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Touch Gesture Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set Touch Gesture Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set Touch Gesture Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Touch Gesture',
'elements': [('Gesture', 'uint8', 1, 'out',  ('Gesture', [('Left To Right', 0),
                                                          ('Right To Left', 1),
                                                          ('Top To Bottom', 2),
                                                          ('Bottom To Top', 3)])),
             ('Duration', 'uint32', 1, 'out'),
             ('X Start', 'uint16', 1, 'out'),
             ('Y Start', 'uint16', 1, 'out'),
             ('X End', 'uint16', 1, 'out'),
             ('Y End', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
TBD
""",
'de':
"""
TBD
"""
}]
})
