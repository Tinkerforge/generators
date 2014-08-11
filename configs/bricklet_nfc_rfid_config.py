# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# NFC/RFID Bricklet communication config

STATE_IDLE_MASK = (1 << 7)
STATE_ERROR_MASK = ((1 << 7) | (1 << 6))

STATE_INITIALIZATION = 0
STATE_IDLE = STATE_IDLE_MASK
STATE_ERROR = STATE_ERROR_MASK
STATE_REQUEST_TAG_ID = 2
STATE_REQUEST_TAG_ID_READY = STATE_IDLE_MASK | STATE_REQUEST_TAG_ID
STATE_REQUEST_TAG_ID_ERROR = STATE_ERROR_MASK | STATE_REQUEST_TAG_ID
STATE_AUTHENTICATING_MIFARE_CLASSIC_PAGE = 3
STATE_AUTHENTICATING_MIFARE_CLASSIC_PAGE_READY = STATE_IDLE_MASK | STATE_AUTHENTICATING_MIFARE_CLASSIC_PAGE
STATE_AUTHENTICATING_MIFARE_CLASSIC_PAGE_ERROR = STATE_ERROR_MASK | STATE_AUTHENTICATING_MIFARE_CLASSIC_PAGE
STATE_WRITE_PAGE = 4
STATE_WRITE_PAGE_READY = STATE_IDLE_MASK | STATE_WRITE_PAGE
STATE_WRITE_PAGE_ERROR = STATE_ERROR_MASK | STATE_WRITE_PAGE
STATE_REQUEST_PAGE = 5
STATE_REQUEST_PAGE_READY = STATE_IDLE_MASK | STATE_REQUEST_PAGE
STATE_REQUEST_PAGE_ERROR = STATE_ERROR_MASK | STATE_REQUEST_PAGE

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 246,
    'name': ('NFCRFID', 'nfc_rfid', 'NFC/RFID'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device that can read and write NFC and RFID tags',
    'released': True,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('RequestTagID', 'request_tag_id'), 
'elements': [('tag_type', 'uint8', 1, 'in', ('TagType', 'tag_type', [('MifareClassic', 'mifare_classic', 0),
                                                                     ('Type1', 'type1', 1),
                                                                     ('Type2', 'type2', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
To read or write a tag that is in proximity of the NFC/RFID Bricklet you 
first have to call this function with the expected tag type as parameter.
It is no problem if you don't know the tag type. You can cycle through 
the available tag types until the tag gives an answer to the request.

Current the following tag types are supported:

* Mifare Classic
* NFC Forum Type 1
* NFC Forum Type 2

After you call :func:`RequestTagID` the NFC/RFID Bricklet will try to read 
the tag ID from the tag. After this process is done the state will change.
You can either register the :func:`StateChanged` callback or you can poll
:func:`GetState` to find out about the state change.

If the state changes to *RequestTagIDError* it means that either there was 
no tag present or that the tag is of an incompatible type. If the state 
changes to *RequestTagIDReady* it means that a compatible tag was found 
and that the tag ID could be read out. You can now get the tag ID by
calling :func:`GetTagID`.

If two tags are in the proximity of the NFC/RFID Bricklet, this
function will cycle through the tags. To select a specific tag you have
to call :func:`RequestTagID` until the correct tag id is found.

In case of any *Error* state the selection is lost and you have to
start again by calling :func:`RequestTagID`.
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

Beim Aufruf von :func:`RequestTagID` probiert das NFC/RFID Bricklet die tag ID
eines Tags auszulesen. Nachdem dieser Prozess beendet ist ändert sich
der Zustand des Bricklets. Es ist möglich den Callback :func:`StateChanged` zu
registrieren oder den Zustand über :func:`GetState` zu pollen.

Wenn der Zustand auf *RequestTagIDError* wechselt ist ein Fehler aufgetreten.
Dies bedeutet, dass entweder kein Tag oder kein Tag vom passenden Typ gefunden
werden konnte. Wenn der Zustand auf *RequestTagIDReady* wechselt ist ein
kompatibles Tag gefunden worden und die Tag ID wurde gespeichert. Die
Tag ID kann nun über :func:`GetTagID` ausgelesen werden.

Wenn sich zwei Tags gleichzeitig in der Nähe des NFC/RFID Bricklets befinden
werden diese nacheinander ausgelesen. Um ein spezifisches Tag zu selektieren
muss :func:`RequestTagID` so lange aufgerufen werden bis das korrekte Tag
gefunden wurde.

Falls sich das NFC/RFID Bricklet in einem der *Error* Zustände befindet
ist die Selektion aufgehoben und :func:`RequestTagID` muss erneut
aufgerufen werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetTagID', 'get_tag_id'), 
'elements': [('tag_type', 'uint8', 1, 'out', ('TagType', 'tag_type', [('MifareClassic', 'mifare_classic', 0),
                                                                      ('Type1', 'type1', 1),
                                                                      ('Type2', 'type2', 2)])),
             ('tid_length', 'uint8', 1, 'out'),
             ('tid', 'uint8', 7, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the tag type, tag ID and the length of the tag ID 
(4 or 7 bytes are possible length). This function can only be called if the
NFC/RFID is currently in one of the *Ready* states. The returned ID
is the ID that was saved through the last call of :func:`RequestTagID`.

To get the tag ID of a tag the approach is as follows:

* Call :func:`RequestTagID`
* Wait for state to change to *RequestTagIDReady* (see :func:`GetState` or :func:`StateChanged`)
* Call :func:`GetTagID`

""",
'de':
"""
Gibt den Tag Typ, die Tag ID und die Länge der Tag ID (4 oder 7 Byte
möglich) zurück. Diese Funktion kann  nur aufgerufen werden wenn
sich das Bricklet gerade in einem der *Ready*-Zustände befindet. Die
zurückgegebene ID ist die letzte ID die durch einen Aufruf von 
:func:`RequestTagID` gefunden wurde.

Der Ansatz um die Tag ID eines Tags zu bekommen sieht wie folgt aus:

* Rufe :func:`RequestTagID` auf
* Warte auf einen Zustandswechsel auf *RequestTagIDReady* (siehe :func:`GetState` oder :func:`StateChanged`)
* Rufe :func:`GetTagID` auf

"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetState', 'get_state'), 
'elements': [('state', 'uint8', 1, 'out', ('State', 'state', [('Initialization', 'initialization', STATE_INITIALIZATION),
                                                              ('Idle', 'idle', STATE_IDLE),
                                                              ('Error', 'error', STATE_ERROR),
                                                              ('RequestTagID', 'request_tag_id', STATE_REQUEST_TAG_ID),
                                                              ('RequestTagIDReady', 'request_tag_id_ready', STATE_REQUEST_TAG_ID_READY),
                                                              ('RequestTagIDError', 'request_tag_id_error', STATE_REQUEST_TAG_ID_ERROR),
                                                              ('AuthenticatingMifareClassicPage', 'authenticating_mifare_classic_page', STATE_AUTHENTICATING_MIFARE_CLASSIC_PAGE),
                                                              ('AuthenticatingMifareClassicPageReady', 'authenticating_mifare_classic_page_ready', STATE_AUTHENTICATING_MIFARE_CLASSIC_PAGE_READY),
                                                              ('AuthenticatingMifareClassicPageError', 'authenticating_mifare_classic_page_error', STATE_AUTHENTICATING_MIFARE_CLASSIC_PAGE_ERROR),
                                                              ('WritePage', 'write_page', STATE_WRITE_PAGE),
                                                              ('WritePageReady', 'write_page_ready', STATE_WRITE_PAGE_READY),
                                                              ('WritePageError', 'write_page_error', STATE_WRITE_PAGE_ERROR),
                                                              ('RequestPage', 'request_page', STATE_REQUEST_PAGE),
                                                              ('RequestPageReady', 'request_page_ready', STATE_REQUEST_PAGE_READY),
                                                              ('RequestPageError', 'request_page_error', STATE_REQUEST_PAGE_ERROR)])),
             ('idle', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current state of the NFC/RFID Bricklet.

On startup the Bricklet will be in the *Initialization* state. The initialization
will only take about 20ms. After that it changes to *Idle*.

The functions of this Bricklet can be called in the *Idle* state and all of
the *Ready* and *Error* states.

Example: If you call :func:`RequestPage`, the state will change to 
*RequestPage* until the reading of the page is finished. Then it will change
to either *RequestPageReady* if it worked or to *RequestPageError* if it
didn't. If the request worked you can get the page by calling :func:`GetPage`.

The same approach is used analogously for the other API functions.
""",
'de':
"""
Gibt den aktuellen Zustand des NFC/RFID Bricklets aus.

Während der Startphase ist der Zustand *Initialization*. Die 
Initialisierung dauert etwa 20ms. Danach ändert sich der Zustand zu
*Idle*.

Die Funktionen dieses Bricklets können aufgerufen werden wenn der Zustand
entweder *Idle* ist oder einer der *Ready* oder *Error*-Zustände
erreicht wurde.

Beispiel: Wenn :func:`RequestPage` aufgerufen wird, änder sich der
Zustand zu *RequestPage* solange der Leseprozess noch nicht abgeschlossen
ist. Danach ändert sich der Zustand zu *RequestPageReady* wenn das lesen
funktioniert hat oder zu *RequestPageError* wenn nicht. Wenn die Anfrage
erfolgreich war kann die Page mit :func:`GetPage` abgerufen werden.

Der gleiche Ansatz kann analog für andere API Funktionen verwendet werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('AuthenticateMifareClassicPage', 'authenticate_mifare_classic_page'), 
'elements': [('page', 'uint16', 1, 'in'),
             ('key_number', 'uint8', 1, 'in', ('Key', 'key', [('A', 'a', 0),
                                                              ('B', 'b', 1)])),
             ('key', 'uint8', 6, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Mifare Classic tags use authentication. If you want to read from or write to
a Mifare Classic page you have to authenticate it beforehand.
Each page can be authenticated with two keys (A and B). A new Mifare Classic
tag that has not yet been written to can can be accessed with key number A
and the default key *[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]*.

The approach to read or write a Mifare Classic page is as follows:

* Call :func:`RequestTagID`
* Wait for state to change to *RequestTagIDReady* (see :func:`GetState` or :func:`StateChanged`)
* Call :func:`GetTagID` and check if tag ID is correct
* Call :func:`AuthenticateMifareClassicPage` with page and key for the page
* Wait for state to change to *AuthenticatingMifareClassicPageReady*
* Call :func:`RequestPage` or :func`WritePage` to read/write page

""",
'de':
"""
Mifare Classic Tags nutzen Authentifizierung. Wenn eine Page eines 
Mifare Classic Tags gelesen oder geschrieben werden soll muss diese
zuvor Authentifiziert werden. Jede Page kann mit zwei Schlüsseln (A und B)
authentifiziert werden. Ein neues Mifare Classic Tag welches noch nicht
beschrieben wurde kann über Schlüsselnummer A mit dem Standardschlüssel
*[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]* genutzt werden.

Der Ansatz um eine Mifare Classic Page zu lesen oder zu schreiben sieht wie
folgt aus:

* Rufe :func:`RequestTagID` auf
* Warte auf einen Zustandswechsel auf *RequestTagIDReady* (siehe :func:`GetState` oder :func:`StateChanged`)
* Rufe :func:`GetTagID` auf und überprüfe ob Tag ID korrekt ist.
* Rufe :func:`AuthenticateMifareClassicPage` mit Page und Schlüssel für die Page auf
* Warte auf einen Zustandswechsel auf *AuthenticatingMifareClassicPageReady*
* Rufe :func:`RequestPage` oder :func`WritePage` zum lesen/schreiben einer Page auf

"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('WritePage', 'write_page'), 
'elements': [('page', 'uint16', 1, 'in'),
             ('data', 'uint8', 16, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes 16 bytes starting from the given page. How many pages are written
depends on the tag type. The page sizes are as follows:

* Mifare Classic page size: 16 byte (1 page is written)
* NFC Forum Type 1 page size: 8 byte (2 pages are written)
* NFC Forum Type 2 page size: 4 byte (4 pages are written)

The general approach for writing to a tag is as follows:

* Call :func:`RequestTagID`
* Wait for state to change to *RequestTagIDReady* (see :func:`GetState` or :func:`StateChanged`)
* Call :func:`GetTagID` and check if tag ID is correct
* Call :func:`WritePage` with page number and data
* Wait for state to change to *WritePageReady*

If you use a Mifare Classic tag you have to authenticate a page before you
can write to it. See :func:`AuthenticateMifareClassicPage`.
""",
'de':
"""
Schreibt 16 Bytes startend von der übergebenen Page. Wie viele Pages
dadurch geschrieben werden hängt vom Typ des Tags ab. Die Pagegrößen
verhalten sich wie folgt:

* Mifare Classic Pagegröße: 16 byte (1 Page wird geschrieben)
* NFC Forum Type 1 Pagegröße: 8 byte (2 Pages werden geschrieben)
* NFC Forum Type 2 Pagegröße: 4 byte (4 Pages werden geschrieben)

Der generelle Ansatz zum Schreiben eines Tags sieht wie folgt aus:

* Rufe :func:`RequestTagID` auf
* Warte auf einen Zustandswechsel auf *RequestTagIDReady* (siehe :func:`GetState` oder :func:`StateChanged`)
* Rufe :func:`GetTagID` auf und überprüfe ob Tag ID korrekt ist.
* Rufe :func:`WritePage` mit der Page sowie den zu schreibenden Daten auf.
* Warte auf einen Zustandswechsel auf *WritePageReady*

Wenn ein Mifare Classic Tag verwendet wird muss die Page authentifiziert
werden bevor sie geschrieben werden kann. Siehe :func:`AuthenticateMifareClassicPage`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('RequestPage', 'request_page'), 
'elements': [('page', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Reads 16 bytes starting from the given page and stores them into a buffer. 
The buffer can then be read out with :func:`GetPage`.
How many pages are read depends on the tag type. The page sizes are 
as follows:

* Mifare Classic page size: 16 byte (one page is read)
* NFC Forum Type 1 page size: 8 byte (two pages are read)
* NFC Forum Type 2 page size: 4 byte (four pages are read)

The general approach for reading a tag is as follows:

* Call :func:`RequestTagID`
* Wait for state to change to *RequestTagIDReady* (see :func:`GetState` or :func:`StateChanged`)
* Call :func:`GetTagID` and check if tag ID is correct
* Call :func:`RequestPage` with page number
* Wait for state to change to *RequestPageReady*
* Call :func:`GetPage` to retrieve the page from the buffer

If you use a Mifare Classic tag you have to authenticate a page before you
can read it. See :func:`AuthenticateMifareClassicPage`.
""",
'de':
"""
Liest 16 Bytes startend von der übergebenen Page und speichert sie in
einem Buffer. Dieser Buffer kann mit :func:`GetPage` ausgelesen werden. 
Wie viele Pages dadurch gelesen werden hängt vom Typ des Tags ab. 
Die Pagegrößen verhalten sich wie folgt:

* Mifare Classic Pagegröße: 16 byte (eine Page wird gelesen)
* NFC Forum Type 1 Pagegröße: 8 byte (zwei Pages werden gelesen)
* NFC Forum Type 2 Pagegröße: 4 byte (vier Pages werden gelesen)

Der generelle Ansatz zum Lesen eines Tags sieht wie folgt aus:

* Rufe :func:`RequestTagID` auf
* Warte auf einen Zustandswechsel auf *RequestTagIDReady* (siehe :func:`GetState` oder :func:`StateChanged`)
* Rufe :func:`GetTagID` auf und überprüfe ob Tag ID korrekt ist.
* Rufe :func:`RequestPage` mit der zu lesenden Page auf
* Warte auf einen Zustandswechsel auf *RequestPageReady*
* Rufe :func:`GetPage` auf um die gespeicherte Page abzufragen

Wenn ein Mifare Classic Tag verwendet wird muss die Page authentifiziert
werden bevor sie gelesen werden kann. Siehe :func:`AuthenticateMifareClassicPage`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetPage', 'get_page'), 
'elements': [('data', 'uint8', 16, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns 16 bytes of data from an internal buffer. To fill the buffer
with specific pages you have to call :func:`RequestPage` beforehand.
""",
'de':
"""
Gibt 16 Bytes Daten aus einem internen Buffer zurück. Der Buffer
kann zuvor mit spezifischen Pages über einen Aufruf von  
:func:`RequestPage` gefüllt werden.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('StateChanged', 'state_changed'), 
'elements': [('state', 'uint8', 1, 'out', ('State', 'state', [('Initialization', 'initialization', STATE_INITIALIZATION),
                                                              ('Idle', 'idle', STATE_IDLE),
                                                              ('Error', 'error', STATE_ERROR),
                                                              ('RequestTagID', 'request_tag_id', STATE_REQUEST_TAG_ID),
                                                              ('RequestTagIDReady', 'request_tag_id_ready', STATE_REQUEST_TAG_ID_READY),
                                                              ('RequestTagIDError', 'request_tag_id_error', STATE_REQUEST_TAG_ID_ERROR),
                                                              ('AuthenticatingMifareClassicPage', 'authenticating_mifare_classic_page', STATE_AUTHENTICATING_MIFARE_CLASSIC_PAGE),
                                                              ('AuthenticatingMifareClassicPageReady', 'authenticating_mifare_classic_page_ready', STATE_AUTHENTICATING_MIFARE_CLASSIC_PAGE_READY),
                                                              ('AuthenticatingMifareClassicPageError', 'authenticating_mifare_classic_page_error', STATE_AUTHENTICATING_MIFARE_CLASSIC_PAGE_ERROR),
                                                              ('WritePage', 'write_page', STATE_WRITE_PAGE),
                                                              ('WritePageReady', 'write_page_ready', STATE_WRITE_PAGE_READY),
                                                              ('WritePageError', 'write_page_error', STATE_WRITE_PAGE_ERROR),
                                                              ('RequestPage', 'request_page', STATE_REQUEST_PAGE),
                                                              ('RequestPageReady', 'request_page_ready', STATE_REQUEST_PAGE_READY),
                                                              ('RequestPageError', 'request_page_error', STATE_REQUEST_PAGE_ERROR)])),
             ('idle', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called if the state of the NFC/RFID Bricklet changes.
See :func:`GetState` for more information about the possible states.
""",
'de':
"""
Dieser Callback wird ausgelöst wenn der Zustand des NFC/RFID Bricklets
sich verändert. Siehe :func:`GetState` für mehr Informationen
über die möglichen Zustände des Bricklets.
"""
}]
})
