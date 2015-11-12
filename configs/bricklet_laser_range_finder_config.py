# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Laser Range Finder Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 255,
    'name': ('LaserRangeFinder', 'laser_range_finder', 'Laser Range Finder', 'Laser Range Finder Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures distance up to 40m with laser light',
        'de': 'Misst Entfernung bis zu 40m mit Laser-Licht'
    },
    'released': True,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': ('GetDistance', 'get_distance'), 
'elements': [('distance', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the measured distance. The value has a range of 0 to 4000
and is given in cm.

The Laser Range Finder Bricklet knows different modes. Distances
are only measured in the distance measurement mode,
see :func:`SetMode`. Also the laser has to be enabled, see
:func:`EnableLaser`.

If you want to get the distance periodically, it is recommended to
use the callback :func:`Distance` and set the period with 
:func:`SetDistanceCallbackPeriod`.
""",
'de':
"""
Gibt die gemessene Distanz zurück. Der Wertebereich ist 0 bis 4000
und die Werte haben die Einheit cm.

Das Laser Range Finder Bricklet kennt verschiedene Modi. Eine Distanz
wird nur im Distanzmodus gemessen, siehe :func:`SetMode`. Zusätzlich
muss der Laser aktiviert werden, siehe :func:`EnableLaser`.

Wenn der Entfernungswert periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`Distance` zu nutzen und die Periode mit 
:func:`SetDistanceCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetVelocity', 'get_velocity'), 
'elements': [('velocity', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the measured velocity. The value has a range of 0 to 12700
and is given in 1/100 m/s.

The Laser Range Finder Bricklet knows different modes. Velocity 
is only measured in the velocity measurement modes, 
see :func:`SetMode`. Also the laser has to be enabled, see
:func:`EnableLaser`.

If you want to get the velocity periodically, it is recommended to
use the callback :func:`Velocity` and set the period with 
:func:`SetVelocityCallbackPeriod`.
""",
'de':
"""
Gibt die gemessene Geschwindigkeit zurück. Der Wertebereich ist 0 bis 12700
und die Werte haben die Einheit 1/100 m/s.

Das Laser Range Finder Bricklet kennt verschiedene Modi. Eine Geschwindigkeit
wird nur in den Geschwindigkeitsmodi gemessen, siehe :func:`SetMode`. Zusätzlich
muss der Laser aktiviert werden, siehe :func:`EnableLaser`.

Wenn der Geschwindigkeitswert periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`Velocity` zu nutzen und die Periode mit 
:func:`SetVelocityCallbackPeriod` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetDistanceCallbackPeriod', 'set_distance_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Distance` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Distance` is only triggered if the distance value has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Distance` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Distance` wird nur ausgelöst wenn sich der Entfernungswert seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetDistanceCallbackPeriod', 'get_distance_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetDistanceCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetDistanceCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetVelocityCallbackPeriod', 'set_velocity_callback_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Velocity` callback is triggered
periodically. A value of 0 turns the callback off.

:func:`Velocity` is only triggered if the velocity value has changed since the
last triggering.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Velocity` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

:func:`Velocity` wird nur ausgelöst wenn sich der Geschwindigkeitswert seit der
letzten Auslösung geändert hat.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetVelocityCallbackPeriod', 'get_velocity_callback_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetVelocityCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetVelocityCallbackPeriod`
gesetzt.
"""
}]
})


com['packets'].append({
'type': 'function',
'name': ('SetDistanceCallbackThreshold', 'set_distance_callback_threshold'), 
'elements': [('option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('min', 'uint16', 1, 'in'),
             ('max', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`DistanceReached` callback. 

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
Setzt den Schwellwert für den :func:`DistanceReached` Callback.

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
'name': ('GetDistanceCallbackThreshold', 'get_distance_callback_threshold'), 
'elements': [('option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('min', 'uint16', 1, 'out'),
             ('max', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`SetDistanceCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetDistanceCallbackThreshold`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetVelocityCallbackThreshold', 'set_velocity_callback_threshold'), 
'elements': [('option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('min', 'int16', 1, 'in'),
             ('max', 'int16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the thresholds for the :func:`VelocityReached` callback. 

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
Setzt den Schwellwert für den :func:`VelocityReached` Callback.

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
'name': ('GetVelocityCallbackThreshold', 'get_velocity_callback_threshold'), 
'elements': [('option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('min', 'int16', 1, 'out'),
             ('max', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the threshold as set by :func:`SetVelocityCallbackThreshold`.
""",
'de':
"""
Gibt den Schwellwert zurück, wie von :func:`SetVelocityCallbackThreshold`
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

* :func:`DistanceReached`,
* :func:`VelocityReached`,

are triggered, if the thresholds

* :func:`SetDistanceCallbackThreshold`,
* :func:`SetVelocityCallbackThreshold`,

keep being reached.

The default value is 100.
""",
'de':
"""
Setzt die Periode in ms mit welcher die Schwellwert Callbacks

* :func:`DistanceReached`,
* :func:`VelocityReached`,
 
ausgelöst werden, wenn die Schwellwerte 

* :func:`SetDistanceCallbackThreshold`,
* :func:`SetVelocityCallbackThreshold`,
 
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
'name': ('SetMovingAverage', 'set_moving_average'), 
'elements': [('distance_average_length', 'uint8', 1, 'in'),
             ('velocity_average_length', 'uint8', 1, 'in')],
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
'name': ('GetMovingAverage', 'get_moving_average'), 
'elements': [('distance_average_length', 'uint8', 1, 'out'),
             ('velocity_average_length', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the length moving average as set by :func:`SetMovingAverage`.
""",
'de':
"""
Gibt die Länge des gleitenden Mittelwerts zurück, wie von 
:func:`SetMovingAverage` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetMode', 'set_mode'), 
'elements': [('mode', 'uint8', 1, 'in', ('Mode', 'mode', [('Distance', 'distance', 0),
                                                          ('VelocityMax13ms', 'velocity_max_13ms', 1),
                                                          ('VelocityMax32ms', 'velocity_max_32ms', 2),
                                                          ('VelocityMax64ms', 'velocity_max_64ms', 3),
                                                          ('VelocityMax127ms', 'velocity_max_127ms', 4)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
The LIDAR has five different modes. One mode is for distance
measurements and four modes are for velocity measurements with
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
Das LIDAR hat fünf verschiedene Modi. Ein Modus ist für
Distanzmessungen und vier Modi sind für Geschwindigkeitsmessungen
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
'name': ('GetMode', 'get_mode'), 
'elements': [('mode', 'uint8', 1, 'out', ('Mode', 'mode', [('Distance', 'distance', 0),
                                                           ('VelocityMax13ms', 'velocity_max_13ms', 1),
                                                           ('VelocityMax32ms', 'velocity_max_32ms', 2),
                                                           ('VelocityMax64ms', 'velocity_max_64ms', 3),
                                                           ('VelocityMax127ms', 'velocity_max_127ms', 4)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the mode as set by :func:`SetMode`.
""",
'de':
"""
Gibt den Modus zurück, wie von :func:`SetMode` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('EnableLaser', 'enable_laser'), 
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Activates the laser of the LIDAR.

We recommend that you wait 250ms after enabling the laser before
the first call of :func:`GetDistance` to ensure stable measurements.
""",
'de':
"""
Aktiviert den Laser des LIDAR.

Wir empfehlen nach dem aktivieren des Lasers 250ms zu warten bis zum
ersten Aufruf von :func:`GetDistance` um stabile Messwerte zu garantieren.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('DisableLaser', 'disable_laser'), 
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
'name': ('IsLaserEnabled', 'is_laser_enabled'), 
'elements': [('laser_enabled', 'bool', 1, 'out')],
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
'name': ('Distance', 'distance'), 
'elements': [('distance', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetDistanceCallbackPeriod`. The :word:`parameter` is the distance value
of the sensor.

:func:`Distance` is only triggered if the distance value has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetDistanceCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die Entfernungswert des Sensors.

:func:`Distance` wird nur ausgelöst wenn sich der Entfernungswert seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('Velocity', 'velocity'), 
'elements': [('velocity', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetVelocityCallbackPeriod`. The :word:`parameter` is the velocity value
of the sensor.

:func:`Velocity` is only triggered if the velocity has changed since the
last triggering.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetVelocityCallbackPeriod`,
ausgelöst. Der :word:`parameter` ist die Geschwindigkeit des Sensors.

:func:`Velocity` wird nur ausgelöst wenn sich der Geschwindigkeitswert seit der
letzten Auslösung geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('DistanceReached', 'distance_reached'), 
'elements': [('distance', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetDistanceCallbackThreshold` is reached.
The :word:`parameter` is the distance value of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetDistanceCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist der Entfernungswert des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('VelocityReached', 'velocity_reached'), 
'elements': [('velocity', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the threshold as set by
:func:`SetVelocityCallbackThreshold` is reached.
The :word:`parameter` is the velocity value of the sensor.

If the threshold keeps being reached, the callback is triggered periodically
with the period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Schwellwert, wie von 
:func:`SetVelocityCallbackThreshold` gesetzt, erreicht wird.
Der :word:`parameter` ist der Geschwindigkeitswert des Sensors.

Wenn der Schwellwert erreicht bleibt, wird der Callback mit der Periode, wie
mit :func:`SetDebouncePeriod` gesetzt, ausgelöst.
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
