# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Quad Relay Bricklet communication config

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
    'released': False,
    'documented': False,
    'discontinued': False,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Set Output Value',
'elements': [('Value', 'bool', 4, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the output value of all four relays. A value of *true* closes the
relay and a value of *false* opens the relay.

Use :func:`Set Selected Output Value` to only change one relay.
""",
'de':
"""
Setzt den Ausgabewert der vier Relais. Ein Wert von *true* schließt das Relais
und ein Wert von *False* öffnet das Relais.

Nutze :func:`Set Selected Output Value` um einzelne Relais zu schalten.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Output Value',
'elements': [('Value', 'bool', 4, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the values as set by :func:`Set Output Value`.
""",
'de':
"""
Gibt die Werte zurück, wie von :func:`Set Output Value` gesetzt.
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
have a RS485 bus and a Quad Relay Bricklet connected to one of the slave
stacks. You can now call this function every second, with a time parameter
of two seconds and channel 0 closed. Channel 0 will be closed all the time. If now
the RS485 connection is lost, then channel 0 will be opened in at most two seconds.
""",
'de':
"""
Konfiguriert einen Monoflop für den angegebenen Channel.

Der zweite Parameter ist eine der gewünschten Zuständ des
festgelegten Channels. Eine *true bedeutet Relais geschlossen und
ein *false* bedeutet Relais offen.

Der dritte Parameter ist die Zeit (in ms) die der Channel den Zustand
halten sollen.

Wenn diese Funktion mit den Parametern (0, 1, 1500) aufgerufen wird,
wird channel 0 geschlossen und nach 1,5s wieder geöffnet.

Ein Monoflop kann zur Ausfallsicherung verwendet werden. Beispiel:
Angenommen ein RS485 Bus und ein Quad Relay Bricklet ist an ein Slave
Stapel verbunden.
Jetzt kann diese Funktion sekündlich, mit einem Zeitparameter von 2 Sekunden,
aufgerufen werden. Der Channel wird die gesamte Zeit im Zustand geschlossen sein.
Wenn jetzt die RS485 Verbindung getrennt wird, wird der Channel nach spätestens
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
Gibt (für den angegebenen Channel) den aktuellen Zustand und die Zeit, wie von
:func:`Set Monoflop` gesetzt, sowie die noch verbleibende Zeit bis zum
Zustandswechsel, zurück.

Wenn der Timer aktuell nicht läuft, ist die noch verbleibende Zeit 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Selected Output Value',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Value', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the output value of the specified channel without affecting the other channels.
""",
'de':
"""
Setzt den Ausgabewert des spezifizierten Channels ohne die anderen Channelne zu beeinflussen.
"""
}]
})

# TODO: Documentation

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
heartbeat. You can also ste the LED to "Channel Status". In this mode the
LED is on if the channel is high and off otherwise.

By default all channel LEDs are configured as "Channel Status".
""",
'de':
"""
Jeder Kanal hat eine dazugehörige LED. Die LEDs können individuell an oder
aus-geschaltet werden. Zusätzlich kann ein Hearbeat oder der Kanal-Status
angezeigt werden. Falls Kanal-Status gewählt wird ist die LED an wenn
ein High-Signal am Kanal anliegt und sonst aus.

Standardmäßig sind die LEDs für alle Kanäle auf "Kanal-Status" konfiguriert.
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
Returns the Channel LED configuration as set by :func:`Set Channel LED Config`
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
:word:`parameters` enthalten den Channel und den aktuellen
Zustand des Channels (der Zustand nach dem Monoflop).
"""
}]
})
