# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Multi Touch Bricklet 2.0 communication config

from commonconstants import *

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
'elements': [('State', 'bool', 13, 'out')],
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
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period in ms is the period with which the :cb:`Touch State` callback
is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.

The default value is (0, false).
""",
'de':
"""
Die Periode in ms ist die Periode mit der der :cb:`Touch State` Callback
ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn der Wert sich im Vergleich zum letzten mal geändert
hat. Ändert der Wert sich nicht innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen des Werts.

Der Standardwert ist (0, false).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Touch State Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
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
'elements': [('State', 'bool', 13, 'out')],
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
'elements': [('Enabled Electrodes', 'bool', 13, 'in')],
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

Default: All electrodes enabled.
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

Standardwert: Alle Elektroden aktiviert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Electrode Config',
'elements': [('Enabled Electrodes', 'bool', 13, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the electrode configuration, as set by :func:`Set Electrode Config`.
""",
'de':
"""
Gibt die Elektrodenkonfiguration zurück, wie von :func:`Set Electrode Config`
gesetzt.
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set Electrode Sensitivity',
'elements': [('Sensitivity', 'uint8', 1, 'in')],
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

The valid sensitivity value range is 5-201.

The default sensitivity value is 181.
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

Der zulässige Wertebereich für den Empfindlichkeitswert ist 5-201.

Der voreingestellte Empfindlichkeitswert ist 181.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Electrode Sensitivity',
'elements': [('Sensitivity', 'uint8', 1, 'out')],
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
'elements': [('Config', 'uint8', 1, 'in', {'constant_group': 'Touch LED Config'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Configures the touch LED to be either turned off, turned on, blink in
heartbeat mode or show the touch state (electrode touched = LED on).

The default value is 3 (show touch state).
""",
'de':
"""
Konfiguriert die Touch-LED. Die LED kann ausgeschaltet, eingeschaltet,
im Herzschlagmodus betrieben werden. Zusätzlich gibt es die Option
mit der LED den Touch-Zustand anzuzeigen (Elektrode berührt = LED an).

Der Standardwert ist 3 (Touch-Zustand).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Touch LED Config',
'elements': [('Config', 'uint8', 1, 'out', {'constant_group': 'Touch LED Config'})],
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
        'label': 'Electrode {}'.format(idx),
        'type': 'Electrode',
        'getters': [{
            'packet': 'Get Touch State',
            'transform': 'value[{}] ? OnOffType.ON : OnOffType.OFF'.format(idx)}],

        'callbacks': [{
            'packet': 'Touch State',
            'transform': 'state[{}] ? OnOffType.ON : OnOffType.OFF'.format(idx)}],
    }

def electrode_config(idx):
    return {
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
            'name': 'Sensitivity',
            'type': 'integer',
            'default': 181,
            'min': 5,
            'max': 201,

            'label': 'Sensitivity',
            'description': 'The sensitivity of the electrodes. An electrode with a high sensitivity will register a touch earlier then an electrode with a low sensitivity.<br/><br/>If you build a big electrode you might need to decrease the sensitivity, since the area that can be charged will get bigger. If you want to be able to activate an electrode from further away you need to increase the sensitivity.'
        }, {
            'name': 'Proximity Enabled',
            'type': 'boolean',
            'default': 'true',

            'label': 'Proximity Enabled',
            'description': "True enables the proximity feature, false disables it. It is recommended that you disable the proximity feature if not needed. This will reduce the amount of traffic that is produced.",
        }, {
            'name': 'Update Interval',
            'type': 'integer',
            'unit': 'ms',
            'label': 'Update Interval',
            'description': 'Specifies the update interval in milliseconds. A value of 0 disables automatic updates.',
            'default': 1000,
            'groupName': 'update_intervals'
        }
    ] + [electrode_config(i) for i in range(0, 12)],
    'init_code': """this.setElectrodeSensitivity(cfg.sensitivity.shortValue());this.recalibrate();
this.setTouchStateCallbackConfiguration(cfg.updateInterval, true);""",
    'channels': [electrode_channel(i) for i in range(0, 12)] + [
        {
            'predicate': 'cfg.proximityEnabled',
            'id': 'Proximity',
            'label': 'Proximity',
            'type': 'Electrode',
            'getters': [{
                'packet': 'Get Touch State',
                'transform': 'value[12] ? OnOffType.ON : OnOffType.OFF'}],

            'callbacks': [{
                'packet': 'Touch State',
                'transform': 'state[12] ? OnOffType.ON : OnOffType.OFF'}]
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
        #oh_generic_channel_type('Electrode', 'Switch', 'NOT USED', description='NOT USED'),
        {
            'id': 'Electrode',
            'item_type': 'Switch',
            'label': 'Electrode',
            'description': 'NOT USED'
        },
        {
            'id': 'Recalibrate',
            'item_type': 'String',
            'label': 'Recalibrate Electrodes',
            'description':'Recalibrates the electrodes. Trigger this channel whenever you changed or moved you electrodes.',
            'command_options': [('Trigger', 'TRIGGER')]
        }
    ]
}
