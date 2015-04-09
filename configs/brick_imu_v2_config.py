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
    'name': ('IMUV2', 'imu_v2', 'IMU 2.0'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for sensing acceleration, magnetic field and angular velocity',
    'released': False,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetAcceleration', 'get_acceleration'), 
'elements': [('x', 'int16', 1, 'out'), 
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
""" 
Returns the calibrated acceleration from the accelerometer for the 
x, y and z axis in mG (G/1000, 1G = 9.80605m/s²).

If you want to get the acceleration periodically, it is recommended 
to use the callback :func:`Acceleration` and set the period with 
:func:`SetAccelerationPeriod`.
""",
'de':
"""
Gibt die kalibrierten Beschleunigungen des Beschleunigungsmessers für die 
X, Y und Z-Achse in mG zurück (G/1000, 1G = 9.80605m/s²).

Wenn die kalibrierten Beschleunigungen periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`Acceleration` zu nutzen und die Periode mit :func:`SetAccelerationPeriod`
vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetMagneticField', 'get_magnetic_field'), 
'elements': [('x', 'int16', 1, 'out'), 
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the calibrated magnetic field from the magnetometer for the 
x, y and z axis in mG (Milligauss or Nanotesla).

If you want to get the magnetic field periodically, it is recommended 
to use the callback :func:`MagneticField` and set the period with 
:func:`SetMagneticFieldPeriod`.
""",
'de':
"""
Gibt das kalibrierte magnetische Feld des Magnetometers mit den X, Y und
Z Komponenten in mG zurück (Milligauss oder Nanotesla).

Wenn das magnetische Feld periodisch abgefragt werden soll, wird empfohlen
den Callback :func:`MagneticField` zu nutzen und die Periode mit :func:`SetMagneticFieldPeriod`
vorzugeben.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetAngularVelocity', 'get_angular_velocity'), 
'elements': [('x', 'int16', 1, 'out'), 
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the calibrated angular velocity from the gyroscope for the 
x, y and z axis in °/14.375s (you have to divide by 14.375 to
get the value in °/s).

If you want to get the angular velocity periodically, it is recommended 
to use the callback :func:`AngularVelocity` and set the period with 
:func:`SetAngularVelocityPeriod`.
""",
'de':
"""
Gibt die kalibrierten Winkelgeschwindigkeiten des Gyroskops für die X, Y und
Z-Achse in °/14,375s zurück. (Um den Wert in °/s zu erhalten ist es notwendig
durch 14,375 zu teilen)

Wenn die Winkelgeschwindigkeiten periodisch abgefragt werden sollen, wird empfohlen
den Callback :func:`AngularVelocity` zu nutzen und die Periode mit
:func:`SetAngularVelocityPeriod` vorzugeben.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetTemperature', 'get_temperature'), 
'elements': [('temperature', 'int8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the temperature of the IMU Brick. The temperature is given in 
°C/100.
""",
'de':
"""
Gibt die Temperatur (in °C/100) des IMU Brick zurück.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetOrientation', 'get_orientation'), 
'elements': [('roll', 'int16', 1, 'out'), 
             ('pitch', 'int16', 1, 'out'),
             ('heading', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current orientation (roll, pitch, heading) of the IMU Brick as Euler
angles in one-hundredth degree. Note that Euler angles always experience a
`gimbal lock <http://en.wikipedia.org/wiki/Gimbal_lock>`__.

We recommend that you use quaternions instead.

The order to sequence in which the orientation values should be applied is 
roll, yaw, pitch. 

If you want to get the orientation periodically, it is recommended 
to use the callback :func:`Orientation` and set the period with 
:func:`SetOrientationPeriod`.
""",
'de':
"""
Gibt die aktuelle Orientierung (Roll-, Nick-, Gierwinkel) des IMU Brick in Eulerwinkeln
(in 1/100 °) zurück. Zu beachten ist, dass Eulerwinkel immer eine 
`kardanische Blockade <http://de.wikipedia.org/wiki/Gimbal_Lock>`__ erfahren.

Wir empfehlen die Verwendung von Quaternionen stattdessen.

Die Reihenfolge in denen die Orientierungswerte angewandt werden sollten,
ist Roll-, Nick-, Gierwinkel.

Wenn die Orientierung periodisch abgefragt werden sollen, wird empfohlen den
Callback :func:`Orientation` zu nutzen und die Periode mit :func:`SetOrientationPeriod`
vorzugeben.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetLinearAcceleration', 'get_linear_acceleration'), 
'elements': [('x', 'int16', 1, 'out'), 
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetGravityVector', 'get_gravity_vector'), 
'elements': [('x', 'int16', 1, 'out'), 
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetQuaternion', 'get_quaternion'), 
'elements': [('w', 'uint16', 1, 'out'),
             ('x', 'uint16', 1, 'out'), 
             ('y', 'uint16', 1, 'out'),
             ('z', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current orientation (x, y, z, w) of the IMU as 
`quaternions <http://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation>`__.

You can go from quaternions to Euler angles with the following formula::

 xAngle = atan2(2*y*w - 2*x*z, 1 - 2*y*y - 2*z*z)
 yAngle = atan2(2*x*w - 2*y*z, 1 - 2*x*x - 2*z*z)
 zAngle =  asin(2*x*y + 2*z*w)

This process is not reversible, because of the 
`gimbal lock <http://en.wikipedia.org/wiki/Gimbal_lock>`__.

It is also possible to calculate independent angles. You can calculate 
yaw, pitch and roll in a right-handed vehicle coordinate system according to DIN70000
with::

 yaw   =  atan2(2*x*y + 2*w*z, w*w + x*x - y*y - z*z)
 pitch = -asin(2*w*y - 2*x*z)
 roll  = -atan2(2*y*z + 2*w*x, -w*w + x*x + y*y - z*z))

Converting the quaternions to an OpenGL transformation matrix is
possible with the following formula::

 matrix = [[1 - 2*(y*y + z*z),     2*(x*y - w*z),     2*(x*z + w*y), 0],
           [    2*(x*y + w*z), 1 - 2*(x*x + z*z),     2*(y*z - w*x), 0],
           [    2*(x*z - w*y),     2*(y*z + w*x), 1 - 2*(x*x + y*y), 0],
           [                0,                 0,                 0, 1]]

If you want to get the quaternions periodically, it is recommended 
to use the callback :func:`Quaternion` and set the period with 
:func:`SetQuaternionPeriod`.
""",
'de':
"""
Gibt die aktuelle Orientierung (x, y, z, w) des IMU Brick als
`Quaterinonen <http://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation>`__ zurück.

Die Umrechnung von Quaternionen in Eulerwinkel ist mit folgender Formel möglich::

 xAngle = atan2(2*y*w - 2*x*z, 1 - 2*y*y - 2*z*z)
 yAngle = atan2(2*x*w - 2*y*z, 1 - 2*x*x - 2*z*z)
 zAngle =  asin(2*x*y + 2*z*w)

Es ist auch möglich unabhängige Winkel zu berechen. Yaw, Pitch und Roll
in einem rechtshändigen Fahrzeugkoordinatensystem nach DIN70000 können
wie folgt berechnet werden::

 yaw   =  atan2(2*x*y + 2*w*z, w*w + x*x - y*y - z*z)
 pitch = -asin(2*w*y - 2*x*z)
 roll  = -atan2(2*y*z + 2*w*x, -w*w + x*x + y*y - z*z))
 
Diese Umrechnung ist irreversibel aufgrund der 
`kardanischen Blockade <http://de.wikipedia.org/wiki/Gimbal_lock>`__.

Die Umrechnung von Quaternionen in eine OpenGL Transformationsmatrix ist
mit folgender Formel möglich::

 matrix = [[1 - 2*(y*y + z*z),     2*(x*y - w*z),     2*(x*z + w*y), 0],
           [    2*(x*y + w*z), 1 - 2*(x*x + z*z),     2*(y*z - w*x), 0],
           [    2*(x*z - w*y),     2*(y*z + w*x), 1 - 2*(x*x + y*y), 0],
           [                0,                 0,                 0, 1]]

Wenn die Quaternionen periodisch abgefragt werden sollen, wird empfohlen den
Callback :func:`Quaternion` zu nutzen und die Periode mit :func:`SetQuaternionPeriod`
vorzugeben.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetAllData', 'get_all_data'), 
'elements': [('acceleration', 'int16', 3, 'out'), 
             ('magnetic_field', 'int16', 3, 'out'),
             ('angular_velocity', 'int16', 3, 'out'),
             ('euler_angle', 'int16', 3, 'out'), 
             ('quaternion', 'uint16', 4, 'out'),
             ('linear_acceleration', 'int16', 3, 'out'),
             ('gravity_vector', 'int16', 3, 'out'), 
             ('temperature', 'int8', 1, 'out'),
             ('calibration_status', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
TODO

If you want to get the data periodically, it is recommended 
to use the callback :func:`AllData` and set the period with 
:func:`SetAllDataPeriod`.
""",
'de':
"""
TODO

Wenn die Daten periodisch abgefragt werden sollen, wird empfohlen den
Callback :func:`AllData` zu nutzen und die Periode mit :func:`SetAllDataPeriod`
vorzugeben.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('LedsOn', 'leds_on'), 
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
'name': ('LedsOff', 'leds_off'), 
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
'name': ('AreLedsOn', 'are_leds_on'), 
'elements': [('leds', 'bool', 1, 'out')],
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
'name': ('SetConfiguration', 'set_configuration'), 
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetConfiguration', 'get_configuration'), 
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('SetAccelerationPeriod', 'set_acceleration_period'), 
'elements': [('period', 'uint32', 1, 'in')],
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
'name': ('GetAccelerationPeriod', 'get_acceleration_period'), 
'elements': [('period', 'uint32', 1, 'out')],
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
'name': ('SetMagneticFieldPeriod', 'set_magnetic_field_period'), 
'elements': [('period', 'uint32', 1, 'in')],
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
'name': ('GetMagneticFieldPeriod', 'get_magnetic_field_period'), 
'elements': [('period', 'uint32', 1, 'out')],
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
'name': ('SetAngularVelocityPeriod', 'set_angular_velocity_period'), 
'elements': [('period', 'uint32', 1, 'in')],
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
'name': ('GetAngularVelocityPeriod', 'get_angular_velocity_period'), 
'elements': [('period', 'uint32', 1, 'out')],
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
'name': ('SetTemperaturePeriod', 'set_temperature_period'), 
'elements': [('period', 'uint32', 1, 'in')],
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
'name': ('GetTemperaturePeriod', 'get_temperature_period'), 
'elements': [('period', 'uint32', 1, 'out')],
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
'name': ('SetOrientationPeriod', 'set_orientation_period'), 
'elements': [('period', 'uint32', 1, 'in')],
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
'name': ('GetOrientationPeriod', 'get_orientation_period'), 
'elements': [('period', 'uint32', 1, 'out')],
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
'name': ('SetLinearAccelerationPeriod', 'set_linear_acceleration_period'), 
'elements': [('period', 'uint32', 1, 'in')],
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
'name': ('GetLinearAccelerationPeriod', 'get_linear_acceleration_period'), 
'elements': [('period', 'uint32', 1, 'out')],
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
'name': ('SetGravityVectorPeriod', 'set_gravity_vector_period'), 
'elements': [('period', 'uint32', 1, 'in')],
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
'name': ('GetGravityVectorPeriod', 'get_gravity_vector_period'), 
'elements': [('period', 'uint32', 1, 'out')],
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
'name': ('SetQuaternionPeriod', 'set_quaternion_period'), 
'elements': [('period', 'uint32', 1, 'in')],
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
'name': ('GetQuaternionPeriod', 'get_quaternion_period'), 
'elements': [('period', 'uint32', 1, 'out')],
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
'name': ('SetAllDataPeriod', 'set_all_data_period'), 
'elements': [('period', 'uint32', 1, 'in')],
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
'name': ('GetAllDataPeriod', 'get_all_data_period'), 
'elements': [('period', 'uint32', 1, 'out')],
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
'name': ('Acceleration', 'acceleration'), 
'elements': [('x', 'int16', 1, 'out'),
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
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
'name': ('MagneticField', 'magnetic_field'), 
'elements': [('x', 'int16', 1, 'out'),
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
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
'name': ('AngularVelocity', 'angular_velocity'), 
'elements': [('x', 'int16', 1, 'out'),
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
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
'name': ('Temperature', 'temperature'), 
'elements': [('temperature', 'int8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetTemperaturePeriod`. The :word:`parameters` TODO.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetTemperaturePeriod`,
ausgelöst. Die :word:`parameters` TODO.
"""
}] 
})

com['packets'].append({
'type': 'callback',
'name': ('LinearAcceleration', 'linear_acceleration'), 
'elements': [('x', 'int16', 1, 'out'),
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetLinearAccelerationPeriod`. The :word:`parameters` TODO.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetLinearAccelerationPeriod`,
ausgelöst. Die :word:`parameters` TODO.
"""
}] 
})

com['packets'].append({
'type': 'callback',
'name': ('GravityVector', 'gravity_vector'), 
'elements': [('x', 'int16', 1, 'out'),
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetGravityVectorPeriod`. The :word:`parameters` TODO.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetGravityVectorPeriod`,
ausgelöst. Die :word:`parameters` TODO.
"""
}] 
})

com['packets'].append({
'type': 'callback',
'name': ('Orientation', 'orientation'), 
'elements': [('roll', 'int16', 1, 'out'),
             ('pitch', 'int16', 1, 'out'),
             ('heading', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetOrientationPeriod`. The :word:`parameters` are the orientation
(roll, pitch and heading (yaw)) of the IMU Brick in Euler angles. See
:func:`GetOrientation` for details.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetOrientationPeriod`,
ausgelöst. Die :word:`parameters` sind die Orientierung (Roll-, Nick-, Gierwinkel) des
IMU Brick in Eulerwinkeln. Siehe :func:`GetOrientation` für Details.
"""
}] 
})

com['packets'].append({
'type': 'callback',
'name': ('Quaternion', 'quaternion'), 
'elements': [('w', 'uint16', 1, 'out'),
             ('x', 'uint16', 1, 'out'),
             ('y', 'uint16', 1, 'out'),
             ('z', 'uint16', 1, 'out')],
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
'name': ('AllData', 'all_data'), 
'elements': [('acc_x', 'int16', 1, 'out'), 
             ('acc_y', 'int16', 1, 'out'),
             ('acc_z', 'int16', 1, 'out'),
             ('mag_x', 'int16', 1, 'out'), 
             ('mag_y', 'int16', 1, 'out'),
             ('mag_z', 'int16', 1, 'out'),
             ('ang_x', 'int16', 1, 'out'), 
             ('ang_y', 'int16', 1, 'out'),
             ('ang_z', 'int16', 1, 'out'),
             ('temperature', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetAllDataPeriod`. The :word:`parameters` are the acceleration,
the magnetic field and the angular velocity for the x, y and z axis as
well as the temperature of the IMU Brick.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetAllDataPeriod`,
ausgelöst. Die :word:`parameters` sind die Beschleunigungen, Magnetfeldkomponenten
und die Winkelgeschwindigkeiten der X, Y und Z-Achse sowie die Temperatur
des IMU Brick.
"""
}] 
})
