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
    'released': False,
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

After you call this function the NFC/RFID Bricklet will try to read the tag 
ID from the tag. After this process is done the state will change. You can 
either register the :func:`StateChanged` callback or you can poll
:func:`GetState` to find out about the state change.

If the state changes to *RequestTagIDError* it means that either there was 
no tag present or that the tag is of an incompatible type. If the state 
changes to *RequestTagIDReady* it means that a compatible tag was found 
and that the tag ID could be read out. You can now get the tag ID by
calling :func:`GetTagID`.

If two tags are in the proximity of the NFC/RFID Bricklet, this
function will cycle through the tags. To select a specific tag you have
to call :func:`RequestTagID` until the correct tag id is found.

In case of any error state the selection is lost and you have to
start again by calling :func:`RequestTagID`.
""",
'de':
"""
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
NFC/RFID is currently in one of the *ready* states. The returned ID
is the ID that was saved through the last call of :func:`RequestTagID`.

To get the tag ID of a tag the approach is as follows:

* Call :func:`RequestTagID`
* Wait for state to change to *RequestTagIDReady* (see :func:`GetState` or :func:`StateChanged`)
* Call :func:`GetTagID`

""",
'de':
"""
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
a Mifare Classic page you have to authenticate it in beforehand.
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

* Mifare Classic page size: 16 byte (1 page is read)
* NFC Forum Type 1 page size: 8 byte (2 pages are read)
* NFC Forum Type 2 page size: 4 byte (4 pages are read)

The general approach for reading a tag is as follows:

* Call :func:`RequestTagID`
* Wait for state to change to *RequestTagIDReady* (see :func:`GetState` or :func:`StateChanged`)
* Call :func:`GetTagID` and check if tag ID is correct
* Call :func:`ReadPage` with page number
* Wait for state to change to *ReadPageReady*
* Call :func:`GetPage` to retrieve the page from the buffer

If you use a Mifare Classic tag you have to authenticate a page before you
can read it. See :func:`AuthenticateMifareClassicPage`.
""",
'de':
"""
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
you have to call :func:`RequestPage`.
""",
'de':
"""
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
"""
}]
})

