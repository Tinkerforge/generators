# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# LED Strip Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 2],
    'category': 'Bricklet',
    'device_identifier': 231,
    'name': ('LEDStrip', 'led_strip', 'LED Strip'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device to control up to 320 RGB LEDs',
    'released': True,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('SetRGBValues', 'set_rgb_values'), 
'elements': [('index', 'uint16', 1, 'in'),
             ('length', 'uint8', 1, 'in'),
             ('r', 'uint8', 16, 'in'),
             ('g', 'uint8', 16, 'in'),
             ('b', 'uint8', 16, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the *rgb* values for the LEDs with the given *length* starting 
from *index*.

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
frame duration ends, see :func:`SetFrameDuration`.

Generic approach: 

* Set the frame duration to a value that represents
  the number of frames per second you want to achieve. 
* Set all of the LED colors for one frame.
* Wait for the :func:`FrameRendered` callback.
* Set all of the LED colors for next frame.
* Wait for the :func:`FrameRendered` callback.
* and so on.

This approach ensures that you can change the LED colors with
a fixed frame rate.

The actual number of controllable LEDs depends on the number of free
Bricklet ports. See :ref:`here <led_strip_bricklet_ram_constraints>` for more
information. A call of :func:`SetRGBValues` with index + length above the
bounds is ignored completely.
""",
'de':
"""
Setzt die *rgb* Werte für die LEDs mit der angegebenen *length*,
beginnend vom angegebenen *index*.

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
nächste *frame duration* abgelaufen ist, siehe :func:`SetFrameDuration`.

Genereller Ansatz:

* Setze *frame duration* auf einen Wert welcher der Anzahl der
  Bilder pro Sekunde entspricht die erreicht werden sollen.
* Setze alle LEDs für einen Frame.
* Warte auf :func:`FrameRendered` Callback.
* Setze alle LEDs für den nächsten Frame.
* Warte auf :func:`FrameRendered` Callback.
* Und so weiter.

Dieser Ansatz garantiert das die LED Farben mit einer
festen Framerate angezeigt werden.

Die effektive Anzahl steuerbarer LEDs ist abhängig von der Anzahl
der freien Bricklet Ports (siehe :ref:`hier <led_strip_bricklet_ram_constraints>`).
Ein Aufruf von :func:`SetRGBValues` mit index + length größer als die 
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
'name': ('GetRGBValues', 'get_rgb_values'), 
'elements': [('index', 'uint16', 1, 'in'),
             ('length', 'uint8', 1, 'in'),
             ('r', 'uint8', 16, 'out'),
             ('g', 'uint8', 16, 'out'),
             ('b', 'uint8', 16, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the rgb with the given *length* starting from the
given *index*.

The values are the last values that were set by :func:`SetRGBValues`.
""",
'de':
"""
Gibt rgb Werte mit der übergebenen *length* zurück, beginnend vom
übergebenen *index*.

Die Werte sind die letzten von :func:`SetRGBValues` gesetzten Werte.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetFrameDuration', 'set_frame_duration'), 
'elements': [('duration', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the frame duration in ms.

Example: If you want to achieve 20 frames per second, you should
set the frame duration to 50ms (50ms * 20 = 1 second). 

For an explanation of the general approach see :func:`SetRGBValues`.

Default value: 100ms (10 frames per second).
""",
'de':
"""
Setzt die *frame duration* (Länge des Frames) in ms.

Beispiel: Wenn 20 Frames pro Sekunde erreicht werden sollen, muss
die Länge des Frames auf 50ms gesetzt werden (50ms * 20 = 1 Sekunde).

Für eine Erklärung des generellen Ansatzes siehe :func:`SetRGBValues`.

Standardwert: 100ms (10 Frames pro Sekunde).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetFrameDuration', 'get_frame_duration'), 
'elements': [('duration', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the frame duration as set by :func:`SetFrameDuration`.
""",
'de':
"""
Gibt die *frame duration* (Länge des Frames) zurück, wie von
:func:`SetFrameDuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetSupplyVoltage', 'get_supply_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')],
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
'name': ('FrameRendered', 'frame_rendered'), 
'elements': [('length', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered directly after a new frame is rendered.

You should send the data for the next frame directly after this callback
was triggered.

For an explanation of the general approach see :func:`SetRGBValues`.
""",
'de':
"""
Dieser Callback wird direkt direkt nachdem ein Frame gerendert wurde ausgelöst.

Die Daten für das nächste Frame sollten direkt nach dem auslösen dieses
Callbacks übertragen werden.

Für eine Erklärung des generellen Ansatzes siehe :func:`SetRGBValues`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetClockFrequency', 'set_clock_frequency'), 
'elements': [('frequency', 'uint32', 1, 'in')],
'since_firmware': [2, 0, 1],
'doc': ['bf', {
'en':
"""
Sets the frequency of the clock in Hz. The range is 10000Hz (10kHz) up to
2000000Hz (2MHz).

The Bricklet will choose the nearest achievable frequency, which may
be off by a few Hz. You can get the exact frequency that is used by
calling :func:`GetClockFrequency`.

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
wie sie genutzt wird kann mit :func:`GetClockFrequency` erfragt werden.

Wenn Probleme mit flackernden LEDs auftreten kann es daran liegen das
Bits auf der Leitung flippen. Dies kann behoben werden in dem man die
Verbindung zwischen Bricklet und LEDs verringert oder in dem man die
Frequenz reduziert.

Mit abnehmender Frequenz nimmt allerdings auch die maximale Framerateab.

Der Standardwert ist 1,66MHz

.. note::
 Die Frequenz in Firmware Version 2.0.0 ist fest auf 2MHz gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetClockFrequency', 'get_clock_frequency'), 
'elements': [('frequency', 'uint32', 1, 'out')],
'since_firmware': [2, 0, 1],
'doc': ['bf', {
'en':
"""
Returns the currently used clock frequency as set by :func:`SetClockFrequency`.
""",
'de':
"""
Gibt die aktuell genutzte Clock-Frequenz zurück, wie von
:func:`SetClockFrequency` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetChipType', 'set_chip_type'), 
'elements': [('chip', 'uint16', 1, 'in', ('ChipType', 'chip_type', [('WS2801', 'ws2801', 2801),
                                                                    ('WS2811', 'ws2811', 2811),
                                                                    ('WS2812', 'ws2812', 2812)]))],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Sets the type of the led driver chip. We currently support
the chips

* WS2801 (``chip`` = 2801),
* WS2811 (``chip`` = 2811) and
* WS2812 (``chip`` = 2812).

The WS2812 is sometimes also called "NeoPixel", a name coined by
Adafruit.

The default value is WS2801 (``chip`` = 2801).
""",
'de':
"""
Setzt den Typ des LED-Treiber-Chips. Aktuell unterstützen
wir die Chips

* WS2801 (``chip`` = 2801),
* WS2811 (``chip`` = 2811) und
* WS2812 (``chip`` = 2812).

Der WS2812 wird manchmal auch "NeoPixel" genannt, ein Name
der von Adafruit geprägt wurde.

Der Standardwert ist WS2801 (``chip`` = 2801).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetChipType', 'get_chip_type'), 
'elements': [('chip', 'uint16', 1, 'out', ('ChipType', 'chip_type', [('WS2801', 'ws2801', 2801),
                                                                     ('WS2811', 'ws2811', 2811),
                                                                     ('WS2812', 'ws2812', 2812)]))],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Returns the currently used chip type as set by :func:`SetChipType`.
""",
'de':
"""
Gibt den aktuell genutzten Typ des Chips zurück, wie von
:func:`SetChipType` gesetzt.
"""
}]
})

