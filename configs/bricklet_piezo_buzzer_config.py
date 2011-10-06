# -*- coding: utf-8 -*-

# Piezo Buzzer Bricklet communication config

com = {
    'author': 'Olaf Lüke (olaf@tinkerforge.com)',
    'version': [1, 0, 0],
    'type': 'Bricklet',
    'name': ('PiezoBuzzer', 'piezo_buzzer'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for controlling a piezo buzzer',
    'packets': []
}

com['packets'].append({
'type': 'method', 
'name': ('Beep', 'beep'), 
'elements': [('duration', 'uint32', 1, 'in')],
'doc': ['bm', {
'en':
"""
Beeps with the duration in ms. For example: If you set a value of 1000,
the piezo buzzer will beep for one second.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('MorseCode', 'morse_code'), 
'elements': [('morse', 'string', 60, 'in')],
'doc': ['bm', {
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
"""
}]
})

com['packets'].append({
'type': 'signal', 
'name': ('BeepFinished', 'beep_finished'), 
'elements': [],
'doc': ['c', {
'en':
"""
This callback is called if a beep set by :func:`Beep` is finished
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'signal', 
'name': ('MorseCodeFinished', 'morse_code_finished'), 
'elements': [],
'doc': ['c', {
'en':
"""
This callback is called if the playback of the morse code set by 
:func:`MorseCode` is finished.
""",
'de':
"""
"""
}]
})
