# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Solid State Relay Bricklet 2.0 communication config

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 296,
    'name': 'Solid State Relay V2',
    'display_name': 'Solid State Relay 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Controls AC and DC Solid State Relays',
        'de': 'Schaltet AC und DC Halbleiterrelais (Solid State Relais)'
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

com['packets'].append({
'type': 'function',
'name': 'Set State',
'elements': [('State', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the state of the relays *true* means on and *false* means off.

A running monoflop timer will be aborted if this function is called.
""",
'de':
"""
Setzt den Zustand des Relais, *true* bedeutet ein und *false* aus.

Ein laufender Monoflop Timer wird abgebrochen, wenn diese Funktion aufgerufen wird.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get State',
'elements': [('State', 'bool', 1, 'out', {'default': False})],
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
'elements': [('State', 'bool', 1, 'in', {}),
             ('Time', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
The first parameter  is the desired state of the relay (*true* means on
and *false* means off). The second parameter indicates the time that
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
dar, welche das Relais den Zustand halten soll.

Wenn diese Funktion mit den Parametern (true, 1500) aufgerufen wird:
Das Relais wird angeschaltet und nach 1,5s wieder ausgeschaltet.

Ein Monoflop kann als Ausfallsicherung verwendet werden. Beispiel:
Angenommen ein RS485 Bus und ein Solid State Relay Bricklet ist an ein Slave Stapel
verbunden. Jetzt kann diese Funktion sekündlich, mit einem Zeitparameter
von 2 Sekunden, aufgerufen werden.
Das Relais wird die gesamte Zeit eingeschaltet sein. Wenn jetzt die RS485 Verbindung
getrennt wird, wird das Relais nach spätestens zwei Sekunden ausschalten.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Monoflop',
'elements': [('State', 'bool', 1, 'out', {}),
             ('Time', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'}),
             ('Time Remaining', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [1, 0, 0],
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
'elements': [('State', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered whenever the monoflop timer reaches 0.
The parameter is the current state of the relay
(the state after the monoflop).
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn ein Monoflop Timer abläuft (0 erreicht).
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



com['openhab'] = {
    'imports': oh_generic_trigger_channel_imports() + ['org.eclipse.smarthome.core.library.types.OnOffType', 'org.eclipse.smarthome.core.library.types.StringType'],
    'param_groups': oh_generic_channel_param_groups(),
    'channels': [{
        'id': 'Relay',
        'label': 'Relay',
        'description': 'Switches the relay. A running monoflop timer for the relay will be aborted if the relay is toggled by this channel.',

        'type': 'Relay',

        'getters': [{
            'packet': 'Get State',
            'transform': 'value ? OnOffType.ON : OnOffType.OFF'}],

        'callbacks': [{
            'packet': 'Monoflop Done',
            'transform': 'state ? OnOffType.ON : OnOffType.OFF'}],

        'setters': [{
            'packet': 'Set State',
            'packet_params': ['cmd == OnOffType.ON']}],
        'setter_command_type': "OnOffType",
    }, {
        'id': 'Monoflop relay',
        'label': 'Monoflop Relay',
        'type': 'Monoflop',

        'getters': [{
            'packet': 'Get Monoflop',
            'transform': 'value.state ? OnOffType.ON : OnOffType.OFF'}],

        'setters': [{
            'packet': 'Set Monoflop',
            'packet_params': ['channelCfg.monoflopValue.booleanValue()', 'channelCfg.monoflopDuration']}],
        'setter_command_type': "StringType", # Command type has to be string type to be able to use command options.
        'setter_refreshs': [{
            'channel': 'Relay',
            'delay': '0'
        }]
    }],
    'channel_types': [
        oh_generic_channel_type('Relay', 'Switch', 'NOT USED',
                    update_style=None,
                    description='NOT USED'),
        {
            'id': 'Monoflop',
            'item_type': 'String',
            'params': [{
                'packet': 'Set Monoflop',
                'element': 'Time',

                'name': 'Monoflop Duration',
                'type': 'integer',
                'default': 1000,
                'min': 0,
                'max': 2**31 - 1,
                'unit': 'ms',

                'label': 'Monoflop Duration',
                'description': 'The time (in ms) that the relay should hold the configured value.',
            },
            {
                'packet': 'Set Monoflop',
                'element': 'State',

                'name': 'Monoflop Value',
                'type': 'boolean',
                'default': 'true',

                'label': 'Monoflop Value',
                'description': 'The desired value of the specified channel. Activated means relay closed and Deactivated means relay open.',
            }],
            'label': 'NOT USED',
            'description':'Triggers a monoflop as configured',
            'command_options': [('Trigger', 'TRIGGER')]
        }
    ],
    'actions': ['Get State', 'Get Monoflop']
}

