# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# LCD 20x4 Bricklet communication config

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 2],
    'category': 'Bricklet',
    'device_identifier': 212,
    'name': 'LCD 20x4',
    'display_name': 'LCD 20x4',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '20x4 character alphanumeric display with blue backlight',
        'de': '20x4 Zeichen alphanumerisches Display mit blauer Hintergrundbeleuchtung'
    },
    'released': True,
    'documented': True,
    'discontinued': False, # selling remaining stock, replaced by LCD 128x64 Bricklet
    'features': [
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Write Line',
'elements': [('Line', 'uint8', 1, 'in', {'range': (0, 3)}),
             ('Position', 'uint8', 1, 'in', {'range': (0, 19)}),
             ('Text', 'string', 20, 'in', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes text to a specific line with a specific position.
The text can have a maximum of 20 characters.

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
Schreibt einen Text in die angegebene Zeile mit einer vorgegebenen Position.
Der Text kann maximal 20 Zeichen lang sein.

Beispiel: (0, 7, "Hallo") schreibt *Hallo* in die Mitte der ersten Zeile
des Display.

Das Display nutzt einen speziellen Zeichensatz der alle ASCII Zeichen beinhaltet außer
Backslash und Tilde. Der Zeichensatz des LCD beinhaltet weiterhin einige Nicht-ASCII Zeichen,
siehe die `Zeichensatzspezifikation <https://github.com/Tinkerforge/lcd-20x4-bricklet/raw/master/datasheets/standard_charset.pdf>`__
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
'elements': [('Backlight', 'bool', 1, 'out', {})],
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
'elements': [('Cursor', 'bool', 1, 'in', {'default': False}),
             ('Blinking', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Configures if the cursor (shown as "_") should be visible and if it
should be blinking (shown as a blinking block). The cursor position
is one character behind the the last text written with
:func:`Write Line`.
""",
'de':
"""
Konfiguriert ob der Cursor (angezeigt als "_") sichtbar ist und ob er
blinkt (angezeigt als blinkender Block). Die Cursor Position ist ein
Zeichen hinter dem zuletzt mit :func:`Write Line` geschriebenen Text.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Config',
'elements': [('Cursor', 'bool', 1, 'out', {'default': False}),
             ('Blinking', 'bool', 1, 'out', {'default': False})],
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
'elements': [('Button', 'uint8', 1, 'in', {'range': (0, 3)}),
             ('Pressed', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns *true* if the button (0 to 2 or 0 to 3 since hardware version 1.2)
is pressed.

If you want to react on button presses and releases it is recommended to use
the :cb:`Button Pressed` and :cb:`Button Released` callbacks.
""",
'de':
"""
Gibt *true* zurück wenn die Taste (0 bis 2 oder 0 bis 3 seit Hardware
Version 1.2) gedrückt ist.

Wenn auf Tastendrücken und -loslassen reagiert werden soll, wird empfohlen die
:cb:`Button Pressed` und :cb:`Button Released` Callbacks zu nutzen.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Button Pressed',
'elements': [('Button', 'uint8', 1, 'out', {'range': (0, 3)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when a button is pressed. The :word:`parameter` is
the number of the button (0 to 2 or 0 to 3 since hardware version 1.2).
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn eine Taste gedrückt wird. Der :word:`parameter`
ist die Nummer der Taste (0 bis 2 oder 0 bis 3 seit Hardware Version 1.2).
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Button Released',
'elements': [('Button', 'uint8', 1, 'out', {'range': (0, 3)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when a button is released. The :word:`parameter` is
the number of the button (0 to 2 or 0 to 3 since hardware version 1.2).
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn eine Taste losgelassen wird. Der :word:`parameter`
ist die Nummer der Taste (0 bis 2 oder 0 bis 3 seit Hardware Version 1.2).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Custom Character',
'elements': [('Index', 'uint8', 1, 'in', {'range': (0, 7)}),
             ('Character', 'uint8', 8, 'in', {'range': (0, 31)})],
'since_firmware': [2, 0, 1],
'doc': ['af', {
'en':
"""
The LCD 20x4 Bricklet can store up to 8 custom characters. The characters
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
characters with the byte representation 8 ("\\\\x08" or "\\\\u0008") to 15
("\\\\x0F" or "\\\\u000F").

You can play around with the custom characters in Brick Viewer version
since 2.0.1.

Custom characters are stored by the LCD in RAM, so they have to be set
after each startup.
""",
'de':
"""
Das LCD 20x4 Bricklet kann bis zu 8 benutzerdefinierte Buchstaben speichern.
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
den Byterepräsentationen 8 ("\\\\x08" oder "\\\\u0008") bis 15 ("\\\\x0F" oder
"\\\\u000F") geschrieben werden.

Es ist möglich die benutzerdefinierten Buchstaben im Brick Viewer ab
Version 2.0.1 einzustellen.

Benutzerdefinierte Buchstaben werden vom LCD im RAM gespeichert, daher
müssen sie nach jedem Start des LCD 20x4 Bricklets gesetzt werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Custom Character',
'elements': [('Index', 'uint8', 1, 'in', {'range': (0, 7)}),
             ('Character', 'uint8', 8, 'out', {'range': (0, 31)})],
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
Index zurück, wie von :func:`Set Custom Character` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Default Text',
'elements': [('Line', 'uint8', 1, 'in', {'range': (0, 3)}),
             ('Text', 'string', 20, 'in', {})],
'since_firmware': [2, 0, 2],
'doc': ['af', {
'en':
"""
Sets the default text for lines 0-3. The max number of characters
per line is 20.

The default text is shown on the LCD, if the default text counter
expires, see :func:`Set Default Text Counter`.
""",
'de':
"""
Setzt den Standard-Text für die Zeilen 0-3. Die maximale Anzahl an
Buchstaben pro Zeile ist 20.

Der Standard-Text wird auf dem LCD angezeigt, wenn der Standard-Text-Zähler
ausläuft, siehe :func:`Set Default Text Counter`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Default Text',
'elements': [('Line', 'uint8', 1, 'in', {'range': (0, 3)}),
             ('Text', 'string', 20, 'out', {})],
'since_firmware': [2, 0, 2],
'doc': ['af', {
'en':
"""
Returns the default text for a given line (0-3) as set by
:func:`Set Default Text`.
""",
'de':
"""
Gibt den Standard-Text für die Zeilen 0-3 zurück, wie von
:func:`Set Default Text` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Default Text Counter',
'elements': [('Counter', 'int32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': -1})],
'since_firmware': [2, 0, 2],
'doc': ['af', {
'en':
"""
Sets the default text counter. This counter is decremented each
ms by the LCD firmware. If the counter reaches 0, the default text
(see :func:`Set Default Text`) is shown on the LCD.

This functionality can be used to show a default text if the controlling
program crashes or the connection is interrupted.

A possible approach is to call :func:`Set Default Text Counter` every
minute with the parameter 1000*60*2 (2 minutes). In this case the
default text will be shown no later than 2 minutes after the
controlling program crashes.

A negative counter turns the default text functionality off.
""",
'de':
"""
Setzt den Standard-Text-Zähler. Der Zähler wird von der LCD
Firmware einmal pro ms dekrementiert. Wenn der Zähler 0 erreicht
wird der Standard-Text auf dem LCD angezeigt (siehe :func:`Set Default Text`).

Diese Funktionalität kann genutzt werden um auf dem LCD einen Text
anzuzeigen falls das kontrollierende Programm abstürzt oder die Verbindung
unterbrochen wird.

Ein möglicher Ansatz dafür ist :func:`Set Default Text Counter` einmal
pro Minute mit dem Parameter 1000*60*2 (zwei Minuten) aufzurufen.
In diesem Fall wird dann der Standard-Text nach spätestens zwei Minuten
angezeigt wenn das kontrollierende Programm abstürzt.

Ein negativer Zählerwert stellt die Standard-Text Funktionalität aus.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Default Text Counter',
'elements': [('Counter', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': -1})],
'since_firmware': [2, 0, 2],
'doc': ['af', {
'en':
"""
Returns the current value of the default text counter.
""",
'de':
"""
Gibt den aktuellen Wert des Standard-Text-Zählers zurück.
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
              ('setter', 'Write Line', [('uint8', 0), ('uint8', 0), ('string', 'FIXME')], 'Write some strings using the FIXME function to map to the LCD charset', None),
              ('setter', 'Write Line', [('uint8', 1), ('uint8', 0), ('string', 'FIXME')], None, None),
              ('setter', 'Write Line', [('uint8', 2), ('uint8', 0), ('string', 'FIXME')], 'Write a string directly including characters from the LCD charset', None)],
'incomplete': True # because of Unicode handling
})

def custom_character_param(idx):
    return {
            'name': 'Custom Character {}'.format(idx),
            'type': 'integer',
            'default': '-1',

            'label': 'Custom Character {}'.format(idx),
            'description': "Custom characters consist of 5x8 pixels and can be addressed with the index 0-7. This character ({}) is printed by writing \\\\x{:02x}. To describe the pixels, the first 5 bits of 8 bytes are used. For example, to make a custom character 'H', you should configure 1229782998376845568, which is the following in binary:<br/>00010001<br/>00010001<br/>00010001<br/>00011111<br/>00010001<br/>00010001<br/>00010001<br/>00000000<br/>.".format(idx, idx+8),
    }

def custom_character_init_code(idx):
    return """
if(cfg.customCharacter{0}.longValue() >= 0) {{
    int[] bytes = new int[8];
    for(int i = 0; i < 8; ++i) {{
        bytes[i] = (cfg.customCharacter{0}.longValue() >> (i * 8)) & 0xFF;
    }}
    this.setCustomCharacter({0}, bytes);
}}""".format(idx)

def default_text_param(idx):
    return {
            'name': 'Default Text Line {}'.format(idx),
            'type': 'text',
            'default': '',

            'label': 'Default Text Line {}'.format(idx),
            'description': 'Sets the default text for line {}. The max number of characters per line is 20. The default text is shown on the LCD, if the default text counter expires.'.format(idx)
    }

def default_text_init_code(idx):
    return """this.setDefaultText({0}, cfg.defaultTextLine{0});""".format(idx)

def button_channel(idx):
    return {
            'id': 'Button {}'.format(idx),
            'label': 'Button {}'.format(idx),
            'type': 'system.rawbutton',
            'getters': [{
                'packet': 'Is Button Pressed',
                'packet_params': [str(idx)],
                'transform': 'value ? CommonTriggerEvents.PRESSED : CommonTriggerEvents.RELEASED'}],

            'callbacks': [{
                    'filter': 'button == {}'.format(idx),
                    'packet': 'Button Pressed',
                    'transform': 'CommonTriggerEvents.PRESSED'
                },{
                    'filter': 'button == {}'.format(idx),
                    'packet': 'Button Released',
                    'transform': 'CommonTriggerEvents.RELEASED'
                },
            ],
            'is_trigger_channel': True
    }

button_channels = [button_channel(i) for i in range(0, 4)]
button_channels[3]['predicate'] = """this.getIdentity().hardwareVersion[1] >= 2"""

com['openhab'] = {
    'imports': oh_generic_channel_imports() + oh_generic_trigger_channel_imports() +  ['org.eclipse.smarthome.core.library.types.StringType','org.eclipse.smarthome.core.library.types.DecimalType', 'org.eclipse.smarthome.core.library.types.OnOffType'],
    'param_groups': oh_generic_channel_param_groups(),
    'params': [
        {
            'packet': 'Set Config',
            'element': 'Cursor',

            'name': 'Show Cursor',
            'type': 'boolean',
            'default': 'false',

            'label': 'Show Cursor',
            'description': "Configures if the cursor (shown as '_') should be visible. The cursor position is one character behind the the last text written.",
        },
        {
            'packet': 'Set Config',
            'element': 'Blinking',

            'name': 'Show Blinking Cursor',
            'type': 'boolean',
            'default': 'false',

            'label': 'Show Blinking Cursor',
            'description': 'Configures if the blinking cursor (shown as a blinking block) should be visible. The cursor position is one character behind the the last text written.',
        },
    ] ,
    'init_code': """this.setConfig(cfg.showCursor, cfg.showBlinkingCursor);""",
    'channels': [
            {
                'id': 'Text',
                'type': 'Text',
                'setters': [{
                    'packet': 'Write Line',
                    'packet_params': ['Helper.parseDisplayCommandLine(cmd.toString(), logger)', 'Helper.parseDisplayCommandPosition(cmd.toString(), logger)', 'Helper.parseDisplayCommandText(cmd.toString(), logger, true)'],
                    'command_type': "StringType",
                }],

            },
            {
                'id': 'Clear Display',
                'type': 'Clear Display',
                'setters': [{
                    'packet': 'Clear Display',
                    'command_type': "StringType",
                }],

            },
            {
                'id': 'Backlight',
                'type': 'Backlight',
                'setters': [{
                        'predicate': 'cmd == OnOffType.ON',
                        'packet': 'Backlight On',
                        'command_type': "OnOffType",
                    }, {
                        'predicate': 'cmd == OnOffType.OFF',
                        'packet': 'Backlight Off',
                        'command_type': "OnOffType",
                    }
                ],
                'getters': [{
                    'packet': 'Is Backlight On',
                    'transform': 'value ? OnOffType.ON : OnOffType.OFF'
                }]
            }
    ] + button_channels,
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
        oh_generic_channel_type('Backlight', 'Switch', 'Backlight',
                    update_style=None,
                    description="Toggles the LCD's backlight")
    ],
    'actions': ['Write Line', 'Clear Display', 'Is Backlight On', 'Get Config', 'Is Button Pressed', 'Set Custom Character', 'Get Custom Character', 'Set Default Text', 'Get Default Text', 'Set Default Text Counter', 'Get Default Text Counter']
}
