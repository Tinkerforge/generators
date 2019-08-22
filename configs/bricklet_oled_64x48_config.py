# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# OLED 64x48 Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 264,
    'name': 'OLED 64x48',
    'display_name': 'OLED 64x48',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '1.68cm (0.66") OLED display with 64x48 pixels',
        'de': '1,68cm (0,66") OLED Display mit 64x48 Pixel'
    },
    'released': True,
    'documented': True,
    'discontinued': False, # selling remaining stock, replaced by OLED 128x64 Bricklet 2.0
    'features': [
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Write',
'elements': [('Data', 'uint8', 64, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Appends 64 byte of data to the window as set by :func:`New Window`.

Each row has a height of 8 pixels which corresponds to one byte of data.

Example: if you call :func:`New Window` with column from 0 to 63 and row
from 0 to 5 (the whole display) each call of :func:`Write` (red arrow) will
write one row.

.. image:: /Images/Bricklets/bricklet_oled_64x48_display.png
   :scale: 100 %
   :alt: Display pixel order
   :align: center
   :target: ../../_images/Bricklets/bricklet_oled_64x48_display.png

The LSB (D0) of each data byte is at the top and the MSB (D7) is at the
bottom of the row.

The next call of :func:`Write` will write the second row and so on. To
fill the whole display you need to call :func:`Write` 6 times.
""",
'de':
"""
Fügt 64 Byte Daten zu dem mit :func:`New Window` gesetztem Fenster hinzu.

Jede Zeile hat eine Höhe von 8 Pixeln welche einem Byte Daten entsprechen.

Beispiel: Wenn :func:`New Window` mit Spalte (Column) von 0 bis 63 und
Zeile (Row) von 0 bis 5 (das ganze Display) aufgerufen wird, schreibt
jedes :func:`Write` (roter Pfeil) eine Zeile.

.. image:: /Images/Bricklets/bricklet_oled_64x48_display.png
   :scale: 100 %
   :alt: Display Pixel Reihenfolge
   :align: center
   :target: ../../_images/Bricklets/bricklet_oled_64x48_display.png

Das LSB (D0) von jedem Daten-Byte ist in der Zeile oben und das
MSB (D7) ist in der Zeile unten.

Der nächste Aufruf von :func:`Write` schreibt die zweite Zeile
usw. Um das ganze Display zu füllen muss :func:`Write` 6 mal
aufgerufen werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'New Window',
'elements': [('Column From', 'uint8', 1, 'in'),
             ('Column To', 'uint8', 1, 'in'),
             ('Row From', 'uint8', 1, 'in'),
             ('Row To', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the window in which you can write with :func:`Write`. One row
has a height of 8 pixels.

The columns have a range of 0 to 63 and the rows have a range of 0 to 5.
""",
'de':
"""
Setzt das Fenster in welches mit :func:`Write` geschrieben
werden kann. Eine Zeile (Row) hat eine Höhe von 8 Pixel.

Die Spalten haben einen Wertebereich von 0 bis 63 und die Zeilen haben
einen Wertebereich von 0 bis 5.
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
Clears the current content of the window as set by :func:`New Window`.
""",
'de':
"""
Löscht den aktuellen Inhalt des mit :func:`New Window` gesetztem Fensters.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Display Configuration',
'elements': [('Contrast', 'uint8', 1, 'in'),
             ('Invert', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the configuration of the display.

You can set a contrast value from 0 to 255 and you can invert the color
(black/white) of the display.

The default values are contrast 143 and inverting off.
""",
'de':
"""
Setzt die Konfiguration des Displays

Es können der Kontrast mit einem Wertebereich von 0 bis 255 gesetzt, sowie die
Farben (schwarz/weiß) des Displays invertiert werden.

Die Standardwerte sind ein Kontrast von 143 und die Invertierung ist aus.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Display Configuration',
'elements': [('Contrast', 'uint8', 1, 'out'),
             ('Invert', 'bool', 1, 'out')],
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
             ('Text', 'string', 13, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes text to a specific line (0 to 5) with a specific position
(0 to 12). The text can have a maximum of 13 characters.

For example: (1, 4, "Hello") will write *Hello* in the middle of the
second line of the display.

You can draw to the display with :func:`Write` and then add text to it
afterwards.

The display uses a special 5x7 pixel charset. You can view the characters
of the charset in Brick Viewer.
""",
'de':
"""
Schreibt einen Text in die angegebene Zeile (0 bis 5) mit einer vorgegebenen
Position (0 bis 12). Der Text kann maximal 13 Zeichen lang sein.

Beispiel: (1, 4, "Hallo") schreibt *Hallo* in die Mitte der zweiten Zeile
des Displays.

Es ist möglich zuerst auf das Display mit :func:`Write` zu malen und danach
Text hinzuzufügen.

Das Display nutzt einen speziellen 5x7 Pixel Zeichensatz. Der Zeichensatz
kann mit Hilfe von Brick Viewer angezeigt werden.
"""
}]
})

com['examples'].append({
'name': 'Hello World',
'functions': [('setter', 'Clear Display', [], 'Clear display', None),
              ('setter', 'Write Line', [('uint8', 0), ('uint8', 0), ('string', 'Hello World')], 'Write "Hello World" starting from upper left corner of the screen', None)]
})

com['examples'].append({
'name': 'Pixel Matrix',
'functions': [('setter', 'Clear Display', [], 'Clear display', None)],
'incomplete': True # because of special logic
})
