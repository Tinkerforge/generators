# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Distance US Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 299,
    'name': 'Distance US V2',
    'display_name': 'Distance US 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '',
        'de': ''
    },
    'released': False, # FIXME: update Distance US Bricklet (1.0) replacement recommendation, once this Bricklet is released
    'documented': False,
    'discontinued': False,
    'features': [
        'comcu_bricklet',
        'bricklet_get_identity'
    ],
    'packets': [],
    'examples': []
}

distance_doc = {
'en':
"""
Returns the distance in mm.
""",
'de':
"""
Gibt die Distanz in mm zurück.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Distance',
    data_name = 'Distance',
    data_type = 'uint16',
    doc       = distance_doc
)


com['packets'].append({
'type': 'function',
'name': 'Set Update Rate',
'elements': [('Update Rate', 'uint8', 1, 'in', ('Update Rate', [('2 Hz', 0),
                                                                ('10 Hz', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the update rate to 2 Hz or 10 Hz.

With 2 Hz update rate the noise is about +-1mm, while with 10 Hz update rate the noise
increases to about +-5mm.

The default update rate is 2 Hz.
""",
'de':
"""
Setzt die Aktualisierungsrate auf 2 Hz oder 10 Hz.

Mit 2 Hz Aktualisierungsrate beträgt das Rauschen ungefähr +-1mm. Bei 10 Hz
erhöht sich das das Rauschen auf ungefähr +-5mm.

Der Standardwert beträgt 2 Hz.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Update Rate',
'elements': [('Update Rate', 'uint8', 1, 'out', ('Update Rate', [('2 Hz', 0),
                                                                 ('10 Hz', 1)]))],
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
'elements': [('Config', 'uint8', 1, 'in', ('Distance LED Config', [('Off', 0),
                                                                   ('On', 1),
                                                                   ('Show Heartbeat', 2),
                                                                   ('Show Distance', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Configures the distance LED to be either turned off, turned on, blink in
heartbeat mode or show the distance (brighter = object is nearer).

The default value is 3 (show distance).
""",
'de':
"""
Konfiguriert die Distanz-LED. Die LED kann ausgeschaltet, eingeschaltet,
im Herzschlagmodus betrieben werden. Zusätzlich gibt es die Option
mit der LED die Distanz anzuzeigen (heller = Objekt näher).

Der Standardwert ist 3 (Distanzanzeige).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Distance LED Config',
'elements': [('Config', 'uint8', 1, 'out', ('Distance LED Config', [('Off', 0),
                                                                    ('On', 1),
                                                                    ('Show Heartbeat', 2),
                                                                    ('Show Distance', 3)]))],
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
