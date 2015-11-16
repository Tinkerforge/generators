# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Distance IR Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'category': 'Bricklet',
    'device_identifier': 25,
    'name': ('Distance IR', 'Distance IR', 'Distance IR Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures distance up to 150cm with infrared light',
        'de': 'Misst Entfernung bis zu 150cm mit Infrarot-Licht'
    },
    'released': True,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Get Distance',
'elements': [('Distance', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the distance measured by the sensor. The value is in mm and possible
distance ranges are 40 to 300, 100 to 800 and 200 to 1500, depending on the
selected IR sensor.

If you want to get the distance periodically, it is recommended to use the
callback :func:`Distance` and set the period with 
:func:`SetDistanceCallbackPeriod`.
""",
'de':
"""
Gibt die gemessene Entfernung des Sensors zurück. Der Wert ist in mm und die möglichen
Entfernungsbereiche sind 40 bis 300, 100 bis 800 und 200 bis 1500, in Abhängigkeit vom
gewählten IR Sensor.

Wenn die Entfernung periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`Distance` zu nutzen und die Periode mit 
:func:`SetDistanceCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Analog Value',
'elements': [('Value', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the value as read by a 12-bit analog-to-digital converter.
The value is between 0 and 4095.

.. note::
 The value returned by :func:`GetDistance` is averaged over several samples
 to yield less noise, while :func:`GetAnalogValue` gives back raw
 unfiltered analog values. The only reason to use :func:`GetAnalogValue` is,
 if you need the full resolution of the analog-to-digital converter.

If you want the analog value periodically, it is recommended to use the 
callback :func:`AnalogValue` and set the period with 
:func:`SetAnalogValueCallbackPeriod`.
""",
'de':
"""
Gibt den Wert, wie vom 12-Bit Analog-Digital-Wandler gelesen, zurück. Der
Wertebereich ist 0 bis 4095.

.. note::
 Der von :func:`GetDistance` zurückgegebene Wert ist über mehrere
 Messwerte gemittelt um das Rauschen zu vermindern, während :func:`GetAnalogValue`
 unverarbeitete Analogwerte zurück gibt. Der einzige Grund :func:`GetAnalogValue`
 zu nutzen, ist die volle Auflösung des Analog-Digital-Wandlers zu erhalten.
 
Wenn der Analogwert periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`AnalogValue` zu nutzen und die Periode mit 
:func:`SetAnalogValueCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Sampling Point',
'elements': [('Position', 'uint8', 1, 'in'),
             ('Distance', 'uint16',1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets a sampling point value to a specific position of the lookup table.
The lookup table comprises 128 equidistant analog values with
corresponding distances.

If you measure a distance of 50cm at the analog value 2048, you
should call this function with (64, 5000). The utilized analog-to-digital
converter has a resolution of 12 bit. With 128 sampling points on the
whole range, this means that every sampling point has a size of 32
analog values. Thus the analog value 2048 has the corresponding sampling
point 64 = 2048/32.

Sampling points are saved on the EEPROM of the Distance IR Bricklet and
loaded again on startup.

.. note::
 An easy way to calibrate the sampling points of the Distance IR Bricklet is
 implemented in the Brick Viewer. If you want to calibrate your Bricklet it is
 highly recommended to use this implementation.
""",
'de':
"""
Setzt einen Messpunkt für eine vorgegebene Position in der Wertetabelle.
Die Wertetabelle beinhaltet 128 äquidistante Analogwerte mit entsprechenden
Entfernungen.

Wenn eine Entfernung von 50cm bei einem Analogwert von 2048 gemessen wird, dann sollte
der Aufruf der Funktion mit (64, 5000) erfolgen. Der verwendete Analog-Digital-Wandler
hat eine Auflösung von 12 Bit. Mit 128 Messpunkten im gesamten Bereich bedeutet das, dass jeder Messpunkt
32 Analogwerte umfasst. Daher wird dem Analogwert 2048 der Messpunkt 64 = 2048/32 zugeordnet.

Messpunkte werden im EEPROM des Distance IR Bricklet gespeichert und werden bei
jedem Hochfahren geladen.

.. note::
 Ein einfacher Weg, die Messpunkte des Distance IR Bricklet zu kalibrieren, ist im Brick Viewer
 implementiert. Wenn der Bricklet kalibriert werden soll wird dringend empfohlen diese Implementierung
 zu nutzen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Sampling Point',
'elements': [('Position', 'uint8', 1, 'in'),
             ('Distance', 'uint16',1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the distance to a sampling point position as set by
:func:`SetSamplingPoint`.
""",
'de':
"""
Gibt die Entfernung eines Messpunktes zurück, wie von :func:`SetSamplingPoint`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Distance Callback Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Distance` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Distance` is only triggered if the distance has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Distance` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Distance` wird nur ausgelöst wenn sich der Strom seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Distance Callback Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetDistanceCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetDistanceCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Analog Value Callback Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`AnalogValue` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`AnalogValue` is only triggered if the analog value has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`AnalogValue` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`AnalogValue` wird nur ausgelöst wenn sich der Analogwert seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Analog Value Callback Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetAnalogValueCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetAnalogValueCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Distance Callback Threshold',
'elements': [('Option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint16', 1, 'in'),
             ('Max', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`DistanceReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the distance is *outside* the min and max values"
 "'i'",    "Callback is triggered when the distance is *inside* the min and max values"
 "'<'",    "Callback is triggered when the distance is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the distance is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`DistanceReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Entfernung *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn die Entfernung *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn die Entfernung kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Entfernung größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Distance Callback Threshold',
'elements': [('Option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint16', 1, 'out'),
             ('Max', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`SetDistanceCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetDistanceCallbackThreshold`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Analog Value Callback Threshold',
'elements': [('Option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint16', 1, 'in'),
             ('Max', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`AnalogValueReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the analog value is *outside* the min and max values"
 "'i'",    "Callback is triggered when the analog value is *inside* the min and max values"
 "'<'",    "Callback is triggered when the analog value is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the analog value is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`AnalogValueReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn der Analogwert *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn der Analogwert *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn der Analogwert kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn der Analogwert größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Analog Value Callback Threshold',
'elements': [('Option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint16', 1, 'out'),
             ('Max', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`SetAnalogValueCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetAnalogValueCallbackThreshold`
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
Sets the period in ms with which the threshold callbacks

* :func:`DistanceReached`,
* :func:`AnalogValueReached`

are triggered, if the thresholds

* :func:`SetDistanceCallbackThreshold`,
* :func:`SetAnalogValueCallbackThreshold`

keep being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callbacks

* :func:`DistanceReached`,
* :func:`AnalogValueReached`
 
ausgelöst werden, wenn die Schwellwerte 

* :func:`SetDistanceCallbackThreshold`,
* :func:`SetAnalogValueCallbackThreshold`
 
weiterhin erreicht bleiben.

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
'name': 'Distance',
'elements': [('Distance', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetDistanceCallbackPeriod`. The :word:`parameter` is the distance of the
sensor.

:func:`Distance` is only triggered if the distance has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetDistanceCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die Entfernung des Sensors.

:func:`Distance` wird nur ausgelöst wenn sich der Strom seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Analog Value',
'elements': [('Value', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetAnalogValueCallbackPeriod`. The :word:`parameter` is the analog value of the
sensor.

:func:`AnalogValue` is only triggered if the analog value has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetAnalogValueCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist der Analogwert des Sensors.

:func:`AnalogValue` wird nur ausgelöst wenn sich der Analogwert seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Distance Reached',
'elements': [('Distance', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetDistanceCallbackThreshold` is reached.
The :word:`parameter` is the distance of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetDistanceCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Entfernung des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Analog Value Reached',
'elements': [('Value', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetAnalogValueCallbackThreshold` is reached.
The :word:`parameter` is the analog value of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetAnalogValueCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist der Analogwert des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Distance', 'distance'), [(('Distance', 'Distance'), 'uint16', 10.0, 'mm', 'cm', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Distance', 'distance'), [(('Distance', 'Distance'), 'uint16', 10.0, 'mm', 'cm', None)], None, None),
              ('callback_period', ('Distance', 'distance'), [], 200)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('Distance Reached', 'distance reached'), [(('Distance', 'Distance'), 'uint16', 10.0, 'mm', 'cm', None)], None, None),
              ('callback_threshold', ('Distance', 'distance'), [], '<', [(30, 0)])]
})
