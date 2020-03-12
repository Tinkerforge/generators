# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Sound Pressure Level Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from commonconstants import add_callback_value_function

from openhab_commonconfig import *

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

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

com['constant_groups'].append({
'name': 'FFT Size',
'type': 'uint8',
'constants': [('128', 0),
              ('256', 1),
              ('512', 2),
              ('1024', 3)]
})

com['constant_groups'].append({
'name': 'Weighting',
'type': 'uint8',
'constants': [('A', 0),
              ('B', 1),
              ('C', 2),
              ('D', 3),
              ('Z', 4),
              ('ITU R 468', 5)]
})

decibel_doc = {
'en':
"""
Returns the measured sound pressure in decibels.

The Bricklet supports the weighting standards dB(A), dB(B), dB(C), dB(D),
dB(Z) and ITU-R 468. You can configure the weighting with :func:`Set Configuration`.

By default dB(A) will be used.
""",
'de':
"""
Gibt die gemessenen Schalldruck in Dezibel zurück.

Das Bricklet unterstützt die Gewichtungen dB(A), dB(B), dB(C), dB(D), dB(Z) und
ITU-R 468. Die Gewichtungsfunktion kann mittels :func:`Set Configuration`
gesetzt werden.

Standardmäßig wird dB(A) genutzt.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Decibel',
    data_name = 'Decibel',
    data_type = 'uint16',
    doc       = decibel_doc,
    scale     = (1, 10),
    unit      = 'Decibel',
    range_    = (0, 120)
)

com['packets'].append({
'type': 'function',
'name': 'Get Spectrum Low Level',
'elements': [('Spectrum Length', 'uint16', 1, 'out', {'range': (64, 512)}),
             ('Spectrum Chunk Offset', 'uint16', 1, 'out', {}),
             ('Spectrum Chunk Data', 'uint16', 30, 'out', {'scale': 'dynamic', 'unit': 'Decibel'})],
'high_level': {'stream_out': {'name': 'Spectrum'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the frequency spectrum. The length of the spectrum is between
512 (FFT size 1024) and 64 (FFT size 128). See :func:`Set Configuration`.

Each array element is one bin of the FFT. The first bin is always the
DC offset and the other bins have a size between 40Hz (FFT size 1024) and
320Hz (FFT size 128).

In sum the frequency of the spectrum always has a range from 0 to
20480Hz (the FFT is applied to samples with a frequency of 40960Hz).

The returned data is already equalized, which means that the microphone
frequency response is compensated and the weighting function is applied
(see :func:`Set Configuration` for the available weighting standards). Use
dB(Z) if you need the unaltered spectrum.

The values are not in dB form yet. If you want a proper dB scale of the
spectrum you have to apply the formula f(x) = 20*log10(max(1, x/sqrt(2)))
on each value.
""",
'de':
"""
Gibt das Frequenzspektrum zurück. Die Länge des Spektrums liegt zwischen 512
(FFT Größe 1024) und 64 (FFT Größe 128). Siehe :func:`Set Configuration`.

Jedes Listen-Element ist eine Gruppe des FFTs. Die erste Gruppe stellt immer
das DC Offset dar. Die anderen Gruppen haben eine Größe zwischen 40Hz (FFT
Größe 1024) und 320Hz (FFT Größe 128).

Der Frequenzbereich des Spektrums besitzt immer einen Umfang von 0 bis 20480Hz
(FFT wird auf Samples mit bis zu 40960Hz angewendet).

Die zurückgegebenen Daten sind bereits ausgeglichen, was bedeutet dass der
Mikrofon-Frequenzgang kompensiert wurde, und die Gewichtungsfunktion wurde
angewendet (siehe :func:`Set Configuration` für die zur Verfügung stehenden
Gewichtungen). Für ein ungewichtets Spektrum kann dB(Z) genutzt werden.

Die Daten sind nicht in dB skaliert. Um diese in einer dB Form darzustellen
muss die Formel f(x) = 20*log10(max(1, x/sqrt(2))) auf jeden Wert angewendet
werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Spectrum Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period is the period with which the :cb:`Spectrum` callback is
triggered periodically. A value of 0 turns the callback off.

Every new measured spectrum will be send at most once. Set the period to 1 to
make sure that you get every spectrum.
""",
'de':
"""
Die Periode ist die Periode mit der der :cb:`Spectrum` Callback ausgelöst
wird. Ein Wert von 0 schaltet den Callback ab.

Jedes gemessene Spektrum wird maximal einmal gesendet. Setze die Periode auf 1
um sicher zu stellen das jedes Spektrum gesendet wird.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Spectrum Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Get Spectrum Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Get Spectrum Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Spectrum Low Level',
'elements': [('Spectrum Length', 'uint16', 1, 'out', {'range': (64, 512)}),
             ('Spectrum Chunk Offset', 'uint16', 1, 'out', {}),
             ('Spectrum Chunk Data', 'uint16', 30, 'out', {'scale': 'dynamic', 'unit': 'Decibel'})],
'high_level': {'stream_out': {'name': 'Spectrum'}},
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set Spectrum Callback Configuration`.

The :word:`parameter` is the same as :func:`Get Spectrum`.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set Spectrum Callback Configuration` gesetzten Konfiguration

Der :word:`parameter` ist der gleiche wie :func:`Get Spectrum`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('FFT Size', 'uint8', 1, 'in', {'constant_group': 'FFT Size', 'default': 3}),
             ('Weighting', 'uint8', 1, 'in', {'constant_group': 'Weighting', 'default': 0}),
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
""",
'de':
"""
Setzt die Sound Pressure Level Bricklet Konfiguration.

Verschiedene FFT Größen führen zu unterschiedlichen Abtastraten und
FFT Größen. Umso größer die FFT Größe ist, umso genauer ist das Ergebnis
der dB(X) Berechnung.

Verfügbare FFT Größen sind:

* 1024: 512 Gruppen, 10 Samples pro Sekunde, jede Gruppe hat Größe 40Hz
* 512: 256 Gruppen, 20 Samples per Sekunde, jede Gruppe hat Größe 80Hz
* 256: 128 Gruppen, 40 Samples per Sekunde, jede Gruppe hat Größe 160Hz
* 128: 64 Gruppen, 80 Samples pro Sekunde, jede Gruppe hat Größe 320Hz

Das Bricklet unterstützt verschiedene Gewichtungsfunktionen. Es kann zwischen
dB(A), dB(B), dB(C), dB(D), dB(Z) und ITU-R 468 gewählt werden.

dB(A/B/C/D) sind Standard-Gewichtungskurven. dB(A) wird of genutzt um
Lautstärke in Konzerten zu messen. dB(Z) besitzt keine Gewichtung und gibt
die Daten ungewichtet zurück. ITU-R 468 ist ein ITU Gewichtungsstandard der
hauptsächlich in UK und Europa verwendet wird.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('FFT Size', 'uint8', 1, 'out', {'constant_group': 'FFT Size', 'default': 3}),
             ('Weighting', 'uint8', 1, 'out', {'constant_group': 'Weighting', 'default': 0}),
],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the configuration as set by :func:`Set Configuration`.
""",
'de':
"""
Gibt die Konfiguration, die mittels :func:`Set Configuration` gesetzt werden kann zurück.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Decibel', 'decibel'), [(('Decibel', 'Decibel'), 'uint16', 1, 10.0, 'dB(A)', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Decibel', 'decibel'), [(('Decibel', 'Decibel'), 'uint16', 1, 10.0, 'dB(A)', None)], None, None),
              ('callback_configuration', ('Decibel', 'decibel'), [], 1000, False, 'x', [(0, 0)])]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('callback', ('Decibel', 'decibel'), [(('Decibel', 'Decibel'), 'uint16', 1, 10.0, 'dB(A)', None)], None, None),
              ('callback_configuration', ('Decibel', 'decibel'), [], 1000, False, '>', [(60, 0)])]
})


com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'params': [
         {
            'packet': 'Set Configuration',
            'element': 'FFT Size',

            'name': 'FFT Size',
            'type': 'integer',
            'label': 'FFT Size',
            'description': 'With different FFT sizes the Bricklet has a different amount of samples per second and the size of the FFT bins changes. The higher the FFT size the more precise is the result of the dB(X) calculation.',
        },
        {
            'packet': 'Set Configuration',
            'element': 'Weighting',

            'name': 'Weighting',
            'type': 'integer',
            'options': [('dB(A)', 0),
              ('dB(B)', 1),
              ('dB(C)', 2),
              ('dB(D)', 3),
              ('dB(Z)', 4),
              ('ITU-R 468', 5)],
            'limit_to_options': 'true',

            'label': 'Weighting',
            'description': 'The Bricklet supports different weighting functions. dB(A/B/C/D) are the standard dB weighting curves. dB(A) is often used to measure volumes at concerts etc. dB(Z) has a flat response, no weighting is applied. ITU-R 468 is an ITU weighting standard mostly used in the UK and Europe.',
        }
    ],
    'init_code': """
this.setConfiguration(cfg.fftSize, cfg.weighting);""",
    'channels': [
        oh_generic_channel('Decibel', 'Decibel'),
    ],
    'channel_types': [
        oh_generic_channel_type('Decibel', 'Number', 'Sound Pressure',
                    update_style='Callback Configuration',
                    description='Measured Sound Pressure',
                    read_only=True,
                    pattern='%.1f %unit%'),
    ],
    'actions': ['Get Decibel', 'Get Spectrum', 'Get Configuration']
}
