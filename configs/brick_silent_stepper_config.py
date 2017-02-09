# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Silent Stepper Brick communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Brick',
    'device_identifier': 19,
    'name': 'Silent Stepper',
    'display_name': 'Silent Stepper',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Silently drives one bipolar stepper motor with up to 46V and 1.6A per phase',
        'de': 'Steuert einen bipolaren Schrittmotor lautlos mit bis zu 46V und 1.6A pro Phase'
    },
    'released': False,
    'documented': False,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Set Max Velocity',
'elements': [('Velocity', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the maximum velocity of the stepper motor in steps per second.
This function does *not* start the motor, it merely sets the maximum
velocity the stepper motor is accelerated to. To get the motor running use
either :func:`Set Target Position`, :func:`Set Steps`, :func:`Drive Forward` or
:func:`Drive Backward`.
""",
'de':
"""
Setzt die maximale Geschwindigkeit des Schrittmotors in Schritten je Sekunde.
Diese Funktion startet *nicht* den Motor, sondern setzt nur die maximale
Geschwindigkeit auf welche der Schrittmotor beschleunigt wird. Um den Motor zu fahren
können :func:`Set Target Position`, :func:`Set Steps`, :func:`Drive Forward` oder
:func:`Drive Backward` verwendet werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Max Velocity',
'elements': [('Velocity', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the velocity as set by :func:`Set Max Velocity`.
""",
'de':
"""
Gibt die Geschwindigkeit zurück, wie von :func:`Set Max Velocity` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Current Velocity',
'elements': [('Velocity', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the *current* velocity of the stepper motor in steps per second.
""",
'de':
"""
Gibt die *aktuelle* Geschwindigkeit des Schrittmotors in Schritten je Sekunde zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Speed Ramping',
'elements': [('Acceleration', 'uint16', 1, 'in'),
             ('Deacceleration', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the acceleration and deacceleration of the stepper motor. The values
are given in *steps/s²*. An acceleration of 1000 means, that
every second the velocity is increased by 1000 *steps/s*.

For example: If the current velocity is 0 and you want to accelerate to a
velocity of 8000 *steps/s* in 10 seconds, you should set an acceleration
of 800 *steps/s²*.

An acceleration/deacceleration of 0 means instantaneous
acceleration/deacceleration (not recommended)

The default value is 1000 for both
""",
'de':
"""
Setzt die Beschleunigung und die Verzögerung des Schrittmotors. Die Werte
müssen in *Schritten/s²* angegeben werden. Eine Beschleunigung von 1000 bedeutet,
dass jede Sekunde die Geschwindigkeit um 1000 *Schritte/s* erhöht wird.

Beispiel: Wenn die aktuelle Geschwindigkeit 0 ist und es soll auf eine Geschwindigkeit
von 8000 *Schritten/s* in 10 Sekunden beschleunigt werden, muss die Beschleunigung auf
800 *Schritte/s²* gesetzt werden.

Eine Beschleunigung/Verzögerung von 0 bedeutet ein sprunghaftes Beschleunigen/Verzögern
(nicht empfohlen).

Der Standardwert ist 1000 für beide Parameter.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Speed Ramping',
'elements': [('Acceleration', 'uint16', 1, 'out'),
             ('Deacceleration', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the acceleration and deacceleration as set by
:func:`Set Speed Ramping`.
""",
'de':
"""
Gibt die Beschleunigung und Verzögerung zurück, wie von :func:`Set Speed Ramping`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Full Brake',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
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
Führt eine aktive Vollbremsung aus.

.. warning::
 Diese Funktion ist für Notsituationen bestimmt,
 in denen ein unverzüglicher Halt notwendig ist. Abhängig von der aktuellen
 Geschwindigkeit und der Kraft des Motors kann eine Vollbremsung brachial sein.

Ein Aufruf von :func:`Stop` stoppt den Motor.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Current Position',
'elements': [('Position', 'int32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the current steps of the internal step counter. This can be used to
set the current position to 0 when some kind of starting position
is reached (e.g. when a CNC machine reaches a corner).
""",
'de':
"""
Setzt den aktuellen Schrittwert des internen Schrittzählers. Dies kann
benutzt werden um die aktuelle Position auf 0 zu setzen wenn ein definierter
Startpunkt erreicht wurde (z.B. wenn eine CNC Maschine eine Ecke erreicht).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Current Position',
'elements': [('Position', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the current position of the stepper motor in steps. On startup
the position is 0. The steps are counted with all possible driving
functions (:func:`Set Target Position`, :func:`Set Steps`, :func:`Drive Forward` or
:func:`Drive Backward`). It also is possible to reset the steps to 0 or
set them to any other desired value with :func:`Set Current Position`.
""",
'de':
"""
Gibt die aktuelle Position des Schrittmotors in Schritten zurück. Nach dem
Hochfahren ist die Position 0. Die Schritte werden bei Verwendung aller möglichen
Fahrfunktionen gezählt (:func:`Set Target Position`, :func:`Set Steps`, :func:`Drive Forward` der
:func:`Drive Backward`). Es ist auch möglich den Schrittzähler auf 0 oder jeden anderen
gewünschten Wert zu setzen mit :func:`Set Current Position`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Target Position',
'elements': [('Position', 'int32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the target position of the stepper motor in steps. For example,
if the current position of the motor is 500 and :func:`Set Target Position` is
called with 1000, the stepper motor will drive 500 steps forward. It will
use the velocity, acceleration and deacceleration as set by
:func:`Set Max Velocity` and :func:`Set Speed Ramping`.

A call of :func:`Set Target Position` with the parameter *x* is equivalent to
a call of :func:`Set Steps` with the parameter
(*x* - :func:`Get Current Position`).
""",
'de':
"""
Setzt die Zielposition des Schrittmotors in Schritten. Beispiel:
Wenn die aktuelle Position des Motors 500 ist und :func:`Set Target Position` mit
1000 aufgerufen wird, dann verfährt der Schrittmotor 500 Schritte vorwärts. Dabei
wird die Geschwindigkeit, Beschleunigung und Verzögerung, wie mit
:func:`Set Max Velocity` und :func:`Set Speed Ramping` gesetzt, verwendet.

Ein Aufruf von :func:`Set Target Position` mit dem Parameter *x* ist
äquivalent mit einem Aufruf von :func:`Set Steps` mit dem Parameter
(*x* - :func:`Get Current Position`).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Target Position',
'elements': [('Position', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the last target position as set by :func:`Set Target Position`.
""",
'de':
"""
Gibt die letzte Zielposition zurück, wie von :func:`Set Target Position`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Steps',
'elements': [('Steps', 'int32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the number of steps the stepper motor should run. Positive values
will drive the motor forward and negative values backward.
The velocity, acceleration and deacceleration as set by
:func:`Set Max Velocity` and :func:`Set Speed Ramping` will be used.
""",
'de':
"""
Setzt die Anzahl der Schritte die der Schrittmotor fahren soll.
Positive Werte fahren den Motor vorwärts und negative rückwärts.
Dabei wird die Geschwindigkeit, Beschleunigung und Verzögerung, wie mit
:func:`Set Max Velocity` und :func:`Set Speed Ramping` gesetzt, verwendet.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Steps',
'elements': [('Steps', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the last steps as set by :func:`Set Steps`.
""",
'de':
"""
Gibt die letzten Schritte zurück, wie von :func:`Set Steps` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Remaining Steps',
'elements': [('Steps', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the remaining steps of the last call of :func:`Set Steps`.
For example, if :func:`Set Steps` is called with 2000 and
:func:`Get Remaining Steps` is called after the motor has run for 500 steps,
it will return 1500.
""",
'de':
"""
Gibt die verbleibenden Schritte des letzten Aufrufs von :func:`Set Steps`
zurück. Beispiel: Wenn :func:`Set Steps` mit 2000 aufgerufen wird und
:func:`Get Remaining Steps` aufgerufen wird wenn der Motor 500 Schritte fahren
hat, wird 1500 zurückgegeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Step Configuration',
'elements': [('Step Resolution', 'uint8', 1, 'in', ('Step Resolution', [('1', 8),
                                                                        ('2', 7),
                                                                        ('4', 6),
                                                                        ('8', 5),
                                                                        ('16', 4),
                                                                        ('32', 3),
                                                                        ('64', 2),
                                                                        ('128', 1),
                                                                        ('256', 0)])),
             ('Interpolation', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the step resolution from full-step up to 1/256-step.

If interpolation is turned on, the Silent Stepper Brick will always interpolate
your step inputs as 1/256-step. If you use full-step mode with interpolation, each
step will generate 256 1/256 steps.

For maximum torque use full-step without interpoltation. For maximum resolution use
1/256-step. Turn interpolation on to make the Stepper driving less noisy.

If you often change the speed with high acceleration you should turn the
interpolation off.

The default is 1/256-step with interpolation on.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Step Configuration',
'elements': [('Step Resolution', 'uint8', 1, 'out', ('Step Resolution', [('1', 8),
                                                                         ('2', 7),
                                                                         ('4', 6),
                                                                         ('8', 5),
                                                                         ('16', 4),
                                                                         ('32', 3),
                                                                         ('64', 2),
                                                                         ('128', 1),
                                                                         ('256', 0)])),
             ('Interpolation', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the step mode as set by :func:`Set Step Configuration`.
""",
'de':
"""
Gibt den Schrittmodus zurück, wie von :func:`Set Step Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Drive Forward',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Drives the stepper motor forward until :func:`Drive Backward` or
:func:`Stop` is called. The velocity, acceleration and deacceleration as
set by :func:`Set Max Velocity` and :func:`Set Speed Ramping` will be used.
""",
'de':
"""
Fährt den Schrittmotor vorwärts bis :func:`Drive Backward` oder
:func:`Stop` aufgerufen wird. Dabei wird die Geschwindigkeit,
Beschleunigung und Verzögerung, wie mit :func:`Set Max Velocity`
und :func:`Set Speed Ramping` gesetzt, verwendet.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Drive Backward',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Drives the stepper motor backward until :func:`Drive Forward` or
:func:`Stop` is triggered. The velocity, acceleration and deacceleration as
set by :func:`Set Max Velocity` and :func:`Set Speed Ramping` will be used.
""",
'de':
"""
Fährt den Schrittmotor rückwärts bis :func:`Drive Forward` oder
:func:`Stop` aufgerufen wird. Dabei wird die Geschwindigkeit,
Beschleunigung und Verzögerung, wie mit :func:`Set Max Velocity`
und :func:`Set Speed Ramping` gesetzt, verwendet.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Stop',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Stops the stepper motor with the deacceleration as set by
:func:`Set Speed Ramping`.
""",
'de':
"""
Stoppt den Schrittmotor mit der Verzögerung, wie von
:func:`Set Speed Ramping` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Stack Input Voltage',
'elements': [('Voltage', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the stack input voltage in mV. The stack input voltage is the
voltage that is supplied via the stack, i.e. it is given by a
Step-Down or Step-Up Power Supply.
""",
'de':
"""
Gibt die Eingangsspannung (in mV) des Stapels zurück. Die Eingangsspannung
des Stapel wird über diesen bereitgestellt und von einer Step-Down oder
Step-Up Power Supply erzeugt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get External Input Voltage',
'elements': [('Voltage', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
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
Gibt die externe Eingangsspannung (in mV) zurück. Die externe Eingangsspannung
wird über die schwarze Stromversorgungsbuchse, in den Stepper Brick, eingespeist.

Sobald eine externe Eingangsspannung und die Spannungsversorgung des Stapels anliegt,
wird der Motor über die externe Spannung versorgt. Sollte nur die Spannungsversorgung
des Stapels verfügbar sein, erfolgt die Versorgung des Motors über diese.

.. warning::
 Das bedeutet, bei einer hohen Versorgungsspannung des Stapels und einer geringen
 externen Versorgungsspannung erfolgt die Spannungsversorgung des Motors über die geringere
 externe Versorgungsspannung. Wenn dann die externe Spannungsversorgung getrennt wird,
 erfolgt sofort die Versorgung des Motors über die höhere Versorgungsspannung des Stapels.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Current Consumption',
'elements': [('Current', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the current consumption of the motor in mA.
""",
'de':
"""
Gibt die Stromaufnahme des Motors zurück (in mA).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Motor Current',
'elements': [('Current', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the current in mA with which the motor will be driven.
The minimum value is 360mA, the maximum value 1640mA and the
default value is 800mA.

.. warning::
 Do not set this value above the specifications of your stepper motor.
 Otherwise it may damage your motor.
""",
'de':
"""
Setzt den Strom in mA mit welchem der Motor angetrieben wird.
Der minimale Wert ist 360mA, der maximale Wert ist 1640mA und der
Standardwert ist 800mA.

.. warning::
 Dieser Wert sollte nicht über die Spezifikation des Schrittmotors gesetzt werden.
 Sonst ist eine Beschädigung des Motors möglich.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Motor Current',
'elements': [('Current', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current as set by :func:`Set Motor Current`.
""",
'de':
"""
Gibt den Strom zurück, wie von :func:`Set Motor Current` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Enable',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Enables the driver chip. The driver parameters can be configured (maximum velocity,
acceleration, etc) before it is enabled.
""",
'de':
"""
Aktiviert die Treiberstufe. Die Treiberparameter können vor der Aktivierung
konfiguriert werden (maximale Geschwindigkeit, Beschleunigung, etc.).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Disable',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Disables the driver chip. The configurations are kept (maximum velocity,
acceleration, etc) but the motor is not driven until it is enabled again.
""",
'de':
"""
Deaktiviert die Treiberstufe. Die Konfiguration (Geschwindigkeit, Beschleunigung,
etc.) bleibt erhalten aber der Motor wird nicht angesteuert bis eine erneute
Aktivierung erfolgt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is Enabled',
'elements': [('Enabled', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns *true* if the driver chip is enabled, *false* otherwise.
""",
'de':
"""
Gibt *true* zurück wenn die Treiberstufe aktiv ist, sonst *false*.
"""
}]
})










com['packets'].append({
'type': 'function',
'name': 'Set Basic Configuration',
'elements': [('Standstill Current', 'uint16', 1, 'in'), # ihold 0-31
             ('Motor Run Current', 'uint16', 1, 'in'),  # irun 0-31
             ('Standstill Delay Time', 'uint16', 1, 'in'), # ihold_delay 0-15 clk cycles
             ('Power Down Time', 'uint16', 1, 'in'), # tpowerdown 0-255
             ('Stealth Threshold', 'uint16', 1, 'in'), # tpwmthrs (in full steps/s)
             ('Coolstep Threshold', 'uint16', 1, 'in'), # tcoolthrs (in full steps/s)
             ('Classic Threshold', 'uint16', 1, 'in'), # thigh (in full steps/s)
             ('High Velocity Chopper Mode', 'bool', 1, 'in')], # vhighchm (bool)
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the basic configuration parameters for the different modes (stealth, coolstep, classic).

* Standstill Current: This value can be used to lower the current during stand still. It takes
  effect after the Power Down Time and the transition time can be controlled with the Standstill Delay
  Time. The unit is in mA and the maximum allowed value is the current motor current
  (see :func:`Set Motor Current`).

* Motor Run Current: The value is applied as a factor to the max current when the motor is
  running. Use a value of at least 16 for good microstep performance. The unit is in mA and the
  maximum allowed value is the current motor current (see :func:`Set Motor Current`).

* Standstill Delay Time: Controls the duration for motor power down after a motion
  as soon as standstill is detected and the Power Down Time is expired. A high Standstill Delay
  Time results in a smooth transition that avoids motor jerk during power down.
  The value range is 0 to 307ms

* Power Down Time: Sets the delay time after a stand still.
  The value range is 0 to 5222ms.

* Stealth Threshold: Sets the upper threshold for stealth mode in steps/s. The value range is
  0-65536 steps/s. If the velocity of the motor goes above this value, stealth mode is turned
  off. Otherwise it is turned on. In stealth mode the torque declines with high speed.

* Coolstep Threshold: Sets the lower threshold for coolstep mode in steps/s. The value range is
  0-65536 steps/s. The Coolstep Threshold needs to be above the Stealth Threshold.

* Classic Threshold: Sets the lower threshold for classic mode. The value range is
  0-65536 steps/s. In classic mode the stepper becomes more noisy, but the torque is maximized.

* High Velocity Shopper Mode: If High Velocity Shopper Mode is enabled, the stepper control
  is optimized to run the stepper motors at high velocities.


If you want to use all three thresholds make sure that
Stealth Threshold < Coolstep Threshold < Classic Threshold.

The default values are:

* Standstill Current: 200
* Motor Run Current: 800
* Standstill Delay Time: 0
* Power Down Time: 1000
* Stealth Threshold: 500
* Coolstep Threshold: 500
* Classic Threshold: 1000
* High Velocity Shopper Mode: false

""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Basic Configuration',
'elements': [('Standstill Current', 'uint16', 1, 'out'), # ihold 0-31 -> max is max motor current
             ('Motor Run Current', 'uint16', 1, 'out'),  # irun 0-31 -> max is max motor current
             ('Standstill Delay Time', 'uint16', 1, 'out'), # ihold_delay 0-15 clk cycles -> max 307 ms
             ('Power Down Time', 'uint16', 1, 'out'), # tpowerdown 0-255 -> max 5222ms
             ('Stealth Threshold', 'uint16', 1, 'out'), # tpwmthrs (in steps/s)
             ('Coolstep Threshold', 'uint16', 1, 'out'), # tcoolthrs (in steps/s)
             ('Classic Threshold', 'uint16', 1, 'out'), # thigh (in steps/s)
             ('High Velocity Chopper Mode', 'bool', 1, 'out')], # vhighchm (bool)
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the configuration as set by :func:`Set Basic Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Basic Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Spreadcycle Configuration',
'elements': [('Slow Decay Duration', 'uint8', 1, 'in'), # toff 0-15
             ('Enable Random Slow Decay', 'bool', 1, 'in'), # rndtf
             ('Fast Decay Duration', 'uint8', 1, 'in'), # hstrt and fd3 if chm=1 0-15
             ('Hysteresis Start Value', 'uint8', 1, 'in'), # hstrt if chm=0 0-7
             ('Hysteresis End Value', 'int8', 1, 'in'), # hend if chm=0 -3-12
             ('Sinewave Offset', 'int8', 1, 'in'), # hend if chm=1 -3-12
             ('Chopper Mode', 'uint8', 1, 'in', ('Chopper Mode', [('Spread Cycle', 0),
                                                                  ('Fast Decay', 1)])), # chm
             ('Comperator Blank Time', 'uint8', 1, 'in'), # tbl 0-3
             ('Fast Decay Without Comperator', 'bool', 1, 'in')], # disfdcc
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Note: If you don't know what any of this means you can very likely keep all of
the values as default!

Sets the Spreadcycle configuration parameters. (TODO: Explain spread cycle)

* Slow Decay Duration: Controls duration of off time setting of slow decay phase. The value
  range is 0-15. 0 = driver disabled, all bridges off. Use 1 only with Comperator Blank time >= 2.

* Enable Random Slow Decay: Set to false to fix chipper off time as set by Slow Decay Duration.
  If you set it to true, Decay Duration is randomly modulated.

* Fast Decay Duration: Sets the fast decay duration. The value range is 0-15. This parameters is
  only used if the Chopper Mode is set to Fast Decay.

* Hysteresis Start Value: Sets the hysteresis start value. The value range is 0-7. This parameter is
  only used if the Chopper Mode is set to Spread Cycle.

* Hysteresis End Value: Sets the hysteresis end value. The value range is -3 to 12. This parameter is
  only used if the Chopper Mode is set to Spread Cycle.

* Sinewave Offset: Sets the sinewave offset. The value range is -3 to 12. This parameters is
  only used if the Chopper Mode is set to Fast Decay. 1/512 of the value becomes added to the absolute
  value of the sinewave.

* Chopper Mode: 0 = Spread Cycle, 1 = Fast Decay.

* Comperator Blank Time: Sets the blank time of the comperator. Available values are

  * 0 = 16 clocks,
  * 1 = 24 clocks,
  * 2 = 36 clocks and
  * 3 = 54 clocks.

  A value of 1 or 2 is recommended for most applications.

* Fast Decay Without Comperator: If set to true the current comparator usage for termination of the
  fast decay cycle is disabled.


The default values are:

* Slow Decay Duration: 4
* Enable Random Slow Decay: 0
* Fast Decay Duration: 0
* Hysteresis Start Value: 0
* Hysteresis End Value: 0
* Sinewave Offset: 0
* Chopper Mode: 0
* Comperator Blank Time: 1
* Fast Decay Without Comperator: false

""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Spreadcycle Configuration',
'elements': [('Slow Decay Duration', 'uint8', 1, 'out'), # toff 0-15
             ('Enable Random Slow Decay', 'bool', 1, 'out'), # rndtf
             ('Fast Decay Duration', 'uint8', 1, 'out'), # hstrt and fd3 if chm=1 0-15
             ('Hysteresis Start Value', 'uint8', 1, 'out'), # hstrt if chm=0 0-7
             ('Hysteresis End Value', 'int8', 1, 'out'), # hend if chm=0 -3-12
             ('Sinewave Offset', 'int8', 1, 'out'), # hend if chm=1 -3-12
             ('Chopper Mode', 'uint8', 1, 'out', ('Chopper Mode', [('Spread Cycle', 0),
                                                                   ('Fast Decay', 1)])), # chm
             ('Comperator Blank Time', 'uint8', 1, 'out'), # tbl 0-3
             ('Fast Decay Without Comperator', 'bool', 1, 'out')], # disfdcc
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Basic Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Basic Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Stealth Configuration',
'elements': [('Enable Stealth', 'bool', 1, 'in'), # en_pwm_mode
             ('Amplitude', 'uint8', 1, 'in'), # pwm_ampl
             ('Gradient', 'uint8', 1, 'in'), # pwm_grad
             ('Enable Autoscale', 'bool', 1, 'in'), # pwm_autoscale
             ('Force Symmetric', 'bool', 1, 'in'), # pwm_symmetric
             ('Freewheel Mode', 'uint8', 1, 'in', ('Freewheel Mode', [('Normal', 0),
                                                                      ('Freewheeling', 1),
                                                                      ('Coil Short LS', 2),
                                                                      ('Coil Short HS', 3)]))], # freewheel
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Note: If you don't know what any of this means you can very likely keep all of
the values as default!

Sets the configuration relevant for stealth mode.

* Enable Stealth: If set to true the stealth mode is enabled, if set to false the
  stealth mode is disabled, even if the speed is below the threshold set in :func:`Set Basic Configuration`.

* Amplitude: If autoscale is disabled, the PWM amplitude is scaled by this value. If autoscale is enabled,
  this value defines the maximum PWM amplitude change per half wave. The value range is 0-255.

* Gradient: If autoscale is disabled, the PWM gradient is scaled by this value. If autoscale is enabled,
  this value defines the maximum PWM gradient. With autoscale a value above 64 is recommended,
  otherwise the regulation might not be able to measure the current. The value range is 0-255.

* Enable Autoscale: If set to true, automatic current control is used. Othwerwise the user defined
  amplitude and gradient are used.

* Force Symmetric: If true, A symmetric PWM cycle is enforced. Otherwise the PWM valuee may change within each
  PWM cycle.

* Freewheel Mode: The freewheel mode defines the behavior in stand still if the Standstill Current
  (see :func:`Set Basic Configuration`) is set to 0.

The default values are:

* Enable Stealth: true
* Amplitude: 128
* Gradient: 4
* Enable Autoscale: true
* Force Symmetric: false
* Freewheel Mode: 0 (Normal)

""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Stealth Configuration',
'elements': [('Enable Stealth', 'bool', 1, 'out'), # en_pwm_mode
             ('Amplitude', 'uint8', 1, 'out'), # pwm_ampl
             ('Gradient', 'uint8', 1, 'out'), # pwm_grad
             ('Enable Autoscale', 'bool', 1, 'out'), # pwm_autoscale
             ('Force Symmetric', 'bool', 1, 'out'), # pwm_symmetric
             ('Freewheel Mode', 'uint8', 1, 'out', ('Freewheel Mode', [('Normal', 0),
                                                                       ('Freewheeling', 1),
                                                                       ('Coil Short LS', 2),
                                                                       ('Coil Short HS', 3)]))], # freewheel (if ihold=0)
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Stealth Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Stealth Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Coolstep Configuration',
'elements': [('Minimum Stallguard Value', 'uint8', 1, 'in'), # semin 0-15
             ('Maximum Stallguard Value', 'uint8', 1, 'in'),  # semax 0-15
             ('Current Up Step Width', 'uint8', 1, 'in', ('Current Up Step Increment', [('1', 0),
                                                                                        ('2', 1),
                                                                                        ('4', 2),
                                                                                        ('8', 3)])),  # seup 0-3
             ('Current Down Step Width', 'uint8', 1, 'in', ('Current Down Step Decrement', [('1', 0),
                                                                                            ('2', 1),
                                                                                            ('8', 2),
                                                                                            ('32', 3)])),  # sedn 0-3
             ('Minimum Current', 'uint8', 1, 'in', ('Minimum Current', [('Half', 0),
                                                                        ('Quarter', 1)])),  # seimin
             ('Stallguard Threshold Value', 'int8', 1, 'in'),  # sgt -64-63
             ('Stallguard Mode', 'uint8', 1, 'in', ('Stallguard Mode', [('Standard', 0),
                                                                        ('Filtered', 1)]))], # sfilt
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Note: If you don't know what any of this means you can very likely keep all of
the values as default!

Sets the configuration relevant for coolstep.

* Minimum Stallguard Value: If the Stallguard result falls below this value*32, the motor current
  is increased to reduce motor load angle. The value range is 0-15. A value of 0 turns coolstep off.

* Maximum Stallguard Value: If the Stallguard result goes above
  (Min Stallguard Value + Max Stallguard Value + 1)*32, the motor current is decreased to save
  energy.

* Current Up Step Width: Sets the up step increment per stallguard value. The value range is 0-3,
  corresponding to the increments 1, 2, 4 and 8.

* Current Down Step Width: Sets the down step decrement per stallguard value. The value range is 0-3,
  corresponding to the decrements 1, 2, 8 and 16.

* Minimum Current: Sets the minimum current for coolstep current control. You can choose between
  half and quarter of the run current.

* Stallguard Threshold Value: Sets the level for stall output (see :func:`Get Driver Status`). The value
  range is -64 to +63. A lower value gives a higher sensitivity. You have to find a suitable value for your
  motor by trial and error, 0 works for most motors.

* Stallguard Mode: Set to 0 for standard resolution or 1 for filtered mode. In filtered mode the stallguard
  signal will be updated every four fullsteps.

The default values are:

* Minimum Stallguard Value: 2
* Maximum Stallguard Value: 10
* Current Up Step Width: 0
* Current Down Step Width: 0
* Minimum Current: 0
* Stallguard Threshold Value: 0
* Stallguard Mode: 0

""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Coolstep Configuration',
'elements': [('Minimum Stallguard Value', 'uint8', 1, 'out'), # semin 0-15
             ('Maximum Stallguard Value', 'uint8', 1, 'out'),  # semax 0-15
             ('Current Up Step Width', 'uint8', 1, 'out', ('Current Up Step Increment', [('1', 0),
                                                                                         ('2', 1),
                                                                                         ('4', 2),
                                                                                         ('8', 3)])),  # seup 0-3
             ('Current Down Step Width', 'uint8', 1, 'out', ('Current Down Step Decrement', [('1', 0),
                                                                                             ('2', 1),
                                                                                             ('8', 2),
                                                                                             ('32', 3)])),  # sedn 0-3
             ('Minimum Current', 'uint8', 1, 'out', ('Minimum Current', [('Half', 0),
                                                                         ('Quarter', 1)])),  # seimin
             ('Stallguard Threshold Value', 'int8', 1, 'out'),  # sgt -64-63
             ('Stallguard Mode', 'uint8', 1, 'out', ('Stallguard Mode', [('Standard', 0),
                                                                         ('Filtered', 1)]))], # sfilt
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Coolstep Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Coolstep Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Misc Configuration',
'elements': [('Disable Short To Ground Protection', 'bool', 1, 'in'), # diss2g
             ('Synchronize Phase Frequency', 'uint8', 1, 'in')], # sync 0=off 1-15
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Note: If you don't know what any of this means you can very likely keep all of
the values as default!

Sets miscellaneous configuration parameters.

* Disable Short To Ground Protection: Set to false to enable short to ground protection, otherwise
  it is disabled.

* Synchronize Phase Frequency: With this parameter you can synchronize the chopper for both phases
  of a two phase motor to avoid the occurrence of a beat. The value range is 0-15. If set to 0,
  the synchronization is turned off. Otherwise the synchronization is done through the formular
  f_sync = f_clk/(value*64). In Classic Mode the synchronization is automatically switched off.

The default values are:

* Disable Short To Ground Protection: 0
* Synchronize Phase Frequency: 0

""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Misc Configuration',
'elements': [('Disable Short To Ground Protection', 'bool', 1, 'out'), # diss2g
             ('Synchronize Phase Frequency', 'uint8', 1, 'out')], # sync 0=off 1-15
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Misc Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Misc Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Driver Status',
'elements': [('Open Load', 'uint8', 1, 'out', ('Open Load', [('None', 0),
                                                             ('Phase A', 1),
                                                             ('Phase B', 2),
                                                             ('Phase AB', 3)])), # ola, olb
             ('Short To Ground', 'uint8', 1, 'out', ('Short To Ground', [('None', 0),
                                                                         ('Phase A', 1),
                                                                         ('Phase B', 2),
                                                                         ('Phase AB', 3)])), # s2ga, s2gb
             ('Over Temperature', 'uint8', 1, 'out', ('Over Temperature', [('None', 0),
                                                                           ('Warning', 1),
                                                                           ('Limit', 2)])), # otpw, ot
             ('Motor Stalled', 'bool', 1, 'out'), # stallGuard
             ('Actual Motor Current', 'uint8', 1, 'out'), # CS ACTUAL
             ('Full Step Active', 'bool', 1, 'out'), # fsactive
             ('Stallguard Result', 'uint8', 1, 'out'), # SG_RESULT
             ('Stealth Voltage Amplitude', 'uint8', 1, 'out')], # PWM_SCALE
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the current driver status.

* Open Load: Indicates if an open load is present on phase A, B or both. False detection can occur in fast motion
  as well as during stand still.

* Short To Ground: Indicates if a short to ground is present on phase A, B or both. If this is detected the driver
  automatically becomes disabled and stays disabled until it is enabled again manually.

* Over Temperature: The over temperature indicator switches to "Warming" if the driver IC warms up. The warning flag
  is expected during long duration stepper uses. If the temperature limit is reached the indicator switches
  to "Limit". In this case the driver becomes disabled until it cools down again.

* Motor Stalled: Is true if a motor stall was detected.

* Actual Motor Current: Indicates the actual current control scaling as used in Coolstep mode.

* Stallguard Result: Indicates the load of the motor. A lower value signals a higher load. Per trial and error
  you can find out which value corresponds to a suitable torque for the velocity used in your application.
  After that you can use this threshold value to find out if a motor stall becomes probable and react on it (e.g.
  decrease velocity).
  During stand still this value can not be used for stall detection, it shows the chopper on-time for motor coil A.

* Stealth Voltage Amplitude: Shows the actual PWM scaling. In Stealth mode it can be used to detect motor load and
  stall if autoscale is enabled (see :func:`Set Stealth Configuration`).

""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Minimum Voltage',
'elements': [('Voltage', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the minimum voltage in mV, below which the :cb:`Under Voltage` callback
is triggered. The minimum possible value that works with the Stepper Brick is 8V.
You can use this function to detect the discharge of a battery that is used
to drive the stepper motor. If you have a fixed power supply, you likely do
not need this functionality.

The default value is 8V.
""",
'de':
"""
Setzt die minimale Spannung in mV, bei welcher der :cb:`Under Voltage` Callback
ausgelöst wird. Der kleinste mögliche Wert mit dem der Stepper Brick noch funktioniert,
ist 8V. Mit dieser Funktion kann eine Entladung der versorgenden Batterie detektiert
werden. Beim Einsatz einer Netzstromversorgung wird diese Funktionalität
höchstwahrscheinlich nicht benötigt.

Der Standardwert ist 8V.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Minimum Voltage',
'elements': [('Voltage', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the minimum voltage as set by :func:`Set Minimum Voltage`.
""",
'de':
"""
Gibt die minimale Spannung zurück, wie von :func:`Set Minimum Voltage` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Under Voltage',
'elements': [('Voltage', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the input voltage drops below the value set by
:func:`Set Minimum Voltage`. The :word:`parameter` is the current voltage given
in mV.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn die Eingangsspannung unter den, mittels
:func:`Set Minimum Voltage` gesetzten, Schwellwert sinkt. Der :word:`parameter`
ist die aktuelle Spannung in mV.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Position Reached',
'elements': [('Position', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when a position set by :func:`Set Steps` or
:func:`Set Target Position` is reached.

.. note::
 Since we can't get any feedback from the stepper motor, this only works if the
 acceleration (see :func:`Set Speed Ramping`) is set smaller or equal to the
 maximum acceleration of the motor. Otherwise the motor will lag behind the
 control value and the callback will be triggered too early.
""",
'de':
"""
Dieser Callback wird ausgelöst immer wenn eine konfigurierte Position, wie von
:func:`Set Steps` oder :func:`Set Target Position` gesetzt, erreicht wird.

.. note::
 Da es nicht möglich ist eine Rückmeldung vom Schrittmotor zu erhalten,
 funktioniert dies nur wenn die konfigurierte Beschleunigung (siehe :func:`Set Speed Ramping`)
 kleiner oder gleich der maximalen Beschleunigung des Motors ist. Andernfalls
 wird der Motor hinter dem Vorgabewert zurückbleiben und der Callback wird
 zu früh ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Time Base',
'elements': [('Time Base', 'uint32', 1, 'in')],
'since_firmware': [1, 1, 6],
'doc': ['af', {
'en':
"""
Sets the time base of the velocity and the acceleration of the stepper brick
(in seconds).

For example, if you want to make one step every 1.5 seconds, you can set
the time base to 15 and the velocity to 10. Now the velocity is
10steps/15s = 1steps/1.5s.

The default value is 1.
""",
'de':
"""
Setzt die Zeitbasis der Geschwindigkeit und Beschleunigung des Stepper Brick
(in Sekunden).

Beispiel: Wenn aller 1,5 Sekunden ein Schritt gefahren werden soll, kann
die Zeitbasis auf 15 und die Geschwindigkeit auf 10 gesetzt werden. Damit ist die
Geschwindigkeit 10Schritte/15s = 1Schritt/1,5s.

Der Standardwert ist 1.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Time Base',
'elements': [('Time Base', 'uint32', 1, 'out')],
'since_firmware': [1, 1, 6],
'doc': ['af', {
'en':
"""
Returns the time base as set by :func:`Set Time Base`.
""",
'de':
"""
Gibt die Zeitbasis zurück, wie von :func:`Set Time Base` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get All Data',
'elements': [('Current Velocity', 'uint16', 1, 'out'),
             ('Current Position', 'int32', 1, 'out'),
             ('Remaining Steps', 'int32', 1, 'out'),
             ('Stack Voltage', 'uint16', 1, 'out'),
             ('External Voltage', 'uint16', 1, 'out'),
             ('Current Consumption', 'uint16', 1, 'out')],
'since_firmware': [1, 1, 6],
'doc': ['af', {
'en':
"""
Returns the following :word:`parameters`: The current velocity,
the current position, the remaining steps, the stack voltage, the external
voltage and the current consumption of the stepper motor.

There is also a callback for this function, see :cb:`All Data` callback.
""",
'de':
"""
Gibt die folgenden :word:`parameters` zurück: Die aktuelle
Geschwindigkeit, die aktuelle Position, die verbleibenden Schritte,
die Spannung des Stapels, die externe Spannung und der aktuelle Stromverbrauch
des Schrittmotors.

Es existiert auch ein Callback für diese Funktion, siehe :cb:`All Data`
Callback.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set All Data Period',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 1, 6],
'doc': ['ccf', {
'en':
"""
Sets the period in ms with which the :cb:`All Data` callback is triggered
periodically. A value of 0 turns the callback off.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :cb:`AllData` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get All Data Period',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 1, 6],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set All Data Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set All Data Period` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'All Data',
'elements': [('Current Velocity', 'uint16', 1, 'out'),
             ('Current Position', 'int32', 1, 'out'),
             ('Remaining Steps', 'int32', 1, 'out'),
             ('Stack Voltage', 'uint16', 1, 'out'),
             ('External Voltage', 'uint16', 1, 'out'),
             ('Current Consumption', 'uint16', 1, 'out')],
'since_firmware': [1, 1, 6],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`Set All Data Period`. The :word:`parameters` are: the current velocity,
the current position, the remaining steps, the stack voltage, the external
voltage and the current consumption of the stepper motor.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`Set All Data Period`,
ausgelöst. Die :word:`parameters` sind die aktuelle Geschwindigkeit,
die aktuelle Position, die verbleibenden Schritte, die Spannung des Stapels, die
externe Spannung und der aktuelle Stromverbrauch des Schrittmotors.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'New State',
'elements': [('State New',      'uint8', 1, 'out', ('State', [('Stop', 1),
                                                              ('Acceleration', 2),
                                                              ('Run', 3),
                                                              ('Deacceleration', 4),
                                                              ('Direction Change To Forward', 5),
                                                              ('Direction Change To Backward', 6)])),
             ('State Previous', 'uint8', 1, 'out', ('State', [('Stop', 1),
                                                              ('Acceleration', 2),
                                                              ('Run', 3),
                                                              ('Deacceleration', 4),
                                                              ('Direction Change To Forward', 5),
                                                              ('Direction Change To Backward', 6)]))],
'since_firmware': [1, 1, 6],
'doc': ['c', {
'en':
"""
This callback is triggered whenever the Stepper Brick enters a new state.
It returns the new state as well as the previous state.
""",
'de':
"""
Dieser Callback wird immer dann ausgelöst wenn der Stepper Brick einen
neuen Zustand erreicht. Es wird sowohl der neue wie auch der alte Zustand
zurückgegeben.
"""
}]
})

com['examples'].append({
'name': 'Configuration',
'functions': [('setter', 'Set Motor Current', [('uint16', 800)], None, '800mA'),
#              ('setter', 'Set Step Mode', [('uint8', 8)], None, '1/8 step mode'),
              ('setter', 'Set Max Velocity', [('uint16', 2000)], None, 'Velocity 2000 steps/s'),
              ('setter', 'Set Speed Ramping', [('uint16', 500), ('uint16', 5000)], 'Slow acceleration (500 steps/s^2),\nFast deacceleration (5000 steps/s^2)', None),
              ('empty',),
              ('setter', 'Enable', [], None, 'Enable motor power'),
              ('setter', 'Set Steps', [('int32', 60000)], None, 'Drive 60000 steps forward'),
              ('wait',)],
'cleanups': [('setter', 'Disable', [], None, None)]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Position Reached', 'position reached'), [(('Position', 'Position'), 'int32', None, None, None, None)], 'Use position reached callback to program random movement', None),
              ('empty',),
              ('setter', 'Enable', [], None, 'Enable motor power'),
              ('setter', 'Set Steps', [('int32', 1)], None, 'Drive one step forward to get things going')],
'cleanups': [('setter', 'Disable', [], None, None)],
'incomplete': True # because of special random movement logic in callback
})
