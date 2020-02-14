# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# RS232 Bricklet 2.0 communication config

from openhab_common import *

com = {
    'author': 'Ishraq Ibne Ashraf <ishraq@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'category': 'Bricklet',
    'device_identifier': 2108,
    'name': 'RS232 V2',
    'display_name': 'RS232 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Communicates with RS232 devices',
        'de': 'Kommuniziert mit RS232 Geräten'
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

com['constant_groups'].append({
'name': 'Parity',
'type': 'uint8',
'constants': [('None', 0),
              ('Odd', 1),
              ('Even', 2)]
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
'name': 'Flowcontrol',
'type': 'uint8',
'constants': [('Off', 0),
              ('Software', 1),
              ('Hardware', 2)]
})

com['packets'].append({
'type': 'function',
'name': 'Write Low Level',
'elements': [('Message Length', 'uint16', 1, 'in', {}),
             ('Message Chunk Offset', 'uint16', 1, 'in', {}),
             ('Message Chunk Data', 'char', 60, 'in', {}),
             ('Message Chunk Written', 'uint8', 1, 'out', {})],
'high_level': {'stream_in': {'name': 'Message', 'short_write': True}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes characters to the RS232 interface. The characters can be binary data,
ASCII or similar is not necessary.

The return value is the number of characters that were written.

See :func:`Set Configuration` for configuration possibilities
regarding baud rate, parity and so on.
""",
'de':
"""
Schreibt Zeichen auf die RS232-Schnittstelle. Die Zeichen können Binärdaten
sein, ASCII o.ä. ist nicht notwendig.

Der Rückgabewert ist die Anzahl der Zeichen die geschrieben wurden.

Siehe :func:`Set Configuration` für Konfigurationsmöglichkeiten
bezüglich Baudrate, Parität usw.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Read Low Level',
'elements': [('Length', 'uint16', 1, 'in', {}),
             ('Message Length', 'uint16', 1, 'out', {}),
             ('Message Chunk Offset', 'uint16', 1, 'out', {}),
             ('Message Chunk Data', 'char', 60, 'out', {})],
'high_level': {'stream_out': {'name': 'Message'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns up to *length* characters from receive buffer.

Instead of polling with this function, you can also use
callbacks. But note that this function will return available
data only when the read callback is disabled.
See :func:`Enable Read Callback` and :cb:`Read` callback.
""",
'de':
"""
Gibt bis zu *length* Zeichen aus dem Empfangsbuffer zurück.

Anstatt mit dieser Funktion zu pollen, ist es auch möglich
Callbacks zu nutzen. Diese Funktion gibt nur Daten zurück wenn
der Read-Callback nicht aktiv ist.
Siehe :func:`Enable Read Callback` und :cb:`Read` Callback.
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
Enables the :cb:`Read` callback.

By default the callback is disabled.
""",
'de':
"""
Aktiviert den :cb:`Read` Callback.

Im Startzustand ist der Callback deaktiviert.
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

Im Startzustand ist der Callback deaktiviert.
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
'elements': [('Baudrate', 'uint32', 1, 'in', {'unit': 'Baud', 'range': (100, 2000000), 'default': 115200}),
             ('Parity', 'uint8', 1, 'in', {'constant_group': 'Parity', 'default': 0}),
             ('Stopbits', 'uint8', 1, 'in', {'constant_group': 'Stopbits', 'default': 1}),
             ('Wordlength', 'uint8', 1, 'in', {'constant_group': 'Wordlength', 'default': 8}),
             ('Flowcontrol', 'uint8', 1, 'in', {'constant_group': 'Flowcontrol', 'default': 0})],

'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the configuration for the RS232 communication.
""",
'de':
"""
Setzt die Konfiguration für die RS232-Kommunikation.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Baudrate', 'uint32', 1, 'out', {'unit': 'Baud', 'range': (100, 2000000), 'default': 115200}),
             ('Parity', 'uint8', 1, 'out', {'constant_group': 'Parity', 'default': 0}),
             ('Stopbits', 'uint8', 1, 'out', {'constant_group': 'Stopbits', 'default': 1}),
             ('Wordlength', 'uint8', 1, 'out', {'constant_group': 'Wordlength', 'default': 8}),
             ('Flowcontrol', 'uint8', 1, 'out', {'constant_group': 'Flowcontrol', 'default': 0})],
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
'type': 'function',
'name': 'Set Buffer Config',
'elements': [('Send Buffer Size', 'uint16', 1, 'in', {'unit': 'Byte', 'range': (1024, 9216), 'default': 5120}),
             ('Receive Buffer Size', 'uint16', 1, 'in', {'unit': 'Byte', 'range': (1024, 9216), 'default': 5120})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the send and receive buffer size in byte. In total the buffers have to be
10240 byte (10KiB) in size, the minimum buffer size is 1024 byte (1KiB) for each.

The current buffer content is lost if this function is called.

The send buffer holds data that is given by :func:`Write` and
can not be written yet. The receive buffer holds data that is
received through RS232 but could not yet be send to the
user, either by :func:`Read` or through :cb:`Read` callback.
""",
'de':
"""
Setzt die Größe des Sende- und Empfangsbuffers. In Summe müssen
die Buffer eine Größe von 10240 Byte (10KiB) haben, die Minimalgröße
ist 1024 Byte (1KiB) für beide.

Der aktuelle Bufferinhalt geht bei einem Aufruf dieser Funktion verloren.

Der Sendebuffer hält die Daten welche über :func:`Write` übergeben und noch
nicht geschrieben werden konnten. Der Empfangsbuffer hält Daten welche
über RS232 empfangen wurden aber noch nicht über :func:`Read` oder
:cb:`Read` Callback an ein Nutzerprogramm übertragen werden konnten.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Buffer Config',
'elements': [('Send Buffer Size', 'uint16', 1, 'out', {'unit': 'Byte', 'range': (1024, 9216), 'default': 5120}),
             ('Receive Buffer Size', 'uint16', 1, 'out', {'unit': 'Byte', 'range': (1024, 9216), 'default': 5120})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the buffer configuration as set by :func:`Set Buffer Config`.
""",
'de':
"""
Gibt die Buffer-Konfiguration zurück, wie von :func:`Set Buffer Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Buffer Status',
'elements': [('Send Buffer Used', 'uint16', 1, 'out', {'unit': 'Byte', 'range': (0, 9216)}),
             ('Receive Buffer Used', 'uint16', 1, 'out', {'unit': 'Byte', 'range': (0, 9216)})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the currently used bytes for the send and received buffer.

See :func:`Set Buffer Config` for buffer size configuration.
""",
'de':
"""
Gibt die aktuell genutzten Bytes des Sende- und Empfangsbuffers zurück.

Siehe :func:`Set Buffer Config` zur Konfiguration der Buffergrößen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Error Count',
'elements': [('Error Count Overrun', 'uint32', 1, 'out', {}),
             ('Error Count Parity', 'uint32', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the current number of overrun and parity errors.
""",
'de':
"""
Gibt die aktuelle Anzahl an Overrun und Parity Fehlern zurück.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Read Low Level',
'elements': [('Message Length', 'uint16', 1, 'out', {}),
             ('Message Chunk Offset', 'uint16', 1, 'out', {}),
             ('Message Chunk Data', 'char', 60, 'out', {})],
'high_level': {'stream_out': {'name': 'Message'}},
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called if new data is available.

To enable this callback, use :func:`Enable Read Callback`.
""",
'de':
"""
Dieser Callback wird aufgerufen wenn neue Daten zur Verfügung stehen.

Dieser Callback kann durch :func:`Enable Read Callback` aktiviert werden.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Error Count',
'elements': [('Error Count Overrun', 'uint32', 1, 'out', {}),
             ('Error Count Parity', 'uint32', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called if a new error occurs. It returns
the current overrun and parity error count.
""",
'de':
"""
Dieser Callback wird aufgerufen wenn ein neuer Fehler auftritt.
Er gibt die Anzahl der aufgetreten Overrun und Parity Fehler zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Frame Readable Callback Configuration',
'elements': [('Frame Size', 'uint16', 1, 'in', {'unit': 'Byte', 'range': (0, 9216)})],
'since_firmware': [2, 0, 3],
'doc': ['ccf', {
'en':
"""
Configures the :cb:`Frame Readable` callback. The frame size is the number of bytes, that have to be readable to trigger the callback.
A frame size of 0 disables the callback.

By default the callback is disabled.
""",
'de':
"""
Konfiguriert den :cb:`Frame Readable` Callback. Die Frame Size ist die Anzahl an Bytes, die lesbar sein müssen, damit der Callback auslöst.
Eine Frame Size von 0 deaktiviert den Callback.

Im Startzustand ist der Callback deaktiviert.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Frame Readable',
'elements': [('Frame Count', 'uint16', 1, 'out', {})],
'since_firmware': [2, 0, 3],
'doc': ['c', {
'en':
"""
This callback is called if at least one frame of data is readable. The frame size is configured with :func:`Set Frame Readable Callback Configuration`.
The frame count parameter is the number of frames that can be read.
This callback is triggered only once until :func:`Read` is called. This means, that if you have configured a frame size of X bytes,
you can read exactly X bytes using the :func:`Read` function, every time the callback triggers without checking the frame count :word:`parameter`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn mindestens ein neuer Frame an Daten verfügbar sind. Die Größe eines Frames kann mit :func:`Set Frame Readable Callback Configuration` konfiguriert werden.
Frame Count ist die Anzahl an Frames, die zum Lesen bereitstehen.
Der Callback wird nur einmal pro :func:`Read` Aufruf ausgelöst. Das heißt, dass wenn eine Framegröße von X Bytes konfiguriert wird, jedes Mal
wenn das Callback ausgelöst wird, X Bytes mit der :func:`Read`-Funktion gelesen werden können, ohne dass der Frame Count-:word:`parameter` geprüft werden muss.
"""
}]
})

com['examples'].append({
'name': 'Loopback',
'description': 'For this example connect the RX1 and TX pin to receive the send message',
'functions': [('callback', ('Read', 'read'), [(('Message', 'Message'), 'char', -65535, None, None, None)], None, None), # FIXME: wrong message type
              ('setter', 'Enable Read Callback', [], 'Enable read callback', None),
              ('setter', 'Write', [('char', ['t', 'e', 's', 't'])], 'Write "test" string', None)],
'incomplete': True # because of special logic and callback with array parameter, write function written output parameter and string split logic
})

com['openhab'] = {
    'imports': oh_generic_channel_imports() + oh_generic_trigger_channel_imports() + ['org.eclipse.smarthome.core.library.types.DecimalType'],
    'param_groups': oh_generic_channel_param_groups(),
    'params': [{
            'packet': 'Set Configuration',
            'element': 'Baudrate',

            'name': 'Baud Rate',
            'type': 'integer',
            'min': 100,
            'max': 2000000,
            'default': 115200,

            'label': 'Baud Rate',
            'description': 'The baud rate to send/receive with.',
        }, {
            'packet': 'Set Configuration',
            'element': 'Parity',

            'name': 'Parity',
            'type': 'integer',
            'options': [('None', 0),
                        ('Odd', 1),
                        ('Even', 2)],
            'limitToOptions': 'true',
            'default': 0,

            'label': 'Parity',
            'description': 'The parity mode to use. See <a href=\\\"https://en.wikipedia.org/wiki/Serial_port#Parity\\\">here</a>'
        }, {
            'packet': 'Set Configuration',
            'element': 'Stopbits',

            'name': 'Stop Bits',
            'type': 'integer',
            'options': [('1', 1),
                        ('2', 2)],
            'limitToOptions': 'true',
            'default': 1,

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
            'limitToOptions': 'true',
            'default': 8,

            'label': 'Word Length',
            'description': 'The length of a serial word. Typically one byte.'
        }, {
            'packet': 'Set Configuration',
            'element': 'Flowcontrol',

            'name': 'Flow Control',
            'type': 'integer',
            'options': [('Off', 0),
                        ('Software', 1),
                        ('Hardware', 2)],
            'limitToOptions': 'true',
            'default': 0,

            'label': 'Flow Control',
            'description': 'The flow control mechanism to use. Software uses control characters in-band. Hardware uses the RTS and CTS lines.'
        }, {
            'packet': 'Set Buffer Config',
            'element': 'Send Buffer Size',

            'name': 'Send Buffer Size',
            'type': 'integer',
            'min': 1024,
            'max': 9216,
            'default': 5120,

            'label': 'Send Buffer Size',
            'description': 'The send buffer size in bytes. In total the send and receive buffers are 10240 byte (10 KiB) in size. The minimum buffer size is 1024 byte (1 KiB) each. The binding will configure the read buffer size accordingly. The send buffer holds data that is given by the user and can not be written to RS232 yet. The receive buffer holds data that is received through RS232 but could not yet be send to the user.'
        }, {
            'packet': 'Set Frame Readable Callback Configuration',
            'element': 'Frame Size',

            'name': 'Frame Size',
            'type': 'integer',
            'min': 0,
            'max': 9216,
            'default': 1,

            'label': 'Frame Size',
            'description': 'The size of receivable data frames in bytes. Set this to something other than 1, if you want to receive data with a fix frame size. The frame readable channel will trigger every time a frame of this size is ready to be read, but will wait until this frame is read before triggering again. This means, you can use this channel as a trigger in a rule, that will read exactly one frame.'
        }],

    'init_code': """this.setConfiguration(cfg.baudRate, cfg.parity, cfg.stopBits, cfg.wordLength, cfg.flowControl);
    this.setBufferConfig(cfg.sendBufferSize, 10240 - cfg.sendBufferSize);
    this.setFrameReadableCallbackConfiguration(cfg.frameSize);""",

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
            'id': 'Overrun Error Count',
            'label': 'Overrun Error Count',
            'type': 'Overrun Error Count',

            'getters': [{
                'packet': 'Get Error Count',
                'transform': 'new DecimalType(value.errorCountOverrun)'
            }],

            'callbacks': [{
                'packet': 'Error Count',
                'transform': 'new DecimalType(errorCountOverrun)'}],
        }, {
            'id': 'Parity Error Count',
            'label': 'Parity Error Count',
            'type': 'Parity Error Count',

            'getters': [{
                'packet': 'Get Error Count',
                'transform': 'new DecimalType(value.errorCountParity)'
            }],

            'callbacks': [{
                'packet': 'Error Count',
                'transform': 'new DecimalType(errorCountParity)'}],
        }, {
            'id': 'Send Buffer Used',
            'label': 'Send Buffer Used',
            'type': 'Send Buffer Used',

            'getters': [{
                'packet': 'Get Buffer Status',
                'transform': 'new QuantityType(value.sendBufferUsed, SmartHomeUnits.BYTE)'
            }],
        }, {
            'id': 'Receive Buffer Used',
            'label': 'Receive Buffer Used',
            'type': 'Receive Buffer Used',

            'getters': [{
                'packet': 'Get Buffer Status',
                'transform': 'new QuantityType(value.receiveBufferUsed, SmartHomeUnits.BYTE)'
            }],
        }],
    'channel_types': [
        oh_generic_channel_type('Overrun Error Count', 'Number', 'Overrun Error Count',
            update_style=None,
            description='The current number of overrun errors',
            read_only=True),
        oh_generic_channel_type('Parity Error Count', 'Number', 'Framing Error Count',
            update_style=None,
            description='The current number of parity errors',
            read_only=True),
        oh_generic_channel_type('Send Buffer Used', 'Number:DataAmount', 'Send Buffer Used',
            update_style=None,
            description='The number of bytes currently in the send buffer',
            read_only=True),
        oh_generic_channel_type('Receive Buffer Used', 'Number:DataAmount', 'Receive Buffer Used',
            update_style=None,
            description='The number of bytes currently in the receive buffer',
            read_only=True),
    ],
    'actions': ['Write', 'Read', 'Get Configuration', 'Get Buffer Config', 'Get Buffer Status', 'Get Error Count']
}

