# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Dual Analog In Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 249,
    'name': 'Industrial Dual Analog In',
    'display_name': 'Industrial Dual Analog In',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures two DC voltages between -35V and +35V with 24bit resolution each',
        'de': 'Misst zwei Gleichspannungen zwischen -35V und +35V mit jeweils 24Bit Auflösung'
    },
    'released': True,
    'documented': True,
    'discontinued': True, # replaced by Industrial Dual Analog In Bricklet 2.0
    'features': [
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

com['packets'].append({
'type': 'function',
'name': 'Get Voltage',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Voltage', 'int32', 1, 'out', {'divisor': 1000, 'unit': 'Volt', 'range': (-35000, 35000)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the voltage for the given channel.

If you want to get the voltage periodically, it is recommended to use the
:cb:`Voltage` callback and set the period with
:func:`Set Voltage Callback Period`.
""",
'de':
"""
Gibt die Spannung für den übergebenen Kanal zurück.

Wenn die Spannung periodisch abgefragt werden soll, wird empfohlen
den :cb:`Voltage` Callback zu nutzen und die Periode mit
:func:`Set Voltage Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Voltage Callback Period',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Period', 'uint32', 1, 'in', {'factor': 1000, 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Voltage` callback is triggered
periodically for the given channel. A value of 0 turns the callback off.

The :cb:`Voltage` callback is only triggered if the voltage has changed since the
last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Voltage` Callback für den
übergebenen Kanal ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Voltage` Callback wird nur ausgelöst, wenn sich die Spannung seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Voltage Callback Period',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Period', 'uint32', 1, 'out', {'divisor': 1000, 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Voltage Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Voltage Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Voltage Callback Threshold',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'int32', 1, 'in', {'divisor': 1000, 'unit': 'Volt', 'default': 0}),
             ('Max', 'int32', 1, 'in', {'divisor': 1000, 'unit': 'Volt', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Voltage Reached` callback for the given
channel.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the voltage is *outside* the min and max values"
 "'i'",    "Callback is triggered when the voltage is *inside* the min and max values"
 "'<'",    "Callback is triggered when the voltage is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the voltage is greater than the min value (max is ignored)"
""",
'de':
"""
Setzt den Schwellwert des :cb:`Voltage Reached` Callbacks für den übergebenen
Kanal.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn die Spannung *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn die Spannung *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn die Spannung kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn die Spannung größer als der min Wert ist (max wird ignoriert)"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Voltage Callback Threshold',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'int32', 1, 'out', {'divisor': 1000, 'unit': 'Volt', 'default': 0}),
             ('Max', 'int32', 1, 'out', {'divisor': 1000, 'unit': 'Volt', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Voltage Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Voltage Callback Threshold` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Debounce Period',
'elements': [('Debounce', 'uint32', 1, 'in', {'factor': 1000, 'unit': 'Second', 'default': 100})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the threshold callback

* :cb:`Voltage Reached`

is triggered, if the threshold

* :func:`Set Voltage Callback Threshold`

keeps being reached.
""",
'de':
"""
Setzt die Periode mit welcher der Schwellwert Callback

* :cb:`Voltage Reached`

ausgelöst werden, wenn der Schwellwert

* :func:`Set Voltage Callback Threshold`

weiterhin erreicht bleibt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Debounce Period',
'elements': [('Debounce', 'uint32', 1, 'out', {'divisor': 1000, 'unit': 'Second', 'default': 100})],
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

See MCP3911 datasheet 7.7 and 7.8. The Industrial Dual Analog In Bricklet
is already factory calibrated by Tinkerforge. It should not be necessary
for you to use this function
""",
'de':
"""
Setzt Offset und Gain der MCP3911 internen Kalibrierungsregister.

Siehe MCP3911 Datenblatt 7.7 und 7.8. Das Industrial Dual Analog In Bricklet
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

com['packets'].append({
'type': 'callback',
'name': 'Voltage',
'elements': [('Channel', 'uint8', 1, 'out', {'range': (0, 1)}),
             ('Voltage', 'int32', 1, 'out', {'divisor': 1000, 'unit': 'Volt', 'range': (-35000, 35000)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Voltage Callback Period`. The :word:`parameter` is the voltage of the
channel.

The :cb:`Voltage` callback is only triggered if the voltage has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Voltage Callback Period`,
ausgelöst. Der :word:`parameter` ist die Spannung des Kanals.

Der :cb:`Voltage` Callback wird nur ausgelöst, wenn sich die Spannung seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Voltage Reached',
'elements': [('Channel', 'uint8', 1, 'out', {'range': (0, 1)}),
             ('Voltage', 'int32', 1, 'out', {'divisor': 1000, 'unit': 'Volt', 'range': (-35000, 35000)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Voltage Callback Threshold` is reached.
The :word:`parameter` is the voltage of the channel.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Voltage Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Spannung des Kanals.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Voltage', 'voltage from channel 1'), [(('Voltage', 'Voltage (Channel 1)'), 'int32', 1, 1000.0, 'V', None)], [('uint8', 1)])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Voltage', 'voltage'), [(('Channel', 'Channel'), 'uint8', 1, None, None, None), (('Voltage', 'Voltage'), 'int32', 1, 1000.0, 'V', None)], None, None),
              ('callback_period', ('Voltage', 'voltage (channel 1)'), [('uint8', 1)], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('Voltage Reached', 'voltage reached'), [(('Channel', 'Channel'), 'uint8', 1, None, None, None), (('Voltage', 'Voltage'), 'int32', 1, 1000.0, 'V', None)], None, None),
              ('callback_threshold', ('Voltage', 'voltage (channel 1)'), [('uint8', 1)], '>', [(10, 0)])]
})



def voltage_channel(index):
    return {
            'id': 'Voltage Channel {0}'.format(index),
            'type': 'Voltage',
            'label': 'Voltage Channel {0}'.format(index),

            'init_code':"""this.setVoltageCallbackPeriod((short){0}, channelCfg.updateInterval);""".format(index),
            'dispose_code': """this.setVoltageCallbackPeriod((short){0}, 0);""".format(index),

            'getters': [{
                'packet': 'Get Voltage',
                'packet_params': ['(short){}'.format(index)],
                'transform': 'new QuantityType<>(value{divisor}, {unit})'}],

            'callbacks': [{
                'filter': 'channel == {0}'.format(index),
                'packet': 'Voltage',
                'transform': 'new QuantityType<>(voltage{divisor}, {unit})'}],

            'java_unit': 'SmartHomeUnits.VOLT',
            'divisor': '1000.0',
            'is_trigger_channel': False
        }

com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'params': [
        {
            'name': 'Sample Rate',
            'type': 'integer',
            'options': [('976 SPS', 0),
                        ('488 SPS', 1),
                        ('244 SPS', 2),
                        ('122 SPS', 3),
                        ('61 SPS', 4),
                        ('4 SPS', 5),
                        ('2 SPS', 6),
                        ('1 SPS', 7)],
            'limitToOptions': 'true',
            'default': '6',

            'label': 'Sample Rate',
            'description': "The voltage measurement sample rate. Decreasing the sample rate will also decrease the noise on the data.",
            'advanced': 'true'
        }
    ],
    'init_code': """this.setSampleRate(cfg.sampleRate.shortValue());""",
    'channels': [
        voltage_channel(0),
        voltage_channel(1),
    ],
    'channel_types': [
        oh_generic_channel_type('Voltage', 'Number:ElectricPotential', 'NOT USED',
                     description='Measured voltage between -35 and 35 V',
                     read_only=True,
                     pattern='%.3f %unit%',
                     min_=-35,
                     max_=35)
    ],
    'actions': ['Get Voltage', 'Get Sample Rate', 'Get Calibration', 'Get ADC Values']
}

