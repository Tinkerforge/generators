# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# LCD 128x64 Bricklet communication config

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'category': 'Bricklet',
    'device_identifier': 298,
    'name': 'LCD 128x64',
    'display_name': 'LCD 128x64',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '7.1cm (2.8") display with 128x64 pixel and touch screen',
        'de': '7,1cm (2,8") Display mit 128x64 Pixel und Touchscreen'
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
'name': 'Gesture',
'type': 'uint8',
'constants': [('Left To Right', 0),
              ('Right To Left', 1),
              ('Top To Bottom', 2),
              ('Bottom To Top', 3)]
})

com['constant_groups'].append({
'name': 'Color',
'type': 'bool',
'constants': [('White', False),
              ('Black', True)]
})

com['constant_groups'].append({
'name': 'Font',
'type': 'uint8',
'constants': [('6x8', 0),
              ('6x16', 1),
              ('6x24', 2),
              ('6x32', 3),
              ('12x16', 4),
              ('12x24', 5),
              ('12x32', 6),
              ('18x24', 7),
              ('18x32', 8),
              ('24x32', 9)]
})

com['constant_groups'].append({
'name': 'Direction',
'type': 'uint8',
'constants': [('Horizontal', 0),
              ('Vertical', 1)]
})

com['constant_groups'].append({
'name': 'Change Tab On',
'type': 'uint8',
'constants': [('Click', 1),
              ('Swipe', 2),
              ('Click And Swipe', 3)]
})

com['constant_groups'].append({
'name': 'Graph Type',
'type': 'uint8',
'constants': [('Dot',  0),
              ('Line', 1),
              ('Bar',  2)]
})

com['constant_groups'].append({
'name': 'Touch LED Config',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Show Heartbeat', 2),
              ('Show Touch', 3)]
})

com['packets'].append({
'type': 'function',
'name': 'Write Pixels Low Level',
'elements': [('X Start', 'uint8', 1, 'in', {'range': (0, 127)}),
             ('Y Start', 'uint8', 1, 'in', {'range': (0, 63)}),
             ('X End', 'uint8', 1, 'in', {'range': (0, 127)}),
             ('Y End', 'uint8', 1, 'in', {'range': (0, 63)}),
             ('Pixels Length', 'uint16', 1, 'in', {'range': (0, 128*64)}),
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

Die Pixel werden zeilenweise von oben nach unten geschrieben
und die Zeilen werden jeweils von links nach rechts geschrieben.

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
             ('Pixels Length', 'uint16', 1, 'out', {'range': (0, 128*64)}),
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

Die Pixel werden zeilenweise von oben nach unten
und die Zeilen werden jeweils von links nach rechts gelesen.

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
'elements': [('Contrast', 'uint8', 1, 'in', {'range': (0, 63), 'default': 14}),
             ('Backlight', 'uint8', 1, 'in', {'range': (0, 100), 'default': 100}),
             ('Invert', 'bool', 1, 'in', {'default': False}),
             ('Automatic Draw', 'bool', 1, 'in', {'default': True})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the configuration of the display.

If automatic draw is set to *true*, the display is automatically updated with every
call of :func:`Write Pixels` and :func:`Write Line`. If it is set to false, the
changes are written into an internal buffer and only shown on the display after
a call of :func:`Draw Buffered Frame`.
""",
'de':
"""
Setzt die Konfiguration des Displays.

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
'elements': [('Contrast', 'uint8', 1, 'out', {'range': (0, 63), 'default': 14}),
             ('Backlight', 'uint8', 1, 'out', {'range': (0, 100), 'default': 100}),
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

This function is a 1:1 replacement for the function with the same name
in the LCD 20x4 Bricklet. You can draw text at a specific pixel position
and with different font sizes with the :func:`Draw Text` function.
""",
'de':
"""
Schreibt einen Text in die angegebene Zeile mit einer vorgegebenen Position.

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

Diese Funktion ist ein 1:1-Ersatz für die Funktion mit dem gleichen Namen
im LCD 20x4 Bricklet. Mit der Funktion :func:`Draw Text` kann Text Pixelgenau
und mit unterschiedlichen Font-Größen gezeichnet werden.
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
Funktion auf den Display geschrieben werden. Dadurch kann Flicker vermieden werden,
wenn ein komplexes Bild in mehreren Schritten aufgebaut wird.

Wenn `Force Complete Redraw` auf *true* gesetzt ist, dann wird der gesamte Display
aktualisiert, anstatt nur die Pixel die sich wirklich verändert haben. Normalerweise
sollte dies nicht notwendig sein, außer bei hängenden Pixeln bedingt durch Fehler.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Touch Position',
'elements': [('Pressure', 'uint16', 1, 'out', {'range': (0, 300)}),
             ('X', 'uint16', 1, 'out', {'range': (0, 127)}),
             ('Y', 'uint16', 1, 'out', {'range': (0, 63)}),
             ('Age', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the last valid touch position:

* Pressure: Amount of pressure applied by the user
* X: Touch position on x-axis
* Y: Touch position on y-axis
* Age: Age of touch press (how long ago it was)
""",
'de':
"""
Gibt die letzte gültige Touch-Position zurück:

* Pressure: Anpressdruck des Touches
* X: Touch-Position auf der X-Achse
* Y: Touch-Position auf der Y-Achse
* Age: Alter des Touches (wie lange ist die Erkennung des Touches her)
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Touch Position Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period is the period with which the :cb:`Touch Position` callback
is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.
""",
'de':
"""
Die Periode ist die Periode mit der der :cb:`Touch Position` Callback
ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn der Wert sich im Vergleich zum letzten mal geändert
hat. Ändert der Wert sich nicht innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen des Werts.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Touch Position Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'out', {'default': False})],
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
'elements': [('Pressure', 'uint16', 1, 'out', {'range': (0, 300)}),
             ('X', 'uint16', 1, 'out', {'range': (0, 127)}),
             ('Y', 'uint16', 1, 'out', {'range': (0, 63)}),
             ('Age', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Touch Position Callback Configuration`. The :word:`parameters` are the
same as for :func:`Get Touch Position`.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Touch Position Callback Configuration`, ausgelöst. Die :word:`parameters` sind
die gleichen wie die von :func:`Get Touch Position`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Touch Gesture',
'elements': [('Gesture', 'uint8', 1, 'out', {'constant_group': 'Gesture'}),
             ('Duration', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'}),
             ('Pressure Max', 'uint16', 1, 'out', {'range': (0, 300)}),
             ('X Start', 'uint16', 1, 'out', {'range': (0, 127)}),
             ('Y Start', 'uint16', 1, 'out', {'range': (0, 63)}),
             ('X End', 'uint16', 1, 'out', {'range': (0, 127)}),
             ('Y End', 'uint16', 1, 'out', {'range': (0, 63)}),
             ('Age', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns one of four touch gestures that can be automatically detected by the Bricklet.

The gestures are swipes from left to right, right to left, top to bottom and bottom to top.

Additionally to the gestures a vector with a start and end position of the gesture is
provided. You can use this vector do determine a more exact location of the gesture (e.g.
the swipe from top to bottom was on the left or right part of the screen).

The age parameter corresponds to the age of gesture (how long ago it was).
""",
'de':
"""
Gibt eine der vier Touch-Gesten zurück, die das Bricklet automatisch erkennen kann.

Die Gesten umfassen Wischen von links nach rechts, rechts nach links, oben nach
unten und unten nach oben.

Zusätzlich zu Geste wird der Vektor von Start- nach Endposition des Wischens
angegeben. Dieser kann genutzt werden um die genaue Position der Geste zu
ermitteln (z.B. ob ein Wischen von oben nach unten auf der linken oder rechten
des Bildschirms erkannt wurde).

Der Age Parameter gibt das Alter der Geste an (wie lange ist die Erkennung
der Geste her).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Touch Gesture Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period is the period with which the :cb:`Touch Gesture` callback
is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.
""",
'de':
"""
Die Periode ist die Periode mit der der :cb:`Touch Gesture` Callback
ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn der Wert sich im Vergleich zum letzten mal geändert
hat. Ändert der Wert sich nicht innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen des Werts.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Touch Gesture Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'out', {'default': False})],
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
'elements': [('Gesture', 'uint8', 1, 'out', {'constant_group': 'Gesture'}),
             ('Duration', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'}),
             ('Pressure Max', 'uint16', 1, 'out', {'range': (0, 300)}),
             ('X Start', 'uint16', 1, 'out', {'range': (0, 127)}),
             ('Y Start', 'uint16', 1, 'out', {'range': (0, 63)}),
             ('X End', 'uint16', 1, 'out', {'range': (0, 127)}),
             ('Y End', 'uint16', 1, 'out', {'range': (0, 63)}),
             ('Age', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Touch Gesture Callback Configuration`. The :word:`parameters` are the
same as for :func:`Get Touch Gesture`.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Touch Gesture Callback Configuration`, ausgelöst. Die :word:`parameters` sind
die gleichen wie die von :func:`Get Touch Gesture`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Draw Line',
'elements': [('Position X Start', 'uint8', 1, 'in', {'range': (0, 127)}),
             ('Position Y Start', 'uint8', 1, 'in', {'range': (0, 63)}),
             ('Position X End', 'uint8', 1, 'in', {'range': (0, 127)}),
             ('Position Y End', 'uint8', 1, 'in', {'range': (0, 63)}),
             ('Color', 'bool', 1, 'in', {'constant_group': 'Color'})],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Draws a white or black line from (x, y)-start to (x, y)-end.
""",
'de':
"""
Zeichnet eine weiße oder schwarze Linie von (x, y)-start nach
(x, y)-end.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Draw Box',
'elements': [('Position X Start', 'uint8', 1, 'in', {'range': (0, 127)}),
             ('Position Y Start', 'uint8', 1, 'in', {'range': (0, 63)}),
             ('Position X End', 'uint8', 1, 'in', {'range': (0, 127)}),
             ('Position Y End', 'uint8', 1, 'in', {'range': (0, 63)}),
             ('Fill', 'bool', 1, 'in', {}),
             ('Color', 'bool', 1, 'in', {'constant_group': 'Color'})],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Draws a white or black box from (x, y)-start to (x, y)-end.

If you set fill to true, the box will be filled with the
color. Otherwise only the outline will be drawn.
""",
'de':
"""
Zeichnet ein weißes oder schwarzes Rechteck von (x, y)-start nach
(x, y)-end.

Wenn fill auf true gesetzt wird, wird das Rechteck mit
der angegebenen Farbe ausgefüllt. Ansonsten wird nur der Umriss
gezeichnet.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Draw Text',
'elements': [('Position X', 'uint8', 1, 'in', {'range': (0, 127)}),
             ('Position Y', 'uint8', 1, 'in', {'range': (0, 63)}),
             ('Font', 'uint8', 1, 'in', {'constant_group': 'Font'}),
             ('Color', 'bool', 1, 'in', {'constant_group': 'Color'}),
             ('Text', 'string', 22, 'in', {})],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Draws a text at the pixel position (x, y).

You can use one of 9 different font sizes and draw the text in white or black.
""",
'de':
"""
Zeichnet einen Text an die Pixelposition (x, y).

Es können 9 unterschiedliche Font-Größen genutzt werden und der Text
kann in weiß oder schwarz gezeichnet werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set GUI Button',
'elements': [('Index', 'uint8', 1, 'in', {'range': (0, 11)}),
             ('Position X', 'uint8', 1, 'in', {'range': (0, 127)}),
             ('Position Y', 'uint8', 1, 'in', {'range': (0, 63)}),
             ('Width', 'uint8', 1, 'in', {'range': (1, 128)}),
             ('Height', 'uint8', 1, 'in', {'range': (1, 64)}),
             ('Text', 'string', 16, 'in', {})],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Draws a clickable button at position (x, y) with the given text.

You can use up to 12 buttons.

The x position + width has to be within the range of 1 to 128 and the y
position + height has to be within the range of 1 to 64.

The minimum useful width/height of a button is 3.

You can enable a callback for a button press with
:func:`Set GUI Button Pressed Callback Configuration`. The callback will
be triggered for press and release-events.

The button is drawn in a separate GUI buffer and the button-frame will
always stay on top of the graphics drawn with :func:`Write Pixels`. To
remove the button use :func:`Remove GUI Button`.

If you want an icon instead of text, you can draw the icon inside of the
button with :func:`Write Pixels`.
""",
'de':
"""
Zeichnet einen klickbaren Button an Position (x, y) mit dem gegebenem Text.

Es können bis zu 12 Buttons genutzt werden.

Die x-Position + Width muss im Wertebereich von 1 bis 128 liegen und die
y-Position+Height muss im Wertebereich von 1 bis 64 liegen.

Die minimale nützliche Breite/Höhe eines Buttons ist 3.

Der Callback für Button-Events kann mit der Funktion
:func:`Set GUI Button Pressed Callback Configuration` eingestellt werden.
Der Callback wird sowohl für gedrückt als auch losgelassen Events ausgelöst.

Der Button wird in einem separaten GUI-Buffer gezeichnet und der Rahmen des
Buttons wird immer über den Grafiken bleiben die mit :func:`Write Pixels`
gezeichnet werden. Um einen Button zu entfernen kann die Funktion
:func:`Remove GUI Button` genutzt werden.

Wenn anstatt des Textes ein Icon verwendet werden soll, kann dieses innerhalb
des Buttons mit per :func:`Write Pixels` gezeichnet werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get GUI Button',
'elements': [('Index', 'uint8', 1, 'in', {'range': (0, 11)}),
             ('Active', 'bool', 1, 'out', {}),
             ('Position X', 'uint8', 1, 'out', {'range': (0, 127)}),
             ('Position Y', 'uint8', 1, 'out', {'range': (0, 63)}),
             ('Width', 'uint8', 1, 'out', {'range': (1, 128)}),
             ('Height', 'uint8', 1, 'out', {'range': (1, 64)}),
             ('Text', 'string', 16, 'out', {})],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Returns the button properties for a given `Index` as set by :func:`Set GUI Button`.

Additionally the `Active` parameter shows if a button is currently active/visible
or not.
""",
'de':
"""
Gibt die Button-Eigenschaften für den gegebenen `Index` zurück, wie von
:func:`Set GUI Button` gesetzt.

Zusätzlich gibt der `Active`-Parameter an ob der Button aktuell aktiv/sichtbar ist
oder nicht.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Remove GUI Button',
'elements': [('Index', 'uint8', 1, 'in', {'range': [(0, 11), (255, 255)]})],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Removes the button with the given index.

You can use index 255 to remove all buttons.
""",
'de':
"""
Entfernt den Button mit dem gegebenen Index.

Index 255 kann genutzt werden um alle Buttons zu entfernen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set GUI Button Pressed Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'in', {'default': False})],
'since_firmware': [2, 0, 2],
'doc': ['ccf', {
'en':
"""
The period is the period with which the :cb:`GUI Button Pressed` callback
is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.
""",
'de':
"""
Die Periode ist die Periode mit der der :cb:`GUI Button Pressed` Callback
ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn der Wert sich im Vergleich zum letzten mal geändert
hat. Ändert der Wert sich nicht innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen des Werts.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get GUI Button Pressed Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'out', {'default': False})],
'since_firmware': [2, 0, 2],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set GUI Button Pressed Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set GUI Button Pressed Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get GUI Button Pressed',
'elements': [('Index', 'uint8', 1, 'in', {'range': (0, 11)}),
             ('Pressed', 'bool', 1, 'out', {})],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Returns the state of the button for the given index.

The state can either be pressed (true) or released (false).
""",
'de':
"""
Gibt den aktuellen Button-Zustand für einen gegebenen Index zurück.

Der Zustand kann entweder gedrückt (true) oder losgelassen (false) sein.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'GUI Button Pressed',
'elements': [('Index', 'uint8', 1, 'out', {'range': (0, 11)}),
             ('Pressed', 'bool', 1, 'out', {})],
'since_firmware': [2, 0, 2],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set GUI Button Pressed Callback Configuration`. The :word:`parameters` are the
same as for :func:`Get GUI Button Pressed`.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set GUI Button Pressed Callback Configuration`, ausgelöst. Die :word:`parameters` sind
die gleichen wie die von :func:`Get GUI Button Pressed`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set GUI Slider',
'elements': [('Index', 'uint8', 1, 'in', {'range': (0, 5)}),
             ('Position X', 'uint8', 1, 'in', {'range': (0, 128)}),
             ('Position Y', 'uint8', 1, 'in', {'range': (0, 64)}),
             ('Length', 'uint8', 1, 'in', {'range': (8, 128)}),
             ('Direction', 'uint8', 1, 'in', {'constant_group': 'Direction'}),
             ('Value', 'uint8', 1, 'in', {'range': (0, 120)})],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Draws a slider at position (x, y) with the given length.

You can use up to 6 sliders.

If you use the horizontal direction, the x position + length has to be
within the range of 1 to 128 and the y position has to be within
the range of 0 to 46.

If you use the vertical direction, the y position + length has to be
within the range of 1 to 64 and the x position has to be within
the range of 0 to 110.

The minimum length of a slider is 8.

The :word:`parameter` value is the start-position of the slider, it can
be between 0 and length-8.

You can enable a callback for the slider value with
:func:`Set GUI Slider Value Callback Configuration`.

The slider is drawn in a separate GUI buffer and it will
always stay on top of the graphics drawn with :func:`Write Pixels`. To
remove the button use :func:`Remove GUI Slider`.
""",
'de':
"""
Zeichnet einen Slider an Position (x, y) mit der gegebenen Länge.

Es können bis zu 8 Slider genutzt werden (Index 0-7).

Wenn eine horizontale Richtung verwendet wird muss Die x-Position + Länge
im Wertebereich von 1 bis 128 und die y-Position im Wertebereich von
0 bis 46 liegen.

Wenn eine vertikale Richtung verwendet wird muss Die y-Position + Länge
im Wertebereich von 1 bis 64 und die x-Position im Wertebereich von
0 bis 110 liegen.

Die minimale Länge des Sliders ist 8.

Der :word:`parameter` value ist die Startposition des Sliders. Diese kann
zwischen 0 und length-8 liegen.

Der Callback für Slider-Events kann mit der Funktion
:func:`Set GUI Slider Value Callback Configuration` eingestellt werden.

Der Slider wird in einem separaten GUI-Buffer gezeichnet und der Rahmen des
Buttons wrd immer über den Grafiken bleiben die mit :func:`Write Pixels`
gezeichnet werden. Um einen Button zu entfernen kann die Funktion
:func:`Remove GUI Slider` genutzt werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get GUI Slider',
'elements': [('Index', 'uint8', 1, 'in', {'range': (0, 5)}),
             ('Active', 'bool', 1, 'out', {}),
             ('Position X', 'uint8', 1, 'out', {'range': (0, 128)}),
             ('Position Y', 'uint8', 1, 'out', {'range': (0, 64)}),
             ('Length', 'uint8', 1, 'out', {'range': (8, 128)}),
             ('Direction', 'uint8', 1, 'out', {'constant_group': 'Direction'}),
             ('Value', 'uint8', 1, 'out', {'range': (0, 120)})],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Returns the slider properties for a given `Index` as set by :func:`Set GUI Slider`.

Additionally the `Active` parameter shows if a button is currently active/visible
or not.
""",
'de':
"""
Gibt die Slider-Eigenschaften für den gegebenen `Index` zurück, wie von
:func:`Set GUI Slider` gesetzt.

Zusätzlich gibt der `Active`-Parameter an ob der Button aktuell aktiv/sichtbar ist
oder nicht.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Remove GUI Slider',
'elements': [('Index', 'uint8', 1, 'in', {'range': [(0, 5), (255, 255)]})],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Removes the slider with the given index.

You can use index 255 to remove all slider.
""",
'de':
"""
Entfernt den Slider mit dem gegebenen Index.

Index 255 kann genutzt werden um alle Slider zu entfernen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set GUI Slider Value Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'in', {'default': False})],
'since_firmware': [2, 0, 2],
'doc': ['ccf', {
'en':
"""
The period is the period with which the :cb:`GUI Slider Value` callback
is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.
""",
'de':
"""
Die Periode ist die Periode mit der der :cb:`GUI Slider Value` Callback
ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn der Wert sich im Vergleich zum letzten mal geändert
hat. Ändert der Wert sich nicht innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen des Werts.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get GUI Slider Value Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'out', {'default': False})],
'since_firmware': [2, 0, 2],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set GUI Slider Value Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set GUI Slider Value Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get GUI Slider Value',
'elements': [('Index', 'uint8', 1, 'in', {'range': (0, 5)}),
             ('Value', 'uint8', 1, 'out', {'range': (0, 120)})],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Returns the current slider value for the given index.
""",
'de':
"""
Gibt den aktuellen Wert des Slider mit dem gegebenen Index zurück.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'GUI Slider Value',
'elements': [('Index', 'uint8', 1, 'out', {'range': (0, 5)}),
             ('Value', 'uint8', 1, 'out', {'range': (0, 120)})],
'since_firmware': [2, 0, 2],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set GUI Slider Value Callback Configuration`. The :word:`parameters` are the
same as for :func:`Get GUI Slider Value`.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set GUI Slider Value Callback Configuration`, ausgelöst. Die :word:`parameters` sind
die gleichen wie die von :func:`Get GUI Slider Value`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set GUI Tab Configuration',
'elements': [('Change Tab Config', 'uint8', 1, 'in', {'constant_group': 'Change Tab On', 'default': 3}),
             ('Clear GUI', 'bool', 1, 'in', {'default': True})],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Sets the general configuration for tabs. You can configure the tabs to only
accept clicks or only swipes (gesture left/right and right/left) or both.

Additionally, if you set `Clear GUI` to true, all of the GUI elements (buttons,
slider, graphs) will automatically be removed on every tab change.
""",
'de':
"""
Setzt die generelle Konfiguration für Tabs. Tabs können auf klicken, wischen
(links/rechts und rechts/links) oder beides reagieren.

Zusätzlich kann `Clear GUI` auf true gesetzt werden. In diesem Fall werden
bei einem wechsel der Tabs automatisch alle GUI Elemente (Buttons, Slider,
Graphen) gelöscht.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get GUI Tab Configuration',
'elements': [('Change Tab Config', 'uint8', 1, 'out', {'constant_group': 'Change Tab On', 'default': 3}),
             ('Clear GUI', 'bool', 1, 'out', {'default': True})],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Returns the tab configuration as set by :func:`Set GUI Tab Configuration`.
""",
'de':
"""
Gibt die Tab-Konfiguration zurück, wie von :func:`Set GUI Tab Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set GUI Tab Text',
'elements': [('Index', 'uint8', 1, 'in', {'range': (0, 9)}),
             ('Text', 'string', 5, 'in', {})],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Adds a text-tab with the given index.

You can use up to 10 tabs.

A text-tab with the same index as a icon-tab will overwrite the icon-tab.
""",
'de':
"""
Fügt einen Text-Tab mit dem gegebenen Index hinzu.

Es können bis zu 10 Tabs verwendet werden.

Ein Text-Tab mit dem gleichen Index wie ein Icon-Tab überschreibt diesen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get GUI Tab Text',
'elements': [('Index', 'uint8', 1, 'in', {'range': (0, 9)}),
             ('Active', 'bool', 1, 'out', {}),
             ('Text', 'string', 5, 'out', {})],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Returns the text for a given index as set by :func:`Set GUI Tab Text`.

Additionally the `Active` parameter shows if the tab is currently active/visible
or not.
""",
'de':
"""
Gibt den Text für den gegebenen Index zurück, wie von :func:`Set GUI Tab Text`
gesetzt.

Zusätzlich gibt der `Active`-Parameter an ob der Tab aktuell aktiv/sichtbar ist
oder nicht.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set GUI Tab Icon',
'elements': [('Index', 'uint8', 1, 'in', {'range': (0, 9)}),
             ('Icon', 'bool', 6*28, 'in', {})],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Adds a icon-tab with the given index. The icon can have a width of 28 pixels
with a height of 6 pixels. It is drawn line-by-line from left to right.

You can use up to 10 tabs.

A icon-tab with the same index as a text-tab will overwrite the text-tab.
""",
'de':
"""
Fügt einen Icon-Tab mit dem gegebenen Index hinzu. Das Icon kann eine Breite von
28 Pixel bei einer Höhe von 6 Pixel haben. Es wird Zeile für Zeile von links
nach rechts gezeichnet.

Es können bis zu 10 Tabs verwendet werden.

Ein Icon-Tab mit dem gleichen Index wie ein Text-Tab überschreibt diesen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get GUI Tab Icon',
'elements': [('Index', 'uint8', 1, 'in', {'range': (0, 9)}),
             ('Active', 'bool', 1, 'out', {}),
             ('Icon', 'bool', 6*28, 'out', {})],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Returns the icon for a given index as set by :func:`Set GUI Tab Icon`.

Additionally the `Active` parameter shows if the tab is currently active/visible
or not.
""",
'de':
"""
Gibt das Icon für den gegebenen Index zurück, wie von :func:`Set GUI Tab Icon`
gesetzt.

Zusätzlich gibt der `Active`-Parameter an ob der Tab aktuell aktiv/sichtbar ist
oder nicht.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Remove GUI Tab',
'elements': [('Index', 'uint8', 1, 'in', {'range': [(0, 9), (255, 255)]})],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Removes the tab with the given index.

You can use index 255 to remove all tabs.
""",
'de':
"""
Entfernt den Tab mit dem gegebenen Index.

Index 255 kann genutzt werden um alle Tabs zu entfernen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set GUI Tab Selected',
'elements': [('Index', 'uint8', 1, 'in', {'range': (0, 9)})],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Sets the tab with the given index as selected (drawn as selected on the display).
""",
'de':
"""
Setzt den Tab mit dem gegebenen Index als "selected" (wird auf dem Display als
ausgewählt gezeichnet)
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set GUI Tab Selected Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'in', {'default': False})],
'since_firmware': [2, 0, 2],
'doc': ['ccf', {
'en':
"""
The period is the period with which the :cb:`GUI Tab Selected` callback
is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.
""",
'de':
"""
Die Periode ist die Periode mit der der :cb:`GUI Tab Selected` Callback
ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn der Wert sich im Vergleich zum letzten mal geändert
hat. Ändert der Wert sich nicht innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen des Werts.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get GUI Tab Selected Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'out', {'default': False})],
'since_firmware': [2, 0, 2],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set GUI Tab Selected Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set GUI Tab Selected Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get GUI Tab Selected',
'elements': [('Index', 'int8', 1, 'out', {'range': (-1, 9)})],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Returns the index of the currently selected tab.
If there are not tabs, the returned index is -1.
""",
'de':
"""
Gibt den Index des aktuell ausgewählten Tabs zurück.
Wenn es keine Tabs gibt, wird -1 als Index zurückgegeben.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'GUI Tab Selected',
'elements': [('Index', 'int8', 1, 'out', {'range': (0, 9)})],
'since_firmware': [2, 0, 2],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set GUI Tab Selected Callback Configuration`. The :word:`parameters` are the
same as for :func:`Get GUI Tab Selected`.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set GUI Tab Selected Callback Configuration`, ausgelöst. Die :word:`parameters` sind
die gleichen wie die von :func:`Get GUI Tab Selected`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set GUI Graph Configuration',
'elements': [('Index', 'uint8', 1, 'in', {'range': (0, 3)}),
             ('Graph Type', 'uint8', 1, 'in', {'constant_group': 'Graph Type'}),
             ('Position X', 'uint8', 1, 'in', {'range': (0, 127)}),
             ('Position Y', 'uint8', 1, 'in', {'range': (0, 63)}),
             ('Width', 'uint8', 1, 'in', {'range': (0, 118)}),
             ('Height', 'uint8', 1, 'in', {'range': (0, 63)}),
             ('Text X', 'string', 4, 'in', {}),
             ('Text Y', 'string', 4, 'in', {})],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Sets the configuration for up to four graphs.

The graph type can be dot-, line- or bar-graph.

The x and y position are pixel positions.

You can add a text for the x and y axis.
The text is drawn at the inside of the graph and it can overwrite some
of the graph data. If you need the text outside of the graph you can
leave this text here empty and use :func:`Draw Text` to draw the caption
outside of the graph.

The data of the graph can be set and updated with :func:`Set GUI Graph Data`.

The graph is drawn in a separate GUI buffer and the graph-frame and data will
always stay on top of the graphics drawn with :func:`Write Pixels`. To
remove the graph use :func:`Remove GUI Graph`.
""",
'de':
"""
Setzt die Konfiguration für bis zu vier Graphen.

Der Graph kann vom Typ Dot-, Line- oder Bar-Graph sein.

Die x- und y-Positionen sind Pixel-Positionen.

Es können bis zu 4 Buchstaben Text zur Beschreibung der x- und y-Achse
genutzt werden. Der Text wird auf die Innenseite des Graphen gezeichnet und
er kann Datenpunkte des Graphen überschreiben. Wenn der Text außerhalb des
Graphen benötigt wird kann die Beschriftung hier leer gelassen werden. Der
Text kann im Nachhinein mit :func:`Draw Text` hinzugefügt werden.

Die Datenpunkte des Graphen können mit der Funktion :func:`Set GUI Graph Data`
gesetzt und aktualisiert werden.

Der Graph wird in einem separaten GUI-Buffer gezeichnet und der Rahmen sowie die
Datenpunkte des Graphen werden immer über den Grafiken bleiben die mit
:func:`Write Pixels` gezeichnet werden. Um einen Graphen zu entfernen kann die
Funktion :func:`Remove GUI Graph` genutzt werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get GUI Graph Configuration',
'elements': [('Index', 'uint8', 1, 'in', {'range': (0, 3)}),
             ('Active', 'bool', 1, 'out', {}),
             ('Graph Type', 'uint8', 1, 'out', {'constant_group': 'Graph Type'}),
             ('Position X', 'uint8', 1, 'out', {'range': (0, 127)}),
             ('Position Y', 'uint8', 1, 'out', {'range': (0, 63)}),
             ('Width', 'uint8', 1, 'out', {'range': (0, 118)}),
             ('Height', 'uint8', 1, 'out', {'range': (0, 63)}),
             ('Text X', 'string', 4, 'out', {}),
             ('Text Y', 'string', 4, 'out', {})],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Returns the graph properties for a given `Index` as set by :func:`Set GUI Graph Configuration`.

Additionally the `Active` parameter shows if a graph is currently active/visible
or not.
""",
'de':
"""
Gibt die Graph-Eigenschaften für den gegebenen `Index` zurück, wie von
:func:`Set GUI Graph Configuration` gesetzt.

Zusätzlich gibt der `Active`-Parameter an ob der Button aktuell aktiv/sichtbar ist
oder nicht.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set GUI Graph Data Low Level',
'elements': [('Index', 'uint8', 1, 'in', {'range': (0, 3)}),
             ('Data Length', 'uint16', 1, 'in', {'range': (0, 118)}),
             ('Data Chunk Offset', 'uint16', 1, 'in', {}),
             ('Data Chunk Data', 'uint8', 59, 'in', {})],
'high_level': {'stream_in': {'name': 'Data'}},
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Sets the data for a graph with the given index. You have to configure the graph with
:func:`Set GUI Graph Configuration` before you can set the first data.

The graph will show the first n values of the data that you set, where
n is the width set with :func:`Set GUI Graph Configuration`. If you set
less then n values it will show the rest of the values as zero.

The maximum number of data-points you can set is 118 (which also corresponds to the
maximum width of the graph).

You have to scale your values to be between 0 and 255. 0 will be shown
at the bottom of the graph and 255 at the top.
""",
'de':
"""
Setzt die Datenpukte für den Graph mit dem gegebenen Index. Der Graph muss mit
:func:`Set GUI Graph Configuration` konfiguriert werden bevor die ersten Daten
gesetzt werden können.

Der Graph zeigt die ersten n Werte der gesetzten Daten an, wobei n die Breite (width)
ist die mit :func:`Set GUI Graph Configuration` gesetzt wurde. Wenn weniger als
n Werte gesetzt werden, werden die restlichen Datenpunkte als 0 angezeigt.

Die maximale Anzahl an Datenpunkte die gesetzt werden kann ist 118 (dies entspricht
auch der maximalen Breite des Graphen).

Die gesetzten Werte müssen zwischen 0 und 255 skaliert werden. 0 wird unten und
255 wird oben im Graph gezeichnet.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get GUI Graph Data Low Level',
'elements': [('Index', 'uint8', 1, 'in', {'range': (0, 3)}),
             ('Data Length', 'uint16', 1, 'out', {'range': (0, 118)}),
             ('Data Chunk Offset', 'uint16', 1, 'out', {}),
             ('Data Chunk Data', 'uint8', 59, 'out', {})],
'high_level': {'stream_out': {'name': 'Data'}},
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Returns the graph data for a given index as set by :func:`Set GUI Graph Data`.
""",
'de':
"""
Gibt die Datenpunkte des Graphen mit dem gegebenen Index zurück, wie von
:func:`Set GUI Graph Data` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Remove GUI Graph',
'elements': [('Index', 'uint8', 1, 'in', {'range': [(0, 3), (255, 255)]})],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Removes the graph with the given index.

You can use index 255 to remove all graphs.
""",
'de':
"""
Entfernt den Graph mit dem gegebenen Index.

Index 255 kann genutzt werden um alle Graphen zu entfernen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Remove All GUI',
'elements': [],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Removes all GUI elements (buttons, slider, graphs, tabs).
""",
'de':
"""
Entfernt alle GUI-Elemente (Buttons, Slider, Graphen, Tabs).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Touch LED Config',
'elements': [('Config', 'uint8', 1, 'in', {'constant_group': 'Touch LED Config', 'default': 3})],
'since_firmware': [2, 0, 2],
'doc': ['af', {
'en':
"""
Sets the touch LED configuration. By default the LED is on if the
LCD is touched.

You can also turn the LED permanently on/off or show a heartbeat.

If the Bricklet is in bootloader mode, the LED is off.
""",
'de':
"""
Setzt die Konfiguration der Kommunikations-LED. Standardmäßig ist die
LED an wenn das LCD berührt wird.

Die LED kann auch permanent an/aus gestellt werden oder einen Herzschlag anzeigen.

Wenn das Bricklet sich im Bootloadermodus befindet ist die LED aus.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Touch LED Config',
'elements': [('Config', 'uint8', 1, 'out', {'constant_group': 'Touch LED Config', 'default': 3})],
'since_firmware': [2, 0, 2],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Touch LED Config`
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Touch LED Config` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Hello World',
'functions': [('setter', 'Clear Display', [], 'Clear display', None),
              ('setter', 'Write Line', [('uint8', 0), ('uint8', 0), ('string', 'Hello World')], 'Write "Hello World" starting from upper left corner of the screen', None)]
})

com['examples'].append({
'name': 'Touch',
'functions': [('callback', ('Touch Position', 'touch position'), [(('Pressure', 'Pressure'), 'uint16', 1, None, None, None), (('X', 'X'), 'uint16', 1, None, None, None), (('Y', 'Y'), 'uint16', 1, None, None, None), (('Age', 'Age'), 'uint32', 1, None, None, None)], None, None),
              ('callback', ('Touch Gesture', 'touch gesture'), [(('Gesture', 'Gesture'), 'uint8:constant', 1, None, None, None), (('Duration', 'Duration'), 'uint32', 1, None, None, None), (('Pressure Max', 'Pressure Max'), 'uint16', 1, None, None, None), (('X Start', 'X Start'), 'uint16', 1, None, None, None), (('X End', 'X End'), 'uint16', 1, None, None, None), (('Y Start', 'Y Start'), 'uint16', 1, None, None, None), (('Y End', 'Y End'), 'uint16', 1, None, None, None), (('Age', 'Age'), 'uint32', 1, None, None, None)], None, None),
              ('callback_configuration', ('Touch Position', 'touch position'), [], 100, True, None, []),
              ('callback_configuration', ('Touch Gesture', 'touch gesture'), [], 100, True, None, [])]
})

com['examples'].append({
'name': 'Big Font',
'functions': [('setter', 'Clear Display', [], 'Clear display', None),
              ('setter', 'Draw Text', [('uint8', 0), ('uint8', 0), ('uint8:constant', 9), ('bool:constant', True), ('string', '24x32')], 'Write "Hello World" with big 24x32 font', None)]
})

com['examples'].append({
'name': 'GUI',
'functions': [('callback', ('GUI Button Pressed', 'GUI button pressed'), [(('Index', 'Index'), 'uint8', 1, None, None, None), (('Pressed', 'Pressed'), 'bool', 1, None, None, None)], None, None),
              ('callback', ('GUI Slider Value', 'GUI slider value'), [(('Index', 'Index'), 'uint8', 1, None, None, None), (('Value', 'Value'), 'uint8', 1, None, None, None)], None, None),
              ('callback', ('GUI Tab Selected', 'GUI tab selected'), [(('Index', 'Index'), 'int8', 1, None, None, None)], None, None),

              ('setter', 'Clear Display', [], 'Clear display', None),
              ('setter', 'Remove All GUI', [], None, None),

              ('setter', 'Set GUI Button', [('uint8', 0), ('uint8', 0), ('uint8', 0), ('uint8', 60), ('uint8', 20), ('string', 'button')], 'Add GUI elements: Button, Slider and Graph with 60 data points', None),
              ('setter', 'Set GUI Slider', [('uint8', 0), ('uint8', 0), ('uint8', 30), ('uint8', 60), ('uint8:constant', 0), ('uint8', 50)], None, None),
              ('setter', 'Set GUI Graph Configuration', [('uint8', 0), ('uint8:constant', 1), ('uint8', 62), ('uint8', 0), ('uint8', 60), ('uint8', 52), ('string', 'X'), ('string', 'Y')], None, None),
              ('setter', 'Set GUI Graph Data', [('uint8', 0), ('uint8', list(range(20, 250, 20)))], 'Add a few data points (the remaining points will be 0)', None),

              ('setter', 'Set GUI Tab Configuration', [('uint8:constant', 3), ('bool', False)], 'Add 5 text tabs without and configure it for click and swipe without auto-redraw', None),
              ('setter', 'Set GUI Tab Text', [('uint8', 0), ('string', 'Tab A')], None, None),
              ('setter', 'Set GUI Tab Text', [('uint8', 1), ('string', 'Tab B')], None, None),
              ('setter', 'Set GUI Tab Text', [('uint8', 2), ('string', 'Tab C')], None, None),
              ('setter', 'Set GUI Tab Text', [('uint8', 3), ('string', 'Tab D')], None, None),
              ('setter', 'Set GUI Tab Text', [('uint8', 4), ('string', 'Tab E')], None, None),

              ('callback_configuration', ('GUI Button Pressed', 'GUI button pressed'), [], 100, True, None, []),
              ('callback_configuration', ('GUI Slider Value', 'GUI slider value'), [], 100, True, None, []),
              ('callback_configuration', ('GUI Tab Selected', 'GUI tab selected'), [], 100, True, None, [])]
})

# FIXME: add pixel-matrix example


def gui_button_pressed_channel(index):
    return {
        'id': 'GUI Button {}'.format(index),
        'label': 'GUI Button {}'.format(index),
        'type': 'system.rawbutton',
        'getters': [{
            'packet': 'Get GUI Button Pressed',
            'packet_params': ['{}'.format(index)],
            'transform': 'value ? CommonTriggerEvents.PRESSED : CommonTriggerEvents.RELEASED'}],

        'callbacks': [{
            'filter': 'index ==  {}'.format(index),
            'packet': 'GUI Button Pressed',
            'transform': 'pressed ? CommonTriggerEvents.PRESSED : CommonTriggerEvents.RELEASED'}],

        'is_trigger_channel': True
    }

def gui_slider_value_channel(index):
    return {
        'id': 'GUI Slider {}'.format(index),
        'label': 'GUI Slider {}'.format(index),
        'type': 'GUI Slider',
        'getters': [{
            'packet': 'Get GUI Slider Value',
            'packet_params': ['{}'.format(index)],
            'transform': 'new DecimalType(value)'}],

        'callbacks': [{
            'filter': 'index ==  {}'.format(index),
            'packet': 'GUI Slider Value',
            'transform': 'new DecimalType(value)'}],

        'is_trigger_channel': False
    }

com['openhab'] = {
    'imports': oh_generic_channel_imports() + oh_generic_trigger_channel_imports() +  ['org.eclipse.smarthome.core.library.types.StringType', 'org.eclipse.smarthome.core.library.types.DecimalType'],
    'param_groups': oh_generic_channel_param_groups(),
    'params': [{
            'name': 'Contrast',
            'type': 'integer',
            'default': '14',
            'min': '0',
            'max': '63',

            'label': 'Contrast',
            'description': "Sets the contrast of the display (0-63).",
        }, {
            'name': 'Default Backlight Intensity',
            'type': 'integer',
            'default': '100',
            'min': '0',
            'max': '100',

            'label': 'Default Backlight Intensity',
            'description': "Sets the default backlight intensity of the display (0-100).",
        }, {
            'name': 'Invert',
            'type': 'boolean',
            'default': 'false',

            'label': 'Invert',
            'description': 'Inverts the color (black/white) of the display.',
        }, {
            'name': 'Automatic Draw',
            'type': 'boolean',
            'default': 'true',

            'label': 'Automatic Draw',
            'description': 'If automatic draw is enabled, the display is automatically updated when writing text or clearing the display. If it is disabled, the changes are written into an internal buffer and only shown on the display after triggering the Draw Buffered Frame channel.',
        }, {
            'name': 'Touch LED Config',
            'type': 'integer',
            'options': [('Off', 0),
                        ('On', 1),
                        ('Show Heartbeat', 2),
                        ('Show Touch', 3)],
            'limitToOptions': 'true',
            'default': 3,
            'label': 'Touch LED Config',
            'description': 'The touch LED configuration. By default the LED is on if the LCD is touched.<br/>You can also turn the LED permanently on/off or show a heartbeat.<br/>If the Bricklet is in bootloader mode, the LED is off.'
        },
        update_interval('GUI Button', 'the GUI buttons', default=100),
        update_interval('GUI Slider', 'the GUI sliders', default=100),
        update_interval('GUI Tab', 'the GUI tabs', default=100),
        update_interval("Touch Position", "touch positions", default=100),
        update_interval("Touch Gesture", "touch gestures", default=100),
    ] ,
    'init_code': """this.setDisplayConfiguration(cfg.contrast, cfg.defaultBacklightIntensity, cfg.invert, cfg.automaticDraw);
    this.setTouchLEDConfig(cfg.touchLEDConfig);
    this.setGUIButtonPressedCallbackConfiguration(cfg.guiButtonUpdateInterval.longValue(), true);
    this.setGUISliderValueCallbackConfiguration(cfg.guiSliderUpdateInterval.longValue(), true);
    this.setGUITabSelectedCallbackConfiguration(cfg.guiTabUpdateInterval.longValue(), true);
    this.setTouchPositionCallbackConfiguration(cfg.touchPositionUpdateInterval, true);
    this.setTouchGestureCallbackConfiguration(cfg.touchGestureUpdateInterval, true);""",
    'channels': [{
                'id': 'Text',
                'type': 'Text',
                'setters': [{
                    'packet': 'Write Line',
                    'packet_params': ['Helper.parseDisplayCommandLine(cmd.toString(), logger)', 'Helper.parseDisplayCommandPosition(cmd.toString(), logger)', 'Helper.parseDisplayCommandText(cmd.toString(), logger)']}],
                'setter_command_type': "StringType",
            }, {
                'id': 'Clear Display',
                'type': 'Clear Display',
                'setters': [{
                    'packet': 'Clear Display'}],
                'setter_command_type': "StringType",
            }, {
                'id': 'Draw Buffered Frame',
                'type': 'Draw Buffered Frame',
                'setters': [{
                    'packet': 'Draw Buffered Frame',
                    'packet_params': ['true']
                }],
                'setter_command_type': "StringType",
            }, {
                'id': 'Backlight',
                'type': 'Backlight',
                'setter_command_type': "Number",
                'setters': [{
                        'packet': 'Set Display Configuration',
                        'packet_params': ['cfg.contrast', 'cmd.intValue()', 'cfg.invert', 'cfg.automaticDraw']
                    }
                ],
                'getters': [{
                    'packet': 'Get Display Configuration',
                    'transform': 'new QuantityType<>(value.backlight, SmartHomeUnits.ONE)'
                }]
            }, {
                'id': 'Touch Position',
                'label': 'Touch Position',
                'type': 'system.trigger',
                'getters': [{
                    'packet': 'Get Touch Position',
                    'transform': 'CommonTriggerEvents.PRESSED'}],

                'callbacks': [{
                    'packet': 'Touch Position',
                    'transform': 'CommonTriggerEvents.PRESSED'}],

                'is_trigger_channel': True,
            }, {
                'id': 'Touch Gesture',
                'label': 'Touch Gesture',
                'type': 'system.trigger',
                'getters': [{
                    'packet': 'Get Touch Gesture',
                    'transform': 'CommonTriggerEvents.PRESSED'}],

                'callbacks': [{
                    'packet': 'Touch Gesture',
                    'transform': 'CommonTriggerEvents.PRESSED'}],

                'is_trigger_channel': True,
            }, {
                'id': 'Selected GUI Tab',
                'type': 'Selected GUI Tab',
                'setter_command_type': "Number",
                'setters': [{
                        'packet': 'Set GUI Tab Selected',
                        'packet_params': ['cmd.intValue()']
                    }
                ],

                'getters': [{
                    'packet': 'Get GUI Tab Selected',
                    'transform': 'new DecimalType(value)'
                }],

                'callbacks': [{
                    'packet': 'GUI Tab Selected',
                    'transform': 'new DecimalType(index)'
                }]
            }
    ] + [gui_button_pressed_channel(i) for i in range(0, 12)] + [gui_slider_value_channel(i) for i in range(0, 6)],
    'channel_types': [
        oh_generic_channel_type('Text', 'String', 'Text',
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
        oh_generic_channel_type('Backlight', 'Number:Dimensionless', 'Backlight',
            description="The backlight intensity value from 0 to 100.",
            min_=0,
            max_=100),
        oh_generic_channel_type('Selected GUI Tab', 'Number', 'Selected GUI Tab',
            description="Returns the index of the currently selected tab. If there are not tabs, the returned index is -1.",
            min_=-1,
            max_=10),
        oh_generic_channel_type('GUI Slider', 'Number', 'GUI Slider',
            description="The current slider value for the given index.",
            min_=0,
            max_=120),
    ],
    'actions': ['Write Pixels', 'Read Pixels', 'Clear Display', 'Write Line', 'Draw Buffered Frame',
                'Get Touch Position', 'Get Touch Gesture',
                'Draw Line', 'Draw Box', 'Draw Text',
                'Set GUI Button', 'Get GUI Button', 'Remove GUI Button', 'Get GUI Button Pressed',
                'Set GUI Slider', 'Get GUI Slider', 'Remove GUI Slider', 'Get GUI Slider Value',
                'Set GUI Tab Configuration', 'Get GUI Tab Configuration',
                'Set GUI Tab Text', 'Get GUI Tab Text', 'Set GUI Tab Icon', 'Get GUI Tab Icon', 'Remove GUI Tab', 'Set GUI Tab Selected', 'Get GUI Tab Selected',
                'Set GUI Graph Configuration', 'Get GUI Graph Configuration', 'Set GUI Graph Data', 'Get GUI Graph Data', 'Remove GUI Graph',
                'Remove All GUI',
                'Get Display Configuration', 'Get Touch LED Config']
}
