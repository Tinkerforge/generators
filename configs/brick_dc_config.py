# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# DC Brick communication config

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 3],
    'category': 'Brick',
    'device_identifier': 11,
    'name': 'DC',
    'display_name': 'DC',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Drives one brushed DC motor with up to 28V and 5A (peak)',
        'de': 'Steuert einen Gleichstrommotor mit bis zu 28V und 5A (Peak)'
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
        'eeprom_bricklet_host',
        'comcu_bricklet_host'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append({
'name': 'Drive Mode',
'type': 'uint8',
'constants': [('Drive Brake', 0),
              ('Drive Coast', 1)]
})

com['packets'].append({
'type': 'function',
'name': 'Set Velocity',
'elements': [('Velocity', 'int16', 1, 'in', {'scale': (100, 32767), 'unit': 'Percent', 'range': (-32767, 32767), 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the velocity of the motor. Whereas -32767 is full speed backward,
0 is stop and 32767 is full speed forward. Depending on the
acceleration (see :func:`Set Acceleration`), the motor is not immediately
brought to the velocity but smoothly accelerated.

The velocity describes the duty cycle of the PWM with which the motor is
controlled, e.g. a velocity of 3277 sets a PWM with a 10% duty cycle.
You can not only control the duty cycle of the PWM but also the frequency,
see :func:`Set PWM Frequency`.
""",
'de':
"""
Setzt die Geschwindigkeit des Motors. Hierbei sind -32767 maximale
Geschwindigkeit rückwärts, 0 ist Halt und 32767 maximale Geschwindigkeit
vorwärts. In Abhängigkeit von der Beschleunigung (siehe :func:`Set Acceleration`)
wird der Motor nicht direkt auf die Geschwindigkeit gebracht sondern
gleichmäßig beschleunigt.

Die Geschwindigkeit beschreibt das Tastverhältnis der PWM für die
Motoransteuerung. Z.B. entspricht ein Geschwindigkeitswert von 3277 einer PWM
mit einem Tastverhältnis von 10%. Weiterhin kann neben dem Tastverhältnis auch
die Frequenz der PWM verändert werden, siehe :func:`Set PWM Frequency`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Velocity',
'elements': [('Velocity', 'int16', 1, 'out', {'scale': (100, 32767), 'unit': 'Percent', 'range': (-32767, 32767), 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the velocity as set by :func:`Set Velocity`.
""",
'de':
"""
Gibt die Geschwindigkeit zurück, wie gesetzt von :func:`Set Velocity`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Current Velocity',
'elements': [('Velocity', 'int16', 1, 'out', {'scale': (100, 32767), 'unit': 'Percent', 'range': (-32767, 32767), 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the *current* velocity of the motor. This value is different
from :func:`Get Velocity` whenever the motor is currently accelerating
to a goal set by :func:`Set Velocity`.
""",
'de':
"""
Gibt die *aktuelle* Geschwindigkeit des Motors zurück. Dieser Wert
unterscheidet sich von :func:`Get Velocity`, sobald der Motor auf einen
neuen Zielwert, wie von :func:`Set Velocity` vorgegeben, beschleunigt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Acceleration',
'elements': [('Acceleration', 'uint16', 1, 'in', {'scale':(100, 32767), 'unit': 'Percent Per Second', 'default': 10000})],
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
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Acceleration',
'elements': [('Acceleration', 'uint16', 1, 'out', {'scale':(100, 32767), 'unit': 'Percent Per Second', 'default': 10000})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the acceleration as set by :func:`Set Acceleration`.
""",
'de':
"""
Gibt die Beschleunigung zurück, wie gesetzt von :func:`Set Acceleration`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set PWM Frequency',
'elements': [('Frequency', 'uint16', 1, 'in', {'unit': 'Hertz', 'range': (1, 20000), 'default': 15000})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the frequency of the PWM with which the motor is driven.
Often a high frequency
is less noisy and the motor runs smoother. However, with a low frequency
there are less switches and therefore fewer switching losses. Also with
most motors lower frequencies enable higher torque.

If you have no idea what all this means, just ignore this function and use
the default frequency, it will very likely work fine.

""",
'de':
"""
Setzt die Frequenz der PWM, welche den Motor steuert.
Oftmals ist eine
hohe Frequenz geräuschärmer und der Motor läuft dadurch ruhiger. Trotz dessen
führt eine geringe Frequenz zu weniger Schaltvorgängen und somit zu
weniger Schaltverlusten. Bei einer Vielzahl von Motoren ermöglichen
geringere Frequenzen höhere Drehmomente.

Im Allgemeinen kann diese Funktion ignoriert werden, da der Standardwert
höchstwahrscheinlich zu einem akzeptablen Ergebnis führt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get PWM Frequency',
'elements': [('Frequency', 'uint16', 1, 'out', {'unit': 'Hertz', 'range': (1, 20000), 'default': 15000})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the PWM frequency as set by :func:`Set PWM Frequency`.
""",
'de':
"""
Gibt die PWM Frequenz zurück, wie gesetzt von :func:`Set PWM Frequency`.
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

Call :func:`Set Velocity` with 0 if you just want to stop the motor.
""",
'de':
"""
Führt eine aktive Vollbremsung aus.

.. warning::
 Diese Funktion ist für Notsituationen bestimmt,
 in denen ein unverzüglicher Halt notwendig ist. Abhängig von der aktuellen
 Geschwindigkeit und der Kraft des Motors kann eine Vollbremsung brachial sein.

Ein Aufruf von :func:`Set Velocity` mit 0 erlaubt einen normalen Stopp des Motors.
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
Gibt die externe Eingangsspannung zurück. Die externe Eingangsspannung
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
'name': 'Get Current Consumption',
'elements': [('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the current consumption of the motor.
""",
'de':
"""
Gibt die Stromaufnahme des Motors zurück.
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
'name': 'Disable',
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
'name': 'Is Enabled',
'elements': [('Enabled', 'bool', 1, 'out', {'default': False})],
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
'name': 'Set Minimum Voltage',
'elements': [('Voltage', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Volt', 'default': 6000})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets the minimum voltage, below which the :cb:`Under Voltage` callback
is triggered. The minimum possible value that works with the DC Brick is 6V.
You can use this function to detect the discharge of a battery that is used
to drive the motor. If you have a fixed power supply, you likely do not need
this functionality.
""",
'de':
"""
Setzt die minimale Spannung, bei welcher der :cb:`Under Voltage` Callback
ausgelöst wird. Der kleinste mögliche Wert mit dem der DC Brick noch funktioniert,
ist 6V. Mit dieser Funktion kann eine Entladung der versorgenden Batterie detektiert
werden. Beim Einsatz einer Netzstromversorgung wird diese Funktionalität
höchstwahrscheinlich nicht benötigt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Minimum Voltage',
'elements': [('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt', 'default': 6000})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the minimum voltage as set by :func:`Set Minimum Voltage`
""",
'de':
"""
Gibt die minimale Spannung zurück, wie von :func:`Set Minimum Voltage` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Drive Mode',
'elements': [('Mode', 'uint8', 1, 'in', {'constant_group': 'Drive Mode', 'default': 0})],
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
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Drive Mode',
'elements': [('Mode', 'uint8', 1, 'out', {'constant_group': 'Drive Mode', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the drive mode, as set by :func:`Set Drive Mode`.
""",
'de':
"""
Gibt den Fahrmodus zurück, wie von :func:`Set Drive Mode` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Current Velocity Period',
'elements': [('Period', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Sets a period with which the :cb:`Current Velocity` callback is triggered.
A period of 0 turns the callback off.
""",
'de':
"""
Setzt die Periode mit welcher der :cb:`Current Velocity` Callback
ausgelöst wird. Ein Wert von 0 deaktiviert den Callback.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Current Velocity Period',
'elements': [('Period', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`Set Current Velocity Period`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`Set Current Velocity Period` gesetzt.
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
'name': 'Emergency Shutdown',
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
 This callback only works in Drive/Brake mode (see :func:`Set Drive Mode`). In
 Drive/Coast mode it is unfortunately impossible to reliably read the
 overcurrent/overtemperature signal from the driver chip.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn entweder der Stromverbrauch (über 5A)
oder die Temperatur der Treiberstufe zu hoch ist (über 175°C). Beide
Möglichkeiten sind letztendlich gleichbedeutend, da die Temperatur
ihren Schwellwert überschreitet sobald der Motor zu viel Strom verbraucht.
Im Falle einer Spannung unter 3,3V (Stapel- oder externe
Spannungsversorgung) wird dieser Callback auch ausgelöst.

Sobald dieser Callback ausgelöst wird, wird die Treiberstufe deaktiviert.
Das bedeutet :func:`Enable` muss aufgerufen werden, um den Motor
erneut zu fahren.

.. note::
 Dieser Callback funktioniert nur im Fahren/Bremsen Modus (siehe
 :func:`Set Drive Mode`). Im Fahren/Leerlauf Modus ist es leider nicht möglich
 das Überstrom/Übertemperatur-Signal zuverlässig aus dem Chip der Treiberstufe
 auszulesen.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Velocity Reached',
'elements': [('Velocity', 'int16', 1, 'out', {'scale': (100, 32767), 'unit': 'Percent', 'range': (-32767, 32767)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered whenever a set velocity is reached. For example:
If a velocity of 0 is present, acceleration is set to 5000 and velocity
to 10000, the :cb:`Velocity Reached` callback will be triggered after about
2 seconds, when the set velocity is actually reached.

.. note::
 Since we can't get any feedback from the DC motor, this only works if the
 acceleration (see :func:`Set Acceleration`) is set smaller or equal to the
 maximum acceleration of the motor. Otherwise the motor will lag behind the
 control value and the callback will be triggered too early.
""",
'de':
"""
Dieser Callback wird ausgelöst immer wenn eine konfigurierte Geschwindigkeit
erreicht wird. Beispiel: Wenn die aktuelle Geschwindigkeit 0 ist, die
Beschleunigung auf 5000 und die Geschwindigkeit auf 10000 konfiguriert ist,
wird der :cb:`Velocity Reached` Callback nach ungefähr 2 Sekunden ausgelöst,
wenn die konfigurierte Geschwindigkeit letztendlich erreicht ist.

.. note::
 Da es nicht möglich ist eine Rückmeldung vom Gleichstrommotor zu erhalten,
 funktioniert dies nur wenn die konfigurierte Beschleunigung (siehe
 :func:`Set Acceleration`) kleiner oder gleich der maximalen Beschleunigung
 des Motors ist. Andernfalls wird der Motor hinter dem Vorgabewert
 zurückbleiben und der Callback wird zu früh ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Current Velocity',
'elements': [('Velocity', 'int16', 1, 'out', {'scale': (100, 32767), 'unit': 'Percent', 'range': (-32767, 32767)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered with the period that is set by
:func:`Set Current Velocity Period`. The :word:`parameter` is the *current*
velocity used by the motor.

The :cb:`Current Velocity` callback is only triggered after the set period
if there is a change in the velocity.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Current Velocity Period`, ausgelöst. Der :word:`parameter` ist die
*aktuelle* vom Motor genutzte Geschwindigkeit.

Der :cb:`Current Velocity` Callback wird nur nach Ablauf der Periode
ausgelöst, wenn sich die Geschwindigkeit geändert hat.
"""
}]
})

#com['packets'].append({
#'type': 'function',
#'name': 'Enable Encoder',
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
#'name': 'Disable Encoder',
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
#'name': 'Is Encoder Enabled',
#'elements': [('Enabled', 'bool', 1, 'out')],
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
#'name': 'Get Encoder Count',
#'elements': [('Reset', 'bool', 1, 'in'),
#             ('Count', 'int32', 1, 'out')],
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
#'name': 'Set Encoder Config',
#'elements': [('Counts Per Revolution', 'uint16', 1, 'in')],
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
#'name': 'Get Encoder Config',
#'elements': [('Counts Per Revolution', 'uint16', 1, 'out')],
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
#'name': 'Set Encoder PID Config',
#'elements': [('P', 'float', 1, 'in'),
#             ('I', 'float', 1, 'in'),
#             ('D', 'float', 1, 'in'),
#             ('Sample Time', 'uint8', 1, 'in')],
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
#'name': 'Get Encoder PID Config',
#'elements': [('P', 'float', 1, 'out'),
#             ('I', 'float', 1, 'out'),
#             ('D', 'float', 1, 'out'),
#             ('Sample Time', 'uint8', 1, 'out')],
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

com['examples'].append({
'name': 'Configuration',
'functions': [('setter', 'Set Drive Mode', [('uint8:constant', 1)], None, None),
              ('setter', 'Set PWM Frequency', [('uint16', 10000)], None, 'Use PWM frequency of 10kHz'),
              ('setter', 'Set Acceleration', [('uint16', 5000)], None, 'Slow acceleration'),
              ('setter', 'Set Velocity', [('int16', 32767)], None, 'Full speed forward'),
              ('setter', 'Enable', [], None, 'Enable motor power'),
              ('wait',)],
'cleanups': [('setter', 'Disable', [], None, 'Disable motor power')]
})

com['examples'].append({
'name': 'Callback',
'functions': [('setter', 'Set Acceleration', [('uint16', 5000)], 'The acceleration has to be smaller or equal to the maximum\nacceleration of the DC motor, otherwise the velocity reached\ncallback will be called too early', 'Slow acceleration'),
              ('setter', 'Set Velocity', [('int16', 32767)], None, 'Full speed forward'),
              ('callback', ('Velocity Reached', 'velocity reached'), [(('Velocity', 'Velocity'), 'int16', 1, None, None, None)], 'Use velocity reached callback to swing back and forth\nbetween full speed forward and full speed backward', None),
              ('setter', 'Enable', [], 'Enable motor power', None)],
'cleanups': [('setter', 'Disable', [], None, 'Disable motor power')],
'incomplete': True # because of special drive logic in callback
})

com['openhab'] = {
    'imports': oh_generic_channel_imports() + oh_generic_trigger_channel_imports() + ['org.eclipse.smarthome.core.library.types.DecimalType'],
    'param_groups': oh_generic_channel_param_groups(),
    'params': [
        {
            'name': 'Minimum Voltage',
            'type': 'decimal',
            'unit': 'V',
            'label': 'Minimum Voltage',
            'description': 'The minimum voltage in V, below which the Under Voltage channel is triggered. The minimum possible value that works with the DC Brick is 5V. You can use this function to detect the discharge of a battery that is used to drive the stepper motor. If you have a fixed power supply, you likely do not need this functionality. The default value is 5V.',
            'default': 5,
        }
    ],
    'init_code': """this.setMinimumVoltage((int)(cfg.minimumVoltage.doubleValue() * 1000.0));""",
    'channels': [{
            'id': 'Velocity Reached',
            'type': 'system.trigger',
            'label': 'Velocity Reached',

            'callbacks': [{
                'packet': 'Velocity Reached',
                'transform': 'CommonTriggerEvents.PRESSED'}],

            'is_trigger_channel': True
        }, {
            'id': 'Emergency Shutdown',
            'type': 'system.trigger',
            'label': 'Emergency Shutdown',

            'callbacks': [{
                'packet': 'Emergency Shutdown',
                'transform': 'CommonTriggerEvents.PRESSED'}],

            'is_trigger_channel': True
        },  {
            'id': 'Under Voltage',
            'type': 'system.trigger',
            'label': 'Under Voltage',

            'callbacks': [{
                'packet': 'Under Voltage',
                'transform': 'CommonTriggerEvents.PRESSED'}],

            'is_trigger_channel': True
        }, {
            'id': 'Current Velocity',
            'type': 'Current Velocity',
            'getters': [{
                'packet': 'Get Current Velocity',
                'packet_params': [],
                'transform': 'new DecimalType(value)'}],
            'callbacks': [{
                'packet': 'Current Velocity',
                'transform': 'new DecimalType(velocity)'}],

            'is_trigger_channel': False,
            'init_code': """this.setCurrentVelocityPeriod(channelCfg.updateInterval);"""
        }
    ],
    'channel_types': [
        oh_generic_channel_type('Current Velocity', 'Number', 'Current Velocity',
            description='The current velocity of the motor.',
            read_only=True,
            min_=-32767,
            max_=32767),
    ],
    'actions': [
        'Set Velocity', 'Get Velocity', 'Get Current Velocity',
        'Set Acceleration', 'Get Acceleration',
        'Full Brake',
        'Enable', 'Disable', 'Is Enabled',
        'Set PWM Frequency', 'Get PWM Frequency',
        'Get Stack Input Voltage', 'Get External Input Voltage',
        'Get Current Consumption',
        'Set Drive Mode', 'Get Drive Mode',
        'Get Minimum Voltage'
    ]
}
