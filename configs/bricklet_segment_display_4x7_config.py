# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Segment Display 4x7 Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 237,
    'name': 'Segment Display 4x7',
    'display_name': 'Segment Display 4x7',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Four 7-segment displays with switchable colon',
        'de': 'Vier 7-Segment-Anzeigen mit schaltbarem Doppelpunkt'
    },
    'released': True,
    'documented': True,
    'discontinued': False,
    'features': [
        'bricklet_get_identity'
    ],
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Set Segments',
'elements': [('Segments', 'uint8', 4, 'in'),
             ('Brightness', 'uint8', 1, 'in'),
             ('Colon', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
The 7-segment display can be set with bitmaps. Every bit controls one
segment:

.. image:: /Images/Bricklets/bricklet_segment_display_4x7_bit_order.png
   :scale: 100 %
   :alt: Bit order of one segment
   :align: center

For example to set a "5" you would want to activate segments 0, 2, 3, 5 and 6.
This is represented by the number 0b01101101 = 0x6d = 109.

The brightness can be set between 0 (dark) and 7 (bright). The colon
parameter turns the colon of the display on or off.
""",
'de':
"""
Die 7-Segment-Anzeige kann mit Bitmaps gesetzt werden. Jedes Bit kontrolliert
ein Segment:

.. image:: /Images/Bricklets/bricklet_segment_display_4x7_bit_order.png
   :scale: 100 %
   :alt: Bitreihenfolge eines Segments
   :align: center

Beispiel: Um eine "5" auf der Anzeige darzustellen müssen die Segment
0, 2, 3, 5 und 6 aktiviert werden. Dies kann mit der Zahl
0b01101101 = 0x6d = 109 repräsentiert werden.

Die Helligkeit kann zwischen 0 (dunkel) und 7 (hell) gesetzt werden.
Der dritte Parameter aktiviert/deaktiviert den Doppelpunkt auf der Anzeige.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Segments',
'elements': [('Segments', 'uint8', 4, 'out'),
             ('Brightness', 'uint8', 1, 'out'),
             ('Colon', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the segment, brightness and color data as set by
:func:`Set Segments`.
""",
'de':
"""
Gibt die Segment-, Helligkeit- und Doppelpunktdaten zurück, wie von
:func:`Set Segments` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Start Counter',
'elements': [('Value From', 'int16', 1, 'in'),
             ('Value To', 'int16', 1, 'in'),
             ('Increment', 'int16', 1, 'in'),
             ('Length', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Starts a counter with the *from* value that counts to the *to*
value with the each step incremented by *increment*.
The *length* of the increment is given in ms.

Example: If you set *from* to 0, *to* to 100, *increment* to 1 and
*length* to 1000, a counter that goes from 0 to 100 with one second
pause between each increment will be started.

The maximum values for *from*, *to* and *increment* is 9999,
the minimum value is -999.

Using a negative increment allows to count backwards.

You can stop the counter at every time by calling :func:`Set Segments`.
""",
'de':
"""
Starter einen Zähler mit dem *from* Wert der bis zum *to* Wert Zählt
mit einer Schrittweite von *increment*. Das Argument *length* gibt die
Pause zwischen den Erhöhungen in ms an.

Beispiel: Wenn *from* auf 0, *to* auf 100, *increment* auf 1 und
*length* auf 1000 gesetzt wird, wird ein Zähler gestartet der von
0 bis 100 zählt mit Rate von einer Sekunde zwischen jeder Erhöhung.

Der Maximalwert für *from*, *to* und *increment* ist 9999, der Minimalwert
ist -999.

Wenn das increment negativ ist läuft der Zähler rückwärts.

Der Zähler kann jederzeit durch einen Aufruf von :func:`Set Segments`
gestoppt werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Counter Value',
'elements': [('Value', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the counter value that is currently shown on the display.

If there is no counter running a 0 will be returned.
""",
'de':
"""
Gibt den aktuellen Zählerstand zurück der auf der Anzeige
angezeigt wird.

Wenn kein Zähler am laufen ist wird eine 0 zurückgegeben.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Counter Finished',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the counter (see :func:`Start Counter`) is
finished.
""",
'de':
"""
Diese Callback wird ausgelöst wenn der Zähler (siehe :func:`Start Counter`)
fertig ist.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'incomplete': True # because of array parameter
})
