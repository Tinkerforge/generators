# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Thermocouple Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 266,
    'name': 'Thermocouple',
    'display_name': 'Thermocouple',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures temperature with thermocouples',
        'de': 'Misst Temperatur mit Thermoelementen'
    },
    'released': True,
    'documented': True,
    'discontinued': True, # replaced by Thermocouple Bricklet 2.0
    'features': [
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

com['constant_groups'].append({
'name': 'Averaging',
'type': 'uint8',
'constants': [('1', 1),
              ('2', 2),
              ('4', 4),
              ('8', 8),
              ('16', 16)]
})

com['constant_groups'].append({
'name': 'Type',
'type': 'uint8',
'constants': [('B', 0),
              ('E', 1),
              ('J', 2),
              ('K', 3),
              ('N', 4),
              ('R', 5),
              ('S', 6),
              ('T', 7),
              ('G8', 8),
              ('G32', 9)]
})

com['constant_groups'].append({
'name': 'Filter Option',
'type': 'uint8',
'constants': [('50Hz', 0),
              ('60Hz', 1)]
})

com['packets'].append({
'type': 'function',
'name': 'Get Temperature',
'elements': [('Temperature', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Degree Celsius', 'range': (-21000, 180000)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the temperature of the thermocouple.

If you want to get the temperature periodically, it is recommended
to use the :cb:`Temperature` callback and set the period with
:func:`Set Temperature Callback Period`.
""",
'de':
"""
Gibt die Temperatur des Thermoelements zurück.

Wenn die Temperatur periodisch abgefragt werden soll, wird empfohlen
den :cb:`Temperature` Callback zu nutzen und die Periode mit
:func:`Set Temperature Callback Period` vorzugeben.
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

The :cb:`Temperature` callback is only triggered if the temperature has changed
since the last triggering.
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
'name': 'Set Debounce Period',
'elements': [('Debounce', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 100})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the threshold callback

* :cb:`Temperature Reached`

is triggered, if the threshold

* :func:`Set Temperature Callback Threshold`

keeps being reached.
""",
'de':
"""
Setzt die Periode mit welcher die Schwellwert Callback

* :cb:`Temperature Reached`

ausgelöst wird, wenn der Schwellwert

* :func:`Set Temperature Callback Threshold`

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
'elements': [('Temperature', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Degree Celsius', 'range': (-21000, 180000)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Temperature Callback Period`. The :word:`parameter` is the
temperature of the thermocouple.

The :cb:`Temperature` callback is only triggered if the temperature has
changed since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Temperature Callback Period`, ausgelöst. Der :word:`parameter` ist
die Temperatur des Thermoelements.

Der :cb:`Temperature` Callback wird nur ausgelöst, wenn sich die Temperatur seit
der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Temperature Reached',
'elements': [('Temperature', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Degree Celsius', 'range': (-21000, 180000)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Temperature Callback Threshold` is reached.
The :word:`parameter` is the temperature of the thermocouple.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Temperature Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Temperatur des Thermoelements.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('Averaging', 'uint8', 1, 'in', {'constant_group': 'Averaging', 'default': 16}),
             ('Thermocouple Type', 'uint8', 1, 'in', {'constant_group': 'Type', 'default': 3}),
             ('Filter', 'uint8', 1, 'in', {'constant_group': 'Filter Option', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
You can configure averaging size, thermocouple type and frequency
filtering.

Available averaging sizes are 1, 2, 4, 8 and 16 samples.

As thermocouple type you can use B, E, J, K, N, R, S and T. If you have a
different thermocouple or a custom thermocouple you can also use
G8 and G32. With these types the returned value will not be in °C/100,
it will be calculated by the following formulas:

* G8: ``value = 8 * 1.6 * 2^17 * Vin``
* G32: ``value = 32 * 1.6 * 2^17 * Vin``

where Vin is the thermocouple input voltage.

The frequency filter can be either configured to 50Hz or to 60Hz. You should
configure it according to your utility frequency.

The conversion time depends on the averaging and filter configuration, it can
be calculated as follows:

* 60Hz: ``time = 82 + (samples - 1) * 16.67``
* 50Hz: ``time = 98 + (samples - 1) * 20``
""",
'de':
"""
Konfiguriert werden können Averaging-Größe, Thermoelement-Typ und
Frequenz-Filterung.

Mögliche Averaging-Größen sind 1, 2, 4, 8 und 16 Samples.

Als Thermoelement-Typ stehen B, E, J, K, N, R, S und T zur Verfügung.
Falls ein anderes Thermoelement benutzt werden soll, können G8 und G32
genutzt werden. Mit diesen Typen wird der Wert nicht in °C/100 zurückgegeben
sondern er wird durch folgende Formeln bestimmt:

* G8: ``Wert = 8 * 1.6 * 2^17 * Vin``
* G32: ``Wert = 32 * 1.6 * 2^17 * Vin``

dabei ist Vin die Eingangsspannung des Thermoelements.

Der Frequenz-Filter kann auf 50Hz und 60Hz konfiguriert werden. Er sollte
abhängig von der lokalen Netzfrequenz gewählt werden.

Die Konvertierungszeit ist abhängig von der Averaging-Größe und der
Frequenz-Filter-Konfiguration. Sie kann wie folgt bestimmt werden:

* 60Hz: ``Zeit = 82 + (Samples - 1) * 16.67``
* 50Hz: ``Zeit = 98 + (Samples - 1) * 20``
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Averaging', 'uint8', 1, 'out', {'constant_group': 'Averaging', 'default': 16}),
             ('Thermocouple Type', 'uint8', 1, 'out', {'constant_group': 'Type', 'default': 3}),
             ('Filter', 'uint8', 1, 'out', {'constant_group': 'Filter Option', 'default': 0})],
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
'name': 'Get Error State',
'elements': [('Over Under', 'bool', 1, 'out', {}),
             ('Open Circuit', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the current error state. There are two possible errors:

* Over/Under Voltage and
* Open Circuit.

Over/Under Voltage happens for voltages below 0V or above 3.3V. In this case
it is very likely that your thermocouple is defective. An Open Circuit error
indicates that there is no thermocouple connected.

You can use the :cb:`Error State` callback to automatically get triggered
when the error state changes.
""",
'de':
"""
Gibt den aktuellen Error-Status zurück. Es gibt zwei mögliche Status:

* Over/Under Voltage und
* Open Circuit.

Over/Under Voltage bei Spannungen unter 0V oder über 3.3V ausgelöst. In diesem
Fall ist mit hoher Wahrscheinlichkeit das Thermoelement defekt. Ein
Open Circuit-Error deutet darauf hin, das kein Thermoelement angeschlossen
ist.

Der :cb:`Error State` Callback wird automatisch jedes mal ausgelöst, wenn sich
der Error-Status ändert.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Error State',
'elements': [('Over Under', 'bool', 1, 'out', {}),
             ('Open Circuit', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This Callback is triggered every time the error state changes
(see :func:`Get Error State`).
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Error-Status sich verändert
(siehe :func:`Get Error State`).
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
    'imports': oh_generic_channel_imports() + ["org.eclipse.smarthome.core.library.types.OnOffType"],
    'params': [{
            'packet': 'Set Configuration',
            'element': 'Averaging',

            'name': 'Average Length',
            'type': 'integer',
            'options': [('1', 1),
                        ('2', 2),
                        ('4', 4),
                        ('8', 8),
                        ('16', 16)],
            'limit_to_options': 'true',
            'default': 16,
            'label': 'Average Length',
            'description': 'Available averaging sizes are 1, 2, 4, 8 and 16 samples.<br/><br/>The conversion time depends on the averaging and filter configuration, it can be calculated as follows:<ul><li>60Hz: time = 82 + (samples - 1) * 16.67</li><li>50Hz: time = 98 + (samples - 1) * 20</li></ul>'
        }, {
            'packet': 'Set Configuration',
            'element': 'Thermocouple Type',

            'name': 'Thermocouple Type',
            'type': 'integer',
            'options': [('B', 0),
                        ('E', 1),
                        ('J', 2),
                        ('K', 3),
                        ('N', 4),
                        ('R', 5),
                        ('S', 6),
                        ('T', 7),
                        ('G8', 8),
                        ('G32', 9)],
            'limit_to_options': 'true',
            'default': 3,
            'label': 'Thermocouple Type',
            'description': 'As thermocouple type you can use B, E, J, K, N, R, S and T. If you have a different thermocouple or a custom thermocouple you can also use G8 and G32. With these types the returned value will not be in °C/100, it will be calculated by the following formulas:<ul><li>G8: value = 8 * 1.6 * 2^17 * Vin</li><li>G32: value = 32 * 1.6 * 2^17 * Vin</li></ul>where Vin is the thermocouple input voltage.'
        }, {
            'packet': 'Set Configuration',
            'element': 'Filter',

            'name': 'Frequency Filter',
            'type': 'integer',
            'options': [('50Hz', 0),
                        ('60Hz', 1)],
            'limit_to_options': 'true',
            'default': 0,
            'label': 'Frequency Filter',
            'description': 'The frequency filter can be either configured to 50Hz or to 60Hz. You should configure it according to your utility frequency.'
        }],
    'param_groups': oh_generic_channel_param_groups(),
    'init_code': """this.setConfiguration(cfg.averageLength.shortValue(), cfg.thermocoupleType.shortValue(), cfg.frequencyFilter.shortValue());""",
    'channels': [
        oh_generic_old_style_channel('Temperature', 'Temperature', 'SIUnits.CELSIUS', divisor=100.0),
        {
            'id': 'Over Under Voltage',
            'type': 'Over Under Voltage',
            'label': 'Over/Under Voltage',

            'getters': [{
                'packet': 'Get Error State',
                'transform': 'value.overUnder ? OnOffType.ON : OnOffType.OFF'}],

            'callbacks': [{
                'packet': 'Error State',
                'transform': 'overUnder ? OnOffType.ON : OnOffType.OFF'}],

            'is_trigger_channel': False
        }, {
            'id': 'Open Circuit',
            'type': 'Open Circuit',
            'label': 'Open Circuit',

            'getters': [{
                'packet': 'Get Error State',
                'transform': 'value.openCircuit ? OnOffType.ON : OnOffType.OFF'}],

            'callbacks': [{
                'packet': 'Error State',
                'transform': 'openCircuit ? OnOffType.ON : OnOffType.OFF'}],

            'is_trigger_channel': False
        }
    ],
    'channel_types': [
        oh_generic_channel_type('Temperature', 'Number:Temperature', 'Temperature',
                    update_style='Callback Period',
                    description='The temperature of the thermocouple.',
                    read_only=True,
                    pattern='%.2f %unit%',
                    min_=-210,
                    max_=1800),
        oh_generic_channel_type('Over Under Voltage', 'Switch', 'Over/Under Voltage Error',
                    update_style=None,
                    description='Over/Under Voltage happens for voltages below 0V or above 3.3V. In this case it is very likely that your thermocouple is defective.',
                    read_only=True),
        oh_generic_channel_type('Open Circuit', 'Switch', 'Open Circuit Error',
                    update_style=None,
                    description='An Open Circuit error indicates that there is no thermocouple connected.',
                    read_only=True),
    ],
    'actions': ['Get Temperature', 'Get Configuration', 'Get Error State']
}

