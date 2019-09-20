# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Heart Rate Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP

com = {
    'author': 'Ishraq Ibne Ashraf <ishraq@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 245,
    'name': 'Heart Rate',
    'display_name': 'Heart Rate',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures heart rate',
        'de': 'Misst Herzfrequenz'
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
'name': 'Beat State',
'type': 'uint8',
'constants': [('Falling', 0),
              ('Rising', 1)]
})

com['packets'].append({
'type': 'function',
'name': 'Get Heart Rate',
'elements': [('Heart Rate', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current heart rate measured.

If you want to get the heart rate periodically, it is recommended
to use the :cb:`Heart Rate` callback and set the period with
:func:`Set Heart Rate Callback Period`.
""",
'de':
"""
Gibt die Herzschlagfrequenz des Sensors zurück.

Wenn die Herzschlagfrequenz periodisch abgefragt werden soll,
wird empfohlen den :cb:`Heart Rate` Callback zu nutzen und die Periode
mit :func:`Set Heart Rate Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Heart Rate Callback Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :cb:`Heart Rate` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Heart Rate` callback is only triggered if the heart rate has changed
since the last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :cb:`Heart Rate` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Heart Rate` Callback wird nur ausgelöst, wenn sich die
Herzschlagfrequenz seit der letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Heart Rate Callback Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Heart Rate Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Heart Rate Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Heart Rate Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option'}),
             ('Min', 'uint16', 1, 'in'),
             ('Max', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Heart Rate Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the heart rate is *outside* the min and max values"
 "'i'",    "Callback is triggered when the heart rate is *inside* the min and max values"
 "'<'",    "Callback is triggered when the heart rate is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the heart rate is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Heart Rate Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn die Herzschlagfrequenz *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn die Herzschlagfrequenz *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn die Herzschlagfrequenz kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn die Herzschlagfrequenz größer als der min Wert ist (max wird ignoriert)"

Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Heart Rate Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option'}),
             ('Min', 'uint16', 1, 'out'),
             ('Max', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Heart Rate Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Heart Rate Callback Threshold` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Debounce Period',
'elements': [('Debounce', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the threshold callback

* :cb:`Heart Rate Reached`

is triggered, if the threshold

* :func:`Set Heart Rate Callback Threshold`

keeps being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callback

* :cb:`Heart Rate Reached`

ausgelöst wird, wenn der Schwellwert

* :func:`Set Heart Rate Callback Threshold`

weiterhin erreicht bleibt.

Der Standardwert ist 100.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Debounce Period',
'elements': [('Debounce', 'uint32', 1, 'out')],
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
'name': 'Heart Rate',
'elements': [('Heart Rate', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Heart Rate Callback Period`. The :word:`parameter` is the heart rate
of the sensor.

The :cb:`Heart Rate` callback is only triggered if the heart rate has changed
since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Heart Rate Callback Period`, ausgelöst. Der :word:`parameter` ist
die Herzschlagfrequenz des Sensors.

Der :cb:`Heart Rate` Callback wird nur ausgelöst, wenn sich die
Herzschlagfrequenz seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Heart Rate Reached',
'elements': [('Heart Rate', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Heart Rate Callback Threshold` is reached.
The :word:`parameter` is the heart rate of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Heart Rate Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Herzschlagfrequenz des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Beat State Changed',
'elements': [('State', 'uint8', 1, 'out', {'constant_group': 'Beat State'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback provides the current heart beat state.It is called
every time a heart beat is detected. The state can either be

* 0 = Falling: The falling edge of a detected heart beat.
* 1 = Rising: The rising edge of a detected heart beat.
""",
'de':
"""
Dieser Callback übergibt den aktuellen Tilt-Status. Der Callback wird
aufgerufen wenn sich der Status ändert. Der Zustand kann folgende Werte
annehmen:

* 0 = Falling:
* 1 = Rising:
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Enable Beat State Changed Callback',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Enables the :cb:`Beat State Changed` callback.
""",
'de':
"""
Aktiviert den :cb:`Beat State Changed` Callback.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Disable Beat State Changed Callback',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Disables the :cb:`Beat State Changed` callback.
""",
'de':
"""
Deaktiviert den :cb:`Beat State Changed` Callback.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is Beat State Changed Callback Enabled',
'elements': [('Enabled', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns *true* if the :cb:`Beat State Changed` callback is enabled.
""",
'de':
"""
Gibt *true* zurück wenn der :cb:`Beat State Changed` Callback aktiviert ist.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Heart Rate', 'heart rate'), [(('Heart Rate', 'Heart Rate'), 'uint16', 1, None, 'bpm', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Heart Rate', 'heart rate'), [(('Heart Rate', 'Heart Rate'), 'uint16', 1, None, 'bpm', None)], None, None),
              ('callback_period', ('Heart Rate', 'heart rate'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('Heart Rate Reached', 'heart rate reached'), [(('Heart Rate', 'Heart Rate'), 'uint16', 1, None, 'bpm', None)], None, None),
              ('callback_threshold', ('Heart Rate', 'heart rate'), [], '>', [(100, 0)])]
})
