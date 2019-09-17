# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Line Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 241,
    'name': 'Line',
    'display_name': 'Line',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures reflectivity of a surface',
        'de': 'Misst Reflektivität einer Oberfläche'
    },
    'released': True,
    'documented': True,
    'discontinued': False, # selling remaining stock, replaced by Color Bricklet 2.0
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
'name': 'Get Reflectivity',
'elements': [('Reflectivity', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the currently measured reflectivity. The reflectivity is
a value between 0 (not reflective) and 4095 (very reflective).

Usually black has a low reflectivity while white has a high
reflectivity.

If you want to get the reflectivity periodically, it is recommended
to use the :cb:`Reflectivity` callback and set the period with
:func:`Set Reflectivity Callback Period`.
""",
'de':
"""
Gibt die aktuell gemessene Reflektivität zurück. Die Reflektivität
ist ein Wert zwischen 0 (nicht reflektiv) und 4095 (sehr reflektiv).

Normalerweise hat schwarz eine geringe Reflektivität während
weiß eine hohe Reflektivität hat.

Wenn die Reflektivität periodisch abgefragt werden soll, wird empfohlen
den :cb:`Reflectivity` Callback zu nutzen und die Periode mit
:func:`Set Reflectivity Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Reflectivity Callback Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :cb:`Reflectivity` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Reflectivity` callback is only triggered if the reflectivity has
changed since the last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :cb:`Reflectivity` Callback ausgelöst
wird. Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Reflectivity` Callback wird nur ausgelöst, wenn sich die Reflektivität
seit der letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Reflectivity Callback Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Reflectivity Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Reflectivity Callback Period`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Reflectivity Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option'}),
             ('Min', 'uint16', 1, 'in'),
             ('Max', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Reflectivity Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the reflectivity is *outside* the min and max values"
 "'i'",    "Callback is triggered when the reflectivity is *inside* the min and max values"
 "'<'",    "Callback is triggered when the reflectivity is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the reflectivity is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Reflectivity Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn die Reflektivität *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn die Reflektivität *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn die Reflektivität kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn die Reflektivität größer als der min Wert ist (max wird ignoriert)"

Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Reflectivity Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option'}),
             ('Min', 'uint16', 1, 'out'),
             ('Max', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Reflectivity Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Reflectivity Callback Threshold`
gesetzt.
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

* :cb:`Reflectivity Reached`

is triggered, if the threshold

* :func:`Set Reflectivity Callback Threshold`

keeps being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callback

* :cb:`Reflectivity Reached`

ausgelöst wird, wenn der Schwellwert

* :func:`Set Reflectivity Callback Threshold`

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
Gibt die Entprellperiode zurück, wie von :func:`Set Debounce Period`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Reflectivity',
'elements': [('Reflectivity', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Reflectivity Callback Period`. The :word:`parameter` is the
reflectivity of the sensor.

The :cb:`Reflectivity` callback is only triggered if the reflectivity has
changed since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Reflectivity Callback Period`,
ausgelöst. Der :word:`parameter` ist die Reflektivität des Sensors.

Der :cb:`Reflectivity` Callback wird nur ausgelöst, wenn sich die Reflektivität
seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Reflectivity Reached',
'elements': [('Reflectivity', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Reflectivity Callback Threshold` is reached.
The :word:`parameter` is the reflectivity of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Reflectivity Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Reflektivität des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Reflectivity', 'reflectivity'), [(('Reflectivity', 'Reflectivity'), 'uint16', 1, None, None, None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Reflectivity', 'reflectivity'), [(('Reflectivity', 'Reflectivity'), 'uint16', 1, None, None, None)], None, None),
              ('callback_period', ('Reflectivity', 'reflectivity'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 1000),
              ('callback', ('Reflectivity Reached', 'reflectivity reached'), [(('Reflectivity', 'Reflectivity'), 'uint16', 1, None, None, None)], None, None),
              ('callback_threshold', ('Reflectivity', 'reflectivity'), [], '>', [(2000, 0)])]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.OnOffType'],
    'param_groups': oh_generic_channel_param_groups(),
    'channels': [
        oh_generic_old_style_channel('Reflectivity', 'Reflectivity', 'SmartHomeUnits.ONE'),
    ],
    'channel_types': [
        oh_generic_channel_type('Reflectivity', 'Number:Dimensionless', 'Reflectivity',
                     description='The currently measured reflectivity. The reflectivity is a value between 0 (not reflective) and 4095 (very reflective).<br/><br/>Usually black has a low reflectivity while white has a high reflectivity.',
                     read_only=True,
                     pattern='%d',
                     min_=0,
                     max_=4095),
    ]
}
