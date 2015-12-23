# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Stepper Brick communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Brick',
    'device_identifier': 19,
    'name': ('Silent Stepper', 'Silent Stepper', 'Silent Stepper Brick'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'TODO',
        'de': 'TODO'
    },
    'released': False,
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
'name': 'Get Max Velocity',
'elements': [('Velocity', 'uint16', 1, 'out')],
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
'name': 'Set Target Position',
'elements': [('Position', 'int32', 1, 'in')],
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
'name': 'Get Target Position',
'elements': [('Position', 'int32', 1, 'out')],
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
'name': 'Set Steps',
'elements': [('Steps', 'int32', 1, 'in')],
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
'name': 'Get Steps',
'elements': [('Steps', 'int32', 1, 'out')],
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
'name': 'Get Remaining Steps',
'elements': [('Steps', 'int32', 1, 'out')],
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
'name': 'Set Step Mode',
'elements': [('Mode', 'uint8', 1, 'in')], # TODO: Add constants
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
'name': 'Get Step Mode',
'elements': [('Mode', 'uint8', 1, 'out')],
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
'name': 'Drive Forward',
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
'name': 'Drive Backward',
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
'name': 'Stop',
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
'name': 'Get Motor Current',
'elements': [('Current', 'uint16', 1, 'out')],
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

# standstill power down
# chopper off time low/medium/high
# chopper hysteresis low/medium/high
# choppper blank time low/medium/high

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('Decay', 'uint16', 1, 'in')],
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
'name': 'Get Configuration',
'elements': [('Decay', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`SetConfiguration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`SetConfiguration` gesetzt.
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
'name': 'Get Minimum Voltage',
'elements': [('Voltage', 'uint16', 1, 'out')],
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
'name': 'Under Voltage',
'elements': [('Voltage', 'uint16', 1, 'out')],
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
'name': 'Position Reached',
'elements': [('Position', 'int32', 1, 'out')],
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
'name': 'Set All Data Period',
'elements': [('Period', 'uint32', 1, 'in')],
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
'name': 'Get All Data Period',
'elements': [('Period', 'uint32', 1, 'out')],
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
'functions': [('callback', ('Position Reached', 'position reached'), [(('Position', 'Position'), 'int32', None, None, None, None)], 'Use position reached callback to program random movement', None),
              ('empty',),
              ('setter', 'Enable', [], None, 'Enable motor power'),
              ('setter', 'Set Steps', [('int32', 1)], None, 'Drive one step forward to get things going')],
'cleanups': [('setter', 'Disable', [], None, None)],
'incomplete': True # because of special random movement logic in callback
})
