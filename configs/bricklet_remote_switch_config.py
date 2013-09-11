# -*- coding: utf-8 -*-

# Remote Switch Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 235,
    'name': ('RemoteSwitch', 'remote_switch', 'Remote Switch'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device that controls mains switches remotely',
    'released': False,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('SwitchSocket', 'switch_socket'), 
'elements': [('house_code', 'uint8', 1, 'in'),
             ('receiver_code', 'uint8', 1, 'in'),
             ('switch_to', 'uint8', 1, 'in', ('SwitchTo', 'switch_to', [('Off', 'off', 0),
                                                                        ('On', 'on', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
To switch a socket you have to give the house code, receiver code and the
state (on or off) you want to switch to.

A detailed description on how you can find the house and receiver code
can be found here. TODO: ADD LINK
""",
'de':
"""
Um eine Steckdose zu schalten muss der House Code, Receiver Code sowie
der Zustand (an oder aus) zu dem geschaltet werden soll übergeben werden.

Eine detaillierte Beschreibung wie man den House und Receiver Code
herausfinden kann gibt es hier. TODO: LINK HINZUFÜGEN
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetSwitchingState', 'get_switching_state'), 
'elements': [('state', 'uint8', 1, 'out', ('SwitchingState', 'switching_state', [('Ready', 'ready', 0),
                                                                                 ('Busy', 'busy', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current switching state. If the current state is busy, the
Bricklet is currently sending a code to switch a socket. It will not
accept any calls of :func:`SwitchSocket` until the state changes to ready.

How long the switching takes is dependent on the number of repeats, see
:func:`SetRepeats`.
""",
'de':
"""
Gibt den aktuellen Zustand des Schaltens zurück. Wenn der aktuell Zustand
busy (beschäftigt) ist, sendet das Bricklet gerade einen Code um eine Steckdose
zu schalten. Weitere Aufrufe von :func:`SwitchSocket` werden ignoriert bis
der Zustand auf ready (fertig) wechselt.

Die Länge des Schaltvorgangs ist abhängig von der Anzahl der Wiederholungen,
siehe :func:`SetRepeats`.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('SwitchingDone', 'switching_done'), 
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called whenever the switching state changes
from busy to ready, see :func:`GetSwitchingState`.
""",
'de':
"""
Dieser Callback wird aufgerufen wenn der Schaltzustand
von busy auf ready wechselt, siehe :func:`GetSwitchingState`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetRepeats', 'set_repeats'), 
'elements': [('repeats', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the number of times the code is send when :func:`SwitchSocket` is called.
The repeats basically correspond to the amount of time that a button of the
remote is pressed. 

Some dimmers are controlled by the length of a button pressed,
this can be simulated by increasing the repeats.

The default value is 5.
""",
'de':
"""
Setzt die Anzahl der Wiederholungen die verwendet werden um einen Code zu
senden wenn :func:`SwitchSocket` aufgerufen wird. Die Wiederholungen
korrespondieren zu der Zeit die eine Taste auf der Fernbedienung gedrückt wird.

Einige Dimmer werden über die Länge des Tastendrucks kontrolliert, dies kann
simuliert werden indem man die Anzahl der Wiederholungen inkrementiert.

Der Standardwert ist 5.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetRepeats', 'get_repeats'), 
'elements': [('repeats', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the number of repeats as set by :func:`SetRepeats`. 
""",
'de':
"""
Gibt die Anzahl der Wiederholungen zurück, wie von :func:`SetRepeats` gesetzt.
"""
}]
})
