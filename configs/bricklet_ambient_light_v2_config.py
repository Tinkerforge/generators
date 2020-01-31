# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Ambient Light Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'api_version_extra': 1, # +1 for "Add unlimited illuminacne range config [a13e071]"
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
    'discontinued': True, # replaced by Ambient Light Bricklet 3.0
    'features': [
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

com['constant_groups'].append({
'name': 'Illuminance Range',
'type': 'uint8',
'constants': [('Unlimited', 6),
              ('64000Lux', 0),
              ('32000Lux', 1),
              ('16000Lux', 2),
              ('8000Lux', 3),
              ('1300Lux', 4),
              ('600Lux', 5)]
})

com['constant_groups'].append({
'name': 'Integration Time',
'type': 'uint8',
'constants': [('50ms', 0),
              ('100ms', 1),
              ('150ms', 2),
              ('200ms', 3),
              ('250ms', 4),
              ('300ms', 5),
              ('350ms', 6),
              ('400ms', 7)]
})

com['packets'].append({
'type': 'function',
'name': 'Get Illuminance',
'elements': [('Illuminance', 'uint32', 1, 'out', {'scale': (1, 100), 'unit': 'Lux'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the illuminance of the ambient light sensor. The measurement range goes
up to about 100000lux, but above 64000lux the precision starts to drop.

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
ab.

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
'name': 'Set Illuminance Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint32', 1, 'in', {'scale': (1, 100), 'unit': 'Lux', 'default': 0}),
             ('Max', 'uint32', 1, 'in', {'scale': (1, 100), 'unit': 'Lux', 'default': 0})],
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
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Illuminance Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn die Beleuchtungsstärke *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn die Beleuchtungsstärke *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn die Beleuchtungsstärke kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn die Beleuchtungsstärke größer als der min Wert ist (max wird ignoriert)"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Illuminance Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint32', 1, 'out', {'scale': (1, 100), 'unit': 'Lux', 'default': 0}),
             ('Max', 'uint32', 1, 'out', {'scale': (1, 100), 'unit': 'Lux', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Illuminance Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Illuminance Callback Threshold` gesetzt.
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

* :cb:`Illuminance Reached`,

are triggered, if the thresholds

* :func:`Set Illuminance Callback Threshold`,

keep being reached.
""",
'de':
"""
Setzt die Periode mit welcher die Schwellwert Callbacks

* :cb:`Illuminance Reached`,

ausgelöst werden, wenn die Schwellwerte

* :func:`Set Illuminance Callback Threshold`,

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
'name': 'Set Configuration',
'elements': [('Illuminance Range', 'uint8', 1, 'in', {'constant_group': 'Illuminance Range', 'default': 3}),
             ('Integration Time', 'uint8', 1, 'in', {'constant_group': 'Integration Time', 'default': 3})],
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
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Illuminance Range', 'uint8', 1, 'out', {'constant_group': 'Illuminance Range', 'default': 3}),
             ('Integration Time', 'uint8', 1, 'out', {'constant_group': 'Integration Time', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Illuminance',
'elements': [('Illuminance', 'uint32', 1, 'out', {'scale': (1, 100), 'unit': 'Lux'})],
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

Der :cb:`Illuminance` Callback wird nur ausgelöst, wenn sich die Beleuchtungsstärke seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Illuminance Reached',
'elements': [('Illuminance', 'uint32', 1, 'out', {'scale': (1, 100), 'unit': 'Lux'})],
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
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
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

com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'params': [{
            'packet': 'Set Configuration',
            'element': 'Illuminance Range',

            'name': 'Illuminance Range',
            'type': 'integer',
            'options': [('Unlimited', 6),
                        ('64000Lux', 0),
                        ('32000Lux', 1),
                        ('16000Lux', 2),
                        ('8000Lux', 3),
                        ('1300Lux', 4),
                        ('600Lux', 5)],
            'limitToOptions': 'true',
            'default': 3,

            'label': 'Illuminance Range',
            'description': 'The unlimited illuminance range allows to measure up to about 100000lux, but above 64000lux the precision starts to drop.<br/><br/>A smaller illuminance range increases the resolution of the data.<br/><br/>If the actual measure illuminance is out-of-range then the current illuminance range maximum +0.01lux is reported. For example, 800001 for the 0-8000lux range.<br/><br/>If the measurement is out-of-range or the sensor is saturated then you should configure the next higher illuminance range. If the highest range is already in use, then start to reduce the integration time.',
        }, {
            'packet': 'Set Configuration',
            'element': 'Integration Time',

            'name': 'Integration Time',
            'type': 'integer',
            'options': [('50ms', 0),
                        ('100ms', 1),
                        ('150ms', 2),
                        ('200ms', 3),
                        ('250ms', 4),
                        ('300ms', 5),
                        ('350ms', 6),
                        ('400ms', 7)],
            'limitToOptions': 'true',
            'default': 3,

            'label': 'Integration Time',
            'description': 'A longer integration time will result in less noise on the data.<br/><br/>With a long integration time the sensor might be saturated before the measured value reaches the maximum of the selected illuminance range. In this case 0lux is reported.<br/><br/>If the measurement is out-of-range or the sensor is saturated then you should configure the next higher illuminance range. If the highest range is already in use, then start to reduce the integration time.',
        }
    ],
    'init_code': """this.setConfiguration(cfg.illuminanceRange, cfg.integrationTime);""",
    'channels': [
        oh_generic_old_style_channel('Illuminance', 'Illuminance', 'SmartHomeUnits.LUX', divisor=100.0)
    ],
    'channel_types': [
        oh_generic_channel_type('Illuminance', 'Number:Illuminance', 'Illuminance',
                    update_style='Callback Period',
                    description='The illuminance of the ambient light sensor. The measurement range goes up to about 100000lux, but above 64000lux the precision starts to drop. An illuminance of 0lux indicates that the sensor is saturated and the configuration should be modified.',
                    read_only=True,
                    pattern='%.2f %unit%',
                    min_=0,
                    max_=100000)
    ],
    'actions': ['Get Illuminance', 'Get Configuration']
}
