# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Performance DC Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2156,
    'name': 'Performance DC',
    'display_name': 'Performance DC',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Drives one brushed DC motor with up to 36V and 10A',
        'de': 'Steuert einen Gleichstrommotor mit bis zu 36V und 10A'
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
Enables/Disables the driver chip. The driver parameters can be configured (velocity,
acceleration, etc) before it is enabled.
""",
'de':
"""
Aktiviert/Deaktiviert die Treiberstufe. Die Treiberparameter können vor der Aktivierung
konfiguriert werden (Geschwindigkeit, Beschleunigung, etc.).
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
'name': 'Set Velocity',
'elements': [('Velocity', 'int16', 1, 'in', {'scale': (100, 32767), 'unit': 'Percent', 'range': (-32767, 32767), 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the velocity of the motor. Whereas -32767 is full speed backward,
0 is stop and 32767 is full speed forward. Depending on the
acceleration (see :func:`Set Motion`), the motor is not immediately
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
vorwärts. In Abhängigkeit von der Beschleunigung (siehe :func:`Set Motion`)
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
'name': 'Set Motion',
'elements': [('Acceleration', 'uint16', 1, 'in', {'scale': (100, 32767), 'unit': 'Percent Per Second', 'default': 10000}),
             ('Deceleration', 'uint16', 1, 'in', {'scale': (100, 32767), 'unit': 'Percent Per Second', 'default': 10000})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the acceleration and deceleration of the motor. It is given in *velocity/s*. An
acceleration of 10000 means, that every second the velocity is increased
by 10000 (or about 30% duty cycle).

For example: If the current velocity is 0 and you want to accelerate to a
velocity of 16000 (about 50% duty cycle) in 10 seconds, you should set
an acceleration of 1600.

If acceleration and deceleration is set to 0, there is no speed ramping, i.e. a new velocity
is immediately given to the motor.
""",
'de':
"""
Setzt die Beschleunigung/Debeschleunigung des Motors. Die Einheit dieses Wertes ist
*Geschwindigkeit/s*. Ein Beschleunigungswert von 10000 bedeutet, dass jede
Sekunde die Geschwindigkeit um 10000 erhöht wird (entspricht rund 30%
Tastverhältnis).

Beispiel: Soll die Geschwindigkeit von 0 auf 16000 (entspricht ungefähr
50% Tastverhältnis) in 10 Sekunden beschleunigt werden, so ist die
Beschleunigung auf 1600 einzustellen.

Eine Beschleunigung/Debeschleunigung von 0 bedeutet ein direkter Sprung des Motors auf die
Zielgeschwindigkeit. Es Wird keine Rampe gefahren.
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
Returns the acceleration/deceleration as set by :func:`Set Motion`.
""",
'de':
"""
Gibt die Beschleunigung/Debeschleunigung zurück, wie gesetzt von :func:`Set Motion`.
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
Returns input voltage, current usage and temperature of the driver.
""",
'de':
"""
Gibt die Eingangsspannung, den Stromverbrauch und die Temperatur des Treibers zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Thermal Shutdown',
'elements': [('Temperature', 'uint8', 1, 'in', {'unit': 'Degree', 'default': 125})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets a temperature threshold that is used for thermal shutdown.

Additionally to this user defined threshold the driver chip will shut down at a temperature of 150°C.

If a thermal sthudown is triggered the driver is disabled and has to be explicitely re-enabled with :func:`Set Enabled`.
""",
'de':
"""
Setzt den Temperatur-Grenzwert für eine thermale Abschaltung.

Neben diesem nutzerdefinierten Grenzwert schaltet er Treiber selbst ab einer Temperatur von 150° ab.

Wenn es zu einer thermalen Abschaltung kommt wird der Treiber deaktiviert und er muss explizit per :func:`Set Enabled` wieder aktiviert werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Thermal Shutdown',
'elements': [('Temperature', 'uint8', 1, 'out', {'unit': 'Degree'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the thermal shutdown temperature as set by :func:`Set Thermal Shutdown`.
""",
'de':
"""
Gibt die thermale Abschalttemperatur zurück, wie von :func:`Set Thermal Shutdown` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set GPIO Configuration',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Debounce', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 200}),
             ('Stop Deceleration', 'uint16', 1, 'in', {'scale': (100, 32767), 'unit': 'Percent Per Second', 'default': 0xFFFF})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the GPIO configuration for the given channel. 
You can configure a debounce and the deceleration that is used if the action is configured as ``normal stop``. See :func:`Set GPIO Action`.
""",
'de':
"""
Setzt die GPIO-Konfiguration für einen Kanal.
Es kann ein Debounce und eine Debeschleunigung gesetzt werden. Letzteres wird genutzt wenn die Action auf ``normal stop`` konfiguriert ist. Siehe :func:`Set GPIO Action`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get GPIO Configuration',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Debounce', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 200}),
             ('Stop Deceleration', 'uint16', 1, 'out', {'scale': (100, 32767), 'unit': 'Percent Per Second', 'default': 0xFFFF})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the GPIO configuration for a channel as set by :func:`Set GPIO Configuration`.
""",
'de':
"""
Gibt die GPIO-Konfiguration für einen Kanal zurück, wie von :func:`Set GPIO Configuration` gesetzt.
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
Sets the GPIO action for the given channel. 

The action can be a normal stop, a full brake or a callback. Each for a rising edge or falling edge.
The actions are a bitmask they can be used at the same time. 
You can for example trigger a full brake and a callback at the same time or for rising and falling edge.

The deceleration speed for the normal stop can be configured with :func:`Set GPIO Configuration`.
""",
'de':
"""
Setzt die GPIO-Action für einen Kanal.

Die Action kann ein ``normal stop``, ein ``full brake`` oder ein ``callback`` sein. Jeweils für eine steigende oder fallende Flanke.
Die Actions sind eine Bitmaske und sie können simultan verwendet werden.
Es ist zum Beispiel möglich einen ``full brake`` und ``callback`` gleichzeitig zu triggern oder eine auf eine steigende und fallende Flanke gleichzeitig.

Die Debeschleunigung für den ``normal stop`` kann über :func:`Set GPIO Configuration` konfiguriert werden.
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
Returns the GPIO action for a channel as set by :func:`Set GPIO Action`.
""",
'de':
"""
Gibt die GPIO-Action für einen Kanal zurück, wie von :func:`Set GPIO Action` gesetzt.
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
Returns the GPIO state for both channels. True if the state is ``high`` and false if the state is ``low``.
""",
'de':
"""
Gibt den GPIO-Zustand für beide Kanäle zurück. True wenn der der Zustand ``high`` ist und false wenn der Zustand ``low`` ist.
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
Configures the error LED to be either turned off, turned on, blink in
heartbeat mode or show an error.

If the LED is configured to show errors it has three different states:

* Off: No error present.
* 1s interval blinking: Input voltage too low (below 6V).
* 250ms interval blinking: Overtemperature or overcurrent.

""",
'de':
"""
Konfiguriert die Touch-LED. Die LED kann ausgeschaltet, eingeschaltet,
im Herzschlagmodus betrieben werden. Zusätzlich gibt es die Option den Fehler-Status anzuzueigen.

Wenn die LED konfiguriert ist um Fehler anzuzueigen gibt es drei unterschiedliche Zustände:

* Aus: Es liegt kein Fehler vor.
* 1s Intervall-Blinken: Eingangsspannung zu klein (unter 6V).
* 250ms Intervall-Blinken: Übertertemperatur oder Überstrom.

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
Configures the CW LED to be either turned off, turned on, blink in
heartbeat mode or if the motor turn clockwise.
""",
'de':
"""
Konfiguriert die CW-LED. Die LED kann ausgeschaltet, eingeschaltet,
im Herzschlagmodus betrieben werden. Zusätzlich gibt es die Option anzuzeigen ob der Motor im Uhrzeigersinn dreht.
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
Configures the CCW LED to be either turned off, turned on, blink in
heartbeat mode or if the motor turn counter-clockwise.
""",
'de':
"""
Konfiguriert die CCW-LED. Die LED kann ausgeschaltet, eingeschaltet,
im Herzschlagmodus betrieben werden. Zusätzlich gibt es die Option anzuzeigen ob der Motor gegen den Uhrzeigersinn dreht.

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
Configures the GPIO LED to be either turned off, turned on, blink in
heartbeat mode or the GPIO state.

The GPIO LED can be configured for both channels.
""",
'de':
"""
Konfiguriert die GPIO-LED. Die LED kann ausgeschaltet, eingeschaltet,
im Herzschlagmodus betrieben werden. Zusätzlich gibt es die Option den GPIO-Zustand anzuzeigen.

Die GPIO-LED kann für beide Kanäle konfiguriert werden.
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
'name': 'Set Emergency Shutdown Callback Configuration',
'elements': [('Enabled', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Enable/Disable :cb:`Emergency Shutdown` callback.
""",
'de':
"""
Aktiviert/Deaktiviert :cb:`Emergency Shutdown` Callback.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Emergency Shutdown Callback Configuration',
'elements': [('Enabled', 'bool', 1, 'out', {'default': True})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set Emergency Shutdown Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set Emergency Shutdown Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Velocity Reached Callback Configuration',
'elements': [('Enabled', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Enable/Disable :cb:`Velocity Reached` callback.
""",
'de':
"""
Aktiviert/Deaktiviert :cb:`Velocity Reached` Callback.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Velocity Reached Callback Configuration',
'elements': [('Enabled', 'bool', 1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set Velocity Reached Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set Velocity Reached Callback Configuration` gesetzt.
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set Current Velocity Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period is the period with which the :cb:`Current Velocity`
callback is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.
""",
'de':
"""
Die Periode ist die Periode mit der der :cb:`Current Velocity`
Callback ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn der Wert sich im Vergleich zum letzten mal geändert
hat. Ändert der Wert sich nicht innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen des Werts.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Current Velocity Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set Current Velocity Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set Current Velocity Callback Configuration` gesetzt.
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
is too high or the temperature of the driver chip is too high
(above 150°C) or the user defined thermal shutdown is triggered (see :func:`Set Thermal Shutdown`). 
n case of a voltage below 6V (input voltage) this
callback is triggered as well.

If this callback is triggered, the driver chip gets disabled at the same time.
That means, :func:`Set Enabled` has to be called to drive the motor again.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn entweder der Stromverbrauch 
oder die Temperatur der Treiberstufe zu hoch ist (über 150°C) oder die
nutzerdefinierte thermale Abschaltungstemperatur überstiegen wird (siehe :func:`Set Thermal Shutdown`). 
Im Falle einer Spannung unter 6V (Eingangsspannung) wird dieser Callback auch ausgelöst.

Sobald dieser Callback ausgelöst wird, wird die Treiberstufe deaktiviert.
Das bedeutet :func:`Set Enabled` muss aufgerufen werden, um den Motor
erneut zu fahren.
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
 acceleration (see :func:`Set Motion`) is set smaller or equal to the
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
 :func:`Set Motion`) kleiner oder gleich der maximalen Beschleunigung
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
:func:`Set Current Velocity Callback Configuration`. The :word:`parameter` is the *current*
velocity used by the motor.

The :cb:`Current Velocity` callback is only triggered after the set period
if there is a change in the velocity.
""",
'de':
"""
Dieser Callback wird mit der Periode, wie gesetzt mit
:func:`Set Current Velocity Callback Configuration`, ausgelöst. Der :word:`parameter` ist die
*aktuelle* vom Motor genutzte Geschwindigkeit.

Der :cb:`Current Velocity` Callback wird nur nach Ablauf der Periode
ausgelöst, wenn sich die Geschwindigkeit geändert hat.
"""
}]
})
