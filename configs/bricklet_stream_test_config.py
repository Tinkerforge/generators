# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Stream Test Bricklet communication config

com = {
    'author': 'Matthias <matthias@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 21111,
    'name': 'Stream Test',
    'display_name': 'Stream Test',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '',
        'de': '',
    },
    'released': False,
    'documented': False,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Normal Write Low Level',
'elements': [('Message Total Length', 'uint32', 1, 'in'),
             ('Message Chunk Offset', 'uint32', 1, 'in'),
             ('Message Chunk Data', 'char', 56, 'in')],
'high_level': {'stream_in': {'name': 'Message'}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Normal Write Extra In 1 Low Level',
'elements': [('Extra', 'uint8', 1, 'in'),
             ('Message Total Length', 'uint32', 1, 'in'),
             ('Message Chunk Offset', 'uint32', 1, 'in'),
             ('Message Chunk Data', 'char', 55, 'in')],
'high_level': {'stream_in': {'name': 'Message'}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Normal Write Extra In 2 Low Level',
'elements': [('Message Total Length', 'uint32', 1, 'in'),
             ('Message Chunk Offset', 'uint32', 1, 'in'),
             ('Message Chunk Data', 'char', 55, 'in'),
             ('Extra', 'uint8', 1, 'in')],
'high_level': {'stream_in': {'name': 'Message'}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Normal Write Extra Out Low Level',
'elements': [('Message Total Length', 'uint32', 1, 'in'),
             ('Message Chunk Offset', 'uint32', 1, 'in'),
             ('Message Chunk Data', 'char', 56, 'in'),
             ('Extra', 'uint8', 1, 'out')],
'high_level': {'stream_in': {'name': 'Message'}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Fixed Write Low Level',
'elements': [('Message Chunk Offset', 'uint16', 1, 'in'),
             ('Message Chunk Data', 'char', 62, 'in')],
'high_level': {'stream_in': {'name': 'Message', 'fixed_total_length': 1000}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Fixed Write Extra In 1 Low Level',
'elements': [('Extra', 'uint8', 1, 'in'),
             ('Message Chunk Offset', 'uint16', 1, 'in'),
             ('Message Chunk Data', 'char', 61, 'in')],
'high_level': {'stream_in': {'name': 'Message', 'fixed_total_length': 1000}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Fixed Write Extra In 2 Low Level',
'elements': [('Message Chunk Offset', 'uint16', 1, 'in'),
             ('Message Chunk Data', 'char', 61, 'in'),
             ('Extra', 'uint8', 1, 'in')],
'high_level': {'stream_in': {'name': 'Message', 'fixed_total_length': 1000}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Fixed Write Extra Out Low Level',
'elements': [('Message Chunk Offset', 'uint16', 1, 'in'),
             ('Message Chunk Data', 'char', 62, 'in'),
             ('Extra', 'uint8', 1, 'out')],
'high_level': {'stream_in': {'name': 'Message', 'fixed_total_length': 1000}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Short Write Low Level',
'elements': [('Message Total Length', 'uint16', 1, 'in'),
             ('Message Chunk Offset', 'uint16', 1, 'in'),
             ('Message Chunk Data', 'char', 60, 'in'),
             ('Message Chunk Written', 'uint8', 1, 'out')],
'high_level': {'stream_in': {'name': 'Message', 'short_write': True}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Short Write Extra In 1 Low Level',
'elements': [('Extra', 'uint8', 1, 'in'),
             ('Message Total Length', 'uint16', 1, 'in'),
             ('Message Chunk Offset', 'uint16', 1, 'in'),
             ('Message Chunk Data', 'char', 59, 'in'),
             ('Message Chunk Written', 'uint8', 1, 'out')],
'high_level': {'stream_in': {'name': 'Message', 'short_write': True}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Short Write Extra In 2 Low Level',
'elements': [('Message Total Length', 'uint16', 1, 'in'),
             ('Message Chunk Offset', 'uint16', 1, 'in'),
             ('Message Chunk Data', 'char', 59, 'in'),
             ('Extra', 'uint8', 1, 'in'),
             ('Message Chunk Written', 'uint8', 1, 'out')],
'high_level': {'stream_in': {'name': 'Message', 'short_write': True}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Short Write Extra Out 1 Low Level',
'elements': [('Message Total Length', 'uint16', 1, 'in'),
             ('Message Chunk Offset', 'uint16', 1, 'in'),
             ('Message Chunk Data', 'char', 60, 'in'),
             ('Extra', 'uint8', 1, 'out'),
             ('Message Chunk Written', 'uint8', 1, 'out')],
'high_level': {'stream_in': {'name': 'Message', 'short_write': True}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Short Write Extra Out 2 Low Level',
'elements': [('Message Total Length', 'uint16', 1, 'in'),
             ('Message Chunk Offset', 'uint16', 1, 'in'),
             ('Message Chunk Data', 'char', 60, 'in'),
             ('Message Chunk Written', 'uint8', 1, 'out'),
             ('Extra', 'uint8', 1, 'out')],
'high_level': {'stream_in': {'name': 'Message', 'short_write': True}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Single Write Low Level',
'elements': [('Message Length', 'uint8', 1, 'in'),
             ('Message Data', 'char', 63, 'in')],
'high_level': {'stream_in': {'name': 'Message', 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Single Write Extra In 1 Low Level',
'elements': [('Extra', 'uint8', 1, 'in'),
             ('Message Length', 'uint8', 1, 'in'),
             ('Message Data', 'char', 62, 'in')],
'high_level': {'stream_in': {'name': 'Message', 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Single Write Extra In 2 Low Level',
'elements': [('Message Length', 'uint8', 1, 'in'),
             ('Message Data', 'char', 62, 'in'),
             ('Extra', 'uint8', 1, 'in')],
'high_level': {'stream_in': {'name': 'Message', 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Single Write Extra Out Low Level',
'elements': [('Message Length', 'uint8', 1, 'in'),
             ('Message Data', 'char', 63, 'in'),
             ('Extra', 'uint8', 1, 'out')],
'high_level': {'stream_in': {'name': 'Message', 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Short Single Write Low Level',
'elements': [('Message Length', 'uint8', 1, 'in'),
             ('Message Data', 'char', 63, 'in'),
             ('Message Written', 'uint8', 1, 'out')],
'high_level': {'stream_in': {'name': 'Message', 'short_write': True, 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Short Single Write Extra In 1 Low Level',
'elements': [('Extra', 'uint8', 1, 'in'),
             ('Message Length', 'uint8', 1, 'in'),
             ('Message Data', 'char', 62, 'in'),
             ('Message Written', 'uint8', 1, 'out')],
'high_level': {'stream_in': {'name': 'Message', 'short_write': True, 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Short Single Write Extra In 2 Low Level',
'elements': [('Message Length', 'uint8', 1, 'in'),
             ('Message Data', 'char', 62, 'in'),
             ('Extra', 'uint8', 1, 'in'),
             ('Message Written', 'uint8', 1, 'out')],
'high_level': {'stream_in': {'name': 'Message', 'short_write': True, 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Short Single Write Extra Out 1 Low Level',
'elements': [('Message Length', 'uint8', 1, 'in'),
             ('Message Data', 'char', 62, 'in'),
             ('Extra', 'uint8', 1, 'out'),
             ('Message Written', 'uint8', 1, 'out')],
'high_level': {'stream_in': {'name': 'Message', 'short_write': True, 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Short Single Write Extra Out 2 Low Level',
'elements': [('Message Length', 'uint8', 1, 'in'),
             ('Message Data', 'char', 63, 'in'),
             ('Message Written', 'uint8', 1, 'out'),
             ('Extra', 'uint8', 1, 'out')],
'high_level': {'stream_in': {'name': 'Message', 'short_write': True, 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Normal Read Low Level',
'elements': [('Message Total Length', 'uint32', 1, 'out'),
             ('Message Chunk Offset', 'uint32', 1, 'out'),
             ('Message Chunk Data', 'char', 56, 'out')],
'high_level': {'stream_out': {'name': 'Message'}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Normal Read Extra In Low Level',
'elements': [('Extra', 'uint8', 1, 'in'),
             ('Message Total Length', 'uint32', 1, 'out'),
             ('Message Chunk Offset', 'uint32', 1, 'out'),
             ('Message Chunk Data', 'char', 56, 'out')],
'high_level': {'stream_out': {'name': 'Message'}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Normal Read Extra Out 1 Low Level',
'elements': [('Extra', 'uint8', 1, 'out'),
             ('Message Total Length', 'uint32', 1, 'out'),
             ('Message Chunk Offset', 'uint32', 1, 'out'),
             ('Message Chunk Data', 'char', 55, 'out')],
'high_level': {'stream_out': {'name': 'Message'}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Normal Read Extra Out 2 Low Level',
'elements': [('Message Total Length', 'uint32', 1, 'out'),
             ('Message Chunk Offset', 'uint32', 1, 'out'),
             ('Message Chunk Data', 'char', 55, 'out'),
             ('Extra', 'uint8', 1, 'out')],
'high_level': {'stream_out': {'name': 'Message'}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Fixed Read Low Level',
'elements': [('Message Chunk Offset', 'uint16', 1, 'out'),
             ('Message Chunk Data', 'char', 62, 'out')],
'high_level': {'stream_out': {'name': 'Message', 'fixed_total_length': 1000}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Fixed Read Extra In Low Level',
'elements': [('Extra', 'uint8', 1, 'in'),
             ('Message Chunk Offset', 'uint16', 1, 'out'),
             ('Message Chunk Data', 'char', 62, 'out')],
'high_level': {'stream_out': {'name': 'Message', 'fixed_total_length': 1000}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Fixed Read Extra Out 1 Low Level',
'elements': [('Extra', 'uint8', 1, 'out'),
             ('Message Chunk Offset', 'uint16', 1, 'out'),
             ('Message Chunk Data', 'char', 61, 'out')],
'high_level': {'stream_out': {'name': 'Message', 'fixed_total_length': 1000}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Fixed Read Extra Out 2 Low Level',
'elements': [('Message Chunk Offset', 'uint16', 1, 'out'),
             ('Message Chunk Data', 'char', 61, 'out'),
             ('Extra', 'uint8', 1, 'out')],
'high_level': {'stream_out': {'name': 'Message', 'fixed_total_length': 1000}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Single Read Low Level',
'elements': [('Message Length', 'uint8', 1, 'out'),
             ('Message Data', 'char', 63, 'out')],
'high_level': {'stream_out': {'name': 'Message', 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Single Read Extra In Low Level',
'elements': [('Extra', 'uint8', 1, 'in'),
             ('Message Length', 'uint8', 1, 'out'),
             ('Message Data', 'char', 62, 'out')],
'high_level': {'stream_out': {'name': 'Message', 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Single Read Extra Out 1 Low Level',
'elements': [('Extra', 'uint8', 1, 'out'),
             ('Message Length', 'uint8', 1, 'out'),
             ('Message Data', 'char', 62, 'out')],
'high_level': {'stream_out': {'name': 'Message', 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Single Read Extra Out 2 Low Level',
'elements': [('Message Length', 'uint8', 1, 'out'),
             ('Message Data', 'char', 62, 'out'),
             ('Extra', 'uint8', 1, 'out')],
'high_level': {'stream_out': {'name': 'Message', 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['llf', {
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
'name': 'Normal Read Low Level',
'elements': [('Message Total Length', 'uint16', 1, 'out'),
             ('Message Chunk Offset', 'uint16', 1, 'out'),
             ('Message Chunk Data', 'char', 60, 'out')],
'high_level': {'stream_out': {'name': 'Message'}},
'since_firmware': [1, 0, 0],
'doc': ['llc', {
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
'name': 'Normal Read Extra 1 Low Level',
'elements': [('Extra', 'uint8', 1, 'out'),
             ('Message Total Length', 'uint16', 1, 'out'),
             ('Message Chunk Offset', 'uint16', 1, 'out'),
             ('Message Chunk Data', 'char', 59, 'out')],
'high_level': {'stream_out': {'name': 'Message'}},
'since_firmware': [1, 0, 0],
'doc': ['llc', {
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
'name': 'Normal Read Extra 2 Low Level',
'elements': [('Message Total Length', 'uint16', 1, 'out'),
             ('Message Chunk Offset', 'uint16', 1, 'out'),
             ('Message Chunk Data', 'char', 59, 'out'),
             ('Extra', 'uint8', 1, 'out')],
'high_level': {'stream_out': {'name': 'Message'}},
'since_firmware': [1, 0, 0],
'doc': ['llc', {
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
'name': 'Fixed Read Low Level',
'elements': [('Message Chunk Offset', 'uint16', 1, 'out'),
             ('Message Chunk Data', 'char', 62, 'out')],
'high_level': {'stream_out': {'name': 'Message', 'fixed_total_length': 1000}},
'since_firmware': [1, 0, 0],
'doc': ['llc', {
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
'name': 'Fixed Read Extra 1 Low Level',
'elements': [('Extra', 'uint8', 1, 'out'),
             ('Message Chunk Offset', 'uint16', 1, 'out'),
             ('Message Chunk Data', 'char', 61, 'out')],
'high_level': {'stream_out': {'name': 'Message', 'fixed_total_length': 1000}},
'since_firmware': [1, 0, 0],
'doc': ['llc', {
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
'name': 'Fixed Read Extra 2 Low Level',
'elements': [('Message Chunk Offset', 'uint16', 1, 'out'),
             ('Message Chunk Data', 'char', 61, 'out'),
             ('Extra', 'uint8', 1, 'out')],
'high_level': {'stream_out': {'name': 'Message', 'fixed_total_length': 1000}},
'since_firmware': [1, 0, 0],
'doc': ['llc', {
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
'name': 'Single Read Low Level',
'elements': [('Message Length', 'uint8', 1, 'out'),
             ('Message Data', 'char', 63, 'out')],
'high_level': {'stream_out': {'name': 'Message', 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['llc', {
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
'name': 'Single Read Extra 1 Low Level',
'elements': [('Extra', 'uint8', 1, 'out'),
             ('Message Length', 'uint8', 1, 'out'),
             ('Message Data', 'char', 62, 'out')],
'high_level': {'stream_out': {'name': 'Message', 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['llc', {
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
'name': 'Single Read Extra 2 Low Level',
'elements': [('Message Length', 'uint8', 1, 'out'),
             ('Message Data', 'char', 62, 'out'),
             ('Extra', 'uint8', 1, 'out')],
'high_level': {'stream_out': {'name': 'Message', 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['llc', {
'en':
"""
""",
'de':
"""
"""
}]
})
