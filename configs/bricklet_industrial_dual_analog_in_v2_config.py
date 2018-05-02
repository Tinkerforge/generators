# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Dual 0-20mA 2.0 Bricklet communication config

# TODO: Documentation.

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

com = {
    'author': 'Ishraq Ibne Ashraf <ishraq@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2121,
    'name': 'Industrial Dual Analog In V2',
    'display_name': 'Industrial Dual Analog In 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures two DC voltages between -35V and +35V with 24bit resolution each',
        'de': 'Misst zwei Gleichspannungen zwischen -35V und +35V mit jeweils 24Bit Auflösung'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'discontinued': False,
    'packets': [],
    'examples': []
}

voltage_doc = {
'en':
"""
Returns the voltage for the given channel in mV.
""",
'de':
"""
Gibt die Spannung für den übergebenen Kanal in mV zurück.
"""
}

add_callback_value_function(
    packets       = com['packets'],
    name          = 'Get Voltage',
    data_name     = 'Voltage',
    data_type     = 'int32',
    channel_based = True,
    doc           = voltage_doc
)

com['packets'].append({
'type': 'function',
'name': 'Set Sample Rate',
'elements': [('Rate', 'uint8', 1, 'in', ('Sample Rate', [('976 SPS', 0),
                                                         ('488 SPS', 1),
                                                         ('244 SPS', 2),
                                                         ('122 SPS', 3),
                                                         ('61 SPS', 4),
                                                         ('4 SPS', 5),
                                                         ('2 SPS', 6),
                                                         ('1 SPS', 7)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the sample rate. The sample rate can be between 1 sample per second
and 976 samples per second. Decreasing the sample rate will also decrease the
noise on the data.

The default value is 6 (2 samples per second).
""",
'de':
"""
Setzt die Abtastrate. Der Wertebereich der verfügbare Abtastraten
liegt zwischen 1 Wert pro Sekunde und 976 Werte pro Sekunde. Ein
Verringern der Abtastrate wird auch das Rauschen auf den Daten verringern.

Der Standardwert ist 6 (2 Werte pro Sekunde).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Sample Rate',
'elements': [('Rate', 'uint8', 1, 'out', ('Sample Rate', [('976 SPS', 0),
                                                          ('488 SPS', 1),
                                                          ('244 SPS', 2),
                                                          ('122 SPS', 3),
                                                          ('61 SPS', 4),
                                                          ('4 SPS', 5),
                                                          ('2 SPS', 6),
                                                          ('1 SPS', 7)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the sample rate as set by :func:`Set Sample Rate`.
""",
'de':
"""
Gibt die Abtastrate zurück, wie von :func:`Set Sample Rate`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Calibration',
'elements': [('Offset', 'int32', 2, 'in'),
             ('Gain', 'int32', 2, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets offset and gain of MCP3911 internal calibration registers.

See MCP3911 datasheet 7.7 and 7.8. The Industrial Dual Analog In Bricklet
is already factory calibrated by Tinkerforge. It should not be necessary
for you to use this function
""",
'de':
"""
Setzt Offset und Gain der MCP3911 internen Kalibrierungsregister.

Siehe MCP3911 Datenblatt 7.7 und 7.8. Das Industrial Dual Analog In Bricklet
wird von Tinkerforge werkskalibriert. Ein Aufruf dieser Funktion sollte
nicht notwendig sein.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Calibration',
'elements': [('Offset', 'int32', 2, 'out'),
             ('Gain', 'int32', 2, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the calibration as set by :func:`Set Calibration`.
""",
'de':
"""
Gibt die Kalibrierung zurück, wie von :func:`Set Calibration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get ADC Values',
'elements': [('Value', 'int32', 2, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the ADC values as given by the MCP3911 IC. This function
is needed for proper calibration, see :func:`Set Calibration`.
""",
'de':
"""
Gibt die ADC-Werte des MCP3911 ICs zurück. Diese Funktion
wird für die Kalibrierung benötigt, siehe :func:`Set Calibration`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Channel LED Config',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Config', 'uint8', 1, 'in', ('Info LED Config', [('Off', 0),
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
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Config', 'uint8', 1, 'out', ('Info LED Config', [('Off', 0),
                                                                ('On', 1),
                                                                ('Show Heartbeat', 2),
                                                                ('Show Channel Status', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the Info LED configuration as set by :func:`Set Info LED Config`
""",
'de':
"""
Gibt die LED-Konfiguration zurück, wie von :func:`Set Info LED Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Channel LED Status Config',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Min', 'int32', 1, 'in'),
             ('Max', 'int32', 1, 'in'),
             ('Config', 'uint8', 1, 'in', ('Channel LED Config', [('Threshold', 0),
                                                                  ('Intensity', 1)]))],
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
'name': 'Get Channel LED Status Config',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Min', 'int32', 1, 'out'),
             ('Max', 'int32', 1, 'out'),
             ('Config', 'uint8', 1, 'out', ('Channel LED Config', [('Threshold', 0),
                                                                   ('Intensity', 1)]))],
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
