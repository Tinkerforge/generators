# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# IO-16 Bricklet communication config

from commonconstants import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'category': 'Bricklet',
    'device_identifier': 28,
    'name': 'IO16',
    'display_name': 'IO-16',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '16-channel digital input/output',
        'de': '16 digitale Ein- und Ausgänge'
    },
    'released': True,
    'documented': True,
    'discontinued': False, # selling remaining stock, replaced by IO-16 Bricklet 2.0
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
'name': 'Set Port',
'elements': [('Port', 'char', 1, 'in'),
             ('Value Mask', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the output value (high or low) for a port ("a" or "b") with a bitmask
(8bit). A 1 in the bitmask means high and a 0 in the bitmask means low.

For example: The value 15 or 0b00001111 will turn the pins 0-3 high and the
pins 4-7 low for the specified port.

All running monoflop timers of the given port will be aborted if this function
is called.

.. note::
 This function does nothing for pins that are configured as input.
 Pull-up resistors can be switched on with :func:`Set Port Configuration`.
""",
'de':
"""
Setzt den Ausgangszustand (logisch 1 oder logisch 0) für einen Port ("a" oder
"b") mittels einer Bitmaske (8Bit). Eine 1 in der Bitmaske bedeutet logisch 1
und eine 0 in der Bitmaske bedeutet logisch 0.

Beispiel: Der Wert 15 bzw. 0b00001111 setzt die Pins 0-3 auf logisch 1 und die
Pins 4-7 auf logisch 0.

Alle laufenden Monoflop Timer für den angegebenen Port werden abgebrochen, wenn
diese Funktion aufgerufen wird.

.. note::
 Diese Funktion bewirkt keine Änderung an Pins die als Eingang konfiguriert sind.
 Pull-Up Widerstände können mit :func:`Set Port Configuration` zugeschaltet werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Port',
'elements': [('Port', 'char', 1, 'in'),
             ('Value Mask', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns a bitmask of the values that are currently measured on the
specified port. This function works if the pin is configured to input
as well as if it is configured to output.
""",
'de':
"""
Gibt eine Bitmaske der aktuell gemessenen Zustände des gewählten Ports zurück.
Diese Funktion gibt die Zustände aller Pins zurück, unabhängig ob diese als
Ein- oder Ausgang konfiguriert sind.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Port Configuration',
'elements': [('Port', 'char', 1, 'in'),
             ('Selection Mask', 'uint8', 1, 'in'),
             ('Direction', 'char', 1, 'in', {'constant_group': 'Direction'}),
             ('Value', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Configures the value and direction of a specified port. Possible directions
are 'i' and 'o' for input and output.

If the direction is configured as output, the value is either high or low
(set as *true* or *false*).

If the direction is configured as input, the value is either pull-up or
default (set as *true* or *false*).

For example:

* ('a', 255, 'i', true) or ('a', 0b11111111, 'i', true) will set all pins of port A as input pull-up.
* ('a', 128, 'i', false) or ('a', 0b10000000, 'i', false) will set pin 7 of port A as input default (floating if nothing is connected).
* ('b', 3, 'o', false) or ('b', 0b00000011, 'o', false) will set pins 0 and 1 of port B as output low.
* ('b', 4, 'o', true) or ('b', 0b00000100, 'o', true) will set pin 2 of port B as output high.

Running monoflop timers for the selected pins will be aborted if this
function is called.

The default configuration is input with pull-up.
""",
'de':
"""
Konfiguriert den Zustand und die Richtung des angegebenen Ports. Mögliche
Richtungen sind 'i' und 'o' für Ein- und Ausgang.

Wenn die Richtung als Ausgang konfiguriert ist, ist der Zustand entweder
logisch 1 oder logisch 0 (gesetzt als *true* oder *false*).

Wenn die Richtung als Eingang konfiguriert ist, ist der Zustand entweder
Pull-Up oder Standard (gesetzt als *true* oder *false*).

Beispiele:

* ('a', 255, 'i', true) bzw. ('a', 0b11111111, 'i', true) setzt alle Pins des Ports a als Eingang mit Pull-Up.
* ('a', 128, 'i', false) bzw. ('a', 0b10000000, 'i', false) setzt Pin 7 des Ports A als Standard Eingang (potentialfrei wenn nicht verbunden).
* ('b', 3, 'o', false) bzw. ('b', 0b00000011, 'o', false) setzt die Pins 0 und 1 des Ports B als Ausgang im Zustand logisch 0.
* ('b', 4, 'o', true) bzw. ('b', 0b00000100, 'o', true) setzt Pin 2 des Ports B als Ausgang im Zustand logisch 1.

Laufende Monoflop Timer für die ausgewählten Pins werden abgebrochen, wenn
diese Funktion aufgerufen wird.

Die Standardkonfiguration ist Eingang mit Pull-Up.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Port Configuration',
'elements': [('Port', 'char', 1, 'in'),
             ('Direction Mask', 'uint8', 1, 'out'),
             ('Value Mask', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns a direction bitmask and a value bitmask for the specified port. A 1 in
the direction bitmask means input and a 0 in the bitmask means output.

For example: A return value of (15, 51) or (0b00001111, 0b00110011) for
direction and value means that:

* pins 0 and 1 are configured as input pull-up,
* pins 2 and 3 are configured as input default,
* pins 4 and 5 are configured as output high
* and pins 6 and 7 are configured as output low.
""",
'de':
"""
Gibt eine Bitmaske für die Richtung und eine Bitmaske für den Zustand der Pins
des gewählten Ports zurück. Eine 1 in der Bitmaske für die Richtung bedeutet
Eingang und eine 0 in der Bitmaske bedeutet Ausgang.

Beispiel: Ein Rückgabewert von (15, 51) bzw. (0b00001111, 0b00110011) für
Richtung und Zustand bedeutet:

* Pin 0 und 1 sind als Eingang mit Pull-Up konfiguriert,
* Pin 2 und 3 sind als Standard Eingang konfiguriert,
* Pin 4 und 5 sind als Ausgang im Zustand logisch 1 konfiguriert
* und Pin 6 und 7 sind als Ausgang im Zustand logisch 0 konfiguriert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Debounce Period',
'elements': [('Debounce', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the debounce period of the :cb:`Interrupt` callback in ms.

For example: If you set this value to 100, you will get the interrupt
maximal every 100ms. This is necessary if something that bounces is
connected to the IO-16 Bricklet, such as a button.

The default value is 100.
""",
'de':
"""
Setzt die Entprellperiode der :cb:`Interrupt` Callback in ms.

Beispiel: Wenn dieser Wert auf 100 gesetzt wird, erhält man den Interrupt
maximal alle 100ms. Dies ist notwendig falls etwas prellendes an
das IO-16 Bricklet angeschlossen ist, wie z.B. eine Taste.

Der Standardwert ist 100.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Debounce Period',
'elements': [('Debounce', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the debounce period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Gibt die Entprellperiode zurück, wie von :func:`Set Debounce Period`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Port Interrupt',
'elements': [('Port', 'char', 1, 'in'),
             ('Interrupt Mask', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the pins on which an interrupt is activated with a bitmask.
Interrupts are triggered on changes of the voltage level of the pin,
i.e. changes from high to low and low to high.

For example: ('a', 129) or ('a', 0b10000001) will enable the interrupt for
pins 0 and 7 of port a.

The interrupt is delivered with the :cb:`Interrupt` callback.
""",
'de':
"""
Setzt durch eine Bitmaske die Pins für welche der Interrupt aktiv ist.
Interrupts werden ausgelöst bei Änderung des Spannungspegels eines Pins,
z.B. ein Wechsel von logisch 1 zu logisch 0 und logisch 0 zu logisch 1.

Beispiel: ('a', 129) bzw. ('a', 0b10000001) aktiviert den Interrupt für die
Pins 0 und 7 des Ports a.

Der Interrupt wird mit dem :cb:`Interrupt` Callback zugestellt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Port Interrupt',
'elements': [('Port', 'char', 1, 'in'),
             ('Interrupt Mask', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the interrupt bitmask for the specified port as set by
:func:`Set Port Interrupt`.
""",
'de':
"""
Gibt die Interrupt Bitmaske für den angegebenen Port zurück, wie von
:func:`Set Port Interrupt` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Interrupt',
'elements': [('Port', 'char', 1, 'out'),
             ('Interrupt Mask', 'uint8', 1, 'out'),
             ('Value Mask', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered whenever a change of the voltage level is detected
on pins where the interrupt was activated with :func:`Set Port Interrupt`.

The values are the port, a bitmask that specifies which interrupts occurred
and the current value bitmask of the port.

For example:

* ('a', 1, 1) or ('a', 0b00000001, 0b00000001) means that on port A an
  interrupt on pin 0 occurred and currently pin 0 is high and pins 1-7 are low.
* ('b', 129, 254) or ('b', 0b10000001, 0b11111110) means that on port B
  interrupts on pins 0 and 7 occurred and currently pin 0 is low and pins 1-7
  are high.
""",
'de':
"""
Dieser Callback wird ausgelöst sobald eine Änderung des Spannungspegels
detektiert wird, an Pins für welche der Interrupt mit :func:`Set Port Interrupt`
aktiviert wurde.

Die Rückgabewerte sind der Port, eine Bitmaske der aufgetretenen Interrupts und
der aktuellen Zustände des Ports.

Beispiele:

* ('a', 1, 1) bzw. ('a', 0b00000001, 0b00000001) bedeutet, dass an Port A ein
  Interrupt am Pin 0 aufgetreten ist und aktuell ist Pin 0 logisch 1 und die
  Pins 1-7 sind logisch 0.
* ('b', 129, 254) bzw. ('b', 0b10000001, 0b11111110) bedeutet, dass an Port B
  Interrupts an den Pins 0 und 7 aufgetreten sind und aktuell ist Pin 0 logisch
  0 und die Pins 1-7 sind logisch 1.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Port Monoflop',
'elements': [('Port', 'char', 1, 'in'),
             ('Selection Mask', 'uint8', 1, 'in'),
             ('Value Mask', 'uint8', 1, 'in'),
             ('Time', 'uint32', 1, 'in')],
'since_firmware': [1, 1, 2],
'doc': ['af', {
'en':
"""
Configures a monoflop of the pins specified by the second parameter as 8 bit
long bitmask. The specified pins must be configured for output. Non-output
pins will be ignored.

The third parameter is a bitmask with the desired value of the specified
output pins. A 1 in the bitmask means high and a 0 in the bitmask means low.

The forth parameter indicates the time (in ms) that the pins should hold
the value.

If this function is called with the parameters ('a', 9, 1, 1500) or
('a', 0b00001001, 0b00000001, 1500): Pin 0 will get high and pin 3 will get
low on port 'a'. In 1.5s pin 0 will get low and pin 3 will get high again.

A monoflop can be used as a fail-safe mechanism. For example: Lets assume you
have a RS485 bus and an IO-16 Bricklet connected to one of the slave
stacks. You can now call this function every second, with a time parameter
of two seconds and pin 0 set to high. Pin 0 will be high all the time. If now
the RS485 connection is lost, then pin 0 will get low in at most two seconds.
""",
'de':
"""
Konfiguriert einen Monoflop für die Pins, wie mittels der 8 Bit langen Bitmaske
des zweiten Parameters festgelegt. Die festgelegten Pins müssen als Ausgänge
konfiguriert sein. Als Eingänge konfigurierte Pins werden ignoriert.

Der dritte Parameter ist eine Bitmaske mit den gewünschten Zuständen der
festgelegten Ausgangspins. Eine 1 in der Bitmaske bedeutet logisch 1 und
eine 0 in der Bitmaske bedeutet logisch 0.

Der vierte Parameter stellt die Zeit (in ms) dar, welche die Pins den Zustand
halten sollen.

Wenn diese Funktion mit den Parametern ('a', 9, 1, 1500) bzw.
('a', 0b00001001, 0b00000001, 1500) aufgerufen wird: Pin 0 wird auf logisch 1
und Pin 3 auf logisch 0 am Port 'a' gesetzt. Nach 1,5s wird Pin 0 wieder
logisch 0 und Pin 3 logisch 1 gesetzt.

Ein Monoflop kann zur Ausfallsicherung verwendet werden. Beispiel:
Angenommen ein RS485 Bus und ein IO-16 Bricklet ist an ein Slave Stapel verbunden.
Jetzt kann diese Funktion sekündlich, mit einem Zeitparameter von 2 Sekunden,
aufgerufen werden. Der Pin wird die gesamte Zeit im Zustand logisch 1 sein. Wenn
jetzt die RS485 Verbindung getrennt wird, wird der Pin nach spätestens zwei
Sekunden in den Zustand logisch 0 wechseln.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Port Monoflop',
'elements': [('Port', 'char', 1, 'in'),
             ('Pin', 'uint8', 1, 'in'),
             ('Value', 'uint8', 1, 'out'),
             ('Time', 'uint32', 1, 'out'),
             ('Time Remaining', 'uint32', 1, 'out')],
'since_firmware': [1, 1, 2],
'doc': ['af', {
'en':
"""
Returns (for the given pin) the current value and the time as set by
:func:`Set Port Monoflop` as well as the remaining time until the value flips.

If the timer is not running currently, the remaining time will be returned
as 0.
""",
'de':
"""
Gibt (für den angegebenen Pin) den aktuellen Zustand und die Zeit, wie von
:func:`Set Port Monoflop` gesetzt, sowie die noch verbleibende Zeit bis zum
Zustandswechsel, zurück.

Wenn der Timer aktuell nicht läuft, ist die noch verbleibende Zeit 0.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Monoflop Done',
'elements': [('Port', 'char', 1, 'out'),
             ('Selection Mask', 'uint8', 1, 'out'),
             ('Value Mask', 'uint8', 1, 'out')],
'since_firmware': [1, 1, 2],
'doc': ['c', {
'en':
"""
This callback is triggered whenever a monoflop timer reaches 0. The
:word:`parameters` contain the port, the involved pins and the current value of
the pins (the value after the monoflop).
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn ein Monoflop Timer abläuft (0 erreicht).
:word:`parameters` enthalten den Port, die beteiligten Pins als Bitmaske und
den aktuellen Zustand als Bitmaske (der Zustand nach dem Monoflop).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Selected Values',
'elements': [('Port', 'char', 1, 'in'),
             ('Selection Mask', 'uint8', 1, 'in'),
             ('Value Mask', 'uint8', 1, 'in')],
'since_firmware': [2, 0, 0],
'doc': ['af', {
'en':
"""
Sets the output value (high or low) for a port ("a" or "b" with a bitmask,
according to the selection mask. The bitmask is 8 bit long and a 1 in the
bitmask means high and a 0 in the bitmask means low.

For example: The parameters ('a', 192, 128) or ('a', 0b11000000, 0b10000000)
will turn pin 7 high and pin 6 low on port A, pins 0-6 will remain untouched.

Running monoflop timers for the selected pins will be aborted if this
function is called.

.. note::
 This function does nothing for pins that are configured as input.
 Pull-up resistors can be switched on with :func:`Set Port Configuration`.
""",
'de':
"""
Setzt den Ausgangszustand (logisch 1 oder logisch 0) mittels einer Bitmaske,
entsprechend der Selektionsmaske. Die Bitmaske hat eine Länge von 8 Bit und
eine 1 in der Bitmaske bedeutet logisch 1 und eine 0 in der Bitmaske bedeutet
logisch 0.

Beispiel: Die Parameter ('a', 192, 128) bzw. ('a', 0b11000000, 0b10000000)
setzen den Pin 7 auf logisch 1 und den Pin 6 auf logisch 0 an Port A. Die Pins
0-6 bleiben unangetastet.

Laufende Monoflop Timer für die ausgewählten Pins werden abgebrochen, wenn
diese Funktion aufgerufen wird.

.. note::
 Diese Funktion bewirkt keine Änderung an Pins die als Eingang konfiguriert sind.
 Pull-Up Widerstände können mit :func:`Set Port Configuration` zugeschaltet werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Edge Count',
'elements': [('Pin', 'uint8', 1, 'in'),
             ('Reset Counter', 'bool', 1, 'in'),
             ('Count', 'uint32', 1, 'out')],
'since_firmware': [2, 0, 3],
'doc': ['bf', {
'en':
"""
Returns the current value of the edge counter for the selected pin on port A.
You can configure the edges that are counted with :func:`Set Edge Count Config`.

If you set the reset counter to *true*, the count is set back to 0
directly after it is read.
""",
'de':
"""
Gibt den aktuellen Wert des Flankenzählers für den ausgewählten Pin von Port A
zurück. Die zu zählenden Flanken können mit :func:`Set Edge Count Config`
konfiguriert werden.

Wenn reset counter auf *true* gesetzt wird, wird der Zählerstand direkt
nach dem auslesen auf 0 zurückgesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Edge Count Config',
'elements': [('Pin', 'uint8', 1, 'in'),
             ('Edge Type', 'uint8', 1, 'in', {'constant_group': 'Edge Type'}),
             ('Debounce', 'uint8', 1, 'in')],
'since_firmware': [2, 0, 3],
'doc': ['af', {
'en':
"""
Configures the edge counter for the selected pin of port A. Pins 0 and 1
are available for edge counting.

The edge type parameter configures if rising edges, falling edges or
both are counted if the pin is configured for input. Possible edge types are:

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
Konfiguriert den Flankenzähler für den ausgewählten Pin von Port A.
Der Flankenzähler steht für Pins 0 und 1 zur Verfügung.

Der edge type Parameter konfiguriert den zu zählenden Flankentyp. Es können
steigende, fallende oder beide Flanken gezählt werden für Pins die als Eingang
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
'name': 'Get Edge Count Config',
'elements': [('Pin', 'uint8', 1, 'in'),
             ('Edge Type', 'uint8', 1, 'out', {'constant_group': 'Edge Type'}),
             ('Debounce', 'uint8', 1, 'out')],
'since_firmware': [2, 0, 3],
'doc': ['af', {
'en':
"""
Returns the edge type and debounce time for the selected pin of port A as set by
:func:`Set Edge Count Config`.
""",
'de':
"""
Gibt den Flankentyp sowie die Entprellzeit für den ausgewählten Pin von Port A
zurück, wie von :func:`Set Edge Count Config` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Input',
'functions': [('getter', ('Get Port', 'value from port A as bitmask'), [(('Value Mask', 'Value Mask (Port A)'), 'uint8:bitmask:8', 1, None, None, None)], [('char', 'a')])]
})

com['examples'].append({
'name': 'Output',
'functions': [('setter', 'Set Port Configuration', [('char', 'a'), ('uint8:bitmask:8', 1 << 0), ('char', 'o'), ('bool', False)], 'Set pin 0 on port A to output low', None),
              ('setter', 'Set Port Configuration', [('char', 'b'), ('uint8:bitmask:8', (1 << 0) | (1 << 7)), ('char', 'o'), ('bool', True)], 'Set pin 0 and 7 on port B to output high', None)]
})

com['examples'].append({
'name': 'Interrupt',
'functions': [('callback', ('Interrupt', 'interrupt'), [(('Port', 'Port'), 'char', 1, None, None, None), (('Interrupt Mask', 'Interrupt Mask'), 'uint8:bitmask:8', 1, None, None, None), (('Value Mask', 'Value Mask'), 'uint8:bitmask:8', 1, None, None, None)], None, None),
              ('setter', 'Set Port Interrupt', [('char', 'a'), ('uint8:bitmask:8', 1 << 2)], 'Enable interrupt on pin 2 of port A', None)]
})


def input_channel(idx):
    return {
            'predicate': 'cfg.pinConfiguration{} > 1'.format(idx),
            'id': 'Input Pin {}'.format(idx),
            'label': 'Measured Level (Pin {}/{})'.format(idx, ('A' if idx <= 7 else 'B') + str(idx % 8)),

            'type': 'Input Pin',

            'getter_packet': 'Get Port',
            'getter_packet_params': ["\'a\'" if idx <= 7 else "\'b\'"],
            'getter_transform': '(value & (1 << {})) > 0 ? OnOffType.ON : OnOffType.OFF'.format(idx % 8),

            'callback_filter': 'port == {} && (interruptMask & (1 << {})) > 0'.format("\'a\'" if idx <= 7 else "\'b\'", idx % 8),
            'callback_packet': 'Interrupt',
            'callback_transform': '(valueMask & (1 << {})) > 0 ? OnOffType.ON : OnOffType.OFF'.format(idx % 8),

            # TODO: Don't hard code update interval. Support channel configuration (not merged into thing conf).
            'init_code':"""this.setPortConfiguration({port}, (short)(1 << {idx_mod}), 'i', cfg.pinConfiguration{idx} % 2 == 1);
            this.setPortInterrupt({port}, (short)(this.getPortInterrupt({port}) | (1 << {idx_mod})));""".format(port="\'a\'" if idx <= 7 else "\'b\'", idx_mod=idx % 8, idx=idx),
            'dispose_code': """this.setPortInterrupt({port}, (short)(this.getPortInterrupt({port}) & ~(1 << {idx})));""".format(port="\'a\'" if idx <= 7 else "\'b\'",idx=idx % 8),
    }

def output_channel(idx):
    return {
            'predicate': 'cfg.pinConfiguration{} <= 1'.format(idx),
            'id': 'Output Pin {}'.format(idx),
            'label': 'Set Level (Pin {}/{})'.format(idx, ('A' if idx <= 7 else 'B') + str(idx % 8)),

            'type': 'Output Pin',

            'getter_packet': 'Get Port',
            'getter_packet_params': ["\'a\'" if idx <= 7 else "\'b\'"],
            'getter_transform': '(value & (1 << {})) > 0 ? OnOffType.ON : OnOffType.OFF'.format(idx % 8),

            'setter_packet': 'Set Selected Values',
            'setter_packet_params': ["\'a\'" if idx <= 7 else "\'b\'", '(short)(1 << {})'.format(idx % 8), 'cmd == OnOffType.ON ? (short)0xFF : (short)0'],
            'setter_command_type': "OnOffType",

            'callback_packet': 'Monoflop Done',
            'callback_filter': 'port == {} && (selectionMask & (1 << {})) > 0'.format("\'a\'" if idx <= 7 else "\'b\'", idx % 8),
            'callback_transform': '(valueMask & (1 << {})) > 0 ? OnOffType.ON : OnOffType.OFF'.format(idx % 8),


            'init_code':"""this.setPortConfiguration({port}, (short)(1 << {idx_mod}), 'o', cfg.pinConfiguration{idx} % 2 == 1);""".format(port="\'a\'" if idx <= 7 else "\'b\'", idx_mod=idx % 8, idx=idx),
    }

def monoflop_channel(idx):
    return {
        'predicate': 'cfg.pinConfiguration{} <= 1'.format(idx),
        'id': 'Monoflop Pin {}'.format(idx),
        'label': 'Monoflop Pin {}'.format(idx),
        'type': 'Monoflop',

        'getter_packet': 'Get Port Monoflop',
        'getter_packet_params': ["\'a\'" if idx <= 7 else "\'b\'", '(short){}'.format(idx % 8)],
        'getter_transform': 'value.value > 0 ? OnOffType.ON : OnOffType.OFF',

        'setter_packet': 'Set Port Monoflop',
        'setter_packet_params': ["\'a\'" if idx <= 7 else "\'b\'", '(short)(1 << {})'.format(idx % 8), 'channelCfg.monoflopValue.booleanValue() ? (short)0xFF : (short)0', 'channelCfg.monoflopDuration.longValue()'],
        'setter_command_type': "StringType", # Command type has to be string type to be able to use command options.
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

            'getter_packet': 'Get Edge Count',
            'getter_packet_params': ['(short){}'.format(index), 'channelCfg.resetOnRead'],
            'getter_transform': 'new QuantityType<>(value, {unit})',

            'java_unit': 'SmartHomeUnits.ONE',
            'is_trigger_channel': False
        }

def pin_config(idx):
    return {
            'name': 'Pin Configuration {}'.format(idx),
            'type': 'integer',
            'options': [
                ('Input with pull-up', 3),
                ('Input without pull-up', 2),
                ('Output (Initial high)', 1),
                ('Output (Initial low)', 0)
            ],
            'limitToOptions': 'true',
            'default': '3',

            'label': 'Pin Configuration {}/{}'.format(idx, ('A' if idx <= 7 else 'B') + str(idx % 8)),
            'description': 'Configures the direction of pin {}/{}. Inputs without pull-up will be floating if nothing is connected. Outputs can have an initial state of low or high.'.format(idx, ('A' if idx <= 7 else 'B') + str(idx % 8)),
        }

channels = [input_channel(i) for i in range(0, 16)] + [output_channel(i) for i in range(0, 16)] + [monoflop_channel(i) for i in range(0, 16)] + [edge_count_channel(i) for i in range(0, 2)]
params = [pin_config(i) for i in range(0, 16)]

com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.OnOffType', 'org.eclipse.smarthome.core.library.types.StringType'],
    'params': params,
    'channels': channels,
    'channel_types': [
        oh_generic_channel_type('Input Pin', 'Switch', 'Measured Level',
                     description='The logic level that is currently measured on the pin.',
                     read_only=True),
        oh_generic_channel_type('Output Pin', 'Switch', 'Set Level',
                     description='The logic level that is currently set on the pin.',
                     read_only=False),
        {
            'id': 'Monoflop',
            'item_type': 'String',
            'params': [{
                'name': 'Monoflop Duration',
                'type': 'integer',
                'default': 1000,
                'min': 0,
                'max': 2**31 - 1,
                'unit': 'ms',

                'label': 'Monoflop duration',
                'description': 'The time (in ms) that the pin should hold the configured value.',
            },
            {
                'name': 'Monoflop Value',
                'type': 'boolean',
                'default': 'true',

                'label': 'Monoflop value',
                'description': 'The desired value of the specified channel. Activated means relay closed and Deactivated means relay open.',
            }],
            'label': 'NOT USED',
            'description':'Triggers a monoflop as configured',
            'command_options': [('Trigger', 'TRIGGER')]
        },
        oh_generic_channel_type('Edge Count', 'Number:Dimensionless', 'Edge Count',
            description='The current value of the edge counter for the selected channel',
            read_only=True,
            params=[{
                'name': 'Edge Type',
                'type': 'integer',
                'options':[('Rising', 0),
                            ('Falling', 1),
                            ('Both', 2)],
                'limitToOptions': 'true',
                'default': '0',

                'label': 'Edge Type',
                'description': 'The edge type parameter configures if rising edges, falling edges or both are counted.',
            },{
                'name': 'Debounce',
                'type': 'integer',

                'default': '100',

                'label': 'Debounce Time',
                'description': 'The debounce time in ms.',
            },{
                'name': 'Reset On Read',
                'type': 'boolean',

                'default': 'false',

                'label': 'Reset Edge Count on Update',
                'description': 'Enabling this will reset the edge counter after OpenHAB reads its value. Use this if you want relative edge counts per update.',
            }])
    ]
}
