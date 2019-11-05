# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Gas Detector Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 252,
    'name': 'Gas Detector',
    'display_name': 'Gas Detector',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures concentration of different gases',
        'de': 'Misst Konzentration verschiedener Gase'
    },
    'released': False,
    'documented': False,
    'discontinued': False,
    'features': [
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

com['constant_groups'].append({
'name': 'Detector Type',
'type': 'uint8',
'constants': [('0', 0),
              ('1', 1)]
})

com['packets'].append({
'type': 'function',
'name': 'Get Value',
'elements': [('Value', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns a value between 0 and 4095.

See `here <TODO>`__ for more information about the measurements.

If you want to get the value periodically, it is recommended
to use the :cb:`Value` callback and set the period with
:func:`Set Value Callback Period`.
""",
'de':
"""
Gibt einen Wert zwischen 0 und 4095 zurück.

Siehe `hier <TODO>`__ für mehr Informationen zu den Messwerten.

Wenn der Wert periodisch abgefragt werden soll, wird empfohlen
den :cb:`Value` Callback zu nutzen und die Periode mit
:func:`Set Value Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Value Callback Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :cb:`Value` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Value` callback is only triggered if the value value has changed
since the last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :cb:`Value` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Value` Callback wird nur ausgelöst, wenn sich der Wert seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Value Callback Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Value Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Value Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Value Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'in'),
             ('Max', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Value Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the value value is *outside* the min and max values"
 "'i'",    "Callback is triggered when the value value is *inside* the min and max values"
 "'<'",    "Callback is triggered when the value value is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the value value is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Value Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn der Wert *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn der Wert *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn der Wert kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn der Wert größer als der min Wert ist (max wird ignoriert)"

Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Value Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'out'),
             ('Max', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Value Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Value Callback Threshold` gesetzt.
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

* :cb:`Value Reached`

is triggered, if the threshold

* :func:`Set Value Callback Threshold`

keeps being reached.
""",
'de':
"""
Setzt die Periode mit welcher die Schwellwert Callback

* :cb:`Value Reached`

ausgelöst wird, wenn der Schwellwert

* :func:`Set Value Callback Threshold`

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
'name': 'Set Moving Average',
'elements': [('Average', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
for the measured value.

Setting the length to 1 will turn the averaging off. With less
averaging, there is more noise on the data.

The range for the averaging is 1-100.

The default value is 100.
""",
'de':
"""
Setzt die Länge eines `gleitenden Mittelwerts <https://de.wikipedia.org/wiki/Gleitender_Mittelwert>`__
für den gemessenen Wert.

Wenn die Länge auf 1 gesetzt wird, ist das Averaging aus. Desto kleiner
die Länge des Mittelwerts ist, desto mehr Rauschen ist auf den Daten.

Der Wertebereich liegt bei 1-100.

Der Standardwert ist 100.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Moving Average',
'elements': [('Average', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the length moving average as set by :func:`Set Moving Average`.
""",
'de':
"""
Gibt die Länge des gleitenden Mittelwerts zurück, wie von
:func:`Set Moving Average` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Detector Type',
'elements': [('Detector Type', 'uint8', 1, 'in', {'constant_group': 'Detector Type'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the detector type.

The following types are currently supported.

* Type 0: MQ2 and MQ5
* Type 1: MQ3

The detector type is written to the EEPROM of the Bricklet, so it only has
to be set once.

You can use the Brick Viewer to set the detector type, so you likely
don't need to use this function in your source code.

The default detector type is 0.
""",
'de':
"""
Setzt den Detektortyp

Die folgenden Typen werden aktuell unterstützt:

* Typ 0: MQ2 und MQ5
* Typ 1: MQ3

Der Detektortyp wird in das EEPROM des Bricklets geschrieben und muss
daher nur einmal gesetzt werden.

Wir empfehlen den Typ des Detektors im Brick Viewer zu setzen anstatt
diese Funktion zu nutzen.

Der standard Detektortyp ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Detector Type',
'elements': [('Detector Type', 'uint8', 1, 'out', {'constant_group': 'Detector Type'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the detector type as set by :func:`Set Detector Type`.
""",
'de':
"""
Gibt den Detektortyp zurück, wie von :func:`Set Detector Type` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Heater On',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Turns the internal heater on.
""",
'de':
"""
Aktiviert die interne Heizung.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Heater Off',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Turns the internal heater off.
""",
'de':
"""
Deaktiviert die interne Heizung.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is Heater On',
'elements': [('Heater', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns *true* if the heater is on, *false* otherwise.
""",
'de':
"""
Gibt *true* zurück wenn die interne Heizung aktiviert ist, *false* sonst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Value',
'elements': [('Value', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Value Callback Period`. The :word:`parameter` is the value value
of the sensor.

The :cb:`Value` callback is only triggered if the value has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Value Callback Period`,
ausgelöst. Der :word:`parameter` ist der Wert.

Der :cb:`Value` Callback wird nur ausgelöst, wenn sich der Wert seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Value Reached',
'elements': [('Value', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Value Callback Threshold` is reached.
The :word:`parameter` is the value of the detector.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Value Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist der Wert des Detektors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})
