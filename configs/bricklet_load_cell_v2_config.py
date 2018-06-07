# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Load Cell Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2104,
    'name': 'Load Cell V2',
    'display_name': 'Load Cell 2.0',
    'manufacturer': 'Tinkerforge',
    'description':  {
        'en': 'Measures weight with a load cell',
        'de': 'Misst Gewicht mit einer Wägezelle'
    },
    'comcu': True,
    'released': True,
    'documented': False,
    'discontinued': False,
    'packets': [],
    'examples': []
}

weight_doc = {
'en':
"""
Returns the currently measured weight in grams.
""",
'de':
"""
Gibt das aktuell gemessene Gewicht in Gramm zurück.
"""
}

add_callback_value_function(
    packets   = com['packets'], 
    name      = 'Get Weight', 
    data_name = 'Weight',
    data_type = 'int32',
    doc       = weight_doc
)

com['packets'].append({
'type': 'function',
'name': 'Set Moving Average',
'elements': [('Average', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
for the weight value.

Setting the length to 1 will turn the averaging off. With less
averaging, there is more noise on the data.

The range for the averaging is 1-100.

The default value is 4.
""",
'de':
"""
Setzt die Länge eines `gleitenden Mittelwerts <https://de.wikipedia.org/wiki/Gleitender_Mittelwert>`__
für den Gewichtswert.

Wenn die Länge auf 1 gesetzt wird, ist das Averaging aus. Desto kleiner
die Länge des Mittelwerts ist, desto mehr Rauschen ist auf den Daten.

Der Wertebereich liegt bei 1-100.

Der Standardwert ist 4.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Moving Average',
'elements': [('Average', 'uint16', 1, 'out')],
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
'name': 'Set Info LED Config',
'elements': [('Config', 'uint8', 1, 'in', ('Info LED Config', [('Off', 0),
                                                               ('On', 1),
                                                               ('Show Heartbeat', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Configures the info LED to be either turned off, turned on, or blink in
heartbeat mode.
""",
'de':
"""
Konfiguriert die Info-LED so es ist entweder ausgeschaltet, eingeschaltet oder
in Herzschlagmodus.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Info LED Config',
'elements': [('Config', 'uint8', 1, 'out', ('Info LED Config', [('Off', 0),
                                                                ('On', 1),
                                                                ('Show Heartbeat', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the LED configuration as set by :func:`Set Info LED Config`
""",
'de':
"""
Gibt die LED-Konfiguration zurück, wie von :func:`Set Info LED Config` gesetzt.
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
To calibrate your Load Cell Bricklet 2.0 you have to

* empty the scale and call this function with 0 and
* add a known weight to the scale and call this function with the weight in
  grams.

The calibration is saved in the flash of the Bricklet and only
needs to be done once.

We recommend to use the Brick Viewer for calibration, you don't need
to call this function in your source code.
""",
'de':
"""
Zum Kalibrieren des Load Cell Bricklet 2.0 müssen die folgenden zwei
Schritte durchgeführt werden:

* Die Waage leeren und die Funktion mit 0 aufrufen.
* Eine bekanntes Gewicht auf die Waage legen und die Funktion mit dem
  Gewicht in Gramm aufrufen.

Die Kalibrierung wird auf dem Flash des Bricklets gespeichert und muss
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
(see :func:`Set Moving Average`) to the measurements.

The gain can be 128x, 64x or 32x. It represents a measurement range of
±20mV, ±40mV and ±80mV respectively. The Load Cell Bricklet uses an
excitation voltage of 5V and most load cells use an output of 2mV/V. That
means the voltage range is ±15mV for most load cells (i.e. gain of 128x
is best). If you don't know what all of this means you should keep it at
128x, it will most likely be correct.

The default rate is 10Hz and the default gain is 128x.
""",
'de':
"""
Für die Messungen sind Rate und Gain konfigurierbar.

Die Rate kann auf 10Hz oder 80Hz gesetzt werden. Eine schnellere Rate
erzeugt mehr Störungen. Zusätzlich ist es möglich einen gleitenden
Mittelwert auf die Werte anzuwenden (siehe :func:`Set Moving Average`).

Der Gain kann zwischen 128x, 64x und 32x konfiguriert werden. Er
repräsentiert einen Messbereich von ±20mV, ±40mV und ±80mV
respektive. Das Load Cell Bricklet nutzt eine
Erregerspannung (Excitation Voltage) von 5V und die meisten Wägezellen
haben eine Ausgabe von 2mV/V. Dies bedeutet, der Spannungsbereich ist
±15mV für die meisten Wägezellen (d.h. ein Gain von 128x ist am
geeignetsten). Falls nicht klar ist was dies alles bedeutet, ein
Gain von 128x ist höchstwahrscheinlich korrekt.

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
Returns the configuration as set by :func:`Set Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Configuration` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Weight', 'weight'), [(('Weight', 'Weight'), 'int32', 1, None, 'g', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Weight', 'weight'), [(('Weight', 'Weight'), 'int32', 1, None, 'g', None)], None, None),
              ('callback_configuration', ('Weight', 'weight'), [], 1000, False, 'x', [(0, 0)])]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('callback', ('Weight', 'weight'), [(('Weight', 'Weight'), 'int32', 1, None, 'g', None)], None, None),
              ('callback_configuration', ('Weight', 'weight'), [], 1000, False, '>', [(200, 0)])]
})
