# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Piezo Speaker Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2145,
    'name': 'Piezo Speaker V2',
    'display_name': 'Piezo Speaker 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '',
        'de': ''
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'discontinued': False,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Set Beep',
'elements': [('Frequency', 'uint16', 1, 'in'),
             ('Volume', 'uint8', 1, 'in'),
             ('Duration', 'uint32', 1, 'in', ('Beep Duration', [('Off', 0),
                                                                ('Infinite', 4294967295)])),],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Beeps with the given frequency and volume for the duration in ms with. 

For example: If you set a duration of 1000, with a volume of 10 and a frequency
value of 2000 the piezo buzzer will beep with maximum loudness for one 
second with a frequency of 2 kHz.

A duration of 0 stops the current beep if any is ongoing.
A duration of 4294967295 results in an infinite beep.

The ranges are:

* Frequency: 50Hz - 15000Hz
* Volume: 0 - 10
* Duration: 0ms - 4294967295ms
""",
'de':
"""
Erzeugt einen Piepton mit der gegebenen Frequenz und Lautstärke für die 
angegebene Dauer in ms.

Beispiel: Wenn *duration* auf 1000, *volume* auf 10 und *frequency* auf 2000 gesetzt wird,
erzeugt der Piezosummer einen Piepton mit maximaler Lautstärke für eine Sekunde mit einer 
Frequenz von 2 kHz.

Eine *duration* von 0 stoppt den aktuellen Piepton. 
Eine *duration* von 4294967295 führt zu einem unendlich langen Piepton.

Die Wertebereiche sind:

* Frequenz: 50Hz - 15000Hz
* Lautstärke: 0 - 10
* Duration: 0ms - 4294967295ms
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Beep',
'elements': [('Frequency', 'uint16', 1, 'out'),
             ('Volume', 'uint8', 1, 'out'),
             ('Duration', 'uint32', 1, 'out', ('Beep Duration', [('Off', 0),
                                                                 ('Infinite', 4294967295)])),
             ('Duration Remaining', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the last beep settings as set by :func:`Set Beep`. If a beep is currently 
running it also returns the remaining duration of the beep in ms.

If the frequency or volume is updated during a beep (with :func:`Update Frequency` 
or :func:`Update Volume`) this function returns the updated value.
""",
'de':
"""
Gibt die letzten Beep-Einstellungen zurück, wie von :func:`Set Beep` gesetzt. Wenn ein
Beep aktuell läuft, wird auch die verbleibende Zeit des Beeps zurück gegeben.

Wenn die Frequenz oder Lautstärke während eines Beeps aktualisiert wird (mit
:func:`Update Frequency` oder :func:`Update Volume`), gibt diese Funktion die
aktualisierten Werte zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Alarm',
'elements': [('Start Frequency', 'uint16', 1, 'in'),
             ('End Frequency', 'uint16', 1, 'in'),
             ('Step Size', 'uint16', 1, 'in'),
             ('Step Delay', 'uint16', 1, 'in'),
             ('Volume', 'uint8', 1, 'in'),
             ('Duration', 'uint32', 1, 'in', ('Alarm Duration', [('Off', 0),
                                                                 ('Infinite', 4294967295)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Creates an alarm (a tone that goes back and force between two specified frequencies).

The following parameters can be set:

* Start Frequency: Start frequency of the alarm in Hz.
* End Frequency: End frequency of the alarm in Hz.
* Step Size: Size of one step of the sweep between the start/end frequencies in Hz.
* Step Delay: Delay between two steps (duration of time that one tone is used in a sweep) in ms.
* Duration: Duration of the alarm in ms.

A duration of 0 stops the current alarm if any is ongoing.
A duration of 4294967295 results in an infinite alarm.

Below you can find two sets of example settings that you can try out. You can use
these as a starting point to find an alarm signal that suits your application.

*Example 1: 10 seconds of loud annoying fast alarm*

* Start Frequency = 800
* End Frequency = 2000
* Step Size = 10
* Step Delay = 1
* Volume = 10
* Duration = 10000

*Example 2: 10 seconds of soft siren sound with slow build-up*

* Start Frequency = 250
* End Frequency = 750
* Step Size = 1
* Step Delay = 5
* Volume = 0
* Duration = 10000

The ranges are:

* Start Frequency: 50Hz - 14999Hz (has to be smaller than end frequency)
* End Frequency: 51Hz - 15000Hz (has to be bigger than start frequency)
* Step Size: 1Hz - 65535Hz (has to be small enough to fit into the frequency range)
* Step Delay: 1ms - 65535ms (has to be small enough to fit into the duration)
* Volume: 0-10
* Duration: 0ms - 4294967295ms
""",
'de':
"""
Startet einen Alarm (Einen Ton der zwischen zwei spezifizierten Frequenzen 
hin und her läuft).

Die folgenden Parameter können genutzt werden:

* *Start Frequency*: Startfrequenz des Alarms in Hz.
* *End Frequency*: Endfrequenz des Alarms in Hz.
* *Step Size*: Schrittgröße eines Schritts im Frequenzdurchlauf zwischen Start-/Endfrequenz in Hz.
* *Step Delay*: Zeit zwischen zwei Schritten (Dauer eines Tons im Frequenzdurchlauf) in ms.
* *Duration*: Dauer des Alarm in ms

Im weiteren gibt es zwei Beispiele zum ausprobieren. Diese Beispiele können
als Startpunkt genutzt werden um ein Alarm-Signal passend für die eigene Anwendung
zu entwerfen.

*Beispiel 1: 10 Sekunden eines lauten nervigen schnellen Alarms*

* *Start Frequency* = 800
* *End Frequency* = 2000
* *Step Size* = 10
* *Step Delay* = 1
* *Volume* = 10
* *Duration* = 10000

*Beispiel 2: 10 Sekunden eines Sirenengeräusches mit langsamen Frequenzdurchlauf*

* *Start Frequency* = 250
* *End Frequency* = 750
* *Step Size* = 1
* *Step Delay* = 5
* *Volume* = 0
* *Duration* = 10000

Die Wertebereiche sind:

* *Start Frequency*: 50Hz - 14999Hz (muss kleiner als *End Frequency* sein)
* *End Frequency*: 51Hz - 15000Hz (muss größer als *Start Frequency* sein)
* *Step Size*: 1Hz - 65535Hz (muss klein genug sein um in den Frequenzbereich zu passen)
* *Step Delay*: 1ms - 65535ms (muss kleiner als *Duration* sein)
* *Volume*: 0-10
* *Duration*: 0ms - 4294967295ms
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Alarm',
'elements': [('Start Frequency', 'uint16', 1, 'out'),
             ('End Frequency', 'uint16', 1, 'out'),
             ('Step Size', 'uint16', 1, 'out'),
             ('Step Delay', 'uint16', 1, 'out'),
             ('Volume', 'uint8', 1, 'out'),
             ('Duration', 'uint32', 1, 'out', ('Alarm Duration', [('Off', 0),
                                                                  ('Infinite', 4294967295)])),
             ('Duration Remaining', 'uint32', 1, 'out'),
             ('Current Frequency', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the last alarm settings as set by :func:`Set Alarm`. If an alarm is currently 
running it also returns the remaining duration of the alarm in ms as well as the
current frequency of the alarm in Hz.

If the volume is updated during a beep (with :func:`Update Volume`) 
this function returns the updated value.
""",
'de':
"""
Gibt die letzten Alarm-Einstellungen zurück, wie von :func:`Set Alarm` gesetzt. Wenn ein
Alarm aktuell läuft, wird auch die verbleibende Zeit des Alarms in ms sowie die aktuelle
Frequenz in Hz zurück gegeben.

Wenn die Lautstärke während eines Alarms aktualisiert wird (mit:func:`Update Volume`), 
gibt diese Funktion die aktualisierten Werte zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Update Volume',
'elements': [('Volume', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Updates the volume of an ongoing beep or alarm.
""",
'de':
"""
Aktualisiert die Lautstärke eines aktuell laufenden Beep oder Alarm.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Update Frequency',
'elements': [('Frequency', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Updates the frequency of an ongoing beep.
""",
'de':
"""
Aktualisiert die Frequenz eines aktuell laufenden Beeps.
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
This callback is triggered if a beep set by :func:`Set Beep` is finished
""",
'de':
"""
Dieser Callback wird ausgelöst wenn ein Piepton, wie von :func:`Set Beep` gesetzt,
beendet wurde.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Alarm Finished',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered if a alarm set by :func:`Set Alarm` is finished
""",
'de':
"""
Dieser Callback wird ausgelöst wenn ein Alarm, wie von :func:`Set Alarm` gesetzt,
beendet wurde.
"""
}]
})

com['examples'].append({
'name': 'Beep',
'functions': [('setter', 'Set Beep', [('uint16', 1000), ('uint8', 0), ('uint32', 2000)], 'Make 2 second beep with a frequency of 1kHz', None)]
})

com['examples'].append({
'name': 'Alarm',
'functions': [('setter', 'Set Alarm', [('uint16', 800), ('uint16', 2000), ('uint16', 10), ('uint16', 1), ('uint8', 10), ('uint32', 10000)], '10 seconds of loud annoying fast alarm', None)]
})
