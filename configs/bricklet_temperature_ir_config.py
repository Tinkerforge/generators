# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Temperature IR Bricklet communication config

from commonconstants import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 217,
    'name': 'Temperature IR',
    'display_name': 'Temperature IR',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures contactless object temperature between -70°C and +380°C',
        'de': 'Kontaktlose Objekttemperaturmessung zwischen -70°C und +380°C'
    },
    'released': True,
    'documented': True,
    'discontinued': True, # replaced by Temperature IR Bricklet 2.0
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
'name': 'Get Ambient Temperature',
'elements': [('Temperature', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the ambient temperature of the sensor. The value
has a range of -400 to 1250 and is given in °C/10,
e.g. a value of 423 means that an ambient temperature of 42.3 °C is
measured.

If you want to get the ambient temperature periodically, it is recommended
to use the :cb:`Ambient Temperature` callback and set the period with
:func:`Set Ambient Temperature Callback Period`.
""",
'de':
"""
Gibt die Umgebungstemperatur des Sensors zurück. Der Wertebereich ist von
-400 bis 1250 und wird in °C/10 angegeben, z.B. bedeutet
ein Wert von 423 eine gemessene Umgebungstemperatur von 42,3 °C.

Wenn die Umgebungstemperatur periodisch abgefragt werden soll, wird empfohlen
den :cb:`Ambient Temperature` Callback zu nutzen und die Periode mit
:func:`Set Ambient Temperature Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Object Temperature',
'elements': [('Temperature', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the object temperature of the sensor, i.e. the temperature
of the surface of the object the sensor is aimed at. The value
has a range of -700 to 3800 and is given in °C/10,
e.g. a value of 3001 means that a temperature of 300.1 °C is measured
on the surface of the object.

The temperature of different materials is dependent on their `emissivity
<https://en.wikipedia.org/wiki/Emissivity>`__. The emissivity of the material
can be set with :func:`Set Emissivity`.

If you want to get the object temperature periodically, it is recommended
to use the :cb:`Object Temperature` callback and set the period with
:func:`Set Object Temperature Callback Period`.
""",
'de':
"""
Gibt die Objekttemperatur des Sensors zurück, z.B. die Temperatur
der Oberfläche auf welche der Sensor zielt. Der Wertebereich ist von
-700 bis 3800 und wird in °C/10 angegeben, z.B. bedeutet
ein Wert von 3001 eine gemessene Temperatur von 300,1 °C auf der Oberfläche
des Objektes.

Die Temperatur von unterschiedlichen Materialien ist abhängig von ihrem
`Emissionsgrad <https://de.wikipedia.org/wiki/Emissionsgrad>`__. Der
Emissionsgrad des Materials kann mit :func:`Set Emissivity` gesetzt werden.

Wenn die Objekttemperatur periodisch abgefragt werden soll, wird empfohlen
den :cb:`Object Temperature` Callback zu nutzen und die Periode mit
:func:`Set Object Temperature Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Emissivity',
'elements': [('Emissivity', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the `emissivity <https://en.wikipedia.org/wiki/Emissivity>`__ that is
used to calculate the surface temperature as returned by
:func:`Get Object Temperature`.

The emissivity is usually given as a value between 0.0 and 1.0. A list of
emissivities of different materials can be found
`here <https://www.infrared-thermography.com/material.htm>`__.

The parameter of :func:`Set Emissivity` has to be given with a factor of
65535 (16-bit). For example: An emissivity of 0.1 can be set with the
value 6553, an emissivity of 0.5 with the value 32767 and so on.

.. note::
 If you need a precise measurement for the object temperature, it is
 absolutely crucial that you also provide a precise emissivity.

The default emissivity is 1.0 (value of 65535) and the minimum emissivity the
sensor can handle is 0.1 (value of 6553).

The emissivity is stored in non-volatile memory and will still be used after a restart or power cycle of the Bricklet.
""",
'de':
"""
Setzt den `Emissionsgrad <https://de.wikipedia.org/wiki/Emissionsgrad>`__,
welcher zur Berechnung der Oberflächentemperatur benutzt wird, wie von
:func:`Get Object Temperature` zurückgegeben.

Der Emissionsgrad wird normalerweise als Wert zwischen 0,0 und 1,0 angegeben.
Eine Liste von Emissionsgraden unterschiedlicher Materialien ist
`hier <https://www.infrared-thermography.com/material.htm>`__ zu finden.

Der Parameter von :func:`Set Emissivity` muss mit eine Faktor von 65535 (16-Bit)
vorgegeben werden. Beispiel: Ein Emissionsgrad von 0,1 kann mit dem Wert
6553 gesetzt werden, ein Emissionsgrad von 0,5 mit dem Wert 32767 und so weiter.

.. note::
 Wenn eine exakte Messung der Objekttemperatur notwendig ist, ist es entscheidend
 eine exakten Emissionsgrad anzugeben.

Der Standard Emissionsgrad ist 1,0 (Wert von 65535) und der minimale
Emissionsgrad welcher der Sensor verarbeiten kann ist 0,1 (Wert von 6553).

Der Emissionsgrad wird in nicht-flüchtigem Speicher gespeichert und wird auch noch einem Neustart weiter genutzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Emissivity',
'elements': [('Emissivity', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the emissivity as set by :func:`Set Emissivity`.
""",
'de':
"""
Gibt den Emissionsgrad zurück, wie von :func:`Set Emissivity` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Ambient Temperature Callback Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :cb:`Ambient Temperature` callback is
triggered periodically. A value of 0 turns the callback off.

The :cb:`Ambient Temperature` callback is only triggered if the temperature has
changed since the last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :cb:`Ambient Temperature` Callback
ausgelöst wird. Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Ambient Temperature` Callback wird nur ausgelöst, wenn sich die
Temperatur seit der letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Ambient Temperature Callback Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Ambient Temperature Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Ambient Temperature Callback Period`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Object Temperature Callback Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :cb:`Object Temperature` callback is
triggered periodically. A value of 0 turns the callback off.

The :cb:`Object Temperature` callback is only triggered if the temperature
has changed since the last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :cb:`Object Temperature` Callback
ausgelöst wird. Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Object Temperature` Callback wird nur ausgelöst, wenn sich die
Temperatur seit der letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Object Temperature Callback Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Object Temperature Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Object Temperature Callback Period`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Ambient Temperature Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option'}),
             ('Min', 'int16', 1, 'in'),
             ('Max', 'int16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Ambient Temperature Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the ambient temperature is *outside* the min and max values"
 "'i'",    "Callback is triggered when the ambient temperature is *inside* the min and max values"
 "'<'",    "Callback is triggered when the ambient temperature is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the ambient temperature is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Ambient Temperature Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn die Umgebungstemperatur *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn die Umgebungstemperatur *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn die Umgebungstemperatur kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn die Umgebungstemperatur größer als der min Wert ist (max wird ignoriert)"

Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Ambient Temperature Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option'}),
             ('Min', 'int16', 1, 'out'),
             ('Max', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Ambient Temperature Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Ambient Temperature Callback Threshold`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Object Temperature Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option'}),
             ('Min', 'int16', 1, 'in'),
             ('Max', 'int16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Object Temperature Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the object temperature is *outside* the min and max values"
 "'i'",    "Callback is triggered when the object temperature is *inside* the min and max values"
 "'<'",    "Callback is triggered when the object temperature is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the object temperature is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Object Temperature Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn die Objekttemperatur *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn die Objekttemperatur *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn die Objekttemperatur kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn die Objekttemperatur größer als der min Wert ist (max wird ignoriert)"

Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Object Temperature Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option'}),
             ('Min', 'int16', 1, 'out'),
             ('Max', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Object Temperature Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Object Temperature Callback Threshold`
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

* :cb:`Ambient Temperature Reached`,
* :cb:`Object Temperature Reached`

are triggered, if the thresholds

* :func:`Set Ambient Temperature Callback Threshold`,
* :func:`Set Object Temperature Callback Threshold`

keep being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callbacks

* :cb:`Ambient Temperature Reached`,
* :cb:`Object Temperature Reached`

ausgelöst werden, wenn die Schwellwerte

* :func:`Set Ambient Temperature Callback Threshold`,
* :func:`Set Object Temperature Callback Threshold`

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
'name': 'Ambient Temperature',
'elements': [('Temperature', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Ambient Temperature Callback Period`. The :word:`parameter` is the
ambient temperature of the sensor.

The :cb:`Ambient Temperature` callback is only triggered if the ambient
temperature has changed since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Ambient Temperature Callback Period`,
ausgelöst. Der :word:`parameter` ist die Temperatur des Sensors.

Der :cb:`Ambient Temperature` Callback wird nur ausgelöst, wenn sich die
Temperatur seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Object Temperature',
'elements': [('Temperature', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Object Temperature Callback Period`. The :word:`parameter` is the
object temperature of the sensor.

The :cb:`Object Temperature` callback is only triggered if the object
temperature has changed since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Object Temperature Callback Period`, ausgelöst. Der
:word:`parameter` ist die Objekttemperatur des Sensors.

Der :cb:`Object Temperature` Callback wird nur ausgelöst, wenn sich die
Objekttemperatur seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Ambient Temperature Reached',
'elements': [('Temperature', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Ambient Temperature Callback Threshold` is reached.
The :word:`parameter` is the ambient temperature of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Ambient Temperature Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Umgebungstemperatur des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Object Temperature Reached',
'elements': [('Temperature', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Object Temperature Callback Threshold` is reached.
The :word:`parameter` is the object temperature of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Object Temperature Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Objekttemperatur des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Ambient Temperature', 'ambient temperature'), [(('Ambient Temperature', 'Ambient Temperature'), 'int16', 1, 10.0, '°C', None)], []),
              ('getter', ('Get Object Temperature', 'object temperature'), [(('Object Temperature', 'Object Temperature'), 'int16', 1, 10.0, '°C', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Object Temperature', 'object temperature'), [(('Temperature', 'Object Temperature'), 'int16', 1, 10.0, '°C', None)], None, None),
              ('callback_period', ('Object Temperature', 'object temperature'), [], 1000)]
})

com['examples'].append({
'name': 'Water Boiling',
'functions': [('setter', 'Set Emissivity', [('uint16', 64224)], 'Set emissivity to 0.98 (emissivity of water, 65535 * 0.98 = 64224.299)', None),
              ('debounce_period', 10000),
              ('callback', ('Object Temperature Reached', 'object temperature reached'), [(('Temperature', 'Object Temperature'), 'int16', 1, 10.0, '°C', None)], None, 'The water is boiling!'),
              ('callback_threshold', ('Object Temperature', 'object temperature'), [], '>', [(100, 0)])]
})

ambient_temp_channel = oh_generic_old_style_channel('Ambient Temperature', 'Ambient Temperature', 'SIUnits.CELSIUS', divisor=10.0, cast_literal='(short)')
ambient_temp_channel['callback_transform'] = 'new QuantityType<>(temperature{divisor}, {unit})'

object_temp_channel = oh_generic_old_style_channel('Object Temperature', 'Object Temperature', 'SIUnits.CELSIUS', divisor=10.0, cast_literal='(short)')
object_temp_channel['callback_transform'] = 'new QuantityType<>(temperature{divisor}, {unit})'

com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'channels': [
        ambient_temp_channel,
        object_temp_channel
    ],
    'channel_types': [
        oh_generic_channel_type('Ambient Temperature', 'Number:Temperature', 'Ambient Temperature',
                     description='Measured ambient temperature',
                     read_only=True,
                     pattern='%.1f %unit%',
                     min_=-40,
                     max_=125),
        oh_generic_channel_type('Object Temperature', 'Number:Temperature', 'Object Temperature',
                     description='Measured object temperature, i.e. the temperature of the surface of the object the sensor is aimed at. The temperature of different materials is dependent on their <a href=https://en.wikipedia.org/wiki/Emissivity>emissivity</a>.',
                     read_only=True,
                     pattern='%.1f %unit%',
                     min_=-70,
                     max_=380)
    ]
}
