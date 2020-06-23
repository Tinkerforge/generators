# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Hall Effect Bricklet 2.0 communication config

from generators.configs.commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from generators.configs.commonconstants import add_callback_value_function

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2132,
    'name': 'Hall Effect V2',
    'display_name': 'Hall Effect 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures magnetic flux density between -7mT and +7mT',
        'de': 'Misst magnetische Flussdichte zwischen -7mT und +7mT'
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

magnetic_flux_density_doc = {
'en':
"""
Returns the `magnetic flux density (magnetic induction) <https://en.wikipedia.org/wiki/Magnetic_flux>`__.
""",
'de':
"""
Gibt die `magnetische Flussdichte (magnetische Induktion) <https://de.wikipedia.org/wiki/Magnetische_Flussdichte>`__ zurück.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Magnetic Flux Density',
    data_name = 'Magnetic Flux Density',
    data_type = 'int16',
    doc       = magnetic_flux_density_doc,
    scale     = (1, 10**6),
    unit      = 'Tesla',
    range_    = (-7000, 7000)
)

com['packets'].append({
'type': 'function',
'name': 'Get Counter',
'elements': [('Reset Counter', 'bool', 1, 'in', {}),
             ('Count', 'uint32', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current value of the counter.

You can configure the low/high thresholds and the debounce time
with :func:`Set Counter Config`.

If you set reset counter to *true*, the count is set back to 0
directly after it is read.

If you want to get the count periodically, it is recommended to use the
:cb:`Counter` callback. You can set the callback configuration
with :func:`Set Counter Callback Configuration`.
""",
'de':
"""
Gibt den aktuellen Wert des Zählers zurück.

Die Schwellwerte (low/high) und Entprellzeit können per
:func:`Set Counter Config` eingestellt werden.

Wenn reset counter auf *true* gesetzt wird, wird der Zählerstand direkt
nach dem Auslesen auf 0 zurückgesetzt.

Wenn der Zähler periodisch benötigt wird, kann auch der :cb:`Counter` Callback
verwendet werden. Der Callback wird mit der Funktion
:func:`Set Counter Callback Configuration` konfiguriert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Counter Config',
'elements': [('High Threshold', 'int16', 1, 'in', {'scale': (1, 10**6), 'unit': 'Tesla', 'default': 2000}),
             ('Low Threshold', 'int16', 1, 'in', {'scale': (1, 10**6), 'unit': 'Tesla', 'default': -2000}),
             ('Debounce', 'uint32', 1, 'in', {'scale': (1, 10**6), 'unit': 'Second', 'range': (0, 10**6), 'default': 10**5})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets a high and a low threshold as well as a debounce time.

If the measured magnetic flux density goes above the high threshold or
below the low threshold, the count of the counter is increased by 1.

The debounce time is the minimum time between two count increments.
""",
'de':
"""
Setzt einen unteren und einen oberen Schwellwert (threshold) sowie
eine Entprellzeit (debounce).

Wenn die gemessene magnetische Flussdichte über den oberen Schwellwert
oder unter den unteren Schwellwert wandert, wird der Zählerstand des Zählers
(siehe :func:`Get Counter`) um 1 erhöht.

Die Entprellzeit ist die Minimalzeit zwischen zwei Zählererhöhungen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Counter Config',
'elements': [('High Threshold', 'int16', 1, 'out', {'scale': (1, 10**6), 'unit': 'Tesla', 'default': 2000}),
             ('Low Threshold', 'int16', 1, 'out', {'scale': (1, 10**6), 'unit': 'Tesla', 'default': -2000}),
             ('Debounce', 'uint32', 1, 'out', {'scale': (1, 10**6), 'unit': 'Second', 'range': (0, 10**6), 'default': 10**5})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the counter config as set by :func:`Set Counter Config`.
""",
'de':
"""
Gibt die Zähler-Konfiguration zurück, wie von :func:`Set Counter Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Counter Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period is the period with which the :cb:`Counter`
callback is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after at least one of the values has changed. If the values didn't
change within the period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.
""",
'de':
"""
Die Periode ist die Periode mit der der :cb:`Counter`
Callback ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn sich mindestens ein Wert im Vergleich zum letzten mal geändert
hat. Ändert sich kein Wert innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn ein Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen der Werte.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Counter Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set Counter Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set Counter Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Counter',
'elements': [('Count', 'uint32', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set Counter Callback Configuration`.

The count is the same as you would get with :func:`Get Counter`.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set Counter Callback Configuration` gesetzten Konfiguration

Der Zählerstand ist der gleiche, der auch per :func:`Get Counter`
abgefragt werden kann.
"""
}]
})

com['examples'].append({
'name': 'Magnetic Flux Density',
'functions': [('getter', ('Get Magnetic Flux Density', 'Magnetic Flux Density'), [(('Magnetic Flux Density', 'Magnetic Flux Density'), 'int16', 1, None, 'µT', None)], [])]
})

com['examples'].append({
'name': 'Counter',
'functions': [('getter', ('Get Counter', 'count without counter reset'), [(('Count', 'Count'), 'uint32', 1, None, None, None)], [('bool', False)])]
})

com['examples'].append({
'name': 'Counter Callback',
'functions': [('setter', 'Set Counter Config', [('int16', 3000), ('int16', -3000), ('uint32', 10000)], 'Configure counter with ±3000µT threshold and 10ms debounce', None),
              ('callback', ('Counter', 'counter'), [(('Counter', 'Counter'), 'uint32', 1, None, None, None)], None, None),
              ('callback_configuration', ('Counter', 'counter'), [], 100, True, None, [])]
})


com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.OnOffType'],
    'param_groups': oh_generic_channel_param_groups(),
    'params': [{
            'packet': 'Set Counter Config',
            'element': 'Low Threshold',

            'name': 'Low Threshold',
            'type': 'integer',
            'label': 'Low Threshold',
            'description': 'The low threshold in µT. If the measured magnetic flux density goes below the low threshold, the count of the counter is increased by 1.',
        }, {
            'packet': 'Set Counter Config',
            'element': 'High Threshold',

            'name': 'High Threshold',
            'type': 'integer',
            'label': 'High Threshold',
            'description': 'The high threshold in µT. If the measured magnetic flux density goes above the high threshold, the count of the counter is increased by 1.',
        }, {
            'packet': 'Set Counter Config',
            'element': 'Debounce',

            'name': 'Debounce',
            'type': 'integer',
            'label': 'Debounce Time',
            'description': 'The debounce time in µs is the minimum time between two count increments.',
        }],
    'channels': [
        {
            'id': 'Counter',
            'type': 'Counter',
            'label': 'Counter',

            'init_code':"""this.setCounterConfig(cfg.highThreshold, cfg.lowThreshold, cfg.debounce.longValue());
            this.setCounterCallbackConfiguration(channelCfg.updateInterval, true);""",
            'dispose_code': """this.setCounterCallbackConfiguration(0, true);""",

            'getters': [{
                'packet': 'Get Counter',
                'element': 'Count',
                'packet_params': ['channelCfg.resetOnRead'],
                'transform': 'new DecimalType(value)'}],

            'callbacks': [{
                'packet': 'Counter',
                'element': 'Count',
                'transform': 'new DecimalType(count)'
            }],
        },
        oh_generic_channel('Magnetic Flux Density', 'Magnetic Flux Density')
    ],
    'channel_types': [
        oh_generic_channel_type('Counter', 'Number', 'Counter',
                    update_style='Callback Configuration',
                    description='The current value of the counter.',
                    params=[{
                        'packet': 'Get Counter',
                        'element': 'Reset Counter',
                        'name': 'Reset On Read',
                        'type': 'boolean',

                        'default': 'false',

                        'label': 'Reset Counter On Update',
                        'description': 'Enabling this will reset the counter after OpenHAB reads its value. Use this if you want relative counts per update.',
                    }]),
        oh_generic_channel_type('Magnetic Flux Density', 'Number', 'Magnetic Flux Density',
                    update_style='Callback Configuration',
                    description='The measured magnetic flux density.'),
    ],
    'actions': ['Get Magnetic Flux Density', 'Get Counter', 'Get Counter Config']
}
