# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Ambient Light Bricklet communication config

from generators.configs.commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'api_version_extra': 1, # +1 for "Break API to fix threshold min/max type mismatch [59d13f6]"
    'category': 'Bricklet',
    'device_identifier': 21,
    'name': 'Ambient Light',
    'display_name': 'Ambient Light',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures ambient light up to 900lux',
        'de': 'Misst Umgebungslicht bis zu 900Lux'
    },
    'released': True,
    'documented': True,
    'discontinued': True, # replaced by Ambient Light Bricklet 3.0
    'features': [
        'device',
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

com['packets'].append({
'type': 'function',
'name': 'Get Illuminance',
'elements': [('Illuminance', 'uint16', 1, 'out', {'scale': (1, 10), 'unit': 'Lux', 'range': (0, 9000)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the illuminance of the ambient light sensor.

If you want to get the illuminance periodically, it is recommended to use the
:cb:`Illuminance` callback and set the period with
:func:`Set Illuminance Callback Period`.
""",
'de':
"""
Gibt die Beleuchtungsstärke des Umgebungslichtsensors zurück.

Wenn die Beleuchtungsstärke periodisch abgefragt werden soll, wird empfohlen
den :cb:`Illuminance` Callback zu nutzen und die Periode mit
:func:`Set Illuminance Callback Period` vorzugeben.
"""
}]
})

analog_value_desc = """
Returns the value as read by a 12-bit analog-to-digital converter.

.. note::
 The value returned by :func:`Get Illuminance` is averaged over several samples
 to yield less noise, while :func:`Get Analog Value` gives back raw
 unfiltered analog values. The only reason to use :func:`Get Analog Value` is,
 if you need the full resolution of the analog-to-digital converter.

 Also, the analog-to-digital converter covers three different ranges that are
 set dynamically depending on the light intensity. It is impossible to
 distinguish between these ranges with the analog value.
"""

com['packets'].append({
'type': 'function',
'name': 'Get Analog Value',
'elements': [('Value', 'uint16', 1, 'out', {'range': (0, 4095)})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en': analog_value_desc + """
If you want the analog value periodically, it is recommended to use the
:cb:`Analog Value` callback and set the period with
:func:`Set Analog Value Callback Period`.
""",
'de':
"""
Gibt den Wert, wie vom 12-Bit Analog-Digital-Wandler gelesen, zurück.

.. note::
 Der von :func:`Get Illuminance` zurückgegebene Wert ist über mehrere
 Messwerte gemittelt um das Rauschen zu vermindern, während :func:`Get Analog Value`
 unverarbeitete Analogwerte zurück gibt. Der einzige Grund :func:`Get Analog Value`
 zu nutzen, ist die volle Auflösung des Analog-Digital-Wandlers zu erhalten.

 Weiterhin deckt der Analog-Digital-Wandler drei unterschiedliche Bereiche ab,
 welche dynamisch gewechselt werden abhängig von der Lichtintensität. Es ist
 nicht möglich, anhand der Analogwerte, zwischen diesen Bereichen zu unterscheiden.

Wenn der Analogwert periodisch abgefragt werden soll, wird empfohlen
den :cb:`Analog Value` Callback zu nutzen und die Periode mit
:func:`Set Analog Value Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Illuminance Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Illuminance` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Illuminance` callback is only triggered if the illuminance has changed
since the last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Illuminance` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Illuminance` Callback wird nur ausgelöst, wenn sich die
Beleuchtungsstärke seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Illuminance Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Illuminance Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Illuminance Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Analog Value Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Analog Value` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Analog Value` callback is only triggered if the analog value has
changed since the last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Analog Value` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Analog Value` Callback wird nur ausgelöst, wenn sich der Analogwert
seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Analog Value Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Analog Value Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Analog Value Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Illuminance Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'in', {'scale': (1, 10), 'unit': 'Lux', 'default': 0}),
             ('Max', 'uint16', 1, 'in', {'scale': (1, 10), 'unit': 'Lux', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Illuminance Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the illuminance is *outside* the min and max values"
 "'i'",    "Callback is triggered when the illuminance is *inside* the min and max values"
 "'<'",    "Callback is triggered when the illuminance is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the illuminance is greater than the min value (max is ignored)"
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Illuminance Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn die Beleuchtungsstärke *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn die Beleuchtungsstärke *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn die Beleuchtungsstärke kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn die Beleuchtungsstärke größer als der min Wert ist (max wird ignoriert)"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Illuminance Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'out', {'scale': (1, 10), 'unit': 'Lux', 'default': 0}),
             ('Max', 'uint16', 1, 'out', {'scale': (1, 10), 'unit': 'Lux', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Illuminance Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Illuminance Callback Threshold` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Analog Value Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'in', {'default': 0}),
             ('Max', 'uint16', 1, 'in', {'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Analog Value Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the analog value is *outside* the min and max values"
 "'i'",    "Callback is triggered when the analog value is *inside* the min and max values"
 "'<'",    "Callback is triggered when the analog value is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the analog value is greater than the min value (max is ignored)"
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Analog Value Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn der Analogwert *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn der Analogwert *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn der Analogwert kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn der Analogwert größer als der min Wert ist (max wird ignoriert)"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Analog Value Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'out', {'default': 0}),
             ('Max', 'uint16', 1, 'out', {'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Analog Value Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Analog Value Callback Threshold` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Debounce Period',
'elements': [('Debounce', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 100})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the threshold callbacks

* :cb:`Illuminance Reached`,
* :cb:`Analog Value Reached`

are triggered, if the thresholds

* :func:`Set Illuminance Callback Threshold`,
* :func:`Set Analog Value Callback Threshold`

keep being reached.
""",
'de':
"""
Setzt die Periode mit welcher die Schwellwert Callbacks

* :cb:`Illuminance Reached`,
* :cb:`Analog Value Reached`

ausgelöst werden, wenn die Schwellwerte

* :func:`Set Illuminance Callback Threshold`,
* :func:`Set Analog Value Callback Threshold`

weiterhin erreicht bleiben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Debounce Period',
'elements': [('Debounce', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 100})],
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
'name': 'Illuminance',
'elements': [('Illuminance', 'uint16', 1, 'out', {'scale': (1, 10), 'unit': 'Lux', 'range': (0, 9000)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Illuminance Callback Period`. The :word:`parameter` is the illuminance of the
ambient light sensor.

The :cb:`Illuminance` callback is only triggered if the illuminance has changed
since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Illuminance Callback Period`,
ausgelöst. Der :word:`parameter` ist die Beleuchtungsstärke des Umgebungslichtsensors.

Der :cb:`Illuminance` Callback wird nur ausgelöst, wenn sich die
Beleuchtungsstärke seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Analog Value',
'elements': [('Value', 'uint16', 1, 'out', {'range': (0, 4095)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Analog Value Callback Period`. The :word:`parameter` is the analog value of the
ambient light sensor.

The :cb:`Analog Value` callback is only triggered if the analog value has
changed since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Analog Value Callback Period`,
ausgelöst. Der :word:`parameter` ist der Analogwert des Umgebungslichtsensors.

Der :cb:`Analog Value` Callback wird nur ausgelöst, wenn sich der Analogwert seit
der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Illuminance Reached',
'elements': [('Illuminance', 'uint16', 1, 'out', {'scale': (1, 10), 'unit': 'Lux', 'range': (0, 9000)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Illuminance Callback Threshold` is reached.
The :word:`parameter` is the illuminance of the ambient light sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Illuminance Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Beleuchtungsstärke des Umgebungslichtsensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Analog Value Reached',
'elements': [('Value', 'uint16', 1, 'out', {'range': (0, 4095)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Analog Value Callback Threshold` is reached.
The :word:`parameter` is the analog value of the ambient light sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Analog Value Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist der Analogwert des Umgebungslichtsensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Illuminance', 'illuminance'), [(('Illuminance', 'Illuminance'), 'uint16', 1, 10.0, 'lx', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Illuminance', 'illuminance'), [(('Illuminance', 'Illuminance'), 'uint16', 1, 10.0, 'lx', None)], None, None),
              ('callback_period', ('Illuminance', 'illuminance'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('Illuminance Reached', 'illuminance reached'), [(('Illuminance', 'Illuminance'), 'uint16', 1, 10.0, 'lx', None)], None, 'Too bright, close the curtains!'),
              ('callback_threshold', ('Illuminance', 'illuminance'), [], '>', [(200, 0)])]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'channels': [
        oh_generic_old_style_channel('Illuminance', 'Illuminance'),
        oh_analog_value_channel()
    ],
    'channel_types': [
        oh_generic_channel_type('Illuminance', 'Number', {'en': 'Illuminance', 'de': 'Beleuchtungsstärke'},
                    update_style='Callback Period',
                    description={'en': 'The illuminance of the ambient light sensor.',
                                 'de': 'Die Beleuchtungsstärke des Umgebungslichtsensors.'}),
        oh_analog_value_channel_type(analog_value_desc)
    ],
    'actions': ['Get Illuminance', 'Get Analog Value']
}
