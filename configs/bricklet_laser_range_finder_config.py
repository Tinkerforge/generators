# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Laser Range Finder Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS

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
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Get Distance',
'elements': [('Distance', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the measured distance. The value has a range of 0 to 4000
and is given in cm.

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
Gibt die gemessene Distanz zurück. Der Wertebereich ist 0 bis 4000
und die Werte haben die Einheit cm.

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
'elements': [('Velocity', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the measured velocity. The value has a range of -12800 to 12700
and is given in 1/100 m/s.

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
Gibt die gemessene Geschwindigkeit zurück. Der Wertebereich ist -12800 bis 12700
und die Werte haben die Einheit 1/100 m/s.

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
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :cb:`Distance` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Distance` callback is only triggered if the distance value has
changed since the last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :cb:`Distance` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Distance` Callback wird nur ausgelöst wenn sich der Entfernungswert
seit der letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Distance Callback Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Distance Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Distance Callback Period`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Velocity Callback Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :cb:`Velocity` callback is triggered
periodically. A value of 0 turns the callback off.

The :cb:`Velocity` callback is only triggered if the velocity value has
changed since the last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :cb:`Velocity` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der :cb:`Velocity` Callback wird nur ausgelöst wenn sich der
Geschwindigkeitswert seit der letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Velocity Callback Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Velocity Callback Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Velocity Callback Period`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Distance Callback Threshold',
'elements': [('Option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint16', 1, 'in'),
             ('Max', 'uint16', 1, 'in')],
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

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Distance Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn der Entfernungswert *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn der Entfernungswert *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn der Entfernungswert kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn der Entfernungswert größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Distance Callback Threshold',
'elements': [('Option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint16', 1, 'out'),
             ('Max', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Distance Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Distance Callback Threshold`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Velocity Callback Threshold',
'elements': [('Option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'int16', 1, 'in'),
             ('Max', 'int16', 1, 'in')],
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

The default value is ('x', 0, 0).
""",
'de':
"""
Setzt den Schwellwert für den :cb:`Velocity Reached` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100
 
 "'x'",    "Callback ist inaktiv"
 "'o'",    "Callback wird ausgelöst wenn der Geschwindigkeitswert *außerhalb* des min und max Wertes ist"
 "'i'",    "Callback wird ausgelöst wenn der Geschwindigkeitswert *innerhalb* des min und max Wertes ist"
 "'<'",    "Callback wird ausgelöst wenn der Geschwindigkeitswert kleiner als der min Wert ist (max wird ignoriert)"
 "'>'",    "Callback wird ausgelöst wenn der Geschwindigkeitswert größer als der min Wert ist (max wird ignoriert)"
 
Der Standardwert ist ('x', 0, 0).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Velocity Callback Threshold',
'elements': [('Option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'int16', 1, 'out'),
             ('Max', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`Set Velocity Callback Threshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`Set Velocity Callback Threshold`
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

* :cb:`Distance Reached`,
* :cb:`Velocity Reached`,

are triggered, if the thresholds

* :func:`Set Distance Callback Threshold`,
* :func:`Set Velocity Callback Threshold`,

keep being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callbacks

* :cb:`Distance Reached`,
* :cb:`Velocity Reached`,
 
ausgelöst werden, wenn die Schwellwerte 

* :func:`Set Distance Callback Threshold`,
* :func:`Set Velocity Callback Threshold`,
 
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
'name': 'Set Moving Average',
'elements': [('Distance Average Length', 'uint8', 1, 'in'),
             ('Velocity Average Length', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
for the distance and velocity.

Setting the length to 0 will turn the averaging completely off. With less
averaging, there is more noise on the data.

The range for the averaging is 0-30.

The default value is 10.
""",
'de':
"""
Setzt die Länge eines `gleitenden Mittelwerts <https://de.wikipedia.org/wiki/Gleitender_Mittelwert>`__
für die Entfernung und Geschwindigkeit.

Wenn die Länge auf 0 gesetzt wird, ist das Averaging komplett aus. Desto kleiner
die Länge des Mittelwerts ist, desto mehr Rauschen ist auf den Daten.

Der Wertebereich liegt bei 0-30.

Der Standardwert ist 10.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Moving Average',
'elements': [('Distance Average Length', 'uint8', 1, 'out'),
             ('Velocity Average Length', 'uint8', 1, 'out')],
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
'elements': [('Mode', 'uint8', 1, 'in', ('Mode', [('Distance', 0),
                                                  ('Velocity Max 13ms', 1),
                                                  ('Velocity Max 32ms', 2),
                                                  ('Velocity Max 64ms', 3),
                                                  ('Velocity Max 127ms', 4)]))],
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

* 0: Distance is measured with resolution 1.0 cm and range 0-400 cm
* 1: Velocity is measured with resolution 0.1 m/s and range is 0-12.7 m/s
* 2: Velocity is measured with resolution 0.25 m/s and range is 0-31.75 m/s
* 3: Velocity is measured with resolution 0.5 m/s and range is 0-63.5 m/s
* 4: Velocity is measured with resolution 1.0 m/s and range is 0-127 m/s

The default mode is 0 (distance is measured).
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

* 0: Distanz wird gemessen mit Auflösung 1,0 cm und Wertebereich 0-400 cm
* 1: Geschwindigkeit wird gemessen mit Auflösung 0,1 m/s und Wertebereich 0-12,7 m/s
* 2: Geschwindigkeit wird gemessen mit Auflösung 0,25 m/s und Wertebereich 0-31,75 m/s
* 3: Geschwindigkeit wird gemessen mit Auflösung 0,5 m/s und Wertebereich 0-63,5 m/s
* 4: Geschwindigkeit wird gemessen mit Auflösung 1,0 m/s und Wertebereich 0-127 m/s

Der Standardmodus ist 0 (Distanzmessung).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Mode',
'elements': [('Mode', 'uint8', 1, 'out', ('Mode', [('Distance', 0),
                                                   ('Velocity Max 13ms', 1),
                                                   ('Velocity Max 32ms', 2),
                                                   ('Velocity Max 64ms', 3),
                                                   ('Velocity Max 127ms', 4)]))],
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
'elements': [('Laser Enabled', 'bool', 1, 'out')],
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
'elements': [('Distance', 'uint16', 1, 'out')],
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

Der :cb:`Distance` Callback wird nur ausgelöst wenn sich der Entfernungswert
seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Velocity',
'elements': [('Velocity', 'int16', 1, 'out')],
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

Der :cb:`Velocity` Callback wird nur ausgelöst wenn sich der
Geschwindigkeitswert seit der letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Distance Reached',
'elements': [('Distance', 'uint16', 1, 'out')],
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
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
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
'elements': [('Velocity', 'int16', 1, 'out')],
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
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
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
'elements': [('Version', 'uint8', 1, 'out', ('Version', [('1', 1),
                                                         ('3', 3)]))],
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
'elements': [('Acquisition Count', 'uint8', 1, 'in'),
             ('Enable Quick Termination', 'bool', 1, 'in'),
             ('Threshold Value', 'uint8', 1, 'in'),
             ('Measurement Frequency', 'uint16', 1, 'in')],
'since_firmware': [2, 0, 3],
'doc': ['bf', {
'en':
"""
.. note::
 This function is only available if you have a LIDAR-Lite sensor with hardware
 version 3. Use :func:`Set Mode` for hardware version 1. You can check
 the sensor hardware version using :func:`Get Sensor Hardware Version`.

The **Aquisition Count** defines the number of times the Laser Range Finder Bricklet
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

Set the **Measurement Frequency** in Hz to force a fixed measurement rate. If set to 0,
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
.. note::
 Diese Funktion ist nur verfügbar, wenn ein LIDAR-Lite Sensor mit Hardware
 Version 3 verbaut ist. Für Hardware Version 1 gibt es :func:`Set Mode`.
 Die Hardware Version des Sensors kann mittels :func:`Get Sensor Hardware Version`
 abgefragt werden.

Der Parameter **Aquisition Count** definiert die Anzahl der Datenerfassungen die integriert
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

Der **Measurement Frequency** Parameter wird in Hz gesetzt. Er erzwingt eine feste Messfrequenz.
Wenn der Wert auf 0 gesetzt wird, nutzt das Laser Range Finder Bricklet die optimale Frequenz je nach
Konfiguration und aktuell gemessener Distanz. Da die Messrate in diesem Fall nicht fest ist, ist die
Geschwindigkeitsmessung nicht stabil. Für eine stabile Geschwindigkeitsmessung sollte eine feste
Messfrequenz eingestellt werden. Desto niedriger die Frequenz ist, desto größer ist die Auflösung
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
'elements': [('Acquisition Count', 'uint8', 1, 'out'),
             ('Enable Quick Termination', 'bool', 1, 'out'),
             ('Threshold Value', 'uint8', 1, 'out'),
             ('Measurement Frequency', 'uint16', 1, 'out')],
'since_firmware': [2, 0, 3],
'doc': ['bf', {
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

com['examples'].append({
'name': 'Simple',
'functions': [('setter', 'Enable Laser', [], 'Turn laser on and wait 250ms for very first measurement to be ready', None),
              ('sleep', 250, None, None),
              ('getter', ('Get Distance', 'distance'), [(('Distance', 'Distance'), 'uint16', None, 'cm', 'cm', None)], [])],
'cleanups': [('setter', 'Disable Laser', [], None, 'Turn laser off')]
})

com['examples'].append({
'name': 'Callback',
'functions': [('setter', 'Enable Laser', [], 'Turn laser on and wait 250ms for very first measurement to be ready', None),
              ('sleep', 250, None, None),
              ('callback', ('Distance', 'distance'), [(('Distance', 'Distance'), 'uint16', None, 'cm', 'cm', None)], None, None),
              ('callback_period', ('Distance', 'distance'), [], 200)],
'cleanups': [('setter', 'Disable Laser', [], None, 'Turn laser off')]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('setter', 'Enable Laser', [], 'Turn laser on and wait 250ms for very first measurement to be ready', None),
              ('sleep', 250, None, None),
              ('debounce_period', 10000),
              ('callback', ('Distance Reached', 'distance reached'), [(('Distance', 'Distance'), 'uint16', None, 'cm', 'cm', None)], None, None),
              ('callback_threshold', ('Distance', 'distance'), [], '>', [(20, 0)])],
'cleanups': [('setter', 'Disable Laser', [], None, 'Turn laser off')]
})
