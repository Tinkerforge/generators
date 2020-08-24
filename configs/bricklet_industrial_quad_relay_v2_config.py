# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Quad Relay Bricklet 2.0 communication config

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2102,
    'name': 'Industrial Quad Relay V2',
    'display_name': 'Industrial Quad Relay 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '4 galvanically isolated solid state relays',
        'de': '4 galvanisch getrennte Halbleiterrelais (Solid State Relais)'
    },
    'released': True,
    'documented': True,
    'discontinued': False,
    'features': [
        'device',
        'comcu_bricklet',
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append({
'name': 'Channel LED Config',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Show Heartbeat', 2),
              ('Show Channel Status', 3)]
})

com['packets'].append({
'type': 'function',
'name': 'Set Value',
'elements': [('Value', 'bool', 4, 'in', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the value of all four relays. A value of *true* closes the
relay and a value of *false* opens the relay.

Use :func:`Set Selected Value` to only change one relay.

All running monoflop timers will be aborted if this function is called.
""",
'de':
"""
Setzt den Wert der vier Relais. Ein Wert von *true* schließt das Relais
und ein Wert von *False* öffnet das Relais.

Nutze :func:`Set Selected Value` um einzelne Relais zu schalten.

Alle laufenden Monoflop Timer werden abgebrochen, wenn diese Funktion aufgerufen
wird.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Value',
'elements': [('Value', 'bool', 4, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the values as set by :func:`Set Value`.
""",
'de':
"""
Gibt die Werte zurück, wie von :func:`Set Value` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Monoflop',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 3)}),
             ('Value', 'bool', 1, 'in', {}),
             ('Time', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Configures a monoflop of the specified channel.

The second parameter is the desired value of the specified
channel. A *true* means relay closed and a *false* means relay open.

The third parameter indicates the time that the channels should hold
the value.

If this function is called with the parameters (0, 1, 1500) channel 0 will
close and in 1.5s channel 0 will open again

A monoflop can be used as a fail-safe mechanism. For example: Lets assume you
have a RS485 bus and a Industrial Quad Relay Bricklet 2.0 connected to one of
the slave stacks. You can now call this function every second, with a time
parameter of two seconds and channel 0 closed. Channel 0 will be closed all the
time. If now the RS485 connection is lost, then channel 0 will be opened in at
most two seconds.
""",
'de':
"""
Konfiguriert einen Monoflop für den angegebenen Kanal.

Der zweite Parameter ist eine der gewünschten Zustände des
festgelegten Kanals. Eine *true bedeutet Relais geschlossen und
ein *false* bedeutet Relais offen.

Der dritte Parameter ist die Zeit die der Kanal den Zustand
halten sollen.

Wenn diese Funktion mit den Parametern (0, 1, 1500) aufgerufen wird,
wird Kanal 0 geschlossen und nach 1,5s wieder geöffnet.

Ein Monoflop kann zur Ausfallsicherung verwendet werden. Beispiel:
Angenommen ein RS485 Bus und ein Industrial Quad Relay Bricklet 2.0 ist an ein
Slave Stapel verbunden.
Jetzt kann diese Funktion sekündlich, mit einem Zeitparameter von 2 Sekunden,
aufgerufen werden. Der Kanal wird die gesamte Zeit im Zustand geschlossen sein.
Wenn jetzt die RS485 Verbindung getrennt wird, wird der Kanal nach spätestens
zwei Sekunden in den Zustand geöffnet wechseln.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Monoflop',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 3)}),
             ('Value', 'bool', 1, 'out', {}),
             ('Time', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'}),
             ('Time Remaining', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'})],
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
Gibt (für den angegebenen Kanal) den aktuellen Zustand und die Zeit, wie von
:func:`Set Monoflop` gesetzt, sowie die noch verbleibende Zeit bis zum
Zustandswechsel, zurück.

Wenn der Timer aktuell nicht läuft, ist die noch verbleibende Zeit 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Selected Value',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 3)}),
             ('Value', 'bool', 1, 'in', {})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the output value of the specified channel without affecting the other
channels.

A running monoflop timer for the specified channel will be aborted if this
function is called.
""",
'de':
"""
Setzt den Ausgabewert des spezifizierten Kanals ohne die anderen Kanäle
zu beeinflussen.

Ein laufender Monoflop Timer für den spezifizierten Kanal wird abgebrochen, wenn
diese Funktion aufgerufen wird.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Channel LED Config',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 3)}),
             ('Config', 'uint8', 1, 'in', {'constant_group': 'Channel LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Each channel has a corresponding LED. You can turn the LED off, on or show a
heartbeat. You can also set the LED to "Channel Status". In this mode the
LED is on if the channel is high and off otherwise.
""",
'de':
"""
Jeder Kanal hat eine dazugehörige LED. Die LEDs können individuell an- oder
ausgeschaltet werden. Zusätzlich kann ein Heartbeat oder der Kanalstatus
angezeigt werden. Falls Kanalstatus gewählt wird ist die LED an wenn
ein High-Signal am Kanal anliegt und sonst aus.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Channel LED Config',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 3)}),
             ('Config', 'uint8', 1, 'out', {'constant_group': 'Channel LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the channel LED configuration as set by :func:`Set Channel LED Config`
""",
'de':
"""
Gibt die Kanal-LED-Konfiguration zurück, wie von :func:`Set Channel LED Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Monoflop Done',
'elements': [('Channel', 'uint8', 1, 'out', {'range': (0, 3)}),
             ('Value', 'bool', 1, 'out', {})],
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
Dieser Callback wird ausgelöst, wenn ein Monoflop Timer abläuft (0 erreicht).
:word:`parameters` enthalten den Kanal und den aktuellen Zustand des Kanals
(der Zustand nach dem Monoflop).
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('loop_header', 10, 'Turn relays alternating on/off 10 times with 100 ms delay'),
              ('sleep', 100, None, None),
              ('setter', 'Set Value', [('bool', [True, False, False, False])], None, None),
              ('sleep', 100, None, None),
              ('setter', 'Set Value', [('bool', [False, True, False, False])], None, None),
              ('sleep', 100, None, None),
              ('setter', 'Set Value', [('bool', [False, False, True, False])], None, None),
              ('sleep', 100, None, None),
              ('setter', 'Set Value', [('bool', [False, False, False, True])], None, None),
              ('loop_footer',)]
})


def relay_channel(channel):
    return {
        'id': 'Relay {}'.format(channel),
        'label': 'Relay {}'.format(channel),
        'description': 'Switches Relay {}. A running monoflop timer for this relay will be aborted if the relay is toggled by this channel.'.format(channel),

        'type': 'Relay',

        'getters': [{
            'packet': 'Get Value',
            'element': 'Value',
            'transform': 'value[{}] ? OnOffType.ON : OnOffType.OFF'.format(channel)}],

        'callbacks': [{
            'packet': 'Monoflop Done',
            'element': 'Value',
            'filter': 'channel == {}'.format(channel),
            'transform': 'value ? OnOffType.ON : OnOffType.OFF'}],

        'setters': [{
            'packet': 'Set Selected Value',
            'element': 'Value',
            'packet_params': [str(channel), 'cmd == OnOffType.ON'],
            'command_type': "OnOffType",
        }],


        'init_code': """this.setChannelLEDConfig({}, channelCfg.channelLEDConfig);""".format(channel)
    }

def monoflop_channel(channel):
    return {
        'id': 'Monoflop Relay {}'.format(channel),
        'label': 'Monoflop Relay {}'.format(channel),
        'type': 'Monoflop',

        'getters': [{
            'packet': 'Get Monoflop',
            'element': 'Value',
            'packet_params': [str(channel)],
            'transform': 'value.value ? OnOffType.ON : OnOffType.OFF'}],

        'setters': [{
            'packet': 'Set Monoflop',
            'packet_params': [str(channel), 'channelCfg.monoflopValue.booleanValue()', 'channelCfg.monoflopDuration'],
            'command_type': "StringType", # Command type has to be string type to be able to use command options.
        }],

        'setter_refreshs': [{
            'channel': 'Relay {}'.format(channel),
            'delay': '0'
        }]
    }

relay_channel_type = oh_generic_channel_type('Relay', 'Switch', 'NOT USED',
                                update_style=None,
                                description='NOT USED')
relay_channel_type['params'] = [
{
    'packet': 'Set Channel LED Config',
    'element': 'Config',

    'name': 'Channel LED Config',
    'type': 'integer',
    'label': 'Channel LED Config',
    'description': 'Each channel has a corresponding LED. You can turn the LED off, on or show a heartbeat. You can also set the LED to Channel Status. In this mode the LED is on if the channel is high and off otherwise.',
},
]


com['openhab'] = {
    'imports': oh_generic_trigger_channel_imports() + ['org.eclipse.smarthome.core.library.types.OnOffType', 'org.eclipse.smarthome.core.library.types.StringType'],
    'param_groups': oh_generic_channel_param_groups(),
    'channels': [relay_channel(i) for i in range(0, 4)] + [monoflop_channel(i) for i in range(0, 4)],
    'channel_types': [
        relay_channel_type,
        {
            'id': 'Monoflop',
            'item_type': 'String',
            'params': [{
                'packet': 'Set Monoflop',
                'element': 'Time',

                'name': 'Monoflop Duration',
                'type': 'integer',
                'default': 1000,
                'unit': 'ms',

                'label': 'Monoflop Duration',
                'description': 'The time (in ms) that the relay should hold the configured value.',
            },
            {
                'packet': 'Set Monoflop',
                'element': 'Value',

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
    'actions': [{'fn': 'Set Value', 'refreshs': ['Relay 0', 'Relay 1', 'Relay 2', 'Relay 3', 'Monoflop Relay 0', 'Monoflop Relay 1', 'Monoflop Relay 2', 'Monoflop Relay 3']},
                {'fn': 'Set Selected Value', 'refreshs': ['Relay 0', 'Relay 1', 'Relay 2', 'Relay 3', 'Monoflop Relay 0', 'Monoflop Relay 1', 'Monoflop Relay 2', 'Monoflop Relay 3']},
                {'fn': 'Set Monoflop', 'refreshs': ['Relay 0', 'Relay 1', 'Relay 2', 'Relay 3', 'Monoflop Relay 0', 'Monoflop Relay 1', 'Monoflop Relay 2', 'Monoflop Relay 3']},
                'Get Value', 'Get Channel LED Config', 'Get Monoflop']
}

