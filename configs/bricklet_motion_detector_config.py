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
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetMotionDetected', 'get_motion_detected'), 
'elements': [('motion', 'uint8', 1, 'out', ('Motion', 'Motion', [('Detected', 'detected', 0),
                                                                          ('NotDetected', 'not_detected', 1)]))],
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
'type': 'callback',
'name': ('MotionDetected', 'motion_detected'), 
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
""",
'de':
"""
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
""",
'de':
"""
"""
}]
})

