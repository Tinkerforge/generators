# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Linear Poti Bricklet communication config

from generators.configs.commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'api_version_extra': 1, # +1 for "Break API to fix threshold min/max type mismatch [59d13f6]"
    'category': 'Bricklet',
    'device_identifier': 213,
    'name': 'Linear Poti',
    'display_name': 'Linear Poti',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '59mm linear potentiometer',
        'de': '59mm Linearpotentiometer'
    },
    'released': True,
    'documented': True,
    'discontinued': False, # selling remaining stock, replaced by Linear Poti Bricklet 2.0
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
'name': 'Get Position',
'elements': [('Position', 'uint16', 1, 'out', {'range': (0, 100)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the position of the linear potentiometer. The value is
between 0 (slider down) and 100 (slider up).

If you want to get the position periodically, it is recommended to use the
:cb:`Position` callback and set the period with
:func:`Set Position Callback Period`.
""",
'de':
"""
Gibt die Position des Linearpotentiometers zurück. Der Wertebereich
ist von 0 (Schieberegler unten) und 100 (Schieberegler oben).

Wenn die Position periodisch abgefragt werden soll, wird empfohlen
den :cb:`Position` Callback zu nutzen und die Periode mit
:func:`Set Position Callback Period` vorzugeben.
"""
}]
})

analog_value_desc = """
Returns the value as read by a 12-bit analog-to-digital converter.

.. note::
 The value returned by :func:`Get Position` is averaged over several samples
 to yield less noise, while :func:`Get Analog Value` gives back raw
 unfiltered analog values. The only reason to use :func:`Get Analog Value` is,
 if you need the full resolution of the analog-to-digital converter.
"""

com['packets'].append({
'type': 'function',
'name': 'Get Analog Value',
'elements': [('Value', 'uint16', 1, 'out', {'range': (0, 4095)})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
analog_value_desc + """
If you want the analog value periodically, it is recommended to use the
:cb:`Analog Value` callback and set the period with
:func:`Set Analog Value Callback Period`.
""",
'de':
"""
Gibt den Wert, wie vom 12-Bit Analog-Digital-Wandler gelesen, zurück.

.. note::
 Der von :func:`Get Position` zurückgegebene Wert ist über mehrere
 Messwerte gemittelt um das Rauschen zu vermindern, während :func:`Get Analog Value`
 unverarbeitete Analogwerte zurück gibt. Der einzige Grund :func:`Get Analog Value`
 zu nutzen, ist die volle Auflösung des Analog-Digital-Wandlers zu erhalten.

Wenn der Analogwert periodisch abgefragt werden soll, wird empfohlen
den :cb:`Analog Value` Callback zu nutzen und die Periode mit
:func:`Set Analog Value Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Position Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Position` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Position` callback is only triggered if the position has changed
since the last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Position` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Position` Callback wird nur ausgelöst, wenn sich die Position seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Position Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Position Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Position Callback Period` gesetzt.
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
Setzt die Periode mit welcher der :cb:`Analog Value` Callback ausgelöst
wird. Ein Wert von 0 deaktiviert den Callback.

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
'name': 'Set Position Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'in', {'default': 0}),
             ('Max', 'uint16', 1, 'in', {'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Position Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the position is *outside* the min and max values"
 "'i'",    "Callback is triggered when the position is *inside* the min and max values"
 "'<'",    "Callback is triggered when the position is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the position is greater than the min value (max is ignored)"
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Position Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn die Position *außerhalb* der min und max Werte ist"
 "'i'",    "Callback wird ausgelöst, wenn die Position *innerhalb* der min und max Werte ist"
 "'<'",    "Callback wird ausgelöst, wenn die Position kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn die Position größer als der min Wert ist (max wird ignoriert)"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Position Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'out', {'default': 0}),
             ('Max', 'uint16', 1, 'out', {'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Position Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Position Callback Threshold` gesetzt.
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
 "'o'",    "Callback wird ausgelöst, wenn der Analogwert *außerhalb* der min und max Werte ist"
 "'i'",    "Callback wird ausgelöst, wenn der Analogwert *innerhalb* der min und max Werte ist"
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

* :cb:`Position Reached`,
* :cb:`Analog Value Reached`

are triggered, if the thresholds

* :func:`Set Position Callback Threshold`,
* :func:`Set Analog Value Callback Threshold`

keep being reached.
""",
'de':
"""
Setzt die Periode mit welcher die Schwellwert Callbacks

* :cb:`Position Reached`,
* :cb:`Analog Value Reached`

ausgelöst werden, wenn die Schwellwerte

* :func:`Set Position Callback Threshold`,
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
'name': 'Position',
'elements': [('Position', 'uint16', 1, 'out', {'range': (0, 100)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Position Callback Period`. The :word:`parameter` is the position
of the linear potentiometer.

The :cb:`Position` callback is only triggered if the position has changed
since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Position Callback Period`,
ausgelöst. Der :word:`parameter` ist die Position des Linearpotentiometers.

Der :cb:`Position` Callback wird nur ausgelöst, wenn sich die Position seit der
letzten Auslösung geändert hat.
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
Linear Potentiometer.

The :cb:`Analog Value` callback is only triggered if the position has changed
since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Analog Value Callback Period`,
ausgelöst. Der :word:`parameter` ist der Analogwert des Linearpotentiometers.

Der :cb:`Analog Value` Callback wird nur ausgelöst, wenn sich der Analogwert
seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Position Reached',
'elements': [('Position', 'uint16', 1, 'out', {'range': (0, 100)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Position Callback Threshold` is reached.
The :word:`parameter` is the position of the linear potentiometer.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Position Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Position des Linearpotentiometers.

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
The :word:`parameter` is the analog value of the linear potentiometer.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Analog Value Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist der Analogwert des Linearpotentiometers.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Position', 'position'), [(('Position', 'Position'), 'uint16', 1, None, None, (0, 100))], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Position', 'position'), [(('Position', 'Position'), 'uint16', 1, None, None, (0, 100))], None, None),
              ('callback_period', ('Position', 'position'), [], 50)]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'channels': [
        oh_generic_old_style_channel('Position', 'Position'),
        oh_analog_value_channel()
    ],
    'channel_types': [
        oh_generic_channel_type('Position', 'Number', 'Position',
                    update_style='Callback Period',
                    description='The position of the linear potentiometer. The value is between 0 (slider down) and 100 (slider up).'),
        oh_analog_value_channel_type(analog_value_desc)
    ],
    'actions': ['Get Position', 'Get Analog Value']
}
