# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Hall Effect Bricklet communication config

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 240,
    'name': 'Hall Effect',
    'display_name': 'Hall Effect',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Detects presence of magnetic field',
        'de': 'Detektiert Magnetfelder'
    },
    'released': True,
    'documented': True,
    'discontinued': False, # selling remaining stock, replaced by Hall Effect Bricklet 2.0
    'features': [
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append({
'name': 'Edge Type',
'type': 'uint8',
'constants': [('Rising', 0),
              ('Falling', 1),
              ('Both', 2)]
})

com['packets'].append({
'type': 'function',
'name': 'Get Value',
'elements': [('Value', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns *true* if a magnetic field of 3.5 millitesla or greater is detected.
""",
'de':
"""
Gibt *true* zurück wenn ein Magnetfeld mit 3,5 Millitesla oder größer
detektiert wird.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Edge Count',
'elements': [('Reset Counter', 'bool', 1, 'in', {}),
             ('Count', 'uint32', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current value of the edge counter. You can configure
edge type (rising, falling, both) that is counted with
:func:`Set Edge Count Config`.

If you set the reset counter to *true*, the count is set back to 0
directly after it is read.
""",
'de':
"""
Gibt den aktuellen Wert des Flankenzählers zurück. Die zu
zählenden Flanken (steigend, fallend, beide) können mit
:func:`Set Edge Count Config` konfiguriert werden.

Wenn reset counter auf *true* gesetzt wird, wird der Zählerstand direkt
nach dem auslesen auf 0 zurückgesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Edge Count Config',
'elements': [('Edge Type', 'uint8', 1, 'in', {'constant_group': 'Edge Type', 'default': 0}),
             ('Debounce', 'uint8', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 100})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
The edge type parameter configures if rising edges, falling edges or
both are counted. Possible edge types are:

* 0 = rising
* 1 = falling
* 2 = both

A magnetic field of 3.5 millitesla or greater causes a falling edge and a
magnetic field of 2.5 millitesla or smaller causes a rising edge.

If a magnet comes near the Bricklet the signal goes low (falling edge), if
a magnet is removed from the vicinity the signal goes high (rising edge).

Configuring an edge counter resets its value to 0.

If you don't know what any of this means, just leave it at default. The
default configuration is very likely OK for you.
""",
'de':
"""
Der edge type Parameter konfiguriert den zu zählenden Flankentyp. Es können
steigende, fallende oder beide Flanken gezählt werden. Mögliche Flankentypen
sind:

* 0 = steigend
* 1 = fallend
* 2 = beide

Wird ein Magnet in die Nähe des Bricklets gebracht (>3,5 Millitesla) erzeugt dies ein *low*-Signal
(fallende Flanke), wenn ein Magnet vom Bricklet entfernt (<2,5 Millitesla) wird entsteht ein
*high*-Signal (steigende Flanke).

Durch das Konfigurieren wird der Wert des Flankenzählers auf 0 zurückgesetzt.

Falls unklar ist was dies alles bedeutet, kann diese Funktion einfach
ignoriert werden. Die Standardwerte sind in fast allen Situationen OK.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Edge Count Config',
'elements': [('Edge Type', 'uint8', 1, 'out', {'constant_group': 'Edge Type', 'default': 0}),
             ('Debounce', 'uint8', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 100})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the edge type and debounce time as set by :func:`Set Edge Count Config`.
""",
'de':
"""
Gibt den Flankentyp sowie die Entprellzeit zurück, wie von
:func:`Set Edge Count Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Edge Interrupt',
'elements': [('Edges', 'uint32', 1, 'in', {'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the number of edges until an interrupt is invoked.

If *edges* is set to n, an interrupt is invoked for every n-th detected edge.

If *edges* is set to 0, the interrupt is disabled.
""",
'de':
"""
Setzt die Anzahl der zu zählenden Flanken bis ein Interrupt
aufgerufen wird.

Wenn *edges* auf n gesetzt ist, wird der Interrupt nach jeder
n-ten detektierten Flanke aufgerufen.

Wenn *edges* auf 0 gesetzt ist, wird der Interrupt deaktiviert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Edge Interrupt',
'elements': [('Edges', 'uint32', 1, 'out', {'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the edges as set by :func:`Set Edge Interrupt`.
""",
'de':
"""
Gibt *edges* zurück, wie von :func:`Set Edge Interrupt` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Edge Count Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Edge Count` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Edge Count` callback is only triggered if the edge count has changed
since the last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Edge Count` Callback ausgelöst
wird. Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Edge Count` Callback wird nur ausgelöst, wenn sich die Flankenzählung
seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Edge Count Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Edge Count Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Edge Count Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Edge Interrupt',
'elements': [('Count', 'uint32', 1, 'out', {}),
             ('Value', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered every n-th count, as configured with
:func:`Set Edge Interrupt`. The :word:`parameters` are the
current count and the current value (see :func:`Get Value` and
:func:`Get Edge Count`).
""",
'de':
"""
Dieser Callback bei jedem n-ten Zählerwert ausgelöst, wie von
:func:`Set Edge Interrupt` konfiguriert. Die :word:`parameter`
sind der aktuelle Zählerstand und der aktuelle Wert (siehe
:func:`Get Value` und :func:`Get Edge Count`).
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Edge Count',
'elements': [('Count', 'uint32', 1, 'out', {}),
             ('Value', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Edge Count Callback Period`. The :word:`parameters` are the
current count and the current value (see :func:`Get Value` and
:func:`Get Edge Count`).

The :cb:`Edge Count` callback is only triggered if the count or value changed
since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Edge Count Callback Period`, ausgelöst. Die :word:`parameter`
sind der aktuelle Zählerstand und der aktuelle Wert (siehe
:func:`Get Value` and :func:`Get Edge Count`).

Der :cb:`Edge Count` Callback wird nur ausgelöst, wenn sich mindestens einer
der beiden Werte seit der letzten Auslösung geändert hat.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Edge Count', 'edge count without reset'), [(('Count', 'Count'), 'uint32', 1, None, None, None)], [('bool', False)])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Edge Count', 'edge count'), [(('Count', 'Count'), 'uint32', 1, None, None, None), (('Value', None), 'bool', 1, None, None, None)], None, None),
              ('callback_period', ('Edge Count', 'edge count'), [], 50)]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.OnOffType'],
    'param_groups': oh_generic_channel_param_groups(),
    'params': [{
            'packet': 'Set Edge Count Config',
            'element': 'Edge Type',

            'name': 'Edge Type',
            'type': 'integer',
            'options':[('Rising', 0),
                        ('Falling', 1),
                        ('Both', 2)],
            'limitToOptions': 'true',
            'default': 0,

            'label': 'Edge Type',
            'description': 'The edge type parameter configures if rising edges, falling edges or both are counted.',
        }, {
            'packet': 'Set Edge Count Config',
            'element': 'Debounce',

            'name': 'Debounce',
            'type': 'integer',

            'default': 100,

            'label': 'Debounce Time',
            'description': 'The debounce time in ms.',
        }],
    'channels': [
        {
            'id': 'Edge Count',
            'type': 'Edge Count',
            'label': 'Edge Count',

            'init_code':"""this.setEdgeCountConfig(cfg.edgeType.shortValue(), cfg.debounce.shortValue());
            this.setEdgeInterrupt(channelCfg.refreshCount);""",

            'getters': [{
                'packet': 'Get Edge Count',
                'packet_params': ['channelCfg.resetOnRead'],
                'transform': 'new QuantityType<>(value, {unit})'}],

            'callbacks': [{
                'packet': 'Edge Count',
                'transform': 'new QuantityType<>(count, {unit})'
            }],

            'java_unit': 'SmartHomeUnits.ONE',
            'is_trigger_channel': False
        }, {
            'id': 'Magnetic Field Detected',
            'type': 'Magnetic Field Detected',
            'label': 'Magnetic Field Detected',

            'getters': [{
                'packet': 'Get Value',
                'transform': 'value ? OnOffType.ON : OnOffType.OFF'}],

            'is_trigger_channel': False
        }
    ],
    'channel_types': [
        oh_generic_channel_type('Edge Count', 'Number:Dimensionless', 'Edge Count',
                    update_style=None,
                    description='The current value of the edge counter.',
                    read_only=True,
                    pattern='%d',
                    params=[{
                        'packet': 'Set Edge Interrupt',
                        'element': 'Edges',

                        'name': 'Refresh Count',
                        'type': 'integer',

                        'default': 1,

                        'label': 'Refresh Value Every N-th Edge.',
                    }, {
                        'packet': 'Get Edge Count',
                        'element': 'Reset Counter',

                        'name': 'Reset On Read',
                        'type': 'boolean',

                        'default': 'false',

                        'label': 'Reset Edge Count On Update',
                        'description': 'Enabling this will reset the edge counter after OpenHAB reads its value. Use this if you want relative edge counts per update.',
                    }]),
        oh_generic_channel_type('Magnetic Field Detected', 'Switch', 'Magnetic Field Detected',
                    update_style=None,
                    description='Enabled if a magnetic field of 3.5 millitesla or greater is detected.',
                    read_only=True),
    ],
    'actions': ['Get Value', {'fn': 'Get Edge Count', 'refreshs': ['Edge Count']}, 'Get Edge Count Config']
}
