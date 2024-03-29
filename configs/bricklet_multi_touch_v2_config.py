# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Multi Touch Bricklet 2.0 communication config

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2129,
    'name': 'Multi Touch V2',
    'display_name': 'Multi Touch 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Capacitive touch sensor for 12 electrodes',
        'de': 'Kapazitiver Touch Sensor für 12 Elektroden'
    },
    'released': True,
    'documented': True,
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
'name': 'Touch LED Config',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Show Heartbeat', 2),
              ('Show Touch', 3)]
})

com['packets'].append({
'type': 'function',
'name': 'Get Touch State',
'elements': [('State', 'bool', 13, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current touch state. The state is given as a array of
bools.

Element 0 to 11 represent the 12 electrodes and element 12 represents
the proximity.

If an electrode is touched, the corresponding element is *true*. If
a hand or similar is in proximity to the electrodes, element 12 is
*true*.

The proximity is activated with a distance of 1-2cm. An electrode
is already counted as touched if a finger is nearly touching the
electrode. This means that you can put a piece of paper or foil
or similar on top of a electrode to build a touch panel with
a professional look.

If you want to get the value periodically, it is recommended to use the
:cb:`Touch State` callback. You can set the callback configuration
with :func:`Set Touch State Callback Configuration`.
""",
'de':
"""
Gibt den aktuellen Tastzustand zurück. Der Zustand wird als
Bool-Array repräsentiert.

Element 0 bis 11 repräsentieren die 12 Elektroden und Element 12
repräsentiert die Proximity (Nähe).

Wird eine Elektrode berührt, ist das korrespondierende Element *true*.
Wenn eine Hand oder vergleichbares in der Nähe der Elektroden ist
wird Element 12 auf *true* gesetzt.

Das Proximity Bit wird ab einer Distanz von ca. 1-2cm aktiviert.
Eine Elektrode wird schon als berührt gezählt wenn ein Finger sie
beinahe berührt. Dadurch ist es möglich ein Stück Papier oder Folie
über die Elektrode zu kleben um damit ein Touchpanel mit einem
professionellen Aussehen zu bauen.

Wenn der Wert periodisch benötigt wird, kann auch der :cb:`Touch State` Callback
verwendet werden. Der Callback wird mit der Funktion
:func:`Set Touch State Callback Configuration` konfiguriert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Touch State Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period is the period with which the :cb:`Touch State` callback
is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.
""",
'de':
"""
Die Periode ist die Periode mit der der :cb:`Touch State` Callback
ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn der Wert sich im Vergleich zum letzten mal geändert
hat. Ändert der Wert sich nicht innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen des Werts.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Touch State Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set Touch State Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set Touch State Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Touch State',
'elements': [('State', 'bool', 13, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
Returns the current touch state, see :func:`Get Touch State` for
information about the state.

This callback is triggered every time the touch state changes with
a given period (see :func:`Set Touch State Callback Configuration`)
""",
'de':
"""
Gibt den aktuellen Tastzustand zurück, siehe :func:`Get Touch State`
für mehr Informationen über den Zustand.

Dieser Callback wird ausgelöst, wenn sich ein Tastzustand ändert mit
der eingestellten Periode (siehe :func:`Set Touch State Callback Configuration`)
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
'elements': [('Enabled Electrodes', 'bool', 13, 'in', {'default': [True]*13})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Enables/disables electrodes with a bool array (see :func:`Get Touch State`).

*True* enables the electrode, *false* disables the electrode. A
disabled electrode will always return *false* as its state. If you
don't need all electrodes you can disable the electrodes that are
not needed.

It is recommended that you disable the proximity electrode (element 12) if
the proximity feature is not needed. This will reduce the amount of
traffic that is produced by the :cb:`Touch State` callback.

Disabling electrodes will also reduce power consumption.
""",
'de':
"""
Aktiviert/deaktiviert Elektroden mit einem Bool-Array (siehe :func:`Get Touch State`).

*True* aktiviert eine Elektrode, *false* deaktiviert eine Elektrode. Eine
deaktivierte Elektrode hat immer den Zustand *false*. Wenn nicht alle
Elektroden gebraucht werden können die ungebrauchten deaktiviert werden.

Wir empfehlen die Proximity-Elektrode (Element 12) zu deaktivieren wenn
das Proximity-Feature nicht benötigt wird. Das verringert den Datenverkehr
der durch den :cb:`Touch State` Callback ausgelöst wird.

Eine deaktivierte Elektrode verringert zusätzlich den Stromverbrauch.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Electrode Config',
'elements': [('Enabled Electrodes', 'bool', 13, 'out', {'default': [True]*13})],
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

com['packets'].append({
'type': 'function',
'name': 'Set Touch LED Config',
'elements': [('Config', 'uint8', 1, 'in', {'constant_group': 'Touch LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Configures the touch LED to be either turned off, turned on, blink in
heartbeat mode or show the touch state (electrode touched = LED on).
""",
'de':
"""
Konfiguriert die Touch-LED. Die LED kann ausgeschaltet, eingeschaltet,
im Herzschlagmodus betrieben werden. Zusätzlich gibt es die Option
mit der LED den Touch-Zustand anzuzeigen (Elektrode berührt = LED an).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Touch LED Config',
'elements': [('Config', 'uint8', 1, 'out', {'constant_group': 'Touch LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the LED configuration as set by :func:`Set Touch LED Config`
""",
'de':
"""
Gibt die LED-Konfiguration zurück, wie von :func:`Set Touch LED Config` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Touch State', 'touch state'), [(('State', ['Electrode {}'.format(i) for i in range(0, 12)] + ['Proximity']), 'bool', 13, None, None, None)], [])],
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Touch State', 'touch state'), [(('State', ['Electrode {}'.format(i) for i in range(0, 12)] + ['Proximity']), 'bool', 13, None, None, None)], None, None),
              ('callback_configuration', ('Touch State', 'touch state'), [], 10, True, None, [])],
})

def electrode_channel(idx):
    return {
        'predicate': 'cfg.electrode{}Enabled'.format(idx),
        'id': 'Electrode {}'.format(idx),
        'label': {'en': 'Electrode {}'.format(idx), 'de': 'Elektrode {}'.format(idx)},
        'type': 'Electrode',
        'getters': [{
            'packet': 'Get Touch State',
            'element': 'State',
            'transform': 'value[{}] ? OpenClosedType.CLOSED : OpenClosedType.OPEN'.format(idx)}],

        'callbacks': [{
            'packet': 'Touch State',
            'element': 'State',
            'transform': 'state[{}] ? OpenClosedType.CLOSED : OpenClosedType.OPEN'.format(idx)}],
    }

def electrode_config(idx):
    return {
            'packet': 'Set Electrode Config',
            'element': 'Enabled Electrodes',
            'element_index': idx,

            'name': 'Electrode {} Enabled'.format(idx),
            'type': 'boolean',

            'label': {'en': 'Electrode {} Enabled'.format(idx), 'de': 'Elektrode {} aktiviert'.format(idx)},
            'description': {'en': "A disabled electrode will always return false as its state. If you don't need all electrodes you can disable the electrodes that are not needed. Disabling electrodes will also reduce power consumption.",
                            'de': 'Eine deaktivierte Elektrode hat immer den Zustand false. Wenn nicht alle Elektroden gebraucht werden können die ungebrauchten deaktiviert werden. Eine deaktivierte Elektrode verringert zusätzlich den Stromverbrauch.'}
        }

com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.OpenClosedType', 'org.eclipse.smarthome.core.library.types.StringType'],
    'param_groups': oh_generic_channel_param_groups(),
    'params': [{
            'packet': 'Set Electrode Sensitivity',
            'element': 'Sensitivity',

            'name': 'Sensitivity',
            'type': 'integer',
            'label': {'en': 'Sensitivity', 'de': 'Empfindlichkeit'},
            'description': {'en': 'The sensitivity of the electrodes. An electrode with a high sensitivity will register a touch earlier then an electrode with a low sensitivity.\n\nIf you build a big electrode you might need to decrease the sensitivity, since the area that can be charged will get bigger. If you want to be able to activate an electrode from further away you need to increase the sensitivity.',
                            'de': 'Die Empfindlichkeit der Elektroden. Eine Elektrode mit einer hohen Empfindlichkeit registriert eine Berührung früher als eine Elektrode mit einer niedrigen Empfindlichkeit.\n\nWenn eine große Elektrode verwendet wird sollte die Empfindlichkeit verringert werden, da eine größere Fläche aufgeladen werden kann. Wenn eine Elektrode aus größerem Abstand aktivierbar seien soll, muss die Empfindlichkeit vergrößert werden.'}
        }, {
            'packet': 'Set Electrode Config',
            'element': 'Enabled Electrodes',
            'element_index': 12,

            'name': 'Proximity Enabled',
            'type': 'boolean',

            'label': {'en': 'Proximity Detection', 'de': 'Proximity(Nähe)-Detektion'},
            'description': {'en': "It is recommended that you disable the proximity feature if not needed. This will reduce the amount of traffic that is produced.",
                            'de': "Wir empfehlen die Proximity-Detektion zu deaktivieren wenn das Proximity-Feature nicht benötigt wird. Das verringert den Datenverkehr der ausgelöst wird."}
        }, {
            'packet': 'Set Touch LED Config',
            'element': 'Config',

            'name': 'Touch LED Mode',
            'type': 'integer',

            'label': {'en': 'Touch LED', 'de': 'Touch-LED'},
            'description': {'en': 'Configures the touch LED to be either turned off, turned on, blink in heartbeat mode or show the touch state (electrode touched = LED on).',
                            'de': 'Konfiguriert die Touch-LED. Die LED kann ausgeschaltet, eingeschaltet, im Herzschlagmodus betrieben werden. Zusätzlich gibt es die Option mit der LED den Touch-Zustand anzuzeigen (Elektrode berührt = LED an).'}
        },
        update_interval('Set Touch State Callback Configuration', 'Period', 'Electrode', 'the electrode and proximity state')
    ] + [electrode_config(i) for i in range(0, 12)],
    'init_code': """this.setElectrodeSensitivity(cfg.sensitivity.shortValue());
        this.recalibrate();
        this.setElectrodeConfig(new boolean[]{{{}, cfg.proximityEnabled}});
        this.setTouchLEDConfig(cfg.touchLEDMode);
        this.setTouchStateCallbackConfiguration(cfg.electrodeUpdateInterval, true);""".format(', '.join(['cfg.electrode{}Enabled'.format(i) for i in range(0, 12)])),
    'channels': [electrode_channel(i) for i in range(0, 12)] + [
        {
            'predicate': 'cfg.proximityEnabled',
            'id': 'Proximity',
            'label': {'en': 'Proximity', 'de': 'Proximity'},
            'description': {'en': 'If a hand or similar is in proximity to the electrodes, this channel is toggled. The proximity is activated with a distance of 1-2cm. This means that you can put a piece of paper or foil or similar on top of a electrode to build a touch panel with a professional look.',
                            'de': 'Wenn eine Hand oder vergleichbares in der Nähe der Elektroden ist wird dieser Channel ausgelöst.\n\nDas Proximity Bit wird ab einer Distanz von ca. 1-2cm aktiviert. Eine Elektrode wird schon als berührt gezählt wenn ein Finger sie beinahe berührt. Dadurch ist es möglich ein Stück Papier oder Folie über die Elektrode zu kleben um damit ein Touchpanel mit einem professionellen Aussehen zu bauen.'},
            'type': 'Electrode',
            'getters': [{
                'packet': 'Get Touch State',
                'element': 'State',
                'transform': 'value[12] ? OpenClosedType.CLOSED : OpenClosedType.OPEN'}],

            'callbacks': [{
                'packet': 'Touch State',
                'element': 'State',
                'transform': 'state[12] ? OpenClosedType.CLOSED : OpenClosedType.OPEN'}]
        },
        {
            'id': 'Recalibrate',
            'type': 'Recalibrate',
            'setters': [{
                'packet': 'Recalibrate',
                'command_type': "StringType" # Command type has to be string type to be able to use command options.
            }],

        },
    ],
    'channel_types': [
        {
            'id': 'Electrode',
            'item_type': 'Contact',
            'label': 'NOT USED',
            'description': {'en': 'The current touch state. An electrode is already counted as touched if a finger is nearly touching the electrode. This means that you can put a piece of paper or foil or similar on top of a electrode to build a touch panel with a professional look.',
                            'de': 'Eine Elektrode wird schon als berührt gezählt wenn ein Finger sie beinahe berührt. Dadurch ist es möglich ein Stück Papier oder Folie über die Elektrode zu kleben um damit ein Touchpanel mit einem professionellen Aussehen zu bauen.'}
        },
        {
            'id': 'Recalibrate',
            'item_type': 'String',
            'label': {'en': 'Recalibrate Electrodes', 'de': 'Elektroden rekalibrieren'},
            'description': {'en': 'Recalibrates the electrodes. Trigger this channel whenever you changed or moved you electrodes.',
                            'de': 'Rekalibriert die Elektroden. Löse diesen Channel aus auf wenn die Elektroden verändert oder bewegt wurden.'},
            'command_options': [('Trigger', 'TRIGGER')]
        }
    ],
    'actions': ['Get Touch State', 'Recalibrate', 'Get Electrode Config', 'Get Electrode Sensitivity', 'Get Touch LED Config']
}
