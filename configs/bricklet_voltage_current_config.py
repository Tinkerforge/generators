# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Voltage/Current Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 227,
    'name': 'Voltage Current',
    'display_name': 'Voltage/Current',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures power, DC voltage and DC current up to 720W/36V/20A',
        'de': 'Misst Leistung, Gleichspannung und Gleichstrom bis zu 720W/36V/20A'
    },
    'released': True,
    'documented': True,
    'discontinued': True, # replaced by Voltage/Current Bricklet 2.0
    'features': [
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append({
'name': 'Averaging',
'type': 'uint8',
'constants': [('1', 0),
              ('4', 1),
              ('16', 2),
              ('64', 3),
              ('128', 4),
              ('256', 5),
              ('512', 6),
              ('1024', 7)]
})

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

com['constant_groups'].append({
'name': 'Conversion Time',
'type': 'uint8',
'constants': [('140us', 0),
              ('204us', 1),
              ('332us', 2),
              ('588us', 3),
              ('1 1ms', 4),
              ('2 116ms', 5),
              ('4 156ms', 6),
              ('8 244ms', 7)]
})

com['packets'].append({
'type': 'function',
'name': 'Get Current',
'elements': [('Current', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere', 'range': (-20000, 20000)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current.

If you want to get the current periodically, it is recommended to use the
:cb:`Current` callback and set the period with
:func:`Set Current Callback Period`.
""",
'de':
"""
Gibt die gemessenen Stromstärke zurück.

Wenn die Stromstärke periodisch abgefragt werden soll, wird empfohlen
den :cb:`Current` Callback zu nutzen und die Periode mit
:func:`Set Current Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Voltage',
'elements': [('Voltage', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt', 'range': (0, 36000)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the voltage.

If you want to get the voltage periodically, it is recommended to use the
:cb:`Voltage` callback and set the period with
:func:`Set Voltage Callback Period`.
""",
'de':
"""
Gibt die gemessenen Spannung zurück.

Wenn die Spannung periodisch abgefragt werden soll, wird empfohlen
den :cb:`Voltage` Callback zu nutzen und die Periode mit
:func:`Set Voltage Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Power',
'elements': [('Power', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Watt', 'range': (0, 720000)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the power.

If you want to get the power periodically, it is recommended to use the
:cb:`Power` callback and set the period with
:func:`Set Power Callback Period`.
""",
'de':
"""
Gibt die gemessenen Leistung zurück.

Wenn die Leistung periodisch abgefragt werden soll, wird empfohlen
den :cb:`Power` Callback zu nutzen und die Periode mit
:func:`Set Power Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('Averaging', 'uint8', 1, 'in', {'constant_group': 'Averaging', 'default': 3}),
             ('Voltage Conversion Time', 'uint8', 1, 'in', {'constant_group': 'Conversion Time', 'default': 4}),
             ('Current Conversion Time', 'uint8', 1, 'in', {'constant_group': 'Conversion Time', 'default': 4})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the configuration of the Voltage/Current Bricklet. It is
possible to configure number of averages as well as
voltage and current conversion time.
""",
'de':
"""
Setzt die Konfiguration des Voltage/Current Bricklet. Es ist
möglich die Anzahl für die Durchschnittsbildung, und die
Wandlungszeit für Spannung und Stromstärke zu definieren.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Averaging', 'uint8', 1, 'out', {'constant_group': 'Averaging', 'default': 3}),
             ('Voltage Conversion Time', 'uint8', 1, 'out', {'constant_group': 'Conversion Time', 'default': 4}),
             ('Current Conversion Time', 'uint8', 1, 'out', {'constant_group': 'Conversion Time', 'default': 4})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
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
'name': 'Set Calibration',
'elements': [('Gain Multiplier', 'uint16', 1, 'in', {}),
             ('Gain Divisor', 'uint16', 1, 'in', {})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Since the shunt resistor that is used to measure the current is not
perfectly precise, it needs to be calibrated by a multiplier and
divisor if a very precise reading is needed.

For example, if you are expecting a measurement of 1000mA and you
are measuring 1023mA, you can calibrate the Voltage/Current Bricklet
by setting the multiplier to 1000 and the divisor to 1023.
""",
'de':
"""
Da der Shunt-Widerstand über den die Stromstärke gemessen wird keine
perfekte Genauigkeit hat, ist es nötig einen Multiplikator und
einen Divisor zu setzen, falls sehr genaue Messwerte nötig sind.

Zum Beispiel: Wenn eine Messung von 1000mA erwartet wird, das
Voltage/Current Bricklet aber 1023mA zurück gibt, sollte
der Multiplikator auf 1000 und der Divisor auf 1023 gesetzt
werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Calibration',
'elements': [('Gain Multiplier', 'uint16', 1, 'out', {}),
             ('Gain Divisor', 'uint16', 1, 'out', {})],
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
Gibt die Periode zurück, wie von :func:`Set Current Callback Period` gesetzt
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
Gibt die Periode zurück, wie von :func:`Set Voltage Callback Period` gesetzt
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Power Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Power` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Power` callback is only triggered if the power has changed since the
last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Power` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Power` Callback wird nur ausgelöst, wenn sich die Leistung seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Power Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Get Power Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Get Power Callback Period` gesetzt
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Current Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'int32', 1, 'in', {'scale': (1, 1000), 'unit': 'Ampere', 'default': 0}),
             ('Max', 'int32', 1, 'in', {'scale': (1, 1000), 'unit': 'Ampere', 'default': 0})],
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
             ('Min', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere', 'default': 0}),
             ('Max', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere', 'default': 0})],
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
'name': 'Set Voltage Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'int32', 1, 'in', {'scale': (1, 1000), 'unit': 'Volt', 'default': 0}),
             ('Max', 'int32', 1, 'in', {'scale': (1, 1000), 'unit': 'Volt', 'default': 0})],
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
             ('Min', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt', 'default': 0}),
             ('Max', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt', 'default': 0})],
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
'name': 'Set Power Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'int32', 1, 'in', {'scale': (1, 1000), 'unit': 'Watt', 'default': 0}),
             ('Max', 'int32', 1, 'in', {'scale': (1, 1000), 'unit': 'Watt', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Power Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the power is *outside* the min and max values"
 "'i'",    "Callback is triggered when the power is *inside* the min and max values"
 "'<'",    "Callback is triggered when the power is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the power is greater than the min value (max is ignored)"
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Power Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn die Leistung *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn die Leistung *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn die Leistung kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn die Leistung größer als der min Wert ist (max wird ignoriert)"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Power Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Watt', 'default': 0}),
             ('Max', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Watt', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Power Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Power Callback Threshold` gesetzt.
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
* :cb:`Voltage Reached`,
* :cb:`Power Reached`

are triggered, if the thresholds

* :func:`Set Current Callback Threshold`,
* :func:`Set Voltage Callback Threshold`,
* :func:`Set Power Callback Threshold`

keep being reached.
""",
'de':
"""
Setzt die Periode mit welcher die Schwellwert Callbacks

* :cb:`Current Reached`,
* :cb:`Voltage Reached`,
* :cb:`Power Reached`

ausgelöst werden, wenn die Schwellwerte

* :func:`Set Current Callback Threshold`,
* :func:`Set Voltage Callback Threshold`,
* :func:`Set Power Callback Threshold`

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
'elements': [('Current', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere', 'range': (-20000, 20000)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Current Callback Period`. The :word:`parameter` is the current of the
sensor.

The :cb:`Current` callback is only triggered if the current has changed since
the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Current Callback Period`, ausgelöst. Der :word:`parameter` ist
die Stromstärke des Sensors.

Der :cb:`Current` Callback wird nur ausgelöst, wenn sich die Stromstärke seit
der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Voltage',
'elements': [('Voltage', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt', 'range': (0, 36000)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Voltage Callback Period`. The :word:`parameter` is the voltage of
the sensor.

The :cb:`Voltage` callback is only triggered if the voltage has changed since
the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Voltage Callback Period`, ausgelöst. Der :word:`parameter` ist
die Spannung des Sensors.

Der :cb:`Voltage` Callback wird nur ausgelöst, wenn sich die Spannung seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Power',
'elements': [('Power', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Watt', 'range': (0, 720000)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Power Callback Period`. The :word:`parameter` is the power of the
sensor.

The :cb:`Power` callback is only triggered if the power has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Power Callback Period`, ausgelöst. Der :word:`parameter` ist die
Leistung des Sensors.

Der :cb:`Power` Callback wird nur ausgelöst, wenn sich die Leistung seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Current Reached',
'elements': [('Current', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere', 'range': (-20000, 20000)})],
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
'name': 'Voltage Reached',
'elements': [('Voltage', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt', 'range': (0, 36000)})],
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
Der :word:`parameter` ist die Spannung des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Power Reached',
'elements': [('Power', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere', 'range': (-20000, 20000)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Power Callback Threshold` is reached.
The :word:`parameter` is the power of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Power Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Spannung des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Voltage', 'voltage'), [(('Voltage', 'Voltage'), 'int32', 1, 1000.0, 'V', None)], []),
              ('getter', ('Get Current', 'current'), [(('Current', 'Current'), 'int32', 1, 1000.0, 'A', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Current', 'current'), [(('Current', 'Current'), 'int32', 1, 1000.0, 'A', None)], None, None),
              ('callback_period', ('Current', 'current'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('Power Reached', 'power reached'), [(('Power', 'Power'), 'int32', 1, 1000.0, 'W', None)], None, None),
              ('callback_threshold', ('Power', 'power'), [], '>', [(10, 0)])]
})


com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'params': [
        {
            'name': 'Averaging',
            'type': 'integer',
            'options': [('1', 0),
                        ('4', 1),
                        ('16', 2),
                        ('64', 3),
                        ('128', 4),
                        ('256', 5),
                        ('512', 6),
                        ('1024', 7)],
            'limitToOptions': 'true',
            'default': '3',

            'label': 'Averaging',
            'description': 'Configures the number of samples to average over.'
        }, {
            'name': 'Voltage Conversion Time',
            'type': 'integer',
            'options': [('140µs', 0),
                        ('204µs', 1),
                        ('332µs', 2),
                        ('588µs', 3),
                        ('1.1ms', 4),
                        ('2.116ms', 5),
                        ('4.156ms', 6),
                        ('8.244ms', 7)],
            'limitToOptions': 'true',
            'default': '4',

            'label': 'Voltage Conversion Time',
            'description': 'Configures the voltage conversion time.'
        }, {
            'name': 'Current Conversion Time',
            'type': 'integer',
            'options': [('140µs', 0),
                        ('204µs', 1),
                        ('332µs', 2),
                        ('588µs', 3),
                        ('1.1ms', 4),
                        ('2.116ms', 5),
                        ('4.156ms', 6),
                        ('8.244ms', 7)],
            'limitToOptions': 'true',
            'default': '4',

            'label': 'Current Conversion Time',
            'description': 'Configures the current conversion time.'
        },
    ],
    'init_code': """this.setConfiguration(cfg.averaging.shortValue(), cfg.voltageConversionTime.shortValue(), cfg.currentConversionTime.shortValue());""",
    'channels': [
        oh_generic_old_style_channel('Current', 'Current', 'SmartHomeUnits.AMPERE', divisor=1000.0),
        oh_generic_old_style_channel('Voltage', 'Voltage', 'SmartHomeUnits.VOLT', divisor=1000.0),
        oh_generic_old_style_channel('Power', 'Power', 'SmartHomeUnits.WATT', divisor=1000.0)
    ],
    'channel_types': [
        oh_generic_channel_type('Voltage', 'Number:ElectricPotential', 'Measured Voltage', description='The measured voltage between 0 and 36V.',
                     read_only=True,
                     pattern='%.3f %unit%',
                     min_=0,
                     max_=36),
        oh_generic_channel_type('Current', 'Number:ElectricCurrent', 'Measured Current', description='The measured current between -20 and 20A.',
                     read_only=True,
                     pattern='%.3f %unit%',
                     min_=-20,
                     max_=20),
        oh_generic_channel_type('Power', 'Number:Power', 'Measured Power', description='The measured power between 0 and 720W.',
                     read_only=True,
                     pattern='%.3f %unit%',
                     min_=0,
                     max_=720)
    ],
    'actions': ['Get Voltage', 'Get Current', 'Get Power', 'Get Configuration', 'Get Calibration']
}
