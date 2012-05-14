# -*- coding: utf-8 -*-

# DC Brick communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'version': [1, 0, 0],
    'type': 'Brick',
    'name': ('DC', 'dc'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for controlling DC motors',
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('SetVelocity', 'set_velocity'), 
'elements': [('velocity', 'int16', 1, 'in')], 
'doc': ['bm', {
'en':
""" 
Sets the velocity of the motor. Whereas -32767 is full speed backward,
0 is stop and 32767 is full speed forward. Depending on the 
acceleration (see :func:`SetAcceleration`), the motor is not immediately 
brought to the velocity but smoothly accelerated.

The velocity describes the duty cycle of the PWM with which the motor is
controlled, e.g. a velocity of 3277 sets a PWM with a 10% duty cycle.
You can not only control the duty cycle of the PWM but also the frequency,
see :func:`SetPWMFrequency`.

The default velocity is 0.
""",
'de':
""" 
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetVelocity', 'get_velocity'), 
'elements': [('velocity', 'int16', 1, 'out')], 
'doc': ['bm', {
'en':
"""
Returns the velocity as set by :func:`SetVelocity`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetCurrentVelocity', 'get_current_velocity'), 
'elements': [('velocity', 'int16', 1, 'out')], 
'doc': ['bm', {
'en':
"""
Returns the *current* velocity of the motor. This value is different
from :func:`GetVelocity` whenever the motor is currently accelerating
to a goal set by :func:`SetVelocity`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetAcceleration', 'set_acceleration'), 
'elements': [('acceleration', 'uint16', 1, 'in')], 
'doc': ['bm', {
'en':
"""
Sets the acceleration of the motor. It is given in *velocity/s*. An
acceleration of 10000 means, that every second the velocity is increased
by 10000 (or about 30% duty cycle).

For example: If the current velocity is 0 and you want to accelerate to a
velocity of 16000 (about 50% duty cycle) in 10 seconds, you should set
an acceleration of 1600.

If acceleration is set to 0, there is no speed ramping, i.e. a new velocity
is immediately given to the motor.

The default acceleration is 10000.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAcceleration', 'get_acceleration'), 
'elements': [('acceleration', 'uint16', 1, 'out')], 
'doc': ['bm', {
'en':
"""
Returns the acceleration as set by :func:`SetAcceleration`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetPWMFrequency', 'set_pwm_frequency'), 
'elements': [('frequency', 'uint16', 1, 'in')], 
'doc': ['am', {
'en':
"""
Sets the frequency (in Hz) of the PWM with which the motor is driven.
The possible range of the frequency is 1-20000Hz. Often a high frequency
is less noisy and the motor runs smoother. However, with a low frequency
there are less switches and therefore fewer switching losses. Also with
most motors lower frequencies enable higher torque.

If you have no idea what all this means, just ignore this function and use
the default frequency, it will very likely work fine.

The default frequency is 15 kHz.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetPWMFrequency', 'get_pwm_frequency'), 
'elements': [('frequency', 'uint16', 1, 'out')], 
'doc': ['am', {
'en':
"""
Returns the PWM frequency (in Hz) as set by :func:`SetPWMFrequency`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
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

Call :func:`SetVelocity` with 0 if you just want to stop the motor.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
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
'type': 'function',
'name': ('GetExternalInputVoltage', 'get_external_input_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')], 
'doc': ['am', {
'en':
"""
Returns the external input voltage in mV. The external input voltage is
given via the black power input connector on the DC Brick. 
 
If there is an external input voltage and a stack input voltage, the motor
will be driven by the external input voltage. If there is only a stack 
voltage present, the motor will be driven by this voltage.

 .. warning:: 
  This means, if you have a high stack voltage and a low external voltage,
  the motor will be driven with the low external voltage. If you then remove
  the external connection, it will immediately be driven by the high
  stack voltage.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetCurrentConsumption', 'get_current_consumption'), 
'elements': [('voltage', 'uint16', 1, 'out')], 
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
'type': 'function',
'name': ('Enable', 'enable'), 
'elements': [], 
'doc': ['bm', {
'en':
"""
Enables the motor. The motor can be configured (velocity, 
acceleration, etc) before it is enabled.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('Disable', 'disable'), 
'elements': [], 
'doc': ['bm', {
'en':
"""
Disables the motor. The configurations are kept (velocity, 
acceleration, etc) but the motor is not driven until it is enabled again.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
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
'type': 'function',
'name': ('SetMinimumVoltage', 'set_minimum_voltage'), 
'elements': [('voltage', 'uint16', 1, 'in')], 
'doc': ['ccm', {
'en':
"""
Sets the minimum voltage in mV, below which the :func:`UnderVoltage` callback
is triggered. The minimum possible value that works with the DC Brick is 5V.
You can use this function to detect the discharge of a battery that is used
to drive the motor. If you have a fixed power supply, you likely do not need 
this functionality.

The default value is 5V.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
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
'type': 'function',
'name': ('SetDriveMode', 'set_drive_mode'), 
'elements': [('mode', 'uint8', 1, 'in')], 
'doc': ['am', {
'en':
"""
Sets the drive mode. Possible modes are:
 * 0 = Drive/Brake
 * 1 = Drive/Coast
 
These modes are different kinds of motor controls.

In Drive/Brake mode, the motor is always either driving or braking. There
is no freewheeling. Advantages are: A more linear correlation between
PWM and velocity, more exact accelerations and the possibility to drive
with slower velocities.

In Drive/Coast mode, the motor is always either driving or freewheeling.
Advantages are: Less current consumption and less demands on the motor/driver.

The default value is 0 = Drive/Brake.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetDriveMode', 'get_drive_mode'), 
'elements': [('mode', 'uint8', 1, 'out')], 
'doc': ['am', {
'en':
"""
Returns the drive mode, as set by :func:`SetDriveMode`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetCurrentVelocityPeriod', 'set_current_velocity_period'), 
'elements': [('period', 'uint16', 1, 'in')], 
'doc': ['ccm', {
'en':
"""
Sets a period in ms with which the :func:`CurrentVelocity` callback is triggered.
A period of 0 turns the callback off.

The default value is 0.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetCurrentVelocityPeriod', 'get_current_velocity_period'), 
'elements': [('period', 'uint16', 1, 'out')], 
'doc': ['ccm', {
'en':
"""
Returns the period as set by :func:`SetCurrentVelocityPeriod`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('UnderVoltage', 'under_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')], 
'doc': ['c', {
'en':
"""
This callback is triggered when the input voltage drops below the value set by
:func:`SetMinimumVoltage`. The :word:`parameter` is the current voltage given
in mV.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('EmergencyShutdown', 'emergency_shutdown'), 
'elements': [], 
'doc': ['c', {
'en':
"""
This callback is triggered if either the current consumption
is too high (above 5A) or the temperature of the driver is too high 
(above 175°C). These two possibilities are essentially the same, since the
temperature will reach this threshold immediately if the motor draws too
much current. In case of a voltage below 3.3V (external or stack) this
callback is triggered as well.

If this callback is triggered, the driver gets disabled at the same time.
That means, :func:`Enable` has to be called to drive the motor again.

.. note::
 This callback only works in Drive/Brake mode (see :func:`SetDriveMode`). In 
 Drive/Coast mode it is unfortunately impossible to reliably read the 
 over current/over temperature signal from the driver chip.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('VelocityReached', 'velocity_reached'), 
'elements': [('velocity', 'int16', 1, 'out')], 
'doc': ['c', {
'en':
"""
This callback is triggered whenever a set velocity is reached. For example:
If a velocity of 0 is present, acceleration is set to 5000 and velocity
to 10000, :func:`VelocityReached` will be triggered after about 2 seconds, when
the set velocity is actually reached.

.. note::
 Since we can't get any feedback from the DC motor, this only works if the
 acceleration (see :func:`SetAcceleration`) is set smaller or equal to the
 maximum acceleration of the motor. Otherwise the motor will lag behind the
 control value and the callback will be triggered too early.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('CurrentVelocity', 'current_velocity'), 
'elements': [('velocity', 'int16', 1, 'out')], 
'doc': ['c', {
'en':
"""
This callback is triggered with the period that is set by
:func:`SetCurrentVelocityPeriod`. The :word:`parameter` is the *current* velocity
used by the motor.

:func:`CurrentVelocity` is only triggered after the set period if there is
a change in the velocity.
""",
'de':
"""
"""
}] 
})
