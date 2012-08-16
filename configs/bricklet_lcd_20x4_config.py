# -*- coding: utf-8 -*-

# LCD 20x4 Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'version': [1, 0, 0],
    'category': 'Bricklet',
    'name': ('LCD20x4', 'lcd_20x4', 'LCD 20x4'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for controlling a LCD with 4 lines a 20 characters',
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('WriteLine', 'write_line'), 
'elements': [('line', 'uint8', 1, 'in'),
             ('position', 'uint8', 1, 'in'),
             ('text', 'string', 20, 'in')],
'doc': ['bm', {
'en':
"""
Writes text to a specific line (0 to 3) with a specific position 
(0 to 19). The text can have a maximum of 20 characters.

For example: (0, 7, "Hello") will write *Hello* in the middle of the
first line of the display.

The display uses a special charset that includes all ASCII characters except
backslash and tilde. The LCD charset also includes several other non-ASCII characters, see
the `charset specification <https://github.com/Tinkerforge/lcd-20x4-bricklet/raw/master/datasheets/standard_charset.pdf>`__
for details. The Unicode example above shows how to specify non-ASCII characters
and how to translate from Unicode to the LCD charset.
""",
'de':
"""
Schreibt einen Text in die angegebene Zeile (0 bis 3) mit einer vorgegebenen
Position (0 bis 19). Der Text kann maximal 20 Zeichen lang sein.

Beispiel: (0, 7, "Hello") schreibt *Hello* in die Mitte der ersten Zeile
des Display.

Das Display nutzt einen speziellen Zeichensatz der alle ASCII Zeichen beinhaltet außer
Backslash und Tilde. Der Zeichensatz des LCD beinhaltet weiterhin einige Nicht-ASCII Zeichen,
siehe die `Zeichensatzspezifikation <<https://github.com/Tinkerforge/lcd-20x4-bricklet/raw/master/datasheets/standard_charset.pdf>`__
für Details. Das gezeigte Unicode Beispiel verdeutlicht die Verwendung von Nicht-ASCII Zeichen
und wie die Wandlung von Unicode in den LCD Zeichensatz möglich ist.

"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('ClearDisplay', 'clear_display'), 
'elements': [],
'doc': ['bm', {
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
'name': ('BacklightOn', 'backlight_on'), 
'elements': [],
'doc': ['bm', {
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
'name': ('BacklightOff', 'backlight_off'), 
'elements': [],
'doc': ['bm', {
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
'name': ('IsBacklightOn', 'is_backlight_on'), 
'elements': [('backlight', 'bool', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns true if the backlight is on and false otherwise.
""",
'de':
"""
Gibt true zurück wenn die Hintergrundbeleuchtung aktiv ist, sonst false.
"""
}]
})



com['packets'].append({
'type': 'function',
'name': ('SetConfig', 'set_config'), 
'elements': [('cursor', 'bool', 1, 'in'),
             ('blinking', 'bool', 1, 'in')],
'doc': ['am', {
'en':
"""
Configures if the cursor (shown as "_") should be visible and if it
should be blinking (shown as a blinking block). The cursor position
is one character behind the the last text written with 
:func:`WriteLine`.

The default is (false, false).
""",
'de':
"""
Konfiguriert ob der Cursor (angezeigt als "_") sichtbar ist und ob er 
blinkt (angezeigt als blinkender Block). Die Cursor Position ist ein 
Zeichen hinter dem zuletzt mit :func:`WriteLine` geschriebenen Text.

Der Standardwert ist (false, false).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetConfig', 'get_config'), 
'elements': [('cursor', 'bool', 1, 'out'),
             ('blinking', 'bool', 1, 'out')],
'doc': ['am', {
'en':
"""
Returns the configuration as set by :func:`SetConfig`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`SetConfig` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('IsButtonPressed', 'is_button_pressed'), 
'elements': [('button', 'uint8', 1, 'in'),
             ('pressed', 'bool', 1, 'out')],
'doc': ['am', {
'en':
"""
Returns true if the button (0 to 2) is pressed. If you want to react
on button presses and releases it is recommended to use the
:func:`ButtonPressed` and :func:`ButtonReleased` callbacks.
""",
'de':
"""
Gibt true zurück wenn die Taste (0 bis 2) gedrückt ist. Wenn auf Tastendrücken
und loslassen reagiert werden soll, wird empfohlen die :func:`ButtonPressed`
und :func:`ButtonReleased` Callbacks zu nutzen.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('ButtonPressed', 'button_pressed'), 
'elements': [('button', 'uint8', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered when a button is pressed. The :word:`parameter` is
the number of the button (0 to 2).
""",
'de':
"""
Dieser Callback wird ausgelöst wenn eine Taste gedrückt wird. The :word:`parameter`
ist die Nummer der Taste (0 bis 2).
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('ButtonReleased', 'button_released'), 
'elements': [('button', 'uint8', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered when a button is released. The :word:`parameter` is
the number of the button (0 to 2).
""",
'de':
"""
Dieser Callback wird ausgelöst wenn eine Taste losgelassen wird. The :word:`parameter`
ist die Nummer der Taste (0 bis 2).
"""
}]
})
