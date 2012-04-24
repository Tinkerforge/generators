# -*- coding: utf-8 -*-

# Stepper Brick communication config

com = {
    'author': 'Olaf Lüke (olaf@tinkerforge.com)',
    'version': [1, 0, 0],
    'type': 'Brick',
    'name': ('Stepper', 'stepper'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for controlling stepper motors',
    'packets': []
}


com['packets'].append({
'type': 'method', 
'name': ('SetMaxVelocity', 'set_max_velocity'), 
'elements': [('velocity', 'uint16', 1, 'in')],
'doc': ['bm', {
'en':
"""
Sets the maximum velocity of the stepper motor in steps per second.
This function does *not* start the motor, it merely sets the maximum
velocity the stepper motor is accelerated to. To get the motor running use
either :func:`SetTargetPosition`, :func:`SetSteps`, :func:`DriveForward` or
:func:`DriveBackward`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetMaxVelocity', 'get_max_velocity'), 
'elements': [('velocity', 'uint16', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns the velocity as set by :func:`SetMaxVelocity`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetCurrentVelocity', 'get_current_velocity'), 
'elements': [('velocity', 'uint16', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns the *current* velocity of the stepper motor in steps per second.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('SetSpeedRamping', 'set_speed_ramping'), 
'elements': [('acceleration', 'uint16', 1, 'in'),
             ('deacceleration', 'uint16', 1, 'in')],
'doc': ['bm', {
'en':
"""
Sets the acceleration and deacceleration of the stepper motor. The values
are given in *steps/s²*. An acceleration of 1000 means, that
every second the velocity is increased by 1000 *steps/s*.

For example: If the current velocity is 0 and you want to accelerate to a
velocity of 8000 *steps/s* in 10 seconds, you should set an acceleration
of 800 *steps/s²*.

An dacceleration/deacceleration of 0 means instantaneous 
acceleration/deacceleration (not recomended)

The default value is 1000 for both
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetSpeedRamping', 'get_speed_ramping'), 
'elements': [('acceleration', 'uint16', 1, 'out'),
             ('deacceleration', 'uint16', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns the acceleration and deacceleration as set by 
:func:`SetSpeedRamping`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('FullBrake', 'full_brake'), 
'elements': [],
'doc': ['bm', {
'en':
"""
Executes an active full brake. 
 
 .. warning::
  This function is for emergency purposes,
  where an immediate brake is necessary. Depending on the current velocity and
  the strength of the motor, a full brake can be quite violent.

Call :func:`Stop` if you just want to stop the motor.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('SetCurrentPosition', 'set_current_position'), 
'elements': [('position', 'int32', 1, 'in')],
'doc': ['am', {
'en':
"""
Sets the current steps of the internal step counter. This can be used to
set the current position to 0 when some kind of starting position
is reached (e.g. when a CNC machine reaches a corner).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetCurrentPosition', 'get_current_position'), 
'elements': [('position', 'int32', 1, 'out')],
'doc': ['am', {
'en':
"""
Returns the current position of the stepper motor in steps. On startup
the position is 0. The steps are counted with all possible driving
functions (:func:`SetTargetPosition`, :func:`SetSteps`, :func:`DriveForward` or
:func:`DriveBackward`). It also is possible to reset the steps to 0 or
set them to any other desired value with :func:`SetCurrentPosition`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('SetTargetPosition', 'set_target_position'), 
'elements': [('position', 'int32', 1, 'in')],
'doc': ['am', {
'en':
"""
Sets the target position of the stepper motor in steps. For example,
if the current position of the motor is 500 and :func:`SetTargetPosition` is
called with 1000, the stepper motor will drive 500 steps forward. It will
use the velocity, acceleration and deacceleration as set by
:func:`SetMaxVelocity` and :func:`SetSpeedRamping`.

A call of :func:`SetTargetPosition` with the parameter *x* is equivalent to
a call of :func:`SetSteps` with the parameter 
(*x* - :func:`GetCurrentPosition`).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetTargetPosition', 'get_target_position'), 
'elements': [('position', 'int32', 1, 'out')],
'doc': ['am', {
'en':
"""
Returns the last target position as set by :func:`SetTargetPosition`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('SetSteps', 'set_steps'), 
'elements': [('steps', 'int32', 1, 'in')],
'doc': ['bm', {
'en':
"""
Sets the number of steps the stepper motor should run. Positive values
will drive the motor forward and negative values backward. 
The velocity, acceleration and deacceleration as set by
:func:`SetMaxVelocity` and :func:`SetSpeedRamping` will be used.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetSteps', 'get_steps'), 
'elements': [('steps', 'int32', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns the last steps as set by :func:`SetSteps`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetRemainingSteps', 'get_remaining_steps'), 
'elements': [('steps', 'int32', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns the remaining steps of the last call of :func:`SetSteps`.
For example, if :func:`SetSteps` is called with 2000 and 
:func:`GetRemainingSteps` is called after the motor has run for 500 steps,
it will return 1500.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('SetStepMode', 'set_step_mode'), 
'elements': [('mode', 'uint8', 1, 'in')],
'doc': ['am', {
'en':
"""
Sets the step mode of the stepper motor. Possible values are:

* Full Step = 1
* Half Step = 2
* Quarter Step = 4
* Eighth Step = 8

A higher value will increase the resolution and
decrease the torque of the stepper motor.

The default value is 8 (Eighth Step).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetStepMode', 'get_step_mode'), 
'elements': [('mode', 'uint8', 1, 'out')],
'doc': ['am', {
'en':
"""
Returns the step mode as set by :func:`SetStepMode`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('DriveForward', 'drive_forward'), 
'elements': [],
'doc': ['bm', {
'en':
"""
Drives the stepper motor forward until :func:`DriveBackward` or
:func:`Stop` is called. The velocity, acceleration and deacceleration as 
set by :func:`SetMaxVelocity` and :func:`SetSpeedRamping` will be used.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('DriveBackward', 'drive_backward'), 
'elements': [],
'doc': ['bm', {
'en':
"""
Drives the stepper motor backward until :func:`DriveForward` or
:func:`Stop` is triggered. The velocity, acceleration and deacceleration as
set by :func:`SetMaxVelocity` and :func:`SetSpeedRamping` will be used.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('Stop', 'stop'), 
'elements': [],
'doc': ['bm', {
'en':
"""
Stops the stepper motor with the deacceleration as set by 
:func:`SetSpeedRamping`.
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
'doc': ['am', {
'en':
"""
Returns the stack input voltage in mV. The stack input voltage is the
voltage that is supplied via the stack, i.e. it is given by a 
Step-Down or Step-Up Power Supply.
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
'doc': ['am', {
'en':
"""
Returns the external input voltage in mV. The external input voltage is
given via the black power input connector on the Stepper Brick. 
 
If there is an external input voltage and a stack input voltage, the motor
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
'name': ('GetCurrentConsumption', 'get_current_consumption'), 
'elements': [('current', 'uint16', 1, 'out')],
'doc': ['am', {
'en':
"""
Returns the current consumption of the motor in mA.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('SetMotorCurrent', 'set_motor_current'), 
'elements': [('current', 'uint16', 1, 'in')],
'doc': ['bm', {
'en':
"""
Sets the current in mA with which the motor will be driven.
The minimum value is 100mA, the maximum value 2291mA and the 
default value is 800mA.

 .. warning::
  Do not set this value above the specifications of your stepper motor.
  Otherwise it may damage your motor.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetMotorCurrent', 'get_motor_current'), 
'elements': [('current', 'uint16', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns the current as set by :func:`SetMotorCurrent`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('Enable', 'enable'), 
'elements': [],
'doc': ['bm', {
'en':
"""
Enables the motor. The motor can be configured (maximum velocity, 
acceleration, etc) before it is enabled.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('Disable', 'disable'), 
'elements': [],
'doc': ['bm', {
'en':
"""
Disables the motor. The configurations are kept (maximum velocity, 
acceleration, etc) but the motor is not driven until it is enabled again.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('IsEnabled', 'is_enabled'), 
'elements': [('enabled', 'bool', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns true if the motor is enabled, false otherwise.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('SetDecay', 'set_decay'), 
'elements': [('decay', 'uint16', 1, 'in')],
'doc': ['am', {
'en':
"""
Sets the decay mode of the stepper motor. The possible value range is
between 0 and 65535. A value of 0 sets the fast decay mode, a value of
65535 sets the slow decay mode and a value in between sets the mixed
decay mode.

For a good explanation of the different decay modes see 
`this <http://robot.avayanex.com/?p=86/>`_ blog post by Avayan.

A good decay mode is unfortunately different for every motor. The best
way to work out a good decay mode for your stepper motor, if you can't
measure the current with an oscilloscope, is to listen to the sound of
the motor. If the value is too low, you often hear a high pitched 
sound and if it is too high you can often hear a humming sound.

Generally, fast decay mode (small value) will be noisier but also
allow higher motor speeds.

The default value is 10000.
 .. note::
  There is unfortunately no formula to calculate a perfect decay
  mode for a given stepper motor. If you have problems with loud noises
  or the maximum motor speed is too slow, you should try to tinker with
  the decay value
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetDecay', 'get_decay'), 
'elements': [('decay', 'uint16', 1, 'out')],
'doc': ['am', {
'en':
"""
Returns the decay mode as set by :func:`SetDecay`
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
Sets the minimum voltage in mV, below which the :func:`UnderVoltage` callback
is triggered. The minimum possible value that works with the Stepper Brick is 8V.
You can use this function to detect the discharge of a battery that is used
to drive the stepper motor. If you have a fixed power supply, you likely do 
not need this functionality.

The default value is 8V.
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
Returns the minimum voltage as set by :func:`SetMinimumVoltage`.
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
This callback is triggered when the input voltage drops below the value set by
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
'elements': [('position', 'int32', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered when a position set by :func:`SetSteps` or
:func:`SetTargetPosition` is reached.

.. note::
 Since we can't get any feedback from the stepper motor, this only works if the
 acceleration (see :func:`SetSpeedRamping`) is set smaller or equal to the
 maximum acceleration of the motor. Otherwise the motor will lag behind the
 control value and the callback will be triggered too early.
""",
'de':
"""
"""
}]
})
