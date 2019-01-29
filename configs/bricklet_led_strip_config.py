# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# LED Strip Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 3],
    'category': 'Bricklet',
    'device_identifier': 231,
    'name': 'LED Strip',
    'display_name': 'LED Strip',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Controls up to 320 RGB LEDs',
        'de': 'Steuert bis zu 320 RGB LEDs'
    },
    'released': True,
    'documented': True,
    'discontinued': True, # replaced by LED Strip Bricklet 2.0
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Set RGB Values',
'elements': [('Index', 'uint16', 1, 'in'),
             ('Length', 'uint8', 1, 'in'),
             ('R', 'uint8', 16, 'in'),
             ('G', 'uint8', 16, 'in'),
             ('B', 'uint8', 16, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the RGB values for the LEDs with the given *length* starting
from *index*.

To make the colors show correctly you need to configure the chip type
(:func:`Set Chip Type`) and a 3-channel channel mapping (:func:`Set Channel Mapping`)
according to the connected LEDs.

The maximum length is 16, the index goes from 0 to 319 and the rgb values
have 8 bits each.

Example: If you set

* index to 5,
* length to 3,
* r to |r_values|,
* g to |g_values| and
* b to |b_values|

the LED with index 5 will be red, 6 will be green and 7 will be blue.

.. note:: Depending on the LED circuitry colors can be permuted.

The colors will be transfered to actual LEDs when the next
frame duration ends, see :func:`Set Frame Duration`.

Generic approach:

* Set the frame duration to a value that represents
  the number of frames per second you want to achieve.
* Set all of the LED colors for one frame.
* Wait for the :cb:`Frame Rendered` callback.
* Set all of the LED colors for next frame.
* Wait for the :cb:`Frame Rendered` callback.
* and so on.

This approach ensures that you can change the LED colors with
a fixed frame rate.

The actual number of controllable LEDs depends on the number of free
Bricklet ports. See :ref:`here <led_strip_bricklet_ram_constraints>` for more
information. A call of :func:`Set RGB Values` with index + length above the
bounds is ignored completely.
""",
'de':
"""
Setzt die RGB Werte für die LEDs mit der angegebenen *length*,
beginnend vom angegebenen *index*.

Damit die Farben richtig angezeigt werden muss den LEDs entsprechend der
richtig Chip Type (:func:`Set Chip Type`) und das richtige 3-Kanal Channel Mapping
(:func:`Set Channel Mapping`) eingestellt werden.

Die maximale Länge ist 16. Der Index geht von 0 bis 319 und die
rgb Werte haben jeweils 8 Bit.

Beispiel: Wenn

* index auf 5,
* length auf 3,
* r auf |r_values|,
* g auf |g_values| und
* b auf |b_values|

gesetzt wird, wird die LED an Index 5 die Farbe Rot annehmen, 6 wird Grün und 7
wird Blau.

.. note:: Abhängig von der internen LED Schaltung können die Farben vertauscht
   sein.

Die Farben werden auf die tatsächlichen LEDs transferiert wenn die
nächste *frame duration* abgelaufen ist, siehe :func:`Set Frame Duration`.

Genereller Ansatz:

* Setze *frame duration* auf einen Wert welcher der Anzahl der
  Bilder pro Sekunde entspricht die erreicht werden sollen.
* Setze alle LEDs für einen Frame.
* Warte auf :cb:`Frame Rendered` Callback.
* Setze alle LEDs für den nächsten Frame.
* Warte auf :cb:`Frame Rendered` Callback.
* Und so weiter.

Dieser Ansatz garantiert, dass die LED Farben mit einer
festen Framerate angezeigt werden.

Die effektive Anzahl steuerbarer LEDs ist abhängig von der Anzahl
der freien Bricklet Ports (siehe :ref:`hier <led_strip_bricklet_ram_constraints>`).
Ein Aufruf von :func:`Set RGB Values` mit index + length größer als die
Begrenzung werden komplett ingnoriert.
"""
},
{
'*': {
'r_values': {'php': 'array(255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)',
             '*': '[255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]'},
'g_values': {'php': 'array(0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)',
             '*': '[0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]'},
'b_values': {'php': 'array(0, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)',
             '*': '[0, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]'}
}
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get RGB Values',
'elements': [('Index', 'uint16', 1, 'in'),
             ('Length', 'uint8', 1, 'in'),
             ('R', 'uint8', 16, 'out'),
             ('G', 'uint8', 16, 'out'),
             ('B', 'uint8', 16, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns RGB value with the given *length* starting from the
given *index*.

The values are the last values that were set by :func:`Set RGB Values`.
""",
'de':
"""
Gibt RGB Werte mit der übergebenen *length* zurück, beginnend vom
übergebenen *index*.

Die Werte sind die letzten von :func:`Set RGB Values` gesetzten Werte.
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

For an explanation of the general approach see :func:`Set RGB Values`.

Default value: 100ms (10 frames per second).
""",
'de':
"""
Setzt die *frame duration* (Länge des Frames) in ms.

Beispiel: Wenn 20 Frames pro Sekunde erreicht werden sollen, muss
die Länge des Frames auf 50ms gesetzt werden (50ms * 20 = 1 Sekunde).

Für eine Erklärung des generellen Ansatzes siehe :func:`Set RGB Values`.

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
'name': 'Frame Rendered',
'elements': [('Length', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered directly after a new frame is rendered. The
:word:`parameter` is the number of LEDs in that frame.

You should send the data for the next frame directly after this callback
was triggered.

For an explanation of the general approach see :func:`Set RGB Values`.
""",
'de':
"""
Dieser Callback wird direkt direkt nachdem ein Frame gerendert wurde ausgelöst.
Der :word:`parameter` ist die Anzahl der LEDs in diesem Frame.

Die Daten für das nächste Frame sollten direkt nach dem auslösen dieses
Callbacks übertragen werden.

Für eine Erklärung des generellen Ansatzes siehe :func:`Set RGB Values`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Clock Frequency',
'elements': [('Frequency', 'uint32', 1, 'in')],
'since_firmware': [2, 0, 1],
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

.. note::
 The frequency in firmware version 2.0.0 is fixed at 2MHz.
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

.. note::
 Die Frequenz in Firmware Version 2.0.0 ist fest auf 2MHz gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Clock Frequency',
'elements': [('Frequency', 'uint32', 1, 'out')],
'since_firmware': [2, 0, 1],
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
'since_firmware': [2, 0, 2],
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
'since_firmware': [2, 0, 2],
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
'name': 'Set RGBW Values',
'elements': [('Index', 'uint16', 1, 'in'),
             ('Length', 'uint8', 1, 'in'),
             ('R', 'uint8', 12, 'in'),
             ('G', 'uint8', 12, 'in'),
             ('B', 'uint8', 12, 'in'),
             ('W', 'uint8', 12, 'in')],
'since_firmware': [2, 0, 6],
'doc': ['bf', {
'en':
"""
Sets the RGBW values for the LEDs with the given *length* starting
from *index*.

To make the colors show correctly you need to configure the chip type
(:func:`Set Chip Type`) and a 4-channel channel mapping (:func:`Set Channel Mapping`)
according to the connected LEDs.

The maximum length is 12, the index goes from 0 to 239 and the rgbw values
have 8 bits each.

Example: If you set

* index to 5,
* length to 4,
* r to |r_values|,
* g to |g_values|,
* b to |b_values| and
* w to |b_values|

the LED with index 5 will be red, 6 will be green, 7 will be blue and 8 will be white.

.. note:: Depending on the LED circuitry colors can be permuted.

The colors will be transfered to actual LEDs when the next
frame duration ends, see :func:`Set Frame Duration`.

Generic approach:

* Set the frame duration to a value that represents
  the number of frames per second you want to achieve.
* Set all of the LED colors for one frame.
* Wait for the :cb:`Frame Rendered` callback.
* Set all of the LED colors for next frame.
* Wait for the :cb:`Frame Rendered` callback.
* and so on.

This approach ensures that you can change the LED colors with
a fixed frame rate.

The actual number of controllable LEDs depends on the number of free
Bricklet ports. See :ref:`here <led_strip_bricklet_ram_constraints>` for more
information. A call of :func:`Set RGBW Values` with index + length above the
bounds is ignored completely.

The LPD8806 LED driver chips have 7-bit channels for RGB. Internally the LED
Strip Bricklets divides the 8-bit values set using this function by 2 to make
them 7-bit. Therefore, you can just use the normal value range (0-255) for
LPD8806 LEDs.

The brightness channel of the APA102 LED driver chips has 5-bit. Internally the
LED Strip Bricklets divides the 8-bit values set using this function by 8 to make
them 5-bit. Therefore, you can just use the normal value range (0-255) for
the brightness channel of APA102 LEDs.
""",
'de':
"""
Setzt die RGBW Werte für die LEDs mit der angegebenen *length*,
beginnend vom angegebenen *index*.

Damit die Farben richtig angezeigt werden muss den LEDs entsptechend der
richtig Chip Type (:func:`Set Chip Type`) und das richtige 4-Kanal Channel Mapping
(:func:`Set Channel Mapping`) eingestellt werden.

Die maximale Länge ist 12. Der Index geht von 0 bis 239 und die
rgbw Werte haben jeweils 8 Bit.

Beispiel: Wenn

* index auf 5,
* length auf 4,
* r auf |r_values|,
* g auf |g_values|,
* b auf |b_values| und
* w auf |w_values|

gesetzt wird, wird die LED an Index 5 die Farbe Rot annehmen, 6 wird Grün, 7
wird Blau und 8 wird Weiß.

.. note:: Abhängig von der internen LED Schaltung können die Farben vertauscht
   sein.

Die Farben werden auf die tatsächlichen LEDs transferiert wenn die
nächste *frame duration* abgelaufen ist, siehe :func:`Set Frame Duration`.

Genereller Ansatz:

* Setze *frame duration* auf einen Wert welcher der Anzahl der
  Bilder pro Sekunde entspricht die erreicht werden sollen.
* Setze alle LEDs für einen Frame.
* Warte auf :cb:`Frame Rendered` Callback.
* Setze alle LEDs für den nächsten Frame.
* Warte auf :cb:`Frame Rendered` Callback.
* Und so weiter.

Dieser Ansatz garantiert das die LED Farben mit einer
festen Framerate angezeigt werden.

Die effektive Anzahl steuerbarer LEDs ist abhängig von der Anzahl
der freien Bricklet Ports (siehe :ref:`hier <led_strip_bricklet_ram_constraints>`).
Ein Aufruf von :func:`Set RGBW Values` mit index + length größer als die
Begrenzung werden komplett ignoriert.

Die LPD8806 LED-Treiber-Chips haben 7-Bit Kanäle für RGB. Intern teilt das
LED Strip Bricklet die 8-Bit Werte die mit dieser Funktion gesetzt werden
durch 2, um daraus 7-Bit Werte zu machen. Daher kann der normale Wertebereich
(0-255) auch für LPD8806 LEDs verwendet werden.

Der Helligkeitskanal der APA102 LED-Treiber-Chips hat 5-Bit. Intern teilt das
LED Strip Bricklet die 8-Bit Werte die mit dieser Funktion gesetzt werden
durch 8, um daraus 5-Bit Werte zu machen. Daher kann der normale Wertebereich
(0-255) auch für den Helligkeitskanal von APA102 LEDs verwendet werden.
"""
},
{
'*': {
'r_values': {'php': 'array(255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)',
             '*': '[255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]'},
'g_values': {'php': 'array(0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)',
             '*': '[0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]'},
'b_values': {'php': 'array(0, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0)',
             '*': '[0, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0]'},
'w_values': {'php': 'array(0, 0, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0)',
             '*': '[0, 0, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0]'}
}
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get RGBW Values',
'elements': [('Index', 'uint16', 1, 'in'),
             ('Length', 'uint8', 1, 'in'),
             ('R', 'uint8', 12, 'out'),
             ('G', 'uint8', 12, 'out'),
             ('B', 'uint8', 12, 'out'),
             ('W', 'uint8', 12, 'out')],
'since_firmware': [2, 0, 6],
'doc': ['bf', {
'en':
"""
Returns RGBW values with the given *length* starting from the
given *index*.

The values are the last values that were set by :func:`Set RGBW Values`.
""",
'de':
"""
Gibt RGBW Werte mit der übergebenen *length* zurück, beginnend vom
übergebenen *index*.

Die Werte sind die letzten von :func:`Set RGBW Values` gesetzten Werte.
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
'since_firmware': [2, 0, 6],
'doc': ['bf', {
'en':
"""
Sets the channel mapping for the connected LEDs.

:func:`Set RGB Values` and :func:`Set RGBW Values` take the data in RGB(W) order.
But the connected LED driver chips might have their 3 or 4 channels in a
different order. For example, the WS2801 chips typically use BGR order, the
WS2812 chips typically use GRB order and the APA102 chips typically use WBGR
order.

The APA102 chips are special. They have three 8-bit channels for RGB
and an additional 5-bit channel for the overall brightness of the RGB LED
making them 4-channel chips. Internally the brightness channel is the first
channel, therefore one of the Wxyz channel mappings should be used. Then
the W channel controls the brightness.

If a 3-channel mapping is selected then :func:`Set RGB Values` has to be used.
Calling :func:`Set RGBW Values` with a 3-channel mapping will produce incorrect
results. Vice-versa if a 4-channel mapping is selected then
:func:`Set RGBW Values` has to be used. Calling :func:`Set RGB Values` with a
4-channel mapping will produce incorrect results.

The default value is BGR (36).
""",
'de':
"""
Setzt das Channel Mapping für die angeschlossenene LEDs.

:func:`Set RGB Values` und :func:`Set RGBW Values` nehmen die Daten in RGB(W)
Reihenfolge entgegen. Aber die angeschlossenen LED-Treiber-Chips erwarten die
Daten für ihre 3 oder 4 Kanäle in einer anderen Reihenfolge. Zum Beispiel
verwenden WS2801 Chips typischerweise BGR Reihenfolge, WS2812 Chips
verwenden typischerweise GRB Reihenfolge und APA102 verwenden typischerweise
WBGR Reihenfolge.

Die APA102 haben eine Besonderheit. Sie haben drei 8-Bit Kanäle für RGB und
einen zusätzlichen 5-Bit Kanal für die Helligkeit der RGB LED. Dadurch ist der
APA102 insgesamt ein 4-Kanal Chip. Intern ist der Helligkeitskanal der erste
Kanal. Daher sollte eines der Wxyz Channel Mappings verwendet werden. Dann kann
über den W Kanal die Helligkeit eingestellt werden.

Wenn ein 3-Kanal Mapping ausgewählt wurde, dann muss auch :func:`Set RGB Values`
für das setzen der Farben verwendet werden. :func:`Set RGBW Values` zusammen
mit einem 3-Kanal Mapping führt zu falscher Darstellung der Farben. Im Gegenzug
muss bei einem 4-Kanal Mapping :func:`Set RGBW Values` für das setzen der Farben
verwendet werden. :func:`Set RGB Values` zusammen mit einem 4-Kanal Mapping führt
zu falscher Darstellung der Farben.

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
'since_firmware': [2, 0, 6],
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
'name': 'Enable Frame Rendered Callback',
'elements': [],
'since_firmware': [2, 0, 6],
'doc': ['ccf', {
'en':
"""
Enables the :cb:`Frame Rendered` callback.

By default the callback is enabled.
""",
'de':
"""
Aktiviert den :cb:`Frame Rendered` Callback.

Standardmäßig ist der Callback aktiviert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Disable Frame Rendered Callback',
'elements': [],
'since_firmware': [2, 0, 6],
'doc': ['ccf', {
'en':
"""
Disables the :cb:`Frame Rendered` callback.

By default the callback is enabled.
""",
'de':
"""
Deaktiviert den :cb:`Frame Rendered` Callback.

Standardmäßig ist der Callback aktiviert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is Frame Rendered Callback Enabled',
'elements': [('Enabled', 'bool', 1, 'out')],
'since_firmware': [2, 0, 6],
'doc': ['ccf', {
'en':
"""
Returns *true* if the :cb:`Frame Rendered` callback is enabled, *false* otherwise.
""",
'de':
"""
Gibt *true* zurück falls der :cb:`Frame Rendered` Callback aktiviert ist, *false*
sonst.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'incomplete': True # because of array parameters
})

com['examples'].append({
'name': 'Callback',
'functions': [('setter', 'Set Frame Duration', [('uint16', 50)], 'Set frame duration to 50ms (20 frames per second)', None),
              ('callback', ('Frame Rendered', 'frame rendered'), [(('Length', 'Length'), 'uint16', 1, None, None, None)], 'Use frame rendered callback to move the active LED every frame', None)],
'incomplete': True # because of array parameters and special logic in callback
})
