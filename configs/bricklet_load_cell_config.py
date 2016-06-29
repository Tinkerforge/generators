# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Load Cell Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 253,
    'name': ('Load Cell', 'Load Cell', 'Load Cell Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description':  {
        'en': 'Measures weight with a load cell',
        'de': 'Misst Gewicht mit einer Wägezelle'
    },
    'released': True,
    'documented': True,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Get Weight',
'elements': [('Weight', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the currently measured weight in grams.

If you want to get the weight periodically, it is recommended 
to use the callback :func:`Weight` and set the period with 
:func:`SetWeightCallbackPeriod`.
""",
'de':
"""
Gibt das aktuell gemessene Gewicht in Gramm zurück.

Wenn das Gewicht periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`Weight` zu nutzen und die Periode mit 
:func:`SetWeightCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Weight Callback Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Weight` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Weight` is only triggered if the weight has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Weight` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Weight` wird nur ausgelöst wenn sich das Gewicht seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Weight Callback Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetWeightCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetWeightCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Weight Callback Threshold',
'elements': [('Option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'int32', 1, 'in'),
             ('Max', 'int32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`WeightReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the weight is *outside* the min and max values"
 "'i'",    "Callback is triggered when the weight is *inside* the min and max values"
 "'<'",    "Callback is triggered when the weight is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the weight is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`WeightReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn das Gewicht *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn das Gewicht *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn das Gewicht kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn das Gewicht größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Weight Callback Threshold',
'elements': [('Option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'int32', 1, 'out'),
             ('Max', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`SetWeightCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetWeightCallbackThreshold`
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

* :func:`WeightReached`

is triggered, if the threshold

* :func:`SetWeightCallbackThreshold`

keeps being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callback

* :func:`WeightReached`
 
ausgelöst wird, wenn der Schwellwert 

* :func:`SetWeightCallbackThreshold`
 
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
'type': 'function',
'name': 'Set Moving Average',
'elements': [('Average', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
for the weight value.

Setting the length to 1 will turn the averaging off. With less
averaging, there is more noise on the data.

The range for the averaging is 1-40.

The default value is 4.
""",
'de':
"""
Setzt die Länge eines `gleitenden Mittelwerts <https://de.wikipedia.org/wiki/Gleitender_Mittelwert>`__
für den Gewichtswert.

Wenn die Länge auf 1 gesetzt wird, ist das Averaging aus. Desto kleiner
die Länge des Mittelwerts ist, desto mehr Rauschen ist auf den Daten.

Der Wertebereich liegt bei 1-40.

Der Standardwert ist 4.
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
Returns the length moving average as set by :func:`SetMovingAverage`.
""",
'de':
"""
Gibt die Länge des gleitenden Mittelwerts zurück, wie von 
:func:`SetMovingAverage` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'LED On',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Turns the LED on.
""",
'de':
"""
Aktiviert die LED.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'LED Off',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Turns the LED off.
""",
'de':
"""
Deaktiviert die LED.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is LED On',
'elements': [('On', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns *true* if the led is on, *false* otherwise.
""",
'de':
"""
Gibt *true* zurück wenn die LED aktiviert ist, *false* sonst.
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Calibrate',
'elements': [('Weight', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
To calibrate your Load Cell Bricklet you have to

* empty the scale and call this function with 0 and
* add a known weight to the scale and call this function with the weight in 
  grams.

The calibration is saved in the EEPROM of the Bricklet and only
needs to be done once.

We recommend to use the Brick Viewer for calibration, you don't need
to call this function in your source code.
""",
'de':
"""
Zum Kalibrieren des Load Cell Bricklet müssen die folgenden zwei 
Schritte durchgeführt werden:

* Die Waage leeren und die Funktion mit 0 aufrufen.
* Eine bekanntes gewicht auf die Waage legen und die Funktion mit dem
  Gewicht in Gramm aufrufen.

Die Kalibrierung wird auf dem EEPROM des Bricklets gespeichert und muss
nur einmal gesetzt werden.

Wir empfehlen die Kalibrierung über den Brick Viewer zu setzen, diese
Funktion muss nicht im Quelltext genutzt werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Tare',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the currently measured weight as tare weight.
""",
'de':
"""
Setzt das aktuell gemessene Gewicht als Leergewicht.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('Rate', 'uint8', 1, 'in', ('Rate', [('10Hz', 0),
                                                  ('80Hz', 1)])),
             ('Gain', 'uint8', 1, 'in', ('Gain', [('128x', 0),
                                                  ('64x', 1),
                                                  ('32x', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
The measurement rate and gain are configurable.

The rate can be either 10Hz or 80Hz. A faster rate will produce more noise.
It is additionally possible to add a moving average
(see :func:`SetMovingAverage`) to the measurements.

The gain can be 128x, 64x or 32x. It represents a measurement range of
±20mV, ±40mV and ±80mV respectively. The Load Cell Bricklet uses an
excitation voltage of 5V and most load cells use an output of 2mV/V. That
means the voltage range is ±15mV for most load cells (i.e. gain of 128x
is best). If you don't know what all of this means you should keep it at 
128x, it will most likely be correct.

The configuration is saved in the EEPROM of the Bricklet and only
needs to be done once.

We recommend to use the Brick Viewer for configuration, you don't need
to call this function in your source code.

The default rate is 10Hz and the default gain is 128x.
""",
'de':
"""
Für die Messungen sind Rate und Gain konfigurierbar.

Die Rate kann auf 10Hz oder 80Hz gesetzt werden. Eine schnellere Rate
erzeugt mehr Störungen. Zusätzlich ist es möglich einen gleitenden
Mittelwert auf die Werte anzuwenden (siehe :func:`SetMovingAverage`).

Der Gain kann zwischen 128x, 64x und 32x konfiguriert werden. Er
respräsentiert einenen Messbereich von ±20mV, ±40mV und ±80mV
respektive. Das Load Cell Bricklet nutzt eine
Erregerspannung (Excitation Voltage) von 5V und die meisten Wägezellen
haben eine Ausgabe von 2mV/V. Dies bedeutet, der Spannungsbereich ist
±15mV für die meisten Wägezellen (d.h. ein Gain von 128x ist am
geeignetsten). Falls nicht klar ist was dies alles bedeutet, ein
Gain von 128x ist höchstwahrscheinlich korrekt.

Die Konfiguration wird auf dem EEPROM des Bricklets gespeichert und muss
nur einmal gesetzt werden.

Wir empfehlen die Konfiguration über den Brick Viewer zu setzen, diese
Funktion muss nicht im Quelltext genutzt werden.

Die Standardwerte sind 10Hz für die Rate und 128x für den Gain.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Rate', 'uint8', 1, 'out', ('Rate', [('10Hz', 0),
                                                   ('80Hz', 1)])),
             ('Gain', 'uint8', 1, 'out', ('Gain', [('128x', 0),
                                                   ('64x', 1),
                                                   ('32x', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`SetConfiguration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`SetConfiguration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Weight',
'elements': [('Weight', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetWeightCallbackPeriod`. The :word:`parameter` is the weight
as measured by the load cell.

:func:`Weight` is only triggered if the weight has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetWeightCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist das Gewicht wie von der Wägezelle gemessen.

:func:`Weight` wird nur ausgelöst wenn sich das Gewicht seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Weight Reached',
'elements': [('Weight', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetWeightCallbackThreshold` is reached.
The :word:`parameter` is the weight as measured by the load cell.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetWeightCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist das Gewicht wie von der Wägezelle gemessen.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Weight', 'weight'), [(('Weight', 'Weight'), 'int32', None, 'g', 'g', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Weight', 'weight'), [(('Weight', 'Weight'), 'int32', None, 'g', 'g', None)], None, None),
              ('callback_period', ('Weight', 'weight'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 1000),
              ('callback', ('Weight Reached', 'weight reached'), [(('Weight', 'Weight'), 'int32', None, 'g', 'g', None)], None, None),
              ('callback_threshold', ('Weight', 'weight'), [], '>', [(200, 0)])]
})
