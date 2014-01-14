# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Quad Relay Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 225,
    'name': ('IndustrialQuadRelay', 'industrial_quad_relay', 'Industrial Quad Relay'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for controlling up to 4 Solid State Relays',
    'released': True,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('SetValue', 'set_value'),
'elements': [('value_mask', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the output value with a bitmask (16bit). A 1 in the bitmask means relay
closed and a 0 means relay open.

For example: The value 3 or 0b0011 will close the relay of pins 0-1 and open
the other pins.

If no groups are used (see :func:`SetGroup`), the pins correspond to the
markings on the Quad Relay Bricklet.

If groups are used, the pins correspond to the element in the group.
Element 1 in the group will get pins 0-3, element 2 pins 4-7, element 3
pins 8-11 and element 4 pins 12-15.
""",
'de':
"""
Setzt die Ausgabewerte mit einer Bitmaske (16Bit). Eine 1 in der Bitmaske
bedeutet Relais geschlossen und eine 0 in der Bitmaske bedeutet Relais offen.

Zum Beispiel: Der Wert 3 bzw. 0b0011 wird die Relais 0-1 schließen und alle
anderen öffnen.

Falls keine Gruppen verwendet werden (siehe :func:`SetGroup`), entsprechen
die Pins der Beschriftung auf dem Quad Relay Bricklet.

Falls Gruppen verwendet werden, entsprechen die Pins den Elementen der
Gruppe. Element 1 in der Gruppe bekommt Pins 0-3,
Element 2 Pins 4-7, Element 3 Pins 8-11 und Element 4 Pins 12-15.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetValue', 'get_value'),
'elements': [('value_mask', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the bitmask as set by :func:`SetValue`.
""",
'de':
"""
Gibt die Bitmaske zurück, wie von :func:`SetValue` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetMonoflop', 'set_monoflop'),
'elements': [('selection_mask', 'uint16', 1, 'in'),
             ('value_mask', 'uint16', 1, 'in'),
             ('time', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Configures a monoflop of the pins specified by the first parameter
bitmask.

The second parameter is a bitmask with the desired value of the specified
pins. A 1 in the bitmask means relay closed and a 0 means relay open.

The third parameter indicates the time (in ms) that the pins should hold
the value.

If this function is called with the parameters (9, 1, 1500) or
(0b1001, 0b0001, 1500): Pin 0 will close and pin 3 will open. In 1.5s pin 0
will open and pin 3 will close again.

A monoflop can be used as a fail-safe mechanism. For example: Lets assume you
have a RS485 bus and a Quad Relay Bricklet connected to one of the slave
stacks. You can now call this function every second, with a time parameter
of two seconds and pin 0 closed. Pin 0 will be closed all the time. If now
the RS485 connection is lost, then pin 0 will be opened in at most two seconds.
""",
'de':
"""
Konfiguriert einen Monoflop für die Pins, wie mittels der Bitmaske
des ersten Parameters festgelegt.

Der zweite Parameter ist eine Bitmaske mit den gewünschten Zuständen der
festgelegten Pins. Eine 1 in der Bitmaske bedeutet Relais geschlossen und
eine 0 in der Bitmaske bedeutet Relais offen.

Der dritte Parameter stellt die Zeit (in ms) dar, welche die Pins den Zustand
halten sollen.

Wenn diese Funktion mit den Parametern (9, 1, 1500) bzw. (0b1001, 0b0001, 1500)
aufgerufen wird: Pin 0 wird auf geschlossen und Pin 3 auf geöffnet gesetzt.
Nach 1,5s wird Pin 0 wieder geöffnet und Pin 3 geschlossen.

Ein Monoflop kann zur Ausfallsicherung verwendet werden. Beispiel:
Angenommen ein RS485 Bus und ein Quad Relay Bricklet ist an ein Slave 
Stapel verbunden.
Jetzt kann diese Funktion sekündlich, mit einem Zeitparameter von 2 Sekunden,
aufgerufen werden. Der Pin wird die gesamte Zeit im Zustand geschlossen sein.
Wenn jetzt die RS485 Verbindung getrennt wird, wird der Pin nach spätestens 
zwei Sekunden in den Zustand geöffnet wechseln.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetMonoflop', 'get_monoflop'),
'elements': [('pin', 'uint8', 1, 'in'),
             ('value', 'uint16', 1, 'out'),
             ('time', 'uint32', 1, 'out'),
             ('time_remaining', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns (for the given pin) the current value and the time as set by
:func:`SetMonoflop` as well as the remaining time until the value flips.

If the timer is not running currently, the remaining time will be returned
as 0.
""",
'de':
"""
Gibt (für den angegebenen Pin) den aktuellen Zustand und die Zeit, wie von 
:func:`SetMonoflop` gesetzt, sowie die noch verbleibende Zeit bis zum
Zustandswechsel, zurück.

Wenn der Timer aktuell nicht läuft, ist die noch verbleibende Zeit 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetGroup', 'set_group'),
'elements': [('group', 'char', 4, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets a group of Quad Relay Bricklets that should work together. You can
find Bricklets that can be grouped together with :func:`GetAvailableForGroup`.

The group consists of 4 elements. Element 1 in the group will get pins 0-3,
element 2 pins 4-7, element 3 pins 8-11 and element 4 pins 12-15.

Each element can either be one of the ports ('a' to 'd') or 'n' if it should
not be used.

For example: If you have two Quad Relay Bricklets connected to port A and
port B respectively, you could call with |abnn|.

Now the pins on the Quad Relay on port A are assigned to 0-3 and the
pins on the Quad Relay on port B are assigned to 4-7. It is now possible
to call :func:`SetValue` and control two Bricklets at the same time.
""",
'de':
"""
Setzt eine Gruppe von Quad Relay Bricklets die zusammenarbeiten sollen.
Mögliche Gruppierungen können mit der Funktion :func:`GetAvailableForGroup`
gefunden werden.

Eine Gruppe besteht aus 4 Element. Element 1 in der Gruppe bekommt Pins 0-3,
Element 2 Pins 4-7, Element 3 Pins 8-11 und Element 4 Pins 12-15.

Jedes Element kann entweder auf einen der Ports ('a' bis 'd') gesetzt werden
oder falls nicht genutzt 'n' gesetzt werden.

Zum Beispiel: Falls zwei Quad Relay Bricklets mit Port A und Port B verbunden
sind, könnte diese Funktion mit |abnn| aufgerufen werden.

In diesem Fall wären die Pins von Port A den Werten 0-3 zugewiesen und
die Pins von Port B den Werten 4-7. Es ist jetzt möglich mit der Funktion
:func:`SetValue` beide Bricklets gleichzeitig zu kontrollieren.
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
'name': ('GetGroup', 'get_group'),
'elements': [('group', 'char', 4, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the group as set by :func:`SetGroup`
""",
'de':
"""
Gibt die Gruppierung zurück, wie von :func:`SetGroup` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAvailableForGroup', 'get_available_for_group'),
'elements': [('available', 'uint8', 1, 'out')],
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
'name': ('MonoflopDone', 'monoflop_done'),
'elements': [('selection_mask', 'uint16', 1, 'out'),
             ('value_mask', 'uint16', 1, 'out')],
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
'name': ('SetSelectedValues', 'set_selected_values'),
'elements': [('selection_mask', 'uint16', 1, 'in'),
             ('value_mask', 'uint16', 1, 'in')],
'since_firmware': [2, 0, 0],
'doc': ['af', {
'en':
"""
Sets the output value with a bitmask, according to the selection mask. 
The bitmask is 16 bit long, *true* refers to a closed relay and 
*false* refers to an open relay.

For example: The values (3, 1) or (0b0011, 0b0001) will close the relay of
pin 0, open the relay of pin 1 and leave the others untouched.

If no groups are used (see :func:`SetGroup`), the pins correspond to the
markings on the Quad Relay Bricklet.

If groups are used, the pins correspond to the element in the group.
Element 1 in the group will get pins 0-3, element 2 pins 4-7, element 3
pins 8-11 and element 4 pins 12-15.
""",
'de':
"""
Setzt die Ausgabewerte mit einer Bitmaske, entsprechend der Selektionsmaske. 
Die Bitmaske ist 16 Bit lang.
*true* steht für ein geschlossenes Relais und *false* für ein offenes
Relay.

Zum Beispiel: Die Werte (3, 1) bzw. (0b0011, 0b0001) wird das Relais 0
schließen, das Relais 1 öffnen und alle anderen unangetastet lassen.

Falls keine Gruppen verwendet werden (siehe :func:`SetGroup`), entsprechen
die Pins der Beschriftung auf dem Quad Relay Bricklet.

Falls Gruppen verwendet werden, entsprechen die Pins den Elementen der
Gruppe. Element 1 in der Gruppe bekommt Pins 0-3,
Element 2 Pins 4-7, Element 3 Pins 8-11 und Element 4 Pins 12-15.
"""
}]
})
