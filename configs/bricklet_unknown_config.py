# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Unknown Bricklet communication config

com = {
    'author': 'Matthias Bolte <matthias@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': -21,
    'name': 'Unknown',
    'display_name': 'Unknown',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '',
        'de': ''
    },
    'released': False,
    'documented': False,
    'discontinued': False,
    'features': [
        'device',
        'comcu_bricklet',
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append({
'name': 'Enumeration Type',
'type': 'uint8',
'constants': [('Available', 0),
              ('Connected', 1),
              ('Disconnected', 2)]
})

com['packets'].append({
'type': 'function',
'function_id': 252,
'name': 'Comcu Enumerate',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
This function is equivalent to the normal enumerate function.
It is used to trigger the initial enumeration of CoMCU-Bricklets.
See :cb:`Enumerate`.
""",
'de':
"""
Diese Funktion ist äquivalent zur normalen Enumerate-Funktion.
Sie wird verwendet, um die initiale Enumerierung von CoMCU-Bricklets auszulösen.
Siehe :cb:`Enumerate`.
"""
}]
})


com['packets'].append({
'type': 'callback',
'function_id': 253,
'name': 'Enumerate',
'elements': [('Uid', 'string', 8, 'out', {}),
             ('Connected Uid', 'string', 8, 'out', {}),
             ('Position', 'char', 1, 'out', {'range': [('a', 'h'), ('i', 'i'), ('z', 'z')]}),
             ('Hardware Version', 'uint8', 3, 'out', [{'name': 'Major'}, {'name': 'Minor'}, {'name': 'Revision'}]),
             ('Firmware Version', 'uint8', 3, 'out', [{'name': 'Major'}, {'name': 'Minor'}, {'name': 'Revision'}]),
             ('Device Identifier', 'uint16', 1, 'out', {}),
             ('Enumeration Type', 'uint8', 1, 'out', {'constant_group': 'Enumeration Type'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
The callback has seven parameters:

 * ``uid``: The UID of the device.
 * ``connected_uid``: UID where the device is connected to. For a Bricklet this
   is the UID of the Brick or Bricklet it is connected to. "0" if the Bricklet is
   directly connected to the calling hardware. With this information it is possible to
   reconstruct the complete network topology.
 * ``position``: 'a' - 'h' (position on Brick) or 'i' (position of the Raspberry Pi (Zero) HAT)
   or 'z' (Bricklet on :ref:`Isolator Bricklet <isolator_bricklet>`).
 * ``hardware_version``: Major, minor and release number for hardware version.
 * ``firmware_version``: Major, minor and release number for firmware version.
 * ``device_identifier``: A number that represents the device.
 * ``enumeration_type``: Type of enumeration.

 Possible enumeration types are:

 * Available: Device is available (enumeration
   triggered by user). This enumeration type can
   occur multiple times for the same device.
 * Connected: Device is newly connected
   (automatically send by Brick after establishing a communication connection).
   This indicates that the device has potentially lost its previous
   configuration and needs to be reconfigured.
 * Disconnected: Device is disconnected (only
   possible for USB connection). In this case only ``uid`` and
   ``enumeration_type`` are valid.

 It should be possible to implement plug-and-play functionality with this
 (as is done in Brick Viewer).
""",
'de':
"""
Der Callback empfängt sieben Parameter:

 * ``uid``: Die UID des Bricks/Bricklets.
 * ``connected_uid``: Die UID des Gerätes mit dem das Bricklet verbunden
   ist. Für ein Bricklet ist dies die UID des Bricks oder Bricklets mit dem es verbunden ist oder
   "0" falls das Bricklet direkt mit der aufrufenden Hardware verbunden ist. Mit diesen Informationen
   sollte es möglich sein die komplette Netzwerktopologie zu rekonstruieren.
 * ``position``: 'a' - 'h' (Position an Brick) oder 'i' (Position des Raspberry Pi (Zero) HAT)
   oder 'z' (Bricklet an :ref:`Isolator Bricklet <isolator_bricklet>`).
 * ``hardware_version``: Major, Minor und Release Nummer der Hardwareversion.
 * ``firmware_version``: Major, Minor und Release Nummer der Firmwareversion.
 * ``device_identifier``: Eine Zahl, welche das Bricklet repräsentiert.
 * ``enumeration_type``: Art der Enumerierung

 Mögliche Enumerierungsarten sind:

 * Available: Gerät ist verfügbar (Enumerierung vom
   Benutzer ausgelöst). Diese Enumerierungsart kann
   mehrfach für das selbe Gerät auftreten.
 * Connected: Gerät wurde neu verbunden (Automatisch
   vom Brick gesendet nachdem die Kommunikation aufgebaut wurde). Dies kann
   bedeuten, dass das Gerät die vorher eingestellte Konfiguration verloren hat
   und neu konfiguriert werden muss.
 * Disconnected: Gerät wurde getrennt (Nur bei
   USB-Verbindungen möglich). In diesem Fall haben nur ``uid`` und
   ``enumeration_type`` einen gültigen Wert.

 Es sollte möglich sein Plug-and-Play-Funktionalität mit diesem Callback
 zu implementieren (wie es im Brick Viewer geschieht).
"""
}]
})

com['packets'].append({
'type': 'function',
'function_id': 254,
'name': 'Enumerate',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
 Broadcasts an enumerate request. All devices will respond with an :cb:`Enumerate` callback.
""",
'de':
"""
 Broadcast einer Enumerierungsanfrage. Alle Bricks und Bricklets werden mit einem :cb:`Enumerate` Callback antworten.
"""
}]
})
