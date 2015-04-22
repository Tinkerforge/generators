# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# DC Brick communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Brick',
    'device_identifier': 11,
    'name': ('DC', 'dc', 'DC', 'DC Brick'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Drives one brushed DC motor with up to 28V and 5A (peak)',
        'de': 'Steuert einen Gleichstrommotor mit bis zu 28V und 5A (Peak)'
    },
    'released': True,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('SetVelocity', 'set_velocity'),
'elements': [('velocity', 'int16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
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
Setzt die Geschwindigkeit des Motors. Hierbei sind -32767 maximale
Geschwindigkeit rückwärts, 0 ist Halt und 32767 maximale Geschwindigkeit
vorwärts. In Abhängigkeit von der Beschleunigung (siehe :func:`SetAcceleration`)
wird der Motor nicht direkt auf die Geschwindigkeit gebracht sondern
gleichmäßig beschleunigt.

Die Geschwindigkeit beschreibt das Tastverhältnis der PWM für die
Motoransteuerung. Z.B. entspricht ein Geschwindigkeitswert von 3277 einer PWM
mit einem Tastverhältnis von 10%. Weiterhin kann neben dem Tastverhältnis auch
die Frequenz der PWM verändert werden, siehe :func:`SetPWMFrequency`.

Der Standardwert für die Geschwindigkeit ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetVelocity', 'get_velocity'),
'elements': [('velocity', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the velocity as set by :func:`SetVelocity`.
""",
'de':
"""
Gibt die Geschwindigkeit zurück, wie gesetzt von :func:`SetVelocity`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetCurrentVelocity', 'get_current_velocity'),
'elements': [('velocity', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the *current* velocity of the motor. This value is different
from :func:`GetVelocity` whenever the motor is currently accelerating
to a goal set by :func:`SetVelocity`.
""",
'de':
"""
Gibt die *aktuelle* Geschwindigkeit des Motors zurück. Dieser Wert
unterscheidet sich von :func:`GetVelocity`, sobald der Motor auf einen
neuen Zielwert, wie von :func:`SetVelocity` vorgegeben, beschleunigt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetAcceleration', 'set_acceleration'),
'elements': [('acceleration', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
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
Setzt die Beschleunigung des Motors. Die Einheit dieses Wertes ist
*Geschwindigkeit/s*. Ein Beschleunigungswert von 10000 bedeutet, dass jede
Sekunde die Geschwindigkeit um 10000 erhöht wird (entspricht rund 30%
Tastverhältnis).

Beispiel: Soll die Geschwindigkeit von 0 auf 16000 (entspricht ungefähr
50% Tastverhältnis) in 10 Sekunden beschleunigt werden, so ist die
Beschleunigung auf 1600 einzustellen.

Eine Beschleunigung von 0 bedeutet ein direkter Sprung des Motors auf die
Zielgeschwindigkeit. Es Wird keine Beschleunigungsrampe gefahren.

Der Standardwert für die Beschleunigung beträgt 10000.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAcceleration', 'get_acceleration'),
'elements': [('acceleration', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the acceleration as set by :func:`SetAcceleration`.
""",
'de':
"""
Gibt die Beschleunigung zurück, wie gesetzt von :func:`SetAcceleration`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetPWMFrequency', 'set_pwm_frequency'),
'elements': [('frequency', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
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
Setzt die Frequenz (in Hz) der PWM, welche den Motor steuert.
Der Wertebereich der Frequenz ist 1-20000Hz. Oftmals ist eine
hohe Frequenz geräuschärmer und der Motor läuft dadurch ruhiger. Trotz dessen
führt eine geringe Frequenz zu weniger Schaltvorgängen und somit zu
weniger Schaltverlusten. Bei einer Vielzahl von Motoren ermöglichen
geringere Frequenzen höhere Drehmomente.

Im Allgemeinen kann diese Funktion ignoriert werden, da der Standardwert
höchstwahrscheinlich zu einem akzeptablen Ergebnis führt.

Der Standardwert der Frequenz ist 15 kHz.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetPWMFrequency', 'get_pwm_frequency'),
'elements': [('frequency', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the PWM frequency (in Hz) as set by :func:`SetPWMFrequency`.
""",
'de':
"""
Gibt die PWM Frequenz (in Hz) zurück, wie gesetzt von :func:`SetPWMFrequency`.
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

Call :func:`SetVelocity` with 0 if you just want to stop the motor.
""",
'de':
"""
Führt eine aktive Vollbremsung aus.

.. warning::
 Diese Funktion ist für Notsituationen bestimmt,
 in denen ein unverzüglicher Halt notwendig ist. Abhängig von der aktuellen
 Geschwindigkeit und der Kraft des Motors kann eine Vollbremsung brachial sein.

Ein Aufruf von :func:`SetVelocity` mit 0 erlaubt einen normalen Stopp des Motors.
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
Gibt die externe Eingangsspannung (in mV) zurück. Die externe Eingangsspannung
wird über die schwarze Stromversorgungsbuchse, in den DC Brick, eingespeist.

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
'elements': [('voltage', 'uint16', 1, 'out')],
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
'name': ('Enable', 'enable'),
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Enables the driver chip. The driver parameters can be configured (velocity,
acceleration, etc) before it is enabled.
""",
'de':
"""
Aktiviert die Treiberstufe. Die Treiberparameter können vor der Aktivierung
konfiguriert werden (Geschwindigkeit, Beschleunigung, etc.).
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
Disables the driver chip. The configurations are kept (velocity,
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
'name': ('SetMinimumVoltage', 'set_minimum_voltage'),
'elements': [('voltage', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the minimum voltage in mV, below which the :func:`UnderVoltage` callback
is triggered. The minimum possible value that works with the DC Brick is 6V.
You can use this function to detect the discharge of a battery that is used
to drive the motor. If you have a fixed power supply, you likely do not need
this functionality.

The default value is 6V.
""",
'de':
"""
Setzt die minimale Spannung in mV, bei welcher der :func:`UnderVoltage` Callback
ausgelöst wird. Der kleinste mögliche Wert mit dem der DC Brick noch funktioniert,
ist 6V. Mit dieser Funktion kann eine Entladung der versorgenden Batterie detektiert
werden. Beim Einsatz einer Netzstromversorgung wird diese Funktionalität
höchstwahrscheinlich nicht benötigt.

Der Standardwert ist 6V.
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
Returns the minimum voltage as set by :func:`SetMinimumVoltage`
""",
'de':
"""
Gibt die minimale Spannung zurück, wie von :func:`SetMinimumVoltage` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetDriveMode', 'set_drive_mode'),
'elements': [('mode', 'uint8', 1, 'in', ('DriveMode', 'drive_mode', [('DriveBrake', 'drive_brake', 0),
                                                                     ('DriveCoast', 'drive_coast', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
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
Advantages are: Less current consumption and less demands on the motor and
driver chip.

The default value is 0 = Drive/Brake.
""",
'de':
"""
Setzt den Fahrmodus. Verfügbare Modi sind:

* 0 = Fahren/Bremsen
* 1 = Fahren/Leerlauf

Diese Modi sind verschiedene Arten der Motoransteuerung.

Im Fahren/Bremsen Modus wird der Motor entweder gefahren oder gebremst.
Es gibt keinen Leerlauf. Vorteile sind die lineare Korrelation zwischen PWM und
Geschwindigkeit, präzisere Beschleunigungen und die Möglichkeit mit geringeren
Geschwindigkeiten zu fahren.

Im Fahren/Leerlauf Modus wir der Motor entweder gefahren oder befindet sich
im Leerlauf. Vorteile sind die geringere Stromaufnahme und geringere
Belastung des Motors und der Treiberstufe.

Der Standardwert ist 0 = Fahren/Bremsen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetDriveMode', 'get_drive_mode'),
'elements': [('mode', 'uint8', 1, 'out', ('DriveMode', 'drive_mode', [('DriveBrake', 'drive_brake', 0),
                                                                      ('DriveCoast', 'drive_coast', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the drive mode, as set by :func:`SetDriveMode`.
""",
'de':
"""
Gibt den Fahrmodus zurück, wie von :func:`SetDriveMode` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetCurrentVelocityPeriod', 'set_current_velocity_period'),
'elements': [('period', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets a period in ms with which the :func:`CurrentVelocity` callback is triggered.
A period of 0 turns the callback off.

The default value is 0.
""",
'de':
"""
Setzt die Periode in ms mit welcher der :func:`CurrentVelocity` Callback
ausgelöst wird. Ein Wert von 0 deaktiviert den Callback.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetCurrentVelocityPeriod', 'get_current_velocity_period'),
'elements': [('period', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetCurrentVelocityPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetCurrentVelocityPeriod` gesetzt.
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
'name': ('EmergencyShutdown', 'emergency_shutdown'),
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered if either the current consumption
is too high (above 5A) or the temperature of the driver chip is too high
(above 175°C). These two possibilities are essentially the same, since the
temperature will reach this threshold immediately if the motor consumes too
much current. In case of a voltage below 3.3V (external or stack) this
callback is triggered as well.

If this callback is triggered, the driver chip gets disabled at the same time.
That means, :func:`Enable` has to be called to drive the motor again.

.. note::
 This callback only works in Drive/Brake mode (see :func:`SetDriveMode`). In
 Drive/Coast mode it is unfortunately impossible to reliably read the
 overcurrent/overtemperature signal from the driver chip.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn entweder der Stromverbrauch (über 5A)
oder die Temperatur der Treiberstufe zu hoch ist (über 175°C). Beide
Möglichkeiten sind letztendlich gleichbedeutend, da die Temperatur
ihren Schwellwert überschreitet sobald der Motor zu viel Strom verbraucht.
Im Falle einer Spannung unter 3,3V (Stapel- oder externe
Spannungsversorgung) wird dieser Callback auch ausgelöst.

Sobald dieser Callback ausgelöst wird, wird die Treiberstufe deaktiviert.
Das bedeutet :func:`Enable` muss aufgerufen werden, um den Motor
erneut zu fahren.

.. note::
 Dieser Callback funktioniert nur im Fahren/Bremsen Modus (siehe :func:`SetDriveMode`).
 Im Fahren/Leerlauf Modus ist es leider nicht möglich das
 Überstrom/Übertemperatur-Signal zuverlässig aus dem Chip der Treiberstufe
 auszulesen.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('VelocityReached', 'velocity_reached'),
'elements': [('velocity', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
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
Dieser Callback wird ausgelöst immer wenn eine konfigurierte Geschwindigkeit
erreicht wird. Beispiel: Wenn die aktuelle Geschwindigkeit 0 ist, die
Beschleunigung auf 5000 und die Geschwindigkeit auf 10000 konfiguriert ist,
wird :func:`VelocityReached` nach ungefähr 2 Sekunden ausgelöst, wenn die
konfigurierte Geschwindigkeit letztendlich erreicht ist.

.. note::
 Da es nicht möglich ist eine Rückmeldung vom Gleichstrommotor zu erhalten,
 funktioniert dies nur wenn die konfigurierte Beschleunigung (siehe :func:`SetAcceleration`)
 kleiner oder gleich der maximalen Beschleunigung des Motors ist. Andernfalls
 wird der Motor hinter dem Vorgabewert zurückbleiben und der Callback wird
 zu früh ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('CurrentVelocity', 'current_velocity'),
'elements': [('velocity', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
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
Dieser Callback wird mit der Periode, wie gesetzt mit :func:`SetCurrentVelocityPeriod`,
ausgelöst. Der :word:`parameter` ist die *aktuelle* vom Motor genutzte Geschwindigkeit.

:func:`CurrentVelocity` wird nur nach Ablauf der Periode ausgelöst, wenn sich die
Geschwindigkeit geändert hat.
"""
}]
})

#com['packets'].append({
#'type': 'function',
#'name': ('EnableEncoder', 'enable_encoder'),
#'elements': [],
#'since_firmware': [2, 0, 1],
#'doc': ['af', {
#'en':
#"""
#""",
#'de':
#"""
#"""
#}]
#})
#
#com['packets'].append({
#'type': 'function',
#'name': ('DisableEncoder', 'disable_encoder'),
#'elements': [],
#'since_firmware': [2, 0, 1],
#'doc': ['af', {
#'en':
#"""
#""",
#'de':
#"""
#"""
#}]
#})
#
#com['packets'].append({
#'type': 'function',
#'name': ('IsEncoderEnabled', 'is_encoder_enabled'),
#'elements': [('enabled', 'bool', 1, 'out')],
#'since_firmware': [2, 0, 1],
#'doc': ['af', {
#'en':
#"""
#""",
#'de':
#"""
#"""
#}]
#})
#
#com['packets'].append({
#'type': 'function',
#'name': ('GetEncoderCount', 'get_encoder_count'),
#'elements': [('reset', 'bool', 1, 'in'),
#             ('count', 'int32', 1, 'out')],
#'since_firmware': [2, 0, 1],
#'doc': ['af', {
#'en':
#"""
#""",
#'de':
#"""
#"""
#}]
#})
#
#com['packets'].append({
#'type': 'function',
#'name': ('SetEncoderConfig', 'set_encoder_config'),
#'elements': [('counts_per_revolution', 'uint16', 1, 'in')],
#'since_firmware': [2, 0, 1],
#'doc': ['af', {
#'en':
#"""
#""",
#'de':
#"""
#"""
#}]
#})
#
#com['packets'].append({
#'type': 'function',
#'name': ('GetEncoderConfig', 'get_encoder_config'),
#'elements': [('counts_per_revolution', 'uint16', 1, 'out')],
#'since_firmware': [2, 0, 1],
#'doc': ['af', {
#'en':
#"""
#""",
#'de':
#"""
#"""
#}]
#})
#
#com['packets'].append({
#'type': 'function',
#'name': ('SetEncoderPIDConfig', 'set_encoder_pid_config'),
#'elements': [('p', 'float', 1, 'in'),
#             ('i', 'float', 1, 'in'),
#             ('d', 'float', 1, 'in'),
#             ('sample_time', 'uint8', 1, 'in')],
#'since_firmware': [2, 0, 1],
#'doc': ['af', {
#'en':
#"""
#""",
#'de':
#"""
#"""
#}]
#})
#
#com['packets'].append({
#'type': 'function',
#'name': ('GetEncoderPIDConfig', 'get_encoder_pid_config'),
#'elements': [('p', 'float', 1, 'out'),
#             ('i', 'float', 1, 'out'),
#             ('d', 'float', 1, 'out'),
#             ('sample_time', 'uint8', 1, 'out')],
#'since_firmware': [2, 0, 1],
#'doc': ['af', {
#'en':
#"""
#""",
#'de':
#"""
#"""
#}]
#})
