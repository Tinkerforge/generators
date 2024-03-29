# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Current25 Bricklet communication config

from generators.configs.commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 24,
    'name': 'Current25',
    'display_name': 'Current25',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures AC/DC current between -25A and +25A',
        'de': 'Misst Gleich- und Wechselstrom zwischen -25A und +25A'
    },
    'released': True,
    'documented': True,
    'discontinued': True, # replaced by Voltage/Current Bricklet 2.0
    'features': [
        'device',
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

com['packets'].append({
'type': 'function',
'name': 'Get Current',
'elements': [('Current', 'int16', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere', 'range': (-25000, 25000)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current of the sensor.

If you want to get the current periodically, it is recommended to use the
:cb:`Current` callback and set the period with
:func:`Set Current Callback Period`.
""",
'de':
"""
Gibt die gemessene Stromstärke des Sensors zurück.

Wenn die Stromstärke periodisch abgefragt werden soll, wird empfohlen
den :cb:`Current` Callback zu nutzen und die Periode mit
:func:`Set Current Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Calibrate',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Calibrates the 0 value of the sensor. You have to call this function
when there is no current present.

The zero point of the current sensor
is depending on the exact properties of the analog-to-digital converter,
the length of the Bricklet cable and the temperature. Thus, if you change
the Brick or the environment in which the Bricklet is used, you might
have to recalibrate.

The resulting calibration will be saved on the EEPROM of the Current
Bricklet.
""",
'de':
"""
Kalibriert den Nullwert des Sensors. Diese Funktion muss aufgerufen werden,
wenn kein Strom fließt.

Der Nullwert des Stromsensors ist abhängig von den exakten Eigenschaften des
Analog-Digital-Wandlers, der Länge des Bricklet Kabels und der Temperatur. Daher ist es,
bei Wechsel des Brick oder bei Veränderung der Umgebung in welcher das Bricklet genutzt wird,
ratsam erneut zu kalibrieren.

Die resultierende Kalibrierung wird in den EEPROM des Current Bricklet gespeichert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is Over Current',
'elements': [('Over', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns *true* if more than 25A were measured.

.. note::
 To reset this value you have to power cycle the Bricklet.
""",
'de':
"""
Gibt *true* zurück wenn mehr als 25A gemessen wurden.

.. note::
 Um diesen Wert zurückzusetzen ist ein Aus- und Wiedereinschalten des Bricklet
 notwendig.
"""
}]
})

analog_value_desc = """
Returns the value as read by a 12-bit analog-to-digital converter.

.. note::
 The value returned by :func:`Get Current` is averaged over several samples
 to yield less noise, while :func:`Get Analog Value` gives back raw
 unfiltered analog values. The only reason to use :func:`Get Analog Value` is,
 if you need the full resolution of the analog-to-digital converter.
"""

com['packets'].append({
'type': 'function',
'name': 'Get Analog Value',
'elements': [('Value', 'uint16', 1, 'out', {'range': (0, 4095)})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
analog_value_desc + """
If you want the analog value periodically, it is recommended to use the
:cb:`Analog Value` callback and set the period with
:func:`Set Analog Value Callback Period`.
""",
'de':
"""
Gibt den Wert, wie vom 12-Bit Analog-Digital-Wandler gelesen, zurück.

.. note::
 Der von :func:`Get Current` zurückgegebene Wert ist über mehrere
 Messwerte gemittelt um das Rauschen zu vermindern, während :func:`Get Analog Value`
 unverarbeitete Analogwerte zurück gibt. Der einzige Grund :func:`Get Analog Value`
 zu nutzen, ist die volle Auflösung des Analog-Digital-Wandlers zu erhalten.

Wenn der Analogwert periodisch abgefragt werden soll, wird empfohlen
den :cb:`Analog Value` Callback zu nutzen und die Periode mit
:func:`Set Analog Value Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Current Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Current` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Current` callback is only triggered if the current has changed since
the last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Current` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Current` Callback wird nur ausgelöst, wenn sich die Stromstärke seit
der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Current Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Current Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Current Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Analog Value Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Analog Value` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Analog Value` callback is only triggered if the analog value has
changed since the last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Analog Value` Callback ausgelöst
wird. Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Analog Value` Callback wird nur ausgelöst, wenn sich der Analogwert
seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Analog Value Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Analog Value Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Analog Value Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Current Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'int16', 1, 'in', {'scale': (1, 1000), 'unit': 'Ampere', 'default': 0}),
             ('Max', 'int16', 1, 'in', {'scale': (1, 1000), 'unit': 'Ampere', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Current Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the current is *outside* the min and max values"
 "'i'",    "Callback is triggered when the current is *inside* the min and max values"
 "'<'",    "Callback is triggered when the current is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the current is greater than the min value (max is ignored)"
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Current Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn die Stromstärke *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn die Stromstärke *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn die Stromstärke kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn die Stromstärke größer als der min Wert ist (max wird ignoriert)"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Current Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'int16', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere', 'default': 0}),
             ('Max', 'int16', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Current Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Current Callback Threshold` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Analog Value Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'in', {'range': (0, 4095), 'default': 0}),
             ('Max', 'uint16', 1, 'in', {'range': (0, 4095), 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Analog Value Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the analog value is *outside* the min and max values"
 "'i'",    "Callback is triggered when the analog value is *inside* the min and max values"
 "'<'",    "Callback is triggered when the analog value is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the analog value is greater than the min value (max is ignored)"
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Analog Value Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn der Analogwert *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn der Analogwert *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn der Analogwert kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn der Analogwert größer als der min Wert ist (max wird ignoriert)"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Analog Value Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'out', {'range': (0, 4095), 'default': 0}),
             ('Max', 'uint16', 1, 'out', {'range': (0, 4095), 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Analog Value Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Analog Value Callback Threshold` gesetzt.
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
Sets the period with which the threshold callbacks

* :cb:`Current Reached`,
* :cb:`Analog Value Reached`

are triggered, if the thresholds

* :func:`Set Current Callback Threshold`,
* :func:`Set Analog Value Callback Threshold`

keep being reached.
""",
'de':
"""
Setzt die Periode mit welcher die Schwellwert Callbacks

* :cb:`Current Reached`,
* :cb:`Analog Value Reached`

ausgelöst werden, wenn die Schwellwerte

* :func:`Set Current Callback Threshold`,
* :func:`Set Analog Value Callback Threshold`

weiterhin erreicht bleiben.
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
'type': 'callback',
'name': 'Current',
'elements': [('Current', 'int16', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere', 'range': (-25000, 25000)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Current Callback Period`. The :word:`parameter` is the current of the
sensor.

The :cb:`Current` callback is only triggered if the current has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Current Callback Period`,
ausgelöst. Der :word:`parameter` ist die Stromstärke des Sensors.

Der :cb:`Current` Callback wird nur ausgelöst, wenn sich die Stromstärke seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Analog Value',
'elements': [('Value', 'uint16', 1, 'out', {'range': (0, 4095)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Analog Value Callback Period`. The :word:`parameter` is the analog value of the
sensor.

The :cb:`Analog Value` callback is only triggered if the current has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Analog Value Callback Period`,
ausgelöst. Der :word:`parameter` ist der Analogwert des Sensors.

Der :cb:`Analog Value` Callback wird nur ausgelöst, wenn sich der Analogwert seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Current Reached',
'elements': [('Current', 'int16', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere', 'range': (-25000, 25000)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Current Callback Threshold` is reached.
The :word:`parameter` is the current of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Current Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Stromstärke des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Analog Value Reached',
'elements': [('Value', 'uint16', 1, 'out', {'range': (0, 4095)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Analog Value Callback Threshold` is reached.
The :word:`parameter` is the analog value of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Analog Value Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist der Analogwert des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Over Current',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when an over current is measured
(see :func:`Is Over Current`).
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn ein Überstrom gemessen wurde
(siehe :func:`Is Over Current`).
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Current', 'current'), [(('Current', 'Current'), 'int16', 1, 1000.0, 'A', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Current', 'current'), [(('Current', 'Current'), 'int16', 1, 1000.0, 'A', None)], None, None),
              ('callback_period', ('Current', 'current'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('Current Reached', 'current reached'), [(('Current', 'Current'), 'int16', 1, 1000.0, 'A', None)], None, None),
              ('callback_threshold', ('Current', 'current'), [], '>', [(5, 0)])]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.OpenClosedType'],
    'param_groups': oh_generic_channel_param_groups(),
    'channels': [
        oh_generic_old_style_channel('Current', 'Current', cast_literal='(short)'),
        {
            'id': 'Over Current',
            'type': 'Over Current',

            'getters': [{
                'packet': 'Is Over Current',
                'element': 'Over',
                'transform': 'value ? OpenClosedType.CLOSED : OpenClosedType.OPEN'}],

            'callbacks': [{
                'packet': 'Over Current',
                'transform': 'OpenClosedType.CLOSED'}]
        },
        oh_analog_value_channel()
    ],
    'channel_types': [
        oh_generic_channel_type('Current', 'Number', {'en': 'Current', 'de': 'Stromstärke'},
                    update_style='Callback Period',
                    description={'en': 'The measured current.', 'de': 'Die gemessene Stromstärke.'}),
        oh_generic_channel_type('Over Current', 'Contact', {'en': 'Over Current', 'de': 'Überstrom'},
                    update_style=None,
                    description={'en': 'Enabled if more than 25A were measured. To reset this value you have to power cycle the Bricklet.',
                                 'de': 'Aktiviert, wenn mehr als 25A gemessen wurden. Um diesen Wert zurückzusetzen ist ein Aus- und Wiedereinschalten des Bricklet notwendig.'}),
        oh_analog_value_channel_type(analog_value_desc)
    ],
    'actions': ['Get Current', 'Is Over Current', 'Get Analog Value']
}

