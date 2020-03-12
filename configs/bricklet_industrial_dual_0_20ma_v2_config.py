# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Dual 0-20mA Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from commonconstants import add_callback_value_function

from openhab_commonconfig import *

com = {
    'author': 'Ishraq Ibne Ashraf <ishraq@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2120,
    'name': 'Industrial Dual 0 20mA V2',
    'display_name': 'Industrial Dual 0-20mA 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures two DC currents between 0mA and 20mA (IEC 60381-1)',
        'de': 'Misst zwei Gleichströme zwischen 0mA und 20mA (IEC 60381-1)'
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
'constants': [('240 SPS', 0),
              ('60 SPS', 1),
              ('15 SPS', 2),
              ('4 SPS', 3)]
})

com['constant_groups'].append({
'name': 'Gain',
'type': 'uint8',
'constants': [('1x', 0),
              ('2x', 1),
              ('4x', 2),
              ('8x', 3)]
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

current_doc = {
'en':
"""
Returns the current of the specified channel.

It is possible to detect if an IEC 60381-1 compatible sensor is connected
and if it works probably.

If the returned current is below 4mA, there is likely no sensor connected
or the connected sensor is defective. If the returned current is over 20mA,
there might be a short circuit or the sensor is defective.
""",
'de':
"""
Gibt die gemessenen Stromstärke des spezifizierten Kanals zurück.

Es ist möglich zu erkennen ob ein IEC 60381-1-kompatibler Sensor angeschlossen
ist und ob er funktionsfähig ist.

Falls die zurückgegebene Stromstärke kleiner als 4mA ist, ist wahrscheinlich
kein Sensor angeschlossen oder der Sensor ist defekt. Falls die zurückgegebene
Stromstärke über 20mA ist, besteht entweder ein Kurzschluss oder der Sensor
ist defekt. Somit ist erkennbar ob ein Sensor angeschlossen und funktionsfähig
ist.
"""
}

add_callback_value_function(
    packets       = com['packets'],
    name          = 'Get Current',
    data_name     = 'Current',
    data_type     = 'int32',
    channel_count = 2,
    doc           = current_doc,
    scale         = (1, 1000*1000*1000),
    unit          = 'Ampere',
    range_        = (0, 22505322)
)

com['packets'].append({
'type': 'function',
'name': 'Set Sample Rate',
'elements': [('Rate', 'uint8', 1, 'in', {'constant_group': 'Sample Rate', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the sample rate to either 240, 60, 15 or 4 samples per second.
The resolution for the rates is 12, 14, 16 and 18 bit respectively.

.. csv-table::
 :header: "Value", "Description"
 :widths: 10, 100

 "0",    "240 samples per second, 12 bit resolution"
 "1",    "60 samples per second, 14 bit resolution"
 "2",    "15 samples per second, 16 bit resolution"
 "3",    "4 samples per second, 18 bit resolution"
""",
'de':
"""
Setzt die Abtastrate auf 240, 60, 15 oder 4 Samples pro Sekunde.
Die Auflösung für die Raten sind 12, 14, 16 und 18 Bit respektive.

.. csv-table::
 :header: "Wert", "Beschreibung"
 :widths: 10, 100

 "0",    "240 Samples pro Sekunde, 12 Bit Auflösung"
 "1",    "60 Samples pro Sekunde, 14 Bit Auflösung"
 "2",    "15 Samples pro Sekunde, 16 Bit Auflösung"
 "3",    "4 Samples pro Sekunde, 18 Bit Auflösung"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Sample Rate',
'elements': [('Rate', 'uint8', 1, 'out', {'constant_group': 'Sample Rate', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the gain as set by :func:`Set Sample Rate`.
""",
'de':
"""
Gibt die Verstärkung zurück, wie von :func:`Set Sample Rate` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Gain',
'elements': [('Gain', 'uint8', 1, 'in', {'constant_group': 'Gain', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets a gain between 1x and 8x. If you want to measure a very small current,
you can increase the gain to get some more resolution.

Example: If you measure 0.5mA with a gain of 8x the return value will be
4mA.
""",
'de':
"""
Setzt den Gain zwischen 1x und 8x. Wenn ein sehr kleiner Strom gemessen werden
soll, dann kann der Gain hochgesetzt werden, um die Auflösung zu verbessern.

Beispiel: Wenn 0,5mA gememsen werden mit einem Gain von 8x dann wird 4mA
zurückgegeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Gain',
'elements': [('Gain', 'uint8', 1, 'out', {'constant_group': 'Gain', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the gain as set by :func:`Set Gain`.
""",
'de':
"""
Gibt die Verstärkung zurück, wie von :func:`Set Gain` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Channel LED Config',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Config', 'uint8', 1, 'in', {'constant_group': 'Channel LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Each channel has a corresponding LED. You can turn the LED off, on or show a
heartbeat. You can also set the LED to "Channel Status". In this mode the
LED can either be turned on with a pre-defined threshold or the intensity
of the LED can change with the measured value.

You can configure the channel status behavior with :func:`Set Channel LED Status Config`.
""",
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
For a positive threshold set the "min" parameter to the threshold value in nA
above which the LED should turn on and set the "max" parameter to 0. Example:
If you set a positive threshold of 10mA, the LED will turn on as soon as the
current exceeds 10mA and turn off again if it goes below 10mA.
For a negative threshold set the "max" parameter to the threshold value in nA
below which the LED should turn on and set the "min" parameter to 0. Example:
If you set a negative threshold of 10mA, the LED will turn on as soon as the
current goes below 10mA and the LED will turn off when the current exceeds 10mA.

In intensity mode you can define a range in nA that is used to scale the brightness
of the LED. Example with min=4mA and max=20mA: The LED is off at 4mA and below,
on at 20mA and above and the brightness is linearly scaled between the values
4mA and 20mA. If the min value is greater than the max value, the LED brightness
is scaled the other way around."""

com['packets'].append({
'type': 'function',
'name': 'Set Channel LED Status Config',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Min', 'int32', 1, 'in', {'scale': (1, 1000*1000*1000), 'unit': 'Ampere', 'default': 4*1000*1000}),
             ('Max', 'int32', 1, 'in', {'scale': (1, 1000*1000*1000), 'unit': 'Ampere', 'default': 20*1000*1000}),
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
Schwellwert in nA gesetzt werden, über dem die LED eingeschaltet werden soll.
Der "max" Parameter muss auf 0 gesetzt werden. Beispiel: Bei einem positiven
Schwellwert von 10mA wird die LED eingeschaltet sobald der gemessene Strom über
10mA steigt und wieder ausgeschaltet sobald der Strom unter 10mA fällt.
Für einen negativen Schwellwert muss der "max" Parameter auf den gewünschten
Schwellwert in nA gesetzt werden, unter dem die LED eingeschaltet werden soll.
Der "max" Parameter muss auf 0 gesetzt werden. Beispiel: Bei einem negativen
Schwellwert von 10mA wird die LED eingeschaltet sobald der gemessene Strom unter
10mA fällt und wieder ausgeschaltet sobald der Strom über 10mA steigt.

Im Intensitätsmodus kann ein Bereich in nA angegeben werden über den die Helligkeit
der LED skaliert wird. Beispiel mit min=4mA und max=20mA: Die LED ist bei 4mA und
darunter aus, bei 20mA und darüber an und zwischen 4mA und 20mA wird die Helligkeit
linear skaliert. Wenn der min Wert größer als der max Wert ist, dann wird die
Helligkeit andersherum skaliert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Channel LED Status Config',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Min', 'int32', 1, 'out', {'scale': (1, 1000*1000*1000), 'unit': 'Ampere', 'default': 4*1000*1000}),
             ('Max', 'int32', 1, 'out', {'scale': (1, 1000*1000*1000), 'unit': 'Ampere', 'default': 20*1000*1000}),
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

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Current', 'current from channel 0'), [(('Current', 'Current (Channel 0)'), 'int32', 1, 1000000.0, 'mA', None)], [('uint8', 0)])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Current', 'current'), [(('Channel', 'Channel'), 'uint8', 1, None, None, None), (('Current', 'Current'), 'int32', 1, 1000000.0, 'mA', None)], None, None),
              ('callback_configuration', ('Current', 'current (channel 0)'), [('uint8', 0)], 1000, False, 'x', [(0, 0)])]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('callback', ('Current', 'current'), [(('Channel', 'Channel'), 'uint8', 1, None, None, None), (('Current', 'Current'), 'int32', 1, 1000000.0, 'mA', None)], None, None),
              ('callback_configuration', ('Current', 'current (channel 0)'), [('uint8', 0)], 10000, False, '>', [(10, 0)])]
})


def current_channel(index):
    return {
            'id': 'Current Sensor {0}'.format(index),
            'type': 'Current',
            'label': 'Current Sensor {0}'.format(index),

            'init_code':"""this.setCurrentCallbackConfiguration({0}, channelCfg.updateInterval, true, \'x\', 0, 0);
            this.setChannelLEDConfig({0}, channelCfg.ledConfig);
            this.setChannelLEDStatusConfig({0}, channelCfg.ledStatusMinimum, channelCfg.ledStatusMaximum, channelCfg.ledStatusMode);""".format(index),
            'dispose_code': """this.setCurrentCallbackConfiguration({0}, 0, true, \'x\', 0, 0);""".format(index),

            'getters': [{
                'packet': 'Get Current',
                'element': 'Current',
                'packet_params': ['{}'.format(index)],
                'transform': 'new QuantityType<>(value{divisor}, {unit})'}],

            'callbacks': [{
                'filter': 'channel == {0}'.format(index),
                'element': 'Current',
                'packet': 'Current',
                'transform': 'new QuantityType<>(current{divisor}, {unit})'}],

        }

def led_status_config():
    return [{
            'packet': 'Set Channel LED Config',
            'element': 'Config',

            'name': 'LED Config',
            'type': 'integer',
            'options': [('Off', 0),
                        ('On', 1),
                        ('Show Heartbeat', 2),
                        ('Show Channel Status', 3)],
            'limit_to_options': 'true',
            'label': 'LED Configuration',
            'description': """Each channel has a corresponding LED. You can turn the LED off, on or show a heartbeat. You can also set the LED to Show Channel Status. In this mode the LED can either be turned on with a pre-defined threshold or the intensity of the LED can change with the measured value.""",
        },
        {
            'packet': 'Set Channel LED Status Config',
            'element': 'Config',

            'name': 'LED Status Mode',
            'type': 'integer',
            'options': [('Threshold', 0),
                        ('Intensity', 1)],
            'limit_to_options': 'true',
            'label': 'LED Status Mode',
            'description': led_status_config_description.replace('\n', '<br/>').replace('"', '\\\"'),
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
    'params': [{
            'packet': 'Set Sample Rate',
            'element': 'Rate',

            'name': 'Sample Rate',
            'type': 'integer',
            'options': [('240 SPS', 0),
                        ('60 SPS', 1),
                        ('15 SPS', 2),
                        ('4 SPS', 3)],
            'limit_to_options': 'true',
            'label': 'Sample Rate',
            'description': "The sample rate to either 240, 60, 15 or 4 samples per second. The resolution for the rates is 12, 14, 16 and 18 bit respectively.",
            'advanced': 'true'
        }, {
            'packet': 'Set Gain',
            'element': 'Gain',

            'name': 'Gain',
            'type': 'integer',
            'options': [('1x', 0),
                        ('2x', 1),
                        ('4x', 2),
                        ('8x', 3)],
            'limit_to_options': 'true',
            'label': 'Gain',
            'description': "The gain between 1x and 8x. If you want to measure a very small current, you can increase the gain to get some more resolution.<br/><br/>Example: If you measure 0.5mA with a gain of 8x the return value will be 4mA.",
            'advanced': 'true'
        }
    ],
    'init_code': """this.setSampleRate(cfg.sampleRate);
    this.setGain(cfg.gain);""",
    'channels': [
        current_channel(0),
        current_channel(1),
    ],
    'channel_types': [
        oh_generic_channel_type('Current', 'Number', 'NOT USED',
                    update_style='Callback Configuration',
                    description='Measured current between 0 and 0.022505322A (22.5mA)',
                    read_only=True,
                    pattern='%.6f %unit%',
                    min_=0,
                    max_=0.022505322,
                    params=led_status_config())
    ],
    'actions': ['Get Current', 'Get Channel LED Config', 'Get Channel LED Status Config', 'Get Sample Rate', 'Get Gain']
}
