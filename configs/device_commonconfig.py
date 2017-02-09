# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Common Device communication config

# is_virtual is set to True for functions without a corresponding TCP/IP packet

common_packets = []

common_packets.append({
'is_virtual': True,
'type': 'function',
'function_id': -1,
'name': 'Get API Version',
'elements': [('API Version', 'uint8', 3, 'out')],
'since_firmware': None,
'doc': ['af', {
'en':
"""
Returns the version of the API definition (major, minor, revision) implemented
by this API bindings. This is neither the release version of this API bindings
nor does it tell you anything about the represented Brick or Bricklet.
""",
'de':
"""
Gibt die Version der API Definition (Major, Minor, Revision) zurück, die diese
API Bindings implementieren. Dies ist weder die Release-Version dieser API
Bindings noch gibt es in irgendeiner Weise Auskunft über den oder das
repräsentierte(n) Brick oder Bricklet.
"""
}]
})

common_packets.append({
'is_virtual': True,
'type': 'function',
'function_id': -1,
'name': 'Get Response Expected',
'elements': [('Function Id', 'uint8', 1, 'in'),
             ('Response Expected', 'bool', 1, 'out')],
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
:func:`Set Response Expected`. For setter functions it is disabled by default
and can be enabled.

Enabling the response expected flag for a setter function allows to detect
timeouts and other error conditions calls of this setter as well. The
device will then send a response for this purpose. If this flag is disabled for
a setter function then no response is send and errors are silently ignored,
because they cannot be detected.

See :func:`Set Response Expected` for the list of function ID :word:`constants`
available for this function.
""",
'de':
"""
Gibt das Response-Expected-Flag für die Funktion mit der angegebenen Funktions
IDs zurück. Es ist *true* falls für die Funktion beim Aufruf eine Antwort
erwartet wird, *false* andernfalls.

Für Getter-Funktionen ist diese Flag immer gesetzt und kann nicht entfernt
werden, da diese Funktionen immer eine Antwort senden. Für
Konfigurationsfunktionen für Callbacks ist es standardmäßig gesetzt, kann aber
entfernt werden mittels :func:`Set Response Expected`. Für Setter-Funktionen ist
es standardmäßig nicht gesetzt, kann aber gesetzt werden.

Wenn das Response-Expected-Flag für eine Setter-Funktion gesetzt ist, können
Timeouts und andere Fehlerfälle auch für Aufrufe dieser Setter-Funktion
detektiert werden. Das Gerät sendet dann eine Antwort extra für diesen Zweck.
Wenn das Flag für eine Setter-Funktion nicht gesetzt ist, dann wird keine
Antwort vom Gerät gesendet und Fehler werden stillschweigend ignoriert, da sie
nicht detektiert werden können.

Siehe :func:`Set Response Expected` für die Liste der verfügbaren Funktions
ID :word:`constants` für diese Funktion.
"""
}]
})

common_packets.append({
'is_virtual': True,
'type': 'function',
'function_id': -1,
'name': 'Set Response Expected',
'elements': [('Function Id', 'uint8', 1, 'in'),
             ('Response Expected', 'bool', 1, 'in')],
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
'is_virtual': True,
'type': 'function',
'function_id': -1,
'name': 'Set Response Expected All',
'elements': [('Response Expected', 'bool', 1, 'in')],
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
