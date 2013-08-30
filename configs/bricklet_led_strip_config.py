# -*- coding: utf-8 -*-

# LED Strip Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 231,
    'name': ('LEDStrip', 'led_strip', 'LED Strip'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device to control up to 320 RGB LEDs',
    'released': False,
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

Example: If you set index to 5, length to 3, r to [255, 0, 0], 
g to [0, 255, 0] and b to [0, 0, 255] the LEDs with index 5, 6
and 7 will get the color red, green and blue respectively.

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
""",
'de':
"""
Setzt die *rgb* Werte für die LEDs mit der angegebenen *length* und
startend vom angegebenen *index*.

Die maximale Länge ist 16. Der Index geht von 0 bis 319 und die
rgb Werte haben jeweils 8 Bit.

Beispiel: Wenn der Index auf 5, die Länge auf 3, r auf [255, 0, 0],
g auf [0, 255, 0] und b auf [0, 0, 255] gesetzt wird, werden die LEDs
mit den Indizes 5, 6 und 7 die Farben Rot, Grün und Blau annehmen.

Die Farben werden auf die tatsächlichen LEDs transferriert wenn die
nächste *frame duration* abgelaufen ist, siehe :func:`SetFrameDuration`.

Genereller Ansatz:

* Setze *frame duration* auf einen Wert welcher der Anzahl der
  Bilder pro Sekunde entspricht die erreicht werden sollen.

* Setze alle LEDs für einen Frame.

* Warte auf :func:`FrameRendered` callback.

* Setze alle LEDs für den nächsten Frame.

* Warte auf :func:`FrameRendered` callback.

* Und so weiter.

Dieser Ansatz garantiert das die LED Farben mit einer
festen Framerate angezeigt werden.
"""
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
Gibt rgb Werte mit der übergebenen *length* zurück, startend vom
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
Returns the current supply voltage of the LEDs. The voltage is given
in mv. 
""",
'de':
"""
Gibt die aktuelle Versorgungsspannung der LEDs zurück. Die Spannung ist
in mv angegeben.
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

