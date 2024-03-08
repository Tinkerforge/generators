# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Dual AC In Bricklet communication config

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerfoe.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2174,
    'name': 'Industrial Dual AC In',
    'display_name': 'Industrial Dual AC In',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '2 inputs that can detect AC voltages of up to 230V',
        'de': '2 Eingänge die AC-Spannungen von bis zu 230V detektieren können'
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
'name': 'Channel',
'type': 'uint8',
'constants': [('0', 0),
              ('1', 1)]
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
'elements': [('Value', 'bool', 2, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the input values as bools, *true* refers to "AC voltage detected" and *false* refers to no "AC voltage detected".
""",
'de':
"""
Gibt die Eingangswerte als Bools zurück, *true* bedeutet, dass eine AC-Spannung anliegt und *false* bedeutet, dass keine AC-Spannung anliegt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Value Callback Configuration',
'elements': [('Channel', 'uint8', 1, 'in', {'constant_group': 'Channel'}),
             ('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
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
             ('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
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
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
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
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
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
'name': 'Set Channel LED Config',
'elements': [('Channel', 'uint8', 1, 'in', {'constant_group': 'Channel'}),
             ('Config', 'uint8', 1, 'in', {'constant_group': 'Channel LED Config', 'default': 3})],
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
'name': 'Value',
'elements': [('Channel', 'uint8', 1, 'out', {'constant_group': 'Channel'}),
             ('Changed', 'bool', 1, 'out', {}),
             ('Value', 'bool', 1, 'out', {})],
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
'elements': [('Changed', 'bool', 2, 'out', {}),
             ('Value', 'bool', 2, 'out', {})],
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
'functions': [('getter', ('Get Value', 'value'), [(('Value', ['Channel 0', 'Channel 1']), 'bool', 2, None, None, None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Value', 'value'), [(('Channel', 'Channel'), 'uint8:constant', 1, None, None, None), (('Changed', 'Changed'), 'bool', 1, None, None, None), (('Value', 'Value'), 'bool', 1, None, None, None)], None, None),
              ('callback_configuration', ('Value', 'value (channel 1)'), [('uint8', 1)], 100, False, None, [])]
})

