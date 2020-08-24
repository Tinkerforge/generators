# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Remote Switch Bricklet communication config

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'category': 'Bricklet',
    'device_identifier': 235,
    'name': 'Remote Switch',
    'display_name': 'Remote Switch',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Controls remote mains switches',
        'de': 'Steuert Funksteckdosen'
    },
    'released': True,
    'documented': True,
    'discontinued': True, # replaced by Remote Switch Bricklet 2.0
    'features': [
        'device',
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append({
'name': 'Switch To',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1)]
})

com['constant_groups'].append({
'name': 'Switching State',
'type': 'uint8',
'constants': [('Ready', 0),
              ('Busy', 1)]
})

com['packets'].append({
'type': 'function',
'name': 'Switch Socket',
'elements': [('House Code', 'uint8', 1, 'in', {'range': (0, 31)}),
             ('Receiver Code', 'uint8', 1, 'in', {'range': (0, 31)}),
             ('Switch To', 'uint8', 1, 'in', {'constant_group': 'Switch To'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
This function is deprecated, use :func:`Switch Socket A` instead.
""",
'de':
"""
Diese Funktion ist veraltet und wurde durch :func:`Switch Socket A` ersetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Switching State',
'elements': [('State', 'uint8', 1, 'out', {'constant_group': 'Switching State'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current switching state. If the current state is busy, the
Bricklet is currently sending a code to switch a socket. It will not
accept any requests to switch sockets until the state changes to ready.

How long the switching takes is dependent on the number of repeats, see
:func:`Set Repeats`.
""",
'de':
"""
Gibt den aktuellen Zustand des Schaltens zurück. Wenn der aktuell Zustand
busy (beschäftigt) ist, sendet das Bricklet gerade einen Code um eine Steckdose
zu schalten. Weitere Schaltanforderungen werden ignoriert bis
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
This callback is triggered whenever the switching state changes
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
'elements': [('Repeats', 'uint8', 1, 'in', {'default': 5})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the number of times the code is sent when one of the switch socket
functions is called. The repeats basically correspond to the amount of time
that a button of the remote is pressed.

Some dimmers are controlled by the length of a button pressed,
this can be simulated by increasing the repeats.
""",
'de':
"""
Setzt die Anzahl der Wiederholungen die verwendet werden um einen Code zu
senden wenn eine der Schalt-Funktionen aufgerufen wird. Die
Wiederholungen korrespondieren zu der Zeit die eine Taste auf der Fernbedienung
gedrückt wird.

Einige Dimmer werden über die Länge des Tastendrucks kontrolliert, dies kann
simuliert werden indem man die Anzahl der Wiederholungen inkrementiert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Repeats',
'elements': [('Repeats', 'uint8', 1, 'out', {'default': 5})],
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
'elements': [('House Code', 'uint8', 1, 'in', {'range': (0, 31)}),
             ('Receiver Code', 'uint8', 1, 'in', {'range': (0, 31)}),
             ('Switch To', 'uint8', 1, 'in', {'constant_group': 'Switch To'})],
'since_firmware': [2, 0, 1],
'doc': ['bf', {
'en':
"""
To switch a type A socket you have to give the house code, receiver code and the
state (on or off) you want to switch to.

A detailed description on how you can figure out the house and receiver code
can be found :ref:`here <remote_switch_bricklet_type_a_house_and_receiver_code>`.
""",
'de':
"""
Um eine Typ A Steckdose zu schalten muss der Housecode, Receivercode sowie
der Zustand (an oder aus) zu dem geschaltet werden soll übergeben werden.

Eine detaillierte Beschreibung wie man den House- und Receivercode herausfinden
kann gibt es :ref:`hier <remote_switch_bricklet_type_a_house_and_receiver_code>`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Switch Socket B',
'elements': [('Address', 'uint32', 1, 'in', {'range': (0, 2**26-1)}),
             ('Unit', 'uint8', 1, 'in', {'range': [(0, 15), (255, 255)]}),
             ('Switch To', 'uint8', 1, 'in', {'constant_group': 'Switch To'})],
'since_firmware': [2, 0, 1],
'doc': ['bf', {
'en':
"""
To switch a type B socket you have to give the address, unit and the state
(on or off) you want to switch to.

To switch all devices with the same address use 255 for the unit.

A detailed description on how you can teach a socket the address and unit can
be found :ref:`here <remote_switch_bricklet_type_b_address_and_unit>`.
""",
'de':
"""
Um eine Typ B Steckdose zu schalten muss die Adresse und Unit sowie
der Zustand (an oder aus) zu dem geschaltet werden soll übergeben werden.

Um alle Geräte mit der selben Adresse zu schalten kann die Unit auf 255 gesetzt werden.

Eine detaillierte Beschreibung wie man Adresse und Unit einer Steckdose anlernen
kann gibt es :ref:`hier <remote_switch_bricklet_type_b_address_and_unit>`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Dim Socket B',
'elements': [('Address', 'uint32', 1, 'in', {'range': (0, 2**26-1)}),
             ('Unit', 'uint8', 1, 'in', {'range': [(0, 15), (255, 255)]}),
             ('Dim Value', 'uint8', 1, 'in', {})],
'since_firmware': [2, 0, 1],
'doc': ['bf', {
'en':
"""
To control a type B dimmer you have to give the address, unit and the
dim value you want to set the dimmer to.

A detailed description on how you can teach a dimmer the address and unit can
be found :ref:`here <remote_switch_bricklet_type_b_address_and_unit>`.
""",
'de':
"""
Um eine Typ B Dimmer zu steuern muss die Adresse und Unit sowie
der Dimmwert auf der Dimmer gesetzt werden soll übergeben werden.

Eine detaillierte Beschreibung wie man Adresse und Unit einem Dimmer anlernen
kann gibt es :ref:`hier <remote_switch_bricklet_type_b_address_and_unit>`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Switch Socket C',
'elements': [('System Code', 'char', 1, 'in', {'range': ('A', 'P')}),
             ('Device Code', 'uint8', 1, 'in', {'range': (1, 16)}),
             ('Switch To', 'uint8', 1, 'in', {'constant_group': 'Switch To'})],
'since_firmware': [2, 0, 1],
'doc': ['bf', {
'en':
"""
To switch a type C socket you have to give the system code, device code and the
state (on or off) you want to switch to.

A detailed description on how you can figure out the system and device code
can be found :ref:`here <remote_switch_bricklet_type_c_system_and_device_code>`.
""",
'de':
"""
Um eine Typ C Steckdose zu schalten muss der Systemcode, Gerätecode sowie
der Zustand (an oder aus) zu dem geschaltet werden soll übergeben werden.

Eine detaillierte Beschreibung wie man den System- und Gerätecode herausfinden
kann gibt es :ref:`hier <remote_switch_bricklet_type_c_system_and_device_code>`.
"""
}]
})

com['examples'].append({
'name': 'Switch Socket',
'functions': [('setter', 'Switch Socket A', [('uint8', 17), ('uint8', 1), ('uint8:constant', 1)], 'Switch on a type A socket with house code 17 and receiver code 1.\nHouse code 17 is 10001 in binary (least-significant bit first)\nand means that the DIP switches 1 and 5 are on and 2-4 are off.\nReceiver code 1 is 10000 in binary (least-significant bit first)\nand means that the DIP switch A is on and B-E are off.', None)]
})

com['openhab'] = {
    'doc': {'de': 'TODO',
    'en':
"""
Usage
^^^^^

The remote switch Bricklet functions as bridge for remote controlled mains switches and dimmers.
Switches/dimmers must be added as things to openHAB manually with the Paper UI. The switch/dimmer thing
can then be configured depending on the addressing type. (See hardware documentation)
"""},
    'is_bridge': True,
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.OnOffType'],
    'param_groups': oh_generic_channel_param_groups(),
    'channels': [{
            'id': 'Switching Done',
            'label': 'Switching Done',
            'type': 'system.trigger',

            'callbacks': [{
                'packet': 'Switching Done',
                'transform': '""'}],
            'description': 'This channel is triggered whenever the switching state changes from busy to ready.'
        }
    ],
    'actions': [
        'Get Switching State', 'Switch Socket A', 'Switch Socket B', 'Dim Socket B', 'Switch Socket C',
        'Set Repeats', 'Get Repeats'
    ]
}
