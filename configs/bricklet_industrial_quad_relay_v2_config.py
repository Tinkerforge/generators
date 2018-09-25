# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Quad Relay Bricklet 2.0 communication config

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
Sets the value of all four relays. A value of *true* closes the
relay and a value of *false* opens the relay.

Use :func:`Set Selected Value` to only change one relay.
""",
'de':
"""
Setzt den Wert der vier Relais. Ein Wert von *true* schließt das Relais
und ein Wert von *False* öffnet das Relais.

Nutze :func:`Set Selected Value` um einzelne Relais zu schalten.
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

Der dritte Parameter ist die Zeit (in ms) die der Kanal den Zustand
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
'name': 'Set Selected Value',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Value', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the output value of the specified channel without affecting the other
channels.
""",
'de':
"""
Setzt den Ausgabewert des spezifizierten Kanals ohne die anderen Kanäle
zu beeinflussen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Channel LED Config',
'elements': [('LED', 'uint8', 1, 'in'),
             ('Config', 'uint8', 1, 'in', ('Channel LED Config', [('Off', 0),
                                                                  ('On', 1),
                                                                  ('Show Heartbeat', 2),
                                                                  ('Show Channel Status', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Each channel has a corresponding LED. You can turn the LED Off, On or show a
heartbeat. You can also set the LED to "Channel Status". In this mode the
LED is on if the channel is high and off otherwise.

By default all channel LEDs are configured as "Channel Status".
""",
'de':
"""
Jeder Kanal hat eine dazugehörige LED. Die LEDs können individuell an oder
aus-geschaltet werden. Zusätzlich kann ein Hearbeat oder der Kanalstatus
angezeigt werden. Falls Kanalstatus gewählt wird ist die LED an wenn
ein High-Signal am Kanal anliegt und sonst aus.

Standardmäßig sind die LEDs für alle Kanäle auf "Kanalstatus" konfiguriert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Channel LED Config',
'elements': [('LED', 'uint8', 1, 'in'),
             ('Config', 'uint8', 1, 'out', ('Channel LED Config', [('Off', 0),
                                                                   ('On', 1),
                                                                   ('Show Heartbeat', 2),
                                                                   ('Show Channel Status', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the channel LED configuration as set by :func:`Set Channel LED Config`
""",
'de':
"""
Gibt die LED-Konfiguration zurück, wie von :func:`Set Channel LED Config` gesetzt.
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
