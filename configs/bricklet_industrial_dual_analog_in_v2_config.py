# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Dual Analog In Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from commonconstants import add_callback_value_function

from openhab_commonconfig import *

com = {
    'author': 'Ishraq Ibne Ashraf <ishraq@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'category': 'Bricklet',
    'device_identifier': 2121,
    'name': 'Industrial Dual Analog In V2',
    'display_name': 'Industrial Dual Analog In 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures two DC voltages between -35V and +35V with 24bit resolution each',
        'de': 'Misst zwei Gleichspannungen zwischen -35V und +35V mit jeweils 24Bit Auflösung'
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

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

com['constant_groups'].append({
'name': 'Sample Rate',
'type': 'uint8',
'constants': [('976 SPS', 0),
              ('488 SPS', 1),
              ('244 SPS', 2),
              ('122 SPS', 3),
              ('61 SPS', 4),
              ('4 SPS', 5),
              ('2 SPS', 6),
              ('1 SPS', 7)]
})

com['constant_groups'].append({
'name': 'Channel LED Config',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Show Heartbeat', 2),
              ('Show Channel Status', 3)]
})

com['constant_groups'].append({
'name': 'Channel LED Status Config',
'type': 'uint8',
'constants': [('Threshold', 0),
              ('Intensity', 1)]
})

com['doc'] = {
'en':
"""
The Bricklet has two input channel. Functions that are related
directly to a channel have a ``channel`` parameter to specify one of the two
channels. Valid values for the ``channel`` parameter are 0 and 1.
""",
'de':
"""
Das Bricklet hat zwei Eingangskanäle. Funktionen die
sich direkt auf einen der Kanäle beziehen haben einen ``channel`` Parameter,
um den Kanal anzugeben. Gültige Werte für der ``channel`` Parameter sind 0
und 1.
"""
}

voltage_doc = {
'en':
"""
Returns the voltage for the given channel.
""",
'de':
"""
Gibt die Spannung für den übergebenen Kanal zurück.
"""
}

add_callback_value_function(
    packets       = com['packets'],
    name          = 'Get Voltage',
    data_name     = 'Voltage',
    data_type     = 'int32',
    channel_count = 2,
    doc           = voltage_doc,
    scale         = (1, 1000),
    unit          = 'Volt',
    range_        = (-35000, 35000)
)

com['packets'].append({
'type': 'function',
'name': 'Set Sample Rate',
'elements': [('Rate', 'uint8', 1, 'in', {'constant_group': 'Sample Rate', 'default': 6})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the sample rate. The sample rate can be between 1 sample per second
and 976 samples per second. Decreasing the sample rate will also decrease the
noise on the data.
""",
'de':
"""
Setzt die Abtastrate. Der Wertebereich der verfügbare Abtastraten
liegt zwischen 1 Wert pro Sekunde und 976 Werte pro Sekunde. Ein
Verringern der Abtastrate wird auch das Rauschen auf den Daten verringern.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Sample Rate',
'elements': [('Rate', 'uint8', 1, 'out', {'constant_group': 'Sample Rate', 'default': 6})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the sample rate as set by :func:`Set Sample Rate`.
""",
'de':
"""
Gibt die Abtastrate zurück, wie von :func:`Set Sample Rate` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Calibration',
'elements': [('Offset', 'int32', 2, 'in', {'range': (-2**23, 2**23-1)}),
             ('Gain', 'int32', 2, 'in', {'range': (-2**23, 2**23-1)})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets offset and gain of MCP3911 internal calibration registers.

See MCP3911 datasheet 7.7 and 7.8. The Industrial Dual Analog In Bricklet 2.0
is already factory calibrated by Tinkerforge. It should not be necessary
for you to use this function
""",
'de':
"""
Setzt Offset und Gain der MCP3911 internen Kalibrierungsregister.

Siehe MCP3911 Datenblatt 7.7 und 7.8. Das Industrial Dual Analog In Bricklet 2.0
wird von Tinkerforge werkskalibriert. Ein Aufruf dieser Funktion sollte
nicht notwendig sein.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Calibration',
'elements': [('Offset', 'int32', 2, 'out', {'range': (-2**23, 2**23-1)}),
             ('Gain', 'int32', 2, 'out', {'range': (-2**23, 2**23-1)})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the calibration as set by :func:`Set Calibration`.
""",
'de':
"""
Gibt die Kalibrierung zurück, wie von :func:`Set Calibration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get ADC Values',
'elements': [('Value', 'int32', 2, 'out', {'range': (-2**23, 2**23-1)})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the ADC values as given by the MCP3911 IC. This function
is needed for proper calibration, see :func:`Set Calibration`.
""",
'de':
"""
Gibt die ADC-Werte des MCP3911 ICs zurück. Diese Funktion
wird für die Kalibrierung benötigt, siehe :func:`Set Calibration`.
"""
}]
})

led_channel_config_description = """Each channel has a corresponding LED. You can turn the LED off, on or show a
heartbeat. You can also set the LED to "Channel Status". In this mode the
LED can either be turned on with a pre-defined threshold or the intensity
of the LED can change with the measured value."""

com['packets'].append({
'type': 'function',
'name': 'Set Channel LED Config',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Config', 'uint8', 1, 'in', {'constant_group': 'Channel LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
{}

You can configure the channel status behavior with :func:`Set Channel LED Status Config`.

By default all channel LEDs are configured as "Channel Status".
""".format(led_channel_config_description),
'de':
"""
Jeder Kanal hat eine dazugehörige LED. Die LEDs können individuell an- oder
ausgeschaltet werden. Zusätzlich kann ein Heartbeat oder der Kanalstatus
angezeigt werden. Falls Kanalstatus gewählt wird kann die LED entweder ab einem
vordefinierten Schwellwert eingeschaltet werden oder ihre Helligkeit anhand des
gemessenen Wertes skaliert werden.

Das Verhalten des Kanalstatus kann mittels :func:`Set Channel LED Status Config`
eingestellt werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Channel LED Config',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Config', 'uint8', 1, 'out', {'constant_group': 'Channel LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the channel LED configuration as set by :func:`Set Channel LED Config`
""",
'de':
"""
Gibt die Kanal-LED-Konfiguration zurück, wie von :func:`Set Channel LED Config` gesetzt.
"""
}]
})

led_status_config_description = """For each channel you can choose between threshold and intensity mode.

In threshold mode you can define a positive or a negative threshold.
For a positive threshold set the "min" parameter to the threshold value in mV
above which the LED should turn on and set the "max" parameter to 0. Example:
If you set a positive threshold of 10V, the LED will turn on as soon as the
voltage exceeds 10V and turn off again if it goes below 10V.
For a negative threshold set the "max" parameter to the threshold value in mV
below which the LED should turn on and set the "min" parameter to 0. Example:
If you set a negative threshold of 10V, the LED will turn on as soon as the
voltage goes below 10V and the LED will turn off when the voltage exceeds 10V.

In intensity mode you can define a range in mV that is used to scale the brightness
of the LED. Example with min=4V, max=20V: The LED is off at 4V, on at 20V
and the brightness is linearly scaled between the values 4V and 20V. If the
min value is greater than the max value, the LED brightness is scaled the other
way around."""

com['packets'].append({
'type': 'function',
'name': 'Set Channel LED Status Config',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Min', 'int32', 1, 'in', {'scale': (1, 1000), 'unit': 'Volt', 'default': 0}),
             ('Max', 'int32', 1, 'in', {'scale': (1, 1000), 'unit': 'Volt', 'default': 10000}),
             ('Config', 'uint8', 1, 'in', {'constant_group': 'Channel LED Status Config', 'default': 1})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the channel LED status config. This config is used if the channel LED is
configured as "Channel Status", see :func:`Set Channel LED Config`.

{}
""".format(led_status_config_description),
'de':
"""
Setzt die Kanal-LED-Status-Konfiguration. Diese Einstellung wird verwendet wenn
die Kanal-LED auf Kanalstatus eingestellt ist, siehe :func:`Set Channel LED Config`.

Für jeden Kanal kann zwischen Schwellwert- und Intensitätsmodus gewählt werden.

Im Schwellwertmodus kann ein positiver oder negativer Schwellwert definiert werden.
Für einen positiven Schwellwert muss der "min" Parameter auf den gewünschten
Schwellwert in mV gesetzt werden, über dem die LED eingeschaltet werden soll.
Der "max" Parameter muss auf 0 gesetzt werden. Beispiel: Bei einem positiven
Schwellwert von 10V wird die LED eingeschaltet sobald die gemessene Spannung
über 10V steigt und wieder ausgeschaltet sobald der Strom unter 10V fällt.
Für einen negativen Schwellwert muss der "max" Parameter auf den gewünschten
Schwellwert in mV gesetzt werden, unter dem die LED eingeschaltet werden soll.
Der "max" Parameter muss auf 0 gesetzt werden. Beispiel: Bei einem negativen
Schwellwert von 10mA wird die LED eingeschaltet sobald die gemessene Spannung
unter 10V fällt und wieder ausgeschaltet sobald der Strom über 10V steigt.

Im Intensitätsmodus kann ein Bereich in mV angegeben werden über den die Helligkeit
der LED skaliert wird. Beispiel mit min=4V und max=20V: Die LED ist bei 4V und
darunter aus, bei 20V und darüber an und zwischen 4V und 20V wird die Helligkeit
linear skaliert. Wenn der min Wert größer als der max Wert ist, dann wird die
Helligkeit andersherum skaliert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Channel LED Status Config',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Min', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt', 'default': 0}),
             ('Max', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt', 'default': 10000}),
             ('Config', 'uint8', 1, 'out', {'constant_group': 'Channel LED Status Config', 'default': 1})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the channel LED status configuration as set by
:func:`Set Channel LED Status Config`.
""",
'de':
"""
Gibt die Kanal-LED-Status-Konfiguration zurück, wie von
:func:`Set Channel LED Status Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get All Voltages',
'elements': [('Voltages', 'int32', 2, 'out', {'scale': (1, 1000), 'unit': 'Volt', 'range': (-35000, 35000)})],
'since_firmware': [2, 0, 6],
'doc': ['af', {
'en':
"""
Returns the voltages for all channels.

If you want to get the value periodically, it is recommended to use the
:cb:`All Voltages` callback. You can set the callback configuration
with :func:`Set All Voltages Callback Configuration`.
""",
'de':
"""
Gibt die Spannung aller Kanäle zurück.

Wenn der Wert periodisch benötigt wird, kann auch der :cb:`All Voltages` Callback
verwendet werden. Der Callback wird mit der Funktion
:func:`Set All Voltages Callback Configuration` konfiguriert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set All Voltages Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'in', {'default': False})],
'since_firmware': [2, 0, 6],
'doc': ['ccf', {
'en':
"""
The period is the period with which the :cb:`All Voltages`
callback is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after at least one of the values has changed. If the values didn't
change within the period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.
""",
'de':
"""
Die Periode ist die Periode mit der der :cb:`All Voltages`
Callback ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn sich mindestens ein Wert im Vergleich zum letzten mal geändert
hat. Ändert sich kein Wert innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn ein Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen der Werte.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get All Voltages Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'out', {'default': False})],
'since_firmware': [2, 0, 6],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set All Voltages Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set All Voltages Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'All Voltages',
'elements': [('Voltages', 'int32', 2, 'out', {'scale': (1, 1000), 'unit': 'Volt', 'range': (-35000, 35000)})],
'since_firmware': [2, 0, 6],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set All Voltages Callback Configuration`.

The :word:`parameters` are the same as :func:`Get All Voltages`.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set All Voltages Callback Configuration` gesetzten Konfiguration

Die :word:`parameters` sind der gleiche wie :func:`Get All Voltages`.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Voltage', 'voltage from channel 0'), [(('Voltage', 'Voltage (Channel 0)'), 'int32', 1, 1000.0, 'V', None)], [('uint8', 0)])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Voltage', 'voltage'), [(('Channel', 'Channel'), 'uint8', 1, None, None, None), (('Voltage', 'Voltage'), 'int32', 1, 1000.0, 'V', None)], None, None),
              ('callback_configuration', ('Voltage', 'voltage (channel 0)'), [('uint8', 0)], 1000, False, 'x', [(0, 0)])]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('callback', ('Voltage', 'voltage'), [(('Channel', 'Channel'), 'uint8', 1, None, None, None), (('Voltage', 'Voltage'), 'int32', 1, 1000.0, 'V', None)], None, None),
              ('callback_configuration', ('Voltage', 'voltage (channel 0)'), [('uint8', 0)], 10000, False, '>', [(10, 0)])]
})

def voltage_channel(index):
    return {
            'id': 'Voltage Channel {0}'.format(index),
            'type': 'Voltage',
            'label': 'Voltage Channel {0}'.format(index),

            'init_code':"""this.setVoltageCallbackConfiguration({0}, channelCfg.updateInterval, true, \'x\', 0, 0);
this.setChannelLEDConfig({0}, channelCfg.ledConfig);
this.setChannelLEDStatusConfig({0}, channelCfg.ledStatusMinimum, channelCfg.ledStatusMaximum, channelCfg.ledStatusMode);""".format(index),
            'dispose_code': """this.setVoltageCallbackConfiguration({0}, 0, true, \'x\', 0, 0);""".format(index),

            'getters': [{
                'packet': 'Get Voltage',
                'element': 'Voltage',
                'packet_params': [str(index)],
                'transform': 'new {number_type}(value{divisor}{unit})'}],

            'callbacks': [{
                'filter': 'channel == {0}'.format(index),
                'packet': 'Voltage',
                'element': 'Voltage',
                'transform': 'new {number_type}(voltage{divisor}{unit})'}],

        }

def led_status_config():
    return [{
            'packet': 'Set Channel LED Config',
            'element': 'Config',

            'name': 'LED Config',
            'type': 'integer',

            'label': 'LED Configuration',
            'description': led_channel_config_description.replace('"', '\\\"'),
        },
        {
            'packet': 'Set Channel LED Status Config',
            'element': 'Config',

            'name': 'LED Status Mode',
            'type': 'integer',

            'label': 'LED Status Mode',
            'description': led_status_config_description.replace('"', '\\\"'),
        },
        {
            'packet': 'Set Channel LED Status Config',
            'element': 'Min',

            'name': 'LED Status Minimum',
            'type': 'integer',
            'min': '-35',
            'max': 35,
            'unit': 'V',
            'default': 0,

            'label': 'LED Status Maximum',
            'description': 'See LED Status Mode for further explaination.',
        },
        {
            'packet': 'Set Channel LED Status Config',
            'element': 'Max',

            'name': 'LED Status Maximum',
            'type': 'integer',
            'min': '-35',
            'max': 35,
            'unit': 'V',
            'default': 10,

            'label': 'LED Status Maximum',
            'description': 'See LED Status Mode for further explaination.',
        }]

com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'params': [
        {
            'packet': 'Set Sample Rate',
            'element': 'Rate',

            'name': 'Sample Rate',
            'type': 'integer',

            'label': 'Sample Rate',
            'description': "The voltage measurement sample rate. Decreasing the sample rate will also decrease the noise on the data.",
        }
    ],
    'init_code': """this.setSampleRate(cfg.sampleRate);""",
    'channels': [
        voltage_channel(0),
        voltage_channel(1),
    ],
    'channel_types': [
        oh_generic_channel_type('Voltage', 'Number', 'NOT USED',
                    update_style='Callback Configuration',
                    description='Measured voltage between -35 and 35 V',
                    params=led_status_config())
    ],
    'actions': ['Get Voltage', 'Get Channel LED Config', 'Get Channel LED Status Config', 'Get Sample Rate', 'Get Calibration', 'Get ADC Values']
}
