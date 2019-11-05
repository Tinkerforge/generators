# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Moisture Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 232,
    'name': 'Moisture',
    'display_name': 'Moisture',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures soil moisture',
        'de': 'Misst Erdfeuchtigkeit'
    },
    'released': True,
    'documented': True,
    'discontinued': True, # currently no replacement available
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
'name': 'Get Moisture Value',
'elements': [('Moisture', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current moisture value. The value has a range of
0 to 4095. A small value corresponds to little moisture, a big
value corresponds to much moisture.

If you want to get the moisture value periodically, it is recommended
to use the :cb:`Moisture` callback and set the period with
:func:`Set Moisture Callback Period`.
""",
'de':
"""
Gibt den aktuellen Feuchtigkeitswert zurück. Der Wert hat einen
Wertebereich von 0 bis 4095. Ein kleiner Wert entspricht einer
geringen Feuchtigkeit, ein großer Wert entspricht einer hohen
Feuchtigkeit.

Wenn der Feuchtigkeitswert periodisch abgefragt werden soll, wird empfohlen
den :cb:`Moisture` Callback zu nutzen und die Periode mit
:func:`Set Moisture Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Moisture Callback Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :cb:`Moisture` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Moisture` callback is only triggered if the moisture value has changed
since the last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :cb:`Moisture` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Moisture` Callback wird nur ausgelöst, wenn sich der Feuchtigkeitswert
seit der letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Moisture Callback Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Moisture Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Moisture Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Moisture Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'in'),
             ('Max', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Moisture Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the moisture value is *outside* the min and max values"
 "'i'",    "Callback is triggered when the moisture value is *inside* the min and max values"
 "'<'",    "Callback is triggered when the moisture value is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the moisture value is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Moisture Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn der Feuchtigkeitswert *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn der Feuchtigkeitswert *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn der Feuchtigkeitswert kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn der Feuchtigkeitswert größer als der min Wert ist (max wird ignoriert)"

Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Moisture Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'out'),
             ('Max', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Moisture Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Moisture Callback Threshold` gesetzt.
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

* :cb:`Moisture Reached`

is triggered, if the threshold

* :func:`Set Moisture Callback Threshold`

keeps being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callback

* :cb:`Moisture Reached`

ausgelöst wird, wenn der Schwellwert

* :func:`Set Moisture Callback Threshold`

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
'name': 'Moisture',
'elements': [('Moisture', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Moisture Callback Period`. The :word:`parameter` is the
moisture value of the sensor.

The :cb:`Moisture` callback is only triggered if the moisture value has changed
since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Moisture Callback Period`,
ausgelöst. Der :word:`parameter` ist der Feuchtigkeitswert des Sensors.

The :cb:`Moisture` Callback wird nur ausgelöst, wenn sich der Feuchtigkeitswert
seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Moisture Reached',
'elements': [('Moisture', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Moisture Callback Threshold` is reached.
The :word:`parameter` is the moisture value of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Moisture Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Feuchtigkeitswert des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Moving Average',
'elements': [('Average', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
for the moisture value.

Setting the length to 0 will turn the averaging completely off. With less
averaging, there is more noise on the data.

The range for the averaging is 0-100.

The default value is 100.
""",
'de':
"""
Setzt die Länge eines `gleitenden Mittelwerts <https://de.wikipedia.org/wiki/Gleitender_Mittelwert>`__
für den Feuchtigkeitswert.

Wenn die Länge auf 0 gesetzt wird, ist das Averaging komplett aus. Desto kleiner
die Länge des Mittelwerts ist, desto mehr Rauschen ist auf den Daten.

Der Wertebereich liegt bei 0-100.

Der Standardwert ist 100.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Moving Average',
'elements': [('Average', 'uint8', 1, 'out')],
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
'functions': [('getter', ('Get Moisture Value', 'moisture value'), [(('Moisture', 'Moisture Value'), 'uint16', 1, None, None, None)], [])]
})

com['examples'].append({
'name': 'Callback',
# FIXME: name mismatch here because of a naming inconsistency in the API
'functions': [('callback', ('Moisture', 'moisture value'), [(('Moisture', 'Moisture Value'), 'uint16', 1, None, None, None)], None, None),
              ('callback_period', ('Moisture', 'moisture value'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
# FIXME: name mismatch here because of a naming inconsistency in the API
'functions': [('debounce_period', 1000),
              ('callback', ('Moisture Reached', 'moisture value reached'), [(('Moisture', 'Moisture Value'), 'uint16', 1, None, None, None)], None, None),
              ('callback_threshold', ('Moisture', 'moisture value'), [], '>', [(200, 0)])]
})

moisture_channel = oh_generic_old_style_channel('Moisture', 'Moisture', 'SmartHomeUnits.ONE')
moisture_channel['getters'][0]['packet'] = 'Get Moisture Value'

com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'params': [{
        'name': 'Moving Average Length',
        'type': 'integer',
        'default': 100,
        'min': 0,
        'max': 100,

        'label': 'Moving Average Length',
        'description': 'The length of a moving averaging for the moisture value.<br/><br/>Setting the length to 0 will turn the averaging off. With less averaging, there is more noise on the data.'

    }],
    'init_code': """this.setMovingAverage(cfg.movingAverageLength.shortValue());""",
    'channels': [
        moisture_channel
    ],
    'channel_types': [
        oh_generic_channel_type('Moisture', 'Number:Dimensionless', 'Moisture',
                    description='The current moisture value. The value has a range of 0 to 4095. A small value corresponds to little moisture, a big value corresponds to much moisture.',
                    read_only=True,
                    pattern='%d',
                    min_=0,
                    max_=4095)
    ],
    'actions': ['Get Moisture Value', 'Get Moving Average']
}
