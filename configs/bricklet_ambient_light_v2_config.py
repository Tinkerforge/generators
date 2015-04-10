# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Ambient Light Bricklet 2.0 communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 259,
    'name': ('AmbientLightV2', 'ambient_light_v2', 'Ambient Light 2.0'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for sensing Ambient Light',
    'released': False,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetIlluminance', 'get_illuminance'), 
'elements': [('illuminance', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the illuminance of the ambient light sensor. The value
has a range of 0 to 9000 and is given in Lux/10, i.e. a value
of 4500 means that an illuminance of 450 Lux is measured.

If you want to get the illuminance periodically, it is recommended to use the
callback :func:`Illuminance` and set the period with 
:func:`SetIlluminanceCallbackPeriod`.
""",
'de':
"""
Gibt die Beleuchtungsstärke des Umgebungslichtsensors zurück. Der Wertbereich
ist von 0 bis 9000 und ist in Lux/10 angegeben, d.h. bei einem Wert von 
4500 wurde eine Beleuchtungsstärke von 450 Lux gemessen.

Wenn die Beleuchtungsstärke periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`Illuminance` zu nutzen und die Periode mit 
:func:`SetIlluminanceCallbackPeriod` vorzugeben.
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
'name': ('SetIlluminanceCallbackThreshold', 'set_illuminance_callback_threshold'), 
'elements': [('option', 'char', 1, 'in', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                  ('Outside', 'outside', 'o'),
                                                                                  ('Inside', 'inside', 'i'),
                                                                                  ('Smaller', 'smaller', '<'),
                                                                                  ('Greater', 'greater', '>')])), 
             ('min', 'uint32', 1, 'in'),
             ('max', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`IlluminanceReached` callback. 

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the illuminance is *outside* the min and max values"
 "'i'",    "Callback is triggered when the illuminance is *inside* the min and max values"
 "'<'",    "Callback is triggered when the illuminance is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the illuminance is greater than the min value (max is ignored)"

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :func:`IlluminanceReached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn die Beleuchtungsstärke *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn die Beleuchtungsstärke *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn die Beleuchtungsstärke kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn die Beleuchtungsstärke größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetIlluminanceCallbackThreshold', 'get_illuminance_callback_threshold'), 
'elements': [('option', 'char', 1, 'out', ('ThresholdOption', 'threshold_option', [('Off', 'off', 'x'),
                                                                                   ('Outside', 'outside', 'o'),
                                                                                   ('Inside', 'inside', 'i'),
                                                                                   ('Smaller', 'smaller', '<'),
                                                                                   ('Greater', 'greater', '>')])), 
             ('min', 'uint32', 1, 'out'),
             ('max', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`SetIlluminanceCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetIlluminanceCallbackThreshold`
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
Sets the period in ms with which the threshold callbacks

* :func:`IlluminanceReached`,

are triggered, if the thresholds

* :func:`SetIlluminanceCallbackThreshold`,

keep being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callbacks

* :func:`IlluminanceReached`,
 
ausgelöst werden, wenn die Schwellwerte 

* :func:`SetIlluminanceCallbackThreshold`,
 
weiterhin erreicht bleiben.

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
'name': ('SetConfiguration', 'set_configuration'), 
'elements': [('illuminance_range', 'uint8', 1, 'in', ('IlluminanceRange', 'illuminance_range', [('64000Lux', '64000lux', 0),
                                                                                                ('32000Lux', '32000lux', 1),
                                                                                                ('16000Lux', '16000lux', 2),
                                                                                                ('8000Lux', '8000lux', 3),
                                                                                                ('1300Lux', '1300lux', 4),
                                                                                                ('600Lux', '600lux', 5)])),
             ('integration_time', 'uint8', 1, 'in', ('IntegrationTime', 'integration_time', [('50ms', '50ms', 0),
                                                                                             ('100ms', '100ms', 1),
                                                                                             ('150ms', '150ms', 2),
                                                                                             ('200ms', '200ms', 3),
                                                                                             ('250ms', '250ms', 4),
                                                                                             ('300ms', '300ms', 5),
                                                                                             ('350ms', '350ms', 6),
                                                                                             ('400ms', '400ms', 7)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
TODO
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetConfiguration', 'get_configuration'), 
'elements': [('illuminance_range', 'uint8', 1, 'out', ('IlluminanceRange', 'illuminance_range', [('64000Lux', '64000lux', 0),
                                                                                                 ('32000Lux', '32000lux', 1),
                                                                                                 ('16000Lux', '16000lux', 2),
                                                                                                 ('8000Lux', '8000lux', 3),
                                                                                                 ('1300Lux', '1300lux', 4),
                                                                                                 ('600Lux', '600lux', 5)])),
             ('integration_time', 'uint8', 1, 'out', ('IntegrationTime', 'integration_time', [('50ms', '50ms', 0),
                                                                                              ('100ms', '100ms', 1),
                                                                                              ('150ms', '150ms', 2),
                                                                                              ('200ms', '200ms', 3),
                                                                                              ('250ms', '250ms', 4),
                                                                                              ('300ms', '300ms', 5),
                                                                                              ('350ms', '350ms', 6),
                                                                                              ('400ms', '400ms', 7)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`SetConfiguration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`SetConfiguration`
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
:func:`SetIlluminanceCallbackPeriod`. The :word:`parameter` is the illuminance of the
ambient light sensor.

:func:`Illuminance` is only triggered if the illuminance has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetIlluminanceCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die Beleuchtungsstärke des Umgebungslichtsensors.

:func:`Illuminance` wird nur ausgelöst wenn sich die Beleuchtungsstärke seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('IlluminanceReached', 'illuminance_reached'), 
'elements': [('illuminance', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetIlluminanceCallbackThreshold` is reached.
The :word:`parameter` is the illuminance of the ambient light sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetIlluminanceCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Beleuchtungsstärke des Umgebungslichtsensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})
