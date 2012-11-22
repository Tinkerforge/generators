# -*- coding: utf-8 -*-

# Common Bricklet communication config

common_packets = []

common_packets.append({
'type': 'function',
'function_id': 255,
'name': ('GetIdentity', 'get_identity'),
'elements': [('uid', 'string', 8, 'out'),
             ('connected_uid', 'string', 8, 'out'),
             ('position', 'char', 1, 'out'),
             ('hardware_version', 'uint8', 3, 'out'),
             ('firmware_version', 'uint8', 3, 'out'),
             ('device_identifier', 'uint16', 1, 'out')],
'since_firmware': {'*': [2, 0, 0]},
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})
