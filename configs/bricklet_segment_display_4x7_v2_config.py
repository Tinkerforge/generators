# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Segment Display 4x7 Bricklet 2.0 communication config

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2137,
    'name': 'Segment Display 4x7 V2',
    'display_name': 'Segment Display 4x7 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Four 7-segment displays with switchable dots',
        'de': 'Vier 7-Segment-Anzeigen mit schaltbare Punkten'
    },
    'released': True,
    'documented': True,
    'discontinued': False,
    'features': [
        'comcu_bricklet',
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Set Segments',
'elements': [('Digit0', 'bool', 8, 'in'),
             ('Digit1', 'bool', 8, 'in'),
             ('Digit2', 'bool', 8, 'in'),
             ('Digit3', 'bool', 8, 'in'),
             ('Colon', 'bool', 2, 'in'),
             ('Tick', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the segments of the Segment Display 4x7 Bricklet 2.0 segment-by-segment.

The data is split into the four digits, two colon dots and the tick mark.

The indices of the segments in the digit and colon parameters are as follows:

.. image:: /Images/Bricklets/bricklet_segment_display_4x7_v2_segment_index.png
   :scale: 100 %
   :alt: Indices of segments
   :align: center

""",
'de':
"""
Setzt die einzelnen Segmente des Segment Display 4x7 Bricklet 2.0 Segment für Segment.

Die Daten sind aufgeteilt in die vier Ziffern (digit0-3), dem Doppelpunkt (colon) und dem Hochkomma (tick).

Die Indizes der Segmente in den Ziffern und dem Doppelpunkt sind wie folgt aufgeteilt:

.. image:: /Images/Bricklets/bricklet_segment_display_4x7_v2_segment_index.png
   :scale: 100 %
   :alt: Indizes der Segmente
   :align: center

"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Segments',
'elements': [('Digit0', 'bool', 8, 'out'),
             ('Digit1', 'bool', 8, 'out'),
             ('Digit2', 'bool', 8, 'out'),
             ('Digit3', 'bool', 8, 'out'),
             ('Colon', 'bool', 2, 'out'),
             ('Tick', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the segment data as set by :func:`Set Segments`.
""",
'de':
"""
Gibt die Segmentdaten zurück, wie von :func:`Set Segments` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Brightness',
'elements': [('Brightness', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
The brightness can be set between 0 (dark) and 7 (bright).

The default value is 7.
""",
'de':
"""
Die Helligkeit kann zwischen 0 (dunkel) und 7 (hell) gesetzt werden.

Der Standardwert ist 7.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Brightness',
'elements': [('Brightness', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the brightness as set by :func:`Set Brightness`.
""",
'de':
"""
Gibt die Helligkeit zurück, wie von :func:`Set Brightness` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Numeric Value',
'elements': [('Value', 'int8', 4, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets a numeric value for each of the digits. The values can be between
-2 and 15. They represent:

* -2: minus sign
* -1: blank
* 0-9: 0-9
* 10: A
* 11: b
* 12: C
* 13: d
* 14: E
* 15: F

Example: A call with [-2, -1, 4, 2] will result in a display of "- 42".
""",
'de':
"""
Setzt einen numerischen Wert für jede Ziffer. Die Werte können zwischen
-2 und 15 seien. Die Werte repräsentieren:

* -2: Minuszeichen
* -1: Leerstelle
* 0-9: 0-9
* 10: A
* 11: b
* 12: C
* 13: d
* 14: E
* 15: F

Beispiel: Ein Aufruf mit [-2, -1, 4, 2] erzeugt eine Anzeige auf dem Display von "- 42".
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Selected Segment',
'elements': [('Segment', 'uint8', 1, 'in'),
             ('Value', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Turns one specified segment on or off.

The indices of the segments are as follows:

.. image:: /Images/Bricklets/bricklet_segment_display_4x7_v2_selected_segment_index.png
   :scale: 100 %
   :alt: Indices of selected segments
   :align: center

""",
'de':
"""
Aktiviert/deaktiviert ein selektiertes Segment.

Die Indizes sind wie folgt aufgeteilt:

.. image:: /Images/Bricklets/bricklet_segment_display_4x7_v2_selected_segment_index.png
   :scale: 100 %
   :alt: Indizes für einzeln selektierte Segmente
   :align: center

"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Selected Segment',
'elements': [('Segment', 'uint8', 1, 'in'),
             ('Value', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the value of a single segment.
""",
'de':
"""
Gibt den Wert eines einzelnen Segments zurück.
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

Using a negative *increment* allows to count backwards.

You can stop the counter at every time by calling :func:`Set Segments`
or :func:`Set Numeric Value`.
""",
'de':
"""
Starter einen Zähler mit dem *from* Wert der bis zum *to* Wert zählt
mit einer Schrittweite von *increment*. Das Argument *length* gibt die
Pause zwischen den Erhöhungen in ms an.

Beispiel: Wenn *from* auf 0, *to* auf 100, *increment* auf 1 und
*length* auf 1000 gesetzt wird, wird ein Zähler gestartet der von
0 bis 100 zählt mit Rate von einer Sekunde zwischen jeder Erhöhung.

Der Maximalwert für *from*, *to* und *increment* ist 9999, der Minimalwert
ist -999.

Wenn *increment* negativ ist läuft der Zähler rückwärts.

Der Zähler kann jederzeit durch einen Aufruf von :func:`Set Segments` oder
:func:`Set Numeric Value` gestoppt werden.
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

Wenn kein Zähler läuft wird eine 0 zurückgegeben.
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
'name': 'Blink Colon',
'functions': [('setter', 'Set Brightness', [('uint8', 7)], None, 'Set to full brightness'),
              ('loop_header', 10, 'Blink colon 10 times'),
              ('setter', 'Set Selected Segment', [('uint8', 32), ('bool', True)], 'Activate segments of colon', None),
              ('setter', 'Set Selected Segment', [('uint8', 33), ('bool', True)], None, None),
              ('empty',),
              ('sleep', 250, None, None),
              ('setter', 'Set Selected Segment', [('uint8', 32), ('bool', False)], 'Deactivate segments of colon', None),
              ('setter', 'Set Selected Segment', [('uint8', 33), ('bool', False)], None, None),
              ('loop_footer',)],
})

com['examples'].append({
'name': 'Numeric Value',
'functions': [('setter', 'Set Brightness', [('uint8', 7)], None, 'Set to full brightness'),
              ('setter', 'Set Numeric Value', [('int8', [-2, -1, 4, 2])], 'Show "- 42" on the Display', None)],
})

com['examples'].append({
'name': 'Set Segments',
'functions': [('setter', 'Set Brightness', [('uint8', 7)], None, 'Set to full brightness'),
              ('setter', 'Set Segments', [('bool', [True]*8), ('bool', [True]*8), ('bool', [True]*8), ('bool', [True]*8), ('bool', [True]*2), ('bool', True)], 'Activate all segments', None)],
})



com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.OnOffType', 'org.eclipse.smarthome.core.library.types.StringType'],

    'param_groups': oh_generic_channel_param_groups(),
    'channels': [{
            'id': 'Brightness',
            'type': 'Brightness',

            'getters': [{
                'packet': 'Get Brightness',
                'transform': 'new QuantityType(value, SmartHomeUnits.ONE)'}],
            'setters': [{
                'packet': 'Set Brightness',
                'packet_params': ['cmd.shortValue()']}],
            'setter_command_type': 'Number'
        }, {
            'id': 'Colon Upper',
            'type': 'Colon Upper',

            'getters': [{
                'packet': 'Get Selected Segment',
                'packet_params': ['32'],
                'transform': 'value ? OnOffType.ON : OnOffType.OFF'}],
            'setters': [{
                'packet': 'Set Selected Segment',
                'packet_params': ['32', 'cmd == OnOffType.ON']}],
            'setter_command_type': 'OnOffType'
        }, {
            'id': 'Colon Lower',
            'type': 'Colon Lower',

            'getters': [{
                'packet': 'Get Selected Segment',
                'packet_params': ['33'],
                'transform': 'value ? OnOffType.ON : OnOffType.OFF'}],
            'setters': [{
                'packet': 'Set Selected Segment',
                'packet_params': ['33', 'cmd == OnOffType.ON']}],
            'setter_command_type': 'OnOffType'
        }, {
            'id': 'Tick',
            'type': 'Tick',

            'getters': [{
                'packet': 'Get Selected Segment',
                'packet_params': ['34'],
                'transform': 'value ? OnOffType.ON : OnOffType.OFF'}],
            'setters': [{
                'packet': 'Set Selected Segment',
                'packet_params': ['34', 'cmd == OnOffType.ON']}],
            'setter_command_type': 'OnOffType'
        }, {
            'id': 'Segments',
            'type': 'Segments',

            'getters': [{
                'packet': 'Get Segments',
                'transform': 'new QuantityType((Helper.bitsToLong(value.digit0) << 24) | (Helper.bitsToLong(value.digit0) << 16) | (Helper.bitsToLong(value.digit0) << 8) | Helper.bitsToLong(value.digit0), SmartHomeUnits.ONE)'
            }],
            'setters': [{
                'packet': 'Set Segments',
                'packet_params': [
                    'Helper.shortToBits((short)(cmd.intValue() >> 24))',
                    'Helper.shortToBits((short)(cmd.intValue() >> 16))',
                    'Helper.shortToBits((short)(cmd.intValue() >> 8))',
                    'Helper.shortToBits((short)cmd.intValue())',
                    'this.getSegments().colon',
                    'this.getSegments().tick',
                ]
            }],
            'setter_command_type': 'Number'
        },  {
            'id': 'Text',
            'type': 'Text',

            'setters': [{
                'packet': 'Set Segments',
                'packet_params': ['Helper.parseSegmentDisplay2TextDigit(cmd.toString(), 0)',
                                  'Helper.parseSegmentDisplay2TextDigit(cmd.toString(), 1)',
                                  'Helper.parseSegmentDisplay2TextDigit(cmd.toString(), 2)',
                                  'Helper.parseSegmentDisplay2TextDigit(cmd.toString(), 3)',
                                  'new boolean[]{cmd.toString().contains("`") || cmd.toString().contains(":"), cmd.toString().contains(",") || cmd.toString().contains(":")}',
                                  'cmd.toString().contains("\'")']
            }],
            'setter_refreshs': [
                {'channel': 'Segments', 'delay': '0'},
                {'channel': 'Colon Upper', 'delay': '0'},
                {'channel': 'Colon Lower', 'delay': '0'},
                {'channel': 'Tick', 'delay': '0'},
            ],
            'setter_command_type': 'StringType'
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
                      description='The seven segment display can be set with bitmaps. Every bit controls one segment as shown <a href=https://www.tinkerforge.com/en/doc/_images/bricklet_segment_display_4x7_bit_order.png>here</a>. The channel accepts an integer, that is split into 4 bytes, controlling one segment each. For example 1717263183, which is 0x665b5b4f in hex will be split into 0x66 for the first segment, 0x5b for the second, 0x5b for the third and 0x4f for the fourth.',
                      pattern='%d'),
        oh_generic_channel_type('Colon Upper', 'Switch', 'Show Upper Colon Dot',
                     description='Turns the colon of the display on or off.'),
        oh_generic_channel_type('Colon Lower', 'Switch', 'Show Lower Colon Dot',
                     description='Turns the colon of the display on or off.'),
        oh_generic_channel_type('Tick', 'Switch', 'Show Tick',
                     description='Turns the colon of the display on or off.'),
        oh_generic_channel_type('Text', 'String', 'Text',
                     description="Text to display on the seven segment display. Supported are A-Z, a-z, 0-9, \\\", (, ), +, -, =, [, ], ^, _ and |. An unsupported character will show as empty. A colon (:) anywhere in the text will light on the display's colon. Alternatively, you can enable only the upper colon dot with a backtick (`) or the lower one with a comma (,). An apostrophe (') anywhere will light up the tick after the third digit. A dot (.) after another character will light the corresponding digit's dot. For example H.i,T.'F will show HiTF on the display and activate the first and third dot, lower colon dot and the tick."),
    ],
    'actions': ['Get Segments', 'Get Brightness', 'Get Selected Segment', 'Start Counter', 'Get Counter Value']
}

