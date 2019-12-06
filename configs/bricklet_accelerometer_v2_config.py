# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Accelerometer Bricklet 2.0 communication config

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'category': 'Bricklet',
    'device_identifier': 2130,
    'name': 'Accelerometer V2',
    'display_name': 'Accelerometer 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures acceleration in three axis',
        'de': 'Misst Beschleunigung in drei Achsen'
    },
    'released': True,
    'documented': True,
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
'name': 'Data Rate',
'type': 'uint8',
'constants': [('0 781Hz', 0),
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
              ('25600Hz', 15)]
})

com['constant_groups'].append({
'name': 'Full Scale',
'type': 'uint8',
'constants': [('2g', 0),
              ('4g', 1),
              ('8g', 2)]
})

com['constant_groups'].append({
'name': 'Info LED Config',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Show Heartbeat', 2)]
})

com['constant_groups'].append({
'name': 'Resolution',
'type': 'uint8',
'constants': [('8bit', 0),
              ('16bit', 1)]
})

com['constant_groups'].append({
'name': 'IIR Bypass',
'type': 'uint8',
'constants': [('Applied', 0),
              ('Bypassed', 1)]
})

com['constant_groups'].append({
'name': 'Low Pass Filter',
'type': 'uint8',
'constants': [('Ninth', 0),
              ('Half', 1)]
})

com['packets'].append({
'type': 'function',
'name': 'Get Acceleration',
'elements': [('X', 'int32', 1, 'out', {'scale': (1, 10000), 'unit': 'Standard Gravity', 'range': 'dynamic'}),
             ('Y', 'int32', 1, 'out', {'scale': (1, 10000), 'unit': 'Standard Gravity', 'range': 'dynamic'}),
             ('Z', 'int32', 1, 'out', {'scale': (1, 10000), 'unit': 'Standard Gravity', 'range': 'dynamic'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the acceleration in x, y and z direction. The values
are given in gₙ/10000 (1gₙ = 9.80665m/s²). The range is
configured with :func:`Set Configuration`.

If you want to get the acceleration periodically, it is recommended
to use the :cb:`Acceleration` callback and set the period with
:func:`Set Acceleration Callback Configuration`.
""",
'de':
"""
Gibt die Beschleunigung in X-, Y- und Z-Richtung zurück. Die Werte
haben die Einheit gₙ/10000 (1gₙ = 9,80665m/s²). Der Wertebereich
wird mit :func:`Set Configuration` konfiguriert.

Wenn die Beschleunigungswerte periodisch abgefragt werden sollen, wird empfohlen
den :cb:`Acceleration` Callback zu nutzen und die Periode mit
:func:`Set Acceleration Callback Configuration` vorzugeben.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('Data Rate', 'uint8', 1, 'in', {'constant_group': 'Data Rate', 'default': 7}),
             ('Full Scale', 'uint8', 1, 'in', {'constant_group': 'Full Scale', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Configures the data rate and full scale range.
Possible values are:

* Data rate of 0.781Hz to 25600Hz.
* Full scale range of ±2g up to ±8g.

Decreasing data rate or full scale range will also decrease the noise on
the data.
""",
'de':
"""
Konfiguriert die Datenrate und den Wertebereich.
Mögliche Konfigurationswerte sind:

* Datenrate zwischen 0,781Hz und 25600Hz.
* Wertebereich von ±2g bis zu ±8g.

Eine Verringerung der Datenrate oder des Wertebereichs verringert auch
automatisch das Rauschen auf den Daten.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Data Rate', 'uint8', 1, 'out', {'constant_group': 'Data Rate', 'default': 7}),
             ('Full Scale', 'uint8', 1, 'out', {'constant_group': 'Full Scale', 'default': 0})],
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
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period is the period with which the :cb:`Acceleration`
callback is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.

If this callback is enabled, the :cb:`Continuous Acceleration 16 Bit` callback
and :cb:`Continuous Acceleration 8 Bit` callback will automatically be disabled.
""",
'de':
"""
Die Periode ist die Periode mit der der :cb:`Acceleration`
Callback ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn der Wert sich im Vergleich zum letzten mal geändert
hat. Ändert der Wert sich nicht innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen des Werts.

Wenn dieser Callback aktiviert ist, werden der
:cb:`Continuous Acceleration 16 Bit` Callback und
:cb:`Continuous Acceleration 8 Bit` Callback automatisch deaktiviert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Acceleration Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'out', {'default': False})],
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
'elements': [('Config', 'uint8', 1, 'in', {'constant_group': 'Info LED Config', 'default': 0})],
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
'elements': [('Config', 'uint8', 1, 'out', {'constant_group': 'Info LED Config', 'default': 0})],
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
'elements': [('X', 'int32', 1, 'out', {'scale': (1, 10000), 'unit': 'Standard Gravity', 'range': 'dynamic'}),
             ('Y', 'int32', 1, 'out', {'scale': (1, 10000), 'unit': 'Standard Gravity', 'range': 'dynamic'}),
             ('Z', 'int32', 1, 'out', {'scale': (1, 10000), 'unit': 'Standard Gravity', 'range': 'dynamic'})],
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
:func:`Set Acceleration Callback Configuration` gesetzten Konfiguration.

Die :word:`parameters` sind die gleichen wie :func:`Get Acceleration`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Continuous Acceleration Configuration',
'elements': [('Enable X', 'bool', 1, 'in', {'default': False}),
             ('Enable Y', 'bool', 1, 'in', {'default': False}),
             ('Enable Z', 'bool', 1, 'in', {'default': False}),
             ('Resolution', 'uint8', 1, 'in', {'constant_group': 'Resolution', 'default': 0})],
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

The returned values are raw ADC data. If you want to put this data into
a FFT to determine the occurrences of specific frequencies we recommend
that you use the data as is. It has all of the ADC noise in it. This noise
looks like pure noise at first glance, but it might still have some frequnecy
information in it that can be utilized by the FFT.

Otherwise you have to use the following formulas that depend on the configured
resolution (8/16 bit) and the full scale range (see :func:`Set Configuration`) to calculate
the data in gₙ/10000 (same unit that is returned by :func:`Get Acceleration`):

* 16 bit, full scale 2g: acceleration = value * 625 / 1024
* 16 bit, full scale 4g: acceleration = value * 1250 / 1024
* 16 bit, full scale 8g: acceleration = value * 2500 / 1024

If a resolution of 8 bit is used, only the 8 most significant bits will be
transferred, so you can use the following formulas:

* 8 bit, full scale 2g: acceleration = value * 256 * 625 / 1024
* 8 bit, full scale 4g: acceleration = value * 256 * 1250 / 1024
* 8 bit, full scale 8g: acceleration = value * 256 * 2500 / 1024

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

Die zurückgegebenen Werte sind Rohwerte des AD-Wandlers. Wenn die Daten mit einem
FFT genutzt werden sollen um Vorkomnisse from Frequenzen zu bestimmen empfehlen wir
die Rohwerte direkt zu nutzen. Die Rohwerte beinhalten das Rauschen des AD-Wandlers,
in diesem Rauschen können allerdings Frequenzinformation enthalten sein die für
einen FFT relevant seien können.

Andernfalls können die folgenden Formeln benutzt werden um die Daten wieder
in der Einheit gₙ/10000 (gleiche Einheit wie von :func:`Get Acceleration` zurückgegeben)
umzuwandeln. Die Formeln hängen ab von der eingestelleten Auflösung (8/16-Bit) und dem
eingestellten Wertebereich (siehe :func:`Set Configuration`):

* 16-Bit, Wertebereich 2g: Beschleunigung = Rohwert * 625 / 1024
* 16-Bit, Wertebereich 4g: Beschleunigung = Rohwert * 1250 / 1024
* 16-Bit, Wertebereich 8g: Beschleunigung = Rohwert * 2500 / 1024

Bei einer Auflösung von 8-Bit werden nur die 8 höchstwertigen Bits übertragen, daher
sehen die Formeln wie folgt aus:

* 8-Bit, Wertebereich 2g: Beschleunigung = Rohwert * 256 * 625 / 1024
* 8-Bit, Wertebereich 4g: Beschleunigung = Rohwert * 256 * 1250 / 1024
* 8-Bit, Wertebereich 8g: Beschleunigung = Rohwert * 256 * 2500 / 1024

Wenn keine Achse aktiviert is, sind beide Callbacks deaktiviert. Wenn einer der
"Continuous Callbacks" genutzt wird, wird der :cb:`Acceleration`-Callback
automatisch deaktiviert.

Der maximale Durchsatz hängt von der Konfiguration ab:

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
'elements': [('Enable X', 'bool', 1, 'out', {'default': False}),
             ('Enable Y', 'bool', 1, 'out', {'default': False}),
             ('Enable Z', 'bool', 1, 'out', {'default': False}),
             ('Resolution', 'uint8', 1, 'out', {'constant_group': 'Resolution', 'default': 0})],
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
'elements': [('Acceleration', 'int16', 30, 'out', {'scale': 'dynamic', 'unit': 'Standard Gravity', 'range': 'dynamic'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
Returns 30 acceleration values with 16 bit resolution. The data rate can
be configured with :func:`Set Configuration` and this callback can be
enabled with :func:`Set Continuous Acceleration Configuration`.

The returned values are raw ADC data. If you want to put this data into
a FFT to determine the occurrences of specific frequencies we recommend
that you use the data as is. It has all of the ADC noise in it. This noise
looks like pure noise at first glance, but it might still have some frequnecy
information in it that can be utilized by the FFT.

Otherwise you have to use the following formulas that depend on the
full scale range (see :func:`Set Configuration`) to calculate
the data in gₙ/10000 (same unit that is returned by :func:`Get Acceleration`):

* Full scale 2g: acceleration = value * 625 / 1024
* Full scale 4g: acceleration = value * 1250 / 1024
* Full scale 8g: acceleration = value * 2500 / 1024

The data is formated in the sequence "x, y, z, x, y, z, ..." depending on
the enabled axis. Examples:

* x, y, z enabled: "x, y, z, ..." 10x repeated
* x, z enabled: "x, z, ..." 15x repeated
* y enabled: "y, ..." 30x repeated

""",
'de':
"""
Gibt 30 Beschleunigungswerte mit 16 bit Auflösung zurück. Die Datenrate
kann mit der Funktion :func:`Set Configuration` eingestellt werden und
der Callback kann per :func:`Set Continuous Acceleration Configuration`
aktiviert werden.

Die zurückgegebenen Werte sind Rohwerte des AD-Wandlers. Wenn die Daten mit einem
FFT genutzt werden sollen um Vorkomnisse from Frequenzen zu bestimmen empfehlen wir
die Rohwerte direkt zu nutzen. Die Rohwerte beinhalten das Rauschen des AD-Wandlers,
in diesem Rauschen können allerdings Frequenzinformation enthalten sein die für
einen FFT relevant seien können.

Andernfalls können die folgenden Formeln benutzt werden um die Daten wieder
in der Einheit gₙ/10000 (gleiche Einheit wie von :func:`Get Acceleration` zurückgegeben)
umzuwandeln. Die Formeln hängen ab von dem
eingestellten Wertebereich (siehe :func:`Set Configuration`):

* Wertebereich 2g: Beschleunigung = Rohwert * 625 / 1024
* Wertebereich 4g: Beschleunigung = Rohwert * 1250 / 1024
* Wertebereich 8g: Beschleunigung = Rohwert * 2500 / 1024

Die Daten sind in der Sequenz "x, y, z, x, y, z, ..." formatiert, abhängig
von den aktivierten Achsen. Beispiele:

* x, y, z aktiviert: "x, y, z, ..." 10x wiederholt
* x, z aktiviert: "x, z, ..." 15x wiederholt
* y aktiviert: "y, ..." 30x wiederholt

"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Continuous Acceleration 8 Bit',
'elements': [('Acceleration', 'int8', 60, 'out', {'scale': 'dynamic', 'unit': 'Standard Gravity', 'range': 'dynamic'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
Returns 60 acceleration values with 8 bit resolution. The data rate can
be configured with :func:`Set Configuration` and this callback can be
enabled with :func:`Set Continuous Acceleration Configuration`.

The returned values are raw ADC data. If you want to put this data into
a FFT to determine the occurrences of specific frequencies we recommend
that you use the data as is. It has all of the ADC noise in it. This noise
looks like pure noise at first glance, but it might still have some frequnecy
information in it that can be utilized by the FFT.

Otherwise you have to use the following formulas that depend on the
full scale range (see :func:`Set Configuration`) to calculate
the data in gₙ/10000 (same unit that is returned by :func:`Get Acceleration`):

* Full scale 2g: acceleration = value * 256 * 625 / 1024
* Full scale 4g: acceleration = value * 256 * 1250 / 1024
* Full scale 8g: acceleration = value * 256 * 2500 / 1024

The data is formated in the sequence "x, y, z, x, y, z, ..." depending on
the enabled axis. Examples:

* x, y, z enabled: "x, y, z, ..." 20x repeated
* x, z enabled: "x, z, ..." 30x repeated
* y enabled: "y, ..." 60x repeated

""",
'de':
"""
Gibt 60 Beschleunigungswerte mit 8 bit Auflösung zurück. Die Datenrate
kann mit der Funktion :func:`Set Configuration` eingestellt werden und
der Callback kann per :func:`Set Continuous Acceleration Configuration`
aktiviert werden.

Die zurückgegebenen Werte sind Rohwerte des AD-Wandlers. Wenn die Daten mit einem
FFT genutzt werden sollen um Vorkomnisse from Frequenzen zu bestimmen empfehlen wir
die Rohwerte direkt zu nutzen. Die Rohwerte beinhalten das Rauschen des AD-Wandlers,
in diesem Rauschen können allerdings Frequenzinformation enthalten sein die für
einen FFT relevant seien können.

Andernfalls können die folgenden Formeln benutzt werden um die Daten wieder
in der Einheit gₙ/10000 (gleiche Einheit wie von :func:`Get Acceleration` zurückgegeben)
umzuwandeln. Die Formeln hängen ab von dem
eingestellten Wertebereich (siehe :func:`Set Configuration`):

* Wertebereich 2g: Beschleunigung = Rohwert * 256 * 625 / 1024
* Wertebereich 4g: Beschleunigung = Rohwert * 256 * 1250 / 1024
* Wertebereich 8g: Beschleunigung = Rohwert * 256 * 2500 / 1024

Die Daten sind in der Sequenz "x, y, z, x, y, z, ..." formatiert, abhängig
von den aktivierten Achsen. Beispiele:

* x, y, z aktiviert: "x, y, z, ..." 20x wiederholt
* x, z aktiviert: "x, z, ..." 30x wiederholt
* y aktiviert: "y, ..." 60x wiederholt

"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Filter Configuration',
'elements': [('IIR Bypass', 'uint8', 1, 'in', {'constant_group': 'IIR Bypass', 'default': 0}),
             ('Low Pass Filter', 'uint8', 1, 'in', {'constant_group': 'Low Pass Filter', 'default': 0})],
'since_firmware': [2, 0, 2],
'doc': ['af', {
'en':
"""
Configures IIR Bypass filter mode and low pass filter roll off corner frequency.

The filter can be applied or bypassed and the corner frequency can be
half or a ninth of the output data rate.

.. image:: /Images/Bricklets/bricklet_accelerometer_v2_filter.png
   :scale: 100 %
   :alt: Accelerometer filter
   :align: center
   :target: ../../_images/Bricklets/bricklet_accelerometer_v2_filter.png
""",
'de':
"""
Konfiguriert den IIR Bypass Filter Modus und die Low Pass Filter Roll Off Corner Frequenz.

Der Filter kann angewendet oder umgangen werden und die Frequenz kann die halbe oder ein Neuntel
der Ausgabe-Datenrate sein.

.. image:: /Images/Bricklets/bricklet_accelerometer_v2_filter.png
   :scale: 100 %
   :alt: Accelerometer filter
   :align: center
   :target: ../../_images/Bricklets/bricklet_accelerometer_v2_filter.png
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Filter Configuration',
'elements': [('IIR Bypass', 'uint8', 1, 'out', {'constant_group': 'IIR Bypass', 'default': 0}),
             ('Low Pass Filter', 'uint8', 1, 'out', {'constant_group': 'Low Pass Filter', 'default': 0})],
'since_firmware': [2, 0, 2],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Filter Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Filter Configuration` gesetzt.
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


com['openhab'] = {
    'imports': oh_generic_channel_imports() + ["org.eclipse.smarthome.core.library.types.OnOffType"],
    'params': [{
            'name': 'Data Rate',
            'type': 'integer',
            'options': [('0.781Hz', 0),
                        ('1.563Hz', 1),
                        ('3.125Hz', 2),
                        ('6.2512Hz', 3),
                        ('12.5Hz', 4),
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
                        ('25600Hz', 15)],
            'limitToOptions': 'true',
            'default': 7,
            'label': 'Data Rate',
            'description': 'The data rate of 0.781Hz to 25600Hz. Decreasing data rate or full scale range will also decrease the noise on the data.'
        }, {
            'name': 'Full Scale Range',
            'type': 'integer',
            'options': [('2g', 0),
                        ('4g', 1),
                        ('8g', 2)],
            'limitToOptions': 'true',
            'default': 0,
            'label': 'Full Scale Range',
            'description': 'Full scale range of -2g to +2g up to -8g to +8g. Decreasing data rate or full scale range will also decrease the noise on the data.'
        }, {
            'name': 'Info LED Mode',
            'type': 'integer',
            'options': [('Off', 0),
                        ('On', 1),
                        ('Show Heartbeat', 2)],
            'limitToOptions': 'true',
            'default': 0,
            'label': 'Info LED Mode',
            'description': 'Configures the info LED (marked as \\\"Force\\\" on the Bricklet) to be either turned off, turned on, or blink in heartbeat mode.'
        }, {
            'name': 'IIR Filter',
            'type': 'boolean',
            'default': 'true',
            'label': 'IIR Filter',
            'description': 'Enable to apply the IIR filter.'
        }, {
            'name': 'Low Pass Filter',
            'type': 'integer',
            'options': [('Ninth', 0),
                        ('Half', 1)],
            'limitToOptions': 'true',
            'default': 0,
            'label': 'Low Pass Filter Corner Frequency',
            'description': 'The low pass filter roll off corner frequency can be half or a ninth of the output data rate.'
        },
        update_interval('Acceleration', 'the acceleration')],
    'param_groups': oh_generic_channel_param_groups(),
    'init_code': """this.setConfiguration(cfg.dataRate, cfg.fullScaleRange);
    this.setFilterConfiguration(cfg.iirFilter ? 0 : 1, cfg.lowPassFilter);
    this.setInfoLEDConfig(cfg.infoLEDMode);
    this.setAccelerationCallbackConfiguration(cfg.accelerationUpdateInterval, true);""",
    'channels': [
        {
            'id': 'Acceleration {}'.format(axis.upper()),
            'type': 'Acceleration',
            'label': 'Acceleration {}'.format(axis.upper()),

            'getters': [{
                'packet': 'Get Acceleration',
                'transform': 'new QuantityType(value.{}{{divisor}}, {{unit}})'.format(axis)}],

            'callbacks': [{
                'packet': 'Acceleration',
                'transform': 'new QuantityType({}{{divisor}}, {{unit}})'.format(axis)}],
            'java_unit': 'SmartHomeUnits.STANDARD_GRAVITY',
            'divisor': '10000.0',
            'is_trigger_channel': False
        } for axis in ['x', 'y', 'z']
    ],
    'channel_types': [
        oh_generic_channel_type('Acceleration', 'Number:Acceleration', 'NOT USED',
                     description='The acceleration in g (1g = 9.80665m/s²), not to be confused with grams.',
                     read_only=True,
                     pattern='%.4f %unit%')
    ],
    'actions': ['Get Acceleration', 'Get Configuration', 'Get Info LED Config', 'Get Filter Configuration']
}
