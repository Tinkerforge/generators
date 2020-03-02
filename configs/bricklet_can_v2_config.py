# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# CAN Bricklet 2.0 communication config

from openhab_common import *

com = {
    'author': 'Matthias Bolte <matthias@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'category': 'Bricklet',
    'device_identifier': 2107,
    'name': 'CAN V2',
    'display_name': 'CAN 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Communicates with CAN bus devices',
        'de': 'Kommuniziert mit CAN-Bus Geräten'
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
'name': 'Frame Type',
'type': 'uint8',
'constants': [('Standard Data', 0),
              ('Standard Remote', 1),
              ('Extended Data', 2),
              ('Extended Remote', 3)]
})

com['constant_groups'].append({
'name': 'Transceiver Mode',
'type': 'uint8',
'constants': [('Normal', 0),
              ('Loopback', 1),
              ('Read Only', 2)]
})

com['constant_groups'].append({
'name': 'Filter Mode',
'type': 'uint8',
'constants': [('Accept All', 0),
              ('Match Standard Only', 1),
              ('Match Extended Only', 2),
              ('Match Standard And Extended', 3)]
})

com['constant_groups'].append({
'name': 'Transceiver State',
'type': 'uint8',
'constants': [('Active', 0),
              ('Passive', 1),
              ('Disabled', 2)]
})

com['constant_groups'].append({
'name': 'Communication LED Config',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Show Heartbeat', 2),
              ('Show Communication', 3)]
})

com['constant_groups'].append({
'name': 'Error LED Config',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Show Heartbeat', 2),
              ('Show Transceiver State', 3),
              ('Show Error', 4)]
})

com['packets'].append({
'type': 'function',
'name': 'Write Frame Low Level',
'elements': [('Frame Type', 'uint8', 1, 'in', {'constant_group': 'Frame Type'}),
             ('Identifier', 'uint32', 1, 'in', {'range': (0, 2**30-1)}),
             ('Data Length', 'uint8', 1, 'in', {'range': (0, 15)}),
             ('Data Data', 'uint8', 15, 'in', {}),
             ('Success', 'bool', 1, 'out', {})],
'high_level': {'stream_in': {'name': 'Data', 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes a data or remote frame to the write queue to be transmitted over the
CAN transceiver.

The Bricklet supports the standard 11-bit (CAN 2.0A) and the additional extended
29-bit (CAN 2.0B) identifiers. For standard frames the Bricklet uses bit 0 to 10
from the ``identifier`` parameter as standard 11-bit identifier. For extended
frames the Bricklet uses bit 0 to 28 from the ``identifier`` parameter as
extended 29-bit identifier.

The ``data`` parameter can be up to 15 bytes long. For data frames up to 8 bytes
will be used as the actual data. The length (DLC) field in the data or remote
frame will be set to the actual length of the ``data`` parameter. This allows
to transmit data and remote frames with excess length. For remote frames only
the length of the ``data`` parameter is used. The actual ``data`` bytes are
ignored.

Returns *true* if the frame was successfully added to the write queue. Returns
*false* if the frame could not be added because write queue is already full or
because the write buffer or the write backlog are configured with a size of
zero (see :func:`Set Queue Configuration`).

The write queue can overflow if frames are written to it at a higher rate
than the Bricklet can transmitted them over the CAN transceiver. This may
happen if the CAN transceiver is configured as read-only or is using a low baud
rate (see :func:`Set Transceiver Configuration`). It can also happen if the CAN
bus is congested and the frame cannot be transmitted because it constantly loses
arbitration or because the CAN transceiver is currently disabled due to a high
write error level (see :func:`Get Error Log`).
""",
'de':
"""
Schreibt einen Data- oder Remote-Frame in den Schreib-Queue, damit dieser über
den CAN-Transceiver übertragen wird.

Das Bricklet unterstützt die Standard 11-Bit (CAN 2.0A) und die zusätzlichen
Extended 29-Bit (CAN 2.0B) Identifier. Für Standard-Frames verwendet das
Bricklet Bit 0 bis 10 des ``identifier`` Parameters als Standard 11-Bit
Identifier. Für Extended-Frames verwendet das Bricklet Bit 0 bis 28 des
``identifier`` Parameters als Extended 29-Bit Identifier.

Der ``data`` Parameter kann bis zu 15 Bytes lang sein. Für Data-Frames werden
davon bis zu 8 Bytes als die eigentlichen Daten verwendet. Das Längenfeld (DLC)
im Daten- oder Remote-Frame wird auf die eigentliche Länge des ``data``
Parameters gesetzt. Dies erlaubt es Daten- und Remote-Frames mit Überlänge zu
übertragen. Für Remote-Frames wird nur die Länge ``data`` Parameters verwendet.
Die eigentlichen ``data`` Bytes werden ignoriert.

Gibt *true* zurück, wenn der Frame dem Schreib-Queue erfolgreich hinzugefügt
wurde. Gibt *false* zurück wenn Frame nicht hinzugefügt werden konnte, weil
der Schreib-Queue bereits voll ist oder weil der Schreib-Buffer oder das
Schreib-Backlog mit einer Länge von Null konfiguriert sind (siehe
:func:`Set Queue Configuration`).

Das Schreib-Queue kann überlaufen, wenn Frames schneller geschrieben werden
als das Bricklet sie über deb CAN-Transceiver übertragen kann. Dies kann
dadurch passieren, dass der CAN-Transceiver als nur-lesend oder mit einer
niedrigen Baudrate konfiguriert ist (siehe :func:`Set Transceiver Configuration`).
Es kann auch sein, dass der CAN-Bus stark belastet ist und der Frame nicht
übertragen werden kann, da er immer wieder die Arbitrierung verliert. Ein anderer
Grund kann sein, dass der CAN-Transceiver momentan deaktiviert ist, bedingt durch
ein hohes Schreib-Fehlerlevel (siehe :func:`Get Error Log`).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Read Frame Low Level',
'elements': [('Success', 'bool', 1, 'out', {}),
             ('Frame Type', 'uint8', 1, 'out', {'constant_group': 'Frame Type'}),
             ('Identifier', 'uint32', 1, 'out', {'range': (0, 2**30-1)}),
             ('Data Length', 'uint8', 1, 'out', {'range': (0, 15)}),
             ('Data Data', 'uint8', 15, 'out', {})],
'high_level': {'stream_out': {'name': 'Data', 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Tries to read the next data or remote frame from the read queue and returns it.
If a frame was successfully read, then the ``success`` return value is set to
*true* and the other return values contain the frame. If the read queue is
empty and no frame could be read, then the ``success`` return value is set to
*false* and the other return values contain invalid data.

The ``identifier`` return value follows the identifier format described for
:func:`Write Frame`.

The ``data`` return value can be up to 15 bytes long. For data frames up to the
first 8 bytes are the actual received data. All bytes after the 8th byte are
always zero and only there to indicate the length of a data or remote frame
with excess length. For remote frames the length of the ``data`` return value
represents the requested length. The actual ``data`` bytes are always zero.

A configurable read filter can be used to define which frames should be
received by the CAN transceiver and put into the read queue (see
:func:`Set Read Filter Configuration`).

Instead of polling with this function, you can also use callbacks. See the
:func:`Set Frame Read Callback Configuration` function and the :cb:`Frame Read`
callback.
""",
'de':
"""
Versucht den nächsten Data- oder Remote-Frame aus dem Lese-Queue zu lesen und
zurückzugeben. Falls ein Frame erfolgreich gelesen wurde, dann wird der
``success`` Rückgabewert auf *true* gesetzt und die anderen Rückgabewerte
beinhalte den gelesenen Frame. Falls der Lese-Queue leer ist und kein Frame
gelesen werden konnte, dann wird der ``success`` Rückgabewert auf *false*
gesetzt und die anderen Rückgabewerte beinhalte ungültige Werte.

Der ``identifier`` Rückgabewerte folgt dem für :func:`Write Frame` beschriebenen
Format.

Der ``data`` Rückgabewerte kann bis zu 15 Bytes lang sein. Bei Data-Frames sind
davon bis zu 8 Byte die eigentlich empfangenen Daten. Alle Bytes nach dem 8ten
Byte sind immer Null und dienen nur der Wiedergabe der Länge von Data- und
Remote-Frames mit Überlänge. Für Remote-Frames stellt die Länge des ``data``
Rückgabewertes die angefragte Länge dar. Die eigentlichen ``data`` Bytes sind
immer Null.

Mittels eines einstellbaren Lesefilters kann festgelegt werden, welche Frames
vom CAN-Transceiver überhaupt empfangen und im Lese-Queue abgelegt werden
sollen (siehe :func:`Set Read Filter Configuration`).

Anstatt mit dieser Funktion zu pollen, ist es auch möglich Callbacks zu nutzen.
Siehe die :func:`Set Frame Read Callback Configuration` Funktion und den
:cb:`Frame Read` Callback.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Frame Read Callback Configuration',
'elements': [('Enabled', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Enables and disables the :cb:`Frame Read` callback.

By default the callback is disabled. Enabling this callback will disable the :cb:`Frame Readable` callback.
""",
'de':
"""
Aktiviert und deaktiviert den :cb:`Frame Read` Callback.

Standardmäßig ist der Callback deaktiviert. Wenn dieser Callback aktiviert wird, wird der :cb:`Frame Readable` Callback deaktiviert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Frame Read Callback Configuration',
'elements': [('Enabled', 'bool', 1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns *true* if the :cb:`Frame Read` callback is enabled, *false* otherwise.
""",
'de':
"""
Gibt *true* zurück falls der :cb:`Frame Read` Callback aktiviert ist, *false*
sonst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Transceiver Configuration',
'elements': [('Baud Rate', 'uint32', 1, 'in', {'unit': 'Bit Per Second', 'range': (10000, 1000000), 'default': 125000}),
             ('Sample Point', 'uint16', 1, 'in', {'scale': (1, 10), 'unit': 'Percent', 'range': (500, 900), 'default': 625}),
             ('Transceiver Mode', 'uint8', 1, 'in', {'constant_group': 'Transceiver Mode', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the transceiver configuration for the CAN bus communication.

The CAN transceiver has three different modes:

* Normal: Reads from and writes to the CAN bus and performs active bus
  error detection and acknowledgement.
* Loopback: All reads and writes are performed internally. The transceiver
  is disconnected from the actual CAN bus.
* Read-Only: Only reads from the CAN bus, but does neither active bus error
  detection nor acknowledgement. Only the receiving part of the transceiver
  is connected to the CAN bus.
""",
'de':
"""
Setzt die Transceiver-Konfiguration für die CAN-Bus-Kommunikation.

Der CAN-Transceiver hat drei verschiedene Modi:

* Normal: Es wird vom CAN-Bus gelesen und auf den CAN-Bus geschrieben und
  aktiv an der Bus-Fehlererkennung und dem Acknowledgement mitgewirkt.
* Loopback: Alle Lese- und Schreiboperationen werden intern durchgeführt. Der
  Transceiver ist nicht mit dem eigentlichen CAN-Bus verbunden.
* Read-Only: Es wird nur vom CAN-Bus gelesen, allerdings ohne aktiv an der
  Bus-Fehlererkennung oder dem Acknowledgement mitzuwirken. Nur der empfangende
  Teil des Transceivers ist mit dem CAN-Bus verbunden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Transceiver Configuration',
'elements': [('Baud Rate', 'uint32', 1, 'out', {'unit': 'Bit Per Second', 'range': (10000, 1000000), 'default': 125000}),
             ('Sample Point', 'uint16', 1, 'out', {'scale': (1, 10), 'unit': 'Percent', 'range': (500, 900), 'default': 625}),
             ('Transceiver Mode', 'uint8', 1, 'out', {'constant_group': 'Transceiver Mode', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the configuration as set by :func:`Set Transceiver Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Transceiver Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Queue Configuration Low Level',
'elements': [('Write Buffer Size', 'uint8', 1, 'in', {'range': (0, 32), 'default': 8}),
             ('Write Buffer Timeout', 'int32', 1, 'in', {'range': (-1, None), 'default': 0}),
             ('Write Backlog Size', 'uint16', 1, 'in', {'range': (0, 768), 'default': 383}),
             ('Read Buffer Sizes Length', 'uint8', 1, 'in', {'range': (0, 32), 'default': 2}),
             ('Read Buffer Sizes Data', 'int8', 32, 'in', {'range': [(-32, -1), (1, 32)], 'default': [16, -8]}),
             ('Read Backlog Size', 'uint16', 1, 'in', {'range': (0, 768), 'default': 383})],
'high_level': {'stream_in': {'name': 'Read Buffer Sizes', 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the write and read queue configuration.

The CAN transceiver has 32 buffers in total in hardware for transmitting and
receiving frames. Additionally, the Bricklet has a backlog for 768 frames in
total in software. The buffers and the backlog can be freely assigned to the
write and read queues.

:func:`Write Frame` writes a frame into the write backlog. The Bricklet moves
the frame from the backlog into a free write buffer. The CAN transceiver then
transmits the frame from the write buffer to the CAN bus. If there are no
write buffers (``write_buffer_size`` is zero) or there is no write backlog
(``write_backlog_size`` is zero) then no frames can be transmitted and
:func:`Write Frame` returns always *false*.

The CAN transceiver receives a frame from the CAN bus and stores it into a
free read buffer. The Bricklet moves the frame from the read buffer into the
read backlog. :func:`Read Frame` reads the frame from the read backlog and
returns it. If there are no read buffers (``read_buffer_sizes`` is empty) or
there is no read backlog (``read_backlog_size`` is zero) then no frames can be
received and :func:`Read Frame` returns always *false*.

There can be multiple read buffers, because the CAN transceiver cannot receive
data and remote frames into the same read buffer. A positive read buffer size
represents a data frame read buffer and a negative read buffer size represents
a remote frame read buffer. A read buffer size of zero is not allowed. By
default the first read buffer is configured for data frames and the second read
buffer is configured for remote frame. There can be up to 32 different read
buffers, assuming that no write buffer is used. Each read buffer has its own
filter configuration (see :func:`Set Read Filter Configuration`).

A valid queue configuration fulfills these conditions::

 write_buffer_size + abs(read_buffer_size_0) + abs(read_buffer_size_1) + ... + abs(read_buffer_size_31) <= 32
 write_backlog_size + read_backlog_size <= 768

The write buffer timeout has three different modes that define how a failed
frame transmission should be handled:

* Single-Shot (< 0): Only one transmission attempt will be made. If the
  transmission fails then the frame is discarded.
* Infinite (= 0): Infinite transmission attempts will be made. The frame will
  never be discarded.
* Milliseconds (> 0): A limited number of transmission attempts will be made.
  If the frame could not be transmitted successfully after the configured
  number of milliseconds then the frame is discarded.

The current content of the queues is lost when this function is called.
""",
'de':
"""
Setzt die Schreibe- und Lese-Queue-Konfiguration.

Der CAN-Transceiver hat insgesamt 32 Buffer in Hardware für das Übertragen
und Empfangen von Frames. Zusätzlich hat das Bricklet ein Backlog für insgesamt
768 Frames in Software. Die Buffer und das Backlog können frei in Schreib- und
Lese-Queues aufgeteilt werden.

:func:`Write Frame` schreibt einen Frame in das Schreib-Backlog. Das Bricklet
überträgt den Frame vom Backlog in einen freien Schreib-Buffer. Der
CAN-Transceiver überträgt dann den Frame vom Schreib-Buffer über den CAN-Bus.
Falls kein Schreib-Buffer (``write_buffer_size`` ist Null) oder kein
Schreib-Backlog (``write_backlog_size`` ist Null) vorhanden ist dann kann kein
Frame übertragen werden und :func:`Write Frame` gibt immer *false* zurück.

Der CAN-Transceiver empfängt einen Frame vom CAN-Bus und speichert ihn in einem
freien Lese-Buffer. Das Bricklet übertragt den Frame vom Lese-Buffer in das
Lese-Backlog. :func:`Read Frame` liest den Frame aus dem Lese-Backlog und gibt
ihn zurück. Falls keine Lese-Buffer (``read_buffer_sizes`` ist leer) oder kein
Lese-Backlog (``read_backlog_size`` ist Null) vorhanden ist dann kann kein
Frame empfangen werden und :func:`Read Frame` gibt immer *false* zurück.

Es kann mehrere Lese-Buffer geben, da der CAN-Transceiver nicht Data- und
Remote-Frames in den gleichen Lese-Buffer empfangen kann. Eine positive
Lese-Buffer-Größe stellt einen Data-Frame-Lese-Buffer dar und eine negative
Lese-Buffer-Größe stellt einen Remote-Frame-Lese-Buffer dar. Eine
Lese-Buffer-Länge von Null ist nicht erlaubt. Standardmäßig ist der erste
Lese-Buffer für Data-Frames konfiguriert und der zweite Lese-Buffer ist für
Remote-Frames konfiguriert. Es kann bis zu 32 verschiedene Lese-Buffer geben,
unter der Annahme, dass kein Schreib-Buffer verwendet wird. Jeder Lese-Buffer
hat seine eigene Filter-Konfiguration (siehe
:func:`Set Read Filter Configuration`).

Eine gültige Queue-Konfiguration erfüllt diese Bedingungen::

 write_buffer_size + abs(read_buffer_size_0) + abs(read_buffer_size_1) + ... + abs(read_buffer_size_31) <= 32
 write_backlog_size + read_backlog_size <= 768

Der Schreib-Timeout hat drei verschiedene Modi, die festlegen wie mit einer
fehlgeschlagen Frame-Übertragung umgegangen werden soll:

* Single-Shot (= -1): Es wird nur ein Übertragungsversuch durchgeführt. Falls die
  Übertragung fehlschlägt wird der Frame verworfen.
* Infinite (= 0): Es werden unendlich viele Übertragungsversuche durchgeführt.
  Der Frame wird niemals verworfen.
* Milliseconds (> 0): Es wird eine beschränkte Anzahl Übertragungsversuche
  durchgeführt. Falls der Frame nach der eingestellten Anzahl Millisekunden
  noch nicht erfolgreich übertragen wurde, dann wird er verworfen.

Der aktuelle Inhalt der Queues geht bei einem Aufruf dieser Funktion verloren.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Queue Configuration Low Level',
'elements': [('Write Buffer Size', 'uint8', 1, 'out', {'range': (0, 32), 'default': 8}),
             ('Write Buffer Timeout', 'int32', 1, 'out', {'range': (-1, None), 'default': 0}),
             ('Write Backlog Size', 'uint16', 1, 'out', {'range': (0, 768), 'default': 383}),
             ('Read Buffer Sizes Length', 'uint8', 1, 'out', {'range': (0, 32), 'default': 2}),
             ('Read Buffer Sizes Data', 'int8', 32, 'out', {'range': [(-32, -1), (1, 32)], 'default': [16, -8]}),
             ('Read Backlog Size', 'uint16', 1, 'out', {'range': (0, 768), 'default': 383})],
'high_level': {'stream_out': {'name': 'Read Buffer Sizes', 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the queue configuration as set by :func:`Set Queue Configuration`.
""",
'de':
"""
Gibt die Queue-Konfiguration zurück, wie von :func:`Set Queue Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Read Filter Configuration',
'elements': [('Buffer Index', 'uint8', 1, 'in', {'range': (0, 31)}),
             ('Filter Mode', 'uint8', 1, 'in', {'constant_group': 'Filter Mode', 'default': 0}),
             ('Filter Mask', 'uint32', 1, 'in', {'range': (0, 2**30-1)}),
             ('Filter Identifier', 'uint32', 1, 'in', {'range': (0, 2**30-1)})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Set the read filter configuration for the given read buffer index. This can be
used to define which frames should be received by the CAN transceiver and put
into the read buffer.

The read filter has four different modes that define if and how the filter mask
and the filter identifier are applied:

* Accept-All: All frames are received.
* Match-Standard-Only: Only standard frames with a matching identifier are
  received.
* Match-Extended-Only: Only extended frames with a matching identifier are
  received.
* Match-Standard-And-Extended: Standard and extended frames with a matching
  identifier are received.

The filter mask and filter identifier are used as bit masks. Their usage
depends on the mode:

* Accept-All: Mask and identifier are ignored.
* Match-Standard-Only: Bit 0 to 10 (11 bits) of filter mask and filter
  identifier are used to match the 11-bit identifier of standard frames.
* Match-Extended-Only: Bit 0 to 28 (29 bits) of filter mask and filter
  identifier are used to match the 29-bit identifier of extended frames.
* Match-Standard-And-Extended: Bit 18 to 28 (11 bits) of filter mask and filter
  identifier are used to match the 11-bit identifier of standard frames, bit 0
  to 17 (18 bits) are ignored in this case. Bit 0 to 28 (29 bits) of filter
  mask and filter identifier are used to match the 29-bit identifier of extended
  frames.

The filter mask and filter identifier are applied in this way: The filter mask
is used to select the frame identifier bits that should be compared to the
corresponding filter identifier bits. All unselected bits are automatically
accepted. All selected bits have to match the filter identifier to be accepted.
If all bits for the selected mode are accepted then the frame is accepted and
is added to the read buffer.

.. csv-table::
 :header: "Filter Mask Bit", "Filter Identifier Bit", "Frame Identifier Bit", "Result"
 :widths: 10, 10, 10, 10

 0, X, X, Accept
 1, 0, 0, Accept
 1, 0, 1, Reject
 1, 1, 0, Reject
 1, 1, 1, Accept

For example, to receive standard frames with identifier 0x123 only, the mode
can be set to Match-Standard-Only with 0x7FF as mask and 0x123 as identifier.
The mask of 0x7FF selects all 11 identifier bits for matching so that the
identifier has to be exactly 0x123 to be accepted.

To accept identifier 0x123 and identifier 0x456 at the same time, just set
filter 2 to 0x456 and keep mask and filter 1 unchanged.

There can be up to 32 different read filters configured at the same time,
because there can be up to 32 read buffer (see :func:`Set Queue Configuration`).

The default mode is accept-all for all read buffers.
""",
'de':
"""
Setzt die Konfiguration für den Lesefilter des angegebenen Lese-Buffers. Damit
kann festgelegt werden, welche Frames von der CAN-Transceiver überhaupt
empfangen und im Lese-Buffer abgelegt werden sollen.

Der Lesefilter hat vier verschiedene Modi, die festlegen ob und wie die
Filter-Maske und der Filter-Identifier angewendet werden:

* Accept-All: Alle Frames werden empfangen.
* Match-Standard-Only: Nur Standard-Frames mit übereinstimmendem Identifier
  werden empfangen.
* Match-Extended-Only: Nur Extended-Frames mit übereinstimmendem Identifier
  werden empfangen.
* Match-Standard-And-Extended: Standard- und Extended-Frames mit
  übereinstimmendem Identifier werden empfangen.

Filter-Maske und Filter-Identifier werden als Bitmasken verwendet. Ihre
Verwendung hängt vom Filter-Modus ab:

* Accept-All: Filter-Maske und Filter-Identifier werden ignoriert.
* Match-Standard-Only: Bit 0 bis 10 (11 Bits) der Filter-Maske und des
  Filter-Identifiers werden zum Abgleich mit dem 11-Bit Identifier von
  Standard-Frames verwendet.
* Match-Extended-Only: Bit 0 bis 28 (29 Bits) der Filter-Maske und des
  Filter-Identifiers Abgleich mit dem 29-Bit Identifier von Extended-Frames
  verwendet.
* Match-Standard-And-Extended: Bit 18 bis 28 (11 Bits) der Filter-Maske und des
  Filter-Identifiers werden zum Abgleich mit dem 11-Bit Identifier von
  Standard-Frames verwendet, Bit 0 bis 17 (18 Bits) werden in diesem Fall
  ignoriert. Bit 0 bis 28 (29 Bits) der Filter-Maske und des Filter-Identifiers
  werden zum Abgleich mit dem 29-Bit Identifier von Extended-Frames verwendet.

Filter-Maske und Filter-Identifier werden auf diese Weise angewendet: Mit der
Filter-Maske werden die Frame-Identifier-Bits ausgewählt, die mit den
entsprechenden Filter-Identifier-Bits verglichen werden sollen. Alle
nicht-ausgewählten Bits werden automatisch akzeptiert. Alle ausgewählten Bits
müssen dem Filter-Identifier entsprechen, um akzeptiert zu werden. Wenn alle
Bits für den ausgewählte Modus akzeptiert wurden, dann ist der Frame akzeptiert
und wird im Lese-Buffer abgelegt.

.. csv-table::
 :header: "Filter-Masken-Bit", "Filter-Identifier-Bit", "Frame-Identifier-Bit", "Ergebnis"
 :widths: 10, 10, 10, 10

 0, X, X, akzeptiert
 1, 0, 0, akzeptiert
 1, 0, 1, verworfen
 1, 1, 0, verworfen
 1, 1, 1, akzeptiert

Ein Beispiel: Um nur Standard-Frames mit Identifier 0x123 zu empfangen kann
der Modus auf Match-Standard-Only mit 0x7FF als Filter-Maske und 0x123 als
Filter-Identifier eingestellt werden. Die Maske 0x7FF wählt alle 11
Identifier-Bits zum Abgleich aus, so dass der Identifier exakt 0x123 sein muss
um akzeptiert zu werden.

Da bis zu 32 Lese-Buffer konfiguriert werden können (siehe
:func:`Set Queue Configuration`) können auch bis zu 32 verschiedenen Lesefilter
gleichzeitig konfiguriert werden.

Der Standardmodus ist Accept-All für alle Lese-Buffer.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Read Filter Configuration',
'elements': [('Buffer Index', 'uint8', 1, 'in', {'range': (0, 31)}),
             ('Filter Mode', 'uint8', 1, 'out', {'constant_group': 'Filter Mode', 'default': 0}),
             ('Filter Mask', 'uint32', 1, 'out', {'range': (0, 2**30-1)}),
             ('Filter Identifier', 'uint32', 1, 'out', {'range': (0, 2**30-1)})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the read filter configuration as set by :func:`Set Read Filter Configuration`.
""",
'de':
"""
Gibt die Lese-Filter-Konfiguration zurück, wie von :func:`Set Read Filter Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Error Log Low Level',
'elements': [('Transceiver State', 'uint8', 1, 'out', {'constant_group': 'Transceiver State'}),
             ('Transceiver Write Error Level', 'uint8', 1, 'out', {}),
             ('Transceiver Read Error Level', 'uint8', 1, 'out', {}),
             ('Transceiver Stuffing Error Count', 'uint32', 1, 'out', {}),
             ('Transceiver Format Error Count', 'uint32', 1, 'out', {}),
             ('Transceiver ACK Error Count', 'uint32', 1, 'out', {}),
             ('Transceiver Bit1 Error Count', 'uint32', 1, 'out', {}),
             ('Transceiver Bit0 Error Count', 'uint32', 1, 'out', {}),
             ('Transceiver CRC Error Count', 'uint32', 1, 'out', {}),
             ('Write Buffer Timeout Error Count', 'uint32', 1, 'out', {}),
             ('Read Buffer Overflow Error Count', 'uint32', 1, 'out', {}),
             ('Read Buffer Overflow Error Occurred Length', 'uint8', 1, 'out', {'range': (0, 32)}),
             ('Read Buffer Overflow Error Occurred Data', 'bool', 32, 'out', {}),
             ('Read Backlog Overflow Error Count', 'uint32', 1, 'out', {})],
'high_level': {'stream_out': {'name': 'Read Buffer Overflow Error Occurred', 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns information about different kinds of errors.

The write and read error levels indicate the current level of stuffing, form,
acknowledgement, bit and checksum errors during CAN bus write and read
operations. For each of this error kinds there is also an individual counter.

When the write error level extends 255 then the CAN transceiver gets disabled
and no frames can be transmitted or received anymore. The CAN transceiver will
automatically be activated again after the CAN bus is idle for a while.

The write buffer timeout, read buffer and backlog overflow counts represents the
number of these errors:

* A write buffer timeout occurs if a frame could not be transmitted before the
  configured write buffer timeout expired (see :func:`Set Queue Configuration`).
* A read buffer overflow occurs if a read buffer of the CAN transceiver
  still contains the last received frame when the next frame arrives. In this
  case the last received frame is lost. This happens if the CAN transceiver
  receives more frames than the Bricklet can handle. Using the read filter
  (see :func:`Set Read Filter Configuration`) can help to reduce the amount of
  received frames. This count is not exact, but a lower bound, because the
  Bricklet might not able detect all overflows if they occur in rapid succession.
* A read backlog overflow occurs if the read backlog of the Bricklet is already
  full when the next frame should be read from a read buffer of the CAN
  transceiver. In this case the frame in the read buffer is lost. This
  happens if the CAN transceiver receives more frames to be added to the read
  backlog than are removed from the read backlog using the :func:`Read Frame`
  function. Using the :cb:`Frame Read` callback ensures that the read backlog
  can not overflow.

The read buffer overflow counter counts the overflows of all configured read
buffers. Which read buffer exactly suffered from an overflow can be figured
out from the read buffer overflow occurrence list
(``read_buffer_overflow_error_occurred``). Reading the error log clears the
occurence list.
""",
'de':
"""
Gibt Informationen über verschiedene Fehlerarten zurück.

Die Schreib- und Lesefehler-Level geben Aufschluss über das aktuelle Level
der Stuffing-, Form-, Acknowledgement-, Bit-, und Prüfsummen-Fehler während
CAN-Bus Schreib- und Leseoperationen. Für jede dieser Fehlerarten ist jeweils
auch ein eigener Zähler vorhanden.

Wenn das Schreibfehler-Level 255 überschreitet dann wird der CAN-Transceiver
deaktiviert und es können keine Frames mehr übertragen und empfangen werden.
Wenn auf dem CAN-Bus für eine Weile Ruhe herrscht, dann wird der CAN-Transceiver
automatisch wieder aktiviert.

Die Werte für Schreib-Buffer-Timeout, Lese-Buffer- und Lese-Backlog-Überlauf
zählen die Anzahl dieser Fehler:

* Ein Schreib-Buffer-Timeout tritt dann auf, wenn ein Frame nicht übertragen
  werden konnte bevor der eingestellte Schreib-Buffer-Timeout abgelaufen ist
  (siehe :func:`Set Queue Configuration`).
* Ein Lese-Buffer-Überlauf tritt dann auf, wenn in einem der Lese-Buffer des
  CAN-Transceiver noch der zuletzt empfangen Frame steht wenn der nächste Frame
  ankommt. In diesem Fall geht der zuletzt empfangen Frame verloren. Dies
  passiert, wenn der CAN-Transceiver mehr Frames empfängt als das Bricklet
  behandeln kann. Mit Hilfe des Lesefilters (siehe
  :func:`Set Read Filter Configuration`) kann die Anzahl der empfangen Frames
  verringert werden. Dieser Zähler ist nicht exakt, sondern stellt eine untere
  Grenze da. Es kann vorkommen, dass das Bricklet nicht alle Überläufe erkennt,
  wenn diese in schneller Abfolge auftreten.
* Ein Lese-Backlog-Überlauf tritt dann auf, wenn das Lese-Backlog des Bricklets
  bereits voll ist und noch ein Frame von einem Lese-Buffer des CAN-Transceiver
  gelesen werden soll. In diesem Fall geht der Frame im Lese-Buffer verloren.
  Dies passiert, wenn der CAN-Transceiver mehr Frames empfängt, die dem
  Lese-Backlog hinzugefügt werden sollen, als Frames mit der :func:`Read Frame`
  Funktion aus dem Lese-Backlog entnommen werden. Die Verwendung des
  :cb:`Frame Read` Callbacks stellt sicher, dass der Lese-Backlog nicht
  überlaufen kann.

Der Lese-Buffer-Überlauf-Zähler zählt die Überläuft aller konfigurierten
Lese-Buffer. In welchem Lese-Buffer seit dem letzten Aufruf dieser Funktion ein
Überlauf aufgetreten ist kann an der Liste des Lese-Buffer-Überlauf-Auftretens
(``read_buffer_overflow_error_occurred``) abgelesen werden. Auslesen des Fehler-Logs
setzt diese Liste zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Communication LED Config',
'elements': [('Config', 'uint8', 1, 'in', {'constant_group': 'Communication LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the communication LED configuration. By default the LED shows
CAN-Bus traffic, it flickers once for every 40 transmitted or received frames.

You can also turn the LED permanently on/off or show a heartbeat.

If the Bricklet is in bootloader mode, the LED is off.
""",
'de':
"""
Setzt die Konfiguration der Kommunikations-LED. Standardmäßig zeigt
die LED die Kommunikationsdatenmenge an. Sie blinkt einmal pro 40 empfangenen
oder gesendeten Frames.

Die LED kann auch permanent an/aus gestellt werden oder einen Herzschlag anzeigen.

Wenn das Bricklet sich im Bootloadermodus befindet ist die LED aus.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Communication LED Config',
'elements': [('Config', 'uint8', 1, 'out', {'constant_group': 'Communication LED Config', 'default': 3})],
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
'elements': [('Config', 'uint8', 1, 'in', {'constant_group': 'Error LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the error LED configuration.

By default (show-transceiver-state) the error LED turns on if the CAN
transceiver is passive or disabled state (see :func:`Get Error Log`). If
the CAN transceiver is in active state the LED turns off.

If the LED is configured as show-error then the error LED turns on if any error
occurs. If you call this function with the show-error option again, the LED will
turn off until the next error occurs.

You can also turn the LED permanently on/off or show a heartbeat.

If the Bricklet is in bootloader mode, the LED is off.
""",
'de':
"""
Setzt die Konfiguration der Error-LED.

Standardmäßig (Show-Transceiver-State) geht die LED an, wenn der CAN-Transceiver
im Passive oder Disabled Zustand ist (siehe :func:`Get Error Log`). Wenn
der CAN-Transceiver im Active Zustand ist, dann geht die LED aus.

Wenn die LED als Show-Error konfiguriert ist, dann geht die LED an wenn ein
Error auftritt. Wenn diese Funktion danach nochmal mit der Show-Error-Option
aufgerufen wird, geht die LED wieder aus bis der nächste Error auftritt.

Die LED kann auch permanent an/aus gestellt werden oder einen Herzschlag
anzeigen.

Wenn das Bricklet sich im Bootloadermodus befindet ist die LED aus.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Error LED Config',
'elements': [('Config', 'uint8', 1, 'out', {'constant_group': 'Error LED Config', 'default': 3})],
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
'type': 'callback',
'name': 'Frame Read Low Level',
'elements': [('Frame Type', 'uint8', 1, 'out', {'constant_group': 'Frame Type'}),
             ('Identifier', 'uint32', 1, 'out', {'range': (0, 2**30-1)}),
             ('Data Length', 'uint8', 1, 'out', {'range': (0, 15)}),
             ('Data Data', 'uint8', 15, 'out', {})],
'high_level': {'stream_out': {'name': 'Data', 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered if a data or remote frame was received by the CAN
transceiver.

The ``identifier`` return value follows the identifier format described for
:func:`Write Frame`.

For details on the ``data`` return value see :func:`Read Frame`.

A configurable read filter can be used to define which frames should be
received by the CAN transceiver and put into the read queue (see
:func:`Set Read Filter Configuration`).

To enable this callback, use :func:`Set Frame Read Callback Configuration`.
""",
'de':
"""
Dieser Callback wird ausgelöst, sobald ein Data- oder Remote-Frame vom
CAN-Transceiver empfangen wurde.

Der ``identifier`` Rückgabewerte folgt dem für :func:`Write Frame` beschriebenen
Format.

Für Details zum ``data`` Rückgabewerte siehe :func:`Read Frame`.

Mittels eines einstellbaren Lesefilters kann festgelegt werden, welche Frames
vom CAN-Transceiver überhaupt empfangen und im Lese-Queue abgelegt werden
sollen (siehe :func:`Set Read Filter Configuration`).

Dieser Callback kann durch :func:`Set Frame Read Callback Configuration`
aktiviert werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Frame Readable Callback Configuration',
'elements': [('Enabled', 'bool', 1, 'in', {'default': False})],
'since_firmware': [2, 0, 3],
'doc': ['ccf', {
'en':
"""
Enables and disables the :cb:`Frame Readable` callback.

By default the callback is disabled. Enabling this callback will disable the :cb:`Frame Read` callback.
""",
'de':
"""
Aktiviert und deaktiviert den :cb:`Frame Readable` Callback.

Standardmäßig ist der Callback deaktiviert. Wenn dieser Callback aktiviert wird, wird der :cb:`Frame Read` Callback deaktiviert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Frame Readable Callback Configuration',
'elements': [('Enabled', 'bool', 1, 'out', {'default': False})],
'since_firmware': [2, 0, 3],
'doc': ['ccf', {
'en':
"""
Returns *true* if the :cb:`Frame Readable` callback is enabled, *false* otherwise.
""",
'de':
"""
Gibt *true* zurück falls der :cb:`Frame Readable` Callback aktiviert ist, *false*
sonst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Frame Readable',
'elements': [],
'since_firmware': [2, 0, 3],
'doc': ['c', {
'en':
"""
This callback is triggered if a data or remote frame was received by the CAN
transceiver. The received frame can be read with :func:`Read Frame`.
If additional frames are received, but :func:`Read Frame` was not called yet, the callback
will not trigger again.

A configurable read filter can be used to define which frames should be
received by the CAN transceiver and put into the read queue (see
:func:`Set Read Filter Configuration`).

To enable this callback, use :func:`Set Frame Readable Callback Configuration`.
""",
'de':
"""
Dieser Callback wird ausgelöst, sobald ein Data- oder Remote-Frame vom
CAN-Transceiver empfangen wurde. Der empfangene Frame kann mit :func:`Read Frame`
ausgelesen werden. Falls weitere Frames empfangen werden, bevor :func:`Read Frame` aufgerufen
wurde, wird der Callback nicht erneut ausgelöst.

Mittels eines einstellbaren Lesefilters kann festgelegt werden, welche Frames
vom CAN-Transceiver überhaupt empfangen und im Lese-Queue abgelegt werden
sollen (siehe :func:`Set Read Filter Configuration`).

Dieser Callback kann durch :func:`Set Frame Readable Callback Configuration`
aktiviert werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Error Occurred Callback Configuration',
'elements': [('Enabled', 'bool', 1, 'in', {'default': False})],
'since_firmware': [2, 0, 3],
'doc': ['ccf', {
'en':
"""
Enables and disables the :cb:`Error Occurred` callback.

By default the callback is disabled.
""",
'de':
"""
Aktiviert und deaktiviert den :cb:`Error Occurred` Callback.

Standardmäßig ist der Callback deaktiviert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Error Occurred Callback Configuration',
'elements': [('Enabled', 'bool', 1, 'out', {'default': False})],
'since_firmware': [2, 0, 3],
'doc': ['ccf', {
'en':
"""
Returns *true* if the :cb:`Error Occurred` callback is enabled, *false* otherwise.
""",
'de':
"""
Gibt *true* zurück falls der :cb:`Error Occurred` Callback aktiviert ist, *false*
sonst.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Error Occurred',
'elements': [],
'since_firmware': [2, 0, 3],
'doc': ['c', {
'en':
"""
This callback is triggered if any error occurred while writing, reading or transmitting CAN frames.

The callback is only triggered once until :func:`Get Error Log` is called. That function will return
details abount the error(s) occurred.

To enable this callback, use :func:`Set Error Occurred Callback Configuration`.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn ein Fehler während des Schreibens, Lesens oder Empfangens von CAN-Frames auftritt.

Der Callback wird nur einmal ausgelöst, bis :func:`Get Error Log` aufgerufen wird. Diese Funktion liefert Details
über aufgetretene Fehler.

Dieser Callback kann durch :func:`Set Error Occurred Callback Configuration`
aktiviert werden.
"""
}]
})

# com['packets'].append({
# 'type': 'function',
# 'name': 'Set Timestamped Frame Configuration',
# 'elements': [('Enabled', 'bool', 1, 'in'),
#             ('Write Backlog Size', 'uint16', 1, 'in'),
#             ('Read Backlog Size', 'uint16', 1, 'in')],
# 'since_firmware': [2, 0, 3],
# 'doc': ['af', {
# 'en':
# """
# """,
# 'de':
# """
# """
# }]
# })

# com['packets'].append({
# 'type': 'function',
# 'name': 'Get Timestamped Frame Configuration',
# 'elements': [('Enabled', 'bool', 1, 'out'),
#             ('Write Backlog Size', 'uint16', 1, 'out'),
#             ('Read Backlog Size', 'uint16', 1, 'out')],
# 'since_firmware': [2, 0, 3],
# 'doc': ['af', {
# 'en':
# """
# """,
# 'de':
# """
# """
# }]
# })

# com['packets'].append({
# 'type': 'function',
# 'name': 'Write Timestamped Frame Low Level',
# 'elements': [('Frame Type', 'uint8', 1, 'in', {'constant_group': 'Frame Type'}),
#             ('Identifier', 'uint32', 1, 'in'),
#             ('Data Length', 'uint8', 1, 'in'),
#             ('Data Data', 'uint8', 15, 'in'),
#             ('Timestamp', 'uint64', 1, 'in'),
#             ('Success', 'bool', 1, 'out')],
# 'high_level': {'stream_in': {'name': 'Data', 'single_chunk': True}},
# 'since_firmware': [2, 0, 3],
# 'doc': ['af', {
# 'en':
# """
# """,
# 'de':
# """
# """
# }]
# })

# com['packets'].append({
# 'type': 'function',
# 'name': 'Read Timestamped Frame Low Level',
# 'elements': [('Success', 'bool', 1, 'out'),
#             ('Frame Type', 'uint8', 1, 'out', {'constant_group': 'Frame Type'}),
#             ('Identifier', 'uint32', 1, 'out'),
#             ('Data Length', 'uint8', 1, 'out'),
#             ('Data Data', 'uint8', 15, 'out'),
#             ('Timestamp', 'uint64', 1, 'out')],
# 'high_level': {'stream_out': {'name': 'Data', 'single_chunk': True}},
# 'since_firmware': [2, 0, 3],
# 'doc': ['af', {
# 'en':
# """
# """,
# 'de':
# """
# """
# }]
# })

# com['packets'].append({
# 'type': 'function',
# 'name': 'Get Timestamp',
# 'elements': [('Timestamp', 'uint64', 1, 'out')],
# 'since_firmware': [2, 0, 3],
# 'doc': ['af', {
# 'en':
# """
# """,
# 'de':
# """
# """
# }]
# })

# com['packets'].append({
# 'type': 'function',
# 'name': 'Set Timestamped Frame Read Callback Configuration',
# 'elements': [('Enabled', 'bool', 1, 'in')],
# 'since_firmware': [2, 0, 3],
# 'doc': ['ccf', {
# 'en':
# """
# """,
# 'de':
# """
# """
# }]
# })

# com['packets'].append({
# 'type': 'function',
# 'name': 'Get Timestamped Frame Read Callback Configuration',
# 'elements': [('Enabled', 'bool', 1, 'out')],
# 'since_firmware': [2, 0, 3],
# 'doc': ['ccf', {
# 'en':
# """
# """,
# 'de':
# """
# """
# }]
# })

# com['packets'].append({
# 'type': 'callback',
# 'name': 'Timestamped Frame Read Low Level',
# 'elements': [('Frame Type', 'uint8', 1, 'out', {'constant_group': 'Frame Type'}),
#             ('Identifier', 'uint32', 1, 'out'),
#             ('Data Length', 'uint8', 1, 'out'),
#             ('Data Data', 'uint8', 15, 'out'),
#             ('Timestamp', 'uint64', 1, 'out')],
# 'high_level': {'stream_out': {'name': 'Data', 'single_chunk': True}},
# 'since_firmware': [2, 0, 3],
# 'doc': ['c', {
# 'en':
# """
# """,
# 'de':
# """
# """
# }]
# })


com['examples'].append({
'name': 'Loopback',
'functions': [('setter', 'Set Transceiver Configuration', [('uint32', 1000000), ('uint16', 625), ('uint8:constant', 1)], 'Configure transceiver for loopback mode', None),
              ('callback', ('Frame Read', 'frame read'), [(('Frame Type', 'Frame Type'), 'uint8:constant', 1, None, None, None), (('Identifier', 'Identifier'), 'uint32', 1, None, None, None), (('Data', 'Data'), 'uint8', -15, None, None, None)], None, None),
              ('setter', 'Set Frame Read Callback Configuration', [('bool', True)], 'Enable frame read callback', None),
              ('setter', 'Write Frame', [('uint8:constant', 0), ('uint32', 1742), ('uint8', [42, 23, 17])], 'Write standard data frame with identifier 1742 and 3 bytes of data', None)],
'cleanups': [('setter', 'Set Frame Read Callback Configuration', [('bool', False)], None, None)],
'incomplete': True # because of callback with array parameter and write-frame function success output parameter
})


com['openhab'] = {
    'imports': oh_generic_channel_imports() + oh_generic_trigger_channel_imports() + ['org.eclipse.smarthome.core.library.types.DecimalType'],
    'param_groups': oh_generic_channel_param_groups(),
    'params': [{
            'packet': 'Set Transceiver Configuration',
            'element': 'Baud Rate',

            'name': 'Baud Rate',
            'type': 'integer',
            'min': 10000,
            'max': 1000000,
            'default': 125000,

            'label': 'Baud Rate',
            'description': 'The baud rate to send/receive with.',
        }, {
            'packet': 'Set Transceiver Configuration',
            'element': 'Sample Point',

            'name': 'Sample Point',
            'type': 'decimal',
            'default': 62.5,
            'min': 50,
            'max': 90,
            'step': 0.1,

            'label': 'Sample Point',
            'description': 'Configures when to sample a bit during each bit period.'
        }, {
            'packet': 'Set Transceiver Configuration',
            'element': 'Transceiver Mode',

            'name': 'Transceiver Mode',
            'type': 'integer',
            'options': [('Normal', 0),
                        ('Loopback', 1),
                        ('Read Only', 2)],
            'limitToOptions': 'true',
            'default': 0,

            'label': 'Transceiver Mode',
            'description': 'The CAN transceiver has three different modes:<ul><li>Normal: Reads from and writes to the CAN bus and performs active bus error detection and acknowledgement.</li><li>Loopback: All reads and writes are performed internally. The transceiver is disconnected from the actual CAN bus.</li><li>Read-Only: Only reads from the CAN bus, but does neither active bus error detection nor acknowledgement. Only the receiving part of the transceiver is connected to the CAN bus.</li></ul>'
        }, {
            'packet': 'Set Communication LED Config',
            'element': 'Config',

            'name': 'Communication LED Config',
            'type': 'integer',
            'options': [('Off', 0),
                        ('On', 1),
                        ('Show Heartbeat', 2),
                        ('Show Communication', 3)],
            'limitToOptions': 'true',
            'default': 3,

            'label': 'Communication LED Config',
            'description': "By default the LED shows CAN-Bus traffic, it flickers once for every 40 transmitted or received frames. You can also turn the LED permanently on/off or show a heartbeat. If the Bricklet is in bootloader mode, the LED is off.",
        }, {
            'packet': 'Set Error LED Config',
            'element': 'Config',

            'name': 'Error LED Config',
            'type': 'integer',
            'options': [('Off', 0),
                        ('On', 1),
                        ('Show Heartbeat', 2),
                        ('Show Transceiver State', 3),
                        ('Show Error', 4)],
            'limitToOptions': 'true',
            'default': 3,

            'label': 'Error LED Config',
            'description': "By default (show-transceiver-state) the error LED turns on if the CAN transceiver is passive or disabled state (see the getErrorLog action). If the CAN transceiver is in active state the LED turns off.<br/><br/>If the LED is configured as show-error then the error LED turns on if any error occurs. If you call this function with the show-error option again, the LED will turn off until the next error occurs.<br/><br/>You can also turn the LED permanently on/off or show a heartbeat.<br/><br/>If the Bricklet is in bootloader mode, the LED is off.",
        }],

    'init_code': """this.setTransceiverConfiguration(cfg.baudRate, (int)(cfg.samplePoint.doubleValue() * 10), cfg.transceiverMode);
    this.setCommunicationLEDConfig(cfg.communicationLEDConfig);
    this.setErrorLEDConfig(cfg.errorLEDConfig);
    this.setFrameReadableCallbackConfiguration(true);
    this.setErrorOccurredCallbackConfiguration(true);""",

    'channels': [{
            'id': 'Frame Readable',
            'label': 'Frame Readable',
            'description': "This channel is triggered when a new frame was received and can be read out. The channel will only trigger again if the frame was read.",
            'type': 'system.trigger',
            'callbacks': [{
                'packet': 'Frame Readable',
                'transform': 'CommonTriggerEvents.PRESSED'}],

            'is_trigger_channel': True,
        }, {
            'id': 'Error Occurred',
            'label': 'Error Occurred',
            'description': "This channel is triggered if any error occurred while writing, reading or transmitting CAN frames. The channel will trigger only once until the getErrorLog action is called.",
            'type': 'system.trigger',
            'callbacks': [{
                'packet': 'Error Occurred',
                'transform': 'CommonTriggerEvents.PRESSED'}],

            'is_trigger_channel': True,
        }],
    'channel_types': [],
    'actions': ['Write Frame', 'Read Frame', 'Get Transceiver Configuration', 'Set Queue Configuration', 'Get Queue Configuration', 'Set Read Filter Configuration', 'Get Read Filter Configuration', 'Get Error Log']
}
