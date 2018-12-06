# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# LCD 128x64 Bricklet communication config

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

This function is a 1:1 replacement for the function with the same name
in the LCD 20x4 Bricklet. You can draw text at a specific pixel position
and with different font sizes with the :func:`Draw Text` function.
""",
'de':
"""
Schreibt einen Text in die angegebene Zeile (0 bis 7) mit einer vorgegebenen
Position (0 bis 21). Der Text kann maximal 22 Zeichen lang sein.

Beispiel: (1, 10, "Hallo") schreibt *Hallo* in die Mitte der zweiten Zeile
des Displays.

Das Display nutzt einen speziellen 5x7 Pixel Zeichensatz. Der Zeichensatz
kann mit Hilfe von Brick Viewer angezeigt werden.

Diese Funktion ist ein 1:1-Ersatz für die Funktion mit dem gleichen Namen
im LCD 20x4 Bricklet. Mit der Funktion :func:`Draw Text` kann Text Pixelgenau
und mit unterschiedlichen Font-Größen gezeichnet werden.
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
Draws a white or black line from (x, y)-start to (x, y)-end. 
The x values have to be within the range of 0 to 127 and the y
values have t be within the range of 0 to 63.
""",
'de':
"""
Zeichnet eine weiße oder schwarze Linie von (x, y)-start nach
(x, y)-end. Der Wertebereich für die x-Werte ist 0 bis 127 und
der Wertebereich für die y-Werte ist 0-63.
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
Draws a white or black box from (x, y)-start to (x, y)-end.
The x values have to be within the range of 0 to 127 and the y
values have to be within the range of 0 to 63.

If you set fill to true, the box will be filled with the
color. Otherwise only the outline will be drawn.
""",
'de':
"""
Zeichnet ein weißes oder schwarzes Rechteck von (x, y)-start nach
(x, y)-end. Der Wertebereich für die x-Werte ist 0 bis 127 und
der Wertebereich für die y-Werte ist 0-63.

Wenn fill auf true gesetzt wird, wird das Rechteck mit
der angegebenen Farbe ausgefüllt. Ansonsten wird nur der Umriss
gezeichnet.
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
Draws a text with up to 22 characters at the pixel position (x, y).

The x values have to be within the range of 0 to 127 and the y
values have to be within the range of 0 to 63.

You can use one of 9 different font sizes and draw the text in white or black.
""",
'de':
"""
Zeichnet einen Text mit bis zu 22 Buchstaben an die Pixelposition (x, y).

Die Wertebereich für die x-Werte ist 0 bis 127 und
der Wertebereich für die y-Werte ist 0-63.

Es können 9 unterschiedliche Font-Größen genutzt werden und der Text
kann in weiß oder schwarz gezeichnet werden.
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
Draws a clickable button at position (x, y) with the given text 
of up to 16 characters.

You can use up to 12 buttons (index 0-11).

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
Zeichnet einen klickbaren Button an Position (x, y) mit dem gegebenem
Text von bis zu 16 Zeichen.

Es können bis zu 12 Buttons genutzt werden (Index 0-11).

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
'elements': [('Index', 'uint8', 1, 'in')],
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
Draws a slider at position (x, y) with the given length.

You can use up to 6 sliders (index 0-5).

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

Das :word:`parameter` value ist die Startposition des Sliders. Diese kann
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
'elements': [('Index', 'uint8', 1, 'in')],
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
'elements': [('Index', 'uint8', 1, 'in'),
             ('Value', 'uint8', 1, 'out')],
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
Sets the general configuration for tabs. You can configure the tabs to only
accept clicks or only swipes (gesture left/right and right/left) or both.

Additionally, if you set `Clear GUI` to true, all of the GUI elements (buttons, 
slider, graphs) will automatically be removed on every tab change.

By default click and swipe as well as automatic GUI clear is enabled.
""",
'de':
"""
Setzt die generelle Konfiguration für Tabs. Tabs können auf klicken, wischen 
(links/rechts und rechts/links) oder beides reagieren.

Zusätzlich kann `Clear GUI` auf true gesetzt werden. In diesem Fall werden
bei einem wechsel der Tabs automatisch alle GUI Elemente (Buttons, Slider,
Graphen) gelöscht.

Standardmäßig ist klicken und wischen sowie das automatische löschen der GUI
aktiviert.
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
'elements': [('Index', 'uint8', 1, 'in'),
             ('Text', 'string', 5, 'in')],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Adds a text-tab with the given index. The text can have a length of up to 5 characters.

You can use up to 10 tabs (index 0-9).

A text-tab with the same index as a icon-tab will overwrite the icon-tab.
""",
'de':
"""
Fügt einen Text-Tab mit dem gegebenen Index hinzu. Der Text kann eine Länge von
bis zu 5 Buchstaben haben.

Es können bis zu 10 Tabs verwendet werden (Index 0-9).

Ein Text-Tab mit dem gleichen Index wie ein Icon-Tab überschreibt diesen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get GUI Tab Text',
'elements': [('Index', 'uint8', 1, 'in'),
             ('Active', 'bool', 1, 'out'),
             ('Text', 'string', 5, 'out')],
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
'elements': [('Index', 'uint8', 1, 'in'),
             ('Icon', 'bool', 6*28, 'in')],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Adds a icon-tab with the given index. The icon can have a width of 28 pixels
with a height of 6 pixels. It is drawn line-by-line from left to right.

You can use up to 10 tabs (index 0-9).

A icon-tab with the same index as a text-tab will overwrite the text-tab.
""",
'de':
"""
Fügt einen Icon-Tab mit dem gegebenen Index hinzu. Das Icon kann eine Breite von
28 Pixel bei einer Höhe von 6 Pixel haben. Es wird Zeile für Zeile von links
nach rechts gezeichnet.

Es können bis zu 10 Tabs verwendet werden (Index 0-9).

Ein Icon-Tab mit dem gleichen Index wie ein Text-Tab überschreibt diesen.
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
'elements': [('Index', 'uint8', 1, 'in')],
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
'elements': [('Index', 'uint8', 1, 'in')],
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
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [2, 0, 2],
'doc': ['ccf', {
'en':
"""
The period in ms is the period with which the :cb:`GUI Tab Selected` callback
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
Die Periode in ms ist die Periode mit der der :cb:`GUI Tab Selected` Callback
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
'name': 'Get GUI Tab Selected Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
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
'elements': [('Index', 'int8', 1, 'out')],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Returns the index of the currently selected tab.
""",
'de':
"""
Gibt den Index des aktuell ausgewählten Tabs zurück.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'GUI Tab Selected',
'elements': [('Index', 'int8', 1, 'out')],
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
Sets the configuration for up to four graphs (index 0-3).

The graph type can be dot-, line- or bar-graph.

The x and y position are pixel positions. They have to be within
the range of (0, 0) to (127, 63). The maximum width is 118 and the
maximum height is 63.

You can add a text for the x and y axis with at most 4 characters each.
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
Setzt die Konfiguration für bis zu vier Graphen (Index 0-3).

Der Graph kann vom Typ Dot-, Line- oder Bar-Graph sein.

Die x- und y-Positionen sind Pixel-Positionen. Diese sind im Wertebereich
von (0, 0) bis (127, 63). Die Maximale Breite (width) ist 118 und die maximale
Höhe (height) ist 63.

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
'elements': [('Index', 'uint8', 1, 'in'),
             ('Data Length', 'uint16', 1, 'in'),
             ('Data Chunk Offset', 'uint16', 1, 'in'),
             ('Data Chunk Data', 'uint8', 59, 'in')],
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
'elements': [('Index', 'uint8', 1, 'in'),
             ('Data Length', 'uint16', 1, 'out'),
             ('Data Chunk Offset', 'uint16', 1, 'out'),
             ('Data Chunk Data', 'uint8', 59, 'out')],
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
'elements': [('Index', 'uint8', 1, 'in')],
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
'elements': [('Config', 'uint8', 1, 'in', ('Touch LED Config', [('Off', 0),
                                                                ('On', 1),
                                                                ('Show Heartbeat', 2),
                                                                ('Show Touch', 3)]))],
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

Wenn das Bricklet sich im Bootlodermodus befindet ist die LED aus.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Touch LED Config',
'elements': [('Config', 'uint8', 1, 'out', ('Touch LED Config', [('Off', 0),
                                                                 ('On', 1),
                                                                 ('Show Heartbeat', 2),
                                                                 ('Show Touch', 3)]))],
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
              ('callback', ('Touch Gesture', 'touch gesture'), [(('Gesture', 'Gesture'), 'uint8', 1, None, None, None), (('Duration', 'Duration'), 'uint32', 1, None, None, None), (('Pressure Max', 'Pressure Max'), 'uint16', 1, None, None, None), (('X Start', 'X Start'), 'uint16', 1, None, None, None), (('X End', 'X End'), 'uint16', 1, None, None, None), (('Y Start', 'Y Start'), 'uint16', 1, None, None, None), (('Y End', 'Y End'), 'uint16', 1, None, None, None), (('Age', 'Age'), 'uint32', 1, None, None, None)], None, None),
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
'functions': [('callback', ('GUI Button Pressed', 'gui button pressed'), [(('Index', 'Index'), 'uint8', 1, None, None, None), (('Pressed', 'Pressed'), 'bool', 1, None, None, None)], None, None),
              ('callback', ('GUI Slider Value', 'gui slider value'), [(('Index', 'Index'), 'uint8', 1, None, None, None), (('Value', 'Value'), 'uint8', 1, None, None, None)], None, None),
              ('callback', ('GUI Tab Selected', 'gui tab selected'), [(('Index', 'Index'), 'int8', 1, None, None, None)], None, None),

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

              ('callback_configuration', ('GUI Button Pressed', 'gui button pressed'), [], 100, True, None, []),
              ('callback_configuration', ('GUI Slider Value', 'gui slider value'), [], 100, True, None, []),
              ('callback_configuration', ('GUI Tab Selected', 'gui tab selected'), [], 100, True, None, [])]

})

# FIXME: add pixel-matrix example
