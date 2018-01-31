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
        'en': 'NFC tag read/write, NFC P2P and Card Emulation',
        'de': 'NFC Tag lesen/Schreiben, NFC P2P und Card Emulation'
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
'name': 'Set Mode',
'elements': [('Mode', 'uint8', 1, 'in', MODE)],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the mode. The NFC Bricklet supports four modes:

* Off 
* Card Emulation (In this mode the Bricklet appears to be a tag for another reader)
* Peer to Peer (In this mode it is possible to exchange data with other readers)
* Reader (In this mode you can read from tags and write to tags)

If you change a mode, the Bricklet will completely reinitialize with this mode. So
you can for example only use the "cardemu"-functions in Card Emulation mode.

The default mode is "off".
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
To read or write a tag that is in proximity of the NFC/RFID Bricklet you
first have to call this function with the expected tag type as parameter.
It is no problem if you don't know the tag type. You can cycle through
the available tag types until the tag gives an answer to the request.

Currently the following tag types are supported:

* Mifare Classic
* NFC Forum Type 1
* NFC Forum Type 2
* NFC Forum Type 3
* NFC Forum Type 4

After you call :func:`Reader Request Tag ID` the NFC/RFID Bricklet will try to read
the tag ID from the tag. After this process is done the state will change.
You can either register the :cb:`Reader State Changed` callback or you can poll
:func:`Reader Get State` to find out about the state change.

If the state changes to *ReaderRequestTagIDError* it means that either there was
no tag present or that the tag is of an incompatible type. If the state
changes to *ReaderRequestTagIDReady* it means that a compatible tag was found
and that the tag ID could be read out. You can now get the tag ID by
calling :func:`Reader Get Tag ID`.

If two tags are in the proximity of the NFC/RFID Bricklet, this
function will cycle through the tags. To select a specific tag you have
to call :func:`Reader Request Tag ID` until the correct tag id is found.

In case of any *Error* state the selection is lost and you have to
start again by calling :func:`Reader Request Tag ID`.
""",
'de':
"""
Um ein Tag welches sich in der nähe des NFC/RFID Bricklets befindet zu
lesen oder zu schreiben muss zuerst diese Funktion mit dem erwarteten
Tag Typ aufgerufen werden. Es ist kein Problem wenn der Typ nicht bekannt
ist. Es ist möglich die verügbaren Tag Typen einfach nacheinander
durchzutesten bis das Tag antwortet.

Aktuell werden die folgenden Tag Typen unterstützt:

* Mifare Classic
* NFC Forum Type 1
* NFC Forum Type 2
* NFC Forum Type 3
* NFC Forum Type 4

Beim Aufruf von :func:`Reader Request Tag ID` probiert das NFC/RFID Bricklet die Tag ID
eines Tags auszulesen. Nachdem dieser Prozess beendet ist ändert sich
der Zustand des Bricklets. Es ist möglich den :cb:`Reader State Changed` Callback zu
registrieren oder den Zustand über :func:`Reader Get State` zu pollen.

Wenn der Zustand auf *ReaderRequestTagIDError* wechselt ist ein Fehler aufgetreten.
Dies bedeutet, dass entweder kein Tag oder kein Tag vom passenden Typ gefunden
werden konnte. Wenn der Zustand auf *Reader RequestTagIDReady* wechselt ist ein
kompatibles Tag gefunden worden und die Tag ID wurde gespeichert. Die
Tag ID kann nun über :func:`Reader Get Tag ID` ausgelesen werden.

Wenn sich zwei Tags gleichzeitig in der Nähe des NFC/RFID Bricklets befinden
werden diese nacheinander ausgelesen. Um ein spezifisches Tag zu selektieren
muss :func:`Reader Request Tag ID` so lange aufgerufen werden bis das korrekte Tag
gefunden wurde.

Falls sich das NFC/RFID Bricklet in einem der *ReaderError* Zustände befindet
ist die Selektion aufgehoben und :func:`Reader Request Tag ID` muss erneut
aufgerufen werden.
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
Returns the tag type, tag ID and the length of the tag ID. 
This function can only be called if the
NFC Bricklet is currently in one of the *Ready* states. The returned ID
is the ID that was saved through the last call of :func:`Reader Request Tag ID`.

To get the tag ID of a tag the approach is as follows:

1. Call :func:`Reader Request Tag ID`
2. Wait for state to change to *ReaderRequestTagIDReady* (see :func:`Reader Get State` or
   :cb:`Reader State Changed` callback)
3. Call :func:`Reader Get Tag ID`
""",
'de':
"""
Gibt den Tag Typ, die Tag ID und die Länge der Tag ID zurück.
Diese Funktion kann nur aufgerufen werden wenn
sich das Bricklet gerade in einem der *ReaderReady*-Zustände befindet. Die
zurückgegebene ID ist die letzte ID die durch einen Aufruf von
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
'elements': [('State', 'uint8', 1, 'out', READER_STATE),
             ('Idle', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current state of the NFC Bricklet if in reader mode.

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
Gibt den aktuellen Zustand des NFC Bricklets aus.

Während der Startphase ist der Zustand *ReaderInitialization*. Die
Initialisierung dauert etwa 20ms. Danach ändert sich der Zustand zu
*ReaderIdle*.

Das Bricklet wird auch neu Initialisiert wenn der Modus geändert wird, siehe :func:`Set Mode`.

Die Funktionen dieses Bricklets können aufgerufen werden wenn der Zustand
entweder *ReaderIdle* ist oder einer der *ReaderReady* oder *ReaderError*-Zustände
erreicht wurde.

Beispiel: Wenn :func:`Reader Request Page` aufgerufen wird, änder sich der
Zustand zu *ReaderRequestPage* solange der Leseprozess noch nicht abgeschlossen
ist. Danach ändert sich der Zustand zu *ReaderRequestPageReady* wenn das lesen
funktioniert hat oder zu *ReaderRequestPageError* wenn nicht. Wenn die Anfrage
erfolgreich war kann die Page mit :func:`Reader Read Page` abgerufen werden.

Der gleiche Ansatz kann analog für andere API Funktionen verwendet werden.
"""
}]
})




# NOTE: Even though a single NDEF record can contain a payload of 2^32 - 1 bytes
#       and streaming APIs support data length of 2^16 - 1 bytes, because of limitations
#       of the NFC API used in the firmware only short NDEF records with maximum
#       payload size of 255 bytes work.
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
Writes Ndef formated data with a maximum of 255 bytes.

This function currently supports NFC Forum Type 2 and 4.

The general approach for writing a Ndef message is as follows:

1. Call :func:`Reader Request Tag ID`
2. Wait for state to change to *ReaderRequestTagIDReady* (see :func:`Reader Get State` or
   :cb:`Reader State Changed` callback)
3. If looking for a specific tag then call :func:`Reader Get Tag ID` and check if the
   expected tag was found, if it was not found got back to step 1
4. Call :func:`Reader Write Ndef` with the Ndef message that you want to write
5. Wait for state to change to *ReaderWriteNdefReady* (see :func:`Reader Get State` or
   :cb:`Reader State Changed` callback)
""",
'de':
"""
TODO
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
Reads Ndef formated data from a tag.

This function currently supports NFC Forum Type 1, 2, 3 and 4.

The general approach for reading a Ndef message is as follows:

1. Call :func:`Reader Request Tag ID`
2. Wait for state to change to *RequestTagIDReady* (see :func:`Reader Get State`
   or :cb:`Reader State Changed` callback)
3. If looking for a specific tag then call :func:`Reader Get Tag ID` and check if the
   expected tag was found, if it was not found got back to step 1
4. Call :func:`Reader Request Ndef`
5. Wait for state to change to *ReaderRequestNdefReady* (see :func:`Reader Get State`
   or :cb:`Reader State Changed` callback)
6. Call :func:`Reader Read Ndef` to retrieve the Ndef message from the buffer
""",
'de':
"""
TODO
"""
}]
})

# NOTE: Even though a single NDEF record can contain a payload of 2^32 - 1 bytes
#       and streaming APIs support data length of 2^16 - 1 bytes, because of limitations
#       of the NFC API used in the firmware only short NDEF records with maximum
#       payload size of 255 bytes work.
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
Returns the Ndef data from an internal buffer. To fill the buffer
with a Ndef message you have to call :func:`Reader Request Ndef` beforehand.

The buffer can have a size of up to 8192 bytes.
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
zuvor Authentifiziert werden. Jede Page kann mit zwei Schlüsseln, A
(``key_number`` = 0) und B (``key_number`` = 1),
authentifiziert werden. Ein neues Mifare Classic Tag welches noch nicht
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
Writes a maximum of 8192 bytes starting from the given page. How many pages are written
depends on the tag type. The page sizes are as follows:

* Mifare Classic page size: 16 byte
* NFC Forum Type 1 page size: 8 byte
* NFC Forum Type 2 page size: 4 byte
* NFC Forum Type 3 page size: 16 byte
* NFC Forum Type 4: No pages, page = file selection (CC or Ndef, see below)

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
support two files: Capability Container file (CC) and Ndef file.

Choose CC by setting page to 3 or Ndef by setting page to 4.
""",
'de':
"""
Schreibt maximal 8192 Bytes startend von der übergebenen Page. Wie viele Pages
dadurch geschrieben werden hängt vom Typ des Tags ab. Die Pagegrößen
verhalten sich wie folgt:

* Mifare Classic Pagegröße: 16 byte
* NFC Forum Type 1 Pagegröße: 8 byte
* NFC Forum Type 2 Pagegröße: 4 byte
* NFC Forum Type 3 Pagegröße: 16 byte
* NFC Forum Type 4: Keine Pages, Page = Dateiwahl (CC oder Ndef, siehe unten)

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
unterstützten aktuell zwei Dateien: Capability Container (CC) und Ndef.

Setze Page auf 3 um CC zu wählen und auf 4 um Ndef zu wählen.
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
Reads a maximum of 8192 bytes starting from the given page and stores them into a buffer.
The buffer can then be read out with :func:`Reader Read Page`.
How many pages are read depends on the tag type. The page sizes are
as follows:

* Mifare Classic page size: 16 byte
* NFC Forum Type 1 page size: 8 byte
* NFC Forum Type 2 page size: 4 byte 
* NFC Forum Type 3 page size: 16 byte
* NFC Forum Type 4: No pages, page = file selection (CC or Ndef, see below)

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
support two files: Capability Container file (CC) and Ndef file.

Choose CC by setting page to 3 or Ndef by setting page to 4.
""",
'de':
"""
Liest maximal 8192 Bytes startend von der übergebenen Page und speichert sie in
einem Buffer. Dieser Buffer kann mit :func:`Reader Read Page` ausgelesen werden.
Wie viele Pages dadurch gelesen werden hängt vom Typ des Tags ab.
Die Pagegrößen verhalten sich wie folgt:

* Mifare Classic Pagegröße: 16 byte
* NFC Forum Type 1 Pagegröße: 8 byte
* NFC Forum Type 2 Pagegröße: 4 byte
* NFC Forum Type 3 Pagegröße: 16 byte
* NFC Forum Type 4: Keine Pages, Page = Dateiwahl (CC oder Ndef, siehe unten)


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
unterstützten aktuell zwei Dateien: Capability Container (CC) und Ndef.

Setze Page auf 3 um CC zu wählen und auf 4 um Ndef zu wählen.
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
Returns the page data from an internal buffer. To fill the buffer
with specific pages you have to call :func:`Reader Request Page` beforehand.

The buffer can have a size of up to 8192 bytes.
""",
'de':
"""
Gibt Daten aus einem internen Buffer zurück. Der Buffer
kann zuvor mit spezifischen Pages über einen Aufruf von
:func:`Reader Request Page` gefüllt werden.

Der Buffer kann eine Größe von bis zu 8192 Bytes haben.
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
This callback is called if the reader state of the NFC Bricklet changes.
See :func:`Reader Get State` for more information about the possible states.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Reader-Zustand des NFC Bricklets
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
Returns the current state of the NFC Bricklet if in card emulation mode.

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
Gibt den aktuellen Zustand des NFC Bricklets aus wenn es sich im Cardemu-Modus befindet.

Während der Startphase ist der Zustand *CardemuInitialization*. Die
Initialisierung dauert etwa 20ms. Danach ändert sich der Zustand zu
*CardmeuIdle*.

Das Bricklet wird auch neu Initialisiert wenn der Modus geändert wird, siehe :func:`Set Mode`.

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
Starts the discovery process. If you call this function and then bring a
smart phone with enabled NFC functionality near to the NFC Bricklet the
state will change from *CardemuDiscovery* to *CardemuDiscoveryReady*.

If no NFC master can be found or if there is an error during discovery
the state will change to *CardemuDiscoveryError*. In this case you
have to restart the discovery.

If the state changes to *CardemuDiscoveryReady* you can start the transfer
of the Ndef message that was written by :func:`Cardemu Write Ndef` by calling
:func:`Cardemu Start Transfer`.
""",
'de':
"""
TODO
"""
}]
})

# NOTE: Even though a single NDEF record can contain a payload of 2^32 - 1 bytes
#       and streaming APIs support data length of 2^16 - 1 bytes, because of limitations
#       of the NFC API used in the firmware only short NDEF records with maximum
#       payload size of 255 bytes work.
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
Writes the Ndef messages that is to be transferred to the NFC master.

The maximum supported Ndef message size in Cardemu mode is 255 byte.

You can call this function at any time in Cardemu mode. The internal buffer
will not be overwritten until you call this function again or change the
mode.
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
You can start the transfer of a Ndef message if the state is *CardemuDiscoveryReady*.

Use parameter 1 to start the transfer. With parameter 0 you can abort the discovery.

Before you call this function with parameter 1. The Ndef message that is to be
transferred is set via :func:`Cardemu Write Ndef`.

After you call this function the state will change to *CardemuTransferNdef*. It will
change to *CardemuTransferNdefReady* if the transfer was successfull or 
*CardemuTransferNdefError* if it wasn't.
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
This callback is called if the cardemu state of the NFC Bricklet changes.
See :func:`Cardemu Get State` for more information about the possible states.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Cardemu-Zustand des NFC Bricklets
sich verändert. Siehe :func:`Cardemu Get State` für mehr Informationen
über die möglichen Zustände des Bricklets.
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
Returns the current state of the NFC Bricklet if in p2p mode.

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
Gibt den aktuellen Zustand des NFC Bricklets aus wenn es sich im P2P-Modus befindet.

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
Starts the discovery process. If you call this function and then bring a
smart phone with enabled NFC P2P app near to the NFC Bricklet the
state will change from *P2PDiscovery* to *P2PDiscoveryReady*.

If no NFC master in P2P mode can be found or if there is an error during discovery
the state will change to *P2PDiscoveryError*. In this case you
have to restart the discovery.

If the state changes to *P2PDiscoveryReady* you can start the Ndef message
transfer or reception with :func:`P2P Start Transfer`.
""",
'de':
"""
TODO
"""
}]
})

# NOTE: Even though a single NDEF record can contain a payload of 2^32 - 1 bytes
#       and streaming APIs support data length of 2^16 - 1 bytes, because of limitations
#       of the NFC API used in the firmware only short NDEF records with maximum
#       payload size of 255 bytes work.
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
Writes the Ndef messages that is to be transferred to the NFC master.

The maximum supported Ndef message size for P2P transfer is 255 byte.

You can call this function at any time in P2P mode. The internal buffer
will not be overwritten until you call this function again, change the
mode or use P2P to read data.
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
You can start the transfer/reception of a Ndef message if the state is *P2PDiscoveryReady*.

Use parameter 2 to read, parameter 1 to write or parameter 0 to abort the discovery.

Before you call this function with parameter 1. The Ndef message that is to be
transferred is set via :func:`P2P Write Ndef`.

After you call this function the state will change to *P2PTransferNdef*. It will
change to *P2PTransferNdefReady* if the transfer was successfull or 
*P2PTransferNdefError* if it wasn't.

If you started a write transfer you are now done. If you started a read transfer
you can now use :func:`P2P Read Ndef` to read the Ndef message that was written
by the NFC peer.
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
Call this function to read the Ndef message that was written by a NFC peer in
NFC P2P mode. The maximum Ndef length is 8192 byte.

The Ndef message is ready if you called :func:`P2P Start Transfer` with a 
read transfer and the state changed to *P2PTransferNdefReady*.
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
This callback is called if the p2p state of the NFC Bricklet changes.
See :func:`P2P Get State` for more information about the possible states.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der P2P-Zustand des NFC Bricklets
sich verändert. Siehe :func:`P2P Get State` für mehr Informationen
über die möglichen Zustände des Bricklets.
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

Die LED kann auch permanent an/aus gestellt werden oder einen Herzschlag anzeigen.

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
