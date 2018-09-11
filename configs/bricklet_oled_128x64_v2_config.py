# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# OLED 128x64 Bricklet 2.0 communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2112,
    'name': 'OLED 128x64 V2',
    'display_name': 'OLED 128x64 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '3.3cm (1.3") OLED with 128x64 pixels',
        'de': '3,3cm (1,3") OLED mit 128x64 Pixel'
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
'elements': [('X Start', 'uint8', 1, 'in'),
             ('Y Start', 'uint8', 1, 'in'),
             ('X End', 'uint8', 1, 'in'),
             ('Y End', 'uint8', 1, 'in'),
             ('Pixels Length', 'uint16', 1, 'in'),
             ('Pixels Chunk Offset', 'uint16', 1, 'in'),
             ('Pixels Chunk Data', 'bool', 56*8, 'in')],
'high_level': {'stream_in': {'name': 'Pixels'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes pixels to the specified window.

The x-axis goes from 0-127 and the y-axis from 0-63. The pixels are written
into the window line by line from left to right.

If automatic draw is enabled (default) the pixels are directly written to
the screen and only changes are updated. If you only need to update a few
pixels, only these pixels are updated on the screen, the rest stays the same.

If automatic draw is disabled the pixels are written to a buffer and the
buffer is transferred to the display only after :func:`Draw Buffered Frame`
is called.

Automatic draw can be configured with the :func:`Set Display Configuration`
function.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Read Pixels Low Level',
'elements': [('X Start', 'uint8', 1, 'in'),
             ('Y Start', 'uint8', 1, 'in'),
             ('X End', 'uint8', 1, 'in'),
             ('Y End', 'uint8', 1, 'in'),
             ('Pixels Length', 'uint16', 1, 'out'),
             ('Pixels Chunk Offset', 'uint16', 1, 'out'),
             ('Pixels Chunk Data', 'bool', 60*8, 'out')],
'high_level': {'stream_out': {'name': 'Pixels'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Reads pixels from the specified window.

The x-axis goes from 0-127 and the y-axis from 0-63. The pixels are read
from the window line by line from left to right.

If automatic draw is enabled the pixels that are read are always the same that are
shown on the display.

If automatic draw is disabled the pixels are read from the internal buffer
(see :func:`Draw Buffered Frame`).

Automatic draw can be configured with the :func:`Set Display Configuration`
function.
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
Clears the complete content of the display.
""",
'de':
"""
Löscht den kompletten aktuellen Inhalt des Displays.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Display Configuration',
'elements': [('Contrast', 'uint8', 1, 'in'),
             ('Invert', 'bool', 1, 'in'),
             ('Automatic Draw', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the configuration of the display.

You can set a contrast value from 0 to 255
and you can invert the color (black/white) of the display.

If automatic draw is set to *true*, the display is automatically updated with every
call of :func:`Write Pixels` or :func:`Write Line`. If it is set to false, the
changes are written into a temporary buffer and only shown on the display after
a call of :func:`Draw Buffered Frame`.

The default values are contrast 143, inverting off
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
Writes text to a specific line (0 to 7) with a specific position
(0 to 21). The text can have a maximum of 22 characters.

For example: (1, 10, "Hello") will write *Hello* in the middle of the
second line of the display.

The display uses a special 5x7 pixel charset. You can view the characters
of the charset in Brick Viewer.
""",
'de':
"""
Schreibt einen Text in die angegebene Zeile (0 bis 7) mit einer vorgegebenen
Position (0 bis 21). Der Text kann maximal 22 Zeichen lang sein.

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
Draws the currently buffered frame. Normally each call of :func:`Write Pixels` or
:func:`Write Line` draws directly onto the display. If you turn automatic draw off
(:func:`Set Display Configuration`), the data is written in a temporary buffer and
only transferred to the display by calling this function.

Set the *force complete redraw* parameter to *true* to redraw the whole display
instead of only the changed parts. Normally it should not be necessary to set this to
*true*. It may only become necessary in case of stuck pixels because of errors.
""",
'de':
"""
"""
}]
})

com['examples'].append({
'name': 'Hello World',
'functions': [('setter', 'Clear Display', [], 'Clear display', None),
              ('setter', 'Write Line', [('uint8', 0), ('uint8', 0), ('string', 'Hello World')], 'Write "Hello World" starting from upper left corner of the screen', None)]
})

# FIXME: add pixel-matrix example
