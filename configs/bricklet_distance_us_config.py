# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Distance US Bricklet communication config

from generators.configs.commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'api_version_extra': 1, # +1 for "Break API to fix threshold min/max type mismatch [59d13f6]"
    'category': 'Bricklet',
    'device_identifier': 229,
    'name': 'Distance US',
    'display_name': 'Distance US',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures distance between 2cm and 400cm with ultrasound',
        'de': 'Misst Entfernung zwischen 2cm und 400cm mit Ultraschall'
    },
    'released': True,
    'documented': True,
    'discontinued': True, # replaced by Distance US Bricklet 2.0
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
'name': 'Get Distance Value',
'elements': [('Distance', 'uint16', 1, 'out', {'range': (0, 4095)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current distance value measured by the sensor.
A small value corresponds to a small distance, a big
value corresponds to a big distance. The relation between the measured distance
value and the actual distance is affected by the 5V supply voltage (deviations
in the supply voltage result in deviations in the distance values) and is
non-linear (resolution is bigger at close range).

If you want to get the distance value periodically, it is recommended to
use the :cb:`Distance` callback and set the period with
:func:`Set Distance Callback Period`.
""",
'de':
"""
Gibt den aktuellen Entfernungswert zurück.
Ein kleiner Wert entspricht einer kleinen
Entfernung, ein großer Wert entspricht einer großen Entfernung. Das Verhältnis
zwischen gemessenem Entfernungswert und wirklicher Entfernung wird durch die
5V Versorgungsspannung beeinflusst (Abweichungen der Versorgungsspannung führen
zu Abweichungen in den Entfernungswerten) und ist nicht-linear (Auflösung ist
größer im Nahbereich).

Wenn der Entfernungswert periodisch abgefragt werden soll, wird empfohlen
den :cb:`Distance` Callback zu nutzen und die Periode mit
:func:`Set Distance Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Distance Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Distance` callback is triggered
periodically. A value of 0 turns the callback off.

Der :cb:`Distance` callback is only triggered if the distance value has changed
since the last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Distance` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Distance` Callback wird nur ausgelöst, wenn sich der Entfernungswert
seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Distance Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Distance Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Distance Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Distance Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'in', {'range': (0, 4095)}),
             ('Max', 'uint16', 1, 'in', {'range': (0, 4095)})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Distance Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the distance value is *outside* the min and max values"
 "'i'",    "Callback is triggered when the distance value is *inside* the min and max values"
 "'<'",    "Callback is triggered when the distance value is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the distance value is greater than the min value (max is ignored)"
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Distance Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn der Entfernungswert *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn der Entfernungswert *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn der Entfernungswert kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn der Entfernungswert größer als der min Wert ist (max wird ignoriert)"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Distance Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'out', {'range': (0, 4095)}),
             ('Max', 'uint16', 1, 'out', {'range': (0, 4095)})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Distance Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Distance Callback Threshold` gesetzt.
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

* :cb:`Distance Reached`,

are triggered, if the thresholds

* :func:`Set Distance Callback Threshold`,

keep being reached.
""",
'de':
"""
Setzt die Periode mit welcher die Schwellwert Callbacks

* :cb:`Distance Reached`,

ausgelöst werden, wenn die Schwellwerte

* :func:`Set Distance Callback Threshold`,

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
'name': 'Distance',
'elements': [('Distance', 'uint16', 1, 'out', {'range': (0, 4095)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Distance Callback Period`. The :word:`parameter` is the distance value
of the sensor.

The :cb:`Distance` callback is only triggered if the distance value has changed
since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Distance Callback Period`,
ausgelöst. Der :word:`parameter` ist die Entfernungswert des Sensors.

Der :cb:`Distance` Callback wird nur ausgelöst, wenn sich der Entfernungswert
seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Distance Reached',
'elements': [('Distance', 'uint16', 1, 'out', {'range': (0, 4095)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Distance Callback Threshold` is reached.
The :word:`parameter` is the distance value of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Distance Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist der Entfernungswert des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Moving Average',
'elements': [('Average', 'uint8', 1, 'in', {'range': (0, 100), 'default': 20})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
for the distance value.

Setting the length to 0 will turn the averaging completely off. With less
averaging, there is more noise on the data.
""",
'de':
"""
Setzt die Länge eines `gleitenden Mittelwerts <https://de.wikipedia.org/wiki/Gleitender_Mittelwert>`__
für den Entfernungswert.

Wenn die Länge auf 0 gesetzt wird, ist das Averaging komplett aus. Desto kleiner
die Länge des Mittelwerts ist, desto mehr Rauschen ist auf den Daten.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Moving Average',
'elements': [('Average', 'uint8', 1, 'out', {'range': (0, 100), 'default': 20})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the length moving average as set by :func:`Set Moving Average`.
""",
'de':
"""
Gibt die Länge des gleitenden Mittelwerts zurück, wie von
:func:`Set Moving Average` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
# FIXME: name mismatch here because of a naming inconsistency in the API
'functions': [('getter', ('Get Distance Value', 'distance value'), [(('Distance', 'Distance Value'), 'uint16', 1, None, None, None)], [])]
})

com['examples'].append({
'name': 'Callback',
# FIXME: name mismatch here because of a naming inconsistency in the API
'functions': [('callback', ('Distance', 'distance value'), [(('Distance', 'Distance Value'), 'uint16', 1, None, None, None)], None, None),
              ('callback_period', ('Distance', 'distance value'), [], 200)]
})

com['examples'].append({
'name': 'Threshold',
# FIXME: name mismatch here because of a naming inconsistency in the API
'functions': [('debounce_period', 10000),
              ('callback', ('Distance Reached', 'distance value reached'), [(('Distance', 'Distance Value'), 'uint16', 1, None, None, None)], None, None),
              ('callback_threshold', ('Distance', 'distance value'), [], '<', [(200, 0)])]
})

distance_channel = oh_generic_old_style_channel('Distance', 'Distance')
distance_channel['getters'][0]['packet'] = 'Get Distance Value'

com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'params': [
        {
            'packet': 'Set Moving Average',
            'element': 'Average',

            'name': 'Moving Average Length',
            'type': 'integer',
            'label': {'en': 'Moving Average Length', 'de': 'Länge des gleitenden Mittelwerts'},
            'description': {'en': 'Sets the length of a moving averaging for the distance value.\n\nSetting the length to 0 will turn the averaging completely off. With less averaging, there is more noise on the data.',
                            'de': 'Setzt die Länge eines gleitenden Mittelwerts für den Entfernungswert.\n\nWenn die Länge auf 0 gesetzt wird, ist das Averaging komplett aus. Desto kleiner die Länge des Mittelwerts ist, desto mehr Rauschen ist auf den Daten.'}
        }
    ],
    'init_code': """this.setMovingAverage(cfg.movingAverageLength.shortValue());""",
    'channels': [
        distance_channel
    ],
    'channel_types': [
        oh_generic_channel_type('Distance', 'Number', {'de': 'Distance', 'en': 'Distanz'},
                    update_style='Callback Period',
                    description={'en': 'The current distance value measured by the sensor. A small value corresponds to a small distance, a big value corresponds to a big distance. The relation between the measured distance value and the actual distance is affected by the 5V supply voltage (deviations in the supply voltage result in deviations in the distance values) and is non-linear (resolution is bigger at close range).',
                                 'de': 'Der aktuelle Entfernungswert. Ein kleiner Wert entspricht einer kleinen Entfernung, ein großer Wert entspricht einer großen Entfernung. Das Verhältnis zwischen gemessenem Entfernungswert und wirklicher Entfernung wird durch die 5V Versorgungsspannung beeinflusst (Abweichungen der Versorgungsspannung führen zu Abweichungen in den Entfernungswerten) und ist nicht-linear (Auflösung ist größer im Nahbereich).'}
        )
    ],
    'actions': ['Get Distance Value', 'Get Moving Average']
}

