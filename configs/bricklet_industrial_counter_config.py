# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Counter Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 293,
    'name': 'Industrial Counter',
    'display_name': 'Industrial Counter',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'TBD',
        'de': 'TBD'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'discontinued': False,
    'packets': [],
    'examples': []
}

CONSTANT_CHANNEL = ('Channel', [('0', 0),
                                ('1', 1),
                                ('2', 2),
                                ('3', 3)])

CONSTANT_COUNT_EDGE = ('Count Edge', [('Rising', 0),
                                      ('Falling', 1),
                                      ('Both', 2)])

CONSTANT_COUNT_DIRECTON = ('Count Direction', [('Up', 0),
                                               ('Down', 1),
                                               ('External Up', 2),
                                               ('External Down', 3)])

CONSTANT_DUTY_CYCLE_PRESCALER = ('Duty Cycle Prescaler', [('1', 0),
                                                          ('2', 1),
                                                          ('4', 2),
                                                          ('8', 3),
                                                          ('16', 4),
                                                          ('32', 5),
                                                          ('64', 6),
                                                          ('128', 7),
                                                          ('256', 8),
                                                          ('512', 9),
                                                          ('1024', 10),
                                                          ('2048', 11),
                                                          ('4096', 12),
                                                          ('8192', 13),
                                                          ('16384', 14),
                                                          ('32768', 15),
                                                          ('Auto', 255)])

CONSTANT_FREQUENCY_INTEGRATION_TIME = ('Frequency Integration Time', [('128 MS', 0),
                                                                      ('256 MS', 1),
                                                                      ('512 MS', 2),
                                                                      ('1024 MS', 3),
                                                                      ('2048 MS', 4),
                                                                      ('4096 MS', 5),
                                                                      ('8192 MS', 6),
                                                                      ('16384 MS', 7),
                                                                      ('32768 MS', 8),
                                                                      ('Auto', 255)])



com['packets'].append({
'type': 'function',
'name': 'Get Counter',
'elements': [('Channel', 'uint8', 1, 'in', CONSTANT_CHANNEL),
             ('Counter', 'int64', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current counter value for the given channel.
""",
'de':
"""
Gibt den aktuellen Zählerstand für den gegebenen Kanal zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get All Counter',
'elements': [('Counter', 'int64', 4, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current counter values for all four channels
""",
'de':
"""
Gibt die Zählerstände für alle vier Kanäle zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Counter',
'elements': [('Channel', 'uint8', 1, 'in', CONSTANT_CHANNEL),
             ('Counter', 'int64', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the counter value for the given channel.

The default value for the counters on startup is 0.
""",
'de':
"""
Setzt den Zählerstand für den gegebenen Kanal.

Der Standardwert für alle Zähler nach dem Start ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set All Counter',
'elements': [('Counter', 'int64', 4, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the counter values for all four channels.

The default value for the counters on startup is 0.
""",
'de':
"""
Setzt die Zählerstände für alle vier Kanäle.

Der Stadardwert für die Zähler nach dem Starten ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Signal Data',
'elements': [('Channel', 'uint8', 1, 'in', CONSTANT_CHANNEL),
             ('Duty Cycle', 'uint16', 1, 'out'),
             ('Period', 'uint64', 1, 'out'),
             ('Frequency', 'uint32', 1, 'out'),
             ('Channel Value', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the signal data (duty cycle, period, frequency and value) for the given channel.

The units are:

* Duty Cycle: 1/100 %
* Period: ns
* Frequency: mHz (1/1000 Hz)
* Channel Value: true = high, false = low
""",
'de':
"""
Gibt die Signaldaten (Tastverhältnis, Periode, Frequenz und Status) für den gegebenen Kanal.

Die Einheiten sind:

* Tastverhältnis: 1/100 %
* Periode: ns
* Frequenz: mHz (1/1000 Hz)
* Kanal Status: true = high, false = low
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get All Signal Data',
'elements': [('Duty Cycle', 'uint16', 4, 'out'),
             ('Period', 'uint64', 4, 'out'),
             ('Frequency', 'uint32', 4, 'out'),
             ('Channel Value', 'bool', 4, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the signal data (duty cycle, period, frequency and value) for all for chanels.

The units are:

* Duty Cycle: 1/100 %
* Period: ns
* Frequency: mHz (1/1000 Hz)
* Channel Value: true = high, false = low
""",
'de':
"""
Gibt die Signaldaten (Tastverhältnis, Periode, Frequenz und Status) für den alle Kanäle zurück.

Die Einheiten sind:

* Tastverhältnis: 1/100 %
* Periode: ns
* Frequenz: mHz (1/1000 Hz)
* Kanal Status: true = high, false = low
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Counter Active',
'elements': [('Channel', 'uint8', 1, 'in', CONSTANT_CHANNEL),
             ('Active', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Activates/deactivates the counter of the given channel.

true = activate, false = deactivate. 

By default all channels are activated.
""",
'de':
"""
Aktiviert/Deaktiviert den Zähler für den gegebenen Kanal.

true = aktiviert, false = deaktiviert.

Standardmäßig sind alle Kanäle aktiviert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set All Counter Active',
'elements': [('Active', 'bool', 4, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Activates/deactivates the counter of all four channels.

true = activate, false = deactivate. 

By default all channels are activated.
""",
'de':
"""
Aktiviert/Deaktiviert den Zähler für alle Kanäle.

true = aktiviert, false = deaktiviert.

Standardmäßig sind alle Kanäle aktiviert.

"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Counter Active',
'elements': [('Channel', 'uint8', 1, 'in', CONSTANT_CHANNEL),
             ('Active', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the activation state of the given channel.

true = activate, false = deactivate. 
""",
'de':
"""
Gibt den Zustand (aktiviert/deaktiviert) des gegebenen Zähler zurück.

true = aktiviert, false = deaktiviert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get All Counter Active',
'elements': [('Active', 'bool', 4, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the activation state of all four channels.

true = activate, false = deactivate. 
""",
'de':
"""
Gibt den Zustand (aktiviert/deaktiviert) aller Zähler zurück.

true = aktiviert, false = deaktiviert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Counter Configuration',
'elements': [('Channel', 'uint8', 1, 'in', CONSTANT_CHANNEL),
             ('Count Edge', 'uint8', 1, 'in', CONSTANT_COUNT_EDGE),
             ('Count Direction', 'uint8', 1, 'in', CONSTANT_COUNT_DIRECTON),
             ('Duty Cycle Prescaler', 'uint8', 1, 'in', CONSTANT_DUTY_CYCLE_PRESCALER),
             ('Frequency Integration Time', 'uint8', 1, 'in', CONSTANT_FREQUENCY_INTEGRATION_TIME)],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the counter configuration for the given channel.

* Count Edge: Counter can count on rising, falling or both edges.
* Count Direction: Counter can count up or down. You can also use 
  another channel as direction input, see 
  `here <http://127.0.0.1:8000/en/doc/Hardware/Bricklets/Industrial_Counter.html#external-count-direction>`__
  for details.
* Duty Cycle Prescaler: Sets a divider for the internal clock. See
  `here <http://127.0.0.1:8000/en/doc/Hardware/Bricklets/Industrial_Counter.html#duty-cycle-prescaler-and-frequency-integration-time>`__
  for details.
* Frequency Integration Time: Sets the integration time for the
  frequency measurement. See 
  `here <http://127.0.0.1:8000/en/doc/Hardware/Bricklets/Industrial_Counter.html#duty-cycle-prescaler-and-frequency-integration-time>`__
  for details.
""",
'de':
"""
Setzt die Zähler-Konfiguration für den gegebenen Kanal.

* Zählerflanke: Der Zähler kann bei der steigenden, fallenden oder beiden Flanken zählen
* Zählerrichtung: Der Zähler kann hoch-/ oder runterzählen. Es kann auch ein weiterer Kanal als Richtungseingang genutzt werden. Siehe 
  `hier <http://127.0.0.1:8000/en/doc/Hardware/Bricklets/Industrial_Counter.html#external-count-direction>`__
  für weitere Details.
* Tastverhältnis Prescaler: Setzt einen Teiler für die interne Clock. Siehe 
  `hier <http://127.0.0.1:8000/en/doc/Hardware/Bricklets/Industrial_Counter.html#duty-cycle-prescaler-and-frequency-integration-time>`__
  für weitere Details.
* Frequenz-Integration: Setzt die Integrationszeit für die Frequenzmessung. Siehe
  `hier <http://127.0.0.1:8000/en/doc/Hardware/Bricklets/Industrial_Counter.html#duty-cycle-prescaler-and-frequency-integration-time>`__
  für weitere Details.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Counter Configuration',
'elements': [('Channel', 'uint8', 1, 'in', CONSTANT_CHANNEL),
             ('Count Edge', 'uint8', 1, 'out', CONSTANT_COUNT_EDGE),
             ('Count Direction', 'uint8', 1, 'out', CONSTANT_COUNT_DIRECTON),
             ('Duty Cycle Prescaler', 'uint8', 1, 'out', CONSTANT_DUTY_CYCLE_PRESCALER),
             ('Frequency Integration Time', 'uint8', 1, 'out', CONSTANT_FREQUENCY_INTEGRATION_TIME)],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the counter configuration as set by :func:`Set Counter Configuration`.
""",
'de':
"""
Gibt die Zähler-Konfiguration zurück, wie Sie mittels :func:`Set Counter Configuration` gesetzt wurde.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set All Counter Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period in ms is the period with which the :cb:`All Counter`
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
Die Periode in ms ist die Periode mit der der :cb:`All Counter`
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
'name': 'Get All Counter Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set All Counter Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set All Counter Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set All Signal Data Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period in ms is the period with which the :cb:`All Signal Data`
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
Die Periode in ms ist die Periode mit der der :cb:`All Signal Data`
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
'name': 'Get All Signal Data Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set All Signal Data Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set All Signal Data Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Channel LED Config',
'elements': [('Channel', 'uint8', 1, 'in', CONSTANT_CHANNEL),
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
'elements': [('Channel', 'uint8', 1, 'in', CONSTANT_CHANNEL),
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
'name': 'All Counter',
'elements': [('Counter', 'int64', 4, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set All Counter Callback Configuration`.

The `parameters` are the same as :func:`Get All Counter`.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set All Counter Callback Configuration` gesetzten Konfiguration

Die `parameters` sind der gleiche wie :func:`Get All Counter`.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'All Signal Data',
'elements': [('Duty Cycle', 'uint16', 4, 'out'),
             ('Period', 'uint64', 4, 'out'),
             ('Frequency', 'uint32', 4, 'out'),
             ('Channel Value', 'bool', 4, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set All Signal Data Callback Configuration`.

The `parameters` are the same as :func:`Get All Signal Data`.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set All Signal Data Callback Configuration` gesetzten Konfiguration

Die `parameters` sind der gleiche wie :func:`Get All Signal Data`.
"""
}]
})
