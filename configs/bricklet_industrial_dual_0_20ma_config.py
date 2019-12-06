# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Dual 0-20mA Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 228,
    'name': 'Industrial Dual 0 20mA',
    'display_name': 'Industrial Dual 0-20mA',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures two DC currents between 0mA and 20mA (IEC 60381-1)',
        'de': 'Misst zwei Gleichströme zwischen 0mA und 20mA (IEC 60381-1)'
    },
    'released': True,
    'documented': True,
    'discontinued': False, # selling remaining stock, replaced by Industrial Dual 0-20mA Bricklet 2.0
    'features': [
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

com['constant_groups'].append({
'name': 'Sample Rate',
'type': 'uint8',
'constants': [('240 SPS', 0),
              ('60 SPS', 1),
              ('15 SPS', 2),
              ('4 SPS', 3)]
})

com['packets'].append({
'type': 'function',
'name': 'Get Current',
'elements': [('Sensor', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Current', 'int32', 1, 'out', {'scale': (1, 10**9), 'unit': 'Ampere', 'range': (0, 22505322)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current of the specified sensor.

It is possible to detect if an IEC 60381-1 compatible sensor is connected
and if it works properly.

If the returned current is below 4mA, there is likely no sensor connected
or the sensor may be defect. If the returned current is over 20mA, there might
be a short circuit or the sensor may be defect.

If you want to get the current periodically, it is recommended to use the
:cb:`Current` callback and set the period with
:func:`Set Current Callback Period`.
""",
'de':
"""
Gibt die gemessenen Stromstärke des angegebenen Sensors zurück.

Es ist möglich zu erkennen ob ein IEC 60381-1-kompatibler Sensor angeschlossen
ist und ob er funktionsfähig ist.

Falls die zurückgegebene Stromstärke kleiner als 4mA ist, ist wahrscheinlich
kein Sensor angeschlossen oder der Sensor ist defekt. Falls die zurückgegebene
Stromstärke über 20mA ist, besteht entweder ein Kurzschluss oder der Sensor
ist defekt. Somit ist erkennbar ob ein Sensor angeschlossen und funktionsfähig
ist.

Wenn die Stromstärke periodisch abgefragt werden soll, wird empfohlen
den :cb:`Current` Callback zu nutzen und die Periode mit
:func:`Set Current Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Current Callback Period',
'elements': [('Sensor', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Current` callback is triggered
periodically for the given sensor. A value of 0 turns the callback off.

The :cb:`Current` callback is only triggered if the current has changed since the
last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Current` Callback für den
übergebenen Sensor ausgelöst wird. Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Current` Callback wird nur ausgelöst, wenn sich die Stromstärke seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Current Callback Period',
'elements': [('Sensor', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Current Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Current Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Current Callback Threshold',
'elements': [('Sensor', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'int32', 1, 'in', {'scale': (1, 10**9), 'unit': 'Ampere', 'default': 0}),
             ('Max', 'int32', 1, 'in', {'scale': (1, 10**9), 'unit': 'Ampere', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Current Reached` callback for the given
sensor.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the current is *outside* the min and max values"
 "'i'",    "Callback is triggered when the current is *inside* the min and max values"
 "'<'",    "Callback is triggered when the current is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the current is greater than the min value (max is ignored)"
""",
'de':
"""
Setzt den Schwellwert des :cb:`Current Reached` Callbacks für den übergebenen
Sensor.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn die Stromstärke *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn die Stromstärke *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn die Stromstärke kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn die Stromstärke größer als der min Wert ist (max wird ignoriert)"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Current Callback Threshold',
'elements': [('Sensor', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'int32', 1, 'out', {'scale': (1, 10**9), 'unit': 'Ampere', 'default': 0}),
             ('Max', 'int32', 1, 'out', {'scale': (1, 10**9), 'unit': 'Ampere', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Current Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Current Callback Threshold` gesetzt.
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
Sets the period with which the threshold callback

* :cb:`Current Reached`

is triggered, if the threshold

* :func:`Set Current Callback Threshold`

keeps being reached.
""",
'de':
"""
Setzt die Periode mit welcher der Schwellwert Callback

* :cb:`Current Reached`

ausgelöst werden, wenn der Schwellwert

* :func:`Set Current Callback Threshold`

weiterhin erreicht bleibt.
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
'type': 'function',
'name': 'Set Sample Rate',
'elements': [('Rate', 'uint8', 1, 'in', {'constant_group': 'Sample Rate', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the sample rate to either 240, 60, 15 or 4 samples per second.
The resolution for the rates is 12, 14, 16 and 18 bit respectively.

.. csv-table::
 :header: "Value", "Description"
 :widths: 10, 100

 "0",    "240 samples per second, 12 bit resolution"
 "1",    "60 samples per second, 14 bit resolution"
 "2",    "15 samples per second, 16 bit resolution"
 "3",    "4 samples per second, 18 bit resolution"
""",
'de':
"""
Setzt die Abtastrate auf 240, 60, 15 oder 4 Samples pro Sekunde.
Die Auflösung für die Raten sind 12, 14, 16 und 18 Bit respektive.

.. csv-table::
 :header: "Wert", "Beschreibung"
 :widths: 10, 100

 "0",    "240 Samples pro Sekunde, 12 Bit Auflösung"
 "1",    "60 Samples pro Sekunde, 14 Bit Auflösung"
 "2",    "15 Samples pro Sekunde, 16 Bit Auflösung"
 "3",    "4 Samples pro Sekunde, 18 Bit Auflösung"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Sample Rate',
'elements': [('Rate', 'uint8', 1, 'out', {'constant_group': 'Sample Rate', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the sample rate as set by :func:`Set Sample Rate`.
""",
'de':
"""
Gibt die Abtastrate zurück, wie von :func:`Set Sample Rate` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Current',
'elements': [('Sensor', 'uint8', 1, 'out', {'range': (0, 1)}),
             ('Current', 'int32', 1, 'out', {'scale': (1, 10**9), 'unit': 'Ampere', 'range': (0, 22505322)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Current Callback Period`. The :word:`parameter` is the current of the
sensor.

The :cb:`Current` callback is only triggered if the current has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Current Callback Period`,
ausgelöst. Der :word:`parameter` ist die Stromstärke des Sensors.

Der :cb:`Current` Callback wird nur ausgelöst, wenn sich die Stromstärke seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Current Reached',
'elements': [('Sensor', 'uint8', 1, 'out', {'range': (0, 1)}),
             ('Current', 'int32', 1, 'out', {'scale': (1, 10**9), 'unit': 'Ampere', 'range': (0, 22505322)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Current Callback Threshold` is reached.
The :word:`parameter` is the current of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Current Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Stromstärke des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Current', 'current from sensor 1'), [(('Current', 'Current (Sensor 1)'), 'int32', 1, 1000000.0, 'mA', None)], [('uint8', 1)])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Current', 'current'), [(('Sensor', 'Sensor'), 'uint8', 1, None, None, None), (('Current', 'Current'), 'int32', 1, 1000000.0, 'mA', None)], None, None),
              ('callback_period', ('Current', 'current (sensor 1)'), [('uint8', 1)], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('Current Reached', 'current reached'), [(('Sensor', 'Sensor'), 'uint8', 1, None, None, None), (('Current', 'Current'), 'int32', 1, 1000000.0, 'mA', None)], None, None),
              ('callback_threshold', ('Current', 'current (sensor 1)'), [('uint8', 1)], '>', [(10, 0)])]
})

def current_channel(index):
    return {
            'id': 'Current Sensor {0}'.format(index),
            'type': 'Current',
            'label': 'Current Sensor {0}'.format(index),

            'init_code':"""this.setCurrentCallbackPeriod((short){0}, channelCfg.updateInterval);""".format(index),
            'dispose_code': """this.setCurrentCallbackPeriod((short){0}, 0);""".format(index),

            'getters': [{
                'packet': 'Get Current',
                'packet_params': ['(short){}'.format(index)],
                'transform': 'new QuantityType<>(value{divisor}, {unit})'}],

            'callbacks': [{
                'filter': 'sensor == {0}'.format(index),
                'packet': 'Current',
                'transform': 'new QuantityType<>(current{divisor}, {unit})'}],

            'java_unit': 'SmartHomeUnits.AMPERE',
            'divisor': '1000000000.0',
            'is_trigger_channel': False
        }

com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'params': [
        {
            'packet': 'Set Sample Rate',
            'element': 'Rate',

            'name': 'Sample Rate',
            'type': 'integer',
            'options': [('240 SPS', 0),
                        ('60 SPS', 1),
                        ('15 SPS', 2),
                        ('4 SPS', 3)],
            'limitToOptions': 'true',
            'default': 3,

            'label': 'Sample Rate',
            'description': "The sample rate to either 240, 60, 15 or 4 samples per second. The resolution for the rates is 12, 14, 16 and 18 bit respectively.",
            'advanced': 'true'
        }
    ],
    'init_code': """this.setSampleRate(cfg.sampleRate.shortValue());""",
    'channels': [
        current_channel(0),
        current_channel(1),
    ],
    'channel_types': [
        oh_generic_channel_type('Current', 'Number:ElectricCurrent', 'NOT USED',
                     description='Measured current between 0 and 0.022505322A (22.5mA)',
                     read_only=True,
                     pattern='%.6f %unit%',
                     min_=0,
                     max_=0.022505322)
    ],
    'actions': ['Get Current', 'Get Sample Rate']
}
