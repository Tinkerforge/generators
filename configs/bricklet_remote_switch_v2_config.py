# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Remote Switch Bricklet 2.0 communication config

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 289,
    'name': 'Remote Switch V2',
    'display_name': 'Remote Switch 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Controls remote mains switches and receives signals from remotes',
        'de': 'Steuert Funksteckdosen und empfängt Signale von Fernbedienungen'
    },
    'released': True,
    'documented': True,
    'discontinued': False,
    'features': [
        'comcu_bricklet',
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append({
'name': 'Switching State',
'type': 'uint8',
'constants': [('Ready', 0),
              ('Busy', 1)]
})

com['constant_groups'].append({
'name': 'Switch To',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1)]
})

com['constant_groups'].append({
'name': 'Remote Type',
'type': 'uint8',
'constants': [('A', 0),
              ('B', 1),
              ('C', 2)]
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
Sets the number of times the code is sent when one of the Switch Socket
functions is called. The repeats basically correspond to the amount of time
that a button of the remote is pressed.

Some dimmers are controlled by the length of a button pressed,
this can be simulated by increasing the repeats.
""",
'de':
"""
Setzt die Anzahl der Wiederholungen die verwendet werden um einen Code zu
senden wenn eine der Switch Socket Funktionen aufgerufen wird. Die
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
'since_firmware': [1, 0, 0],
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
'since_firmware': [1, 0, 0],
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
'since_firmware': [1, 0, 0],
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
'since_firmware': [1, 0, 0],
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

com['packets'].append({
'type': 'function',
'name': 'Set Remote Configuration',
'elements': [('Remote Type', 'uint8', 1, 'in', {'constant_group': 'Remote Type', 'default': 0}),
             ('Minimum Repeats', 'uint16', 1, 'in', {'default': 2}),
             ('Callback Enabled', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the configuration for **receiving** data from a remote of type A, B or C.

* Remote Type: A, B or C depending on the type of remote you want to receive.
* Minimum Repeats: The minimum number of repeated data packets until the callback
  is triggered (if enabled).
* Callback Enabled: Enable or disable callback (see :cb:`Remote Status A` callback,
  :cb:`Remote Status B` callback and :cb:`Remote Status C` callback).
""",
'de':
"""
Setzt die Konfiguration für das **Empfangen** von Daten von Fernbedienungen der
Typen A, B und C.

* Remote Type: A, B oder C abhängig vom Typ der Fernbedienung die empfangen
  werden soll.
* Minimum Repeats: Die Mindestanzahl an wiederholten Datenpaketen bevor der
  Callback ausgelöst wird (falls aktiviert).
* Callback Enabled: Aktiviert/Deaktivert den Callback (siehe :cb:`Remote Status A`
  Callback, :cb:`Remote Status B` Callback und :cb:`Remote Status C` Callback).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Remote Configuration',
'elements': [('Remote Type', 'uint8', 1, 'out', {'constant_group': 'Remote Type', 'default': 0}),
             ('Minimum Repeats', 'uint16', 1, 'out', {'default': 2}),
             ('Callback Enabled', 'bool', 1, 'out', {'default': False})],
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
'elements': [('House Code', 'uint8', 1, 'out', {'range': (0, 31)}),
             ('Receiver Code', 'uint8', 1, 'out', {'range': (0, 31)}),
             ('Switch To', 'uint8', 1, 'out', {'constant_group': 'Switch To'}),
             ('Repeats', 'uint16', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the house code, receiver code, switch state (on/off) and number of
repeats for remote type A.

Repeats == 0 means there was no button press. Repeats >= 1 means there
was a button press with the specified house/receiver code. The repeats are the
number of received identical data packets. The longer the button is pressed,
the higher the repeat number.

Use the callback to get this data automatically when a button is pressed,
see :func:`Set Remote Configuration` and :cb:`Remote Status A` callback.
""",
'de':
"""
Gibt den Housecode, Receivercode, Schaltzustand (an/aus) und Anzahl der
Wiederholungen für eine Typ A Fernbedienung zurück.

Repeats == 0 bedeutet, dass kein Knopf auf der Fernbedienung gedrückt wurde.
Repeats >= 1 bedeutet, dass ein Knopf mit dem angegebenen House/Receivercode
auf der Fernbedienung gedrückt wurde. Die repeats sind die Anzahl der
empfangenen identischen Datenpakete.

Es kann auch automatisch ein Callback ausgelöst werden, wenn Daten empfangen werden,
siehe :func:`Set Remote Configuration` und :cb:`Remote Status A` Callback.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Remote Status B',
'elements': [('Address', 'uint32', 1, 'out', {'range': (0, 2**26-1)}),
             ('Unit', 'uint8', 1, 'out', {'range': (0, 15)}),
             ('Switch To', 'uint8', 1, 'out', {'constant_group': 'Switch To'}),
             ('Dim Value', 'uint8', 1, 'out', {}),
             ('Repeats', 'uint16', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the address (unique per remote), unit (button number), switch state
(on/off) and number of repeats for remote type B.

If the remote supports dimming the dim value is used instead of the switch state.

If repeats=0 there was no button press. If repeats >= 1 there
was a button press with the specified address/unit. The repeats are the number of received
identical data packets. The longer the button is pressed, the higher the repeat number.

Use the callback to get this data automatically when a button is pressed,
see :func:`Set Remote Configuration` and :cb:`Remote Status B` callback.
""",
'de':
"""
Gibt die Address (eindeutig für jede Fernbedienung), Unit (Knopfnummer),
Schaltzustand (an/aus) und Anzahl der Wiederholungen für eine Typ B
Fernbedienung zurück.

Falls die Fernbedienung Dimmen unterstützt, dann wie der Dimmwert anstatt des
Schaltzustandes verwendet.

Repeats == 0 bedeutet, dass kein Knopf auf der Fernbedienung gedrückt wurde.
Repeats >= 1 bedeutet, dass ein Knopf mit der angegebenen Address/Unit auf der
Fernbedienung gedrückt wurde. Die repeats sind die Anzahl der empfangenen
identischen Datenpakete.

Es kann auch automatisch ein Callback ausgelöst werden, wenn Daten empfangen werden,
siehe :func:`Set Remote Configuration` und :cb:`Remote Status B` Callback.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Remote Status C',
'elements': [('System Code', 'char', 1, 'out', {'range': ('A', 'P')}),
             ('Device Code', 'uint8', 1, 'out', {'range': (1, 16)}),
             ('Switch To', 'uint8', 1, 'out', {'constant_group': 'Switch To'}),
             ('Repeats', 'uint16', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the system code, device code, switch state (on/off) and number of repeats for
remote type C.

If repeats=0 there was no button press. If repeats >= 1 there
was a button press with the specified system/device code. The repeats are the number of received
identical data packets. The longer the button is pressed, the higher the repeat number.

Use the callback to get this data automatically when a button is pressed,
see :func:`Set Remote Configuration` and :cb:`Remote Status C` callback.
""",
'de':
"""
Gibt die Systemcode, Gerätecode, Schaltzustand (an/aus) und Anzahl der
Wiederholungen für eine Typ C Fernbedienung zurück.

Repeats == 0 bedeutet, dass kein Knopf auf der Fernbedienung gedrückt wurde.
Repeats >= 1 bedeutet, dass ein Knopf mit der angegebenen System/Gerätecode auf der
Fernbedienung gedrückt wurde. Die repeats sind die Anzahl der empfangenen
identischen Datenpakete.

Es kann auch automatisch ein Callback ausgelöst werden, wenn Daten empfangen werden,
siehe :func:`Set Remote Configuration` und :cb:`Remote Status C` Callback.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Remote Status A',
'elements': [('House Code', 'uint8', 1, 'out', {'range': (0, 31)}),
             ('Receiver Code', 'uint8', 1, 'out', {'range': (0, 31)}),
             ('Switch To', 'uint8', 1, 'out', {'constant_group': 'Switch To'}),
             ('Repeats', 'uint16', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
Returns the house code, receiver code, switch state (on/off) and number of repeats for
remote type A.

The repeats are the number of received identical data packets. The longer the button is pressed,
the higher the repeat number. The callback is triggered with every repeat.

You have to enable the callback with :func:`Set Remote Configuration`. The number
of repeats that you can set in the configuration is the minimum number of repeats that have
to be seen before the callback is triggered for the first time.
""",
'de':
"""
Gibt den Housecode, Receivercode, Schaltzustand (an/aus) und Anzahl der
Wiederholungen für eine Typ A Fernbedienung zurück.

Die Wiederholungen ist die Anzahl empfangener identischer Datenpakete. Je länger
der Knopf auf der Fernbedienung gedrückt wird, desto höher die Anzahl der
Wiederholungen. Der Callback wird bei jeder Wiederholung ausgelöst.

Der Callback muss zuerst aktiviert werden mittels :func:`Set Remote Configuration`.
Die Mindestanzahl an Wiederholungen die konfiguriert werden kann ist die Anzahl
an Wiederholungen die empfangen worden sein muss bevor der Callback das erste
mal ausgelöst wird.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Remote Status B',
'elements': [('Address', 'uint32', 1, 'out', {'range': (0, 2**26-1)}),
             ('Unit', 'uint8', 1, 'out', {'range': [(0, 15), (255, 255)]}),
             ('Switch To', 'uint8', 1, 'out', {'constant_group': 'Switch To'}),
             ('Dim Value', 'uint8', 1, 'out', {}),
             ('Repeats', 'uint16', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
Returns the address (unique per remote), unit (button number), switch state (on/off) and number of repeats for
remote type B.

If the remote supports dimming the dim value is used instead of the switch state.

The repeats are the number of received identical data packets. The longer the button is pressed,
the higher the repeat number. The callback is triggered with every repeat.

You have to enable the callback with :func:`Set Remote Configuration`. The number
of repeats that you can set in the configuration is the minimum number of repeats that have
to be seen before the callback is triggered for the first time.
""",
'de':
"""
Gibt die Address (eindeutig für jede Fernbedienung), Unit (Knopfnummer),
Schaltzustand (an/aus) und Anzahl der Wiederholungen für eine Typ B
Fernbedienung zurück.

Die Wiederholungen ist die Anzahl empfangener identischer Datenpakete. Je länger
der Knopf auf der Fernbedienung gedrückt wird, desto höher die Anzahl der
Wiederholungen. Der Callback wird bei jeder Wiederholung ausgelöst.

Der Callback muss zuerst aktiviert werden mittels :func:`Set Remote Configuration`.
Die Mindestanzahl an Wiederholungen die konfiguriert werden kann ist die Anzahl
an Wiederholungen die empfangen worden sein muss bevor der Callback das erste
mal ausgelöst wird.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Remote Status C',
'elements': [('System Code', 'char', 1, 'out', {'range': ('A', 'P')}),
             ('Device Code', 'uint8', 1, 'out', {'range': (1, 16)}),
             ('Switch To', 'uint8', 1, 'out', {'constant_group': 'Switch To'}),
             ('Repeats', 'uint16', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
Returns the system code, device code, switch state (on/off) and number of repeats for
remote type C.

The repeats are the number of received identical data packets. The longer the button is pressed,
the higher the repeat number. The callback is triggered with every repeat.

You have to enable the callback with :func:`Set Remote Configuration`. The number
of repeats that you can set in the configuration is the minimum number of repeats that have
to be seen before the callback is triggered for the first time.
""",
'de':
"""
Gibt die Systemcode, Gerätecode, Schaltzustand (an/aus) und Anzahl der
Wiederholungen für eine Typ C Fernbedienung zurück.

Die Wiederholungen ist die Anzahl empfangener identischer Datenpakete. Je länger
der Knopf auf der Fernbedienung gedrückt wird, desto höher die Anzahl der
Wiederholungen. Der Callback wird bei jeder Wiederholung ausgelöst.

Der Callback muss zuerst aktiviert werden mittels :func:`Set Remote Configuration`.
Die Mindestanzahl an Wiederholungen die konfiguriert werden kann ist die Anzahl
an Wiederholungen die empfangen worden sein muss bevor der Callback das erste
mal ausgelöst wird.
"""
}]
})

com['examples'].append({
'name': 'Switch Socket',
'functions': [('setter', 'Switch Socket A', [('uint8', 17), ('uint8', 1), ('uint8:constant', 1)], 'Switch on a type A socket with house code 17 and receiver code 1.\nHouse code 17 is 10001 in binary (least-significant bit first)\nand means that the DIP switches 1 and 5 are on and 2-4 are off.\nReceiver code 1 is 10000 in binary (least-significant bit first)\nand means that the DIP switch A is on and B-E are off.', None)]
})

com['examples'].append({
'name': 'Remote Callback',
'functions': [('setter', 'Set Remote Configuration', [('uint8:constant', 0), ('uint8', 1), ('bool', True)], 'Configure to receive from remote type A with minimum repeats set to 1 and enable callback', None),
              ('callback', ('Remote Status A', 'remote status a'), [
                (('House Code', 'House Code'), 'uint8', 1, None, None, None),
                (('Receiver Code', 'Receiver Code'), 'uint8', 1, None, None, None),
                (('Switch To', 'Switch To'), 'uint8:constant', 1, None, None, None),
                (('Repeats', 'Repeats'), 'uint16', 1, None, None, None)
              ],
              None, None)]
})

com['openhab'] = {
    'is_bridge': True,
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.OnOffType',
                                               'org.eclipse.smarthome.core.library.types.DecimalType'],
    'param_groups': oh_generic_channel_param_groups(),
    'params': [{
        'packet': 'Set Remote Configuration',
        'element': 'Remote Type',

        'name': 'Remote Type',
        'type': 'integer',
        'options': [('A', 0),
                    ('B', 1),
                    ('C', 2)],
        'limitToOptions': 'true',
        'default': 0,

        'label': 'Remote Type',
        'description': 'Type A, B or C depending on the type of remote you want to receive.',
    }, {
        'packet': 'Set Remote Configuration',
        'element': 'Minimum Repeats',

        'name': 'Minimum Repeats',
        'type': 'integer',
        'default': 2,

        'label': 'Minimum Repeats',
        'description': 'The minimum number of repeated data packets until the Remote Status channels trigger.',
    }],
    'init_code': """this.setRemoteConfiguration(cfg.remoteType, cfg.minimumRepeats, true);""",
    'channels': [{
            'id': 'Switching Done',
            'label': 'Switching Done',
            'type': 'system.trigger',

            'callbacks': [{
                'packet': 'Switching Done',
                'transform': '""'}],

            'is_trigger_channel': True,
            'description': 'This channel is triggered whenever the switching state changes from busy to ready.'
        }, {
            'id': 'Remote Status A Available',
            'label': 'Remote Status A Available',
            'type': 'system.trigger',

            'callbacks': [{
                'packet': 'Remote Status A',
                'transform': '""'}],

            'is_trigger_channel': True,
            'description': 'This channel is triggered if at least the configured minimum of repeats of identical data packets for remote type A were received. You can get the house and receiver code, switch state and repeats with the getRemoteStatusA action.'
        }, {
            'id': 'Remote Status B Available',
            'label': 'Remote Status B Available',
            'type': 'system.trigger',

            'callbacks': [{
                'packet': 'Remote Status B',
                'transform': '""'}],

            'is_trigger_channel': True,
            'description': 'This channel is triggered if at least the configured minimum of repeats of identical data packets for remote type B were received. You can get the house and receiver code, switch state and repeats with the getRemoteStatusB action.'
        }, {
            'id': 'Remote Status C Available',
            'label': 'Remote Status C Available',
            'type': 'system.trigger',

            'callbacks': [{
                'packet': 'Remote Status C',
                'transform': '""'}],

            'is_trigger_channel': True,
            'description': 'This channel is triggered if at least the configured minimum of repeats of identical data packets for remote type C were received. You can get the house and receiver code, switch state and repeats with the getRemoteStatusC action.'
        }
    ],
    'actions': [
        'Get Switching State', 'Switch Socket A', 'Switch Socket B', 'Dim Socket B', 'Switch Socket C',
        'Get Remote Configuration', 'Get Remote Status A', 'Get Remote Status B', 'Get Remote Status C',
        'Set Repeats', 'Get Repeats'
    ]
}
