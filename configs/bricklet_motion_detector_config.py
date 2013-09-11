# -*- coding: utf-8 -*-

# Motion Detector Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 233,
    'name': ('MotionDetector', 'motion_detector', 'Motion Detector'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device that reads out PIR motion detector',
    'released': False,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetMotionDetected', 'get_motion_detected'), 
'elements': [('motion', 'uint8', 1, 'out', ('Motion', 'motion', [('Detected', 'detected', 0),
                                                                 ('NotDetected', 'not_detected', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns 0 if a motion was detected. How long this returns 0 after a motion
was detected can be adjusted with one of the small potentiometers on the
Motion Detector Bricklet, see here. TODO: ADD LINK
""",
'de':
"""
Gibt 0 zurück wenn eine Bewegung detektiert wurde. Wie lange 0 zurückgegeben wird
nachdem eine Bewegung detektiert wurde kann mit einem kleinen Poti auf
dem Motion Detector Bricklet eingestellt werden, siehe hier. TODO: LINK HINZUFÜGEN
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('MotionDetected', 'motion_detected'), 
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
'name': ('DetectionCycleEnded', 'detection_cycle_ended'), 
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

