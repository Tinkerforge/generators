# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Digital In 4 Bricklet communication config

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'category': 'Bricklet',
    'device_identifier': 223,
    'name': 'Industrial Digital In 4',
    'display_name': 'Industrial Digital In 4',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '4 galvanically isolated digital inputs',
        'de': '4 galvanisch getrennte digitale Eingänge'
    },
    'released': True,
    'documented': True,
    'discontinued': True, # replaced by Industrial Digital In 4 Bricklet 2.0
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
'elements': [('Value Mask', 'uint16', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the input value with a bitmask. The bitmask is 16bit long, *true*
refers to high and *false* refers to low.

For example: The value 3 or 0b0011 means that pins 0-1 are high and the other
pins are low.

If no groups are used (see :func:`Set Group`), the pins correspond to the
markings on the IndustrialDigital In 4 Bricklet.

If groups are used, the pins correspond to the element in the group.
Element 1 in the group will get pins 0-3, element 2 pins 4-7, element 3
pins 8-11 and element 4 pins 12-15.
""",
'de':
"""
Gibt die Ausgabewerte mit einer Bitmaske zurück. Die Bitmaske ist 16Bit lang.
*true* bedeutet logisch 1 und *false* logisch 0.

Zum Beispiel: Der Wert 3 bzw. 0b0011 bedeutet, dass die Pins 0-1 auf logisch 1
und alle anderen auf logisch 0 sind.

Falls keine Gruppen verwendet werden (siehe :func:`Set Group`), entsprechen
die Pins der Beschriftung auf dem Industrial Digital In 4 Bricklet.

Falls Gruppen verwendet werden, entsprechen die Pins den Elementen der
Gruppe. Element 1 in der Gruppe bekommt Pins 0-3,
Element 2 Pins 4-7, Element 3 Pins 8-11 und Element 4 Pins 12-15.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Group',
'elements': [('Group', 'char', 4, 'in', {'range': [('a', 'd'), ('n', 'n')]})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets a group of Digital In 4 Bricklets that should work together. You can
find Bricklets that can be grouped together with :func:`Get Available For Group`.

The group consists of 4 elements. Element 1 in the group will get pins 0-3,
element 2 pins 4-7, element 3 pins 8-11 and element 4 pins 12-15.

Each element can either be one of the ports ('a' to 'd') or 'n' if it should
not be used.

For example: If you have two Digital In 4 Bricklets connected to port A and
port B respectively, you could call with |abnn|.

Now the pins on the Digital In 4 on port A are assigned to 0-3 and the
pins on the Digital In 4 on port B are assigned to 4-7. It is now possible
to call :func:`Get Value` and read out two Bricklets at the same time.

Changing the group configuration resets all edge counter configurations
and values.
""",
'de':
"""
Setzt eine Gruppe von Digital In 4 Bricklets die zusammenarbeiten sollen.
Mögliche Gruppierungen können mit der Funktion :func:`Get Available For Group`
gefunden werden.

Eine Gruppe besteht aus 4 Element. Element 1 in der Gruppe bekommt Pins 0-3,
Element 2 Pins 4-7, Element 3 Pins 8-11 und Element 4 Pins 12-15.

Jedes Element kann entweder auf einen der Ports ('a' bis 'd') gesetzt werden
oder falls nicht genutzt 'n' gesetzt werden.

Zum Beispiel: Falls zwei Digital In 4 Bricklets mit Port A und Port B verbunden
sind, könnte diese Funktion mit |abnn| aufgerufen werden.

In diesem Fall wären die Pins von Port A den Werten 0-3 zugewiesen und
die Pins von Port B den Werten 4-7. Es ist jetzt möglich mit der Funktion
:func:`Get Value` beide Bricklets gleichzeitig auszulesen.

Änderungen an der Gruppeneinteilung setzt die Konfiguration und Zählerwerte
aller Flankenzähler zurück.
"""
},
{
'*': {
'abnn': {'php': "``array('a', 'b', 'n', 'n')``",
         '*': "``['a', 'b', 'n', 'n']``"}
}
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Group',
'elements': [('Group', 'char', 4, 'out', {'range': [('a', 'd'), ('n', 'n')]})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the group as set by :func:`Set Group`
""",
'de':
"""
Gibt die Gruppierung zurück, wie von :func:`Set Group` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Available For Group',
'elements': [('Available', 'uint8', 1, 'out', {'range': (0, 15)})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns a bitmask of ports that are available for grouping. For example the
value 5 or 0b0101 means: Port A and port C are connected to Bricklets that
can be grouped together.
""",
'de':
"""
Gibt eine Bitmaske von Ports zurück die für die Gruppierung zur Verfügung
stehen. Zum Beispiel bedeutet der Wert 5 bzw. 0b0101: Port A und Port C sind
mit Bricklets verbunden die zusammen gruppiert werden können.
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
connected to the Digital In 4 Bricklet, such as a button.
""",
'de':
"""
Setzt die Entprellperiode der :cb:`Interrupt` Callback.

Beispiel: Wenn dieser Wert auf 100 gesetzt wird, erhält man den Interrupt
maximal alle 100ms. Dies ist notwendig falls etwas prellendes an
das Digital In 4 Bricklet angeschlossen ist, wie z.B. einen Schalter.
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
'elements': [('Interrupt Mask', 'uint16', 1, 'in', {})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the pins on which an interrupt is activated with a bitmask.
Interrupts are triggered on changes of the voltage level of the pin,
i.e. changes from high to low and low to high.

For example: An interrupt bitmask of 9 or 0b1001 will enable the interrupt for
pins 0 and 3.

The interrupts use the grouping as set by :func:`Set Group`.

The interrupt is delivered with the :cb:`Interrupt` callback.
""",
'de':
"""
Setzt durch eine Bitmaske die Pins für welche der Interrupt aktiv ist.
Interrupts werden ausgelöst bei Änderung des Spannungspegels eines Pins,
z.B. ein Wechsel von logisch 1 zu logisch 0 und logisch 0 zu logisch 1.

Beispiel: Eine Interrupt Bitmaske von 9 bzw. 0b1001 aktiviert den Interrupt für
die Pins 0 und 3.

Die Interrupts benutzen die Gruppierung, wie von :func:`Set Group` gesetzt.

Der Interrupt wird mit dem :cb:`Interrupt` Callback zugestellt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Interrupt',
'elements': [('Interrupt Mask', 'uint16', 1, 'out', {})],
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
'elements': [('Interrupt Mask', 'uint16', 1, 'out', {}),
             ('Value Mask', 'uint16', 1, 'out', {})],
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

The interrupts use the grouping as set by :func:`Set Group`.
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

Die Interrupts benutzen die Gruppierung, wie von :func:`Set Group` gesetzt.
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

The edge counters use the grouping as set by :func:`Set Group`.
""",
'de':
"""
Gibt den aktuellen Wert des Flankenzählers für den ausgewählten Pin zurück. Die
zu zählenden Flanken können mit :func:`Set Edge Count Config` konfiguriert werden.

Wenn reset counter auf *true* gesetzt wird, wird der Zählerstand direkt
nach dem auslesen auf 0 zurückgesetzt.

Die Flankenzähler benutzen die Gruppierung, wie von :func:`Set Group` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Edge Count Config',
'elements': [('Selection Mask', 'uint16', 1, 'in', {}),
             ('Edge Type', 'uint8', 1, 'in', {'constant_group': 'Edge Type', 'default': 0}),
             ('Debounce', 'uint8', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 100})],
'since_firmware': [2, 0, 1],
'doc': ['af', {
'en':
"""
Configures the edge counter for the selected pins. A bitmask of 9 or 0b1001 will
enable the edge counter for pins 0 and 3.

The edge type parameter configures if rising edges, falling edges or
both are counted if the pin is configured for input. Possible edge types are:

* 0 = rising
* 1 = falling
* 2 = both

Configuring an edge counter resets its value to 0.

If you don't know what any of this means, just leave it at default. The
default configuration is very likely OK for you.

The edge counters use the grouping as set by :func:`Set Group`.
""",
'de':
"""
Konfiguriert den Flankenzähler für die ausgewählten Pins. Eine Bitmaske von 9
bzw. 0b1001 aktiviert den Flankenzähler für die Pins 0 und 3.

Der edge type Parameter konfiguriert den zu zählenden Flankentyp. Es können
steigende, fallende oder beide Flanken gezählt werden für Pins die als Eingang
konfiguriert sind. Mögliche Flankentypen sind:

* 0 = steigend
* 1 = fallend
* 2 = beide

Durch das Konfigurieren wird der Wert des Flankenzählers auf 0 zurückgesetzt.

Falls unklar ist was dies alles bedeutet, kann diese Funktion einfach
ignoriert werden. Die Standardwerte sind in fast allen Situationen OK.

Die Flankenzähler benutzen die Gruppierung, wie von :func:`Set Group` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Edge Count Config',
'elements': [('Pin', 'uint8', 1, 'in', {}),
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
'name': 'Simple',
'functions': [('getter', ('Get Value', 'value as bitmask'), [(('Value Mask', 'Value Mask'), 'uint16:bitmask:4', 1, None, None, None)], [])]
})

com['examples'].append({
'name': 'Interrupt',
'functions': [('callback', ('Interrupt', 'interrupt'), [(('Interrupt Mask', 'Interrupt Mask'), 'uint16:bitmask:4', 1, None, None, None), (('Value Mask', 'Value Mask'), 'uint16:bitmask:4', 1, None, None, None)], None, None),
              ('setter', 'Set Interrupt', [('uint16:bitmask:4', 1 << 0)], 'Enable interrupt on pin 0', None)]
})

def input_channel(idx):
    return {
            'id': 'Input Pin {}'.format(idx),
            'label': 'Input Value (Pin {})'.format(idx),

            'type': 'Input Pin',

            'getters': [{
                'packet': 'Get Value',
                'transform': '(value & (1 << {})) > 0 ? OnOffType.ON : OnOffType.OFF'.format(idx)}],

            'callbacks': [{
                'filter': '(interruptMask & (1 << {})) > 0'.format(idx),
                'packet': 'Interrupt',
                'transform': '(valueMask & (1 << {})) > 0 ? OnOffType.ON : OnOffType.OFF'.format(idx)}],

            'init_code':"""this.setInterrupt((short)(this.getInterrupt() | (1 << {idx})));""".format(idx=idx),
            'dispose_code': """this.setInterrupt((short)(this.getInterrupt() & ~(1 << {idx})));""".format(idx=idx),
    }

def edge_count_channel(index):
    return {
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


channels = [input_channel(i) for i in range(0, 4)] + [edge_count_channel(i) for i in range(0, 4)]

com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.OnOffType', 'org.eclipse.smarthome.core.library.types.StringType'],
    'channels': channels,
    'channel_types': [
        oh_generic_channel_type('Input Pin', 'Switch', 'Input Value',
                    update_style=None,
                    description='The logic level that is currently measured on the pin.',
                    read_only=True),
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
                'packet': 'Set Edge Count Config',
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
    'actions': ['Get Value', 'Get Edge Count Config']
}
