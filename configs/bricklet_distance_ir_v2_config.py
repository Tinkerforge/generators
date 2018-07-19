# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Distance IR Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2125,
    'name': 'Distance IR V2',
    'display_name': 'Distance IR 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures distance up to 150cm with infrared light',
        'de': 'Misst Entfernung bis zu 150cm mit Infrarot-Licht'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'discontinued': False,
    'packets': [],
    'examples': []
}


distance_doc = {
'en':
"""
Returns the distance measured by the sensor. The value is in mm and possible
distance ranges are 40 to 300, 100 to 800 and 200 to 1500, depending on the
selected IR sensor.
""",
'de':
"""
Gibt die gemessene Entfernung des Sensors zurück. Der Wert ist in mm und die möglichen
Entfernungsbereiche sind 40 bis 300, 100 bis 800 und 200 bis 1500, in Abhängigkeit vom
gewählten IR Sensor.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Distance',
    data_name = 'Distance',
    data_type = 'uint16',
    doc       = distance_doc
)
