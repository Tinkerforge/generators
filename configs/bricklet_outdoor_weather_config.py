# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Outdoor Weather Bricklet communication config

from openhab_common import *

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

com['constant_groups'].append({
'name': 'Wind Direction',
'type': 'uint8',
'constants': [('N', 0),
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
              ('Error', 255)]
})

com['packets'].append({
'type': 'function',
'name': 'Get Station Identifiers Low Level',
'elements': [('Identifiers Length', 'uint16', 1, 'out', {'range': (0, 256)}),
             ('Identifiers Chunk Offset', 'uint16', 1, 'out', {}),
             ('Identifiers Chunk Data', 'uint8', 60, 'out', {})],
'high_level': {'stream_out': {'name': 'Identifiers'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the identifiers (number between 0 and 255) of all `stations
<https://www.tinkerforge.com/en/shop/accessories/sensors/outdoor-weather-station-ws-6147.html>`__
that have been seen since the startup of the Bricklet.

Each station gives itself a random identifier on first startup.

Since firmware version 2.0.2 a station is removed from the list if no data was received for
12 hours.
""",
'de':
"""
Gibt die Identifier (Zahl zwischen 0 und 255) von allen 'Stationen
<https://www.tinkerforge.com/de/shop/accessories/sensors/outdoor-weather-station-ws-6147.html>`__
die seit dem Start des Bricklets entdeckt wurden.

Jede Station gibt sich selbst einen zufälligen Identifier beim ersten Start.

Seit Firmware-Version 2.0.2 wird eine Station von der Liste wieder entfernt wenn für 12
Stunden am Stück keine Daten empfangen werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Sensor Identifiers Low Level',
'elements': [('Identifiers Length', 'uint16', 1, 'out', {'range': (0, 256)}),
             ('Identifiers Chunk Offset', 'uint16', 1, 'out'),
             ('Identifiers Chunk Data', 'uint8', 60, 'out')],
'high_level': {'stream_out': {'name': 'Identifiers'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the identifiers (number between 0 and 255) of all `sensors
<https://www.tinkerforge.com/en/shop/accessories/sensors/temperature-humidity-sensor-th-6148.html>`__
that have been seen since the startup of the Bricklet.

Each sensor gives itself a random identifier on first startup.

Since firmware version 2.0.2 a sensor is removed from the list if no data was received for
12 hours.
""",
'de':
"""
Gibt die Identifier (Zahl zwischen 0 und 255) von allen 'Sensoren
<https://www.tinkerforge.com/en/shop/accessories/sensors/temperature-humidity-sensor-th-6148.html>`__
die seit dem Start des Bricklets entdeckt wurden.

Jede Sensor gibt sich selbst einen zufälligen Identifier beim ersten Start.

Seit Firmware-Version 2.0.2 wird ein Sensor von der Liste wieder entfernt wenn für 12
Stunden am Stück keine Daten empfangen werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Station Data',
'elements': [('Identifier', 'uint8', 1, 'in', {}),
             ('Temperature', 'int16', 1, 'out', {'scale': (1, 10), 'unit': 'Degree Celsius', 'range': (-400, 650)}),
             ('Humidity', 'uint8', 1, 'out', {'unit': 'Percent Relative Humidity', 'range': (10, 99)}),
             ('Wind Speed', 'uint32', 1, 'out', {'scale': (1, 10), 'unit': 'Meter Per Second'}),
             ('Gust Speed', 'uint32', 1, 'out', {'scale': (1, 10), 'unit': 'Meter Per Second'}),
             ('Rain', 'uint32', 1, 'out', {'scale': (1, 10), 'unit': 'Millimeter'}),
             ('Wind Direction', 'uint8', 1, 'out', {'constant_group': 'Wind Direction'}),
             ('Battery Low', 'bool', 1, 'out', {}),
             ('Last Change', 'uint16', 1, 'out', {'unit': 'Second'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the last received data for a station with the given identifier.
Call :func:`Get Station Identifiers` for a list of all available identifiers.

The return values are:

* Temperature,
* Humidity,
* Wind Speed,
* Gust Speed,
* Rain Fall,
* Wind Direction,
* Battery Low (true if battery is low) and
* Last Change (time since the reception of this data).
""",
'de':
"""
Gibt die zuletzt empfangenen Daten für die Station mit dem entsprechenden
Identifier zurück.

Die Rückgabewerte sind:

* Temperatur,
* Luftfeuchte,
* Windgeschwindigkeit,
* Windböengeschwindigkeit,
* Niederschlag,
* Windrichtung,
* Batteriewarnung (true wenn der Batteriestand niedrig) und
* Letzte Änderung (Zeit seitdem diese Daten empfangen wurden).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Sensor Data',
'elements': [('Identifier', 'uint8', 1, 'in', {}),
             ('Temperature', 'int16', 1, 'out', {'scale': (1, 10), 'unit': 'Degree Celsius'}),
             ('Humidity', 'uint8', 1, 'out', {'unit': 'Percent Relative Humidity'}),
             ('Last Change', 'uint16', 1, 'out', {'unit': 'Second'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the last measured data for a sensor with the given identifier.
Call :func:`Get Sensor Identifiers` for a list of all available identifiers.

The return values are:

* Temperature,
* Humidity and
* Last Change (time since the last reception of data).
""",
'de':
"""
Gibt die zuletzt empfangenen Daten für den Sensor mit dem entsprechenden
Identifier zurück.

Die Rückgabewerte sind:

* Temperatur,
* Luftfeuchte und
* Letzte Änderung (Zeit seitdem diese Daten empfangen wurden).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Station Callback Configuration',
'elements': [('Enable Callback', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Turns callback for station data on or off.
""",
'de':
"""
Aktiviert/Deaktiviert den Callback für Stationsdaten.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Station Callback Configuration',
'elements': [('Enable Callback', 'bool', 1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the configuration as set by :func:`Set Station Callback Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück wie von :func:`Set Station Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Sensor Callback Configuration',
'elements': [('Enable Callback', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Turns callback for sensor data on or off.
""",
'de':
"""
Aktiviert/Deaktiviert den Callback für Sensordaten.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Sensor Callback Configuration',
'elements': [('Enable Callback', 'bool', 1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the configuration as set by :func:`Set Sensor Callback Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück wie von :func:`Set Sensor Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Station Data',
'elements': [('Identifier', 'uint8', 1, 'out', {}),
             ('Temperature', 'int16', 1, 'out', {'scale': (1, 10), 'unit': 'Degree Celsius', 'range': (-400, 650)}),
             ('Humidity', 'uint8', 1, 'out', {'unit': 'Percent Relative Humidity', 'range': (10, 99)}),
             ('Wind Speed', 'uint32', 1, 'out', {'scale': (1, 10), 'unit': 'Meter Per Second'}),
             ('Gust Speed', 'uint32', 1, 'out', {'scale': (1, 10), 'unit': 'Meter Per Second'}),
             ('Rain', 'uint32', 1, 'out', {'scale': (1, 10), 'unit': 'Millimeter'}),
             ('Wind Direction', 'uint8', 1, 'out', {'constant_group': 'Wind Direction'}),
             ('Battery Low', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
Reports the station data every time a new data packet is received.
See :func:`Get Station Data` for information about the data.

For each station the callback will be triggered about every 45 seconds.

Turn the callback on/off with :func:`Set Station Callback Configuration`
(by default it is turned off).
""",
'de':
"""
Meldet die Stationsdaten bei jedem eingehenden Datenpaket. Siehe
:func:`Get Station Data` für Details über die Daten.

Für jede Station wird dieser Callback ca. alle 45 Sekunden ausgelöst werden.

Der Callback kann mittels :func:`Set Station Callback Configuration`
aktiviert/deaktiviert werden (standardmäßig ist der Callback deaktiviert).
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Sensor Data',
'elements': [('Identifier', 'uint8', 1, 'out', {}),
             ('Temperature', 'int16', 1, 'out', {'scale': (1, 10), 'unit': 'Degree Celsius'}),
             ('Humidity', 'uint8', 1, 'out', {'unit': 'Percent Relative Humidity'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
Reports the sensor data every time a new data packet is received.
See :func:`Get Sensor Data` for information about the data.

For each sensor the callback will be called about every 45 seconds.

Turn the callback on/off with :func:`Set Sensor Callback Configuration`
(by default it is turned off).
""",
'de':
"""
Meldet die Sensordaten bei jedem eingehenden Datenpaket. Siehe
:func:`Get Sensor Data` für Details über die Daten.

Für jeden Sensor wird dieser Callback ca. alle 45 Sekunden ausgelöst werden.

Der Callback kann mittels :func:`Set Sensor Callback Configuration`
aktiviert/deaktiviert werden (standardmäßig ist der Callback deaktiviert).
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
                (('Wind Direction', 'Wind Direction (Station)'), 'uint8:constant', 1, None, None, None), # FIXME: print as constant
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

com['openhab'] = {
    'custom': True
}
