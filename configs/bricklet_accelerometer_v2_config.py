# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Accelerometer Bricklet 2.0 communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2130,
    'name': 'Accelerometer V2',
    'display_name': 'Accelerometer 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '',
        'de': ''
    },
    'comcu': True,
    'released': True,
    'documented': True,
    'discontinued': False,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Get Acceleration',
'elements': [('X', 'int32', 1, 'out'),
             ('Y', 'int32', 1, 'out'),
             ('Z', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the acceleration in x, y and z direction. The values
are given in g/10000 (1g = 9.80665m/s²), not to be confused with grams.

If you want to get the acceleration periodically, it is recommended
to use the :cb:`Acceleration` callback and set the period with
:func:`Set Acceleration Callback Configuration`.
""",
'de':
"""
Gibt die Beschleunigung in X-, Y- und Z-Richtung zurück. Die Werte
haben die Einheit g/10000 (1g = 9,80665m/s²), nicht zu verwechseln mit Gramm.

Wenn die Beschleunigungswerte periodisch abgefragt werden sollen, wird empfohlen
den :cb:`Acceleration` Callback zu nutzen und die Periode mit
:func:`Set Acceleration Callback Configuration` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('Data Rate', 'uint8', 1, 'in', ('Data Rate', [('0 781Hz', 0),
                                                            ('1 563Hz', 1),
                                                            ('3 125Hz', 2),
                                                            ('6 2512Hz', 3),
                                                            ('12 5Hz', 4),
                                                            ('25Hz', 5),
                                                            ('50Hz', 6),
                                                            ('100Hz', 7),
                                                            ('200Hz', 8),
                                                            ('400Hz', 9),
                                                            ('800Hz', 10),
                                                            ('1600Hz', 11),
                                                            ('3200Hz', 12),
                                                            ('6400Hz', 13),
                                                            ('12800Hz', 14),
                                                            ('25600Hz', 15)])),
             ('Full Scale', 'uint8', 1, 'in', ('Full Scale', [('2g', 0),
                                                              ('4g', 1),
                                                              ('8g', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Configures the data rate, full scale range and filter bandwidth.
Possible values are:

* Data rate of 0.781Hz to 25600Hz.
* Full scale range of -2G to +2G up to -8G to +8G.

Decreasing data rate or full scale range will also decrease the noise on
the data.

The default values are 100Hz data rate and -2G to +2G range.
""",
'de':
"""
Konfiguriert die Datenrate, den Wertebereich und die Filterbandbreite.
Mögliche Konfigurationswerte sind:

* Datenrate zwischen 0,781Hz und 25600Hz.
* Wertebereich von -2G bis +2G bis zu -8G bis +8G.

Eine Verringerung der Datenrate oder des Wertebereichs verringert auch
automatisch das Rauschen auf den Daten.

Die Standardwerte sind 100Hz Datenrate und -2G bis +2G Wertebereich.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Data Rate', 'uint8', 1, 'out', ('Data Rate', [('0 781Hz', 0),
                                                             ('1 563Hz', 1),
                                                             ('3 125Hz', 2),
                                                             ('6 2512Hz', 3),
                                                             ('12 5Hz', 4),
                                                             ('25Hz', 5),
                                                             ('50Hz', 6),
                                                             ('100Hz', 7),
                                                             ('200Hz', 8),
                                                             ('400Hz', 9),
                                                             ('800Hz', 10),
                                                             ('1600Hz', 11),
                                                             ('3200Hz', 12),
                                                             ('6400Hz', 13),
                                                             ('12800Hz', 14),
                                                             ('25600Hz', 15)])),
             ('Full Scale', 'uint8', 1, 'out', ('Full Scale', [('2g', 0),
                                                               ('4g', 1),
                                                               ('8g', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the configuration as set by :func:`Set Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Acceleration Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period in ms is the period with which the :cb:`Acceleration`
callback is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.

The default value is (0, false).
""",
'de':
"""
Die Periode in ms ist die Periode mit der der :cb:`Acceleration`
Callback ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn der Wert sich im Vergleich zum letzten mal geändert
hat. Ändert der Wert sich nicht innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen des Werts.

Der Standardwert ist (0, false).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Acceleration Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set Acceleration Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set Acceleration Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Info LED Config',
'elements': [('Config', 'uint8', 1, 'in', ('Info LED Config', [('Off', 0),
                                                               ('On', 1),
                                                               ('Show Heartbeat', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Configures the info LED (marked as "Force" on the Bricklet) to be either turned off,
turned on, or blink in heartbeat mode.
""",
'de':
"""
Konfiguriert die Info-LED (als "Force" auf dem Bricklet gekennzeichnet).
Die LED kann ausgeschaltet, eingeschaltet oder im Herzschlagmodus betrieben werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Info LED Config',
'elements': [('Config', 'uint8', 1, 'out', ('Info LED Config', [('Off', 0),
                                                                ('On', 1),
                                                                ('Show Heartbeat', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the LED configuration as set by :func:`Set Info LED Config`
""",
'de':
"""
Gibt die LED-Konfiguration zurück, wie von :func:`Set Info LED Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Acceleration',
'elements': [('X', 'int32', 1, 'out'),
             ('Y', 'int32', 1, 'out'),
             ('Z', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set Acceleration Callback Configuration`.

The :word:`parameters` are the same as :func:`Get Acceleration`.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set Acceleration Callback Configuration` gesetzten Konfiguration

Die :word:`parameters` sind der gleiche wie :func:`Get Acceleration`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Continuous Acceleration Configuration',
'elements': [('Enable X', 'bool', 1, 'in'),
             ('Enable Y', 'bool', 1, 'in'),
             ('Enable Z', 'bool', 1, 'in'),
             ('Resolution', 'uint8', 1, 'in', ('Resolution', [('8bit', 0),
                                                              ('16bit', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
For high throughput of acceleration data (> 1000Hz) you have to use the
:cb:`Continuous Acceleration 16 Bit` or :cb:`Continuous Acceleration 8 Bit`
callbacks.

You can enable the callback for each axis (x, y, z) individually and choose a
resolution of 8 bit or 16 bit.

If at least one of the axis is enabled and the resolution is set to 8 bit,
the :cb:`Continuous Acceleration 8 Bit` callback is activated. If at least
one of the axis is enabled and the resolution is set to 16 bit,
the :cb:`Continuous Acceleration 16 Bit` callback is activated.

If no axis is enabled, both callbacks are disabled. If one of the continuous
callbacks is enabled, the :cb:`Acceleration` callback is disabled.

The maximum throughput depends on the exact configuration:

.. csv-table::
 :header: "Number of axis enabled", "Throughput 8 bit", "Throughout 16 bit"
 :widths: 20, 20, 20

 "1", "25600Hz", "25600Hz"
 "2", "25600Hz", "15000Hz"
 "3", "20000Hz", "10000Hz"

""",
'de':
"""
Um einen hohen Durchsatz an Beschleunigungswerten zu erreichen (> 1000Hz) müssen
die :cb:`Continuous Acceleration 16 Bit` oder :cb:`Continuous Acceleration 8 Bit`
Callbacks genutzt werden.

Die Callbacks können für die Achsen (x, y, z) individuell aktiviert werden. Des
weiteren kann eine Auflösung von 8-Bit oder 16-Bit ausgewählt werden.

Wenn mindestens eine Achse aktiviert ist mit 8-Bit Auflösung,
wird der :cb:`Continuous Acceleration 8 Bit`-Callback aktiviert.
Wenn mindestens eine Achse aktiviert ist mit 16-Bit Auflösung,
wird der :cb:`Continuous Acceleration 16 Bit`-Callback aktiviert.

Wenn keine Achse aktiviert is, sind beide Callbacks deaktiviert. Wenn einer der
"Continuous Callbacks" genutzt wird, wird der :cb:`Acceleration`-Callback
automatisch deaktiviert.

Der maximale Durchsatz hängt von der Konfiguraiton ab:

.. csv-table::
 :header: "Anzahl aktiviert Achsen", "Durchsatz 8-Bit", "Durchsatz 16-Bit"
 :widths: 20, 20, 20

 "1", "25600Hz", "25600Hz"
 "2", "25600Hz", "15000Hz"
 "3", "20000Hz", "10000Hz"

"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Continuous Acceleration Configuration',
'elements': [('Enable X', 'bool', 1, 'out'),
             ('Enable Y', 'bool', 1, 'out'),
             ('Enable Z', 'bool', 1, 'out'),
             ('Resolution', 'uint8', 1, 'out', ('Resolution', [('8bit', 0),
                                                               ('16bit', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the continuous acceleration configuration as set by
:func:`Set Continuous Acceleration Configuration`.
""",
'de':
"""
Gibt die Konfiguration für kontinuierliche Beschleunigungswerte zurück, wie mittels
:func:`Set Continuous Acceleration Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Continuous Acceleration 16 Bit',
'elements': [('Acceleration', 'int16', 30, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
Returns 30 acceleration values with 16 bit resolution. The data rate can
be configured with :func:`Set Configuration` and this callback can be
enabled with :func:`Set Continuous Acceleration Configuration`.

The data is formated in the sequence "x, y, z, x, y, z, ..." depending on
the enabled axis. Examples:

* x, y, z enabled: "x, y, z, ... 10x ..., x, y, z"
* x, z enabled: "x, z, ... 15x ..., x, z"
* y enabled: "y, ... 30x ..., y"

""",
'de':
"""
Gibt 30 Beschleunigungswerte mit 16 bit Auflösung zurück. Die Datenrate
kann mit der Funktion :func:`Set Configuration` eingestellt werden und
der Callback kann per :func:`Set Continuous Acceleration Configuration`
aktiviert werden.

Die Daten sind in der Sequenz "x, y, z, x, y, z, ..." formatiert, abhängig
von den aktivierten Achsen. Beispiele:

* x, y, z aktiviert: "x, y, z, ... 10x ..., x, y, z"
* x, z aktiviert: "x, z, ... 15x ..., x, z"
* y aktiviert: "y, ... 30x ..., y"

"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Continuous Acceleration 8 Bit',
'elements': [('Acceleration', 'int8', 60, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
Returns 30 acceleration values with 8 bit resolution. The data rate can
be configured with :func:`Set Configuration` and this callback can be
enabled with :func:`Set Continuous Acceleration Configuration`.

The data is formated in the sequence "x, y, z, x, y, z, ..." depending on
the enabled axis. Examples:

* x, y, z enabled: "x, y, z, ... 20x ..., x, y, z"
* x, z enabled: "x, z, ... 30x ..., x, z"
* y enabled: "y, ... 60x ..., y"

""",
'de':
"""
Gibt 30 Beschleunigungswerte mit 8 bit Auflösung zurück. Die Datenrate
kann mit der Funktion :func:`Set Configuration` eingestellt werden und
der Callback kann per :func:`Set Continuous Acceleration Configuration`
aktiviert werden.

Die Daten sind in der Sequenz "x, y, z, x, y, z, ..." formatiert, abhängig
von den aktivierten Achsen. Beispiele:

* x, y, z aktiviert: "x, y, z, ... 20x ..., x, y, z"
* x, z aktiviert: "x, z, ... 30x ..., x, z"
* y aktiviert: "y, ... 60x ..., y"

"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Acceleration', 'acceleration'), [(('X', 'Acceleration [X]'), 'int32', 1, 10000.0, 'g', None), (('Y', 'Acceleration [Y]'), 'int32', 1, 10000.0, 'g', None), (('Z', 'Acceleration [Z]'), 'int32', 1, 10000.0, 'g', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Acceleration', 'acceleration'), [(('X', 'Acceleration [X]'), 'int32', 1, 10000.0, 'g', None), (('Y', 'Acceleration [Y]'), 'int32', 1, 10000.0, 'g', None), (('Z', 'Acceleration [Z]'), 'int32', 1, 10000.0, 'g', None)], None, None),
              ('callback_configuration', ('Acceleration', 'acceleration'), [], 1000, False, None, [])]
})
