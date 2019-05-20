# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Joystick Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 210,
    'name': 'Joystick',
    'display_name': 'Joystick',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '2-axis joystick with push-button',
        'de': '2-Achsen Joystick mit Taster'
    },
    'released': True,
    'documented': True,
    'discontinued': False, # selling remaining stock, replaced by Joystick Bricklet 2.0
    'features': [
        'bricklet_get_identity'
    ],
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Get Position',
'elements': [('X', 'int16', 1, 'out'),
             ('Y', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the position of the joystick. The value ranges between -100 and
100 for both axis. The middle position of the joystick is x=0, y=0. The
returned values are averaged and calibrated (see :func:`Calibrate`).

If you want to get the position periodically, it is recommended to use the
:cb:`Position` callback and set the period with
:func:`Set Position Callback Period`.
""",
'de':
"""
Gibt die Position des Joystick zurück. Der Wertebereich ist von -100 bis
100 für beide Achsen. Die Mittelposition des Joysticks ist x=0, y=0.
Die zurückgegebenen Werte sind gemittelt und kalibriert (siehe :func:`Calibrate`).

Wenn die Position periodisch abgefragt werden sollen, wird empfohlen
den :cb:`Position` Callback zu nutzen und die Periode mit
:func:`Set Position Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is Pressed',
'elements': [('Pressed', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns *true* if the button is pressed and *false* otherwise.

It is recommended to use the :cb:`Pressed` and :cb:`Released` callbacks
to handle the button.
""",
'de':
"""
Gibt *true* zurück wenn die Taste gedrückt ist und sonst *false*.

Es wird empfohlen die :cb:`Pressed` und :cb:`Released` Callbacks
zu nutzen, um die Taste programmatisch zu behandeln.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Analog Value',
'elements': [('X', 'uint16', 1, 'out'),
             ('Y', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the values as read by a 12-bit analog-to-digital converter.
The values are between 0 and 4095 for both axis.

.. note::
 The values returned by :func:`Get Position` are averaged over several samples
 to yield less noise, while :func:`Get Analog Value` gives back raw
 unfiltered analog values. The only reason to use :func:`Get Analog Value` is,
 if you need the full resolution of the analog-to-digital converter.

If you want the analog values periodically, it is recommended to use the
:cb:`Analog Value` callback and set the period with
:func:`Set Analog Value Callback Period`.
""",
'de':
"""
Gibt den Wert, wie vom 12-Bit Analog-Digital-Wandler gelesen, zurück. Der
Wertebereich ist 0 bis 4095.

.. note::
 Der von :func:`Get Position` zurückgegebene Wert ist über mehrere
 Messwerte gemittelt um das Rauschen zu vermindern, während :func:`Get Analog Value`
 unverarbeitete Analogwerte zurück gibt. Der einzige Grund :func:`Get Analog Value`
 zu nutzen, ist die volle Auflösung des Analog-Digital-Wandlers zu erhalten.

Wenn die Analogwerte periodisch abgefragt werden sollen, wird empfohlen
den :cb:`Analog Value` Callback zu nutzen und die Periode mit
:func:`Set Analog Value Callback Period` vorzugeben.
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
Calibrates the middle position of the joystick. If your Joystick Bricklet
does not return x=0 and y=0 in the middle position, call this function
while the joystick is standing still in the middle position.

The resulting calibration will be saved on the EEPROM of the Joystick
Bricklet, thus you only have to calibrate it once.
""",
'de':
"""
Kalibriert die Mittelposition des Joysticks. Sollte der Joystick Bricklet
nicht x=0 und y=0 in der Mittelposition zurückgeben, kann diese Funktion
aufgerufen werden wenn der Joystick sich unbewegt in der Mittelposition befindet.

Die resultierende Kalibrierung wird in den EEPROM des Joystick Bricklet gespeichert,
somit ist die Kalibrierung nur einmalig notwendig.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Position Callback Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :cb:`Position` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Position` callback is only triggered if the position has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :cb:`Position` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

The :cb:`Position` Callback wird nur ausgelöst wenn sich die Position seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Position Callback Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Position Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Position Callback Period`
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
Sets the period in ms with which the :cb:`Analog Value` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Analog Value` callback is only triggered if the analog values have
changed since the last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :cb:`Analog Value` Callback ausgelöst
wird. Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Analog Value` Callback wird nur ausgelöst wenn sich die Analogwerte
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
Gibt die Periode zurück, wie von :func:`Set Analog Value Callback Period`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Position Callback Threshold',
'elements': [('Option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('Min X', 'int16', 1, 'in'),
             ('Max X', 'int16', 1, 'in'),
             ('Min Y', 'int16', 1, 'in'),
             ('Max Y', 'int16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Position Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the position is *outside* the min and max values"
 "'i'",    "Callback is triggered when the position is *inside* the min and max values"
 "'<'",    "Callback is triggered when the position is smaller than the min values (max is ignored)"
 "'>'",    "Callback is triggered when the position is greater than the min values (max is ignored)"

The default value is ('x', 0, 0, 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Position Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Position *außerhalb* der min und max Werte ist"
 "'i'",    "Callback wird ausgelöst wenn die Position *innerhalb* der min und max Werte ist"
 "'<'",    "Callback wird ausgelöst wenn die Position kleiner als die min Werte ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Position größer als die min Werte ist (max wird ignoriert)"

Der Standardwert ist ('x', 0, 0, 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Position Callback Threshold',
'elements': [('Option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('Min X', 'int16', 1, 'out'),
             ('Max X', 'int16', 1, 'out'),
             ('Min Y', 'int16', 1, 'out'),
             ('Max Y', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Position Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Position Callback Threshold`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Analog Value Callback Threshold',
'elements': [('Option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('Min X', 'uint16', 1, 'in'),
             ('Max X', 'uint16', 1, 'in'),
             ('Min Y', 'uint16', 1, 'in'),
             ('Max Y', 'uint16', 1, 'in')],
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
 "'o'",    "Callback is triggered when the analog values are *outside* the min and max values"
 "'i'",    "Callback is triggered when the analog values are *inside* the min and max values"
 "'<'",    "Callback is triggered when the analog values are smaller than the min values (max is ignored)"
 "'>'",    "Callback is triggered when the analog values are greater than the min values (max is ignored)"

The default value is ('x', 0, 0, 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Analog Value Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Analogwerte *außerhalb* der min und max Werte ist"
 "'i'",    "Callback wird ausgelöst wenn die Analogwerte *innerhalb* der min und max Werte ist"
 "'<'",    "Callback wird ausgelöst wenn die Analogwerte kleiner als die min Werte ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Analogwerte größer als die min Werte ist (max wird ignoriert)"

Der Standardwert ist ('x', 0, 0, 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Analog Value Callback Threshold',
'elements': [('Option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('Min X', 'uint16', 1, 'out'),
             ('Max X', 'uint16', 1, 'out'),
             ('Min Y', 'uint16', 1, 'out'),
             ('Max Y', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Analog Value Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Analog Value Callback Threshold`
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

* :cb:`Position Reached`,
* :cb:`Analog Value Reached`

are triggered, if the thresholds

* :func:`Set Position Callback Threshold`,
* :func:`Set Analog Value Callback Threshold`

keep being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callbacks

* :cb:`Position Reached`,
* :cb:`Analog Value Reached`

ausgelöst werden, wenn die Schwellwerte

* :func:`Set Position Callback Threshold`,
* :func:`Set Analog Value Callback Threshold`

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
Returns the debounce period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Gibt die Entprellperiode zurück, wie von :func:`Set Debounce Period`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Position',
'elements': [('X', 'int16', 1, 'out'),
             ('Y', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Position Callback Period`. The :word:`parameter` is the position of the
joystick.

The :cb:`Position` callback is only triggered if the position has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Position Callback Period`,
ausgelöst. Der :word:`parameter` ist die Position des Joysticks.

Der :cb:`Position` Callback wird nur ausgelöst, wenn sich die Position seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Analog Value',
'elements': [('X', 'uint16', 1, 'out'),
             ('Y', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Analog Value Callback Period`. The :word:`parameters` are the
analog values of the joystick.

The :cb:`Analog Value` callback is only triggered if the values have changed
since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Analog Value Callback Period`,
ausgelöst. Der :word:`parameter` sind die Analogwerte des Joysticks.

Der :cb:`Analog Value` Callback wird nur ausgelöst wenn sich die Analogwerte
seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Position Reached',
'elements': [('X', 'int16', 1, 'out'),
             ('Y', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Position Callback Threshold` is reached.
The :word:`parameters` are the position of the joystick.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von
:func:`Set Position Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Position des Joysticks.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Analog Value Reached',
'elements': [('X', 'uint16', 1, 'out'),
             ('Y', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Analog Value Callback Threshold` is reached.
The :word:`parameters` are the analog values of the joystick.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von
:func:`Set Analog Value Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` sind die Analogwerte des Joystick.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Pressed',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the button is pressed.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn die Taste gedrückt wird.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Released',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the button is released.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn die Taste losgelassen wird.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Position', 'position'), [(('X', 'Position [X]'), 'int16', 1, None, None, None), (('Y', 'Position [Y]'), 'int16', 1, None, None, None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Pressed', 'pressed'), [], None, 'Pressed'),
              ('callback', ('Released', 'released'), [], None, 'Released')]
})

com['examples'].append({
'name': 'Find Borders',
'functions': [('debounce_period', 200),
              ('callback', ('Position Reached', 'position reached'), [(('X', 'Position [X]'), 'int16', 1, None, None, None), (('Y', 'Position [Y]'), 'int16', 1, None, None, None)], None, None),
              ('callback_threshold', ('Position', 'position'), [], 'o', [(-99, 99), (-99, 99)])],
'incomplete': True # because of special print logic in callback
})
