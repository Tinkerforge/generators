# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Dual 0-20mA 2.0 Bricklet communication config

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

channel_0_current_doc = {
'en':
"""
Returns the current of channel 0. The value is in nA and between 0nA and
22505322nA (22.5mA).

It is possible to detect if an IEC 60381-1 compatible sensor is connected
and if it works probably.

If the returned current is below 4mA, there is likely no sensor connected
or the sensor is may be defective. If the returned current is over 20mA,
there might be a short circuit or the sensor is may be defective.

If you want to get the current periodically, it is recommended to use the
:cb:`Channel 0 Current` callback and set the period with
:func:`Set Channel 0 Current Callback Configuration`.
""",
'de':
"""
Gibt die gemessenen Stromstärke des Channel 0 zurück. Der Wert ist in nA
und im Bereich von 0nA bis 22505322nA (22,5mA).

Es ist möglich zu erkennen ob ein IEC 60381-1-kompatibler Sensor angeschlossen
ist und ob er funktionsfähig ist.

Falls die zurückgegebene Stromstärke kleiner als 4mA ist, ist wahrscheinlich
kein Sensor angeschlossen oder der Sensor ist defekt. Falls die zurückgegebene
Stromstärke über 20mA ist, besteht entweder ein Kurzschluss oder der Sensor
ist defekt. Somit ist erkennbar ob ein Sensor angeschlossen und funktionsfähig
ist.

Wenn die Stromstärke periodisch abgefragt werden soll, wird empfohlen
den :cb:`Channel 0 Current` Callback zu nutzen und die Periode mit
:func:`Set Channel 0 Current Callback Configuration` vorzugeben.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Channel 0 Current',
    data_name = 'Channel 0 Current',
    data_type = 'int32',
    doc       = channel_0_current_doc
)

channel_1_current_doc = {
'en':
"""
Returns the current of channel 1. The value is in nA and between 0nA and
22505322nA (22.5mA).

It is possible to detect if an IEC 60381-1 compatible sensor is connected
and if it works probably.

If the returned current is below 4mA, there is likely no sensor connected
or the sensor is may be defective. If the returned current is over 20mA,
there might be a short circuit or the sensor is may be defective.

If you want to get the current periodically, it is recommended to use the
:cb:`Channel 1 Current` callback and set the period with
:func:`Set Channel 1 Current Callback Configuration`.
""",
'de':
"""
Gibt die gemessenen Stromstärke des Channel 1 zurück. Der Wert ist in nA
und im Bereich von 0nA bis 22505322nA (22,5mA).

Es ist möglich zu erkennen ob ein IEC 60381-1-kompatibler Sensor angeschlossen
ist und ob er funktionsfähig ist.

Falls die zurückgegebene Stromstärke kleiner als 4mA ist, ist wahrscheinlich
kein Sensor angeschlossen oder der Sensor ist defekt. Falls die zurückgegebene
Stromstärke über 20mA ist, besteht entweder ein Kurzschluss oder der Sensor
ist defekt. Somit ist erkennbar ob ein Sensor angeschlossen und funktionsfähig
ist.

Wenn die Stromstärke periodisch abgefragt werden soll, wird empfohlen
den :cb:`Channel 1 Current` Callback zu nutzen und die Periode mit
:func:`Set Channel 1 Current Callback Configuration` vorzugeben.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Channel 1 Current',
    data_name = 'Channel 1 Current',
    data_type = 'int32',
    doc       = channel_1_current_doc
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
'name': 'Set Gain',
'elements': [('Gain', 'uint8', 1, 'in', ('Gain', [('1X', 0),
                                                  ('2X', 1),
                                                  ('4X', 2),
                                                  ('8X', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""

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
Gibt die Verstärkung zurück, wie von :func:`Set Gain`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Info LED Config',
'elements': [('LED', 'uint8', 1, 'in'),
             ('Config', 'uint8', 1, 'in', ('Info LED Config', [('Off', 0),
                                                               ('On', 1),
                                                               ('Show Heartbeat', 2),
                                                               ('Show Channel Status', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""

""",
'de':
"""

"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Info LED Config',
'elements': [('LED', 'uint8', 1, 'in'),
             ('Config', 'uint8', 1, 'out', ('Info LED Config', [('Off', 0),
                                                                ('On', 1),
                                                                ('Show Heartbeat', 2),
                                                                ('Show Channel Status', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the Info LED configuration as set by :func:`Set Info LED Config`
""",
'de':
"""
Gibt die LED-Konfiguration zurück, wie von :func:`Set Info LED Config` gesetzt.
"""
}]
})
