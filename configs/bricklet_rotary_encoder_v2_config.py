# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Rotary Encoder Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'api_version_extra': 1, # +1 for "Fix min/max types in add_callback_value_function logic [aff5bfc]"
    'category': 'Bricklet',
    'device_identifier': 294,
    'name': 'Rotary Encoder V2',
    'display_name': 'Rotary Encoder 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '360° rotary encoder with push-button',
        'de': '360° Drehgeber/Drehencoder mit Taster'
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

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

count_doc = {
'en':
"""
Returns the current count of the encoder. If you set reset
to true, the count is set back to 0 directly after the
current count is read.

The encoder has 24 steps per rotation.

Turning the encoder to the left decrements the counter,
so a negative count is possible.
""",
'de':
"""
Gibt den aktuellen Zählerwert des Encoders zurück. Wenn
reset auf true gesetzt wird, wird der Zählerstand
direkt nach dem auslesen auf 0 zurück gesetzt.

Der Encoder hat 24 Schritte pro Umdrehung.

Wenn der Encoder nach links gedreht wird wird der Zählerwert
dekrementiert, d.h. negative Zählerwerte sind möglich.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Count',
    data_name = 'Count',
    data_type = 'int32',
    doc       = count_doc
)

com['packets'][0]['elements'].insert(0, ('Reset', 'bool', 1, 'in'))

com['packets'].append({
'type': 'function',
'name': 'Is Pressed',
'elements': [('Pressed', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns *true* if the button is pressed and *false* otherwise.

It is recommended to use the :cb:`Pressed` and :cb:`Released` callbacks
to handle the button.
""",
'de':
"""
Gibt *true* zurück wenn der Taster gedrückt ist und sonst *false*.

Es wird empfohlen die :cb:`Pressed` und :cb:`Released` Callbacks
zu nutzen, um den Taster programmatisch zu behandeln.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Pressed',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the button is pressed.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Taster gedrückt wird.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Released',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the button is released.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Taster losgelassen wird.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Count', 'count without reset'), [(('Count', 'Count'), 'int32', 1, None, None, None)], [('bool', False)])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Count', 'count'), [(('Count', 'Count'), 'int32', 1, None, None, None)], None, None),
              ('callback_configuration', ('Count', 'count'), [], 1000, False, 'x', [(0, 0)])]
})
