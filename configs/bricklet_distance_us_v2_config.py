# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Distance US Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from commonconstants import add_callback_value_function

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 299,
    'name': 'Distance US V2',
    'display_name': 'Distance US 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures distance between 30cm and 500cm with ultrasound',
        'de': 'Misst Entfernung zwischen 30cm und 500cm mit Ultraschall'
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
'name': 'Update Rate',
'type': 'uint8',
'constants': [('2 Hz', 0),
              ('10 Hz', 1)]
})

com['constant_groups'].append({
'name': 'Distance LED Config',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Show Heartbeat', 2),
              ('Show Distance', 3)]
})

distance_doc = {
'en':
"""
Returns the distance.
""",
'de':
"""
Gibt die Distanz zurück.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Distance',
    data_name = 'Distance',
    data_type = 'uint16',
    doc       = distance_doc,
    scale     = (1, 1000),
    unit      = 'Meter',
    range_    = (300, 5000)
)

com['packets'].append({
'type': 'function',
'name': 'Set Update Rate',
'elements': [('Update Rate', 'uint8', 1, 'in', {'constant_group': 'Update Rate', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the update rate to 2 Hz or 10 Hz.

With 2 Hz update rate the noise is about ±1mm, while with 10 Hz update rate the noise
increases to about ±5mm.
""",
'de':
"""
Setzt die Aktualisierungsrate auf 2 Hz oder 10 Hz.

Mit 2 Hz Aktualisierungsrate beträgt das Rauschen ungefähr ±1mm. Bei 10 Hz
erhöht sich das das Rauschen auf ungefähr ±5mm.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Update Rate',
'elements': [('Update Rate', 'uint8', 1, 'out', {'constant_group': 'Update Rate', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the update rate as set by :func:`Set Update Rate`.
""",
'de':
"""
Gibt die Aktualisierungsrate zurück, wie von :func:`Set Update Rate` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Distance LED Config',
'elements': [('Config', 'uint8', 1, 'in', {'constant_group': 'Distance LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Configures the distance LED to be either turned off, turned on, blink in
heartbeat mode or show the distance (brighter = object is nearer).
""",
'de':
"""
Konfiguriert die Distanz-LED. Die LED kann ausgeschaltet, eingeschaltet,
im Herzschlagmodus betrieben werden. Zusätzlich gibt es die Option
mit der LED die Distanz anzuzeigen (heller = Objekt näher).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Distance LED Config',
'elements': [('Config', 'uint8', 1, 'out', {'constant_group': 'Distance LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the LED configuration as set by :func:`Set Distance LED Config`
""",
'de':
"""
Gibt die LED-Konfiguration zurück, wie von :func:`Set Distance LED Config` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Distance', 'distance'), [(('Distance', 'Distance'), 'uint16', 1, 10.0, 'cm', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Distance', 'distance'), [(('Distance', 'Distance'), 'uint16', 1, 10.0, 'cm', None)], None, None),
              ('callback_configuration', ('Distance', 'distance'), [], 100, False, 'x', [(0, 0)])]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('callback', ('Distance', 'distance'), [(('Distance', 'Distance'), 'uint16', 1, 10.0, 'cm', None)], None, None),
              ('callback_configuration', ('Distance', 'distance'), [], 100, False, '>', [(100, 0)])]
})


com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'params': [
        {
            'name': 'Update Rate',
            'type': 'integer',
            'default': 0,
            'options':  [('2 Hz', 0),
                         ('10 Hz', 1)],
            'limitToOptions': 'true',

            'label': 'Update Rate',
            'description': 'With 2 Hz update rate the noise is about +-1mm, while with 10 Hz update rate the noise increases to about +-5mm.',
        }, {
            'name': 'Distance LED Config',
            'type': 'integer',
            'default': 3,
            'options': [('Off', 0),
                        ('On', 1),
                        ('Show Heartbeat', 2),
                        ('Show Distance', 3)],
            'limitToOptions': 'true',

            'label': 'Distance LED Config',
            'description': 'Configures the distance LED to be either turned off, turned on, blink in heartbeat mode or show the distance (brighter = object is nearer).',
        }
    ],
    'init_code': """this.setUpdateRate(cfg.updateRate);
this.setDistanceLEDConfig(cfg.distanceLEDConfig);""",
    'channels': [
        oh_generic_channel('Distance', 'Distance', 'SIUnits.METRE', divisor=1000.0)
    ],
    'channel_types': [
        oh_generic_channel_type('Distance', 'Number:Length', 'Distance',
                     description='The current distance measured by the sensor.',
                     read_only=True,
                     pattern='%.3f %unit%',
                     min_=0.3,
                     max_=5)
    ],
    'actions': ['Get Distance', 'Get Update Rate', 'Get Distance LED Config']
}
