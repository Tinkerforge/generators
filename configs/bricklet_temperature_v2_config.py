# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Temperature Bricklet 2.0 communication config

from generators.configs.commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from generators.configs.commonconstants import add_callback_value_function

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2113,
    'name': 'Temperature V2',
    'display_name': 'Temperature 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures ambient temperature with 0.2°C accuracy',
        'de': 'Misst Umgebungstemperatur mit 0,2°C Genauigkeit'
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
'name': 'Heater Config',
'type': 'uint8',
'constants': [('Disabled', 0),
              ('Enabled',  1)]
})

temperature_doc = {
'en':
"""
Returns the temperature measured by the sensor.
""",
'de':
"""
Gibt die gemessene Temperatur des Sensors zurück.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Temperature',
    data_name = 'Temperature',
    data_type = 'int16',
    doc       = temperature_doc,
    scale     = (1, 100),
    unit      = 'Degree Celsius',
    range_    = (-4500, 13000)
)

com['packets'].append({
'type': 'function',
'name': 'Set Heater Configuration',
'elements': [('Heater Config', 'uint8', 1, 'in', {'constant_group': 'Heater Config', 'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Enables/disables the heater. The heater can be used to test the sensor.
""",
'de':
"""
Aktiviert/deaktiviert das Heizelement. Das Heizelement kann genutzt werden
um den Sensor zu testen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Heater Configuration',
'elements': [('Heater Config', 'uint8', 1, 'out', {'constant_group': 'Heater Config'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the heater configuration as set by :func:`Set Heater Configuration`.
""",
'de':
"""
Gibt die Heizelement-Konfiguration zurück, wie von :func:`Set Heater Configuration` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Temperature', 'temperature'), [(('Temperature', 'Temperature'), 'int16', 1, 100.0, '°C', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Temperature', 'temperature'), [(('Temperature', 'Temperature'), 'int16', 1, 100.0, '°C', None)], None, None),
              ('callback_configuration', ('Temperature', 'temperature'), [], 1000, False, 'x', [(0, 0)])]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('callback', ('Temperature', 'temperature'), [(('Temperature', 'Temperature'), 'int16', 1, 100.0, '°C', None)], None, 'It is too hot, we need air conditioning!'),
              ('callback_configuration', ('Temperature', 'temperature'), [], 1000, False, '>', [(30, 0)])]
})


com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.OnOffType'],
    'param_groups': oh_generic_channel_param_groups(),
    'channels': [
        oh_generic_channel('Temperature', 'Temperature'),
        {
            'id': 'Heater',
            'type': 'Heater',

            'setters': [{
                'packet': 'Set Heater Configuration',
                'element': 'Heater Config',
                'packet_params': ['cmd == OnOffType.ON ? BrickletTemperatureV2.HEATER_CONFIG_ENABLED : BrickletTemperatureV2.HEATER_CONFIG_DISABLED'],
                'command_type': "OnOffType"
            }],

            'getters': [{
                'packet': 'Get Heater Configuration',
                'element': 'Heater Config',
                'transform': 'value == BrickletTemperatureV2.HEATER_CONFIG_ENABLED ? OnOffType.ON : OnOffType.OFF'}]
        }
    ],
    'channel_types': [
        oh_generic_channel_type('Temperature', 'Number', 'Temperature',
                    update_style='Callback Configuration',
                    description='The measured temperature'),
        oh_generic_channel_type('Heater', 'Switch', 'Heater',
                    update_style=None,
                    description='Enables/disables the heater. The heater can be used to dry the sensor in extremely wet conditions.'),
    ],
    'actions': ['Get Temperature', {'fn': 'Set Heater Configuration', 'refreshs': ['Heater']}, 'Get Heater Configuration']
}
