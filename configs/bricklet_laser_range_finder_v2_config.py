# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Laser Range Finder Bricklet 2.0 communication config

from generators.configs.commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from generators.configs.commonconstants import add_callback_value_function

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2144,
    'name': 'Laser Range Finder V2',
    'display_name': 'Laser Range Finder 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures distance up to 40m with laser light',
        'de': 'Misst Entfernung bis zu 40m mit Laser-Licht'
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
'name': 'Distance LED Config',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Show Heartbeat', 2),
              ('Show Distance', 3)]
})

distance_doc = {
'en':
"""
Returns the measured distance.

The laser has to be enabled, see :func:`Set Enable`.
""",
'de':
"""
Gibt die gemessene Distanz zurück.

Der Laser muss aktiviert werden, siehe :func:`Set Enable`.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Distance',
    data_name = 'Distance',
    data_type = 'int16',
    doc       = distance_doc,
    scale     = (1, 100),
    unit      = 'Meter',
    range_    = (0, 4000)
)

velocity_doc = {
'en':
"""
Returns the measured velocity. The value has a range of -12800 to 12700
and is given in 1/100 m/s.

The velocity measurement only produces stables results if a fixed
measurement rate (see :func:`Set Configuration`) is configured. Also the laser
has to be enabled, see :func:`Set Enable`.
""",
'de':
"""
Gibt die gemessene Geschwindigkeit zurück.

Die Geschwindigkeitsmessung liefert nur dann stabile Werte,
wenn eine feste Messfrequenz (siehe :func:`Set Configuration`) eingestellt ist.
Zusätzlich muss der Laser aktiviert werden, siehe :func:`Set Enable`.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Velocity',
    data_name = 'Velocity',
    data_type = 'int16',
    doc       = velocity_doc,
    scale     = (1, 100),
    unit      = 'Meter Per Second',
    range_    = (-12800, 12700)
)

com['packets'].append({
'type': 'function',
'name': 'Set Enable',
'elements': [('Enable', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Enables the laser of the LIDAR if set to *true*.

We recommend that you wait 250ms after enabling the laser before
the first call of :func:`Get Distance` to ensure stable measurements.
""",
'de':
"""
Aktiviert den Laser des LIDAR wenn auf *true* gesetzt.

Wir empfehlen nach dem Aktivieren des Lasers 250ms zu warten bis zum
ersten Aufruf von :func:`Get Distance` um stabile Messwerte zu garantieren.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Enable',
'elements': [('Enable', 'bool', 1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the value as set by :func:`Set Enable`.
""",
'de':
"""
Gibt den Wert zurück wie von :func:`Set Enable` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('Acquisition Count', 'uint8', 1, 'in', {'range': (1, 255), 'default': 128}),
             ('Enable Quick Termination', 'bool', 1, 'in', {'default': False}),
             ('Threshold Value', 'uint8', 1, 'in', {'default': 0}),
             ('Measurement Frequency', 'uint16', 1, 'in', {'unit': 'Hertz', 'range': [(0, 0), (10, 500)], 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
The **Acquisition Count** defines the number of times the Laser Range Finder Bricklet
will integrate acquisitions to find a correlation record peak. With a higher count,
the Bricklet can measure longer distances. With a lower count, the rate increases. The
allowed values are 1-255.

If you set **Enable Quick Termination** to true, the distance measurement will be terminated
early if a high peak was already detected. This means that a higher measurement rate can be achieved
and long distances can be measured at the same time. However, the chance of false-positive
distance measurements increases.

Normally the distance is calculated with a detection algorithm that uses peak value,
signal strength and noise. You can however also define a fixed **Threshold Value**.
Set this to a low value if you want to measure the distance to something that has
very little reflection (e.g. glass) and set it to a high value if you want to measure
the distance to something with a very high reflection (e.g. mirror). Set this to 0 to
use the default algorithm. The other allowed values are 1-255.

Set the **Measurement Frequency** to force a fixed measurement rate. If set to 0,
the Laser Range Finder Bricklet will use the optimal frequency according to the other
configurations and the actual measured distance. Since the rate is not fixed in this case,
the velocity measurement is not stable. For a stable velocity measurement you should
set a fixed measurement frequency. The lower the frequency, the higher is the resolution
of the calculated velocity. The allowed values are 10Hz-500Hz (and 0 to turn the fixed
frequency off).

The default values for Acquisition Count, Enable Quick Termination, Threshold Value and
Measurement Frequency are 128, false, 0 and 0.
""",
'de':
"""
Der Parameter **Acquisition Count** definiert die Anzahl der Datenerfassungen die integriert
werden, um eine Korrelation zu finden. Mit einer größeren Anzahl kann das Bricklet höhere
Distanzen messen, mit einer kleineren Anzahl ist die Messrate höher. Erlaubte Werte sind 1-255.

Wenn der Parameter **Enable Quick Termination** auf true gesetzt wird, wird die Distanzmessung
abgeschlossen, sobald das erste mal ein hoher Peak erfasst wird. Dadurch kann eine höhere Messrate
erreicht werden wobei gleichzeitig Messungen mit langer Distanz möglich sind. Die Wahrscheinlichkeit
einer Falschmessung erhöht sich allerdings.

Normalerweise wird die Distanz mit Hilfe eines Detektionsalgorithmus berechnet. Dieser verwendet
Peak-Werte, Signalstärke und Rauschen. Es ist möglich stattdessen über den Parameter
**Threshold Value** einen festen Schwellwert zu setzen der zur Distanzbestimmung genutzt werden soll.
Um den Abstand zu einem Objekt mit sehr niedriger Reflektivität zu messen (z.B. Glas) kann der Wert
niedrig gesetzt werden. Um den Abstand zu einem Objekt mit sehr hoher Reflektivität zu messen
(z.B. Spiegel) kann der Wert sehr hoch gesetzt werden. Mit einem Wert von 0 wird der Standardalgorithmus
genutzt. Ansonsten ist der erlaubte Wertebereich 1-255.

Der **Measurement Frequency** Parameter wird gesetzt. Er erzwingt eine feste Messfrequenz.
Wenn der Wert auf 0 gesetzt wird, nutzt das Laser Range Finder Bricklet die optimale Frequenz je nach
Konfiguration und aktuell gemessener Distanz. Da die Messrate in diesem Fall nicht fest ist, ist die
Geschwindigkeitsmessung nicht stabil. Für eine stabile Geschwindigkeitsmessung sollte eine feste
Messfrequenz eingestellt werden. Je niedriger die Frequenz ist, desto größer ist die Auflösung
der Geschwindigkeitsmessung. Der erlaubte Wertbereich ist 10Hz-500Hz (und 0 um die feste
Messfrequenz auszustellen).

Die Standardwerte für Acquisition Count, Enable Quick Termination, Threshold Value und
Measurement Frequency sind 128, false, 0 und 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Acquisition Count', 'uint8', 1, 'out', {'range': (1, 255), 'default': 128}),
             ('Enable Quick Termination', 'bool', 1, 'out', {'default': False}),
             ('Threshold Value', 'uint8', 1, 'out', {'default': 0}),
             ('Measurement Frequency', 'uint16', 1, 'out', {'unit': 'Hertz', 'range': [(0, 0), (10, 500)], 'default': 0})],
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

com['packets'].append({
'type': 'function',
'name': 'Set Moving Average',
'elements': [('Distance Average Length', 'uint8', 1, 'in', {'default': 10}),
             ('Velocity Average Length', 'uint8', 1, 'in', {'default': 10})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
for the distance and velocity.

Setting the length to 0 will turn the averaging completely off. With less
averaging, there is more noise on the data.
""",
'de':
"""
Setzt die Länge eines `gleitenden Mittelwerts <https://de.wikipedia.org/wiki/Gleitender_Mittelwert>`__
für die Entfernung und Geschwindigkeit.

Wenn die Länge auf 0 gesetzt wird, ist das Averaging komplett aus. Desto kleiner
die Länge des Mittelwerts ist, desto mehr Rauschen ist auf den Daten.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Moving Average',
'elements': [('Distance Average Length', 'uint8', 1, 'out', {'default': 10}),
             ('Velocity Average Length', 'uint8', 1, 'out', {'default': 10})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the length moving average as set by :func:`Set Moving Average`.
""",
'de':
"""
Gibt die Länge des gleitenden Mittelwerts zurück, wie von
:func:`Set Moving Average` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Offset Calibration',
'elements': [('Offset', 'int16', 1, 'in', {'scale': (1, 100), 'unit': 'Meter', 'range': (None, 2**15 - 1 - 4000)})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
The offset is added to the measured distance.
It is saved in non-volatile memory, you only have to set it once.

The Bricklet comes with a per-sensor factory-calibrated offset value,
you should not have to call this function.

If you want to re-calibrate the offset you first have to set it to 0.
Calculate the offset by measuring the distance to a known distance
and set it again.
""",
'de':
"""
Der Offset wird auf die Distanz addiert. Es wird in
nicht-flüchtigen Speicher gespeichert und muss nur einmal gesetzt werden.

Der Offset wird für das Bricklet pro Sensor von Tinkerforge werkskalibriert.
Ein Aufruf dieser Funktion sollte also nicht notwendig sein.

Wenn der Offset re-kalibriert werden soll muss er zuerst auf 0 gesetzt. Danach
kann der Offset wieder gesetzt werden in dem die Differenz zu einer
bekannte Distanz gemessen wird.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Offset Calibration',
'elements': [('Offset', 'int16', 1, 'out', {'scale': (1, 100), 'unit': 'Meter', 'range': (None, 2**15-1-4000)})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the offset value as set by :func:`Set Offset Calibration`.
""",
'de':
"""
Gibt den Offset-Wert zurück, wie von :func:`Set Offset Calibration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Distance LED Config',
'elements': [('Config', 'uint8', 1, 'in', {'constant_group': 'Distance LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Configures the distance LED to be either turned off, turned on, blink in
heartbeat mode or show the distance (brighter = object is nearer).
""",
'de':
"""
Konfiguriert die Distanz-LED. Die LED kann ausgeschaltet, eingeschaltet,
im Herzschlagmodus betrieben werden. Zusätzlich gibt es die Option
mit der LED die Distanz anzuzeigen (heller = Objekt näher).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Distance LED Config',
'elements': [('Config', 'uint8', 1, 'out', {'constant_group': 'Distance LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the LED configuration as set by :func:`Set Distance LED Config`
""",
'de':
"""
Gibt die LED-Konfiguration zurück, wie von :func:`Set Distance LED Config` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('setter', 'Set Enable', [('bool', True)], 'Turn laser on and wait 250ms for very first measurement to be ready', None),
              ('sleep', 250, None, None),
              ('getter', ('Get Distance', 'distance'), [(('Distance', 'Distance'), 'int16', 1, None, 'cm', None)], [])],
'cleanups': [('setter', 'Set Enable', [('bool', False)], 'Turn laser off', None)]
})

com['examples'].append({
'name': 'Callback',
'functions': [('setter', 'Set Enable', [('bool', True)], 'Turn laser on and wait 250ms for very first measurement to be ready', None),
              ('sleep', 250, None, None),
              ('callback', ('Distance', 'distance'), [(('Distance', 'Distance'), 'int16', 1, None, 'cm', None)], None, None),
              ('callback_configuration', ('Distance', 'distance'), [], 200, False, 'x', [(0, 0)])],
'cleanups': [('setter', 'Set Enable', [('bool', False)], 'Turn laser off', None)]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('setter', 'Set Enable', [('bool', True)], 'Turn laser on and wait 250ms for very first measurement to be ready', None),
              ('sleep', 250, None, None),
              ('callback', ('Distance', 'distance'), [(('Distance', 'Distance'), 'int16', 1, None, 'cm', None)], None, None),
              ('callback_configuration', ('Distance', 'distance'), [], 1000, False, '>', [(20, 0)])],
'cleanups': [('setter', 'Set Enable', [('bool', False)], 'Turn laser off', None)]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.OnOffType'],
    'params': [{
            'packet': 'Set Moving Average',
            'element': 'Distance Average Length',

            'name': 'Distance Moving Average Length',
            'type': 'integer',
            'label': {'en': 'Distance Moving Average Length', 'de': 'Länge des gleitenden Distanz-Mittelwerts'},
            'description': {'en': 'The length of a moving averaging for the distance.',
                            'de': 'Die Länge eines gleitenden Mittelwerts für die Distanz'},
            'groupName': 'average'
        }, {
            'packet': 'Set Moving Average',
            'element': 'Velocity Average Length',

            'name': 'Velocity Moving Average Length',
            'type': 'integer',
            'label': {'en': 'Velocity Moving Average Length', 'de': 'Länge des gleitenden Geschwindigkeits-Mittelwerts'},
            'description': {'en': 'The length of a moving averaging for the velocity.',
                            'de': 'Die Länge eines gleitenden Mittelwerts für die Geschwindigkeit'},
            'groupName': 'average'
        }, {
            'packet': 'Set Configuration',
            'element': 'Acquisition Count',

            'name': 'Acquisition Count',
            'type': 'integer',
            'label': 'Acquisition Count',
            'label': {'en': 'Acquisition Count', 'de': 'Datenerfassungs-Anzahl'},
            'description': {'en': 'The acquisition count defines the number of times the Laser Range Finder Bricklet will integrate acquisitions to find a correlation record peak. With a higher count, the Bricklet can measure longer distances. With a lower count, the rate increases.',
                            'de': 'Die Datenerfassungs-Anzahl definiert die Anzahl der Datenerfassungen die integriert werden, um eine Korrelation zu finden. Mit einer größeren Anzahl kann das Bricklet höhere Distanzen messen, mit einer kleineren Anzahl ist die Messrate höher. Erlaubte Werte sind 1-255.'},
        }, {
            'packet': 'Set Configuration',
            'element': 'Enable Quick Termination',

            'name': 'Enable Quick Termination',
            'type': 'boolean',

            'label': {'en': 'Quick Termination', 'de': 'Schnellterminierung'},
            'description': {'en': 'If you enable Quick Termination, the distance measurement will be terminated early if a high peak was already detected. This means that a higher measurement rate can be achieved and long distances can be measured at the same time. However, the chance of false-positive distance measurements increases.',
                            'de': 'Wenn die Schnellterminierung aktiviert wird, wird die Distanzmessung abgeschlossen, sobald das erste mal ein hoher Peak erfasst wird. Dadurch kann eine höhere Messrate erreicht werden wobei gleichzeitig Messungen mit langer Distanz möglich sind. Die Wahrscheinlichkeit einer Falschmessung erhöht sich allerdings.'},
        }, {
            'packet': 'Set Configuration',
            'element': 'Threshold Value',

            'name': 'Threshold Value',
            'type': 'integer',
            'label': {'en': 'Threshold Value', 'de': 'Schwellwert'},
            'description': {'en': 'Normally the distance is calculated with a detection algorithm that uses peak value, signal strength and noise. You can however also define a fixed Threshold Value. Set this to a low value if you want to measure the distance to something that has very little reflection (e.g. glass) and set it to a high value if you want to measure the distance to something with a very high reflection (e.g. mirror). Set this to 0 to use the default algorithm.',
                            'de': 'Normalerweise wird die Distanz mit Hilfe eines Detektionsalgorithmus berechnet. Dieser verwendet Peak-Werte, Signalstärke und Rauschen. Es ist möglich stattdessen einen festen Schwellwert zu setzen der zur Distanzbestimmung genutzt werden soll. Um den Abstand zu einem Objekt mit sehr niedriger Reflektivität zu messen (z.B. Glas) kann der Wert niedrig gesetzt werden. Um den Abstand zu einem Objekt mit sehr hoher Reflektivität zu messen (z.B. Spiegel) kann der Wert sehr hoch gesetzt werden. Mit einem Wert von 0 wird der Standardalgorithmus genutzt.'},
        }, {
            'virtual': True,
            'name': 'Enable Fixed Measurement Frequency',
            'type': 'boolean',
            'default': 'false',

            'label': {'en': 'Fixed Measurement Frequency', 'de': 'Feste Messfrequenz'},
            'description': {'en': 'For a stable velocity measurement you should set a fixed measurement frequency. See Measurement Frequency for details.',
                            'de': 'Für eine stabile Geschwindigkeitsmessung sollte die feste Messfrequenz aktiviert werden. Siehe die Messfrequenz-Konfiguration für Details.'},
        }, {
            'packet': 'Set Configuration',
            'element': 'Measurement Frequency',

            'name': 'Measurement Frequency',
            'type': 'integer',
            'min': 10,
            'default': 10,

            'label': {'en': 'Measurement Frequency', 'de': 'Messfrequenz'},
            'description': {'en': 'If the fixed measurement frequency is enabled, the measurement frequency is forced to this value. If it is disabled, the Laser Range Finder Bricklet will use the optimal frequency according to the other configurations and the actual measured distance. Since the rate is not fixed in this case, the velocity measurement is not stable. For a stable velocity measurement you should set a fixed measurement frequency. The lower the frequency, the higher is the resolution of the calculated velocity.',
                            'de': 'Wenn die feste Messfrequenz aktiviert ist, wird eine Messfrequenz von diesem Wert erzwungen. Wenn sie deaktiviert ist, nutzt das Laser Range Finder Bricklet die optimale Frequenz je nach Konfiguration und aktuell gemessener Distanz. Da die Messrate in diesem Fall nicht fest ist, ist die Geschwindigkeitsmessung nicht stabil. Für eine stabile Geschwindigkeitsmessung sollte eine feste Messfrequenz eingestellt werden. Je niedriger die Frequenz ist, desto größer ist die Auflösung der Geschwindigkeitsmessung.'},
        }, {
            'packet': 'Set Distance LED Config',
            'element': 'Config',

            'name': 'Distance LED Config',
            'type': 'integer',

            'label': {'en': 'Distance LED', 'de': 'Distanz-LED'},
            'description': {'en': 'Configures the distance LED to be either turned off, turned on, blink in heartbeat mode or show the distance (brighter = object is nearer).',
                            'de': 'Konfiguriert die Distanz-LED. Die LED kann ausgeschaltet, eingeschaltet, im Herzschlagmodus betrieben werden. Zusätzlich gibt es die Option mit der LED die Distanz anzuzeigen (heller = Objekt näher).'}
        }],
    'param_groups': oh_generic_channel_param_groups() + [{
            'name': 'average',
            'label': 'Averaging',
            'description': 'Sets the different averaging parameters. It is possible to set the length of a normal averaging for the temperature and pressure, as well as an additional length of a moving average for the pressure. The moving average is calculated from the normal averages. There is no moving average for the temperature.\n\nThe maximum length for the pressure average is 10, for the temperature average is 255 and for the moving average is 25.\n\nSetting the all three parameters to 0 will turn the averaging completely off. If the averaging is off, there is lots of noise on the data, but the data is without delay. Thus we recommend to turn the averaging off if the Barometer Bricklet data is to be used for sensor fusion with other sensors.\n\nThe default values are 10 for the normal averages and 25 for the moving average.',
            'advanced': 'true'
        }
    ],
    'init_code': """
    this.setConfiguration(cfg.acquisitionCount, cfg.enableQuickTermination, cfg.thresholdValue, cfg.enableFixedMeasurementFrequency ? cfg.measurementFrequency : 0);
    this.setMovingAverage(cfg.distanceMovingAverageLength, cfg.velocityMovingAverageLength);
    this.setDistanceLEDConfig(cfg.distanceLEDConfig);""",
    'channels': [
        oh_generic_channel('Distance', 'Distance'),
        oh_generic_channel('Velocity', 'Velocity'),
        {
            'id': 'Laser',
            'type': 'Laser',

            'setters': [{
                'packet': 'Set Enable',
                'element': 'Enable',
                'packet_params': ['cmd == OnOffType.ON'],
                'command_type': "OnOffType",
            }],

            'getters': [{
                'packet': 'Get Enable',
                'element': 'Enable',
                'transform': 'value? OnOffType.ON : OnOffType.OFF'}]
        }
    ],
    'channel_types': [
        oh_generic_channel_type('Distance', 'Number', {'en': 'Distance', 'de': 'Distanz'},
                    update_style='Callback Configuration',
                    description={'en': 'The measured distance. The laser has to be enabled.',
                                 'de': 'Die gemessene Distanz. Der Laser muss aktiviert sein.'}),
        oh_generic_channel_type('Velocity', 'Number', 'Velocity',
                    update_style='Callback Configuration',
                    description={'en': 'The measured velocity. The velocity measurement only produces stables results if a fixed measurement frequency is configured. Also the laser has to be enabled.',
                                 'de': 'Die gemessene Geschwindigkeit. Die Geschwindigkeitsmessung liefert nur stabile Werte, wenn eine feste Messfrequenz konfiguriert ist. Außerdem muss der Laser aktiviert sein.'}),
        oh_generic_channel_type('Laser', 'Switch', {'en': 'Laser', 'de': 'Laser'},
                    update_style=None,
                    description={'en': 'Activates/Deactivates the laser of the LIDAR.',
                                 'de': 'Aktiviert/Deaktiviert den Laser des LIDARs.'}),
    ],
    'actions': ['Get Distance', 'Get Velocity',
                {'fn': 'Set Enable', 'refreshs': ['Laser']}, 'Get Enable',
                'Get Configuration', 'Get Distance LED Config', 'Get Moving Average', 'Get Offset Calibration']
}
