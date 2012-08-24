# -*- coding: utf-8 -*-

# Servo Brick communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'version': [1, 0, 1],
    'category': 'Brick',
    'name': ('Servo', 'servo', 'Servo'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for controlling up to seven servos',
    'packets': []
}

com['api'] = {
'en':
"""
Every function of the Servo Brick API that has a *servo_num* parameter can
address a servo with the servo number (0 to 6) or with a bitmask for the
servos, if the last bit is set. For example: "1" will address servo 1,
"(1 << 1) | (1 << 5) | (1 << 7)" will address servos 1 and 5, "0xFF" will
address all seven servos, etc. This allows to set configurations to several
servos with one function call. It is guaranteed that the changes will take
effect in the same PWM period for all servos you specified in the bitmask.
""",
'de':
"""
Jede Funktion der Servo Brick API, welche den *servo_num* Parameter verwendet,
kann einen Servo über die Servo Nummer (0 bis 6) adressieren oder mit einer
Bitmaske für alle Servos wenn das höchstwertigste Bit gesetzt ist. Beispiel:
"1" adressiert den Server 1, "(1 << 1) | (1 << 5) | (1 << 7)" adressiert die
Servos 1 und 5, "0xFF" adressiert alle 7 Servos, und so weiter. Das ermöglicht
es Konfigurationen von verschiedenen Servos mit einem Funktionsaufruf durchzuführen.
Es ist sichergestellt das die Änderungen in der selben PWM Periode vorgenommen werden,
für alle Servos entsprechend der Bitmaske.
"""
}

com['packets'].append({
'type': 'function',
'name': ('Enable', 'enable'), 
'elements': [('servo_num', 'uint8', 1, 'in')], 
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
'name': ('Disable', 'disable'), 
'elements': [('servo_num', 'uint8', 1, 'in')], 
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
'name': ('IsEnabled', 'is_enabled'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('enabled', 'bool', 1, 'out')], 
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
'name': ('SetPosition', 'set_position'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('position', 'int16', 1, 'in')], 
'doc': ['bf', {
'en':
"""
Sets the position in °/100 for the specified servo. 

The default range of the position is -9000 to 9000, but it can be specified
according to your servo with :func:`SetDegree`.

If you want to control a linear servo or RC brushless motor controller or
similar with the Servo Brick, you can also define lengths or speeds with
:func:`SetDegree`.
""",
'de':
"""
Setzt die Position in °/100 für den angegebenen Servo.

Der Standardbereich für die Position ist -9000 bis 9000, aber dies kann,
entsprechend dem verwendetem Servo, mit :func:`SetDegree` definiert werden.

Wenn ein Linearservo oder RC Brushless Motor Controller oder ähnlich mit dem
Servo Brick gesteuert werden soll, können Längen oder Geschwindigkeiten mit
:func:`SetDegree` definiert werden.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetPosition', 'get_position'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('position', 'int16', 1, 'out')], 
'doc': ['bf', {
'en':
"""
Returns the position of the specified servo as set by :func:`SetPosition`.
""",
'de':
"""
Gibt die Position des angegebenen Servos zurück, wie von :func:`SetPosition`
gesetzt.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetCurrentPosition', 'get_current_position'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('position', 'int16', 1, 'out')], 
'doc': ['bf', {
'en':
"""
Returns the *current* position of the specified servo. This may not be the
value of :func:`SetPosition` if the servo is currently approaching a
position goal.
""",
'de':
"""
Gibt die *aktuelle* Position des angegebenen Servos zurück. Dies kann vom Wert
von :func:`SetPosition` abweichen, wenn der Servo gerade sein Positionsziel anfährt.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('SetVelocity', 'set_velocity'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('velocity', 'uint16', 1, 'in')], 
'doc': ['bf', {
'en':
"""
Sets the maximum velocity of the specified servo in °/100s. The velocity
is accelerated according to the value set by :func:`SetAcceleration`.

The minimum velocity is 0 (no movement) and the maximum velocity is 65535.
With a value of 65535 the position will be set immediately (no velocity).

The default value is 65535.
""",
'de':
"""
Setzt die maximale Geschwindigkeit des angegebenen Servos in °/100s. 
Die Geschwindigkeit wird entsprechend mit dem Wert, wie von :func:`SetAcceleration`
gesetzt, beschleunigt.

Die minimale Geschwindigkeit ist 0 (keine Bewegung) und die maximale ist 65535.
Mit einem Wert von 65535 wird die Position sofort gesetzt (keine Geschwindigkeit).

Der Standardwert ist 65535.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetVelocity', 'get_velocity'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('velocity', 'uint16', 1, 'out')], 
'doc': ['bf', {
'en':
"""
Returns the velocity of the specified servo as set by :func:`SetVelocity`.
""",
'de':
"""
Gibt die Geschwindigkeit des angegebenen Servos zurück, wie von :func:`SetVelocity`
gesetzt.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetCurrentVelocity', 'get_current_velocity'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('velocity', 'uint16', 1, 'out')], 
'doc': ['bf', {
'en':
"""
Returns the *current* velocity of the specified servo. This may not be the
value of :func:`SetVelocity` if the servo is currently approaching a
velocity goal.
""",
'de':
"""
Gibt die *aktuelle* Geschwindigkeit des angegebenen Servos zurück. Dies kann vom Wert
von :func:`SetVelocity` abweichen, wenn der Servo gerade sein Geschwindigkeitsziel anfährt.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('SetAcceleration', 'set_acceleration'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('acceleration', 'uint16', 1, 'in')], 
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
'name': ('GetAcceleration', 'get_acceleration'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('acceleration', 'uint16', 1, 'out')], 
'doc': ['bf', {
'en':
"""
Returns the acceleration for the specified servo as set by 
:func:`SetAcceleration`.
""",
'de':
"""
Gibt die Beschleunigung des angegebenen Servos zurück, wie von 
:func:`SetAcceleration` gesetzt.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('SetOutputVoltage', 'set_output_voltage'), 
'elements': [('voltage', 'uint16', 1, 'in')], 
'doc': ['bf', {
'en':
"""
Sets the output voltages with which the servos are driven in mV.
The minimum output voltage is 5000mV and the maximum output voltage is 
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
Die minimale Ausgangsspannung ist 5000mV und die maximale 9000mV.

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
'name': ('GetOutputVoltage', 'get_output_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')], 
'doc': ['bf', {
'en':
"""
Returns the output voltage as specified by :func:`SetOutputVoltage`.
""",
'de':
"""
Gibt die Ausgangsspannung zurück, wie von :func:`SetOutputVoltage` gesetzt.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('SetPulseWidth', 'set_pulse_width'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('min', 'uint16', 1, 'in'),
             ('max', 'uint16', 1, 'in')], 
'doc': ['bf', {
'en':
"""
Sets the minimum and maximum pulse width of the specified servo in µs.

Usually, servos are controlled with a 
`PWM <http://en.wikipedia.org/wiki/Pulse-width_modulation>`_, whereby the 
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
Setzt die minimale und maximale Pulsbreite des angegebenen Servos in µs.

Normalerweise werden Servos mit einer
`PWM <http://de.wikipedia.org/wiki/Pulsweitenmodulation>`_ angesteuert,
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
'name': ('GetPulseWidth', 'get_pulse_width'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('min', 'uint16', 1, 'out'),
             ('max', 'uint16', 1, 'out')], 
'doc': ['bf', {
'en':
"""
Returns the minimum and maximum pulse width for the specified servo as set by
:func:`SetPulseWidth`.
""",
'de':
"""
Gibt die minimale und maximale Pulsweite des angegebenen Servos zurück, wie von
:func:`SetPulseWidth` gesetzt.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('SetDegree', 'set_degree'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('min', 'int16', 1, 'in'),
             ('max', 'int16', 1, 'in')], 
'doc': ['bf', {
'en':
"""
Sets the minimum and maximum degree for the specified servo (by default
given as °/100).

This only specifies the abstract values between which the minimum and maximum
pulse width is scaled. For example: If you specify a pulse width of 1000µs
to 2000µs and a degree range of -90° to 90°, a call of :func:`SetPosition`
with 0 will result in a pulse width of 1500µs 
(-90° = 1000µs, 90° = 2000µs, etc.).

Possible usage:

* The datasheet of your servo specifies a range of 200° with the middle position
  at 110°. In this case you can set the minimum to -9000 and the maximum to 11000.
* You measure a range of 220° on your servo and you don't have or need a middle
  position. In this case you can set the minimum to 0 and the maximum to 22000.
* You have a linear servo with a drive length of 20cm, In this case you could
  set the minimum to 0 and the maximum to 20000. Now you can set the Position
  with :func:`SetPosition` with a resolution of cm/100. Also the velocity will
  have a resolution of cm/100s and the acceleration will have a resolution of
  cm/100s².
* You don't care about units and just want the highest possible resolution. In
  this case you should set the minimum to -32767 and the maximum to 32767.
* You have a brushless motor with a maximum speed of 10000 rpm and want to
  control it with a RC brushless motor controller. In this case you can set the
  minimum to 0 and the maximum to 10000. :func:`SetPosition` now controls the rpm.

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
:func:`SetPosition` mit 0 in einer Pulsweite von 1500µs resultieren
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
  Position mittels :func:`SetPosition` mit einer Auflösung von cm/100 gesetzt
  werden. Auch die Geschwindigkeit hat eine Auflösung von cm/100s und die
  Beschleunigung von cm/100s².
* Die Einheit ist irrelevant und eine möglichst hohe Auflösung ist gewünscht.
  In diesem Fall kann das Minimum auf -32767 und das Maximum auf 32767 gesetzt
  werden.
* Ein Brushless Motor, mit einer maximalen Drehzahl von 1000 U/min, soll mit
  einem RC Brushless Motor Controller gesteuert werden. In diesem Fall kann das
  Minimum auf 0 und das Maximum auf 10000 gesetzt werden. :func:`SetPosition`
  steuert jetzt die Drehzal in U/min.

Beide Werte haben einen Wertebereich von -32767 bis 32767 (signed 16-bit integer).
Der minimale Wert muss kleiner als der maximale sein.

Die Standardwerte sind -9000 und 9000 für den minimalen und maximalen Winkel.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetDegree', 'get_degree'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('min', 'int16', 1, 'out'),
             ('max', 'int16', 1, 'out')], 
'doc': ['bf', {
'en':
"""
Returns the minimum and maximum degree for the specified servo as set by
:func:`SetDegree`.
""",
'de':
"""
Gibt den minimalen und maximalen Winkel für den angegebenen Servo zurück,
wie von :func:`SetDegree` gesetzt.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('SetPeriod', 'set_period'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('period', 'uint16', 1, 'in')],
'doc': ['bf', {
'en':
"""
Sets the period of the specified servo in µs.

Usually, servos are controlled with a 
`PWM <http://en.wikipedia.org/wiki/Pulse-width_modulation>`_. Different
servos expect PWMs with different periods. Most servos run well with a 
period of about 20ms.

If your servo comes with a datasheet that specifies a period, you should
set it accordingly. If you don't have a datasheet and you have no idea
what the correct period is, the default value (19.5ms) will most likely
work fine. 

The minimum possible period is 2000µs and the maximum is 65535µs.

The default value is 19.5ms (19500µs).
""",
'de':
"""
Setzt die Periode des angegebenen Servos in µs.

Normalerweise werden Servos mit einer
`PWM <http://de.wikipedia.org/wiki/Pulsweitenmodulation>`_ angesteuert.
Unterschiedliche Servos erwarten PWMs mit unterschiedlichen Perioden.
Die meisten Servos werden mit einer Periode von 20ms betrieben.

Wenn im Datenblatt des Servos die Periode spezifiziert ist, sollte dieser
Wert entsprechend gesetzt werden. Sollte der Servo ohne ein Datenblatt
vorliegen und die korrekte Periode unbekannt sein, wird der Standardwert
(19,5ms) meinst funktionieren.

Die minimal mögliche Periode ist 2000µs und die maximale 65535µs.

Der Standardwert ist 19,5ms (19500µs).
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetPeriod', 'get_period'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('period', 'uint16', 1, 'out')],
'doc': ['bf', {
'en':
"""
Returns the period for the specified servo as set by :func:`SetPeriod`.
""",
'de':
"""
Gibt die Periode für den angegebenen Servo zurück, wie von :func:`SetPeriod`
gesetzt.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetServoCurrent', 'get_servo_current'), 
'elements': [('servo_num', 'uint8', 1, 'in'),
             ('current', 'uint16', 1, 'out')],
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
'name': ('GetOverallCurrent', 'get_overall_current'), 
'elements': [('current', 'uint16', 1, 'out')],
'doc': ['bf', {
'en':
"""
Returns the current consumption of all servos together in mA.
""",
'de':
"""
Gibt die Summe aller Stromverbräuche der Servos in mA zurück.
"""
}] 
})

com['packets'].append({
'type': 'function',
'name': ('GetStackInputVoltage', 'get_stack_input_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')],
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
'name': ('GetExternalInputVoltage', 'get_external_input_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')],
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
'name': ('SetMinimumVoltage', 'set_minimum_voltage'), 
'elements': [('voltage', 'uint16', 1, 'in')],
'doc': ['ccf', {
'en':
"""
Sets the minimum voltage in mV, below which the :func:`UnderVoltage` callback
is triggered. The minimum possible value that works with the Servo Brick is 5V.
You can use this function to detect the discharge of a battery that is used
to drive the stepper motor. If you have a fixed power supply, you likely do 
not need this functionality.

The default value is 5V (5000mV).
""",
'de':
"""
Setzt die minimale Spannung in mV, bei welcher der :func:`UnderVoltage` Callback
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
'name': ('GetMinimumVoltage', 'get_minimum_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')],
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
'type': 'callback',
'name': ('UnderVoltage', 'under_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')],
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
'elements': [('servo_num', 'uint8', 1, 'out'),
             ('position', 'int16', 1, 'out')], 
'doc': ['c', {
'en':
"""
This callback is triggered when a position set by :func:`SetPosition`
is reached. The :word:`parameters` are the servo and the position that is reached.

.. note::
 Since we can't get any feedback from the servo, this only works if the
 velocity (see :func:`SetVelocity`) is set smaller or equal to the
 maximum velocity of the servo. Otherwise the servo will lag behind the
 control value and the callback will be triggered too early.
""",
'de':
"""
Dieser Callback wird ausgelöst immer wenn eine konfigurierte Position, wie von
:func:`SetPosition` gesetzt, erreicht wird. Die :word:`parameters` sind der
Servo und die Position die erreicht wurde.

.. note::
 Da es nicht möglich ist eine Rückmeldung vom Servo zu erhalten,
 funktioniert dies nur wenn die konfigurierte Geschwindigkeit (siehe :func:`SetVelocity`)
 kleiner oder gleich der maximalen Geschwindigkeit des Motors ist. Andernfalls
 wird der Motor hinter dem Vorgabewert zurückbleiben und der Callback wird
 zu früh ausgelöst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('VelocityReached', 'velocity_reached'), 
'elements': [('servo_num', 'uint8', 1, 'out'),
             ('velocity', 'int16', 1, 'out')], 
'doc': ['c', {
'en':
"""
This callback is triggered when a velocity set by :func:`SetVelocity`
is reached. The :word:`parameters` are the servo and the velocity that is reached.

.. note::
 Since we can't get any feedback from the servo, this only works if the
 acceleration (see :func:`SetAcceleration`) is set smaller or equal to the
 maximum acceleration of the servo. Otherwise the servo will lag behind the
 control value and the callback will be triggered too early.
""",
'de':
"""
Dieser Callback wird ausgelöst immer wenn eine konfigurierte Geschwindigkeit, wie von
:func:`SetVelocity` gesetzt, erreicht wird. Die :word:`parameters` sind der
Servo und die Geschwindigkeit die erreicht wurde.

.. note::
 Da es nicht möglich ist eine Rückmeldung vom Servo zu erhalten,
 funktioniert dies nur wenn die konfigurierte Beschleunigung (siehe :func:`SetAcceleration`)
 kleiner oder gleich der maximalen Beschleunigung des Motors ist. Andernfalls
 wird der Motor hinter dem Vorgabewert zurückbleiben und der Callback wird
 zu früh ausgelöst.
"""
}]
})
