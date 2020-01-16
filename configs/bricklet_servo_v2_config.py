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

com['doc'] = {
'en':
"""
Every function of the Servo Brick API that has a *servo_num* parameter can
address a servo with the servo number (0 to 9). If it is a setter function then
multiple servos can be addressed at once with a bitmask for the
servos, if the highest bit is set. For example: ``1`` will address servo 1,
``(1 << 1) | (1 << 5) | (1 << 15)`` will address servos 1 and 5.
This allows to set configurations to several
servos with one function call. It is guaranteed that the changes will take
effect in the same PWM period for all servos you specified in the bitmask.
""",
'de':
"""
Jede Funktion der Servo Brick API, welche den *servo_num* Parameter verwendet,
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
'elements': [('Enabled', 'bool', 10, 'out'),
             ('Current Position', 'int16', 10, 'out'),
             ('Current Velocity', 'int16', 10, 'out'),
             ('Current', 'uint16', 10, 'out'),
             ('Input Voltage', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
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
'name': 'Set Enable',
'elements': [('Servo Channel', 'uint16', 1, 'in'),
             ('Enable', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Enables a servo (0 to 9). If a servo is enabled, the configured position,
velocity, acceleration, etc. are applied immediately.
""",
'de':
"""
Aktiviert einen Servo (0 bis 9). Wenn ein Servo aktiviert wird, wird die
konfigurierte Position, Geschwindigkeit, Beschleunigung, etc. sofort übernommen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Enabled',
'elements': [('Servo Channel', 'uint16', 1, 'in'),
             ('Enable', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns *true* if the specified servo is enabled, *false* otherwise.
""",
'de':
"""
Gibt zurück ob ein Servo aktiviert ist.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Position',
'elements': [('Servo Channel', 'uint16', 1, 'in'),
             ('Position', 'int16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the position in °/100 for the specified servo.

The default range of the position is -9000 to 9000, but it can be specified
according to your servo with :func:`Set Degree`.

If you want to control a linear servo or RC brushless motor controller or
similar with the Servo Brick, you can also define lengths or speeds with
:func:`Set Degree`.
""",
'de':
"""
Setzt die Position in °/100 für den angegebenen Servo.

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
'elements': [('Servo Channel', 'uint16', 1, 'in'),
             ('Position', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the position of the specified servo as set by :func:`Set Position`.
""",
'de':
"""
Gibt die Position des angegebenen Servos zurück, wie von :func:`Set Position`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Current Position',
'elements': [('Servo Channel', 'uint16', 1, 'in'),
             ('Position', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the *current* position of the specified servo. This may not be the
value of :func:`Set Position` if the servo is currently approaching a
position goal.
""",
'de':
"""
Gibt die *aktuelle* Position des angegebenen Servos zurück. Dies kann vom Wert
von :func:`Set Position` abweichen, wenn der Servo gerade sein Positionsziel
anfährt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Current Velocity',
'elements': [('Servo Channel', 'uint16', 1, 'in'),
             ('Velocity', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the *current* velocity of the specified servo. This may not be the
value of TBD if the servo is currently approaching a
velocity goal.
""",
'de':
"""
Gibt die *aktuelle* Geschwindigkeit des angegebenen Servos zurück. Dies kann
vom Wert von TBD abweichen, wenn der Servo gerade sein
Geschwindigkeitsziel anfährt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Motion Configuration',
'elements': [('Servo Channel', 'uint16', 1, 'in'),
             ('Velocity', 'uint16', 1, 'in'),
             ('Acceleration', 'uint16', 1, 'in'),
             ('Deceleration', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO: Acc/Dec in °/100s²

Sets the maximum velocity of the specified servo in °/100s. 

The minimum velocity is 0 (no movement) and the maximum velocity is 65535.
With a value of 65535 the position will be set immediately (no velocity).

The default value is 65535.
""",
'de':
"""
Setzt die maximale Geschwindigkeit des angegebenen Servos in °/100s.
Die Geschwindigkeit wird entsprechend mit dem Wert, wie von
TBD gesetzt, beschleunigt.

Die minimale Geschwindigkeit ist 0 (keine Bewegung) und die maximale ist 65535.
Mit einem Wert von 65535 wird die Position sofort gesetzt (keine Geschwindigkeit).

Der Standardwert ist 65535.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Motion Configuration',
'elements': [('Servo Channel', 'uint16', 1, 'in'),
             ('Velocity', 'uint16', 1, 'out'),
             ('Acceleration', 'uint16', 1, 'out'),
             ('Deceleration', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO: Acc/Dec
Returns the velocity of the specified servo as set by :func:`Set Motion Configuration`.
""",
'de':
"""
Gibt die Geschwindigkeit des angegebenen Servos zurück, wie von
:func:`Set Motion Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Pulse Width',
'elements': [('Servo Channel', 'uint16', 1, 'in'),
             ('Min', 'uint32', 1, 'in'),
             ('Max', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the minimum and maximum pulse width of the specified servo in µs.

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
Setzt die minimale und maximale Pulsweite des angegebenen Servos in µs.

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
'elements': [('Servo Channel', 'uint16', 1, 'in'),
             ('Min', 'uint32', 1, 'out'),
             ('Max', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the minimum and maximum pulse width for the specified servo as set by
:func:`Set Pulse Width`.
""",
'de':
"""
Gibt die minimale und maximale Pulsweite des angegebenen Servos zurück, wie von
:func:`Set Pulse Width` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Degree',
'elements': [('Servo Channel', 'uint16', 1, 'in'),
             ('Min', 'int16', 1, 'in'),
             ('Max', 'int16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the minimum and maximum degree for the specified servo (by default
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
Setzt den minimalen und maximalen Winkel des angegebenen Servos (standardmäßig
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
'elements': [('Servo Channel', 'uint16', 1, 'in'),
             ('Min', 'int16', 1, 'out'),
             ('Max', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the minimum and maximum degree for the specified servo as set by
:func:`Set Degree`.
""",
'de':
"""
Gibt den minimalen und maximalen Winkel für den angegebenen Servo zurück,
wie von :func:`Set Degree` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Period',
'elements': [('Servo Channel', 'uint16', 1, 'in'),
             ('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the period of the specified servo in µs.

Usually, servos are controlled with a
`PWM <https://en.wikipedia.org/wiki/Pulse-width_modulation>`__. Different
servos expect PWMs with different periods. Most servos run well with a
period of about 20ms.

If your servo comes with a datasheet that specifies a period, you should
set it accordingly. If you don't have a datasheet and you have no idea
what the correct period is, the default value (19.5ms) will most likely
work fine.

The minimum possible period is 1µs and the maximum is 65535µs.

The default value is 19.5ms (19500µs).
""",
'de':
"""
Setzt die Periode des angegebenen Servos in µs.

Normalerweise werden Servos mit einer
`PWM <https://de.wikipedia.org/wiki/Pulsweitenmodulation>`__ angesteuert.
Unterschiedliche Servos erwarten PWMs mit unterschiedlichen Perioden.
Die meisten Servos werden mit einer Periode von 20ms betrieben.

Wenn im Datenblatt des Servos die Periode spezifiziert ist, sollte dieser
Wert entsprechend gesetzt werden. Sollte der Servo ohne ein Datenblatt
vorliegen und die korrekte Periode unbekannt sein, wird der Standardwert
(19,5ms) meinst funktionieren.

Die minimal mögliche Periode ist 1µs und die maximale 65535µs.

Der Standardwert ist 19,5ms (19500µs).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Period',
'elements': [('Servo Channel', 'uint16', 1, 'in'),
             ('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the period for the specified servo as set by :func:`Set Period`.
""",
'de':
"""
Gibt die Periode für den angegebenen Servo zurück, wie von :func:`Set Period`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Servo Current',
'elements': [('Servo Channel', 'uint16', 1, 'in'),
             ('Current', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current consumption of the specified servo in mA.
""",
'de':
"""
Gibt den Stromverbrauch des angegebenen Servos in mA zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Servo Current Configuration',
'elements': [('Servo Channel', 'uint16', 1, 'in'),
             ('Averaging Duration', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
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
'name': 'Get Servo Current Configuration',
'elements': [('Servo Channel', 'uint16', 1, 'in'),
             ('Averaging Duration', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
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
'name': 'Set Input Voltage Configuration',
'elements': [('Averaging Duration', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
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
'name': 'Get Input Voltage Configuration',
'elements': [('Averaging Duration', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
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
'name': 'Get Overall Current',
'elements': [('Current', 'uint16', 1, 'out')],
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
'elements': [('Voltage', 'uint16', 1, 'out')],
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
'name': 'Calibrate Servo Current',
'elements': [],
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
