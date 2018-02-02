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
        'en': '433MHz receiver for outdoor weather station',
        'de': '433MHz Empfänger für Außen-Wetterstation'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'discontinued': False,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Get Station Identifiers Low Level',
'elements': [('Identifiers Length', 'uint16', 1, 'out'),
             ('Identifiers Chunk Offset', 'uint16', 1, 'out'),
             ('Identifiers Chunk Data', 'uint8', 60, 'out')],
'high_level': {'stream_out': {'name': 'Identifiers'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the identifiers (number betwen 0 and 255) of all `stations <TBD>`__ that have been seen
since the startup of the Bricklet.

Each station gives itself a random identifier on first startup.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Sensor Identifiers Low Level',
'elements': [('Identifiers Length', 'uint16', 1, 'out'),
             ('Identifiers Chunk Offset', 'uint16', 1, 'out'),
             ('Identifiers Chunk Data', 'uint8', 60, 'out')],
'high_level': {'stream_out': {'name': 'Identifiers'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the Identifiers (number between 0 and 255) of all `sensors <TBD>`__ that have been seen
since the startup of the Bricklet.

Each sensor gives itself a random identifier on first startup.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Station Data',
'elements': [('Identifier', 'uint8', 1, 'in'),
             ('Temperature', 'int16', 1, 'out'),   # in °C/10
             ('Humidity', 'uint8', 1, 'out'),      # in %RH
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
Returns the last measured data for a station with the given identifier.
Call :func:`Get Station Identifiers` for a list of all available identifiers.

The return values are

* Temperature in °C/10,
* Humidity in %RH,
* Wind Speed in m/10s,
* Gust Speed in m/10s,
* Rain Fall in mm/10,
* Wind Direction (N, NNE, NE, ENE, E, ESE, SE, SSE, S, SSW, SW, WSW, W, WNW, NW, NNW),
* Battery Low (true or false) and
* Last Change (time in seconds since the last reception of data).

""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Sensor Data',
'elements': [('Identifier', 'uint8', 1, 'in'),
             ('Temperature', 'int16', 1, 'out'),   # in °C/10
             ('Humidity', 'uint8', 1, 'out'),      # in %RH
             ('Last Change', 'uint16', 1, 'out')], # in seconds
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the last measured data for a sensor with the given identifier.
Call :func:`Get Sensor Identifiers` for a list of all available identifiers.

The return values are

* Temperature in °C/10,
* Humidity in %RH and
* Last Change (time in seconds since the last reception of data).

""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Station Callback Configuration',
'elements': [('Enable Callback', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Turns callback for station data on or off. Default is off.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Station Callback Configuration',
'elements': [('Enable Callback', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the configuration as set by :func:`Set Station Callback Configuration`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Sensor Callback Configuration',
'elements': [('Enable Callback', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Turns callback for sensor data on or off. Default is off.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Sensor Callback Configuration',
'elements': [('Enable Callback', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the configuration as set by :func:`Set Sensor Callback Configuration`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Station Data',
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
Returns the station data every time a new data packet is received.
See :func:`Get Station Data` for information about the data.

For each station the callback will be called about every 45 seconds.

Turn the callback on/off with :func:`Set Station Callback Configuration` (by default it is turned off).
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Sensor Data',
'elements': [('Identifier', 'uint8', 1, 'out'),
             ('Temperature', 'int16', 1, 'out'),   # in °C/10
             ('Humidity', 'uint8', 1, 'out')],     # in %rel
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
Returns the sensor data every time a new data packet is received.
See :func:`Get Sensor Data` for information about the data.

For each station the callback will be called about every 45 seconds.

Turn the callback on/off with :func:`Set Sensor Callback Configuration` (by default it is turned off).
""",
'de':
"""
TODO
"""
}]
})

com['examples'].append({
'name': 'Callback',
'functions': [('setter', 'Set Station Callback Configuration', [('bool', True)], 'Enable station data callbacks', None),
              ('setter', 'Set Sensor Callback Configuration', [('bool', True)], 'Enable sensor data callbacks', None),
              ('callback', ('Station Data', 'station data'),
              [
                (('Identifier', 'Identifier (Station)'), 'uint8', 1, None, None, None),
                (('Temperature', 'Temperature (Station)'), 'int16', 1, 10.0, '°C', None),
                (('Humidity', 'Humidity (Station)'), 'uint8', 1, None, '%RH', None),
                (('Wind Speed', 'Wind Speed (Station)'), 'uint32', 1, 10.0, 'm/s', None),
                (('Gust Speed', 'Gust Speed (Station)'), 'uint32', 1, 10.0, 'm/s', None),
                (('Rain', 'Rain (Station)'), 'uint32', 1, 10.0, 'mm', None),
                (('Wind Direction', 'Wind Direction (Station)'), 'uint8', 1, None, None, None), # FIXME: print as constant
                (('Battery Low', 'Battery Low (Station)'), 'bool', 1, None, None, None)
              ],
              None, None),
              ('callback', ('Sensor Data', 'sensor data'),
              [
                (('Identifier', 'Identifier (Sensor)'), 'uint8', 1, None, None, None),
                (('Temperature', 'Temperature (Sensor)'), 'int16', 1, 10.0, '°C', None),
                (('Humidity', 'Humidity (Sensor)'), 'uint8', 1, None, '%RH', None)
              ],
              None, None)]
})
