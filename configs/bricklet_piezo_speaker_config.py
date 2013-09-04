# -*- coding: utf-8 -*-

# Piezo Speaker Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 242,
    'name': ('PiezoSpeaker', 'piezo_speaker', 'Piezo Speaker'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for controlling a piezo buzzer with configurable frequencies',
    'released': False,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('Beep', 'beep'), 
'elements': [('duration', 'uint32', 1, 'in'),
             ('frequency', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Beeps with the given frequency for the duration in ms. For example: 
If you set a duration of 1000, with a frequency value of 2000
the piezo buzzer will beep for one second with a frequency of
approximately 2 kHz.

*frequency* can be set between 585 and 7100.

The Piezo Speaker Bricklet can only approximate the frequency, it will play
the best possible match by applying the calibration (see :func:`Calibrate`).
""",
'de':
"""
Erzeugt einen Piepton mit der gegebenen Frequenz für eine Dauer in ms. 
Beispiel: Wenn *duration* auf 1000 und *frequency* auf 2000 gesetzt wird, 
erzeugt der Piezosummer einen Piepton für eine Sekunde mit einer Frequenz 
von ca. 2 kHz.

*frequency* kann die Werte 585 bis 7100 annehmen.

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
Der zweite Parameter ist die Frequenz (see :func:`Beep`).

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
The Pizeo Speaker Bricklet can play 512 different tones. This function
plays each tone and measures the exact frequency back. The result is a
mapping between setting value and frequency. This mapping is stored
in the EEPROM and loaded on startup.

The Bricklet should come calibrated, you only need to call this
function (once) every time you reflash the Bricklet plugin.
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
