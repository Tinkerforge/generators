# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Color Bricklet communication config

com = {
    'author': 'Ishraq Ibne Ashraf <ishraq@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 243,
    'name': ('Color', 'color', 'Color'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for measuring color (RGB value), illuminance and color temperature',
    'released': True,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetColor', 'get_color'), 
'elements': [('r', 'uint16', 1, 'out'),
             ('g', 'uint16', 1, 'out'),
             ('b', 'uint16', 1, 'out'),
             ('c', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the measured color of the sensor. The values
have a range of 0 to 65535.

The red (r), green (g), blue (b) and clear (c) colors are measured
with four different photodiodes that are responsive at different
wavelengths:

.. image:: /Images/Bricklets/bricklet_color_wavelength_chart_600.jpg
   :scale: 100 %
   :alt: Chart Responsivity / Wavelength
   :align: center
   :target: ../../_images/Bricklets/bricklet_color_wavelength_chart_600.jpg

If you want to get the color periodically, it is recommended 
to use the callback :func:`Color` and set the period with 
:func:`SetColorCallbackPeriod`.
""",
'de':
"""
Gibt die gemessene Farbe des Sensors zurück. Der Wertebereich ist von
0 bis 65535.

Die rot (r), grün (g), blau (b) and clear (c) werden mit vier
unterschiedlichen Fotodioden gemessen. Diese sind Empfindlich
in unterschiedlichen Wellenlängen:

.. image:: /Images/Bricklets/bricklet_color_wavelength_chart_600.jpg
   :scale: 100 %
   :alt: Chart Responsivity / Wavelength
   :align: center
   :target: ../../_images/Bricklets/bricklet_color_wavelength_chart_600.jpg

Wenn die Farbe periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`Color` zu nutzen und die Periode mit 
:func:`SetColorCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetColorCallbackPeriod', 'set_color_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Color` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Color` is only triggered if the color has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Color` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Color` wird nur ausgelöst wenn sich die Color seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetColorCallbackPeriod', 'get_color_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetColorCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetColorCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetColorCallbackThreshold', 'set_color_callback_threshold'), 
'elements': [('option', 'char', 1, 'in', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                  ('Outside', 'outside', 'o'),
                                                                                  ('Inside', 'inside', 'i'),
                                                                                  ('Smaller', 'smaller', '<'),
                                                                                  ('Greater', 'greater', '>')])), 
             ('min_r', 'uint16', 1, 'in'),
             ('max_r', 'uint16', 1, 'in'),
             ('min_g', 'uint16', 1, 'in'),
             ('max_g', 'uint16', 1, 'in'),
             ('min_b', 'uint16', 1, 'in'),
             ('max_b', 'uint16', 1, 'in'),
             ('min_c', 'uint16', 1, 'in'),
             ('max_c', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`ColorReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the temperature is *outside* the min and max values"
 "'i'",    "Callback is triggered when the temperature is *inside* the min and max values"
 "'<'",    "Callback is triggered when the temperature is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the temperature is greater than the min value (max is ignored)"

The default value is ('x', 0, 0, 0, 0, 0, 0, 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`ColorReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Temperatur *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn die Temperatur *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn die Temperatur kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Temperatur größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0, 0, 0, 0, 0, 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetColorCallbackThreshold', 'get_color_callback_threshold'), 
'elements': [('option', 'char', 1, 'out', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                   ('Outside', 'outside', 'o'),
                                                                                   ('Inside', 'inside', 'i'),
                                                                                   ('Smaller', 'smaller', '<'),
                                                                                   ('Greater', 'greater', '>')])), 
             ('min_r', 'uint16', 1, 'out'),
             ('max_r', 'uint16', 1, 'out'),
             ('min_g', 'uint16', 1, 'out'),
             ('max_g', 'uint16', 1, 'out'),
             ('min_b', 'uint16', 1, 'out'),
             ('max_b', 'uint16', 1, 'out'),
             ('min_c', 'uint16', 1, 'out'),
             ('max_c', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`SetColorCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetColorCallbackThreshold`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetDebouncePeriod', 'set_debounce_period'), 
'elements': [('debounce', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the threshold callback

* :func:`ColorReached`

is triggered, if the threshold

* :func:`SetColorCallbackThreshold`

keeps being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callback

* :func:`ColorReached`
 
ausgelöst wird, wenn der Schwellwert 

* :func:`SetColorCallbackThreshold`
 
weiterhin erreicht bleibt.

Der Standardwert ist 100.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetDebouncePeriod', 'get_debounce_period'), 
'elements': [('debounce', 'uint32', 1, 'out')],
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
'name': ('Color', 'color'), 
'elements': [('r', 'uint16', 1, 'out'),
             ('g', 'uint16', 1, 'out'),
             ('b', 'uint16', 1, 'out'),
             ('c', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetColorCallbackPeriod`. The :word:`parameter` is the color
of the sensor as RGBC.

:func:`Color` is only triggered if the color has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetColorCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die Farbe des Sensors als RGBC

:func:`Color` wird nur ausgelöst wenn sich die Farbe seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('ColorReached', 'color_reached'), 
'elements': [('r', 'uint16', 1, 'out'),
             ('g', 'uint16', 1, 'out'),
             ('b', 'uint16', 1, 'out'),
             ('c', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetColorCallbackPeriod`. The :word:`parameter` is the color
of the sensor as RGBC.

:func:`Color` is only triggered if the color has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetColorCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die Farbe des Sensors als RGBC.

:func:`Color` wird nur ausgelöst wenn sich die Farbe seit der
letzten Auslösung geändert hat.
"""
}]
})


com['packets'].append({
'type': 'function',
'name': ('LightOn', 'light_on'), 
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
'name': ('LightOff', 'light_off'), 
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
'name': ('IsLightOn', 'is_light_on'), 
'elements': [('light', 'uint8', 1, 'out', ('Light', 'light', [('On', 'on', 0),
                                                              ('Off', 'off', 1)]))],
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
'name': ('SetConfig', 'set_config'), 
'elements': [('gain', 'uint8', 1, 'in', ('Gain', 'gain', [('1x', '1x', 0),
                                                          ('4x', '4x', 1),
                                                          ('16x', '16x', 2),
                                                          ('60x', '60x', 3)])),
             ('integration_time', 'uint8', 1, 'in', ('IntegrationTime', 'integration_time', [('2ms', '2ms', 0),
                                                                                             ('24ms', '24ms', 1),
                                                                                             ('101ms', '101ms', 2),
                                                                                             ('154ms', '154ms', 3),
                                                                                             ('700ms', '700ms', 4)]))],
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

The default values are 60x gain and 154ms integration time.
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

Die Standardwerte sind 60x Verstärkung und 154ms Integrationszeit.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetConfig', 'get_config'), 
'elements': [('gain', 'uint8', 1, 'out', ('Gain', 'gain', [('1x', '1x', 0),
                                                            ('4x', '4x', 1),
                                                            ('16x', '16x', 2),
                                                            ('60x', '60x', 3)])),
             ('integration_time', 'uint8', 1, 'out', ('IntegrationTime', 'integration_time', [('2ms', '2ms', 0),
                                                                                              ('24ms', '24ms', 1),
                                                                                              ('101ms', '101ms', 2),
                                                                                              ('154ms', '154ms', 3),
                                                                                              ('700ms', '700ms', 4)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the configuration as set by :func:`SetConfig`.
""",
'de':
"""
Gibt die Einstellungen zurück, wie von :func:`SetConfig`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetIlluminance', 'get_illuminance'), 
'elements': [('illuminance', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the illuminance affected by the gain and integration time as
set by :func:`SetConfig`. To get the illuminance in Lux apply this formula::

 lux = illuminance * 700 / gain / integration_time

To get a correct illuminance measurement make sure that the color
values themself are not saturated. The color value (R, G or B)
is saturated if it is equal to the maximum value of 65535.
In that case you have to reduce the gain, see :func:`SetConfig`.
""",
'de':
"""
Gibt die Beleuchtungsstärke beeinflusst durch die Verstärkung und die
Integrationszeit zurück. Verstärkung und Integrationszeit können mit
:func:`SetConfig` eingestellt werden. Um die Beleuchtungsstärke in Lux zu
ermitteln muss folgende Formel angewendet werden::

 lux = illuminance * 700 / gain / integration_time

Für eine korrekte Messung der Beleuchtungsstärke muss sichergestellt
sein, dass die Farbwerte (R, G oder B) nicht saturiert sind. Ein
Farbwert ist saturiert wenn der Wert 65535 beträgt. In diesem Fall
kann die Verstärkung per :func:`SetConfig` reduziert werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetColorTemperature', 'get_color_temperature'), 
'elements': [('color_temperature', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the color temperature in Kelvin.

To get a correct color temperature measurement make sure that the color
values themself are not saturated. The color value (R, G or B)
is saturated if it is equal to the maximum value of 65535.
In that case you have to reduce the gain, see :func:`SetConfig`.
""",
'de':
"""
Gibt die Farbtemperatur in Kelvin zurück.

Für eine korrekte Messung der Farbtemperatur muss sichergestellt
sein das die Farbwerte (R, G oder B) nicht saturiert sind. Ein
Farbwert ist saturiert wenn der Wert 65535 beträgt. In diesem Fall
kann die Verstärkung per :func:`SetConfig` reduziert werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetIlluminanceCallbackPeriod', 'set_illuminance_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Illuminance` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Illuminance` is only triggered if the illuminance has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Illuminance` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Illuminance` wird nur ausgelöst wenn sich die Beleuchtungsstärke seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetIlluminanceCallbackPeriod', 'get_illuminance_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetIlluminanceCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetIlluminanceCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetColorTemperatureCallbackPeriod', 'set_color_temperature_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`ColorTemperature` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`ColorTemperature` is only triggered if the color temperature has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`ColorTemperature` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`ColorTemperature` wird nur ausgelöst wenn sich die Farbtemperatur seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetColorTemperatureCallbackPeriod', 'get_color_temperature_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetColorTemperatureCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetColorTemperatureCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('Illuminance', 'illuminance'), 
'elements': [('illuminance', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetIlluminanceCallbackPeriod`. The :word:`parameter` is the illuminance.
See :func:`GetIlluminance` for how to interrept this value.

:func:`Illuminance` is only triggered if the illuminance has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetIlluminanceCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die Beleuchtungsstärke des Sensors.
Siehe :func:`GetIlluminance` für eine Erklärung wie dieser zu interpretieren ist.

:func:`Illuminance` wird nur ausgelöst wenn sich die Beleuchtungsstärke seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('ColorTemperature', 'color_temperature'), 
'elements': [('color_temperature', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetColorTemperatureCallbackPeriod`. The :word:`parameter` is the 
color temperature in Kelvin.

:func:`ColorTemperature` is only triggered if the color temperature has 
changed since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetColorTemperatureCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die Farbtemperatur des Sensors in Kelvin.

:func:`ColorTemperature` wird nur ausgelöst wenn sich die Farbtemperatur seit der
letzten Auslösung geändert hat.
"""
}]
})

