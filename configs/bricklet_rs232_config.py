# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# RS232 Bricklet communication config

from openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 3],
    'category': 'Bricklet',
    'device_identifier': 254,
    'name': 'RS232',
    'display_name': 'RS232',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Communicates with RS232 devices',
        'de': 'Kommuniziert mit RS232 Geräten'
    },
    'released': True,
    'documented': True,
    'discontinued': False, # selling remaining stock, replaced by RS232 Bricklet 2.0
    'features': [
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append({
'name': 'Baudrate',
'type': 'uint8',
'constants': [('300', 0),
              ('600', 1),
              ('1200', 2),
              ('2400', 3),
              ('4800', 4),
              ('9600', 5),
              ('14400', 6),
              ('19200', 7),
              ('28800', 8),
              ('38400', 9),
              ('57600', 10),
              ('115200', 11),
              ('230400', 12)]
})

com['constant_groups'].append({
'name': 'Parity',
'type': 'uint8',
'constants': [('None', 0),
              ('Odd', 1),
              ('Even', 2),
              ('Forced Parity 1', 3),
              ('Forced Parity 0', 4)]
})

com['constant_groups'].append({
'name': 'Stopbits',
'type': 'uint8',
'constants': [('1', 1),
              ('2', 2)]
})

com['constant_groups'].append({
'name': 'Wordlength',
'type': 'uint8',
'constants': [('5', 5),
              ('6', 6),
              ('7', 7),
              ('8', 8)]
})

com['constant_groups'].append({
'name': 'Hardware Flowcontrol',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1)]
})

com['constant_groups'].append({
'name': 'Software Flowcontrol',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1)]
})

com['constant_groups'].append({
'name': 'Error',
'type': 'uint8',
'constants': [('Overrun', 1),
              ('Parity', 2),
              ('Framing', 4)]
})

com['packets'].append({
'type': 'function',
'name': 'Write',
'elements': [('Message', 'char', 60, 'in', {}),
             ('Length', 'uint8', 1, 'in', {'range': (0, 60)}),
             ('Written', 'uint8', 1, 'out', {'range': (0, 60)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes a string of up to 60 characters to the RS232 interface. The string
can be binary data, ASCII or similar is not necessary.

The length of the string has to be given as an additional parameter.

The return value is the number of bytes that could be written.

See :func:`Set Configuration` for configuration possibilities
regarding baudrate, parity and so on.
""",
'de':
"""
Schreibt einen String aus bis zu 60 Zeichen auf die RS232-Schnittstelle. Der
String kann aus Binärdaten bestehen, ASCII o.ä. ist nicht notwendig.

Die Länge des Strings muss als ein zusätzlicher Parameter angegeben werden.

Der Rückgabewert ist die Anzahl der Zeichen die geschrieben werden konnten.

Siehe :func:`Set Configuration` für Konfigurationsmöglichkeiten
bezüglich Baudrate, Parität usw.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Read',
'elements': [('Message', 'char', 60, 'out', {}),
             ('Length', 'uint8', 1, 'out', {'range': (0, 60)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the currently buffered message. The maximum length
of message is 60. If the length is given as 0, there was no
new data available.

Instead of polling with this function, you can also use
callbacks. See :func:`Enable Read Callback` and :cb:`Read` callback.
""",
'de':
"""
Gibt die aktuell gespeicherte Nachricht zurück. Die maximale Länge
beträgt 60. Wenn die Länge als 0 gegeben wird, waren keine
neuen Daten verfügbar.

Anstatt mit dieser Funktion zu pollen, ist es auch möglich
Callbacks zu nutzen. Siehe :func:`Enable Read Callback` und
:cb:`Read` Callback.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Enable Read Callback',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Enables the :cb:`Read` callback. This will disable the :cb:`Frame Readable` callback.

By default the callback is disabled.
""",
'de':
"""
Aktiviert den :cb:`Read` Callback. Dies deaktiviert den :cb:`Frame Readable` Callback.

Im Startzustand ist der Callback deaktiviert
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Disable Read Callback',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Disables the :cb:`Read` callback.

By default the callback is disabled.
""",
'de':
"""
Deaktiviert den :cb:`Read` Callback.

Im Startzustand ist der Callback deaktiviert
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is Read Callback Enabled',
'elements': [('Enabled', 'bool', 1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns *true* if the :cb:`Read` callback is enabled,
*false* otherwise.
""",
'de':
"""
Gibt *true* zurück falls :cb:`Read` Callback aktiviert ist,
*false* sonst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('Baudrate', 'uint8', 1, 'in', {'constant_group': 'Baudrate', 'default': 11}),
             ('Parity', 'uint8', 1, 'in', {'constant_group': 'Parity', 'default': 0}),
             ('Stopbits', 'uint8', 1, 'in', {'constant_group': 'Stopbits', 'default': 1}),
             ('Wordlength', 'uint8', 1, 'in', {'constant_group': 'Wordlength', 'default': 8}),
             ('Hardware Flowcontrol', 'uint8', 1, 'in', {'constant_group': 'Hardware Flowcontrol', 'default': 0}),
             ('Software Flowcontrol', 'uint8', 1, 'in', {'constant_group': 'Software Flowcontrol', 'default': 0})],

'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the configuration for the RS232 communication.

Hard-/Software flow control can either be on or off but not both simultaneously on.
""",
'de':
"""
Setzt die Konfiguration für die RS232-Kommunikation.

Hard-/Software Flow Control kann entweder an oder aus sein aber nicht beides gleichzeitig an.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Baudrate', 'uint8', 1, 'out', {'constant_group': 'Baudrate', 'default': 11}),
             ('Parity', 'uint8', 1, 'out', {'constant_group': 'Parity', 'default': 0}),
             ('Stopbits', 'uint8', 1, 'out', {'constant_group': 'Stopbits', 'default': 1}),
             ('Wordlength', 'uint8', 1, 'out', {'constant_group': 'Wordlength', 'default': 8}),
             ('Hardware Flowcontrol', 'uint8', 1, 'out', {'constant_group': 'Hardware Flowcontrol', 'default': 0}),
             ('Software Flowcontrol', 'uint8', 1, 'out', {'constant_group': 'Software Flowcontrol', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the configuration as set by :func:`Set Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Read',
'elements': [('Message', 'char', 60, 'out', {}),
             ('Length', 'uint8', 1, 'out', {'range': (1, 60)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called if new data is available. The message has
a maximum size of 60 characters. The actual length of the message
is given in addition.

To enable this callback, use :func:`Enable Read Callback`.
""",
'de':
"""
Dieser Callback wird aufgerufen wenn neue Daten zur Verfügung stehen.
Die Nachricht hat eine Maximalgröße von 60 Zeichen. Die Länge
der Nachricht wird zusätzlich übergeben.

Dieser Callback kann durch :func:`Enable Read Callback` aktiviert werden.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Error',
'elements': [('Error', 'uint8', 1, 'out', {'constant_group': 'Error'})],
'since_firmware': [2, 0, 1],
'doc': ['c', {
'en':
"""
This callback is called if an error occurs.
Possible errors are overrun, parity or framing error.
""",
'de':
"""
Dieser Callback wird aufgerufen wenn ein Fehler auftritt.
Mögliche Fehler sind Overrun-, Parity- oder Framing-Fehler.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Break Condition',
'elements': [('Break Time', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [2, 0, 2],
'doc': ['bf', {
'en':
"""
Sets a break condition (the TX output is forced to a logic 0 state).
The parameter sets the hold-time of the break condition.
""",
'de':
"""
Setzt eine Break Condition (die TX-Ausgabe wird fest of logisch 0 gezwungen).
Der Parameter setzt die Haltezeit der Break Condition.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Frame Readable Callback Configuration',
'elements': [('Frame Size', 'uint8', 1, 'in', {'unit': 'Byte', 'range': (0, 100), 'default': 0})],
'since_firmware': [2, 0, 4],
'doc': ['ccf', {
'en':
"""
Configures the :cb:`Frame Readable` callback. The frame size is the number of bytes, that have to be readable to trigger the callback.
A frame size of 0 disables the callback. A frame size greater than 0 enables the callback and disables the :cb:`Read` callback.

By default the callback is disabled.
""",
'de':
"""
Konfiguriert den :cb:`Frame Readable` Callback. Die Frame Size ist die Anzahl an Bytes, die lesbar sein müssen, damit der Callback auslöst.
Eine Frame Size von 0 deaktiviert den Callback. Eine Frame Size größer als 0 aktiviert diesen und deaktiviert den :cb:`Read` Callback.

Im Startzustand ist der Callback deaktiviert.
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Get Frame Readable Callback Configuration',
'elements': [('Frame Size', 'uint8', 1, 'out', {'unit': 'Byte', 'range': (0, 100), 'default': 0})],
'since_firmware': [2, 0, 4],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by :func:`Set Frame Readable Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels :func:`Set Frame Readable Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Frame Readable',
'elements': [('Frame Count', 'uint8', 1, 'out', {})],
'since_firmware': [2, 0, 4],
'doc': ['c', {
'en':
"""
This callback is called if at least one frame of data is readable. The frame size is configured with :func:`Set Frame Readable Callback Configuration`.
The frame count parameter is the number of frames that can be read.
This callback is triggered only once until :func:`Read` or :func:`Read Frame` is called. This means, that if you have configured a frame size of X bytes,
you can read exactly X bytes using the :func:`Read Frame` function, every time the callback triggers without checking the frame count :word:`parameter`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn mindestens ein neuer Frame an Daten verfügbar sind. Die Größe eines Frames kann mit :func:`Set Frame Readable Callback Configuration` konfiguriert werden.
Frame Count ist die Anzahl an Frames, die zum Lesen bereitstehen.
Der Callback wird nur einmal pro :func:`Read` oder :func:`Read Frame` Aufruf ausgelöst. Das heißt, dass wenn eine Framegröße von X Bytes konfiguriert wird, jedes Mal
wenn das Callback ausgelöst wird, X Bytes mit der :func:`Read Frame`-Funktion gelesen werden können, ohne dass der Frame Count-:word:`parameter` geprüft werden muss.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Read Frame',
'elements': [('Message', 'char', 60, 'out', {}),
             ('Length', 'uint8', 1, 'out', {'range': (0, 60)})],
'since_firmware': [2, 0, 4],
'doc': ['bf', {
'en':
"""
Returns up to one frame of bytes from the read buffer.
The frame size is configured with :func:`Set Frame Readable Callback Configuration`.
If the length is given as 0, there was no
new data available.
""",
'de':
"""
Gibt bis zu einem Frame an Daten aus dem Lesebuffer zurück.
Die Größe eines Frames kann mit :func:`Set Frame Readable Callback Configuration` konfiguriert werden.
Wenn die Länge als 0 gegeben wird, waren keine
neuen Daten verfügbar.
"""
}]
})

com['examples'].append({
'name': 'Loopback',
'description': 'For this example connect the RX1 and TX pin to receive the send message',
'functions': [('callback', ('Read', 'read'), [(('Message', 'Message'), 'char', 60, None, None, None), (('Length', 'Length'), 'uint8', 1, None, None, None)], None, None), # FIXME: wrong message type
              ('setter', 'Enable Read Callback', [], 'Enable read callback', None)],
'incomplete': True # because of special logic and callback with array parameter
})

com['openhab'] = {
    'imports': oh_generic_channel_imports() + oh_generic_trigger_channel_imports() + ['org.eclipse.smarthome.core.library.types.DecimalType'],
    'param_groups': oh_generic_channel_param_groups(),
    'params': [{
            'packet': 'Set Configuration',
            'element': 'Baudrate',

            'name': 'Baud Rate',
            'type': 'integer',
            'options': [('300', 0),
                        ('600', 1),
                        ('1200', 2),
                        ('2400', 3),
                        ('4800', 4),
                        ('9600', 5),
                        ('14400', 6),
                        ('19200', 7),
                        ('28800', 8),
                        ('38400', 9),
                        ('57600', 10),
                        ('115200', 11),
                        ('230400', 12)],
            'limit_to_options': 'true',
            'label': 'Baud Rate',
            'description': 'The baud rate to send/receive with.',
        }, {
            'packet': 'Set Configuration',
            'element': 'Parity',

            'name': 'Parity',
            'type': 'integer',
            'options': [('None', 0),
                        ('Odd', 1),
                        ('Even', 2),
                        ('Forced Parity 1', 3),
                        ('Forced Parity 0', 4)],
            'limit_to_options': 'true',
            'label': 'Parity',
            'description': 'The parity mode to use. See <a href=\\\"https://en.wikipedia.org/wiki/Serial_port#Parity\\\">here</a>'
        }, {
            'packet': 'Set Configuration',
            'element': 'Stopbits',

            'name': 'Stop Bits',
            'type': 'integer',
            'options': [('1', 1),
                        ('2', 2)],
            'limit_to_options': 'true',
            'label': 'Stop Bits',
            'description': 'The number of stop bits to send/expect.'
        }, {
            'packet': 'Set Configuration',
            'element': 'Wordlength',

            'name': 'Word Length',
            'type': 'integer',
            'options': [('5', 5),
                        ('6', 6),
                        ('7', 7),
                        ('8', 8)],
            'limit_to_options': 'true',
            'label': 'Word Length',
            'description': 'The length of a serial word. Typically one byte.'
        }, {
            'virtual': True,

            'name': 'Flow Control',
            'type': 'integer',
            'options': [('Off', 0),
                        ('Software', 1),
                        ('Hardware', 2)],
            'limit_to_options': 'true',
            'default': 0,

            'label': 'Flow Control',
            'description': 'The flow control mechanism to use. Software uses control characters in-band. Hardware uses the RTS and CTS lines.'
        }, {
            'packet': 'Set Frame Readable Callback Configuration',
            'element': 'Frame Size',

            'name': 'Frame Size',
            'type': 'integer',
            'default': 1,

            'label': 'Frame Size',
            'description': 'The size of receivable data frames in bytes. Set this to something other than 1, if you want to receive data with a fix frame size. The frame readable channel will trigger every time a frame of this size is ready to be read, but will wait until this frame is read before triggering again. This means, you can use this channel as a trigger in a rule, that will read exactly one frame.'
        }],

    'init_code': """this.setConfiguration(cfg.baudRate.shortValue(), cfg.parity.shortValue(), cfg.stopBits.shortValue(), cfg.wordLength.shortValue(), (short)(cfg.flowControl == 1 ? 1 : 0), (short)(cfg.flowControl == 2 ? 1 : 0));
    this.setFrameReadableCallbackConfiguration(cfg.frameSize.shortValue());""",

    'channels': [{
            'id': 'Frame Readable',
            'label': 'Frame Readable',
            'description': "This channel is triggered in when a new frame was received and can be read out. The channel will only trigger again if the frame was read.",
            'type': 'system.trigger',
            'callbacks': [{
                'packet': 'Frame Readable',
                'transform': 'CommonTriggerEvents.PRESSED'}],

            'is_trigger_channel': True,
        }, {
            'id': 'Overrun Error',
            'label': 'Overrun Error',
            'type': 'system.trigger',
            'description': 'Triggers if an overrun error occures.',

            'callbacks': [{
                'packet': 'Error',
                'element': 'Error',
                'filter': '(error & 1 << 0) == 0',
                'transform': 'CommonTriggerEvents.PRESSED'}],

            'is_trigger_channel': True,
        }, {
            'id': 'Parity Error',
            'label': 'Parity Error',
            'type': 'system.trigger',
            'description': 'Triggers if a parity error occures.',

            'callbacks': [{
                'packet': 'Error',
                'element': 'Error',
                'filter': '(error & 1 << 1) == 0',
                'transform': 'CommonTriggerEvents.PRESSED'}],

            'is_trigger_channel': True,
        }, {
            'id': 'Framing Error',
            'label': 'Framing Error',
            'type': 'system.trigger',
            'description': 'Triggers if a framing error occures.',

            'callbacks': [{
                'packet': 'Error',
                'element': 'Error',
                'filter': '(error & 1 << 2) == 0',
                'transform': 'CommonTriggerEvents.PRESSED'}],

            'is_trigger_channel': True,
        }],
    'channel_types': [],
    'actions': ['Write', 'Read', 'Read Frame', 'Get Configuration', 'Set Break Condition']
}
