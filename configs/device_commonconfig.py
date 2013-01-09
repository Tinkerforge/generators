# -*- coding: utf-8 -*-

# Common Device communication config

common_packets = []

common_packets.append({
'type': 'function',
'function_id': -1,
'name': ('GetAPIVersion', 'get_api_version'),
'elements': [('api_version', 'uint8', 3, 'out')],
'since_firmware': None,
'doc': ['af', {
'en':
"""
Returns the API version (major, minor, revision) of the bindings for this
device.
""",
'de':
"""
Gibt die API Version (Major, Minor, Revision) der Bindings für diese Gerät
zurück.
"""
}]
})

common_packets.append({
'type': 'function',
'function_id': -1,
'name': ('GetResponseExpected', 'get_response_expected'),
'elements': [('function_id', 'uint8', 1, 'in'),
             ('response_expected', 'bool', 1, 'out')],
'since_firmware': None,
'doc': ['af', {
'en':
"""
Returns the response expected flag for the function specified by the function
ID parameter. It is *true* if the function is expected to send a response,
*false* otherwise.

For getter functions this is enabled by default and cannot be disabled,
because those functions will always send a response. For callback configuration
functions it is enabled by default too, but can be disabled by
:func:`SetResponseExpected`. For setter functions it is disabled by default
and can be enabled.

Enabling the response expected flag for a setter function allows to detect
timeouts and other error conditions calls of this setter as well. The
device will then send a response for this purpose. If this flag is disabled for
a setter function then no response is send and errors are silently ignored,
because they cannot be detected.
""",
'de':
"""
Gibt das Response-Expected-Flag für die Funktion mit der angegebenen Funktion
IDs zurück. Es ist *true* falls für die Funktion beim Aufruf eine Antwort
erwartet wird, *false* andernfalls.

Für Getter-Funktionen ist diese Flag immer gesetzt und kann nicht entfernt
werden, da diese Funktionen immer eine Antwort senden. Für
Konfigurationsfunktionen für Callbacks ist es standardmäßig gesetzt, kann aber
entfernt werden mittels :func:`SetResponseExpected`. Für Setter-Funktionen ist
es standardmäßig nicht gesetzt, kann aber gesetzt werden.

Wenn das Response-Expected-Flag für eine Setter-Funktion gesetzt ist, können
Timeouts und andere Fehlerfälle auch für Aufrufe dieser Setter-Funktion
detektiert werden. Das Gerät sendet dann eine Antwort extra für diesen Zweck.
Wenn das Flag für eine Setter-Funktion nicht gesetzt ist, dann wird keine
Antwort vom Gerät gesendet und Fehler werden stillschweigend ignoriert, da sie
nicht detektiert werden können.
"""
}]
})

common_packets.append({
'type': 'function',
'function_id': -1,
'name': ('SetResponseExpected', 'set_response_expected'),
'elements': [('function_id', 'uint8', 1, 'in'),
             ('response_expected', 'bool', 1, 'in')],
'since_firmware': None,
'doc': ['af', {
'en':
"""
Changes the response expected flag of the function specified by the
function ID parameter. This flag can only be changed for setter (default value:
*false*) and callback configuration functions (default value: *true*). For
getter functions it is always enabled and callbacks it is always disabled.

Enabling the response expected flag for a setter function allows to detect
timeouts and other error conditions calls of this setter as well. The
device will then send a response for this purpose. If this flag is disabled for
a setter function then no response is send and errors are silently ignored,
because they cannot be detected.
""",
'de':
"""
Ändert das Response-Expected-Flag für die Funktion mit der angegebenen Funktion
IDs. Diese Flag kann nur für Setter-Funktionen (Standardwert: *false*) und
Konfigurationsfunktionen für Callbacks (Standardwert: *true*) geändert werden.
Für Getter-Funktionen ist das Flag immer gesetzt und für Callbacks niemals.

Wenn das Response-Expected-Flag für eine Setter-Funktion gesetzt ist, können
Timeouts und andere Fehlerfälle auch für Aufrufe dieser Setter-Funktion
detektiert werden. Das Gerät sendet dann eine Antwort extra für diesen Zweck.
Wenn das Flag für eine Setter-Funktion nicht gesetzt ist, dann wird keine
Antwort vom Gerät gesendet und Fehler werden stillschweigend ignoriert, da sie
nicht detektiert werden können.
"""
}]
})

common_packets.append({
'type': 'function',
'function_id': -1,
'name': ('SetResponseExpectedAll', 'set_response_expected_all'),
'elements': [('response_expected', 'bool', 1, 'in')],
'since_firmware': None,
'doc': ['af', {
'en':
"""
Changes the response expected flag for all setter and callback configuration
functions of this device at once.
""",
'de':
"""
Ändert das Response-Expected-Flag für alle Setter-Funktionen und
Konfigurationsfunktionen für Callbacks diese Gerätes.
"""
}]
})
