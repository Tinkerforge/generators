# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Accelerometer Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'api_version_extra': 1, # +1 for "Break API to fix bool return type mismatch in Servo Brick and Accelerometer Brickelt API [cbddb0a]"
    'category': 'Bricklet',
    'device_identifier': 250,
    'name': 'Accelerometer',
    'display_name': 'Accelerometer',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures acceleration in three axis',
        'de': 'Misst Beschleunigung in drei Achsen'
    },
    'released': True,
    'documented': True,
    'discontinued': True, # replaced by Accelerometer Bricklet 2.0
    'features': [
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

com['constant_groups'].append({
'name': 'Data Rate',
'type': 'uint8',
'constants': [('Off', 0),
              ('3Hz', 1),
              ('6Hz', 2),
              ('12Hz', 3),
              ('25Hz', 4),
              ('50Hz', 5),
              ('100Hz', 6),
              ('400Hz', 7),
              ('800Hz', 8),
              ('1600Hz', 9)]
})

com['constant_groups'].append({
'name': 'Full Scale',
'type': 'uint8',
'constants': [('2g', 0),
              ('4g', 1),
              ('6g', 2),
              ('8g', 3),
              ('16g', 4)]
})

com['constant_groups'].append({
'name': 'Filter Bandwidth',
'type': 'uint8',
'constants': [('800Hz', 0),
              ('400Hz', 1),
              ('200Hz', 2),
              ('50Hz', 3)]
})

com['packets'].append({
'type': 'function',
'name': 'Get Acceleration',
'elements': [('X', 'int16', 1, 'out', {'scale': (1, 1000), 'unit': 'Standard Gravity', 'range': 'dynamic'}),
             ('Y', 'int16', 1, 'out', {'scale': (1, 1000), 'unit': 'Standard Gravity', 'range': 'dynamic'}),
             ('Z', 'int16', 1, 'out', {'scale': (1, 1000), 'unit': 'Standard Gravity', 'range': 'dynamic'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the acceleration in x, y and z direction. The values
are given in gₙ/1000 (1gₙ = 9.80665m/s²). The range is
configured with :func:`Set Configuration`.

If you want to get the acceleration periodically, it is recommended
to use the :cb:`Acceleration` callback and set the period with
:func:`Set Acceleration Callback Period`.
""",
'de':
"""
Gibt die Beschleunigung in X-, Y- und Z-Richtung zurück. Die Werte
haben die Einheit gₙ/1000 (1gₙ = 9,80665m/s²). Der Wertebereich
wird mit :func:`Set Configuration` konfiguriert.

Wenn die Beschleunigungswerte periodisch abgefragt werden sollen, wird empfohlen
den :cb:`Acceleration` Callback zu nutzen und die Periode mit
:func:`Set Acceleration Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Acceleration Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Acceleration` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Acceleration` callback is only triggered if the acceleration has
changed since the last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Acceleration` Callback ausgelöst
wird. Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Acceleration` Callback wird nur ausgelöst, wenn sich die Acceleration
seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Acceleration Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Acceleration Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Acceleration Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Acceleration Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min X', 'int16', 1, 'in', {'scale': (1, 1000), 'unit': 'Standard Gravity', 'default': 0}),
             ('Max X', 'int16', 1, 'in', {'scale': (1, 1000), 'unit': 'Standard Gravity', 'default': 0}),
             ('Min Y', 'int16', 1, 'in', {'scale': (1, 1000), 'unit': 'Standard Gravity', 'default': 0}),
             ('Max Y', 'int16', 1, 'in', {'scale': (1, 1000), 'unit': 'Standard Gravity', 'default': 0}),
             ('Min Z', 'int16', 1, 'in', {'scale': (1, 1000), 'unit': 'Standard Gravity', 'default': 0}),
             ('Max Z', 'int16', 1, 'in', {'scale': (1, 1000), 'unit': 'Standard Gravity', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Acceleration Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the acceleration is *outside* the min and max values"
 "'i'",    "Callback is triggered when the acceleration is *inside* the min and max values"
 "'<'",    "Callback is triggered when the acceleration is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the acceleration is greater than the min value (max is ignored)"
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Acceleration Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn die Beschleunigung *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn die Beschleunigung *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn die Beschleunigung kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn die Beschleunigung größer als der min Wert ist (max wird ignoriert)"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Acceleration Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min X', 'int16', 1, 'out', {'scale': (1, 1000), 'unit': 'Standard Gravity', 'default': 0}),
             ('Max X', 'int16', 1, 'out', {'scale': (1, 1000), 'unit': 'Standard Gravity', 'default': 0}),
             ('Min Y', 'int16', 1, 'out', {'scale': (1, 1000), 'unit': 'Standard Gravity', 'default': 0}),
             ('Max Y', 'int16', 1, 'out', {'scale': (1, 1000), 'unit': 'Standard Gravity', 'default': 0}),
             ('Min Z', 'int16', 1, 'out', {'scale': (1, 1000), 'unit': 'Standard Gravity', 'default': 0}),
             ('Max Z', 'int16', 1, 'out', {'scale': (1, 1000), 'unit': 'Standard Gravity', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Acceleration Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Acceleration Callback Threshold` gesetzt.
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

* :cb:`Acceleration Reached`

is triggered, if the threshold

* :func:`Set Acceleration Callback Threshold`

keeps being reached.
""",
'de':
"""
Setzt die Periode mit welcher die Schwellwert Callback

* :cb:`Acceleration Reached`

ausgelöst wird, wenn der Schwellwert

* :func:`Set Acceleration Callback Threshold`

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
'name': 'Get Temperature',
'elements': [('Temperature', 'int16', 1, 'out', {'unit': 'Degree Celsius', 'range': (-103, 152)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the temperature of the accelerometer.
""",
'de':
"""
Gibt die Temperatur des Beschleunigungssensors zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('Data Rate', 'uint8', 1, 'in', {'constant_group': 'Data Rate', 'default': 6}),
             ('Full Scale', 'uint8', 1, 'in', {'constant_group': 'Full Scale', 'default': 1}),
             ('Filter Bandwidth', 'uint8', 1, 'in', {'constant_group': 'Filter Bandwidth', 'default': 2})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Configures the data rate, full scale range and filter bandwidth.
Possible values are:

* Data rate of 0Hz to 1600Hz.
* Full scale range of ±2gₙ up to ±16gₙ.
* Filter bandwidth between 50Hz and 800Hz.

Decreasing data rate or full scale range will also decrease the noise on
the data.
""",
'de':
"""
Konfiguriert die Datenrate, den Wertebereich und die Filterbandbreite.
Mögliche Konfigurationswerte sind:

* Datenrate zwischen 0Hz und 1600Hz.
* Wertebereich von ±2gₙ bis zu ±16gₙ.
* Filterbandbreite zwischen 50Hz und 800Hz.

Eine Verringerung der Datenrate oder des Wertebereichs verringert auch
automatisch das Rauschen auf den Daten.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Data Rate', 'uint8', 1, 'out', {'constant_group': 'Data Rate', 'default': 6}),
             ('Full Scale', 'uint8', 1, 'out', {'constant_group': 'Full Scale', 'default': 1}),
             ('Filter Bandwidth', 'uint8', 1, 'out', {'constant_group': 'Filter Bandwidth', 'default': 2})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'LED On',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Enables the LED on the Bricklet.
""",
'de':
"""
Aktiviert die LED auf dem Bricklet.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'LED Off',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Disables the LED on the Bricklet.
""",
'de':
"""
Deaktiviert die LED auf dem Bricklet.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is LED On',
'elements': [('On', 'bool', 1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns *true* if the LED is enabled, *false* otherwise.
""",
'de':
"""
Gibt *true* zurück wenn die LED aktiviert ist, *false* sonst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Acceleration',
'elements': [('X', 'int16', 1, 'out', {'scale': (1, 1000), 'unit': 'Standard Gravity', 'range': 'dynamic'}),
             ('Y', 'int16', 1, 'out', {'scale': (1, 1000), 'unit': 'Standard Gravity', 'range': 'dynamic'}),
             ('Z', 'int16', 1, 'out', {'scale': (1, 1000), 'unit': 'Standard Gravity', 'range': 'dynamic'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Acceleration Callback Period`. The :word:`parameters` are the
X, Y and Z acceleration. The range is
configured with :func:`Set Configuration`.

The :cb:`Acceleration` callback is only triggered if the acceleration has
changed since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Acceleration Callback Period`, ausgelöst. Die :word:`parameters`
sind die Beschleunigungen der X-, Y- und Z-Achse. Der Wertebereich
wird mit :func:`Set Configuration` konfiguriert.

Der :cb:`Acceleration` Callback wird nur ausgelöst, wenn sich die Beschleunigung
seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Acceleration Reached',
'elements': [('X', 'int16', 1, 'out', {'scale': (1, 1000), 'unit': 'Standard Gravity', 'range': 'dynamic'}),
             ('Y', 'int16', 1, 'out', {'scale': (1, 1000), 'unit': 'Standard Gravity', 'range': 'dynamic'}),
             ('Z', 'int16', 1, 'out', {'scale': (1, 1000), 'unit': 'Standard Gravity', 'range': 'dynamic'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Acceleration Callback Threshold` is reached.
The :word:`parameters` are the X, Y and Z acceleration. The range is
configured with :func:`Set Configuration`.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Acceleration Callback Threshold` gesetzt, erreicht wird.
Die :word:`parameters` sind die Beschleunigungen der X-, Y- und Z-Achse. Der Wertebereich
wird mit :func:`Set Configuration` konfiguriert.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Acceleration', 'acceleration'), [(('X', 'Acceleration [X]'), 'int16', 1, 1000.0, 'g', None), (('Y', 'Acceleration [Y]'), 'int16', 1, 1000.0, 'g', None), (('Z', 'Acceleration [Z]'), 'int16', 1, 1000.0, 'g', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Acceleration', 'acceleration'), [(('X', 'Acceleration [X]'), 'int16', 1, 1000.0, 'g', None), (('Y', 'Acceleration [Y]'), 'int16', 1, 1000.0, 'g', None), (('Z', 'Acceleration [Z]'), 'int16', 1, 1000.0, 'g', None)], None, None),
              ('callback_period', ('Acceleration', 'acceleration'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('Acceleration Reached', 'acceleration reached'), [(('X', 'Acceleration [X]'), 'int16', 1, 1000.0, 'g', None), (('Y', 'Acceleration [Y]'), 'int16', 1, 1000.0, 'g', None), (('Z', 'Acceleration [Z]'), 'int16', 1, 1000.0, 'g', None)], None, None),
              ('callback_threshold', ('Acceleration', 'acceleration'), [], '>', [(2, 0), (2, 0), (2, 0)])]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports() + ["org.eclipse.smarthome.core.library.types.OnOffType"],
    'params': [{
            'name': 'Data Rate',
            'type': 'integer',
            'options': [('Off', 0),
                        ('3Hz', 1),
                        ('6Hz', 2),
                        ('12Hz', 3),
                        ('25Hz', 4),
                        ('50Hz', 5),
                        ('100Hz', 6),
                        ('400Hz', 7),
                        ('800Hz', 8),
                        ('1600Hz', 9)],
            'limitToOptions': 'true',
            'default': 6,
            'label': 'Data Rate',
            'description': 'The data rate of 0Hz to 1600Hz. Decreasing data rate or full scale range will also decrease the noise on the data.'
        }, {
            'name': 'Full Scale Range',
            'type': 'integer',
            'options': [('2g', 0),
                        ('4g', 1),
                        ('6g', 2),
                        ('8g', 3),
                        ('16g', 4)],
            'limitToOptions': 'true',
            'default': 1,
            'label': 'Full Scale Range',
            'description': 'Full scale range of -2g to +2g up to -16g to +16g. Decreasing data rate or full scale range will also decrease the noise on the data.'
        }, {
            'name': 'Frequency Filter',
            'type': 'integer',
            'options': [('800Hz', 0),
                        ('400Hz', 1),
                        ('200Hz', 2),
                        ('50Hz', 3)],
            'limitToOptions': 'true',
            'default': 2,
            'label': 'Frequency Filter',
            'description': 'Filter bandwidth between 50Hz and 800Hz.'
        },
        update_interval('Acceleration', 'the acceleration')],
    'param_groups': oh_generic_channel_param_groups(),
    'init_code': """this.setConfiguration(cfg.dataRate.shortValue(), cfg.fullScaleRange.shortValue(), cfg.frequencyFilter.shortValue());
    this.setAccelerationCallbackPeriod(cfg.accelerationUpdateInterval);""",
    'channels': [
        {
            'id': 'Acceleration {}'.format(axis.upper()),
            'type': 'Acceleration',
            'label': 'Acceleration {}'.format(axis.upper()),

            'getters': [{
                'packet': 'Get Acceleration',
                'transform': 'new QuantityType(value.{}{{divisor}}, {{unit}})'.format(axis)}],

            'callbacks': [{
                'packet': 'Acceleration',
                'transform': 'new QuantityType({}{{divisor}}, {{unit}})'.format(axis)}],
            'java_unit': 'SmartHomeUnits.STANDARD_GRAVITY',
            'divisor': '1000.0',
            'is_trigger_channel': False
        } for axis in ['x', 'y', 'z']
    ] + [{
            'id': 'Temperature',
            'type': 'Temperature',
            'label': 'Temperature',

            'getters': [{
                'packet': 'Get Temperature',
                'transform': 'new QuantityType(value{divisor}, {unit})'}],
            'java_unit': 'SIUnits.CELSIUS',
            'is_trigger_channel': False
        }, {
            'id': 'LED',
            'type': 'LED',

            'setters': [{
                'predicate': 'cmd == OnOffType.ON',
                'packet': 'LED On'
            }, {
                'predicate': 'cmd == OnOffType.OFF',
                'packet': 'LED Off'
            }],
            'setter_command_type': "OnOffType",

            'getters': [{
                'packet': 'Is LED On',
                'transform': 'value? OnOffType.ON : OnOffType.OFF'}]
        }
    ],
    'channel_types': [
        oh_generic_channel_type('Acceleration', 'Number:Acceleration', 'NOT USED',
                     description='The acceleration in g (1g = 9.80665m/s²), not to be confused with grams.',
                     read_only=True,
                     pattern='%.3f %unit%'),
        oh_generic_channel_type('LED', 'Switch', 'LED',
                     description='Enables/Disables the LED on the Bricklet.'),
        oh_generic_channel_type('Temperature', 'Number:Temperature', 'Temperature',
                     description='The temperature of the accelerometer',
                     read_only=True),
    ],
    'actions': ['Get Acceleration', 'Get Temperature', 'Is LED On', 'Get Configuration']
}
