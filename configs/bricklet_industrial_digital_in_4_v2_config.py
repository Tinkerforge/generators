# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Digital In 4 Bricklet 2.0 communication config

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2100,
    'name': 'Industrial Digital In 4 V2',
    'display_name': 'Industrial Digital In 4 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '4 galvanically isolated digital inputs',
        'de': '4 galvanisch getrennte digitale Eingänge'
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
'name': 'Channel',
'type': 'uint8',
'constants': [('0', 0),
              ('1', 1),
              ('2', 2),
              ('3', 3)]
})

com['constant_groups'].append({
'name': 'Edge Type',
'type': 'uint8',
'constants': [('Rising', 0),
              ('Falling', 1),
              ('Both', 2)]
})

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
'name': 'Get Value',
'elements': [('Value', 'bool', 4, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the input value as bools, *true* refers to high and *false* refers to low.
""",
'de':
"""
Gibt die Eingangswerte als Bools zurück, *true* bedeutet logisch 1 und *false* logisch 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Value Callback Configuration',
'elements': [('Channel', 'uint8', 1, 'in', {'constant_group': 'Channel'}),
             ('Period', 'uint32', 1, 'in', {'factor': 1000, 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
This callback can be configured per channel.

The period is the period with which the :cb:`Value`
callback is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.
""",
'de':
"""
Dieser Callback kann pro Kanal konfiguriert werden.

Die Periode ist die Periode mit der der :cb:`Value`
Callback ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn der Wert sich im Vergleich zum letzten mal geändert
hat. Ändert der Wert sich nicht innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen des Werts.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Value Callback Configuration',
'elements': [('Channel', 'uint8', 1, 'in', {'constant_group': 'Channel'}),
             ('Period', 'uint32', 1, 'out', {'divisor': 1000, 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration for the given channel as set by
:func:`Set Value Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration für den gegebenen Kanal zurück, wie mittels
:func:`Set Value Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set All Value Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in', {'factor': 1000, 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period is the period with which the :cb:`All Value`
callback is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.
""",
'de':
"""
Die Periode ist die Periode mit der der :cb:`All Value`
Callback ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn der Wert sich im Vergleich zum letzten mal geändert
hat. Ändert der Wert sich nicht innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen des Werts.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get All Value Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out', {'divisor': 1000, 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set All Value Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set All Value Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Edge Count',
'elements': [('Channel', 'uint8', 1, 'in', {'constant_group': 'Channel'}),
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
Gibt den aktuellen Wert des Flankenzählers für den ausgewählten Kanal zurück.
Die zu zählenden Flanken können mit :func:`Set Edge Count Configuration`
konfiguriert werden.

Wenn reset counter auf *true* gesetzt wird, wird der Zählerstand direkt
nach dem auslesen auf 0 zurückgesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Edge Count Configuration',
'elements': [('Channel', 'uint8', 1, 'in', {'constant_group': 'Channel'}),
             ('Edge Type', 'uint8', 1, 'in', {'constant_group': 'Edge Type'}),
             ('Debounce', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Configures the edge counter for a specific channel.

The edge type parameter configures if rising edges, falling edges or both are
counted. Possible edge types are:

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
steigende, fallende oder beide Flanken gezählt werden. Mögliche Flankentypen
sind:

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
'elements': [('Channel', 'uint8', 1, 'in', {'constant_group': 'Channel'}),
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
'type': 'function',
'name': 'Set Channel LED Config',
'elements': [('Channel', 'uint8', 1, 'in', {'constant_group': 'Channel'}),
             ('Config', 'uint8', 1, 'in', {'constant_group': 'Channel LED Config'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Each channel has a corresponding LED. You can turn the LED off, on or show a
heartbeat. You can also set the LED to "Channel Status". In this mode the
LED is on if the channel is high and off otherwise.

By default all channel LEDs are configured as "Channel Status".
""",
'de':
"""
Jeder Kanal hat eine dazugehörige LED. Die LEDs können individuell an oder
ausgeschaltet werden. Zusätzlich kann ein Heartbeat oder der Kanalstatus
angezeigt werden. Falls Kanalstatus gewählt wird ist die LED an wenn
ein High-Signal am Kanal anliegt und sonst aus.

Standardmäßig sind die LEDs für alle Kanäle auf Kanalstatus konfiguriert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Channel LED Config',
'elements': [('Channel', 'uint8', 1, 'in', {'constant_group': 'Channel'}),
             ('Config', 'uint8', 1, 'out', {'constant_group': 'Channel LED Config'})],
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
'name': 'Value',
'elements': [('Channel', 'uint8', 1, 'out', {'constant_group': 'Channel'}),
             ('Changed', 'bool', 1, 'out'),
             ('Value', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set Value Callback Configuration`.

The :word:`parameters` are the channel, a value-changed indicator and the actual
value for the channel. The `changed` parameter is true if the value has changed
since the last callback.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set Value Callback Configuration` gesetzten Konfiguration

Die :word:`parameters` sind der Kanal, Changed und der Wert. Der `changed`-Parameter
ist True wenn sich der Wert seit dem letzten Callback geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'All Value',
'elements': [('Changed', 'bool', 4, 'out'),
             ('Value', 'bool', 4, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set All Value Callback Configuration`.

The :word:`parameters` are the same as :func:`Get Value`. Additional the
`changed` parameter is true if the value has changed since
the last callback.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set All Value Callback Configuration` gesetzten Konfiguration

Die :word:`parameters` sind der gleiche wie :func:`Get Value`. Zusätzlich ist der
`changed`-Parameter True wenn sich der Wert seit dem letzten Callback geändert hat.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Value', 'value'), [(('Value', ['Channel 0', 'Channel 1', 'Channel 2', 'Channel 3']), 'bool', 4, None, None, None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Value', 'value'), [(('Channel', 'Channel'), 'uint8:constant', 1, None, None, None), (('Changed', 'Changed'), 'bool', 1, None, None, None), (('Value', 'Value'), 'bool', 1, None, None, None)], None, None),
              ('callback_configuration', ('Value', 'value (channel 1)'), [('uint8', 1)], 100, False, None, [])]
})

com['examples'].append({
'name': 'Edge Count',
'functions': [('setter', 'Set Edge Count Configuration', [('uint8', 3), ('uint8', 0), ('uint8', 10)], 'Configure rising edge count (channel 3) with 10ms debounce', None),
              ('loop_header', 10, 'Get edge count 10 times with 1s delay'),
              ('sleep', 1000, None, None),
              ('getter', ('Get Edge Count', 'edge count'), [(('Count', 'Count'), 'uint32', 1, None, None, None)], [('uint8', 3), ('bool', False)]),
              ('loop_footer',)]
})

def input_channel(index):
    return {
            'id': 'Input {0}'.format(index),
            'type': 'Input',
            'label': 'Input Value {0}'.format(index),

            'init_code':"""this.setValueCallbackConfiguration({0}, channelCfg.updateInterval, true);
this.setChannelLEDConfig({0}, channelCfg.ledConfig);""".format(index),
            'dispose_code': """this.setValueCallbackConfiguration({0}, 0, true);""".format(index),

            'getters': [{
                'packet': 'Get Value',
                'transform': 'value[{0}] ? OnOffType.ON : OnOffType.OFF'.format(index)}],

            'callbacks': [{
                'filter': 'channel == {0}'.format(index),
                'packet': 'Value',
                'transform': 'value ? OnOffType.ON : OnOffType.OFF'}],

            'is_trigger_channel': False
        }

def edge_count_channel(index):
    return {
            'id': 'Edge Count Input {0}'.format(index),
            'type': 'Edge Count',
            'label': 'Edge Count Input {0}'.format(index),

            'init_code':"""this.setEdgeCountConfiguration({0}, channelCfg.edgeType, channelCfg.debounce);""".format(index),

            'getters': [{
                'packet': 'Get Edge Count',
                'packet_params': [str(index), 'channelCfg.resetOnRead'],
                'transform': 'new QuantityType<>(value, {unit})'}],

            'java_unit': 'SmartHomeUnits.ONE',
            'is_trigger_channel': False
        }


com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.OnOffType'],
    'channels': [input_channel(i) for i in range(0, 4)] + [edge_count_channel(i) for i in range(0, 4)],
    'channel_types': [
        oh_generic_channel_type('Input', 'Switch', 'Input Value',
                     description='The logic level that is currently measured on the input.',
                     read_only=True,
                     params=[{
                        'name': 'LED Config',
                        'type': 'integer',
                        'options': [('Off', 0),
                                    ('On', 1),
                                    ('Show Heartbeat', 2),
                                    ('Show Channel Status', 3)],
                        'limitToOptions': 'true',
                        'default': '3',

                        'label': 'LED Configuration',
                        'description': 'Each channel has a corresponding LED. You can turn the LED off, on or show a heartbeat. You can also set the LED to Channel Status. In this mode the LED is on if the channel is high and off otherwise.',
                    }]),
        oh_generic_channel_type('Edge Count', 'Number:Dimensionless', 'Edge Count',
                     description='The current value of the edge counter for the selected channel',
                     read_only=True,
                     params=[{
                            'name': 'Edge Type',
                            'type': 'integer',
                            'options':[('Rising', 0),
                                       ('Falling', 1),
                                       ('Both', 2)],
                            'limitToOptions': 'true',
                            'default': '0',

                            'label': 'Edge Type',
                            'description': 'The edge type parameter configures if rising edges, falling edges or both are counted.',
                        },{
                            'name': 'Debounce',
                            'type': 'integer',

                            'default': '100',

                            'label': 'Debounce Time',
                            'description': 'The debounce time in ms.',
                        },{
                            'name': 'Reset On Read',
                            'type': 'boolean',

                            'default': 'false',

                            'label': 'Reset Edge Count On Update',
                            'description': 'Enabling this will reset the edge counter after OpenHAB reads its value. Use this if you want relative edge counts per update.',
                        }])
    ],
    'actions': ['Get Value', 'Get Channel LED Config', 'Get Edge Count Configuration']
}
