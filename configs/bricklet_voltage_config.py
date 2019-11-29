# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Voltage Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'api_version_extra': 1, # +1 for "Break API to fix threshold min/max type mismatch [59d13f6]"
    'category': 'Bricklet',
    'device_identifier': 218,
    'name': 'Voltage',
    'display_name': 'Voltage',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures DC voltage between 0V and 50V',
        'de': 'Misst Gleichspannung zwischen 0V und 50V'
    },
    'released': True,
    'documented': True,
    'discontinued': True, # replaced by Analog In Bricklet 3.0
    'features': [
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

com['packets'].append({
'type': 'function',
'name': 'Get Voltage',
'elements': [('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt', 'range': (0, 50000)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the voltage of the sensor.

If you want to get the voltage periodically, it is recommended to use the
:cb:`Voltage` callback and set the period with
:func:`Set Voltage Callback Period`.
""",
'de':
"""
Gibt die gemessene Spannung des Sensors zurück.

Wenn die Spannung periodisch abgefragt werden soll, wird empfohlen
den :cb:`Voltage` Callback zu nutzen und die Periode mit
:func:`Set Voltage Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Analog Value',
'elements': [('Value', 'uint16', 1, 'out', {'range': (0, 4095)})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the value as read by a 12-bit analog-to-digital converter.

.. note::
 The value returned by :func:`Get Voltage` is averaged over several samples
 to yield less noise, while :func:`Get Analog Value` gives back raw
 unfiltered analog values. The only reason to use :func:`Get Analog Value` is,
 if you need the full resolution of the analog-to-digital converter.

If you want the analog value periodically, it is recommended to use the
:cb:`Analog Value` callback and set the period with
:func:`Set Analog Value Callback Period`.
""",
'de':
"""
Gibt den Wert, wie vom 12-Bit Analog-Digital-Wandler gelesen, zurück.

.. note::
 Der von :func:`Get Voltage` zurückgegebene Wert ist über mehrere
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
'name': 'Set Voltage Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Voltage` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Voltage` callback is only triggered if the voltage has changed since
the last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Voltage` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Voltage` Callback wird nur ausgelöst, wenn sich die Spannung seit der
letzten Auslösung geändert hat.

"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Voltage Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
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
'name': 'Set Voltage Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Volt', 'default': 0}),
             ('Max', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Volt', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Voltage Reached` callback.

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
Setzt den Schwellwert für den :cb:`Voltage Reached` Callback.

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
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt', 'default': 0}),
             ('Max', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt', 'default': 0})],
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
'name': 'Set Analog Value Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'in', {'default': 0}),
             ('Max', 'uint16', 1, 'in', {'default': 0})],
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
             ('Min', 'uint16', 1, 'out', {'default': 0}),
             ('Max', 'uint16', 1, 'out', {'default': 0})],
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

* :cb:`Voltage Reached`,
* :cb:`Analog Value Reached`

are triggered, if the thresholds

* :func:`Set Voltage Callback Threshold`,
* :func:`Set Analog Value Callback Threshold`

keep being reached.
""",
'de':
"""
Setzt die Periode mit welcher die Schwellwert Callbacks

* :cb:`Voltage Reached`,
* :cb:`Analog Value Reached`

ausgelöst werden, wenn die Schwellwerte

* :func:`Set Voltage Callback Threshold`,
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
'name': 'Voltage',
'elements': [('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt', 'range': (0, 50000)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Voltage Callback Period`. The :word:`parameter` is the voltage of the
sensor.

The :cb:`Voltage` callback is only triggered if the voltage has changed since
the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Voltage Callback Period`,
ausgelöst. Der :word:`parameter` ist die gemessene Spannung des Sensors.

Der :cb:`Voltage` Callback wird nur ausgelöst, wenn sich die Spannung seit der
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
:func:`Set Analog Value Callback Period`. The :word:`parameter` is the
analog value of the sensor.

The :cb:`Analog Value` callback is only triggered if the voltage has changed
since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Analog Value Callback Period`,
ausgelöst. Der :word:`parameter` ist der Analogwert des Sensors.

Der :cb:`Analog Value` Callback wird nur ausgelöst, wenn sich der Analogwert
seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Voltage Reached',
'elements': [('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt', 'range': (0, 50000)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Voltage Callback Threshold` is reached.
The :word:`parameter` is the voltage of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Voltage Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die gemessene Spannung des Sensors.

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

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Voltage', 'voltage'), [(('Voltage', 'Voltage'), 'uint16', 1, 1000.0, 'V', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Voltage', 'voltage'), [(('Voltage', 'Voltage'), 'uint16', 1, 1000.0, 'V', None)], None, None),
              ('callback_period', ('Voltage', 'voltage'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('Voltage Reached', 'voltage reached'), [(('Voltage', 'Voltage'), 'uint16', 1, 1000.0, 'V', None)], None, None),
              ('callback_threshold', ('Voltage', 'voltage'), [], '>', [(5, 0)])]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'channels': [
        oh_generic_old_style_channel('Voltage', 'Voltage', 'SmartHomeUnits.VOLT', divisor=1000.0),
    ],
    'channel_types': [
        oh_generic_channel_type('Voltage', 'Number:ElectricPotential', 'Voltage',
                     description='Measured voltage',
                     read_only=True,
                     pattern='%.2f %unit%',
                     min_=0,
                     max_=50)
    ],
    'actions': ['Get Voltage', 'Get Analog Value']
}
