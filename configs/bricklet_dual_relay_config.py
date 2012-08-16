# -*- coding: utf-8 -*-

# Dual Relay Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'version': [1, 0, 1],
    'category': 'Bricklet',
    'name': ('DualRelay', 'dual_relay', 'Dual Relay'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for controlling two relays',
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('SetState', 'set_state'), 
'elements': [('relay1', 'bool', 1, 'in'),
             ('relay2', 'bool', 1, 'in')],
'doc': ['bm', {
'en':
"""
Sets the state of the relays, *true* means on and *false* means off. 
For example: (true, false) turns relay 1 on and relay 2 off.

If you just want to set one of the relays and don't know the current state
of the other relay, you can get the state with :func:`GetState`.

Running monoflop timers will be overwritten if this function is called.

The default value is (false, false).
""",
'de':
"""
Setzt den Zustand der Relais, *true* bedeutet ein und *false* aus.
Beispiel: (true, false) schaltet Relais 1 ein und Relais 2 aus.

Wenn nur eines der Relais gesetzt werden soll und der aktuelle Zustand des anderen Relais
nicht bekannt ist, dann kann der Zustand mit :func:`GetState` ausgelesen werden.

Laufende Monoflop Timer werden überschrieben wenn diese Funktion aufgerufen wird.

Der Standardwert ist (false, false).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetState', 'get_state'), 
'elements': [('relay1', 'bool', 1, 'out'),
             ('relay2', 'bool', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns the state of the relays, *true* means on and *false* means off. 
""",
'de':
"""
Gibt den Zustand der Relais zurück, *true* bedeutet ein und *false* aus.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetMonoflop', 'set_monoflop'), 
'elements': [('relay', 'uint8', 1, 'in'),
             ('state', 'bool', 1, 'in'),
             ('time', 'uint32', 1, 'in')],
'doc': ['am', {
'en':
"""
The first parameter can be 1 or 2 (relay 1 or relay 2). The second parameter 
is the desired state of the relay (*true* means on and *false* means off).
The third parameter indicates the time (in ms) that the relay should hold 
the state.

If this function is called with the parameters (1, true, 1500):
Relay 1 will turn on and in 1.5s it will turn off again.

A monoflop can be used as a failsafe mechanism. For example: Lets assume you 
have a RS485 bus and a Dual Relay Bricklet connected to one of the slave 
stacks. You can now call this function every second, with a time parameter
of two seconds. The relay will be on all the time. If now the RS485 
connection is lost, the relay will turn off in at most two seconds.

.. versionadded:: 1.1.1
""",
'de':
"""
Der erste Parameter kann 1 oder 2 sein (Relais 1 oder Relais 2). Der zweite
Parameter ist der gewünschte Zustand des Relais (*true* bedeutet ein und *false* aus).
Der dritte Parameter stellt die Zeit (in ms) dar, welche das Relais den Zustand halten soll.

Wenn diese Funktion mit den Parametern (1, true, 1500) aufgerufen wird:
Relais 1 wird angeschalten und nach 1,5s wieder ausgeschalten.

Ein Monoflop kann als fehlersicherer Mechanismus verwendet werden. Beispiel:
Angenommen ein RS485 Bus und ein Dual Relay Bricklet ist an ein Slave Stapel verbunden.
Jetzt kann diese Funktion sekündlich, mit einem Zeitparameter von 2 Sekunden, aufgerufen werden.
Das Relais wird die gesamte Zeit ein sein. Wenn jetzt die RS485 Verbindung getrennt wird, 
wird das Relais nach spätestens zwei Sekunden ausschalten.

.. versionadded:: 1.1.1
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetMonoflop', 'get_monoflop'), 
'elements': [('relay', 'uint8', 1, 'in'),
             ('state', 'bool', 1, 'out'),
             ('time', 'uint32', 1, 'out'),
             ('time_remaining', 'uint32', 1, 'out')],
'doc': ['am', {
'en':
"""
Returns (for the given relay) the current state and the time as set by 
:func:`SetMonoflop` as well as the remaining time until the state flips.

If the timer is not running currently, the remaining time will be returned
as 0.

.. versionadded:: 1.1.1
""",
'de':
"""
Gibt (für das angegebene Relais) den aktuellen Zustand und die Zeit, wie von 
:func:`SetMonoflop gesetzt, sowie die noch verbleibende Zeit bis zum Zustandswechsel, zurück.

Wenn der Timer aktuell nicht läuft, ist die noch verbleibende Zeit 0.

.. versionadded:: 1.1.1
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('MonoflopDone', 'monoflop_done'), 
'elements': [('relay', 'uint8', 1, 'out'),
             ('state', 'bool', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered whenever a monoflop timer reaches 0. The 
parameter contain the relay (1 or 2) and the current state of the relay 
(the state after the monoflop).

.. versionadded:: 1.1.1
""",
'de':
"""
Dieser Callback wird ausgelöst wenn ein Monoflop Timer abläuft (0 erreicht).
Die Parameter enthalten das auslösende Relais (1 oder 2) und den aktuellen Zustand
des Relais (der Zustand nach dem Monoflop).

.. versionadded:: 1.1.1
"""
}]
})
