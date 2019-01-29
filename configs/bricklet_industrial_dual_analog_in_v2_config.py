# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Dual Analog In Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

com = {
    'author': 'Ishraq Ibne Ashraf <ishraq@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2121,
    'name': 'Industrial Dual Analog In V2',
    'display_name': 'Industrial Dual Analog In 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures two DC voltages between -35V and +35V with 24bit resolution each',
        'de': 'Misst zwei Gleichspannungen zwischen -35V und +35V mit jeweils 24Bit Auflösung'
    },
    'comcu': True,
    'released': True,
    'documented': True,
    'discontinued': False,
    'packets': [],
    'examples': []
}

com['doc'] = {
'en':
"""
The Bricklet has two input channel. Functions that are related
directly to a channel have a ``channel`` parameter to specify one of the two
channels. Valid values for the ``channel`` parameter are 0 and 1.
""",
'de':
"""
Das Bricklet hat zwei Eingangskanäle. Funktionen die
sich direkt auf einen der Kanäle beziehen haben einen ``channel`` Parameter,
um den Kanal anzugeben. Gültige Werte für das ``channel`` Parameter sind 0
und 1.
"""
}

voltage_doc = {
'en':
"""
Returns the voltage for the given channel in mV.
""",
'de':
"""
Gibt die Spannung für den übergebenen Kanal in mV zurück.
"""
}

add_callback_value_function(
    packets      = com['packets'],
    name         = 'Get Voltage',
    data_name    = 'Voltage',
    data_type    = 'int32',
    has_channels = True,
    doc          = voltage_doc
)

com['packets'].append({
'type': 'function',
'name': 'Set Sample Rate',
'elements': [('Rate', 'uint8', 1, 'in', ('Sample Rate', [('976 SPS', 0),
                                                         ('488 SPS', 1),
                                                         ('244 SPS', 2),
                                                         ('122 SPS', 3),
                                                         ('61 SPS', 4),
                                                         ('4 SPS', 5),
                                                         ('2 SPS', 6),
                                                         ('1 SPS', 7)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the sample rate. The sample rate can be between 1 sample per second
and 976 samples per second. Decreasing the sample rate will also decrease the
noise on the data.

The default value is 6 (2 samples per second).
""",
'de':
"""
Setzt die Abtastrate. Der Wertebereich der verfügbare Abtastraten
liegt zwischen 1 Wert pro Sekunde und 976 Werte pro Sekunde. Ein
Verringern der Abtastrate wird auch das Rauschen auf den Daten verringern.

Der Standardwert ist 6 (2 Werte pro Sekunde).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Sample Rate',
'elements': [('Rate', 'uint8', 1, 'out', ('Sample Rate', [('976 SPS', 0),
                                                          ('488 SPS', 1),
                                                          ('244 SPS', 2),
                                                          ('122 SPS', 3),
                                                          ('61 SPS', 4),
                                                          ('4 SPS', 5),
                                                          ('2 SPS', 6),
                                                          ('1 SPS', 7)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the sample rate as set by :func:`Set Sample Rate`.
""",
'de':
"""
Gibt die Abtastrate zurück, wie von :func:`Set Sample Rate`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Calibration',
'elements': [('Offset', 'int32', 2, 'in'),
             ('Gain', 'int32', 2, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets offset and gain of MCP3911 internal calibration registers.

See MCP3911 datasheet 7.7 and 7.8. The Industrial Dual Analog In Bricklet 2.0
is already factory calibrated by Tinkerforge. It should not be necessary
for you to use this function
""",
'de':
"""
Setzt Offset und Gain der MCP3911 internen Kalibrierungsregister.

Siehe MCP3911 Datenblatt 7.7 und 7.8. Das Industrial Dual Analog In Bricklet 2.0
wird von Tinkerforge werkskalibriert. Ein Aufruf dieser Funktion sollte
nicht notwendig sein.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Calibration',
'elements': [('Offset', 'int32', 2, 'out'),
             ('Gain', 'int32', 2, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the calibration as set by :func:`Set Calibration`.
""",
'de':
"""
Gibt die Kalibrierung zurück, wie von :func:`Set Calibration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get ADC Values',
'elements': [('Value', 'int32', 2, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the ADC values as given by the MCP3911 IC. This function
is needed for proper calibration, see :func:`Set Calibration`.
""",
'de':
"""
Gibt die ADC-Werte des MCP3911 ICs zurück. Diese Funktion
wird für die Kalibrierung benötigt, siehe :func:`Set Calibration`.
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
For a positive threshold set the "min" parameter to the threshold value in mV
above which the LED should turn on and set the "max" parameter to 0. Example:
If you set a positive threshold of 10V, the LED will turn on as soon as the
voltage exceeds 10V and turn off again if it goes below 10V.
For a negative threshold set the "max" parameter to the threshold value in mV
below which the LED should turn on and set the "min" parameter to 0. Example:
If you set a negative threshold of 10V, the LED will turn on as soon as the
voltage goes below 10V and the LED will turn off when the voltage exceeds 10V.

In intensity mode you can define a range in mV that is used to scale the brightness
of the LED. Example with min=4V, max=20V: The LED is off at 4V, on at 20V
and the brightness is linearly scaled between the values 4V and 20V. If the
min value is greater than the max value, the LED brightness is scaled the other
way around.

By default the channel LED status config is set to intensity with min=0V and
max=10V.
""",
'de':
"""
Setzt die Kanal-LED-Status-Konfiguration. Diese Einstellung wird verwendet wenn
die Kanal-LED auf Kanalstatus eingestellt ist, siehe :func:`Set Channel LED Config`.

Für jeden Kanal kann zwischen Schwellwert- und Intensitätsmodus gewählt werden.

Im Schwellwertmodus kann ein positiver oder negativer Schwellwert definiert werden.
Für einen positiven Schwellwert muss das "min" Parameter auf den gewünschten
Schwellwert in mV gesetzt werden, über dem die LED eingeschaltet werden soll.
Der "max" Parameter muss auf 0 gesetzt werden. Beispiel: Bei einem positiven
Schwellwert von 10V wird die LED eingeschaltet sobald die gemessene Spannung
über 10V steigt und wieder ausgeschaltet sobald der Strom unter 10V fällt.
Für einen negativen Schwellwert muss das "max" Parameter auf den gewünschten
Schwellwert in mV gesetzt werden, unter dem die LED eingeschaltet werden soll.
Der "max" Parameter muss auf 0 gesetzt werden. Beispiel: Bei einem negativen
Schwellwert von 10mA wird die LED eingeschaltet sobald die gemessene Spannung
unter 10V fällt und wieder ausgeschaltet sobald der Strom über 10V steigt.

Im Intensitätsmodus kann ein Bereich in mV angegeben werden über den die Helligkeit
der LED skaliert wird. Beispiel mit min=4V und max=20V: Die LED ist bei 4V und
darunter aus, bei 20V und darüber an und zwischen 4V und 20V wird die Helligkeit
linear skaliert. Wenn der min Wert größer als der max Wert ist, dann wird die
Helligkeit andersherum skaliert.

Standardwerte: Intensitätsmodus mit min=0V und max=10V.
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
'functions': [('getter', ('Get Voltage', 'voltage from channel 0'), [(('Voltage', 'Voltage (Channel 0)'), 'int32', 1, 1000.0, 'V', None)], [('uint8', 0)])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Voltage', 'voltage'), [(('Channel', 'Channel'), 'uint8', 1, None, None, None), (('Voltage', 'Voltage'), 'int32', 1, 1000.0, 'V', None)], None, None),
              ('callback_configuration', ('Voltage', 'voltage (channel 0)'), [('uint8', 0)], 1000, False, 'x', [(0, 0)])]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('callback', ('Voltage', 'voltage'), [(('Channel', 'Channel'), 'uint8', 1, None, None, None), (('Voltage', 'Voltage'), 'int32', 1, 1000.0, 'V', None)], None, None),
              ('callback_configuration', ('Voltage', 'voltage (channel 0)'), [('uint8', 0)], 10000, False, '>', [(10, 0)])]
})
