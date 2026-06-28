# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# WARP Front Panel Bricklet communication config

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2179,
    'name': 'WARP Front Panel',
    'display_name': 'WARP Front Panel',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Display and status LED for the front panel of the WARP Energy Manager 2.0',
        'de': 'TBD'
    },
    'released': False,
    'documented': False,
    'discontinued': False,
    'esp32_firmware': 'energy_manager_v2',
    'features': [
        'device',
        'comcu_bricklet',
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append({
'name': 'Flash Status',
'type': 'uint8',
'constants': [('OK', 0),
              ('Busy', 1)]
})


com['constant_groups'].append({
'name': 'LED Pattern',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Blinking', 2),
              ('Breathing', 3)]
})


com['constant_groups'].append({
'name': 'LED Color',
'type': 'uint8',
'constants': [('Green', 0),
              ('Red', 1),
              ('Yellow', 2)]
})

com['constant_groups'].append({
'name': 'Display',
'type': 'uint8',
'constants': [('Off', 0),
              ('Automatic', 1)]
})

# Page = 256 Byte of 64 Byte Subpages
# Sector = 4096 Byte

com['packets'].append({
'type': 'function',
'name': 'Set Flash Index',
'elements': [('Page Index', 'uint32', 1, 'in'),
             ('Sub Page Index', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the page and sub-page index for the next flash write/read. The flash is
organized in pages of 256 bytes (4 sub-pages of 64 bytes each) and sectors of
4096 bytes. The flash holds the sprites and fonts used by the display.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Flash Index',
'elements': [('Page Index', 'uint32', 1, 'out'),
             ('Sub Page Index', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current flash index as set by :func:`Set Flash Index`.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Flash Data', # Uses current Index and increments it by 1
'elements': [('Data', 'uint8', 64, 'in'),
             ('Next Page Index', 'uint32', 1, 'out'),
             ('Next Sub Page Index', 'uint8', 1, 'out'),
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Flash Status'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes 64 bytes of data (one sub-page) to the flash at the current index and
increments the index by one sub-page. The next index is returned together with
a status. The status is *Busy* if the previous write has not finished yet, in
which case the data is not written and has to be sent again.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Erase Flash Sector',
'elements': [('Sector Index', 'uint16', 1, 'in'),
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Flash Status'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Erases the flash sector (4096 bytes) with the given index. The status is *Busy*
if an erase is already in progress.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Erase Flash',
'elements': [('Status', 'uint8', 1, 'out', {'constant_group': 'Flash Status'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Erases the complete flash. The status is *Busy* if an erase is already in
progress.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Status Bar',
'elements': [('Ethernet Status', 'uint32', 1, 'in'),
             ('WIFI Status', 'uint32', 1, 'in'),
             ('Hours', 'uint8', 1, 'in'),
             ('Minutes', 'uint8', 1, 'in'),
             ('Seconds', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the content of the status bar at the top of the display: the Ethernet and
WiFi connection status and the current time (hours, minutes, seconds).
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Status Bar',
'elements': [('Ethernet Status', 'uint32', 1, 'out'),
             ('WIFI Status', 'uint32', 1, 'out'),
             ('Hours', 'uint8', 1, 'out'),
             ('Minutes', 'uint8', 1, 'out'),
             ('Seconds', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the status bar content as set by :func:`Set Status Bar`.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Display Page Index',
'elements': [('Page Index', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the index of the currently shown display page.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Display Page Index',
'elements': [('Page Index', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the index of the currently shown display page as set by
:func:`Set Display Page Index`.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Display Front Page Icon',
'elements': [('Icon Index', 'uint32', 1, 'in'),
             ('Active', 'bool', 1, 'in'),
             ('Sprite Index', 'uint32', 1, 'in'),
             ('Text 1', 'char', 6, 'in'),
             ('Font Index 1', 'uint8', 1, 'in'),
             ('Text 2', 'char', 6, 'in'),
             ('Font Index 2', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Configures one of the up to 13 icons (icon index 0-12) on the front page. Each
icon consists of a sprite and two lines of text with a configurable font. Set
Active to *true* to show the icon or *false* to hide it. The sprite and fonts
have to be present in the flash, see :func:`Set Flash Data`.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Display Front Page Icon',
'elements': [('Icon Index', 'uint32', 1, 'in'),
             ('Active', 'bool', 1, 'out'),
             ('Sprite Index', 'uint32', 1, 'out'),
             ('Text 1', 'char', 10, 'out'),
             ('Font Index 1', 'uint8', 1, 'out'),
             ('Text 2', 'char', 10, 'out'),
             ('Font Index 2', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the configuration of the given front page icon as set by
:func:`Set Display Front Page Icon`.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Display Wifi Setup 1',
'elements': [('IP Address', 'char', 15, 'in'),
             ('SSID', 'char', 49, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the IP address and SSID shown on the WiFi setup page. Together with the
password (see :func:`Set Display Wifi Setup 2`) a QR code for WiFi access is
generated.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Display Wifi Setup 1',
'elements': [('IP Address', 'char', 15, 'out'),
             ('SSID', 'char', 49, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the IP address and SSID as set by :func:`Set Display Wifi Setup 1`.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Display Wifi Setup 2',
'elements': [('Password', 'char', 64, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the WiFi password shown on the WiFi setup page, see
:func:`Set Display Wifi Setup 1`.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Display Wifi Setup 2',
'elements': [('Password', 'char', 64, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the WiFi password as set by :func:`Set Display Wifi Setup 2`.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set LED State',
'elements': [('Pattern', 'uint8', 1, 'in', {'constant_group': 'LED Pattern'}),
             ('Color', 'uint8', 1, 'in', {'constant_group': 'LED Color'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the pattern (off, on, blinking or breathing) and the color (green, red or
yellow) of the status LED.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get LED State',
'elements': [('Pattern', 'uint8', 1, 'out', {'constant_group': 'LED Pattern'}),
             ('Color', 'uint8', 1, 'out', {'constant_group': 'LED Color'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the LED state as set by :func:`Set LED State`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Display',
'elements': [('Display', 'uint8', 1, 'in', {'constant_group': 'Display'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the display mode. In *Off* the display is turned off. In *Automatic* the
display is turned on and switches off again after a countdown (see
:func:`Get Display`).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Display',
'elements': [('Display', 'uint8', 1, 'out', {'constant_group': 'Display'}),
             ('Countdown', 'uint32', 1, 'out')], # in ms, 0 = Off
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the display mode as set by :func:`Set Display` and the remaining
countdown in ms until the display turns off (0 if the display is off).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Flash Metadata',
'elements': [('Version Flash', 'uint32', 1, 'out'),
             ('Version Expected', 'uint32', 1, 'out'),
             ('Length Flash', 'uint32', 1, 'out'),
             ('Length Expected', 'uint32', 1, 'out'),
             ('Checksum Flash', 'uint32', 1, 'out'),
             ('Checksum Expected', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the metadata (version, length and checksum) of the data currently in
the flash together with the values expected by the firmware. This can be used
to check whether the flash content (sprites and fonts) is up to date.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Flash Data Done',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when a flash write triggered by
:func:`Set Flash Data` is done.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Redraw Everything',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Triggers a complete redraw of the display.
""",
'de':
"""
TODO
"""
}]
})
