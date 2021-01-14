# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Servo Bricklet 2.0 communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2157,
    'name': 'Servo V2',
    'display_name': 'Servo 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Drives up to 10 RC Servos',
        'de': 'Steuert bis zu 10 RC Servos'
    },
    'released': True,
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

com['doc'] = {
'en':
"""
Every function of the Servo Brick API that has a *servo_channel* parameter can
address a servo with the servo channel (0 to 9). If it is a setter function then
multiple servos can be addressed at once with a bitmask for the
servos, if the highest bit is set. For example: ``1`` will address servo 1,
``(1 << 1) | (1 << 5) | (1 << 15)`` will address servos 1 and 5.
This allows to set configurations to several
servos with one function call. It is guaranteed that the changes will take
effect in the same PWM period for all servos you specified in the bitmask.
""",
'de':
"""
Jede Funktion der Servo Brick API, welche den *servo_channel* Parameter verwendet,
kann einen Servo über die Servo-Kanal (0 bis 9) adressieren. Falls es sich um
eine Setter-Funktion handelt können mehrere Servos gleichzeitig mit einer
Bitmaske adressiert werden. Um dies zu kennzeichnen muss das höchstwertigste
Bit gesetzt werden. Beispiel: ``1`` adressiert den Servo 1,
``(1 << 1) | (1 << 5) | (1 << 15)`` adressiert die Servos 1 und 5.
Das ermöglicht es Konfigurationen von
verschiedenen Servos mit einem Funktionsaufruf durchzuführen. Es ist
sichergestellt das die Änderungen in der selben PWM Periode vorgenommen werden,
für alle Servos entsprechend der Bitmaske.
"""
}

com['packets'].append({
'type': 'function',
'name': 'Get Status',
'elements': [('Enabled', 'bool', 10, 'out', {}),
             ('Current Position', 'int16', 10, 'out', {'scale': (1, 100), 'unit': 'Degree', 'range': 'dynamic'}),
             ('Current Velocity', 'int16', 10, 'out', {'scale': (1, 100), 'unit': 'Degree Per Second', 'range': (0, 500000)}),
             ('Current', 'uint16', 10, 'out', {'scale': (1, 1000), 'unit': 'Ampere'}),
             ('Input Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the status information of the Servo Bricklet 2.0.

The status includes

* for each channel if it is enabled or disabled,
* for each channel the current position,
* for each channel the current velocity,
* for each channel the current usage and
* the input voltage.

Please note that the position and the velocity is a snapshot of the
current position and velocity of the servo in motion.
""",
'de':
"""
Gibt die Status-Informationen des Servo Bricklet 2.0 zurück.

Der Status umfasst

* für jeden Kanal die Information ob dieser gerade aktiviert oder deaktiviert ist,
* für jeden Kanal die aktuelle Position
* für jeden Kanal die aktuelle Geschwindigkeit,
* für jeden Kanal den Stromverbrauch und
* die Eingangsspannung

Hinweis: Die Position und Geschwindigkeit ist eine Momentaufnahme der
aktuellen Position und Geschwindigkeit eines sich in Bewegung befindlichen Servos.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Enable',
'elements': [('Servo Channel', 'uint16', 1, 'in', {'range': [(0, 9), (32768, 32768 | 0x3ff)]}),
             ('Enable', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Enables a servo channel (0 to 9). If a servo is enabled, the configured position,
velocity, acceleration, etc. are applied immediately.
""",
'de':
"""
Aktiviert einen Servo-Kanal (0 bis 9). Wenn ein Servo aktiviert wird, wird die
konfigurierte Position, Geschwindigkeit, Beschleunigung, etc. sofort übernommen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Enabled',
'elements': [('Servo Channel', 'uint16', 1, 'in', {'range': (0, 9)}),
             ('Enable', 'bool', 1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns *true* if the specified servo channel is enabled, *false* otherwise.
""",
'de':
"""
Gibt zurück ob ein Servo-Kanal aktiviert ist.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Position',
'elements': [('Servo Channel', 'uint16', 1, 'in', {'range': [(0, 9), (32768, 32768 | 0x3ff)]}),
             ('Position', 'int16', 1, 'in', {'scale': (1, 100), 'unit': 'Degree', 'range': 'dynamic'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the position in °/100 for the specified servo channel.

The default range of the position is -9000 to 9000, but it can be specified
according to your servo with :func:`Set Degree`.

If you want to control a linear servo or RC brushless motor controller or
similar with the Servo Brick, you can also define lengths or speeds with
:func:`Set Degree`.
""",
'de':
"""
Setzt die Position in °/100 für den angegebenen Servo-Kanal.

Der Standardbereich für die Position ist -9000 bis 9000, aber dies kann,
entsprechend dem verwendetem Servo, mit :func:`Set Degree` definiert werden.

Wenn ein Linearservo oder RC Brushless Motor Controller oder ähnlich mit dem
Servo Brick gesteuert werden soll, können Längen oder Geschwindigkeiten mit
:func:`Set Degree` definiert werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Position',
'elements': [('Servo Channel', 'uint16', 1, 'in', {'range': (0, 9)}),
             ('Position', 'int16', 1, 'out', {'scale': (1, 100), 'unit': 'Degree', 'range': 'dynamic'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the position of the specified servo channel as set by :func:`Set Position`.
""",
'de':
"""
Gibt die Position des angegebenen Servo-Kanals zurück, wie von :func:`Set Position`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Current Position',
'elements': [('Servo Channel', 'uint16', 1, 'in', {'range': (0, 9)}),
             ('Position', 'int16', 1, 'out', {'scale': (1, 100), 'unit': 'Degree', 'range': 'dynamic'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the *current* position of the specified servo channel. This may not be the
value of :func:`Set Position` if the servo is currently approaching a
position goal.
""",
'de':
"""
Gibt die *aktuelle* Position des angegebenen Servo-Kanals zurück. Dies kann vom Wert
von :func:`Set Position` abweichen, wenn der Servo gerade sein Positionsziel
anfährt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Current Velocity',
'elements': [('Servo Channel', 'uint16', 1, 'in', {'range': (0, 9)}),
             ('Velocity', 'uint16', 1, 'out', {'scale': (1, 100), 'unit': 'Degree Per Second', 'range': (0, 500000)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the *current* velocity of the specified servo channel. This may not be the
velocity specified by :func:`Set Motion Configuration`. if the servo is
currently approaching a velocity goal.
""",
'de':
"""
Gibt die *aktuelle* Geschwindigkeit des angegebenen Servo-Kanals zurück. Dies kann
von der Geschwindigkeit die per :func:`Set Motion Configuration` gesetzt wurde
abweichen, wenn der Servo gerade sein Geschwindigkeitsziel anfährt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Motion Configuration',
'elements': [('Servo Channel', 'uint16', 1, 'in', {'range': [(0, 9), (32768, 32768 | 0x3ff)]}),
             ('Velocity', 'uint32', 1, 'in', {'scale': (1, 100), 'unit': 'Degree Per Second', 'range': (0, 500000), 'default': 100000}),
             ('Acceleration', 'uint32', 1, 'in', {'scale': (1, 100), 'unit': 'Degree Per Second Squared', 'range': (0, 500000), 'default': 50000}),
             ('Deceleration', 'uint32', 1, 'in', {'scale': (1, 100), 'unit': 'Degree Per Second Squared', 'range': (0, 500000), 'default': 50000})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the maximum velocity of the specified servo channel in °/100s as well as
the acceleration and deceleration in °/100s²

With a velocity of 0 °/100s the position will be set immediately (no velocity).

With an acc-/deceleration of 0 °/100s² the velocity will be set immediately
(no acc-/deceleration).
""",
'de':
"""
Setzt die maximale Geschwindigkeit des angegebenen Servo-Kanals in °/100s sowie die
Beschleunigung und Verzögerung in °/100s².

Mit einer Geschwindigkeit von 0 °/100s wird die Position sofort gesetzt (keine
Geschwindigkeit).

Mit einer Beschleunigung/Verzögerung von 0 °/100s² wird die Geschwindigkeit
sofort gesetzt (keine Beschleunigung/Verzögerung).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Motion Configuration',
'elements': [('Servo Channel', 'uint16', 1, 'in', {'range': (0, 9)}),
             ('Velocity', 'uint32', 1, 'out', {'scale': (1, 100), 'unit': 'Degree Per Second', 'range': (0, 500000), 'default': 100000}),
             ('Acceleration', 'uint32', 1, 'out', {'scale': (1, 100), 'unit': 'Degree Per Second Squared', 'range': (0, 500000), 'default': 50000}),
             ('Deceleration', 'uint32', 1, 'out', {'scale': (1, 100), 'unit': 'Degree Per Second Squared', 'range': (0, 500000), 'default': 50000})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the motion configuration as set by :func:`Set Motion Configuration`.
""",
'de':
"""
Gibt die 'Motion Configuration' zurück, wie von :func:`Set Motion Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Pulse Width',
'elements': [('Servo Channel', 'uint16', 1, 'in', {'range': [(0, 9), (32768, 32768 | 0x3ff)]}),
             ('Min', 'uint32', 1, 'in', {'scale': (1, 10**6), 'unit': 'Second', 'default': 1000}),
             ('Max', 'uint32', 1, 'in', {'scale': (1, 10**6), 'unit': 'Second', 'default': 2000})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the minimum and maximum pulse width of the specified servo channel in µs.

Usually, servos are controlled with a
`PWM <https://en.wikipedia.org/wiki/Pulse-width_modulation>`__, whereby the
length of the pulse controls the position of the servo. Every servo has
different minimum and maximum pulse widths, these can be specified with
this function.

If you have a datasheet for your servo that specifies the minimum and
maximum pulse width, you should set the values accordingly. If your servo
comes without any datasheet you have to find the values via trial and error.

Both values have a range from 1 to 65535 (unsigned 16-bit integer). The
minimum must be smaller than the maximum.

The default values are 1000µs (1ms) and 2000µs (2ms) for minimum and
maximum pulse width.
""",
'de':
"""
Setzt die minimale und maximale Pulsweite des angegebenen Servo-Kanals in µs.

Normalerweise werden Servos mit einer
`PWM <https://de.wikipedia.org/wiki/Pulsweitenmodulation>`__ angesteuert,
wobei die Länge des Pulses die Position des Servos steuert. Jeder Servo
hat unterschiedliche minimale und maximale Pulsweiten, diese können mit
dieser Funktion spezifiziert werden.

Wenn im Datenblatt des Servos die minimale und maximale Pulsweite
spezifiziert ist, sollten diese Werte entsprechend gesetzt werden. Sollte
der Servo ohne ein Datenblatt vorliegen, müssen die Werte durch Ausprobieren
gefunden werden.

Beide Werte haben einen Wertebereich von 1 bis 65535 (unsigned 16-bit integer).
Der minimale Wert muss kleiner als der maximale sein.

Die Standardwerte sind 1000µs (1ms) und 2000µs (2ms) für minimale und maximale
Pulsweite.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Pulse Width',
'elements': [('Servo Channel', 'uint16', 1, 'in', {'range': (0, 9)}),
             ('Min', 'uint32', 1, 'out', {'scale': (1, 10**6), 'unit': 'Second', 'default': 1000}),
             ('Max', 'uint32', 1, 'out', {'scale': (1, 10**6), 'unit': 'Second', 'default': 2000})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the minimum and maximum pulse width for the specified servo channel as set by
:func:`Set Pulse Width`.
""",
'de':
"""
Gibt die minimale und maximale Pulsweite des angegebenen Servo-Kanals zurück, wie von
:func:`Set Pulse Width` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Degree',
'elements': [('Servo Channel', 'uint16', 1, 'in', {'range': [(0, 9), (32768, 32768 | 0x3ff)]}),
             ('Min', 'int16', 1, 'in', {'scale': (1, 100), 'unit': 'Degree', 'default': -9000}),
             ('Max', 'int16', 1, 'in', {'scale': (1, 100), 'unit': 'Degree', 'default': 9000})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the minimum and maximum degree for the specified servo channel (by default
given as °/100).

This only specifies the abstract values between which the minimum and maximum
pulse width is scaled. For example: If you specify a pulse width of 1000µs
to 2000µs and a degree range of -90° to 90°, a call of :func:`Set Position`
with 0 will result in a pulse width of 1500µs
(-90° = 1000µs, 90° = 2000µs, etc.).

Possible usage:

* The datasheet of your servo specifies a range of 200° with the middle position
  at 110°. In this case you can set the minimum to -9000 and the maximum to 11000.
* You measure a range of 220° on your servo and you don't have or need a middle
  position. In this case you can set the minimum to 0 and the maximum to 22000.
* You have a linear servo with a drive length of 20cm, In this case you could
  set the minimum to 0 and the maximum to 20000. Now you can set the Position
  with :func:`Set Position` with a resolution of cm/100. Also the velocity will
  have a resolution of cm/100s and the acceleration will have a resolution of
  cm/100s².
* You don't care about units and just want the highest possible resolution. In
  this case you should set the minimum to -32767 and the maximum to 32767.
* You have a brushless motor with a maximum speed of 10000 rpm and want to
  control it with a RC brushless motor controller. In this case you can set the
  minimum to 0 and the maximum to 10000. :func:`Set Position` now controls the rpm.

Both values have a possible range from -32767 to 32767
(signed 16-bit integer). The minimum must be smaller than the maximum.

The default values are -9000 and 9000 for the minimum and maximum degree.
""",
'de':
"""
Setzt den minimalen und maximalen Winkel des angegebenen Servo-Kanals (standardmäßig
in °/100).

Dies definiert die abstrakten Werte zwischen welchen die minimale und maximale
Pulsweite skaliert wird. Beispiel: Wenn eine Pulsweite von 1000µs bis 2000µs und
ein Winkelbereich von -90° bis 90° spezifiziert ist, wird ein Aufruf von
:func:`Set Position` mit 0 in einer Pulsweite von 1500µs resultieren
(-90° = 1000µs, 90° = 2000µs, etc.).

Anwendungsfälle:

* Das Datenblatt des Servos spezifiziert einen Bereich von 200° mit einer
  Mittelposition bei 110°. In diesem Fall kann das Minimum auf -9000 und das
  Maximum auf 11000 gesetzt werden.
* Es wird ein Bereich von 220° am Servo gemessen und eine Mittelposition ist
  nicht bekannt bzw. wird nicht benötigt. In diesem Fall kann das Minimum auf 0
  und das Maximum auf 22000 gesetzt werden.
* Ein Linearservo mit einer Antriebslänge von 20cm. In diesem Fall kann das
  Minimum auf 0 und das Maximum auf 20000 gesetzt werden. Jetzt kann die
  Position mittels :func:`Set Position` mit einer Auflösung von cm/100 gesetzt
  werden. Auch die Geschwindigkeit hat eine Auflösung von cm/100s und die
  Beschleunigung von cm/100s².
* Die Einheit ist irrelevant und eine möglichst hohe Auflösung ist gewünscht.
  In diesem Fall kann das Minimum auf -32767 und das Maximum auf 32767 gesetzt
  werden.
* Ein Brushless Motor, mit einer maximalen Drehzahl von 1000 U/min, soll mit
  einem RC Brushless Motor Controller gesteuert werden. In diesem Fall kann das
  Minimum auf 0 und das Maximum auf 10000 gesetzt werden. :func:`Set Position`
  steuert jetzt die Drehzahl in U/min.

Beide Werte haben einen Wertebereich von -32767 bis 32767 (signed 16-bit integer).
Der minimale Wert muss kleiner als der maximale sein.

Die Standardwerte sind -9000 und 9000 für den minimalen und maximalen Winkel.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Degree',
'elements': [('Servo Channel', 'uint16', 1, 'in', {'range': (0, 9)}),
             ('Min', 'int16', 1, 'out', {'scale': (1, 100), 'unit': 'Degree', 'default': -9000}),
             ('Max', 'int16', 1, 'out', {'scale': (1, 100), 'unit': 'Degree', 'default': 9000})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the minimum and maximum degree for the specified servo channel as set by
:func:`Set Degree`.
""",
'de':
"""
Gibt den minimalen und maximalen Winkel für den angegebenen Servo-Kanals zurück,
wie von :func:`Set Degree` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Period',
'elements': [('Servo Channel', 'uint16', 1, 'in', {'range': [(0, 9), (32768, 32768 | 0x3ff)]}),
             ('Period', 'uint32', 1, 'in', {'scale': (1, 10**6), 'unit': 'Second', 'range': (1, 1000000), 'default': 19500})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the period of the specified servo channel in µs.

Usually, servos are controlled with a
`PWM <https://en.wikipedia.org/wiki/Pulse-width_modulation>`__. Different
servos expect PWMs with different periods. Most servos run well with a
period of about 20ms.

If your servo comes with a datasheet that specifies a period, you should
set it accordingly. If you don't have a datasheet and you have no idea
what the correct period is, the default value (19.5ms) will most likely
work fine.

The minimum possible period is 1µs and the maximum is 1000000µs.

The default value is 19.5ms (19500µs).
""",
'de':
"""
Setzt die Periode des angegebenen Servo-Kanals in µs.

Normalerweise werden Servos mit einer
`PWM <https://de.wikipedia.org/wiki/Pulsweitenmodulation>`__ angesteuert.
Unterschiedliche Servos erwarten PWMs mit unterschiedlichen Perioden.
Die meisten Servos werden mit einer Periode von 20ms betrieben.

Wenn im Datenblatt des Servos die Periode spezifiziert ist, sollte dieser
Wert entsprechend gesetzt werden. Sollte der Servo ohne ein Datenblatt
vorliegen und die korrekte Periode unbekannt sein, wird der Standardwert
(19,5ms) meinst funktionieren.

Die minimal mögliche Periode ist 1µs und die maximale 1000000µs.

Der Standardwert ist 19,5ms (19500µs).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Period',
'elements': [('Servo Channel', 'uint16', 1, 'in', {'range': (0, 9)}),
             ('Period', 'uint32', 1, 'out', {'scale': (1, 10**6), 'unit': 'Second', 'range': (1, 1000000), 'default': 19500})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the period for the specified servo channel as set by :func:`Set Period`.
""",
'de':
"""
Gibt die Periode für den angegebenen Servo-Kanal zurück, wie von :func:`Set Period`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Servo Current',
'elements': [('Servo Channel', 'uint16', 1, 'in', {'range': (0, 9)}),
             ('Current', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current consumption of the specified servo channel in mA.
""",
'de':
"""
Gibt den Stromverbrauch des angegebenen Servo-Kanals in mA zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Servo Current Configuration',
'elements': [('Servo Channel', 'uint16', 1, 'in', {'range': [(0, 9), (32768, 32768 | 0x3ff)]}),
             ('Averaging Duration', 'uint8', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 255, 'range': (1, 255)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the averaging duration of the current measurement for the specified servo channel in ms.
""",
'de':
"""
Setzt die Durchschnittsberechnungsdauer der Strommessung des angegebenen Servo-Kanals in ms.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Servo Current Configuration',
'elements': [('Servo Channel', 'uint16', 1, 'in', {'range': (0, 9)}),
             ('Averaging Duration', 'uint8', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 255, 'range': (1, 255)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the servo current configuration for the specified servo channel as set
by :func:`Set Servo Current Configuration`.
""",
'de':
"""
Gibt die Servo-Stromverbrauchskonfiguration für den angegebenen Servo-Kanal
zurück, wie von :func:`Set Servo Current Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Input Voltage Configuration',
'elements': [('Averaging Duration', 'uint8', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 255, 'range': (1, 255)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the averaging duration of the input voltage measurement for the specified servo channel in ms.
""",
'de':
"""
Setzt die Durchschnittsberechnungsdauer der Eingangsspannungsmessung des angegebenen Servo-Kanals in ms.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Input Voltage Configuration',
'elements': [('Averaging Duration', 'uint8', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 255, 'range': (1, 255)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the input voltage configuration as set by :func:`Set Input Voltage Configuration`.
""",
'de':
"""
Gibt die Servo-Eingangsspannungskonfiguration zurück, wie von :func:`Set Input Voltage Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Overall Current',
'elements': [('Current', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Ampere'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current consumption of all servos together in mA.
""",
'de':
"""
Gibt den Stromverbrauch aller Servos zusammen in mA zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Input Voltage',
'elements': [('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the input voltage in mV. The input voltage is
given via the black power input connector on the Servo Brick.
""",
'de':
"""
Gibt die externe Eingangsspannung (in mV) zurück. Die externe Eingangsspannung
wird über die schwarze Stromversorgungsbuchse, in den Servo Brick, eingespeist.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Current Calibration',
'elements': [('Offset', 'int16', 10, 'in', {'scale': (1, 1000), 'unit': 'Ampere'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets an offset value (in mA) for each channel.

Note: On delivery the Servo Bricklet 2.0 is already calibrated.
""",
'de':
"""
Setzt einen Offset-Wert (in mA) für jeden Kanal.

Hinweis: Im Auslieferungszustand ist das Servo Bricklet 2.0 bereits kalibriert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Current Calibration',
'elements': [('Offset', 'int16', 10, 'out', {'scale': (1, 1000), 'unit': 'Ampere'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the current calibration as set by :func:`Set Current Calibration`.
""",
'de':
"""
Gibt die Stromkalibrierung zurück, wie von :func:`Set Current Calibration`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Position Reached Callback Configuration',
'elements': [('Servo Channel', 'uint16', 1, 'in', {'range': [(0, 9), (32768, 32768 | 0x3ff)]}),
             ('Enabled', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Enable/Disable :cb:`Position Reached` callback.
""",
'de':
"""
Aktiviert/Deaktiviert :cb:`Position Reached` Callback.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Position Reached Callback Configuration',
'elements': [('Servo Channel', 'uint16', 1, 'in', {'range': (0, 9)}),
             ('Enabled', 'bool', 1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set Position Reached Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set Position Reached Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Position Reached',
'elements': [('Servo Channel', 'uint16', 1, 'out', {'range': (0, 9)}),
             ('Position', 'int16', 1, 'out', {'scale': (1, 100), 'unit': 'Degree', 'range': 'dynamic'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when a position set by :func:`Set Position`
is reached. If the new position matches the current position then the
callback is not triggered, because the servo didn't move.
The :word:`parameters` are the servo and the position that is reached.

You can enable this callback with :func:`Set Position Reached Callback Configuration`.

.. note::
 Since we can't get any feedback from the servo, this only works if the
 velocity (see :func:`Set Motion Configuration`) is set smaller or equal to the
 maximum velocity of the servo. Otherwise the servo will lag behind the
 control value and the callback will be triggered too early.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn eine konfigurierte Position, wie von
:func:`Set Position` gesetzt, erreicht wird. Falls die neue Position der
aktuellen Position entspricht, wird der Callback nicht ausgelöst, weil sich der
Servo nicht bewegt hat.
Die :word:`parameters` sind der Servo und die Position die erreicht wurde.

Dieser Callback kann mit :func:`Set Position Reached Callback Configuration` aktiviert werden.

.. note::
 Da es nicht möglich ist eine Rückmeldung vom Servo zu erhalten,
 funktioniert dies nur wenn die konfigurierte Geschwindigkeit (siehe :func:`Set Motion Configuration`)
 kleiner oder gleich der maximalen Geschwindigkeit des Motors ist. Andernfalls
 wird der Motor hinter dem Vorgabewert zurückbleiben und der Callback wird
 zu früh ausgelöst.
"""
}]
})

com['examples'].append({
'name': 'Configuration',
'functions': [('setter', 'Set Degree', [('uint16', 0), ('int16', -10000), ('int16', 10000)], 'Servo 1: Connected to port 0, period of 19.5ms, pulse width of 1 to 2ms\n         and operating angle -100 to 100°', None),
              ('setter', 'Set Pulse Width', [('uint16', 0), ('uint32', 1000), ('uint32', 2000)], None, None),
              ('setter', 'Set Period', [('uint16', 0), ('uint32', 19500)], None, None),
              ('setter', 'Set Motion Configuration', [('uint16', 0), ('uint32', 500000), ('uint32', 1000), ('uint32', 1000)], None, 'Full velocity with slow ac-/deceleration'),
              ('empty',),
              ('setter', 'Set Degree', [('uint16', 5), ('int16', -9000), ('int16', 9000)], 'Servo 2: Connected to port 5, period of 20ms, pulse width of 0.95 to 1.95ms\n         and operating angle -90 to 90°', None),
              ('setter', 'Set Pulse Width', [('uint16', 5), ('uint32', 950), ('uint32', 1950)], None, None),
              ('setter', 'Set Period', [('uint16', 5), ('uint32', 20000)], None, None),
              ('setter', 'Set Motion Configuration', [('uint16', 5), ('uint32', 500000), ('uint32', 500000), ('uint32', 500000)], None, 'Full velocity with full ac-/deceleration'),
              ('empty',),
              ('setter', 'Set Position', [('uint16', 0), ('int16', 10000)], None, 'Set to most right position'),
              ('setter', 'Set Enable', [('uint16', 0), ('bool', True)], None, None),
              ('empty',),
              ('setter', 'Set Position', [('uint16', 5), ('int16', -9000)], None, 'Set to most left position'),
              ('setter', 'Set Enable', [('uint16', 5), ('bool', True)], None, None),
              ('wait',)],
'cleanups': [('setter', 'Set Enable', [('uint16', 0), ('bool', False)], None, None),
             ('setter', 'Set Enable', [('uint16', 5), ('bool', False)], None, None)]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Position Reached', 'position reached'), [(('Servo Channel', 'Servo Channel'), 'uint16', 1, None, None, None), (('Position', 'Position'), 'int16', 1, None, None, None)], 'Use position reached callback to swing back and forth', None),
              ('setter', 'Set Position Reached Callback Configuration', [('uint16', 0), ('bool', True)], 'Enable position reached callback', None),
              ('setter', 'Set Motion Configuration', [('uint16', 0), ('uint32', 10000), ('uint32', 500000), ('uint32', 500000)], 'Set velocity to 100°/s. This has to be smaller or equal to the\nmaximum velocity of the servo you are using, otherwise the position\nreached callback will be called too early', None),
              ('setter', 'Set Position', [('uint16', 0), ('int16', 9000)], None, None),
              ('setter', 'Set Enable', [('uint16', 0), ('bool', True)], None, None)],
'cleanups': [('setter', 'Set Enable', [('uint16', 0), ('bool', False)], None, None)],
'incomplete': True # because of special ping/pong logic in callback
})
