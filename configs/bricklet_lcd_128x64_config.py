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
        'en': '7.1cm (2.8") display with 128x64 pixel and touch screen',
        'de': '7,1cm (2,8") Display mit 128x64 Pixel und Touchscreen'
    },
    'comcu': True,
    'released': True,
    'documented': True,
    'discontinued': False,
    'packets': [],
    'examples': []
}

COLOR = ('Color', [('White', False), ('Black', True)])

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

The x-axis goes from 0 to 127 and the y-axis from 0 to 63. The pixels are written
into the window line by line top to bottom and each line is written from left to
right.

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

Die X-Achse läuft von 0 bis 127 und die Y-Achse von 0 bis 63. Die Pixel werden
zeilenweise von oben nach unten geschrieben und die Zeilen werden jeweils von
links nach rechts geschrieben.

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

The x-axis goes from 0 to 127 and the y-axis from 0 to 63. The pixels are read
from the window line by line top to bottom and each line is read from left to
right.

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
             ('Backlight', 'uint8', 1, 'in'),
             ('Invert', 'bool', 1, 'in'),
             ('Automatic Draw', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the configuration of the display.

You can set a contrast value from 0 to 63, a backlight intensity value
from 0 to 100 and you can invert the color (white/black) of the display.

If automatic draw is set to *true*, the display is automatically updated with every
call of :func:`Write Pixels` and :func:`Write Line`. If it is set to false, the
changes are written into an internal buffer and only shown on the display after
a call of :func:`Draw Buffered Frame`.

The default values are contrast 14, backlight intensity 100, inverting off
and automatic draw on.
""",
'de':
"""
Setzt die Konfiguration des Displays.

Der Kontrast kann zwischen 0 und 63, die Backlight-Intensität zwischen 0 und 100
und das Farbschema invertiert (weiß/schwarz) eingestellt werden.

Wenn Automatic Draw aktiviert (*true*) ist dann wird das Display bei jedem
Aufruf von :func:`Write Pixels` und :func:`Write Line` aktualisiert. Wenn
Automatic Draw deaktiviert (*false*) ist, dann werden Änderungen in einen
internen Buffer geschrieben, der dann bei bei einem Aufruf von
:func:`Draw Buffered Frame` auf dem Display angezeigt wird.

Standardwerte: Kontrast 14, Backlight-Intensität 100, Invertierung aus und
Automatic Draw aktiviert.
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
'elements': [('Pressure', 'uint16', 1, 'out'),
             ('X', 'uint16', 1, 'out'),
             ('Y', 'uint16', 1, 'out'),
             ('Age', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the last valid touch position:

* Pressure: Amount of pressure applied by the user (0-300)
* X: Touch position on x-axis (0-127)
* Y: Touch position on y-axis (0-63)
* Age: Age of touch press in ms (how long ago it was)
""",
'de':
"""
Gibt die letzte gültige Touch-Position zurück:

* Pressure: Anpressdruck des Touches (0-300)
* X: Touch-Position auf der X-Achse (0-127)
* Y: Touch-Position auf der Y-Achse (0-63)
* Age: Alter des Touches in ms (wie lange ist die Erkennung des Touches her)
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
             ('Y', 'uint16', 1, 'out'),
             ('Age', 'uint32', 1, 'out')],
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
'elements': [('Gesture', 'uint8', 1, 'out', ('Gesture', [('Left To Right', 0),
                                                         ('Right To Left', 1),
                                                         ('Top To Bottom', 2),
                                                         ('Bottom To Top', 3)])),
             ('Duration', 'uint32', 1, 'out'),
             ('Pressure Max', 'uint16', 1, 'out'),
             ('X Start', 'uint16', 1, 'out'),
             ('Y Start', 'uint16', 1, 'out'),
             ('X End', 'uint16', 1, 'out'),
             ('Y End', 'uint16', 1, 'out'),
             ('Age', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns one of four touch gestures that can be automatically detected by the Bricklet.

The gestures are swipes from left to right, right to left, top to bottom and bottom to top.

Additionally to the gestures a vector with a start and end position of the gesture is
provided. You can use this vector do determine a more exact location of the gesture (e.g.
the swipe from top to bottom was on the left or right part of the screen).

The age parameter corresponds to the age of gesture in ms (how long ago it was).
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

Das Age Parameter gibt das Alter der Geste in ms an (wie lange ist die Erkennung
der Geste her).
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
             ('Pressure Max', 'uint16', 1, 'out'),
             ('X Start', 'uint16', 1, 'out'),
             ('Y Start', 'uint16', 1, 'out'),
             ('X End', 'uint16', 1, 'out'),
             ('Y End', 'uint16', 1, 'out'),
             ('Age', 'uint32', 1, 'out')],
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
'elements': [('Position X Start', 'uint8', 1, 'in'),
             ('Position Y Start', 'uint8', 1, 'in'),
             ('Position X End', 'uint8', 1, 'in'),
             ('Position Y End', 'uint8', 1, 'in'),
             ('Color', 'bool', 1, 'in', COLOR)],
'since_firmware': [2, 0, 2],
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
'name': 'Draw Box',
'elements': [('Position X Start', 'uint8', 1, 'in'),
             ('Position Y Start', 'uint8', 1, 'in'),
             ('Position X End', 'uint8', 1, 'in'),
             ('Position Y End', 'uint8', 1, 'in'),
             ('Fill', 'bool', 1, 'in'),
             ('Color', 'bool', 1, 'in', COLOR)],
'since_firmware': [2, 0, 2],
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
'name': 'Draw Text',
'elements': [('Position X', 'uint8', 1, 'in'),
             ('Position Y', 'uint8', 1, 'in'),
             ('Font', 'uint8', 1, 'in',  ('Font', [('6x8', 0),
                                                   ('6x16', 1),
                                                   ('6x24', 2),
                                                   ('6x32', 3),
                                                   ('12x16', 4),
                                                   ('12x24', 5),
                                                   ('12x32', 6),
                                                   ('18x24', 7),
                                                   ('18x32', 8),
                                                   ('24x32', 9)])),
             ('Color', 'bool', 1, 'in', COLOR),
             ('Text', 'string', 22, 'in')],
'since_firmware': [2, 0, 2],
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
'name': 'Set GUI Button',
'elements': [('Index', 'uint8', 1, 'in'),
             ('Position X', 'uint8', 1, 'in'),
             ('Position Y', 'uint8', 1, 'in'),
             ('Width', 'uint8', 1, 'in'),
             ('Height', 'uint8', 1, 'in'),
             ('Text', 'string', 16, 'in')],
'since_firmware': [2, 0, 2],
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
'name': 'Get GUI Button',
'elements': [('Index', 'uint8', 1, 'in'),
             ('Active', 'bool', 1, 'out'),
             ('Position X', 'uint8', 1, 'out'),
             ('Position Y', 'uint8', 1, 'out'),
             ('Width', 'uint8', 1, 'out'),
             ('Height', 'uint8', 1, 'out'),
             ('Text', 'string', 16, 'out')],
'since_firmware': [2, 0, 2],
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
'name': 'Remove GUI Button',
'elements': [('Index', 'uint8', 1, 'in')],
'since_firmware': [2, 0, 2],
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
'name': 'Set GUI Button Pressed Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [2, 0, 2],
'doc': ['ccf', {
'en':
"""
The period in ms is the period with which the :cb:`GUI Button Pressed` callback
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
Die Periode in ms ist die Periode mit der der :cb:`GUI Button Pressed` Callback
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
'name': 'Get GUI Button Pressed Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
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
'elements': [('Index', 'uint8', 1, 'in'),
             ('Pressed', 'bool', 1, 'out')],
'since_firmware': [2, 0, 2],
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
'type': 'callback',
'name': 'GUI Button Pressed',
'elements': [('Index', 'uint8', 1, 'out'),
             ('Pressed', 'bool', 1, 'out')],
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
'elements': [('Index', 'uint8', 1, 'in'),
             ('Position X', 'uint8', 1, 'in'),
             ('Position Y', 'uint8', 1, 'in'),
             ('Length', 'uint8', 1, 'in'),
             ('Direction', 'uint8', 1, 'in', ('Direction', [('Horizontal', 0),
                                                            ('Vertical', 1)])),
             ('Value', 'uint8', 1, 'in')],
'since_firmware': [2, 0, 2],
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
'name': 'Get GUI Slider',
'elements': [('Index', 'uint8', 1, 'in'),
             ('Active', 'bool', 1, 'out'),
             ('Position X', 'uint8', 1, 'out'),
             ('Position Y', 'uint8', 1, 'out'),
             ('Length', 'uint8', 1, 'out'),
             ('Direction', 'uint8', 1, 'out', ('Direction', [('Horizontal', 0),
                                                             ('Vertical', 1)])),
             ('Value', 'uint8', 1, 'out')],
'since_firmware': [2, 0, 2],
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
'name': 'Remove GUI Slider',
'elements': [('Index', 'uint8', 1, 'in')],
'since_firmware': [2, 0, 2],
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
'name': 'Set GUI Slider Value Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [2, 0, 2],
'doc': ['ccf', {
'en':
"""
The period in ms is the period with which the :cb:`GUI Slider Value` callback
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
Die Periode in ms ist die Periode mit der der :cb:`GUI Slider Value` Callback
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
'name': 'Get GUI Slider Value Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
'since_firmware': [2, 0, 2],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set GUI Slider Changed Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set GUI Slider Changed Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get GUI Slider Value',
'elements': [('Index', 'uint8', 1, 'in'),
             ('Value', 'uint8', 1, 'out')],
'since_firmware': [2, 0, 2],
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
'type': 'callback',
'name': 'GUI Slider Value',
'elements': [('Index', 'uint8', 1, 'out'),
             ('Value', 'uint8', 1, 'out')],
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
'elements': [('Change Tab Config', 'uint8', 1, 'in', ('Change Tab On', [('Click', 1),
                                                                        ('Swipe', 2),
                                                                        ('Click And Swipe', 3)])),
             ('Clear GUI', 'bool', 1, 'in')],
'since_firmware': [2, 0, 2],
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
'name': 'Get GUI Tab Configuration',
'elements': [('Change Tab Config', 'uint8', 1, 'out', ('Change Tab On', [('Click', 1),
                                                                         ('Swipe', 2),
                                                                         ('Click And Swipe', 3)])),
             ('Clear GUI', 'bool', 1, 'out')],
'since_firmware': [2, 0, 2],
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
'name': 'Set GUI Tab Text',
'elements': [('Index', 'uint8', 1, 'in'),
             ('Text', 'string', 8, 'in')],
'since_firmware': [2, 0, 2],
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
'name': 'Get GUI Tab Text',
'elements': [('Index', 'uint8', 1, 'in'),
             ('Active', 'bool', 1, 'out'),
             ('Text', 'string', 8, 'out')],
'since_firmware': [2, 0, 2],
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
'name': 'Set GUI Tab Icon',
'elements': [('Index', 'uint8', 1, 'in'),
             ('Icon', 'bool', 6*28, 'in')],
'since_firmware': [2, 0, 2],
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
'name': 'Get GUI Tab Icon',
'elements': [('Index', 'uint8', 1, 'in'),
             ('Active', 'bool', 1, 'out'),
             ('Icon', 'bool', 6*28, 'out')],
'since_firmware': [2, 0, 2],
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
'name': 'Remove GUI Tab',
'elements': [('Index', 'uint8', 1, 'in')],
'since_firmware': [2, 0, 2],
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
'name': 'Set GUI Tab Current',
'elements': [('Index', 'uint8', 1, 'in')],
'since_firmware': [2, 0, 2],
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
'name': 'Set GUI Tab Current Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [2, 0, 2],
'doc': ['ccf', {
'en':
"""
The period in ms is the period with which the :cb:`GUI Tab Current` callback
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
Die Periode in ms ist die Periode mit der der :cb:`GUI Tab Current` Callback
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
'name': 'Get GUI Tab Current Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
'since_firmware': [2, 0, 2],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set GUI Tab Current Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set GUI Tab Current Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get GUI Tab Current',
'elements': [('Index', 'int8', 1, 'out')],
'since_firmware': [2, 0, 2],
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
'type': 'callback',
'name': 'GUI Tab Current',
'elements': [('Index', 'int8', 1, 'out')],
'since_firmware': [2, 0, 2],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set GUI Tab Current Callback Configuration`. The :word:`parameters` are the
same as for :func:`Get GUI Tab Current`.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set GUI Tab Current Callback Configuration`, ausgelöst. Die :word:`parameters` sind
die gleichen wie die von :func:`Get GUI Tab Current`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set GUI Graph Configuration',
'elements': [('Index', 'uint8', 1, 'in'),
             ('Graph Type', 'uint8', 1, 'in', ('Graph Type', [('Dot',  0),
                                                              ('Line', 1),
                                                              ('Bar',  2)])),
             ('Position X', 'uint8', 1, 'in'),
             ('Position Y', 'uint8', 1, 'in'),
             ('Width', 'uint8', 1, 'in'),
             ('Height', 'uint8', 1, 'in'),
             ('Text X', 'string', 4, 'in'),
             ('Text Y', 'string', 4, 'in')],
'since_firmware': [2, 0, 2],
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
'name': 'Get GUI Graph Configuration',
'elements': [('Index', 'uint8', 1, 'in'),
             ('Active', 'bool', 1, 'out'),
             ('Graph Type', 'uint8', 1, 'out', ('Graph Type', [('Dot',  0),
                                                               ('Line', 1),
                                                               ('Bar',  2)])),
             ('Position X', 'uint8', 1, 'out'),
             ('Position Y', 'uint8', 1, 'out'),
             ('Width', 'uint8', 1, 'out'),
             ('Height', 'uint8', 1, 'out'),
             ('Text X', 'string', 4, 'out'),
             ('Text Y', 'string', 4, 'out')],
'since_firmware': [2, 0, 2],
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
'name': 'Set GUI Graph Data Low Level',
'elements': [('Index', 'uint8', 1, 'in'),
             ('Data Length', 'uint16', 1, 'in'),
             ('Data Chunk Offset', 'uint16', 1, 'in'),
             ('Data Chunk Data', 'uint8', 59, 'in')],
'high_level': {'stream_in': {'name': 'Data'}},
'since_firmware': [2, 0, 2],
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
'name': 'Get GUI Graph Data Low Level',
'elements': [('Index', 'uint8', 1, 'in'),
             ('Data Length', 'uint16', 1, 'out'),
             ('Data Chunk Offset', 'uint16', 1, 'out'),
             ('Data Chunk Data', 'uint8', 59, 'out')],
'high_level': {'stream_out': {'name': 'Data'}},
'since_firmware': [2, 0, 2],
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
'name': 'Remove GUI Graph',
'elements': [('Index', 'uint8', 1, 'in')],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""

index = 255 => remove all graphs

""",
'de':
"""

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
              ('callback', ('Touch Gesture', 'touch gesture'), [(('Gesture', 'Gesture'), 'uint8', 1, None, None, None), (('Duration', 'Duration'), 'uint32', 1, None, None, None), (('Pressure Max', 'Pressure Max'), 'uint16', 1, None, None, None), (('X Start', 'X Start'), 'uint16', 1, None, None, None), (('X End', 'X End'), 'uint16', 1, None, None, None), (('Y Start', 'Y Start'), 'uint16', 1, None, None, None), (('Y End', 'Y End'), 'uint16', 1, None, None, None), (('Age', 'Age'), 'uint32', 1, None, None, None)], None, None),
              ('callback_configuration', ('Touch Position', 'touch position'), [], 100, True, None, []),
              ('callback_configuration', ('Touch Gesture', 'touch gesture'), [], 100, True, None, [])]
})

# FIXME: add pixel-matrix example
