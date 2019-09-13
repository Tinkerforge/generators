# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# HAT Zero Brick communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from commonconstants import add_callback_value_function

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'category': 'Brick',
    'device_identifier': 112,
    'name': 'HAT Zero',
    'display_name': 'HAT Zero',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'HAT for Raspberry Pi Zero with 4 Bricklets ports',
        'de': 'HAT für Raspberry Pi Zero mit 4 Bricklet-Ports'
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

voltage_doc = {
'en':
"""
Returns the USB supply voltage of the Raspberry Pi in mV.
""",
'de':
"""
Gibt die USB-Versorgungsspannung des Raspberry Pi in mV zurück.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get USB Voltage',
    data_name = 'Voltage',
    data_type = 'uint16',
    doc       = voltage_doc,
    callback_since_firmware = [2, 0, 1]
)

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get USB Voltage', 'voltage'), [(('Voltage', 'Voltage'), 'uint16', 1, 1000.0, 'V', None)], [])]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'channels': [
        #oh_generic_channel('USB Voltage', 'USB Voltage', 'SmartHomeUnits.VOLT', divisor=1000.0),
        {
            'id': 'USB Voltage',
            'type': 'USB Voltage',
            'init_code':"""this.set{camel}CallbackConfiguration(channelCfg.updateInterval, true, \'x\', 0, 0);""",
            'dispose_code': """this.set{camel}CallbackConfiguration(0, true, \'x\', 0, 0);""",
            'getters': [{
                'packet': 'Get {title_words}',
                'packet_params': [],
                'transform': 'new QuantityType<>(value{divisor}, {unit})'}],

            'callbacks': [{
                'packet': 'USB Voltage',
                'transform': 'new QuantityType<>(voltage{divisor}, {unit})',
                'filter': 'true'}],

            'java_unit': 'SmartHomeUnits.VOLT',
            'divisor': 1000.0,
            'is_trigger_channel': False
    }
    ],
    'channel_types': [
        oh_generic_channel_type('USB Voltage', 'Number:ElectricPotential', 'USB Voltage',
                     description='The USB supply voltage of the Raspberry Pi.',
                     read_only=True,
                     pattern='%.3f %unit%')
    ]
}
