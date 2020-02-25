# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# IO-4 Bricklet communication config

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'category': 'Bricklet',
    'device_identifier': 29,
    'name': 'IO4',
    'display_name': 'IO-4',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '4-channel digital input/output',
        'de': '4 digitale Ein- und Ausgänge'
    },
    'released': True,
    'documented': True,
    'discontinued': True, # replaced by IO-4 Bricklet 2.0
    'features': [
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append({
'name': 'Direction',
'type': 'char',
'constants': [('In', 'i'),
              ('Out', 'o')]
})

com['constant_groups'].append({
'name': 'Edge Type',
'type': 'uint8',
'constants': [('Rising', 0),
              ('Falling', 1),
              ('Both', 2)]
})

com['packets'].append({
'type': 'function',
'name': 'Set Value',
'elements': [('Value Mask', 'uint8', 1, 'in', {'range': (0, 15)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the output value (high or low) with a bitmask (4bit). A 1 in the bitmask
means high and a 0 in the bitmask means low.

For example: The value 3 or 0b0011 will turn the pins 0-1 high and the
pins 2-3 low.

All running monoflop timers will be aborted if this function is called.

.. note::
 This function does nothing for pins that are configured as input.
 Pull-up resistors can be switched on with :func:`Set Configuration`.
""",
'de':
"""
Setzt den Ausgangszustand (logisch 1 oder logisch 0) mittels einer Bitmaske
(4Bit). Eine 1 in der Bitmaske bedeutet logisch 1 und eine 0 in der Bitmaske
bedeutet logisch 0.

Beispiel: Der Wert 3 bzw. 0b0011 setzt die Pins 0-1 auf logisch 1 und die
Pins 2-3 auf logisch 0.

Alle laufenden Monoflop Timer werden abgebrochen, wenn diese Funktion aufgerufen
wird.

.. note::
 Diese Funktion bewirkt keine Änderung an Pins die als Eingang konfiguriert sind.
 Pull-Up Widerstände können mit :func:`Set Configuration` zugeschaltet werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Value',
'elements': [('Value Mask', 'uint8', 1, 'out', {'range': (0, 15)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns a bitmask of the values that are currently measured.
This function works if the pin is configured to input
as well as if it is configured to output.
""",
'de':
"""
Gibt eine Bitmaske der aktuell gemessenen Zustände zurück.
Diese Funktion gibt die Zustände aller Pins zurück, unabhängig ob diese als
Ein- oder Ausgang konfiguriert sind.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('Selection Mask', 'uint8', 1, 'in', {'range': (0, 15)}),
             ('Direction', 'char', 1, 'in', {'constant_group': 'Direction', 'default': 'i'}),
             ('Value', 'bool', 1, 'in', {'default': True})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Configures the value and direction of the specified pins. Possible directions
are 'i' and 'o' for input and output.

If the direction is configured as output, the value is either high or low
(set as *true* or *false*).

If the direction is configured as input, the value is either pull-up or
default (set as *true* or *false*).

For example:

* (15, 'i', true) or (0b1111, 'i', true) will set all pins of as input pull-up.
* (8, 'i', false) or (0b1000, 'i', false) will set pin 3 of as input default (floating if nothing is connected).
* (3, 'o', false) or (0b0011, 'o', false) will set pins 0 and 1 as output low.
* (4, 'o', true) or (0b0100, 'o', true) will set pin 2 of as output high.

Running monoflop timers for the specified pins will be aborted if this
function is called.
""",
'de':
"""
Konfiguriert den Zustand und die Richtung eines angegebenen Pins. Mögliche
Richtungen sind 'i' und 'o' für Ein- und Ausgang.

Wenn die Richtung als Ausgang konfiguriert ist, ist der Zustand entweder
logisch 1 oder logisch 0 (gesetzt als *true* oder *false*).

Wenn die Richtung als Eingang konfiguriert ist, ist der Zustand entweder
Pull-Up oder Standard (gesetzt als *true* oder *false*).

Beispiele:

* (15, 'i', true) bzw. (0b1111, 'i', true) setzt alle Pins als Eingang mit Pull-Up.
* (8, 'i', false) bzw. (0b1000, 'i', false) setzt Pin 3 als Standard Eingang (potentialfrei wenn nicht verbunden).
* (3, 'o', false) bzw. (0b0011, 'o', false) setzt die Pins 0 und 1 als Ausgang im Zustand logisch 0.
* (4, 'o', true) bzw. (0b0100, 'o', true) setzt Pin 2 als Ausgang im Zustand logisch 1.

Laufende Monoflop Timer für die angegebenen Pins werden abgebrochen, wenn
diese Funktion aufgerufen wird.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Direction Mask', 'uint8', 1, 'out', {'range': (0, 15)}),
             ('Value Mask', 'uint8', 1, 'out', {'range': (0, 15)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns a value bitmask and a direction bitmask. A 1 in the direction bitmask
means input and a 0 in the bitmask means output.

For example: A return value of (3, 5) or (0b0011, 0b0101) for direction and
value means that:

* pin 0 is configured as input pull-up,
* pin 1 is configured as input default,
* pin 2 is configured as output high and
* pin 3 is are configured as output low.
""",
'de':
"""
Gibt eine Bitmaske für die Richtung und eine Bitmaske für den Zustand der Pins
zurück. Eine 1 in der Bitmaske für die Richtung bedeutet Eingang und eine 0
in der Bitmaske bedeutet Ausgang.

Beispiel: Ein Rückgabewert von (3, 5) bzw. (0b0011, 0b0101) für Richtung und
Zustand bedeutet:

* Pin 0 ist als Eingang mit Pull-Up konfiguriert,
* Pin 1 ist als Standard Eingang konfiguriert,
* Pin 2 ist als Ausgang im Zustand logisch 1 konfiguriert und
* Pin 3 ist als Ausgang im Zustand logisch 0 konfiguriert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Debounce Period',
'elements': [('Debounce', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 100})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the debounce period of the :cb:`Interrupt` callback.

For example: If you set this value to 100, you will get the interrupt
maximal every 100ms. This is necessary if something that bounces is
connected to the IO-4 Bricklet, such as a button.
""",
'de':
"""
Setzt die Entprellperiode der :cb:`Interrupt` Callback.

Beispiel: Wenn dieser Wert auf 100 gesetzt wird, erhält man den Interrupt
maximal alle 100ms. Dies ist notwendig falls etwas prellendes an
das IO-4 Bricklet angeschlossen ist, wie z.B. eine Taste.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Debounce Period',
'elements': [('Debounce', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 100})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the debounce period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Gibt die Entprellperiode zurück, wie von :func:`Set Debounce Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Interrupt',
'elements': [('Interrupt Mask', 'uint8', 1, 'in', {'range': (0, 15)})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the pins on which an interrupt is activated with a bitmask.
Interrupts are triggered on changes of the voltage level of the pin,
i.e. changes from high to low and low to high.

For example: An interrupt bitmask of 10 or 0b1010 will enable the interrupt for
pins 1 and 3.

The interrupt is delivered with the :cb:`Interrupt` callback.
""",
'de':
"""
Setzt durch eine Bitmaske die Pins für welche der Interrupt aktiv ist.
Interrupts werden ausgelöst bei Änderung des Spannungspegels eines Pins,
z.B. ein Wechsel von logisch 1 zu logisch 0 und logisch 0 zu logisch 1.

Beispiel: Eine Interrupt Bitmaske von 10 bzw. 0b1010 aktiviert den Interrupt für
die Pins 1 und 3.

Der Interrupt wird mit dem :cb:`Interrupt` Callback zugestellt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Interrupt',
'elements': [('Interrupt Mask', 'uint8', 1, 'out', {'range': (0, 15)})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the interrupt bitmask as set by :func:`Set Interrupt`.
""",
'de':
"""
Gibt die Interrupt Bitmaske zurück, wie von :func:`Set Interrupt` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Interrupt',
'elements': [('Interrupt Mask', 'uint8', 1, 'out', {'range': (0, 15)}),
             ('Value Mask', 'uint8', 1, 'out', {'range': (0, 15)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered whenever a change of the voltage level is detected
on pins where the interrupt was activated with :func:`Set Interrupt`.

The values are a bitmask that specifies which interrupts occurred
and the current value bitmask.

For example:

* (1, 1) or (0b0001, 0b0001) means that an interrupt on pin 0 occurred and
  currently pin 0 is high and pins 1-3 are low.
* (9, 14) or (0b1001, 0b1110) means that interrupts on pins 0 and 3
  occurred and currently pin 0 is low and pins 1-3 are high.
""",
'de':
"""
Dieser Callback wird ausgelöst sobald eine Änderung des Spannungspegels
detektiert wird, an Pins für welche der Interrupt mit :func:`Set Interrupt`
aktiviert wurde.

Die Rückgabewerte sind eine Bitmaske der aufgetretenen Interrupts und der
aktuellen Zustände.

Beispiele:

* (1, 1) bzw. (0b0001, 0b0001) bedeutet, dass ein Interrupt am Pin 0 aufgetreten
  ist und aktuell Pin 0 logisch 1 ist und die Pins 1-3 logisch 0 sind.
* (9, 14) bzw. (0b1001, 0b1110) bedeutet, dass Interrupts an den Pins 0 und 3
  aufgetreten sind und aktuell Pin 0 logisch 0 ist und die Pins 1-3 logisch 1 sind.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Monoflop',
'elements': [('Selection Mask', 'uint8', 1, 'in', {'range': (0, 15)}),
             ('Value Mask', 'uint8', 1, 'in', {'range': (0, 15)}),
             ('Time', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [1, 1, 1],
'doc': ['af', {
'en':
"""
Configures a monoflop of the pins specified by the first parameter as 4 bit
long bitmask. The specified pins must be configured for output. Non-output
pins will be ignored.

The second parameter is a bitmask with the desired value of the specified
output pins. A 1 in the bitmask means high and a 0 in the bitmask means low.

The third parameter indicates the time that the pins should hold
the value.

If this function is called with the parameters (9, 1, 1500) or
(0b1001, 0b0001, 1500): Pin 0 will get high and pin 3 will get low. In 1.5s pin
0 will get low and pin 3 will get high again.

A monoflop can be used as a fail-safe mechanism. For example: Lets assume you
have a RS485 bus and an IO-4 Bricklet connected to one of the slave
stacks. You can now call this function every second, with a time parameter
of two seconds and pin 0 set to high. Pin 0 will be high all the time. If now
the RS485 connection is lost, then pin 0 will get low in at most two seconds.
""",
'de':
"""
Konfiguriert einen Monoflop für die Pins, wie mittels der 4 Bit langen Bitmaske
des ersten Parameters festgelegt. Die festgelegten Pins müssen als Ausgänge
konfiguriert sein. Als Eingänge konfigurierte Pins werden ignoriert.

Der zweite Parameter ist eine Bitmaske mit den gewünschten Zustanden der
festgelegten Ausgangspins. Eine 1 in der Bitmaske bedeutet logisch 1 und
eine 0 in der Bitmaske bedeutet logisch 0.

Der dritte Parameter stellt die Zeit dar, welche die Pins den Zustand
halten sollen.

Wenn diese Funktion mit den Parametern (9, 1, 1500) bzw. (0b1001, 0b0001, 1500)
aufgerufen wird: Pin 0 wird auf logisch 1 und Pin 3 auf logisch 0 gesetzt.
Nach 1,5s wird Pin 0 wieder logisch 0 und Pin 3 logisch 1 gesetzt.

Ein Monoflop kann zur Ausfallsicherung verwendet werden. Beispiel:
Angenommen ein RS485 Bus und ein IO-4 Bricklet ist an ein Slave Stapel verbunden.
Jetzt kann diese Funktion sekündlich, mit einem Zeitparameter von 2 Sekunden,
aufgerufen werden. Der Pin wird die gesamte Zeit im Zustand logisch 1 sein.
Wenn jetzt die RS485 Verbindung getrennt wird, wird der Pin nach spätestens zwei
Sekunden in den Zustand logisch 0 wechseln.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Monoflop',
'elements': [('Pin', 'uint8', 1, 'in', {'range': (0, 3)}),
             ('Value', 'uint8', 1, 'out', {'range': (0, 1)}),
             ('Time', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'}),
             ('Time Remaining', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [1, 1, 1],
'doc': ['af', {
'en':
"""
Returns (for the given pin) the current value and the time as set by
:func:`Set Monoflop` as well as the remaining time until the value flips.

If the timer is not running currently, the remaining time will be returned
as 0.
""",
'de':
"""
Gibt (für den angegebenen Pin) den aktuellen Zustand und die Zeit, wie von
:func:`Set Monoflop` gesetzt, sowie die noch verbleibende Zeit bis zum
Zustandswechsel, zurück.

Wenn der Timer aktuell nicht läuft, ist die noch verbleibende Zeit 0.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Monoflop Done',
'elements': [('Selection Mask', 'uint8', 1, 'out', {'range': (0, 15)}),
             ('Value Mask', 'uint8', 1, 'out', {'range': (0, 15)})],
'since_firmware': [1, 1, 1],
'doc': ['c', {
'en':
"""
This callback is triggered whenever a monoflop timer reaches 0. The
:word:`parameters` contain the involved pins and the current value of the pins
(the value after the monoflop).
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn ein Monoflop Timer abläuft (0 erreicht).
:word:`parameters` enthalten die beteiligten Pins als Bitmaske und den aktuellen
Zustand als Bitmaske (der Zustand nach dem Monoflop).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Selected Values',
'elements': [('Selection Mask', 'uint8', 1, 'in', {'range': (0, 15)}),
             ('Value Mask', 'uint8', 1, 'in', {'range': (0, 15)})],
'since_firmware': [2, 0, 0],
'doc': ['af', {
'en':
"""
Sets the output value (high or low) with a bitmask, according to
the selection mask. The bitmask is 4 bit long, *true* refers to high
and *false* refers to low.

For example: The parameters (9, 4) or (0b0110, 0b0100) will turn
pin 1 low and pin 2 high, pin 0 and 3 will remain untouched.

Running monoflop timers for the selected pins will be aborted if this
function is called.

.. note::
 This function does nothing for pins that are configured as input.
 Pull-up resistors can be switched on with :func:`Set Configuration`.
""",
'de':
"""
Setzt den Ausgangszustand (logisch 1 oder logisch 0) mittels einer Bitmaske,
entsprechend der Selektionsmaske. Die Bitmaske hat eine Länge von 4 Bit,
*true* bedeutet logisch 1 und *false*
logisch 0.

Beispiel: Die Parameter (9, 4) bzw (0b0110, 0b0100) setzen den Pin 1 auf
logisch 0 und den Pin 2 auf logisch 1. Die Pins 0 und 3 bleiben unangetastet.

Laufende Monoflop Timer für die ausgewählten Pins werden abgebrochen, wenn
diese Funktion aufgerufen wird.

.. note::
 Diese Funktion bewirkt keine Änderung an Pins die als Eingang konfiguriert sind.
 Pull-Up Widerstände können mit :func:`Set Configuration` zugeschaltet werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Edge Count',
'elements': [('Pin', 'uint8', 1, 'in', {'range': (0, 3)}),
             ('Reset Counter', 'bool', 1, 'in', {}),
             ('Count', 'uint32', 1, 'out', {})],
'since_firmware': [2, 0, 1],
'doc': ['bf', {
'en':
"""
Returns the current value of the edge counter for the selected pin. You can
configure the edges that are counted with :func:`Set Edge Count Config`.

If you set the reset counter to *true*, the count is set back to 0
directly after it is read.
""",
'de':
"""
Gibt den aktuellen Wert des Flankenzählers für den ausgewählten Pin zurück. Die
zu zählenden Flanken können mit :func:`Set Edge Count Config` konfiguriert werden.

Wenn reset counter auf *true* gesetzt wird, wird der Zählerstand direkt
nach dem auslesen auf 0 zurückgesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Edge Count Config',
'elements': [('Selection Mask', 'uint8', 1, 'in', {'range': (0, 15)}),
             ('Edge Type', 'uint8', 1, 'in', {'constant_group': 'Edge Type', 'default': 0}),
             ('Debounce', 'uint8', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 100})],
'since_firmware': [2, 0, 1],
'doc': ['af', {
'en':
"""
Configures the edge counter for the selected pins.

The edge type parameter configures if rising edges, falling edges or
both are counted if the pin is configured for input. Possible edge types are:

* 0 = rising (default)
* 1 = falling
* 2 = both

Configuring an edge counter resets its value to 0.

If you don't know what any of this means, just leave it at default. The
default configuration is very likely OK for you.
""",
'de':
"""
Konfiguriert den Flankenzähler für die ausgewählten Pins.

Der edge type Parameter konfiguriert den zu zählenden Flankentyp. Es können
steigende, fallende oder beide Flanken gezählt werden für Pins die als Eingang
konfiguriert sind. Mögliche Flankentypen sind:

* 0 = steigend (Standard)
* 1 = fallend
* 2 = beide

Durch das Konfigurieren wird der Wert des Flankenzählers auf 0 zurückgesetzt.

Falls unklar ist was dies alles bedeutet, kann diese Funktion einfach
ignoriert werden. Die Standardwerte sind in fast allen Situationen OK.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Edge Count Config',
'elements': [('Pin', 'uint8', 1, 'in', {'range': (0, 3)}),
             ('Edge Type', 'uint8', 1, 'out', {'constant_group': 'Edge Type', 'default': 0}),
             ('Debounce', 'uint8', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 100})],
'since_firmware': [2, 0, 1],
'doc': ['af', {
'en':
"""
Returns the edge type and debounce time for the selected pin as set by
:func:`Set Edge Count Config`.
""",
'de':
"""
Gibt den Flankentyp sowie die Entprellzeit für den ausgewählten Pin zurück,
wie von :func:`Set Edge Count Config` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Input',
'functions': [('getter', ('Get Value', 'value as bitmask'), [(('Value Mask', 'Value Mask'), 'uint8:bitmask:4', 1, None, None, None)], [])]
})

com['examples'].append({
'name': 'Output',
'functions': [('setter', 'Set Configuration', [('uint8:bitmask:4', 1 << 1), ('char', 'o'), ('bool', False)], 'Set pin 1 to output low', None),
              ('setter', 'Set Configuration', [('uint8:bitmask:4', (1 << 2) | (1 << 3)), ('char', 'o'), ('bool', True)], 'Set pin 2 and 3 to output high', None)]
})

com['examples'].append({
'name': 'Interrupt',
'functions': [('callback', ('Interrupt', 'interrupt'), [(('Interrupt Mask', 'Interrupt Mask'), 'uint8:bitmask:4', 1, None, None, None), (('Value Mask', 'Value Mask'), 'uint8:bitmask:4', 1, None, None, None)], None, None),
              ('setter', 'Set Interrupt', [('uint8:bitmask:4', 1 << 0)], 'Enable interrupt on pin 0', None)]
})


def input_channel(idx):
    return {
            'predicate': 'cfg.pinConfiguration{} > 1'.format(idx),
            'id': 'Input Pin {}'.format(idx),
            'label': 'Input Value Pin {}'.format(idx),

            'type': 'Input Pin',

            'getters': [{
                'packet': 'Get Value',
                'transform': '(value & (1 << {})) > 0 ? OnOffType.ON : OnOffType.OFF'.format(idx)}],

            'callbacks': [{
                'filter': '(interruptMask & (1 << {})) > 0'.format(idx),
                'packet': 'Interrupt',
                'transform': '(valueMask & (1 << {})) > 0 ? OnOffType.ON : OnOffType.OFF'.format(idx)}],

            'init_code':"""this.setInterrupt((short)(this.getInterrupt() | (1 << {idx})));
            this.setConfiguration((short)(1 << {idx}), 'i', cfg.pinConfiguration{idx} % 2 == 1);""".format(idx=idx),
            'dispose_code': """this.setInterrupt((short)(this.getInterrupt() & ~(1 << {idx})));""".format(idx=idx),
    }

def output_channel(idx):
    return {
            'predicate': 'cfg.pinConfiguration{} <= 1'.format(idx),
            'id': 'Output Pin {}'.format(idx),
            'label': 'Output Value Pin {}'.format(idx),

            'type': 'Output Pin',

            'getters': [{
                'packet': 'Get Value',
                'transform': '(value & (1 << {})) > 0 ? OnOffType.ON : OnOffType.OFF'.format(idx)}],

            'setters': [{
                'packet': 'Set Selected Values',
                'packet_params': ['(short)(1 << {})'.format(idx), 'cmd == OnOffType.ON ? (short)0xFF : (short)0'],
                'command_type': "OnOffType",
            }],


            'callbacks': [{
                'packet': 'Monoflop Done',
                'filter': '(selectionMask & (1 << {})) > 0'.format(idx),
                'transform': '(valueMask & (1 << {})) > 0 ? OnOffType.ON : OnOffType.OFF'.format(idx)}],

            'init_code':"""this.setConfiguration((short)(1 << {idx}), 'o', cfg.pinConfiguration{idx} % 2 == 1);""".format(idx=idx),
    }

def monoflop_channel(idx):
    return {
        'predicate': 'cfg.pinConfiguration{} <= 1'.format(idx),
        'id': 'Monoflop Pin {}'.format(idx),
        'label': 'Monoflop Pin {}'.format(idx),
        'type': 'Monoflop',

        'getters': [{
            'packet': 'Get Monoflop',
            'packet_params': ['(short){}'.format(idx)],
            'transform': 'value.value > 0 ? OnOffType.ON : OnOffType.OFF'}],

        'setters': [{
            'packet': 'Set Monoflop',
            'packet_params': ['(short)(1 << {})'.format(idx), 'channelCfg.monoflopValue.booleanValue() ? (short)0xFF : (short)0', 'channelCfg.monoflopDuration.longValue()'],
            'command_type': "StringType", # Command type has to be string type to be able to use command options.
        }],

        'setter_refreshs': [{
            'channel': 'Output Pin {}'.format(idx),
            'delay': '0'
        }]
    }


def edge_count_channel(index):
    return {
            'predicate': 'cfg.pinConfiguration{} > 1'.format(index),
            'id': 'Edge Count Pin {0}'.format(index),
            'type': 'Edge Count',
            'label': 'Edge Count Pin {0}'.format(index),

            'init_code':"""this.setEdgeCountConfig((short)(1 << {}), channelCfg.edgeType.shortValue(), channelCfg.debounce.shortValue());""".format(index),

            'getters': [{
                'packet': 'Get Edge Count',
                'packet_params': ['(short){}'.format(index), 'channelCfg.resetOnRead'],
                'transform': 'new QuantityType<>(value, {unit})'}],

            'java_unit': 'SmartHomeUnits.ONE',
            'is_trigger_channel': False
        }

def pin_config(idx):
    return {
            'virtual': True,
            'name': 'Pin Configuration {}'.format(idx),
            'type': 'integer',
            'options': [
                ('Input with pull-up', 3),
                ('Input without pull-up', 2),
                ('Output (Initial high)', 1),
                ('Output (Initial low)', 0)
            ],
            'limitToOptions': 'true',
            'default': 3,

            'label': 'Pin Configuration {}'.format(idx),
            'description': 'Configures the direction of pin {}. Inputs without pull-up will be floating if nothing is connected. Outputs can have an initial state of low or high.'.format(idx),
        }

channels = [input_channel(i) for i in range(0, 4)] + [output_channel(i) for i in range(0, 4)] + [monoflop_channel(i) for i in range(0, 4)] + [edge_count_channel(i) for i in range(0, 4)]
params = [pin_config(i) for i in range(0, 4)]

com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.OnOffType', 'org.eclipse.smarthome.core.library.types.StringType'],
    'params': params,
    'channels': channels,
    'channel_types': [
        oh_generic_channel_type('Input Pin', 'Switch', 'Input Value',
                    update_style=None,
                    description='The logic level that is currently measured on the pin.',
                    read_only=True),
        oh_generic_channel_type('Output Pin', 'Switch', 'Output Value',
                    update_style=None,
                    description='The logic level that is currently set on the pin.',
                    read_only=False),
        {
            'id': 'Monoflop',
            'item_type': 'String',
            'params': [{
                'packet': 'Set Monoflop',
                'element': 'Time',

                'name': 'Monoflop Duration',
                'type': 'integer',
                'default': 1000,
                'min': 0,
                'max': '4294967295L',
                'unit': 'ms',

                'label': 'Monoflop Duration',
                'description': 'The time (in ms) that the pin should hold the configured value.',
            },
            {
                'packet': 'Set Monoflop',
                'element': 'Value Mask',

                'name': 'Monoflop Value',
                'type': 'boolean',
                'default': 'true',

                'label': 'Monoflop Value',
                'description': 'The desired value of the specified channel. Activated means relay closed and Deactivated means relay open.',
            }],
            'label': 'NOT USED',
            'description':'Triggers a monoflop as configured',
            'command_options': [('Trigger', 'TRIGGER')]
        },
        oh_generic_channel_type('Edge Count', 'Number:Dimensionless', 'Edge Count',
            update_style=None,
            description='The current value of the edge counter for the selected channel',
            read_only=True,
            params=[{
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
            },{
                'packet': 'Set Debounce Period',
                'element': 'Debounce',

                'name': 'Debounce',
                'type': 'integer',

                'default': 100,

                'label': 'Debounce Time',
                'description': 'The debounce time in ms.',
            },{
                'packet': 'Get Edge Count',
                'element': 'Reset Counter',

                'name': 'Reset On Read',
                'type': 'boolean',

                'default': 'false',

                'label': 'Reset Edge Count On Update',
                'description': 'Enabling this will reset the edge counter after OpenHAB reads its value. Use this if you want relative edge counts per update.',
            }])
    ],
    'actions': [{'fn': 'Set Value', 'refreshs': ['Output Pin 0', 'Output Pin 1', 'Output Pin 2', 'Output Pin 3', 'Monoflop Pin 0', 'Monoflop Pin 1', 'Monoflop Pin 2', 'Monoflop Pin 3']},
                {'fn': 'Set Selected Values', 'refreshs': ['Output Pin 0', 'Output Pin 1', 'Output Pin 2', 'Output Pin 3', 'Monoflop Pin 0', 'Monoflop Pin 1', 'Monoflop Pin 2', 'Monoflop Pin 3']},
                {'fn': 'Set Monoflop', 'refreshs': ['Output Pin 0', 'Output Pin 1', 'Output Pin 2', 'Output Pin 3', 'Monoflop Pin 0', 'Monoflop Pin 1', 'Monoflop Pin 2', 'Monoflop Pin 3']},
                'Get Value', 'Get Configuration',
                {'fn': 'Get Edge Count', 'refreshs': ['Edge Count Pin 0', 'Edge Count Pin 1', 'Edge Count Pin 2', 'Edge Count Pin 3']},
                'Get Monoflop', 'Get Edge Count Config']
}
