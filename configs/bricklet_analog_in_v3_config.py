# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Analog In 3.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 295,
    'name': 'Analog In V3',
    'display_name': 'Analog In 3.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures DC voltage between 0V and 42V',
        'de': 'Misst Gleichspannung zwischen 0V und 42V'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'discontinued': False,
    'packets': [],
    'examples': []
}

OVERSAMPLING = ('Oversampling', [('32', 0),
                                 ('64', 1),
                                 ('128', 2),
                                 ('256', 3),
                                 ('512', 4),
                                 ('1024', 5),
                                 ('2048', 6),
                                 ('4096', 7),
                                 ('8192', 8),
                                 ('16384', 9)])

voltage_doc = {
'en':
"""
Returns the measured voltage. The value is in mV and
between 0V and 42V. The resolution is approximately 10mV to 1mV
depending on the oversampling configuration (:func:`Set Oversampling`).
""",
'de':
"""
Gibt die gemessene Spannung zurück. Der Wert ist in mV und im
Bereich von 0 bis 42V. Die Auflösung ca. 10mV bis 1mV abhängig von der
Überabtastungs-Konfiguration (:func:`Set Oversampling`).
"""
}

add_callback_value_function(
    packets   = com['packets'], 
    name      = 'Get Voltage', 
    data_name = 'Voltage',
    data_type = 'uint16',
    doc       = voltage_doc
)

com['packets'].append({
'type': 'function',
'name': 'Set Oversampling',
'elements': [('Oversampling', 'uint8', 1, 'in', OVERSAMPLING)],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the oversampling between 32 and 16384. The Bricklet
takes one 12bit sample every 17.5us. Thus an oversampling
of 32 is equivalent to an integration time of 0.56ms and
a oversampling of 16384 is equivalent to an integration
time of 286ms.

The oversampling uses the moving average principle. A
new value is always calculated once per ms.

With increased oversampling the noise decreases. With decreased
oversampling the reaction time increases (changes in voltage will be
measured faster).

The default oversampling value is 4096x.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Oversampling',
'elements': [('Oversampling', 'uint8', 1, 'out', OVERSAMPLING)],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the oversampling value as set by :func:`Set Oversampling`.
""",
'de':
"""
Gibt den Überabtastungsfaktor zurück, wie von :func:`Set Oversampling` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Calibration',
'elements': [('Offset', 'int16', 1, 'in'),
             ('Multiplier', 'uint16', 1, 'in'),
             ('Divisor', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets a calibration for the measured voltage value.
The formula for the calibration is as follows:

* Calibrated Value = (Value + Offset) * Multiplier / Divisor

We recommend that you use the Brick Viewer to calibrate
the Bricklet. The calibration will be saved and only
has to be done once.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Calibration',
'elements': [('Offset', 'int16', 1, 'out'),
             ('Multiplier', 'uint16', 1, 'out'),
             ('Divisor', 'uint16', 1, 'out')],
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

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Voltage', 'voltage'), [(('Voltage', 'Voltage'), 'uint16', 1, 1000.0, 'V', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Voltage', 'voltage'), [(('Voltage', 'Voltage'), 'uint16', 1, 1000.0, 'V', None)], None, None),
              ('callback_configuration', ('Voltage', 'voltage'), [], 1000, 'x', [(0, 0)])]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('callback', ('Voltage', 'voltage'), [(('Voltage', 'Voltage'), 'uint16', 1, 1000.0, 'V', None)], None, None),
              ('callback_configuration', ('Voltage', 'voltage'), [], 1000, '<', [(5, 0)])]
})
