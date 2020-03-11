# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Laser Range Finder Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from commonconstants import add_callback_value_function

from openhab_commonconfig import *

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

com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.OnOffType'],
    'params': [{
            'packet': 'Set Moving Average',
            'element': 'Distance Average Length',

            'name': 'Distance Moving Average Length',
            'type': 'integer',
            'default': 10,
            'min': 0,
            'max': 255,

            'label': 'Distance Moving Average Length',
            'groupName': 'average'
        }, {
            'packet': 'Set Moving Average',
            'element': 'Velocity Average Length',

            'name': 'Velocity Moving Average Length',
            'type': 'integer',
            'default': 10,
            'min': 0,
            'max': 255,

            'label': 'Velocity Moving Average Length',
            'groupName': 'average'
        }, {
            'packet': 'Set Configuration',
            'element': 'Acquisition Count',

            'name': 'Acquisition Count',
            'type': 'integer',
            'min': 1,
            'max': 255,
            'default': 128,

            'label': 'Acquisition Count',
            'description': 'The Acquisition Count defines the number of times the Laser Range Finder Bricklet will integrate acquisitions to find a correlation record peak. With a higher count, the Bricklet can measure longer distances. With a lower count, the rate increases. This setting will be ignored if you have a LIDAR-Lite sensor with hardware version 1.',
            'groupName': 'sensor'
        }, {
            'packet': 'Set Configuration',
            'element': 'Enable Quick Termination',

            'name': 'Enable Quick Termination',
            'type': 'boolean',
            'default': 'false',

            'label': 'Enable Quick Termination',
            'description': 'If you enable Quick Termination, the distance measurement will be terminated early if a high peak was already detected. This means that a higher measurement rate can be achieved and long distances can be measured at the same time. However, the chance of false-positive distance measurements increases. This setting will be ignored if you have a LIDAR-Lite sensor with hardware version 1.',
            'groupName': 'sensor'
        }, {
            'packet': 'Set Configuration',
            'element': 'Threshold Value',

            'name': 'Threshold Value',
            'type': 'integer',
            'min': 0,
            'max': 255,
            'default': 0,

            'label': 'Threshold Value',
            'description': 'Normally the distance is calculated with a detection algorithm that uses peak value, signal strength and noise. You can however also define a fixed Threshold Value. Set this to a low value if you want to measure the distance to something that has very little reflection (e.g. glass) and set it to a high value if you want to measure the distance to something with a very high reflection (e.g. mirror). Set this to 0 to use the default algorithm. This setting will be ignored if you have a LIDAR-Lite sensor with hardware version 1.',
            'groupName': 'sensor'
        }, {
            'virtual': True,
            'name': 'Enable Fixed Measurement Frequency',
            'type': 'boolean',
            'default': 'false',

            'label': 'Enable Fixed Measurement Frequency',
            'description': 'For a stable velocity measurement you should set a fixed measurement frequency. See Measurement Frequency for details. This setting will be ignored if you have a LIDAR-Lite sensor with hardware version 1.',
            'groupName': 'sensor'
        }, {
            'packet': 'Set Configuration',
            'element': 'Measurement Frequency',

            'name': 'Measurement Frequency',
            'type': 'integer',
            'min': 10,
            'max': 500,
            'default': 10,

            'label': 'Measurement Frequency',
            'description': 'Set the Measurement Frequency in Hz to force a fixed measurement rate. If set to 0, the Laser Range Finder Bricklet will use the optimal frequency according to the other configurations and the actual measured distance. Since the rate is not fixed in this case, the velocity measurement is not stable. For a stable velocity measurement you should set a fixed measurement frequency. The lower the frequency, the higher is the resolution of the calculated velocity. The allowed values are 10Hz-500Hz. This setting will be ignored if you have a LIDAR-Lite sensor with hardware version 1.',
            'groupName': 'sensor'
        }, {
            'packet': 'Set Distance LED Config',
            'element': 'Config',

            'name': 'Distance LED Config',
            'type': 'integer',
            'default': 3,
            'options': [('Off', 0),
                        ('On', 1),
                        ('Show Heartbeat', 2),
                        ('Show Distance', 3)],
            'limit_to_options': 'true',

            'label': 'Distance LED Config',
            'description': 'Configures the distance LED to be either turned off, turned on, blink in heartbeat mode or show the distance (brighter = object is nearer).',
        }],
    'param_groups': oh_generic_channel_param_groups() + [{
            'name': 'average',
            'label': 'Averaging',
            'description': 'Sets the different averaging parameters. It is possible to set the length of a normal averaging for the temperature and pressure, as well as an additional length of a moving average for the pressure. The moving average is calculated from the normal averages. There is no moving average for the temperature.<br/><br/>The maximum length for the pressure average is 10, for the temperature average is 255 and for the moving average is 25.<br/><br/>Setting the all three parameters to 0 will turn the averaging completely off. If the averaging is off, there is lots of noise on the data, but the data is without delay. Thus we recommend to turn the averaging off if the Barometer Bricklet data is to be used for sensor fusion with other sensors.<br/><br/>The default values are 10 for the normal averages and 25 for the moving average.',
            'advanced': 'true'
        }, {
            'name': 'sensor3',
            'label': 'Sensor Version 3',
            'description': 'Configuration for LIDAR-Lite sensors with hardware version 3',
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
            'id': 'Enable Laser',
            'type': 'Enable Laser',

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
        oh_generic_channel_type('Distance', 'Number', 'Distance',
                    update_style='Callback Configuration',
                    description='The measured distance. Sensor hardware version 1 cannot measure distance and velocity at the same time. Therefore, the distance mode has to be enabled. Sensor hardware version 3 can measure distance and velocity at the same time. Also the laser has to be enabled.',
                    read_only=True,
                    pattern='%.2f %unit%',
                    min_=0,
                    max_=40),
        oh_generic_channel_type('Velocity', 'Number', 'Velocity',
                    update_style='Callback Configuration',
                    description='The measured velocity. Sensor hardware version 1 cannot measure distance and velocity at the same time. Therefore, the velocity mode has to be enabled. Sensor hardware version 3 can measure distance and velocity at the same time, but the velocity measurement only produces stables results if a fixed measurement rateis configured. Also the laser has to be enabled.',
                    read_only=True,
                    pattern='%.2f %unit%',
                    min_=-128,
                    max_=127),
        oh_generic_channel_type('Enable Laser', 'Switch', 'Enable Laser',
                    update_style=None,
                    description='Activates the laser of the LIDAR.'),
    ],
    'actions': ['Get Distance', 'Get Velocity',
                {'fn': 'Set Enable', 'refreshs': ['Enable Laser']}, 'Get Enable',
                'Get Configuration', 'Get Distance LED Config', 'Get Moving Average', 'Get Offset Calibration']
}
