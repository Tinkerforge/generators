# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# NFC Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'category': 'Bricklet',
    'device_identifier': 286,
    'name': 'NFC',
    'display_name': 'NFC',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'NFC tag read/write, NFC P2P and Card Emulation',
        'de': 'NFC Tag Lesen/Schreiben, NFC P2P und Card Emulation'
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
'name': 'Mode',
'type': 'uint8',
'constants': [('Off', 0),
              ('Cardemu', 1),
              ('P2P', 2),
              ('Reader', 3)]
})

com['constant_groups'].append({
'name': 'Tag Type',
'type': 'uint8',
'constants': [('Mifare Classic', 0),
              ('Type1', 1),
              ('Type2', 2),
              ('Type3', 3),
              ('Type4', 4)]
})

STATE_IDLE_MASK = (1 << 7)
STATE_ERROR_MASK = ((1 << 7) | (1 << 6))

STATE_INITIALIZATION = 0
STATE_IDLE = STATE_IDLE_MASK
STATE_ERROR = STATE_ERROR_MASK

READER_STATE_REQUEST_TAG_ID = 2
READER_STATE_REQUEST_TAG_ID_READY = STATE_IDLE_MASK | READER_STATE_REQUEST_TAG_ID
READER_STATE_REQUEST_TAG_ID_ERROR = STATE_ERROR_MASK | READER_STATE_REQUEST_TAG_ID
READER_STATE_AUTHENTICATE_MIFARE_CLASSIC_PAGE = 3
READER_STATE_AUTHENTICATE_MIFARE_CLASSIC_PAGE_READY = STATE_IDLE_MASK | READER_STATE_AUTHENTICATE_MIFARE_CLASSIC_PAGE
READER_STATE_AUTHENTICATE_MIFARE_CLASSIC_PAGE_ERROR = STATE_ERROR_MASK | READER_STATE_AUTHENTICATE_MIFARE_CLASSIC_PAGE
READER_STATE_WRITE_PAGE = 4
READER_STATE_WRITE_PAGE_READY = STATE_IDLE_MASK | READER_STATE_WRITE_PAGE
READER_STATE_WRITE_PAGE_ERROR = STATE_ERROR_MASK | READER_STATE_WRITE_PAGE
READER_STATE_REQUEST_PAGE = 5
READER_STATE_REQUEST_PAGE_READY = STATE_IDLE_MASK | READER_STATE_REQUEST_PAGE
READER_STATE_REQUEST_PAGE_ERROR = STATE_ERROR_MASK | READER_STATE_REQUEST_PAGE
READER_STATE_WRITE_NDEF = 6
READER_STATE_WRITE_NDEF_READY = STATE_IDLE_MASK | READER_STATE_WRITE_NDEF
READER_STATE_WRITE_NDEF_ERROR = STATE_ERROR_MASK | READER_STATE_WRITE_NDEF
READER_STATE_REQUEST_NDEF = 7
READER_STATE_REQUEST_NDEF_READY = STATE_IDLE_MASK | READER_STATE_REQUEST_NDEF
READER_STATE_REQUEST_NDEF_ERROR = STATE_ERROR_MASK | READER_STATE_REQUEST_NDEF

com['constant_groups'].append({
'name': 'Reader State',
'type': 'uint8',
'constants': [('Initialization', STATE_INITIALIZATION),
              ('Idle', STATE_IDLE),
              ('Error', STATE_ERROR),
              ('Request Tag ID', READER_STATE_REQUEST_TAG_ID),
              ('Request Tag ID Ready', READER_STATE_REQUEST_TAG_ID_READY),
              ('Request Tag ID Error', READER_STATE_REQUEST_TAG_ID_ERROR),
              ('Authenticate Mifare Classic Page', READER_STATE_AUTHENTICATE_MIFARE_CLASSIC_PAGE),
              ('Authenticate Mifare Classic Page Ready', READER_STATE_AUTHENTICATE_MIFARE_CLASSIC_PAGE_READY),
              ('Authenticate Mifare Classic Page Error', READER_STATE_AUTHENTICATE_MIFARE_CLASSIC_PAGE_ERROR),
              ('Write Page', READER_STATE_WRITE_PAGE),
              ('Write Page Ready', READER_STATE_WRITE_PAGE_READY),
              ('Write Page Error', READER_STATE_WRITE_PAGE_ERROR),
              ('Request Page', READER_STATE_REQUEST_PAGE),
              ('Request Page Ready', READER_STATE_REQUEST_PAGE_READY),
              ('Request Page Error', READER_STATE_REQUEST_PAGE_ERROR),
              ('Write NDEF', READER_STATE_WRITE_NDEF),
              ('Write NDEF Ready', READER_STATE_WRITE_NDEF_READY),
              ('Write NDEF Error', READER_STATE_WRITE_NDEF_ERROR),
              ('Request NDEF', READER_STATE_REQUEST_NDEF),
              ('Request NDEF Ready', READER_STATE_REQUEST_NDEF_READY),
              ('Request NDEF Error', READER_STATE_REQUEST_NDEF_ERROR)]
})

CARDEMU_STATE_DISCOVER = 2
CARDEMU_STATE_DISCOVER_READY = STATE_IDLE_MASK | CARDEMU_STATE_DISCOVER
CARDEMU_STATE_DISCOVER_ERROR = STATE_ERROR_MASK | CARDEMU_STATE_DISCOVER
CARDEMU_STATE_TRANSFER_NDEF = 3
CARDEMU_STATE_TRANSFER_NDEF_READY = STATE_IDLE_MASK | CARDEMU_STATE_TRANSFER_NDEF
CARDEMU_STATE_TRANSFER_NDEF_ERROR = STATE_ERROR_MASK | CARDEMU_STATE_TRANSFER_NDEF

com['constant_groups'].append({
'name': 'Key',
'type': 'uint8',
'constants': [('A', 0),
              ('B', 1)]
})

com['constant_groups'].append({
'name': 'Reader Write',
'type': 'uint16',
'constants': [('Type4 Capability Container', 3),
              ('Type4 NDEF', 4)]
})

com['constant_groups'].append({
'name': 'Reader Request',
'type': 'uint16',
'constants': [('Type4 Capability Container', 3),
              ('Type4 NDEF', 4)]
})

com['constant_groups'].append({
'name': 'Cardemu State',
'type': 'uint8',
'constants': [('Initialization', STATE_INITIALIZATION),
              ('Idle', STATE_IDLE),
              ('Error', STATE_ERROR),
              ('Discover', CARDEMU_STATE_DISCOVER),
              ('Discover Ready', CARDEMU_STATE_DISCOVER_READY),
              ('Discover Error', CARDEMU_STATE_DISCOVER_ERROR),
              ('Transfer NDEF', CARDEMU_STATE_TRANSFER_NDEF),
              ('Transfer NDEF Ready', CARDEMU_STATE_TRANSFER_NDEF_READY),
              ('Transfer NDEF Error', CARDEMU_STATE_TRANSFER_NDEF_ERROR)]
})

com['constant_groups'].append({
'name': 'Cardemu Transfer',
'type': 'uint8',
'constants': [('Abort', 0),
              ('Write', 1)]
})

P2P_STATE_DISCOVER = 2
P2P_STATE_DISCOVER_READY = STATE_IDLE_MASK | P2P_STATE_DISCOVER
P2P_STATE_DISCOVER_ERROR = STATE_ERROR_MASK | P2P_STATE_DISCOVER
P2P_STATE_TRANSFER_NDEF = 3
P2P_STATE_TRANSFER_NDEF_READY = STATE_IDLE_MASK | P2P_STATE_TRANSFER_NDEF
P2P_STATE_TRANSFER_NDEF_ERROR = STATE_ERROR_MASK | P2P_STATE_TRANSFER_NDEF

com['constant_groups'].append({
'name': 'P2P State',
'type': 'uint8',
'constants': [('Initialization', STATE_INITIALIZATION),
              ('Idle', STATE_IDLE),
              ('Error', STATE_ERROR),
              ('Discover', P2P_STATE_DISCOVER),
              ('Discover Ready', P2P_STATE_DISCOVER_READY),
              ('Discover Error', P2P_STATE_DISCOVER_ERROR),
              ('Transfer NDEF', P2P_STATE_TRANSFER_NDEF),
              ('Transfer NDEF Ready', P2P_STATE_TRANSFER_NDEF_READY),
              ('Transfer NDEF Error', P2P_STATE_TRANSFER_NDEF_ERROR)]
})

com['constant_groups'].append({
'name': 'P2P Transfer',
'type': 'uint8',
'constants': [('Abort', 0),
              ('Write', 1),
              ('Read', 2)]
})

com['constant_groups'].append({
'name': 'Detection LED Config',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Show Heartbeat', 2),
              ('Show Detection', 3)]
})

com['packets'].append({
'type': 'function',
'name': 'Set Mode',
'elements': [('Mode', 'uint8', 1, 'in', {'constant_group': 'Mode', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the mode. The NFC Bricklet supports four modes:

* Off
* Card Emulation (Cardemu): Emulates a tag for other readers
* Peer to Peer (P2P): Exchange data with other readers
* Reader: Reads and writes tags

If you change a mode, the Bricklet will reconfigure the hardware for this mode.
Therefore, you can only use functions corresponding to the current mode. For
example, in Reader mode you can only use Reader functions.
""",
'de':
"""
Setzt den Modus. Das NFC Bricklet unterstützt vier Modi:

* Off (Aus)
* Card Emulation (Cardemu): Emuliert einen Tag für andere Reader
* Peer to Peer (P2P): Datenaustausch mit anderen Readern
* Reader: Liest und schreibt Tags

Wenn der Modus geändert wird, dann rekonfiguriert das Bricklet die Hardware für
den gewählten Modus. Daher können immer nur die dem Modus zugehörigen Funktionen
verwendet werden. Es können also im Reader Modus nur die Reader Funktionen
verwendet werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Mode',
'elements': [('Mode', 'uint8', 1, 'out', {'constant_group': 'Mode', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the mode as set by :func:`Set Mode`.
""",
'de':
"""
Gibt den aktuellen Modus zurück, wie von :func:`Set Mode` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Reader Request Tag ID',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
After you call :func:`Reader Request Tag ID` the NFC Bricklet will try to read
the tag ID from the tag. After this process is done the state will change.
You can either register the :cb:`Reader State Changed` callback or you can poll
:func:`Reader Get State` to find out about the state change.

If the state changes to *ReaderRequestTagIDError* it means that either there was
no tag present or that the tag has an incompatible type. If the state
changes to *ReaderRequestTagIDReady* it means that a compatible tag was found
and that the tag ID has been saved. You can now read out the tag ID by
calling :func:`Reader Get Tag ID`.

If two tags are in the proximity of the NFC Bricklet, this
function will cycle through the tags. To select a specific tag you have
to call :func:`Reader Request Tag ID` until the correct tag ID is found.

In case of any *ReaderError* state the selection is lost and you have to
start again by calling :func:`Reader Request Tag ID`.
""",
'de':
"""
Um ein Tag welches sich in der nähe des NFC Bricklets befindet zu
lesen oder zu schreiben muss zuerst diese Funktion mit dem erwarteten
Tag Typ aufgerufen werden. Es ist kein Problem wenn der Typ nicht bekannt
ist. Es ist möglich die verfügbaren Tag Typen einfach nacheinander
durchzutesten bis das Tag antwortet.

Aktuell werden die folgenden Tag Typen unterstützt:

* Mifare Classic
* NFC Forum Type 1
* NFC Forum Type 2
* NFC Forum Type 3
* NFC Forum Type 4

Beim Aufruf von :func:`Reader Request Tag ID` versucht das NFC Bricklet die Tag ID
eines Tags auszulesen. Nachdem dieser Prozess beendet ist ändert sich
der Zustand des Bricklets. Es ist möglich den :cb:`Reader State Changed` Callback zu
registrieren oder den Zustand über :func:`Reader Get State` zu pollen.

Wenn der Zustand auf *ReaderRequestTagIDError* wechselt ist ein Fehler aufgetreten.
Dies bedeutet, dass entweder kein Tag oder kein Tag vom passenden Typ gefunden
werden konnte. Wenn der Zustand auf *ReaderRequestTagIDReady* wechselt ist ein
kompatibles Tag gefunden worden und die Tag ID wurde gespeichert. Die
Tag ID kann nun über :func:`Reader Get Tag ID` ausgelesen werden.

Wenn sich zwei Tags gleichzeitig in der Nähe des NFC Bricklets befinden
werden diese nacheinander ausgelesen. Um ein spezifisches Tag zu selektieren
muss :func:`Reader Request Tag ID` so lange aufgerufen werden bis das korrekte Tag
gefunden wurde.

Falls sich das NFC Bricklet in einem der *ReaderError* Zustände befindet
ist die Selektion aufgehoben und :func:`Reader Request Tag ID` muss erneut
aufgerufen werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Reader Get Tag ID Low Level',
'elements': [('Tag Type', 'uint8', 1, 'out', {'constant_group': 'Tag Type'}),
             ('Tag ID Length', 'uint8', 1, 'out', {'range': (0, 32)}),
             ('Tag ID Data', 'uint8', 32, 'out', {})],
'high_level': {'stream_out': {'name': 'Tag ID', 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the tag type and the tag ID. This function can only be called if the
NFC Bricklet is currently in one of the *ReaderReady* states. The returned tag ID
is the tag ID that was saved through the last call of :func:`Reader Request Tag ID`.

To get the tag ID of a tag the approach is as follows:

1. Call :func:`Reader Request Tag ID`
2. Wait for state to change to *ReaderRequestTagIDReady* (see :func:`Reader Get State` or
   :cb:`Reader State Changed` callback)
3. Call :func:`Reader Get Tag ID`
""",
'de':
"""
Gibt den Tag Typ und die Tag ID zurück. Diese Funktion kann nur aufgerufen werden wenn
sich das Bricklet gerade in einem der *ReaderReady*-Zustände befindet. Die
zurückgegebene tag ID ist die letzte tag ID die durch einen Aufruf von
:func:`Reader Request Tag ID` gefunden wurde.

Der Ansatz um die Tag ID eines Tags zu bekommen sieht wie folgt aus:

1. Rufe :func:`Reader Request Tag ID` auf
2. Warte auf einen Zustandswechsel auf *ReaderRequestTagIDReady* (siehe
   :func:`Reader Get State` oder :cb:`Reader State Changed` Callback)
3. Rufe :func:`Reader Get Tag ID` auf
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Reader Get State',
'elements': [('State', 'uint8', 1, 'out', {'constant_group': 'Reader State'}),
             ('Idle', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current reader state of the NFC Bricklet.

On startup the Bricklet will be in the *ReaderInitialization* state. The
initialization will only take about 20ms. After that it changes to *ReaderIdle*.

The Bricklet is also reinitialized if the mode is changed, see :func:`Set Mode`.

The functions of this Bricklet can be called in the *ReaderIdle* state and all of
the *ReaderReady* and *ReaderError* states.

Example: If you call :func:`Reader Request Page`, the state will change to
*ReaderRequestPage* until the reading of the page is finished. Then it will change
to either *ReaderRequestPageReady* if it worked or to *ReaderRequestPageError* if it
didn't. If the request worked you can get the page by calling :func:`Reader Read Page`.

The same approach is used analogously for the other API functions.
""",
'de':
"""
Gibt den aktuellen Reader Zustand des NFC Bricklets aus.

Während der Startphase ist der Zustand *ReaderInitialization*. Die
Initialisierung dauert etwa 20ms. Danach ändert sich der Zustand zu
*ReaderIdle*.

Das Bricklet wird auch neu initialisiert wenn der Modus geändert wird, siehe
:func:`Set Mode`.

Die Funktionen dieses Bricklets können aufgerufen werden wenn der Zustand
entweder *ReaderIdle* ist oder einer der *ReaderReady* oder *ReaderError*-Zustände
erreicht wurde.

Beispiel: Wenn :func:`Reader Request Page` aufgerufen wird, ändert sich der
Zustand zu *ReaderRequestPage* solange der Leseprozess noch nicht abgeschlossen
ist. Danach ändert sich der Zustand zu *ReaderRequestPageReady* wenn das Lesen
funktioniert hat oder zu *ReaderRequestPageError* wenn nicht. Wenn die Anfrage
erfolgreich war kann die Page mit :func:`Reader Read Page` abgerufen werden.

Der gleiche Ansatz kann analog für andere API Funktionen verwendet werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Reader Write NDEF Low Level',
'elements': [('NDEF Length', 'uint16', 1, 'in', {'range': (0, 8192)}),
             ('NDEF Chunk Offset', 'uint16', 1, 'in', {}),
             ('NDEF Chunk Data', 'uint8', 60, 'in', {})],
'high_level': {'stream_in': {'name': 'NDEF'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes NDEF formated data.

This function currently supports NFC Forum Type 2 and 4.

The general approach for writing a NDEF message is as follows:

1. Call :func:`Reader Request Tag ID`
2. Wait for state to change to *ReaderRequestTagIDReady* (see
   :func:`Reader Get State` or :cb:`Reader State Changed` callback)
3. If looking for a specific tag then call :func:`Reader Get Tag ID` and check
   if the expected tag was found, if it was not found got back to step 1
4. Call :func:`Reader Write NDEF` with the NDEF message that you want to write
5. Wait for state to change to *ReaderWriteNDEFReady* (see :func:`Reader Get State`
   or :cb:`Reader State Changed` callback)
""",
'de':
"""
Schreibt NDEF formatierte Daten.

Diese Funktion unterstützt aktuell NFC Forum Type 2 und 4.

Der Ansatz um eine NDEF Nachricht zu schreiben sieht wie folgt aus:

1. Rufe :func:`Reader Request Tag ID` auf
2. Warte auf einen Zustandswechsel auf *ReaderRequestTagIDReady* (siehe
   :func:`Reader Get State` oder :cb:`Reader State Changed` Callback)
3. Wenn mit einem bestimmten Tag gearbeitet werden soll, dann rufe
   :func:`Reader Get Tag ID` auf und überprüfe, ob der erwartete Tag gefunden
   wurde, wenn er nicht gefunden wurde mit Schritt 1 fortfahren
4. Rufe :func:`Reader Write NDEF` mit der zu schreibenden NDEF Nachricht auf
5. Warte auf einen Zustandswechsel auf *ReaderWriteNDEFReady*
   (siehe :func:`Reader Get State` oder :cb:`Reader State Changed` Callback)
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Reader Request NDEF',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Reads NDEF formated data from a tag.

This function currently supports NFC Forum Type 1, 2, 3 and 4.

The general approach for reading a NDEF message is as follows:

1. Call :func:`Reader Request Tag ID`
2. Wait for state to change to *RequestTagIDReady* (see :func:`Reader Get State`
   or :cb:`Reader State Changed` callback)
3. If looking for a specific tag then call :func:`Reader Get Tag ID` and check if the
   expected tag was found, if it was not found got back to step 1
4. Call :func:`Reader Request NDEF`
5. Wait for state to change to *ReaderRequestNDEFReady* (see :func:`Reader Get State`
   or :cb:`Reader State Changed` callback)
6. Call :func:`Reader Read NDEF` to retrieve the NDEF message from the buffer
""",
'de':
"""
Liest NDEF formatierten Daten von einem Tag.

Diese Funktion unterstützt aktuell NFC Forum Type 1, 2, 3 und 4.

Der Ansatz um eine NDEF Nachricht zu lesen sieht wie folgt aus:

1. Rufe :func:`Reader Request Tag ID` auf
2. Warte auf einen Zustandswechsel auf *ReaderRequestTagIDReady* (siehe
   :func:`Reader Get State` oder :cb:`Reader State Changed` Callback)
3. Wenn mit einem bestimmten Tag gearbeitet werden soll, dann rufe
   :func:`Reader Get Tag ID` auf und überprüfe, ob der erwartete Tag gefunden
   wurde, wenn er nicht gefunden wurde mit Schritt 1 fortfahren
4. Rufe :func:`Reader Request NDEF` auf
5. Warte auf einen Zustandswechsel auf *ReaderRequestNDEFReady*
   (siehe :func:`Reader Get State` oder :cb:`Reader State Changed` Callback)
6. Rufe :func:`Reader Read NDEF` auf um die gespeicherte NDEF Nachricht abzufragen
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Reader Read NDEF Low Level',
'elements': [('NDEF Length', 'uint16', 1, 'out', {'range': (0, 8192)}),
             ('NDEF Chunk Offset', 'uint16', 1, 'out', {}),
             ('NDEF Chunk Data', 'uint8', 60, 'out', {})],
'high_level': {'stream_out': {'name': 'NDEF'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the NDEF data from an internal buffer. To fill the buffer
with a NDEF message you have to call :func:`Reader Request NDEF` beforehand.
""",
'de':
"""
Gibt NDEF Daten aus einem internen Buffer zurück. Der Buffer
kann zuvor mit einer NDEF Nachricht über einen Aufruf von
:func:`Reader Request NDEF` gefüllt werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Reader Authenticate Mifare Classic Page',
'elements': [('Page', 'uint16', 1, 'in', {}),
             ('Key Number', 'uint8', 1, 'in', {'constant_group': 'Key'}),
             ('Key', 'uint8', 6, 'in', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Mifare Classic tags use authentication. If you want to read from or write to
a Mifare Classic page you have to authenticate it beforehand.
Each page can be authenticated with two keys: A (``key_number`` = 0) and B
(``key_number`` = 1). A new Mifare Classic
tag that has not yet been written to can be accessed with key A
and the default key ``[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]``.

The approach to read or write a Mifare Classic page is as follows:

1. Call :func:`Reader Request Tag ID`
2. Wait for state to change to *ReaderRequestTagIDReady* (see :func:`Reader Get State`
   or :cb:`Reader State Changed` callback)
3. If looking for a specific tag then call :func:`Reader Get Tag ID` and check if the
   expected tag was found, if it was not found got back to step 1
4. Call :func:`Reader Authenticate Mifare Classic Page` with page and key for the page
5. Wait for state to change to *ReaderAuthenticatingMifareClassicPageReady* (see
   :func:`Reader Get State` or :cb:`Reader State Changed` callback)
6. Call :func:`Reader Request Page` or :func:`Reader Write Page` to read/write page

The authentication will always work for one whole sector (4 pages).
""",
'de':
"""
Mifare Classic Tags nutzen Authentifizierung. Wenn eine Page eines
Mifare Classic Tags gelesen oder geschrieben werden soll muss diese
zuvor authentifiziert werden. Jede Page kann mit zwei Schlüsseln, A
(``key_number`` = 0) und B (``key_number`` = 1),
authentifiziert werden. Ein neuer Mifare Classic Tag welches noch nicht
beschrieben wurde kann über Schlüssel A mit dem Standardschlüssel
``[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]`` genutzt werden.

Der Ansatz um eine Mifare Classic Page zu lesen oder zu schreiben sieht wie
folgt aus:

1. Rufe :func:`Reader Request Tag ID` auf
2. Warte auf einen Zustandswechsel auf *ReaderRequestTagIDReady* (siehe :func:`Reader Get State`
   oder :cb:`Reader State Changed` Callback)
3. Wenn mit einem bestimmten Tag gearbeitet werden soll, dann rufe
   :func:`Reader Get Tag ID` auf und überprüfe, ob der erwartete Tag gefunden wurde,
   wenn er nicht gefunden wurde mit Schritt 1 fortfahren
4. Rufe :func:`Reader Authenticate Mifare Classic Page` mit Page und Schlüssel für die
   Page auf
5. Warte auf einen Zustandswechsel auf *ReaderAuthenticatingMifareClassicPageReady*
   (siehe :func:`Reader Get State` oder :cb:`Reader State Changed` Callback)
6. Rufe :func:`Reader Request Page` oder :func:`Reader Write Page` zum Lesen/Schreiben einer
   Page auf

Die Authentifizierung bezieht sich immer auf einen ganzen Sektor (4 Pages).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Reader Write Page Low Level',
'elements': [('Page', 'uint16', 1, 'in', {'constant_group': 'Reader Write'}),
             ('Data Length', 'uint16', 1, 'in', {'range': (0, 8192)}),
             ('Data Chunk Offset', 'uint16', 1, 'in', {}),
             ('Data Chunk Data', 'uint8', 58, 'in', {})],
'high_level': {'stream_in': {'name': 'Data'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes a maximum of 8192 bytes starting from the given page. How many pages are written
depends on the tag type. The page sizes are as follows:

* Mifare Classic page size: 16 byte
* NFC Forum Type 1 page size: 8 byte
* NFC Forum Type 2 page size: 4 byte
* NFC Forum Type 3 page size: 16 byte
* NFC Forum Type 4: No pages, page = file selection (CC or NDEF, see below)

The general approach for writing to a tag is as follows:

1. Call :func:`Reader Request Tag ID`
2. Wait for state to change to *ReaderRequestTagIDReady* (see :func:`Reader Get State` or
   :cb:`Reader State Changed` callback)
3. If looking for a specific tag then call :func:`Reader Get Tag ID` and check if the
   expected tag was found, if it was not found got back to step 1
4. Call :func:`Reader Write Page` with page number and data
5. Wait for state to change to *ReaderWritePageReady* (see :func:`Reader Get State` or
   :cb:`Reader State Changed` callback)

If you use a Mifare Classic tag you have to authenticate a page before you
can write to it. See :func:`Reader Authenticate Mifare Classic Page`.

NFC Forum Type 4 tags are not organized into pages but different files. We currently
support two files: Capability Container file (CC) and NDEF file.

Choose CC by setting page to 3 or NDEF by setting page to 4.
""",
'de':
"""
Schreibt maximal 8192 Bytes beginnend von der übergebenen Page. Wie viele Pages
dadurch geschrieben werden hängt vom Typ des Tags ab. Die Pagegrößen
verhalten sich wie folgt:

* Mifare Classic Pagegröße: 16 byte
* NFC Forum Type 1 Pagegröße: 8 byte
* NFC Forum Type 2 Pagegröße: 4 byte
* NFC Forum Type 3 Pagegröße: 16 byte
* NFC Forum Type 4: Keine Pages, Page = Dateiwahl (CC oder NDEF, siehe unten)

Der generelle Ansatz zum Schreiben eines Tags sieht wie folgt aus:

1. Rufe :func:`Reader Request Tag ID` auf
2. Warte auf einen Zustandswechsel auf *RequestTagIDReady* (siehe
   :func:`Reader Get State` oder :cb:`Reader State Changed` callback)
3. Wenn mit einem bestimmten Tag gearbeitet werden soll, dann rufe
   :func:`Reader Get Tag ID` auf und überprüfe, ob der erwartete Tag gefunden wurde,
   wenn er nicht gefunden wurde mit Schritt 1 fortfahren
4. Rufe :func:`Reader Write Page` mit der Page sowie den zu schreibenden Daten auf
5. Warte auf einen Zustandswechsel auf *ReaderWritePageReady* (siehe
   :func:`Reader Get State` oder :cb:`Reader State Changed` Callback)

Wenn ein Mifare Classic Tag verwendet wird muss die Page authentifiziert
werden bevor sie geschrieben werden kann. Siehe
:func:`Reader Authenticate Mifare Classic Page`.

NFC Forum Type 4 Tags sind nicht in Pages organisiert sondern Dateien. Wir
unterstützten aktuell zwei Dateien: Capability Container (CC) und NDEF.

Setze Page auf 3 um CC zu wählen und auf 4 um NDEF zu wählen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Reader Request Page',
'elements': [('Page', 'uint16', 1, 'in', {'constant_group': 'Reader Request'}),
             ('Length', 'uint16', 1, 'in', {'range': (0, 8192)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Reads a maximum of 8192 bytes starting from the given page and stores them into a buffer.
The buffer can then be read out with :func:`Reader Read Page`.
How many pages are read depends on the tag type. The page sizes are
as follows:

* Mifare Classic page size: 16 byte
* NFC Forum Type 1 page size: 8 byte
* NFC Forum Type 2 page size: 4 byte
* NFC Forum Type 3 page size: 16 byte
* NFC Forum Type 4: No pages, page = file selection (CC or NDEF, see below)

The general approach for reading a tag is as follows:

1. Call :func:`Reader Request Tag ID`
2. Wait for state to change to *RequestTagIDReady* (see :func:`Reader Get State`
   or :cb:`Reader State Changed` callback)
3. If looking for a specific tag then call :func:`Reader Get Tag ID` and check if the
   expected tag was found, if it was not found got back to step 1
4. Call :func:`Reader Request Page` with page number
5. Wait for state to change to *ReaderRequestPageReady* (see :func:`Reader Get State`
   or :cb:`Reader State Changed` callback)
6. Call :func:`Reader Read Page` to retrieve the page from the buffer

If you use a Mifare Classic tag you have to authenticate a page before you
can read it. See :func:`Reader Authenticate Mifare Classic Page`.

NFC Forum Type 4 tags are not organized into pages but different files. We currently
support two files: Capability Container file (CC) and NDEF file.

Choose CC by setting page to 3 or NDEF by setting page to 4.
""",
'de':
"""
Liest maximal 8192 Bytes beginnend von der übergebenen Page und speichert sie in
einem Buffer. Dieser Buffer kann mit :func:`Reader Read Page` ausgelesen werden.
Wie viele Pages dadurch gelesen werden hängt vom Typ des Tags ab.
Die Pagegrößen verhalten sich wie folgt:

* Mifare Classic Pagegröße: 16 byte
* NFC Forum Type 1 Pagegröße: 8 byte
* NFC Forum Type 2 Pagegröße: 4 byte
* NFC Forum Type 3 Pagegröße: 16 byte
* NFC Forum Type 4: Keine Pages, Page = Dateiwahl (CC oder NDEF, siehe unten)

Der generelle Ansatz zum Lesen eines Tags sieht wie folgt aus:

1. Rufe :func:`Reader Request Tag ID` auf
2. Warte auf einen Zustandswechsel auf *RequestTagIDReady* (siehe
   :func:`Reader Get State` oder :cb:`Reader State Changed` Callback)
3. Wenn mit einem bestimmten Tag gearbeitet werden soll, dann rufe
   :func:`Reader Get Tag ID` auf und überprüfe, ob der erwartete Tag gefunden wurde,
   wenn er nicht gefunden wurde mit Schritt 1 fortfahren
4. Rufe :func:`Reader Request Page` mit der zu lesenden Page auf
5. Warte auf einen Zustandswechsel auf *ReaderRequestPageReady* (siehe
   :func:`Reader Get State` oder :cb:`Reader State Changed` Callback)
6. Rufe :func:`Reader Read Page` auf um die gespeicherte Page abzufragen

Wenn ein Mifare Classic Tag verwendet wird muss die Page authentifiziert
werden bevor sie gelesen werden kann. Siehe :func:`Reader Authenticate Mifare Classic Page`.

NFC Forum Type 4 Tags sind nicht in Pages organisiert sondern Dateien. Wir
unterstützten aktuell zwei Dateien: Capability Container (CC) und NDEF.

Setze Page auf 3 um CC zu wählen und auf 4 um NDEF zu wählen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Reader Read Page Low Level',
'elements': [('Data Length', 'uint16', 1, 'out', {'range': (0, 8192)}),
             ('Data Chunk Offset', 'uint16', 1, 'out'),
             ('Data Chunk Data', 'uint8', 60, 'out')],
'high_level': {'stream_out': {'name': 'Data'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the page data from an internal buffer. To fill the buffer
with specific pages you have to call :func:`Reader Request Page` beforehand.
""",
'de':
"""
Gibt Daten aus einem internen Buffer zurück. Der Buffer
kann zuvor mit spezifischen Pages über einen Aufruf von
:func:`Reader Request Page` gefüllt werden.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Reader State Changed',
'elements': [('State', 'uint8', 1, 'out', {'constant_group': 'Reader State'}),
             ('Idle', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called if the reader state of the NFC Bricklet changes.
See :func:`Reader Get State` for more information about the possible states.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Reader-Zustand des NFC Bricklets
sich verändert. Siehe :func:`Reader Get State` für mehr Informationen
über die möglichen Zustände des Bricklets.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Cardemu Get State',
'elements': [('State', 'uint8', 1, 'out', {'constant_group': 'Cardemu State'}),
             ('Idle', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current cardemu state of the NFC Bricklet.

On startup the Bricklet will be in the *CardemuInitialization* state. The
initialization will only take about 20ms. After that it changes to *CardemuIdle*.

The Bricklet is also reinitialized if the mode is changed, see :func:`Set Mode`.

The functions of this Bricklet can be called in the *CardemuIdle* state and all of
the *CardemuReady* and *CardemuError* states.

Example: If you call :func:`Cardemu Start Discovery`, the state will change to
*CardemuDiscover* until the discovery is finished. Then it will change
to either *CardemuDiscoverReady* if it worked or to *CardemuDiscoverError* if it
didn't.

The same approach is used analogously for the other API functions.
""",
'de':
"""
Gibt den aktuellen Cardemu-Zustand des NFC Bricklets aus.

Während der Startphase ist der Zustand *CardemuInitialization*. Die
Initialisierung dauert etwa 20ms. Danach ändert sich der Zustand zu
*CardmeuIdle*.

Das Bricklet wird auch neu initialisiert wenn der Modus geändert wird, siehe :func:`Set Mode`.

Die Funktionen dieses Bricklets können aufgerufen werden wenn der Zustand
entweder *CardemuIdle* ist oder einer der *CardemuReady* oder *CardemuError*-Zustände
erreicht wurde.

Beispiel: Wenn :func:`Cardemu Start Discovery` aufgerufen wird, änder sich der
Zustand zu *CardemuDiscover* solange der Discover-Prozess noch nicht abgeschlossen
ist. Danach ändert sich der Zustand zu *CardemuDiscoverReady* wenn der Discover-Prozess
funktioniert hat oder zu *CardemuDiscoverError* wenn nicht.

Der gleiche Ansatz kann analog für andere API Funktionen verwendet werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Cardemu Start Discovery',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Starts the discovery process. If you call this function while a NFC
reader device is near to the NFC Bricklet the state will change from
*CardemuDiscovery* to *CardemuDiscoveryReady*.

If no NFC reader device can be found or if there is an error during
discovery the cardemu state will change to *CardemuDiscoveryError*. In this case you
have to restart the discovery process.

If the cardemu state changes to *CardemuDiscoveryReady* you can start the NDEF message
transfer with :func:`Cardemu Write NDEF` and :func:`Cardemu Start Transfer`.
""",
'de':
"""
Startet den Discovery Prozess. Wenn diese Funktion aufgerufen wird während
ein NFC Lesegerät sich in Reichweite befindet, dann wechselt
der Cardemu Zustand von *CardemuDiscovery* nach *CardemuDiscoveryReady*.

Falls kein NFC Lesegerät gefunden werden kann oder während des Discovery
Prozesses ein Fehler auftritt dann wechselt der Cardemu Zustand zu *CardemuDiscoveryReady*.
In diesem Fall muss der Discovery Prozess.

Wenn der Cardemu Zustand zu *CardemuDiscoveryReady* wechselt kann eine NDEF Nachricht
mittels :func:`Cardemu Write NDEF` und :func:`Cardemu Start Transfer` übertragen werden.
"""
}]
})

# NOTE: Even though a single NDEF record can contain a payload of 2^32 - 1 bytes
#       and streaming APIs support data length of 2^16 - 1 bytes, because of limitations
#       of the NFC API used in the firmware only short NDEF records with maximum
#       payload size of 255 bytes work.
com['packets'].append({
'type': 'function',
'name': 'Cardemu Write NDEF Low Level',
'elements': [('NDEF Length', 'uint16', 1, 'in', {'range': (0, 255)}),
             ('NDEF Chunk Offset', 'uint16', 1, 'in'),
             ('NDEF Chunk Data', 'uint8', 60, 'in')],
'high_level': {'stream_in': {'name': 'NDEF'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes the NDEF messages that is to be transferred to the NFC peer.

The maximum supported NDEF message size in Cardemu mode is 255 byte.

You can call this function at any time in Cardemu mode. The internal buffer
will not be overwritten until you call this function again or change the
mode.
""",
'de':
"""
Schreibt eine NDEF Nachricht die an einen NFC Peer übertragen werden soll.

Die maximale NDEF Nachrichtengröße im Cardemu-Modus beträgt 255 Byte.

Diese Funktion kann im Cardemu-Modus jederzeit aufgerufen werden. Der interne
Buffer wird nicht überschrieben solange diese Funktion nicht erneut aufgerufen
oder der Modus nicht gewechselt wird.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Cardemu Start Transfer',
'elements': [('Transfer', 'uint8', 1, 'in', {'constant_group': 'Cardemu Transfer'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
You can start the transfer of a NDEF message if the cardemu state is *CardemuDiscoveryReady*.

Before you call this function to start a write transfer, the NDEF message that
is to be transferred has to be written via :func:`Cardemu Write NDEF` first.

After you call this function the state will change to *CardemuTransferNDEF*. It will
change to *CardemuTransferNDEFReady* if the transfer was successful or
*CardemuTransferNDEFError* if it wasn't.
""",
'de':
"""
Der Transfer einer NDEF Nachricht kann im Cardemu-Zustand *CardemuDiscoveryReady*
gestartet werden.

Bevor ein Schreib-Transfer gestartet werden kann muss zuerst die zu
übertragenden NDEF Nachricht mittels :func:`Cardemu Write NDEF` geschrieben werden.

Nach einem Aufruf dieser Funktion ändert sich der Cardemu-Zustand zu *CardemuTransferNDEF*.
Danach ändert sich der P2P Zustand zu *CardemuTransferNDEFReady* wenn der Transfer
erfolgreich war oder zu *CardemuTransferNDEFError* falls nicht.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Cardemu State Changed',
'elements': [('State', 'uint8', 1, 'out', {'constant_group': 'Cardemu State'}),
             ('Idle', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called if the cardemu state of the NFC Bricklet changes.
See :func:`Cardemu Get State` for more information about the possible states.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der Cardemu-Zustand des NFC Bricklets
sich verändert. Siehe :func:`Cardemu Get State` für mehr Informationen
über die möglichen Zustände des Bricklets.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'P2P Get State',
'elements': [('State', 'uint8', 1, 'out', {'constant_group': 'P2P State'}),
             ('Idle', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current P2P state of the NFC Bricklet.

On startup the Bricklet will be in the *P2PInitialization* state. The
initialization will only take about 20ms. After that it changes to *P2PIdle*.

The Bricklet is also reinitialized if the mode is changed, see :func:`Set Mode`.

The functions of this Bricklet can be called in the *P2PIdle* state and all of
the *P2PReady* and *P2PError* states.

Example: If you call :func:`P2P Start Discovery`, the state will change to
*P2PDiscover* until the discovery is finished. Then it will change
to either P2PDiscoverReady* if it worked or to *P2PDiscoverError* if it
didn't.

The same approach is used analogously for the other API functions.
""",
'de':
"""
Gibt den aktuellen P2P-Zustand des NFC Bricklets aus.

Während der Startphase ist der Zustand *P2PInitialization*. Die
Initialisierung dauert etwa 20ms. Danach ändert sich der Zustand zu
*P2PIdle*.

Das Bricklet wird auch neu Initialisiert wenn der Modus geändert wird, siehe :func:`Set Mode`.

Die Funktionen dieses Bricklets können aufgerufen werden wenn der Zustand
entweder *P2PIdle* ist oder einer der *P2PReady* oder *P2PError*-Zustände
erreicht wurde.

Beispiel: Wenn :func:`P2P Start Discovery` aufgerufen wird, änder sich der
Zustand zu *P2PDiscover* solange der Discover-Prozess noch nicht abgeschlossen
ist. Danach ändert sich der Zustand zu *P2PDiscoverReady* wenn der Discover-Prozess
funktioniert hat oder zu *P2PDiscoverError* wenn nicht.

Der gleiche Ansatz kann analog für andere API Funktionen verwendet werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'P2P Start Discovery',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Starts the discovery process. If you call this function while another NFC
P2P enabled device is near to the NFC Bricklet the state will change from
*P2PDiscovery* to *P2PDiscoveryReady*.

If no NFC P2P enabled device can be found or if there is an error during
discovery the P2P state will change to *P2PDiscoveryError*. In this case you
have to restart the discovery process.

If the P2P state changes to *P2PDiscoveryReady* you can start the NDEF message
transfer with :func:`P2P Start Transfer`.
""",
'de':
"""
Startet den Discovery Prozess. Wenn diese Funktion aufgerufen wird während
ein anderes NFC P2P fähiges Gerät sich in Reichweite befindet, dann wechselt
der P2P Zustand von *P2PDiscovery* nach *P2PDiscoveryReady*.

Falls kein NFC P2P fähiges Gerät gefunden werden kann oder während des Discovery
Prozesses ein Fehler auftritt dann wechselt der P2P Zustand zu *P2PDiscoveryError*.
In diesem Fall muss der Discovery Prozess.

Wenn der P2P Zustand zu *P2PDiscoveryReady* wechselt kann eine NDEF Nachricht
mittels :func:`P2P Write NDEF` und :func:`P2P Start Transfer` übertragen werden.
"""
}]
})

# NOTE: Even though a single NDEF record can contain a payload of 2^32 - 1 bytes
#       and streaming APIs support data length of 2^16 - 1 bytes, because of limitations
#       of the NFC API used in the firmware only short NDEF records with maximum
#       payload size of 255 bytes work.
com['packets'].append({
'type': 'function',
'name': 'P2P Write NDEF Low Level',
'elements': [('NDEF Length', 'uint16', 1, 'in', {'range': (0, 255)}),
             ('NDEF Chunk Offset', 'uint16', 1, 'in', {}),
             ('NDEF Chunk Data', 'uint8', 60, 'in', {})],
'high_level': {'stream_in': {'name': 'NDEF'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes the NDEF messages that is to be transferred to the NFC peer.

The maximum supported NDEF message size for P2P transfer is 255 byte.

You can call this function at any time in P2P mode. The internal buffer
will not be overwritten until you call this function again, change the
mode or use P2P to read an NDEF messages.
""",
'de':
"""
Schreibt eine NDEF Nachricht die an einen NFC Peer übertragen werden soll.

Die maximale NDEF Nachrichtengröße für P2P Übertragungen beträgt 255 Byte.

Diese Funktion kann im P2P-Modus jederzeit aufgerufen werden. Der interne
Buffer wird nicht überschrieben solange diese Funktion nicht erneut aufgerufen,
der Modus nicht gewechselt oder über P2P eine NDEF Nachricht gelesen wird.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'P2P Start Transfer',
'elements': [('Transfer', 'uint8', 1, 'in', {'constant_group': 'P2P Transfer'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
You can start the transfer of a NDEF message if the P2P state is *P2PDiscoveryReady*.

Before you call this function to start a write transfer, the NDEF message that
is to be transferred has to be written via :func:`P2P Write NDEF` first.

After you call this function the P2P state will change to *P2PTransferNDEF*. It will
change to *P2PTransferNDEFReady* if the transfer was successfull or
*P2PTransferNDEFError* if it wasn't.

If you started a write transfer you are now done. If you started a read transfer
you can now use :func:`P2P Read NDEF` to read the NDEF message that was written
by the NFC peer.
""",
'de':
"""
Der Transfer einer NDEF Nachricht kann im P2P Zustand *P2PDiscoveryReady* gestartet
werden.

Bevor ein Schreib-Transfer gestartet werden kann muss zuerst die zu
übertragenden NDEF Nachricht mittels :func:`P2P Write NDEF` geschrieben werden.

Nach einem Aufruf dieser Funktion ändert sich der P2P Zustand zu *P2PTransferNDEF*.
Danach ändert sich der P2P Zustand zu *P2PTransferNDEFReady* wenn der Transfer
erfolgreich war oder zu *P2PTransferNDEFError* falls nicht.

Ein Schreib-Transfer ist danach abgeschlossen. Bei einem Lese-Transfer kann jetzt
die vom NFC Peer geschriebene NDEF Nachricht mittels :func:`P2P Read NDEF`
ausgelesen werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'P2P Read NDEF Low Level',
'elements': [('NDEF Length', 'uint16', 1, 'out', {'range': (0, 8192)}),
             ('NDEF Chunk Offset', 'uint16', 1, 'out', {}),
             ('NDEF Chunk Data', 'uint8', 60, 'out', {})],
'high_level': {'stream_out': {'name': 'NDEF'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the NDEF message that was written by a NFC peer in NFC P2P mode.

The NDEF message is ready if you called :func:`P2P Start Transfer` with a
read transfer and the P2P state changed to *P2PTransferNDEFReady*.
""",
'de':
"""
Gibt die NDEF Nachricht zurück, die von einem NFC Peer im P2P Modus geschrieben
wurde.

Die NDEF Nachricht ist bereit sobald sich nach einem :func:`P2P Start Transfer`
Aufruf mit einem Lese-Transfer der P2P Zustand zu *P2PTransferNDEFReady* ändert.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'P2P State Changed',
'elements': [('State', 'uint8', 1, 'out', {'constant_group': 'P2P State'}),
             ('Idle', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called if the P2P state of the NFC Bricklet changes.
See :func:`P2P Get State` for more information about the possible states.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn der P2P-Zustand des NFC Bricklets
sich verändert. Siehe :func:`P2P Get State` für mehr Informationen
über die möglichen Zustände des Bricklets.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Detection LED Config',
'elements': [('Config', 'uint8', 1, 'in', {'constant_group': 'Detection LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the detection LED configuration. By default the LED shows
if a card/reader is detected.

You can also turn the LED permanently on/off or show a heartbeat.

If the Bricklet is in bootloader mode, the LED is off.
""",
'de':
"""
Setzt die Konfiguration der Kommunikations-LED. Standardmäßig zeigt
die LED ob eine Karte/ein Lesegerät detektiert wurde.

Die LED kann auch permanent an/aus gestellt werden oder einen Herzschlag anzeigen.

Wenn das Bricklet sich im Bootloadermodus befindet ist die LED aus.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Detection LED Config',
'elements': [('Config', 'uint8', 1, 'out', {'constant_group': 'Detection LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Detection LED Config`
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Detection LED Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Maximum Timeout',
'elements': [('Timeout', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 2000})],
'since_firmware': [2, 0, 1],
'doc': ['af', {
'en':
"""
Sets the maximum timeout.

This is a global maximum used for all internal state timeouts. The timeouts depend heavily
on the used tags etc. For example: If you use a Type 2 tag and you want to detect if
it is present, you have to use :func:`Reader Request Tag ID` and wait for the state
to change to either the error state or the ready state.

With the default configuration this takes 2-3 seconds. By setting the maximum timeout to
100ms you can reduce this time to ~150-200ms. For Type 2 this would also still work
with a 20ms timeout (a Type 2 tag answers usually within 10ms). A type 4 tag can take
up to 500ms in our tests.

If you need a fast response time to discover if a tag is present or not you can find
a good timeout value by trial and error for your specific tag.

By default we use a very conservative timeout, to be sure that any tag can always
answer in time.
""",
'de':
"""
Setzt den maximalen Timeout.

Dies ist das globale Maximum für die internen State-Timeouts. Der korrekte Timeout hängt
vom verwendeten Tag Typ ab. Zum Beispiel: Wenn ein Typ 2 Tag verwendet wird und herausgefunden
werden soll ob der Tag in Reichweite des Bricklets ist, muss :func:`Reader Request Tag ID`
aufgerufen werden. Der State wechselt dann entweder auf Ready oder Error (Tag gefunden/nicht
gefunden).

Mit den Standardeinstellungen dauert dies ca. 2-3 Sekunden. Wenn man das maximale Timeout
auf 100ms setzt reduziert sich diese zeit auf ~150-200ms. Für Typ 2 funktioniert das auch
noch mit einem Timeout von 20ms (Ein Typ 2 Tag antwortet für gewöhnlich innerhalb von 10ms).
Ein Typ 4 Tag benötigte bis zu 500ms in unsren Tests.

Wenn eine schnelle reaktionszeit benötigt wird, kann das Timeout entsprechend verrigert werden
einen guten Wert kann man per Trial-and-Error für einen spezfiischen Tag-Typ ermitteln.

Standardmäßig nutzen wir einen sehr konservativen Timeout um sicher zu stellen das alle
Tags definitiv funktionieren.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Maximum Timeout',
'elements': [('Timeout', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 2000})],
'since_firmware': [2, 0, 1],
'doc': ['af', {
'en':
"""
Returns the timeout as set by :func:`Set Maximum Timeout`
""",
'de':
"""
Gibt das Timeout zurück, wie von :func:`Set Maximum Timeout` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Scan For Tags',
'functions': [('callback', ('Reader State Changed', 'reader state changed'), [(('State', 'State'), 'uint8', 1, None, None, None), (('Idle', 'Idle'), 'bool', 1, None, None, None)], None, None),
              ('setter', 'Set Mode', [('uint8:constant', 3)], 'Enable reader mode', None)],
'incomplete': True # because of special logic in callback
})

com['examples'].append({
'name': 'Emulate NDEF',
'functions': [('callback', ('Cardemu State Changed', 'cardemu state changed'), [(('State', 'State'), 'uint8', 1, None, None, None), (('Idle', 'Idle'), 'bool', 1, None, None, None)], None, None),
              ('setter', 'Set Mode', [('uint8:constant', 1)], 'Enable cardemu mode', None)],
'incomplete': True # because of special logic in callback
})

com['examples'].append({
'name': 'Write Read Type2',
'functions': [('callback', ('Reader State Changed', 'reader state changed'), [(('State', 'State'), 'uint8', 1, None, None, None), (('Idle', 'Idle'), 'bool', 1, None, None, None)], None, None),
              ('setter', 'Set Mode', [('uint8:constant', 3)], 'Enable reader mode', None)],
'incomplete': True # because of special logic in callback
})
