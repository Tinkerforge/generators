# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Voltage/Current Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from commonconstants import add_callback_value_function

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2105,
    'name': 'Voltage Current V2',
    'display_name': 'Voltage/Current 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures power, DC voltage and DC current up to 720W/36V/20A',
        'de': 'Misst Leistung, Gleichspannung und Gleichstrom bis zu 720W/36V/20A'
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
'constants': [('1', 0),
              ('4', 1),
              ('16', 2),
              ('64', 3),
              ('128', 4),
              ('256', 5),
              ('512', 6),
              ('1024', 7)]
})

com['constant_groups'].append({
'name': 'Conversion Time',
'type': 'uint8',
'constants': [('140us', 0),
              ('204us', 1),
              ('332us', 2),
              ('588us', 3),
              ('1 1ms', 4),
              ('2 116ms', 5),
              ('4 156ms', 6),
              ('8 244ms', 7)]
})

current_doc = {
'en':
"""
Returns the current.
""",
'de':
"""
Gibt die gemessenen Stromstärke zurück.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Current',
    data_name = 'Current',
    data_type = 'int32',
    doc       = current_doc,
    scale     = (1, 1000),
    unit      = 'Ampere',
    range_    = (-20000, 20000)
)

voltage_doc = {
'en':
"""
Returns the voltage.
""",
'de':
"""
Gibt die gemessenen Spannung zurück.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Voltage',
    data_name = 'Voltage',
    data_type = 'int32',
    doc       = voltage_doc,
    scale     = (1, 1000),
    unit      = 'Volt',
    range_    = (0, 36000)
)

power_doc = {
'en':
"""
Returns the power.
""",
'de':
"""
Gibt die gemessenen Leistung zurück.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Power',
    data_name = 'Power',
    data_type = 'int32',
    doc       = power_doc,
    scale     = (1, 1000),
    unit      = 'Watt',
    range_    = (0, 720000)
)

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('Averaging', 'uint8', 1, 'in', {'constant_group': 'Averaging', 'default': 3}),
             ('Voltage Conversion Time', 'uint8', 1, 'in', {'constant_group': 'Conversion Time', 'default': 4}),
             ('Current Conversion Time', 'uint8', 1, 'in', {'constant_group': 'Conversion Time', 'default': 4})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the configuration of the Voltage/Current Bricklet 2.0. It is
possible to configure number of averages as well as
voltage and current conversion time.
""",
'de':
"""
Setzt die Konfiguration des Voltage/Current Bricklet 2.0. Es ist
möglich die Anzahl für die Durchschnittsbildung, und die
Wandlungszeit für Spannung und Stromstärke zu definieren.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Averaging', 'uint8', 1, 'out', {'constant_group': 'Averaging', 'default': 3}),
             ('Voltage Conversion Time', 'uint8', 1, 'out', {'constant_group': 'Conversion Time', 'default': 4}),
             ('Current Conversion Time', 'uint8', 1, 'out', {'constant_group': 'Conversion Time', 'default': 4})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
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
'name': 'Set Calibration',
'elements': [('Voltage Multiplier', 'uint16', 1, 'in', {}),
             ('Voltage Divisor', 'uint16', 1, 'in', {}),
             ('Current Multiplier', 'uint16', 1, 'in', {}),
             ('Current Divisor', 'uint16', 1, 'in', {})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Since the ADC and the shunt resistor used for the measurements
are not perfect they need to be calibrated by a multiplier and
a divisor if a very precise reading is needed.

For example, if you are expecting a current of 1000mA and you
are measuring 1023mA, you can calibrate the Voltage/Current Bricklet
by setting the current multiplier to 1000 and the divisor to 1023.
The same applies for the voltage.

The calibration will be saved on the EEPROM of the Voltage/Current
Bricklet and only needs to be done once.
""",
'de':
"""
Da der ADC und der Shunt-Widerstand für die Messungen verwendet
werden nicht perfekt sind, ist es nötig einen Multiplikator und
einen Divisor zu setzen falls sehr genaue Messwerte nötig sind.

Zum Beispiel: Wenn eine Messung von 1000mA erwartet wird, das
Voltage/Current Bricklet 2.0 aber 1023mA zurück gibt, sollte
der Multiplikator auf 1000 und der Divisor auf 1023 gesetzt
werden. Das gleiches gilt für die Spannung.

Die Kalibrierung wird in den EEPROM des Voltage/Current Bricklet
gespeichert und muss nur einmal gesetzt werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Calibration',
'elements': [('Voltage Multiplier', 'uint16', 1, 'out', {}),
             ('Voltage Divisor', 'uint16', 1, 'out', {}),
             ('Current Multiplier', 'uint16', 1, 'out', {}),
             ('Current Divisor', 'uint16', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the calibration as set by :func:`Set Calibration`.
""",
'de':
"""
Gibt die Kalibrierung zurück, wie von :func:`Set Calibration` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Voltage', 'voltage'), [(('Voltage', 'Voltage'), 'int32', 1, 1000.0, 'V', None)], []),
              ('getter', ('Get Current', 'current'), [(('Current', 'Current'), 'int32', 1, 1000.0, 'A', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Current', 'current'), [(('Current', 'Current'), 'int32', 1, 1000.0, 'A', None)], None, None),
              ('callback_configuration', ('Current', 'current'), [], 1000, False, 'x', [(0, 0)])]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('callback', ('Power', 'power'), [(('Power', 'power'), 'int32', 1, 1000.0, 'W', None)], None, None),
              ('callback_configuration', ('Power', 'power'), [], 1000, False, '>', [(10, 0)])]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'params': [
        {
            'packet': 'Set Configuration',
            'element': 'Averaging',

            'name': 'Averaging',
            'type': 'integer',
            'options': [('1', 0),
                        ('4', 1),
                        ('16', 2),
                        ('64', 3),
                        ('128', 4),
                        ('256', 5),
                        ('512', 6),
                        ('1024', 7)],
            'limitToOptions': 'true',
            'default': 3,

            'label': 'Averaging',
            'description': 'Configures the number of samples to average over.'
        }, {
            'packet': 'Set Configuration',
            'element': 'Voltage Conversion Time',

            'name': 'Voltage Conversion Time',
            'type': 'integer',
            'options': [('140µs', 0),
                        ('204µs', 1),
                        ('332µs', 2),
                        ('588µs', 3),
                        ('1.1ms', 4),
                        ('2.116ms', 5),
                        ('4.156ms', 6),
                        ('8.244ms', 7)],
            'limitToOptions': 'true',
            'default': 4,

            'label': 'Voltage Conversion Time',
            'description': 'Configures the voltage conversion time.'
        }, {
             'packet': 'Set Configuration',
            'element': 'Current Conversion Time',

            'name': 'Current Conversion Time',
            'type': 'integer',
            'options': [('140µs', 0),
                        ('204µs', 1),
                        ('332µs', 2),
                        ('588µs', 3),
                        ('1.1ms', 4),
                        ('2.116ms', 5),
                        ('4.156ms', 6),
                        ('8.244ms', 7)],
            'limitToOptions': 'true',
            'default': 4,

            'label': 'Current Conversion Time',
            'description': 'Configures the current conversion time.'
        },
    ],
    'init_code': """this.setConfiguration(cfg.averaging, cfg.voltageConversionTime, cfg.currentConversionTime);""",
    'channels': [
        oh_generic_channel('Current', 'Current', 'SmartHomeUnits.AMPERE', divisor=1000.0),
        oh_generic_channel('Voltage', 'Voltage', 'SmartHomeUnits.VOLT', divisor=1000.0),
        oh_generic_channel('Power', 'Power', 'SmartHomeUnits.WATT', divisor=1000.0)
    ],
    'channel_types': [
        oh_generic_channel_type('Voltage', 'Number:ElectricPotential', 'Measured Voltage',
                    update_style='Callback Configuration',
                    description='The measured voltage between 0 and 36V.',
                    read_only=True,
                    pattern='%.3f %unit%',
                    min_=0,
                    max_=36),
        oh_generic_channel_type('Current', 'Number:ElectricCurrent', 'Measured Current',
                    update_style='Callback Configuration',
                    description='The measured current between -20 and 20A.',
                    read_only=True,
                    pattern='%.3f %unit%',
                    min_=-20,
                    max_=20),
        oh_generic_channel_type('Power', 'Number:Power', 'Measured Power',
                    update_style='Callback Configuration',
                    description='The measured power between 0 and 720W.',
                    read_only=True,
                    pattern='%.3f %unit%',
                    min_=0,
                    max_=720)
    ],
    'actions': ['Get Voltage', 'Get Current', 'Get Power', 'Get Configuration', 'Get Calibration']
}
