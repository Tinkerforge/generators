# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Dual 0-20mA Bricklet 2.0 communication config

# TODO: Documentation and examples.

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
    'released': False,
    'documented': False,
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
Gibt die gemessenen Stromstärke des spezifiziert Channel zurück. Der Wert
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
'elements': [('Gain', 'uint8', 1, 'in', ('Gain', [('1X', 0),
                                                  ('2X', 1),
                                                  ('4X', 2),
                                                  ('8X', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets a gain between 1x and 8x. If you want to measure a very small current,
you can incerase the gain to get some more resolution.

Example: If you measure 0.5mA with a gain of 8x the return value will be
4mA.

The default gain is 1x.
""",
'de':
"""

"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Gain',
'elements': [('Gain', 'uint8', 1, 'out', ('Gain', [('1X', 0),
                                                   ('2X', 1),
                                                   ('4X', 2),
                                                   ('8X', 3)]))],
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
Each channel has a corresponding LED. You can turn the LED Off, On or show a
heartbeat. You can also set the LED to "Channel Status". In this mode the
LED can either be turned on with a pre-defined threshold or the intensity
of the LED can change with the measured value.

You can configure the channel status behavior with :func:`Set Channel LED Status Config`.

By default all channel LEDs are configured as "Channel Status".
""",
'de':
"""

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
Returns the Channel LED configuration as set by :func:`Set Channel LED Config`
""",
'de':
"""
Gibt die LED-Konfiguration zurück, wie von :func:`Set Channel LED Config` gesetzt.
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
Sets the channel LED status config. This config is used if the channel LED is configured
as Channel Status, see :func:`Set Channel LED Config`.

For each channel you can choose between the threshold and intensity.

In the threshold-mode you can define a positive threshold in nA as the "min" parameter. The "max"
parameter has to be 0. Example: If you set a positive threshold of 10mA, the LED will turn on
as soon as the current exceeds 10mA and turn off again if it goes below 10mA. You can also define
a negative threshold. For that you set the "max" parameter to the threshold value in nA and set
the "min" parameter to 0. Example: If you set a negative threshold of 10mA, the LED will turn on
as soon as the current goes below 10mA and the LED will turn off when the current exceeds 10mA.

In the intensity-mode you can define a range that is used to scale the brightness of the LED.
Example with min=4mA, max=20mA: The LED is off at 4mA, on at 20mA and the brightness is linearly
scaled between the vales 4mA and 20mA. If the min value is greater than the max value, the
LED brightness is scaled the other way around.
""",
'de':
"""

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
Returns the Channel LED configuration as set by :func:`Set Channel LED Status Config`
""",
'de':
"""
Gibt die LED-Konfiguration zurück, wie von :func:`Set Channel LED Status Config` gesetzt.
"""
}]
})
