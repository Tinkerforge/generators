# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# RGB LED Matrix Bricklet communication config

from generators.configs.openhab_commonconfig import *

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
    'released': True,
    'documented': True,
    'discontinued': True, # currently no replacement available
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
'name': 'Set Red',
'elements': [('Red', 'uint8', 64, 'in', {})],
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
'elements': [('Red', 'uint8', 64, 'out', {'default': [0] * 64})],
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
'elements': [('Green', 'uint8', 64, 'in', {'default': [0] * 64})],
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
'elements': [('Green', 'uint8', 64, 'out', {'default': [0] * 64})],
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
'elements': [('Blue', 'uint8', 64, 'in', {'default': [0] * 64})],
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
'elements': [('Blue', 'uint8', 64, 'out', {'default': [0] * 64})],
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
'elements': [('Frame Duration', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the frame duration.

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
""",
'de':
"""
Setzt die *Frame Duration* (Dauer des Frames).

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
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Frame Duration',
'elements': [('Frame Duration', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the frame duration as set by :func:`Set Frame Duration`.
""",
'de':
"""
Gibt die *Frame Duration* (Dauer des Frames) zurück, wie von
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
'elements': [('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the current supply voltage of the Bricklet.
""",
'de':
"""
Gibt die aktuelle Versorgungsspannung des Bricklets zurück.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Frame Started',
'elements': [('Frame Number', 'uint32', 1, 'out', {})],
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


com['openhab'] = {
    'imports': oh_generic_channel_imports() + oh_generic_trigger_channel_imports() + ['org.eclipse.smarthome.core.library.types.StringType'],
    'param_groups': oh_generic_channel_param_groups(),
    'init_code': """this.setFrameDuration(cfg.frameDuration);""",
    'params': [ {
            'packet': 'Set Frame Duration',
            'element': 'Frame Duration',

            'name': 'Frame Duration',
            'type': 'integer',
            'label': 'Frame Duration',
            'description': 'The frame duration in milliseconds. This configures how fast the Frame Started Channel will trigger. 0 disables the callback.'
        }],
    'channels': [{
            'id': 'Frame Started',
            'label': 'Frame Started',
            'description': 'This channel is triggered directly after a new frame render is started. You should send the data for the next frame directly after this listener was triggered.',
            'type': 'system.trigger',

            'callbacks': [{
                'packet': 'Frame Started',
                'transform': '""'}],
        }, {
            'id': 'LED Values',
            'type': 'LED Values',
            'setters': [{
                    'packet': 'Set Red',
                    'element': 'Red',
                    'packet_params': ['Helper.parseLEDMatrixValues(cmd.toString(), 0, logger)'],
                    'command_type': "StringType"
                }, {
                    'packet': 'Set Green',
                    'element': 'Green',
                    'packet_params': ['Helper.parseLEDMatrixValues(cmd.toString(), 1, logger)'],
                    'command_type': "StringType"
                }, {
                    'packet': 'Set Blue',
                    'element': 'Blue',
                    'packet_params': ['Helper.parseLEDMatrixValues(cmd.toString(), 2, logger)'],
                    'command_type': "StringType"
                }
            ],
        },
    ],
    'channel_types': [
        oh_generic_channel_type('LED Values', 'String', 'LED Values',
                    update_style=None,
                    description="The RGB(W) values for the LEDs.\n\nCommand format is a ','-separated list of integers. The first integer is the index of the first LED to set, additional integers are the values to set. Values are between 0 (off) and 255 (on). If the channel mapping has 3 colors, you need to give the data in the sequence R,G,B,R,G,B,R,G,B,... if the channel mapping has 4 colors you need to give data in the sequence R,G,B,W,R,G,B,W,R,G,B,W...\n\nThe data is double buffered and the colors will be transfered to the LEDs when the next frame duration ends. You can set at most 2048 RGB values or 1536 RGBW values.\n\n For example sending 2,255,0,0,0,255,0,0,0,255 will set the LED 2 to red, LED 3 to green and LED 4 to blue.")
    ],
    'actions': ['Get Red', 'Get Green', 'Get Blue', 'Set Red', 'Set Green', 'Set Blue', 'Get Frame Duration', 'Draw Frame', 'Get Supply Voltage']
}
