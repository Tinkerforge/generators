# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# IO-4 Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'category': 'Bricklet',
    'device_identifier': 2111,
    'name': 'IO4 V2',
    'display_name': 'IO-4 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '4-channel digital input/output',
        'de': '4 digitale Ein- und Ausgänge'
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
'name': 'Set Value',
'elements': [('Value', 'bool', 4, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the output value (high or low) with a bitmask (4bit). A 1 in the bitmask
means high and a 0 in the bitmask means low.

For example: The value 3 or 0b0011 will turn the pins 0-1 high and the
pins 2-3 low.

.. note::
 This function does nothing for pins that are configured as input.
 Pull-up resistors can be switched on with :func:`Set Configuration`.
""",
'de':
"""
Setzt den Ausgangszustand (logisch 1 oder logisch 0) mittels einer Bitmaske
(4Bit). Eine 1 in der Bitmaske bedeutet logisch 1 und eine 0 in der Bitmaske
bedeutet logisch 0.

Beispiel: Der Wert 3 bzw. 0b0011 setzt die Pins 0-1 auf logisch 1 und die
Pins 2-3 auf logisch 0.

.. note::
 Diese Funktion bewirkt keine Änderung an Pins die als Eingang konfiguriert sind.
 Pull-Up Widerstände können mit :func:`Set Configuration` zugeschaltet werden.
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Get Value',
'elements': [('Value', 'bool', 4, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns a bitmask of the values that are currently measured.
This function works if the pin is configured to input
as well as if it is configured to output.
""",
'de':
"""
Gibt eine Bitmaske der aktuell gemessenen Zustände zurück.
Diese Funktion gibt die Zustände aller Pins zurück, unabhängig ob diese als
Ein- oder Ausgang konfiguriert sind.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Selected Value',
'elements': [('Pin', 'uint8', 1, 'in'),
             ('Value', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TBD
""",
'de':
"""
TBD
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Selected Value',
'elements': [('Pin', 'uint8', 1, 'in'),
             ('Value', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TBD
""",
'de':
"""
TBD
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('Pin', 'bool', 1, 'in'),
             ('Direction', 'char', 1, 'in', ('Direction', [('In', 'i'),
                                                           ('Out', 'o')])),
             ('Value', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Configures the value and direction of the specified pins. Possible directions
are 'i' and 'o' for input and output.

If the direction is configured as output, the value is either high or low
(set as *true* or *false*).

If the direction is configured as input, the value is either pull-up or
default (set as *true* or *false*).

For example:

* (15, 'i', true) or (0b1111, 'i', true) will set all pins of as input pull-up.
* (8, 'i', false) or (0b1000, 'i', false) will set pin 3 of as input default (floating if nothing is connected).
* (3, 'o', false) or (0b0011, 'o', false) will set pins 0 and 1 as output low.
* (4, 'o', true) or (0b0100, 'o', true) will set pin 2 of as output high.

The default configuration is input with pull-up.
""",
'de':
"""
Konfiguriert den Zustand und die Richtung eines angegebenen Pins. Mögliche
Richtungen sind 'i' und 'o' für Ein- und Ausgang.

Wenn die Richtung als Ausgang konfiguriert ist, ist der Zustand entweder
logisch 1 oder logisch 0 (gesetzt als *true* oder *false*).

Wenn die Richtung als Eingang konfiguriert ist, ist der Zustand entweder
Pull-Up oder Standard (gesetzt als *true* oder *false*).

Beispiele:

* (15, 'i', true) bzw. (0b1111, 'i', true) setzt alle Pins als Eingang mit Pull-Up.
* (8, 'i', false) bzw. (0b1000, 'i', false) setzt Pin 3 als Standard Eingang (potentialfrei wenn nicht verbunden).
* (3, 'o', false) bzw. (0b0011, 'o', false) setzt die Pins 0 und 1 als Ausgang im Zustand logisch 0.
* (4, 'o', true) bzw. (0b0100, 'o', true) setzt Pin 2 als Ausgang im Zustand logisch 1.

Die Standardkonfiguration ist Eingang mit Pull-Up.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Pin', 'uint8', 1, 'in'),
             ('Direction', 'char', 1, 'out', ('Direction', [('In', 'i'),
                                                           ('Out', 'o')])),
             ('Value', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns a value bitmask and a direction bitmask. A 1 in the direction bitmask
means input and a 0 in the bitmask means output.

For example: A return value of (3, 5) or (0b0011, 0b0101) for direction and
value means that:

* pin 0 is configured as input pull-up,
* pin 1 is configured as input default,
* pin 2 is configured as output high and
* pin 3 is are configured as output low.
""",
'de':
"""
Gibt eine Bitmaske für die Richtung und eine Bitmaske für den Zustand der Pins
zurück. Eine 1 in der Bitmaske für die Richtung bedeutet Eingang und eine 0
in der Bitmaske bedeutet Ausgang.

Beispiel: Ein Rückgabewert von (3, 5) bzw. (0b0011, 0b0101) für Richtung und
Zustand bedeutet:

* Pin 0 ist als Eingang mit Pull-Up konfiguriert,
* Pin 1 ist als Standard Eingang konfiguriert,
* Pin 2 ist als Ausgang im Zustand logisch 1 konfiguriert und
* Pin 3 ist als Ausgang im Zustand logisch 0 konfiguriert.
"""
}]
})


# Interrupt, Monoflop, Edge Count

