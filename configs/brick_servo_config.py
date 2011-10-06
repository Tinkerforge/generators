# -*- coding: utf-8 -*-

# Servo Brick communication config

com = {
    'author': 'Olaf Lüke (olaf@tinkerforge.com)',
    'version': [1, 0, 0],
    'type': 'Brick',
    'name': ('Servo', 'servo'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for controlling up to seven servos',
    'packets': []
}

com['api'] = """
Every method of the Servo Brick API that has a *servo_num* parameter can
address a servo with the servo number (0 to 6) or with a bitmask for the 
servos, if the last bit is set. For example: "1" will address servo 1, 
"(1 << 1) | (1 << 5) | (1 << 8)" will address servos 1 and 5, "0xFF" will
address all seven servos, etc. This allows to set configurations to several
servos with one function call. It is guaranteed that the changes will take
effect in the same PWM period for all servos you specified in the bitmask.
"""

com['packets'].append({
'type': 'method', 
'name': ('Enable', 'enable'), 
'elements': [('servo_num', 'uint8', 1, 'in')], 
'doc': ['bm', {
'en':
"""
Enables a servo (0 to 6). If a servo is enabled, the configured position,
velocity, acceleration, etc. are applied immediately.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('Disable', 'disable'), 
'elements': [('servo_num', 'uint8', 1, 'in')], 
'doc': ['bm', {
'en':
"""
Disables a servo (0 to 6). Disabled servos are not driven at all, i.e. a
disabled servo will not hold its position if a load is applied.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('IsEnabled', 'is_enabled'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('enabled', 'bool', 1, 'out')], 
'doc': ['bm', {
'en':
"""
Returns true if the specified servo is enabled, false otherwise.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('SetPosition', 'set_position'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('position', 'int16', 1, 'in')], 
'doc': ['bm', {
'en':
"""
Sets the position in °/100 for the specified servo. 

The default range of the position is -9000 to 9000, but it can be specified
according to your servo with :func:`SetDegree`.

If you want to control a linear servo or RC brushless motor controller or
similar with the Servo Brick, you can also define lengths or speeds with
:func:`SetDegree`.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetPosition', 'get_position'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('position', 'int16', 1, 'out')], 
'doc': ['bm', {
'en':
"""
Returns the position of the specified servo as set by :func:`SetPosition`.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetCurrentPosition', 'get_current_position'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('position', 'int16', 1, 'out')], 
'doc': ['bm', {
'en':
"""
Returns the *current* position of the specified servo. This may not be the
value of :func:`SetPosition` if the servo is currently approaching a
position goal.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('SetVelocity', 'set_velocity'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('velocity', 'uint16', 1, 'in')], 
'doc': ['bm', {
'en':
"""
Sets the maximum velocity of the specified servo in °/100s. The velocity
is accelerated according to the value set by :func:`SetAcceleration`.

The minimum velocity is 0 (no movement) and the maximum velocity is 65535.
With a value of 65535 the position will be set immediately (no velocity).

The default value is 65535.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetVelocity', 'get_velocity'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('velocity', 'uint16', 1, 'out')], 
'doc': ['bm', {
'en':
"""
Returns the velocity of the specified servo as set by :func:`SetVelocity`.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetCurrentVelocity', 'get_current_velocity'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('velocity', 'uint16', 1, 'out')], 
'doc': ['bm', {
'en':
"""
Returns the *current* velocity of the specified servo. This may not be the
value of :func:`SetVelocity` if the servo is currently approaching a
velocity goal.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('SetAcceleration', 'set_acceleration'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('acceleration', 'uint16', 1, 'in')], 
'doc': ['bm', {
'en':
"""
Sets the acceleration of the specified servo in °/100s².

The minimum acceleration is 1 and the maximum acceleration is 65535.
With a value of 65535 the velocity will be set immediately (no acceleration).

The default value is 65535.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetAcceleration', 'get_acceleration'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('acceleration', 'uint16', 1, 'out')], 
'doc': ['bm', {
'en':
"""
Returns the acceleration for the specified servo as set by 
:func:`SetAcceleration`.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('SetOutputVoltage', 'set_output_voltage'), 
'elements': [('voltage', 'uint16', 1, 'in')], 
'doc': ['bm', {
'en':
"""
Sets the output voltages with which the servos are driven in mV.
The minimum output voltage is 5000mV and the maximum output voltage is 
9000mV.

 .. note::
  We recommend that you set this value to the maximum voltage that is
  specified for your servo, most servos achieve their maximum force only
  with high voltages.

The default value is 5000.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetOutputVoltage', 'get_output_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')], 
'doc': ['bm', {
'en':
"""
Returns the output voltage as specified by :func:`SetOutputVoltage`.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('SetPulseWidth', 'set_pulse_width'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('min', 'uint16', 1, 'in'),
             ('max', 'uint16', 1, 'in')], 
'doc': ['bm', {
'en':
"""
Sets the minimum and maximum pulse width of the specified servo in µs.

Usually, servos are controlled with a 
`PWM <http://en.wikipedia.org/wiki/Pulse-width_modulation>`_, whereby the 
length of the pulse controls the position of the servo. Every servo has
different minimum and maximum pulse widths, these can be specified with
this function.

If you have a datasheet for your servo that specifies the minimum and
maximum pulse width, you should set the values accordingly. If your servo
comes without any datasheet you have to find the values via trial and error.

Both values have a range from 1 to 65535 (unsigned 16 bit integer). The
minimum must be smaller than the maximum.

The default values are 1000µs (1ms) and 2000µs (2ms) for minimum and 
maximum pulse width.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetPulseWidth', 'get_pulse_width'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('min', 'uint16', 1, 'out'),
             ('max', 'uint16', 1, 'out')], 
'doc': ['bm', {
'en':
"""
Returns the minimum and maximum pulse width for the specified servo as set by
:func:`SetPulseWidth`.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('SetDegree', 'set_degree'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('min', 'int16', 1, 'in'),
             ('max', 'int16', 1, 'in')], 
'doc': ['bm', {
'en':
"""
Sets the minimum and maximum degree for the specified servo (by default
given as °/100).

This only specifies the abstract values between which the minimum and maximum
pulse width is scaled. For example: If you specifiy a pulse width of 1000µs
to 2000µs and a degree range of -90° to 90°, a call of :func:`SetPosition`
with 0 will result in a pulse width of 1500µs 
(-90° = 1000µs, 90° = 2000µs, etc.).

Possible usage:

 * The datasheet of your servo specifies a range of 200° with the middle position at 110°. In this case you can set the minimum to -9000 and the maximum to 11000.
 * You measure a range of 220° on your servo and you don't have or need a middle position. In this case you can set the minimum to 0 and the maximum to 22000.
 * You have a linear servo with a drive length of 20cm, In this case you could set the minimum to 0 and the maximum to 20000. Now you can set the Position with :func:`SetPosition` with a resolution of cm/100. Also the velocity will have a resoltion of cm/100s and the acceleration will have a resolution of cm/100s².
 * You don't care about units and just want the highest possible resolution. In this case you should set the minimum to -32767 and the maximum to 32767.
 * You have a brushless motor with a maximum speed of 10000 rpm and want to conrol it with a RC brushless motor controller. In this case you can set the minimum to 0 and the maximum to 10000. :func:`SetPosition` now controls the rpm.

Both values have a possible range from -32767 to 32767 
(signed 16 bit integer). The minimum must be smaller than the maximum.

The default values are -9000 and 9000 for the minimum and maximum degree.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetDegree', 'get_degree'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('min', 'int16', 1, 'out'),
             ('max', 'int16', 1, 'out')], 
'doc': ['bm', {
'en':
"""
Returns the minimum and maximum degree for the specified servo as set by
:func:`SetDegree`.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('SetPeriod', 'set_period'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('period', 'uint16', 1, 'in')],
'doc': ['bm', {
'en':
"""
Sets the period of the specified servo in µs.

Usually, servos are controlled with a 
`PWM <http://en.wikipedia.org/wiki/Pulse-width_modulation>`_. Different
servos expect PWMs with different periods. Most servos run well with a 
period of about 20ms.

If your servo comes with a datasheet that specifies a period, you should
set it accordingly. If you don't have a datasheet and you have no idea
what the correct period is, the default value (19.5ms) will most likely
work fine. 

The minimum possible period is 2000µs and the maximum is 65535µs.

The default value is 19.5ms (19500µs).
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetPeriod', 'get_period'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('period', 'uint16', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns the period for the specified servo as set by :func:`SetPeriod`.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetServoCurrent', 'get_servo_current'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('current', 'uint16', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns the current consumption of the specified servo in mA.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetOverallCurrent', 'get_overall_current'), 
'elements': [('current', 'uint16', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns the current consumption of all servos together in mA.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetStackInputVoltage', 'get_stack_input_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns the stack input voltage in mV. The stack input voltage is the
voltage that is supplied via the stack, i.e. it is given by a 
Step-Down or Step-Up power supply Brick.
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('GetExternalInputVoltage', 'get_external_input_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns the external input voltage in mV. The external input voltage is
given via the black power input connector on the Servo Brick. 
 
If there is  an externel input voltage and a stack input voltage, the motor 
will be driven by the external input voltage. If there is only a stack 
voltage present, the motor will be driven by this voltage.

 .. warning:: 
  This means, if you have a high stack voltage and a low external voltage,
  the motor will be driven with the low external voltage. If you then remove
  the external connection, it will immediately be driven by the high
  stack voltage
""",
'de':
"""
"""
}] 
})

com['packets'].append({
'type': 'method', 
'name': ('SetMinimumVoltage', 'set_minimum_voltage'), 
'elements': [('voltage', 'uint16', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the minimum voltage in mV, below which the :func:`UnderVoltage` signal
is called. The minimum possible value that works with the Servo Brick is 5V. 
You can use this function to detect the discharge of a battery that is used
to drive the stepper motor. If you have a fixed power supply, you likely do 
not need this functionality.

The default value is 5V (5000mV).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetMinimumVoltage', 'get_minimum_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the minimum voltage as set by :func:`SetMinimumVoltage`
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'signal', 
'name': ('UnderVoltage', 'under_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is called when the input voltage drops below the value set by
:func:`SetMinimumVoltage`. The parameter is the current voltage given
in mV.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'signal', 
'name': ('PositionReached', 'position_reached'), 
'elements': [('servo_num', 'uint8', 1, 'out'),
             ('position', 'int16', 1, 'out')], 
'doc': ['c', {
'en':
"""
This callback is called when a position set by :func:`SetPosition` 
is reached. The parameters are the servo and the position that is reached.

.. note::
 Since we can't get any feedback from the servo, this only works if the
 velocity (see :func:`SetVelocity`) is set smaller or equal to the
 maximum velocity of the servo. Otherwise the servo will lag behind the
 control value and the callback will be called too early.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'signal', 
'name': ('VelocityReached', 'velocity_reached'), 
'elements': [('servo_num', 'uint8', 1, 'out'),
             ('velocity', 'int16', 1, 'out')], 
'doc': ['c', {
'en':
"""
This callback is called when a velocity set by :func:`SetVelocity` 
is reached. The parameters are the servo and the velocity that is reached.

.. note::
 Since we can't get any feedback from the servo, this only works if the
 acceleration (see :func:`SetAcceleration`) is set smaller or equal to the
 maximum acceleration of the servo. Otherwise the servo will lag behind the
 control value and the callback will be called too early.
""",
'de':
"""
"""
}]
})
