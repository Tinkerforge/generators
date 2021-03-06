# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Color Bricklet communication config

from generators.configs.commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Ishraq Ibne Ashraf <ishraq@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 243,
    'name': 'Color',
    'display_name': 'Color',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures color (RGB value), illuminance and color temperature',
        'de': 'Misst Farbe (RGB Wert), Beleuchtungsstärke und Farbtemperatur'
    },
    'released': True,
    'documented': True,
    'discontinued': False, # selling remaining stock, replaced by CAN Bricklet 2.0
    'features': [
        'device',
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

com['constant_groups'].append({
'name': 'Light',
'type': 'uint8',
'constants': [('On', 0),
              ('Off', 1)]
})

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
:func:`Set Color Callback Period`.
""",
'de':
"""
Gibt die gemessene Farbe des Sensors zurück.

Die rot (r), grün (g), blau (b) und clear (c) werden mit vier
unterschiedlichen Fotodioden gemessen. Diese sind Empfindlich
in unterschiedlichen Wellenlängen:

.. image:: /Images/Bricklets/bricklet_color_wavelength_chart_600.jpg
   :scale: 100 %
   :alt: Chart Responsivity / Wavelength
   :align: center
   :target: ../../_images/Bricklets/bricklet_color_wavelength_chart_600.jpg

Wenn die Farbe periodisch abgefragt werden soll, wird empfohlen
den :cb:`Color` Callback zu nutzen und die Periode mit
:func:`Set Color Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Color Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Color` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Color` callback is only triggered if the color has changed since the
last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Color` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Color` Callback wird nur ausgelöst, wenn sich die Color seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Color Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Color Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Color Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Color Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min R', 'uint16', 1, 'in', {'default': 0}),
             ('Max R', 'uint16', 1, 'in', {'default': 0}),
             ('Min G', 'uint16', 1, 'in', {'default': 0}),
             ('Max G', 'uint16', 1, 'in', {'default': 0}),
             ('Min B', 'uint16', 1, 'in', {'default': 0}),
             ('Max B', 'uint16', 1, 'in', {'default': 0}),
             ('Min C', 'uint16', 1, 'in', {'default': 0}),
             ('Max C', 'uint16', 1, 'in', {'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Color Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the temperature is *outside* the min and max values"
 "'i'",    "Callback is triggered when the temperature is *inside* the min and max values"
 "'<'",    "Callback is triggered when the temperature is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the temperature is greater than the min value (max is ignored)"
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Color Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn die Temperatur *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn die Temperatur *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn die Temperatur kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn die Temperatur größer als der min Wert ist (max wird ignoriert)"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Color Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min R', 'uint16', 1, 'out', {'default': 0}),
             ('Max R', 'uint16', 1, 'out', {'default': 0}),
             ('Min G', 'uint16', 1, 'out', {'default': 0}),
             ('Max G', 'uint16', 1, 'out', {'default': 0}),
             ('Min B', 'uint16', 1, 'out', {'default': 0}),
             ('Max B', 'uint16', 1, 'out', {'default': 0}),
             ('Min C', 'uint16', 1, 'out', {'default': 0}),
             ('Max C', 'uint16', 1, 'out', {'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Color Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Color Callback Threshold` gesetzt.
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

* :cb:`Color Reached`

is triggered, if the threshold

* :func:`Set Color Callback Threshold`

keeps being reached.
""",
'de':
"""
Setzt die Periode mit welcher die Schwellwert Callback

* :cb:`Color Reached`

ausgelöst wird, wenn der Schwellwert

* :func:`Set Color Callback Threshold`

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
:func:`Set Color Callback Period`. The :word:`parameter` is the color
of the sensor as RGBC.

The :cb:`Color` callback is only triggered if the color has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Color Callback Period`,
ausgelöst. Der :word:`parameter` ist die Farbe des Sensors als RGBC.

Der :cb:`Color` Callback wird nur ausgelöst, wenn sich die Farbe seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Color Reached',
'elements': [('R', 'uint16', 1, 'out', {}),
             ('G', 'uint16', 1, 'out', {}),
             ('B', 'uint16', 1, 'out', {}),
             ('C', 'uint16', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Color Callback Threshold` is reached.
The :word:`parameter` is the color
of the sensor as RGBC.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Color Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Farbe des Sensors als RGBC.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Light On',
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
'name': 'Light Off',
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
'name': 'Is Light On',
# FIXME: should return bool, but cannot be fixed because the Bricklet returns 0 for "On"
'elements': [('Light', 'uint8', 1, 'out', {'constant_group': 'Light', 'default': 1})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the state of the LED. Possible values are:

* 0: On
* 1: Off
""",
'de':
"""
Gibt den Zustand der LED zurück. Mögliche Werte sind:

* 0: On
* 1: Off
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Config',
'elements': [('Gain', 'uint8', 1, 'in', {'constant_group': 'Gain', 'default': 3}),
             ('Integration Time', 'uint8', 1, 'in', {'constant_group': 'Integration Time', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the configuration of the sensor. Gain and integration time
can be configured in this way.

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
be more accurate but it will take longer time to get the conversion
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

Eine Erhöhung der Verstärkung ermöglicht es dem Sensor Farben aus größeren
Entfernungen zu erkennen.

Die Integrationszeit ist ein Trade-off zwischen Konvertierungszeit und
Genauigkeit. Mit einer höheren Integrationszeit werden die Werte genauer,
es dauert allerdings länger bis ein Resultat bereitsteht.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Config',
'elements': [('Gain', 'uint8', 1, 'out', {'constant_group': 'Gain', 'default': 3}),
             ('Integration Time', 'uint8', 1, 'out', {'constant_group': 'Integration Time', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the configuration as set by :func:`Set Config`.
""",
'de':
"""
Gibt die Einstellungen zurück, wie von :func:`Set Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Illuminance',
'elements': [('Illuminance', 'uint32', 1, 'out', {'scale': 'dynamic', 'unit': 'Lux', 'range': (0, 103438)})], # range end as by the firmware implementation
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the illuminance affected by the gain and integration time as
set by :func:`Set Config`. To get the illuminance in Lux apply this formula::

 lux = illuminance * 700 / gain / integration_time

To get a correct illuminance measurement make sure that the color
values themselves are not saturated. The color value (R, G or B)
is saturated if it is equal to the maximum value of 65535.
In that case you have to reduce the gain, see :func:`Set Config`.
""",
'de':
"""
Gibt die Beleuchtungsstärke beeinflusst durch die Verstärkung und die
Integrationszeit zurück. Verstärkung und Integrationszeit können mit
:func:`Set Config` eingestellt werden. Um die Beleuchtungsstärke in Lux zu
ermitteln muss folgende Formel angewendet werden::

 lux = illuminance * 700 / gain / integration_time

Für eine korrekte Messung der Beleuchtungsstärke muss sichergestellt
sein, dass die Farbwerte (R, G oder B) nicht saturiert sind. Ein
Farbwert ist saturiert wenn der Wert 65535 beträgt. In diesem Fall
kann die Verstärkung per :func:`Set Config` reduziert werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Color Temperature',
'elements': [('Color Temperature', 'uint16', 1, 'out', {'unit': 'Kelvin'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the color temperature.

To get a correct color temperature measurement make sure that the color
values themselves are not saturated. The color value (R, G or B)
is saturated if it is equal to the maximum value of 65535.
In that case you have to reduce the gain, see :func:`Set Config`.
""",
'de':
"""
Gibt die Farbtemperatur zurück.

Für eine korrekte Messung der Farbtemperatur muss sichergestellt
sein das die Farbwerte (R, G oder B) nicht saturiert sind. Ein
Farbwert ist saturiert wenn der Wert 65535 beträgt. In diesem Fall
kann die Verstärkung per :func:`Set Config` reduziert werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Illuminance Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Illuminance` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Illuminance` callback is only triggered if the illuminance has changed
since the last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Illuminance` Callback ausgelöst
wird. Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Illuminance` Callback wird nur ausgelöst, wenn sich die
Beleuchtungsstärke seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Illuminance Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Illuminance Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Illuminance Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Color Temperature Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Color Temperature` callback is
triggered periodically. A value of 0 turns the callback off.

The :cb:`Color Temperature` callback is only triggered if the color temperature
has changed since the last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Color Temperature` Callback
ausgelöst wird. Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Color Temperature` Callback wird nur ausgelöst, wenn sich die
Farbtemperatur seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Color Temperature Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Color Temperature Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Color Temperature Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Illuminance',
'elements': [('Illuminance', 'uint32', 1, 'out', {'scale': 'dynamic', 'unit': 'Lux', 'range': (0, 103438)})], # range end as by the firmware implementation
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Illuminance Callback Period`. The :word:`parameter` is the illuminance.
See :func:`Get Illuminance` for how to interpret this value.

The :cb:`Illuminance` callback is only triggered if the illuminance has changed
since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Illuminance Callback Period`,
ausgelöst. Der :word:`parameter` ist die Beleuchtungsstärke des Sensors.
Siehe :func:`Get Illuminance` für eine Erklärung wie dieser zu interpretieren ist.

Der :cb:`Illuminance` Callback wird nur ausgelöst, wenn sich die
Beleuchtungsstärke seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Color Temperature',
'elements': [('Color Temperature', 'uint16', 1, 'out', {'unit': 'Kelvin'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Color Temperature Callback Period`. The :word:`parameter` is the
color temperature.

The :cb:`Color Temperature` callback is only triggered if the color temperature
has changed since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Color Temperature Callback Period`, ausgelöst. Der :word:`parameter`
ist die Farbtemperatur des Sensors.

Der :cb:`Color Temperature` Callback wird nur ausgelöst, wenn sich die
Farbtemperatur seit der letzten Auslösung geändert hat.
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
              ('callback_period', ('Color', 'color'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('Color Reached', 'color reached'), [(('R', 'Color [R]'), 'uint16', 1, None, None, None), (('G', 'Color [G]'), 'uint16', 1, None, None, None), (('B', 'Color [B]'), 'uint16', 1, None, None, None), (('C', 'Color [C]'), 'uint16', 1, None, None, None)], None, None),
              ('callback_threshold', ('Color', 'color'), [], '>', [(100, 0), (200, 0), (300, 0), (400, 0)])]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.HSBType', 'org.eclipse.smarthome.core.library.types.OnOffType'],
    'params': [{
            'packet': 'Set Config',
            'element': 'Gain',

            'name': 'Gain',
            'type': 'integer',

            'label': {'en': 'Gain', 'de': 'Verstärkung'},
            'description': {'en': 'Increasing the gain enables the sensor to detect a color from a higher distance.',
                            'de': 'Eine Erhöhung der Verstärkung ermöglicht es dem Sensor Farben aus größeren Entfernungen zu erkennen.'}
        }, {
            'packet': 'Set Config',
            'element': 'Integration Time',

            'name': 'Integration Time',
            'type': 'integer',
            'label': {'en': 'Integration Time', 'de': 'Integrationszeit'},
            'description': {'en': 'The integration time provides a trade-off between conversion time and accuracy. With a longer integration time the values read will be more accurate but it will take longer time to get the conversion results.',
                            'de': 'Die Integrationszeit ist ein Trade-off zwischen Konvertierungszeit und Genauigkeit. Mit einer höheren Integrationszeit werden die Werte genauer, es dauert allerdings länger bis ein Resultat bereitsteht.'}
        }],
    'param_groups': oh_generic_channel_param_groups(),
    'init_code': """this.setConfig(cfg.gain.shortValue(), cfg.integrationTime.shortValue());""",
    'channels': [
        {
            'id': 'Color',
            'type': 'Color',
            'init_code':"""this.set{camel}CallbackPeriod(channelCfg.updateInterval);""",
            'dispose_code': """this.set{camel}CallbackPeriod(0);""",

            'getters': [{
                'packet': 'Get Color',
                'transform': 'HSBType.fromRGB(value.r * 255 / 65535, value.g * 255 / 65535, value.b * 255 / 65535)'}],
            'callbacks': [{
                'packet': 'Color',
                'transform': 'HSBType.fromRGB(r * 255 / 65535, g * 255 / 65535, b * 255 / 65535)'}]
        },
        oh_generic_old_style_channel('Illuminance', 'Illuminance', divisor='cfg.gain * cfg.integrationTime / 700.0', has_threshold=False),
        oh_generic_old_style_channel('Color Temperature', 'Color Temperature', has_threshold=False),
        {
            'id': 'Light',
            'type': 'Light',
            'getters': [{
                'packet': 'Is Light On',
                'transform': 'value == 0 ? OnOffType.ON : OnOffType.OFF'}],
            'setters': [{
                    'predicate': 'cmd == OnOffType.ON',
                    'packet': 'Light On',
                    'command_type': 'OnOffType'
                }, {
                    'predicate': 'cmd == OnOffType.OFF',
                    'packet': 'Light Off',
                    'command_type': 'OnOffType'
                }],
        },
    ],
    'channel_types': [
        oh_generic_channel_type('Color', 'Color', {'en': 'Color', 'de': 'Farbe'},
                    update_style='Callback Period',
                    description={'en': 'The measured color', 'de': 'Die gemessene Farbe'}),
        oh_generic_channel_type('Illuminance', 'Number', {'en': 'Illuminance', 'de': 'Beleuchtungsstärke'},
                    update_style='Callback Period',
                    description={'en': 'The measured illuminance. To get a correct illuminance measurement make sure that the color values themself are not saturated. The color value (R, G or B) is saturated if it is equal to the maximum value of 255. In that case you have to reduce the gain.',
                                 'de': 'Die gemessene Beleuchtungsstärke. Für eine korrekte Messung der Beleuchtungsstärke muss sichergestellt sein, dass die Farbwerte (R, G oder B) nicht saturiert sind. Ein Farbwert ist saturiert wenn der Wert 255 beträgt. In diesem Fall muss die Verstärkung reduziert werden.'}),
        oh_generic_channel_type('Color Temperature', 'Number', {'en': 'Color Temperature', 'de': 'Farbtemperatur'},
                    update_style='Callback Period',
                    description={'en': 'To get a correct color temperature measurement make sure that the color values themself are not saturated. The color value (R, G or B) is saturated if it is equal to the maximum value of 255. In that case you have to reduce the gain.',
                                 'de': 'Für eine korrekte Messung der Farbtemperatur muss sichergestellt sein das die Farbwerte (R, G oder B) nicht saturiert sind. Ein Farbwert ist saturiert wenn der Wert 255 beträgt. In diesem Fall muss die Verstärkung reduziert werden.'}),
        oh_generic_channel_type('Light', 'Switch', {'en': 'Light', 'de': 'Licht'},
                    update_style=None,
                    description={'en': 'Turns the white LED on the Bricklet on/off.',
                                 'de': 'Schaltet die weiße LED am Bricklet an/aus.'}),
    ],
    'actions': ['Get Color', {'fn': 'Light On', 'refreshs': ['Light']}, {'fn': 'Light Off', 'refreshs': ['Light']}, 'Is Light On', 'Get Config', 'Get Illuminance', 'Get Color Temperature']
}

