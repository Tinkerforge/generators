# -*- coding: utf-8 -*-

# Multi Touch Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 234,
    'name': ('MultiTouch', 'multi_touch', 'Multi Touch'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device with 12 touch sensors',
    'released': False,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetTouchState', 'get_touch_state'), 
'elements': [('state', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current touch state. The state is given as a bitfield.

Bits 0 to 11 represent the 12 electrodes and bit 12 represents
the proximity.

If an electrode is touched, the corresponding bit is true. If
a hand or similar is in proximity to the electrodes, bit 12 is
*true*.

Example: The state 4103 = 0x1007 = 0b1000000000111 means that
electrodes 0, 1 and 2 are touched and that something is in the
proximity of the electrodes.

The proximity is activated with a distance of 1-2cm. An electrode
is already counted as touched if a finger is nearly touching the
electrode. This means that you can put a piece of paper or foil
or similar on top of a electrode to build a touch panel with
a professional look.
""",
'de':
"""
Gibt den aktuellen Tastzustand zurück. Der Zustand ist als ein
Bitfeld repräsentiert.

Bits 0 bis 11 repräsentieren die 12 Elektroden und Bit 12
repräsentiert die Proximity (Nähe).

Wird eine Elektrode berührt, ist das korrespondierende Bit *true*.
Wenn eine Hand oder vergleichbares in der Nähe der Elektroden ist
wird Bit 12 auf *true* gesetzt.

Beispiel: Der Zustand 4103 = 0x1007 = 0b1000000000111 bedeutet dass
die Elektroden 0, 1 und 2 berührt werden und das sich etwas in der
nähe der Elektroden befindet.

Das Proximity Bit wird ab einer Distanz von ca. 1-2cm aktiviert.
Eine Elektrode wird schon als berührt gezählt wenn ein Finger sie
beinahe berührt. Dadurch ist es möglich ein Stück Papier oder Folie
über die Elektrode zu kleben um damit ein Touchpanel mit einem
professionellen aussehen zu bauen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('Recalibrate', 'recalibrate'), 
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Recalibrates the electrodes. Call this function whenever you changed
or moved you electrodes.
""",
'de':
"""
Rekalibriert die Elektroden. Rufe diese Funktion auf wenn die
Elektroden verändert oder bewegt wurden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetElectrodeConfig', 'set_electrode_config'), 
'elements': [('enabled_electrodes', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Enables/disables electrodes with a bitfield (see :func:`GetTouchState`).

*True* enables the electrode, *false* disables the electrode. A
disabled electrode will always return *false* as its state. If you
don't need all electrodes you can disable the electrodes that are
not needed.

It is recommended that you disable the proximity bit (bit 12) if
the proximity feature is not needed. This will reduce the amount of
traffic that is produced by the :func:`TouchState` callback.

Disabling electrodes will also reduce power consumption.

Default: 8191 = 0x1FFF = 0b1111111111111 (all electrodes enabled)
""",
'de':
"""
Aktiviert/deaktiviert Elektroden mit einem Bitfeld (siehe :func:`GetTouchState`).

*True* aktiviert eine Elektrode, *false* deaktiviert eine Elektrode. Eine
deaktivierte Elektrode hat immer den Zustand *false*. Wenn nicht alle
Elektroden gebraucht werden können die ungebrauchten deaktiviert werden.

Wir empfehlen das Proximity Bit (bit 12) zu deaktivieren wenn
das Proximity-Feature nicht benötigt wird. Das verringert den Datenverkehr
der durch den :func:`TouchState` Callback ausgelöst wird.

Eine deaktivierte Elektrode verringert zusätzlich den Stromverbrauch.

Standardwert: 8191 = 0x1FFF = 0b1111111111111 (alle Elektroden aktiviert)
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetElectrodeConfig', 'get_electrode_config'), 
'elements': [('enabled_electrodes', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the electrode configuration, as set by :func:`SetElectrodeConfig`.
""",
'de':
"""
Gibt die Elektrodenkonfiguration zurück, wie von :func:`SetElectrodeConfig`
gesetzt.
"""
}]
})


com['packets'].append({
'type': 'callback',
'name': ('TouchState', 'touch_state'), 
'elements': [('state', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
Returns the current touch state, see :func:`GetTouchState` for
information about the state.

This callback is triggered every time the touch state changes.
""",
'de':
"""
Gibt den aktuellen Tastzustand zurück, siehe :func:`GetTouchState`
für mehr Informationen über den Zustand.

Dieser Callback wird ausgelöst wenn sich ein Tastzustand ändert.
"""
}]
})
