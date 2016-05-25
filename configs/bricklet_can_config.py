# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# CAN Bricklet communication config

com = {
    'author': 'Matthias Bolte <matthias@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 270,
    'name': ('CAN', 'CAN', 'CAN Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Communicates with CAN bus devices',
        'de': 'Kommuniziert mit CAN-Bus Geräten'
    },
    'released': False,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Write Frame',
'elements': [('Frame Type', 'uint8', 1, 'in', ('Frame Type', [('Standard Data', 0),
                                                              ('Standard Remote', 1),
                                                              ('Extended Data', 2),
                                                              ('Extended Remote', 3)])),
             ('Identifier', 'uint32', 1, 'in'),
             ('Data', 'uint8', 8, 'in'),
             ('Length', 'uint8', 1, 'in'),
             ('Success', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes a data or remote frame to the write buffer to be transmitted over the
CAN transceiver.

The Bricklet supports the standard 11-bit (CAN 2.0A) and the extended 29-bit
(CAN 2.0B) identifiers. For remote frames the ``data`` parameter is ignored.

Returns *true* if the frame was successfully added to the write buffer. Returns
*false* if the frame could not be added because write buffer is already full.

The write buffer can overflow if frames are written to it at a higher rate
than the Bricklet can transmitted them over the CAN transceiver. This may
happen if the CAN transceiver is configured as read-only or is using a low baud
rate (see :func:`SetConfiguration`). It can also happen if the CAN bus is
congested and the frame cannot be transmitted because it constantly loses
arbitration or because the CAN transceiver is currently disabled due to a high
write error level (see :func:`GetErrorLog`).
""",
'de':
"""
Schreibt einen Data- oder Remote-Frame in den Schreib-Buffer, damit dieser über
den CAN-Transceiver übertragen wird.

Das Bricklet unterstützt die Standard 11-Bit (CAN 2.0A) und die Extended 29-Bit
(CAN 2.0B) Identifier. Für Remote-Frames wird das ``data`` Parameter ignoriert.

Gibt *true* zurück, wenn der Frame dem Schreib-Buffer erfolgreich hinzugefügt
wurde. Gibt *false* zurück wenn Frame nicht hinzugefügt werden konnte, weil
der Schreib-Buffer bereits voll ist.

Der Schreib-Buffer kann überlaufen, wenn Frames schneller geschrieben werden
als das Bricklet sie über deb CAN-Transceiver übertragen kann. Dies kann
dadurch passieren, dass der CAN-Transceiver als nur-lesend oder mit einer
niedrigen Baudrate konfiguriert ist (siehe :func:`SetConfiguration`). Es kann
auch sein, dass der CAN-Bus stark belastet ist und der Frame nicht übertragen
werden kann, da er immer wieder die Arbitrierung verliert. Ein anderer Grund
kann sein, dass der CAN-Transceiver momentan deaktiviert ist, bedingt duch ein
hohes Schreib-Fehlerlevel (siehe :func:`GetErrorLog`).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Read Frame',
'elements': [('Success', 'bool', 1, 'out'),
             ('Frame Type', 'uint8', 1, 'out', ('Frame Type', [('Standard Data', 0),
                                                               ('Standard Remote', 1),
                                                               ('Extended Data', 2),
                                                               ('Extended Remote', 3)])),
             ('Identifier', 'uint32', 1, 'out'),
             ('Data', 'uint8', 8, 'out'),
             ('Length', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Tries to read the next data or remote frame from the read buffer and return it.
If a frame was successfully read, then the ``success`` return value is set to
*true* and the other return values contain the frame. If the read buffer is
empty and no frame could be read, then the ``success`` return value is set to
*false* and the other return values contain invalid data.

For remote frames the ``data`` return value always contains invalid data.

A configurable read filter can be used to define which frames should be
received by the CAN transceiver and put into the read buffer (see
:func:`SetReadFilter`).

Instead of polling with this function, you can also use callbacks. See the
:func:`EnableFrameReadCallback` function and the :func:`FrameRead` callback.
""",
'de':
"""
Versucht den nächsten Data- oder Remote-Frame aus dem Lese-Buffer zu lesen und
zurückzugeben. Falls ein Frame erfolgreich gelesen wurde, dann wird der
``success`` Rückgabewert auf *true* gesetzt und die anderen Rückgabewerte
beinhalte den gelesenen Frame. Falls der Lese-Buffer leer ist und kein Frame
gelesen werden konnte, dann wird der ``success`` Rückgabewert auf *false*
gesetzt und die anderen Rückgabewerte beinhalte ungültige Werte.

Für Remote-Frames beinhalte der ``data`` Rückgabewerte immer gültigen Werte.

Mittels eines einstellbaren Lesefilters kann festgelegt werden, welche Frames
vom CAN-Transceiver überhaupt empfangen und im Lese-Buffer abgelegt werden
sollen (siehe :func:`SetReadFilter`).

Anstatt mit dieser Funktion zu pollen, ist es auch möglich Callbacks zu nutzen.
Siehe die :func:`EnableFrameReadCallback` Funktion und den :func:`FrameRead`
Callback.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Enable Frame Read Callback',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Enables the :func:`FrameRead` callback.

By default the callback is disabled.
""",
'de':
"""
Aktiviert den :func:`FrameRead` Callback.

Standardmäßig ist der Callback deaktiviert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Disable Frame Read Callback',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Disables the :func:`FrameRead` callback.

By default the callback is disabled.
""",
'de':
"""
Deaktiviert den :func:`FrameRead` Callback.

Standardmäßig ist der Callback deaktiviert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is Frame Read Callback Enabled',
'elements': [('Enabled', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns *true* if the :func:`FrameRead` callback is enabled, *false* otherwise.
""",
'de':
"""
Gibt *true* zurück falls der :func:`FrameRead` Callback aktiviert ist, *false*
sonst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('Baud Rate', 'uint8', 1, 'in', ('Baud Rate', [('10000', 0),
                                                            ('20000', 1),
                                                            ('50000', 2),
                                                            ('125000', 3),
                                                            ('250000', 4),
                                                            ('500000', 5),
                                                            ('800000', 6),
                                                            ('1000000', 7)])),
             ('Transceiver Mode', 'uint8', 1, 'in', ('Transceiver Mode', [('Normal', 0),
                                                                          ('Loopback', 1),
                                                                          ('Read Only', 2)])),
             ('Write Timeout', 'int32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the configuration for the CAN bus communication.

The baud rate can be configured in steps between 10 and 1000 kbit/s.

The CAN transceiver has three different modes:

* Normal: Reads from and writes and to the CAN bus and performs active bus
  error detection and acknowledgement.
* Loopback: All reads and writes are performed internally. The transceiver
  is disconnected from the actual CAN bus.
* Read-Only: Only reads from the CAN bus, but does neither active bus error
  detection nor acknowledgement. Only the receiving part of the transceiver
  is connected to the CAN bus.

The write timeout has three different modes that define how a failed frame
transmission should be handled:

* One-Shot (< 0): Only one transmission attempt will be made. If the
  transmission fails then the frame is discarded.
* Infinite (= 0): Infinite transmission attempts will be made. The frame will
  never be discarded.
* Milliseconds (> 0): A limited number of transmission attempts will be made.
  If the frame could not be transmitted successfully after the configured
  number of milliseconds then the frame is discarded.

The default is: 125 kbit/s, normal transceiver mode and infinite write timeout.
""",
'de':
"""
Setzt die Konfiguration für die CAN-Bus-Kommunikation.

Die Baudrate kann in Schritten zwischen 10 und 1000 kBit/s eingestellt werden.

Der CAN-Transceiver hat drei verschiedene Modi:

* Normal: Es wird vom CAN-Bus gelesen und auf den CAN-Bus geschrieben und
  aktiv an der Bus-Fehlererkennung und dem Acknowledgement mitgewirkt.
* Loopback: Alle Lese- und Schreiboperationen werden intern durchgeführt. Der
  Transceiver ist nicht mit dem eigentlichen CAN-Bus verbunden.
* Read-Only: Es wird nur vom CAN-Bus gelesen, allerdings ohne aktiv an der
  Bus-Fehlererkennung oder dem Acknowledgement mitzuwirken. Nur der empfangende
  Teil des Transceivers ist mit dem CAN-Bus verbunden.

Der Schreib-Timeout hat drei verschiedene Modi, die festlegen wie mit einer
fehlgeschlagen Frame-Übertragung umgegangen werden soll:

* One-Shot (< 0): Es wird nur ein Übertragungsversuch durchgeführt. Falls die
  Übertragung fehlschlägt wird der Frame verworfen.
* Infinite (= 0): Es werden unendlich viele Übertragungsversuche durchgeführt.
  Der Frame wird niemals verworfen.
* Milliseconds (> 0): Es wird eine beschränkte Anzahl Übertragungsversuche
  durchgeführt. Falls der Frame nach der eingestellten Anzahl Millisekunden
  noch nicht erfolgreich übertragen wurde, dann wird er verworfen.

Der Standard ist: 125 kBit/s, Normaler Transceiver-Modus und unendlicher
Schreib-Timeout.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Baud Rate', 'uint8', 1, 'out', ('Baud Rate', [('10000', 0),
                                                             ('20000', 1),
                                                             ('50000', 2),
                                                             ('125000', 3),
                                                             ('250000', 4),
                                                             ('500000', 5),
                                                             ('800000', 6),
                                                             ('1000000', 7)])),
             ('Transceiver Mode', 'uint8', 1, 'out', ('Transceiver Mode', [('Normal', 0),
                                                                           ('Loopback', 1),
                                                                           ('Read Only', 2)])),
             ('Write Timeout', 'int32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the configuration as set by :func:`SetConfiguration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`SetConfiguration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Read Filter',
'elements': [('Mode', 'uint8', 1, 'in', ('Filter Mode', [('Disabled', 0),
                                                         ('Accept All', 1),
                                                         ('Match Standard', 2),
                                                         ('Match Standard And Data', 3),
                                                         ('Match Extended', 4)])),
             ('Mask', 'uint32', 1, 'in'),
             ('Filter1', 'uint32', 1, 'in'),
             ('Filter2', 'uint32', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Set the read filter configuration. This can be used to define which frames
should be received by the CAN transceiver and put into the read buffer.

The read filter has five different modes that define if and how the mask and
the two filters are applied:

* Disabled: No filtering is applied at all. All frames are received even
  incomplete and defective frames. This mode should be used for debugging only.
* Accept-All: All complete and error-free frames are received.
* Match-Standard: Only standard frames with a matching identifier are received.
* Match-Standard-and-Data: Only standard frames with matching identifier and
  data bytes are received.
* Match-Extended: Only extended frames with a matching identifier are received.

The mask and filters are used as bit masks. Their usage depends on the mode:

* Disabled: Mask and filters are ignored.
* Accept-All: Mask and filters are ignored.
* Match-Standard: Bit 0 to 10 (11 bits) of mask and filters are used to match
  the 11-bit identifier of standard frames.
* Match-Standard-and-Data: Bit 0 to 10 (11 bits) of mask and filters are used
  to match the 11-bit identifier of standard frames. Bit 11 to 18 (8 bits) and
  bit 19 to 26 (8 bits) of mask and filters are used to match the first and
  second data byte (if present) of standard frames.
* Match-Extended: Bit 0 to 28 (29 bits) of mask and filters are used to match
  the 29-bit identifier of extended frames.

The mask and filters are applied in this way: The mask is used to select the
identifier and data bits that should be compared to the corresponding filter
bits. All unselected bits are automatically accepted. All selected bits have
to match one of the filters to be accepted. If all bits for the selected mode
are accepted then the frame is accepted and is added to the read buffer.

.. csv-table::
 :header: "Mask Bit", "Filter Bit", "Identifier/Data Bit", "Result"
 :widths: 10, 10, 10, 10

 0, X, X, Accept
 1, 0, 0, Accept
 1, 0, 1, Reject
 1, 1, 0, Reject
 1, 1, 1, Accept

For example, to receive standard frames with identifier 0x123 only the mode can
be set to Match-Standard with 0x7FF as mask and 0x123 as filter 1 and filter 2.
The mask of 0x7FF selects all 11 identifier bits for matching so that the
identifier has to be exactly 0x123 to be accepted.

To accept identifier 0x123 and identifier 0x456 at the same time, just set
filter 2 to 0x456 and keep mask and filter 1 unchanged.

The default mode is accept-all.
""",
'de':
"""
Setzt die Konfiguration für den Lesefilter. Damit kann festgelegt werden,
welche Frames von der CAN-Transceiver überhaupt empfangen und im Lese-Buffer
abgelegt werden sollen.

Der Lesefilter hat fünf verschiedene Modi, die festlegen ob und wie die Maske
und die beiden Filter angewendet werden:

* Disabled: Es wird keinerlei Filterung durchgeführt. Alle Frames inklusive
  unvollständiger und fehlerhafter Frames werden empfangen. Dieser Modus sollte
  nur für Debugging-Zwecke verwendet werden.
* Accept-All: Alle vollständigen und fehlerfreien Frames werden empfangen.
* Match-Standard: Nur Standard-Frames, deren Identifier der eingestellten
  Maske und Filtern entspricht, werden empfangen.
* Match-Standard-and-Data: Nur Standard-Frames, deren Identifier und Daten der
  eingestellten Maske und Filtern entspricht, werden empfangen.
* Match-Extended: Nur Extended-Frames, deren Identifier der eingestellten
  Maske und Filtern entspricht, werden empfangen.

Maske und Filter werden als Bitmasken verwendet. Ihre Verwendung hängt vom
Modus ab:

* Disabled: Maske und Filter werden ignoriert.
* Accept-All: Maske und Filter werden ignoriert.
* Match-Standard: Bit 0 bis 10 (11 Bits) der Maske und Filter werden zum
  Abgleich mit dem 11-Bit Identifier von Standard-Frames verwendet.
* Match-Standard-and-Data: Bit 0 bis 10 (11 Bits) der Maske und Filter werden
  zum Abgleich mit dem 11-Bit Identifier von Standard-Frames verwendet. Bit 11
  bis 18 (8 Bits) und Bit 19 bis 26 (8 Bits) der Maske und Filter werden zum
  Abgleich mit dem ersten und zweiten Daten-Byte (sofern vorhanden) von
  Standard-Frames verwendet.
* Match-Extended: Bit 0 bis 28 (29 Bits) der Maske und Filter werden zum
  Abgleich mit dem 29-Bit Identifier von Extended-Frames verwendet.

Maske und Filter werden auf diese Weise angewendet: Mit der Maske werden die
Identifier- und Daten-Bits ausgewählt, die mit den entsprechenden Filter-Bits
verglichen werden sollen. Alle nicht-ausgewählten Bits werden automatisch
akzeptiert. Alle ausgewählten Bits müssen einem der beiden Filter entsprechen,
um akzeptiert zu werden. Wenn alle Bits für den ausgewählte Modus akzeptiert
wurden, dann ist der Frame akzeptiert und wird im Lese-Buffer abgelegt.

.. csv-table::
 :header: "Masken-Bit", "Filter-Bit", "Identifier/Daten-Bit", "Ergebnis"
 :widths: 10, 10, 10, 10

 0, X, X, akzeptiert
 1, 0, 0, akzeptiert
 1, 0, 1, verworfen
 1, 1, 0, verworfen
 1, 1, 1, akzeptiert

Ein Beispiel: Um nur Standard-Frames mit Identifier 0x123 zu empfangen kann
der Modus auf Match-Standard mit 0x7FF als Maske und 0x123 als Filter 1 und
Filter 2 eingestellt werden. Die Maske 0x7FF wählt alle 11 Identifier-Bits
zum Abgleich aus, so dass der Identifier exakt 0x123 sein muss um akzeptiert
zu werden.

Um Identifier 0x123 und 0x456 gleichzeitig zu akzeptieren kann Filter 2 auf
0x456 gesetzt und die Maske und Filter 1 beibehalten werden.

Der Standardmodus ist Accept-All.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Read Filter',
'elements': [('Mode', 'uint8', 1, 'out', ('Filter Mode', [('Disabled', 0),
                                                          ('Accept All', 1),
                                                          ('Match Standard', 2),
                                                          ('Match Standard And Data', 3),
                                                          ('Match Extended', 4)])),
             ('Mask', 'uint32', 1, 'out'),
             ('Filter1', 'uint32', 1, 'out'),
             ('Filter2', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the read filter as set by :func:`SetReadFilter`.
""",
'de':
"""
Gibt die Lesefilter zurück, wie von :func:`SetReadFilter` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Error Log',
'elements': [('Write Error Level', 'uint8', 1, 'out'),
             ('Read Error Level', 'uint8', 1, 'out'),
             ('Transceiver Disabled', 'bool', 1, 'out'), # FIXME: use bitmask instead to allow for future extensions?
             ('Write Timeout Count', 'uint32', 1, 'out'),
             ('Read Register Overflow Count', 'uint32', 1, 'out'), # FIXME: this is not exact, just a lower bound, because the Bricklet might not detect all overflows
             ('Read Buffer Overflow Count', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns information about different kinds of errors.

The write and read error levels indicate the current level of checksum,
acknowledgement, form, bit and stuffing errors during CAN bus write and read
operations.

When the write error level extends 255 then the CAN transceiver gets disabled
and no frames can be transmitted or received anymore. The CAN transceiver will
automatically be activated again after the CAN bus is idle for a while.

The write and read error levels are not available in read-only transceiver mode
(see :func:`SetConfiguration`) and are reset to 0 as a side effect of changing
the configuration or the read filter.

The write timeout, read register and buffer overflow counts represents the
number of these errors:

* A write timeout occurs if a frame could not be transmitted before the
  configured write timeout expired (see :func:`SetConfiguration`).
* A read register overflow occurs if the read register of the CAN transceiver
  still contains the last received frame when the next frame arrives. In this
  case the newly arrived frame is lost. This happens if the CAN transceiver
  receives more frames than the Bricklet can handle. Using the read filter
  (see :func:`SetReadFilter`) can help to reduce the amount of received frames.
* A read buffer overflow occurs if the read buffer of the Bricklet is already
  full when the next frame should be read from the read register of the CAN
  transceiver. In this case the frame in the read register is lost. This
  happens if the CAN transceiver receives more frames to be added to the read
  buffer than are removed from the read buffer using the :func:`ReadFrame`
  function. Using the :func:`FrameRead` callback ensures that the read buffer
  can never overflow.
""",
'de':
"""
Gibt Informationen über verschiedene Fehlerarten zurück.

Die Schreib- und Lesefehler-Level geben Aufschluss über das aktuelle Level
der Prüfsummen-, Acknowledgement-, Form-, Bit- und Stuffing-Fehler während
CAN-Bus Schreib- und Leseoperationen.

Wenn das Schreibfehler-Level 255 überschreitet dann wird der CAN-Transceiver
deaktiviert und es können keine Frames mehr übertragen und empfangen werden.
Wenn auf dem CAN-Bus für eine Weile Ruhe herrscht, dann wird der
CAN-Transceiver automatisch wieder aktiviert.

Die Schreib- und Lesefehler-Level Werte sind im Read-Only Transceiver-Modus
nicht verfügbar (see :func:`SetConfiguration`). Außerdem werden sie als
Seiteneffekt von Konfigurations- und Lesefilteränderungen auf 0 zurückgesetzt.

Die Werte für Schreib-Timeout, Lese-Register- und Lese-Buffer-Überlauf zählen
die Anzahl dieser Fehler:

* Ein Schreib-Timeout tritt dann auf, wenn ein Frame nicht übertragen werden
  konnte bevor der eingestellte Schreib-Timeout abgelaufen ist (siehe
  :func:`SetConfiguration`).
* Ein Lese-Register-Überlauf tritt dann auf, wenn im Lese-Register des
  CAN-Transceiver noch der zuletzt empfangen Frame steht wenn der nächste Frame
  ankommt. In diesem Fall geht der neu ankommende Frame verloren. Dies
  passiert, wenn der CAN-Transceiver mehr Frames empfängt als das Bricklet
  behandeln kann. Mit Hilfe des Lesefilters (siehe :func:`SetReadFilter`) kann
  die Anzahl der empfangen Frames verringert werden.
* Ein Lese-Buffer-Überlauf tritt dann auf, wenn der Lese-Buffer des Bricklets
  bereits voll ist und noch ein Frame vom Lese-Register des CAN-Transceiver
  gelesen werden soll. In diesem Fall geht der Frame im Lese-Register verloren.
  Dies passiert, wenn der CAN-Transceiver mehr Frames empfängt, die dem
  Lese-Buffer hinzugefügt werden sollen, als Frames mit der :func:`ReadFrame`
  Funktion aus dem Lese-Buffer entnommen werden. Die Verwendung des
  :func:`FrameRead` Callbacks stellt sicher, dass der Lese-Buffer niemals
  überlaufen kann.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Frame Read',
'elements': [('Frame Type', 'uint8', 1, 'out', ('Frame Type', [('Standard Data', 0),
                                                               ('Standard Remote', 1),
                                                               ('Extended Data', 2),
                                                               ('Extended Remote', 3)])),
             ('Identifier', 'uint32', 1, 'out'),
             ('Data', 'uint8', 8, 'out'),
             ('Length', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered if a data or remote frame was received by the CAN
transceiver.

For remote frames the ``data`` return value always contains invalid values.

A configurable read filter can be used to define which frames should be
received by the CAN transceiver at all (see :func:`SetReadFilter`).

To enable this callback, use :func:`EnableFrameReadCallback`.
""",
'de':
"""
Dieser Callback wird ausgelöst, sobald ein Data- oder Remote-Frame vom
CAN-Transceiver empfangen wurde.

Für Remote-Frames beinhalte der ``data`` Rückgabewerte immer ungültigen Werte.

Mittels eines einstellbaren Lesefilters kann festgelegt werden, welche Frames
von der CAN-Transceiver überhaupt empfangen werden sollen (siehe
:func:`SetReadFilter`).

Dieser Callback kann durch :func:`EnableFrameReadCallback` aktiviert werden.
"""
}]
})

com['examples'].append({
'name': 'Loopback',
'functions': [('setter', 'Set Configuration', [('uint8:constant', 7), ('uint8:constant', 1), ('int32', 0)], 'Configure transceiver for loopback mode', None),
              ('setter', 'Enable Frame Read Callback', [], 'Enable frame read callback', None)],
'cleanups': [('setter', 'Disable Frame Read Callback', [], None, None)],
'incomplete': True # because of callback with array parameter
})
