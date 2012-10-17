# -*- coding: utf-8 -*-

# Industrial Digital Out 4 Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'binding_version': [1, 0, 0],
    'category': 'Bricklet',
    'name': ('IndustrialDigitalOut4', 'industrial_digital_out_4', 'Industrial Digital Out 4'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for controlling up to 4 optically coupled digital outputs',
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
Sets the output value with a bitmask. The bitmask
is 16 bit long, *true* refers to high and *false* refers to 
low.

For example: The value 0b0000000000000011 will turn pins 0-1 
high and the other pins low.

If no groups are used (see :func:`SetGroup`), the pins correspond to the
markings on the Digital Out 4 Bricklet.

If groups are used, the pins correspond to the element in the group.
Element 1 in the group will get pins 0-3, element 2 pins 4-7, element 3
pins 8-11 and element 4 pins 12-15.
""",
'de':
"""
Setzt die Ausgabewerte mit einer Bitmaske. Die Bitmaske ist 16 Bit lang.
*true* bedeutet logisch 1 und *false* logisch 0.

Zum Beispiel: Der Wert 0b0000000000000011 wird die Pins 0-1 auf logisch 1
und alle anderen auf logisch 0 setzen.

Falls keine Gruppen verwendet werden (siehe :func:`SetGroup`), entsprechen
die Pins der Beschriftung auf dem Digital Out 4 Bricklet.

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
'elements': [('pin_mask', 'uint16', 1, 'in'),
             ('value_mask', 'uint16', 1, 'in'),
             ('time', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Configures a monoflop of the pins specified by the first parameter
bitmask.

The second parameter is a bitmask with the desired value of the specified
pins (*true* means high and *false* means low).

The third parameter indicates the time (in ms) that the pins should hold
the value.

If this function is called with the parameters 
((1 << 0) | (1 << 3), (1 << 0), 1500):
Pin 0 will get high and pin 3 will get low. In 1.5s pin 0 will get low and
pin 3 will get high again.

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
festgelegten Pins (*true* bedeutet logisch 1 und *false* bedeutet logisch 0).

Der dritte Parameter stellt die Zeit (in ms) dar, welche die Pins den Zustand
halten sollen.

Wenn diese Funktion mit den Parametern ((1 << 0) | (1 << 3), (1 << 0), 1500)
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
Sets a group of Digital Out 4 Bricklets that should work together. You can
find Bricklets that can be grouped together with :func:`GetAvailableForGroup`.

The group consists of 4 elements. Element 1 in the group will get pins 0-3,
element 2 pins 4-7, element 3 pins 8-11 and element 4 pins 12-15.

Each element can either be one of the ports ('a' to 'd') or 'n' if it should
not be used.

For example: If you have two Digital Out 4 Bricklets connected to port A and
port B respectively, you could call with "['a', 'b', 'n', 'n']".

Now the pins on the Digital Out 4 on port A are assigned to 0-3 and the
pins on the Digital Out 4 on port B are assigned to 4-7. It is now possible
to call :func:`SetValue` and control two Bricklets at the same time.
""",
'de':
"""
Setzt eine Gruppe von Digital Out 4 Bricklets die zusammenarbeiten sollen.
Mögliche Gruppierungen können mit der Funktion :func:`GetAvailableForGroup`
gefunden werden.

Eine Gruppe besteht aus 4 Element. Element 1 in der Gruppe bekommt Pins 0-3,
Element 2 Pins 4-7, Element 3 Pins 8-11 und Element 4 Pins 12-15.

Jedes Element kann entweder auf einen der Ports ('a' bis 'd') gesetzt werden
oder falls nicht genutzt 'n' gesetzt werden.

Zum Beispiel: Falls zwei Digital Out 4 Bricklets mit Port A und Port B verbunden
sind, könnte diese Funktion mit "['a', 'b', 'n', 'n']" aufgerufen werden.

In diesem Fall wären die Pins von Port A den Werten 0-3 zugewiesen und
die Pins von Port B den Werten 4-7. Es ist jetzt möglich mit der Funktion
:func:`SetValue` beide Bricklets gleichzeitig zu kontrollieren.
"""
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
value 0b0101 means: Port *A* and Port *C* are connected to Bricklets that
can be grouped together.
""",
'de':
"""
Gibt eine Bitmaske von Ports zurück die für die Gruppierung zur Verfügung
stehen. Zum Beispiel bedeutet der Wert 0b0101: Port *A* und Port *C* sind
mit Bricklets verbunden die zusammen gruppiert werden können.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('MonoflopDone', 'monoflop_done'),
'elements': [('pin_mask', 'uint16', 1, 'out'),
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
