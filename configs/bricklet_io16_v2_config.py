# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# IO-16 Bricklet 2.0 communication config

from commonconstants import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2114,
    'name': 'IO16 V2',
    'display_name': 'IO-16 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '16-channel digital input/output',
        'de': '16 digitale Ein- und Ausgänge'
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
'name': 'Direction',
'type': 'char',
'constants': [('In', 'i'),
              ('Out', 'o')]
})

com['constant_groups'].append({
'name': 'Edge Type',
'type': 'uint8',
'constants': [('Rising', 0),
              ('Falling', 1),
              ('Both', 2)]
})

com['doc'] = {
'en':
"""
The Bricklet has sixteen channels that are named 0 to 15 in the API. The
corresponding connectors on the Bricklet are labeled A0 to A7 for channel 0 to 7
and B0 to B7 for channels 8 to 15.
""",
'de':
"""
Das Bricklet hat sechzehn Kanäle die in der API von 0 bis 15 benannt sind. Die
entsprechenden Anschlüsse auf dem Bricklet sind mit A0 bis A7 für die Kanäle 0
bis 7 und B0 bis B7 für die Kanäle 8 bis 15 benannt.
"""
}

com['packets'].append({
'type': 'function',
'name': 'Set Value',
'elements': [('Value', 'bool', 16, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the output value of all sixteen channels. A value of *true* or *false* outputs
logic 1 or logic 0 respectively on the corresponding channel.

Use :func:`Set Selected Value` to change only one output channel state.

For example: (True, True, False, False, ..., False) will turn the channels 0-1
high and the channels 2-15 low.

All running monoflop timers will be aborted if this function is called.

.. note::
 This function does nothing for channels that are configured as input. Pull-up
 resistors can be switched on with :func:`Set Configuration`.
""",
'de':
"""
Setzt den Zustand aller sechzehn Kanäle. Der Wert *true* bzw. *false* erzeugen
logisch 1 bzw. logisch 0 auf dem entsprechenden Kanal.

Mittels :func:`Set Selected Value` können auch einzelnen Kanäle gesetzt werden.

Beispiel: (True, True, False, False, ..., False) setzt die Kanäle 0-1 auf logisch 1 und die
Kanäle 2-15 auf logisch 0.

Alle laufenden Monoflop Timer werden abgebrochen, wenn diese Funktion
aufgerufen wird.

.. note::
 Diese Funktion bewirkt keine Änderung an Kanälen die als Eingang konfiguriert
 sind. Pull-Up Widerstände können mit :func:`Set Configuration` zugeschaltet
 werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Value',
'elements': [('Value', 'bool', 16, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the logic levels that are currently measured on the channels.
This function works if the channel is configured as input as well as if it is
configured as output.
""",
'de':
"""
Gibt die aktuell gemessenen Zustände zurück. Diese Funktion gibt die Zustände
aller Kanäle zurück, unabhängig ob diese als Ein- oder Ausgang konfiguriert
sind.
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

A running monoflop timer for the specific channel will be aborted if this
function is called.

.. note::
 This function does nothing for channels that are configured as input. Pull-up
 resistors can be switched on with :func:`Set Configuration`.
""",
'de':
"""
Setzt den Ausgabewert des ausgewählten Kanals ohne die anderen Kanäle zu
beeinflussen.

Ein laufender Monoflop Timer für den ausgewählten Kanal wird abgebrochen,
wenn diese Funktion aufgerufen wird.

.. note::
 Diese Funktion bewirkt keine Änderung an Kanälen die als Eingang konfiguriert
 sind. Pull-Up Widerstände können mit :func:`Set Configuration` zugeschaltet
 werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Direction', 'char', 1, 'in', {'constant_group': 'Direction'}),
             ('Value', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Configures the value and direction of a specific channel. Possible directions
are 'i' and 'o' for input and output.

If the direction is configured as output, the value is either high or low
(set as *true* or *false*).

If the direction is configured as input, the value is either pull-up or
default (set as *true* or *false*).

For example:

* (0, 'i', true) will set channel-0 as input pull-up.
* (1, 'i', false) will set channel-1 as input default (floating if nothing is connected).
* (2, 'o', true) will set channel-2 as output high.
* (3, 'o', false) will set channel-3 as output low.

A running monoflop timer for the specific channel will be aborted if this
function is called.

The default configuration is input with pull-up.
""",
'de':
"""
Konfiguriert den Zustand und die Richtung eines angegebenen Kanals. Mögliche
Richtungen sind 'i' und 'o' für Ein- und Ausgang.

Wenn die Richtung als Ausgang konfiguriert ist, ist der Zustand entweder
logisch 1 oder logisch 0 (gesetzt als *true* oder *false*).

Wenn die Richtung als Eingang konfiguriert ist, ist der Zustand entweder
Pull-Up oder Standard (gesetzt als *true* oder *false*).

Beispiele:

* (0, 'i', true) setzt Kanal-0 als Eingang mit Pull-Up.
* (1, 'i', false) setzt Kanal-1 als Standard Eingang (potentialfrei wenn nicht verbunden).
* (2, 'o', true) setzt Kanal-2 als Ausgang im Zustand logisch 1.
* (3, 'o', false) setzt Kanal-3 als Ausgang im Zustand logisch 0.

Ein laufender Monoflop Timer für den angegebenen Kanal wird abgebrochen,
wenn diese Funktion aufgerufen wird.

Die Standardkonfiguration ist Eingang mit Pull-Up.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Direction', 'char', 1, 'out', {'constant_group': 'Direction'}),
             ('Value', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the channel configuration as set by :func:`Set Configuration`.
""",
'de':
"""
Gibt die Kanal-Konfiguration zurück, wie von :func:`Set Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Input Value Callback Configuration',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
This callback can be configured per channel.

The period in ms is the period with which the :cb:`Input Value`
callback is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.

The default value is (0, false).
""",
'de':
"""
Dieser Callback kann pro Kanal konfiguriert werden.

Die Periode in ms ist die Periode mit der der :cb:`Input Value`
Callback ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn der Wert sich im Vergleich zum letzten mal geändert
hat. Ändert der Wert sich nicht innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen des Werts.

Der Standardwert ist (0, false).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Input Value Callback Configuration',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set Input Value Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set Input Value Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set All Input Value Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period in ms is the period with which the :cb:`All Input Value`
callback is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.

The default value is (0, false).
""",
'de':
"""
Die Periode in ms ist die Periode mit der der :cb:`All Input Value`
Callback ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn der Wert sich im Vergleich zum letzten mal geändert
hat. Ändert der Wert sich nicht innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen des Werts.

Der Standardwert ist (0, false).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get All Input Value Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set All Input Value Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set All Input Value Callback Configuration` gesetzt.
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
Configures a monoflop of the specified channel.

The second parameter is the desired value of the specified
channel. A *true* means relay closed and a *false* means relay open.

The third parameter indicates the time (in ms) that the channels should hold
the value.

If this function is called with the parameters (0, 1, 1500) channel 0 will
close and in 1.5s channel 0 will open again

A monoflop can be used as a fail-safe mechanism. For example: Lets assume you
have a RS485 bus and a IO-16 Bricklet 2.0 connected to one of
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

Der dritte Parameter ist die Zeit (in ms) die der Kanal den Zustand
halten sollen.

Wenn diese Funktion mit den Parametern (0, 1, 1500) aufgerufen wird,
wird Kanal 0 geschlossen und nach 1,5s wieder geöffnet.

Ein Monoflop kann zur Ausfallsicherung verwendet werden. Beispiel:
Angenommen ein RS485 Bus und ein IO-16 Bricklet 2.0 ist an ein
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
Gibt (für den angegebenen Kanal) den aktuellen Zustand und die Zeit, wie von
:func:`Set Monoflop` gesetzt, sowie die noch verbleibende Zeit bis zum
Zustandswechsel, zurück.

Wenn der Timer aktuell nicht läuft, ist die noch verbleibende Zeit 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Edge Count',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Reset Counter', 'bool', 1, 'in'),
             ('Count', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the current value of the edge counter for the selected channel. You can
configure the edges that are counted with :func:`Set Edge Count Configuration`.

If you set the reset counter to *true*, the count is set back to 0
directly after it is read.
""",
'de':
"""
Gibt den aktuellen Wert des Flankenzählers für den ausgewählten Kanal zurück. Die
zu zählenden Flanken können mit :func:`Set Edge Count Configuration` konfiguriert werden.

Wenn `reset counter` auf *true* gesetzt wird, wird der Zählerstand direkt
nach dem auslesen auf 0 zurückgesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Edge Count Configuration',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Edge Type', 'uint8', 1, 'in', {'constant_group': 'Edge Type'}),
             ('Debounce', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Configures the edge counter for a specific channel.

The edge type parameter configures if rising edges, falling edges or
both are counted if the channel is configured for input. Possible edge types are:

* 0 = rising (default)
* 1 = falling
* 2 = both

The debounce time is given in ms.

Configuring an edge counter resets its value to 0.

If you don't know what any of this means, just leave it at default. The
default configuration is very likely OK for you.

Default values: 0 (edge type) and 100ms (debounce time)
""",
'de':
"""
Konfiguriert den Flankenzähler für einen bestimmten Kanal.

Der edge type Parameter konfiguriert den zu zählenden Flankentyp. Es können
steigende, fallende oder beide Flanken gezählt werden für Kanäle die als Eingang
konfiguriert sind. Mögliche Flankentypen sind:

* 0 = steigend (Standard)
* 1 = fallend
* 2 = beide

Die Entprellzeit (debounce) wird in ms angegeben.

Durch das Konfigurieren wird der Wert des Flankenzählers auf 0 zurückgesetzt.

Falls unklar ist was dies alles bedeutet, kann diese Funktion einfach
ignoriert werden. Die Standardwerte sind in fast allen Situationen OK.

Standardwerte: 0 (edge type) und 100ms (debounce).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Edge Count Configuration',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Edge Type', 'uint8', 1, 'out', {'constant_group': 'Edge Type'}),
             ('Debounce', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the edge type and debounce time for the selected channel as set by
:func:`Set Edge Count Configuration`.
""",
'de':
"""
Gibt den Flankentyp sowie die Entprellzeit für den ausgewählten Kanals zurück,
wie von :func:`Set Edge Count Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Input Value',
'elements': [('Channel', 'uint8', 1, 'out'),
             ('Changed', 'bool', 1, 'out'),
             ('Value', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set Input Value Callback Configuration`.

The parameters are the channel, a value-changed indicator and the actual value
for the channel. The `changed` parameter is true if the value has changed since
the last callback.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set Input Value Callback Configuration` gesetzten Konfiguration

Die Parameter sind der Kanal, Changed und der Wert. Der `changed`-Parameter
ist True wenn sich der Wert seit dem letzten Callback geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'All Input Value',
'elements': [('Changed', 'bool', 16, 'out'),
             ('Value', 'bool', 16, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set All Input Value Callback Configuration`.

The :word:`parameters` are the same as :func:`Get Value`. Additional the
`changed` parameter is true if the value has changed since
the last callback.

""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set All Input Value Callback Configuration` gesetzten Konfiguration

Die :word:`parameters` sind der gleiche wie :func:`Get Value`. Zusätzlich ist der
`changed`-Parameter True wenn sich der Wert seit dem letzten Callback geändert hat.
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
Dieser Callback wird ausgelöst, wenn ein Monoflop Timer abläuft (0 erreicht).
:word:`parameters` enthalten den Kanal und den aktuellen Zustand des Kanals
(der Zustand nach dem Monoflop).
"""
}]
})

com['examples'].append({
'name': 'Output',
'functions': [('setter', 'Set Configuration', [('uint8', 7), ('char', 'o'), ('bool', False)], 'Configure channel 7 as output low', None),
              ('loop_header', 10, 'Set channel 7 alternating high/low 10 times with 100 ms delay'),
              ('sleep', 100, None, None),
              ('setter', 'Set Selected Value', [('uint8', 7), ('bool', True)], None, None),
              ('sleep', 100, None, None),
              ('setter', 'Set Selected Value', [('uint8', 7), ('bool', False)], None, None),
              ('loop_footer',)]
})

com['examples'].append({
'name': 'Interrupt',
'functions': [('callback', ('Input Value', 'input value'), [(('Channel', 'Channel'), 'uint8', 1, None, None, None), (('Changed', 'Changed'), 'bool', 1, None, None, None), (('Value', 'Value'), 'bool', 1, None, None, None)], None, None),
              ('callback_configuration', ('Input Value', 'input value (channel 4)'), [('uint8', 4)], 500, False, None, [])]
})


def input_channel(idx):
    return {
            'predicate': 'cfg.pinConfiguration{} > 1'.format(idx),
            'id': 'Input Pin {}'.format(idx),
            'label': 'Measured Level (Pin {}/{})'.format(idx, ('A' if idx <= 7 else 'B') + str(idx % 8)),

            'type': 'Input Pin',

            'getter_packet': 'Get Value',
            'getter_transform': 'value[{}] ? OnOffType.ON : OnOffType.OFF'.format(idx),

            'callback_filter': 'channel == {}'.format(idx),
            'callback_packet': 'Input Value',
            'callback_transform': 'value ? OnOffType.ON : OnOffType.OFF'.format(idx),

            # TODO: Don't hard code update interval. Support channel configuration (not merged into thing conf).
            'init_code':"""this.setInputValueCallbackConfiguration({0}, 1000, false);
            this.setConfiguration({0}, 'i', cfg.pinConfiguration{0} % 2 == 1);""".format(idx),
            'dispose_code': """this.setInputValueCallbackConfiguration({}, 0, false);""".format(idx),
    }

def output_channel(idx):
    return {
            'predicate': 'cfg.pinConfiguration{} <= 1'.format(idx),
            'id': 'Output Pin {}'.format(idx),
            'label': 'Set Level (Pin {}/{})'.format(idx, ('A' if idx <= 7 else 'B') + str(idx % 8)),

            'type': 'Output Pin',

            'getter_packet': 'Get Value',
            'getter_transform': 'value[{}] ? OnOffType.ON : OnOffType.OFF'.format(idx),

            'setter_packet': 'Set Selected Value',
            'setter_packet_params': [str(idx), 'cmd == OnOffType.ON'],
            'setter_command_type': "OnOffType",

            'callback_packet': 'Monoflop Done',
            'callback_filter': 'channel == {}'.format(idx),
            'callback_transform': 'value ? OnOffType.ON : OnOffType.OFF',


            'init_code':"""this.setConfiguration({0}, 'o', cfg.pinConfiguration{0} % 2 == 1);""".format(idx),
    }

def monoflop_channel(channel):
    return {
        'predicate': 'cfg.pinConfiguration{} <= 1'.format(channel),
        'id': 'Monoflop Pin {}'.format(channel),
        'label': 'Monoflop Pin {}'.format(channel),
        'type': 'Monoflop',

        'getter_packet': 'Get Monoflop',
        'getter_packet_params': [str(channel)],
        'getter_transform': 'value.value ? OnOffType.ON : OnOffType.OFF',

        'setter_packet': 'Set Monoflop',
        #TODO: cfg needs monoflop channel number
        'setter_packet_params': [str(channel), 'channelCfg.monoflopValue.booleanValue()', 'channelCfg.monoflopDuration'],
        'setter_command_type': "StringType", # Command type has to be string type to be able to use command options.
        'setter_refreshs': [{
            'channel': 'Output Pin {}'.format(channel),
            'delay': '0'
        }]
    }

def pin_config(idx):
    return {
            'name': 'Pin Configuration {}'.format(idx),
            'type': 'integer',
            'options': [
                ('Input with pull-up', 3),
                ('Input without pull-up', 2),
                ('Output (Initial high)', 1),
                ('Output (Initial low)', 0)
            ],
            'limitToOptions': 'true',
            'default': '3',

            'label': 'Pin Configuration {}/{}'.format(idx, ('A' if idx <= 7 else 'B') + str(idx % 8)),
            'description': 'Configures the direction of pin {}/{}. Inputs without pull-up will be floating if nothing is connected. Outputs can have an initial state of low or high.'.format(idx, ('A' if idx <= 7 else 'B') + str(idx % 8)),
        }

channels = [input_channel(i) for i in range(0, 16)] + [output_channel(i) for i in range(0, 16)] + [monoflop_channel(i) for i in range(0, 16)]
params = [pin_config(i) for i in range(0, 16)]

com['openhab'] = {
    'imports': ['org.eclipse.smarthome.core.library.types.OnOffType', 'org.eclipse.smarthome.core.library.types.StringType'],
    'params': params,
    'channels': channels,
    'channel_types': [
        oh_generic_channel_type('Input Pin', 'Switch', 'Measured Level',
                     description='The logic level that is currently measured on the pin.',
                     read_only=True),
        oh_generic_channel_type('Output Pin', 'Switch', 'Set Level',
                     description='The logic level that is currently set on the pin.',
                     read_only=False),
        {
            'id': 'Monoflop',
            'item_type': 'String',
            'params': [{
                'name': 'Monoflop Duration',
                'type': 'integer',
                'default': 1000,
                'min': 0,
                'max': 2**31 - 1,
                'unit': 'ms',

                'label': 'Monoflop duration',
                'description': 'The time (in ms) that the pin should hold the configured value.',
            },
            {
                'name': 'Monoflop Value',
                'type': 'boolean',
                'default': 'true',

                'label': 'Monoflop value',
                'description': 'The desired value of the specified channel. Activated means relay closed and Deactivated means relay open.',
            }],
            'label': 'NOT USED',
            'description':'Triggers a monoflop as configured',
            'command_options': [('Trigger', 'TRIGGER')]
        }
    ]
}
