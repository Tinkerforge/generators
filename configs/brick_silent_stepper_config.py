# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Silent Stepper Brick communication config

from openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'category': 'Brick',
    'device_identifier': 19,
    'name': 'Silent Stepper',
    'display_name': 'Silent Stepper',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Silently drives one bipolar stepper motor with up to 46V and 1.6A per phase',
        'de': 'Steuert einen bipolaren Schrittmotor lautlos mit bis zu 46V und 1.6A pro Phase'
    },
    'released': True,
    'documented': True,
    'discontinued': False,
    'features': [
        'brick_get_identity',
        'brick_status_led',
        'brick_reset',
        'brick_chip_temperature',
        'send_timeout_count',
        'eeprom_bricklet_host_2_ports',
        'comcu_bricklet_host',
        'comcu_bricklet_host_2_ports',
        'standard_bricklet_host_2_ports'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append({
'name': 'Step Resolution',
'type': 'uint8',
'constants': [('1', 8),
              ('2', 7),
              ('4', 6),
              ('8', 5),
              ('16', 4),
              ('32', 3),
              ('64', 2),
              ('128', 1),
              ('256', 0)]
})

com['constant_groups'].append({
'name': 'Chopper Mode',
'type': 'uint8',
'constants': [('Spread Cycle', 0),
              ('Fast Decay', 1)]
})

com['constant_groups'].append({
'name': 'Freewheel Mode',
'type': 'uint8',
'constants': [('Normal', 0),
              ('Freewheeling', 1),
              ('Coil Short LS', 2),
              ('Coil Short HS', 3)]
})

com['constant_groups'].append({
'name': 'Current Up Step Increment',
'type': 'uint8',
'constants': [('1', 0),
              ('2', 1),
              ('4', 2),
              ('8', 3)]
})

com['constant_groups'].append({
'name': 'Current Down Step Decrement',
'type': 'uint8',
'constants': [('1', 0),
              ('2', 1),
              ('8', 2),
              ('32', 3)]
})

com['constant_groups'].append({
'name': 'Minimum Current',
'type': 'uint8',
'constants': [('Half', 0),
              ('Quarter', 1)]
})

com['constant_groups'].append({
'name': 'Stallguard Mode',
'type': 'uint8',
'constants': [('Standard', 0),
              ('Filtered', 1)]
})

com['constant_groups'].append({
'name': 'Open Load',
'type': 'uint8',
'constants': [('None', 0),
              ('Phase A', 1),
              ('Phase B', 2),
              ('Phase AB', 3)]
})

com['constant_groups'].append({
'name': 'Short To Ground',
'type': 'uint8',
'constants': [('None', 0),
              ('Phase A', 1),
              ('Phase B', 2),
              ('Phase AB', 3)]
})

com['constant_groups'].append({
'name': 'Over Temperature',
'type': 'uint8',
'constants': [('None', 0),
              ('Warning', 1),
              ('Limit', 2)]
})

com['constant_groups'].append({
'name': 'State',
'type': 'uint8',
'constants': [('Stop', 1),
              ('Acceleration', 2),
              ('Run', 3),
              ('Deacceleration', 4),
              ('Direction Change To Forward', 5),
              ('Direction Change To Backward', 6)]
})

com['packets'].append({
'type': 'function',
'name': 'Set Max Velocity',
'elements': [('Velocity', 'uint16', 1, 'in', {'unit': 'Steps Per Second'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the maximum velocity of the stepper motor.
This function does *not* start the motor, it merely sets the maximum
velocity the stepper motor is accelerated to. To get the motor running use
either :func:`Set Target Position`, :func:`Set Steps`, :func:`Drive Forward` or
:func:`Drive Backward`.
""",
'de':
"""
Setzt die maximale Geschwindigkeit des Schrittmotors.
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
'elements': [('Velocity', 'uint16', 1, 'out', {'unit': 'Steps Per Second'})],
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
'elements': [('Velocity', 'uint16', 1, 'out', {'unit': 'Steps Per Second'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the *current* velocity of the stepper motor.
""",
'de':
"""
Gibt die *aktuelle* Geschwindigkeit des Schrittmotors zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Speed Ramping',
'elements': [('Acceleration', 'uint16', 1, 'in', {'unit': 'Steps Per Second Squared', 'default': 1000}),
             ('Deacceleration', 'uint16', 1, 'in', {'unit': 'Steps Per Second Squared', 'default': 1000})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the acceleration and deacceleration of the stepper motor.
An acceleration of 1000 means, that
every second the velocity is increased by 1000 *steps/s*.

For example: If the current velocity is 0 and you want to accelerate to a
velocity of 8000 *steps/s* in 10 seconds, you should set an acceleration
of 800 *steps/s²*.

An acceleration/deacceleration of 0 means instantaneous
acceleration/deacceleration (not recommended)
""",
'de':
"""
Setzt die Beschleunigung und die Verzögerung des Schrittmotors.
Eine Beschleunigung von 1000 bedeutet,
dass jede Sekunde die Geschwindigkeit um 1000 *Schritte/s* erhöht wird.

Beispiel: Wenn die aktuelle Geschwindigkeit 0 ist und es soll auf eine Geschwindigkeit
von 8000 *Schritten/s* in 10 Sekunden beschleunigt werden, muss die Beschleunigung auf
800 *Schritte/s²* gesetzt werden.

Eine Beschleunigung/Verzögerung von 0 bedeutet ein sprunghaftes Beschleunigen/Verzögern
(nicht empfohlen).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Speed Ramping',
'elements': [('Acceleration', 'uint16', 1, 'out', {'unit': 'Steps Per Second Squared', 'default': 1000}),
             ('Deacceleration', 'uint16', 1, 'out', {'unit': 'Steps Per Second Squared', 'default': 1000})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the acceleration and deacceleration as set by
:func:`Set Speed Ramping`.
""",
'de':
"""
Gibt die Beschleunigung und Verzögerung zurück, wie von :func:`Set Speed Ramping` gesetzt.
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
'elements': [('Position', 'int32', 1, 'in', {})],
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
'elements': [('Position', 'int32', 1, 'out', {})],
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
'elements': [('Position', 'int32', 1, 'in', {})],
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
'elements': [('Position', 'int32', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the last target position as set by :func:`Set Target Position`.
""",
'de':
"""
Gibt die letzte Zielposition zurück, wie von :func:`Set Target Position` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Steps',
'elements': [('Steps', 'int32', 1, 'in', {})],
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
'elements': [('Steps', 'int32', 1, 'out', {})],
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
'elements': [('Steps', 'int32', 1, 'out', {})],
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
'elements': [('Step Resolution', 'uint8', 1, 'in', {'constant_group': 'Step Resolution', 'default': 0}),
             ('Interpolation', 'bool', 1, 'in', {'default': True})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the step resolution from full-step up to 1/256-step.

If interpolation is turned on, the Silent Stepper Brick will always interpolate
your step inputs as 1/256-step. If you use full-step mode with interpolation, each
step will generate 256 1/256 steps.

For maximum torque use full-step without interpolation. For maximum resolution use
1/256-step. Turn interpolation on to make the Stepper driving less noisy.

If you often change the speed with high acceleration you should turn the
interpolation off.
""",
'de':
"""
Setzt die Schrittauflösung von Vollschritt bis zu 1/256 Schritt.

Wenn Interpolation aktiviert ist, führt der Silent Stepper Brick immer 1/256
interpolierte Schritte aus. Wenn zum Beispiel Vollschritt mit Interpolation
genutzt wird, führt jeder Schritt zu 256 1/256 Schritten beim Motor.

Für einen maximalen Drehmoment sollte Vollschritt mit Interpolation genutzt
werden. Für maximale Auflösung sollte 1/256 Schritt genutzt werden.
Interpolation führt auch dazu, dass der Motor weniger Geräusche erzeugt.

Für den Fall, dass oft die Geschwindigkeit mit sehr hohen Beschleunigungen
geändert wird, sollte Interpolation ausgeschaltet werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Step Configuration',
'elements': [('Step Resolution', 'uint8', 1, 'out', {'constant_group': 'Step Resolution'}),
             ('Interpolation', 'bool', 1, 'out', {'default': True})],
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
'elements': [('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the stack input voltage. The stack input voltage is the
voltage that is supplied via the stack, i.e. it is given by a
Step-Down or Step-Up Power Supply.
""",
'de':
"""
Gibt die Eingangsspannung des Stapels zurück. Die Eingangsspannung
des Stapel wird über diesen bereitgestellt und von einer Step-Down oder
Step-Up Power Supply erzeugt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get External Input Voltage',
'elements': [('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the external input voltage. The external input voltage is
given via the black power input connector on the Silent Stepper Brick.

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
Gibt die externe Eingangsspannung zurück. Die externe Eingangsspannung
wird über die schwarze Stromversorgungsbuchse, in den Silent Stepper Brick,
eingespeist.

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
'function_id': 22,
'name': 'Set Motor Current',
'elements': [('Current', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Ampere', 'range': (360, 1640), 'default': 800})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the current with which the motor will be driven.

.. warning::
 Do not set this value above the specifications of your stepper motor.
 Otherwise it may damage your motor.
""",
'de':
"""
Setzt den Strom mit welchem der Motor angetrieben wird.

.. warning::
 Dieser Wert sollte nicht über die Spezifikation des Schrittmotors gesetzt werden.
 Sonst ist eine Beschädigung des Motors möglich.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Motor Current',
'elements': [('Current', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere', 'range': (360, 1640), 'default': 800})],
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
'elements': [('Enabled', 'bool', 1, 'out', {})],
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
'elements': [('Standstill Current', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Ampere', 'default': 200}),
             ('Motor Run Current', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Ampere', 'default': 800}),
             ('Standstill Delay Time', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'range': (0, 307), 'default': 0}),
             ('Power Down Time', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'range': (0, 5222), 'default': 1000}),
             ('Stealth Threshold', 'uint16', 1, 'in', {'unit': 'Steps Per Second', 'default': 500}),
             ('Coolstep Threshold', 'uint16', 1, 'in', {'unit': 'Steps Per Second', 'default': 500}),
             ('Classic Threshold', 'uint16', 1, 'in', {'unit': 'Steps Per Second', 'default': 1000}),
             ('High Velocity Chopper Mode', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the basic configuration parameters for the different modes (Stealth, Coolstep, Classic).

* Standstill Current: This value can be used to lower the current during stand still. This might
  be reasonable to reduce the heating of the motor and the Brick. When the motor is in standstill
  the configured motor phase current will be driven until the configured
  Power Down Time is elapsed. After that the phase current will be reduced to the standstill
  current. The elapsed time for this reduction can be configured with the Standstill Delay Time.
  The maximum allowed value is the configured maximum motor current
  (see :func:`Set Motor Current`).

* Motor Run Current: The value sets the motor current when the motor is running.
  Use a value of at least one half of the global maximum motor current for a good
  microstep performance. The maximum allowed value is the current
  motor current. The API maps the entered value to 1/32 ... 32/32 of the maximum
  motor current. This value should be used to change the motor current during motor movement,
  whereas the global maximum motor current should not be changed while the motor is moving
  (see :func:`Set Motor Current`).

* Standstill Delay Time: Controls the duration for motor power down after a motion
  as soon as standstill is detected and the Power Down Time is expired. A high Standstill Delay
  Time results in a smooth transition that avoids motor jerk during power down.

* Power Down Time: Sets the delay time after a stand still.

* Stealth Threshold: Sets the upper threshold for Stealth mode.
  If the velocity of the motor goes above this value, Stealth mode is turned
  off. Otherwise it is turned on. In Stealth mode the torque declines with high speed.

* Coolstep Threshold: Sets the lower threshold for Coolstep mode.
  The Coolstep Threshold needs to be above the Stealth Threshold.

* Classic Threshold: Sets the lower threshold for classic mode.
  In classic mode the stepper becomes more noisy, but the torque is maximized.

* High Velocity Chopper Mode: If High Velocity Chopper Mode is enabled, the stepper control
  is optimized to run the stepper motors at high velocities.

If you want to use all three thresholds make sure that
Stealth Threshold < Coolstep Threshold < Classic Threshold.
""",
'de':
"""
Setzt die Basiskonfiguration-Parameter für verschiedene Modi (Stealth, Coolstep, Classic).

* Standstill Current: Mit diesem Wert kann der Phasenstrom im Stillstand
  reduziert werden. Dies ist zum Beispiel sinnvoll um das Aufheizen des Motors
  zu verringern. Wenn der Motor steht wird dieser mit dem eingestellte
  Phasenstrom betrieben bis die eingestellte Power Down Time um ist. Danach
  wird der Phasenstrom schrittweise bis zum Standstill Current reduziert. Die
  dafür benötigte Zeit wird mittels Power Down Time eingestellt.
  Der eingestellte Phasenstrom ist das Maximum für diesen Wert
  (see :func:`Set Motor Current`).

* Motor Run Current: Dieser Wert setzt den Phasenstrom, wenn der Motor sich dreht.
  Ein Wert von mindestens der Hälfte des maximalen Phasenstrom sollte für gute
  Ergebnisse im Mikroschrittbetrieb gesetzt werden. Der maximal
  zulässige Wert ist der maximale Phasenstrom. Der eingegebene Wert wird von der API intern
  in einen Faktor im Bereich von 1/32 ... 32/32 umgerechnet, mit dem der Phasenstrom
  begrenzt wird. Der maximale Phasenstrom sollte im laufenden Betrieb nicht geändert werden.
  Für eine Änderung im laufenden Betrieb ist dieser Wert da (see :func:`Set Motor Current`).

* Standstill Delay Time:
  Steuert die Zeit für das Verringern des Motorstroms bis zum
  Standstill Current. Eine hohe Standstill Delay Time führt zu einem ruhigen und
  ruckelfreien Übergang.

* Power Down Time: Setzt die Wartezeit nach dem Stehenbleiben.

* Stealth Threshold: Setzt den oberen Grenzwert für den Stealth Modus.
  Wenn die Geschwindigkeit des Motors über diesem Wert liegt wird
  der Stealth Modus abgeschaltet. Ansonsten angeschaltet. Im Stealth Modus nimmt das Drehmoment mit
  steigender Geschwindigkeit ab.

* Coolstep Threshold: Setzt den unteren Grenzwert für den Coolstep Modus.
  Der Coolstep Grenzwert muss über dem Stealth Grenzwert liegen.

* Classic Threshold:  Sets den unteren Grenzwert für den Classic Modus.
  Im Classic Modus wird der Schrittmotor geräuschvoll aber das Drehmoment wird
  maximiert.

* High Velocity Chopper Mode: Wenn der High Velocity Chopper Modus aktiviert wird, optimiert der
  Schrittmotortreiber die Ansteuerung des Motors für hohe Geschwindigkeiten.

Wenn alle drei Grenzwerte (Thresholds) genutzt werden sollen muss sichergestellt werden,
dass Stealth Threshold < Coolstep Threshold < Classic Threshold.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Basic Configuration',
'elements': [('Standstill Current', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere', 'default': 200}),
             ('Motor Run Current', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere', 'default': 800}),
             ('Standstill Delay Time', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'range': (0, 307), 'default': 0}),
             ('Power Down Time', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'range': (0, 5222), 'default': 1000}),
             ('Stealth Threshold', 'uint16', 1, 'out', {'unit': 'Steps Per Second', 'default': 500}),
             ('Coolstep Threshold', 'uint16', 1, 'out', {'unit': 'Steps Per Second', 'default': 500}),
             ('Classic Threshold', 'uint16', 1, 'out', {'unit': 'Steps Per Second', 'default': 1000}),
             ('High Velocity Chopper Mode', 'bool', 1, 'out', {'default': False})],
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
'elements': [('Slow Decay Duration', 'uint8', 1, 'in', {'range': (0, 15), 'default': 4}), # toff 0-15
             ('Enable Random Slow Decay', 'bool', 1, 'in', {'default': False}), # rndtf
             ('Fast Decay Duration', 'uint8', 1, 'in', {'range': (0, 15), 'default': 0}), # hstrt and fd3 if chm=1 0-15
             ('Hysteresis Start Value', 'uint8', 1, 'in', {'range': (0, 7), 'default': 0}), # hstrt if chm=0 0-7
             ('Hysteresis End Value', 'int8', 1, 'in', {'range': (-3, 12), 'default': 0}), # hend if chm=0 -3-12
             ('Sine Wave Offset', 'int8', 1, 'in', {'range': (-3, 12), 'default': 0}), # hend if chm=1 -3-12
             ('Chopper Mode', 'uint8', 1, 'in', {'constant_group': 'Chopper Mode', 'default': 0}), # chm
             ('Comparator Blank Time', 'uint8', 1, 'in', {'range': (0, 3), 'default': 1}), # tbl 0-3
             ('Fast Decay Without Comparator', 'bool', 1, 'in', {'default': False})], # disfdcc
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Note: If you don't know what any of this means you can very likely keep all of
the values as default!

Sets the Spreadcycle configuration parameters. Spreadcycle is a chopper algorithm which actively
controls the motor current flow. More information can be found in the TMC2130 datasheet on page
47 (7 spreadCycle and Classic Chopper).

* Slow Decay Duration: Controls duration of off time setting of slow decay phase.
  0 = driver disabled, all bridges off. Use 1 only with Comparator Blank time >= 2.

* Enable Random Slow Decay: Set to false to fix chopper off time as set by Slow Decay Duration.
  If you set it to true, Decay Duration is randomly modulated.

* Fast Decay Duration: Sets the fast decay duration. This parameters is
  only used if the Chopper Mode is set to Fast Decay.

* Hysteresis Start Value: Sets the hysteresis start value. This parameter is
  only used if the Chopper Mode is set to Spread Cycle.

* Hysteresis End Value: Sets the hysteresis end value. This parameter is
  only used if the Chopper Mode is set to Spread Cycle.

* Sine Wave Offset: Sets the sine wave offset. This parameters is
  only used if the Chopper Mode is set to Fast Decay. 1/512 of the value becomes added to the absolute
  value of the sine wave.

* Chopper Mode: 0 = Spread Cycle, 1 = Fast Decay.

* Comparator Blank Time: Sets the blank time of the comparator. Available values are

  * 0 = 16 clocks,
  * 1 = 24 clocks,
  * 2 = 36 clocks and
  * 3 = 54 clocks.

  A value of 1 or 2 is recommended for most applications.

* Fast Decay Without Comparator: If set to true the current comparator usage for termination of the
  fast decay cycle is disabled.
""",
'de':
"""
Note: Typischerweise können diese Werte bei ihren Standardwerten gelassen werden. Sie sollten nur
geändert werden, wenn man weiß was man tut.

Setzt die Spreadcycle Konfigurationsparameter. Spreadcycle ist ein  Chopper-Algorithmus der aktiv
den Motorstrom regelt. Weitere Informationen dazu können im TMC2130 Datenblatt auf Seite
47 (7 spreadCycle and Classic Chopper) gefunden werden.

* Slow Decay Duration: Steuert die Aus-Zeit (off time) in der Slow Decay Phase.
  0 = Treiber deaktiviert, alle Brücken aus. Nur wenn die Comparator Blank Time >=2
  ist sollte ein Wert von 1 gesetzt werden.

* Enable Random Slow Decay: Muss auf False gesetzt werden um die Aus-Zeit (off time) des Choppers
  auf die gesetzte Slow Decay Duration zu setzen. Wenn dieser Wert auf True gesetzt wird, wird die
  Decay Dauer zufällig variiert.

* Fast Decay Duration: Setzt die Fast Decay Dauer. Dieser Parameter
  wird nur benutzt, wenn der Spread Cycle als Chopper Modus genutzt wird.

* Hysteresis Start Value: Setzt der Startwert der Hysterese. Dieser Parameter
  wird nur benutzt, wenn der Spread Cycle als Chopper Modus genutzt wird.

* Hysteresis End Value: Setzt den Endwert der Hysterese. Dieser Parameter
  wird nur benutzt, wenn der Spread Cycle als Chopper Modus genutzt wird.

* Sinewave Offset: Setzt den Sinuswellen Offset. Der Wert wird nur benutzt,
  wenn als Chopper Modus Fast Decay benutzt wird. 1/512 dieses Werts wird zum Absolutwert der Sinuswelle
  hinzuaddiert.

* Chopper Mode: 0 = Spread Cycle, 1 = Fast Decay.

* Comperator Blank Time: Setzt die Totzeit von Komparator. Mögliche Werte sind

  * 0 = 16 Takte,
  * 1 = 24 Takte,
  * 2 = 36 Takte und
  * 3 = 54 Takte.

  Ein Wert von 1 oder 2 wird für die meisten Anwendungen empfohlen.

* Fast Decay Without Comperator: Wenn dieser Wert auf True gesetzt wird, dann wird der Strom-Komparator nicht
  im Fast Decay Modus genutzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Spreadcycle Configuration',
'elements': [('Slow Decay Duration', 'uint8', 1, 'out', {'range': (0, 15), 'default': 4}), # toff 0-15
             ('Enable Random Slow Decay', 'bool', 1, 'out', {'default': False}), # rndtf
             ('Fast Decay Duration', 'uint8', 1, 'out', {'range': (0, 15), 'default': 0}), # hstrt and fd3 if chm=1 0-15
             ('Hysteresis Start Value', 'uint8', 1, 'out', {'range': (0, 7), 'default': 0}), # hstrt if chm=0 0-7
             ('Hysteresis End Value', 'int8', 1, 'out', {'range': (-3, 12), 'default': 0}), # hend if chm=0 -3-12
             ('Sine Wave Offset', 'int8', 1, 'out', {'range': (-3, 12), 'default': 0}), # hend if chm=1 -3-12
             ('Chopper Mode', 'uint8', 1, 'out', {'constant_group': 'Chopper Mode', 'default': 0}), # chm
             ('Comparator Blank Time', 'uint8', 1, 'out', {'range': (0, 3), 'default': 1}), # tbl 0-3
             ('Fast Decay Without Comparator', 'bool', 1, 'out', {'default': False})], # disfdcc
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
'elements': [('Enable Stealth', 'bool', 1, 'in', {'default': True}), # en_pwm_mode
             ('Amplitude', 'uint8', 1, 'in', {'default': 128}), # pwm_ampl
             ('Gradient', 'uint8', 1, 'in', {'default': 4}), # pwm_grad
             ('Enable Autoscale', 'bool', 1, 'in', {'default': True}), # pwm_autoscale
             ('Force Symmetric', 'bool', 1, 'in', {'default': False}), # pwm_symmetric
             ('Freewheel Mode', 'uint8', 1, 'in', {'constant_group': 'Freewheel Mode', 'default': 0})], # freewheel
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Note: If you don't know what any of this means you can very likely keep all of
the values as default!

Sets the configuration relevant for Stealth mode.

* Enable Stealth: If set to true the stealth mode is enabled, if set to false the
  stealth mode is disabled, even if the speed is below the threshold set in :func:`Set Basic Configuration`.

* Amplitude: If autoscale is disabled, the PWM amplitude is scaled by this value. If autoscale is enabled,
  this value defines the maximum PWM amplitude change per half wave.

* Gradient: If autoscale is disabled, the PWM gradient is scaled by this value. If autoscale is enabled,
  this value defines the maximum PWM gradient. With autoscale a value above 64 is recommended,
  otherwise the regulation might not be able to measure the current.

* Enable Autoscale: If set to true, automatic current control is used. Otherwise the user defined
  amplitude and gradient are used.

* Force Symmetric: If true, A symmetric PWM cycle is enforced. Otherwise the PWM value may change within each
  PWM cycle.

* Freewheel Mode: The freewheel mode defines the behavior in stand still if the Standstill Current
  (see :func:`Set Basic Configuration`) is set to 0.
""",
'de':
"""
Note: Typischerweise können diese Werte bei ihren Standardwerten gelassen werden. Sie sollten nur
geändert werden, wenn man weiß was man tut.

Setzt die Konfigurationsparameter für den Stealth Modus.

* Enable Stealth: Stealth Modus wird aktiviert, wenn dieser Wert auf True gesetzt wird. Ansonsten ist
  der Modus deaktiviert auch wenn die Geschwindigkeit des Motors unter dem Grenzwert, der mittels
  :func:`Set Basic Configuration` gesetzt wurde, liegt.

* Amplitude: Wenn Autoscale aktiviert wurde, wird die PWM Amplitude mit diesem Wert skaliert.
  Wenn autoscale deaktiviert ist, definiert dieser Wert die maximale PWM Amplitudenänderungen pro Halbwelle.

* Gradient: Wenn Autoscale deaktiviert wurde, wird der PWM Steigung (Gradient) bei diesem Wert skaliert. Wird
  Autoscale aktiviert, definiert dieser Wert die maximale PWM Steigung. Mit Autoscale wird ein Wert
  über 64 empfohlen, ansonsten kann es sein, dass die Regelung den Strom nicht korrekt messen kann.

* Enable Autoscale: Die automatische Stromregelung ist aktiviert, wenn dieser Wert auf True gesetzt wird.
  Ansonsten werden die vom Nutzer definierten Amplituden und Steigungen genutzt.

* Force Symmetric: Wenn auf True gesetzt wird, dann wird ein symmetrisches PWM erzwungen. Ansonsten kann
  sich der PWM Wert innerhalb eines PWM Taktes ändern.

* Freewheel Mode: Der Freewheel Modus definiert das Verhalten im Stillstand, wenn der Standstill Current
  (siehe :func:`Set Basic Configuration`) auf 0 gesetzt wurde.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Stealth Configuration',
'elements': [('Enable Stealth', 'bool', 1, 'out', {'default': True}), # en_pwm_mode
             ('Amplitude', 'uint8', 1, 'out', {'default': 128}), # pwm_ampl
             ('Gradient', 'uint8', 1, 'out', {'default': 4}), # pwm_grad
             ('Enable Autoscale', 'bool', 1, 'out', {'default': True}), # pwm_autoscale
             ('Force Symmetric', 'bool', 1, 'out', {'default': False}), # pwm_symmetric
             ('Freewheel Mode', 'uint8', 1, 'out', {'constant_group': 'Freewheel Mode', 'default': 0})], # freewheel
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
'elements': [('Minimum Stallguard Value', 'uint8', 1, 'in', {'range': (0, 15), 'default': 2}), # semin 0-15
             ('Maximum Stallguard Value', 'uint8', 1, 'in', {'range': (0, 15), 'default': 10}), # semax 0-15
             ('Current Up Step Width', 'uint8', 1, 'in', {'constant_group': 'Current Up Step Increment', 'default': 0}), # seup 0-3
             ('Current Down Step Width', 'uint8', 1, 'in', {'constant_group': 'Current Down Step Decrement', 'default': 0}), # sedn 0-3
             ('Minimum Current', 'uint8', 1, 'in', {'constant_group': 'Minimum Current', 'default': 0}), # seimin
             ('Stallguard Threshold Value', 'int8', 1, 'in', {'range': (-64, 63), 'default': 0}), # sgt -64-63
             ('Stallguard Mode', 'uint8', 1, 'in', {'constant_group': 'Stallguard Mode', 'default': 0})], # sfilt
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Note: If you don't know what any of this means you can very likely keep all of
the values as default!

Sets the configuration relevant for Coolstep.

* Minimum Stallguard Value: If the Stallguard result falls below this value*32, the motor current
  is increased to reduce motor load angle. A value of 0 turns Coolstep off.

* Maximum Stallguard Value: If the Stallguard result goes above
  (Min Stallguard Value + Max Stallguard Value + 1) * 32, the motor current is decreased to save
  energy.

* Current Up Step Width: Sets the up step increment per Stallguard value. The value range is 0-3,
  corresponding to the increments 1, 2, 4 and 8.

* Current Down Step Width: Sets the down step decrement per Stallguard value. The value range is 0-3,
  corresponding to the decrements 1, 2, 8 and 16.

* Minimum Current: Sets the minimum current for Coolstep current control. You can choose between
  half and quarter of the run current.

* Stallguard Threshold Value: Sets the level for stall output (see :func:`Get Driver Status`).
  A lower value gives a higher sensitivity. You have to find a suitable value for your
  motor by trial and error, 0 works for most motors.

* Stallguard Mode: Set to 0 for standard resolution or 1 for filtered mode. In filtered mode the Stallguard
  signal will be updated every four full-steps.
""",
'de':
"""
Note: Typischerweise können diese Werte bei ihren Standardwerten gelassen werden. Sie sollten nur
geändert werden, wenn man weiß was man tut.

Setzt die Konfigurationsparameter für Coolstep.

* Minimum Stallguard Value: Wenn der Stallguard-Wert unter diesem Wert*32 fällt wird der Motorstrom
  erhöht um den Motorbelastungswinkel (motor load angle) zu reduzieren.
  Ein Wert von 0 deaktiviert Coolstep.

* Maximum Stallguard Value: Wenn der Stallguard-Wert über (Min Stallguard Value + Max Stallguard Value + 1)*32
  geht wird der Motorstrom verringert um Energie zu sparen.

* Current Up Step Width: Setzt das Inkrement pro Stallguard-Wert. Der Wertebereich ist 0-3,
  was mit den Inkrementen 1, 2, 4 und 8 korrespondiert.

* Current Down Step Width: Setzt das Decrement pro Stallguard-Wert. Der Wertebereich ist 0-3,
  was mit den Dekrementen 1, 2, 8 und 16 korrespondiert.

* Minimum Current: Setzt den minimalen Strom für die Coolstep Stromregelung. Es kann zwischen der Hälfte und einem
  Viertel des Motorstroms gewählt werden.

* Stallguard Threshold Value: Setzt den Grenzwert für die Stall-Ausgabe (Motor blockiert)
  (siehe :func:`Get Driver Status`). Ein niedriger Wert führt zu einer höheren
  Empfindlichkeit. Der korrekte Wert muss typischerweise ausprobiert werden. 0 sollte für die meisten Motoren
  funktionieren.

* Stallguard Mode: Setze 0 für eine Standardauflösung und 1 für Filtered Mode. Im Filtered Modus wird das Stallguard
  Signal nur alle vier Vollschritte aktualisiert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Coolstep Configuration',
'elements': [('Minimum Stallguard Value', 'uint8', 1, 'out', {'range': (0, 15), 'default': 2}), # semin 0-15
             ('Maximum Stallguard Value', 'uint8', 1, 'out', {'range': (0, 15), 'default': 10}), # semax 0-15
             ('Current Up Step Width', 'uint8', 1, 'out', {'constant_group': 'Current Up Step Increment', 'default': 0}), # seup 0-3
             ('Current Down Step Width', 'uint8', 1, 'out', {'constant_group': 'Current Down Step Decrement', 'default': 0}), # sedn 0-3
             ('Minimum Current', 'uint8', 1, 'out', {'constant_group': 'Minimum Current', 'default': 0}), # seimin
             ('Stallguard Threshold Value', 'int8', 1, 'out', {'range': (-64, 63), 'default': 0}), # sgt -64-63
             ('Stallguard Mode', 'uint8', 1, 'out', {'constant_group': 'Stallguard Mode', 'default': 0})], # sfilt
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
'elements': [('Disable Short To Ground Protection', 'bool', 1, 'in', {'default': False}), # diss2g
             ('Synchronize Phase Frequency', 'uint8', 1, 'in', {'range': (0, 15), 'default': 0})], # sync 0=off 1-15
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
  the synchronization is turned off. Otherwise the synchronization is done through the formula
  f_sync = f_clk/(value*64). In Classic Mode the synchronization is automatically switched off.
  f_clk is 12.8MHz.
""",
'de':
"""
Note: Typischerweise können diese Werte bei ihren Standardwerten gelassen werden. Sie sollten nur
geändert werden, wenn man weiß was man tut.

Setzt verschiedene Parametereinstellungen.

* Disable Short To Ground Protection: Setze diesen Wert auf False um den Kurzschluss nach Masse
  Schutz zu aktivieren. Ansonsten ist dieser deaktiviert.

* Synchronize Phase Frequency: Mit diesem Parameter kann der Chopper für beide Phasen eines
  zweiphasen Motors synchronisiert werden. Der Wertebereich ist 0-15. Wenn der Wert auf 0 gesetzt
  wird ist die Synchronisation abgeschaltet. Ansonsten wird die Synchronisation mit folgender
  Formel durchgeführt: f_sync = f_clk/(value*64). Im Classic Modus ist die Synchronisation
  automatisch abgeschaltet. f_clk ist 12.8MHz.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Misc Configuration',
'elements': [('Disable Short To Ground Protection', 'bool', 1, 'out', {'default': False}), # diss2g
             ('Synchronize Phase Frequency', 'uint8', 1, 'out', {'range': (0, 15), 'default': 0})], # sync 0=off 1-15
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
'elements': [('Open Load', 'uint8', 1, 'out', {'constant_group': 'Open Load'}), # ola, olb
             ('Short To Ground', 'uint8', 1, 'out', {'constant_group': 'Short To Ground'}), # s2ga, s2gb
             ('Over Temperature', 'uint8', 1, 'out', {'constant_group': 'Over Temperature'}), # otpw, ot
             ('Motor Stalled', 'bool', 1, 'out', {}), # stallGuard
             ('Actual Motor Current', 'uint8', 1, 'out', {'range': (0, 31)}), # CS ACTUAL
             ('Full Step Active', 'bool', 1, 'out', {}), # fsactive
             ('Stallguard Result', 'uint8', 1, 'out', {}), # SG_RESULT
             ('Stealth Voltage Amplitude', 'uint8', 1, 'out', {})], # PWM_SCALE
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the current driver status.

* Open Load: Indicates if an open load is present on phase A, B or both. This could mean that there is a problem
  with the wiring of the motor. False detection can occur in fast motion as well as during stand still.

* Short To Ground: Indicates if a short to ground is present on phase A, B or both. If this is detected the driver
  automatically becomes disabled and stays disabled until it is enabled again manually.

* Over Temperature: The over temperature indicator switches to "Warning" if the driver IC warms up. The warning flag
  is expected during long duration stepper uses. If the temperature limit is reached the indicator switches
  to "Limit". In this case the driver becomes disabled until it cools down again.

* Motor Stalled: Is true if a motor stall was detected.

* Actual Motor Current: Indicates the actual current control scaling as used in Coolstep mode.
  It represents a multiplier of 1/32 to 32/32 of the
  ``Motor Run Current`` as set by :func:`Set Basic Configuration`. Example: If a ``Motor Run Current``
  of 1000mA was set and the returned value is 15, the ``Actual Motor Current`` is 16/32*1000mA = 500mA.

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
Gibt den aktuellen Treiberstatus zurück.

* Open Load: Gibt an, dass keine Last an den Phasen A oder B, oder bei beiden vorhanden ist (open load).
  In dem Fall kann es ein Problem mit der Verkabelung des Motors geben. Es kann aber auch Fehlmeldungen geben,
  wenn der Motor sich schnell bewegt oder sich im Stillstand befindet.

* Short To Ground: Gibt an, dass es einen Kurzschlus zwischen einer Phase (A,B) oder beiden Phasen nach Masse gibt.
  Wenn dies erkannt wird, wird der Treiber automatisch deaktiviert und muss wieder manuell aktiviert werden.

* Over Temperature: Wenn der Treiber sich aufwärmt gibt dieser Status "Warning" aus. Dies ist erwartet, wenn
  der Motor längere Zeit benutzt wird. Wenn das Temperaturlimit erreicht wird ändert sich der Status zu "Limit".
  In diesem Fall wird der Treiber automatisch deaktiviert bis er sich wieder abgekühlt hat.

* Motor Stalled: Ist True, wenn erkannt wurde, dass der Motor blockiert.

* Actual Motor Current: Gibt die aktuelle Motorstromskalierung im Coolstep Modus aus.
  Er repräsentiert einer Multiplikator von 1/32 bis zu 32/32 vom
  ``Motor Run Current``, wie von :func:`Set Basic Configuration` gesetzt. Beispiel: Wenn ein ``Motor Run Current``
  von 1000mA gesetzt wurde und ein Wert von 15 zurückgegeben wird, entspricht das einem ``Actual Motor Current``
  von 16/32*1000mA = 500mA.

* Stallguard Result: Der Stallguard Wert gibt einen Hinweis auf die Last des Motors. Ein niedriger Wert bedeutet eine
  höhere Last. Über Ausprobieren kann man mit diesem Wert herausfinden, welcher Wert zu einem geeigneten Drehmoment bei
  der aktuellen Geschwindigkeit führt. Danach kann über diesen Wert herausgefunden werden, wenn eine Blockierung des
  Motors wahrscheinlich wird und es kann dementsprechend darauf reagiert werden (z.B. indem die Geschwindigkeit reduziert
  wird). Im Stillstand kann dieser Wert nicht benutzt werden. Er zeigt dann die Chopper On-Time für Motorspule A.

* Stealth Voltage Amplitude: Zeigt das aktuelle PWM Scaling. Im Stealth Modus kann dieser Wert benutzt werden um die
  Motorlast abzuschätzen und eine Blockierung erkannt werden, wenn autoscale aktiviert wurde (see :func:`Set Stealth Configuration`).

"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Minimum Voltage',
'elements': [('Voltage', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Volt', 'default': 8000})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the minimum voltage, below which the :cb:`Under Voltage` callback
is triggered. The minimum possible value that works with the Silent Stepper
Brick is 8V.
You can use this function to detect the discharge of a battery that is used
to drive the stepper motor. If you have a fixed power supply, you likely do
not need this functionality.
""",
'de':
"""
Setzt die minimale Spannung, bei welcher der :cb:`Under Voltage` Callback
ausgelöst wird. Der kleinste mögliche Wert mit dem der Silent Stepper Brick noch
funktioniert,
ist 8V. Mit dieser Funktion kann eine Entladung der versorgenden Batterie detektiert
werden. Beim Einsatz einer Netzstromversorgung wird diese Funktionalität
höchstwahrscheinlich nicht benötigt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Minimum Voltage',
'elements': [('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt', 'default': 8000})],
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
'elements': [('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the input voltage drops below the value set by
:func:`Set Minimum Voltage`. The :word:`parameter` is the current voltage.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn die Eingangsspannung unter den, mittels
:func:`Set Minimum Voltage` gesetzten, Schwellwert sinkt. Der :word:`parameter`
ist die aktuelle Spannung.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Position Reached',
'elements': [('Position', 'int32', 1, 'out', {})],
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
'elements': [('Time Base', 'uint32', 1, 'in', {'unit': 'Second', 'default': 1})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the time base of the velocity and the acceleration of the Silent Stepper
Brick.

For example, if you want to make one step every 1.5 seconds, you can set
the time base to 15 and the velocity to 10. Now the velocity is
10steps/15s = 1steps/1.5s.
""",
'de':
"""
Setzt die Zeitbasis der Geschwindigkeit und Beschleunigung des Silent Stepper
Brick.

Beispiel: Wenn aller 1,5 Sekunden ein Schritt gefahren werden soll, kann
die Zeitbasis auf 15 und die Geschwindigkeit auf 10 gesetzt werden. Damit ist die
Geschwindigkeit 10Schritte/15s = 1Schritt/1,5s.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Time Base',
'elements': [('Time Base', 'uint32', 1, 'out', {'unit': 'Second', 'default': 1})],
'since_firmware': [1, 0, 0],
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
'elements': [('Current Velocity', 'uint16', 1, 'out', {'unit': 'Steps Per Second'}),
             ('Current Position', 'int32', 1, 'out', {}),
             ('Remaining Steps', 'int32', 1, 'out', {}),
             ('Stack Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'}),
             ('External Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'}),
             ('Current Consumption', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the following parameters: The current velocity,
the current position, the remaining steps, the stack voltage, the external
voltage and the current consumption of the stepper motor.

The current consumption is calculated by multiplying the ``Actual Motor Current``
value (see :func:`Set Basic Configuration`) with the ``Motor Run Current``
(see :func:`Get Driver Status`). This is an internal calculation of the
driver, not an independent external measurement.

The current consumption calculation was broken up to firmware 2.0.1, it is fixed
since firmware 2.0.2.

There is also a callback for this function, see :cb:`All Data` callback.
""",
'de':
"""
Gibt die folgenden Parameter zurück: Die aktuelle
Geschwindigkeit, die aktuelle Position, die verbleibenden Schritte,
die Spannung des Stapels, die externe Spannung und der aktuelle Stromverbrauch
des Schrittmotors.

Der Stromverbrauch des Schrittmotors wird berechnet aus dem
``Actual Motor Current``-Wert (siehe :func:`Set Basic Configuration`) multipliziert
mit dem  ``Motor Run Current`` (see :func:`Get Driver Status`). Es handelt
sich dabei um eine interne Berechnung des Treibers, nicht um eine externe
unabhängige Messung.

Die Stromverbrauchsberechnung war bis Firmware 2.0.1 fehlerhaft, sie
funktioniert seit Version 2.0.2 wie beschrieben.

Es existiert auch ein Callback für diese Funktion, siehe :cb:`All Data`
Callback.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set All Data Period',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the period with which the :cb:`All Data` callback is triggered
periodically. A value of 0 turns the callback off.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`All Data` Callback ausgelöst wird.
Ein Wert von 0 deaktiviert den Callback.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get All Data Period',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
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
'elements': [('Current Velocity', 'uint16', 1, 'out', {'unit': 'Steps Per Second'}),
             ('Current Position', 'int32', 1, 'out', {}),
             ('Remaining Steps', 'int32', 1, 'out', {}),
             ('Stack Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'}),
             ('External Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'}),
             ('Current Consumption', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere'})],
'since_firmware': [1, 0, 0],
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
'elements': [('State New', 'uint8', 1, 'out', {'constant_group': 'State'}),
             ('State Previous', 'uint8', 1, 'out', {'constant_group': 'State'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered whenever the Silent Stepper Brick enters a new state.
It returns the new state as well as the previous state.
""",
'de':
"""
Dieser Callback wird immer dann ausgelöst, wenn der Silent Stepper Brick einen
neuen Zustand erreicht. Es wird sowohl der neue wie auch der alte Zustand
zurückgegeben.
"""
}]
})

com['examples'].append({
'name': 'Configuration',
'functions': [('setter', 'Set Motor Current', [('uint16', 800)], None, '800mA'),
              ('setter', 'Set Step Configuration', [('uint8:constant', 5), ('bool', True)], None, '1/8 steps (interpolated)'),
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
'functions': [('callback', ('Position Reached', 'position reached'), [(('Position', 'Position'), 'int32', 1, None, None, None)], 'Use position reached callback to program random movement', None),
              ('empty',),
              ('setter', 'Set Step Configuration', [('uint8:constant', 5), ('bool', True)], None, '1/8 steps (interpolated)'),
              ('setter', 'Enable', [], None, 'Enable motor power'),
              ('setter', 'Set Steps', [('int32', 1)], None, 'Drive one step forward to get things going')],
'cleanups': [('setter', 'Disable', [], None, None)],
'incomplete': True # because of special random movement logic in callback
})

def data_channel(name_words, name_headless, type_, divisor=1, unit=None):
    return {
        'id': name_words,
        'type': name_words,
        'getters': [{
            'packet': 'Get All Data',
            'element': name_words,
            'packet_params': [],
            'transform': 'new {type}(value.{headless}{{divisor}}{{unit}})'.format(type=type_,headless=name_headless,unit=', ' + unit if unit is not None else '')}],
        'callbacks': [{
            'packet': 'All Data',
            'element': name_words,
            'transform': 'new {type}({headless}{{divisor}}{{unit}})'.format(type=type_,headless=name_headless,unit=', ' + unit if unit is not None else '')}],

        'is_trigger_channel': False,
        'java_unit': unit,
        'divisor': divisor,
    }

com['openhab'] = {
    'imports': oh_generic_channel_imports() + oh_generic_trigger_channel_imports() + ['org.eclipse.smarthome.core.library.types.DecimalType'],
    'param_groups': oh_generic_channel_param_groups(),
    'params': [
        update_interval('Set All Data Period', 'Period', "All Data", "all data"),
        {
            'packet': 'Set Minimum Voltage',
            'element': 'Voltage',

            'name': 'Minimum Voltage',
            'type': 'decimal',
            'unit': 'V',
            'label': 'Minimum Voltage',
            'description': 'The minimum voltage in V, below which the Unter Voltage channel is triggered. The minimum possible value that works with the Silent Stepper Brick is 8V. You can use this function to detect the discharge of a battery that is used to drive the stepper motor. If you have a fixed power supply, you likely do not need this functionality. The default value is 8V.',
            'default': 8,
        }
    ],

    'init_code': """this.setAllDataPeriod(cfg.allDataUpdateInterval);
    this.setMinimumVoltage((int)(cfg.minimumVoltage.doubleValue() * 1000.0));""",

    'channels': [
        data_channel('Current Velocity', 'currentVelocity', 'DecimalType', 1, None),
        data_channel('Current Position', 'currentPosition', 'DecimalType', 1, None),
        data_channel('Remaining Steps', 'remainingSteps', 'DecimalType', 1, None),
        data_channel('Stack Voltage', 'stackVoltage', 'QuantityType<>', 1000.0, 'SmartHomeUnits.VOLT'),
        data_channel('External Voltage', 'externalVoltage', 'QuantityType<>', 1000.0, 'SmartHomeUnits.VOLT'),
        data_channel('Current Consumption', 'currentConsumption', 'QuantityType<>', 1000.0, 'SmartHomeUnits.AMPERE'),
        {
            'id': 'State',
            'type': 'State',
            'label': 'State',

            'callbacks': [{
                'packet': 'New State',
                'element': 'State New',
                'transform': 'new DecimalType(stateNew)'}],

            'is_trigger_channel': False
        }, {
            'id': 'Previous State',
            'type': 'State',
            'label': 'Previous State',

            'callbacks': [{
                'packet': 'New State',
                'element': 'State Previous',
                'transform': 'new DecimalType(statePrevious)'}],

            'is_trigger_channel': False
        }, {
            'id': 'Position Reached',
            'type': 'system.trigger',
            'label': 'Position Reached',
            'description': "This channel is triggered when a position set by the setSteps or setTargetPosition action is reached.<br/><br/>Note<br/><br/>Since we can't get any feedback from the stepper motor, this only works if the acceleration (see setSpeedRamping()) is set smaller or equal to the maximum acceleration of the motor. Otherwise the motor will lag behind the control value and the listener will be triggered too early.",

            'callbacks': [{
                'packet': 'Position Reached',
                'transform': 'CommonTriggerEvents.PRESSED'}],

            'is_trigger_channel': True
        },  {
            'id': 'Unter Voltage',
            'type': 'system.trigger',
            'label': 'Unter Voltage',
            'description': 'This channel is triggered when the input voltage drops below the configured minimum voltage.',

            'callbacks': [{
                'packet': 'Under Voltage',
                'transform': 'CommonTriggerEvents.PRESSED'}],

            'is_trigger_channel': True
        }
    ],
    'channel_types': [
        oh_generic_channel_type('Current Velocity', 'Number', 'Velocity',
            update_style=None,
            description='The current velocity of the stepper motor in steps per second.',
            read_only=True),
        oh_generic_channel_type('Current Position', 'Number', 'Position',
            update_style=None,
            description='The current position of the stepper motor in steps. On startup the position is 0.',
            read_only=True),
        oh_generic_channel_type('Remaining Steps', 'Number', 'Remaining Steps',
            update_style=None,
            description='The remaining steps of the last call of the setSteps() action.',
            read_only=True),
        oh_generic_channel_type('Stack Voltage', 'Number:ElectricPotential', 'Stack Voltage',
            update_style=None,
            description='The stack input voltage in V. The stack input voltage is the voltage that is supplied via the stack, i.e. it is given by a Step-Down or Step-Up Power Supply.',
            pattern='%.3f %unit%',
            read_only=True),
        oh_generic_channel_type('External Voltage', 'Number:ElectricPotential', 'External Voltage',
            update_style=None,
            description='The external input voltage in mV. The external input voltage is given via the black power input connector on the Silent Stepper Brick.<br/><br/>If there is an external input voltage and a stack input voltage, the motor will be driven by the external input voltage. If there is only a stack voltage present, the motor will be driven by this voltage.<br/><br/><b>Warning: This means, if you have a high stack voltage and a low external voltage, the motor will be driven with the low external voltage. If you then remove the external connection, it will immediately be driven by the high stack voltage</b>',
            pattern='%.3f %unit%',
            read_only=True),
        oh_generic_channel_type('Current Consumption', 'Number:ElectricCurrent', 'Current Consumption',
            update_style=None,
            description='The current consumption of the motor in A.',
            pattern='%.3f %unit%',
            read_only=True),
        oh_generic_channel_type('State', 'Number', 'State',
            update_style=None,
            description='State of the brick: <ul><li>Stop = 1</li><li>Acceleration = 2</li><li>Run = 3</li><li>Deacceleration = 4</li><li>Direction change to forward = 5</li><li>Direction change to backward = 6</li></ul>',
            read_only=True),
    ],
    'actions': ['Set Max Velocity', 'Get Max Velocity', 'Get Current Velocity', 'Set Speed Ramping', 'Get Speed Ramping',
                'Full Brake', 'Set Steps', 'Get Steps', 'Get Remaining Steps', 'Drive Forward', 'Drive Backward', 'Stop',
                'Set Motor Current', 'Get Motor Current', 'Enable', 'Disable', 'Is Enabled',
                'Set Basic Configuration', 'Get Basic Configuration',
                'Set Current Position', 'Get Current Position', 'Set Target Position', 'Get Target Position',
                'Set Step Configuration', 'Get Step Configuration',
                'Get Stack Input Voltage', 'Get External Input Voltage',
                'Set Spreadcycle Configuration', 'Get Spreadcycle Configuration',
                'Set Stealth Configuration', 'Get Stealth Configuration',
                'Set Coolstep Configuration', 'Get Coolstep Configuration',
                'Set Misc Configuration', 'Get Misc Configuration',
                'Get Driver Status', 'Set Time Base', 'Get Time Base', 'Get All Data', 'Get All Data Period']
}

