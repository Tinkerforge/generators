# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# LCD 16x2 Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 211,
    'name': 'LCD 16x2',
    'display_name': 'LCD 16x2',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '16x2 character alphanumeric display with blue backlight',
        'de': '16x2 Zeichen alphanumerisches Display mit blauer Hintergrundbeleuchtung'
    },
    'released': True,
    'documented': True,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Write Line',
'elements': [('Line', 'uint8', 1, 'in'),
             ('Position', 'uint8', 1, 'in'),
             ('Text', 'string', 16, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes text to a specific line (0 to 1) with a specific position
(0 to 15). The text can have a maximum of 16 characters.

For example: (0, 5, "Hello") will write *Hello* in the middle of the
first line of the display.

The display uses a special charset that includes all ASCII characters except
backslash and tilde. The LCD charset also includes several other non-ASCII characters, see
the `charset specification <https://github.com/Tinkerforge/lcd-16x2-bricklet/raw/master/datasheets/standard_charset.pdf>`__
for details. The Unicode example above shows how to specify non-ASCII characters
and how to translate from Unicode to the LCD charset.
""",
'de':
"""
Schreibt einen Text in die angegebene Zeile (0 bis 1) mit einer vorgegebenen
Position (0 bis 15). Der Text kann maximal 16 Zeichen lang sein.

Beispiel: (0, 5, "Hallo") schreibt *Hallo* in die Mitte der ersten Zeile
des Display.

Das Display nutzt einen speziellen Zeichensatz der alle ASCII Zeichen beinhaltet außer
Backslash und Tilde. Der Zeichensatz des LCD beinhaltet weiterhin einige Nicht-ASCII Zeichen,
siehe die `Zeichensatzspezifikation <https://github.com/Tinkerforge/lcd-16x2-bricklet/raw/master/datasheets/standard_charset.pdf>`__
für Details. Das gezeigte Unicode Beispiel verdeutlicht die Verwendung von Nicht-ASCII Zeichen
und wie die Wandlung von Unicode in den LCD Zeichensatz möglich ist.
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
Deletes all characters from the display.
""",
'de':
"""
Löscht alle Zeichen auf dem Display.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Backlight On',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Turns the backlight on.
""",
'de':
"""
Aktiviert die Hintergrundbeleuchtung.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Backlight Off',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Turns the backlight off.
""",
'de':
"""
Deaktiviert die Hintergrundbeleuchtung.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is Backlight On',
'elements': [('Backlight', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns *true* if the backlight is on and *false* otherwise.
""",
'de':
"""
Gibt *true* zurück wenn die Hintergrundbeleuchtung aktiv ist, sonst *false*.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Config',
'elements': [('Cursor', 'bool', 1, 'in'),
             ('Blinking', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Configures if the cursor (shown as "_") should be visible and if it
should be blinking (shown as a blinking block). The cursor position
is one character behind the the last text written with
:func:`Write Line`.

The default is (false, false).
""",
'de':
"""
Konfiguriert ob der Cursor (angezeigt als "_") sichtbar ist und ob er
blinkt (angezeigt als blinkender Block). Die Cursor Position ist ein
Zeichen hinter dem zuletzt mit :func:`Write Line` geschriebenen Text.

Der Standardwert ist (false, false).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Config',
'elements': [('Cursor', 'bool', 1, 'out'),
             ('Blinking', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Config`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is Button Pressed',
'elements': [('Button', 'uint8', 1, 'in'),
             ('Pressed', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns *true* if the button (0 to 2) is pressed.

If you want to react on button presses and releases it is recommended to use the
:cb:`Button Pressed` and :cb:`Button Released` callbacks.
""",
'de':
"""
Gibt *true* zurück wenn die Taste (0 bis 2) gedrückt ist.

Wenn auf Tastendrücken und -loslassen reagiert werden soll, wird empfohlen die
:cb:`Button Pressed` und :cb:`Button Released` Callbacks zu nutzen.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Button Pressed',
'elements': [('Button', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when a button is pressed. The :word:`parameter` is
the number of the button (0 to 2).
""",
'de':
"""
Dieser Callback wird ausgelöst wenn eine Taste gedrückt wird. Der :word:`parameter`
ist die Nummer der Taste (0 bis 2).
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Button Released',
'elements': [('Button', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when a button is released. The :word:`parameter` is
the number of the button (0 to 2).
""",
'de':
"""
Dieser Callback wird ausgelöst wenn eine Taste losgelassen wird. Der :word:`parameter`
ist die Nummer der Taste (0 bis 2).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Custom Character',
'elements': [('Index', 'uint8', 1, 'in'),
             ('Character', 'uint8', 8, 'in')],
'since_firmware': [2, 0, 1],
'doc': ['af', {
'en':
"""
The LCD 16x2 Bricklet can store up to 8 custom characters. The characters
consist of 5x8 pixels and can be addressed with the index 0-7. To describe
the pixels, the first 5 bits of 8 bytes are used. For example, to make
a custom character "H", you should transfer the following:

* ``character[0] = 0b00010001`` (decimal value 17)
* ``character[1] = 0b00010001`` (decimal value 17)
* ``character[2] = 0b00010001`` (decimal value 17)
* ``character[3] = 0b00011111`` (decimal value 31)
* ``character[4] = 0b00010001`` (decimal value 17)
* ``character[5] = 0b00010001`` (decimal value 17)
* ``character[6] = 0b00010001`` (decimal value 17)
* ``character[7] = 0b00000000`` (decimal value 0)

The characters can later be written with :func:`Write Line` by using the
characters with the byte representation 8 to 15.

You can play around with the custom characters in Brick Viewer since
version 2.0.1.

Custom characters are stored by the LCD in RAM, so they have to be set
after each startup.
""",
'de':
"""
Das LCD 16x2 Bricklet kann bis zu 8 benutzerdefinierte Buchstaben speichern.
Die Buchstaben bestehen aus 5x8 Pixel und sie können über den Index 0-7
adressiert werden. Um die Pixel zu beschreiben, werden die ersten 5 Bit
von 8 Bytes verwenden. Zum Beispiel, um den Buchstaben "H" zu erzeugen,
sollte das folgende Array gesendet werden:

* ``character[0] = 0b00010001`` (Dezimalwert 17)
* ``character[1] = 0b00010001`` (Dezimalwert 17)
* ``character[2] = 0b00010001`` (Dezimalwert 17)
* ``character[3] = 0b00011111`` (Dezimalwert 31)
* ``character[4] = 0b00010001`` (Dezimalwert 17)
* ``character[5] = 0b00010001`` (Dezimalwert 17)
* ``character[6] = 0b00010001`` (Dezimalwert 17)
* ``character[7] = 0b00000000`` (Dezimalwert 0)

Die Buchstaben können später mit :func:`Write Line` mit den chars mit
den Byterepräsentationen 8 bis 15 geschrieben werden.

Es ist möglich die benutzerdefinierten Buchstaben im Brick Viewer ab
Version 2.0.1 einzustellen.

Benutzerdefinierte Buchstaben werden vom LCD im RAM gespeichert, daher
müssen sie nach jedem Start des LCD 16x2 Bricklets gesetzt werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Custom Character',
'elements': [('Index', 'uint8', 1, 'in'),
             ('Character', 'uint8', 8, 'out')],
'since_firmware': [2, 0, 1],
'doc': ['af', {
'en':
"""
Returns the custom character for a given index, as set with
:func:`Set Custom Character`.
""",
'de':
"""
Gibt den benutzerdefinierten Buchstaben für den gegebenen
Index zurück, wie von :func:`Get Custom Character` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Hello World',
'functions': [('setter', 'Backlight On', [], 'Turn backlight on', None),
              ('setter', 'Write Line', [('uint8', 0), ('uint8', 0), ('string', 'Hello World')], 'Write "Hello World"', None)]
})

com['examples'].append({
'name': 'Button Callback',
'functions': [('callback', ('Button Pressed', 'button pressed'), [(('Button', 'Button Pressed'), 'uint8', 1, None, None, None)], None, None),
              ('callback', ('Button Released', 'button released'), [(('Button', 'Button Released'), 'uint8', 1, None, None, None)], None, None)]
})

com['examples'].append({
'name': 'Unicode',
'functions': [('setter', 'Backlight On', [], 'Turn backlight on', None),
              ('setter', 'Write Line', [('uint8', 0), ('uint8', 0), ('string', 'FIXME')], 'Write a string using the FIXME function to map to the LCD charset', None),
              ('setter', 'Write Line', [('uint8', 1), ('uint8', 0), ('string', 'FIXME')], 'Write a string directly including characters from the LCD charset', None)],
'incomplete': True # because of Unicode handling
})
