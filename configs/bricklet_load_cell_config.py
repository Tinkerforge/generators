# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Load Cell Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 253,
    'name': 'Load Cell',
    'display_name': 'Load Cell',
    'manufacturer': 'Tinkerforge',
    'description':  {
        'en': 'Measures weight with a load cell',
        'de': 'Misst Gewicht mit einer Wägezelle'
    },
    'released': True,
    'documented': True,
    'discontinued': True, # replaced by Load Cell Bricklet 2.0
    'features': [
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

com['constant_groups'].append({
'name': 'Rate',
'type': 'uint8',
'constants': [('10Hz', 0),
              ('80Hz', 1)]
})

com['constant_groups'].append({
'name': 'Gain',
'type': 'uint8',
'constants': [('128x', 0),
              ('64x', 1),
              ('32x', 2)]
})

com['packets'].append({
'type': 'function',
'name': 'Get Weight',
'elements': [('Weight', 'int32', 1, 'out', {'unit': 'Gram'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the currently measured weight.

If you want to get the weight periodically, it is recommended
to use the :cb:`Weight` callback and set the period with
:func:`Set Weight Callback Period`.
""",
'de':
"""
Gibt das aktuell gemessene Gewicht zurück.

Wenn das Gewicht periodisch abgefragt werden soll, wird empfohlen
den :cb:`Weight` Callback zu nutzen und die Periode mit
:func:`Set Weight Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Weight Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Weight` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Weight` callback is only triggered if the weight has changed since the
last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Weight` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Weight` Callback wird nur ausgelöst, wenn sich das Gewicht seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Weight Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Weight Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Weight Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Weight Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'int32', 1, 'in', {'unit': 'Gram', 'default': 0}),
             ('Max', 'int32', 1, 'in', {'unit': 'Gram', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Weight Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the weight is *outside* the min and max values"
 "'i'",    "Callback is triggered when the weight is *inside* the min and max values"
 "'<'",    "Callback is triggered when the weight is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the weight is greater than the min value (max is ignored)"
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Weight Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn das Gewicht *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn das Gewicht *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn das Gewicht kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn das Gewicht größer als der min Wert ist (max wird ignoriert)"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Weight Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'int32', 1, 'out', {'unit': 'Gram', 'default': 0}),
             ('Max', 'int32', 1, 'out', {'unit': 'Gram', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Weight Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Weight Callback Threshold` gesetzt.
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
Sets the period with which the threshold callback

* :cb:`Weight Reached`

is triggered, if the threshold

* :func:`Set Weight Callback Threshold`

keeps being reached.
""",
'de':
"""
Setzt die Periode mit welcher die Schwellwert Callback

* :cb:`Weight Reached`

ausgelöst wird, wenn der Schwellwert

* :func:`Set Weight Callback Threshold`

weiterhin erreicht bleibt.
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
'type': 'function',
'name': 'Set Moving Average',
'elements': [('Average', 'uint8', 1, 'in', {'range': (1, 40), 'default': 4})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
for the weight value.

Setting the length to 1 will turn the averaging off. With less
averaging, there is more noise on the data.
""",
'de':
"""
Setzt die Länge eines `gleitenden Mittelwerts <https://de.wikipedia.org/wiki/Gleitender_Mittelwert>`__
für den Gewichtswert.

Wenn die Länge auf 1 gesetzt wird, ist das Averaging aus. Desto kleiner
die Länge des Mittelwerts ist, desto mehr Rauschen ist auf den Daten.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Moving Average',
'elements': [('Average', 'uint8', 1, 'out', {'range': (1, 40), 'default': 4})],
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
'elements': [('On', 'bool', 1, 'out', {'default': False})],
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
'elements': [('Weight', 'uint32', 1, 'in', {'unit': 'Gram'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
To calibrate your Load Cell Bricklet you have to

* empty the scale and call this function with 0 and
* add a known weight to the scale and call this function with the weight.

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
* Eine bekanntes Gewicht auf die Waage legen und die Funktion mit dem
  Gewicht aufrufen.

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
'elements': [('Rate', 'uint8', 1, 'in', {'constant_group': 'Rate', 'default': 0}),
             ('Gain', 'uint8', 1, 'in', {'constant_group': 'Gain', 'default': 0})],
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

The configuration is saved in the EEPROM of the Bricklet and only
needs to be done once.

We recommend to use the Brick Viewer for configuration, you don't need
to call this function in your source code.
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

Die Konfiguration wird auf dem EEPROM des Bricklets gespeichert und muss
nur einmal gesetzt werden.

Wir empfehlen die Konfiguration über den Brick Viewer zu setzen, diese
Funktion muss nicht im Quelltext genutzt werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Rate', 'uint8', 1, 'out', {'constant_group': 'Rate', 'default': 0}),
             ('Gain', 'uint8', 1, 'out', {'constant_group': 'Gain', 'default': 0})],
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

com['packets'].append({
'type': 'callback',
'name': 'Weight',
'elements': [('Weight', 'int32', 1, 'out', {'unit': 'Gram'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Weight Callback Period`. The :word:`parameter` is the weight
as measured by the load cell.

The :cb:`Weight` callback is only triggered if the weight has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Weight Callback Period`,
ausgelöst. Der :word:`parameter` ist das Gewicht wie von der Wägezelle gemessen.

Der :cb:`Weight` Callback wird nur ausgelöst, wenn sich das Gewicht seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Weight Reached',
'elements': [('Weight', 'int32', 1, 'out', {'unit': 'Gram'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Weight Callback Threshold` is reached.
The :word:`parameter` is the weight as measured by the load cell.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Weight Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist das Gewicht wie von der Wägezelle gemessen.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
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
              ('callback_period', ('Weight', 'weight'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 1000),
              ('callback', ('Weight Reached', 'weight reached'), [(('Weight', 'Weight'), 'int32', 1, None, 'g', None)], None, None),
              ('callback_threshold', ('Weight', 'weight'), [], '>', [(200, 0)])]
})


com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.StringType', 'org.eclipse.smarthome.core.library.types.OnOffType'],
    'param_groups': oh_generic_channel_param_groups(),
    'params': [{
            'packet': 'Set Moving Average',
            'element': 'Average',
            'name': 'Moving Average',
            'type': 'integer',
            'default': 4,
            'min': 1,
            'max': 40,

            'label': 'Moving Average',
            'description': 'The length of a moving averaging for the weight value.<br/><br/>Setting the length to 1 will turn the averaging off. With less averaging, there is more noise on the data.'
        }
    ],
    'init_code': """this.setMovingAverage(cfg.movingAverage.shortValue());""",
    'channels': [
        oh_generic_old_style_channel('Weight', 'Weight', 'SIUnits.GRAM', divisor=1),
        {
            'id': 'Tare',
            'type': 'Tare',

            'setters': [{
                'packet': 'Tare',
                'command_type': "StringType", # Command type has to be string type to be able to use command options.
            }],

            'setter_refreshs': [{
                'channel': 'Weight',
                'delay': '0'
            }]
        }, {
            'id': 'LED',
            'type': 'LED',

            'setters': [{
                'predicate': 'cmd == OnOffType.ON',
                'packet': 'LED On',
                'command_type': "OnOffType",
            }, {
                'predicate': 'cmd == OnOffType.OFF',
                'packet': 'LED On',
                'command_type': "OnOffType",
            }],

            'getters': [{
                'packet': 'Is LED On',
                'transform': 'value ? OnOffType.ON : OnOffType.OFF'
            }]
        }
    ],
    'channel_types': [
        oh_generic_channel_type('Weight', 'Number:Mass', 'Weight',
                    update_style='Callback Period',
                    description='The currently measured weight',
                    read_only=True,
                    pattern='%d %unit%',
                    min_=0),
        {
            'id': 'Tare',
            'item_type': 'String',
            'label': 'Tare',
            'description':'Sets the currently measured weight as tare weight.',
            'command_options': [('Tare', 'TARE')]
        },
        oh_generic_channel_type('LED', 'Switch', 'LED',
                    update_style=None,
                    description='Activates/Deactivates the LED.'),
    ],
    'actions': ['Get Weight', 'Tare', 'Get Moving Average', 'Get Configuration',
                {'fn': 'LED On', 'refreshs': ['LED']}, {'fn': 'LED Off', 'refreshs': ['LED']}, 'Is LED On']
}
