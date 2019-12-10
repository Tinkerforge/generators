# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Load Cell Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from commonconstants import add_callback_value_function

from openhab_common import *

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
    'released': True,
    'documented': True,
    'discontinued': False,
    'features': [
        'comcu_bricklet',
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

com['constant_groups'].append({
'name': 'Info LED Config',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Show Heartbeat', 2)]
})

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

weight_doc = {
'en':
"""
Returns the currently measured weight.
""",
'de':
"""
Gibt das aktuell gemessene Gewicht zurück.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Weight',
    data_name = 'Weight',
    data_type = 'int32',
    doc       = weight_doc,
    unit      = 'Gram'
)

com['packets'].append({
'type': 'function',
'name': 'Set Moving Average',
'elements': [('Average', 'uint16', 1, 'in', {'range': (1, 100), 'default': 4})],
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
'elements': [('Average', 'uint16', 1, 'out', {'range': (1, 100), 'default': 4})],
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
'elements': [('Config', 'uint8', 1, 'in', {'constant_group': 'Info LED Config', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Configures the info LED to be either turned off, turned on, or blink in
heartbeat mode.
""",
'de':
"""
Konfiguriert die Info-LED. Die LED kann ausgeschaltet, eingeschaltet oder
im Herzschlagmodus betrieben werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Info LED Config',
'elements': [('Config', 'uint8', 1, 'out', {'constant_group': 'Info LED Config', 'default': 0})],
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
'elements': [('Weight', 'uint32', 1, 'in', {'unit': 'Gram'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
To calibrate your Load Cell Bricklet 2.0 you have to

* empty the scale and call this function with 0 and
* add a known weight to the scale and call this function with the weight.

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
  Gewicht aufrufen.

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


com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.StringType'],
    'param_groups': oh_generic_channel_param_groups(),
    'params': [{
            'packet': 'Set Moving Average',
            'element': 'Average',

            'name': 'Moving Average',
            'type': 'integer',
            'default': 4,
            'min': 1,
            'max': 100,

            'label': 'Moving Average',
            'description': 'The length of a moving averaging for the weight value.<br/><br/>Setting the length to 1 will turn the averaging off. With less averaging, there is more noise on the data.'
        }, {
            'packet': 'Set Configuration',
            'element': 'Rate',

            'name': 'Measurement Rate',
            'type': 'integer',
            'options': [('10Hz', 0),
                        ('80Hz', 1)],
            'limitToOptions': 'true',
            'default': 0,

            'label': 'Measurement Rate',
            'description': 'The rate can be either 10Hz or 80Hz. A faster rate will produce more noise.',
        }, {
            'packet': 'Set Configuration',
            'element': 'Gain',

            'name': 'Gain',
            'type': 'integer',
            'options': [('128x', 0),
                        ('64x', 1),
                        ('32x', 2)],
            'limitToOptions': 'true',
            'default': 0,

            'label': 'Gain',
            'description': "The gain can be 128x, 64x or 32x. It represents a measurement range of ±20mV, ±40mV and ±80mV respectively. The Load Cell Bricklet uses an excitation voltage of 5V and most load cells use an output of 2mV/V. That means the voltage range is ±15mV for most load cells (i.e. gain of 128x is best). If you don't know what all of this means you should keep it at 128x, it will most likely be correct.",
        }, {
            'packet': 'Set Info LED Config',
            'element': 'Config',

            'name': 'Info LED',
            'type': 'integer',
            'options': [('Off', 0),
                        ('On', 1),
                        ('Show Heartbeat', 2)],
            'limitToOptions': 'true',
            'default': 0,

            'label': 'Info LED',
            'description': 'Configures the info LED to be either turned off, turned on, or blink in heartbeat mode.',
        },
    ],
    'init_code': """this.setConfiguration(cfg.measurementRate, cfg.gain);
this.setMovingAverage(cfg.movingAverage);
this.setInfoLEDConfig(cfg.infoLED);""",
    'channels': [
        oh_generic_channel('Weight', 'Weight', 'SIUnits.GRAM', divisor=1),
        {
            'id': 'Tare',
            'type': 'Tare',

            'setters': [{
                'packet': 'Tare'}],
            'setter_command_type': "StringType", # Command type has to be string type to be able to use command options.
            'setter_refreshs': [{
                'channel': 'Weight',
                'delay': '0'
            }]
        }
    ],
    'channel_types': [
        oh_generic_channel_type('Weight', 'Number:Mass', 'Weight',
                    update_style='Callback Configuration',
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
        }
    ],
    'actions': ['Get Weight', 'Get Info LED Config', 'Tare', 'Get Moving Average', 'Get Configuration']
}
