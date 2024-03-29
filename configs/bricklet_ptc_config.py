# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# PTC Bricklet communication config

from generators.configs.commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'category': 'Bricklet',
    'device_identifier': 226,
    'name': 'PTC',
    'display_name': 'PTC',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Reads temperatures from Pt100 und Pt1000 sensors',
        'de': 'Liest Temperaturen von Pt100 und Pt1000 Sensoren'
    },
    'released': True,
    'documented': True,
    'discontinued': True, # replaced by Industrial PTC Bricklet
    'features': [
        'device',
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

com['constant_groups'].append({
'name': 'Filter Option',
'type': 'uint8',
'constants': [('50Hz', 0),
              ('60Hz', 1)]
})

com['constant_groups'].append({
'name': 'Wire Mode',
'type': 'uint8',
'constants': [('2', 2),
              ('3', 3),
              ('4', 4)]
})

com['packets'].append({
'type': 'function',
'name': 'Get Temperature',
'elements': [('Temperature', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Degree Celsius', 'range': (-24600, 84900)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the temperature of connected sensor.

If you want to get the temperature periodically, it is recommended
to use the :cb:`Temperature` callback and set the period with
:func:`Set Temperature Callback Period`.
""",
'de':
"""
Gibt die Temperatur des verbundenen Sensors zurück.

Wenn die Temperatur periodisch abgefragt werden soll, wird empfohlen
den :cb:`Temperature` Callback zu nutzen und die Periode mit
:func:`Set Temperature Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Resistance',
'elements': [('Resistance', 'int32', 1, 'out', {'scale': 'dynamic', 'unit': 'Ohm'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the value as measured by the MAX31865 precision delta-sigma ADC.

The value can be converted with the following formulas:

* Pt100:  resistance = (value * 390) / 32768
* Pt1000: resistance = (value * 3900) / 32768

If you want to get the resistance periodically, it is recommended
to use the :cb:`Resistance` callback and set the period with
:func:`Set Resistance Callback Period`.
""",
'de':
"""
Gibt den Wert zurück, wie vom "MAX31865 Präzisions Delta-Sigma ADC" berechnet.

Der Wert kann mit den folgenden Formeln in einen Widerstand konvertiert werden:

* Pt100:  Widerstand = (Wert * 390) / 32768
* Pt1000: Widerstand = (Wert * 3900) / 32768

Wenn der Widerstand periodisch abgefragt werden soll, wird empfohlen
den :cb:`Resistance` Callback zu nutzen und die Periode mit
:func:`Set Resistance Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Temperature Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Temperature` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Temperature` callback is only triggered if the temperature has
changed since the last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Temperature` Callback ausgelöst
wird. Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Temperature` Callback wird nur ausgelöst, wenn sich die Temperatur seit
der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Temperature Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Temperature Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Temperature Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Resistance Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Resistance` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Resistance` callback is only triggered if the resistance has changed
since the last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Resistance` Callback ausgelöst
wird. Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Resistance` Callback wird nur ausgelöst, wenn sich der Widerstand seit
der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Resistance Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Resistance Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Resistance Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Temperature Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'int32', 1, 'in', {'scale': (1, 100), 'unit': 'Degree Celsius', 'default': 0}),
             ('Max', 'int32', 1, 'in', {'scale': (1, 100), 'unit': 'Degree Celsius', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Temperature Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the temperature is *outside* the min and max values"
 "'i'",    "Callback is triggered when the temperature is *inside* the min and max values"
 "'<'",    "Callback is triggered when the temperature is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the temperature is greater than the min value (max is ignored)"
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Temperature Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn die Temperatur *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn die Temperatur *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn die Temperatur kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn die Temperatur größer als der min Wert ist (max wird ignoriert)"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Temperature Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Degree Celsius', 'default': 0}),
             ('Max', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Degree Celsius', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Temperature Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Temperature Callback Threshold` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Resistance Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'int32', 1, 'in', {'scale': 'dynamic', 'unit': 'Ohm', 'default': 0}),
             ('Max', 'int32', 1, 'in', {'scale': 'dynamic', 'unit': 'Ohm', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Resistance Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the temperature is *outside* the min and max values"
 "'i'",    "Callback is triggered when the temperature is *inside* the min and max values"
 "'<'",    "Callback is triggered when the temperature is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the temperature is greater than the min value (max is ignored)"
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Resistance Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn die Temperatur *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn die Temperatur *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn die Temperatur kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn die Temperatur größer als der min Wert ist (max wird ignoriert)"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Resistance Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'int32', 1, 'out', {'scale': 'dynamic', 'unit': 'Ohm','default': 0}),
             ('Max', 'int32', 1, 'out', {'scale': 'dynamic', 'unit': 'Ohm','default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Resistance Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Resistance Callback Threshold` gesetzt.
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

* :cb:`Temperature Reached`,
* :cb:`Resistance Reached`

is triggered, if the threshold

* :func:`Set Temperature Callback Threshold`,
* :func:`Set Resistance Callback Threshold`

keeps being reached.
""",
'de':
"""
Setzt die Periode mit welcher die Schwellwert Callback

* :cb:`Temperature Reached`,
* :cb:`Resistance Reached`

ausgelöst wird, wenn der Schwellwert

* :func:`Set Temperature Callback Threshold`,
* :func:`Set Resistance Callback Threshold`

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
'type': 'callback',
'name': 'Temperature',
'elements': [('Temperature', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Degree Celsius', 'range': (-24600, 84900)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Temperature Callback Period`. The :word:`parameter` is the
temperature of the connected sensor.

The :cb:`Temperature` callback is only triggered if the temperature has changed
since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Temperature Callback Period`,
ausgelöst. Der :word:`parameter` ist die Temperatur des verbundenen Sensors.

Der :cb:`Temperature` Callback wird nur ausgelöst, wenn sich die Temperatur
seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Temperature Reached',
'elements': [('Temperature', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Degree Celsius', 'range': (-24600, 84900)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Temperature Callback Threshold` is reached.
The :word:`parameter` is the temperature of the connected sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Temperature Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Temperatur des verbundenen Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Resistance',
'elements': [('Resistance', 'int32', 1, 'out', {'scale': 'dynamic', 'unit': 'Ohm'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Resistance Callback Period`. The :word:`parameter` is the resistance
of the connected sensor.

The :cb:`Resistance` callback is only triggered if the resistance has changed
since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Resistance Callback Period`,
ausgelöst. Der :word:`parameter` ist der Widerstand des verbundenen Sensors.

Der :cb:`Resistance` Callback wird nur ausgelöst, wenn sich der Widerstand seit
der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Resistance Reached',
'elements': [('Resistance', 'int32', 1, 'out', {'scale': 'dynamic', 'unit': 'Ohm'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Resistance Callback Threshold` is reached.
The :word:`parameter` is the resistance of the connected sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Resistance Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist der Widerstand des verbundenen Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Noise Rejection Filter',
'elements': [('Filter', 'uint8', 1, 'in', {'constant_group': 'Filter Option', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the noise rejection filter to either 50Hz (0) or 60Hz (1).
Noise from 50Hz or 60Hz power sources (including
harmonics of the AC power's fundamental frequency) is
attenuated by 82dB.
""",
'de':
"""
Setzt den Entstörfilter auf 50Hz (0) oder 60Hz (1).
Störungen von 50Hz oder 60Hz Stromquellen (inklusive
Oberwellen der Stromquellen-Grundfrequenz) werden
um 82dB abgeschwächt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Noise Rejection Filter',
'elements': [('Filter', 'uint8', 1, 'out', {'constant_group': 'Filter Option', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the noise rejection filter option as set by
:func:`Set Noise Rejection Filter`
""",
'de':
"""
Gibt die Einstellung des Entstörfilters zurück, wie von
:func:`Set Noise Rejection Filter` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is Sensor Connected',
'elements': [('Connected', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns *true* if the sensor is connected correctly.

If this function
returns *false*, there is either no Pt100 or Pt1000 sensor connected,
the sensor is connected incorrectly or the sensor itself is faulty.
""",
'de':
"""
Gibt *true* zurück wenn ein Sensor korrekt verbunden ist.

Falls diese Funktion *false* zurück gibt, ist entweder kein
Pt100 oder Pt1000 Sensor verbunden, der Sensor ist inkorrekt
verbunden oder der Sensor selbst ist fehlerhaft.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Wire Mode',
'elements': [('Mode', 'uint8', 1, 'in', {'constant_group': 'Wire Mode', 'default': 2})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the wire mode of the sensor. Possible values are 2, 3 and 4 which
correspond to 2-, 3- and 4-wire sensors. The value has to match the jumper
configuration on the Bricklet.
""",
'de':
"""
Stellt die Leiter-Konfiguration des Sensors ein. Mögliche Werte sind 2, 3 und
4, dies entspricht 2-, 3- und 4-Leiter-Sensoren. Der Wert muss er
Jumper-Konfiguration am Bricklet entsprechen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Wire Mode',
'elements': [('Mode', 'uint8', 1, 'out', {'constant_group': 'Wire Mode', 'default': 2})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the wire mode as set by :func:`Set Wire Mode`
""",
'de':
"""
Gibt die Leiter-Konfiguration zurück, wie von :func:`Set Wire Mode` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Sensor Connected Callback Configuration',
'elements': [('Enabled', 'bool', 1, 'in', {'default': False})],
'since_firmware': [2, 0, 2],
'doc': ['ccf', {
'en':
"""
If you enable this callback, the :cb:`Sensor Connected` callback is triggered
every time a Pt sensor is connected/disconnected.
""",
'de':
"""
Wenn dieser Callback aktiviert ist, wird der :cb:`Sensor Connected` Callback
jedes mal ausgelöst, wenn ein Pt-Sensor verbunden/getrennt wird.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Sensor Connected Callback Configuration',
'elements': [('Enabled', 'bool', 1, 'out', {'default': False})],
'since_firmware': [2, 0, 2],
'doc': ['ccf', {
'en':
"""
Returns the configuration as set by :func:`Set Sensor Connected Callback Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Sensor Connected Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Sensor Connected',
'elements': [('Connected', 'bool', 1, 'out', {})],
'since_firmware': [2, 0, 2],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set Sensor Connected Callback Configuration`.

The :word:`parameter` is the same as :func:`Is Sensor Connected`.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set Sensor Connected Callback Configuration` gesetzten Konfiguration

Der :word:`parameter` ist der gleiche wie bei :func:`Is Sensor Connected`.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Temperature', 'temperature'), [(('Temperature', 'Temperature'), 'int32', 1, 100.0, '°C', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Temperature', 'temperature'), [(('Temperature', 'Temperature'), 'int32', 1, 100.0, '°C', None)], None, None),
              ('callback_period', ('Temperature', 'temperature'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('Temperature Reached', 'temperature reached'), [(('Temperature', 'Temperature'), 'int32', 1, 100.0, '°C', None)], None, None),
              ('callback_threshold', ('Temperature', 'temperature'), [], '>', [(30, 0)])]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.OpenClosedType'],
    'param_groups': oh_generic_channel_param_groups(),
    'params': [
        {
            'packet': 'Set Wire Mode',
            'element': 'Mode',

            'name': 'Wire Mode',
            'type': 'integer',
            'options': [('2-wire', 2),
                        ('3-wire', 3),
                        ('4-wire', 4)],
            'limit_to_options': 'true',
            'label': 'Wire Mode',
            'description': 'The wire mode of the sensor. Possible values are 2, 3 and 4 which correspond to 2-, 3- and 4-wire sensors. The value has to match the jumper configuration on the Bricklet.',
        },
        {
            'packet': 'Set Noise Rejection Filter',
            'element': 'Filter',

            'name': 'Noise Rejection Filter Frequency',
            'type': 'integer',
            'label': 'Noise Rejection Filter Frequency',
            'description': 'Sets the noise rejection filter to either 50 Hz or 60 Hz. Noise from 50 Hz or 60 Hz power sources (including harmonics of the AC power’s fundamental frequency) is attenuated by 82dB',
        }, {
            'virtual': True,

            'name': 'Sensor Type',
            'type': 'integer',
            'options': [('Pt100', 100),
                        ('Pt1000', 1000)],
            'limit_to_options': 'true',
            'default': 100,
            'label': 'Sensor Type',
            'description': 'The type of the sensor. The value has to match the jumper configuration on the Bricklet or else the calculated resistance will not be correct.',
        }
    ],
    'init_code': """this.setWireMode(cfg.wireMode.shortValue());
this.setNoiseRejectionFilter(cfg.noiseRejectionFilterFrequency.shortValue());
this.setSensorConnectedCallbackConfiguration(true);""",
    'channels': [
        oh_generic_old_style_channel('Temperature', 'Temperature'),
        oh_generic_old_style_channel('Resistance', 'Resistance', divisor='(32768 / cfg.sensorType == 100 ? 390 : 3900)'),
        {
            'id': 'Sensor Connected',
            'type': 'Sensor Connected',
            'getters': [{
                'packet': 'Is Sensor Connected',
                'element': 'Connected',
                'transform': 'value ? OpenClosedType.CLOSED : OpenClosedType.OPEN'}],
            'callbacks': [{
                'packet': 'Sensor Connected',
                'element': 'Connected',
                'transform': 'connected ? OpenClosedType.CLOSED : OpenClosedType.OPEN'
            }]
        },
    ],
    'channel_types': [
        oh_generic_channel_type('Temperature', 'Number', 'Temperature',
                    update_style='Callback Period',
                    description='Temperature of the connected sensor'),
        oh_generic_channel_type('Resistance', 'Number', 'Resistance',
                    update_style='Callback Period',
                    description='The value as measured by the MAX31865 precision delta-sigma ADC. Configure the thing to Pt 100 or Pt 1000, to make sure the conversion is correct.'),
        oh_generic_channel_type('Sensor Connected', 'Contact', 'Sensor Connected',
                    update_style=None,
                    description='Indicates if the sensor is connected correctly. If this is disabled, there is either no Pt100 or Pt1000 sensor connected, the sensor is connected incorrectly or the sensor itself is faulty.'),
    ],
    'actions': ['Get Temperature', 'Is Sensor Connected', 'Get Wire Mode', 'Get Resistance', 'Get Noise Rejection Filter']
}
