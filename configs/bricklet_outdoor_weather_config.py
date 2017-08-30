# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Outdoor Weather Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

WIND_DIRECTION = ('Wind Direction', [('N', 0),
                                     ('NNE', 1),
                                     ('NE', 2),
                                     ('ENE', 3),
                                     ('E', 4),
                                     ('ESE', 5),
                                     ('SE', 6),
                                     ('SSE', 7),
                                     ('S', 8),
                                     ('SSW', 9),
                                     ('SW', 10),
                                     ('WSW', 11),
                                     ('W', 12),
                                     ('WNW', 13),
                                     ('NW', 14),
                                     ('NNW', 15),
                                     ('Error', 255)])

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 288,
    'name': 'Outdoor Weather',
    'display_name': 'Outdoor Weather',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'TODO',
        'de': 'TODO'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Get Weather Station Identifiers Low Level',
'elements': [('Identifiers Length', 'uint16', 1, 'out'),
             ('Identifiers Chunk Offset', 'uint16', 1, 'out'),
             ('Identifiers Chunk Data', 'uint8', 60, 'out')],
'high_level': {'stream_out': {'name': 'Identifiers'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Weather Station Data',
'elements': [('Identifier', 'uint8', 1, 'in'),
             ('Temperature', 'int16', 1, 'out'),   # in °C/10
             ('Humidity', 'uint8', 1, 'out'),      # in %rel
             ('Wind Speed', 'uint32', 1, 'out'),   # in m/10s
             ('Gust Speed', 'uint32', 1, 'out'),   # in m/10s
             ('Rain', 'uint32', 1, 'out'),         # in mm/10
             ('Wind Direction', 'uint8', 1, 'out', WIND_DIRECTION),
             ('Battery Low', 'bool', 1, 'out'),    # true = battery low
             ('Last Change', 'uint16', 1, 'out')], # in seconds
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Weather Station Callback Configuration',
'elements': [('Enable Callback', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Weather Station Callback Configuration',
'elements': [('Enable Callback', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Weather Station Data',
'elements': [('Identifier', 'uint8', 1, 'out'),
             ('Temperature', 'int16', 1, 'out'),   # in °C/10
             ('Humidity', 'uint8', 1, 'out'),      # in %rel
             ('Wind Speed', 'uint32', 1, 'out'),   # in m/10s
             ('Gust Speed', 'uint32', 1, 'out'),   # in m/10s
             ('Rain', 'uint32', 1, 'out'),         # in mm/10
             ('Wind Direction', 'uint8', 1, 'out', WIND_DIRECTION),
             ('Battery Low', 'bool', 1, 'out')],   # true = battery low
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
Called about every 45 seconds
TODO
""",
'de':
"""
TODO
"""
}]
})
