# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Servo Brick communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'category': 'Brick',
    'device_identifier': 14,
    'name': 'Servo',
    'display_name': 'Servo',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Drives up to 7 RC Servos with up to 3A',
        'de': 'Steuert bis zu 7 RC Servos mit bis zu 3A'
    },
    'released': True,
    'documented': True,
    'packets': [],
    'examples': []
}

com['doc'] = {
'en':
"""
Every function of the Servo Brick API that has a *servo_num* parameter can
address a servo with the servo number (0 to 6). If it is a setter function then
multiple servos can be addressed at once with a bitmask for the
servos, if the highest bit is set. For example: ``1`` will address servo 1,
``(1 << 1) | (1 << 5) | (1 << 7)`` will address servos 1 and 5, ``0xFF`` will
address all seven servos, etc. This allows to set configurations to several
servos with one function call. It is guaranteed that the changes will take
effect in the same PWM period for all servos you specified in the bitmask.
""",
'de':
"""
Jede Funktion der Servo Brick API, welche den *servo_num* Parameter verwendet,
kann einen Servo über die Servo Nummer (0 bis 6) adressieren. Falls es sich um
eine Setter-Funktion handelt können mehrere Servos gleichzeitig mit einer
Bitmaske adressiert werden. Um dies zu kennzeichnen muss das höchstwertigste
Bit gesetzt werden. Beispiel: ``1`` adressiert den Servo 1,
``(1 << 1) | (1 << 5) | (1 << 7)`` adressiert die Servos 1 und 5, ``0xFF``
adressiert alle 7 Servos, und so weiter. Das ermöglicht es Konfigurationen von
verschiedenen Servos mit einem Funktionsaufruf durchzuführen. Es ist
sichergestellt das die Änderungen in der selben PWM Periode vorgenommen werden,
für alle Servos entsprechend der Bitmaske.
"""
}

com['packets'].append({
'type': 'function',
'name': 'Enable',
'elements': [('Servo Num', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Enables a servo (0 to 6). If a servo is enabled, the configured position,
velocity, acceleration, etc. are applied immediately.
""",
'de':
"""
Aktiviert einen Servo (0 bis 6). Wenn ein Servo aktiviert wird, wird die
konfigurierte Position, Geschwindigkeit, Beschleunigung, etc. sofort übernommen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Disable',
'elements': [('Servo Num', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Disables a servo (0 to 6). Disabled servos are not driven at all, i.e. a
disabled servo will not hold its position if a load is applied.
""",
'de':
"""
Deaktiviert einen Servo (0 bis 6). Deaktivierte Servos werden nicht angesteuert,
z.B. halten deaktivierte Servos nicht ihre Position wenn eine Last angebracht ist.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is Enabled',
'elements': [('Servo Num', 'uint8', 1, 'in'),
             ('Enabled', 'bool', 1, 'out')],
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
'elements': [('Servo Num', 'uint8', 1, 'in'),
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
'elements': [('Servo Num', 'uint8', 1, 'in'),
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
'elements': [('Servo Num', 'uint8', 1, 'in'),
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
'name': 'Set Velocity',
'elements': [('Servo Num', 'uint8', 1, 'in'),
             ('Velocity', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the maximum velocity of the specified servo in °/100s. The velocity
is accelerated according to the value set by :func:`Set Acceleration`.

The minimum velocity is 0 (no movement) and the maximum velocity is 65535.
With a value of 65535 the position will be set immediately (no velocity).

The default value is 65535.
""",
'de':
"""
Setzt die maximale Geschwindigkeit des angegebenen Servos in °/100s.
Die Geschwindigkeit wird entsprechend mit dem Wert, wie von
:func:`Set Acceleration` gesetzt, beschleunigt.

Die minimale Geschwindigkeit ist 0 (keine Bewegung) und die maximale ist 65535.
Mit einem Wert von 65535 wird die Position sofort gesetzt (keine Geschwindigkeit).

Der Standardwert ist 65535.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Velocity',
'elements': [('Servo Num', 'uint8', 1, 'in'),
             ('Velocity', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the velocity of the specified servo as set by :func:`Set Velocity`.
""",
'de':
"""
Gibt die Geschwindigkeit des angegebenen Servos zurück, wie von
:func:`Set Velocity` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Current Velocity',
'elements': [('Servo Num', 'uint8', 1, 'in'),
             ('Velocity', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the *current* velocity of the specified servo. This may not be the
value of :func:`Set Velocity` if the servo is currently approaching a
velocity goal.
""",
'de':
"""
Gibt die *aktuelle* Geschwindigkeit des angegebenen Servos zurück. Dies kann
vom Wert von :func:`Set Velocity` abweichen, wenn der Servo gerade sein
Geschwindigkeitsziel anfährt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Acceleration',
'elements': [('Servo Num', 'uint8', 1, 'in'),
             ('Acceleration', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the acceleration of the specified servo in °/100s².

The minimum acceleration is 1 and the maximum acceleration is 65535.
With a value of 65535 the velocity will be set immediately (no acceleration).

The default value is 65535.
""",
'de':
"""
Setzt die Beschleunigung des angegebenen Servos in °/100s².

Die minimale Beschleunigung ist 1 und die maximale 65535. Mit einem Wert von
65535 wird die Geschwindigkeit sofort gesetzt (keine Beschleunigung).

Der Standardwert ist 65535.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Acceleration',
'elements': [('Servo Num', 'uint8', 1, 'in'),
             ('Acceleration', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the acceleration for the specified servo as set by
:func:`Set Acceleration`.
""",
'de':
"""
Gibt die Beschleunigung des angegebenen Servos zurück, wie von
:func:`Set Acceleration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Output Voltage',
'elements': [('Voltage', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the output voltages with which the servos are driven in mV.
The minimum output voltage is 2000mV and the maximum output voltage is
9000mV.

.. note::
 We recommend that you set this value to the maximum voltage that is
 specified for your servo, most servos achieve their maximum force only
 with high voltages.

The default value is 5000.
""",
'de':
"""
Setzt die Ausgangsspannung mit welchem der Servo angetrieben wird in mV.
Die minimale Ausgangsspannung ist 2000mV und die maximale 9000mV.

.. note::
 Es wird empfohlen diesen Wert auf die maximale Spannung laut Spezifikation
 des Servos zu setzten. Die meisten Servos erreichen ihre maximale Kraft
 nur mit hohen Spannungen

Der Standardwert ist 5000.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Output Voltage',
'elements': [('Voltage', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the output voltage as specified by :func:`Set Output Voltage`.
""",
'de':
"""
Gibt die Ausgangsspannung zurück, wie von :func:`Set Output Voltage` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Pulse Width',
'elements': [('Servo Num', 'uint8', 1, 'in'),
             ('Min', 'uint16', 1, 'in'),
             ('Max', 'uint16', 1, 'in')],
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
'elements': [('Servo Num', 'uint8', 1, 'in'),
             ('Min', 'uint16', 1, 'out'),
             ('Max', 'uint16', 1, 'out')],
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
'elements': [('Servo Num', 'uint8', 1, 'in'),
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
'elements': [('Servo Num', 'uint8', 1, 'in'),
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
'elements': [('Servo Num', 'uint8', 1, 'in'),
             ('Period', 'uint16', 1, 'in')],
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
'elements': [('Servo Num', 'uint8', 1, 'in'),
             ('Period', 'uint16', 1, 'out')],
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
'elements': [('Servo Num', 'uint8', 1, 'in'),
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
'name': 'Get Stack Input Voltage',
'elements': [('Voltage', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the stack input voltage in mV. The stack input voltage is the
voltage that is supplied via the stack, i.e. it is given by a
Step-Down or Step-Up Power Supply.
""",
'de':
"""
Gibt die Eingangsspannung des Stapels in mV zurück. Die Eingangsspannung
des Stapels wird über diesen verteilt, z.B. mittels einer Step-Down
oder Step-Up Power Supply.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get External Input Voltage',
'elements': [('Voltage', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the external input voltage in mV. The external input voltage is
given via the black power input connector on the Servo Brick.

If there is an external input voltage and a stack input voltage, the motors
will be driven by the external input voltage. If there is only a stack
voltage present, the motors will be driven by this voltage.

.. warning::
 This means, if you have a high stack voltage and a low external voltage,
 the motors will be driven with the low external voltage. If you then remove
 the external connection, it will immediately be driven by the high
 stack voltage
""",
'de':
"""
Gibt die externe Eingangsspannung (in mV) zurück. Die externe Eingangsspannung
wird über die schwarze Stromversorgungsbuchse, in den Servo Brick, eingespeist.

Sobald eine externe Eingangsspannung und die Spannungsversorgung des Stapels anliegt,
werden die Motoren über die externe Spannung versorgt. Sollte nur die Spannungsversorgung
des Stapels verfügbar sein, erfolgt die Versorgung der Motoren über diese.

.. warning::
 Das bedeutet, bei einer hohen Versorgungsspannung des Stapels und einer geringen
 externen Versorgungsspannung erfolgt die Spannungsversorgung der Motoren über die geringere
 externe Versorgungsspannung. Wenn dann die externe Spannungsversorgung getrennt wird,
 erfolgt sofort die Versorgung der Motoren über die höhere Versorgungsspannung des Stapels.
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
Sets the minimum voltage in mV, below which the :cb:`Under Voltage` callback
is triggered. The minimum possible value that works with the Servo Brick is 5V.
You can use this function to detect the discharge of a battery that is used
to drive the stepper motor. If you have a fixed power supply, you likely do
not need this functionality.

The default value is 5V (5000mV).
""",
'de':
"""
Setzt die minimale Spannung in mV, bei welcher der :cb:`Under Voltage` Callback
ausgelöst wird. Der kleinste mögliche Wert mit dem der Servo Brick noch funktioniert,
ist 5V. Mit dieser Funktion kann eine Entladung der versorgenden Batterie detektiert
werden. Beim Einsatz einer Netzstromversorgung wird diese Funktionalität
höchstwahrscheinlich nicht benötigt.

Der Standardwert ist 5V (5000mV).
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
Returns the minimum voltage as set by :func:`Set Minimum Voltage`
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
'elements': [('Voltage', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when the input voltage drops below the value set by
:func:`Set Minimum Voltage`. The :word:`parameter` is the current voltage given
in mV.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn die Eingangsspannung unter den, mittels
:func:`Set Minimum Voltage` gesetzten, Schwellwert sinkt. Der :word:`parameter`
ist die aktuelle Spannung in mV.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Position Reached',
'elements': [('Servo Num', 'uint8', 1, 'out'),
             ('Position', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when a position set by :func:`Set Position`
is reached. The :word:`parameters` are the servo and the position that is reached.

You can enable this callback with :func:`Enable Position Reached Callback`.

.. note::
 Since we can't get any feedback from the servo, this only works if the
 velocity (see :func:`Set Velocity`) is set smaller or equal to the
 maximum velocity of the servo. Otherwise the servo will lag behind the
 control value and the callback will be triggered too early.
""",
'de':
"""
Dieser Callback wird ausgelöst immer wenn eine konfigurierte Position, wie von
:func:`Set Position` gesetzt, erreicht wird. Die :word:`parameters` sind der
Servo und die Position die erreicht wurde.

Dieser Callback kann mit :func:`Enable Position Reached Callback` aktiviert werden.

.. note::
 Da es nicht möglich ist eine Rückmeldung vom Servo zu erhalten,
 funktioniert dies nur wenn die konfigurierte Geschwindigkeit (siehe :func:`Set Velocity`)
 kleiner oder gleich der maximalen Geschwindigkeit des Motors ist. Andernfalls
 wird der Motor hinter dem Vorgabewert zurückbleiben und der Callback wird
 zu früh ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Velocity Reached',
'elements': [('Servo Num', 'uint8', 1, 'out'),
             ('Velocity', 'int16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when a velocity set by :func:`Set Velocity`
is reached. The :word:`parameters` are the servo and the velocity that is reached.

You can enable this callback with :func:`Enable Velocity Reached Callback`.

.. note::
 Since we can't get any feedback from the servo, this only works if the
 acceleration (see :func:`Set Acceleration`) is set smaller or equal to the
 maximum acceleration of the servo. Otherwise the servo will lag behind the
 control value and the callback will be triggered too early.
""",
'de':
"""
Dieser Callback wird ausgelöst immer wenn eine konfigurierte Geschwindigkeit, wie von
:func:`Set Velocity` gesetzt, erreicht wird. Die :word:`parameters` sind der
Servo und die Geschwindigkeit die erreicht wurde.

Dieser Callback kann mit :func:`Enable Velocity Reached Callback` aktiviert werden.

.. note::
 Da es nicht möglich ist eine Rückmeldung vom Servo zu erhalten,
 funktioniert dies nur wenn die konfigurierte Beschleunigung (siehe :func:`Set Acceleration`)
 kleiner oder gleich der maximalen Beschleunigung des Motors ist. Andernfalls
 wird der Motor hinter dem Vorgabewert zurückbleiben und der Callback wird
 zu früh ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Enable Position Reached Callback',
'elements': [],
'since_firmware': [2, 0, 1],
'doc': ['ccf', {
'en':
"""
Enables the :cb:`Position Reached` callback.

Default is disabled.
""",
'de':
"""
Aktiviert den :cb:`Position Reached` Callback.

Voreinstellung ist deaktiviert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Disable Position Reached Callback',
'elements': [],
'since_firmware': [2, 0, 1],
'doc': ['ccf', {
'en':
"""
Disables the :cb:`Position Reached` callback.

Default is disabled.
""",
'de':
"""
Deaktiviert den :cb:`Position Reached` Callback.

Voreinstellung ist deaktiviert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is Position Reached Callback Enabled',
'elements': [('Enabled', 'bool', 1, 'out')],
'since_firmware': [2, 0, 1],
'doc': ['ccf', {
'en':
"""
Returns *true* if :cb:`Position Reached` callback is enabled, *false* otherwise.
""",
'de':
"""
Gibt *true* zurück wenn der :cb:`Position Reached` Callback aktiviert ist, *false* sonst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Enable Velocity Reached Callback',
'elements': [],
'since_firmware': [2, 0, 1],
'doc': ['ccf', {
'en':
"""
Enables the :cb:`Velocity Reached` callback.

Default is disabled.
""",
'de':
"""
Aktiviert den :cb:`Velocity Reached` Callback.

Voreinstellung ist deaktiviert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Disable Velocity Reached Callback',
'elements': [],
'since_firmware': [2, 0, 1],
'doc': ['ccf', {
'en':
"""
Disables the :cb:`Velocity Reached` callback.

Default is disabled.
""",
'de':
"""
Deaktiviert den :cb:`Velocity Reached` Callback.

Voreinstellung ist deaktiviert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is Velocity Reached Callback Enabled',
'elements': [('Enabled', 'bool', 1, 'out')],
'since_firmware': [2, 0, 1],
'doc': ['ccf', {
'en':
"""
Returns *true* if :cb:`Velocity Reached` callback is enabled, *false* otherwise.
""",
'de':
"""
Gibt *true* zurück wenn der :cb:`Velocity Reached` Callback aktiviert ist, *false* sonst.
"""
}]
})

com['examples'].append({
'name': 'Configuration',
'functions': [('setter', 'Set Output Voltage', [('uint16', 5500)], 'Configure two servos with voltage 5.5V\nServo 1: Connected to port 0, period of 19.5ms, pulse width of 1 to 2ms\n         and operating angle -100 to 100°\n\nServo 2: Connected to port 5, period of 20ms, pulse width of 0.95 \n         to 1.95ms and operating angle -90 to 90°', None),
              ('empty',),
              ('setter', 'Set Degree', [('uint8', 0), ('int16', -10000), ('int16', 10000)], None, None),
              ('setter', 'Set Pulse Width', [('uint8', 0), ('uint16', 1000), ('uint16', 2000)], None, None),
              ('setter', 'Set Period', [('uint8', 0), ('uint16', 19500)], None, None),
              ('setter', 'Set Acceleration', [('uint8', 0), ('uint16', 1000)], None, 'Slow acceleration'),
              ('setter', 'Set Velocity', [('uint8', 0), ('uint16', 65535)], None, 'Full speed'),
              ('empty',),
              ('setter', 'Set Degree', [('uint8', 5), ('int16', -9000), ('int16', 9000)], None, None),
              ('setter', 'Set Pulse Width', [('uint8', 5), ('uint16', 950), ('uint16', 1950)], None, None),
              ('setter', 'Set Period', [('uint8', 5), ('uint16', 20000)], None, None),
              ('setter', 'Set Acceleration', [('uint8', 5), ('uint16', 65535)], None, 'Full acceleration'),
              ('setter', 'Set Velocity', [('uint8', 5), ('uint16', 65535)], None, 'Full speed'),
              ('empty',),
              ('setter', 'Set Position', [('uint8', 0), ('int16', 10000)], None, 'Set to most right position'),
              ('setter', 'Enable', [('uint8', 0)], None, None),
              ('empty',),
              ('setter', 'Set Position', [('uint8', 5), ('int16', -9000)], None, 'Set to most left position'),
              ('setter', 'Enable', [('uint8', 5)], None, None),
              ('wait',)],
'cleanups': [('setter', 'Disable', [('uint8', 0)], None, None),
             ('setter', 'Disable', [('uint8', 5)], None, None)]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Position Reached', 'position reached'), [(('Servo Num', 'Servo Number'), 'uint8', 1, None, None, None, None), (('Position', 'Position'), 'int16', 1, None, None, None, None)], 'Use position reached callback to swing back and forth', None),
              ('setter', 'Enable Position Reached Callback', [], 'Enable position reached callback', None),
              ('setter', 'Set Velocity', [('uint8', 0), ('uint16', 10000)], 'Set velocity to 100°/s. This has to be smaller or equal to the\nmaximum velocity of the servo you are using, otherwise the position\nreached callback will be called too early', None),
              ('setter', 'Set Position', [('uint8', 0), ('int16', 9000)], None, None),
              ('setter', 'Enable', [('uint8', 0)], None, None)],
'cleanups': [('setter', 'Disable', [('uint8', 0)], None, None)],
'incomplete': True # because of special ping/pong logic in callback
})
