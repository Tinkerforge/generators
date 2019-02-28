# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Hall Effect Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2132,
    'name': 'Hall Effect V2',
    'display_name': 'Hall Effect 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '',
        'de': ''
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'discontinued': False,
    'packets': [],
    'examples': []
}

magnetic_flux_density_doc = {
'en':
"""
Returns the magnetic flux density (magnetic induction) in uT (micro Tesla).

TBD: Range etc?
""",
'de':
"""
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Magnetic Flux Density',
    data_name = 'Magnetic Flux Density',
    data_type = 'int16',
    doc       = magnetic_flux_density_doc
)

com['packets'].append({
'type': 'function',
'name': 'Get Counter',
'elements': [('Reset Counter', 'bool', 1, 'in'),
             ('Count', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Counter works up to 10kHz.

Returns the current value of the edge counter. You can configure
edge type (rising, falling, both) that is counted with
:func:`Set Counter Config`.

If you set the reset counter to *true*, the count is set back to 0
directly after it is read.

If you want to get the count periodically, it is recommended to use the
:cb:`Counter` callback. You can set the callback configuration
with :func:`Set Counter Callback Configuration`.
""",
'de':
"""
Gibt den aktuellen Wert des Flankenzählers zurück. Die zu
zählenden Flanken (steigend, fallend, beide) können mit
:func:`Set Counter Config` konfiguriert werden.

Wenn reset counter auf *true* gesetzt wird, wird der Zählerstand direkt
nach dem auslesen auf 0 zurückgesetzt.

Wenn der Zähler periodisch benötigt wird, kann auch der :cb:`Counter` Callback
verwendet werden. Der Callback wird mit der Funktion
:func:`Set Counter Callback Configuration` konfiguriert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Counter Config',
'elements': [('High Threshold', 'int16', 1, 'in'),
             ('Low Threshold', 'int16', 1, 'in'),
             ('Debounce', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""

debounce in us, max 1s
""",
'de':
"""

"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Counter Config',
'elements': [('High Threshold', 'int16', 1, 'out'),
             ('Low Threshold', 'int16', 1, 'out'),
             ('Debounce', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""

""",
'de':
"""

"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Counter Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period in ms is the period with which the :cb:`Counter`
callback is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after at least one of the values has changed. If the values didn't
change within the period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.

The default value is (0, false).
""",
'de':
"""
Die Periode in ms ist die Periode mit der der :cb:`Counter`
Callback ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn sich mindestens ein Wert im Vergleich zum letzten mal geändert
hat. Ändert sich kein Wert innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn ein Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen der Werte.

Der Standardwert ist (0, false).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Counter Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set Counter Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set Counter Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Counter',
'elements': [('Count', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set Counter Callback Configuration`.

The count is the same as you would get with :func:`Get Counter`.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set Counter Callback Configuration` gesetzten Konfiguration

Der Zählerstand ist der gleiche, der auch per :func:`Get Counter`
abgefragt werden kann.
"""
}]
})
