# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Performance Stepper Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2158,
    'name': 'Performance Stepper',
    'display_name': 'Performance Stepper',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'TBD',
        'de': 'TBD'
    },
    'released': False,
    'documented': False,
    'discontinued': False,
    'features': [
        'comcu_bricklet',
        'bricklet_get_identity'
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
'name': 'Ramping Mode',
'type': 'uint8',
'constants': [('Positioning', 0),
              ('Velocity Negative', 1),
              ('Velocity Positive', 2),
              ('Hold', 3)]
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

com['constant_groups'].append({
'name': 'GPIO Action',
'type': 'uint32',
'constants': [('None', 0),
              ('Normal Stop Rising Edge', 1 << 0),    # -> ramping mode = velocity, amax=stop deceleration max, vmax=0
              ('Normal Stop Falling Edge', 1 << 1),
              ('Emergency Stop Rising Edge', 1 << 2),
              ('Emergency Stop Falling Edge', 1 << 3),
              ('Callback Rising Edge', 1 << 4),
              ('Callback Falling Edge', 1 << 5)]
})

com['constant_groups'].append({
'name': 'Error LED Config',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Show Heartbeat', 2),
              ('Show Error', 3)]
})

com['constant_groups'].append({
'name': 'Enable LED Config',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Show Heartbeat', 2),
              ('Show Enable', 3)]
})

com['constant_groups'].append({
'name': 'Steps LED Config',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Show Heartbeat', 2),
              ('Show Steps', 3)]
})

com['constant_groups'].append({
'name': 'GPIO LED Config',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Show Heartbeat', 2),
              ('Show GPIO Active High', 3),
              ('Show GPIO Active Low', 4)]
})

com['constant_groups'].append({
'name': 'Filter Time',
'type': 'uint8',
'constants': [('100', 0),
              ('200', 1),
              ('300', 2),
              ('400', 3)]
})

com['constant_groups'].append({
'name': 'Spike Filter Bandwidth',
'type': 'uint8',
'constants': [('100', 0),
              ('1000', 1),
              ('2000', 2),
              ('3000', 3)]
})

# TODO: Fix defaults!
com['packets'].append({
'type': 'function',
'name': 'Set Motion Configuration',
'elements': [('Ramping Mode', 'uint8', 1, 'in', {'constant_group': 'Ramping Mode'}), # rampmode 0 to 3
             ('Velocity Start', 'int32', 1, 'in', {'range': (0, 0x1FFFF), 'default': 0, 'unit': 'Steps Per Second'}), # vstart 0 to 2^18 -1
             ('Acceleration 1', 'int32', 1, 'in', {'range': (0, 0xFFFF), 'default': 0, 'unit': 'Steps Per Second Squared'}), # a1 0 to 2^16 -1
             ('Velocity 1', 'int32', 1, 'in', {'range': (0, 0xFFFFF), 'default': 0, 'unit': 'Steps Per Second'}), # v1 0 to 2^20 -1,
             ('Acceleration Max', 'int32', 1, 'in', {'range': (0, 0xFFFF), 'default': 0, 'unit': 'Steps Per Second Squared'}), # amax 0 to 2^16 -1
             ('Velocity Max', 'int32', 1, 'in', {'range': (0, 0x7FFFFF - 511), 'default': 0, 'unit': 'Steps Per Second'}), # vmax 0 to 2^23 -512,
             ('Deceleration Max', 'int32', 1, 'in', {'range': (0, 0xFFFF), 'default': 0, 'unit': 'Steps Per Second Squared'}), # dmax 0 to 2^16 -1
             ('Deceleration 1', 'int32', 1, 'in', {'range': (1, 0xFFFF), 'default': 1, 'unit': 'Steps Per Second Squared'}), # d1 0 to 2^16 -1   != 0
             ('Velocity Stop', 'int32', 1, 'in', {'range': (1, 0x1FFFF), 'default': 1, 'unit': 'Steps Per Second'}), # vstop 0 to 2^18 -1   != 0
             ('Ramp Zero Wait', 'int32', 1, 'in', {'range': (0, 2796), 'default': 100, 'unit': 'Second', 'scale': (1, 1000)})], # tzerowait 0 to 2^16 -1  (high level 0-2796ms)
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TBD
""",
'de':
"""
TBD
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Motion Configuration',
'elements': [('Ramping Mode', 'uint8', 1, 'out', {'constant_group': 'Ramping Mode'}), # rampmode 0 to 3
             ('Velocity Start', 'int32', 1, 'out', {'range': (0, 0x1FFFF), 'default': 0, 'unit': 'Steps Per Second'}), # vstart 0 to 2^18 -1
             ('Acceleration 1', 'int32', 1, 'out', {'range': (0, 0xFFFF), 'default': 0, 'unit': 'Steps Per Second Squared'}), # a1 0 to 2^16 -1
             ('Velocity 1', 'int32', 1, 'out', {'range': (0, 0xFFFFF), 'default': 0, 'unit': 'Steps Per Second'}), # v1 0 to 2^20 -1,
             ('Acceleration Max', 'int32', 1, 'out', {'range': (0, 0xFFFF), 'default': 0, 'unit': 'Steps Per Second Squared'}), # amax 0 to 2^16 -1
             ('Velocity Max', 'int32', 1, 'out', {'range': (0, 0x7FFFFF - 511), 'default': 0, 'unit': 'Steps Per Second'}), # vmax 0 to 2^23 -512,
             ('Deceleration Max', 'int32', 1, 'out', {'range': (0, 0xFFFF), 'default': 0, 'unit': 'Steps Per Second Squared'}), # dmax 0 to 2^16 -1
             ('Deceleration 1', 'int32', 1, 'out', {'range': (1, 0xFFFF), 'default': 1, 'unit': 'Steps Per Second Squared'}), # d1 0 to 2^16 -1   != 0
             ('Velocity Stop', 'int32', 1, 'out', {'range': (1, 0x1FFFF), 'default': 1, 'unit': 'Steps Per Second'}), # vstop 0 to 2^18 -1   != 0
             ('Ramp Zero Wait', 'int32', 1, 'out', {'range': (0, 2796), 'default': 100, 'unit': 'Second', 'scale': (1, 1000)})], # tzerowait 0 to 2^16 -1  (high level 0-2796ms)
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TBD
""",
'de':
"""
TBD
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Current Position',
'elements': [('Position', 'int32', 1, 'in', {})], # xactual
'since_firmware': [1, 0, 0],
'doc': ['bf', {
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
'elements': [('Position', 'int32', 1, 'out', {})], # xactual
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current position of the stepper motor in steps. On startup
the position is 0. The steps are counted with all possible driving
functions (:func:`Set Target Position`, :func:`Set Steps`). 
It also is possible to reset the steps to 0 or
set them to any other desired value with :func:`Set Current Position`.
""",
'de':
"""
Gibt die aktuelle Position des Schrittmotors in Schritten zurück. Nach dem
Hochfahren ist die Position 0. Die Schritte werden bei Verwendung aller möglichen
Fahrfunktionen gezählt (:func:`Set Target Position`, :func:`Set Steps`). 
Es ist auch möglich den Schrittzähler auf 0 oder jeden anderen
gewünschten Wert zu setzen mit :func:`Set Current Position`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Current Velocity',
'elements': [('Velocity', 'int32', 1, 'out', {})], # vactual
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TBD
""",
'de':
"""
TBD
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set Target Position',
'elements': [('Position', 'int32', 1, 'in', {})], # xtarget
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the target position of the stepper motor in steps. For example,
if the current position of the motor is 500 and :func:`Set Target Position` is
called with 1000, the stepper motor will drive 500 steps forward. It will
use the velocity, acceleration and deacceleration as set by
:func:`Set Motion Configuration`.

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
:func:`Set Motion Configuration` gesetzt, verwendet.

Ein Aufruf von :func:`Set Target Position` mit dem Parameter *x* ist
äquivalent mit einem Aufruf von :func:`Set Steps` mit dem Parameter
(*x* - :func:`Get Current Position`).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Target Position',
'elements': [('Position', 'int32', 1, 'out', {})], # xtarget
'since_firmware': [1, 0, 0],
'doc': ['bf', {
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
:func:`Set Motion Configuration` will be used.
""",
'de':
"""
Setzt die Anzahl der Schritte die der Schrittmotor fahren soll.
Positive Werte fahren den Motor vorwärts und negative rückwärts.
Dabei wird die Geschwindigkeit, Beschleunigung und Verzögerung, wie mit
:func:`Set Motion Configuration` gesetzt, verwendet.
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
'elements': [('Step Resolution', 'uint8', 1, 'in', {'constant_group': 'Step Resolution', 'default': 0}), # chopconf mres 0-8
             ('Interpolation', 'bool', 1, 'in', {'default': True})], # chopconf intpol
'since_firmware': [1, 0, 0],
'doc': ['bf', {
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
'elements': [('Step Resolution', 'uint8', 1, 'out', {'constant_group': 'Step Resolution'}), # chopconf mres 0-8
             ('Interpolation', 'bool', 1, 'out', {'default': True})], # chopconf intpol
'since_firmware': [1, 0, 0],
'doc': ['bf', {
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
'function_id': 22,
'name': 'Set Motor Current',
'elements': [('Current', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Ampere'})], # global scaler TODO: , 'range': (360, 1640), 'default': 800
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
'elements': [('Current', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere'})], # global scaler TODO: , 'range': (360, 1640), 'default': 800
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
'name': 'Set Enabled',
'elements': [('Enabled', 'bool', 1, 'in', {})],
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
'name': 'Get Enabled',
'elements': [('Enabled', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TBD
""",
'de':
"""
TBD
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Basic Configuration',
'elements': [('Standstill Current', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Ampere'}), # ihold # TODO: Default depends on version, 'default': 200
             ('Motor Run Current', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Ampere'}), # irun  # TODO: Default depends on version, 'default': 800
             ('Standstill Delay Time', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'range': (0, 327), 'default': 50}), # iholddelay 0-15 * 2^18 t_clk (high level 0-327ms)
             ('Power Down Time', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'range': (0, 5570), 'default': 250}), # tpowerdown 0-255 * 2^18 t_clk (high level 0-5570ms)
             ('Stealth Threshold', 'uint16', 1, 'in', {'unit': 'Steps Per Second', 'default': 500}), # tpwmthrs
             ('Coolstep Threshold', 'uint16', 1, 'in', {'unit': 'Steps Per Second', 'default': 500}), # tcoolthrs
             ('Classic Threshold', 'uint16', 1, 'in', {'unit': 'Steps Per Second', 'default': 1000}), # thigh
             ('High Velocity Chopper Mode', 'bool', 1, 'in', {'default': False})], # chopconf vhighchm
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
'elements': [('Standstill Current', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere'}), # ihold # TODO: Default depends on version, 'default': 200
             ('Motor Run Current', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere'}), # irun # TODO: Default depends on version, 'default': 800
             ('Standstill Delay Time', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'range': (0, 327), 'default': 50}), # iholddelay 0-15 * 2^18 t_clk (high level 0-327ms)
             ('Power Down Time', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'range': (0, 5570), 'default': 250}), # tpowerdown 0-255 * 2^18 t_clk (high level 0-5570ms)
             ('Stealth Threshold', 'uint16', 1, 'out', {'unit': 'Steps Per Second', 'default': 500}), # tpwmthrs
             ('Coolstep Threshold', 'uint16', 1, 'out', {'unit': 'Steps Per Second', 'default': 500}), # tcoolthrs
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
             ('High Velocity Fullstep', 'bool', 1, 'in', {'default': False}), # vhighfs
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

* High Velocity Fullstep: TODO.

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
             ('High Velocity Fullstep', 'bool', 1, 'out', {'default': False}), # vhighfs
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
             ('Offset', 'uint8', 1, 'in', {'default': 128}), # pwm_ofs
             ('Gradient', 'uint8', 1, 'in', {'default': 4}), # pwm_grad
             ('Enable Autoscale', 'bool', 1, 'in', {'default': True}), # pwm_autoscale
             ('Enable Autogradient', 'bool', 1, 'in', {'default': False}), # pwm_autograd
             ('Freewheel Mode', 'uint8', 1, 'in', {'constant_group': 'Freewheel Mode', 'default': 0}), # freewheel
             ('Regulation Loop Gradient', 'uint8', 1, 'in', {'default': 4}), # pwm_reg
             ('Amplitude Limit', 'uint8', 1, 'in', {'default': 12})], # pwm_lim
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

* Enable Autogradient: TODO

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

* Enable Autogradient: TODO

* Freewheel Mode: Der Freewheel Modus definiert das Verhalten im Stillstand, wenn der Standstill Current
  (siehe :func:`Set Basic Configuration`) auf 0 gesetzt wurde.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Stealth Configuration',
'elements': [('Enable Stealth', 'bool', 1, 'out', {'default': True}), # en_pwm_mode
             ('Offset', 'uint8', 1, 'out', {'default': 128}), # pwm_ofs
             ('Gradient', 'uint8', 1, 'out', {'default': 4}), # pwm_grad
             ('Enable Autoscale', 'bool', 1, 'out', {'default': True}), # pwm_autoscale
             ('Enable Autogradient', 'bool', 1, 'out', {'default': False}), # pwm_autograd
             ('Freewheel Mode', 'uint8', 1, 'out', {'constant_group': 'Freewheel Mode', 'default': 0}), # freewheel
             ('Regulation Loop Gradient', 'uint8', 1, 'out', {'default': 4}), # pwm_reg
             ('Amplitude Limit', 'uint8', 1, 'out', {'default': 12})], # pwm_lim
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
'name': 'Set Short Configuration',
'elements': [('Disable Short To Voltage Protection', 'bool', 1, 'in', {'default': False}), # diss2vs
             ('Disable Short To Ground Protection', 'bool', 1, 'in', {'default': False}), # diss2g
             ('Short To Voltage Level', 'uint8', 1, 'in', {'range': (4, 15), 'default': 12}), # s2vs_level 4 high sensivitivy, 15 low
             ('Short To Ground Level', 'uint8', 1, 'in', {'range': (2, 15), 'default': 12}), # s2g_level 2 high sensivitivy, 15 low
             ('Spike Filter Bandwidth', 'uint8', 1, 'in', {'constant_group': 'Spike Filter Bandwidth', 'default': 3}), # shortfilter 100ns, 1000ns, 2000ns, 3000ns
             ('Short Detection Delay', 'bool', 1, 'in', {'default': True}), # shortdelay: False = 750ns, True=1500ns
             ('Filter Time', 'uint8', 1, 'in', {'constant_group': 'Filter Time', 'default': 0})], # filt_isense
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Note: If you don't know what any of this means you can very likely keep all of
the values as default!

Sets miscellaneous configuration parameters.

* Disable Short To Ground Protection: Set to false to enable short to ground protection, otherwise
  it is disabled.

* TODO
""",
'de':
"""
Note: Typischerweise können diese Werte bei ihren Standardwerten gelassen werden. Sie sollten nur
geändert werden, wenn man weiß was man tut.

Setzt verschiedene Parametereinstellungen.

* Disable Short To Ground Protection: Setze diesen Wert auf False um den Kurzschluss nach Masse
  Schutz zu aktivieren. Ansonsten ist dieser deaktiviert.

* TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Short Configuration',
'elements': [('Disable Short To Voltage Protection', 'bool', 1, 'out', {'default': False}), # diss2vs
             ('Disable Short To Ground Protection', 'bool', 1, 'out', {'default': False}), # diss2g
             ('Short To Voltage Level', 'uint8', 1, 'out', {'range': (4, 15), 'default': 12}), # s2vs_level 4 high sensivitivy, 15 low
             ('Short To Ground Level', 'uint8', 1, 'out', {'range': (2, 15), 'default': 12}), # s2g_level 2 high sensivitivy, 15 low
             ('Spike Filter Bandwidth', 'uint8', 1, 'out', {'constant_group': 'Spike Filter Bandwidth', 'default': 3}), # shortfilter 100ns, 1000ns, 2000ns, 3000ns
             ('Short Detection Delay', 'bool', 1, 'out', {'default': True}), # shortdelay: False = 750ns, True=1500ns
             ('Filter Time', 'uint8', 1, 'out', {'constant_group': 'Filter Time', 'default': 0})], # filt_isense
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Short Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Short Configuration` gesetzt.
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
'name': 'Get Input Voltage',
'elements': [('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
TBD
""",
'de':
"""
TBD
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Temperature',
'elements': [('Temperature', 'int16', 1, 'out', {'scale': (1, 10), 'unit': 'Degree'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
TBD
""",
'de':
"""
TBD
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set GPIO Configuration',
'elements': [('Debounce', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 200}),
             ('Stop Deceleration', 'int32', 1, 'in', {'range': (0, 0xFFFF), 'default': 0xFFFF, 'unit': 'Steps Per Second Squared'})], # amax
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TBD
""",
'de':
"""
TBD
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get GPIO Configuration',
'elements': [('Debounce', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 200}),
             ('Stop Deceleration', 'int32', 1, 'out', {'range': (0, 0xFFFF), 'default': 0xFFFF, 'unit': 'Steps Per Second Squared'})], # amax
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TBD
""",
'de':
"""
TBD
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set GPIO Action',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Action', 'uint32', 1, 'in', {'constant_group': 'GPIO Action', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TBD
""",
'de':
"""
TBD
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get GPIO Action',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Action', 'uint32', 1, 'out', {'constant_group': 'GPIO Action', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TBD
""",
'de':
"""
TBD
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get GPIO State',
'elements': [('GPIO State', 'bool', 2, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TBD
""",
'de':
"""
TBD
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Error LED Config',
'elements': [('Config', 'uint8', 1, 'in', {'constant_group': 'Error LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Configures the touch LED to be either turned off, turned on, blink in
heartbeat mode or show TBD.

TODO: 

* one second interval blink: Input voltage too small
* 250ms interval blink: Overtemperature warning
* full red: motor disabled because of short to ground in phase a or b or because of overtemperature

""",
'de':
"""
Konfiguriert die Touch-LED. Die LED kann ausgeschaltet, eingeschaltet,
im Herzschlagmodus betrieben werden. Zusätzlich gibt es die Option
TBD
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Error LED Config',
'elements': [('Config', 'uint8', 1, 'out', {'constant_group': 'Error LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the LED configuration as set by :func:`Set Error LED Config`
""",
'de':
"""
Gibt die LED-Konfiguration zurück, wie von :func:`Set Error LED Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Enable LED Config',
'elements': [('Config', 'uint8', 1, 'in', {'constant_group': 'Enable LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Configures the touch LED to be either turned off, turned on, blink in
heartbeat mode or show TBD.
""",
'de':
"""
Konfiguriert die Touch-LED. Die LED kann ausgeschaltet, eingeschaltet,
im Herzschlagmodus betrieben werden. Zusätzlich gibt es die Option
TBD
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Enable LED Config',
'elements': [('Config', 'uint8', 1, 'out', {'constant_group': 'Enable LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the LED configuration as set by :func:`Set Enable LED Config`
""",
'de':
"""
Gibt die LED-Konfiguration zurück, wie von :func:`Set Enable LED Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Steps LED Config',
'elements': [('Config', 'uint8', 1, 'in', {'constant_group': 'Steps LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Configures the touch LED to be either turned off, turned on, blink in
heartbeat mode or show TBD.
""",
'de':
"""
Konfiguriert die Touch-LED. Die LED kann ausgeschaltet, eingeschaltet,
im Herzschlagmodus betrieben werden. Zusätzlich gibt es die Option
TBD
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Steps LED Config',
'elements': [('Config', 'uint8', 1, 'out', {'constant_group': 'Steps LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the LED configuration as set by :func:`Set Steps LED Config`
""",
'de':
"""
Gibt die LED-Konfiguration zurück, wie von :func:`Set Steps LED Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set GPIO LED Config',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Config', 'uint8', 1, 'in', {'constant_group': 'GPIO LED Config', 'default': 4})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Configures the touch LED to be either turned off, turned on, blink in
heartbeat mode or show TBD.
""",
'de':
"""
Konfiguriert die Touch-LED. Die LED kann ausgeschaltet, eingeschaltet,
im Herzschlagmodus betrieben werden. Zusätzlich gibt es die Option
TBD
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get GPIO LED Config',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Config', 'uint8', 1, 'out', {'constant_group': 'GPIO LED Config', 'default': 4})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the LED configuration as set by :func:`Set GPIO LED Config`
""",
'de':
"""
Gibt die LED-Konfiguration zurück, wie von :func:`Set GPIO LED Config` gesetzt.
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Write Register',
'elements': [('Register', 'uint8', 1, 'in', {}),
             ('Value', 'uint32', 1, 'in', {}),
             ('Status', 'uint8', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TBD
""",
'de':
"""
TBD
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Read Register',
'elements': [('Register', 'uint8', 1, 'in', {}),
             ('Status', 'uint8', 1, 'out', {}),
             ('Value', 'uint32', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TBD
""",
'de':
"""
TBD
"""
}]
})

