# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Segment Display 4x7 Bricklet communication config

from openhab_common import *

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
    'discontinued': False, # selling remaining stock, replaced by Segment Display 4x7 Bricklet 2.0
    'features': [
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Set Segments',
'elements': [('Segments', 'uint8', 4, 'in', {'range': (0, 0x7F)}),
             ('Brightness', 'uint8', 1, 'in', {'range': (0, 7)}),
             ('Colon', 'bool', 1, 'in', {})],
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
'elements': [('Segments', 'uint8', 4, 'out', {'range': (0, 0x7F)}),
             ('Brightness', 'uint8', 1, 'out', {'range': (0, 7)}),
             ('Colon', 'bool', 1, 'out', {})],
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
'elements': [('Value From', 'int16', 1, 'in', {'range': (-999, 9999)}),
             ('Value To', 'int16', 1, 'in', {'range': (-999, 9999)}),
             ('Increment', 'int16', 1, 'in', {'range': (-999, 9999)}),
             ('Length', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Starts a counter with the *from* value that counts to the *to*
value with the each step incremented by *increment*.
*length* is the pause between each increment.

Example: If you set *from* to 0, *to* to 100, *increment* to 1 and
*length* to 1000, a counter that goes from 0 to 100 with one second
pause between each increment will be started.

Using a negative increment allows to count backwards.

You can stop the counter at every time by calling :func:`Set Segments`.
""",
'de':
"""
Starter einen Zähler mit dem *from* Wert der bis zum *to* Wert Zählt
mit einer Schrittweite von *increment*. Das Argument *length* ist
die Länge der Pause zwischen zwei Inkrements.

Beispiel: Wenn *from* auf 0, *to* auf 100, *increment* auf 1 und
*length* auf 1000 gesetzt wird, wird ein Zähler gestartet der von
0 bis 100 zählt mit Rate von einer Sekunde zwischen jeder Erhöhung.

Wenn das increment negativ ist läuft der Zähler rückwärts.

Der Zähler kann jederzeit durch einen Aufruf von :func:`Set Segments`
gestoppt werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Counter Value',
'elements': [('Value', 'uint16', 1, 'out', {'range': (-999, 9999)})],
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
Diese Callback wird ausgelöst, wenn der Zähler (siehe :func:`Start Counter`)
fertig ist.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'incomplete': True # because of array parameter
})


com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.OnOffType', 'org.eclipse.smarthome.core.library.types.StringType'],

    'param_groups': oh_generic_channel_param_groups(),
    'channels': [{
            'id': 'Brightness',
            'type': 'Brightness',

            'getters': [{
                'packet': 'Get Segments',
                'transform': 'new QuantityType(value.brightness, SmartHomeUnits.ONE)'}],
            'setters': [{
                'packet': 'Set Segments',
                'packet_params': ['this.getSegments().segments', 'cmd.shortValue()', 'this.getSegments().colon'],
                'command_type': 'Number'
            }],

        }, {
            'id': 'Colon',
            'type': 'Colon',

            'getters': [{
                'packet': 'Get Segments',
                'transform': 'value.colon ? OnOffType.ON : OnOffType.OFF'}],
            'setters': [{
                'packet': 'Set Segments',
                'packet_params': ['this.getSegments().segments', 'this.getSegments().brightness', 'cmd == OnOffType.ON'],
                'command_type': 'OnOffType'
            }],
        }, {
            'id': 'Segments',
            'type': 'Segments',

            'getters': [{
                'packet': 'Get Segments',
                'transform': 'new QuantityType((int)value.segments[0] << 24 | (int)value.segments[1] << 16 | (int)value.segments[2] << 8 | (int)value.segments[3], SmartHomeUnits.ONE)'
            }],
            'setters': [{
                'packet': 'Set Segments',
                'packet_params': ['new short[]{(short)(cmd.intValue() >> 24), (short)(cmd.intValue() >> 16), (short)(cmd.intValue() >> 8), (short)(cmd.intValue())}', 'this.getSegments().brightness', 'this.getSegments().colon'],
                'command_type': 'Number'
            }],

        },  {
            'id': 'Text',
            'type': 'Text',

            'setters': [{
                'packet': 'Set Segments',
                'packet_params': ['Helper.parseSegmentDisplayText(cmd.toString())', 'this.getSegments().brightness', 'cmd.toString().contains(":")'],
                'command_type': 'StringType'
            }],
            'setter_refreshs': [
                {'channel': 'Segments', 'delay': '0'},
                {'channel': 'Colon', 'delay': '0'},
            ],

        }
    ],
    'channel_types': [ {
            'id': 'Brightness',
            'item_type': 'Number:Dimensionless',
            'label': 'Brightness',
            'description': 'The brightness can be set between 0 (dark) and 7 (bright).',
            'read_only': False,
            'pattern': '%d',
            'min': 0,
            'max': 7,
            'is_trigger_channel': False,
            'options': [('0', '0'),
                        ('1', '1'),
                        ('2', '2'),
                        ('3', '3'),
                        ('4', '4'),
                        ('5', '5'),
                        ('6', '6'),
                        ('7', '7')]
        },
        oh_generic_channel_type('Segments', 'Number:Dimensionless', 'Segments',
                    update_style=None,
                    description='The seven segment display can be set with bitmaps. Every bit controls one segment as shown <a href=https://www.tinkerforge.com/en/doc/_images/bricklet_segment_display_4x7_bit_order.png>here</a>. The channel accepts an integer, that is split into 4 bytes, controlling one segment each. For example 1717263183, which is 0x665b5b4f in hex will be split into 0x66 for the first segment, 0x5b for the second, 0x5b for the third and 0x4f for the fourth.',
                    pattern='%d'),
        oh_generic_channel_type('Colon', 'Switch', 'Show Colon',
                    update_style=None,
                    description='Turns the colon of the display on or off.'),
        oh_generic_channel_type('Text', 'String', 'Text',
                    update_style=None,
                    description="Text to display on the seven segment display. Supported are A-Z, a-z, 0-9, \\\", (, ), +, -, =, [, ], ^, _ and |. An unsupported character will show as empty. A colon anywhere in the text will light the display's colon on. For example HiTF: will show as Hi:TF on the display."),
    ],
    'actions': [{'fn': 'Set Segments', 'refreshs': ['Segments', 'Colon', 'Brightness']}, 'Get Segments', 'Start Counter', 'Get Counter Value']
}

