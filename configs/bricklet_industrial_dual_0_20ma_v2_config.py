# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Dual 0-20mA Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

com = {
    'author': 'Ishraq Ibne Ashraf <ishraq@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2120,
    'name': 'Industrial Dual 0 20mA V2',
    'display_name': 'Industrial Dual 0-20mA 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures two DC currents between 0mA and 20mA (IEC 60381-1)',
        'de': 'Misst zwei Gleichströme zwischen 0mA und 20mA (IEC 60381-1)'
    },
    'comcu': True,
    'released': True,
    'documented': True,
    'discontinued': False,
    'packets': [],
    'examples': []
}

current_doc = {
'en':
"""
Returns the current of the specified channel. The value is in nA and between
0nA and 22505322nA (22.5mA).

It is possible to detect if an IEC 60381-1 compatible sensor is connected
and if it works probably.

If the returned current is below 4mA, there is likely no sensor connected
or the connected sensor is defective. If the returned current is over 20mA,
there might be a short circuit or the sensor is defective.
""",
'de':
"""
Gibt die gemessenen Stromstärke des spezifizierten Kanals zurück. Der Wert
ist in nA und im Bereich von 0nA bis 22505322nA (22,5mA).

Es ist möglich zu erkennen ob ein IEC 60381-1-kompatibler Sensor angeschlossen
ist und ob er funktionsfähig ist.

Falls die zurückgegebene Stromstärke kleiner als 4mA ist, ist wahrscheinlich
kein Sensor angeschlossen oder der Sensor ist defekt. Falls die zurückgegebene
Stromstärke über 20mA ist, besteht entweder ein Kurzschluss oder der Sensor
ist defekt. Somit ist erkennbar ob ein Sensor angeschlossen und funktionsfähig
ist.
"""
}

add_callback_value_function(
    packets      = com['packets'],
    name         = 'Get Current',
    data_name    = 'Current',
    data_type    = 'int32',
    has_channels = True,
    doc          = current_doc
)

com['packets'].append({
'type': 'function',
'name': 'Set Sample Rate',
'elements': [('Rate', 'uint8', 1, 'in', ('Sample Rate', [('240 SPS', 0),
                                                         ('60 SPS', 1),
                                                         ('15 SPS', 2),
                                                         ('4 SPS', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the sample rate to either 240, 60, 15 or 4 samples per second.
The resolution for the rates is 12, 14, 16 and 18 bit respectively.

.. csv-table::
 :header: "Value", "Description"
 :widths: 10, 100

 "0",    "240 samples per second, 12 bit resolution"
 "1",    "60 samples per second, 14 bit resolution"
 "2",    "15 samples per second, 16 bit resolution"
 "3",    "4 samples per second, 18 bit resolution"

The default value is 3 (4 samples per second with 18 bit resolution).
""",
'de':
"""
Setzt die Abtastrate auf 240, 60, 15 oder 4 Samples pro Sekunde.
Die Auflösung für die Raten sind 12, 14, 16 und 18 Bit respektive.

.. csv-table::
 :header: "Wert", "Beschreibung"
 :widths: 10, 100

 "0",    "240 Samples pro Sekunde, 12 Bit Auflösung"
 "1",    "60 Samples pro Sekunde, 14 Bit Auflösung"
 "2",    "15 Samples pro Sekunde, 16 Bit Auflösung"
 "3",    "4 Samples pro Sekunde, 18 Bit Auflösung"

Der Standardwert ist 3 (4 Samples pro Sekunde mit 18 Bit Auflösung).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Sample Rate',
'elements': [('Rate', 'uint8', 1, 'out', ('Sample Rate', [('240 SPS', 0),
                                                          ('60 SPS', 1),
                                                          ('15 SPS', 2),
                                                          ('4 SPS', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the gain as set by :func:`Set Sample Rate`.
""",
'de':
"""
Gibt die Verstärkung zurück, wie von :func:`Set Sample Rate`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Gain',
'elements': [('Gain', 'uint8', 1, 'in', ('Gain', [('1x', 0),
                                                  ('2x', 1),
                                                  ('4x', 2),
                                                  ('8x', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets a gain between 1x and 8x. If you want to measure a very small current,
you can increase the gain to get some more resolution.

Example: If you measure 0.5mA with a gain of 8x the return value will be
4mA.

The default gain is 1x.
""",
'de':
"""
Setzt den Gain zwischen 1x und 8x. Wenn ein sehr kleiner Strom gemessen werden
soll, dann kann der Gain hochgesetzt werden, um die Auflösung zu verbessern.

Beispiel: Wenn 0,5mA gememsen werden mit einem Gain von 8x dann wird 4mA
zurückgegeben.

Der Standardwert ist 1x.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Gain',
'elements': [('Gain', 'uint8', 1, 'out', ('Gain', [('1x', 0),
                                                   ('2x', 1),
                                                   ('4x', 2),
                                                   ('8x', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the gain as set by :func:`Set Gain`.
""",
'de':
"""
Gibt die Verstärkung zurück, wie von :func:`Set Gain` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Channel LED Config',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Config', 'uint8', 1, 'in', ('Channel LED Config', [('Off', 0),
                                                                  ('On', 1),
                                                                  ('Show Heartbeat', 2),
                                                                  ('Show Channel Status', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Each channel has a corresponding LED. You can turn the LED off, on or show a
heartbeat. You can also set the LED to "Channel Status". In this mode the
LED can either be turned on with a pre-defined threshold or the intensity
of the LED can change with the measured value.

You can configure the channel status behavior with :func:`Set Channel LED Status Config`.

By default all channel LEDs are configured as "Channel Status".
""",
'de':
"""
Jeder Kanal hat eine dazugehörige LED. Die LEDs können individuell an- oder
ausgeschaltet werden. Zusätzlich kann ein Heartbeat oder der Kanalstatus
angezeigt werden. Falls Kanalstatus gewählt wird kann die LED entweder ab einem
vordefinierten Schwellwert eingeschaltet werden oder ihre Helligkeit anhand des
gemessenen Wertes skaliert werden.

Das Verhalten des Kanalstatus kann mittels :func:`Set Channel LED Status Config`
eingestellt werden.

Standardmäßig sind die LEDs für alle Kanäle auf Kanalstatus konfiguriert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Channel LED Config',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Config', 'uint8', 1, 'out', ('Channel LED Config', [('Off', 0),
                                                                   ('On', 1),
                                                                   ('Show Heartbeat', 2),
                                                                   ('Show Channel Status', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the channel LED configuration as set by :func:`Set Channel LED Config`
""",
'de':
"""
Gibt die Kanal-LED-Konfiguration zurück, wie von :func:`Set Channel LED Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Channel LED Status Config',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Min', 'int32', 1, 'in'),
             ('Max', 'int32', 1, 'in'),
             ('Config', 'uint8', 1, 'in', ('Channel LED Status Config', [('Threshold', 0),
                                                                         ('Intensity', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the channel LED status config. This config is used if the channel LED is
configured as "Channel Status", see :func:`Set Channel LED Config`.

For each channel you can choose between threshold and intensity mode.

In threshold mode you can define a positive or a negative threshold.
For a positive threshold set the "min" parameter to the threshold value in nA
above which the LED should turn on and set the "max" parameter to 0. Example:
If you set a positive threshold of 10mA, the LED will turn on as soon as the
current exceeds 10mA and turn off again if it goes below 10mA.
For a negative threshold set the "max" parameter to the threshold value in nA
below which the LED should turn on and set the "min" parameter to 0. Example:
If you set a negative threshold of 10mA, the LED will turn on as soon as the
current goes below 10mA and the LED will turn off when the current exceeds 10mA.

In intensity mode you can define a range in nA that is used to scale the brightness
of the LED. Example with min=4mA and max=20mA: The LED is off at 4mA and below,
on at 20mA and above and the brightness is linearly scaled between the values
4mA and 20mA. If the min value is greater than the max value, the LED brightness
is scaled the other way around.

By default the channel LED status config is set to intensity with min=4mA and
max=20mA.
""",
'de':
"""
Setzt die Kanal-LED-Status-Konfiguration. Diese Einstellung wird verwendet wenn
die Kanal-LED auf Kanalstatus eingestellt ist, siehe :func:`Set Channel LED Config`.

Für jeden Kanal kann zwischen Schwellwert- und Intensitätsmodus gewählt werden.

Im Schwellwertmodus kann ein positiver oder negativer Schwellwert definiert werden.
Für einen positiven Schwellwert muss das "min" Parameter auf den gewünschten
Schwellwert in nA gesetzt werden, über dem die LED eingeschaltet werden soll.
Der "max" Parameter muss auf 0 gesetzt werden. Beispiel: Bei einem positiven
Schwellwert von 10mA wird die LED eingeschaltet sobald der gemessene Strom über
10mA steigt und wieder ausgeschaltet sobald der Strom unter 10mA fällt.
Für einen negativen Schwellwert muss das "max" Parameter auf den gewünschten
Schwellwert in nA gesetzt werden, unter dem die LED eingeschaltet werden soll.
Der "max" Parameter muss auf 0 gesetzt werden. Beispiel: Bei einem negativen
Schwellwert von 10mA wird die LED eingeschaltet sobald der gemessene Strom unter
10mA fällt und wieder ausgeschaltet sobald der Strom über 10mA steigt.

Im Intensitätsmodus kann ein Bereich in nA angegeben werden über den die Helligkeit
der LED skaliert wird. Beispiel mit min=4mA und max=20mA: Die LED ist bei 4mA und
darunter aus, bei 20mA und darüber an und zwischen 4mA und 20mA wird die Helligkeit
linear skaliert. Wenn der min Wert größer als der max Wert ist, dann wird die
Helligkeit andersherum skaliert.

Standardwerte: Intensitätsmodus mit min=4mA und max=20mA.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Channel LED Status Config',
'elements': [('Channel', 'uint8', 1, 'in'),
             ('Min', 'int32', 1, 'out'),
             ('Max', 'int32', 1, 'out'),
             ('Config', 'uint8', 1, 'out', ('Channel LED Status Config', [('Threshold', 0),
                                                                          ('Intensity', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the channel LED status configuration as set by
:func:`Set Channel LED Status Config`.
""",
'de':
"""
Gibt die Kanal-LED-Status-Konfiguration zurück, wie von
:func:`Set Channel LED Status Config` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Current', 'current from channel 0'), [(('Current', 'Current (Channel 0)'), 'int32', 1, 1000000.0, 'mA', None)], [('uint8', 0)])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Current', 'current'), [(('Channel', 'Channel'), 'uint8', 1, None, None, None), (('Current', 'Current'), 'int32', 1, 1000000.0, 'mA', None)], None, None),
              ('callback_configuration', ('Current', 'current (channel 0)'), [('uint8', 0)], 1000, False, 'x', [(0, 0)])]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('callback', ('Current', 'current'), [(('Channel', 'Channel'), 'uint8', 1, None, None, None), (('Current', 'Current'), 'int32', 1, 1000000.0, 'mA', None)], None, None),
              ('callback_configuration', ('Current', 'current (channel 0)'), [('uint8', 0)], 10000, False, '>', [(10, 0)])]
})
