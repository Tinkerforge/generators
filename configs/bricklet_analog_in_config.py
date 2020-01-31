# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Analog In Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 3],
    'api_version_extra': 1, # +1 for "Break API to fix threshold min/max type mismatch [59d13f6]"
    'category': 'Bricklet',
    'device_identifier': 219,
    'name': 'Analog In',
    'display_name': 'Analog In',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures DC voltage between 0V and 45V',
        'de': 'Misst Gleichspannung zwischen 0V und 45V'
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

com['constant_groups'].append({
'name': 'Range',
'type': 'uint8',
'constants': [('Automatic', 0),
              ('Up To 6V', 1),
              ('Up To 10V', 2),
              ('Up To 36V', 3),
              ('Up To 45V', 4),
              ('Up To 3V', 5)]
})

com['packets'].append({
'type': 'function',
'name': 'Get Voltage',
'elements': [('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt', 'range': (0, 45000)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the voltage of the sensor. The resolution between 0 and 6V is about 2mV.
Between 6 and 45V the resolution is about 10mV.

If you want to get the voltage periodically, it is recommended to use the
:cb:`Voltage` callback and set the period with
:func:`Set Voltage Callback Period`.
""",
'de':
"""
Gibt die gemessene Spannung des Sensors zurück. Die Auflösung im Bereich 0 bis 6V beträgt rund 2mV.
Zwischen 6 und 45V ist die Auflösung rund 10mV.

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
'elements': [('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt', 'range': (0, 45000)})],
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
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Voltage Callback Period`, ausgelöst. Der :word:`parameter` ist die
gemessene Spannung des Sensors.

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
:func:`Set Analog Value Callback Period`. The :word:`parameter` is the analog
value of the sensor.

The :cb:`Analog Value` callback is only triggered if the voltage has changed
since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Analog Value Callback Period`, ausgelöst. Der :word:`parameter`
ist der Analogwert des Sensors.

Der :cb:`Analog Value` Callback wird nur ausgelöst, wenn sich der Analogwert
seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Voltage Reached',
'elements': [('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt', 'range': (0, 45000)})],
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

com['packets'].append({
'type': 'function',
'name': 'Set Range',
'elements': [('Range', 'uint8', 1, 'in', {'constant_group': 'Range', 'default': 0})],
'since_firmware': [2, 0, 1],
'doc': ['bf', {
'en':
"""
Sets the measurement range. Possible ranges:

* 0: Automatically switched
* 1: 0V - 6.05V, ~1.48mV resolution
* 2: 0V - 10.32V, ~2.52mV resolution
* 3: 0V - 36.30V, ~8.86mV resolution
* 4: 0V - 45.00V, ~11.25mV resolution
* 5: 0V - 3.3V, ~0.81mV resolution, new in version 2.0.3$nbsp;(Plugin)
""",
'de':
"""
Setzt den Messbereich. Mögliche Bereiche:

* 0: Automatisch geschaltet
* 1: 0V - 6,05V, ~1,48mV Auflösung
* 2: 0V - 10,32V, ~2,52mV Auflösung
* 3: 0V - 36,30V, ~8,86mV Auflösung
* 4: 0V - 45,00V, ~11,25mV Auflösung
* 5: 0V - 3,3V, ~0,81mV Auflösung, neu in Version 2.0.3$nbsp;(Plugin)
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Range',
'elements': [('Range', 'uint8', 1, 'out', {'constant_group': 'Range', 'default': 0})],
'since_firmware': [2, 0, 1],
'doc': ['bf', {
'en':
"""
Returns the measurement range as set by :func:`Set Range`.
""",
'de':
"""
Gibt den Messbereich zurück, wie von :func:`Set Range` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Averaging',
'elements': [('Average', 'uint8', 1, 'in', {'default': 50})],
'since_firmware': [2, 0, 3],
'doc': ['af', {
'en':
"""
Set the length of a averaging for the voltage value.

Setting the length to 0 will turn the averaging completely off. If the
averaging is off, there is more noise on the data, but the data is without
delay.
""",
'de':
"""
Setzt die Länge des Mittelwerts für die Spannung.

Wenn die Länge auf 0 gesetzt wird, ist das Averaging komplett aus. In diesem
Fall gibt es mehr Rauschen auf den Daten, allerdings sind die Daten dann ohne
Verzögerung.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Averaging',
'elements': [('Average', 'uint8', 1, 'out', {'default': 50})],
'since_firmware': [2, 0, 3],
'doc': ['af', {
'en':
"""
Returns the averaging configuration as set by :func:`Set Averaging`.
""",
'de':
"""
Gibt die Averaging-Konfiguration zurück, wie von :func:`Set Averaging` gesetzt.
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
              ('callback_threshold', ('Voltage', 'voltage'), [], '<', [(5, 0)])]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'params': [{
            'packet': 'Set Averaging',
            'element': 'Average',

            'name': 'Average Length',
            'type': 'integer',
            'default': 50,

            'label': 'Average Length',
            'description': 'The length of a averaging for the voltage value.<br/><br/>Setting the length to 0 will turn the averaging completely off. If the averaging is off, there is more noise on the data, but the data is without delay.<br/><br/>The default value is 50.'
        },{
            'packet': 'Set Range',
            'element': 'Range',

            'name': 'Measurement Range',
            'type': 'integer',
            'options': [('Automatic', 0),
                        ('Up To 6V', 1),
                        ('Up To 10V', 2),
                        ('Up To 36V', 3),
                        ('Up To 45V', 4),
                        ('Up To 3V', 5)],
            'limitToOptions': 'true',
            'default': 0,

            'label': 'Measurement Range',
            'description': 'The measurement range.<br/><br/>Possible ranges are: <ul><li>Automatically switched</li><li>0V - 6.05V, ~1.48mV resolution</li><li>0V - 10.32V, ~2.52mV resolution</li><li>0V - 36.30V, ~8.86mV resolution</li><li>- 45.00V, ~11.25mV resolution</li><li>0V - 3.3V, ~0.81mV resolution</li>',
        }
        ],
    'channels': [
        oh_generic_old_style_channel('Voltage', 'Voltage', 'SmartHomeUnits.VOLT', divisor=1000.0),
    ],
    'init_code': """this.setAveraging(cfg.averageLength);
    this.setRange(cfg.measurementRange);""",
    'channel_types': [
        oh_generic_channel_type('Voltage', 'Number:ElectricPotential', 'Voltage',
                    update_style='Callback Period',
                    description='Measured voltage',
                    read_only=True,
                    pattern='%.2f %unit%',
                    min_=0,
                    max_=42)
    ],
    'actions': ['Get Voltage', 'Get Analog Value', 'Get Averaging']
}
