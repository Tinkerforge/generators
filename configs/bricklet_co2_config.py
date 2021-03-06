# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# CO2 Bricklet communication config

from generators.configs.commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 262,
    'name': 'CO2',
    'display_name': 'CO2',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures CO2 concentration in ppm',
        'de': 'Misst CO2-Konzentration in ppm'
    },
    'released': True,
    'documented': True,
    'discontinued': True, # replaced by CO2 Bricklet 2.0
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
'name': 'Get CO2 Concentration',
'elements': [('CO2 Concentration', 'uint16', 1, 'out', {'unit': 'Parts Per Million', 'range': (0, 10000)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the measured CO2 concentration.

If you want to get the CO2 concentration periodically, it is recommended to use
the :cb:`CO2 Concentration` callback and set the period with
:func:`Set CO2 Concentration Callback Period`.
""",
'de':
"""
Gibt die gemessene CO2-Konzentration zurück.

Wenn die CO2-Konzentration periodisch abgefragt werden soll, wird empfohlen
den :cb:`CO2 Concentration` Callback zu nutzen und die Periode mit
:func:`Set CO2 Concentration Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set CO2 Concentration Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`CO2 Concentration` callback is
triggered periodically. A value of 0 turns the callback off.

The :cb:`CO2 Concentration` callback is only triggered if the CO2 concentration
has changed since the last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`CO2 Concentration` Callback
ausgelöst wird. Ein Wert von 0 deaktiviert den Callback.

Der :cb:`CO2 Concentration` Callback wird nur ausgelöst, wenn sich die
CO2-Konzentration seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get CO2 Concentration Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set CO2 Concentration Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set CO2 Concentration Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set CO2 Concentration Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'in', {'unit': 'Parts Per Million', 'default': 0}),
             ('Max', 'uint16', 1, 'in', {'unit': 'Parts Per Million', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`CO2 Concentration Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the CO2 concentration is *outside* the min and max values"
 "'i'",    "Callback is triggered when the CO2 concentration is *inside* the min and max values"
 "'<'",    "Callback is triggered when the CO2 concentration is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the CO2 concentration is greater than the min value (max is ignored)"
""",
'de':
"""
Setzt den Schwellwert für den :cb:`CO2 Concentration Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn die CO2-Konzentration *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn die CO2-Konzentration *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn die CO2-Konzentration kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn die CO2-Konzentration größer als der min Wert ist (max wird ignoriert)"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get CO2 Concentration Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'out', {'unit': 'Parts Per Million', 'default': 0}),
             ('Max', 'uint16', 1, 'out', {'unit': 'Parts Per Million', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set CO2 Concentration Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set CO2 Concentration Callback Threshold` gesetzt.
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

* :cb:`CO2 Concentration Reached`,

are triggered, if the thresholds

* :func:`Set CO2 Concentration Callback Threshold`,

keep being reached.
""",
'de':
"""
Setzt die Periode mit welcher die Schwellwert Callbacks

* :cb:`CO2 Concentration Reached`,

ausgelöst werden, wenn die Schwellwerte

* :func:`Set CO2 Concentration Callback Threshold`,

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
'name': 'CO2 Concentration',
'elements': [('CO2 Concentration', 'uint16', 1, 'out', {'unit': 'Parts Per Million', 'range': (0, 10000)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set CO2 Concentration Callback Period`. The :word:`parameter` is the CO2
concentration of the sensor.

The :cb:`CO2 Concentration` callback is only triggered if the CO2 concentration
has changed since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set CO2 Concentration Callback Period`, ausgelöst. Der :word:`parameter`
ist die gemessene CO2-Konzentration des Sensors.

Der :cb:`CO2 Concentration` Callback wird nur ausgelöst, wenn sich die
CO2-Konzentration seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'CO2 Concentration Reached',
'elements': [('CO2 Concentration', 'uint16', 1, 'out', {'unit': 'Parts Per Million', 'range': (0, 10000)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set CO2 Concentration Callback Threshold` is reached.
The :word:`parameter` is the CO2 concentration.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set CO2 Concentration Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die gemessene CO2-Konzentration.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get CO2 Concentration', 'CO2 concentration'), [(('CO2 Concentration', 'CO2 Concentration'), 'uint16', 1, None, 'ppm', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('CO2 Concentration', 'CO2 concentration'), [(('CO2 Concentration', 'CO2 Concentration'), 'uint16', 1, None, 'ppm', None)], None, None),
              ('callback_period', ('CO2 Concentration', 'CO2 concentration'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('CO2 Concentration Reached', 'CO2 concentration reached'), [(('CO2 Concentration', 'CO2 Concentration'), 'uint16', 1, None, 'ppm', None)], None, None),
              ('callback_threshold', ('CO2 Concentration', 'CO2 concentration'), [], '>', [(750, 0)])]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'channels': [
        oh_generic_old_style_channel('CO2 Concentration', 'CO2 Concentration')
    ],
    'channel_types': [
        oh_generic_channel_type('CO2 Concentration', 'Number', {'en': 'CO2 Concentration', 'de': 'CO2-Konzentration'},
                    update_style='Callback Period',
                    description={'en': 'The measured CO2 concentration.',
                                 'de': 'Die gemessene CO2-Konzentration.'})
    ],
    'actions': ['Get CO2 Concentration']
}
