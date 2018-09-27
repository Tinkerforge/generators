# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# IO-4 Bricklet 2.0 communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2111,
    'name': 'IO4 V2',
    'display_name': 'IO-4 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '4-channel digital input/output',
        'de': '4 digitale Ein- und Ausgänge'
    },
    'comcu': True,
    'released': True,
    'documented': True,
    'discontinued': False,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Set Value',
'elements': [('Value', 'bool', 4, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the output value of all four channels. A value of *true* or *false* outputs
logic 1 or logic 0 respectively on the corresponding channel.

Use :func:`Set Selected Value` to change only one output channel state.

For example: (True, True, False, False) will turn the channels 0-1 high and the
channels 2-3 low.

.. note::
 This function does nothing for channels that are configured as input. Pull-up
 resistors can be switched on with :func:`Set Configuration`.
""",
'de':
"""
Beispiel: (True, True, False, False) setzt die Kanäle 0-1 auf logisch 1 und die
Kanäle 2-3 auf logisch 0.

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
'elements': [('Value', 'bool', 4, 'out')],
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

.. note::
 This function does nothing for channels that are configured as input. Pull-up
 resistors can be switched on with :func:`Set Configuration`.
""",
'de':
"""
Setzt den Ausgabewert des spezifizierte Kanals ohne die anderen Kanäle zu
beeinflussen.

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
             ('Direction', 'char', 1, 'in', ('Direction', [('In', 'i'),
                                                           ('Out', 'o')])),
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

* (0, 'i', true) will set channel 0 as input pull-up.
* (1, 'i', false) will set channel 1 as input default (floating if nothing is connected).
* (2, 'o', true) will set channel 2 as output high.
* (3, 'o', false) will set channel 3 as output low.

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

* (0, 'i', true) setzt Kanal 0 als Eingang mit Pull-Up.
* (1, 'i', false) setzt Kanal 1 als Standard Eingang (potentialfrei wenn nicht verbunden).
* (2, 'o', true) setzt Kanal 2 als Ausgang im Zustand logisch 1.
* (3, 'o', false) setzt Kanal 3 als Ausgang im Zustand logisch 0.

Die Standardkonfiguration ist Eingang mit Pull-Up.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Direction', 'char', 1, 'out', ('Direction', [('In', 'i'),
                                                            ('Out', 'o')])),
             ('Value', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
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
Returns the callback configuration for the given channel as set by
:func:`Set Input Value Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration für den gegebenen Kanal zurück, wie mittels
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
The first parameter is the desired state of the channel (*true* means output *high*
and *false* means output *low*). The second parameter indicates the time (in ms) that
the channel should hold the state.

If this function is called with the parameters (true, 1500):
The channel will turn on and in 1.5s it will turn off again.

A monoflop can be used as a failsafe mechanism. For example: Lets assume you
have a RS485 bus and a IO-4 Bricklet 2.0 is connected to one of the slave
stacks. You can now call this function every second, with a time parameter
of two seconds. The channel will be *high* all the time. If now the RS485
connection is lost, the channel will turn *low* in at most two seconds.
""",
'de':
"""
Der erste Parameter ist der gewünschte Zustand des Kanals
(*true* bedeutet *high* und *false* *low*). Der zweite Parameter stellt die Zeit
(in ms) dar, in welcher der Kanal den Zustand halten soll.

Wenn diese Funktion mit den Parametern (true, 1500) aufgerufen wird:
Der Kanal wird angeschaltet und nach 1,5s wieder ausgeschaltet.

Ein Monoflop kann als Ausfallsicherung verwendet werden. Beispiel:
Angenommen ein RS485 Bus und ein IO-4 Bricklet 2.0 ist an ein Slave Stapel
verbunden. Jetzt kann diese Funktion sekündlich, mit einem Zeitparameter
von 2 Sekunden, aufgerufen werden.
Der Kanal wird die gesamte Zeit eingeschaltet sein. Wenn jetzt die RS485 Verbindung
getrennt wird, wird der Kanal nach spätestens zwei Sekunden ausschalten.
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
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Edge Type', 'uint8', 1, 'in', ('Edge Type', [('Rising', 0),
                                                            ('Falling', 1),
                                                            ('Both', 2)])),
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
             ('Edge Type', 'uint8', 1, 'out', ('Edge Type', [('Rising', 0),
                                                             ('Falling', 1),
                                                             ('Both', 2)])),
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
Gibt den Flankentyp sowie die Entprellzeit für den ausgewählten Kanal zurück,
wie von :func:`Set Edge Count Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set PWM Configuration',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Frequency', 'uint32', 1, 'in'),
             ('Duty Cycle', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Activates a PWM for the given channel with the frequency given in 1/10Hz and the duty
cycle given in 1/100%.

You need to set the channel to output before you call this function, otherwise it will
be ignored. To turn the PWM off again, you can set the frequency to 0 or any other
function that changes a value of the channel (e.g. :func:`Set Selected Value`).

The maximum frequency value is 320000000 (32MHz). The maximum duty cycle value is
10000 (100%).

The default values are 0, 0.
""",
'de':
"""
Aktiviert ein PWM auf dem angegebenen Kanal. Die Frequenz wird in 1/10Hz angegeben und
die Duty Cycle in 1/100%.

Bevor diese Funktion aufgerufen wird, muss der Kanal als Ausgabe konfiguriert werden,
ansonsten wird der Aufruf ignoriert. Um die PWM wieder auszustellen, kann die Frequenz auf
0 gesetzt werden oder eine andere Funktion aufgerufen werden die Einstellungen am
Kanal verändert (z.B. :func:`Set Selected Value`).

Der maximale Frequenzwert beträgt 320000000 (32MHz). Der Maximale Duty Cycle-Wert beträgt
10000 (100%).

Die Standardwerte sind 0, 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get PWM Configuration',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Frequency', 'uint32', 1, 'out'),
             ('Duty Cycle', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the PWM configuration as set by :func:`Set PWM Configuration`.
""",
'de':
"""
Gibt die PWM Konfiguration zurück, wie von :func:`Set PWM Configuration` gesetzt.
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
'elements': [('Changed', 'bool', 4, 'out'),
             ('Value', 'bool', 4, 'out')],
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
Dieser Callback wird ausgelöst wenn ein Monoflop Timer abläuft (0 erreicht).
:word:`parameters` enthalten den Kanal und den aktuellen
Zustand des Kanals (der Zustand nach dem Monoflop).
"""
}]
})
