# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# DC Bricklet 2.0 communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2156,
    'name': 'DC V2',
    'display_name': 'DC 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'TBD',
        'de': 'TBD'
    },
    'released': False,
    'documented': False,
    'discontinued': False,
    'features': [
        'device',
        'comcu_bricklet',
        'bricklet_get_identity'
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

com['constant_groups'].append({
'name': 'GPIO Action',
'type': 'uint32',
'constants': [('None', 0),
              ('Normal Stop Rising Edge', 1 << 0),   
              ('Normal Stop Falling Edge', 1 << 1),
              ('Full Brake Rising Edge', 1 << 2),
              ('Full Brake Falling Edge', 1 << 3),
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
'name': 'CW LED Config',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Show Heartbeat', 2),
              ('Show CW As Forward', 3),
              ('Show CW As Backward', 4)]
})

com['constant_groups'].append({
'name': 'CCW LED Config',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Show Heartbeat', 2),
              ('Show CCW As Forward', 3),
              ('Show CCW As Backward', 4)]
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



com['packets'].append({
'type': 'function',
'name': 'Set Enabled',
'elements': [('Enabled', 'bool', 1, 'in', {})],
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
'name': 'Get Enabled',
'elements': [('Enabled', 'bool', 1, 'out', {'default': False})],
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
'name': 'Set Velocity',
'elements': [('Velocity', 'int16', 1, 'in', {'scale': (100, 32767), 'unit': 'Percent', 'range': (-32767, 32767), 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the velocity of the motor. Whereas -32767 is full speed backward,
0 is stop and 32767 is full speed forward. Depending on the
acceleration (see TBD), the motor is not immediately
brought to the velocity but smoothly accelerated.

The velocity describes the duty cycle of the PWM with which the motor is
controlled, e.g. a velocity of 3277 sets a PWM with a 10% duty cycle.
You can not only control the duty cycle of the PWM but also the frequency,
see TBD.
""",
'de':
"""
Setzt die Geschwindigkeit des Motors. Hierbei sind -32767 maximale
Geschwindigkeit rückwärts, 0 ist Halt und 32767 maximale Geschwindigkeit
vorwärts. In Abhängigkeit von der Beschleunigung (siehe TBD)
wird der Motor nicht direkt auf die Geschwindigkeit gebracht sondern
gleichmäßig beschleunigt.

Die Geschwindigkeit beschreibt das Tastverhältnis der PWM für die
Motoransteuerung. Z.B. entspricht ein Geschwindigkeitswert von 3277 einer PWM
mit einem Tastverhältnis von 10%. Weiterhin kann neben dem Tastverhältnis auch
die Frequenz der PWM verändert werden, siehe TBD.
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
'name': 'Set Motion',
'elements': [('Acceleration', 'uint16', 1, 'in', {'scale': (100, 32767), 'unit': 'Percent Per Second', 'default': 10000}),
             ('Deceleration', 'uint16', 1, 'in', {'scale': (100, 32767), 'unit': 'Percent Per Second', 'default': 10000})],
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
'name': 'Get Motion',
'elements': [('Acceleration', 'uint16', 1, 'out', {'scale': (100, 32767), 'unit': 'Percent Per Second', 'default': 10000}),
             ('Deceleration', 'uint16', 1, 'out', {'scale': (100, 32767), 'unit': 'Percent Per Second', 'default': 10000})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the acceleration as set by :func:`Set Motion`.
""",
'de':
"""
Gibt die Beschleunigung zurück, wie gesetzt von :func:`Set Motion`.
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
'doc': ['bf', {
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
'name': 'Get Power Statistics',
'elements': [('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'}),
             ('Current', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere'}),
             ('Temperature', 'int16', 1, 'out', {'scale': (1, 10), 'unit': 'Degree'})],
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
'name': 'Set GPIO Configuration',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Debounce', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 200}),
             ('Stop Deceleration', 'uint16', 1, 'in', {'default': 0xFFFF, 'unit': 'Steps Per Second Squared'})],
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
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Debounce', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 200}),
             ('Stop Deceleration', 'uint16', 1, 'out', {'default': 0xFFFF, 'unit': 'Steps Per Second Squared'})],
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
'name': 'Set CW LED Config',
'elements': [('Config', 'uint8', 1, 'in', {'constant_group': 'CW LED Config', 'default': 3})],
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
'name': 'Get CW LED Config',
'elements': [('Config', 'uint8', 1, 'out', {'constant_group': 'CW LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the LED configuration as set by :func:`Set CW LED Config`
""",
'de':
"""
Gibt die LED-Konfiguration zurück, wie von :func:`Set CW LED Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set CCW LED Config',
'elements': [('Config', 'uint8', 1, 'in', {'constant_group': 'CCW LED Config', 'default': 3})],
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
'name': 'Get CCW LED Config',
'elements': [('Config', 'uint8', 1, 'out', {'constant_group': 'CCW LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the LED configuration as set by :func:`Set CCW LED Config`
""",
'de':
"""
Gibt die LED-Konfiguration zurück, wie von :func:`Set CCW LED Config` gesetzt.
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
