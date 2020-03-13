# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Motion Detector Bricklet communication config

from openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'category': 'Bricklet',
    'device_identifier': 233,
    'name': 'Motion Detector',
    'display_name': 'Motion Detector',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Passive infrared (PIR) motion sensor with 7m range',
        'de': 'Passiver Infrarot (PIR) Bewegungssensor mit 7m Reichweite'
    },
    'released': True,
    'documented': True,
    'discontinued': False, # selling remaining stock, replaced by Motion Detector Bricklet 2.0
    'features': [
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append({
'name': 'Motion',
'type': 'uint8',
'constants': [('Not Detected', 0),
              ('Detected', 1)]
})

com['constant_groups'].append({
'name': 'Status LED Config',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Show Status', 2)]
})

com['packets'].append({
'type': 'function',
'name': 'Get Motion Detected',
'elements': [('Motion', 'uint8', 1, 'out', {'constant_group': 'Motion'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns 1 if a motion was detected. How long this returns 1 after a motion
was detected can be adjusted with one of the small potentiometers on the
Motion Detector Bricklet, see :ref:`here
<motion_detector_bricklet_sensitivity_delay_block_time>`.

There is also a blue LED on the Bricklet that is on as long as the Bricklet is
in the "motion detected" state.
""",
'de':
"""
Gibt 1 zurück wenn eine Bewegung detektiert wurde. Wie lange 1 zurückgegeben
wird nachdem eine Bewegung detektiert wurde kann mit einem kleinen Poti auf
dem Motion Detector Bricklet eingestellt werden, siehe :ref:`hier
<motion_detector_bricklet_sensitivity_delay_block_time>`.

Auf dem Bricklet selbst ist eine blaue LED, die leuchtet solange das Bricklet
im "Bewegung detektiert" Zustand ist.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Motion Detected',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called after a motion was detected.
""",
'de':
"""
Dieser Callback wird aufgerufen nachdem eine Bewegung detektiert wurde.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Detection Cycle Ended',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called when the detection cycle ended. When this
callback is called, a new motion can be detected again after approximately 2
seconds.
""",
'de':
"""
Dieser Callback wird aufgerufen wenn ein Bewegungserkennungszyklus
beendet ist. Wenn dieser Callback aufgerufen wurde kann wieder
eine weitere Bewegung erkannt werden nach ungefähr 2 Sekunden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Status LED Config',
'elements': [('Config', 'uint8', 1, 'in', {'constant_group': 'Status LED Config', 'default': 2})],
'since_firmware': [2, 0, 1],
'doc': ['af', {
'en':
"""
Sets the status led configuration.

By default the status LED turns on if a motion is detected and off is no motion
is detected.

You can also turn the LED permanently on/off.
""",
'de':
"""
Setzt die Konfiguration der Status-LED.

Standardmäßig geht die LED an, wenn eine Bewegung erkannt wird und
aus wenn keine Bewegung erkannt wird.

Die LED kann auch permanent an/aus gestellt werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Status LED Config',
'elements': [('Config', 'uint8', 1, 'out', {'constant_group': 'Status LED Config', 'default': 2})],
'since_firmware': [2, 0, 1],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Status LED Config`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Status LED Config` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Motion Detected', 'motion detected'), [], None, 'Motion Detected'),
              ('callback', ('Detection Cycle Ended', 'detection cycle ended'), [], None, 'Detection Cycle Ended (next detection possible in ~3 seconds)')]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'channels': [
        {
            'id': 'Motion Detected',
            'label': 'Motion Detected',
            'type': 'system.trigger',

            'callbacks': [{
                'packet': 'Motion Detected',
                'transform': '""'}],
            'description': 'This channel is triggered after a motion was detected.'
        }, {
            'id': 'Detection Cycle Ended',
            'label': 'Detection Cycle Ended',
            'type': 'system.trigger',

            'callbacks': [{
                'packet': 'Detection Cycle Ended',
                'transform': '""'}],
            'description': 'This channel is triggered when the detection cycle ended. A new motion can be detected again after approximately 2 seconds.'
        },
    ],
    'channel_types': [],
    'actions': ['Get Motion Detected']
}
