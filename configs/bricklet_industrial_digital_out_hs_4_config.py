# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Digital Out HS 4 Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2150,
    'name': 'Industrial Digital Out HS 4',
    'display_name': 'Industrial Digital Out HS 4',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'TBD',
        'de': 'TBD'
    },
    'released': False,
    'documented': False,
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
'elements': [('Value', 'bool', 4, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the output value of all four channels. A value of *true* or *false* outputs
logic 1 or logic 0 respectively on the corresponding channel.

Use :func:`Set Selected Value` to change only one output channel state.

All running monoflop timers and PWMs will be aborted if this function is called.

For example: (True, True, False, False) will turn the channels 0-1 high and the
channels 2-3 low.
""",
'de':
"""
Setzt den Zustand aller vier Kanäle. Der Wert *true* bzw. *false* erzeugen
logisch 1 bzw. logisch 0 auf dem entsprechenden Kanal.

Mittels :func:`Set Selected Value` können auch einzelnen Kanäle gesetzt werden.

Alle laufenden Monoflop Timer und PWMs werden abgebrochen, wenn diese Funktion
aufgerufen wird.

Beispiel: (True, True, False, False) setzt die Kanäle 0-1 auf logisch 1 und die
Kanäle 2-3 auf logisch 0.
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
Returns the logic levels that are currently output on the channels.
""",
'de':
"""
Gibt die aktuellen Zustände der Kanäle zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Measurements',
'elements': [('Voltage', 'uint16', 2, 'out'),
             ('Current', 'uint16', 4, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TBD: mA/mV
""",
'de':
"""
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

A running monoflop timer or PWM for the specific channel will be aborted if this
function is called.
""",
'de':
"""
Setzt den Ausgabewert des spezifizierten Kanals ohne die anderen Kanäle zu
beeinflussen.

Ein laufender Monoflop Timer oder PWM für den spezifizierten Kanal wird
abgebrochen, wenn diese Funktion aufgerufen wird.
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

A PWM for the selected channel will be aborted if this function is called.

A monoflop can be used as a failsafe mechanism. For example: Lets assume you
have a RS485 bus and a IO-4 Bricklet is connected to one of the slave
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

Ein PWM für den ausgewählten Kanal wird abgebrochen, wenn diese Funktion
aufgerufen wird.

Ein Monoflop kann als Ausfallsicherung verwendet werden. Beispiel:
Angenommen ein RS485 Bus und ein IO-4 Bricklet ist an ein Slave Stapel
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

com['packets'].append({
'type': 'function',
'name': 'Set Channel LED Config',
'elements': [('Channel', 'uint8', 1, 'in'),
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
Jeder Kanal hat eine dazugehörige LED. Die LEDs können individuell an- oder
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
'elements': [('Channel', 'uint8', 1, 'in'),
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

To turn the PWM off again, you can set the frequency to 0 or any other
function that changes a value of the channel (e.g. :func:`Set Selected Value`).

The maximum duty cycle value is 10000 (100%). The optocoupler of the Industrial Digital
Out 4 Bricklet 2.0 has a rise time and fall time of 11.5us (each) at 24V. So the maximum
useful frequency value is about 400000 (40kHz).

A running monoflop timer for the given channel will be aborted if this function
is called.

The default values are 0, 0.
""",
'de':
"""
Aktiviert ein PWM auf dem angegebenen Kanal. Die Frequenz wird in 1/10Hz angegeben und
die Duty Cycle in 1/100%.

Um die PWM wieder auszustellen, kann die Frequenz auf
0 gesetzt werden oder eine andere Funktion aufgerufen werden die Einstellungen am
Kanal verändert (z.B. :func:`Set Selected Value`).

Der Maximale Duty Cycle-Wert beträgt 10000 (100%). Der auf dem Industrial Digital
Out 4 Bricklet 2.0 verwendete Optokoppler hat eine Anstiegszeit und Abfallzeit von
jeweils 11.5us bei einer Spannung von 24V. Dadurch ist ergibt sich ein maximaler Frequenzwert
von ca. 400000 (40kHz).

Ein laufender Monoflop Timer für den angegebenen Kanal wird abgebrochen, wenn
diese Funktion aufgerufen wird.

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
'type': 'function',
'name': 'Set Measurements Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period is the period with which the :cb:`Measurements` callback
is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.
""",
'de':
"""
Die Periode ist die Periode mit der der :cb:`Measurements` Callback
ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

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
'name': 'Get Measurements Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set Measurements Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set Measurements Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Measurements',
'elements': [('Voltage', 'uint16', 2, 'out'),
             ('Current', 'uint16', 4, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set Measurements Callback Configuration`.

The :word:`parameters` are the same as :func:`Get Measurements`.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set Measurements Callback Configuration` gesetzten Konfiguration

Die :word:`parameters` sind der gleiche wie :func:`Get Measurements`.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('loop_header', 10, 'Set channels alternating high/low 10 times with 100 ms delay'),
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
