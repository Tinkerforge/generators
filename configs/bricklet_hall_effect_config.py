# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Hall Effect Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 240,
    'name': ('Hall Effect', 'Hall Effect', 'Hall Effect Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Detects presence of magnetic field',
        'de': 'Detektiert Magnetfelder'
    },
    'released': True,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Get Value',
'elements': [('Value', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns *true* if a magnetic field of 35 Gauss (3.5mT) or greater is detected.
""",
'de':
"""
Gibt *true* zurück wenn ein Magnetfeld mit 35 Gauss (3,5mT) oder größer
detektiert wird.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Edge Count',
'elements': [('Reset Counter', 'bool', 1, 'in'),
             ('Count', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current value of the edge counter. You can configure
edge type (rising, falling, both) that is counted with
:func:`SetEdgeCountConfig`.

If you set the reset counter to *true*, the count is set back to 0
directly after it is read.
""",
'de':
"""
Gibt den aktuellen Wert des Flankenzählers zurück. Die zu
zählenden Flanken (steigend, fallend, beide) können mit
:func:`SetEdgeCountConfig` konfiguriert werden.

Wenn reset counter auf *true* gesetzt wird, wird der Zählerstand direkt
nach dem auslesen auf 0 zurückgesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Edge Count Config',
'elements': [('Edge Type', 'uint8', 1, 'in', ('Edge Type', [('Rising', 0),
                                                            ('Falling', 1),
                                                            ('Both', 2)])),
             ('Debounce', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
The edge type parameter configures if rising edges, falling edges or 
both are counted. Possible edge types are:

* 0 = rising (default)
* 1 = falling
* 2 = both

A magnetic field of 35 Gauss (3.5mT) or greater causes a falling edge and a
magnetic field of 25 Gauss (2.5mT) or smaller causes a rising edge.

If a magnet comes near the Bricklet the signal goes low (falling edge), if
a magnet is removed from the vicinity the signal goes high (rising edge).

The debounce time is given in ms.

Configuring an edge counter resets its value to 0.

If you don't know what any of this means, just leave it at default. The
default configuration is very likely OK for you.

Default values: 0 (edge type) and 100ms (debounce time)
""",
'de':
"""
Der edge type Parameter konfiguriert den zu zählenden Flankentyp. Es können
steigende, fallende oder beide Flanken gezählt werden. Mögliche Flankentypen
sind:

* 0 = steigend (Standard)
* 1 = fallend
* 2 = beide

Wird ein Magnet in die Nähe des Bricklets gebracht (>35 Gauss) erzeugt dies ein *low*-Signal
(fallende Flanke), wenn ein Magnet vom Bricklet entfernt (<25 Gauss) wird entsteht ein
*high*-Signal (steigende Flanke).

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
'name': 'Get Edge Count Config',
'elements': [('Edge Type', 'uint8', 1, 'out', ('Edge Type', [('Rising', 0),
                                                             ('Falling', 1),
                                                             ('Both', 2)])),
             ('Debounce', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the edge type and debounce time as set by :func:`SetEdgeCountConfig`.
""",
'de':
"""
Gibt den Flankentyp sowie die Entprellzeit zurück, wie von
:func:`SetEdgeCountConfig` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Edge Interrupt',
'elements': [('Edges', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the number of edges until an interrupt is invoked.

If *edges* is set to n, an interrupt is invoked for every n-th detected edge.

If *edges* is set to 0, the interrupt is disabled.

Default value is 0.
""",
'de':
"""
Setzt die Anzahl der zu zählenden Flanken bis ein Interrupt
aufgerufen wird.

Wenn *edges* auf n gesetzt ist, wird der Interrupt nach jeder
n-ten detektierten Flanke aufgerufen.

Wenn *edges* auf 0 gesetzt ist, wird der Interrupt deaktiviert.

Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Edge Interrupt',
'elements': [('Edges', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the edges as set by :func:`SetEdgeInterrupt`.
""",
'de':
"""
Gibt *edges* zurück, wie von :func:`SetEdgeInterrupt` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Edge Count Callback Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`EdgeCount` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`EdgeCount` is only triggered if the edge count has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`EdgeCount` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`EdgeCount` wird nur ausgelöst wenn sich die Flankenzählung seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Edge Count Callback Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetEdgeCountCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetEdgeCountCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Edge Interrupt',
'elements': [('Count', 'uint32', 1, 'out'),
             ('Value', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered every n-th count, as configured with
:func:`SetEdgeInterrupt`. The :word:`parameters` are the
current count and the current value (see :func:`GetValue` and :func:`GetEdgeCount`).
""",
'de':
"""
Dieser Callback bei jedem n-ten Zählerwert ausgelöst, wie von
:func:`SetEdgeInterrupt` konfiguriert. Die :word:`parameter` 
sind der aktuelle Zählerstand und der aktuelle Wert (siehe
:func:`GetValue` und :func:`GetEdgeCount`).
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Edge Count',
'elements': [('Count', 'uint32', 1, 'out'),
             ('Value', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetEdgeCountCallbackPeriod`. The :word:`parameters` are the
current count and the current value (see :func:`GetValue` and :func:`GetEdgeCount`).

:func:`EdgeCount` is only triggered if the count or value changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit 
:func:`SetEdgeCountCallbackPeriod`, ausgelöst. Die :word:`parameter` 
sind der aktuelle Zählerstand und der aktuelle Wert (siehe
:func:`GetValue` and :func:`GetEdgeCount`).

:func:`EdgeCount` wird nur ausgelöst wenn sich mindestens einer
der beiden Werte seit der letzten Auslösung geändert hat.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Edge Count', 'edge count without reset'), [(('Edge Count', 'Edge Count'), 'uint32', None, None, None, None)], [('bool', False)])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Edge Count', 'edge count'), [(('Edge Count', 'Edge Count'), 'uint32', None, None, None, None), (('Value', None), 'bool', None, None, None, None)], None, None),
              ('callback_period', ('Edge Count', 'edge count'), [], 50)]
})
