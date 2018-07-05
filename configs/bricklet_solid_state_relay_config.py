# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Solid State Relay Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 244,
    'name': 'Solid State Relay',
    'display_name': 'Solid State Relay',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Controls AC and DC Solid State Relays',
        'de': 'Schaltet AC und DC Halbleiterrelais (Solid State Relais)'
    },
    'released': True,
    'documented': True,
    'discontinued': False, # selling remaining stock, replaced by Solid State Relay Bricklet 2.0
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Set State',
'elements': [('State', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the state of the relays *true* means on and *false* means off.

Running monoflop timers will be overwritten if this function is called.

The default value is *false*.
""",
'de':
"""
Setzt den Zustand des Relais, *true* bedeutet ein und *false* aus.

Laufende Monoflop Timer werden überschrieben wenn diese Funktion aufgerufen wird.

Der Standardwert ist *false*.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get State',
'elements': [('State', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the state of the relay, *true* means on and *false* means off.
""",
'de':
"""
Gibt den Zustand der Relais zurück, *true* bedeutet ein und *false* aus.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Monoflop',
'elements': [('State', 'bool', 1, 'in'),
             ('Time', 'uint32', 1, 'in')],
'since_firmware': [1, 1, 1],
'doc': ['af', {
'en':
"""
The first parameter  is the desired state of the relay (*true* means on
and *false* means off). The second parameter indicates the time (in ms) that
the relay should hold the state.

If this function is called with the parameters (true, 1500):
The relay will turn on and in 1.5s it will turn off again.

A monoflop can be used as a failsafe mechanism. For example: Lets assume you
have a RS485 bus and a Solid State Relay Bricklet connected to one of the slave
stacks. You can now call this function every second, with a time parameter
of two seconds. The relay will be on all the time. If now the RS485
connection is lost, the relay will turn off in at most two seconds.
""",
'de':
"""
Der erste Parameter ist der gewünschte Zustand des Relais
(*true* bedeutet ein und *false* aus). Der zweite Parameter stellt die Zeit
(in ms) dar, welche das Relais den Zustand halten soll.

Wenn diese Funktion mit den Parametern (true, 1500) aufgerufen wird:
Das Relais wird angeschaltet und nach 1,5s wieder ausgeschaltet.

Ein Monoflop kann als Ausfallsicherung verwendet werden. Beispiel:
Angenommen ein RS485 Bus und ein Dual Relay Bricklet ist an ein Slave Stapel
verbunden. Jetzt kann diese Funktion sekündlich, mit einem Zeitparameter
von 2 Sekunden, aufgerufen werden.
Das Relais wird die gesamte Zeit ein sein. Wenn jetzt die RS485 Verbindung
getrennt wird, wird das Relais nach spätestens zwei Sekunden ausschalten.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Monoflop',
'elements': [('State', 'bool', 1, 'out'),
             ('Time', 'uint32', 1, 'out'),
             ('Time Remaining', 'uint32', 1, 'out')],
'since_firmware': [1, 1, 1],
'doc': ['af', {
'en':
"""
Returns the current state and the time as set by
:func:`Set Monoflop` as well as the remaining time until the state flips.

If the timer is not running currently, the remaining time will be returned
as 0.
""",
'de':
"""
Gibt den aktuellen Zustand und die Zeit, wie von
:func:`Set Monoflop` gesetzt, sowie die noch verbleibende Zeit bis zum
Zustandswechsel, zurück.

Wenn der Timer aktuell nicht läuft, ist die noch verbleibende Zeit 0.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Monoflop Done',
'elements': [('State', 'bool', 1, 'out')],
'since_firmware': [1, 1, 1],
'doc': ['c', {
'en':
"""
This callback is triggered whenever the monoflop timer reaches 0.
The parameter is the current state of the relay
(the state after the monoflop).
""",
'de':
"""
Dieser Callback wird ausgelöst wenn ein Monoflop Timer abläuft (0 erreicht).
Der Parameter ist der aktuellen Zustand des Relais
(der Zustand nach dem Monoflop).
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('loop_header', 5, 'Turn relay on/off 10 times with 1 second delay'),
              ('sleep', 1000, None, None),
              ('setter', 'Set State', [('bool', True)], None, None),
              ('sleep', 1000, None, None),
              ('setter', 'Set State', [('bool', False)], None, None),
              ('loop_footer',)]
})
