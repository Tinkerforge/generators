# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Stepper Brick communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Brick',
    'device_identifier': 15,
    'name': ('Stepper', 'stepper', 'Stepper', 'Stepper Brick'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Drives one bipolar stepper motor with up to 38V and 2.5A per phase',
        'de': 'Steuert einen bipolaren Schrittmotor mit bis zu 38V und 2,5A pro Phase'
    },
    'released': True,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': ('SetMaxVelocity', 'set_max_velocity'), 
'elements': [('velocity', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
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
Setzt die maximale Geschwindigkeit des Schrittmotors in Schritten je Sekunde.
Diese Funktion startet *nicht* den Motor, sondern setzt nur die maximale
Geschwindigkeit auf welche der Schrittmotor beschleunigt wird. Um den Motor zu fahren
können :func:`SetTargetPosition`, :func:`SetSteps`, :func:`DriveForward` oder
:func:`DriveBackward` verwendet werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetMaxVelocity', 'get_max_velocity'), 
'elements': [('velocity', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the velocity as set by :func:`SetMaxVelocity`.
""",
'de':
"""
Gibt die Geschwindigkeit zurück, wie von :func:`SetMaxVelocity` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetCurrentVelocity', 'get_current_velocity'), 
'elements': [('velocity', 'uint16', 1, 'out')],
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
'name': ('SetSpeedRamping', 'set_speed_ramping'), 
'elements': [('acceleration', 'uint16', 1, 'in'),
             ('deacceleration', 'uint16', 1, 'in')],
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
'name': ('GetSpeedRamping', 'get_speed_ramping'), 
'elements': [('acceleration', 'uint16', 1, 'out'),
             ('deacceleration', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the acceleration and deacceleration as set by 
:func:`SetSpeedRamping`.
""",
'de':
"""
Gibt die Beschleunigung und Verzögerung zurück, wie von :func:`SetSpeedRamping` 
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('FullBrake', 'full_brake'), 
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
'name': ('SetCurrentPosition', 'set_current_position'), 
'elements': [('position', 'int32', 1, 'in')],
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
'name': ('GetCurrentPosition', 'get_current_position'), 
'elements': [('position', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
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
Gibt die aktuelle Position des Schrittmotors in Schritten zurück. Nach dem 
Hochfahren ist die Position 0. Die Schritte werden bei Verwendung aller möglichen
Fahrfunktionen gezählt (:func:`SetTargetPosition`, :func:`SetSteps`, :func:`DriveForward` der
:func:`DriveBackward`). Es ist auch möglich den Schrittzähler auf 0 oder jeden anderen
gewünschten Wert zu setzen mit :func:`SetCurrentPosition`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetTargetPosition', 'set_target_position'), 
'elements': [('position', 'int32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
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
Setzt die Zielposition des Schrittmotors in Schritten. Beispiel:
Wenn die aktuelle Position des Motors 500 ist und :func:`SetTargetPosition` mit 
1000 aufgerufen wird, dann verfährt der Schrittmotor 500 Schritte vorwärts. Dabei
wird die Geschwindigkeit, Beschleunigung und Verzögerung, wie mit 
:func:`SetMaxVelocity` und :func:`SetSpeedRamping` gesetzt, verwendet.

Ein Aufruf von :func:`SetTargetPosition` mit dem Parameter *x* ist 
äquivalent mit einem Aufruf von :func:`SetSteps` mit dem Parameter
(*x* - :func:`GetCurrentPosition`).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetTargetPosition', 'get_target_position'), 
'elements': [('position', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the last target position as set by :func:`SetTargetPosition`.
""",
'de':
"""
Gibt die letzte Zielposition zurück, wie von :func:`SetTargetPosition`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetSteps', 'set_steps'), 
'elements': [('steps', 'int32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the number of steps the stepper motor should run. Positive values
will drive the motor forward and negative values backward. 
The velocity, acceleration and deacceleration as set by
:func:`SetMaxVelocity` and :func:`SetSpeedRamping` will be used.
""",
'de':
"""
Setzt die Anzahl der Schritte die der Schrittmotor fahren soll.
Positive Werte fahren den Motor vorwärts und negative rückwärts.
Dabei wird die Geschwindigkeit, Beschleunigung und Verzögerung, wie mit 
:func:`SetMaxVelocity` und :func:`SetSpeedRamping` gesetzt, verwendet.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetSteps', 'get_steps'), 
'elements': [('steps', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the last steps as set by :func:`SetSteps`.
""",
'de':
"""
Gibt die letzten Schritte zurück, wie von :func:`SetSteps` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetRemainingSteps', 'get_remaining_steps'), 
'elements': [('steps', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the remaining steps of the last call of :func:`SetSteps`.
For example, if :func:`SetSteps` is called with 2000 and 
:func:`GetRemainingSteps` is called after the motor has run for 500 steps,
it will return 1500.
""",
'de':
"""
Gibt die verbleibenden Schritte des letzten Aufrufs von :func:`SetSteps`
zurück. Beispiel: Wenn :func:`SetSteps` mit 2000 aufgerufen wird und 
:func:`GetRemainingSteps` aufgerufen wird wenn der Motor 500 Schritte fahren
hat, wird 1500 zurückgegeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetStepMode', 'set_step_mode'), 
'elements': [('mode', 'uint8', 1, 'in', ('StepMode', 'step_mode', [('FullStep', 'full_step', 1),
                                                                   ('HalfStep', 'half_step', 2),
                                                                   ('QuarterStep', 'quarter_step', 4),
                                                                   ('EighthStep', 'eighth_step', 8)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
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
Setzt den Schrittmodus des Schrittmotors. Mögliche Werte sind:

* Vollschritt = 1
* Halbschritt = 2
* Viertelschritt = 4
* Achtelschritt = 8

Ein höherer Wert erhöht die Auflösung und verringert das
Drehmoment des Schrittmotors.

Der Standardwert ist 8 (Achtelschritt).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetStepMode', 'get_step_mode'), 
'elements': [('mode', 'uint8', 1, 'out', ('StepMode', 'step_mode', [('FullStep', 'full_step', 1),
                                                                    ('HalfStep', 'half_step', 2),
                                                                    ('QuarterStep', 'quarter_step', 4),
                                                                    ('EighthStep', 'eighth_step', 8)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the step mode as set by :func:`SetStepMode`.
""",
'de':
"""
Gibt den Schrittmodus zurück, wie von :func:`SetStepMode` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('DriveForward', 'drive_forward'), 
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Drives the stepper motor forward until :func:`DriveBackward` or
:func:`Stop` is called. The velocity, acceleration and deacceleration as 
set by :func:`SetMaxVelocity` and :func:`SetSpeedRamping` will be used.
""",
'de':
"""
Fährt den Schrittmotor vorwärts bis :func:`DriveBackward` oder
:func:`Stop` aufgerufen wird. Dabei wird die Geschwindigkeit, 
Beschleunigung und Verzögerung, wie mit :func:`SetMaxVelocity`
und :func:`SetSpeedRamping` gesetzt, verwendet.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('DriveBackward', 'drive_backward'), 
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Drives the stepper motor backward until :func:`DriveForward` or
:func:`Stop` is triggered. The velocity, acceleration and deacceleration as
set by :func:`SetMaxVelocity` and :func:`SetSpeedRamping` will be used.
""",
'de':
"""
Fährt den Schrittmotor rückwärts bis :func:`DriveForward` oder
:func:`Stop` aufgerufen wird. Dabei wird die Geschwindigkeit, 
Beschleunigung und Verzögerung, wie mit :func:`SetMaxVelocity`
und :func:`SetSpeedRamping` gesetzt, verwendet.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('Stop', 'stop'), 
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Stops the stepper motor with the deacceleration as set by 
:func:`SetSpeedRamping`.
""",
'de':
"""
Stoppt den Schrittmotor mit der Verzögerung, wie von 
:func:`SetSpeedRamping` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetStackInputVoltage', 'get_stack_input_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')],
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
'name': ('GetExternalInputVoltage', 'get_external_input_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')],
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
'name': ('GetCurrentConsumption', 'get_current_consumption'), 
'elements': [('current', 'uint16', 1, 'out')],
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
'name': ('SetMotorCurrent', 'set_motor_current'), 
'elements': [('current', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
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
Setzt den Strom in mA mit welchem der Motor angetrieben wird.
Der minimale Wert ist 100mA, der maximale Wert ist 2291mA und der
Standardwert ist 800mA.

.. warning::
 Dieser Wert sollte nicht über die Spezifikation des Schrittmotors gesetzt werden.
 Sonst ist eine Beschädigung des Motors möglich.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetMotorCurrent', 'get_motor_current'), 
'elements': [('current', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current as set by :func:`SetMotorCurrent`.
""",
'de':
"""
Gibt den Strom zurück, wie von :func:`SetMotorCurrent` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('Enable', 'enable'), 
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
'name': ('Disable', 'disable'), 
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
'name': ('IsEnabled', 'is_enabled'), 
'elements': [('enabled', 'bool', 1, 'out')],
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
'name': ('SetDecay', 'set_decay'), 
'elements': [('decay', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the decay mode of the stepper motor. The possible value range is
between 0 and 65535. A value of 0 sets the fast decay mode, a value of
65535 sets the slow decay mode and a value in between sets the mixed
decay mode.

Changing the decay mode is only possible if synchronous rectification
is enabled (see :func:`SetSyncRect`).

For a good explanation of the different decay modes see 
`this <http://ebldc.com/?p=86/>`__ blog post by Avayan.

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
Setzt den Decay Modus (Abklingmodus) des Schrittmotors. Der mögliche
Wertebereich ist 0 bis 65535. Ein Wert von 0 setzt den Fast Decay Modus
(schneller Stromabbau), ein Wert von 65535 den Slow Decay Modus (langsamer 
Stromabbau) ein Wert dazwischen den Mixed Decay Modus (Nutzung beider Modi).

Eine Änderung des Decay Modus ist nur möglich wenn die Synchrongleichrichtung
aktiviert ist (siehe :func:`SetSyncRect`).

Für eine gute Erläuterung der verschiedenen Decay Modi siehe 
`diesen <http://ebldc.com/?p=86/>`__ Blogeintrag (Englisch) von Avayan oder
`diesen <http://www.schrittmotor-blog.de/?p=51>`__ Blogeintrag (Deutsch) von
T. Ostermann.

Ein guter Decay Modus ist leider unterschiedlich für jeden Motor. Der beste
Weg einen guten Decay Modus für den jeweiligen Schrittmotor zu finden, wenn der
Strom nicht mit einem Oszilloskop gemessen werden kann, ist auf die Geräusche des
Motors zu hören. Wenn der Wert zu gering ist, ist oftmals ein hoher Ton zu hören
und wenn er zu hoch ist, oftmals ein brummendes Geräusch.

Im Allgemeinen ist der Fast Decay Modus (kleine Werte) geräuschvoller, erlaubt aber
höhere Motorgeschwindigkeiten.

Der Standardwert ist 10000.

.. note::
 Es existiert leider keine Formel zur Berechnung des optimalen Decay Modus eines
 Schrittmotors. Sollten Probleme mit lauten Geräuschen oder einer zu geringen maximalen
 Motorgeschwindigkeit bestehen, bleibt nur Ausprobieren um einen besseren Decay Modus zu finden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetDecay', 'get_decay'), 
'elements': [('decay', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the decay mode as set by :func:`SetDecay`.
""",
'de':
"""
Gibt den Decay Modus zurück, wie von :func:`SetDecay` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetMinimumVoltage', 'set_minimum_voltage'), 
'elements': [('voltage', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
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
Setzt die minimale Spannung in mV, bei welcher der :func:`UnderVoltage` Callback
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
'name': ('GetMinimumVoltage', 'get_minimum_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the minimum voltage as set by :func:`SetMinimumVoltage`.
""",
'de':
"""
Gibt die minimale Spannung zurück, wie von :func:`SetMinimumVoltage` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('UnderVoltage', 'under_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the input voltage drops below the value set by
:func:`SetMinimumVoltage`. The :word:`parameter` is the current voltage given
in mV.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn die Eingangsspannung unter den, mittels
:func:`SetMinimumVoltage` gesetzten, Schwellwert sinkt. Der :word:`parameter`
ist die aktuelle Spannung in mV.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('PositionReached', 'position_reached'), 
'elements': [('position', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
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
Dieser Callback wird ausgelöst immer wenn eine konfigurierte Position, wie von
:func:`SetSteps` oder :func:`SetTargetPosition` gesetzt, erreicht wird. 

.. note::
 Da es nicht möglich ist eine Rückmeldung vom Schrittmotor zu erhalten,
 funktioniert dies nur wenn die konfigurierte Beschleunigung (siehe :func:`SetSpeedRamping`)
 kleiner oder gleich der maximalen Beschleunigung des Motors ist. Andernfalls
 wird der Motor hinter dem Vorgabewert zurückbleiben und der Callback wird
 zu früh ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetSyncRect', 'set_sync_rect'), 
'elements': [('sync_rect', 'bool', 1, 'in')],
'since_firmware': [1, 1, 4],
'doc': ['af', {
'en':
"""
Turns synchronous rectification on or off (*true* or *false*).

With synchronous rectification on, the decay can be changed
(see :func:`SetDecay`). Without synchronous rectification fast
decay is used.

For an explanation of synchronous rectification see 
`here <https://en.wikipedia.org/wiki/Active_rectification>`__.

.. warning::
 If you want to use high speeds (> 10000 steps/s) for a large 
 stepper motor with a large inductivity we strongly
 suggest that you disable synchronous rectification. Otherwise the
 Brick may not be able to cope with the load and overheat.

The default value is *false*.
""",
'de':
"""
Aktiviert oder deaktiviert (*true* oder *false*) die Synchrongleichrichtung.

Bei aktiver Synchrongleichrichtung kann der Decay Modus geändert werden
(Siehe :func:`SetDecay`). Ohne Synchrongleichrichtung wird der Fast
Decay Modus verwendet.

Für eine Erläuterung der Synchrongleichrichtung siehe
`hier <https://de.wikipedia.org/wiki/Gleichrichter#Synchrongleichrichter>`__.

.. warning::
 Wenn hohe Geschwindigkeiten (> 10000 Schritte/s) mit einem großen
 Schrittmotor mit einer hohen Induktivität genutzt werden sollen, wird
 dringend geraten die Synchrongleichrichtung zu deaktivieren. Sonst kann
 es vorkommen, dass der Brick die Last nicht bewältigen kann und überhitzt.
 
Der Standardwert ist *false*.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('IsSyncRect', 'is_sync_rect'), 
'elements': [('sync_rect', 'bool', 1, 'out')],
'since_firmware': [1, 1, 4],
'doc': ['af', {
'en':
"""
Returns *true* if synchronous rectification is enabled, *false* otherwise.
""",
'de':
"""
Gibt zurück ob die Synchrongleichrichtung aktiviert ist.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetTimeBase', 'set_time_base'), 
'elements': [('time_base', 'uint32', 1, 'in')],
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
'name': ('GetTimeBase', 'get_time_base'), 
'elements': [('time_base', 'uint32', 1, 'out')],
'since_firmware': [1, 1, 6],
'doc': ['af', {
'en':
"""
Returns the time base as set by :func:`SetTimeBase`.
""",
'de':
"""
Gibt die Zeitbasis zurück, wie von :func:`SetTimeBase` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAllData', 'get_all_data'), 
'elements': [('current_velocity', 'uint16', 1, 'out'),
             ('current_position', 'int32', 1, 'out'),
             ('remaining_steps', 'int32', 1, 'out'),
             ('stack_voltage', 'uint16', 1, 'out'),
             ('external_voltage', 'uint16', 1, 'out'),
             ('current_consumption', 'uint16', 1, 'out')],
'since_firmware': [1, 1, 6],
'doc': ['af', {
'en':
"""
Returns the following :word:`parameters`: The current velocity,
the current position, the remaining steps, the stack voltage, the external
voltage and the current consumption of the stepper motor.

There is also a callback for this function, see :func:`AllData`.
""",
'de':
"""
Gibt die folgenden :word:`parameters` zurück: Die aktuelle
Geschwindigkeit, die aktuelle Position, die verbleibenden Schritte,
die Spannung des Stapels, die externe Spannung und der aktuelle Stromverbrauch
des Schrittmotors.

Es existiert auch ein Callback für diese Funktion, siehe :func:`AllData`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetAllDataPeriod', 'set_all_data_period'), 
'elements': [('period', 'uint32', 1, 'in')],
'since_firmware': [1, 1, 6],
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
'since_firmware': [1, 1, 6],
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
'name': ('AllData', 'all_data'), 
'elements': [('current_velocity', 'uint16', 1, 'out'),
             ('current_position', 'int32', 1, 'out'),
             ('remaining_steps', 'int32', 1, 'out'),
             ('stack_voltage', 'uint16', 1, 'out'),
             ('external_voltage', 'uint16', 1, 'out'),
             ('current_consumption', 'uint16', 1, 'out')],
'since_firmware': [1, 1, 6],
'doc': ['c', {
'en':
"""
This callback is triggered periodically with the period that is set by
:func:`SetAllDataPeriod`. The :word:`parameters` are: the current velocity,
the current position, the remaining steps, the stack voltage, the external
voltage and the current consumption of the stepper motor.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetAllDataPeriod`,
ausgelöst. Die :word:`parameters` sind die aktuelle Geschwindigkeit,
die aktuelle Position, die verbleibenden Schritte, die Spannung des Stapels, die
externe Spannung und der aktuelle Stromverbrauch des Schrittmotors.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('NewState', 'new_state'), 
'elements': [('state_new',      'uint8', 1, 'out', ('State', 'state', [('Stop', 'stop', 1),
                                                                       ('Acceleration', 'acceleration', 2),
                                                                       ('Run', 'run', 3),
                                                                       ('Deacceleration', 'deacceleration', 4),
                                                                       ('DirectionChangeToForward', 'direction_change_to_forward', 5),
                                                                       ('DirectionChangeToBackward', 'direction_change_to_backward', 6)])),
             ('state_previous', 'uint8', 1, 'out', ('State', 'state', [('Stop', 'stop', 1),
                                                                       ('Acceleration', 'acceleration', 2),
                                                                       ('Run', 'run', 3),
                                                                       ('Deacceleration', 'deacceleration', 4),
                                                                       ('DirectionChangeToForward', 'direction_change_to_forward', 5),
                                                                       ('DirectionChangeToBackward', 'direction_change_to_backward', 6)]))],
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
              ('setter', 'Set Step Mode', [('uint8', 8)], None, '1/8 step mode'),
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
'functions': [('callback', ('Position Reached', 'position reached'), [(('position', 'Position'), 'int32', None, None, None, None)], 'Use position reached callback to program random movement', None),
              ('empty',),
              ('setter', 'Enable', [], None, 'Enable motor power'),
              ('setter', 'Set Steps', [('int32', 1)], None, 'Drive one step forward to get things going')],
'cleanups': [('setter', 'Disable', [], None, None)],
'incomplete': True # because of special random movement logic in callback
})
