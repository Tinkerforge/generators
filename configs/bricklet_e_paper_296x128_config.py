# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# E-Paper 296x128 Bricklet communication config

from openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2146,
    'name': 'E Paper 296x128',
    'display_name': 'E-Paper 296x128',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Three color 296x128 e-paper display',
        'de': 'Dreifarbiges 296x128 E-Paper-Display'
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
'name': 'Draw Status',
'type': 'uint8',
'constants': [('Idle', 0),
              ('Copying', 1),
              ('Drawing', 2)]
})

com['constant_groups'].append({
'name': 'Color',
'type': 'uint8',
'constants': [('Black', 0),
              ('White', 1),
              ('Red', 2),
              ('Gray', 2)]
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
'name': 'Orientation',
'type': 'uint8',
'constants': [('Horizontal', 0),
              ('Vertical', 1)]
})

com['constant_groups'].append({
'name': 'Update Mode',
'type': 'uint8',
'constants': [('Default', 0),
              ('Black White', 1),
              ('Delta', 2)]
})

com['constant_groups'].append({
'name': 'Display Type',
'type': 'uint8',
'constants': [('Black White Red', 0),
              ('Black White Gray', 1)]
})

com['packets'].append({
'type': 'function',
'name': 'Draw',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Draws the current black/white and red or gray buffer to the e-paper display.

The Bricklet does not have any double-buffering. You should not call
this function while writing to the buffer. See :func:`Get Draw Status`.
""",
'de':
"""
Zeichnet den aktuellen Schwarz-/Weiß- und Rot- oder Grau-Buffer auf
das E-Paper-Display.

Das Bricklet nutzt kein Double-Buffering. Diese Funktion sollte daher
nicht aufgerufen werden während in den Buffer geschrieben wird.
Siehe :func:`Get Draw Status`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Draw Status',
'elements': [('Draw Status', 'uint8', 1, 'out', {'constant_group': 'Draw Status'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns one of three draw statuses:

* Idle
* Copying: Data is being copied from the buffer of the Bricklet to the buffer of the display.
* Drawing: The display is updating its content (during this phase the flickering etc happens).

You can write to the buffer (through one of the write or draw functions) when the status is
either *idle* or *drawing*. You should not write to the buffer while it is being *copied* to the
display. There is no double-buffering.
""",
'de':
"""
Gibt einen von drei möglichen Status zurück:

* Idle
* Copying: Daten werden vom Buffer des Bricklets in den Buffer des Displays kopiert.
* Drawing: Das Display aktualisiert den Inhalt (während dieser Phase flackert das Display).

Der Buffer kann beschrieben werden (durch eine der *write*- oder *draw*-Funktionen) wenn der
Status entweder *idle* oder *drawing* ist. Der Buffer sollte nicht beschrieben werden während
er *kopiert* wird. Es findet kein Double-Buffering statt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Write Black White Low Level',
'elements': [('X Start', 'uint16', 1, 'in', {'range': (0, 295)}),
             ('Y Start', 'uint8', 1, 'in', {'range': (0, 127)}),
             ('X End', 'uint16', 1, 'in', {'range': (0, 295)}),
             ('Y End', 'uint8', 1, 'in', {'range': (0, 127)}),
             ('Pixels Length', 'uint16', 1, 'in', {'range': (0, 296*128)}),
             ('Pixels Chunk Offset', 'uint16', 1, 'in', {}),
             ('Pixels Chunk Data', 'bool', 54*8, 'in', {})],
'high_level': {'stream_in': {'name': 'Pixels'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes black/white pixels to the specified window into the buffer.

The pixels are written into the window line by line top to bottom
and each line is written from left to right.

The value 0 (false) corresponds to a black pixel and the value 1 (true) to a
white pixel.

This function writes the pixels into the black/white pixel buffer, to draw the
buffer to the display use :func:`Draw`.

Use :func:`Write Color` to write red or gray pixels.
""",
'de':
"""
Schreibt schwarze/weiße Pixel in das angegebene Fenster in den Buffer.

Die Pixel werden zeilenweise von oben nach unten geschrieben
und die Zeilen werden jeweils von links nach rechts geschrieben.

Der Wert 0 (false) entspricht einem schwarzen Pixel und der Wert 1 (true) einem
weißen Pixel.

Diese Funktion schreibt Pixel in den Schwarz-/Weiß-Buffer. Der Buffer kann mit der Funktion :func:`Draw`
auf das Display übertragen werden.

Die Funktion :func:`Write Color` kann genutzt werden um rote oder graue Pixel zu
schreiben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Read Black White Low Level',
'elements': [('X Start', 'uint16', 1, 'in', {'range': (0, 295)}),
             ('Y Start', 'uint8', 1, 'in', {'range': (0, 127)}),
             ('X End', 'uint16', 1, 'in', {'range': (0, 295)}),
             ('Y End', 'uint8', 1, 'in', {'range': (0, 127)}),
             ('Pixels Length', 'uint16', 1, 'out', {'range': (0, 296*128)}),
             ('Pixels Chunk Offset', 'uint16', 1, 'out', {}),
             ('Pixels Chunk Data', 'bool', 58*8, 'out', {})],
'high_level': {'stream_out': {'name': 'Pixels'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current content of the black/white pixel buffer for the specified window.

The pixels are read into the window line by line top to bottom and
each line is read from left to right.

The current content of the buffer does not have to be the current content of the display.
It is possible that the data was not drawn to the display yet and after a restart of
the Bricklet the buffer will be reset to black, while the display retains its content.
""",
'de':
"""
Gibt den aktuellen Inhalt des Schwarz-/Weiß-Buffers für das spezifizierte Fenster
zurück.

Die Pixel werden zeilenweise von oben nach unten gelesen und die Zeilen
werden jeweils von links nach rechts gelesen.

Der aktuelle Inhalt des Buffers muss nicht dem aktuellen Inhalt des Displays entsprechen.
Es ist möglich das der Buffer noch nicht auf das Display übertragen wurde und nach einem
Neustart wird der Buffer des Bricklets als schwarz initialisiert, während das Display
den Inhalt beibehält.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Write Color Low Level',
'elements': [('X Start', 'uint16', 1, 'in', {'range': (0, 295)}),
             ('Y Start', 'uint8', 1, 'in', {'range': (0, 127)}),
             ('X End', 'uint16', 1, 'in', {'range': (0, 295)}),
             ('Y End', 'uint8', 1, 'in', {'range': (0, 127)}),
             ('Pixels Length', 'uint16', 1, 'in', {'range': (0, 296*128)}),
             ('Pixels Chunk Offset', 'uint16', 1, 'in', {}),
             ('Pixels Chunk Data', 'bool', 54*8, 'in', {})],
'high_level': {'stream_in': {'name': 'Pixels'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
The E-Paper 296x128 Bricklet is available with the colors black/white/red and
black/white/gray. Depending on the model this function writes either red or
gray pixels to the specified window into the buffer.

The pixels are written into the window line by line top to bottom
and each line is written from left to right.

The value 0 (false) means that this pixel does not have color. It will be either black
or white (see :func:`Write Black White`). The value 1 (true) corresponds to a red or gray
pixel, depending on the Bricklet model.

This function writes the pixels into the red or gray pixel buffer, to draw the buffer
to the display use :func:`Draw`.

Use :func:`Write Black White` to write black/white pixels.
""",
'de':
"""
Das E-Paper 296x128 Bricklet ist in den Farben schwarz/weiß/rot sowie schwarz/weiß/grau
verfügbar. Abhängig vom verwendeten Modell schreibt diese Funktion entweder rote oder
graue Pixel in das spezifizierte Fenster des Buffers.

Die Pixel werden zeilenweise von oben nach unten geschrieben
und die Zeilen werden jeweils von links nach rechts geschrieben.

Der Wert 0 (false) bedeutet dass das Pixel keine Farbe hat. Es ist in diesem Fall entweder
schwarz oder weiß (siehe :func:`Write Black White`). Der Wert 1 (true) entspricht einem
roten oder grauen Pixel, abhängig vom Modell des Bricklets.

Diese Funktion schreibt Pixel in den Rot- oder Grau-Buffer. Der Buffer kann mit der Funktion :func:`Draw`
auf das Display übertragen werden.

Die Funktion :func:`Write Black White` kann genutzt werden um schwarze/weiße Pixel zu
schreiben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Read Color Low Level',
'elements': [('X Start', 'uint16', 1, 'in', {'range': (0, 295)}),
             ('Y Start', 'uint8', 1, 'in', {'range': (0, 127)}),
             ('X End', 'uint16', 1, 'in', {'range': (0, 295)}),
             ('Y End', 'uint8', 1, 'in', {'range': (0, 127)}),
             ('Pixels Length', 'uint16', 1, 'out', {'range': (0, 296*128)}),
             ('Pixels Chunk Offset', 'uint16', 1, 'out', {}),
             ('Pixels Chunk Data', 'bool', 58*8, 'out', {})],
'high_level': {'stream_out': {'name': 'Pixels'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current content of the red or gray pixel buffer for the specified window.

The pixels are written into the window line by line top to bottom
and each line is written from left to right.

The current content of the buffer does not have to be the current content of the display.
It is possible that the data was not drawn to the display yet and after a restart of
the Bricklet the buffer will be reset to black, while the display retains its content.
""",
'de':
"""
Gibt den aktuellen Inhalt des Rot- oder Grau-Buffers für das spezifizierte Fenster
zurück.

Die Pixel werden zeilenweise von oben nach unten gelesen
und die Zeilen werden jeweils von links nach rechts gelesen.

Der aktuelle Inhalt des Buffers muss nicht dem aktuellen Inhalt des Displays entsprechen.
Es ist möglich das der Buffer noch nicht auf das Display übertragen wurde und nach einem
Neustart wird der Buffer des Bricklets als schwarz initialisiert, während das Display
den Inhalt beibehält.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Fill Display',
'elements': [('Color', 'uint8', 1, 'in', {'constant_group': 'Color'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Fills the complete content of the display with the given color.

This function writes the pixels into the black/white/red|gray pixel buffer, to draw the buffer
to the display use :func:`Draw`.
""",
'de':
"""
Füllt den kompletten Inhalt des Displays mit der gegebenen Farbe.

Diese Funktion schreibt Pixel in den Schwarz-/Weiß-/Grau|Rot-Buffer. Der Buffer kann mit der Funktion :func:`Draw`
auf das Display übertragen werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Draw Text',
'elements': [('Position X', 'uint16', 1, 'in', {'range': (0, 295)}),
             ('Position Y', 'uint8', 1, 'in', {'range': (0, 127)}),
             ('Font', 'uint8', 1, 'in', {'constant_group': 'Font'}),
             ('Color', 'uint8', 1, 'in', {'constant_group': 'Color'}),
             ('Orientation', 'uint8', 1, 'in', {'constant_group': 'Orientation'}),
             ('Text', 'string', 50, 'in', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Draws a text with up to 50 characters at the pixel position (x, y).

You can use one of 9 different font sizes and draw the text in
black/white/red|gray. The text can be drawn horizontal or vertical.

This function writes the pixels into the black/white/red|gray pixel buffer, to draw the buffer
to the display use :func:`Draw`.
""",
'de':
"""
Zeichnet einen Text mit bis zu 50 Buchstaben an die Pixelposition (x, y).

Es können 9 unterschiedliche Font-Größen genutzt werden und der Text
kann in schwarz/weiß/rot|grau gezeichnet werden. Der Text kann horizontal
oder vertikal gezeichnet werden.

Diese Funktion schreibt Pixel in den Schwarz-/Weiß-/Grau|Rot-Buffer. Der Buffer kann mit der Funktion :func:`Draw`
auf das Display übertragen werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Draw Line',
'elements': [('Position X Start', 'uint16', 1, 'in', {'range': (0, 295)}),
             ('Position Y Start', 'uint8', 1, 'in', {'range': (0, 127)}),
             ('Position X End', 'uint16', 1, 'in', {'range': (0, 295)}),
             ('Position Y End', 'uint8', 1, 'in', {'range': (0, 127)}),
             ('Color', 'uint8', 1, 'in', {'constant_group': 'Color'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Draws a line from (x, y)-start to (x, y)-end in the given color.

This function writes the pixels into the black/white/red|gray pixel buffer, to draw the buffer
to the display use :func:`Draw`.
""",
'de':
"""
Zeichnet eine Linie von (x, y)-Start nach (x, y)-Ende in der eingestellten Farbe.

Diese Funktion schreibt Pixel in den Schwarz-/Weiß-/Grau|Rot-Buffer. Der Buffer kann mit der Funktion :func:`Draw`
auf das Display übertragen werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Draw Box',
'elements': [('Position X Start', 'uint16', 1, 'in', {'range': (0, 295)}),
             ('Position Y Start', 'uint8', 1, 'in', {'range': (0, 127)}),
             ('Position X End', 'uint16', 1, 'in', {'range': (0, 295)}),
             ('Position Y End', 'uint8', 1, 'in', {'range': (0, 127)}),
             ('Fill', 'bool', 1, 'in', {}),
             ('Color', 'uint8', 1, 'in', {'constant_group': 'Color'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Draws a box from (x, y)-start to (x, y)-end in the given color.

If you set fill to true, the box will be filled with the
color. Otherwise only the outline will be drawn.

This function writes the pixels into the black/white/red|gray pixel buffer, to draw the buffer
to the display use :func:`Draw`.
""",
'de':
"""
Zeichnet ein Rechteck von (x, y)-Start nach (x, y)-Ende in der eingestellten Farbe.

Wenn fill auf true gesetzt wird, wird das Rechteck mit
der angegebenen Farbe ausgefüllt. Ansonsten wird nur der Umriss
gezeichnet.

Diese Funktion schreibt Pixel in den Schwarz-/Weiß-/Grau|Rot-Buffer. Der Buffer kann mit der Funktion :func:`Draw`
auf das Display übertragen werden.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Draw Status',
'elements': [('Draw Status', 'uint8', 1, 'out', {'constant_group': 'Draw Status'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
Callback for the current draw status. Will be called every time the
draw status changes (see :func:`Get Draw Status`).
""",
'de':
"""
Callback für den aktuellen Draw Status. Diese Callback wird jedes mal
ausgelöst, wenn sich der Draw Status ändert (siehe :func:`Get Draw Status`).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Update Mode',
'elements': [('Update Mode', 'uint8', 1, 'in', {'constant_group': 'Update Mode', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
.. note::
 The default update mode corresponds to the default e-paper display
 manufacturer settings. All of the other modes are experimental and
 will result in increased ghosting and possibly other long-term
 side effects.

 If you want to know more about the inner workings of an e-paper display
 take a look at this excellent video from Ben Krasnow:
 `https://www.youtube.com/watch?v=MsbiO8EAsGw <https://www.youtube.com/watch?v=MsbiO8EAsGw>`__.

 If you are not sure about this option, leave the update mode at default.

Currently there are three update modes available:

* Default: Settings as given by the manufacturer. An update will take about
  7.5 seconds and during the update the screen will flicker several times.
* Black/White: This will only update the black/white pixel. It uses the manufacturer
  settings for black/white and ignores the red or gray pixel buffer. With this mode the
  display will flicker once and it takes about 2.5 seconds. Compared to the default settings
  there is more ghosting.
* Delta: This will only update the black/white pixel. It uses an aggressive method where
  the changes are not applied for a whole buffer but only for the delta between the last
  and the next buffer. With this mode the display will not flicker during an update and
  it takes about 900-950ms. Compared to the other two settings there is more ghosting. This
  mode can be used for something like a flicker-free live update of a text.

With the black/white/red display if you use either the black/white or the delta mode,
after a while of going back and forth between black and white the white color will
start to appear red-ish or pink-ish.

If you use the aggressive delta mode and rapidly change the content, we recommend that you
change back to the default mode every few hours and in the default mode cycle between the
three available colors a few times. This will get rid of the ghosting and after that you can
go back to the delta mode with flicker-free updates.
""",
'de':
"""
.. note::
 Der *Default* Update-Modus basiert auf den Standardeinstellungen des E-Paper-Display
 Herstellers. Alle anderen Modi sind experimentell und es tritt mehr Ghosting sowie
 mögliche Langzeiteffekte auf.

 Für einen Überblick über die Funktionsweise eines E-Paper-Displays können wir
 das exzellente Video von Ben Krasnow empfehlen:
 `https://www.youtube.com/watch?v=MsbiO8EAsGw <https://www.youtube.com/watch?v=MsbiO8EAsGw>`__.

 Falls es nicht klar ist was diese Optionen bedeuten, empfehlen wir den
 Update-Modus auf *Default* zu belassen.

Aktuell gibt es drei unterschiedliche Update-Modi:

* Default: Einstellungen wie vom Hersteller vorgegeben. Eine Bildschirmaktualisierung dauert
  ungefähr 7,5 Sekunden und während der Aktualisierung flackert der Bildschirm mehrfach.
* Black/White: In diesem Modus werden nur die schwarzen und weißen Pixel aktualisiert. Es
  werden die Herstellereinstellungen für schwarz/weiß genutzt, allerdings wird der
  rote oder graue Buffer ignoriert. Mit diesem Modus flackert das Display bei einer Aktualisierung
  einmal und es dauert in etwa 2,5 Sekunden. Verglichen zu der Standardeinstellung entsteht
  mehr Ghosting.
* Delta: In diesem Modus werden auch nur die schwarzen und weißen Pixel aktualisiert. Es wird
  eine aggressive Aktualisierungsmethode genutzt. Änderungen werden nicht auf dem kompletten
  Buffer angewendet, sondern nur auf dem Unterschied (Delta) zwischen dem letzten und dem nächsten
  Buffer. Mit diesem Modus flackert das Display nicht und eine Aktualisierung dauert 900-950ms.
  Verglichen zu den anderen beiden Modi gibt es mehr Ghosting. Dieser Modus ist gut geeignet um z.B.
  flackerfrei einen regelmäßig aktualisierten Text darzustellen.

Wenn der Black/White- oder Delta-Modus zusammen mit dem schwarz/weiß/rot-Bildschirm verwendet wird,
bekommt die weiße Farbe nach mehrmaligem Wechsel zwischen schwarz und weiß einen rötlichen Stich.

Wenn der Delta-Modus mit schnell Aktualisierungen verwendet wird, empfehlen wir in regelmäßigen
Abständen zurück zum Default-Modus zu wechseln um dort vollflächig zwischen den drei Farben hin
und her zu wechseln. Dadurch wird das Ghosting welches durch die Verwendung des Delta-Modus
entsteht wieder entfernt. Danach kann dann wieder in den Delta-Modus gewechselt werden für
flackerfreie Aktualisierungen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Update Mode',
'elements': [('Update Mode', 'uint8', 1, 'out', {'constant_group': 'Update Mode', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the update mode as set by :func:`Set Update Mode`.
""",
'de':
"""
Gibt den Update Mode zurück, wie von :func:`Set Update Mode` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Display Type',
'elements': [('Display Type', 'uint8', 1, 'in', {'constant_group': 'Display Type'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the type of the display. The e-paper display is available
in black/white/red and black/white/gray. This will be factory set
during the flashing and testing phase. The value is saved in
non-volatile memory and will stay after a power cycle.
""",
'de':
"""
Setzt den Typ des Displays. Das E-Paper Display ist in den Farben
schwarz/weiß/rot und schwarz/weiß/grau verfügbar. Das korrekte
Display wird bereits werksseitig während des Flashens und Testens
gesetzt. Der Wert wird in nicht-flüchtigem Speicher gespeichert und
bleibt bei einem Neustart unverändert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Display Type',
'elements': [('Display Type', 'uint8', 1, 'out', {'constant_group': 'Display Type'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the type of the e-paper display. It can either be
black/white/red or black/white/gray.
""",
'de':
"""
Gibt den Typ des E-Paper Displays zurück. Der Typ kann entweder
schwarz/weiß/rot oder schwarz/weiß/grau sein.
"""
}]
})

com['examples'].append({
'name': 'Hello World',
'functions': [('setter', 'Fill Display', [('uint8:constant', 0)], 'Use black background', None),
              ('setter', 'Draw Text', [('uint8', 16), ('uint8', 48), ('uint8:constant', 9), ('uint8:constant', 1), ('uint8:constant', 0), ('string', 'Hello World')], 'Write big white "Hello World" in the middle of the screen', None),
              ('setter', 'Draw', [], None, None)]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports() + oh_generic_trigger_channel_imports() +  ['org.eclipse.smarthome.core.library.types.StringType', 'org.eclipse.smarthome.core.library.types.DecimalType'],
    'param_groups': oh_generic_channel_param_groups(),
    'channels': [{
        'id': 'Draw Status',
        'type': 'Draw Status',
        'getters': [{
            'packet': 'Get Draw Status',
            'transform': 'new DecimalType(value)'}],

        'callbacks': [{
            'packet': 'Draw Status',
            'transform': 'new DecimalType(drawStatus)'}]
    }],
    'channel_types': [
        oh_generic_channel_type('Draw Status', 'Number', 'Draw Status',
                    update_style=None,
                    description="One of three draw statuses:<ul><li>0: Idle</li><li>1: Copying: Data is being copied from the buffer of the Bricklet to the buffer of the display.</li><li>2: Drawing: The display is updating its content (during this phase the flickering etc happens).</li></ul><br/><br/>You can write to the buffer (through one of the write or draw functions) when the status is either idle or drawing. You should not write to the buffer while it is being copied to the display. There is no double-buffering."),
    ],
    'actions': ['Draw', 'Get Draw Status',
                'Write Black White', 'Read Black White', 'Write Color', 'Read Color', 'Fill Display',
                'Draw Text', 'Draw Line', 'Draw Box',
                'Set Update Mode', 'Get Update Mode', 'Get Display Type']
}
