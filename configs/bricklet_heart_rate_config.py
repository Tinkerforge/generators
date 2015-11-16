# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Heart Rate Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS

com = {
    'author': 'Ishraq Ibne Ashraf <ishraq@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 245,
    'name': ('Heart Rate', 'Heart Rate', 'Heart Rate Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures heart rate',
        'de': 'Misst Herzfrequenz'
    },
    'released': False,
    'packets': [],
    'examples': []
}

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
to use the callback :func:`HeartRate` and set the period with 
:func:`SetHeartRateCallbackPeriod`.
""",
'de':
"""
Gibt die Herzschlagfrequenz des Sensors zurück.

Wenn die Herzschlagfrequenz periodisch abgefragt werden soll,
wird empfohlen den Callback :func:`HeartRate` zu nutzen und die Periode
mit :func:`SetHeartRateCallbackPeriod` vorzugeben.
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
Sets the period in ms with which the :func:`HeartRate` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`HeartRate` is only triggered if the heart rate has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`HeartRate` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`HeartRate` wird nur ausgelöst wenn sich die Herzschlagfrequenz seit der
letzten Auslösung geändert hat.

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
Returns the period as set by :func:`SetHeartRateCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetHeartRateCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Heart Rate Callback Threshold',
'elements': [('Option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint16', 1, 'in'),
             ('Max', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`HeartRateReached` callback. 

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
Setzt den Schwellwert für den :func:`HeartRateReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Herzschlagfrequenz *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn die Herzschlagfrequenz *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn die Herzschlagfrequenz kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Herzschlagfrequenz größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Heart Rate Callback Threshold',
'elements': [('Option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint16', 1, 'out'),
             ('Max', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`SetHeartRateCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetHeartRateCallbackThreshold`
gesetzt.
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

* :func:`HeartRateReached`

is triggered, if the threshold

* :func:`SetHeartRateCallbackThreshold`

keeps being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callback

* :func:`HeartRateReached`
 
ausgelöst wird, wenn der Schwellwert 

* :func:`SetHeartRateCallbackThreshold`
 
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
Returns the debounce period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Gibt die Entprellperiode zurück, wie von :func:`SetDebouncePeriod`
gesetzt.
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
:func:`SetHeartRateCallbackPeriod`. The :word:`parameter` is the heart rate
of the sensor.

:func:`HeartRate` is only triggered if the heart rate has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`SetHeartRateCallbackPeriod`, ausgelöst. Der :word:`parameter` ist
die Herzschlagfrequenz des Sensors.

:func:`HeartRate` wird nur ausgelöst wenn sich die Herzschlagfrequenz
seit der letzten Auslösung geändert hat.
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
:func:`SetHeartRateCallbackThreshold` is reached.
The :word:`parameter` is the heart rate of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetHeartRateCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Herzschlagfrequenz des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Beat State Changed',
'elements': [('State', 'uint8', 1, 'out', ('Beat State', [('Falling', 0),
                                                          ('Rising', 1)]))],
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
Enables the :func:`BeatStateChanged` callback.
""",
'de':
"""
Aktiviert den :func:`BeatStateChanged` Callback.
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
Disables the :func:`BeatStateChanged` callback.
""",
'de':
"""
Deaktiviert den :func:`BeatStateChanged` Callback.
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
Returns *true* if the :func:`BeatStateChanged` callback is enabled.
""",
'de':
"""
Gibt *true* zurück wenn der :func:`BeatStateChanged` Callback aktiviert ist.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Heart Rate', 'heart rate'), [(('Heart Rate', 'Heart Rate'), 'uint16', None, 'bpm', 'bpm', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Heart Rate', 'heart rate'), [(('Heart Rate', 'Heart Rate'), 'uint16', None, 'bpm', 'bpm', None)], None, None),
              ('callback_period', ('Heart Rate', 'heart rate'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('Heart Rate Reached', 'heart rate reached'), [(('Heart Rate', 'Heart Rate'), 'uint16', None, 'bpm', 'bpm', None)], None, None),
              ('callback_threshold', ('Heart Rate', 'heart rate'), [], '>', [(100, 0)])]
})
