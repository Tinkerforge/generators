# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Thermocouple Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from commonconstants import add_callback_value_function

from openhab_common import *

com = {
    'author': 'Ishraq Ibne Ashraf <ishraq@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2109,
    'name': 'Thermocouple V2',
    'display_name': 'Thermocouple 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures temperature with thermocouples',
        'de': 'Misst Temperatur mit Thermoelementen'
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

temperature_doc = {
'en':
"""
Returns the temperature of the thermocouple. The value is given in °C/100,
e.g. a value of 4223 means that a temperature of 42.23 °C is measured.

If you want to get the temperature periodically, it is recommended
to use the :cb:`Temperature` callback and set the period with
:func:`Set Temperature Callback Configuration`.
""",
'de':
"""
Gibt die Temperatur des Thermoelements zurück. Der Wert wird in °C/100
angegeben, z.B. bedeutet ein Wert von 4223 eine gemessene Temperatur von
42,23 °C.

Wenn die Temperatur periodisch abgefragt werden soll, wird empfohlen
den :cb:`Temperature` Callback zu nutzen und die Periode mit
:func:`Set Temperature Callback Configuration` vorzugeben.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Temperature',
    data_name = 'Temperature',
    data_type = 'int32',
    doc       = temperature_doc,
    scale     = (1, 100),
    unit      = 'Degree Celsius',
    range_    = (-21000, 180000)
)

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
              ('callback_configuration', ('Temperature', 'temperature'), [], 1000, False, 'x', [(0, 0)])]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('callback', ('Temperature', 'temperature'), [(('Temperature', 'Temperature'), 'int32', 1, 100.0, '°C', None)], None, None),
              ('callback_configuration', ('Temperature', 'temperature'), [], 10000, False, '>', [(30, 0)])]
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
            'limitToOptions': 'true',
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
            'limitToOptions': 'true',
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
            'limitToOptions': 'true',
            'default': 0,
            'label': 'Frequency Filter',
            'description': 'The frequency filter can be either configured to 50Hz or to 60Hz. You should configure it according to your utility frequency.'
        }],
    'param_groups': oh_generic_channel_param_groups(),
    'init_code': """this.setConfiguration(cfg.averageLength, cfg.thermocoupleType, cfg.frequencyFilter);""",
    'channels': [
        oh_generic_channel('Temperature', 'Temperature', 'SIUnits.CELSIUS', divisor=100.0),
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
                    update_style='Callback Configuration',
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
