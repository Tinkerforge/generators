# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# PTC Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 226,
    'name': ('PTC', 'PTC', 'PTC Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Reads temperatures from Pt100 und Pt1000 sensors',
        'de': 'Liest Temperaturen von Pt100 und Pt1000 Sensoren'
    },
    'released': True,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Get Temperature',
'elements': [('Temperature', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the temperature of connected sensor. The value
has a range of -246 to 849 °C and is given in °C/100,
e.g. a value of 4223 means that a temperature of 42.23 °C is measured.

If you want to get the temperature periodically, it is recommended 
to use the callback :func:`Temperature` and set the period with 
:func:`SetTemperatureCallbackPeriod`.
""",
'de':
"""
Gibt die Temperatur des verbundenen Sensors zurück. Der Wertebereich ist von
-246 bis 849 °C und wird in °C/100 angegeben, z.B. bedeutet 
ein Wert von 4223 eine gemessene Temperatur von 42,23 °C.

Wenn die Temperatur periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`Temperature` zu nutzen und die Periode mit 
:func:`SetTemperatureCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Resistance',
'elements': [('Resistance', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the value as measured by the MAX31865 precision delta-sigma ADC.

The value can be converted with the following formulas:

* Pt100:  resistance = (value * 390) / 32768
* Pt1000: resistance = (value * 3900) / 32768

If you want to get the resistance periodically, it is recommended 
to use the callback :func:`Resistance` and set the period with 
:func:`SetResistanceCallbackPeriod`.
""",
'de':
"""
Gibt den Wert zurück, wie vom "MAX31865 Präzisions Delta-Sigma ADC" berechnet.

Der Wert kann mit den folgenden Formeln in einen Widerstand konvertiert werden:

* Pt100:  Widerstand = (Wert * 390) / 32768
* Pt1000: Widerstand = (Wert * 3900) / 32768

Wenn der Widerstand periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`Resistance` zu nutzen und die Periode mit 
:func:`SetResistanceCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Temperature Callback Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Temperature` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Temperature` is only triggered if the temperature has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Temperature` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Temperature` wird nur ausgelöst wenn sich die Temperatur seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Temperature Callback Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetTemperatureCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetTemperatureCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Resistance Callback Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Resistance` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Resistance` is only triggered if the resistance has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Resistance` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Resistance` wird nur ausgelöst wenn sich der Widerstand seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Resistance Callback Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetResistanceCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetResistanceCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Temperature Callback Threshold',
'elements': [('Option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'int32', 1, 'in'),
             ('Max', 'int32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`TemperatureReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the temperature is *outside* the min and max values"
 "'i'",    "Callback is triggered when the temperature is *inside* the min and max values"
 "'<'",    "Callback is triggered when the temperature is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the temperature is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`TemperatureReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Temperatur *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn die Temperatur *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn die Temperatur kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Temperatur größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Temperature Callback Threshold',
'elements': [('Option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'int32', 1, 'out'),
             ('Max', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`SetTemperatureCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetTemperatureCallbackThreshold`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Resistance Callback Threshold',
'elements': [('Option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint16', 1, 'in'),
             ('Max', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`ResistanceReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the temperature is *outside* the min and max values"
 "'i'",    "Callback is triggered when the temperature is *inside* the min and max values"
 "'<'",    "Callback is triggered when the temperature is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the temperature is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`ResistanceReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Temperatur *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn die Temperatur *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn die Temperatur kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Temperatur größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Resistance Callback Threshold',
'elements': [('Option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint16', 1, 'out'),
             ('Max', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`SetResistanceCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetResistanceCallbackThreshold`
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

* :func:`TemperatureReached`,
* :func:`ResistanceReached`

is triggered, if the threshold

* :func:`SetTemperatureCallbackThreshold`,
* :func:`SetResistanceCallbackThreshold`

keeps being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callback

* :func:`TemperatureReached`,
* :func:`ResistanceReached`
 
ausgelöst wird, wenn der Schwellwert 

* :func:`SetTemperatureCallbackThreshold`,
* :func:`SetResistanceCallbackThreshold`
 
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
'type': 'callback',
'name': 'Temperature',
'elements': [('Temperature', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetTemperatureCallbackPeriod`. The :word:`parameter` is the temperature
of the connected sensor.

:func:`Temperature` is only triggered if the temperature has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetTemperatureCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die Temperatur des verbundenen Sensors.

:func:`Temperature` wird nur ausgelöst wenn sich die Temperatur seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Temperature Reached',
'elements': [('Temperature', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetTemperatureCallbackThreshold` is reached.
The :word:`parameter` is the temperature of the connected sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetTemperatureCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Temperatur des verbundenen Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Resistance',
'elements': [('Resistance', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetResistanceCallbackPeriod`. The :word:`parameter` is the resistance
of the connected sensor.

:func:`Resistance` is only triggered if the resistance has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetResistanceCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist der Widerstand des verbundenen Sensors.

:func:`Resistance` wird nur ausgelöst wenn sich der Widerstand seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Resistance Reached',
'elements': [('Resistance', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetResistanceCallbackThreshold` is reached.
The :word:`parameter` is the resistance of the connected sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetResistanceCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist der Widerstand des verbundenen Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Noise Rejection Filter',
'elements': [('Filter', 'uint8', 1, 'in', ('Filter Option', [('50Hz', 0),
                                                             ('60Hz', 1)]))],
'since_firmware': [1, 0, 0], 
'doc': ['af', {
'en':
"""
Sets the noise rejection filter to either 50Hz (0) or 60Hz (1).
Noise from 50Hz or 60Hz power sources (including
harmonics of the AC power's fundamental frequency) is
attenuated by 82dB.

Default value is 0 = 50Hz.
""",
'de':
"""
Setzt den Entstörfilter auf 50Hz (0) oder 60Hz (1).
Störungen von 50Hz oder 60Hz Stromquellen (inklusive
Oberwellen der Stromquellen-Grundfrequenz) werden
um 82dB abgeschwächt.

Der Standardwert ist 0 = 50Hz.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Noise Rejection Filter',
'elements': [('Filter', 'uint8', 1, 'out', ('Filter Option', [('50Hz', 0),
                                                              ('60Hz', 1)]))],
'since_firmware': [1, 0, 0], 
'doc': ['af', {
'en':
"""
Returns the noise rejection filter option as set by 
:func:`SetNoiseRejectionFilter`
""",
'de':
"""
Gibt die Einstellung des Entstörfilters zurück, wie von
:func:`SetNoiseRejectionFilter` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is Sensor Connected',
'elements': [('Connected', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0], 
'doc': ['bf', {
'en':
"""
Returns *true* if the sensor is connected correctly. 

If this function
returns *false*, there is either no Pt100 or Pt1000 sensor connected,
the sensor is connected incorrectly or the sensor itself is faulty.
""",
'de':
"""
Gibt *true* zurück wenn ein Sensor korrekt verbunden ist.

Falls diese Funktion *false* zurück gibt, ist entweder kein
Pt100 oder Pt1000 Sensor verbunden, der Sensor ist inkorrekt
verbunden oder der Sensor selbst ist fehlerhaft.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Wire Mode',
'elements': [('Mode', 'uint8', 1, 'in', ('Wire Mode', [('2', 2),
                                                       ('3', 3),
                                                       ('4', 4)]))],
'since_firmware': [1, 0, 0], 
'doc': ['bf', {
'en':
"""
Sets the wire mode of the sensor. Possible values are 2, 3 and 4 which
correspond to 2-, 3- and 4-wire sensors. The value has to match the jumper
configuration on the Bricklet.

The default value is 2 = 2-wire.
""",
'de':
"""
Stellt die Leiter-Konfiguration des Sensors ein. Mögliche Werte sind 2, 3 und
4, dies entspricht 2-, 3- und 4-Leiter-Sensoren. Der Wert muss er
Jumper-Konfiguration am Bricklet entsprechen.

Der Standardwert ist 2 = 2-Leiter.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Wire Mode',
'elements': [('Mode', 'uint8', 1, 'out', ('Wire Mode', [('2', 2),
                                                        ('3', 3),
                                                        ('4', 4)]))],
'since_firmware': [1, 0, 0], 
'doc': ['bf', {
'en':
"""
Returns the wire mode as set by :func:`SetWireMode`
""",
'de':
"""
Gibt die Leiter-Konfiguration zurück, wie von :func:`SetWireMode` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Temperature', 'temperature'), [(('Temperature', 'Temperature'), 'int32', 100.0, '°C/100', '°C', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Temperature', 'temperature'), [(('Temperature', 'Temperature'), 'int32', 100.0, '°C/100', '°C', None)], None, None),
              ('callback_period', ('Temperature', 'temperature'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('Temperature Reached', 'temperature reached'), [(('Temperature', 'Temperature'), 'int32', 100.0, '°C/100', '°C', None)], None, None),
              ('callback_threshold', ('Temperature', 'temperature'), [], '>', [(30, 0)])]
})
