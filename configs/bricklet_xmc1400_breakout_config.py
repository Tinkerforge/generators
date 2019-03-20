# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# XMC1400 Breakout Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 279,
    'name': 'XMC1400 Breakout',
    'display_name': 'XMC1400 Breakout',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Bricklet development board',
        'de': 'Bricklet Entwicklungsboard'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'discontinued': False,
    'packets': [],
    'examples': []
}

GPIO_MODE = ('GPIO Mode', [('Input Tristate', 0),
                           ('Input Pull Down', 1),
                           ('Input Pull Up', 2),
                           ('Input Sampling', 3),
                           ('Input Inverted Tristate', 4),
                           ('Input Inverted Pull Down', 5),
                           ('Input Inverted Pull Up', 6),
                           ('Input Inverted Sampling', 7),
                           ('Output Push Pull', 8),
                           ('Output Open Drain', 9)])

GPIO_INPUT_HYSTERESIS = ('GPIO Input Hysteresis', [('Standard', 0),
                                                   ('Large', 4)])


com['packets'].append({
'type': 'function',
'name': 'Set GPIO Config',
'elements': [('Port', 'uint8', 1, 'in'),
             ('Pin', 'uint8', 1, 'in'),
             ('Mode', 'uint8', 1, 'in', GPIO_MODE),
             ('Input Hysteresis', 'uint8', 1, 'in', GPIO_INPUT_HYSTERESIS),
             ('Output Level', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Example for a setter function. The values are the values that can be given to
the XMC_GPIO_Init function. See communication.c in the firmware.
""",
'de':
"""
Beispiel für eine Setter-Funktion. Die Werte werden direkt an die Funktion
XMC_GPIO_Init übergeben. Siehe communication.c in the firmware.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get GPIO Input',
'elements': [('Port', 'uint8', 1, 'in'),
             ('Pin', 'uint8', 1, 'in'),
             ('Value', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Example for a getter function. Returns the result of a
XMC_GPIO_GetInput call for the given port/pin.
""",
'de':
"""
Beispiel für eine Getter-Funktion. Gibt das Resultat eines
XMC_GPIO-GetInput-Aufrufs für den gegebenen Port/Pin zurück.
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set ADC Channel Config',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Enable', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Enables a ADC channel for the ADC driver example (adc.c/adc.h).

There are 8 ADC channels and they correspond to the following pins:

* Channel 0: P2_6
* Channel 1: P2_8
* Channel 2: P2_9
* Channel 3: P2_10
* Channel 4: P2_11
* Channel 5: P2_0
* Channel 6: P2_1
* Channel 7: P2_2
""",
'de':
"""
Aktiviert einen ADC-Kanal für das ADC-Treiber Beispiel (adc.c/adc.h).

Es gibt 8 ADC-Kanäle und sie korrespondieren zu den folgenden Pinnen:

* Kanal 0: P2_6
* Kanal 1: P2_8
* Kanal 2: P2_9
* Kanal 3: P2_10
* Kanal 4: P2_11
* Kanal 5: P2_0
* Kanal 6: P2_1
* Kanal 7: P2_2
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get ADC Channel Config',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Enable', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the config for the given channel as set by :func:`Set ADC Channel Config`.
""",
'de':
"""
Gibt die Konfiguration für den gegebenen Kanal zurück, wie
von :func:`Set ADC Channel Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get ADC Channel Value',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Value', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the 12-bit value of the given ADC channel of the ADC driver example.
""",
'de':
"""
Gibt den 12-Bit Wert für den gegebenen ADC-Kanal des ADC-Treiber-Beispiels zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get ADC Values',
'elements': [('Values', 'uint16', 8, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the values for all 8 ADC channels of the adc driver example.

This example function also has a corresponding callback.

See :func:`Set ADC Values Callback Configuration` and :cb:`ADC Values`.
""",
'de':
"""
Gibt die Werte aller 8 ADC-Kanäle des ADC-Treiber-Beispiels zurück.

Diese Beispiel-Funktion hat auch einen korrespondierenden Callback.

Siehe :func:`Set ADC Values Callback Configuration` und :cb:`ADC Values`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set ADC Values Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period in ms is the period with which the :cb:`ADC Values`
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
Die Periode in ms ist die Periode mit der der :cb:`ADC Values`
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
'name': 'Get ADC Values Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set ADC Values Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set ADC Values Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'ADC Values',
'elements': [('Values', 'uint16', 8, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set ADC Values Callback Configuration`.

The :word:`parameters` are the same as :func:`Get ADC Values`.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set PM Concentration Callback Configuration` gesetzten Konfiguration

Die :word:`parameters` sind der gleiche wie :func:`Get ADC Values`.
"""
}]
})

count_doc = {
'en':
"""
Returns the value of the example count (see example.c).

This example function uses "add_callback_value_function"-helper in the
generater. The getter as well as the callback and callback configuration
functions are auto-generated for the API as well as the firmware.
""",
'de':
"""
Gibt den Wert des Beispiel-Zählers zurück (siehe example.c).

Diese Beispiel-Funktion nutzt die "add_callback_value_function"-Hilfsfunktion
im Generator. Der Getter sowie der Callback und die Callback-Konfigurations-Funktionen
werden automatisch für die API und die Firmware generiert.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Count',
    data_name = 'Count',
    data_type = 'uint32',
    doc       = count_doc
)
