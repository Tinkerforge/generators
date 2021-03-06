# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# HAT Zero Brick communication config

from generators.configs.commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from generators.configs.commonconstants import add_callback_value_function

from generators.configs.openhab_commonconfig import *

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
        'device',
        'comcu_bricklet',
        'hat_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

voltage_doc = {
'en':
"""
Returns the USB supply voltage of the Raspberry Pi.
""",
'de':
"""
Gibt die USB-Versorgungsspannung des Raspberry Pi zurück.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get USB Voltage',
    data_name = 'Voltage',
    data_type = 'uint16',
    doc       = voltage_doc,
    callback_since_firmware = [2, 0, 1],
    scale     = (1, 1000),
    unit      = 'Volt'
)

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get USB Voltage', 'voltage'), [(('Voltage', 'Voltage'), 'uint16', 1, 1000.0, 'V', None)], [])]
})

usb_voltage_channel = oh_generic_channel('USB Voltage', 'USB Voltage', element_name='Voltage')
usb_voltage_channel['callbacks'][0]['transform'] = 'new {number_type}(voltage{divisor}{unit})'

com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'channels': [usb_voltage_channel],
    'channel_types': [
        oh_generic_channel_type('USB Voltage', 'Number:ElectricPotential', 'USB Voltage',
                    update_style='Callback Configuration',
                    description='The USB supply voltage of the Raspberry Pi.')
    ],
    'actions': ['Get USB Voltage']
}
