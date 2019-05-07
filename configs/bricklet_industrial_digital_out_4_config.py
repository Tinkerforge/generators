# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Digital Out 4 Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 224,
    'name': 'Industrial Digital Out 4',
    'display_name': 'Industrial Digital Out 4',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '4 galvanically isolated digital outputs',
        'de': '4 galvanisch getrennte digitale Ausgänge'
    },
    'released': True,
    'documented': True,
    'discontinued': False, # selling remaining stock, replaced by Industrial Digital Out 4 Bricklet 2.0
    'features': [
        'bricklet_get_identity'
    ],
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Set Value',
'elements': [('Value Mask', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the output value with a bitmask (16bit). A 1 in the bitmask means high
and a 0 in the bitmask means low.

For example: The value 3 or 0b0011 will turn pins 0-1 high and the other pins
low.

If no groups are used (see :func:`Set Group`), the pins correspond to the
markings on the Industrial Digital Out 4 Bricklet.

If groups are used, the pins correspond to the element in the group.
Element 1 in the group will get pins 0-3, element 2 pins 4-7, element 3
pins 8-11 and element 4 pins 12-15.

All running monoflop timers will be aborted if this function is called.
""",
'de':
"""
Setzt die Ausgabewerte mit einer Bitmaske (16Bit). Eine 1 in der Bitmaske
bedeutet logisch 1 und eine 0 in der Bitmaske bedeutet logisch 0.

Zum Beispiel: Der Wert 3 bzw. 0b0011 wird die Pins 0-1 auf logisch 1
und alle anderen auf logisch 0 setzen.

Falls keine Gruppen verwendet werden (siehe :func:`Set Group`), entsprechen
die Pins der Beschriftung auf dem Industrial Digital Out 4 Bricklet.

Falls Gruppen verwendet werden, entsprechen die Pins den Elementen der
Gruppe. Element 1 in der Gruppe bekommt Pins 0-3,
Element 2 Pins 4-7, Element 3 Pins 8-11 und Element 4 Pins 12-15.

Alle laufenden Monoflop Timer werden abgebrochen, wenn diese Funktion aufgerufen
wird.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Value',
'elements': [('Value Mask', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the bitmask as set by :func:`Set Value`.
""",
'de':
"""
Gibt die Bitmaske zurück, wie von :func:`Set Value` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Monoflop',
'elements': [('Selection Mask', 'uint16', 1, 'in'),
             ('Value Mask', 'uint16', 1, 'in'),
             ('Time', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Configures a monoflop of the pins specified by the first parameter
bitmask.

The second parameter is a bitmask with the desired value of the specified
pins. A 1 in the bitmask means high and a 0 in the bitmask means low.

The third parameter indicates the time (in ms) that the pins should hold
the value.

If this function is called with the parameters (9, 1, 1500) or
(0b1001, 0b0001, 1500): Pin 0 will get high and pin 3 will get low. In 1.5s
pin 0 will get low and pin 3 will get high again.

A monoflop can be used as a fail-safe mechanism. For example: Lets assume you
have a RS485 bus and a Digital Out 4 Bricklet connected to one of the slave
stacks. You can now call this function every second, with a time parameter
of two seconds and pin 0 high. Pin 0 will be high all the time. If now
the RS485 connection is lost, then pin 0 will turn low in at most two seconds.
""",
'de':
"""
Konfiguriert einen Monoflop für die Pins, wie mittels der Bitmaske
des ersten Parameters festgelegt.

Der zweite Parameter ist eine Bitmaske mit den gewünschten Zuständen der
festgelegten Pins. Eine 1 in der Bitmaske bedeutet logisch 1 und
eine 0 in der Bitmaske bedeutet logisch 0.

Der dritte Parameter stellt die Zeit (in ms) dar, welche die Pins den Zustand
halten sollen.

Wenn diese Funktion mit den Parametern (9, 1, 1500) bzw. (0b1001, 0b0001, 1500)
aufgerufen wird: Pin 0 wird auf logisch 1 und Pin 3 auf logisch 0 gesetzt.
Nach 1,5s wird Pin 0 wieder auf logisch 0 und Pin 3 auf logisch 1 gesetzt.

Ein Monoflop kann zur Ausfallsicherung verwendet werden. Beispiel:
Angenommen ein RS485 Bus und ein Digital Out 4 Bricklet ist an ein Slave
Stapel verbunden.
Jetzt kann diese Funktion sekündlich, mit einem Zeitparameter von 2 Sekunden,
aufgerufen werden. Der Pin wird die gesamte Zeit im Zustand logisch 1 sein.
Wenn jetzt die RS485 Verbindung getrennt wird, wird der Pin nach spätestens
zwei Sekunden in den Zustand logisch 0 wechseln.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Monoflop',
'elements': [('Pin', 'uint8', 1, 'in'),
             ('Value', 'uint16', 1, 'out'),
             ('Time', 'uint32', 1, 'out'),
             ('Time Remaining', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns (for the given pin) the current value and the time as set by
:func:`Set Monoflop` as well as the remaining time until the value flips.

If the timer is not running currently, the remaining time will be returned
as 0.
""",
'de':
"""
Gibt (für den angegebenen Pin) den aktuellen Zustand und die Zeit, wie von
:func:`Set Monoflop` gesetzt, sowie die noch verbleibende Zeit bis zum
Zustandswechsel, zurück.

Wenn der Timer aktuell nicht läuft, ist die noch verbleibende Zeit 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Group',
'elements': [('Group', 'char', 4, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets a group of Digital Out 4 Bricklets that should work together. You can
find Bricklets that can be grouped together with :func:`Get Available For Group`.

The group consists of 4 elements. Element 1 in the group will get pins 0-3,
element 2 pins 4-7, element 3 pins 8-11 and element 4 pins 12-15.

Each element can either be one of the ports ('a' to 'd') or 'n' if it should
not be used.

For example: If you have two Digital Out 4 Bricklets connected to port A and
port B respectively, you could call with |abnn|.

Now the pins on the Digital Out 4 on port A are assigned to 0-3 and the
pins on the Digital Out 4 on port B are assigned to 4-7. It is now possible
to call :func:`Set Value` and control two Bricklets at the same time.
""",
'de':
"""
Setzt eine Gruppe von Digital Out 4 Bricklets die zusammenarbeiten sollen.
Mögliche Gruppierungen können mit der Funktion :func:`Get Available For Group`
gefunden werden.

Eine Gruppe besteht aus 4 Element. Element 1 in der Gruppe bekommt Pins 0-3,
Element 2 Pins 4-7, Element 3 Pins 8-11 und Element 4 Pins 12-15.

Jedes Element kann entweder auf einen der Ports ('a' bis 'd') gesetzt werden
oder falls nicht genutzt 'n' gesetzt werden.

Zum Beispiel: Falls zwei Digital Out 4 Bricklets mit Port A und Port B verbunden
sind, könnte diese Funktion mit |abnn| aufgerufen werden.

In diesem Fall wären die Pins von Port A den Werten 0-3 zugewiesen und
die Pins von Port B den Werten 4-7. Es ist jetzt möglich mit der Funktion
:func:`Set Value` beide Bricklets gleichzeitig zu kontrollieren.
"""
},
{
'*': {
'abnn': {'php': "``array('a', 'b', 'n', 'n')``",
         '*': "``['a', 'b', 'n', 'n']``"}
}
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Group',
'elements': [('Group', 'char', 4, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the group as set by :func:`Set Group`
""",
'de':
"""
Gibt die Gruppierung zurück, wie von :func:`Set Group` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Available For Group',
'elements': [('Available', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns a bitmask of ports that are available for grouping. For example the
value 5 or 0b0101 means: Port A and port C are connected to Bricklets that
can be grouped together.
""",
'de':
"""
Gibt eine Bitmaske von Ports zurück die für die Gruppierung zur Verfügung
stehen. Zum Beispiel bedeutet der Wert 5 bzw. 0b0101: Port A und Port C sind
mit Bricklets verbunden die zusammen gruppiert werden können.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Monoflop Done',
'elements': [('Selection Mask', 'uint16', 1, 'out'),
             ('Value Mask', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered whenever a monoflop timer reaches 0. The
:word:`parameters` contain the involved pins and the current value of the pins
(the value after the monoflop).
""",
'de':
"""
Dieser Callback wird ausgelöst wenn ein Monoflop Timer abläuft (0 erreicht).
:word:`parameters` enthalten die beteiligten Pins als Bitmaske und den aktuellen
Zustand als Bitmaske (der Zustand nach dem Monoflop).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Selected Values',
'elements': [('Selection Mask', 'uint16', 1, 'in'),
             ('Value Mask', 'uint16', 1, 'in')],
'since_firmware': [2, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the output value with a bitmask, according to the selection mask.
The bitmask is 16 bit long, *true* refers to high and *false* refers to
low.

For example: The values (3, 1) or (0b0011, 0b0001) will turn pin 0 high, pin 1
low the other pins remain untouched.

If no groups are used (see :func:`Set Group`), the pins correspond to the
markings on the Industrial Digital Out 4 Bricklet.

If groups are used, the pins correspond to the element in the group.
Element 1 in the group will get pins 0-3, element 2 pins 4-7, element 3
pins 8-11 and element 4 pins 12-15.

Running monoflop timers for the selected pins will be aborted if this function
is called.
""",
'de':
"""
Setzt die Ausgabewerte mit einer Bitmaske, entsprechend der Selektionsmaske.
Die Bitmaske ist 16 Bit lang. *true* bedeutet logisch 1 und *false* logisch 0.

Zum Beispiel: Die Werte (3, 1) bzw. (0b0011, 0b0001) werden den Pin 0 auf
logisch 1 und den Pin 1 auf logisch 0 setzen. Alle anderen Pins bleiben
unangetastet.

Falls keine Gruppen verwendet werden (siehe :func:`Set Group`), entsprechen
die Pins der Beschriftung auf dem Industrial Digital Out 4 Bricklet.

Falls Gruppen verwendet werden, entsprechen die Pins den Elementen der
Gruppe. Element 1 in der Gruppe bekommt Pins 0-3,
Element 2 Pins 4-7, Element 3 Pins 8-11 und Element 4 Pins 12-15.

Laufende Monoflop Timer für die ausgewählten Pins werden abgebrochen, wenn
diese Funktion aufgerufen wird.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('loop_header', 10, 'Set pins alternating high/low 10 times with 100ms delay'),
              ('sleep', 100, None, None),
              ('setter', 'Set Value', [('uint16:bitmask:4', 1 << 0)], None, None),
              ('sleep', 100, None, None),
              ('setter', 'Set Value', [('uint16:bitmask:4', 1 << 1)], None, None),
              ('sleep', 100, None, None),
              ('setter', 'Set Value', [('uint16:bitmask:4', 1 << 2)], None, None),
              ('sleep', 100, None, None),
              ('setter', 'Set Value', [('uint16:bitmask:4', 1 << 3)], None, None),
              ('loop_footer',)]
})
