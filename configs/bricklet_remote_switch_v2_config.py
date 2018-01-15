# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Remote Switch Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 289,
    'name': 'Remote Switch V2',
    'display_name': 'Remote Switch 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Controls remote mains switches',
        'de': 'Steuert Funksteckdosen'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Get Switching State',
'elements': [('State', 'uint8', 1, 'out', ('Switching State', [('Ready', 0),
                                                               ('Busy', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current switching state. If the current state is busy, the
Bricklet is currently sending a code to switch a socket. It will not
accept any calls of switch socket functions until the state changes to ready.

How long the switching takes is dependent on the number of repeats, see
:func:`Set Repeats`.
""",
'de':
"""
Gibt den aktuellen Zustand des Schaltens zurück. Wenn der aktuell Zustand
busy (beschäftigt) ist, sendet das Bricklet gerade einen Code um eine Steckdose
zu schalten. Weitere Aufrufe der Switch Socket Funktionen werden ignoriert bis
der Zustand auf ready (fertig) wechselt.

Die Länge des Schaltvorgangs ist abhängig von der Anzahl der Wiederholungen,
siehe :func:`Set Repeats`.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Switching Done',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called whenever the switching state changes
from busy to ready, see :func:`Get Switching State`.
""",
'de':
"""
Dieser Callback wird aufgerufen wenn der Schaltzustand
von busy auf ready wechselt, siehe :func:`Get Switching State`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Repeats',
'elements': [('Repeats', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the number of times the code is send when one of the Switch Socket
functions is called. The repeats basically correspond to the amount of time
that a button of the remote is pressed.

Some dimmers are controlled by the length of a button pressed,
this can be simulated by increasing the repeats.

The default value is 5.
""",
'de':
"""
Setzt die Anzahl der Wiederholungen die verwendet werden um einen Code zu
senden wenn eine der Switch Socket Funktionen aufgerufen wird. Die
Wiederholungen korrespondieren zu der Zeit die eine Taste auf der Fernbedienung
gedrückt wird.

Einige Dimmer werden über die Länge des Tastendrucks kontrolliert, dies kann
simuliert werden indem man die Anzahl der Wiederholungen inkrementiert.

Der Standardwert ist 5.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Repeats',
'elements': [('Repeats', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the number of repeats as set by :func:`Set Repeats`.
""",
'de':
"""
Gibt die Anzahl der Wiederholungen zurück, wie von :func:`Set Repeats` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Switch Socket A',
'elements': [('House Code', 'uint8', 1, 'in'),
             ('Receiver Code', 'uint8', 1, 'in'),
             ('Switch To', 'uint8', 1, 'in', ('Switch To', [('Off', 0),
                                                            ('On', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
To switch a type A socket you have to give the house code, receiver code and the
state (on or off) you want to switch to.

The house code and receiver code have a range of 0 to 31 (5bit).

A detailed description on how you can figure out the house and receiver code
can be found :ref:`here <remote_switch_bricklet_type_a_house_and_receiver_code>`.
""",
'de':
"""
Um eine Typ A Steckdose zu schalten muss der Housecode, Receivercode sowie
der Zustand (an oder aus) zu dem geschaltet werden soll übergeben werden.

Der House- und Receivercode hat einen Wertebereich von 0 bis 31 (5Bit).

Eine detaillierte Beschreibung wie man den House- und Receivercode herausfinden
kann gibt es :ref:`hier <remote_switch_bricklet_type_a_house_and_receiver_code>`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Switch Socket B',
'elements': [('Address', 'uint32', 1, 'in'),
             ('Unit', 'uint8', 1, 'in'),
             ('Switch To', 'uint8', 1, 'in', ('Switch To', [('Off', 0),
                                                            ('On', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
To switch a type B socket you have to give the address, unit and the state
(on or off) you want to switch to.

The address has a range of 0 to 67108863 (26bit) and the unit has a range
of 0 to 15 (4bit). To switch all devices with the same address use 255 for
the unit.

A detailed description on how you can teach a socket the address and unit can
be found :ref:`here <remote_switch_bricklet_type_b_address_and_unit>`.
""",
'de':
"""
Um eine Typ B Steckdose zu schalten muss die Adresse und Unit sowie
der Zustand (an oder aus) zu dem geschaltet werden soll übergeben werden.

Die Adresse hat einen Wertebereich von 0 bis 67108863 (26Bit) und die Unit hat
einen Wertebereich von 0 bis 15 (4Bit). Um alle Geräte mit der selben Adresse
zu schalten kann die Unit auf 255 gesetzt werden.

Eine detaillierte Beschreibung wie man Adresse und Unit einer Steckdose anlernen
kann gibt es :ref:`hier <remote_switch_bricklet_type_b_address_and_unit>`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Dim Socket B',
'elements': [('Address', 'uint32', 1, 'in'),
             ('Unit', 'uint8', 1, 'in'),
             ('Dim Value', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
To control a type B dimmer you have to give the address, unit and the
dim value you want to set the dimmer to.

The address has a range of 0 to 67108863 (26bit), the unit and the dim value
has a range of 0 to 15 (4bit).

A detailed description on how you can teach a dimmer the address and unit can
be found :ref:`here <remote_switch_bricklet_type_b_address_and_unit>`.
""",
'de':
"""
Um eine Typ B Dimmer zu steuern muss die Adresse und Unit sowie
der Dimmwert auf der Dimmer gesetzt werden soll übergeben werden.

Die Adresse hat einen Wertebereich von 0 bis 67108863 (26Bit), die Unit und
der Dimmwert haben einen Wertebereich von 0 bis 15 (4Bit).

Eine detaillierte Beschreibung wie man Adresse und Unit einem Dimmer anlernen
kann gibt es :ref:`hier <remote_switch_bricklet_type_b_address_and_unit>`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Switch Socket C',
'elements': [('System Code', 'char', 1, 'in'),
             ('Device Code', 'uint8', 1, 'in'),
             ('Switch To', 'uint8', 1, 'in', ('Switch To', [('Off', 0),
                                                            ('On', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
To switch a type C socket you have to give the system code, device code and the
state (on or off) you want to switch to.

The system code has a range of 'A' to 'P' (4bit) and the device code has a
range of 1 to 16 (4bit).

A detailed description on how you can figure out the system and device code
can be found :ref:`here <remote_switch_bricklet_type_c_system_and_device_code>`.
""",
'de':
"""
Um eine Typ A Steckdose zu schalten muss der Systemcode, Gerätecode sowie
der Zustand (an oder aus) zu dem geschaltet werden soll übergeben werden.

Der Systemcode hat einen Wertebereich von 'A' bis 'P' (4Bit) und der Gerätecode
hat einen Wertebereich von 1 bis 16 (4Bit).

Eine detaillierte Beschreibung wie man den System- und Gerätecode herausfinden
kann gibt es :ref:`hier <remote_switch_bricklet_type_c_system_and_device_code>`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Remote Configuration',
'elements': [('Remote Type', 'uint8', 1, 'in', ('Remote Type', [('A', 0),
                                                                ('B', 1),
                                                                ('C', 2)])),
             ('Minimum Repeats', 'uint16', 1, 'in'),
             ('Callback Enabled', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the configuration for **receiving** data from a remote of type A, B or C.

* Remote Type: Set to A, B or C depending on the type of remote you want to receive.
* Minimum Repeats: The minimum number of repeated data packets until the callback is called (if enabled).
* Callback Enabled: Enable or disable callback (see :cb:`Remote Status A`, :cb:`Remote Status B`, :cb:`Remote Status C`).

Default is 'A', 2, false.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Remote Configuration',
'elements': [('Remote Type', 'uint8', 1, 'out', ('Remote Type', [('A', 0),
                                                                 ('B', 1),
                                                                 ('C', 2)])),
             ('Minimum Repeats', 'uint16', 1, 'out'),
             ('Callback Enabled', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the remote configuration as set by :func:`Set Remote Configuration`
""",
'de':
"""
Gibt die Konfiguration zurück wie von :func:`Set Remote Configuration` gesetzt.
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Get Remote Status A',
'elements': [('House Code', 'uint8', 1, 'out'),
             ('Receiver Code', 'uint8', 1, 'out'),
             ('Switch To', 'uint8', 1, 'out', ('Switch To', [('Off', 0),
                                                             ('On', 1)])),
             ('Repeats', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the house code, receiver code, switch state (on/off) and number of repeats for
remote type A.

If repeats=0 there was no button press. If repeats >= 1 there
was a button press with the specified house/receiver code. The repeates are the number of received
identical data packets. The longer the button is pressed, the higher the repeat number.

Use the callback to get this data automatically when a button is pressed, 
see :func:`Set Remote Configuration` and :cb:`Remote Status A`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Remote Status B',
'elements': [('Address', 'uint32', 1, 'out'),
             ('Unit', 'uint8', 1, 'out'),
             ('Switch To', 'uint8', 1, 'out', ('Switch To', [('Off', 0),
                                                             ('On', 1)])),
             ('Dim Value', 'uint8', 1, 'out'),
             ('Repeats', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the address (unique per remote), unit (button number), switch state (on/off) and number of repeats for
remote type B. 

If the remote supporst dimming the dim value is used instead of the switch state.

If repeats=0 there was no button press. If repeats >= 1 there
was a button press with the specified address/unit. The repeates are the number of received
identical data packets. The longer the button is pressed, the higher the repeat number.

Use the callback to get this data automatically when a button is pressed, 
see :func:`Set Remote Configuration` and :cb:`Remote Status B`.
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Get Remote Status C',
'elements': [('System Code', 'char', 1, 'out'),
             ('Device Code', 'uint8', 1, 'out'),
             ('Switch To', 'uint8', 1, 'out', ('Switch To', [('Off', 0),
                                                             ('On', 1)])),
             ('Repeats', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the system code, device code, switch state (on/off) and number of repeats for
remote type C.

If repeats=0 there was no button press. If repeats >= 1 there
was a button press with the specified system/device code. The repeates are the number of received
identical data packets. The longer the button is pressed, the higher the repeat number.

Use the callback to get this data automatically when a button is pressed, 
see :func:`Set Remote Configuration` and :cb:`Remote Status C`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Remote Status A',
'elements': [('House Code', 'uint8', 1, 'out'),
             ('Receiver Code', 'uint8', 1, 'out'),
             ('Switch To', 'uint8', 1, 'out', ('Switch To', [('Off', 0),
                                                             ('On', 1)])),
             ('Repeats', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
Returns the house code, receiver code, switch state (on/off) and number of repeats for
remote type A.

The repeates are the number of received identical data packets. The longer the button is pressed, 
the higher the repeat number. The callback is called with every repeat.

You have to enable the callback with :func:`Set Remote Configuration`. The number
of repeats that you can set in the configuration is the minimum number of repeats that have
to be seen before the callback is triggered.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Remote Status B',
'elements': [('Address', 'uint32', 1, 'out'),
             ('Unit', 'uint8', 1, 'out'),
             ('Switch To', 'uint8', 1, 'out', ('Switch To', [('Off', 0),
                                                             ('On', 1)])),
             ('Dim Value', 'uint8', 1, 'out'),
             ('Repeats', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
Returns the address (unique per remote), unit (button number), switch state (on/off) and number of repeats for
remote type B. 

If the remote supporst dimming the dim value is used instead of the switch state.

The repeates are the number of received identical data packets. The longer the button is pressed, 
the higher the repeat number. The callback is called with every repeat.

You have to enable the callback with :func:`Set Remote Configuration`. The number
of repeats that you can set in the configuration is the minimum number of repeats that have
to be seen before the callback is triggered.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Remote Status C',
'elements': [('System Code', 'char', 1, 'out'),
             ('Device Code', 'uint8', 1, 'out'),
             ('Switch To', 'uint8', 1, 'out', ('Switch To', [('Off', 0),
                                                             ('On', 1)])),
             ('Repeats', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
Returns the system code, device code, switch state (on/off) and number of repeats for
remote type C.

The repeates are the number of received identical data packets. The longer the button is pressed,
the higher the repeat number. The callback is called with every repeat.

You have to enable the callback with :func:`Set Remote Configuration`. The number
of repeats that you can set in the configuration is the minimum number of repeats that have
to be seen before the callback is triggered.
""",
'de':
"""
"""
}]
})

com['examples'].append({
'name': 'Switch Socket',
'functions': [('setter', 'Switch Socket A', [('uint8', 17), ('uint8', 1), ('uint8:constant', 1)], 'Switch on a type A socket with house code 17 and receiver code 1.\nHouse code 17 is 10001 in binary (least-significant bit first)\nand means that the DIP switches 1 and 5 are on and 2-4 are off.\nReceiver code 1 is 10000 in binary (least-significant bit first)\nand means that the DIP switch A is on and B-E are off.', None)]
})

com['examples'].append({
'name': 'Callback',
'functions': [('setter', 'Set Remote Configuration', [('uint8:constant', 0), ('uint8', 1), ('bool', 1)], 'Configure to receive from remote type A with minimum repeats set to 1 and enable callback', None),
              ('callback', ('Remote Status A', 'remote status a'), [
                (('House Code', 'House Code'), 'uint8', 1, None, None, None, None),
                (('Receiver Code', 'Receiver Code'), 'uint8', 1, None, None, None, None),
                (('Switch To', 'Switch To'), 'uint8', 1, None, None, None, None),
                (('Repeats', 'Repeats'), 'uint16', 1, None, None, None, None)
              ],
              None, None)]
})
