# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Ambient Light Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'category': 'Bricklet',
    'device_identifier': 259,
    'name': ('AmbientLightV2', 'ambient_light_v2', 'Ambient Light 2.0', 'Ambient Light Bricklet 2.0'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures ambient light up to 64000lux',
        'de': 'Misst Umgebungslicht bis zu 64000Lux'
    },
    'released': True,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': ('GetIlluminance', 'get_illuminance'), 
'elements': [('illuminance', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the illuminance of the ambient light sensor. The measurement range goes
up to about 100000lux, but above 64000lux the precision starts to drop.
The illuminance is given in lux/100, i.e. a value of 450000 means that an
illuminance of 4500lux is measured.

.. versionchanged:: 2.0.2$nbsp;(Plugin)
  An illuminance of 0lux indicates that the sensor is saturated and the
  configuration should be modified, see :func:`SetConfiguration`.

If you want to get the illuminance periodically, it is recommended to use the
callback :func:`Illuminance` and set the period with 
:func:`SetIlluminanceCallbackPeriod`.
""",
'de':
"""
Gibt die Beleuchtungsstärke des Umgebungslichtsensors zurück. Der Messbereich
erstreckt sich bis über 100000Lux, aber ab 64000Lux nimmt die Messgenauigkeit
ab. Die Beleuchtungsstärke ist in Lux/100 angegeben, d.h. bei einem Wert von
450000 wurde eine Beleuchtungsstärke von 4500Lux gemessen.

.. versionchanged:: 2.0.2$nbsp;(Plugin)
  Eine Beleuchtungsstärke von 0Lux bedeutet, dass der Sensor gesättigt
  (saturated) ist und die Konfiguration angepasst werden sollte, siehe
  :func:`SetConfiguration`.

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
'elements': [('option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
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
'elements': [('option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
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
'elements': [('illuminance_range', 'uint8', 1, 'in', ('IlluminanceRange', 'illuminance_range', [('Unlimited', 'unlimited', 6),
                                                                                                ('64000Lux', '64000lux', 0),
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
Sets the configuration. It is possible to configure an illuminance range
between 0-600lux and 0-64000lux and an integration time between 50ms and 400ms.

.. versionadded:: 2.0.2$nbsp;(Plugin)
  The unlimited illuminance range allows to measure up to about 100000lux, but
  above 64000lux the precision starts to drop.

A smaller illuminance range increases the resolution of the data. A longer
integration time will result in less noise on the data.

.. versionchanged:: 2.0.2$nbsp;(Plugin)
  If the actual measure illuminance is out-of-range then the current illuminance
  range maximum +0.01lux is reported by :func:`GetIlluminance` and the
  :func:`Illuminance` callback. For example, 800001 for the 0-8000lux range.

.. versionchanged:: 2.0.2$nbsp;(Plugin)
  With a long integration time the sensor might be saturated before the measured
  value reaches the maximum of the selected illuminance range. In this case 0lux
  is reported by :func:`GetIlluminance` and the :func:`Illuminance` callback.

If the measurement is out-of-range or the sensor is saturated then you should
configure the next higher illuminance range. If the highest range is already
in use, then start to reduce the integration time.

The default values are 0-8000lux illuminance range and 200ms integration time.
""",
'de':
"""
Setzt die Konfiguration. Es ist möglich den Helligkeitswertebereich zwischen
0-600Lux und 0-64000Lux sowie eine Integrationszeit zwischen 50ms und 400ms
zu konfigurieren.

.. versionadded:: 2.0.2$nbsp;(Plugin)
  Der unbeschränkt (unlimited) Helligkeitswertebereich ermöglicht es bis über
  100000Lux zu messen, aber ab 64000Lux nimmt die Messgenauigkeit ab.

Ein kleinerer Helligkeitswertebereich erhöht die Auflösung der Daten. Eine
längere Integrationszeit verringert das Rauschen auf den Daten.

.. versionchanged:: 2.0.2$nbsp;(Plugin)
  Wenn der eigentliche Messwert außerhalb des eingestellten
  Helligkeitswertebereichs liegt, dann geben :func:`GetIlluminance` und der
  :func:`Illuminance` Callback das Maximum des eingestellten
  Helligkeitswertebereichs +0,01Lux zurück. Also z.B. 800001 für den 0-8000Lux
  Bereich.

.. versionchanged:: 2.0.2$nbsp;(Plugin)
  Bei einer langen Integrationszeit kann es sein, dass der Sensor gesättigt
  (saturated) ist bevor der Messwert das Maximum des ausgewählten
  Helligkeitswertebereichs erreicht hat. In diesem Fall geben
  :func:`GetIlluminance` und der :func:`Illuminance` Callback 0Lux zurück.

Wenn der Messwert außerhalb des eingestellten Helligkeitswertebereichs liegt
oder der Sensor gesättigt ist, dann sollte der nächst höhere
Helligkeitswertebereich eingestellt werden. Wenn der höchste
Helligkeitswertebereich schon erreicht ist, dann kann noch die Integrationszeit
verringert werden.

Die Standardwerte sind 0-8000Lux Helligkeitsbereich und 200ms Integrationszeit.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetConfiguration', 'get_configuration'), 
'elements': [('illuminance_range', 'uint8', 1, 'out', ('IlluminanceRange', 'illuminance_range', [('Unlimited', 'unlimited', 6),
                                                                                                 ('64000Lux', '64000lux', 0),
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

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Illuminance', 'illuminance'), [(('Illuminance', 'Illuminance'), 'uint32', 100.0, 'Lux/100', 'Lux', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Illuminance', 'illuminance'), [(('Illuminance', 'Illuminance'), 'uint32', 100.0, 'Lux/100', 'Lux', None)], None, None),
              ('callback_period', ('Illuminance', 'illuminance'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('Illuminance Reached', 'illuminance reached'), [(('Illuminance', 'Illuminance'), 'uint32', 100.0, 'Lux/100', 'Lux', None)], None, 'Too bright, close the curtains!'),
              ('callback_threshold', ('Illuminance', 'illuminance'), [], '>', [(500, 0)])]
})
