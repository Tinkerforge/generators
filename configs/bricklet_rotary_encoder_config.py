# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Rotary Encoder Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 236,
    'name': 'Rotary Encoder',
    'display_name': 'Rotary Encoder',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '360° rotary encoder with push-button',
        'de': '360° Drehgeber/Drehencoder mit Taster'
    },
    'released': True,
    'documented': True,
    'discontinued': True, # replaced by Rotary Encoder Bricklet 2.0
    'features': [
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

com['packets'].append({
'type': 'function',
'name': 'Get Count',
'elements': [('Reset', 'bool', 1, 'in'),
             ('Count', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current count of the encoder. If you set reset
to true, the count is set back to 0 directly after the
current count is read.

The encoder has 24 steps per rotation

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
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Count Callback Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :cb:`Count` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Count` callback is only triggered if the count has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :cb:`Count` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Count` Callback wird nur ausgelöst, wenn sich der Zählerwert seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Count Callback Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Count Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Count Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Count Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'int32', 1, 'in'),
             ('Max', 'int32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Count Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the count is *outside* the min and max values"
 "'i'",    "Callback is triggered when the count is *inside* the min and max values"
 "'<'",    "Callback is triggered when the count is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the count is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Count Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn der Zählerwert *außerhalb* der min und max Werte ist"
 "'i'",    "Callback wird ausgelöst, wenn die Zählerwert *innerhalb* der min und max Werte ist"
 "'<'",    "Callback wird ausgelöst, wenn die Zählerwert kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn die Zählerwert größer als der min Wert ist (max wird ignoriert)"

Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Count Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'int32', 1, 'out'),
             ('Max', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Count Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Count Callback Threshold` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Debounce Period',
'elements': [('Debounce', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the threshold callback

* :cb:`Count Reached`

is triggered, if the thresholds

* :func:`Set Count Callback Threshold`

keeps being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher der Schwellwert-Callback

* :cb:`Count Reached`

ausgelöst wird, wenn der Schwellwert

* :func:`Set Count Callback Threshold`

weiterhin erreicht bleibt.

Der Standardwert ist 100.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Debounce Period',
'elements': [('Debounce', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the debounce period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Gibt die Entprellperiode zurück, wie von :func:`Set Debounce Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Count',
'elements': [('Count', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Count Callback Period`. The :word:`parameter` is the count of
the encoder.

The :cb:`Count` callback is only triggered if the count has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Count Callback Period`, ausgelöst. Der :word:`parameter` ist der
Zählerwert des Encoders.

Der :cb:`Count` Callback wird nur ausgelöst, wenn sich der Zähler seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Count Reached',
'elements': [('Count', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Count Callback Threshold` is reached.
The :word:`parameter` is the count of the encoder.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Count Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist der Zählerwert des Encoders.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

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
Dieser Callback wird ausgelöst, wenn der Taster gedrückt wird.
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
Dieser Callback wird ausgelöst, wenn der Taster losgelassen wird.
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
              ('callback_period', ('Count', 'count'), [], 50)]
})

count_channel = oh_generic_old_style_channel('Count', 'Count', 'SmartHomeUnits.ONE')
count_channel['getters'][0]['packet_params'] = ['false']

com['openhab'] = {
    'imports': oh_generic_channel_imports() + oh_generic_trigger_channel_imports() +['org.eclipse.smarthome.core.library.types.StringType'],
    'param_groups': oh_generic_channel_param_groups(),
    'channels': [
        count_channel,
        {
            'id': 'Reset Counter',
            'type': 'Reset Counter',

            'setters': [{
                'packet': 'Get Count',
                'packet_params': ['true']}],
            'setter_command_type': "StringType", # Command type has to be string type to be able to use command options.
            'setter_refreshs': [{
                'channel': 'Count',
                'delay': '0'
            }]
        },
        {
            'id': 'Pressed',
            'type': 'system.rawbutton',
            'label': 'Pressed',

            'getters': [{
                'packet': 'Is Pressed',
                'transform': "value ? CommonTriggerEvents.PRESSED : CommonTriggerEvents.RELEASED"}],

            'callbacks': [{
                    'packet': 'Pressed',
                    'transform': 'CommonTriggerEvents.PRESSED'
                },{
                    'packet': 'Released',
                    'transform': 'CommonTriggerEvents.RELEASED'
                }],
            'is_trigger_channel': True
        }
    ],
    'channel_types': [
        oh_generic_channel_type('Count', 'Number:Dimensionless', 'Count',
                     description='The current count of the encoder. The encoder has 24 steps per rotation. Turning the encoder to the left decrements the counter, so a negative count is possible.',
                     read_only=True,
                     pattern='%d'),
        {
            'id': 'Reset Counter',
            'item_type': 'String',
            'label': 'Reset Counter',
            'description':'Resets the counter to 0.',
            'command_options': [('Reset', 'RESET')]
        }
    ],
    'actions': ['Get Count', 'Is Pressed']
}
