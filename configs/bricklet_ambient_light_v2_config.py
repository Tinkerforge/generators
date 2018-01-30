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
    'name': 'Ambient Light V2',
    'display_name': 'Ambient Light 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures ambient light up to 64000lux',
        'de': 'Misst Umgebungslicht bis zu 64000Lux'
    },
    'released': True,
    'documented': True,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Get Illuminance',
'elements': [('Illuminance', 'uint32', 1, 'out')],
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
  configuration should be modified, see :func:`Set Configuration`.

If you want to get the illuminance periodically, it is recommended to use the
:cb:`Illuminance` callback and set the period with
:func:`Set Illuminance Callback Period`.
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
  :func:`Set Configuration`.

Wenn die Beleuchtungsstärke periodisch abgefragt werden soll, wird empfohlen
den :cb:`Illuminance` Callback zu nutzen und die Periode mit
:func:`Set Illuminance Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Illuminance Callback Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :cb:`Illuminance` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Illuminance` callback is only triggered if the illuminance has changed
since the last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :cb:`Illuminance` Callback ausgelöst
wird. Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Illuminance` Callback wird nur ausgelöst wenn sich die
Beleuchtungsstärke seit der letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Illuminance Callback Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Illuminance Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Illuminance Callback Period`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Illuminance Callback Threshold',
'elements': [('Option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint32', 1, 'in'),
             ('Max', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Illuminance Reached` callback.

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
Setzt den Schwellwert für den :cb:`Illuminance Reached` Callback.

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
'name': 'Get Illuminance Callback Threshold',
'elements': [('Option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint32', 1, 'out'),
             ('Max', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Illuminance Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Illuminance Callback Threshold`
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

* :cb:`Illuminance Reached`,

are triggered, if the thresholds

* :func:`Set Illuminance Callback Threshold`,

keep being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callbacks

* :cb:`Illuminance Reached`,

ausgelöst werden, wenn die Schwellwerte

* :func:`Set Illuminance Callback Threshold`,

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
'type': 'function',
'name': 'Set Configuration',
'elements': [('Illuminance Range', 'uint8', 1, 'in', ('Illuminance Range', [('Unlimited', 6),
                                                                            ('64000Lux', 0),
                                                                            ('32000Lux', 1),
                                                                            ('16000Lux', 2),
                                                                            ('8000Lux', 3),
                                                                            ('1300Lux', 4),
                                                                            ('600Lux', 5)])),
             ('Integration Time', 'uint8', 1, 'in', ('Integration Time', [('50ms', 0),
                                                                          ('100ms', 1),
                                                                          ('150ms', 2),
                                                                          ('200ms', 3),
                                                                          ('250ms', 4),
                                                                          ('300ms', 5),
                                                                          ('350ms', 6),
                                                                          ('400ms', 7)]))],
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
  range maximum +0.01lux is reported by :func:`Get Illuminance` and the
  :cb:`Illuminance` callback. For example, 800001 for the 0-8000lux range.

.. versionchanged:: 2.0.2$nbsp;(Plugin)
  With a long integration time the sensor might be saturated before the measured
  value reaches the maximum of the selected illuminance range. In this case 0lux
  is reported by :func:`Get Illuminance` and the :cb:`Illuminance` callback.

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
  Helligkeitswertebereichs liegt, dann geben :func:`Get Illuminance` und der
  :cb:`Illuminance` Callback das Maximum des eingestellten
  Helligkeitswertebereichs +0,01Lux zurück. Also z.B. 800001 für den 0-8000Lux
  Bereich.

.. versionchanged:: 2.0.2$nbsp;(Plugin)
  Bei einer langen Integrationszeit kann es sein, dass der Sensor gesättigt
  (saturated) ist bevor der Messwert das Maximum des ausgewählten
  Helligkeitswertebereichs erreicht hat. In diesem Fall geben
  :func:`Get Illuminance` und der :cb:`Illuminance` Callback 0Lux zurück.

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
'name': 'Get Configuration',
'elements': [('Illuminance Range', 'uint8', 1, 'out', ('Illuminance Range', [('Unlimited', 6),
                                                                             ('64000Lux', 0),
                                                                             ('32000Lux', 1),
                                                                             ('16000Lux', 2),
                                                                             ('8000Lux', 3),
                                                                             ('1300Lux', 4),
                                                                             ('600Lux', 5)])),
             ('Integration Time', 'uint8', 1, 'out', ('Integration Time', [('50ms', 0),
                                                                           ('100ms', 1),
                                                                           ('150ms', 2),
                                                                           ('200ms', 3),
                                                                           ('250ms', 4),
                                                                           ('300ms', 5),
                                                                           ('350ms', 6),
                                                                           ('400ms', 7)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Configuration`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Illuminance',
'elements': [('Illuminance', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Illuminance Callback Period`. The :word:`parameter` is the illuminance of the
ambient light sensor.

The :cb:`Illuminance` callback is only triggered if the illuminance has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Illuminance Callback Period`,
ausgelöst. Der :word:`parameter` ist die Beleuchtungsstärke des Umgebungslichtsensors.

Der :cb:`Illuminance` Callback wird nur ausgelöst wenn sich die Beleuchtungsstärke seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Illuminance Reached',
'elements': [('Illuminance', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Illuminance Callback Threshold` is reached.
The :word:`parameter` is the illuminance of the ambient light sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von
:func:`Set Illuminance Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist die Beleuchtungsstärke des Umgebungslichtsensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Illuminance', 'illuminance'), [(('Illuminance', 'Illuminance'), 'uint32', 1, 100.0, 'lx', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Illuminance', 'illuminance'), [(('Illuminance', 'Illuminance'), 'uint32', 1, 100.0, 'lx', None)], None, None),
              ('callback_period', ('Illuminance', 'illuminance'), [], 1000)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('debounce_period', 10000),
              ('callback', ('Illuminance Reached', 'illuminance reached'), [(('Illuminance', 'Illuminance'), 'uint32', 1, 100.0, 'lx', None)], None, 'Too bright, close the curtains!'),
              ('callback_threshold', ('Illuminance', 'illuminance'), [], '>', [(500, 0)])]
})
