# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Piezo Speaker Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 242,
    'name': ('PiezoSpeaker', 'piezo_speaker', 'Piezo Speaker', 'Piezo Speaker Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Creates beep with configurable frequency',
        'de': 'Erzeugt Piepton mit konfigurierbarer Frequenz'
    },
    'released': True,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': ('Beep', 'beep'), 
'elements': [('duration', 'uint32', 1, 'in', ('BeepDuration', 'beep_duration', [('Off', 'off', 0),
                                                                                ('Infinite', 'infinite', 4294967295)])),
             ('frequency', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Beeps with the given frequency for the duration in ms. For example: 
If you set a duration of 1000, with a frequency value of 2000
the piezo buzzer will beep for one second with a frequency of
approximately 2 kHz.

.. versionchanged:: 2.0.2~(Plugin)
   A duration of 0 stops the current beep if any, the frequency parameter is
   ignored. A duration of 4294967295 results in an infinite beep.

The *frequency* parameter can be set between 585 and 7100.

The Piezo Speaker Bricklet can only approximate the frequency, it will play
the best possible match by applying the calibration (see :func:`Calibrate`).
""",
'de':
"""
Erzeugt einen Piepton mit der gegebenen Frequenz für die angegebene Dauer in ms. 
Beispiel: Wenn *duration* auf 1000 und *frequency* auf 2000 gesetzt wird, 
erzeugt der Piezosummer einen Piepton für eine Sekunde mit einer Frequenz 
von ca. 2 kHz.

.. versionchanged:: 2.0.2~(Plugin)
   Eine *durarion* von 0 stoppt den aktuellen Piepton, das *frequency* Parameter
   wird ignoriert. Eine *durarion* von 4294967295 führt zu einem unendlich
   langen Piepton.

Das *frequency* Parameter kann Werte von 585 bis 7100 annehmen.

Das Piezo Speaker Bricklet kann die angegebenen Frequenzen nur approximieren,
es wählt die bestmögliche Zuordnung anhand der Kalibrierung 
(siehe :func:`Calibrate`).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('MorseCode', 'morse_code'), 
'elements': [('morse', 'string', 60, 'in'),
             ('frequency', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets morse code that will be played by the piezo buzzer. The morse code
is given as a string consisting of "." (dot), "-" (minus) and " " (space)
for *dits*, *dahs* and *pauses*. Every other character is ignored.
The second parameter is the frequency (see :func:`Beep`).

For example: If you set the string "...---...", the piezo buzzer will beep
nine times with the durations "short short short long long long short 
short short".

The maximum string size is 60.
""",
'de':
"""
Setzt Morsecode welcher vom Piezosummer abgespielt wird. Der Morsecode wird
als Zeichenkette, mit den Zeichen "." (Punkt), "-" (Minus) und " " (Leerzeichen)
für *kurzes Signale*, *langes Signale* und *Pausen*. Alle anderen Zeichen
werden ignoriert.
Der zweite Parameter ist die Frequenz (siehe :func:`Beep`).

Beispiel: Wenn die Zeichenkette "...---..." gesetzt wird, gibt der Piezosummer neun
Pieptöne aus mit den Dauern "kurz kurz kurz lang lang lang kurz kurz kurz".

Die maximale Zeichenkettenlänge ist 60.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('Calibrate', 'calibrate'), 
'elements': [('calibration', 'bool', 1, 'out')],
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
'name': ('BeepFinished', 'beep_finished'), 
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered if a beep set by :func:`Beep` is finished
""",
'de':
"""
Dieser Callback wird ausgelöst wenn ein Piepton, wie von :func:`Beep` gesetzt,
beendet wurde.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('MorseCodeFinished', 'morse_code_finished'), 
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered if the playback of the morse code set by
:func:`MorseCode` is finished.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn die Wiedergabe des Morsecodes, wie von
:func:`MorseCode` gesetzt, beendet wurde.
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
