# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# HAT Brick communication config

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'category': 'Brick',
    'device_identifier': 111,
    'name': 'HAT',
    'display_name': 'HAT',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'HAT for Raspberry Pi with 8 Bricklets ports and real-time clock',
        'de': 'HAT für Raspberry Pi mit 8 Bricklet-Ports und Echtzeituhr'
    },
    'released': True,
    'documented': True,
    'discontinued': False,
    'features': [
        'comcu_bricklet',
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Set Sleep Mode',
'elements': [('Power Off Delay', 'uint32', 1, 'in', {'unit': 'Second'}),
             ('Power Off Duration', 'uint32', 1, 'in', {'unit': 'Second'}),
             ('Raspberry Pi Off', 'bool', 1, 'in', {}),
             ('Bricklets Off', 'bool', 1, 'in', {}),
             ('Enable Sleep Indicator', 'bool', 1, 'in', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the sleep mode.

.. note::
 Calling this function will cut the Raspberry Pi's power after Power Off Delay seconds.
 You have to shut down the operating system yourself, e.g. by calling 'sudo shutdown -h now'.

Parameters:

* Power Off Delay: Time before the RPi/Bricklets are powered off.
* Power Off Duration: Duration that the RPi/Bricklets stay powered off.
* Raspberry Pi Off: RPi is powered off if set to true.
* Bricklets Off: Bricklets are powered off if set to true.
* Enable Sleep Indicator: If set to true, the status LED will blink in a 1s interval
  during the whole power off duration. This will draw additional 0.3mA.

Example: To turn RPi and Bricklets off in 5 seconds for 10 minutes with sleep
indicator enabled, call (5, 60*10, true, true, true).

This function can also be used to implement a watchdog. To do this you can
write a program that calls this function once per second in a loop with
(10, 2, true, false, false). If the RPi crashes or gets stuck
the HAT will reset the RPi after 10 seconds.
""",
'de':
"""
Setzt den Schlaf-Modus.

.. note::
 Diese Funktion schaltet die Stromversorgung des Raspberry Pis nach Power Off Delay Sekunden ab.
 Das Betriebssystem muss manuell heruntergefahren werden, zum Beispiel durch Ausführen von
 'sudo shutdown -h now'.

Parameter:

* Power Off Delay: Zeit in Sekunden bis der RPi/die Bricklets ausgeschaltet werden.
* Power Off Duration: Dauer in Sekunden für die der RPi/die Bricklets ausgeschaltet bleiben.
* Raspberry Pi Off: RPi wird ausgeschaltet, falls auf *true* gesetzt.
* Bricklets Off: Bricklets werden ausgeschaltet falls auf *true* gesetzt.
* Enable Sleep Indicator: Wenn dieser Parameter auf *true* gesetzt wird, blinkt
  die Status-LED während der Schlafdauer mit einem Intervall von 1s. Dies verbraucht
  zusätzliche 0,3mA.

Beispiel: Um den RPi und die Bricklets in 5 Sekunden für 10 Minuten mit aktivierter
Status-LED auszuschalten, rufe (5, 60*10, *true*, *true*, *true*) auf.

Diese Funktion kann auch genutzt werden um einen Watchdog zu implementieren. Dazu
kann ein Programm geschrieben werden, welches in einer Schleife einmal pro Sekunde folgendes
aufruft: (10, 2, *true*, *false*, *false*). Dies führt dazu, dass das HAT
den RPi nach 10 Sekunden neustartet, wenn dieser abgestürzt oder stecken geblieben ist.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Sleep Mode',
'elements': [('Power Off Delay', 'uint32', 1, 'out', {'unit': 'Second'}),
             ('Power Off Duration', 'uint32', 1, 'out', {'unit': 'Second'}),
             ('Raspberry Pi Off', 'bool', 1, 'out', {}),
             ('Bricklets Off', 'bool', 1, 'out', {}),
             ('Enable Sleep Indicator', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the sleep mode settings as set by :func:`Set Sleep Mode`.
""",
'de':
"""
Gibt die Sleep-Mode-Einstellungen zurück, wie von :func:`Set Sleep Mode` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Bricklet Power',
'elements': [('Bricklet Power', 'bool', 1, 'in', {'default': True})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Set to true/false to turn the power supply of the connected Bricklets on/off.
""",
'de':
"""
Kann auf true/false gesetzt werden um die Spannungsversorgung der angeschlossenen
Bricklets an/aus zu stellen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Bricklet Power',
'elements': [('Bricklet Power', 'bool', 1, 'out', {'default': True})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the power status of the connected Bricklets as set by :func:`Set Bricklet Power`.
""",
'de':
"""
Gibt den Status der Stromversorgung der angeschlossenen Bricklets zurück, wie von
:func:`Set Bricklet Power` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Voltages',
'elements': [('Voltage USB', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'}),
             ('Voltage DC', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the USB supply voltage and the DC input supply voltage.

There are three possible combinations:

* Only USB connected: The USB supply voltage will be fed back to the
  DC input connector. You will read the USB voltage and a slightly lower
  voltage on the DC input.
* Only DC input connected: The DC voltage will not be fed back to the
  USB connector. You will read the DC input voltage and the USB voltage
  will be 0.
* USB and DC input connected: You will read both voltages. In this case
  the USB supply will be without load, but it will work as backup if you
  disconnect the DC input (or if the DC input voltage falls below the
  USB voltage).
""",
'de':
"""
Gibt die USB- und DC-Input-Versorgungsspannung zurück.

Es gibt drei mögliche Kombinationen:

* Nur USB verbunden: Die USB-Versorgungsspannung wird auf den DC-Input-Stecker
  zurückgespeist. Die USB-Spannung wird angezeigt und die DC-Input-Spannung ist
  etwas niedriger als die USB-Spannung.
* Nur DC-Input verbunden: Die DC-Versorgungsspannung wird nicht auf den
  USB-Stecker zurückgespeist. Die DC-Versorgungsspannung wird angezeigt und die
  USB-Spannung ist 0.
* USB und DC-Input verbunden: Beide Spannungen werden angezeigt. In diesem Fall
  ist die USB-Versorgungsspannung ohne Last, sie wird als Backup verwendet wenn
  der DC-Input getrennt wird (oder die DC-Input-Versorgungsspannung unter die
  USB-Spannung fällt).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Voltages Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'in', {'default': False})],
'since_firmware': [2, 0, 1],
'doc': ['ccf', {
'en':
"""
The period is the period with which the :cb:`Voltages`
callback is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.
""",
'de':
"""
Die Periode ist die Periode mit der der :cb:`Voltages`
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
'name': 'Get Voltages Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'out', {'default': False})],
'since_firmware': [2, 0, 1],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set Voltages Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set Voltages Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Voltages',
'elements': [('Voltage USB', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'}),
             ('Voltage DC', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'})],
'since_firmware': [2, 0, 1],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set Voltages Callback Configuration`.

The :word:`parameters` are the same as :func:`Get Voltages`.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set Voltages Callback Configuration` gesetzten Konfiguration

Die :word:`parameters` sind der gleiche wie :func:`Get Voltages`.
"""
}]
})

com['examples'].append({
'name': 'Sleep',
'functions': [('setter', 'Set Sleep Mode', [('uint32', 2), ('uint32', 60*30), ('bool', True), ('bool', True), ('bool', True)], 'Turn Raspberry Pi and Bricklets off in 2 seconds for 30 minutes with sleep indicator enabled', None)]
})

com['examples'].append({
'name': 'Print Voltages',
'functions': [('getter', ('Get Voltages', 'get voltages'), [(('Voltage USB', 'Voltage USB'), 'uint16', 1, 1000.0, 'V', None), (('Voltage DC', 'Voltage DC'), 'uint16', 1, 1000.0, 'V', None)], [])]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.OnOffType', 'org.eclipse.smarthome.core.library.types.StringType'],
    'param_groups': oh_generic_channel_param_groups() +  [{
        'name': 'sleep',
        'label': 'Sleep Mode',
        'description': 'Configures the sleep mode.',
        'advanced': 'true'
    }],
    'params': [update_interval('Set Voltages Callback Configuration', 'Period', 'Voltages', 'the voltages')],
    'channels': [{
            'id': 'Sleep',
            'type': 'Sleep',

            'setters': [{
                'packet': 'Set Sleep Mode',
                'packet_params': ['channelCfg.powerOffDelay', 'channelCfg.powerOffDuration', 'channelCfg.raspberryPiOff', 'channelCfg.brickletsOff', 'channelCfg.sleepIndicator'],
                'command_type': "StringType", # Command type has to be string type to be able to use command options.
            }],

        }, {
            'id': 'Power Bricklets',
            'type': 'Power Bricklets',

            'setters': [{
                'packet': 'Set Bricklet Power',
                'packet_params': ['cmd == OnOffType.ON'],
                'command_type': "OnOffType",
            }],


            'getters': [{
                'packet': 'Get Bricklet Power',
                'transform': 'value? OnOffType.ON : OnOffType.OFF'}]
        }, {
            'id': 'USB Voltage',
            'type': 'USB Voltage',
            'getters': [{
                'packet': 'Get Voltages',
                'packet_params': [],
                'transform': 'new QuantityType<>(value.voltageUSB{divisor}, {unit})'}],

            'callbacks': [{
                'packet': 'Voltages',
                'transform': 'new QuantityType<>(voltageUSB{divisor}, {unit})',
                'filter': 'true'}],

            'init_code':"""this.setVoltagesCallbackConfiguration(cfg.voltagesUpdateInterval, true);""",
            'dispose_code': """this.setVoltagesCallbackConfiguration(0, true);""",

            'java_unit': 'SmartHomeUnits.VOLT',
            'divisor': 1000.0,
            'is_trigger_channel': False
        }, {
            'id': 'DC Voltage',
            'type': 'DC Voltage',
            'getters': [{
                'packet': 'Get Voltages',
                'packet_params': [],
                'transform': 'new QuantityType<>(value.voltageDC{divisor}, {unit})'}],

            'callbacks': [{
                'packet': 'Voltages',
                'transform': 'new QuantityType<>(voltageDC{divisor}, {unit})',
                'filter': 'true'}],

            'java_unit': 'SmartHomeUnits.VOLT',
            'divisor': 1000.0,
            'is_trigger_channel': False
        }
    ],
    'channel_types': [
        oh_generic_channel_type('USB Voltage', 'Number:ElectricPotential', 'USB Voltage',
                    update_style=None,
                    description='The USB supply voltage.<br/><br/>There are three possible combinations:<ul><li>Only USB connected: The USB supply voltage will be fed back to the DC input connector. You will read the USB voltage and a slightly lower voltage on the DC input.</li><li>Only DC input connected: The DC voltage will not be fed back to the USB connector. You will read the DC input voltage and the USB voltage will be 0.</li><li>USB and DC input connected: You will read both voltages. In this case the USB supply will be without load, but it will work as backup if you disconnect the DC input (or if the DC input voltage falls below the USB voltage).</li></ul>',
                    read_only=True,
                    pattern='%.3f %unit%'),
        oh_generic_channel_type('DC Voltage', 'Number:ElectricPotential', 'DC Voltage',
                    update_style=None,
                    description='The DC supply voltage.<br/><br/>There are three possible combinations:<ul><li>Only USB connected: The USB supply voltage will be fed back to the DC input connector. You will read the USB voltage and a slightly lower voltage on the DC input.</li><li>Only DC input connected: The DC voltage will not be fed back to the USB connector. You will read the DC input voltage and the USB voltage will be 0.</li><li>USB and DC input connected: You will read both voltages. In this case the USB supply will be without load, but it will work as backup if you disconnect the DC input (or if the DC input voltage falls below the USB voltage).</li></ul>',
                    read_only=True,
                    pattern='%.3f %unit%'),
        oh_generic_channel_type('Power Bricklets', 'Switch', 'Power Bricklets',
                    update_style=None,
                    description='Enable/disable to turn the power supply of the connected Bricklets on/off.'),
        {
            'id': 'Sleep',
            'item_type': 'String',
            'params': [{
                    'packet': 'Set Sleep Mode',
                    'element': 'Power Off Delay',

                    'name': 'Power Off Delay',
                    'type': 'integer',
                    'default': 60,

                    'label': 'Power Off Delay',
                    'description': 'Time in seconds before the RPi/Bricklets are powered off.',
                    'groupName': 'sleep'
                }, {
                    'packet': 'Set Sleep Mode',
                    'element': 'Power Off Duration',

                    'name': 'Power Off Duration',
                    'type': 'integer',
                    'default': 10,

                    'label': 'Power Off Duration',
                    'description': 'Duration in seconds that the RPi/Bricklets stay powered off.',
                    'groupName': 'sleep'
                }, {
                    'packet': 'Set Sleep Mode',
                    'element': 'Raspberry Pi Off',

                    'name': 'Raspberry Pi Off',
                    'type': 'boolean',
                    'default': 'false',

                    'label': 'Raspberry Pi Off',
                    'description': 'Raspberry Pi is powered off if enabled.',
                    'groupName': 'sleep'
                }, {
                    'packet': 'Set Sleep Mode',
                    'element': 'Bricklets Off',

                    'name': 'Bricklets Off',
                    'type': 'boolean',
                    'default': 'true',

                    'label': 'Bricklets Off',
                    'description': 'Bricklets are powered off if enabled.',
                    'groupName': 'sleep'
                }, {
                    'packet': 'Set Sleep Mode',
                    'element': 'Enable Sleep Indicator',

                    'name': 'Sleep Indicator',
                    'type': 'boolean',
                    'default': 'true',

                    'label': 'Sleep Indicator',
                    'description': 'If enabled, the status LED will blink in a 1s interval during the whole power off duration. This will draw additional 0.3mA.',
                    'groupName': 'sleep'
                }
            ],
            'label': 'Sleep',
            'description': "Starts the configured sleep mode. Note: Triggering this will cut the Raspberry Pi's power after the configured amount of seconds. You have to shut down the operating system yourself, e.g. by calling 'sudo shutdown -h now'.",
            'command_options': [('Trigger', 'Start Sleep Mode')]
        }
    ]
}
