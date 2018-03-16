# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Digital In 4 Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
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
'name': 'Get Input Value',
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
'name': 'Set Input Value Callback Configuration',
'elements': [('Pin', 'uint8', 1, 'in'),
             ('Enable', 'uint8', 1, 'in'),
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
'elements': [('Pin', 'uint8', 1, 'in'),
             ('Enable', 'bool', 1, 'out'),
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
'type': 'callback',
'name': 'Input Value',
'elements': [('Enabled', 'bool', 4, 'out'),
             ('Changed', 'bool', 4, 'out'),
             ('Value', 'bool', 4, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered whenever a change of the voltage level is detected
on pins where the interrupt was activated with :func:`Set Input Value Callback Configuration`.

The values are a bitmask that specifies which interrupts occurred
and the current value bitmask.

For example:

* (1, 1) or (0b0001, 0b0001) means that an interrupt on pin 0 occurred and
  currently pin 0 is high and pins 1-3 are low.
* (9, 14) or (0b1001, 0b1110) means that interrupts on pins 0 and 3
  occurred and currently pin 0 is low and pins 1-3 are high.
""",
'de':
"""
Dieser Callback wird ausgelöst sobald eine Änderung des Spannungspegels
detektiert wird, an Pins für welche der Interrupt mit :func:`Set Input Value Callback Configuration`
aktiviert wurde.

Die Rückgabewerte sind eine Bitmaske der aufgetretenen Interrupts und der
aktuellen Zustände.

Beispiele:

* (1, 1) bzw. (0b0001, 0b0001) bedeutet, dass ein Interrupt am Pin 0 aufgetreten
  ist und aktuell Pin 0 logisch 1 ist und die Pins 1-3 logisch 0 sind.
* (9, 14) bzw. (0b1001, 0b1110) bedeutet, dass Interrupts an den Pins 0 und 3
  aufgetreten sind und aktuell Pin 0 logisch 0 ist und die Pins 1-3 logisch 1 sind.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Edge Count',
'elements': [('Pin', 'uint8', 1, 'in'),
             ('Reset Counter', 'bool', 1, 'in'),
             ('Count', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the current value of the edge counter for the selected pin. You can
configure the edges that are counted with :func:`Set Edge Count Configuration`.

If you set the reset counter to *true*, the count is set back to 0
directly after it is read.
""",
'de':
"""
Gibt den aktuellen Wert des Flankenzählers für den ausgewählten Pin zurück. Die
zu zählenden Flanken können mit :func:`Set Edge Count Configuration` konfiguriert werden.

Wenn reset counter auf *true* gesetzt wird, wird der Zählerstand direkt
nach dem auslesen auf 0 zurückgesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Edge Count Configuration',
'elements': [('Pin', 'uint8', 1, 'in'),
             ('Edge Type', 'uint8', 1, 'in', ('Edge Type', [('Rising', 0),
                                                            ('Falling', 1),
                                                            ('Both', 2)])),
             ('Debounce', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Configures the edge counter for the selected pins. A bitmask of 9 or 0b1001 will
enable the edge counter for pins 0 and 3.

The edge type parameter configures if rising edges, falling edges or
both are counted if the pin is configured for input. Possible edge types are:

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
Konfiguriert den Flankenzähler für die ausgewählten Pins. Eine Bitmaske von 9
bzw. 0b1001 aktiviert den Flankenzähler für die Pins 0 und 3.

Der edge type Parameter konfiguriert den zu zählenden Flankentyp. Es können
steigende, fallende oder beide Flanken gezählt werden für Pins die als Eingang
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
'elements': [('Pin', 'uint8', 1, 'in'),
             ('Edge Type', 'uint8', 1, 'out', ('Edge Type', [('Rising', 0),
                                                             ('Falling', 1),
                                                             ('Both', 2)])),
             ('Debounce', 'uint8', 1, 'out')],
'since_firmware': [2, 0, 1],
'doc': ['af', {
'en':
"""
Returns the edge type and debounce time for the selected pin as set by
:func:`Set Edge Count Configuration`.
""",
'de':
"""
Gibt den Flankentyp sowie die Entprellzeit für den ausgewählten Pin zurück,
wie von :func:`Set Edge Count Configuration` gesetzt.
"""
}]
})

