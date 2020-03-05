# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Humidity Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from commonconstants import add_callback_value_function

from openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 2],
    'api_version_extra': 1, # +1 for "Fix min/max types in add_callback_value_function logic [aff5bfc]"
    'category': 'Bricklet',
    'device_identifier': 283,
    'name': 'Humidity V2',
    'display_name': 'Humidity 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures relative humidity',
        'de': 'Misst relative Luftfeuchtigkeit'
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
              ('Enabled', 1)]
})

com['constant_groups'].append({
'name': 'SPS',
'type': 'uint8',
'constants': [('20', 0),
              ('10', 1),
              ('5', 2),
              ('1', 3),
              ('02', 4),
              ('01', 5)]
})

humidity_doc = {
'en':
"""
Returns the humidity measured by the sensor.
""",
'de':
"""
Gibt die gemessene Luftfeuchtigkeit des Sensors zurück.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Humidity',
    data_name = 'Humidity',
    data_type = 'uint16',
    doc       = humidity_doc,
    scale     = (1, 100),
    unit      = 'Percent Relative Humidity',
    range_    = (0, 10000)
)

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
    range_    = (-4000, 16500)
)

com['packets'].append({
'type': 'function',
'name': 'Set Heater Configuration',
'elements': [('Heater Config', 'uint8', 1, 'in', {'constant_group': 'Heater Config', 'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Enables/disables the heater. The heater can be used to dry the sensor in
extremely wet conditions.
""",
'de':
"""
Aktiviert/deaktiviert das Heizelement. Das Heizelement kann genutzt werden
um den Sensor bei extremer Feuchtigkeit zu trocknen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Heater Configuration',
'elements': [('Heater Config', 'uint8', 1, 'out', {'constant_group': 'Heater Config', 'default': False})],
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

com['packets'].append({
'type': 'function',
'name': 'Set Moving Average Configuration',
'elements': [('Moving Average Length Humidity', 'uint16', 1, 'in', {'range': (1, 1000), 'default': 5}),
             ('Moving Average Length Temperature', 'uint16', 1, 'in', {'range': (1, 1000), 'default': 5})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
for the humidity and temperature.

Setting the length to 1 will turn the averaging off. With less
averaging, there is more noise on the data.

New data is gathered every 50ms*. With a moving average of length 1000 the resulting
averaging window has a length of 50s. If you want to do long term measurements the longest
moving average will give the cleanest results.

\* In firmware version 2.0.3 we added the :func:`Set Samples Per Second` function. It
configures the measurement frequency. Since high frequencies can result in self-heating
of th IC, changed the default value from 20 samples per second to 1. With 1 sample per second
a moving average length of 1000 would result in an averaging window of 1000 seconds!
""",
'de':
"""
Setzt die Länge eines `gleitenden Mittelwerts <https://de.wikipedia.org/wiki/Gleitender_Mittelwert>`__
für die Luftfeuchtigkeit und Temperatur.

Wenn die Länge auf 1 gesetzt wird, ist die Mittelwertbildung deaktiviert.
Je kürzer die Länge des Mittelwerts ist, desto mehr Rauschen ist auf den Daten.

Einer neue Wert wird alle 50ms* gemessen. Mit einer Mittelwerts-Länge von 1000 hat das
resultierende gleitende Fenster eine Zeitspanne von 50s. Bei Langzeitmessungen gibt
ein langer Mittelwert die saubersten Resultate.

\* In Firmware Version 2.0.3 haben wir die Funktion :func:`Set Samples Per Second`
hinzugefügt. Diese konfiguriert die Messfrequenz. Da eine hohe Messfrequenz zu
Selbsterhitzung führen kann haben wir die Standardeinstellung von 20 SPS auf 1 SPS
geändert. Mit einer Messung pro Sekunde entspricht eine Mittelwert-Länge von 1000
einem Zeitfenster von 1000 Sekunden!
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Moving Average Configuration',
'elements': [('Moving Average Length Humidity', 'uint16', 1, 'out', {'range': (1, 1000), 'default': 5}),
             ('Moving Average Length Temperature', 'uint16', 1, 'out', {'range': (1, 1000), 'default': 5})],

'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the moving average configuration as set by :func:`Set Moving Average Configuration`.
""",
'de':
"""
Gibt die Moving Average-Konfiguration zurück, wie von :func:`Set Moving Average Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Samples Per Second',
'elements': [('SPS', 'uint8', 1, 'in', {'constant_group': 'SPS', 'default': 3})],
'since_firmware': [2, 0, 3],
'doc': ['bf', {
'en':
"""
Sets the samples per second that are gathered by the humidity/temperature sensor HDC1080.

We added this function since we found out that a high measurement frequency can lead to
self-heating of the sensor. Which can distort the temperature measurement.

If you don't need a lot of measurements, you can use the lowest available measurement
frequency of 0.1 samples per second for the least amount of self-heating.

Before version 2.0.3 the default was 20 samples per second. The new default is 1 sample per second.
""",
'de':
"""
Setzt die Messungen pro Sekunde mit denen neue Luftfeuchte/Temperatur-Werte vom
HDC1080 Sensor gelesen werden.

Wir haben diese Funktion hinzugefügt, da eine hohe Messfrequenz zu einer Selbsterhitzung
des Sensors führen kann. Diese kann die Temperaturmessung verfälschen.

Wenn wenig Messwerte benötigt werden kann die Frequenz auf bis zu 0,1 Messungen pro
Sekunde verringert werden um einen Fehler durch Selbsterhitzung möglichst weit zu
minimieren.

Vor Version 2.0.3 wurden 20 Messungen pro Sekunde gemacht. Der neue Standardwert seit
2.0.3 ist 1 Messung pro Sekunde.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Samples Per Second',
'elements': [('SPS', 'uint8', 1, 'out', {'constant_group': 'SPS', 'default': 3})],
'since_firmware': [2, 0, 3],
'doc': ['bf', {
'en':
"""
Returnes the samples per second, as set by :func:`Set Samples Per Second`.
""",
'de':
"""
Gibt die Messwerte pro Sekunde zurück, wie von :func:`Set Samples Per Second` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Humidity', 'humidity'), [(('Humidity', 'Humidity'), 'uint16', 1, 100.0, '%RH', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Humidity', 'humidity'), [(('Humidity', 'Humidity'), 'uint16', 1, 100.0, '%RH', None)], None, None),
              ('callback_configuration', ('Humidity', 'humidity'), [], 1000, False, 'x', [(0, 0)])]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('callback', ('Humidity', 'humidity'), [(('Humidity', 'Humidity'), 'uint16', 1, 100.0, '%RH', None)], None, 'Recommended humidity for human comfort is 30 to 60 %RH.'),
              ('callback_configuration', ('Humidity', 'humidity'), [], 10000, False, 'o', [(30, 60)])]
})




com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.OnOffType'],
    'param_groups': oh_generic_channel_param_groups() +  [{
        'name': 'average',
        'label': 'Averaging',
        'description': 'Sets the length of a moving averaging for the humidity and temperature.<br/><br/>Setting the length to 1 will turn the averaging off. With less averaging, there is more noise on the data.<br/><br/>The range for the averaging is 1-1000.<br/><br/>New data is gathered every 50ms*. With a moving average of length 1000 the resulting averaging window has a length of 50s. If you want to do long term measurements the longest moving average will give the cleanest results.<br/><br/>The default value is 5.<br/><br/>* In firmware version 2.0.3 we added the setSamplesPerSecond() function. It configures the measurement frequency. Since high frequencies can result in self-heating of th IC, changed the default value from 20 samples per second to 1. With 1 sample per second a moving average length of 1000 would result in an averaging window of 1000 seconds!',
        'advanced': 'true'
    }],
    'params': [
        {
            'packet': 'Set Moving Average Configuration',
            'element': 'Moving Average Length Humidity',

            'name': 'Humidity Moving Average Length',
            'type': 'integer',
            'default': 5,
            'min': 1,
            'max': 1000,

            'label': 'Humidity Moving Average Length',
            'groupName': 'average'
        },
        {
            'packet': 'Set Moving Average Configuration',
            'element': 'Moving Average Length Temperature',

            'name': 'Temperature Moving Average Length',
            'type': 'integer',
            'default': 5,
            'min': 1,
            'max': 1000,

            'label': 'Temperature Moving Average Length',
            'groupName': 'average'
        },
        {
            'packet': 'Set Samples Per Second',
            'element': 'SPS',

            'name': 'Sample Rate',
            'type': 'integer',
            'options': [('20 SPS', 0),
                        ('10 SPS', 1),
                        ('5 SPS',  2),
                        ('1 SPS',  3),
                        ('0.2 SPS', 4),
                        ('0.1 SPS', 5)],
            'limit_to_options': 'true',
            'default': 3,

            'label': 'Sample Rate',
            'description': "The samples per second that are gathered by the humidity/temperature sensor HDC1080.<br/><br/>We added this function since we found out that a high measurement frequency can lead to self-heating of the sensor. Which can distort the temperature measurement.<br/><br/>If you don't need a lot of measurements, you can use the lowest available measurement frequency of 0.1 samples per second for the least amount of self-heating.",
        }
    ],
    'init_code': """this.setSamplesPerSecond(cfg.sampleRate);
this.setMovingAverageConfiguration(cfg.humidityMovingAverageLength, cfg.temperatureMovingAverageLength);""",
    'channels': [
        oh_generic_channel('Humidity', 'Humidity', 'SmartHomeUnits.PERCENT', divisor=100.0),
        oh_generic_channel('Temperature', 'Temperature', 'SIUnits.CELSIUS', divisor=100.0),
        {
            'id': 'Heater',
            'type': 'Heater',

            'setters': [{
                'packet': 'Set Heater Configuration',
                'packet_params': ['cmd == OnOffType.ON ? BrickletHumidityV2.HEATER_CONFIG_ENABLED : BrickletHumidityV2.HEATER_CONFIG_DISABLED'],
                'command_type': "OnOffType",
            }],


            'getters': [{
                'packet': 'Get Heater Configuration',
                'transform': 'value == BrickletHumidityV2.HEATER_CONFIG_ENABLED ? OnOffType.ON : OnOffType.OFF'}]
        }
    ],
    'channel_types': [
        oh_generic_channel_type('Humidity', 'Number:Dimensionless', 'Humidity',
                    update_style='Callback Configuration',
                    description='Measured relative humidity',
                    read_only=True,
                    pattern='%.2f %%',
                    min_=0,
                    max_=100),
        oh_generic_channel_type('Temperature', 'Number:Temperature', 'Temperature',
                    update_style='Callback Configuration',
                    description='Measured temperature',
                    read_only=True,
                    pattern='%.2f %unit%',
                    min_=-40,
                    max_=165),
        oh_generic_channel_type('Heater', 'Switch', 'Heater',
                    update_style=None,
                    description='Enables/disables the heater. The heater can be used to dry the sensor in extremely wet conditions.'),
    ],
    'actions': ['Get Humidity', 'Get Temperature', {'fn': 'Set Heater Configuration', 'refreshs': ['Heater']}, 'Get Heater Configuration', 'Get Moving Average Configuration', 'Get Samples Per Second']
}
