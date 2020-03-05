# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Piezo Speaker Bricklet 2.0 communication config

from openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2145,
    'name': 'Piezo Speaker V2',
    'display_name': 'Piezo Speaker 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Creates beep and alarm with configurable volume and frequency',
        'de': 'Erzeugt Piepton und Alarm mit konfigurierbarer Lautstärke und Frequenz'
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
'name': 'Beep Duration',
'type': 'uint32',
'constants': [('Off', 0),
              ('Infinite', 4294967295)]
})

com['constant_groups'].append({
'name': 'Alarm Duration',
'type': 'uint32',
'constants': [('Off', 0),
              ('Infinite', 4294967295)]
})

com['packets'].append({
'type': 'function',
'name': 'Set Beep',
'elements': [('Frequency', 'uint16', 1, 'in', {'unit': 'Hertz', 'range': (50, 15000)}),
             ('Volume', 'uint8', 1, 'in', {'range': (0, 10)}),
             ('Duration', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'range': 'type', 'constant_group': 'Beep Duration'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Beeps with the given frequency and volume for the duration.

A duration of 0 stops the current beep if any is ongoing.
A duration of 4294967295 results in an infinite beep.
""",
'de':
"""
Erzeugt einen Piepton mit der gegebenen Frequenz und Lautstärke für die
angegebene Dauer.

Eine *duration* von 0 stoppt den aktuellen Piepton.
Eine *duration* von 4294967295 führt zu einem unendlich langen Piepton.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Beep',
'elements': [('Frequency', 'uint16', 1, 'out', {'unit': 'Hertz', 'range': (50, 15000)}),
             ('Volume', 'uint8', 1, 'out', {'range': (0, 10)}),
             ('Duration', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'range': 'type', 'constant_group': 'Beep Duration'}),
             ('Duration Remaining', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the last beep settings as set by :func:`Set Beep`. If a beep is currently
running it also returns the remaining duration of the beep.

If the frequency or volume is updated during a beep (with :func:`Update Frequency`
or :func:`Update Volume`) this function returns the updated value.
""",
'de':
"""
Gibt die letzten Beep-Einstellungen zurück, wie von :func:`Set Beep` gesetzt. Wenn ein
Beep aktuell läuft, wird auch die verbleibende Zeit des Beeps zurück gegeben.

Wenn die Frequenz oder Lautstärke während eines Beeps aktualisiert wird (mit
:func:`Update Frequency` oder :func:`Update Volume`), gibt diese Funktion die
aktualisierten Werte zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Alarm',
'elements': [('Start Frequency', 'uint16', 1, 'in', {'unit': 'Hertz', 'range': (50, 14999)}),
             ('End Frequency', 'uint16', 1, 'in', {'unit': 'Hertz', 'range': (51, 15000)}),
             ('Step Size', 'uint16', 1, 'in', {'unit': 'Hertz', 'range': (0, 14950)}),
             ('Step Delay', 'uint16', 1, 'in', {'scale': (1, 1000), 'unit': 'Second'}),
             ('Volume', 'uint8', 1, 'in', {'range': (0, 10)}),
             ('Duration', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'range': 'type', 'constant_group': 'Alarm Duration'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Creates an alarm (a tone that goes back and force between two specified frequencies).

The following parameters can be set:

* Start Frequency: Start frequency of the alarm.
* End Frequency: End frequency of the alarm.
* Step Size: Size of one step of the sweep between the start/end frequencies.
* Step Delay: Delay between two steps (duration of time that one tone is used in a sweep).
* Duration: Duration of the alarm.

A duration of 0 stops the current alarm if any is ongoing.
A duration of 4294967295 results in an infinite alarm.

Below you can find two sets of example settings that you can try out. You can use
these as a starting point to find an alarm signal that suits your application.

Example 1: 10 seconds of loud annoying fast alarm

* Start Frequency = 800
* End Frequency = 2000
* Step Size = 10
* Step Delay = 1
* Volume = 10
* Duration = 10000

Example 2: 10 seconds of soft siren sound with slow build-up

* Start Frequency = 250
* End Frequency = 750
* Step Size = 1
* Step Delay = 5
* Volume = 0
* Duration = 10000

The following conditions must be met:

* Start Frequency: has to be smaller than end frequency
* End Frequency: has to be bigger than start frequency
* Step Size: has to be small enough to fit into the frequency range
* Step Delay: has to be small enough to fit into the duration
""",
'de':
"""
Startet einen Alarm (Einen Ton der zwischen zwei spezifizierten Frequenzen
hin und her läuft).

Die folgenden Parameter können genutzt werden:

* *Start Frequency*: Startfrequenz des Alarms.
* *End Frequency*: Endfrequenz des Alarms.
* *Step Size*: Schrittgröße eines Schritts im Frequenzdurchlauf zwischen Start-/Endfrequenz.
* *Step Delay*: Zeit zwischen zwei Schritten (Dauer eines Tons im Frequenzdurchlauf).
* *Duration*: Dauer des Alarm.

Nachfolgend gibt es zwei Beispiele zum ausprobieren. Diese Beispiele können
als Startpunkt genutzt werden um ein Alarm-Signal passend für die eigene Anwendung
zu entwerfen.

*Beispiel 1: 10 Sekunden eines lauten nervigen schnellen Alarms*

* *Start Frequency* = 800
* *End Frequency* = 2000
* *Step Size* = 10
* *Step Delay* = 1
* *Volume* = 10
* *Duration* = 10000

*Beispiel 2: 10 Sekunden eines Sirenengeräusches mit langsamen Frequenzdurchlauf*

* *Start Frequency* = 250
* *End Frequency* = 750
* *Step Size* = 1
* *Step Delay* = 5
* *Volume* = 0
* *Duration* = 10000

Die folgenden Einschränkungen müssen eingehalten werden:

* *Start Frequency*: muss kleiner als *End Frequency* sein
* *End Frequency*: muss größer als *Start Frequency* sein
* *Step Size*: muss klein genug sein um in den Frequenzbereich zu passen
* *Step Delay*: muss kleiner als *Duration* sein
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Alarm',
'elements': [('Start Frequency', 'uint16', 1, 'out', {'unit': 'Hertz', 'range': (50, 14999)}),
             ('End Frequency', 'uint16', 1, 'out', {'unit': 'Hertz', 'range': (51, 15000)}),
             ('Step Size', 'uint16', 1, 'out', {'unit': 'Hertz', 'range': (50, 14950)}),
             ('Step Delay', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'}),
             ('Volume', 'uint8', 1, 'out', {'range': (0, 10)}),
             ('Duration', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'range': 'type', 'constant_group': 'Alarm Duration'}),
             ('Duration Remaining', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'range': 'type', 'constant_group': 'Alarm Duration'}),
             ('Current Frequency', 'uint16', 1, 'out', {'unit': 'Hertz', 'range': (50, 15000)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the last alarm settings as set by :func:`Set Alarm`. If an alarm is currently
running it also returns the remaining duration of the alarm as well as the
current frequency of the alarm.

If the volume is updated during an alarm (with :func:`Update Volume`)
this function returns the updated value.
""",
'de':
"""
Gibt die letzten Alarm-Einstellungen zurück, wie von :func:`Set Alarm` gesetzt. Wenn ein
Alarm aktuell läuft, wird auch die verbleibende Zeit des Alarms sowie die aktuelle
Frequenz zurück gegeben.

Wenn die Lautstärke während eines Alarms aktualisiert wird (mit :func:`Update Volume`),
gibt diese Funktion die aktualisierten Werte zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Update Volume',
'elements': [('Volume', 'uint8', 1, 'in', {'range': (0, 10)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Updates the volume of an ongoing beep or alarm.
""",
'de':
"""
Aktualisiert die Lautstärke eines aktuell laufenden Beep oder Alarm.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Update Frequency',
'elements': [('Frequency', 'uint16', 1, 'in', {'unit': 'Hertz', 'range': (50, 15000)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Updates the frequency of an ongoing beep.
""",
'de':
"""
Aktualisiert die Frequenz eines aktuell laufenden Beeps.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Beep Finished',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered if a beep set by :func:`Set Beep` is finished
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn ein Piepton, wie von :func:`Set Beep` gesetzt,
beendet wurde.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Alarm Finished',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered if a alarm set by :func:`Set Alarm` is finished
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn ein Alarm, wie von :func:`Set Alarm` gesetzt,
beendet wurde.
"""
}]
})

com['examples'].append({
'name': 'Beep',
'functions': [('setter', 'Set Beep', [('uint16', 1000), ('uint8', 0), ('uint32', 2000)], 'Make 2 second beep with a frequency of 1kHz', None)]
})

com['examples'].append({
'name': 'Alarm',
'functions': [('setter', 'Set Alarm', [('uint16', 800), ('uint16', 2000), ('uint16', 10), ('uint16', 1), ('uint8', 10), ('uint32', 10000)], '10 seconds of loud annoying fast alarm', None)]
})

com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.OnOffType',
                                               'org.eclipse.smarthome.core.library.types.DecimalType'],
    'param_groups': oh_generic_channel_param_groups(),
    'channels': [
        {
            'id': 'Beep',
            'type': 'Beep',
            'label': 'Beep',

            'setters': [{
                'packet': 'Set Beep',
                'packet_params': ['channelCfg.defaultFrequency, channelCfg.defaultVolume, cmd == OnOffType.ON ? channelCfg.duration.longValue() : 0'],
                'command_type': "OnOffType"
            }],

            'setter_refreshs': [{
                'channel': 'Volume',
                'delay': 0
            }, {
                'channel': 'Beep Frequency',
                'delay': 0
            }],

            'getters': [{
                'packet': 'Get Beep',
                'transform': 'value.durationRemaining > 0 ? OnOffType.ON : OnOffType.OFF'}],

            'callbacks': [{
                'packet': 'Beep Finished',
                'transform': 'OnOffType.OFF'}],
        },  {
            'id': 'Alarm',
            'type': 'Alarm',
            'label': 'Alarm',

            'setters': [{
                'packet': 'Set Alarm',
                'packet_params': ['channelCfg.startFrequency, channelCfg.endFrequency, channelCfg.stepSize, channelCfg.stepDelay, channelCfg.defaultVolume, cmd == OnOffType.ON ? channelCfg.duration : 0'],
                'command_type': "OnOffType"
            }],

            'setter_refreshs': [{
                'channel': 'Volume',
                'delay': 0
            }],

            'getters': [{
                'packet': 'Get Alarm',
                'transform': 'value.durationRemaining > 0 ? OnOffType.ON : OnOffType.OFF'}],

            'callbacks': [{
                'packet': 'Alarm Finished',
                'transform': 'OnOffType.OFF'}],
        }, {
            'id': 'Volume',
            'type': 'Volume',
            'label': 'Volume',

            'setters': [{
                'packet': 'Update Volume',
                'packet_params': ['cmd.intValue()'],
                'command_type': "Number"
            }],


            'getters': [{
                'packet': 'Get Beep',
                'predicate': 'value.durationRemaining > 0',
                'transform': 'new DecimalType(value.volume)'
            }, {
                'packet': 'Get Alarm',
                'predicate': 'value.durationRemaining > 0',
                'transform': 'new DecimalType(value.volume)'
            }]
        }, {
            'id': 'Beep Frequency',
            'type': 'Beep Frequency',
            'label': 'Beep Frequency',

            'setters': [{
                'packet': 'Update Frequency',
                'packet_params': ['cmd.intValue()'],
                'command_type': "Number"
            }],

            'getters': [{
                    'packet': 'Get Beep',
                    'predicate': 'value.durationRemaining > 0',
                    'transform': 'new QuantityType<>(value.frequency, SmartHomeUnits.HERTZ)'
            }]
        }
    ],
    'channel_types': [
        oh_generic_channel_type('Beep', 'Switch', 'Beep',
                    update_style=None,
                    description='Beeps with the configured default frequency and volume for the configured duration. Frequency and Volume can be updated using the corresponding channels.',
                    read_only=False,
                    params=[{
                            'packet': 'Set Beep',
                            'element': 'Frequency',

                            'name': 'Default Frequency',
                            'type': 'integer',
                            'default': 2000,
                            'min': 50,
                            'max': 15000,
                            'label': 'Default Frequency',
                            'description': 'The frequency in Hz to start the beep with. The range of the frequency is 50Hz to 15000Hz.'
                        }, {
                            'packet': 'Set Beep',
                            'element': 'Volume',

                            'name': 'Default Volume',
                            'type': 'integer',
                            'default': 0,
                            'min': 0,
                            'max': 10,
                            'label': 'Default Volume',
                            'description': 'The volume to start the beep with. The range of the volume is 0 to 10.'
                        },  {
                            'packet': 'Set Beep',
                            'element': 'Duration',

                            'name': 'Duration',
                            'type': 'decimal',
                            'default': 0,
                            'min': 0,
                            'max': '4294967295L',
                            'step': '1',
                            'label': 'Duration',
                            'description': 'The duration in ms to beep for. A duration of 0 stops the current beep if any is ongoing. A duration of 4294967295 results in an infinite beep.'
                    }]),
        oh_generic_channel_type('Alarm', 'Switch', 'Alarm',
                    update_style=None,
                    description='Creates an alarm (a tone that goes back and force between two specified frequencies). The following parameters can be set:<br/><br/><ul><li>Start Frequency: Start frequency of the alarm in Hz.</li></br><li>End Frequency: End frequency of the alarm in Hz.</li></br><li>Step Size: Size of one step of the sweep between the start/end frequencies in Hz.</li></br><li>Step Delay: Delay between two steps (duration of time that one tone is used in a sweep) in ms.</li></br><li>Duration: Duration of the alarm in ms.</li></ul></br><br/>A duration of 0 stops the current alarm if any is ongoing. A duration of 4294967295 results in an infinite alarm.',
                    read_only=False,
                    params=[{
                            'packet': 'Set Alarm',
                            'element': 'Start Frequency',

                            'name': 'Start Frequency',
                            'type': 'integer',
                            'default': 250,
                            'min': 50,
                            'max': 14999,
                            'label': 'Start Frequency',
                            'description': 'Start frequency of the alarm in Hz. The range of the start frequency is 50Hz to 14999Hz. (has to be smaller than end frequency)'
                        }, {
                            'packet': 'Set Alarm',
                            'element': 'End Frequency',

                            'name': 'End Frequency',
                            'type': 'integer',
                            'default': 750,
                            'min': 51,
                            'max': 15000,
                            'label': 'End Frequency',
                            'description': 'End frequency of the alarm in Hz. The range of the end frequency is 51Hz to 15000Hz. (has to be bigger than start frequency)'
                        }, {
                            'packet': 'Set Alarm',
                            'element': 'Step Size',

                            'name': 'Step Size',
                            'type': 'integer',
                            'default': 1,
                            'min': 1,
                            'max': 14950,
                            'label': 'Step Size',
                            'description': 'Size of one step of the sweep between the start/end frequencies in Hz. 1Hz - 65536Hz (has to be small enough to fit into the frequency range)'
                        }, {
                            'packet': 'Set Alarm',
                            'element': 'Step Delay',

                            'name': 'Step Delay',
                            'type': 'integer',
                            'default': 1,
                            'min': 0,
                            'max': 65535,
                            'label': 'Step Delay',
                            'description': 'Delay between two steps (duration of time that one tone is used in a sweep) in ms. 1ms - 65535ms (has to be small enough to fit into the duration)'
                        },{
                            'packet': 'Set Alarm',
                            'element': 'Volume',

                            'name': 'Default Volume',
                            'type': 'integer',
                            'default': 0,
                            'min': 0,
                            'max': 10,
                            'label': 'Default Volume',
                            'description': 'The volume to start the alarm with. The range of the volume is 0 to 10.'
                        }, {
                            'packet': 'Set Alarm',
                            'element': 'Duration',

                            'name': 'Duration',
                            'type': 'integer',
                            'default': 0,
                            'min': 0,
                            'max': '4294967295L',
                            'label': 'Duration',
                            'description': 'The duration in ms to sound the alarm for. A duration of 0 stops the current alarm if any is ongoing. A duration of 4294967295 results in an infinite alarm.'
                        }
                    ]),
        oh_generic_channel_type('Volume', 'Number', 'Volume',
                    update_style=None,
                    description='Volume of an ongoing beep or alarm. The range of the volume is 0 to 10.',
                    read_only=False,
                    min_=0,
                    max_=10),
        oh_generic_channel_type('Beep Frequency', 'Number', 'Beep Frequency',
                    update_style=None,
                    description='Frequency of an ongoing beep. The range of the frequency is 50Hz to 15000Hz.',
                    read_only=False,
                    min_=50,
                    max_=15000),
    ],
    'actions': [{'fn': 'Set Beep', 'refreshs': ['Beep', 'Alarm']}, 'Get Beep', {'fn': 'Set Alarm', 'refreshs': ['Beep', 'Alarm']}, 'Get Alarm', 'Update Volume', 'Update Frequency']
}
