# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# GPS Bricklet communication config

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
    'released': False,
    'documented': False,
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
Sets the 64 red led values of the matrix.
""",
'de':
"""
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
Returns the red led values as set by :func:`Set Red`.
""",
'de':
"""
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
Sets the 64 green led values of the matrix.
""",
'de':
"""
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
Returns the green led values as set by :func:`Set Green`.
""",
'de':
"""
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
Sets the 64 blue led values of the matrix.
""",
'de':
"""
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
Returns the lbue led values as set by :func:`Set Blue`.
""",
'de':
"""
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
Setzt die *frame duration* (Länge des Frames) in ms.

Beispiel: Wenn 20 Frames pro Sekunde erreicht werden sollen, muss
die Länge des Frames auf 50ms gesetzt werden (50ms * 20 = 1 Sekunde).

Setze diesen Wert auf 0 um das automatische schreiben der Frames
auszustellen.

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
Gibt die *frame duration* (Länge des Frames) in ms zurück, wie von
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
function to transfer one frame to the matrix.

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
"""
}]
})

