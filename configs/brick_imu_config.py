# -*- coding: utf-8 -*-

# IMU Brick communication config

com = {
    'author': 'Olaf Lüke (olaf@tinkerforge.com)',
    'version': '1.0',
    'type': 'Brick',
    'name': ('IMU', 'imu'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for sensing acceleration, magnetic field and angular velocity',
    'packets': []
}

com['packets'].append({
'type': 'method', 
'name': ('GetAcceleration', 'get_acceleration'), 
'elements': [('x', 'int16', 1, 'out'), 
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'doc': ['bm', {
'en':
""" 
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetMagneticField', 'get_magnetic_field'), 
'elements': [('x', 'int16', 1, 'out'), 
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetAngularVelocity', 'get_angular_velocity'), 
'elements': [('x', 'int16', 1, 'out'), 
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
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
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetOrientation', 'get_orientation'), 
'elements': [('roll', 'int16', 1, 'out'), 
             ('pitch', 'int16', 1, 'out'),
             ('yaw', 'int16', 1, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetQuaternion', 'get_quaternion'), 
'elements': [('w', 'float', 1, 'out'),
             ('x', 'float', 1, 'out'), 
             ('y', 'float', 1, 'out'),
             ('z', 'float', 1, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetIMUTemperature', 'get_imu_temperature'), 
'elements': [('temperature', 'int16', 1, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})


com['packets'].append({
'type': 'method', 
'name': ('LedsOn', 'leds_on'), 
'elements': [],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})
    
com['packets'].append({
'type': 'method', 
'name': ('LedsOff', 'leds_off'), 
'elements': [],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('AreLedsOn', 'are_leds_on'), 
'elements': [('leds', 'bool', 1, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('SetAccelerationRange', 'set_acceleration_range'), 
'elements': [('range', 'uint8', 1, 'in')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetAccelerationRange', 'get_acceleration_range'), 
'elements': [('range', 'uint8', 1, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('SetMagnetometerRange', 'set_magnetometer_range'), 
'elements': [('range', 'uint8', 1, 'in')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetMagnetometerRange', 'get_magnetometer_range'), 
'elements': [('range', 'uint8', 1, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('SetZero', 'set_zero'), 
'elements': [],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('SetDebouncePeriod', 'set_debounce_period'), 
'elements': [('debounce_period', 'uint32', 1, 'in')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetDebouncePeriod', 'get_debounce_period'), 
'elements': [('debounce_period', 'uint32', 1, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('SetAccelerationThreshold', 'set_acceleration_threshold'), 
'elements': [('num', 'uint8', 1, 'in'),
             ('threshold', 'int16', 3, 'in'),
             ('option', 'char', 3, 'in')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetAccelerationThreshold', 'get_acceleration_threshold'), 
'elements': [('num', 'uint8', 1, 'in'),
             ('threshold', 'int16', 3, 'out'),
             ('option', 'char', 3, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('SetMagneticFieldThreshold', 'set_magnetic_field_threshold'), 
'elements': [('num', 'uint8', 1, 'in'),
             ('threshold', 'int16', 3, 'in'),
             ('option', 'char', 3, 'in')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetMagneticFieldThreshold', 'get_magnetic_field_threshold'), 
'elements': [('num', 'uint8', 1, 'in'),
             ('threshold', 'int16', 3, 'out'),
             ('option', 'char', 3, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('SetAngularVelocityThreshold', 'set_angular_velocity_threshold'), 
'elements': [('num', 'uint8', 1, 'in'),
             ('threshold', 'int16', 3, 'in'),
             ('option', 'char', 3, 'in')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetAngularVelocityThreshold', 'get_angular_velocity_threshold'), 
'elements': [('num', 'uint8', 1, 'in'),
             ('threshold', 'int16', 3, 'out'),
             ('option', 'char', 3, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('SetAllDataThreshold', 'set_all_data_threshold'), 
'elements': [('num', 'uint8', 1, 'in'),
             ('threshold', 'int16', 9, 'in'),
             ('option', 'char', 9, 'in')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetAllDataThreshold', 'get_all_data_threshold'), 
'elements': [('num', 'uint8', 1, 'in'),
             ('threshold', 'int16', 9, 'out'),
             ('option', 'char', 9, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('SetOrientationThreshold', 'set_orientation_threshold'), 
'elements': [('num', 'uint8', 1, 'in'),
             ('threshold', 'int16', 3, 'in'),
             ('option', 'char', 3, 'in')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetOrientationThreshold', 'get_orientation_threshold'), 
'elements': [('num', 'uint8', 1, 'in'),
             ('threshold', 'int16', 3, 'out'),
             ('option', 'char', 3, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('SetAccelerationPeriod', 'set_acceleration_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetAccelerationPeriod', 'get_acceleration_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('SetMagneticFieldPeriod', 'set_magnetic_field_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetMagneticFieldPeriod', 'get_magnetic_field_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('SetAngularVelocityPeriod', 'set_angular_velocity_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetAngularVelocityPeriod', 'get_angular_velocity_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('SetAllDataPeriod', 'set_all_data_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetAllDataPeriod', 'get_all_data_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('SetOrientationPeriod', 'set_orientation_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetOrientationPeriod', 'get_orientation_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('SetQuaternionPeriod', 'set_quaternion_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetQuaternionPeriod', 'get_quaternion_period'), 
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'signal', 
'name': ('Acceleration', 'acceleration'), 
'elements': [('x', 'int16', 1, 'out'),
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'signal', 
'name': ('MagneticField', 'magnetic_field'), 
'elements': [('x', 'int16', 1, 'out'),
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'signal', 
'name': ('AngularVelocity', 'angular_velocity'), 
'elements': [('x', 'int16', 1, 'out'),
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'signal', 
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
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'signal', 
'name': ('Orientation', 'orientation'), 
'elements': [('roll', 'int16', 1, 'out'),
             ('pitch', 'int16', 1, 'out'),
             ('yaw', 'int16', 1, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'signal', 
'name': ('Quaternion', 'quaternion'), 
'elements': [('w', 'float', 1, 'out'),
             ('x', 'float', 1, 'out'),
             ('y', 'float', 1, 'out'),
             ('z', 'float', 1, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'signal', 
'name': ('AccelerationReached', 'acceleration_reached'), 
'elements': [('x', 'int16', 1, 'out'),
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'signal', 
'name': ('MagneticFieldReached', 'magnetic_field_reached'), 
'elements': [('x', 'int16', 1, 'out'),
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'signal', 
'name': ('AngularVelocityReached', 'angular_velocity_reached'), 
'elements': [('x', 'int16', 1, 'out'),
             ('y', 'int16', 1, 'out'),
             ('z', 'int16', 1, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'signal', 
'name': ('AllDataReached', 'all_data_reached'), 
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
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'signal', 
'name': ('OrientationReached', 'orientation_reached'), 
'elements': [('roll', 'int16', 1, 'out'),
             ('pitch', 'int16', 1, 'out'),
             ('yaw', 'int16', 1, 'out')],
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}] 
})

