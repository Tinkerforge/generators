# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# LED Strip Bricklet 2.0 communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2103,
    'name': 'LED Strip V2',
    'display_name': 'LED Strip 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Controls up to 2048 RGB(W) LEDs',
        'de': 'Steuert bis zu 2048 RGB(W) LEDs'
    },
    'comcu': True,
    'released': True,
    'documented': True,
    'discontinued': False,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Set LED Values Low Level',
'elements': [('Index', 'uint16', 1, 'in'),
             ('Value Length', 'uint16', 1, 'in'),
             ('Value Chunk Offset', 'uint16', 1, 'in'),
             ('Value Chunk Data', 'uint8', 58, 'in')],
'high_level': {'stream_in': {'name': 'Value'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the RGB(W) values for the LEDs starting from *index*.
You can set at most 2048 RGB values or 1536 RGBW values.

To make the colors show correctly you need to configure the chip type
(see :func:`Set Chip Type`) and a channel mapping (see :func:`Set Channel Mapping`)
according to the connected LEDs.

If the channel mapping has 3 colors, you need to give the data in the sequence
RGBRGBRGB... if the channel mapping has 4 colors you need to give data in the
sequence RGBWRGBWRGBW...

The data is double buffered and the colors will be transfered to the
LEDs when the next frame duration ends (see :func:`Set Frame Duration`).

Generic approach:

* Set the frame duration to a value that represents the number of frames per
  second you want to achieve.
* Set all of the LED colors for one frame.
* Wait for the :cb:`Frame Started` callback.
* Set all of the LED colors for next frame.
* Wait for the :cb:`Frame Started` callback.
* And so on.

This approach ensures that you can change the LED colors with a fixed frame rate.
""",
'de':
"""
Setzt die RGB(W) Werte der LEDs beginnend beim *index*.
Es können bis zu 2048 RGB Werte oder 1536 RGBW Werte gesetzt werden.

Damit die Farben richtig angezeigt werden muss den LEDs entsprechend der
richtig Chip Type (siehe :func:`Set Chip Type`) und das richtige Channel Mapping
(siehe :func:`Set Channel Mapping`) eingestellt werden.

Wenn das Channel Mapping 3 Farben hat, müssen die Werte in der Sequenz
RGBRGBRGB... übergeben werden. Hat das Mapping 4 Farben, müssen die Werte in
der Sequenz RGBWRGBWRGBW... übergeben werden.

Die Daten werden Zwischengespeichert und die Farben werden auf die LEDs
transferiert wenn die nächste *frame duration*  abgelaufen ist (siehe
:func:`Set Frame Duration`).

Genereller Ansatz:

* Setze *frame duration* auf einen Wert welcher der Anzahl der Bilder pro
  Sekunde entspricht die erreicht werden sollen.
* Setze alle LEDs für einen Frame.
* Warte auf den :cb:`Frame Started` Callback.
* Setze alle LEDs für den nächsten Frame.
* Warte auf den :cb:`Frame Started` Callback.
* Und so weiter.

Dieser Ansatz garantiert, dass die LED Farben mit einer festen Framerate
angezeigt werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get LED Values Low Level',
'elements': [('Index', 'uint16', 1, 'in'),
             ('Length', 'uint16', 1, 'in'),
             ('Value Length', 'uint16', 1, 'out'),
             ('Value Chunk Offset', 'uint16', 1, 'out'),
             ('Value Chunk Data', 'uint8', 60, 'out')],
'high_level': {'stream_out': {'name': 'Value'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the RGB(W) values as set by :func:`Set LED Values`.
""",
'de':
"""
Gibt die RGB(W) Werte zurück, wie von :func:`Set LED Values` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Frame Duration',
'elements': [('Duration', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the frame duration in ms.

Example: If you want to achieve 20 frames per second, you should
set the frame duration to 50ms (50ms * 20 = 1 second).

For an explanation of the general approach see :func:`Set LED Values`.

Default value: 100ms (10 frames per second).
""",
'de':
"""
Setzt die *frame duration* (Länge des Frames) in ms.

Beispiel: Wenn 20 Frames pro Sekunde erreicht werden sollen, muss
die Länge des Frames auf 50ms gesetzt werden (50ms * 20 = 1 Sekunde).

Für eine Erklärung des generellen Ansatzes siehe :func:`Set LED Values`.

Standardwert: 100ms (10 Frames pro Sekunde).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Frame Duration',
'elements': [('Duration', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the frame duration in ms as set by :func:`Set Frame Duration`.
""",
'de':
"""
Gibt die *frame duration* (Länge des Frames) in ms zurück, wie von
:func:`Set Frame Duration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Supply Voltage',
'elements': [('Voltage', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current supply voltage of the LEDs. The voltage is given in mV.
""",
'de':
"""
Gibt die aktuelle Versorgungsspannung der LEDs zurück. Die Spannung ist
in mV angegeben.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Frame Started',
'elements': [('Length', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered directly after a new frame render is started.
The :word:`parameter` is the number of LEDs in that frame.

You should send the data for the next frame directly after this callback
was triggered.

For an explanation of the general approach see :func:`Set LED Values`.
""",
'de':
"""
Dieser Callback wird direkt nachdem dem start eines Frames ausgelöst.
Der :word:`parameter` ist die Anzahl der LEDs in diesem Frame.

Die Daten für das nächste Frame sollten direkt nach dem auslösen dieses
Callbacks übertragen werden.

Für eine Erklärung des generellen Ansatzes siehe :func:`Set LED Values`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Clock Frequency',
'elements': [('Frequency', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the frequency of the clock in Hz. The range is 10000Hz (10kHz) up to
2000000Hz (2MHz).

The Bricklet will choose the nearest achievable frequency, which may
be off by a few Hz. You can get the exact frequency that is used by
calling :func:`Get Clock Frequency`.

If you have problems with flickering LEDs, they may be bits flipping. You
can fix this by either making the connection between the LEDs and the
Bricklet shorter or by reducing the frequency.

With a decreasing frequency your maximum frames per second will decrease
too.

The default value is 1.66MHz.
""",
'de':
"""
Setzt die Frequenz der Clock-Leitung in Hz. Der erlaubte Wertebereich
beläuft von sich 10000Hz (10kHz) bis 2000000Hz (2MHz).

Das Bricklet wählt die nächst mögliche erreichbare Frequenz. Diese
kann ein paar Hz neben des gesetzten Wertes liegen. Die exakte Frequenz
wie sie genutzt wird kann mit :func:`Get Clock Frequency` erfragt werden.

Wenn Probleme mit flackernden LEDs auftreten kann es daran liegen das
Bits auf der Leitung flippen. Dies kann behoben werden in dem man die
Verbindung zwischen Bricklet und LEDs verringert oder in dem man die
Frequenz reduziert.

Mit abnehmender Frequenz nimmt allerdings auch die maximale Framerate ab.

Der Standardwert ist 1,66MHz
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Clock Frequency',
'elements': [('Frequency', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the currently used clock frequency as set by :func:`Set Clock Frequency`.
""",
'de':
"""
Gibt die aktuell genutzte Clock-Frequenz zurück, wie von
:func:`Set Clock Frequency` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Chip Type',
'elements': [('Chip', 'uint16', 1, 'in', ('Chip Type', [('WS2801', 2801),
                                                        ('WS2811', 2811),
                                                        ('WS2812', 2812),
                                                        ('LPD8806', 8806),
                                                        ('APA102', 102)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the type of the LED driver chip. We currently support the chips

* WS2801,
* WS2811,
* WS2812 / SK6812 / NeoPixel RGB,
* SK6812RGBW / NeoPixel RGBW (Chip Type = WS2812),
* LPD8806 and
* APA102 / DotStar.

The default value is WS2801 (2801).
""",
'de':
"""
Setzt den Typ des LED-Treiber-Chips. Aktuell unterstützen
wir die folgenden Chips

* WS2801,
* WS2811,
* WS2812 / SK6812 / NeoPixel RGB,
* SK6812RGBW / NeoPixel RGBW (Chip Type = WS2812),
* LPD8806 and
* APA102 / DotStar.

Der Standardwert ist WS2801 (2801).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Chip Type',
'elements': [('Chip', 'uint16', 1, 'out', ('Chip Type', [('WS2801', 2801),
                                                         ('WS2811', 2811),
                                                         ('WS2812', 2812),
                                                         ('LPD8806', 8806),
                                                         ('APA102', 102)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the currently used chip type as set by :func:`Set Chip Type`.
""",
'de':
"""
Gibt den aktuell genutzten Typ des Chips zurück, wie von
:func:`Set Chip Type` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Channel Mapping',
'elements': [('Mapping', 'uint8', 1, 'in', ('Channel Mapping', [('RGB', 6),
                                                                ('RBG', 9),
                                                                ('BRG', 33),
                                                                ('BGR', 36),
                                                                ('GRB', 18),
                                                                ('GBR', 24),
                                                                ('RGBW', 27),
                                                                ('RGWB', 30),
                                                                ('RBGW', 39),
                                                                ('RBWG', 45),
                                                                ('RWGB', 54),
                                                                ('RWBG', 57),
                                                                ('GRWB', 78),
                                                                ('GRBW', 75),
                                                                ('GBWR', 108),
                                                                ('GBRW', 99),
                                                                ('GWBR', 120),
                                                                ('GWRB', 114),
                                                                ('BRGW', 135),
                                                                ('BRWG', 141),
                                                                ('BGRW', 147),
                                                                ('BGWR', 156),
                                                                ('BWRG', 177),
                                                                ('BWGR', 180),
                                                                ('WRBG', 201),
                                                                ('WRGB', 198),
                                                                ('WGBR', 216),
                                                                ('WGRB', 210),
                                                                ('WBGR', 228),
                                                                ('WBRG', 225)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the channel mapping for the connected LEDs.

If the mapping has 4 colors, the function :func:`Set LED Values` expects 4
values per pixel and if the mapping has 3 colors it expects 3 values per pixel.

The function always expects the order RGB(W). The connected LED driver chips
might have their 3 or 4 channels in a different order. For example, the WS2801
chips typically use BGR order, then WS2812 chips typically use GRB order and
the APA102 chips typically use WBGR order.

The APA102 chips are special. They have three 8-bit channels for RGB
and an additional 5-bit channel for the overall brightness of the RGB LED
making them 4-channel chips. Internally the brightness channel is the first
channel, therefore one of the Wxyz channel mappings should be used. Then
the W channel controls the brightness.

The default value is BGR (36).
""",
'de':
"""
Setzt das Channel Mapping für die angeschlossenen LEDs.

Falls das Mapping 4 Farben hat, erwartet die Funktion :func:`Set LED Values`
4 Werte pro Pixel. Bei einem Mapping mit 3 Farben werden 3 Werte pro Pixel
erwartet.

Die Funktion erwartet immer die Reihenfolge RGB(W).
Die angeschlossenen LED-Treiber-Chips können die Daten für ihre
3 oder 4 Kanäle in einer anderen Reihenfolge erwarten. Zum Beispiel
verwenden WS2801 Chips typischerweise BGR Reihenfolge, WS2812 Chips
verwenden typischerweise GRB Reihenfolge und APA102 verwenden typischerweise
WBGR Reihenfolge.

Die APA102 haben eine Besonderheit. Sie haben drei 8-Bit Kanäle für RGB und
einen zusätzlichen 5-Bit Kanal für die Helligkeit der RGB LED. Dadurch ist der
APA102 insgesamt ein 4-Kanal Chip. Intern ist der Helligkeitskanal der erste
Kanal. Daher sollte eines der Wxyz Channel Mappings verwendet werden. Dann kann
über den W Kanal die Helligkeit eingestellt werden.

Der Standardwert ist BGR (36).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Channel Mapping',
'elements': [('Mapping', 'uint8', 1, 'out', ('Channel Mapping', [('RGB', 6),
                                                                 ('RBG', 9),
                                                                 ('BRG', 33),
                                                                 ('BGR', 36),
                                                                 ('GRB', 18),
                                                                 ('GBR', 24),
                                                                 ('RGBW', 27),
                                                                 ('RGWB', 30),
                                                                 ('RBGW', 39),
                                                                 ('RBWG', 45),
                                                                 ('RWGB', 54),
                                                                 ('RWBG', 57),
                                                                 ('GRWB', 78),
                                                                 ('GRBW', 75),
                                                                 ('GBWR', 108),
                                                                 ('GBRW', 99),
                                                                 ('GWBR', 120),
                                                                 ('GWRB', 114),
                                                                 ('BRGW', 135),
                                                                 ('BRWG', 141),
                                                                 ('BGRW', 147),
                                                                 ('BGWR', 156),
                                                                 ('BWRG', 177),
                                                                 ('BWGR', 180),
                                                                 ('WRBG', 201),
                                                                 ('WRGB', 198),
                                                                 ('WGBR', 216),
                                                                 ('WGRB', 210),
                                                                 ('WBGR', 228),
                                                                 ('WBRG', 225)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the currently used channel mapping as set by :func:`Set Channel Mapping`.
""",
'de':
"""
Gibt die aktuell genutzten Channel Mapping zurück, wie von
:func:`Set Channel Mapping` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Frame Started Callback Configuration',
'elements': [('Enable', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Enables/disables the :cb:`Frame Started` callback.

By default the callback is enabled.
""",
'de':
"""
Aktiviert/deaktiviert den :cb:`Frame Started` Callback.

Standardmäßig ist der Callback aktiviert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Frame Started Callback Configuration',
'elements': [('Enable', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the configuration as set by
:func:`Set Frame Started Callback Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von
:func:`Set Frame Started Callback Configuration` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('setter', 'Set LED Values', [('uint16', 0), ('uint8', [255, 0, 0, 0, 255, 0, 0, 0, 255])], 'Set first 3 LEDs to red, green and blue', None)]
})

com['examples'].append({
'name': 'Callback',
'functions': [('setter', 'Set Frame Duration', [('uint16', 50)], 'Set frame duration to 50ms (20 frames per second)', None),
              ('callback', ('Frame Started', 'frame started'), [(('Length', 'Length'), 'uint16', 1, None, None, None)], 'Use frame started callback to move the active LED every frame', None)],
'incomplete': True # because of array parameters and special logic in callback
})
