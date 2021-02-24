# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Ambient Light Bricklet 3.0 communication config

from generators.configs.commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from generators.configs.commonconstants import add_callback_value_function

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2131,
    'name': 'Ambient Light V3',
    'display_name': 'Ambient Light 3.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures ambient light up to 64000lux',
        'de': 'Misst Umgebungslicht bis zu 64000Lux'
    },
    'released': True,
    'documented': True,
    'discontinued': False,
    'features': [
        'device',
        'comcu_bricklet',
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

illuminance_doc = {
'en':
"""
Returns the illuminance of the ambient light sensor. The measurement range goes
up to about 100000lux, but above 64000lux the precision starts to drop.
The illuminance is given in lux/100, i.e. a value of 450000 means that an
illuminance of 4500lux is measured.

An illuminance of 0lux indicates an error condition where the sensor cannot
perform a reasonable measurement. This can happen with very dim or very bright
light conditions. In bright light conditions this might indicate that the sensor
is saturated and the configuration should be modified (:func:`Set Configuration`)
to better match the conditions.
""",
'de':
"""
Gibt die Beleuchtungsstärke des Umgebungslichtsensors zurück. Der Messbereich
erstreckt sich bis über 100000Lux, aber ab 64000Lux nimmt die Messgenauigkeit
ab. Die Beleuchtungsstärke ist in Lux/100 angegeben, d.h. bei einem Wert von
450000 wurde eine Beleuchtungsstärke von 4500Lux gemessen.

Eine Beleuchtungsstärke von 0Lux bedeutet eine Ausnahmesituation in der der
Sensor keine sinnvolle Messung durchführen kann. Dies kann bei sehr schwacher
oder sehr starker Beleuchtung auftreten. Bei starker Beleuchtung bedeutet diese
möglicherweise, dass der Sensor gesättigt (saturated) ist und die Konfiguration
angepasst werden sollte (:func:`Set Configuration`), um besser der Beleuchtung
zu entsprechen.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Illuminance',
    data_name = 'Illuminance',
    data_type = 'uint32',
    doc       = illuminance_doc,
    scale     = (1, 100),
    unit      = 'Lux'
)

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('Illuminance Range', 'uint8', 1, 'in', {'constant_group': 'Illuminance Range', 'default': 3}),
             ('Integration Time', 'uint8', 1, 'in', {'constant_group': 'Integration Time', 'default': 2})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the configuration. It is possible to configure an illuminance range
between 0-600lux and 0-64000lux and an integration time between 50ms and 400ms.

The unlimited illuminance range allows to measure up to about 100000lux, but
above 64000lux the precision starts to drop.

A smaller illuminance range increases the resolution of the data. A longer
integration time will result in less noise on the data.

If the actual measure illuminance is out-of-range then the current illuminance
range maximum +0.01lux is reported by :func:`Get Illuminance` and the
:cb:`Illuminance` callback. For example, 800001 for the 0-8000lux range.

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

Der unbeschränkt (unlimited) Helligkeitswertebereich ermöglicht es bis über
100000Lux zu messen, aber ab 64000Lux nimmt die Messgenauigkeit ab.

Ein kleinerer Helligkeitswertebereich erhöht die Auflösung der Daten. Eine
längere Integrationszeit verringert das Rauschen auf den Daten.

Wenn der eigentliche Messwert außerhalb des eingestellten
Helligkeitswertebereichs liegt, dann geben :func:`Get Illuminance` und der
:cb:`Illuminance` Callback das Maximum des eingestellten
Helligkeitswertebereichs +0,01Lux zurück. Also z.B. 800001 für den 0-8000Lux
Bereich.

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
             ('Integration Time', 'uint8', 1, 'out', {'constant_group': 'Integration Time', 'default': 2})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
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

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Illuminance', 'Illuminance'), [(('Illuminance', 'Illuminance'), 'uint32', 1, 100.0, 'lx', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Illuminance', 'illuminance'), [(('Illuminance', 'Illuminance'), 'uint32', 1, 100.0, 'lx', None)], None, None),
              ('callback_configuration', ('Illuminance', 'illuminance'), [], 1000, False, 'x', [(0, 0)])]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('callback', ('Illuminance', 'illuminance'), [(('Illuminance', 'Illuminance'), 'uint32', 1, 100.0, 'lx', None)], None, 'Too bright, close the curtains!'),
              ('callback_configuration', ('Illuminance', 'illuminance'), [], 1000, False, '>', [(500, 0)])]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'params': [{
            'packet': 'Set Configuration',
            'element': 'Illuminance Range',

            'name': 'Illuminance Range',
            'type': 'integer',

            'label': {'en': 'Illuminance Range', 'de': 'Helligkeitswertebereich'},
            'description':  {'en': 'The unlimited illuminance range allows to measure up to about 100000lux, but above 64000lux the precision starts to drop.\n\nA smaller illuminance range increases the resolution of the data.\n\nIf the actual measure illuminance is out-of-range then the current illuminance range maximum +0.01lux is reported. For example, 8000.01 for the 0-8000lux range.\n\nIf the measurement is out-of-range or the sensor is saturated then you should configure the next higher illuminance range. If the highest range is already in use, then start to reduce the integration time.',
                             'de': 'Der unbeschränkt (unlimited) Helligkeitswertebereich ermöglicht es bis über 100000Lux zu messen, aber ab 64000Lux nimmt die Messgenauigkeit ab.\n\nEin kleinerer Helligkeitswertebereich erhöht die Auflösung der Daten. \n\nWenn der eigentliche Messwert außerhalb des eingestellten Helligkeitswertebereichs liegt, dann gibt der Channel das Maximum des eingestellten Helligkeitswertebereichs +0,01Lux zurück. Also z.B. 8000,01 für den 0-8000Lux Bereich.\n\nWenn der Messwert außerhalb des eingestellten Helligkeitswertebereichs liegt oder der Sensor gesättigt ist, dann sollte der nächst höhere Helligkeitswertebereich eingestellt werden. Wenn der höchste Helligkeitswertebereich schon erreicht ist, dann kann noch die Integrationszeit verringert werden.'}
        }, {
            'packet': 'Set Configuration',
            'element': 'Integration Time',

            'name': 'Integration Time',
            'type': 'integer',
            'label': {'en': 'Integration Time', 'de': 'Integrationszeit'},
            'description': {'en': 'A longer integration time will result in less noise on the data.\n\nWith a long integration time the sensor might be saturated before the measured value reaches the maximum of the selected illuminance range. In this case 0lux is reported.\n\nIf the measurement is out-of-range or the sensor is saturated then you should configure the next higher illuminance range. If the highest range is already in use, then start to reduce the integration time.',
                            'de': 'Eine längere Integrationszeit verringert das Rauschen auf den Daten.\n\nBei einer langen Integrationszeit kann es sein, dass der Sensor gesättigt (saturated) ist bevor der Messwert das Maximum des ausgewählten Helligkeitswertebereichs erreicht hat. In diesem Fall gibt der Channel 0Lux zurück.\n\nWenn der Messwert außerhalb des eingestellten Helligkeitswertebereichs liegt oder der Sensor gesättigt ist, dann sollte der nächst höhere Helligkeitswertebereich eingestellt werden. Wenn der höchste Helligkeitswertebereich schon erreicht ist, dann kann noch die Integrationszeit verringert werden.'},
        }
    ],
    'init_code': """this.setConfiguration(cfg.illuminanceRange.shortValue(), cfg.integrationTime.shortValue());""",
    'channels': [
        oh_generic_channel('Illuminance', 'Illuminance')
    ],
    'channel_types': [
        oh_generic_channel_type('Illuminance', 'Number', {'en': 'Illuminance', 'de': 'Beleuchtungsstärke'},
                    update_style='Callback Configuration',
                    description={'en': 'The illuminance of the ambient light sensor. The measurement range goes up to about 100000lux, but above 64000lux the precision starts to drop. An illuminance of 0lux indicates that the sensor is saturated and the configuration should be modified.',
                                 'de': 'Gibt die Beleuchtungsstärke des Umgebungslichtsensors zurück. Der Messbereich erstreckt sich bis über 100000 Lux, aber ab 64000 Lux nimmt die Messgenauigkeit ab.\n\nEine Beleuchtungsstärke von 0 Lux bedeutet, dass der Sensor gesättigt (saturated) ist und die Konfiguration angepasst werden sollte.'})
    ],
    'actions': ['Get Illuminance', 'Get Configuration']
}
