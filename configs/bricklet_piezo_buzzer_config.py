# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Piezo Buzzer Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 214,
    'name': ('PiezoBuzzer', 'piezo_buzzer', 'Piezo Buzzer', 'Piezo Buzzer Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Creates 1kHz beep',
        'de': 'Erzeugt 1kHz Piepton'
    },
    'released': True,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': ('Beep', 'beep'), 
'elements': [('duration', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Beeps with the duration in ms. For example: If you set a value of 1000,
the piezo buzzer will beep for one second.
""",
'de':
"""
Erzeugt einen Piepton mit der angegebenen Dauer in ms. Beispiel: Wenn der
Wert auf 1000 gesetzt wird, erzeugt der Piezosummer einen Piepton für eine Sekunde.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('MorseCode', 'morse_code'), 
'elements': [('morse', 'string', 60, 'in')],
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

The maximum string size is 60.
""",
'de':
"""
Setzt Morsecode welcher vom Piezosummer abgespielt wird. Der Morsecode wird
als Zeichenkette, mit den Zeichen "." (Punkt), "-" (Minus) und " " (Leerzeichen)
für *kurzes Signale*, *langes Signale* und *Pausen*. Alle anderen Zeichen
werden ignoriert.

Beispiel: Wenn die Zeichenkette "...---..." gesetzt wird, gibt der Piezosummer neun
Pieptöne aus mit den Dauern "kurz kurz kurz lang lang lang kurz kurz kurz".

Die maximale Zeichenkettenlänge ist 60.
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
'functions': [('setter', 'Beep', [('uint32', 2000)], 'Make 2 second beep', None)]
})

com['examples'].append({
'name': 'Morse Code',
'functions': [('setter', 'Morse Code', [('string', '... --- ...')], 'Morse SOS', None)]
})
