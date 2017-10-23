# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# NFC Bricklet communication config

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


READER_STATE = ('Reader State', [('Initialization', STATE_INITIALIZATION),
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
                                 ('Write Ndef', READER_STATE_WRITE_NDEF),
                                 ('Write Ndef Ready', READER_STATE_WRITE_NDEF_READY),
                                 ('Write Ndef Error', READER_STATE_WRITE_NDEF_ERROR),
                                 ('Request Ndef', READER_STATE_REQUEST_NDEF),
                                 ('Request Ndef Ready', READER_STATE_REQUEST_NDEF_READY),
                                 ('Request Ndef Error', READER_STATE_REQUEST_NDEF_ERROR)])

CARDEMU_STATE_DISCOVER = 2
CARDEMU_STATE_DISCOVER_READY = STATE_IDLE_MASK | CARDEMU_STATE_DISCOVER
CARDEMU_STATE_DISCOVER_ERROR = STATE_ERROR_MASK | CARDEMU_STATE_DISCOVER
CARDEMU_STATE_TRANSFER_NDEF = 3
CARDEMU_STATE_TRANSFER_NDEF_READY = STATE_IDLE_MASK | CARDEMU_STATE_TRANSFER_NDEF
CARDEMU_STATE_TRANSFER_NDEF_ERROR = STATE_ERROR_MASK | CARDEMU_STATE_TRANSFER_NDEF

CARDEMU_STATE = ('Cardemu State', [('Initialization', STATE_INITIALIZATION),
                                   ('Idle', STATE_IDLE),
                                   ('Error', STATE_ERROR),
                                   ('Discover', CARDEMU_STATE_DISCOVER),
                                   ('Discover Ready', CARDEMU_STATE_DISCOVER_READY),
                                   ('Discover Error', CARDEMU_STATE_DISCOVER_ERROR),
                                   ('Transfer Ndef', CARDEMU_STATE_TRANSFER_NDEF),
                                   ('Transfer Ndef Ready', CARDEMU_STATE_TRANSFER_NDEF_READY),
                                   ('Transfer Ndef Error', CARDEMU_STATE_TRANSFER_NDEF_ERROR)])

P2P_STATE_DISCOVER = 2
P2P_STATE_DISCOVER_READY = STATE_IDLE_MASK | P2P_STATE_DISCOVER
P2P_STATE_DISCOVER_ERROR = STATE_ERROR_MASK | P2P_STATE_DISCOVER
P2P_STATE_TRANSFER_NDEF = 3
P2P_STATE_TRANSFER_NDEF_READY = STATE_IDLE_MASK | P2P_STATE_TRANSFER_NDEF
P2P_STATE_TRANSFER_NDEF_ERROR = STATE_ERROR_MASK | P2P_STATE_TRANSFER_NDEF

P2P_STATE = ('P2P State', [('Initialization', STATE_INITIALIZATION),
                           ('Idle', STATE_IDLE),
                           ('Error', STATE_ERROR),
                           ('Discover', P2P_STATE_DISCOVER),
                           ('Discover Ready', P2P_STATE_DISCOVER_READY),
                           ('Discover Error', P2P_STATE_DISCOVER_ERROR),
                           ('Transfer Ndef', P2P_STATE_TRANSFER_NDEF),
                           ('Transfer Ndef Ready', P2P_STATE_TRANSFER_NDEF_READY),
                           ('Transfer Ndef Error', P2P_STATE_TRANSFER_NDEF_ERROR)])



MODE = ('Mode', [('Off',     0),
                 ('Cardemu', 1),
                 ('P2P',     2),
                 ('Reader',  3)])

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 286,
    'name': 'NFC',
    'display_name': 'NFC',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'TODO',
        'de': 'TODO'
    },
    'released': False,
    'documented': False,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Set Mode',
'elements': [('Mode', 'uint8', 1, 'in', MODE)],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Mode',
'elements': [('Mode', 'uint8', 1, 'out', MODE)],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
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
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Reader Get Tag ID Low Level',
'elements': [('Tag Type', 'uint8', 1, 'out', ('Tag Type', [('Mifare Classic', 0),
                                                           ('Type1', 1),
                                                           ('Type2', 2),
                                                           ('Type3', 3),
                                                           ('Type4', 4)])),
             ('Tag ID Length', 'uint8', 1, 'out'),
             ('Tag ID Data', 'uint8', 32, 'out')],
'high_level': {'stream_out': {'name': 'Tag ID', 'single_chunk': True}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the tag type, tag ID and the length of the tag ID
(4 or 7 bytes are possible length). This function can only be called if the
NFC Bricklet is currently in one of the *Ready* states. The returned ID
is the ID that was saved through the last call of :func:`Reader Request Tag ID`.

To get the tag ID of a tag the approach is as follows:

1. Call :func:`Reader Request Tag ID`
2. Wait for state to change to *RequestTagIDReady* (see :func:`Reader Get State` or
   :cb:`Reader State Changed` callback)
3. Call :func:`Reader Get Tag ID`
""",
'de':
"""
Gibt den Tag Typ, die Tag ID und die Länge der Tag ID (4 oder 7 Byte
möglich) zurück. Diese Funktion kann  nur aufgerufen werden wenn
sich das Bricklet gerade in einem der *Ready*-Zustände befindet. Die
zurückgegebene ID ist die letzte ID die durch einen Aufruf von
:func:`Reader Request Tag ID` gefunden wurde.

Der Ansatz um die Tag ID eines Tags zu bekommen sieht wie folgt aus:

1. Rufe :func:`Reader Request Tag ID` auf
2. Warte auf einen Zustandswechsel auf *RequestTagIDReady* (siehe
   :func:`Reader Get State` oder :cb:`Reader State Changed` Callback)
3. Rufe :func:`Reader Get Tag ID` auf
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Reader Get State',
'elements': [('State', 'uint8', 1, 'out', READER_STATE),
             ('Idle', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current state of the NFC Bricklet.

On startup the Bricklet will be in the *Initialization* state. The
initialization will only take about 20ms. After that it changes to *Idle*.

The functions of this Bricklet can be called in the *Idle* state and all of
the *Ready* and *Error* states.

Example: If you call :func:`Reader Request Page`, the state will change to
*RequestPage* until the reading of the page is finished. Then it will change
to either *RequestPageReady* if it worked or to *RequestPageError* if it
didn't. If the request worked you can get the page by calling :func:`Reader Read Page`.

The same approach is used analogously for the other API functions.
""",
'de':
"""
Gibt den aktuellen Zustand des NFC Bricklets aus.

Während der Startphase ist der Zustand *Initialization*. Die
Initialisierung dauert etwa 20ms. Danach ändert sich der Zustand zu
*Idle*.

Die Funktionen dieses Bricklets können aufgerufen werden wenn der Zustand
entweder *Idle* ist oder einer der *Ready* oder *Error*-Zustände
erreicht wurde.

Beispiel: Wenn :func:`Reader Request Page` aufgerufen wird, änder sich der
Zustand zu *RequestPage* solange der Leseprozess noch nicht abgeschlossen
ist. Danach ändert sich der Zustand zu *RequestPageReady* wenn das lesen
funktioniert hat oder zu *RequestPageError* wenn nicht. Wenn die Anfrage
erfolgreich war kann die Page mit :func:`Reader Read Page` abgerufen werden.

Der gleiche Ansatz kann analog für andere API Funktionen verwendet werden.
"""
}]
})




com['packets'].append({
'type': 'function',
'name': 'Reader Write Ndef Low Level',
'elements': [('Ndef Length', 'uint16', 1, 'in'),
             ('Ndef Chunk Offset', 'uint16', 1, 'in'),
             ('Ndef Chunk Data', 'uint8', 60, 'in')],
'high_level': {'stream_in': {'name': 'Ndef'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
works with type 2 and 4
has to be ndef formated already

""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Reader Request Ndef',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Reader Read Ndef Low Level',
'elements': [('Ndef Length', 'uint16', 1, 'out'),
             ('Ndef Chunk Offset', 'uint16', 1, 'out'),
             ('Ndef Chunk Data', 'uint8', 60, 'out')],
'high_level': {'stream_out': {'name': 'Ndef'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO

works with type 1-4
""",
'de':
"""
TODO
"""
}]
})







com['packets'].append({
'type': 'function',
'name': 'Reader Authenticate Mifare Classic Page',
'elements': [('Page', 'uint16', 1, 'in'),
             ('Key Number', 'uint8', 1, 'in', ('Key', [('A', 0),
                                                       ('B', 1)])),
             ('Key', 'uint8', 6, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO:
TODO: authenticating a page always authenticates a whole sector of 4 pages!
TODO:


Mifare Classic tags use authentication. If you want to read from or write to
a Mifare Classic page you have to authenticate it beforehand.
Each page can be authenticated with two keys: A (``key_number`` = 0) and B
(``key_number`` = 1). A new Mifare Classic
tag that has not yet been written to can can be accessed with key A
and the default key ``[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]``.

The approach to read or write a Mifare Classic page is as follows:

1. Call :func:`Reader Request Tag ID`
2. Wait for state to change to *RequestTagIDReady* (see :func:`Reader Get State`
   or :cb:`Reader State Changed` callback)
3. If looking for a specific tag then call :func:`Reader Get Tag ID` and check if the
   expected tag was found, if it was not found got back to step 1
4. Call :func:`Reader Authenticate Mifare Classic Page` with page and key for the page
5. Wait for state to change to *AuthenticatingMifareClassicPageReady* (see
   :func:`Reader Get State` or :cb:`Reader State Changed` callback)
6. Call :func:`Reader Request Page` or :func:`Reader Write Page` to read/write page
""",
'de':
"""
Mifare Classic Tags nutzen Authentifizierung. Wenn eine Page eines
Mifare Classic Tags gelesen oder geschrieben werden soll muss diese
zuvor Authentifiziert werden. Jede Page kann mit zwei Schlüsseln, A
(``key_number`` = 0) und B (``key_number`` = 1),
authentifiziert werden. Ein neues Mifare Classic Tag welches noch nicht
beschrieben wurde kann über Schlüssel A mit dem Standardschlüssel
``[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]`` genutzt werden.

Der Ansatz um eine Mifare Classic Page zu lesen oder zu schreiben sieht wie
folgt aus:

1. Rufe :func:`Reader Request Tag ID` auf
2. Warte auf einen Zustandswechsel auf *RequestTagIDReady* (siehe :func:`Reader Get State`
   oder :cb:`Reader State Changed` Callback)
3. Wenn mit einem bestimmten Tag gearbeitet werden soll, dann rufe
   :func:`Reader Get Tag ID` auf und überprüfe, ob der erwartete Tag gefunden wurde,
   wenn er nicht gefunden wurde mit Schritt 1 fortfahren
4. Rufe :func:`Reader Authenticate Mifare Classic Page` mit Page und Schlüssel für die
   Page auf
5. Warte auf einen Zustandswechsel auf *AuthenticatingMifareClassicPageReady*
   (siehe :func:`Reader Get State` oder :cb:`Reader State Changed` Callback)
6. Rufe :func:`Reader Request Page` oder :func:`Reader Write Page` zum Lesen/Schreiben einer
   Page auf
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Reader Write Page Low Level',
'elements': [('Page', 'uint16', 1, 'in', ('Reader Write', [('Type4 Capability Container', 3),
                                                           ('Type4 Ndef', 4)])),
             ('Data Length', 'uint16', 1, 'in'),
             ('Data Chunk Offset', 'uint16', 1, 'in'),
             ('Data Chunk Data', 'uint8', 58, 'in')],
'high_level': {'stream_in': {'name': 'Data'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes 16 bytes starting from the given page. How many pages are written
depends on the tag type. The page sizes are as follows:

* Mifare Classic page size: 16 byte (one page is written)
* NFC Forum Type 1 page size: 8 byte (two pages are written)
* NFC Forum Type 2 page size: 4 byte (four pages are written)
* NFC Forum Type 3 page size: 16 byte (one page is written)

* NFC Forum Type 4: no pages, page = file selection (cc or ndef)

The general approach for writing to a tag is as follows:

1. Call :func:`Reader Request Tag ID`
2. Wait for state to change to *RequestTagIDReady* (see :func:`Reader Get State` or
   :cb:`Reader State Changed` callback)
3. If looking for a specific tag then call :func:`Reader Get Tag ID` and check if the
   expected tag was found, if it was not found got back to step 1
4. Call :func:`Reader Write Page` with page number and data
5. Wait for state to change to *WritePageReady* (see :func:`Reader Get State` or
   :cb:`Reader State Changed` callback)

If you use a Mifare Classic tag you have to authenticate a page before you
can write to it. See :func:`Reader Authenticate Mifare Classic Page`.
""",
'de':
"""
Schreibt 16 Bytes startend von der übergebenen Page. Wie viele Pages
dadurch geschrieben werden hängt vom Typ des Tags ab. Die Pagegrößen
verhalten sich wie folgt:

* Mifare Classic Pagegröße: 16 byte (eine Page wird geschrieben)
* NFC Forum Type 1 Pagegröße: 8 byte (zwei Pages werden geschrieben)
* NFC Forum Type 2 Pagegröße: 4 byte (vier Pages werden geschrieben)

Der generelle Ansatz zum Schreiben eines Tags sieht wie folgt aus:

1. Rufe :func:`Reader Request Tag ID` auf
2. Warte auf einen Zustandswechsel auf *RequestTagIDReady* (siehe
   :func:`Reader Get State` oder :cb:`Reader State Changed` callback)
3. Wenn mit einem bestimmten Tag gearbeitet werden soll, dann rufe
   :func:`Reader Get Tag ID` auf und überprüfe, ob der erwartete Tag gefunden wurde,
   wenn er nicht gefunden wurde mit Schritt 1 fortfahren
4. Rufe :func:`Reader Write Page` mit der Page sowie den zu schreibenden Daten auf
5. Warte auf einen Zustandswechsel auf *WritePageReady* (siehe
   :func:`Reader Get State` oder :cb:`Reader State Changed` Callback)

Wenn ein Mifare Classic Tag verwendet wird muss die Page authentifiziert
werden bevor sie geschrieben werden kann. Siehe
:func:`Reader Authenticate Mifare Classic Page`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Reader Request Page',
'elements': [('Page', 'uint16', 1, 'in', ('Reader Request', [('Type4 Capability Container', 3),
                                                             ('Type4 Ndef', 4)])),
             ('Length', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Reads 16 bytes starting from the given page and stores them into a buffer.
The buffer can then be read out with :func:`Reader Read Page`.
How many pages are read depends on the tag type. The page sizes are
as follows:

* Mifare Classic page size: 16 byte (one page is read)
* NFC Forum Type 1 page size: 8 byte (two pages are read)
* NFC Forum Type 2 page size: 4 byte (four pages are read)

The general approach for reading a tag is as follows:

1. Call :func:`Reader Request Tag ID`
2. Wait for state to change to *RequestTagIDReady* (see :func:`Reader Get State`
   or :cb:`Reader State Changed` callback)
3. If looking for a specific tag then call :func:`Reader Get Tag ID` and check if the
   expected tag was found, if it was not found got back to step 1
4. Call :func:`Reader Request Page` with page number
5. Wait for state to change to *RequestPageReady* (see :func:`Reader Get State`
   or :cb:`Reader State Changed` callback)
6. Call :func:`Reader Read Page` to retrieve the page from the buffer

If you use a Mifare Classic tag you have to authenticate a page before you
can read it. See :func:`Reader Authenticate Mifare Classic Page`.
""",
'de':
"""
Liest 16 Bytes startend von der übergebenen Page und speichert sie in
einem Buffer. Dieser Buffer kann mit :func:`Reader Read Page` ausgelesen werden.
Wie viele Pages dadurch gelesen werden hängt vom Typ des Tags ab.
Die Pagegrößen verhalten sich wie folgt:

* Mifare Classic Pagegröße: 16 byte (eine Page wird gelesen)
* NFC Forum Type 1 Pagegröße: 8 byte (zwei Pages werden gelesen)
* NFC Forum Type 2 Pagegröße: 4 byte (vier Pages werden gelesen)

Der generelle Ansatz zum Lesen eines Tags sieht wie folgt aus:

1. Rufe :func:`Reader Request Tag ID` auf
2. Warte auf einen Zustandswechsel auf *RequestTagIDReady* (siehe
   :func:`Reader Get State` oder :cb:`Reader State Changed` Callback)
3. Wenn mit einem bestimmten Tag gearbeitet werden soll, dann rufe
   :func:`Reader Get Tag ID` auf und überprüfe, ob der erwartete Tag gefunden wurde,
   wenn er nicht gefunden wurde mit Schritt 1 fortfahren
4. Rufe :func:`Reader Request Page` mit der zu lesenden Page auf
5. Warte auf einen Zustandswechsel auf *RequestPageReady* (siehe
   :func:`Reader Get State` oder :cb:`Reader State Changed` Callback)
6. Rufe :func:`Reader Read Page` auf um die gespeicherte Page abzufragen

Wenn ein Mifare Classic Tag verwendet wird muss die Page authentifiziert
werden bevor sie gelesen werden kann. Siehe :func:`Reader Authenticate Mifare Classic Page`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Reader Read Page Low Level',
'elements': [('Data Length', 'uint16', 1, 'out'),
             ('Data Chunk Offset', 'uint16', 1, 'out'),
             ('Data Chunk Data', 'uint8', 60, 'out')],
'high_level': {'stream_out': {'name': 'Data'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Reader State Changed',
'elements': [('State', 'uint8', 1, 'out', READER_STATE),
             ('Idle', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called if the state of the NFC Bricklet changes.
See :func:`Reader Get State` for more information about the possible states.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Zustand des NFC Bricklets
sich verändert. Siehe :func:`Reader Get State` für mehr Informationen
über die möglichen Zustände des Bricklets.
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Cardemu Get State',
'elements': [('State', 'uint8', 1, 'out', CARDEMU_STATE),
             ('Idle', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
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
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Cardemu Write Ndef Low Level',
'elements': [('Ndef Length', 'uint16', 1, 'in'),
             ('Ndef Chunk Offset', 'uint16', 1, 'in'),
             ('Ndef Chunk Data', 'uint8', 60, 'in')],
'high_level': {'stream_in': {'name': 'Ndef'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Cardemu Start Transfer',
'elements': [('Transfer', 'uint8', 1, 'in', ('Cardemu Transfer', [('Abort', 0),
                                                                  ('Write', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Cardemu State Changed',
'elements': [('State', 'uint8', 1, 'out', CARDEMU_STATE),
             ('Idle', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'P2P Get State',
'elements': [('State', 'uint8', 1, 'out', P2P_STATE),
             ('Idle', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
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
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'P2P Write Ndef Low Level',
'elements': [('Ndef Length', 'uint16', 1, 'in'),
             ('Ndef Chunk Offset', 'uint16', 1, 'in'),
             ('Ndef Chunk Data', 'uint8', 60, 'in')],
'high_level': {'stream_in': {'name': 'Ndef'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'P2P Start Transfer',
'elements': [('Transfer', 'uint8', 1, 'in', ('P2P Transfer', [('Abort', 0),
                                                              ('Write', 1),
                                                              ('Read', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'P2P Read Ndef Low Level',
'elements': [('Ndef Length', 'uint16', 1, 'out'),
             ('Ndef Chunk Offset', 'uint16', 1, 'out'),
             ('Ndef Chunk Data', 'uint8', 60, 'out')],
'high_level': {'stream_out': {'name': 'Ndef'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'P2P State Changed',
'elements': [('State', 'uint8', 1, 'out', P2P_STATE),
             ('Idle', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Detection LED Config',
'elements': [('Config', 'uint8', 1, 'in', ('Detection LED Config', [('Off', 0),
                                                                    ('On', 1),
                                                                    ('Show Heartbeat', 2),
                                                                    ('Show Detection', 3)]))],
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

Die LED kann auch permanaent an/aus gestellt werden oder einen Herzschlag anzeigen.

Wenn das Bricklet sich im Bootlodermodus befindet ist die LED aus.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Detection LED Config',
'elements': [('Config', 'uint8', 1, 'out', ('Detection LED Config', [('Off', 0),
                                                                     ('On', 1),
                                                                     ('Show Heartbeat', 2),
                                                                     ('Show Detection', 3)]))],
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
