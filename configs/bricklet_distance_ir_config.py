# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Distance IR Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'api_version_extra': 1, # +1 for "Break API to fix threshold min/max type mismatch [59d13f6]"
    'category': 'Bricklet',
    'device_identifier': 25,
    'name': 'Distance IR',
    'display_name': 'Distance IR',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures distance up to 150cm with infrared light',
        'de': 'Misst Entfernung bis zu 150cm mit Infrarot-Licht'
    },
    'released': True,
    'documented': True,
    'discontinued': False, # selling remaining stock, replaced by Distance IR Bricklet 2.0
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
:cb:`Distance` callback and set the period with
:func:`Set Distance Callback Period`.
""",
'de':
"""
Gibt die gemessene Entfernung des Sensors zurück. Der Wert ist in mm und die möglichen
Entfernungsbereiche sind 40 bis 300, 100 bis 800 und 200 bis 1500, in Abhängigkeit vom
gewählten IR Sensor.

Wenn die Entfernung periodisch abgefragt werden soll, wird empfohlen
den :cb:`Distance` Callback zu nutzen und die Periode mit
:func:`Set Distance Callback Period` vorzugeben.
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
 The value returned by :func:`Get Distance` is averaged over several samples
 to yield less noise, while :func:`Get Analog Value` gives back raw
 unfiltered analog values. The only reason to use :func:`Get Analog Value` is,
 if you need the full resolution of the analog-to-digital converter.

If you want the analog value periodically, it is recommended to use the
:cb:`Analog Value` callback and set the period with
:func:`Set Analog Value Callback Period`.
""",
'de':
"""
Gibt den Wert, wie vom 12-Bit Analog-Digital-Wandler gelesen, zurück. Der
Wertebereich ist 0 bis 4095.

.. note::
 Der von :func:`Get Distance` zurückgegebene Wert ist über mehrere
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
:func:`Set Sampling Point`.
""",
'de':
"""
Gibt die Entfernung eines Messpunktes zurück, wie von :func:`Set Sampling Point` gesetzt.
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
Sets the period in ms with which the :cb:`Distance` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Distance` callback is only triggered if the distance has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :cb:`Distance` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Distance` Callback wird nur ausgelöst, wenn sich der Strom seit der
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
Returns the period as set by :func:`Set Distance Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Distance Callback Period` gesetzt.
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
Sets the period in ms with which the :cb:`Analog Value` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Analog Value` callback is only triggered if the analog value has
changed since the last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :cb:`Analog Value` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Analog Value` Callback wird nur ausgelöst, wenn sich der Analogwert
seit der letzten Auslösung geändert hat.

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
'name': 'Set Distance Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'in'),
             ('Max', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Distance Reached` callback.

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
Setzt den Schwellwert für den :cb:`Distance Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn die Entfernung *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn die Entfernung *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn die Entfernung kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn die Entfernung größer als der min Wert ist (max wird ignoriert)"

Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Distance Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'out'),
             ('Max', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Distance Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Distance Callback Threshold` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Analog Value Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'in'),
             ('Max', 'uint16', 1, 'in')],
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

The default value is ('x', 0, 0).
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

Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Analog Value Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'out'),
             ('Max', 'uint16', 1, 'out')],
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
'elements': [('Debounce', 'uint32', 1, 'in', {'factor': 1000, 'unit': 'Second', 'default': 100})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the threshold callbacks

* :cb:`Distance Reached`,
* :cb:`Analog Value Reached`

are triggered, if the thresholds

* :func:`Set Distance Callback Threshold`,
* :func:`Set Analog Value Callback Threshold`

keep being reached.
""",
'de':
"""
Setzt die Periode mit welcher die Schwellwert Callbacks

* :cb:`Distance Reached`,
* :cb:`Analog Value Reached`

ausgelöst werden, wenn die Schwellwerte

* :func:`Set Distance Callback Threshold`,
* :func:`Set Analog Value Callback Threshold`

weiterhin erreicht bleiben.
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
'type': 'callback',
'name': 'Distance',
'elements': [('Distance', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Distance Callback Period`. The :word:`parameter` is the distance of the
sensor.

The :cb:`Distance` callback is only triggered if the distance has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Distance Callback Period`,
ausgelöst. Der :word:`parameter` ist die Entfernung des Sensors.

Der :cb:`Distance` Callback wird nur ausgelöst, wenn sich der Strom seit der
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
:func:`Set Analog Value Callback Period`. The :word:`parameter` is the analog value of the
sensor.

The :cb:`Analog Value` callback is only triggered if the analog value has changed
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
'name': 'Distance Reached',
'elements': [('Distance', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Distance Callback Threshold` is reached.
The :word:`parameter` is the distance of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Distance Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Entfernung des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
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
'functions': [('getter', ('Get Distance', 'distance'), [(('Distance', 'Distance'), 'uint16', 1, 10.0, 'cm', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Distance', 'distance'), [(('Distance', 'Distance'), 'uint16', 1, 10.0, 'cm', None)], None, None),
              ('callback_period', ('Distance', 'distance'), [], 200)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('Distance Reached', 'distance reached'), [(('Distance', 'Distance'), 'uint16', 1, 10.0, 'cm', None)], None, None),
              ('callback_threshold', ('Distance', 'distance'), [], '<', [(30, 0)])]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'channels': [
        oh_generic_old_style_channel('Distance', 'Distance', 'SIUnits.METRE', divisor=1000.0)
    ],
    'channel_types': [
        oh_generic_channel_type('Distance', 'Number:Length', 'Distance',
                     description='Measured distance',
                     read_only=True,
                     pattern='%.3f %unit%',
                     min_=40,
                     max_=1500)
    ],
    'actions': ['Get Distance', 'Get Analog Value', 'Get Sampling Point']
}
