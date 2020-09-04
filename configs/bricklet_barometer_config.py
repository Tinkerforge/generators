# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Barometer Bricklet communication config

from generators.configs.commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Matthias Bolte <matthias@tinkerforge.com>',
    'api_version': [2, 0, 2],
    'category': 'Bricklet',
    'device_identifier': 221,
    'name': 'Barometer',
    'display_name': 'Barometer',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures air pressure and altitude changes',
        'de': 'Misst Luftdruck und Höhenänderungen'
    },
    'released': True,
    'documented': True,
    'discontinued': False, # selling remaining stock, replaced by Barometer Bricklet 2.0
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
'name': 'I2C Mode',
'type': 'uint8',
'constants': [('Fast', 0),
              ('Slow', 1)]
})


com['packets'].append({
'type': 'function',
'name': 'Get Air Pressure',
'elements': [('Air Pressure', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Hectopascal', 'range': (10000, 1200000)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the air pressure of the air pressure sensor.

If you want to get the air pressure periodically, it is recommended to use the
:cb:`Air Pressure` callback and set the period with
:func:`Set Air Pressure Callback Period`.
""",
'de':
"""
Gibt den Luftdruck des Luftdrucksensors zurück.

Wenn der Luftdruck periodisch abgefragt werden soll, wird empfohlen
den :cb:`Air Pressure` Callback zu nutzen und die Periode mit
:func:`Set Air Pressure Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Altitude',
'elements': [('Altitude', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Meter'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the relative altitude of the air pressure sensor. The value is
calculated based on the difference between the current air pressure
and the reference air pressure that can be set with :func:`Set Reference Air Pressure`.

If you want to get the altitude periodically, it is recommended to use the
:cb:`Altitude` callback and set the period with
:func:`Set Altitude Callback Period`.
""",
'de':
"""
Gibt die relative Höhe des Luftdrucksensors zurück. Der Wert wird
auf Basis der Differenz zwischen dem aktuellen Luftdruck und dem
Referenzluftdruck berechnet, welcher mit :func:`Set Reference Air Pressure`
gesetzt werden kann.

Wenn die Höhe periodisch abgefragt werden soll, wird empfohlen den
:cb:`Altitude` Callback zu nutzen und die Periode mit
:func:`Set Altitude Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Air Pressure Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Air Pressure` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Air Pressure` callback is only triggered if the air pressure has
changed since the last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Air Pressure` Callback ausgelöst
wird. Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Air Pressure` Callback wird nur ausgelöst, wenn sich der Luftdruck
seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Air Pressure Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Air Pressure Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Air Pressure Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Altitude Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Altitude` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Altitude` callback is only triggered if the altitude has changed since
the last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Altitude` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Altitude` Callback wird nur ausgelöst, wenn sich Höhe seit der letzten
Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Altitude Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Altitude Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Altitude Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Air Pressure Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'int32', 1, 'in', {'scale': (1, 1000), 'unit': 'Hectopascal', 'default': 0}),
             ('Max', 'int32', 1, 'in', {'scale': (1, 1000), 'unit': 'Hectopascal', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Air Pressure Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the air pressure is *outside* the min and max values"
 "'i'",    "Callback is triggered when the air pressure is *inside* the min and max values"
 "'<'",    "Callback is triggered when the air pressure is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the air pressure is greater than the min value (max is ignored)"
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Air Pressure Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn der Luftdruck *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn der Luftdruck *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn der Luftdruck kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn der Luftdruck größer als der min Wert ist (max wird ignoriert)"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Air Pressure Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Hectopascal', 'default': 0}),
             ('Max', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Hectopascal', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Air Pressure Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Air Pressure Callback Threshold` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Altitude Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'int32', 1, 'in', {'scale': (1, 100), 'unit': 'Meter', 'default': 0}),
             ('Max', 'int32', 1, 'in', {'scale': (1, 100), 'unit': 'Meter', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Altitude Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the altitude is *outside* the min and max values"
 "'i'",    "Callback is triggered when the altitude is *inside* the min and max values"
 "'<'",    "Callback is triggered when the altitude is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the altitude is greater than the min value (max is ignored)"
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Altitude Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn die Höhe *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn die Höhe *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn die Höhe kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn die Höhe größer als der min Wert ist (max wird ignoriert)"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Altitude Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Meter', 'default': 0}),
             ('Max', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Meter', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Altitude Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Altitude Callback Threshold` gesetzt.
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
Sets the period with which the threshold callbacks

* :cb:`Air Pressure Reached`,
* :cb:`Altitude Reached`

are triggered, if the thresholds

* :func:`Set Air Pressure Callback Threshold`,
* :func:`Set Altitude Callback Threshold`

keep being reached.
""",
'de':
"""
Setzt die Periode mit welcher die Schwellwert Callbacks

* :cb:`Air Pressure Reached`,
* :cb:`Altitude Reached`

ausgelöst werden, wenn die Schwellwerte

* :func:`Set Air Pressure Callback Threshold`,
* :func:`Set Altitude Callback Threshold`

weiterhin erreicht bleiben.
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
'name': 'Set Reference Air Pressure',
'elements': [('Air Pressure', 'int32', 1, 'in', {'scale': (1, 1000), 'unit': 'Hectopascal', 'range': [(0, 0), (10000, 1200000)], 'default': 1013250})],
'since_firmware': [1, 1, 0],
'doc': ['bf', {
'en':
"""
Sets the reference air pressure for the altitude calculation.
Setting the reference to the current air pressure results in a calculated
altitude of 0cm. Passing 0 is a shortcut for passing the current air pressure as
reference.

Well known reference values are the Q codes
`QNH <https://en.wikipedia.org/wiki/QNH>`__ and
`QFE <https://en.wikipedia.org/wiki/Mean_sea_level_pressure#Mean_sea_level_pressure>`__
used in aviation.
""",
'de':
"""
Setzt den Referenzluftdruck für die Höhenberechnung. Wenn der
aktuelle Luftdruckwert als Referenz übergeben wird dann gibt die Höhenberechnung
0cm aus. Als Abkürzung kann auch 0 übergeben werden, dadurch wird der
Referenzluftdruck intern auf den aktuellen Luftdruckwert gesetzt.

Wohl bekannte Referenzluftdruckwerte, die in der Luftfahrt verwendet werden, sind
`QNH <https://de.wikipedia.org/wiki/Barometrische_H%C3%B6henmessung_in_der_Luftfahrt#QNH>`__ und
`QFE <https://de.wikipedia.org/wiki/Barometrische_H%C3%B6henmessung_in_der_Luftfahrt#QFE>`__
aus dem Q-Schlüssel.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Chip Temperature',
'elements': [('Temperature', 'int16', 1, 'out', {'scale': (1, 100), 'unit': 'Degree Celsius', 'range': (-4000, 8500)})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the temperature of the air pressure sensor.

This temperature is used internally for temperature compensation of the air
pressure measurement. It is not as accurate as the temperature measured by the
:ref:`temperature_bricklet` or the :ref:`temperature_ir_bricklet`.
""",
'de':
"""
Gibt die Temperatur des Luftdrucksensors zurück.

Diese Temperatur wird intern zur Temperaturkompensation der Luftdruckmessung
verwendet. Sie ist nicht so genau wie die Temperatur die vom
:ref:`temperature_bricklet` oder dem :ref:`temperature_ir_bricklet` gemessen
wird.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Air Pressure',
'elements': [('Air Pressure', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Hectopascal', 'range': (10000, 1200000)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Air Pressure Callback Period`. The :word:`parameter` is the air
pressure of the air pressure sensor.

The :cb:`Air Pressure` callback is only triggered if the air pressure has
changed since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Air Pressure Callback Period`, ausgelöst. Der :word:`parameter` ist
der Luftdruck des Luftdrucksensors.

Der :cb:`Air Pressure` Callback wird nur ausgelöst, wenn sich der Luftdruck
seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Altitude',
'elements': [('Altitude', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Meter'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Altitude Callback Period`. The :word:`parameter` is the altitude of
the air pressure sensor.

The :cb:`Altitude` callback is only triggered if the altitude has changed since
the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Altitude Callback Period`, ausgelöst. Der :word:`parameter` ist
die Höhe des Luftdrucksensors.

Der :cb:`Altitude` Callback wird nur ausgelöst, wenn sich die Höhe seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Air Pressure Reached',
'elements': [('Air Pressure', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Hectopascal', 'range': (10000, 1200000)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Air Pressure Callback Threshold` is reached.
The :word:`parameter` is the air pressure of the air pressure sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Air Pressure Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist der Luftdruck des Luftdrucksensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Altitude Reached',
'elements': [('Altitude', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Meter'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Altitude Callback Threshold` is reached.
The :word:`parameter` is the altitude of the air pressure sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Altitude Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Höhe des Luftdrucksensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Reference Air Pressure',
'elements': [('Air Pressure', 'int32', 1, 'out', {'scale': (1, 1000), 'unit': 'Hectopascal', 'range': (10000, 1200000), 'default': 1013250})],
'since_firmware': [1, 1, 0],
'doc': ['bf', {
'en':
"""
Returns the reference air pressure as set by :func:`Set Reference Air Pressure`.
""",
'de':
"""
Gibt den Referenzluftdruckwert zurück, wie von :func:`Set Reference Air Pressure` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Averaging',
'elements': [('Moving Average Pressure', 'uint8', 1, 'in', {'range': (0, 25), 'default': 25}),
             ('Average Pressure', 'uint8', 1, 'in', {'range': (0, 10), 'default': 10}),
             ('Average Temperature', 'uint8', 1, 'in', {'default': 10})],
'since_firmware': [2, 0, 1],
'doc': ['af', {
'en':
"""
Sets the different averaging parameters. It is possible to set
the length of a normal averaging for the temperature and pressure,
as well as an additional length of a
`moving average <https://en.wikipedia.org/wiki/Moving_average>`__
for the pressure. The moving average is calculated from the normal
averages.  There is no moving average for the temperature.

Setting the all three parameters to 0 will turn the averaging
completely off. If the averaging is off, there is lots of noise
on the data, but the data is without delay. Thus we recommend
to turn the averaging off if the Barometer Bricklet data is
to be used for sensor fusion with other sensors.
""",
'de':
"""
Setzt die unterschiedlichen Averaging-Parameter (Mittelwertbildung).
Es ist möglich die Länge des Mittelwerts für Temperatur und
Luftdruck anzugeben. Zusätzlich gibt kann die Länge für
einen
`gleitenden Mittelwert <https://de.wikipedia.org/wiki/Gleitender_Mittelwert>`__
für den Luftdruck angegeben werden. Der gleitende Mittelwert wird
mit den Werten des normalen Mittelwerts berechnet. Es gibt keinen
gleitenden Mittelwert für die Temperatur.

Wenn alle drei Parameter auf 0 gesetzt werden, ist das Averaging
komplett aus. In diesem Fall gibt es viel Rauschen auf den Daten,
allerdings sind die Daten dann ohne Verzögerung. Wir empfehlen
das Averaging auszustellen wenn die Daten des Barometer Bricklets
zusammen mit anderen Sensordaten fusioniert werden sollen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Averaging',
'elements': [('Moving Average Pressure', 'uint8', 1, 'out', {'range': (0, 25), 'default': 25}),
             ('Average Pressure', 'uint8', 1, 'out', {'range': (0, 10), 'default': 10}),
             ('Average Temperature', 'uint8', 1, 'out', {'default': 10})],
'since_firmware': [2, 0, 1],
'doc': ['af', {
'en':
"""
Returns the averaging configuration as set by :func:`Set Averaging`.
""",
'de':
"""
Gibt die Averaging-Konfiguration zurück, wie von :func:`Set Averaging` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set I2C Mode',
'elements': [('Mode', 'uint8', 1, 'in', {'constant_group': 'I2C Mode', 'default': 0})],
'since_firmware': [2, 0, 3],
'doc': ['af', {
'en':
"""
Sets the I2C mode. Possible modes are:

* 0: Fast (400kHz)
* 1: Slow (100kHz)

If you have problems with obvious outliers in the
Barometer Bricklet measurements, they may be caused by EMI issues.
In this case it may be helpful to lower the I2C speed.

It is however not recommended to lower the I2C speed in applications where
a high throughput needs to be achieved.
""",
'de':
"""
Setzt den I2C Modus. Mögliche Modi sind:

* 0: Fast (400kHz)
* 1: Slow (100kHz)

Wenn Probleme mit offensichtlichen Ausreißern in den
Barometer Bricklet Messungen auftreten, können diese eventuell aufgrund
von elektromagnetischen Störungen sein. In diesem Fall kann es helfen
die I2C Geschwindigkeit zu verringern.

Falls in einem System ein hoher Durchsatz an Nachrichten erwünscht ist,
sollte die I2C Geschwindigkeit allerdings nicht verringert werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get I2C Mode',
'elements': [('Mode', 'uint8', 1, 'out', {'constant_group': 'I2C Mode', 'default': 0})],
'since_firmware': [2, 0, 3],
'doc': ['af', {
'en':
"""
Returns the I2C mode as set by :func:`Set I2C Mode`.
""",
'de':
"""
Gibt den I2C Modus zurück, wie von :func:`Set I2C Mode` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Air Pressure', 'air pressure'), [(('Air Pressure', 'Air Pressure'), 'int32', 1, 1000.0, 'hPa', None)], []),
              ('getter', ('Get Altitude', 'altitude'), [(('Altitude', 'Altitude'), 'int32', 1, 100.0, 'm', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Air Pressure', 'air pressure'), [(('Air Pressure', 'Air Pressure'), 'int32', 1, 1000.0, 'hPa', None)], None, None),
              ('callback_period', ('Air Pressure', 'air pressure'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('Air Pressure Reached', 'air pressure reached'), [(('Air Pressure', 'Air Pressure'), 'int32', 1, 1000.0, 'hPa', None)], None, 'Enjoy the potentially good weather!'),
              ('callback_threshold', ('Air Pressure', 'air pressure'), [], '>', [(1025, 0)])]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports() + ["java.math.BigDecimal"],
    'params': [{
            'packet': 'Set Reference Air Pressure',
            'element': 'Air Pressure',

            'name': 'Reference Air Pressure',
            'type': 'decimal',
            'min': 10, # Disallow 0 intentionally.

            'label': {'en': 'Reference Air Pressure', 'de': 'Referenzluftdruck'},
            'description': {'en': 'The reference air pressure in hPa for the altitude calculation. Valid values are between 10 and 1200. Setting the reference to the current air pressure results in a calculated altitude of 0 cm.',
                            'de': 'Der Referenzluftdruck für die Höhenberechnung. Wenn der aktuelle Luftdruckwert als Referenz übergeben wird dann gibt die Höhenberechnung 0cm aus.'}
        },
        {
            'packet': 'Set Averaging',
            'element': 'Moving Average Pressure',

            'name': 'Pressure Moving Average Length',
            'type': 'integer',
            'label': {'en': 'Pressure Moving Average Length', 'de': 'Länge des gleitenden Druck-Mittelwerts'},
            'description': {'en': 'The length of the moving average for the air pressure. The moving average is calculated over the normal averages.',
                            'de': 'Die Länge des gleitenden Mittelwerts für den Luftdruck. Der gleitende Mittelwert wird mit den Werten des normalen Mittelwerts berechnet.'},
            'groupName': 'average'
        },
        {
            'packet': 'Set Averaging',
            'element': 'Average Pressure',

            'name': 'Pressure Average Length',
            'type': 'integer',
            'label': {'en': 'Pressure Average Length', 'de': 'Druck-Mittelwertlänge'},
            'description': {'en': 'The number of samples to average over for the air pressure.',
                            'de': 'Die Anzahl an Messungen über die der Mittelwert für den Luftdruck gebildet wird.'},
            'groupName': 'average'
        },
        {
            'packet': 'Set Averaging',
            'element': 'Average Temperature',

            'name': 'Temperature Average Length',
            'type': 'integer',
            'label': {'en': 'Temperature Average Length', 'de': 'Temperatur-Mittelwertlänge'},
            'description': {'en': 'The number of samples to average over for the temperature.',
                            'de': 'Die Anzahl an Messungen über die der Mittelwert für die Temperatur gebildet wird.'},
            'groupName': 'average'
        }],
    'param_groups': oh_generic_channel_param_groups() + [
     {
        'name': 'average',
        'label': {'en': 'Averaging', 'de': 'Mittelwertbildung'},
        'description': {'en': 'The averaging parameters. It is possible to set the length of a normal averaging for the temperature and pressure, as well as an additional length of a moving average for the pressure. The moving average is calculated from the normal averages. There is no moving average for the temperature.\n\nThe maximum length for the pressure average is 10, for the temperature average is 255 and for the moving average is 25.\n\nSetting the all three parameters to 0 will turn the averaging completely off. If the averaging is off, there is lots of noise on the data, but the data is without delay. Thus we recommend to turn the averaging off if the Barometer Bricklet data is to be used for sensor fusion with other sensors.',
                        'de': 'Die Parameter zur Mittelwertbildung. Es ist möglich die Länge des Mittelwerts für Temperatur und Luftdruck anzugeben. Zusätzlich gibt kann die Länge für einen `gleitenden Mittelwert <https://de.wikipedia.org/wiki/Gleitender_Mittelwert>`__ für den Luftdruck angegeben werden. Der gleitende Mittelwert wird mit den Werten des normalen Mittelwerts berechnet. Es gibt keinen gleitenden Mittelwert für die Temperatur.\n\nWenn alle drei Parameter auf 0 gesetzt werden, ist das Averaging komplett aus. In diesem Fall gibt es viel Rauschen auf den Daten, allerdings sind die Daten dann ohne Verzögerung. Wir empfehlen das Averaging auszustellen wenn die Daten des Barometer Bricklets zusammen mit anderen Sensordaten fusioniert werden sollen.'},
        'advanced': 'true'
    }
    ],
    'init_code': """this.setReferenceAirPressure(cfg.referenceAirPressure.multiply(new BigDecimal(1000)).intValue());
this.setAveraging(cfg.pressureMovingAverageLength.shortValue(), cfg.pressureAverageLength.shortValue(), cfg.temperatureAverageLength.shortValue());""",
    'channels': [
        oh_generic_old_style_channel('Air Pressure', 'Air Pressure', 'SmartHomeUnits.BAR', divisor=1000000.0),
        oh_generic_old_style_channel('Altitude', 'Altitude')
    ],
    'channel_types': [
        oh_generic_channel_type('Air Pressure', 'Number:Pressure', {'en': 'Air Pressure', 'de': 'Luftdruck'},
                    update_style='Callback Period',
                    description={'en': 'The measured air pressure', 'de': 'Der gemessene Luftdruck'}),
        oh_generic_channel_type('Altitude', 'Number', {'en': 'Altitude', 'de': 'Höhe'},
                    update_style='Callback Period',
                    description={'en': 'The relative altitude. The value is calculated based on the difference between the current air pressure and the reference air pressure.',
                                 'de': 'Die relative Höhe. Der Wert wird auf Basis der Differenz zwischen dem aktuellen Luftdruck und dem Referenzluftdruck berechnet.'})
    ],
    'actions': ['Get Air Pressure', 'Get Altitude', 'Get Reference Air Pressure', 'Get Averaging']
}

