# -*- coding: utf-8 -*-

# IMU Brick communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'version': [1, 0, 0],
    'type': 'Brick',
    'name': ('IMU', 'imu'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for sensing acceleration, magnetic field and angular velocity',
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetAcceleration', 'get_acceleration'), 
'elements': [('x', 'int16', 1, 'out'), 
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'doc': ['am', {
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
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetMagneticField', 'get_magnetic_field'), 
'elements': [('x', 'int16', 1, 'out'), 
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'doc': ['am', {
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
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetAngularVelocity', 'get_angular_velocity'), 
'elements': [('x', 'int16', 1, 'out'), 
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'doc': ['am', {
'en':
"""
Returns the calibrated angular velocity from the gyroscope for the 
x, y and z axis in °/17.5s (you have to divide by 17.5 to
get the value in °/s).

If you want to get the angular velocity periodically, it is recommended 
to use the callback :func:`AngularVelocity` and set the period with 
:func:`SetAngularVelocityPeriod`.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetAllData', 'get_all_data'), 
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
'doc': ['am', {
'en':
"""
Returns the data from :func:`GetAcceleration`, :func:`GetMagneticField` 
and :func:`GetAngularVelocity` as well as the temperature of the IMU Brick.

The temperature is given in °C/100.

If you want to get the data periodically, it is recommended 
to use the callback :func:`AllData` and set the period with 
:func:`SetAllDataPeriod`.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetOrientation', 'get_orientation'), 
'elements': [('roll', 'int16', 1, 'out'), 
             ('pitch', 'int16', 1, 'out'),
             ('yaw', 'int16', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns the current orientation (roll, pitch, yaw) of the IMU Brick as Euler
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
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetQuaternion', 'get_quaternion'), 
'elements': [('x', 'float', 1, 'out'),
             ('y', 'float', 1, 'out'), 
             ('z', 'float', 1, 'out'),
             ('w', 'float', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns the current orientation (x, y, z, w) of the IMU as 
`quaternions <http://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation>`__.

You can go from quaternions to Euler angles with the following formula::

 roll  = atan2(2*y*w - 2*x*z, 1 - 2*y*y - 2*z*z)
 pitch = atan2(2*x*w - 2*y*z, 1 - 2*x*x - 2*z*z)
 yaw   = asin(2*x*y + 2*z*w)

This process is not reversible, because of the 
`gimbal lock <http://en.wikipedia.org/wiki/Gimbal_lock>`__.

Converting the quaternions to an OpenGL translation matrix is
possible with the following formula::

 matrix = [[1 - 2*(y*y + z*z), 2*(x*y - w*z),     2*(x*z + w*y),     0],
           [2*(x*y + w*z),     1 - 2*(x*x + z*z), 2*(y*z - w*x),     0],
           [2*(x*z - w*y),     2*(y*z + w*x),     1 - 2*(x*x + y*y), 0],
           [0,                 0,                 0,                 1]]

If you want to get the quaternions periodically, it is recommended 
to use the callback :func:`Quaternion` and set the period with 
:func:`SetQuaternionPeriod`.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetIMUTemperature', 'get_imu_temperature'), 
'elements': [('temperature', 'int16', 1, 'out')],
'doc': ['am', {
'en':
"""
Returns the temperature of the IMU Brick. The temperature is given in 
°C/100.
""",
'de':
"""
"""
}] 
})


com['packets'].append({
'type': 'function',
'name': ('LedsOn', 'leds_on'), 
'elements': [],
'doc': ['bm', {
'en':
"""
Turns the orientation and direction LEDs of the IMU Brick on.
""",
'de':
"""
"""
}] 
})
    
com['packets'].append({
'type': 'function',
'name': ('LedsOff', 'leds_off'), 
'elements': [],
'doc': ['bm', {
'en':
"""
Turns the orientation and direction LEDs of the IMU Brick off.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('AreLedsOn', 'are_leds_on'), 
'elements': [('leds', 'bool', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns true if the orientation and direction LEDs of the IMU Brick
are on, false otherwise.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('SetAccelerationRange', 'set_acceleration_range'), 
'elements': [('range', 'uint8', 1, 'in')],
'doc': ['am', {
'en':
"""
Not implemented yet.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetAccelerationRange', 'get_acceleration_range'), 
'elements': [('range', 'uint8', 1, 'out')],
'doc': ['am', {
'en':
"""
Not implemented yet.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('SetMagnetometerRange', 'set_magnetometer_range'), 
'elements': [('range', 'uint8', 1, 'in')],
'doc': ['am', {
'en':
"""
Not implemented yet.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetMagnetometerRange', 'get_magnetometer_range'), 
'elements': [('range', 'uint8', 1, 'out')],
'doc': ['am', {
'en':
"""
Not implemented yet.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('SetConvergenceSpeed', 'set_convergence_speed'), 
'elements': [('speed', 'uint16', 1, 'in')],
'doc': ['bm', {
'en':
"""
Sets the convergence speed of the IMU Brick in °/s. The convergence speed 
determines how the different sensor measurements are fused.

If the orientation of the IMU Brick is off by 10° and the convergence speed is 
set to 20°/s, it will take 0.5s until the orientation is corrected. However,
if the correct orientation is reached and the convergence speed is too high,
the orientation will fluctuate with the fluctuations of the accelerometer and
the magnetometer.

If you set the convergence speed to 0, practically only the gyroscope is used
to calculate the orientation. This gives very smooth movements, but errors of the
gyroscope will not be corrected. If you set the convergence speed to something
above 500, practically only the magnetometer and the accelerometer are used to
calculate the orientation. In this case the movements are abrupt and the values
will fluctuate, but there won't be any errors that accumulate over time.

In an application with high angular velocities, we recommend a high convergence
speed, so the errors of the gyroscope can be corrected fast. In applications with
only slow movements we recommend a low convergence speed. You can change the
convergence speed on the fly. So it is possible (and recommended) to increase 
the convergence speed before an abrupt movement and decrease it afterwards 
again.

You might want to play around with the convergence speed in the Brick Viewer to
get a feeling for a good value for your application.

The default value is 30.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetConvergenceSpeed', 'get_convergence_speed'), 
'elements': [('speed', 'uint16', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns the convergence speed as set by :func:`SetConvergenceSpeed`.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('SetCalibration', 'set_calibration'), 
'elements': [('typ', 'uint8', 1, 'in'),
             ('data', 'int16', 10, 'in')],
'doc': ['am', {
'en':
"""
There are several different types that can be calibrated:

.. csv-table::
 :header: "Type", "Description", "Values"
 :widths: 10, 40, 100

 "0", "Accelerometer Gain", "[mul x, mul y, mul z, div x, div y, div z, 0, 0, 0, 0]" 
 "1", "Accelerometer Bias", "[bias x, bias y, bias z, 0, 0, 0, 0, 0, 0, 0]"
 "2", "Magnetometer Gain", "[mul x, mul y, mul z, div x, div y, div z, 0, 0, 0, 0]" 
 "3", "Magnetometer Bias", "[bias x, bias y, bias z, 0, 0, 0, 0, 0, 0, 0]"
 "4", "Gyroscope Gain", "[mul x, mul y, mul z, div x, div y, div z, 0, 0, 0, 0]" 
 "5", "Gyroscope Bias", "[bias xl, bias yl, bias zl, temp l, bias xh, bias yh, bias zh, temp h, 0, 0]"

The calibration via gain and bias is done with the following formula::

 new_value = (bias + orig_value) * gain_mul / gain_div

If you really want to write your own calibration software, please keep
in mind that you first have to undo the old calibration (set bias to 0 and
gain to 1/1) and that you have to average over several thousand values
to obtain a usable result in the end.

The gyroscope bias is highly dependent on the temperature, so you have to
calibrate the bias two times with different temperatures. The values xl, yl, zl 
and temp l are the bias for x, y, z and the corresponding temperature for a 
low temperature. The values xh, yh, zh and temp h are the same for a high 
temperatures. The temperature difference should be at least 5°C. If you have 
a temperature where the IMU Brick is mostly used, you should use this 
temperature for one of the sampling points.

.. note::
 We highly recommend that you use the Brick Viewer to calibrate your
 IMU Brick.

""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetCalibration', 'get_calibration'), 
'elements': [('typ', 'uint8', 1, 'in'),
             ('data', 'int16', 10, 'out')],
'doc': ['am', {
'en':
"""
Returns the calibration for a given type as set by :func:`SetCalibration`.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('SetAccelerationPeriod', 'set_acceleration_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the period in ms with which the :func:`Acceleration` callback is triggered
periodically. A value of 0 turns the callback off.

The default value is 0.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetAccelerationPeriod', 'get_acceleration_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the period as set by :func:`SetAccelerationPeriod`.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('SetMagneticFieldPeriod', 'set_magnetic_field_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the period in ms with which the :func:`MagneticField` callback is triggered
periodically. A value of 0 turns the callback off.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetMagneticFieldPeriod', 'get_magnetic_field_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the period as set by :func:`SetMagneticFieldPeriod`.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('SetAngularVelocityPeriod', 'set_angular_velocity_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the period in ms with which the :func:`AngularVelocity` callback is triggered
periodically. A value of 0 turns the callback off.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetAngularVelocityPeriod', 'get_angular_velocity_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the period as set by :func:`SetAngularVelocityPeriod`.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('SetAllDataPeriod', 'set_all_data_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the period in ms with which the :func:`AllData` callback is triggered
periodically. A value of 0 turns the callback off.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetAllDataPeriod', 'get_all_data_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the period as set by :func:`SetAllDataPeriod`.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('SetOrientationPeriod', 'set_orientation_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the period in ms with which the :func:`Orientation` callback is triggered
periodically. A value of 0 turns the callback off.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetOrientationPeriod', 'get_orientation_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the period as set by :func:`SetOrientationPeriod`.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('SetQuaternionPeriod', 'set_quaternion_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the period in ms with which the :func:`Quaternion` callback is triggered
periodically. A value of 0 turns the callback off.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetQuaternionPeriod', 'get_quaternion_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the period as set by :func:`SetQuaternionPeriod`.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'callback',
'name': ('Acceleration', 'acceleration'), 
'elements': [('x', 'int16', 1, 'out'),
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetAccelerationPeriod`. The :word:`parameters` are the acceleration
for the x, y and z axis.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'callback',
'name': ('MagneticField', 'magnetic_field'), 
'elements': [('x', 'int16', 1, 'out'),
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetMagneticFieldPeriod`. The :word:`parameters` are the magnetic field
for the x, y and z axis.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'callback',
'name': ('AngularVelocity', 'angular_velocity'), 
'elements': [('x', 'int16', 1, 'out'),
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetAngularVelocityPeriod`. The :word:`parameters` are the angular velocity
for the x, y and z axis.
""",
'de':
"""
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
"""
}] 
})

com['packets'].append({
'type': 'callback',
'name': ('Orientation', 'orientation'), 
'elements': [('roll', 'int16', 1, 'out'),
             ('pitch', 'int16', 1, 'out'),
             ('yaw', 'int16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetOrientationPeriod`. The :word:`parameters` are the orientation
(roll, pitch and yaw) of the IMU Brick in Euler angles. See
:func:`GetOrientation` for details.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'callback',
'name': ('Quaternion', 'quaternion'), 
'elements': [('x', 'float', 1, 'out'),
             ('y', 'float', 1, 'out'),
             ('z', 'float', 1, 'out'),
             ('w', 'float', 1, 'out')],
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
"""
}] 
})
