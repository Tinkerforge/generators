# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# RGB LED Matrix Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 272,
    'name': 'RGB LED Matrix',
    'display_name': 'RGB LED Matrix',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'RGB LED Matrix with 8x8 pixel',
        'de': 'RGB LED Matrix mit 8x8 Pixel'
    },
    'comcu': True,
    'released': True,
    'documented': True,
    'discontinued': True, # currently no replacement available
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Set Red',
'elements': [('Red', 'uint8', 64, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the 64 red LED values of the matrix.
""",
'de':
"""
Setzt die Werte der 64 roten LEDs der Matrix.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Red',
'elements': [('Red', 'uint8', 64, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the red LED values as set by :func:`Set Red`.
""",
'de':
"""
Gibt die Werte der roten LED zurück, wie von :func:`Set Red` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Green',
'elements': [('Green', 'uint8', 64, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the 64 green LED values of the matrix.
""",
'de':
"""
Setzt die Werte der 64 grünen LEDs der Matrix.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Green',
'elements': [('Green', 'uint8', 64, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the green LED values as set by :func:`Set Green`.
""",
'de':
"""
Gibt die Werte der grünen LED zurück, wie von :func:`Set Green` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Blue',
'elements': [('Blue', 'uint8', 64, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the 64 blue LED values of the matrix.
""",
'de':
"""
Setzt die Werte der 64 blauen LEDs der Matrix.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Blue',
'elements': [('Blue', 'uint8', 64, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the blue LED values as set by :func:`Set Blue`.
""",
'de':
"""
Gibt die Werte der blauen LED zurück, wie von :func:`Set Blue` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Frame Duration',
'elements': [('Frame Duration', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the frame duration in ms.

Example: If you want to achieve 20 frames per second, you should
set the frame duration to 50ms (50ms * 20 = 1 second).

Set this value to 0 to turn the automatic frame write mechanism off.

Approach:

* Call :func:`Set Frame Duration` with value > 0.
* Set LED values for first frame with :func:`Set Red`, :func:`Set Green`, :func:`Set Blue`.
* Wait for :cb:`Frame Started` callback.
* Set LED values for second frame with :func:`Set Red`, :func:`Set Green`, :func:`Set Blue`.
* Wait for :cb:`Frame Started` callback.
* and so on.

For frame duration of 0 see :func:`Draw Frame`.

Default value: 0 = off.
""",
'de':
"""
Setzt die *Frame Duration* (Dauer des Frames) in ms.

Beispiel: Wenn 20 Frames pro Sekunde erreicht werden sollen, muss
die Länge des Frames auf 50ms gesetzt werden (50ms * 20 = 1 Sekunde).

Setze diesen Wert auf 0 um das automatische schreiben der Frames
auszustellen.

Vorgehensweise:

* :func:`Set Frame Duration` mit einem Wert > 0 aufrufen.
* LED Werte für den ersten Frame mit :func:`Set Red`, :func:`Set Green` und :func:`Set Blue` setzen.
* Auf :cb:`Frame Started` Callback warten.
* LED Werte für den nächsten Frame mit :func:`Set Red`, :func:`Set Green` und :func:`Set Blue` setzen.
* Auf :cb:`Frame Started` Callback warten.
* Und so weiter.

Für eine *Frame Duration* von 0 siehe :func:`Draw Frame`.

Standardwert: 0 = aus.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Frame Duration',
'elements': [('Frame Duration', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the frame duration in ms as set by :func:`Set Frame Duration`.
""",
'de':
"""
Gibt die *Frame Duration* (Dauer des Frames) in ms zurück, wie von
:func:`Set Frame Duration` gesetzt.
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Draw Frame',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
If you set the frame duration to 0 (see :func:`Set Frame Duration`), you can use this
function to transfer the frame to the matrix.

Approach:

* Call :func:`Set Frame Duration` with 0.
* Set LED values for first frame with :func:`Set Red`, :func:`Set Green`, :func:`Set Blue`.
* Call :func:`Draw Frame`.
* Wait for :cb:`Frame Started` callback.
* Set LED values for second frame with :func:`Set Red`, :func:`Set Green`, :func:`Set Blue`.
* Call :func:`Draw Frame`.
* Wait for :cb:`Frame Started` callback.
* and so on.
""",
'de':
"""
Wenn die *Frame Duration* (Dauer des Frames) auf 0 gesetzt ist (siehe
:func:`Set Frame Duration`), dann kann diese Funktionen aufgerufen werden um
den Frame auf die Matrix zu übertragen.

Vorgehensweise:

* :func:`Set Frame Duration` mit 0 aufrufen.
* LED Werte für den ersten Frame mit :func:`Set Red`, :func:`Set Green` und :func:`Set Blue` setzen.
* :func:`Draw Frame` aufrufen.
* Auf :cb:`Frame Started` Callback warten.
* LED Werte für den nächsten Frame mit :func:`Set Red`, :func:`Set Green` und :func:`Set Blue` setzen.
* :func:`Draw Frame` aufrufen.
* Auf :cb:`Frame Started` Callback warten.
* Und so weiter.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Supply Voltage',
'elements': [('Voltage', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the current supply voltage of the Bricklet. The voltage is given in mV.
""",
'de':
"""
Gibt die aktuelle Versorgungsspannung des Bricklets zurück. Die Spannung ist
in mV angegeben.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Frame Started',
'elements': [('Frame Number', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered as soon as a new frame write is started.
The LED values are double buffered, so you can send the LED values
for the next frame directly after this callback is triggered.
""",
'de':
"""
Dieser Callback wird aufgerufen sobald die Übertragung des Frames auf die Matrix
beginnt. Die LED Werte werden in einem Doublebuffer gespeichert, so dass der
nächste Frame an das Bricklet übertragen werden kann sobald dieser Callback
ausgelöst wird.
"""
}]
})
