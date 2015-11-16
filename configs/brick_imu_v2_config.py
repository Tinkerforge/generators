# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# IMU Brick 2.0 communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Brick',
    'device_identifier': 18,
    'name': ('IMU V2', 'IMU 2.0', 'IMU Brick 2.0'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Full fledged AHRS with 9 degrees of freedom',
        'de': 'Voll ausgestattetes AHRS mit 9 Freiheitsgraden'
    },
    'released': True,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Get Acceleration',
'elements': [('X', 'int16', 1, 'out'),
             ('Y', 'int16', 1, 'out'),
             ('Z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
""" 
Returns the calibrated acceleration from the accelerometer for the 
x, y and z axis in 1/100 m/s².

If you want to get the acceleration periodically, it is recommended 
to use the callback :func:`Acceleration` and set the period with 
:func:`SetAccelerationPeriod`.
""",
'de':
"""
Gibt die kalibrierten Beschleunigungen des Beschleunigungsmessers für die 
X-, Y- und Z-Achse in 1/100 m/s².

Wenn die Beschleunigungen periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`Acceleration` zu nutzen und die Periode mit :func:`SetAccelerationPeriod`
vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Magnetic Field',
'elements': [('X', 'int16', 1, 'out'),
             ('Y', 'int16', 1, 'out'),
             ('Z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the calibrated magnetic field from the magnetometer for the 
x, y and z axis in 1/16 µT (Microtesla).

If you want to get the magnetic field periodically, it is recommended 
to use the callback :func:`MagneticField` and set the period with 
:func:`SetMagneticFieldPeriod`.
""",
'de':
"""
Gibt das kalibrierte magnetische Feld des Magnetometers mit den X-, Y- und
Z-Komponenten in 1/16 µT zurück (Microtesla).

Wenn das magnetische Feld periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`MagneticField` zu nutzen und die Periode mit :func:`SetMagneticFieldPeriod`
vorzugeben.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Get Angular Velocity',
'elements': [('X', 'int16', 1, 'out'),
             ('Y', 'int16', 1, 'out'),
             ('Z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the calibrated angular velocity from the gyroscope for the 
x, y and z axis in 1/16 °/s.

If you want to get the angular velocity periodically, it is recommended 
to use the callback :func:`AngularVelocity` and set the period with 
:func:`SetAngularVelocityPeriod`.
""",
'de':
"""
Gibt die kalibrierte Winkelgeschwindigkeiten des Gyroskops für die X-, Y- und
Z-Achse in 1/16 °/s zurück.

Wenn die Winkelgeschwindigkeiten periodisch abgefragt werden sollen, wird empfohlen
den Callback :func:`AngularVelocity` zu nutzen und die Periode mit
:func:`SetAngularVelocityPeriod` vorzugeben.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Get Temperature',
'elements': [('Temperature', 'int8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the temperature of the IMU Brick. The temperature is given in 
°C. The temperature is measured in the core of the BNO055 IC, it is not the
ambient temperature
""",
'de':
"""
Gibt die Temperatur (in °C) des IMU Brick zurück. Die Temperatur wird im Kern
des BNO055 ICs gemessen, es handelt sich nicht um die Umgebungstemperatur.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Get Orientation',
'elements': [('Heading', 'int16', 1, 'out'),
             ('Roll', 'int16', 1, 'out'),
             ('Pitch', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current orientation (heading, roll, pitch) of the IMU Brick as
independent Euler angles in 1/16 degree. Note that Euler angles always
experience a `gimbal lock <https://en.wikipedia.org/wiki/Gimbal_lock>`__. We
recommend that you use quaternions instead, if you need the absolute orientation.

The rotation angle has the following ranges:

* heading: 0° to 360°
* roll: -90° to +90°
* pitch: -180° to +180°

If you want to get the orientation periodically, it is recommended 
to use the callback :func:`Orientation` and set the period with 
:func:`SetOrientationPeriod`.
""",
'de':
"""
Gibt die aktuelle Orientierung (Gier-, Roll-, Nickwinkel) des IMU Brick in
unabhängigen Eulerwinkeln (in 1/16 °) zurück. Zu beachten ist, dass Eulerwinkel
immer eine `kardanische Blockade <https://de.wikipedia.org/wiki/Gimbal_Lock>`__
erfahren. Wir empfehlen daher stattdessen Quaternionen zu verwenden, wenn die
absolute Lage im Raum bestimmt werden soll.

Die Rotationswinkel haben den folgenden Wertebereich:

* Gierwinkel: 0° bis 360°
* Rollwinkel: -90° bis +90°
* Nickwinkel: -180° bis +180°

Wenn die Orientierung periodisch abgefragt werden sollen, wird empfohlen den
Callback :func:`Orientation` zu nutzen und die Periode mit :func:`SetOrientationPeriod`
vorzugeben.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Get Linear Acceleration',
'elements': [('X', 'int16', 1, 'out'),
             ('Y', 'int16', 1, 'out'),
             ('Z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the linear acceleration of the IMU Brick for the
x, y and z axis in 1/100 m/s².

The linear acceleration is the acceleration in each of the three
axis of the IMU Brick with the influences of gravity removed.

It is also possible to get the gravity vector with the influence of linear
acceleration removed, see :func:`GetGravityVector`.

If you want to get the linear acceleration periodically, it is recommended 
to use the callback :func:`LinearAcceleration` and set the period with 
:func:`SetLinearAccelerationPeriod`.
""",
'de':
"""
Gibt die lineare Beschleunigungen des IMU Brick für die 
X-, Y- und Z-Achse in 1/100 m/s² zurück.

Die lineare Beschleunigung ist die Beschleunigung in jede der drei
Achsen. Der Einfluss von Erdbeschleunigung ist entfernt.

Es ist auch möglich einen Vektor der Erdbeschleunigung zu bekommen, siehe
:func:GetGravityVector`

Wenn die Beschleunigungen periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`LinearAcceleration` zu nutzen und die Periode mit 
:func:`SetLinearAccelerationPeriod` vorzugeben.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Get Gravity Vector',
'elements': [('X', 'int16', 1, 'out'),
             ('Y', 'int16', 1, 'out'),
             ('Z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current gravity vector of the IMU Brick for the
x, y and z axis in 1/100 m/s².

The gravity vector is the acceleration that occurs due to gravity.
Influences of additional linear acceleration are removed.

It is also possible to get the linear acceleration with the influence 
of gravity removed, see :func:`GetLinearAcceleration`.

If you want to get the gravity vector periodically, it is recommended 
to use the callback :func:`GravityVector` and set the period with 
:func:`SetGravityVectorPeriod`.
""",
'de':
"""
Gibt den Vektor der Erdbeschleunigung des IMU Brick für die 
X-, Y- und Z-Achse in 1/100 m/s² zurück.

Die Erdbeschleunigung ist die Beschleunigung die auf Grund von Schwerkraft
entsteht. Einflüsse von linearen Beschleunigungen sind entfernt.

Es ist auch möglich die lineare Beschleunigung zu bekommen, siehe
:func:GetLinearAcceleration`

Wenn die Erdbeschleunigungen periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`GravityVector` zu nutzen und die Periode mit 
:func:`SetGravityVectorPeriod` vorzugeben.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Get Quaternion',
'elements': [('W', 'int16', 1, 'out'),
             ('X', 'int16', 1, 'out'),
             ('Y', 'int16', 1, 'out'),
             ('Z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current orientation (w, x, y, z) of the IMU Brick as
`quaternions <https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation>`__.

You have to divide the returns values by 16383 (14 bit) to get
the usual range of -1.0 to +1.0 for quaternions.

If you want to get the quaternions periodically, it is recommended 
to use the callback :func:`Quaternion` and set the period with 
:func:`SetQuaternionPeriod`.
""",
'de':
"""
Gibt die aktuelle Orientierung (w, x, y, z) des IMU Brick als
`Quaterinonen <https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation>`__ zurück.

Die zurückgegebenen Werte müssen mit 16383 (14 Bit) dividiert werden um
in den üblichen Wertebereich für Quaternionen (-1,0 bis +1,0) gebracht zu werden.

Wenn die Quaternionen periodisch abgefragt werden sollen, wird empfohlen den
Callback :func:`Quaternion` zu nutzen und die Periode mit :func:`SetQuaternionPeriod`
vorzugeben.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Get All Data',
'elements': [('Acceleration', 'int16', 3, 'out'),
             ('Magnetic Field', 'int16', 3, 'out'),
             ('Angular Velocity', 'int16', 3, 'out'),
             ('Euler Angle', 'int16', 3, 'out'),
             ('Quaternion', 'int16', 4, 'out'),
             ('Linear Acceleration', 'int16', 3, 'out'),
             ('Gravity Vector', 'int16', 3, 'out'),
             ('Temperature', 'int8', 1, 'out'),
             ('Calibration Status', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Return all of the available data of the IMU Brick.

* acceleration in 1/100 m/s² (see :func:`GetAcceleration`)
* magnetic field in 1/16 µT (see :func:`GetMagneticField`)
* angular velocity in 1/16 °/s (see :func:`GetAngularVelocity`)
* Euler angles in 1/16 ° (see :func:`GetOrientation`)
* quaternion 1/16383 (see :func:`GetQuaternion`)
* linear acceleration 1/100 m/s² (see :func:`GetLinearAcceleration`)
* gravity vector 1/100 m/s² (see :func:`GetGravityVector`)
* temperature in 1 °C (see :func:`GetTemperature`)
* calibration status (see below)

The calibration status consists of four pairs of two bits. Each pair
of bits represents the status of the current calibration.

* bit 0-1: Magnetometer
* bit 2-3: Accelerometer
* bit 4-5: Gyroscope
* bit 6-7: System

A value of 0 means for "not calibrated" and a value of 3 means
"fully calibrated". In your program you should always be able to
ignore the calibration status, it is used by the calibration
window of the Brick Viewer and it can be ignored after the first
calibration. See the documentation in the calibration window for
more information regarding the calibration of the IMU Brick.

If you want to get the data periodically, it is recommended 
to use the callback :func:`AllData` and set the period with 
:func:`SetAllDataPeriod`.
""",
'de':
"""
Gibt alle Daten zurück die dem IMU Brick zur Verfügung stehen.

* Beschleunigung in 1/100 m/s² (see :func:`GetAcceleration`)
* Magnetfeld in 1/16 µT (see :func:`GetMagneticField`)
* Winkelgeschwindigkeit in 1/16 °/s (see :func:`GetAngularVelocity`)
* Eulerwinkel in 1/16 ° (see :func:`GetOrientation`)
* Quaternion 1/16383 (see :func:`GetQuaternion`)
* Lineare Beschleunigung 1/100 m/s² (see :func:`GetLinearAcceleration`)
* Erdbeschleunigungsvektor 1/100 m/s² (see :func:`GetGravityVector`)
* Temperatur in 1 °C (see :func:`GetTemperature`)
* Kalibrierungsstatus (siehe unten)

Der Kalibrierungsstatus besteht aus vier paaren von je zwei Bits. Jedes
Paar von Bits repräsentiert den Status der aktuellen Kalibrierung.

* Bit 0-1: Magnetometer
* Bit 2-3: Beschleunigungsmesser
* Bit 4-5: Gyroskop
* Bit 6-7: System

Ein Wert von 0 bedeutet "nicht kalibriert" und ein Wert von 3
bedeutet "vollständig kalibriert". Normalerweise kann der 
Kalibrierungsstatus vollständig ignoriert werden. Er wird vom
Brick Viewer im Kalibrierungsfenster benutzt und nur für die
initiale Kalibrierung benötigt. Mehr Information zur Kalibrierung
des IMU Bricks gibt es im Kalibrierungsfenster.

Wenn die Daten periodisch abgefragt werden sollen, wird empfohlen den
Callback :func:`AllData` zu nutzen und die Periode mit :func:`SetAllDataPeriod`
vorzugeben.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Leds On',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Turns the orientation and direction LEDs of the IMU Brick on.
""",
'de':
"""
Aktiviert die Orientierungs- und Richtungs-LEDs des IMU Brick.
"""
}] 
})
    
com['packets'].append({
'type': 'function',
'name': 'Leds Off',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Turns the orientation and direction LEDs of the IMU Brick off.
""",
'de':
"""
Deaktiviert die Orientierungs- und Richtungs-LEDs des IMU Brick.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Are Leds On',
'elements': [('Leds', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns *true* if the orientation and direction LEDs of the IMU Brick
are on, *false* otherwise.
""",
'de':
"""
Gibt zurück ob die Orientierungs- und Richtungs-LEDs des IMU Brick aktiv sind. 
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Save Calibration',
'elements': [('Calibration Done', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
A call of this function saves the current calibration to be used
as a starting point for the next restart of continuous calibration
of the IMU Brick.

A return value of *true* means that the calibration could be used and
*false* means that it could not be used (this happens if the calibration 
status is not "fully calibrated").

This function is used by the calibration window of the Brick Viewer, you
should not need to call it in your program.
""",
'de':
"""
Ein Aufruf dieser Funktion speichert die aktuelle Kalibrierung damit
sie beim nächsten Neustart des IMU Brick als Startpunkt für die
kontinuierliche Kalibrierung genutzt werden kann.

Ein Rückgabewert von *true* bedeutet das die Kalibrierung genutzt werden
konnte und *false* bedeutet das die Kalibrierung nicht genutzt werden
konnte (dies passiert wenn der Kalibrierungsstatus nicht "fully calibrated"
ist).

Diese Funktion wird vom Kalibrierungsfenster des Brick Viewer benutzt. Sie
sollte in einem normalen Benutzerprogramm nicht aufgerufen werden müssen.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Set Acceleration Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Acceleration` callback is triggered
periodically. A value of 0 turns the callback off.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Acceleration` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.

Der Standardwert ist 0.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Get Acceleration Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetAccelerationPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetAccelerationPeriod` gesetzt.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Set Magnetic Field Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`MagneticField` callback is triggered
periodically. A value of 0 turns the callback off.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`MagneticField` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Get Magnetic Field Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetMagneticFieldPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetMagneticFieldPeriod` gesetzt.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Set Angular Velocity Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`AngularVelocity` callback is triggered
periodically. A value of 0 turns the callback off.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`AngularVelocity` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Get Angular Velocity Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetAngularVelocityPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetAngularVelocityPeriod` gesetzt.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Set Temperature Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Temperature` callback is triggered
periodically. A value of 0 turns the callback off.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Temperature` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Get Temperature Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetTemperaturePeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetTemperaturePeriod` gesetzt.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Set Orientation Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Orientation` callback is triggered
periodically. A value of 0 turns the callback off.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Orientation` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Get Orientation Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetOrientationPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetOrientationPeriod` gesetzt.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Set Linear Acceleration Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`LinearAcceleration` callback is triggered
periodically. A value of 0 turns the callback off.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`LinearAcceleration` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Get Linear Acceleration Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetLinearAccelerationPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetLinearAccelerationPeriod` gesetzt.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Set Gravity Vector Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`GravityVector` callback is triggered
periodically. A value of 0 turns the callback off.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`GravityVector` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Get Gravity Vector Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetGravityVectorPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetGravityVectorPeriod` gesetzt.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Set Quaternion Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`Quaternion` callback is triggered
periodically. A value of 0 turns the callback off.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`Quaternion` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Get Quaternion Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetQuaternionPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetQuaternionPeriod` gesetzt.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Set All Data Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :func:`AllData` callback is triggered
periodically. A value of 0 turns the callback off.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`AllData` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': 'Get All Data Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetAllDataPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetAllDataPeriod` gesetzt.
"""
}] 
})

com['packets'].append({
'type': 'callback',
'name': 'Acceleration',
'elements': [('X', 'int16', 1, 'out'),
             ('Y', 'int16', 1, 'out'),
             ('Z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetAccelerationPeriod`. The :word:`parameters` are the acceleration
for the x, y and z axis.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetAccelerationPeriod`,
ausgelöst. Die :word:`parameters` sind die Beschleunigungen der X, Y und Z-Achse.
"""
}] 
})

com['packets'].append({
'type': 'callback',
'name': 'Magnetic Field',
'elements': [('X', 'int16', 1, 'out'),
             ('Y', 'int16', 1, 'out'),
             ('Z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetMagneticFieldPeriod`. The :word:`parameters` are the magnetic field
for the x, y and z axis.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetMagneticFieldPeriod`,
ausgelöst. Die :word:`parameters` sind die Magnetfeldkomponenten der X, Y und Z-Achse.
"""
}] 
})

com['packets'].append({
'type': 'callback',
'name': 'Angular Velocity',
'elements': [('X', 'int16', 1, 'out'),
             ('Y', 'int16', 1, 'out'),
             ('Z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetAngularVelocityPeriod`. The :word:`parameters` are the angular velocity
for the x, y and z axis.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetAngularVelocityPeriod`,
ausgelöst. Die :word:`parameters` sind die Winkelgeschwindigkeiten der X, Y und Z-Achse.
"""
}] 
})

com['packets'].append({
'type': 'callback',
'name': 'Temperature',
'elements': [('Temperature', 'int8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetTemperaturePeriod`. The :word:`parameter` is the temperature.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetTemperaturePeriod`,
ausgelöst. Der :word:`parameter` ist die Temperatur.
"""
}] 
})

com['packets'].append({
'type': 'callback',
'name': 'Linear Acceleration',
'elements': [('X', 'int16', 1, 'out'),
             ('Y', 'int16', 1, 'out'),
             ('Z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetLinearAccelerationPeriod`. The :word:`parameters` are the 
linear acceleration for the x, y and z axis.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetLinearAccelerationPeriod`,
ausgelöst. Die :word:`parameter` sind die linearen Beschleunigungen der X, Y und Z-Achse.
"""
}] 
})

com['packets'].append({
'type': 'callback',
'name': 'Gravity Vector',
'elements': [('X', 'int16', 1, 'out'),
             ('Y', 'int16', 1, 'out'),
             ('Z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetGravityVectorPeriod`. The :word:`parameters` gravity vector
for the x, y and z axis.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetGravityVectorPeriod`,
ausgelöst. Die :word:`parameter` sind die Erdbeschleunigungsvektor-Werte 
der X, Y und Z-Achse.
"""
}] 
})

com['packets'].append({
'type': 'callback',
'name': 'Orientation',
'elements': [('Heading', 'int16', 1, 'out'),
             ('Roll', 'int16', 1, 'out'),
             ('Pitch', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetOrientationPeriod`. The :word:`parameters` are the orientation
(heading (yaw), roll, pitch) of the IMU Brick in Euler angles. See
:func:`GetOrientation` for details.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetOrientationPeriod`,
ausgelöst. Die :word:`parameters` sind die Orientierung (Gier-, Roll-, Nickwinkel) des
IMU Brick in Eulerwinkeln. Siehe :func:`GetOrientation` für Details.
"""
}] 
})

com['packets'].append({
'type': 'callback',
'name': 'Quaternion',
'elements': [('W', 'int16', 1, 'out'),
             ('X', 'int16', 1, 'out'),
             ('Y', 'int16', 1, 'out'),
             ('Z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetQuaternionPeriod`. The :word:`parameters` are the orientation
(x, y, z, w) of the IMU Brick in quaternions. See :func:`GetQuaternion`
for details.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetQuaternionPeriod`,
ausgelöst. Die :word:`parameters` sind die Orientierung (x, y, z, w) des
IMU Brick in Quaternionen. Siehe :func:`GetQuaternion` für Details.
"""
}] 
})

com['packets'].append({
'type': 'callback',
'name': 'All Data',
'elements': [('Acceleration', 'int16', 3, 'out'),
             ('Magnetic Field', 'int16', 3, 'out'),
             ('Angular Velocity', 'int16', 3, 'out'),
             ('Euler Angle', 'int16', 3, 'out'),
             ('Quaternion', 'int16', 4, 'out'),
             ('Linear Acceleration', 'int16', 3, 'out'),
             ('Gravity Vector', 'int16', 3, 'out'),
             ('Temperature', 'int8', 1, 'out'),
             ('Calibration Status', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetAllDataPeriod`. The :word:`parameters` are as for :func:`GetAllData`.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetAllDataPeriod`,
ausgelöst. Die :word:`parameter` sind die gleichen wie bei :func:`GetAllData`.
"""
}] 
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Quaternion', 'quaternion'), [(('W', 'Quaternion[W]'), 'int16', 16383.0, None, None, None), (('X', 'Quaternion[X]'), 'int16', 16383.0, None, None, None), (('Y', 'Quaternion[Y]'), 'int16', 16383.0, None, None, None), (('Z', 'Quaternion[Z]'), 'int16', 16383.0, None, None, None)], [])],
'incomplete': True # because of %.02f formatting
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Quaternion', 'quaternion'), [(('W', 'Quaternion[W]'), 'int16', 16383.0, None, None, None), (('X', 'Quaternion[X]'), 'int16', 16383.0, None, None, None), (('Y', 'Quaternion[Y]'), 'int16', 16383.0, None, None, None), (('Z', 'Quaternion[Z]'), 'int16', 16383.0, None, None, None)], None, None),
              ('callback_period', ('Quaternion', 'quaternion'), [], 100)],
'incomplete': True # because of %.02f formatting
})

com['examples'].append({
'name': 'All Data',
'functions': [('callback', ('All Data', 'all data'), [(('Acceleration', 'Acceleration'), 'int16', 100.0, '1/100 m/s²', 'm/s²', None), (('Magnetic Field', 'Magnetic Field'), 'int16', 16.0, '1/16 µT', 'µT', None), (('Angular Velocity', 'Angular Velocity'), 'int16', 16.0, '1/16 °/s', '°/s', None), (('Euler Angle', 'Euler Angle'), 'int16', 16.0, '°/16', '°', None), (('Quaternion', 'Quaternion'), 'int16', 16383.0, None, None, None), (('Linear Acceleration', 'Linear Acceleration'), 'int16', 100.0, '1/100 m/s²', 'm/s²', None), (('Gravity Vector', 'Gravity Vector'), 'int16', 100.0, '1/100 m/s²', 'm/s²', None), (('Temperature', 'Temperature'), 'int8', None, '°C', '°C', None), (('Calibration Status', 'Calibration Status'), 'uint8:bitmask:8', None, None, None, None)], None, None),
              ('callback_period', ('All Data', 'all data'), [], 100)],
'incomplete': True # because of %.02f formatting and parameters with array type
})
