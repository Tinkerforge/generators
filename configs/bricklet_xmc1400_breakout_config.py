# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# XMC1400 Breakout Bricklet communication config

from generators.configs.commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from generators.configs.commonconstants import add_callback_value_function

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 279,
    'name': 'XMC1400 Breakout',
    'display_name': 'XMC1400 Breakout',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Breakout for Infineon XMC1400 microcontroller',
        'de': 'Entwicklungsboard für Infineon XMC1400 Mikrocontroller'
    },
    'released': True,
    'documented': True,
    'discontinued': False,
    'features': [
        'device',
        'comcu_bricklet',
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

com['constant_groups'].append({
'name': 'GPIO Mode',
'type': 'uint8',
'constants': [('Input Tristate', 0),
              ('Input Pull Down', 1),
              ('Input Pull Up', 2),
              ('Input Sampling', 3),
              ('Input Inverted Tristate', 4),
              ('Input Inverted Pull Down', 5),
              ('Input Inverted Pull Up', 6),
              ('Input Inverted Sampling', 7),
              ('Output Push Pull', 8),
              ('Output Open Drain', 9)]
})

com['constant_groups'].append({
'name': 'GPIO Input Hysteresis',
'type': 'uint8',
'constants': [('Standard', 0),
              ('Large', 4)]
})

com['packets'].append({
'type': 'function',
'name': 'Set GPIO Config',
'elements': [('Port', 'uint8', 1, 'in', {'range': (0, 4)}),
             ('Pin', 'uint8', 1, 'in', {'range': 'dynamic'}),
             ('Mode', 'uint8', 1, 'in', {'constant_group': 'GPIO Mode'}),
             ('Input Hysteresis', 'uint8', 1, 'in', {'constant_group': 'GPIO Input Hysteresis'}),
             ('Output Level', 'bool', 1, 'in', {})],
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
XMC_GPIO_Init übergeben. Siehe communication.c in der Firmware.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get GPIO Input',
'elements': [('Port', 'uint8', 1, 'in', {'range': (0, 4)}),
             ('Pin', 'uint8', 1, 'in', {'range': 'dynamic'}),
             ('Value', 'bool', 1, 'out', {})],
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
XMC_GPIO_GetInput-Aufrufs für den gegebenen Port/Pin zurück.
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set ADC Channel Config',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 7)}),
             ('Enable', 'bool', 1, 'in', {})],
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
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 7)}),
             ('Enable', 'bool', 1, 'out', {})],
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
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 7)}),
             ('Value', 'uint16', 1, 'out', {'range': (0, 4095)})],
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
'elements': [('Values', 'uint16', 8, 'out', {'range': (0, 4095)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the values for all 8 ADC channels of the adc driver example.

This example function also has a corresponding callback.

See :func:`Set ADC Values Callback Configuration` and :cb:`ADC Values` callback.
""",
'de':
"""
Gibt die Werte aller 8 ADC-Kanäle des ADC-Treiber-Beispiels zurück.

Diese Beispiel-Funktion hat auch einen korrespondierenden Callback.

Siehe :func:`Set ADC Values Callback Configuration` und :cb:`ADC Values` Callback.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set ADC Values Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period is the period with which the :cb:`ADC Values`
callback is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.
""",
'de':
"""
Die Periode ist die Periode mit der der :cb:`ADC Values`
Callback ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

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
'name': 'Get ADC Values Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'out', {'default': False})],
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
'elements': [('Values', 'uint16', 8, 'out', {'range': (0, 4095)})],
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
:func:`Set ADC Values Callback Configuration` gesetzten Konfiguration

Die :word:`parameters` sind der gleiche wie :func:`Get ADC Values`.
"""
}]
})

count_doc = {
'en':
"""
Returns the value of the example count (see example.c).

This example function uses the "add_callback_value_function"-helper in the
generator. The getter as well as the callback and callback configuration
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

com['examples'].append({
'name': 'GPIO',
'functions': [('loop_header', 5, 'Set Port 1, Pin 0 alternating high/low for 5 times with 1s delay'),
              ('sleep', 1000, None, None),
              ('setter', 'Set GPIO Config', [('uint8', 1), ('uint8', 0), ('uint8:constant', 8), ('uint8', 0), ('bool', False)], None, None),
              ('sleep', 1000, None, None),
              ('setter', 'Set GPIO Config', [('uint8', 1), ('uint8', 0), ('uint8:constant', 8), ('uint8', 0), ('bool', True)], None, None),
              ('loop_footer',)]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'params': [
        update_interval('Set ADC Values Callback Configuration', 'Period', 'ADC Values', 'ADC values')
    ],
    'init_code': """this.setADCValuesCallbackConfiguration(cfg.adcValuesUpdateInterval, true);""",
    'dispose_code': """this.setADCValuesCallbackConfiguration(0, true);""",
    'channels': [
        oh_generic_channel('Count', 'Count')
    ] + [
        {
        'id': 'ADC Value {}'.format(i),
        'label': 'ADC Value {}'.format(i),
        'type': 'ADC Value',

        'getters': [{
            'packet': 'Get ADC Values',
            'element': 'Values',
            'packet_params': [],
            'transform': 'new {{number_type}}(value[{}]{{divisor}}{{unit}})'.format(i)}],

        'callbacks': [{
            'packet': 'ADC Values',
            'element': 'Values',
            'transform': 'new {{number_type}}(values[{}]{{divisor}}{{unit}})'.format(i)
            }]
    } for i in range(0, 8)],
    'channel_types': [
        oh_generic_channel_type('Count', 'Number', 'Count',
                    update_style='Callback Configuration',
                    description='The value of the example count (see example.c)'),
        oh_generic_channel_type('ADC Value', 'Number', 'ADC Value',
                    update_style=None,
                    description='The value for one of the 8 ADC channels of the adc driver example.')
    ],
    'actions': ['Get Count']
}
