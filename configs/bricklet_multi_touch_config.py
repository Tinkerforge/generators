# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Multi Touch Bricklet communication config

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 234,
    'name': 'Multi Touch',
    'display_name': 'Multi Touch',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Capacitive touch sensor for 12 electrodes',
        'de': 'Kapazitiver Touch Sensor für 12 Elektroden'
    },
    'released': True,
    'documented': True,
    'discontinued': False, # selling remaining stock, replaced by Multi Touch Bricklet 2.0
    'features': [
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Get Touch State',
'elements': [('State', 'uint16', 1, 'out', {'range': (0, 0x1FFF)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current touch state. The state is given as a bitfield.

Bits 0 to 11 represent the 12 electrodes and bit 12 represents
the proximity.

If an electrode is touched, the corresponding bit is *true*. If
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
professionellen Aussehen zu bauen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Recalibrate',
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
'name': 'Set Electrode Config',
'elements': [('Enabled Electrodes', 'uint16', 1, 'in', {'range': (0, 0x1FFF), 'default': 0x1FFF})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Enables/disables electrodes with a bitfield (see :func:`Get Touch State`).

*True* enables the electrode, *false* disables the electrode. A
disabled electrode will always return *false* as its state. If you
don't need all electrodes you can disable the electrodes that are
not needed.

It is recommended that you disable the proximity bit (bit 12) if
the proximity feature is not needed. This will reduce the amount of
traffic that is produced by the :cb:`Touch State` callback.

Disabling electrodes will also reduce power consumption.

Default: 8191 = 0x1FFF = 0b1111111111111 (all electrodes and proximity feature enabled)
""",
'de':
"""
Aktiviert/deaktiviert Elektroden mit einem Bitfeld (siehe :func:`Get Touch State`).

*True* aktiviert eine Elektrode, *false* deaktiviert eine Elektrode. Eine
deaktivierte Elektrode hat immer den Zustand *false*. Wenn nicht alle
Elektroden gebraucht werden können die ungebrauchten deaktiviert werden.

Wir empfehlen das Proximity Bit (Bit 12) zu deaktivieren wenn
das Proximity-Feature nicht benötigt wird. Das verringert den Datenverkehr
der durch den :cb:`Touch State` Callback ausgelöst wird.

Eine deaktivierte Elektrode verringert zusätzlich den Stromverbrauch.

Standardwert: 8191 = 0x1FFF = 0b1111111111111 (alle Elektroden und Proximity-Feature aktiviert)
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Electrode Config',
'elements': [('Enabled Electrodes', 'uint16', 1, 'out', {'range': (0, 0x1FFF), 'default': 0x1FFF})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the electrode configuration, as set by :func:`Set Electrode Config`.
""",
'de':
"""
Gibt die Elektrodenkonfiguration zurück, wie von :func:`Set Electrode Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Touch State',
'elements': [('State', 'uint16', 1, 'out', {'range': (0, 0x1FFF)})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
Returns the current touch state, see :func:`Get Touch State` for
information about the state.

This callback is triggered every time the touch state changes.
""",
'de':
"""
Gibt den aktuellen Tastzustand zurück, siehe :func:`Get Touch State`
für mehr Informationen über den Zustand.

Dieser Callback wird ausgelöst, wenn sich ein Tastzustand ändert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Electrode Sensitivity',
'elements': [('Sensitivity', 'uint8', 1, 'in', {'range': (5, 201), 'default': 181})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the sensitivity of the electrodes. An electrode with a high sensitivity
will register a touch earlier then an electrode with a low sensitivity.

If you build a big electrode you might need to decrease the sensitivity, since
the area that can be charged will get bigger. If you want to be able to
activate an electrode from further away you need to increase the sensitivity.

After a new sensitivity is set, you likely want to call :func:`Recalibrate`
to calibrate the electrodes with the newly defined sensitivity.
""",
'de':
"""
Setzt die Empfindlichkeit der Elektrode. Eine Elektrode mit einer hohen
Empfindlichkeit registriert eine Berührung früher als eine Elektrode mit einer
niedrigen Empfindlichkeit.

Wenn eine große Elektrode verwendet wird sollte die Empfindlichkeit verringert
werden, da eine größere Fläche aufgeladen werden kann. Wenn eine Elektrode aus
größerem Abstand aktivierbar seien soll, muss die Empfindlichkeit
vergrößert werden.

Nachdem eine neue Empfindlichkeit gesetzt wurde, macht es Sinn
:func:`Recalibrate` aufzurufen damit die Elektroden mit der neu
definierten Empfindlichkeit kalibriert werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Electrode Sensitivity',
'elements': [('Sensitivity', 'uint8', 1, 'out', {'range': (5, 201), 'default': 181})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current sensitivity, as set by :func:`Set Electrode Sensitivity`.
""",
'de':
"""
Gibt die aktuelle Empfindlichkeit zurück, wie von
:func:`Set Electrode Sensitivity` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Touch State', 'touch state'), [(('State', 'Touch State'), 'uint16', 1, None, None, None)], [])],
'incomplete': True # because of special print logic
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Touch State', 'touch state'), [(('State', 'Touch State'), 'uint16', 1, None, None, None)], None, None)],
'incomplete': True # because of special print logic in callback
})

def electrode_channel(idx):
    return {
        'predicate': 'cfg.electrode{}Enabled'.format(idx),
        'id': 'Electrode {}'.format(idx),
        'label': 'Electrode {}'.format(idx),
        'type': 'Electrode',
        'getters': [{
            'packet': 'Get Touch State',
            'transform': '(value & (1 << {})) > 0 ? OnOffType.ON : OnOffType.OFF'.format(idx)}],

        'callbacks': [{
            'packet': 'Touch State',
            'transform': '(state & (1 << {})) > 0 ? OnOffType.ON : OnOffType.OFF'.format(idx)}],
    }

def electrode_config(idx):
    return {
            'packet': 'Set Electrode Config',
            'element': 'Enabled Electrodes',
            'element_index': idx,

            'name': 'Electrode {} Enabled'.format(idx),
            'type': 'boolean',
            'default': 'true',

            'label': 'Electrode {} Enabled'.format(idx),
            'description': "True enables the electrode, false disables the electrode. A disabled electrode will always return false as its state. If you don't need all electrodes you can disable the electrodes that are not needed. Disabling electrodes will also reduce power consumption.",
        }

com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.OnOffType', 'org.eclipse.smarthome.core.library.types.StringType'],
    'param_groups': oh_generic_channel_param_groups(),
    'params': [{
            'packet': 'Set Electrode Sensitivity',
            'element': 'Sensitivity',

            'name': 'Sensitivity',
            'type': 'integer',
            'default': 181,
            'min': 5,
            'max': 201,

            'label': 'Sensitivity',
            'description': 'The sensitivity of the electrodes. An electrode with a high sensitivity will register a touch earlier then an electrode with a low sensitivity.<br/><br/>If you build a big electrode you might need to decrease the sensitivity, since the area that can be charged will get bigger. If you want to be able to activate an electrode from further away you need to increase the sensitivity.'
        }, {
            'packet': 'Set Electrode Config',
            'element': 'Enabled Electrodes',
            'element_index': 12,

            'name': 'Proximity Enabled',
            'type': 'boolean',
            'default': 'true',

            'label': 'Proximity Enabled',
            'description': "True enables the proximity feature, false disables it. It is recommended that you disable the proximity feature if not needed. This will reduce the amount of traffic that is produced.",
        }
    ] + [electrode_config(i) for i in range(0, 12)],
    'init_code': """this.setElectrodeSensitivity(cfg.sensitivity.shortValue());
        this.recalibrate();
        this.setElectrodeConfig({} | (cfg.proximityEnabled ? 1 << 12 : 0));""".format(' | '.join(['(cfg.electrode{0}Enabled ? 1 << {0} : 0)'.format(i) for i in range(0, 12)])),
    'channels': [electrode_channel(i) for i in range(0, 12)] + [
        {
            'predicate': 'cfg.proximityEnabled',
            'id': 'Proximity',
            'label': 'Proximity',
            'description': 'The current touch state. If a hand or similar is in proximity to the electrodes, this channel is toggled. The proximity is activated with a distance of 1-2cm. This means that you can put a piece of paper or foil or similar on top of a electrode to build a touch panel with a professional look.',
            'type': 'Electrode',
            'getters': [{
                'packet': 'Get Touch State',
                'transform': '(value & (1 << 12)) > 0 ? OnOffType.ON : OnOffType.OFF'}],

            'callbacks': [{
                'packet': 'Touch State',
                'transform': '(state & (1 << 12)) > 0 ? OnOffType.ON : OnOffType.OFF'}]
        },
        {
            'id': 'Recalibrate',
            'type': 'Recalibrate',
            'setters': [{
                'packet': 'Recalibrate'}],
            'setter_command_type': "StringType" # Command type has to be string type to be able to use command options.
        },
    ],
    'channel_types': [
        oh_generic_channel_type('Electrode', 'Switch', 'NOT USED',
                    update_style=None,
                    description='The current touch state. An electrode is already counted as touched if a finger is nearly touching the electrode. This means that you can put a piece of paper or foil or similar on top of a electrode to build a touch panel with a professional look.'),
        {
            'id': 'Recalibrate',
            'item_type': 'String',
            'label': 'Recalibrate Electrodes',
            'description':'Recalibrates the electrodes. Trigger this channel whenever you changed or moved you electrodes.',
            'command_options': [('Trigger', 'TRIGGER')]
        }
    ],
    'actions': ['Get Touch State', 'Recalibrate', 'Get Electrode Config', 'Get Electrode Sensitivity']
}
