# -*- coding: utf-8 -*-

# Segment Display 4x7 Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 237,
    'name': ('SegmentDisplay4x7', 'segment_display_4x7', 'Segment Display 4x7'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for controling four 7-segment displays',
    'released': False,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('SetSegments', 'set_segments'), 
'elements': [('segments', 'uint8', 4, 'in'),
             ('brightness', 'uint8', 1, 'in'),
             ('colon', 'bool', 1, 'in')],
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
This is represented by the number 0b00110101 = 0x35 = 53.

The brightness can be set between 0 (dark) and 7 (bright). The colon
parameter turns the colon of the display on or off.
""",
'de':
"""
Die 7-Segment Anzeige kann mit Bitmaps gesetzt werden. Jedes Bit kontrolliert
ein Segment:

.. image:: /Images/Bricklets/bricklet_segment_display_4x7_bit_order.png
   :scale: 100 %
   :alt: Bitreihenfolge eines Segments
   :align: center

Beispiel: Um eine "5" auf der Anzeige darzustellen müssen die Segment 
0, 2, 3, 5 und 6 aktiviert werden. Dies kann mit der Zahl 
0b00110101 = 0x35 = 53 representiert werden.

Die Helligkeit kann zwischen 0 (dunkel) und 7 (hell) gesetzt werden.
Der dritte Parameter aktiviert/deaktiviert den Doppelpunkt auf der Anzeige.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetSegments', 'get_segments'), 
'elements': [('segments', 'uint8', 4, 'out'),
             ('brightness', 'uint8', 1, 'out'),
             ('colon', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the segment, brightness and color data as set by 
:func:`SetSegments`.
""",
'de':
"""
Gibt die Segment-, Helligkeit- und Doppenpunktdaten zurück, wie von 
:func:`SetSegments` gesetzt.
"""
}]
})
