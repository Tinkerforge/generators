# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Piezo Speaker Bricklet communication config

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 242,
    'name': 'Piezo Speaker',
    'display_name': 'Piezo Speaker',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Creates beep with configurable frequency',
        'de': 'Erzeugt Piepton mit konfigurierbarer Frequenz'
    },
    'released': True,
    'documented': True,
    'discontinued': False, # selling remaining stock, replaced by Piezo Speaker Bricklet 2.0
    'features': [
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append({
'name': 'Beep Duration',
'type': 'uint32',
'constants': [('Off', 0),
              ('Infinite', 4294967295)]
})

com['packets'].append({
'type': 'function',
'name': 'Beep',
'elements': [('Duration', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'range': 'type', 'constant_group': 'Beep Duration'}),
             ('Frequency', 'uint16', 1, 'in', {'unit': 'Hertz', 'range': (585, 7100)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Beeps with the given frequency for the given duration.

.. versionchanged:: 2.0.2$nbsp;(Plugin)
   A duration of 0 stops the current beep if any, the frequency parameter is
   ignored. A duration of 4294967295 results in an infinite beep.

The Piezo Speaker Bricklet can only approximate the frequency, it will play
the best possible match by applying the calibration (see :func:`Calibrate`).
""",
'de':
"""
Erzeugt einen Piepton mit der gegebenen Frequenz für die angegebene Dauer.

.. versionchanged:: 2.0.2$nbsp;(Plugin)
   Eine *durarion* von 0 stoppt den aktuellen Piepton, der *frequency* Parameter
   wird ignoriert. Eine *durarion* von 4294967295 führt zu einem unendlich
   langen Piepton.

Das Piezo Speaker Bricklet kann die angegebenen Frequenzen nur approximieren,
es wählt die bestmögliche Zuordnung anhand der Kalibrierung
(siehe :func:`Calibrate`).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Morse Code',
'elements': [('Morse', 'string', 60, 'in', {}),
             ('Frequency', 'uint16', 1, 'in', {'unit': 'Hertz', 'range': (585, 7100)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets morse code that will be played by the piezo buzzer. The morse code
is given as a string consisting of "." (dot), "-" (minus) and " " (space)
for *dits*, *dahs* and *pauses*. Every other character is ignored.

For example: If you set the string "...---...", the piezo buzzer will beep
nine times with the durations "short short short long long long short
short short".
""",
'de':
"""
Setzt Morsecode welcher vom Piezosummer abgespielt wird. Der Morsecode wird
als Zeichenkette, mit den Zeichen "." (Punkt), "-" (Minus) und " " (Leerzeichen)
für *kurzes Signale*, *langes Signale* und *Pausen*. Alle anderen Zeichen
werden ignoriert.

Beispiel: Wenn die Zeichenkette "...---..." gesetzt wird, gibt der Piezosummer neun
Pieptöne aus mit den Dauern "kurz kurz kurz lang lang lang kurz kurz kurz".
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Calibrate',
'elements': [('Calibration', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
The Piezo Speaker Bricklet can play 512 different tones. This function
plays each tone and measures the exact frequency back. The result is a
mapping between setting value and frequency. This mapping is stored
in the EEPROM and loaded on startup.

The Bricklet should come calibrated, you only need to call this
function (once) every time you reflash the Bricklet plugin.

Returns *true* after the calibration finishes.
""",
'de':
"""
Das Piezo Speaker Bricklet kann 512 unterschiedliche Töne spielen. Diese
Funktion spielt jeden Ton einmal und misst die exakte Frequenz zurück.
Das Ergebnis ist eine Zuordnung von Stellwerten zu Frequenzen. Diese
Zuordnung wird im EEPROM gespeichert und bei jedem start des Bricklets
geladen.

Das Bricklet sollte bei Auslieferung bereits kalibriert sein. Diese
Funktion muss lediglich (einmalig) nach jedem neuflashen des Bricklet-Plugins
ausgeführt werden.

Gibt *true* nach Abschluss der Kalibrierung zurück.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Beep Finished',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered if a beep set by :func:`Beep` is finished
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn ein Piepton, wie von :func:`Beep` gesetzt,
beendet wurde.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Morse Code Finished',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered if the playback of the morse code set by
:func:`Morse Code` is finished.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn die Wiedergabe des Morsecodes, wie von
:func:`Morse Code` gesetzt, beendet wurde.
"""
}]
})

com['examples'].append({
'name': 'Beep',
'functions': [('setter', 'Beep', [('uint16', 2000), ('uint16', 1000)], 'Make 2 second beep with a frequency of 1kHz', None)]
})

com['examples'].append({
'name': 'Morse Code',
'functions': [('setter', 'Morse Code', [('string', '... --- ...'), ('uint16', 2000)], 'Morse SOS with a frequency of 2kHz', None)]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.OnOffType'],
    'param_groups': oh_generic_channel_param_groups(),
    'channels': [{
            'id': 'Beep Finished',
            'label': 'Beep Finished',
            'type': 'system.trigger',

            'callbacks': [{
                'packet': 'Beep Finished',
                'transform': '""'}],
            'description': 'This channel is triggered if a beep set by the beep action is finished.'
        }, {
            'id': 'Morse Code Finished',
            'label': 'Morse Code Finished',
            'type': 'system.trigger',

            'callbacks': [{
                'packet': 'Morse Code Finished',
                'transform': '""'}],
            'description': 'This channel is triggered if the playback of the morse code set by the morseCode action is finished.'
        },
    ],
    'channel_types': [
    ],
    'actions': ['Beep', 'Morse Code']
}
