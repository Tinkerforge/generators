# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Analog Out Bricklet 2.0 communication config

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2116,
    'name': 'Industrial Analog Out V2',
    'display_name': 'Industrial Analog Out 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Generates configurable DC voltage and current, 0V to 10V and 4mA to 20mA',
        'de': 'Erzeugt konfigurierbare Gleichspannung und -strom, 0V bis 10V und 4mA bis 20mA'
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

com['constant_groups'].append({
'name': 'Voltage Range',
'type': 'uint8',
'constants': [('0 To 5V', 0),
              ('0 To 10V', 1)]
})

com['constant_groups'].append({
'name': 'Current Range',
'type': 'uint8',
'constants': [('4 To 20mA', 0),
              ('0 To 20mA', 1),
              ('0 To 24mA', 2)]
})

com['constant_groups'].append({
'name': 'Out LED Config',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Show Heartbeat', 2),
              ('Show Out Status', 3)]
})

com['constant_groups'].append({
'name': 'Out LED Status Config',
'type': 'uint8',
'constants': [('Threshold', 0),
              ('Intensity', 1)]
})

com['packets'].append({
'type': 'function',
'name': 'Set Enabled',
'elements': [('Enabled', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Enables/disables the output of voltage and current.

The default is disabled.
""",
'de':
"""
Aktiviert/deaktiviert die Ausgabe von Spannung und Strom.

Der Standardwert ist deaktiviert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Enabled',
'elements': [('Enabled', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns *true* if output of voltage and current is enabled, *false* otherwise.
""",
'de':
"""
Gibt *true* zurück falls die Ausgabe von Spannung und Strom aktiviert ist,
*false* sonst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Voltage',
'elements': [('Voltage', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the output voltage in mV.

The output voltage and output current are linked. Changing the output voltage
also changes the output current.
""",
'de':
"""
Setzt die Ausgangsspannung in mV.

Die Ausgangsspannung und der Ausgangsstrom sind gekoppelt. Eine Änderung der
Ausgangsspannung führt auch zu einer Änderung des Ausgangsstroms.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Voltage',
'elements': [('Voltage', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the voltage as set by :func:`Set Voltage`.
""",
'de':
"""
Gibt die Spannung zurück, wie von :func:`Set Voltage` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Current',
'elements': [('Current', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the output current in µA.

The output current and output voltage are linked. Changing the output current
also changes the output voltage.
""",
'de':
"""
Setzt den Ausgangsstrom in µA.

Der Ausgangsstrom und die Ausgangsspannung sind gekoppelt. Eine Änderung des
Ausgangsstroms führt auch zu einer Änderung der Ausgangsspannung.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Current',
'elements': [('Current', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current as set by :func:`Set Current`.
""",
'de':
"""
Gibt die Spannung zurück, wie von :func:`Set Current` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('Voltage Range', 'uint8', 1, 'in', {'constant_group': 'Voltage Range'}),
             ('Current Range', 'uint8', 1, 'in', {'constant_group': 'Current Range'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Configures the voltage and current range.

Possible voltage ranges are:

* 0V to 5V
* 0V to 10V (default)

Possible current ranges are:

* 4mA to 20mA (default)
* 0mA to 20mA
* 0mA to 24mA

The resolution will always be 12 bit. This means, that the
precision is higher with a smaller range.
""",
'de':
"""
Konfiguriert die Spannungs- und Stromwertebereiche.

Einstellbare Spannungswertebereiche sind:

* 0V bis 5V
* 0V bis 10V (Standard)

Einstellbare Stromwertebereiche sind:

* 4mA bis 20mA (Standard)
* 0mA bis 20mA
* 0mA bis 24mA

Die Auflösung ist immer 12 Bit. Dass heißt, die Genauigkeit erhöht
sich bei kleineren Wertebereichen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Voltage Range', 'uint8', 1, 'out', {'constant_group': 'Voltage Range'}),
             ('Current Range', 'uint8', 1, 'out', {'constant_group': 'Current Range'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Out LED Config',
'elements': [('Config', 'uint8', 1, 'in', {'constant_group': 'Out LED Config'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
You can turn the Out LED off, on or show a
heartbeat. You can also set the LED to "Out Status". In this mode the
LED can either be turned on with a pre-defined threshold or the intensity
of the LED can change with the output value (voltage or current).

You can configure the channel status behavior with :func:`Set Out LED Status Config`.

By default the LED is configured as "Out Status"
""",
'de':
"""
Die Out LED kann an- oder
ausgeschaltet werden. Zusätzlich kann ein Heartbeat oder der "Out-Status"
angezeigt werden. Falls Out-Status gewählt wird kann die LED entweder ab einem
vordefinierten Schwellwert eingeschaltet werden oder ihre Helligkeit anhand des
Ausgabewertes (Spannung oder Strom) skaliert werden.

Das Verhalten des Out-Status kann mittels :func:`Set Out LED Status Config`
eingestellt werden.

Standardmäßig ist die LED auf Out-Status konfiguriert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Out LED Config',
'elements': [('Config', 'uint8', 1, 'out', {'constant_group': 'Out LED Config'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the Out LED configuration as set by :func:`Set Out LED Config`
""",
'de':
"""
Gibt die Out-LED-Konfiguration zurück, wie von :func:`Set Out LED Config` gesetzt.
"""
}]
})

out_led_status_description = """For each channel you can choose between threshold and intensity mode.

In threshold mode you can define a positive or a negative threshold.
For a positive threshold set the "min" parameter to the threshold value in mV or
µA above which the LED should turn on and set the "max" parameter to 0. Example:
If you set a positive threshold of 5V, the LED will turn on as soon as the
output value exceeds 5V and turn off again if it goes below 5V.
For a negative threshold set the "max" parameter to the threshold value in mV or
µA below which the LED should turn on and set the "min" parameter to 0. Example:
If you set a negative threshold of 5V, the LED will turn on as soon as the
output value goes below 5V and the LED will turn off when the output value
exceeds 5V.

In intensity mode you can define a range mV or µA that is used to scale the brightness
of the LED. Example with min=2V, max=8V: The LED is off at 2V and below, on at
8V and above and the brightness is linearly scaled between the values 2V and 8V.
If the min value is greater than the max value, the LED brightness is scaled the
other way around."""

com['packets'].append({
'type': 'function',
'name': 'Set Out LED Status Config',
'elements': [('Min', 'uint16', 1, 'in'),
             ('Max', 'uint16', 1, 'in'),
             ('Config', 'uint8', 1, 'in', {'constant_group': 'Out LED Status Config'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the Out LED status config. This config is used if the Out LED is
configured as "Out Status", see :func:`Set Out LED Config`.

{}

By default the channel LED status config is set to intensity with min=0V and
max=10V.
""".format(out_led_status_description),
'de':
"""
Setzt die Out-LED-Status-Konfiguration. Diese Einstellung wird verwendet wenn
die Out-LED auf Out-Status eingestellt ist, siehe :func:`Set Out LED Config`.

Für jeden Kanal kann zwischen Schwellwert- und Intensitätsmodus gewählt werden.

Im Schwellwertmodus kann ein positiver oder negativer Schwellwert definiert werden.
Für einen positiven Schwellwert muss das "min" Parameter auf den gewünschten
Schwellwert in mV oder µA gesetzt werden, über dem die LED eingeschaltet werden
soll. Der "max" Parameter muss auf 0 gesetzt werden. Beispiel: Bei einem
positiven Schwellwert von 5V wird die LED eingeschaltet sobald der Ausgabewert
über 5V steigt und wieder ausgeschaltet sobald der Ausgabewert unter 5V fällt.
Für einen negativen Schwellwert muss das "max" Parameter auf den gewünschten
Schwellwert in mV oder µA gesetzt werden, unter dem die LED eingeschaltet werden
soll. Der "max" Parameter muss auf 0 gesetzt werden. Beispiel: Bei einem negativen
Schwellwert von 5V wird die LED eingeschaltet sobald der Ausgabewert unter
5V fällt und wieder ausgeschaltet sobald der Ausgabewert über 5V steigt.

Im Intensitätsmodus kann ein Bereich in mV oder µA angegeben werden über den die
Helligkeit der LED skaliert wird. Beispiel mit min=2V und max=8V: Die LED ist
bei 2V und darunter aus, bei 8V und darüber an und zwischen 2V und 8V wird die
Helligkeit linear skaliert. Wenn der min Wert größer als der max Wert ist, dann
wird die Helligkeit andersherum skaliert.

Standardwerte: Intensitätsmodus mit min=0V und max=10V.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Out LED Status Config',
'elements': [('Min', 'uint16', 1, 'out'),
             ('Max', 'uint16', 1, 'out'),
             ('Config', 'uint8', 1, 'out', {'constant_group': 'Out LED Status Config'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the Out LED status configuration as set by :func:`Set Out LED Status Config`.
""",
'de':
"""
Gibt die Out-LED-Status-Konfiguration zurück, wie von :func:`Set Out LED Status Config` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple Voltage',
'functions': [('setter', 'Set Voltage', [('uint16', 3300)], 'Set output voltage to 3.3V', None),
              ('setter', 'Set Enabled', [('bool', True)], None, None),
              ('wait',)],
'cleanups': [('setter', 'Set Enabled', [('bool', False)], None, None)]
})

com['examples'].append({
'name': 'Simple Current',
'functions': [('setter', 'Set Current', [('uint16', 4500)], 'Set output current to 4.5mA', None),
              ('setter', 'Set Enabled', [('bool', True)], None, None),
              ('wait',)],
'cleanups': [('setter', 'Set Enabled', [('bool', False)], None, None)]
})



com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.OnOffType', 'org.eclipse.smarthome.core.library.types.DecimalType'],
    'params': [
        {
            'name': 'Control Voltage',
            'type': 'integer',
            'options': [
                ('Current', '0'),
                ('Voltage', '1'),
            ],
            'limitToOptions': 'true',
            'default': '1',

            'label': 'Output Configuration',
            'description': 'Sets the output configuration. As the output voltage and current level depend on each other, only one can be controlled at the same time.',
        }, {
            'name': 'Voltage Range',
            'type': 'integer',
            'options': [('0 To 5V', 0),
                        ('0 To 10V', 1)
            ],
            'limitToOptions': 'true',
            'default': '1',

            'label': 'Voltage Range',
            'description': 'Configures the voltage range. The resolution will always be 12 bit. This means, that the precision is higher with a smaller range.',
        }, {
            'name': 'Current Range',
            'type': 'integer',
            'options': [('4 To 20mA', 0),
                        ('0 To 20mA', 1),
                        ('0 To 24mA', 2)
            ],
            'limitToOptions': 'true',
            'default': '1',

            'label': 'Current Range',
            'description': 'Configures the current range. The resolution will always be 12 bit. This means, that the precision is higher with a smaller range.',
        }, {
            'name': 'Out LED Config',
            'type': 'integer',
            'options': [('Off', 0),
                        ('On', 1),
                        ('Show Heartbeat', 2),
                        ('Show Out Status', 3)],
            'limitToOptions': 'true',
            'default': '3',

            'label': 'Output LED Configuration',
            'description': 'You can turn the Out LED off, on or show a heartbeat. You can also set the LED to Out Status. In this mode the LED can either be turned on with a pre-defined threshold or the intensity of the LED can change with the output value (voltage or current).',
        }, {
            'name': 'Out LED Status Mode',
            'type': 'integer',
            'options': [('Threshold', 0),
                        ('Intensity', 1)],
            'limitToOptions': 'true',
            'default': '1',

            'label': 'Output LED Status Mode',
            'description': out_led_status_description.replace('\n', '<br/>').replace('"', '\\\"'),
        }, {
            'name': 'Out LED Status Minimum',
            'type': 'decimal',
            'min': '0',
            'max': '10',
            'default': '0',

            'label': 'Output LED Status Maximum',
            'description': 'See LED Status Mode for further explaination.',
        }, {
            'name': 'Out LED Status Maximum',
            'type': 'decimal',
            'min': '0',
            'max': '10',
            'default': '10',

            'label': 'Output LED Status Maximum',
            'description': 'See LED Status Mode for further explaination.',
        }
    ],
    'init_code': """this.setConfiguration(cfg.voltageRange, cfg.currentRange);
this.setOutLEDConfig(cfg.outLEDConfig);
this.setOutLEDStatusConfig((int)(cfg.outLEDStatusMinimum.doubleValue() * (cfg.controlVoltage == 1 ? 1000.0 : 1000000.0)),
                           (int)(cfg.outLEDStatusMaximum.doubleValue() * (cfg.controlVoltage == 1 ? 1000.0 : 1000000.0)),
                           cfg.outLEDStatusMode);""",
    'channels': [{
            'id': 'Enabled',
            'type': 'Enabled',

            'setters': [{
                'packet': 'Set {title_words}',
                'packet_params': ['cmd == OnOffType.ON']}],
            'setter_command_type': "OnOffType",

            'getters': [{
                'packet': 'Get {title_words}',
                'transform': 'value ? OnOffType.ON : OnOffType.OFF'}]
        },
        {
            'id': 'Current',
            'type': 'Current',

            'predicate': 'cfg.controlVoltage == 0',

            'setters': [{
                'packet': 'Set {title_words}',
                'packet_params': ['(int)(cmd.doubleValue() * 1000000.0)']}],
            'setter_command_type': "QuantityType",

            'getters': [{
                'packet': 'Get {title_words}',
                'transform': 'new QuantityType(value / 1000000.0, SmartHomeUnits.AMPERE)'}]
        },
        {
            'id': 'Voltage',
            'type': 'Voltage',

            'predicate': 'cfg.controlVoltage == 1',

            'setters': [{
                'packet': 'Set {title_words}',
                'packet_params': ['(int)(cmd.doubleValue() * 1000.0)']}],
            'setter_command_type': "QuantityType",

            'getters': [{
                'packet': 'Get {title_words}',
                'transform': 'new QuantityType(value / 1000.0, SmartHomeUnits.VOLT)'}]
        }
    ],
    'channel_types': [
        oh_generic_channel_type('Enabled', 'Switch', 'Output Enabled',
                     description='Enables/disables the output of voltage and current.',
                     read_only=False),
        oh_generic_channel_type('Voltage', 'Number:ElectricPotential', 'Output Voltage',
                     description='The output voltage in V. The output voltage and output current are linked. Changing the output voltage also changes the output current.',
                     read_only=False,
                     pattern='%.3f %unit%',
                     min_=0,
                     max_=10),
        oh_generic_channel_type('Current', 'Number:ElectricCurrent', 'Output Current',
                     description='The output current in A. The output current and output voltage are linked. Changing the output current also changes the output voltage.',
                     read_only=False,
                     pattern='%.6f %unit%',
                     min_=0,
                     max_=0.024)
    ]
}


