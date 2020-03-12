# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Laser Range Finder Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP

from openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'category': 'Bricklet',
    'device_identifier': 255,
    'name': 'Laser Range Finder',
    'display_name': 'Laser Range Finder',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures distance up to 40m with laser light',
        'de': 'Misst Entfernung bis zu 40m mit Laser-Licht'
    },
    'released': True,
    'documented': True,
    'discontinued': True, # replaced by Laser Range Finder Bricklet 2.0
    'features': [
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

com['constant_groups'].append({
'name': 'Mode',
'type': 'uint8',
'constants': [('Distance', 0),
              ('Velocity Max 13ms', 1),
              ('Velocity Max 32ms', 2),
              ('Velocity Max 64ms', 3),
              ('Velocity Max 127ms', 4)]
})

com['constant_groups'].append({
'name': 'Version',
'type': 'uint8',
'constants': [('1', 1),
              ('3', 3)]
})

com['packets'].append({
'type': 'function',
'name': 'Get Distance',
'elements': [('Distance', 'uint16', 1, 'out', {'scale': (1, 100), 'unit': 'Meter', 'range': (0, 4000)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the measured distance.

Sensor hardware version 1 (see :func:`Get Sensor Hardware Version`) cannot
measure distance and velocity at the same time. Therefore, the distance mode
has to be enabled using :func:`Set Mode`.
Sensor hardware version 3 can measure distance and velocity at the same
time. Also the laser has to be enabled, see :func:`Enable Laser`.

If you want to get the distance periodically, it is recommended to
use the :cb:`Distance` callback and set the period with
:func:`Set Distance Callback Period`.
""",
'de':
"""
Gibt die gemessene Distanz zurück.

Sensor Hardware Version 1 (siehe :func:`Get Sensor Hardware Version`) kann nicht
gleichzeitig Distanz und Geschwindigkeit messen. Daher muss mittels
:func:`Set Mode` der Distanzmodus aktiviert sein.
Sensor Hardware Version 3 kann gleichzeitig Distanz und Geschwindigkeit
messen. Zusätzlich muss der Laser aktiviert werden, siehe :func:`Enable Laser`.

Wenn der Entfernungswert periodisch abgefragt werden soll, wird empfohlen
den :cb:`Distance` Callback zu nutzen und die Periode mit
:func:`Set Distance Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Velocity',
'elements': [('Velocity', 'int16', 1, 'out', {'scale': (1, 100), 'unit': 'Meter Per Second', 'range': (-12800, 12700)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the measured velocity.

Sensor hardware version 1 (see :func:`Get Sensor Hardware Version`) cannot
measure distance and velocity at the same time. Therefore, the velocity mode
has to be enabled using :func:`Set Mode`.
Sensor hardware version 3 can measure distance and velocity at the same
time, but the velocity measurement only produces stables results if a fixed
measurement rate (see :func:`Set Configuration`) is configured. Also the laser
has to be enabled, see :func:`Enable Laser`.

If you want to get the velocity periodically, it is recommended to
use the :cb:`Velocity` callback and set the period with
:func:`Set Velocity Callback Period`.
""",
'de':
"""
Gibt die gemessene Geschwindigkeit zurück.

Sensor Hardware Version 1 (siehe :func:`Get Sensor Hardware Version`) kann nicht
gleichzeitig Distanz und Geschwindigkeit messen. Daher muss mittels
:func:`Set Mode` ein Geschwindigkeitsmodus aktiviert sein.
Sensor Hardware Version 3 kann gleichzeitig Distanz und Geschwindigkeit
messen, jedoch liefert die Geschwindigkeitsmessung nur dann stabile Werte,
wenn eine feste Messfrequenz (siehe :func:`Set Configuration`) eingestellt ist.
Zusätzlich muss der Laser aktiviert werden, siehe :func:`Enable Laser`.

Wenn der Geschwindigkeitswert periodisch abgefragt werden soll, wird empfohlen
den :cb:`Velocity` Callback zu nutzen und die Periode mit
:func:`Set Velocity Callback Period` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Distance Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Distance` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Distance` callback is only triggered if the distance value has
changed since the last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Distance` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Distance` Callback wird nur ausgelöst, wenn sich der Entfernungswert
seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Distance Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Distance Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Distance Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Velocity Callback Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`Velocity` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Velocity` callback is only triggered if the velocity value has
changed since the last triggering.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Velocity` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Velocity` Callback wird nur ausgelöst, wenn sich der
Geschwindigkeitswert seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Velocity Callback Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Velocity Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Velocity Callback Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Distance Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'in', {'scale': (1, 100), 'unit': 'Meter', 'default': 0}),
             ('Max', 'uint16', 1, 'in', {'scale': (1, 100), 'unit': 'Meter', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Distance Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the distance value is *outside* the min and max values"
 "'i'",    "Callback is triggered when the distance value is *inside* the min and max values"
 "'<'",    "Callback is triggered when the distance value is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the distance value is greater than the min value (max is ignored)"
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Distance Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn der Entfernungswert *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn der Entfernungswert *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn der Entfernungswert kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn der Entfernungswert größer als der min Wert ist (max wird ignoriert)"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Distance Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'uint16', 1, 'out', {'scale': (1, 100), 'unit': 'Meter', 'default': 0}),
             ('Max', 'uint16', 1, 'out', {'scale': (1, 100), 'unit': 'Meter', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Distance Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Distance Callback Threshold` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Velocity Callback Threshold',
'elements': [('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'int16', 1, 'in', {'scale': (1, 100), 'unit': 'Meter Per Second', 'default': 0}),
             ('Max', 'int16', 1, 'in', {'scale': (1, 100), 'unit': 'Meter Per Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :cb:`Velocity Reached` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Callback is turned off"
 "'o'",    "Callback is triggered when the velocity is *outside* the min and max values"
 "'i'",    "Callback is triggered when the velocity is *inside* the min and max values"
 "'<'",    "Callback is triggered when the velocity is smaller than the min value (max is ignored)"
 "'>'",    "Callback is triggered when the velocity is greater than the min value (max is ignored)"
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Velocity Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst, wenn der Geschwindigkeitswert *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst, wenn der Geschwindigkeitswert *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst, wenn der Geschwindigkeitswert kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst, wenn der Geschwindigkeitswert größer als der min Wert ist (max wird ignoriert)"
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Velocity Callback Threshold',
'elements': [('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
             ('Min', 'int16', 1, 'out', {'scale': (1, 100), 'unit': 'Meter Per Second', 'default': 0}),
             ('Max', 'int16', 1, 'out', {'scale': (1, 100), 'unit': 'Meter Per Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Velocity Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Velocity Callback Threshold` gesetzt.
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

* :cb:`Distance Reached`,
* :cb:`Velocity Reached`,

are triggered, if the thresholds

* :func:`Set Distance Callback Threshold`,
* :func:`Set Velocity Callback Threshold`,

keep being reached.
""",
'de':
"""
Setzt die Periode mit welcher die Schwellwert Callbacks

* :cb:`Distance Reached`,
* :cb:`Velocity Reached`,

ausgelöst werden, wenn die Schwellwerte

* :func:`Set Distance Callback Threshold`,
* :func:`Set Velocity Callback Threshold`,

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
'name': 'Set Moving Average',
'elements': [('Distance Average Length', 'uint8', 1, 'in', {'range': (0, 30), 'default': 10}),
             ('Velocity Average Length', 'uint8', 1, 'in', {'range': (0, 30), 'default': 10})],
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
'elements': [('Distance Average Length', 'uint8', 1, 'out', {'range': (0, 30), 'default': 10}),
             ('Velocity Average Length', 'uint8', 1, 'out', {'range': (0, 30), 'default': 10})],
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
'name': 'Set Mode',
'elements': [('Mode', 'uint8', 1, 'in', {'constant_group': 'Mode', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
.. note::
 This function is only available if you have a LIDAR-Lite sensor with hardware
 version 1. Use :func:`Set Configuration` for hardware version 3. You can check
 the sensor hardware version using :func:`Get Sensor Hardware Version`.

The LIDAR-Lite sensor (hardware version 1) has five different modes. One mode is
for distance measurements and four modes are for velocity measurements with
different ranges.

The following modes are available:

* 0: Distance is measured with resolution 1.0 cm and range 0-4000 cm
* 1: Velocity is measured with resolution 0.1 m/s and range is 0-12.7 m/s
* 2: Velocity is measured with resolution 0.25 m/s and range is 0-31.75 m/s
* 3: Velocity is measured with resolution 0.5 m/s and range is 0-63.5 m/s
* 4: Velocity is measured with resolution 1.0 m/s and range is 0-127 m/s
""",
'de':
"""
.. note::
 Diese Funktion ist nur verfügbar, wenn ein LIDAR-Lite Sensor mit Hardware
 Version 1 verbaut ist. Für Hardware Version 3 gibt es :func:`Set Configuration`.
 die Hardware Version des Sensors kann mittels :func:`Get Sensor Hardware Version`
 abgefragt werden.

Der LIDAR-Lite Sensor (Hardware Version 1) hat fünf verschiedene Modi. Ein Modus
ist für Distanzmessungen und vier Modi sind für Geschwindigkeitsmessungen
mit unterschiedlichen Wertebereichen.

Die folgenden Modi können genutzt werden:

* 0: Distanz wird gemessen mit Auflösung 1,0 cm und Wertebereich 0-4000 cm
* 1: Geschwindigkeit wird gemessen mit Auflösung 0,1 m/s und Wertebereich 0-12,7 m/s
* 2: Geschwindigkeit wird gemessen mit Auflösung 0,25 m/s und Wertebereich 0-31,75 m/s
* 3: Geschwindigkeit wird gemessen mit Auflösung 0,5 m/s und Wertebereich 0-63,5 m/s
* 4: Geschwindigkeit wird gemessen mit Auflösung 1,0 m/s und Wertebereich 0-127 m/s
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Mode',
'elements': [('Mode', 'uint8', 1, 'out', {'constant_group': 'Mode', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the mode as set by :func:`Set Mode`.
""",
'de':
"""
Gibt den Modus zurück, wie von :func:`Set Mode` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Enable Laser',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Activates the laser of the LIDAR.

We recommend that you wait 250ms after enabling the laser before
the first call of :func:`Get Distance` to ensure stable measurements.
""",
'de':
"""
Aktiviert den Laser des LIDAR.

Wir empfehlen nach dem aktivieren des Lasers 250ms zu warten bis zum
ersten Aufruf von :func:`Get Distance` um stabile Messwerte zu garantieren.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Disable Laser',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Deactivates the laser of the LIDAR.
""",
'de':
"""
Deaktiviert den Laser des LIDAR.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is Laser Enabled',
'elements': [('Laser Enabled', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns *true* if the laser is enabled, *false* otherwise.
""",
'de':
"""
Gibt *true* zurück wenn der Laser aktiviert ist, *false* sonst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Distance',
'elements': [('Distance', 'uint16', 1, 'out', {'scale': (1, 100), 'unit': 'Meter', 'range': (0, 4000)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Distance Callback Period`. The :word:`parameter` is the distance
value of the sensor.

The :cb:`Distance` callback is only triggered if the distance value has changed
since the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Distance Callback Period`,
ausgelöst. Der :word:`parameter` ist die Entfernungswert des Sensors.

Der :cb:`Distance` Callback wird nur ausgelöst, wenn sich der Entfernungswert
seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Velocity',
'elements': [('Velocity', 'int16', 1, 'out', {'scale': (1, 100), 'unit': 'Meter Per Second', 'range': (-12800, 12700)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set Velocity Callback Period`. The :word:`parameter` is the velocity
value of the sensor.

The :cb:`Velocity` callback is only triggered if the velocity has changed since
the last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set Velocity Callback Period`,
ausgelöst. Der :word:`parameter` ist die Geschwindigkeit des Sensors.

Der :cb:`Velocity` Callback wird nur ausgelöst, wenn sich der
Geschwindigkeitswert seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Distance Reached',
'elements': [('Distance', 'uint16', 1, 'out', {'scale': (1, 100), 'unit': 'Meter', 'range': (0, 4000)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Distance Callback Threshold` is reached.
The :word:`parameter` is the distance value of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Distance Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist der Entfernungswert des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Velocity Reached',
'elements': [('Velocity', 'int16', 1, 'out', {'scale': (1, 100), 'unit': 'Meter Per Second', 'range': (-12800, 12700)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`Set Velocity Callback Threshold` is reached.
The :word:`parameter` is the velocity value of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`Set Debounce Period`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Schwellwert, wie von
:func:`Set Velocity Callback Threshold` gesetzt, erreicht wird.
Der :word:`parameter` ist der Geschwindigkeitswert des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`Set Debounce Period` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Sensor Hardware Version',
'elements': [('Version', 'uint8', 1, 'out', {'constant_group': 'Version'})],
'since_firmware': [2, 0, 3],
'doc': ['af', {
'en':
"""
Returns the LIDAR-Lite hardware version.
""",
'de':
"""
Gibt die LIDAR-Lite Hardware version zurück.
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
'since_firmware': [2, 0, 3],
'doc': ['bf', {
'en':
"""
.. note::
 This function is only available if you have a LIDAR-Lite sensor with hardware
 version 3. Use :func:`Set Mode` for hardware version 1. You can check
 the sensor hardware version using :func:`Get Sensor Hardware Version`.

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
""",
'de':
"""
.. note::
 Diese Funktion ist nur verfügbar, wenn ein LIDAR-Lite Sensor mit Hardware
 Version 3 verbaut ist. Für Hardware Version 1 gibt es :func:`Set Mode`.
 Die Hardware Version des Sensors kann mittels :func:`Get Sensor Hardware Version`
 abgefragt werden.

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
'since_firmware': [2, 0, 3],
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
'functions': [('setter', 'Enable Laser', [], 'Turn laser on and wait 250ms for very first measurement to be ready', None),
              ('sleep', 250, None, None),
              ('getter', ('Get Distance', 'distance'), [(('Distance', 'Distance'), 'uint16', 1, None, 'cm', None)], [])],
'cleanups': [('setter', 'Disable Laser', [], None, 'Turn laser off')]
})

com['examples'].append({
'name': 'Callback',
'functions': [('setter', 'Enable Laser', [], 'Turn laser on and wait 250ms for very first measurement to be ready', None),
              ('sleep', 250, None, None),
              ('callback', ('Distance', 'distance'), [(('Distance', 'Distance'), 'uint16', 1, None, 'cm', None)], None, None),
              ('callback_period', ('Distance', 'distance'), [], 200)],
'cleanups': [('setter', 'Disable Laser', [], None, 'Turn laser off')]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('setter', 'Enable Laser', [], 'Turn laser on and wait 250ms for very first measurement to be ready', None),
              ('sleep', 250, None, None),
              ('debounce_period', 10000),
              ('callback', ('Distance Reached', 'distance reached'), [(('Distance', 'Distance'), 'uint16', 1, None, 'cm', None)], None, None),
              ('callback_threshold', ('Distance', 'distance'), [], '>', [(20, 0)])],
'cleanups': [('setter', 'Disable Laser', [], None, 'Turn laser off')]
})

distance_channel = oh_generic_old_style_channel('Distance', 'Distance')
distance_channel['predicate'] = 'this.getSensorHardwareVersion() == 3 || cfg.mode == 0'

velocity_channel = oh_generic_old_style_channel('Velocity', 'Velocity', cast_literal='(short)')
velocity_channel['predicate'] = 'this.getSensorHardwareVersion() == 3 || cfg.mode != 0'

com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.OnOffType'],
    'params': [{
            'packet': 'Set Moving Average',
            'element': 'Distance Average Length',

            'name': 'Distance Moving Average Length',
            'type': 'integer',
            'label': 'Distance Moving Average Length',
            'groupName': 'average'
        }, {
            'packet': 'Set Moving Average',
            'element': 'Velocity Average Length',

            'name': 'Velocity Moving Average Length',
            'type': 'integer',
            'label': 'Velocity Moving Average Length',
            'groupName': 'average'
        }, {
            'packet': 'Set Mode',
            'element': 'Mode',

            'name': 'Mode',
            'type': 'integer',
            'options': [('Distance', 0),
                        ('Velocity Max 13m/s', 1),
                        ('Velocity Max 32m/s', 2),
                        ('Velocity Max 64m/s', 3),
                        ('Velocity Max 127m/s', 4)],
            'limit_to_options': 'true',
            'label': 'Mode',
            'description': 'The LIDAR-Lite sensor (hardware version 1) has five different modes. One mode is for distance measurements and four modes are for velocity measurements with different ranges.<br/><br/>The following modes are available:<br/><ul><li>0: Distance is measured with resolution 1.0 cm and range 0-400 cm</li><li>1: Velocity is measured with resolution 0.1 m/s and range is 0-12.7 m/s</li><li>2: Velocity is measured with resolution 0.25 m/s and range is 0-31.75 m/s</li><li>3: Velocity is measured with resolution 0.5 m/s and range is 0-63.5 m/s</li><li>4: Velocity is measured with resolution 1.0 m/s and range is 0-127 m/s</li></ul>This setting will be ignored if you have a LIDAR-Lite sensor with hardware version 3.',
            'groupName': 'sensor1'
        }, {
            'packet': 'Set Configuration',
            'element': 'Acquisition Count',

            'name': 'Acquisition Count',
            'type': 'integer',
            'label': 'Acquisition Count',
            'description': 'The Acquisition Count defines the number of times the Laser Range Finder Bricklet will integrate acquisitions to find a correlation record peak. With a higher count, the Bricklet can measure longer distances. With a lower count, the rate increases. This setting will be ignored if you have a LIDAR-Lite sensor with hardware version 1.',
            'groupName': 'sensor3'
        }, {
            'packet': 'Set Configuration',
            'element': 'Enable Quick Termination',


            'name': 'Enable Quick Termination',
            'type': 'boolean',

            'label': 'Enable Quick Termination',
            'description': 'If you enable Quick Termination, the distance measurement will be terminated early if a high peak was already detected. This means that a higher measurement rate can be achieved and long distances can be measured at the same time. However, the chance of false-positive distance measurements increases. This setting will be ignored if you have a LIDAR-Lite sensor with hardware version 1.',
            'groupName': 'sensor3'
        }, {
            'packet': 'Set Configuration',
            'element': 'Threshold Value',

            'name': 'Threshold Value',
            'type': 'integer',
            'label': 'Threshold Value',
            'description': 'Normally the distance is calculated with a detection algorithm that uses peak value, signal strength and noise. You can however also define a fixed Threshold Value. Set this to a low value if you want to measure the distance to something that has very little reflection (e.g. glass) and set it to a high value if you want to measure the distance to something with a very high reflection (e.g. mirror). Set this to 0 to use the default algorithm. This setting will be ignored if you have a LIDAR-Lite sensor with hardware version 1.',
            'groupName': 'sensor3'
        }, {
            'virtual': True,
            'name': 'Enable Fixed Measurement Frequency',
            'type': 'boolean',
            'default': 'false',

            'label': 'Enable Fixed Measurement Frequency',
            'description': 'For a stable velocity measurement you should set a fixed measurement frequency. See Measurement Frequency for details. This setting will be ignored if you have a LIDAR-Lite sensor with hardware version 1.',
            'groupName': 'sensor3'
        }, {
            'packet': 'Set Configuration',
            'element': 'Measurement Frequency',

            'name': 'Measurement Frequency',
            'type': 'integer',
            'min': 10, # Disallow 0 intentionally: controlled by "enable fixed measurement frequency"
            'default': 10, # Disallow 0 intentionally: controlled by "enable fixed measurement frequency"

            'label': 'Measurement Frequency',
            'description': 'Set the Measurement Frequency in Hz to force a fixed measurement rate. If set to 0, the Laser Range Finder Bricklet will use the optimal frequency according to the other configurations and the actual measured distance. Since the rate is not fixed in this case, the velocity measurement is not stable. For a stable velocity measurement you should set a fixed measurement frequency. The lower the frequency, the higher is the resolution of the calculated velocity. The allowed values are 10Hz-500Hz. This setting will be ignored if you have a LIDAR-Lite sensor with hardware version 1.',
            'groupName': 'sensor3'
        }],
    'param_groups': oh_generic_channel_param_groups() + [{
            'name': 'average',
            'label': 'Averaging',
            'description': 'Sets the different averaging parameters. It is possible to set the length of a normal averaging for the temperature and pressure, as well as an additional length of a moving average for the pressure. The moving average is calculated from the normal averages. There is no moving average for the temperature.<br/><br/>The maximum length for the pressure average is 10, for the temperature average is 255 and for the moving average is 25.<br/><br/>Setting the all three parameters to 0 will turn the averaging completely off. If the averaging is off, there is lots of noise on the data, but the data is without delay. Thus we recommend to turn the averaging off if the Barometer Bricklet data is to be used for sensor fusion with other sensors.<br/><br/>The default values are 10 for the normal averages and 25 for the moving average.',
            'advanced': 'true'
        }, {
            'name': 'sensor1',
            'label': 'Sensor Version 1',
            'description': 'Configuration for LIDAR-Lite sensors with hardware version 1',
        }, {
            'name': 'sensor3',
            'label': 'Sensor Version 3',
            'description': 'Configuration for LIDAR-Lite sensors with hardware version 3',
        }
    ],
    'init_code': """if(this.getSensorHardwareVersion() == 1) {{
        this.setMode(cfg.mode.shortValue());
    }} else {{
        this.setConfiguration(cfg.acquisitionCount.shortValue(), cfg.enableQuickTermination, cfg.thresholdValue.shortValue(), cfg.enableFixedMeasurementFrequency ? cfg.measurementFrequency : 0);
    }}
    this.setMovingAverage(cfg.distanceMovingAverageLength.shortValue(), cfg.velocityMovingAverageLength.shortValue());""",
    'channels': [
        distance_channel,
        velocity_channel,
        {
            'id': 'Enable Laser',
            'type': 'Enable Laser',

            'setters': [{
                    'predicate': 'cmd == OnOffType.ON',
                    'packet': 'Enable Laser',
                    'command_type': "OnOffType",
                }, {
                    'predicate': 'cmd == OnOffType.OFF',
                    'packet': 'Disable Laser',
                    'command_type': "OnOffType",
                }],


            'getters': [{
                'packet': 'Is Laser Enabled',
                'element': 'Laser Enabled',
                'transform': 'value? OnOffType.ON : OnOffType.OFF'}]
        }
    ],
    'channel_types': [
        oh_generic_channel_type('Distance', 'Number', 'Distance',
                    update_style='Callback Period',
                    description='The measured distance. Sensor hardware version 1 cannot measure distance and velocity at the same time. Therefore, the distance mode has to be enabled. Sensor hardware version 3 can measure distance and velocity at the same time. Also the laser has to be enabled.',
                    read_only=True,
                    pattern='%.2f %unit%',
                    min_=0,
                    max_=40),
        oh_generic_channel_type('Velocity', 'Number', 'Velocity',
                    update_style='Callback Period',
                    description='The measured velocity. Sensor hardware version 1 cannot measure distance and velocity at the same time. Therefore, the velocity mode has to be enabled. Sensor hardware version 3 can measure distance and velocity at the same time, but the velocity measurement only produces stables results if a fixed measurement rateis configured. Also the laser has to be enabled.',
                    read_only=True,
                    pattern='%.2f %unit%',
                    min_=-128,
                    max_=127),
        oh_generic_channel_type('Enable Laser', 'Switch', 'Enable Laser',
                    update_style=None,
                    description='Activates the laser of the LIDAR.'),
    ],
    'actions': ['Get Distance', 'Get Velocity', 'Get Mode',
                {'fn': 'Enable Laser', 'refreshs': ['Enable Laser']}, {'fn': 'Disable Laser', 'refreshs': ['Enable Laser']}, 'Is Laser Enabled',
                'Get Configuration', 'Get Moving Average', 'Get Sensor Hardware Version']
}

