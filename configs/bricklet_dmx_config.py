# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# DMX Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 285,
    'name': 'DMX',
    'display_name': 'DMX',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'DMX Master and Slave',
        'de': 'DMX Master und Slave'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Set DMX Mode',
'elements': [('DMX Mode', 'uint8', 1, 'in', ('DMX Mode', [('Master', 0),
                                                          ('Slave', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the DMX mode to either Slave or Master.

Calling this function sets frame number to 0.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get DMX Mode',
'elements': [('DMX Mode', 'uint8', 1, 'out', ('DMX Mode', [('Master', 0),
                                                           ('Slave', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the DMX mode, as set by func:`Get DMX Mode`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Write Frame Low Level',
'elements': [('Frame Length', 'uint16', 1, 'in'),
             ('Frame Chunk Offset', 'uint16', 1, 'in'),
             ('Frame Chunk Data', 'uint8', 60, 'in')],
'high_level': {'stream_in': {'name': 'Frame'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes a DMX frame. The maximum frame size is 512 byte. Each byte represents one channel.

The next frame can be written after the :cb:`Frame Started` callback was called. The frame
is double buffered, so a new frame can be written as soon as the writing of the prior frame
starts.

The data will be transfered when the next frame duration ends, see :func:`Set Frame Duration`.

Generic approach:

* Set the frame duration to a value that represents the number of frames per second you want to achieve.
* Set channels for one frame.
* Wait for the :cb:`Frame Started` callback.
* Set channels for next frame.
* Wait for the :cb:`Frame Started` callback.
* and so on.

This approach ensures that you can set new DMX data with a fixed frame rate.

This function can only be called in Master Mode.
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Read Frame Low Level',
'elements': [('Frame Length', 'uint16', 1, 'out'),
             ('Frame Chunk Offset', 'uint16', 1, 'out'),
             ('Frame Chunk Data', 'uint8', 56, 'out'),
             ('Frame Number', 'uint32', 1, 'out')],
'high_level': {'stream_out': {'name': 'Frame'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the last frame that was written by the DMX Master. The size of the array 
is equivalent to the number of channels in the frame. Each byte represents one channel.

The next frame is available after the :cb:`Frame Available` callback was called.

Generic approach:

* Call :func:`Read Frame` to get first frame.
* Wait for the :cb:`Frame Available` callback.
* Call :func:`Read Frame` to get second frame.
* Wait for the :cb:`Frame Available` callback.
* and so on.

Instead of polling this function you can also use the :cb:`Frame` callback.
You can enable it with :func:`Set Frame Callback Config`.

The frame number starts at 0 and it is increased by one with each received frame.

This function can only be called in Slave Mode.
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set Frame Duration',
'elements': [('Frame Duration', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the duration of a frame in ms. 

Example: If you want to achieve 20 frames per second, you should
set the frame duration to 50ms (50ms * 20 = 1 second).

If you always want to send a frame as fast as possible you can set
this value to 0.

This setting is only used in Master Mode.

Default value: 100ms (10 frames per second).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Frame Duration',
'elements': [('Frame Duration', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the frame duration as set by :func:`Set Frame Duration`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Frame Error Count',
'elements': [('Overrun Error Count', 'uint32', 1, 'out'),
             ('Framing Error Count', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the current number of overrun and framing errors.
""",
'de':
"""
Gibt die aktuelle Anzahl an Overrun und Framing Fehlern zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Communication LED Config',
'elements': [('Config', 'uint8', 1, 'in', ('Communication LED Config', [('Off', 0),
                                                                        ('On', 1),
                                                                        ('Show Heartbeat', 2),
                                                                        ('Show Communication', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the communication LED configuration. By default the LED shows
communication traffic, it flickers once for every 10 received data packets.

You can also turn the LED permanently on/off or show a heartbeat.

If the Bricklet is in bootloader mode, the LED is off.
""",
'de':
"""
Setzt die Konfiguration der Kommunikations-LED. Standardmäßig zeigt
die LED die Kommunikationsdatenmenge an. Sie blinkt einmal auf pro 10 empfangenen
Datenpaketen zwischen Brick und Bricklet.

Die LED kann auch permanaent an/aus gestellt werden oder einen Herzschlag anzeigen.

Wenn das Bricklet sich im Bootlodermodus befindet ist die LED aus.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Communication LED Config',
'elements': [('Config', 'uint8', 1, 'out', ('Communication LED Config', [('Off', 0),
                                                                         ('On', 1),
                                                                         ('Show Heartbeat', 2),
                                                                         ('Show Communication', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Communication LED Config`
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Communication LED Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Error LED Config',
'elements': [('Config', 'uint8', 1, 'in', ('Error LED Config', [('Off', 0),
                                                                ('On', 1),
                                                                ('Show Heartbeat', 2),
                                                                ('Show Error', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the error LED configuration.

By default the error LED turns on if there is any error (see :cb:`Frame Error Count`
callback). If you call this function with the Show-Error option again, the LED
will turn off until the next error occurs.

You can also turn the LED permanently on/off or show a heartbeat.

If the Bricklet is in bootloader mode, the LED is off.
""",
'de':
"""
Setzt die Konfiguration der Error-LED.

Standardmäßig geht die LED an, wenn ein Error auftritt (siehe :cb:`Frame Error Count`
Callback). Wenn diese Funktion danach nochmal mit der Show-Error-Option
aufgerufen wird, geht die LED wieder aus bis der nächste Error auftritt.

Die LED kann auch permanaent an/aus gestellt werden oder einen Herzschlag
anzeigen.

Wenn das Bricklet sich im Bootlodermodus befindet ist die LED aus.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Error LED Config',
'elements': [('Config', 'uint8', 1, 'out', ('Error LED Config', [('Off', 0),
                                                                 ('On', 1),
                                                                 ('Show Heartbeat', 2),
                                                                 ('Show Error', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Error LED Config`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Error LED Config` gesetzt.
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set Frame Callback Config',
'elements': [('Frame Started Callback Enabled', 'bool', 1, 'in'),
             ('Frame Available Callback Enabled', 'bool', 1, 'in'),
             ('Frame Callback Enabled', 'bool', 1, 'in'),
             ('Frame Error Count Callback Enabled', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Enables/Disables the different callbacks. By default the
:cb:`Frame Started` and :cb:`Frame Available` callbacks are enabled while
the :cb:`Frame` and :cb:`Frame Error Count` callbacks are disabled.

If you want to use the :cb:`Frame` callback you can enable it and disable
the cb:`Frame Available` callback at the same time. It becomes redundent in
this case.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Frame Callback Config',
'elements': [('Frame Started Callback Enabled', 'bool', 1, 'out'),
             ('Frame Available Callback Enabled', 'bool', 1, 'out'),
             ('Frame Callback Enabled', 'bool', 1, 'out'),
             ('Frame Error Count Callback Enabled', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the frame callback config as set by :func:`Set Frame Callback Config`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Frame Started',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered as soon as a new frame write is started.
You should send the data for the next frame directly after this callback
was triggered.

For an explanation of the general approach see :func:`Write Frame`.

This callback can be enabled via :func:`Set Frame Callback Config`.

This callback can only be triggered in Master Mode.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Frame Available',
'elements': [('Frame Number', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered in slave mode when a new frame was written by the DMX Master
and it can be read out. You have to read the frame before the Master has written
the next frame, see :func:`Read Frame` for more details.

The parameter is the frame number, it is increased by one with each received frame.

This callback can be enabled via :func:`Set Frame Callback Config`.

This callback can only be triggered in Slave Mode.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Frame Low Level',
'elements': [('Frame Length', 'uint16', 1, 'out'),
             ('Frame Chunk Offset', 'uint16', 1, 'out'),
             ('Frame Chunk Data', 'uint8', 56, 'out'),
             ('Frame Number', 'uint32', 1, 'out')],
'high_level': {'stream_out': {'name': 'Frame'}},
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called as soon as a new frame is available
(written by the DMX Master). 

The size of the array is equivalent to the number of channels in 
the frame. Each byte represents one channel.

This callback can be enabled via :func:`Set Frame Callback Config`.

This callback can only be triggered in Slave Mode.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Frame Error Count',
'elements': [('Overrun Error Count', 'uint32', 1, 'out'),
             ('Framing Error Count', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called if a new error occurs. It returns
the current overrun and framing error count.
""",
'de':
"""
Dieser Callback wird aufgerufen wenn ein neuer Fehler auftritt.
Er gibt die Anzahl der aufgetreten Overrun and Framing Fehler zurück.
"""
}]
})
