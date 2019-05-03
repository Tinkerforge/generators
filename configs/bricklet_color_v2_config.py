# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Color Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

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
    'released': False,
    'documented': False,
    'discontinued': False,
    'features': [
        'comcu_bricklet',
        'bricklet_get_identity'
    ],
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Get Color',
'elements': [('R', 'uint16', 1, 'out'),
             ('G', 'uint16', 1, 'out'),
             ('B', 'uint16', 1, 'out'),
             ('C', 'uint16', 1, 'out')],
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
to use the :cb:`Color` callback and set the period with
:func:`Set Color Callback Configuration`.
""",
'de':
"""
Gibt die gemessene Farbe des Sensors zurück. Der Wertebereich ist von
0 bis 65535.

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
:func:`Set Color Callback Configuration` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Color Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period in ms is the period with which the :cb:`Color`
callback is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.

The default value is (0, false).
""",
'de':
"""
Die Periode in ms ist die Periode mit der der :cb:`Color`
Callback ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn der Wert sich im Vergleich zum letzten mal geändert
hat. Ändert der Wert sich nicht innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen des Werts.

Der Standardwert ist (0, false).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Color Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
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
'elements': [('R', 'uint16', 1, 'out'),
             ('G', 'uint16', 1, 'out'),
             ('B', 'uint16', 1, 'out'),
             ('C', 'uint16', 1, 'out')],
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

Der :cb:`Color` Callback wird nur ausgelöst wenn sich die Farbe seit der
letzten Auslösung geändert hat.
"""
}]
})

illuminance_doc = {
'en':
"""
Returns the illuminance affected by the gain and integration time as
set by :func:`Set Config`. To get the illuminance in Lux apply this formula::

 lux = illuminance * 700 / gain / integration_time

To get a correct illuminance measurement make sure that the color
values themself are not saturated. The color value (R, G or B)
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
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Illuminance',
    data_name = 'Illuminance',
    data_type = 'uint32',
    doc       = illuminance_doc
)

color_temperature_doc = {
'en':
"""
Returns the color temperature in Kelvin.

To get a correct color temperature measurement make sure that the color
values themself are not saturated. The color value (R, G or B)
is saturated if it is equal to the maximum value of 65535.
In that case you have to reduce the gain, see :func:`Set Config`.
""",
'de':
"""
Gibt die Farbtemperatur in Kelvin zurück.

Für eine korrekte Messung der Farbtemperatur muss sichergestellt
sein das die Farbwerte (R, G oder B) nicht saturiert sind. Ein
Farbwert ist saturiert wenn der Wert 65535 beträgt. In diesem Fall
kann die Verstärkung per :func:`Set Config` reduziert werden.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Color Temperature',
    data_name = 'Color Temperature',
    data_type = 'uint16',
    doc       = color_temperature_doc
)

com['packets'].append({
'type': 'function',
'name': 'Set Light',
'elements': [('Enable', 'bool', 1, 'in')],
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
'elements': [('Enable', 'bool', 1, 'out')],
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
'name': 'Set Config',
'elements': [('Gain', 'uint8', 1, 'in', ('Gain', [('1x', 0),
                                                  ('4x', 1),
                                                  ('16x', 2),
                                                  ('60x', 3)])),
             ('Integration Time', 'uint8', 1, 'in', ('Integration Time', [('2ms', 0),
                                                                          ('24ms', 1),
                                                                          ('101ms', 2),
                                                                          ('154ms', 3),
                                                                          ('700ms', 4)]))],
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
'name': 'Get Config',
'elements': [('Gain', 'uint8', 1, 'out', ('Gain', [('1x', 0),
                                                   ('4x', 1),
                                                   ('16x', 2),
                                                   ('60x', 3)])),
             ('Integration Time', 'uint8', 1, 'out', ('Integration Time', [('2ms', 0),
                                                                           ('24ms', 1),
                                                                           ('101ms', 2),
                                                                           ('154ms', 3),
                                                                           ('700ms', 4)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the configuration as set by :func:`Set Config`.
""",
'de':
"""
Gibt die Einstellungen zurück, wie von :func:`Set Config`
gesetzt.
"""
}]
})


