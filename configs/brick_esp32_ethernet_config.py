# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# ESP32 Ethernet Brick communication config

com = {
    'author': 'Matthias Bolte <matthias@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Brick',
    'device_identifier': 115,
    'name': 'ESP32 Ethernet',
    'display_name': 'ESP32 Ethernet',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'ESP32 microcontroller based Brick with Ethernet and 6 Bricklet ports',
        'de': 'ESP32 Mikrocontroller basierter Brick mit Ethernet und 6 Bricklet-Ports'
    },
    'released': True,
    'documented': True,
    'discontinued': False,
    'esp32_firmware': 'esp32_ethernet',
    'features': [
        'device',
        'brick_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}
