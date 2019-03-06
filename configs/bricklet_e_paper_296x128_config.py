# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# E-Paper 296x128 Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2146,
    'name': 'E Paper 296x128',
    'display_name': 'E-Paper 296x128',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'TBD',
        'de': 'TBD'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'discontinued': False,
    'packets': [],
    'examples': []
}

COLOR = ('Color', [('Black', 0), ('White', 1), ('Red', 2), ('Gray', 2)])
ORIENTATION = ('Orientation', [('Horizontal', 0), ('Vertical', 1)])
DRAW_STATUS = ('Draw Status', [('Idle', 0), ('Copying', 1), ('Drawing', 2)])
UPDATE_MODE = ('Update Mode', [('Default', 0), ('Black White', 1), ('Delta', 2)])
DISPLAY = ('Display', [('Black White Red', 0), ('Black White Gray', 1)])

com['packets'].append({
'type': 'function',
'name': 'Draw',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
buffer -> display
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Draw Status',
'elements': [('Draw Status', 'uint8', 1, 'out', DRAW_STATUS)],
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
'name': 'Write Black White Low Level',
'elements': [('X Start', 'uint16', 1, 'in'),
             ('Y Start', 'uint8', 1, 'in'),
             ('X End', 'uint16', 1, 'in'),
             ('Y End', 'uint8', 1, 'in'),
             ('Pixels Length', 'uint16', 1, 'in'),
             ('Pixels Chunk Offset', 'uint16', 1, 'in'),
             ('Pixels Chunk Data', 'bool', 54*8, 'in')],
'high_level': {'stream_in': {'name': 'Pixels'}},
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
'name': 'Read Black White Low Level',
'elements': [('X Start', 'uint16', 1, 'in'),
             ('Y Start', 'uint8', 1, 'in'),
             ('X End', 'uint16', 1, 'in'),
             ('Y End', 'uint8', 1, 'in'),
             ('Pixels Length', 'uint16', 1, 'out'),
             ('Pixels Chunk Offset', 'uint16', 1, 'out'),
             ('Pixels Chunk Data', 'bool', 58*8, 'out')],
'high_level': {'stream_out': {'name': 'Pixels'}},
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
'name': 'Write Color Low Level',
'elements': [('X Start', 'uint16', 1, 'in'),
             ('Y Start', 'uint8', 1, 'in'),
             ('X End', 'uint16', 1, 'in'),
             ('Y End', 'uint8', 1, 'in'),
             ('Pixels Length', 'uint16', 1, 'in'),
             ('Pixels Chunk Offset', 'uint16', 1, 'in'),
             ('Pixels Chunk Data', 'bool', 54*8, 'in')],
'high_level': {'stream_in': {'name': 'Pixels'}},
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
'name': 'Read Color Low Level',
'elements': [('X Start', 'uint16', 1, 'in'),
             ('Y Start', 'uint8', 1, 'in'),
             ('X End', 'uint16', 1, 'in'),
             ('Y End', 'uint8', 1, 'in'),
             ('Pixels Length', 'uint16', 1, 'out'),
             ('Pixels Chunk Offset', 'uint16', 1, 'out'),
             ('Pixels Chunk Data', 'bool', 58*8, 'out')],
'high_level': {'stream_out': {'name': 'Pixels'}},
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
'name': 'Fill Display',
'elements': [('Color', 'uint8', 1, 'in', COLOR)],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Fills the complete content of the display with the given color.
""",
'de':
"""
Füllt den ko kompletten Inhalt des Displays mit der gegebenen Farbe.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Draw Text',
'elements': [('Position X', 'uint16', 1, 'in'),
             ('Position Y', 'uint8', 1, 'in'),
             ('Font', 'uint8', 1, 'in',  ('Font', [('6x8', 0),
                                                   ('6x16', 1),
                                                   ('6x24', 2),
                                                   ('6x32', 3),
                                                   ('12x16', 4),
                                                   ('12x24', 5),
                                                   ('12x32', 6),
                                                   ('18x24', 7),
                                                   ('18x32', 8),
                                                   ('24x32', 9)])),
             ('Color', 'uint8', 1, 'in', COLOR),
             ('Orientation', 'uint8', 1, 'in', ORIENTATION),
             ('Text', 'string', 50, 'in')],
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
'name': 'Draw Line',
'elements': [('Position X Start', 'uint16', 1, 'in'),
             ('Position Y Start', 'uint8', 1, 'in'),
             ('Position X End', 'uint16', 1, 'in'),
             ('Position Y End', 'uint8', 1, 'in'),
             ('Color', 'uint8', 1, 'in', COLOR)],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Draws line from (x, y)-start to (x, y)-end in the given color.
The x values have to be within the range of 0 to 127 and the y
values have t be within the range of 0 to 63.
""",
'de':
"""
Zeichnet eine Linie von (x, y)-start nach (x, y)-end in der eingestellten Farbe. 
Der Wertebereich für die x-Werte ist 0 bis 127 und
der Wertebereich für die y-Werte ist 0-63.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Draw Box',
'elements': [('Position X Start', 'uint16', 1, 'in'),
             ('Position Y Start', 'uint8', 1, 'in'),
             ('Position X End', 'uint16', 1, 'in'),
             ('Position Y End', 'uint8', 1, 'in'),
             ('Fill', 'bool', 1, 'in'),
             ('Color', 'uint8', 1, 'in', COLOR)],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Draws a box from (x, y)-start to (x, y)-end in the given color.
The x values have to be within the range of 0 to 127 and the y
values have to be within the range of 0 to 63.

If you set fill to true, the box will be filled with the
color. Otherwise only the outline will be drawn.
""",
'de':
"""
Zeichnet ein Rechteck von (x, y)-start nach (x, y)-end in der eingestellten Farbe. 
Der Wertebereich für die x-Werte ist 0 bis 127 und
der Wertebereich für die y-Werte ist 0-63.

Wenn fill auf true gesetzt wird, wird das Rechteck mit
der angegebenen Farbe ausgefüllt. Ansonsten wird nur der Umriss
gezeichnet.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Draw Status',
'elements': [('Draw Status', 'uint8', 1, 'out', DRAW_STATUS)],
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
'type': 'function',
'name': 'Set Update Mode',
'elements': [('Update Mode', 'uint8', 1, 'in', UPDATE_MODE)],
'since_firmware': [1, 0, 0],
'doc': ['af', {
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
'name': 'Get Update Mode',
'elements': [('Update Mode', 'uint8', 1, 'out', UPDATE_MODE)],
'since_firmware': [1, 0, 0],
'doc': ['af', {
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
'name': 'Set Display',
'elements': [('Display', 'uint8', 1, 'in', DISPLAY)],
'since_firmware': [1, 0, 0],
'doc': ['af', {
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
'name': 'Get Display',
'elements': [('Display', 'uint8', 1, 'out', DISPLAY)],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})
