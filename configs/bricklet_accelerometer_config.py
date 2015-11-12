# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Accelerometer Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 250,
    'name': ('Accelerometer', 'accelerometer', 'Accelerometer', 'Accelerometer Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures acceleration in three axis',
        'de': 'Misst Beschleunigung in drei Achsen'
    },
    'released': True,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': ('GetAcceleration', 'get_acceleration'), 
'elements': [('x', 'int16', 1, 'out'),
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the acceleration in x, y and z direction. The values
are given in g/1000 (1g = 9.80665m/s²), not to be confused with grams.

If you want to get the acceleration periodically, it is recommended 
to use the callback :func:`Acceleration` and set the period with 
:func:`SetAccelerationCallbackPeriod`.
""",
'de':
"""
Gibt die Beschleunigung in X-, Y- und Z-Richtung zurück. Die Werte
haben die Einheit g/1000 (1g = 9,80665m/s²), nicht zu verwechseln mit Gramm.

Wenn die Beschleunigungswerte periodisch abgefragt werden sollen, wird empfohlen
den Callback :func:`Acceleration` zu nutzen und die Periode mit 
:func:`SetAccelerationCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetAccelerationCallbackPeriod', 'set_acceleration_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Acceleration` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Acceleration` is only triggered if the acceleration has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Acceleration` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Acceleration` wird nur ausgelöst wenn sich die Acceleration seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAccelerationCallbackPeriod', 'get_acceleration_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetAccelerationCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetAccelerationCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetAccelerationCallbackThreshold', 'set_acceleration_callback_threshold'), 
'elements': [('option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('min_x', 'int16', 1, 'in'),
             ('max_x', 'int16', 1, 'in'),
             ('min_y', 'int16', 1, 'in'),
             ('max_y', 'int16', 1, 'in'),
             ('min_z', 'int16', 1, 'in'),
             ('max_z', 'int16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`AccelerationReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the acceleration is *outside* the min and max values"
 "'i'",    "Callback is triggered when the acceleration is *inside* the min and max values"
 "'<'",    "Callback is triggered when the acceleration is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the acceleration is greater than the min value (max is ignored)"

The default value is ('x', 0, 0, 0, 0, 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`AccelerationReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Beschleunigung *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn die Beschleunigung *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn die Beschleunigung kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Beschleunigung größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0, 0, 0, 0, 0, 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAccelerationCallbackThreshold', 'get_acceleration_callback_threshold'), 
'elements': [('option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('min_x', 'int16', 1, 'out'),
             ('max_x', 'int16', 1, 'out'),
             ('min_y', 'int16', 1, 'out'),
             ('max_y', 'int16', 1, 'out'),
             ('min_z', 'int16', 1, 'out'),
             ('max_z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`SetAccelerationCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetAccelerationCallbackThreshold`
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

* :func:`AccelerationReached`

is triggered, if the threshold

* :func:`SetAccelerationCallbackThreshold`

keeps being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callback

* :func:`AccelerationReached`
 
ausgelöst wird, wenn der Schwellwert 

* :func:`SetAccelerationCallbackThreshold`
 
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
'type': 'function',
'name': ('GetTemperature', 'get_temperature'), 
'elements': [('temperature', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the temperature of the accelerometer in °C.
""",
'de':
"""
Gibt die Temperatur des Beschleunigungssensors in °C zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetConfiguration', 'set_configuration'), 
'elements': [('data_rate', 'uint8', 1, 'in', ('DataRate', 'data_rate', [('Off', 'off', 0),
                                                                        ('3Hz', '3hz', 1),
                                                                        ('6Hz', '6hz', 2),
                                                                        ('12Hz', '12hz', 3),
                                                                        ('25Hz', '25hz', 4),
                                                                        ('50Hz', '50hz', 5),
                                                                        ('100Hz', '100hz', 6),
                                                                        ('400Hz', '400hz', 7),
                                                                        ('800Hz', '800hz', 8),
                                                                        ('1600Hz', '1600hz', 9)])),
             ('full_scale', 'uint8', 1, 'in', ('FullScale', 'full_scale', [('2g', '2g', 0),
                                                                           ('4g', '4g', 1),
                                                                           ('6g', '6g', 2),
                                                                           ('8g', '8g', 3),
                                                                           ('16g', '16g', 4)])),
             ('filter_bandwidth', 'uint8', 1, 'in', ('FilterBandwidth', 'filter_bandwidth', [('800Hz', '800hz', 0),
                                                                                             ('400Hz', '400hz', 1),
                                                                                             ('200Hz', '200hz', 2),
                                                                                             ('50Hz', '50hz', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Configures the data rate, full scale range and filter bandwidth.
Possible values are:

* Data rate of 0Hz to 1600Hz.
* Full scale range of -2G to +2G up to -16G to +16G.
* Filter bandwidth between 50Hz and 800Hz.

Decreasing data rate or full scale range will also decrease the noise on 
the data.

The default values are 100Hz data rate, -4G to +4G range and 200Hz
filter bandwidth.
""",
'de':
"""
Konfiguriert die Datenrate, den Wertebereich und die Filterbandbreite.
Mögliche Konfigurationswerte sind:

* Datenrate zwischen 0Hz und 1600Hz.
* Wertebereich von -2G bis +2G bis zu -16G bis +16G.
* Filterbandbreite zwischen 50Hz und 800Hz.

Eine Verringerung der Datenrate oder des Wertebereichs verringert auch
automatisch das Rauschen auf den Daten.

Die Standardwerte sind 100Hz Datenrate, -4G bis +4G Wertebereich und 200Hz
Filterbandbreite.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetConfiguration', 'get_configuration'), 
'elements': [('data_rate', 'uint8', 1, 'out', ('DataRate', 'data_rate', [('Off', 'off', 0),
                                                                         ('3Hz', '3hz', 1),
                                                                         ('6Hz', '6hz', 2),
                                                                         ('12Hz', '12hz', 3),
                                                                         ('25Hz', '25hz', 4),
                                                                         ('50Hz', '50hz', 5),
                                                                         ('100Hz', '100hz', 6),
                                                                         ('400Hz', '400hz', 7),
                                                                         ('800Hz', '800hz', 8),
                                                                         ('1600Hz', '1600hz', 9)])),
             ('full_scale', 'uint8', 1, 'out', ('FullScale', 'full_scale', [('2g', '2g', 0),
                                                                            ('4g', '4g', 1),
                                                                            ('6g', '6g', 2),
                                                                            ('8g', '8g', 3),
                                                                            ('16g', '16g', 4)])),
             ('filter_bandwidth', 'uint8', 1, 'out', ('FilterBandwidth', 'filter_bandwidth', [('800Hz', '800hz', 0),
                                                                                              ('400Hz', '400hz', 1),
                                                                                              ('200Hz', '200hz', 2),
                                                                                              ('50Hz', '50hz', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`SetConfiguration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`SetConfiguration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('LEDOn', 'led_on'), 
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Enables the LED on the Bricklet.
""",
'de':
"""
Aktiviert die LED auf dem Bricklet.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('LEDOff', 'led_off'), 
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Disables the LED on the Bricklet.
""",
'de':
"""
Deaktiviert die LED auf dem Bricklet.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('IsLEDOn', 'is_led_on'), 
'elements': [('value', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns *true* if the LED is enabled, *false* otherwise.
""",
'de':
"""
Gibt *true* zurück wenn die LED aktiviert ist, *false* sonst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('Acceleration', 'acceleration'), 
'elements': [('x', 'int16', 1, 'out'),
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetAccelerationCallbackPeriod`. The :word:`parameters` are the
X, Y and Z acceleration.

:func:`Acceleration` is only triggered if the acceleration has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetAccelerationCallbackPeriod`,
ausgelöst. Die :word:`parameter` sind die Beschleunigungen der X-, Y- und 
Z-Achse.

:func:`Acceleration` wird nur ausgelöst wenn sich die Beschleunigung seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('AccelerationReached', 'acceleration_reached'), 
'elements': [('x', 'int16', 1, 'out'),
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetAccelerationCallbackThreshold` is reached.
The :word:`parameters` are the X, Y and Z acceleration.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetAccelerationCallbackThreshold` gesetzt, erreicht wird.
Die :word:`parameter` sind die Beschleunigungen der X-, Y- und Z-Achse.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Acceleration', 'acceleration'), [(('x', 'Acceleration[X]'), 'int16', 1000.0, 'g/1000', 'g', None), (('y', 'Acceleration[Y]'), 'int16', 1000.0, 'g/1000', 'g', None), (('z', 'Acceleration[Z]'), 'int16', 1000.0, 'g/1000', 'g', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Acceleration', 'acceleration'), [(('x', 'Acceleration[X]'), 'int16', 1000.0, 'g/1000', 'g', None), (('y', 'Acceleration[Y]'), 'int16', 1000.0, 'g/1000', 'g', None), (('z', 'Acceleration[Z]'), 'int16', 1000.0, 'g/1000', 'g', None)], None, None),
              ('callback_period', ('Acceleration', 'acceleration'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('Acceleration Reached', 'acceleration reached'), [(('x', 'Acceleration[X]'), 'int16', 1000.0, 'g/1000', 'g', None), (('y', 'Acceleration[Y]'), 'int16', 1000.0, 'g/1000', 'g', None), (('z', 'Acceleration[Z]'), 'int16', 1000.0, 'g/1000', 'g', None)], None, None),
              ('callback_threshold', ('Acceleration', 'acceleration'), [], '>', [(2, 0), (2, 0), (2, 0)])]
})
