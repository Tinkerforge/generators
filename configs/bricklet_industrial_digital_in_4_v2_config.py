# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Digital In 4 Bricklet communication config

# TODO: Documentation and examples.

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2100,
    'name': 'Industrial Digital In 4 V2',
    'display_name': 'Industrial Digital In 4 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '4 galvanically isolated digital inputs',
        'de': '4 galvanisch getrennte digitale Eingänge'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'discontinued': False,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Get Value',
'elements': [('Value', 'bool', 4, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the input value as bools, *true*
refers to high and *false* refers to low.
""",
'de':
"""
Gibt die Ausgabewerte als Bools zurück, *true* 
bedeutet logisch 1 und *false* logisch 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Selected Value',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Value', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the logic levels that are currently measured on a specific channel.
""",
'de':
"""
Gibt die aktuell gemessenen Zustand zurück die derzeit auf einem bestimmten Channel
gemessen werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Input Value Callback Configuration',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
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
'name': 'Get Input Value Callback Configuration',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
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
'name': 'Set All Input Value Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
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
'name': 'Get All Input Value Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
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
'name': 'Get Edge Count',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Reset Counter', 'bool', 1, 'in'),
             ('Count', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the current value of the edge counter for the selected channel. You can
configure the edges that are counted with :func:`Set Edge Count Configuration`.

If you set the reset counter to *true*, the count is set back to 0
directly after it is read.
""",
'de':
"""
Gibt den aktuellen Wert des Flankenzählers für den ausgewählten Channel zurück. Die
zu zählenden Flanken können mit :func:`Set Edge Count Configuration` konfiguriert werden.

Wenn reset counter auf *true* gesetzt wird, wird der Zählerstand direkt
nach dem auslesen auf 0 zurückgesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Edge Count Configuration',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Edge Type', 'uint8', 1, 'in', ('Edge Type', [('Rising', 0),
                                                            ('Falling', 1),
                                                            ('Both', 2)])),
             ('Debounce', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Configures the edge counter for a specific channel.

The edge type parameter configures if rising edges, falling edges or
both are counted if the channel is configured for input. Possible edge types are:

* 0 = rising (default)
* 1 = falling
* 2 = both

The debounce time is given in ms.

Configuring an edge counter resets its value to 0.

If you don't know what any of this means, just leave it at default. The
default configuration is very likely OK for you.

Default values: 0 (edge type) and 100ms (debounce time)
""",
'de':
"""
Konfiguriert den Flankenzähler für einen bestimmten Kanal.

Der edge type Parameter konfiguriert den zu zählenden Flankentyp. Es können
steigende, fallende oder beide Flanken gezählt werden für Channels die als Eingang
konfiguriert sind. Mögliche Flankentypen sind:

* 0 = steigend (Standard)
* 1 = fallend
* 2 = beide

Die Entprellzeit (debounce) wird in ms angegeben.

Durch das Konfigurieren wird der Wert des Flankenzählers auf 0 zurückgesetzt.

Falls unklar ist was dies alles bedeutet, kann diese Funktion einfach
ignoriert werden. Die Standardwerte sind in fast allen Situationen OK.

Standardwerte: 0 (edge type) und 100ms (debounce).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Edge Count Configuration',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Edge Type', 'uint8', 1, 'out', ('Edge Type', [('Rising', 0),
                                                             ('Falling', 1),
                                                             ('Both', 2)])),
             ('Debounce', 'uint8', 1, 'out')],
'since_firmware': [2, 0, 1],
'doc': ['af', {
'en':
"""
Returns the edge type and debounce time for the selected channel as set by
:func:`Set Edge Count Configuration`.
""",
'de':
"""
Gibt den Flankentyp sowie die Entprellzeit für den ausgewählten Channel zurück,
wie von :func:`Set Edge Count Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Info LED Config',
'elements': [('LED', 'uint8', 1, 'in'),
             ('Config', 'uint8', 1, 'in', ('Info LED Config', [('Off', 0),
                                                               ('On', 1),
                                                               ('Show Heartbeat', 2),
                                                               ('Show Channel Status', 3)]))],
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
'name': 'Get Info LED Config',
'elements': [('LED', 'uint8', 1, 'in'),
             ('Config', 'uint8', 1, 'out', ('Info LED Config', [('Off', 0),
                                                                ('On', 1),
                                                                ('Show Heartbeat', 2),
                                                                ('Show Channel Status', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the Info LED configuration as set by :func:`Set Info LED Config`
""",
'de':
"""
Gibt die LED-Konfiguration zurück, wie von :func:`Set Info LED Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Input Value',
'elements': [('Channel', 'uint8', 1, 'out'),
             ('Changed', 'bool', 1, 'out'),
             ('Value', 'bool', 1, 'out')],
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
'name': 'All Input Value',
'elements': [('Changed', 'bool', 4, 'out'),
             ('Value', 'bool', 4, 'out')],
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
