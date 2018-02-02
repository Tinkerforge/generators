# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Sound Pressure Level Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 290,
    'name': 'Sound Pressure Level',
    'display_name': 'Sound Pressure Level',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures Sound Pressure Level in dB(A/B/C/D/Z)',
        'de': 'Misst Schalldruck in dB(A/B/C/D/Z)'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'discontinued': False,
    'packets': [],
    'examples': []
}

decibel_doc = {
'en':
"""
Returns the measured decibels. The values are given in dB/10 (tenths dB).

The Bricklet supports the weighting standards dB(A), dB(B), dB(C), dB(D),
dB(Z) and ITU-R 468. You can configure the weighting with :func:`Set Configuration`.

By default dB(A) will be used.
""",
'de':
"""
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Decibel',
    data_name = 'Decibel',
    data_type = 'uint16',
    doc       = decibel_doc
)

com['packets'].append({
'type': 'function',
'name': 'Get Spectrum Low Level',
'elements': [('Spectrum Length', 'uint16', 1, 'out'),
             ('Spectrum Chunk Offset', 'uint16', 1, 'out'),
             ('Spectrum Chunk Data', 'uint16', 30, 'out')],
'high_level': {'stream_out': {'name': 'Spectrum'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the spectrum. The length of the spectrum is between
512 (FFT size 1024) and 64 (FFT size 128). See :func:`Set Configuration`.

Each array element is one bin of the FFT. The first bin is always the
DC offset and the other bins have a size between 40Hz (FFT size 1024) and
320Hz (FFT size 128).

In sum the frequency of the spectrum always has a range from 0 to
20480Hz (the FFT is applied to samples with a frequency of 40960Hz).

The Returned data is already equalized and the weighting function is applied
(see :func:`Set Configuration` for the available weighting standards). Use
dB(Z) if you need the unaltered spectrum.

The values are not in dB form yet. If you want a proper dB scale of the
spectrum you have to apply the formula f(x) = 20*log10(max(1, x/sqrt(2))) 
on each value.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Spectrum Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period in ms is the period with which the :cb:`Spectrum` callback is triggered
periodically. A value of 0 turns the callback off.

Every new measured spectrum will be send at most once. Set the period to 1 to make
sure that you get every spectrum.

The default value is 0.
""",
'de':
"""
Die Periode in ms ist die Periode mit der der :cb:`Spectrum` Callback ausgelöst wird.
Ein Wert von 0 schaltet den Callback ab.

Jedes gemessene Spektrum wird maximal einmal gesendet. Setze die Periode auf 1
um sicher zu stellen das jedes Spektrum gesendet wird.

Der Standardwert ist 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Spectrum Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by :func:`Get Spectrum Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels :func:`Get Spectrum Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Spectrum Low Level',
'elements': [('Spectrum Length', 'uint16', 1, 'out'),
             ('Spectrum Chunk Offset', 'uint16', 1, 'out'),
             ('Spectrum Chunk Data', 'uint16', 30, 'out')],
'high_level': {'stream_out': {'name': 'Spectrum'}},
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set Spectrum Callback Configuration`. 

The `parameter` is the same as :func:`Get Spectrum`.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:Set Spectrum Callback Configuration` gesetzten Konfiguration

Der `parameter` ist der gleiche wie :func:`Get Spectrum`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('FFT Size', 'uint8', 1, 'in', ('FFT Size', [('128', 0),
                                                          ('256', 1),
                                                          ('512', 2),
                                                          ('1024', 3)])),
             ('Weighting', 'uint8', 1, 'in', ('Weighting', [('A', 0),
                                                            ('B', 1),
                                                            ('C', 2),
                                                            ('D', 3),
                                                            ('Z', 4),
                                                            ('ITU R 468', 5)])),
],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the Sound Pressure Level Bricklet configuration.

With different FFT sizes the Bricklet has a different
amount of samples per second and the size of the FFT bins
changes. The higher the FFT size the more precise is the result
of the dB(X) calculation.

Available FFT sizes are:

* 1024: 512 bins, 10 samples per second, each bin has size 40Hz
* 512: 256 bins, 20 samples per second, each bin has size 80Hz
* 256: 128 bins, 40 samples per second, each bin has size 160Hz
* 128: 64 bins, 80 samples per second, each bin has size 320Hz

The Bricklet supports different weighting functions. You can choose
between dB(A), dB(B), dB(C), dB(D), dB(Z) and ITU-R 468.

dB(A/B/C/D) are the standard dB weighting curves. dB(A) is
often used to measure volumes at concerts etc. dB(Z) has a
flat response, no weighting is applied. ITU-R 468 is an ITU
weighting standard mostly used in the UK and Europe.

The defaults are FFT size 1024 and weighting standard dB(A).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('FFT Size', 'uint8', 1, 'out', ('FFT Size', [('128', 0),
                                                           ('256', 1),
                                                           ('512', 2),
                                                           ('1024', 3)])),
             ('Weighting', 'uint8', 1, 'out', ('Weighting', [('A', 0),
                                                             ('B', 1),
                                                             ('C', 2),
                                                             ('D', 3),
                                                             ('Z', 4),
                                                             ('ITU R 468', 5)])),
],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the configuration as set by :func:`Set Configuration`.
""",
'de':
"""
"""
}]
})
