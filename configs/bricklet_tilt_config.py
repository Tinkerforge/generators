# -*- coding: utf-8 -*-

# Tilt Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 239,
    'name': ('Tilt', 'tilt', 'Tilt'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for sensing tilt and vibration',
    'released': False,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetTiltState', 'get_tilt_state'),
'elements': [('state', 'uint8', 1, 'out', ('TiltState', 'tilt_state', [('Closed', 'closed', 0),
                                                                       ('Open', 'open', 1),
                                                                       ('ClosedVibrating', 'closed_vibrating', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current tilt state. The state can either be

* Closed: The ball in the tilt switch closes the circuit.
* Open: The ball in the tilt switch does not close the circuit.
* Closed Vibrating: The tilt switch is in motion (rapid change between open and close).

""",
'de':
"""
Gibt den aktuellen Tilt-Zustand zurück. Der Zustand kann folgende Werte
annehmen:

* Closed: Der Ball im Neigungsschalter schließt den Stromkreis.
* Open: Der Ball im Neigungsschalter schließt den Stromkreis nicht.
* Closed Vibrating: Der Neigungsschalter ist in Bewegung (schnelle Änderungen zwischen open und close).

"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('EnableTiltStateCallback', 'enable_tilt_state_callback'),
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Enables the :func:`TiltState` callback.
""",
'de':
"""
Aktiviert den :func:`TiltState` Callback.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('DisableTiltStateCallback', 'disable_tilt_state_callback'),
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Disables the :func:`TiltState` callback.
""",
'de':
"""
Deaktiviert den :func:`TiltState` Callback.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('IsTiltStateCallbackEnabled', 'is_tilt_state_callback_enabled'),
'elements': [('enabled', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns *true* if the :func:`TiltState` callback is enabled.
""",
'de':
"""
Gibt *true* zurück wenn der :func:`TiltState` Callback aktiviert ist.
"""
}]
})


com['packets'].append({
'type': 'callback',
'name': ('TiltState', 'tilt_state'), 
'elements': [('state', 'uint8', 1, 'out', ('TiltState', 'tilt_state', [('Closed', 'closed', 0),
                                                                       ('Open', 'open', 1),
                                                                       ('ClosedVibrating', 'closed_vibrating', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback provides the current tilt state. It is called everytime the
state changes.

See :func:`GetTiltState` for a description of the states.
""",
'de':
"""
Dieser Callback übergibt den aktuellen Tilt-Status. Der Callback wird
aufgerufen wenn sich der Status ändert.

Siehe :func:`GetTiltState` für eine Beschreibung der Zustände.
"""
}]
})
