# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Counter Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 293,
    'name': 'Industrial Counter',
    'display_name': 'Industrial Counter',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'TBD',
        'de': 'TBD'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'discontinued': False,
    'packets': [],
    'examples': []
}

CONSTANT_PIN = ('PIN', [('0', 0),
                        ('1', 1),
                        ('2', 2),
                        ('3', 3)])

CONSTANT_COUNT_EDGE = ('Count Edge', [('Rising', 0),
                                      ('Falling', 1),
                                      ('Both', 2)])

CONSTANT_COUNT_DIRECTON = ('Count Direction', [('Up', 0),
                                               ('Down', 1),
                                               ('External Up', 2),
                                               ('External Down', 3)])

CONSTANT_DUTY_CYCLE_PRESCALER = ('Duty Cycle Prescaler', [('1', 0),
                                                          ('2', 1),
                                                          ('4', 2),
                                                          ('8', 3),
                                                          ('16', 4),
                                                          ('32', 5),
                                                          ('64', 6),
                                                          ('128', 7),
                                                          ('256', 8),
                                                          ('512', 9),
                                                          ('1024', 10),
                                                          ('2048', 11),
                                                          ('4096', 12),
                                                          ('8192', 13),
                                                          ('16384', 14),
                                                          ('32768', 15),
                                                          ('Auto', 255)])

CONSTANT_FREQUENCY_INTEGRATION_TIME = ('Frequency Integration Time', [('128 MS', 0),
                                                                      ('256 MS', 1),
                                                                      ('512 MS', 2),
                                                                      ('1024 MS', 3),
                                                                      ('2048 MS', 4),
                                                                      ('4096 MS', 5),
                                                                      ('8192 MS', 6),
                                                                      ('16384 MS', 7),
                                                                      ('32768 MS', 8),
                                                                      ('Auto', 255)])



com['packets'].append({
'type': 'function',
'name': 'Get Counter',
'elements': [('Pin', 'uint8', 1, 'in', CONSTANT_PIN),
             ('Counter', 'int64', 1, 'out')],
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
'name': 'Get All Counter',
'elements': [('Counter', 'int64', 4, 'out')],
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
'name': 'Set Counter',
'elements': [('Pin', 'uint8', 1, 'in', CONSTANT_PIN),
             ('Counter', 'int64', 1, 'in')],
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
'name': 'Set All Counter',
'elements': [('Counter', 'int64', 4, 'in')],
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
'name': 'Get Signal Data',
'elements': [('Pin', 'uint8', 1, 'in', CONSTANT_PIN),
             ('Duty Cycle', 'uint16', 1, 'out'),
             ('Period', 'uint64', 1, 'out'),
             ('Frequency', 'uint32', 1, 'out'),
             ('Pin Value', 'bool', 1, 'out')],
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
'name': 'Get All Signal Data',
'elements': [('Duty Cycle', 'uint16', 4, 'out'),
             ('Period', 'uint64', 4, 'out'),
             ('Frequency', 'uint32', 4, 'out'),
             ('Pin Value', 'bool', 4, 'out')],
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
'name': 'Set Counter Active',
'elements': [('Pin', 'uint8', 1, 'in', CONSTANT_PIN),
             ('Active', 'bool', 1, 'in')],
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
'name': 'Set All Counter Active',
'elements': [('Active', 'bool', 4, 'in')],
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
'name': 'Get Counter Active',
'elements': [('Pin', 'uint8', 1, 'in', CONSTANT_PIN),
             ('Active', 'bool', 1, 'out')],
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
'name': 'Get All Counter Active',
'elements': [('Active', 'bool', 4, 'out')],
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
'name': 'Set Counter Configuration',
'elements': [('Pin', 'uint8', 1, 'in', CONSTANT_PIN),
             ('Count Edge', 'uint8', 1, 'in', CONSTANT_COUNT_EDGE),
             ('Count Direction', 'uint8', 1, 'in', CONSTANT_COUNT_DIRECTON),
             ('Duty Cycle Prescaler', 'uint8', 1, 'in', CONSTANT_DUTY_CYCLE_PRESCALER),
             ('Frequency Integration Time', 'uint8', 1, 'in', CONSTANT_FREQUENCY_INTEGRATION_TIME)],
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
'name': 'Get Counter Configuration',
'elements': [('Pin', 'uint8', 1, 'in', CONSTANT_PIN),
             ('Count Edge', 'uint8', 1, 'out', CONSTANT_COUNT_EDGE),
             ('Count Direction', 'uint8', 1, 'out', CONSTANT_COUNT_DIRECTON),
             ('Duty Cycle Prescaler', 'uint8', 1, 'out', CONSTANT_DUTY_CYCLE_PRESCALER),
             ('Frequency Integration Time', 'uint8', 1, 'out', CONSTANT_FREQUENCY_INTEGRATION_TIME)],
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
'name': 'Set All Counter Callback Configuration',
#'corresponding_getter': 'Get All Counter' ,
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get All Counter Callback Configuration',
#'corresponding_getter': 'Get All Counter',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set All Signal Data Callback Configuration',
#'corresponding_getter': 'Get All Signal Data' ,
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get All Signal Data Callback Configuration',
#'corresponding_getter': 'Get All Signal Data',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

# TODO: Documentation

com['packets'].append({
'type': 'function',
'name': 'Set Channel LED Config',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Config', 'uint8', 1, 'in', ('Channel LED Config', [('Off', 0),
                                                                  ('On', 1),
                                                                  ('Show Heartbeat', 2),
                                                                  ('Show Channel Status', 3)]))],
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
'name': 'Get Channel LED Config',
'elements': [('LED', 'uint8', 1, 'in'),
             ('Config', 'uint8', 1, 'out', ('Channel LED Config', [('Off', 0),
                                                                   ('On', 1),
                                                                   ('Show Heartbeat', 2),
                                                                   ('Show Channel Status', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the Channel LED configuration as set by :func:`Set Channel LED Config`
""",
'de':
"""
Gibt die LED-Konfiguration zurück, wie von :func:`Set Channel LED Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'All Counter',
#'corresponding_getter': 'Get All Counter',
'elements': [('Counter', 'int64', 4, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'All Signal Data',
#'corresponding_getter': 'Get All Signal Data',
'elements': [('Duty Cycle', 'uint16', 4, 'out'),
             ('Period', 'uint64', 4, 'out'),
             ('Frequency', 'uint32', 4, 'out'),
             ('Pin Value', 'bool', 4, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
""",
'de':
"""
"""
}]
})


