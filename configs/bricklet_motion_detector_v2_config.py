# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Motion Detector Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 292,
    'name': 'Motion Detector V2',
    'display_name': 'Motion Detector 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Passive infrared (PIR) motion sensor, 12m range',
        'de': 'Passiver Infrarot (PIR) Bewegungssensor, 12m Reichweite'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'packets': [],
    'examples': []
}


com['packets'].append({
'type': 'function',
'name': 'Get Motion Detected',
'elements': [('Motion', 'uint8', 1, 'out', ('Motion', [('Not Detected', 0),
                                                       ('Detected', 1)]))],
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
'type': 'function',
'name': 'Set Sensitivity',
'elements': [('Sensitivity', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the sensitivity of the PIR sensor. The range is 0-100. At full 
sensitivity (100), the Bricklet can detect motion in a range of approximately 12m.

The range depends on many things in the enivronment (e.g. reflections) and the
size of the object to be detected. While a big person might be detected in a range
of 10m a cat may only be detected at 2m distance with the same setting.

So you will have to find a good sensitivty for your application by trial and error.

The default sensitivity value is 50.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Sensitivity',
'elements': [('Sensitivity', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the sensitivity as set by :func:`Set Sensitivity`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Indicator',
'elements': [('Top Left', 'uint8', 1, 'in'),
             ('Top Right', 'uint8', 1, 'in'),
             ('Bottom', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the blue backlight of the fresnel lens. The backlight consists of
three LEDs. The brightness of each LED can be controlled with a 8-bit value
(0-255). A value of 0 turns the LED off and a value of 255 turns the LED
to full brightness.

The default value is 0, 0, 0.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Indicator',
'elements': [('Top Left', 'uint8', 1, 'out'),
             ('Top Right', 'uint8', 1, 'out'),
             ('Bottom', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the indicator configuration as set by :func:`Set Indicator`.
""",
'de':
"""
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

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Motion Detected', 'motion detected'), [], None, 'Motion Detected'),
              ('callback', ('Detection Cycle Ended', 'detection cycle ended'), [], None, 'Detection Cycle Ended (next detection possible in ~2 seconds)')]
})
