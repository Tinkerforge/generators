# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# OLED 128x64 Bricklet 2.0 communication config

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2112,
    'name': 'OLED 128x64 V2',
    'display_name': 'OLED 128x64 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '3.3cm (1.3") OLED display with 128x64 pixels',
        'de': '3,3cm (1,3") OLED Display mit 128x64 Pixel'
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
'name': 'Write Pixels Low Level',
'elements': [('X Start', 'uint8', 1, 'in', {'range': (0, 127)}),
             ('Y Start', 'uint8', 1, 'in', {'range': (0, 63)}),
             ('X End', 'uint8', 1, 'in', {'range': (0, 127)}),
             ('Y End', 'uint8', 1, 'in', {'range': (0, 63)}),
             ('Pixels Length', 'uint16', 1, 'in', {'range': (0, 128 * 64)}),
             ('Pixels Chunk Offset', 'uint16', 1, 'in', {}),
             ('Pixels Chunk Data', 'bool', 56*8, 'in', {})],
'high_level': {'stream_in': {'name': 'Pixels'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes pixels to the specified window.

The pixels are written into the window line by line top to bottom
and each line is written from left to right.

If automatic draw is enabled (default) the pixels are directly written to
the screen. Only pixels that have actually changed are updated on the screen,
the rest stays the same.

If automatic draw is disabled the pixels are written to an internal buffer and
the buffer is transferred to the display only after :func:`Draw Buffered Frame`
is called. This can be used to avoid flicker when drawing a complex frame in
multiple steps.

Automatic draw can be configured with the :func:`Set Display Configuration`
function.
""",
'de':
"""
Schreibt Pixel in das angegebene Fenster.

Die Pixel werden zeilenweise von oben nach unten
die Zeilen werden jeweils von links nach rechts geschrieben.

Wenn Automatic Draw aktiviert ist (Standard), dann werden die Pixel direkt auf
den Display geschrieben. Nur Pixel die sich wirklich verändert haben werden
auf dem Display aktualisiert.

Wenn Automatic Draw deaktiviert ist, dann werden die Pixel in einen internen
Buffer geschrieben der dann durch einen Aufruf von :func:`Draw Buffered Frame`
auf dem Display angezeigt werden kann. Dadurch kann Flicker vermieden werden,
wenn ein komplexes Bild in mehreren Schritten aufgebaut wird.

Automatic Draw kann über die :func:`Set Display Configuration` Funktion
eingestellt werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Read Pixels Low Level',
'elements': [('X Start', 'uint8', 1, 'in', {'range': (0, 127)}),
             ('Y Start', 'uint8', 1, 'in', {'range': (0, 63)}),
             ('X End', 'uint8', 1, 'in', {'range': (0, 127)}),
             ('Y End', 'uint8', 1, 'in', {'range': (0, 63)}),
             ('Pixels Length', 'uint16', 1, 'out', {'range': (0, 128 * 64)}),
             ('Pixels Chunk Offset', 'uint16', 1, 'out', {}),
             ('Pixels Chunk Data', 'bool', 60*8, 'out', {})],
'high_level': {'stream_out': {'name': 'Pixels'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Reads pixels from the specified window.

The pixels are read from the window line by line top to bottom
and each line is read from left to right.

If automatic draw is enabled (default) the pixels that are read are always the
same that are shown on the display.

If automatic draw is disabled the pixels are read from the internal buffer
(see :func:`Draw Buffered Frame`).

Automatic draw can be configured with the :func:`Set Display Configuration`
function.
""",
'de':
"""
Liest Pixel aus dem angegebenen Fenster.

Die X-Achse läuft von 0 bis 127 und die Y-Achse von 0 bis 63. Die Pixel werden
zeilenweise von oben nach unten und die Zeilen werden jeweils von links nach
rechts gelesen.

Wenn Automatic Draw aktiviert ist (Standard), dann werden die Pixel direkt vom
Display gelesen.

Wenn Automatic Draw deaktiviert ist, dann werden die Pixel aus einen internen
Buffer gelesen (siehe :func:`Draw Buffered Frame`).

Automatic Draw kann über die :func:`Set Display Configuration` Funktion
eingestellt werden.
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

If automatic draw is enabled (default) the pixels are directly cleared.

If automatic draw is disabled the the internal buffer is cleared and
the buffer is transferred to the display only after :func:`Draw Buffered Frame`
is called. This can be used to avoid flicker when drawing a complex frame in
multiple steps.

Automatic draw can be configured with the :func:`Set Display Configuration`
function.
""",
'de':
"""
Löscht den kompletten aktuellen Inhalt des Displays.

Wenn Automatic Draw aktiviert ist (Standard), dann werden die Pixel direkt
gelöscht.

Wenn Automatic Draw deaktiviert ist, dann werden die Pixel im internen
Buffer gelöscht der dann durch einen Aufruf von :func:`Draw Buffered Frame`
auf dem Display angezeigt werden kann. Dadurch kann Flicker vermieden werden,
wenn ein komplexes Bild in mehreren Schritten aufgebaut wird.

Automatic Draw kann über die :func:`Set Display Configuration` Funktion
eingestellt werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Display Configuration',
'elements': [('Contrast', 'uint8', 1, 'in', {'default': 143}),
             ('Invert', 'bool', 1, 'in', {'default': False}),
             ('Automatic Draw', 'bool', 1, 'in', {'default': True})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the configuration of the display.

You can set a contrast value from 0 to 255 and you can invert the color
(white/black) of the display.

If automatic draw is set to *true*, the display is automatically updated with every
call of :func:`Write Pixels` or :func:`Write Line`. If it is set to false, the
changes are written into an internal buffer and only shown on the display after
a call of :func:`Draw Buffered Frame`.
""",
'de':
"""
Setzt die Konfiguration des Displays.

Der Kontrast kann zwischen 0 und 255 und das Farbschema invertiert
(weiß/schwarz) eingestellt werden.

Wenn Automatic Draw aktiviert (*true*) ist dann wird das Display bei jedem
Aufruf von :func:`Write Pixels` und :func:`Write Line` aktualisiert. Wenn
Automatic Draw deaktiviert (*false*) ist, dann werden Änderungen in einen
internen Buffer geschrieben, der dann bei bei einem Aufruf von
:func:`Draw Buffered Frame` auf dem Display angezeigt wird.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Display Configuration',
'elements': [('Contrast', 'uint8', 1, 'out', {'default': 143}),
             ('Invert', 'bool', 1, 'out', {'default': False}),
             ('Automatic Draw', 'bool', 1, 'out', {'default': True})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Display Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Display Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Write Line',
'elements': [('Line', 'uint8', 1, 'in', {'range': (0, 7)}),
             ('Position', 'uint8', 1, 'in', {'range': (0, 21)}),
             ('Text', 'string', 22, 'in', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes text to a specific line with a specific position.
The text can have a maximum of 22 characters.

For example: (1, 10, "Hello") will write *Hello* in the middle of the
second line of the display.

The display uses a special 5x7 pixel charset. You can view the characters
of the charset in Brick Viewer.

If automatic draw is enabled (default) the text is directly written to
the screen. Only pixels that have actually changed are updated on the screen,
the rest stays the same.

If automatic draw is disabled the text is written to an internal buffer and
the buffer is transferred to the display only after :func:`Draw Buffered Frame`
is called. This can be used to avoid flicker when drawing a complex frame in
multiple steps.

Automatic draw can be configured with the :func:`Set Display Configuration`
function.
""",
'de':
"""
Schreibt einen Text in die angegebene Zeile mit einer vorgegebenen Position.
Der Text kann maximal 22 Zeichen lang sein.

Beispiel: (1, 10, "Hallo") schreibt *Hallo* in die Mitte der zweiten Zeile
des Displays.

Das Display nutzt einen speziellen 5x7 Pixel Zeichensatz. Der Zeichensatz
kann mit Hilfe von Brick Viewer angezeigt werden.

Wenn Automatic Draw aktiviert ist (Standard), dann wird der Text direkt auf
den Display geschrieben. Nur Pixel die sich wirklich verändert haben werden
auf dem Display aktualisiert.

Wenn Automatic Draw deaktiviert ist, dann wird der Text in einen internen
Buffer geschrieben der dann durch einen Aufruf von :func:`Draw Buffered Frame`
auf dem Display angezeigt werden kann. Dadurch kann Flicker vermieden werden,
wenn ein komplexes Bild in mehreren Schritten aufgebaut wird.

Automatic Draw kann über die :func:`Set Display Configuration` Funktion
eingestellt werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Draw Buffered Frame',
'elements': [('Force Complete Redraw', 'bool', 1, 'in', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Draws the currently buffered frame. Normally each call of :func:`Write Pixels` and
:func:`Write Line` draws directly onto the display. If you turn automatic draw off
(:func:`Set Display Configuration`), the data is written in an internal buffer and
only transferred to the display by calling this function. This can be used to
avoid flicker when drawing a complex frame in multiple steps.

Set the `force complete redraw` to *true* to redraw the whole display
instead of only the changed parts. Normally it should not be necessary to set this to
*true*. It may only become necessary in case of stuck pixels because of errors.
""",
'de':
"""
Stellt den aktuell Inhalt des internen Buffers auf dem Display dar. Normalerweise
schreibt jeder Aufruf von :func:`Write Pixels` und :func:`Write Line` direkt auf
den Display. Wenn jedoch Automatic Draw deaktiviert ist (:func:`Set Display Configuration`),
dann werden Änderungen in einen internen Buffer anstatt auf den
Display geschrieben. Der internen Buffer kann dann durch einen Aufruf dieser
Funktion auf den Display geschrieben werden. Dadurch kann Flicker vermieden
werden, wenn ein komplexes Bild in mehreren Schritten aufgebaut wird.

Wenn `Force Complete Redraw` auf *true* gesetzt ist, dann wird der gesamte Display
aktualisiert, anstatt nur die Pixel die sich wirklich verändert haben. Normalerweise
sollte dies nicht notwendig sein, außer bei hängenden Pixeln bedingt durch Fehler.
"""
}]
})

com['examples'].append({
'name': 'Hello World',
'functions': [('setter', 'Clear Display', [], 'Clear display', None),
              ('setter', 'Write Line', [('uint8', 0), ('uint8', 0), ('string', 'Hello World')], 'Write "Hello World" starting from upper left corner of the screen', None)]
})

# FIXME: add pixel-matrix example


com['openhab'] = {
    'imports': oh_generic_channel_imports() + oh_generic_trigger_channel_imports() +  ['org.eclipse.smarthome.core.library.types.StringType', 'com.tinkerforge.Helper'],
    'param_groups': oh_generic_channel_param_groups(),
    'params': [
        {
            'packet': 'Set Display Configuration',
            'element': 'Contrast',

            'name': 'Contrast',
            'type': 'integer',
            'default': 143,
            'min': 0,
            'max': 255,

            'label': 'Contrast',
            'description': "Sets the contrast of the display (0-255).",
        },
        {
            'packet': 'Set Display Configuration',
            'element': 'Invert',

            'name': 'Invert',
            'type': 'boolean',
            'default': 'false',

            'label': 'Invert',
            'description': 'Inverts the color (black/white) of the display.',
        },
        {
            'packet': 'Set Display Configuration',
            'element': 'Automatic Draw',

            'name': 'Automatic Draw',
            'type': 'boolean',
            'default': 'true',

            'label': 'Automatic Draw',
            'description': 'If automatic draw is enabled, the display is automatically updated when writing text or clearing the display. If it is disabled, the changes are written into an internal buffer and only shown on the display after triggering the Draw Buffered Frame channel.',
        },
    ] ,
    'init_code': """this.setDisplayConfiguration(cfg.contrast.shortValue(), cfg.invert, cfg.automaticDraw);""",
    'channels': [
            {
                'id': 'Text',
                'type': 'Text',
                'setters': [{
                    'packet': 'Write Line',
                    'packet_params': ['Helper.parseDisplayCommandLine(cmd.toString(), logger)', 'Helper.parseDisplayCommandPosition(cmd.toString(), logger)', 'Helper.parseDisplayCommandText(cmd.toString(), logger)']}],
                'setter_command_type': "StringType",
            },
            {
                'id': 'Clear Display',
                'type': 'Clear Display',
                'setters': [{
                    'packet': 'Clear Display'}],
                'setter_command_type': "StringType",
            },
            {
                'id': 'Draw Buffered Frame',
                'type': 'Draw Buffered Frame',
                'setters': [{
                    'packet': 'Draw Buffered Frame',
                    'packet_params': ['true']
                }],
                'setter_command_type': "StringType",
            }
    ],
    'channel_types': [
        oh_generic_channel_type('Text', 'String', 'Text',
                    update_style=None,
                    description="Text to display on the LCD. Command format is [line],[position],[text].<br/><br/>Additional ',' are handled as part of the text. Unicode characters are converted to the LCD character set if possible. Additionally you can use \\\\x[two hex digits] to use a character of the LCD character set directly."),
        {
            'id': 'Clear Display',
            'item_type': 'String',
            'label': 'Clear Display',
            'description':'Deletes all characters from the display.',
            'command_options': [('Clear', 'CLEAR')]
        },
        {
            'id': 'Draw Buffered Frame',
            'item_type': 'String',
            'label': 'Draw Buffered Frame',
            'description':'Draws the currently buffered frame.',
            'command_options': [('Draw', 'DRAW')]
        },
    ],
    'actions': ['Write Pixels', 'Read Pixels', 'Clear Display', 'Draw Buffered Frame', 'Write Line', 'Get Display Configuration']
}
