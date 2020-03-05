# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Color Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from commonconstants import add_callback_value_function

from openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2128,
    'name': 'Color V2',
    'display_name': 'Color 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures color (RGB value), illuminance and color temperature',
        'de': 'Misst Farbe (RGB Wert), Beleuchtungsstärke und Farbtemperatur'
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
'name': 'Gain',
'type': 'uint8',
'constants': [('1x', 0),
              ('4x', 1),
              ('16x', 2),
              ('60x', 3)]
})

com['constant_groups'].append({
'name': 'Integration Time',
'type': 'uint8',
'constants': [('2ms', 0),
              ('24ms', 1),
              ('101ms', 2),
              ('154ms', 3),
              ('700ms', 4)]
})

com['packets'].append({
'type': 'function',
'name': 'Get Color',
'elements': [('R', 'uint16', 1, 'out', {}),
             ('G', 'uint16', 1, 'out', {}),
             ('B', 'uint16', 1, 'out', {}),
             ('C', 'uint16', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the measured color of the sensor.

The red (r), green (g), blue (b) and clear (c) colors are measured
with four different photodiodes that are responsive at different
wavelengths:

.. image:: /Images/Bricklets/bricklet_color_wavelength_chart_600.jpg
   :scale: 100 %
   :alt: Chart Responsivity / Wavelength
   :align: center
   :target: ../../_images/Bricklets/bricklet_color_wavelength_chart_600.jpg

If you want to get the color periodically, it is recommended
to use the :cb:`Color` callback and set the period with
:func:`Set Color Callback Configuration`.
""",
'de':
"""
Gibt die gemessene Farbe des Sensors zurück.

Die rot (r), grün (g), blau (b) und clear (c) Farbanteile werden mit vier
unterschiedlichen Fotodioden gemessen. Diese sind Empfindlich
in unterschiedlichen Wellenlängen:

.. image:: /Images/Bricklets/bricklet_color_wavelength_chart_600.jpg
   :scale: 100 %
   :alt: Chart Responsivity / Wavelength
   :align: center
   :target: ../../_images/Bricklets/bricklet_color_wavelength_chart_600.jpg

Wenn die Farbe periodisch abgefragt werden soll, wird empfohlen
den :cb:`Color` Callback zu nutzen und die Periode mit
:func:`Set Color Callback Configuration` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Color Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period is the period with which the :cb:`Color`
callback is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.
""",
'de':
"""
Die Periode ist die Periode mit der der :cb:`Color`
Callback ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn der Wert sich im Vergleich zum letzten mal geändert
hat. Ändert der Wert sich nicht innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen des Werts.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Color Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set Color Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set Color Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Color',
'elements': [('R', 'uint16', 1, 'out', {}),
             ('G', 'uint16', 1, 'out', {}),
             ('B', 'uint16', 1, 'out', {}),
             ('C', 'uint16', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Color Callback Configuration`. The :word:`parameter` is the color
of the sensor as RGBC.

The :cb:`Color` callback is only triggered if the color has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Color Callback Configuration`,
ausgelöst. Der :word:`parameter` ist die Farbe des Sensors als RGBC.

Der :cb:`Color` Callback wird nur ausgelöst, wenn sich die Farbe seit der
letzten Auslösung geändert hat.
"""
}]
})

illuminance_doc = {
'en':
"""
Returns the illuminance affected by the gain and integration time as
set by :func:`Set Configuration`. To get the illuminance in Lux apply this formula::

 lux = illuminance * 700 / gain / integration_time

To get a correct illuminance measurement make sure that the color
values themselves are not saturated. The color value (R, G or B)
is saturated if it is equal to the maximum value of 65535.
In that case you have to reduce the gain, see :func:`Set Configuration`.
""",
'de':
"""
Gibt die Beleuchtungsstärke beeinflusst durch die Verstärkung und die
Integrationszeit zurück. Verstärkung und Integrationszeit können mit
:func:`Set Configuration` eingestellt werden. Um die Beleuchtungsstärke in Lux zu
ermitteln, muss folgende Formel angewendet werden::

 lux = illuminance * 700 / gain / integration_time

Für eine korrekte Messung der Beleuchtungsstärke muss sichergestellt
sein, dass die Farbwerte (R, G oder B) nicht saturiert sind. Ein
Farbwert ist saturiert, wenn der Wert 65535 beträgt. In diesem Fall
kann die Verstärkung per :func:`Set Configuration` reduziert werden.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Illuminance',
    data_name = 'Illuminance',
    data_type = 'uint32',
    doc       = illuminance_doc,
    scale     = 'dynamic',
    unit      = 'Lux',
    range_    = (0, 103438)
)

color_temperature_doc = {
'en':
"""
Returns the color temperature.

To get a correct color temperature measurement make sure that the color
values themselves are not saturated. The color value (R, G or B)
is saturated if it is equal to the maximum value of 65535.
In that case you have to reduce the gain, see :func:`Set Configuration`.
""",
'de':
"""
Gibt die Farbtemperatur zurück.

Für eine korrekte Messung der Farbtemperatur muss sichergestellt
sein, dass die Farbwerte (R, G oder B) nicht saturiert sind. Ein
Farbwert ist saturiert, wenn der Wert 65535 beträgt. In diesem Fall
kann die Verstärkung per :func:`Set Configuration` reduziert werden.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Color Temperature',
    data_name = 'Color Temperature',
    data_type = 'uint16',
    doc       = color_temperature_doc,
    unit      = 'Kelvin'
)

com['packets'].append({
'type': 'function',
'name': 'Set Light',
'elements': [('Enable', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Turns the white LED on the Bricklet on/off.
""",
'de':
"""
Aktiviert/deaktiviert die weiße LED auf dem Bricklet.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Light',
'elements': [('Enable', 'bool', 1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the value as set by :func:`Set Light`.
""",
'de':
"""
Gibt den Wert zurück, wie von :func:`Set Light` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('Gain', 'uint8', 1, 'in', {'constant_group': 'Gain', 'default': 3}),
             ('Integration Time', 'uint8', 1, 'in', {'constant_group': 'Integration Time', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the configuration of the sensor. Gain and integration time
can be configured this way.

For configuring the gain:

* 0: 1x Gain
* 1: 4x Gain
* 2: 16x Gain
* 3: 60x Gain

For configuring the integration time:

* 0: 2.4ms
* 1: 24ms
* 2: 101ms
* 3: 154ms
* 4: 700ms

Increasing the gain enables the sensor to detect a
color from a higher distance.

The integration time provides a trade-off between conversion time
and accuracy. With a longer integration time the values read will
be more accurate but it will take longer to get the conversion
results.
""",
'de':
"""
Setzt die Konfiguration des Sensors. Verstärkung und Integrationszeit können
eingestellt werden.

Für die Konfiguration der Verstärkung:

* 0: 1x Gain
* 1: 4x Gain
* 2: 16x Gain
* 3: 60x Gain

Für die Konfiguration der Integrationszeit:

* 0: 2,4ms
* 1: 24ms
* 2: 101ms
* 3: 154ms
* 4: 700ms

Eine Erhöhung der Verstärkung ermöglicht es dem Sensor, Farben aus größeren
Entfernungen zu erkennen.

Die Integrationszeit ist ein Trade-off zwischen Konvertierungszeit und
Genauigkeit. Mit einer höheren Integrationszeit werden die Werte genauer,
es dauert allerdings länger, bis ein Resultat bereitsteht.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Gain', 'uint8', 1, 'out', {'constant_group': 'Gain', 'default': 3}),
             ('Integration Time', 'uint8', 1, 'out', {'constant_group': 'Integration Time', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the configuration as set by :func:`Set Configuration`.
""",
'de':
"""
Gibt die Einstellungen zurück, wie von :func:`Set Configuration` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Color', 'color'), [(('R', 'Color [R]'), 'uint16', 1, None, None, None), (('G', 'Color [G]'), 'uint16', 1, None, None, None), (('B', 'Color [B]'), 'uint16', 1, None, None, None), (('C', 'Color [C]'), 'uint16', 1, None, None, None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Color', 'color'), [(('R', 'Color [R]'), 'uint16', 1, None, None, None), (('G', 'Color [G]'), 'uint16', 1, None, None, None), (('B', 'Color [B]'), 'uint16', 1, None, None, None), (('C', 'Color [C]'), 'uint16', 1, None, None, None)], None, None),
              ('callback_configuration', ('Color', 'color'), [], 100, False, None, [])]
})


com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.HSBType', 'org.eclipse.smarthome.core.library.types.OnOffType'],
    'params': [{
            'packet': 'Set Configuration',
            'element': 'Gain',

            'name': 'Gain',
            'type': 'integer',
            'options': [('1x', 0),
                        ('4x', 1),
                        ('16x', 2),
                        ('60x', 3)],
            'limit_to_options': 'true',
            'default': 3,

            'label': 'Gain',
            'description': 'Increasing the gain enables the sensor to detect a color from a higher distance.',
        }, {
            'packet': 'Set Configuration',
            'element': 'Integration Time',

            'name': 'Integration Time',
            'type': 'integer',
            'options': [('2ms', 0),
                        ('24ms', 1),
                        ('101ms', 2),
                        ('154ms', 3),
                        ('700ms', 4)],
            'limit_to_options': 'true',
            'default': 3,

            'label': 'Integration Time',
            'description': 'The integration time provides a trade-off between conversion time and accuracy. With a longer integration time the values read will be more accurate but it will take longer time to get the conversion results.',
        }],
    'param_groups': oh_generic_channel_param_groups(),
    'init_code': """this.setConfiguration(cfg.gain, cfg.integrationTime);""",
    'channels': [
        {
            'id': 'Color',
            'type': 'Color',
            'init_code':"""this.set{camel}CallbackConfiguration(channelCfg.updateInterval, true);""",
            'dispose_code': """this.set{camel}CallbackConfiguration(0, false);""",

            'getters': [{
                'packet': 'Get Color',
                'transform': 'HSBType.fromRGB(value.r * 255 / 65535, value.g * 255 / 65535, value.b * 255 / 65535)'}],
            'callbacks': [{
                'packet': 'Color',
                'transform': 'HSBType.fromRGB(r * 255 / 65535, g * 255 / 65535, b * 255 / 65535)'}]
        },
        oh_generic_channel('Illuminance', 'Illuminance', 'SmartHomeUnits.LUX', divisor='cfg.gain * cfg.integrationTime / 700.0'),
        oh_generic_channel('Color Temperature', 'Color Temperature', 'SmartHomeUnits.KELVIN', divisor=1),
        {
            'id': 'Light',
            'type': 'Light',
            'getters': [{
                'packet': 'Get Light',
                'transform': 'value ? OnOffType.ON : OnOffType.OFF'}],
            'setters': [{
                'packet': 'Set Light',
                'packet_params': ['cmd == OnOffType.ON'],
                'command_type': 'OnOffType'
            }],

        },
    ],
    'channel_types': [
        oh_generic_channel_type('Color', 'Color', 'Color',
                    update_style='Callback Configuration',
                    description='Measured color',
                    read_only=True),
        oh_generic_channel_type('Illuminance', 'Number:Illuminance', 'Illuminance',
                    update_style='Callback Configuration',
                    description='Measured illuminance. To get a correct illuminance measurement make sure that the color values themself are not saturated. The color value (R, G or B) is saturated if it is equal to the maximum value of 255. In that case you have to reduce the gain.',
                    read_only=True),
        oh_generic_channel_type('Color Temperature', 'Number:Temperature', 'Color Temperature',
                    update_style='Callback Configuration',
                    description='To get a correct color temperature measurement make sure that the color values themself are not saturated. The color value (R, G or B) is saturated if it is equal to the maximum value of 255. In that case you have to reduce the gain.',
                    read_only=True),
        oh_generic_channel_type('Light', 'Switch', 'Enable Light',
                    update_style=None,
                    description='Turns the white LED on the Bricklet on/off.'),
    ],
    'actions': ['Get Color', 'Get Illuminance', 'Get Color Temperature', {'fn': 'Set Light', 'refreshs': ['Light']}, 'Get Light', 'Get Configuration']
}
