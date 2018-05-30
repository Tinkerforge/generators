# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Digital Out 4 Bricklet 2.0 communication config

# TODO: Documentation and examples.

com = {
    'author': 'Ishraq Ibne Ashraf <ishraq@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2124,
    'name': 'Industrial Digital Out 4 V2',
    'display_name': 'Industrial Digital Out 4 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '4 galvanically isolated digital outputs',
        'de': '4 galvanisch getrennte digitale Ausgänge'
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
Sets the output value of all four Channels. A value of *true* or *false* outputs
logic 1 or logic 0 respectively on the corresponding channel.

Use :func:`Set Selected Value` to change only one output channel state.

For example: (True, True, False, False) will turn the channels 0-1 high and the
channels 2-3 low.
""",
'de':
"""
Beispiel: (True, True, False, False) setzt die Channels 0-1 auf logisch 1 und die
Channels 2-3 auf logisch 0.
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
Returns the logic levels that are currently measured on the channels.
""",
'de':
"""
Gibt die aktuell gemessenen Zustände zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Selected Value',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Value', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the output value of a specific channel without affecting the other channels.
""",
'de':
"""
Setzt den Ausgabewert des spezifizierte Channel ohne die anderen Channele zu
beeinflussen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Monoflop',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Value', 'bool', 1, 'in'),
             ('Time', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
The first parameter is the desired state of the channel (*true* means output *high*
and *false* means output *low*). The second parameter indicates the time (in ms) that
the channel should hold the state.

If this function is called with the parameters (true, 1500):
The channel will turn on and in 1.5s it will turn off again.

A monoflop can be used as a failsafe mechanism. For example: Lets assume you
have a RS485 bus and a IO4 Bricklet is connected to one of the slave
stacks. You can now call this function every second, with a time parameter
of two seconds. The channel will be *high* all the time. If now the RS485
connection is lost, the channel will turn *low* in at most two seconds.
""",
'de':
"""
Der erste Parameter ist der gewünschte Zustand des Kanals
(*true* bedeutet *high* und *false* *low*). Der zweite Parameter stellt die Zeit
(in ms) dar, in welcher der Kanal den Zustand halten soll.

Wenn diese Funktion mit den Parametern (true, 1500) aufgerufen wird:
Der Kanal wird angeschaltet und nach 1,5s wieder ausgeschaltet.

Ein Monoflop kann als Ausfallsicherung verwendet werden. Beispiel:
Angenommen ein RS485 Bus und ein IO4 Bricklet ist an ein Slave Stapel
verbunden. Jetzt kann diese Funktion sekündlich, mit einem Zeitparameter
von 2 Sekunden, aufgerufen werden.
Der Kanal wird die gesamte Zeit eingeschaltet sein. Wenn jetzt die RS485 Verbindung
getrennt wird, wird der Kanal nach spätestens zwei Sekunden ausschalten.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Monoflop',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Value', 'bool', 1, 'out'),
             ('Time', 'uint32', 1, 'out'),
             ('Time Remaining', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns (for the given channel) the current value and the time as set by
:func:`Set Monoflop` as well as the remaining time until the value flips.

If the timer is not running currently, the remaining time will be returned
as 0.
""",
'de':
"""
Gibt (für den angegebenen Channel) den aktuellen Zustand und die Zeit, wie von
:func:`Set Monoflop` gesetzt, sowie die noch verbleibende Zeit bis zum
Zustandswechsel, zurück.

Wenn der Timer aktuell nicht läuft, ist die noch verbleibende Zeit 0.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Monoflop Done',
'elements': [('Channel', 'uint8', 1, 'out'),
             ('Value', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered whenever a monoflop timer reaches 0. The
:word:`parameters` contain the channel and the current value of the channel
(the value after the monoflop).
""",
'de':
"""
Dieser Callback wird ausgelöst wenn ein Monoflop Timer abläuft (0 erreicht).
:word:`parameters` enthalten den Channel und den aktuellen
Zustand des Channels (der Zustand nach dem Monoflop).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Channel LED Config',
'elements': [('LED', 'uint8', 1, 'in'),
             ('Config', 'uint8', 1, 'in', ('Channel LED Config', [('Off', 0),
                                                                  ('On', 1),
                                                                  ('Show Heartbeat', 2),
                                                                  ('Show Channel Status', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Each channel has a corresponding LED. You can turn the LED Off, On or show a
heartbeat. You can also set the LED to "Channel Status". In this mode the
LED is on if the channel is high and off otherwise.

By default all channel LEDs are configured as "Channel Status".
""",
'de':
"""
Jeder Kanal hat eine dazugehörige LED. Die LEDs können individuell an oder
aus-geschaltet werden. Zusätzlich kann ein Hearbeat oder der Kanal-Status
angezeigt werden. Falls Kanal-Status gewählt wird ist die LED an wenn
ein High-Signal am Kanal anliegt und sonst aus.

Standardmäßig sind die LEDs für alle Kanäle auf "Kanal-Status" konfiguriert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Channel LED Config',
'elements': [('LED', 'uint8', 1, 'in'),
             ('Config', 'uint8', 1, 'out', ('Channel LED Config', [('Off', 0),
                                                                   ('On', 1),
                                                                   ('Show Heartbeat', 2),
                                                                   ('Show Channel Status', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the Channel LED configuration as set by :func:`Set Channel LED Config`
""",
'de':
"""
Gibt die LED-Konfiguration zurück, wie von :func:`Set Channel LED Config` gesetzt.
"""
}]
})
