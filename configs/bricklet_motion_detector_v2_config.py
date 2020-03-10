# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Motion Detector Bricklet 2.0 communication config

from openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 292,
    'name': 'Motion Detector V2',
    'display_name': 'Motion Detector 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Passive infrared (PIR) motion sensor with 12m range and dimmable backlight',
        'de': 'Passiver Infrarot (PIR) Bewegungssensor mit 12m Reichweite und dimmbarer Beleuchtung'
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
'name': 'Motion',
'type': 'uint8',
'constants': [('Not Detected', 0),
              ('Detected', 1)]
})

com['packets'].append({
'type': 'function',
'name': 'Get Motion Detected',
'elements': [('Motion', 'uint8', 1, 'out', {'constant_group': 'Motion'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns 1 if a motion was detected. It returns 1 approx. for 1.8 seconds
until the sensor checks for a new movement.

There is also a blue LED on the Bricklet that is on as long as the Bricklet is
in the "motion detected" state.
""",
'de':
"""
Gibt 1 zurück wenn eine Bewegung detektiert wurde. 1 wird für ca. 1,8 Sekunden
zurückgegeben bevor der Sensor wieder erneut eine Bewegung detektieren kann.

Auf dem Bricklet selbst ist eine blaue LED, die leuchtet solange das Bricklet
im "Bewegung detektiert" Zustand ist.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Sensitivity',
'elements': [('Sensitivity', 'uint8', 1, 'in', {'range': (0, 100), 'default': 50})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the sensitivity of the PIR sensor. At full
sensitivity (100), the Bricklet can detect motion in a range of approximately 12m.

The actual range depends on many things in the environment (e.g. reflections) and the
size of the object to be detected. While a big person might be detected in a range
of 10m a cat may only be detected at 2m distance with the same setting.

So you will have to find a good sensitivity for your application by trial and error.
""",
'de':
"""
Setzt die Empfindlichkeit des PIR Sensors. Bei
maximaler Empfindlichkeit (100) kann das Bricklet Bewegung bin in ca. 12m
Entfernung erkennen.

Die wirkliche Entfernung hängt von vielen Dingen in der Umgebung ab (z.B.
Ruflektionen) und der Größe des zu erkennenden Objekts. Während eine große
Person bei 10m erkannt werden kann, wird eine Katze vielleicht erst an 2m erkannt
mit den gleichen Einstellungen.

Daher muss die passenden Empfindlichkeit je nach Anwendung experimentell
bestimmt werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Sensitivity',
'elements': [('Sensitivity', 'uint8', 1, 'out', {'range': (0, 100), 'default': 50})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the sensitivity as set by :func:`Set Sensitivity`.
""",
'de':
"""
Gibt die Empfindlichkeit zurück, wie von :func:`Set Sensitivity` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Indicator',
'elements': [('Top Left', 'uint8', 1, 'in', {'default': 0}),
             ('Top Right', 'uint8', 1, 'in', {'default': 0}),
             ('Bottom', 'uint8', 1, 'in', {'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the blue backlight of the fresnel lens. The backlight consists of
three LEDs. The brightness of each LED can be controlled with a 8-bit value
(0-255). A value of 0 turns the LED off and a value of 255 turns the LED
to full brightness.
""",
'de':
"""
Stellt die blaue Beleuchtung der Fresnel-Linse ein. Die Beleuchtung besteht aus
drei LEDs. Die Helligkeit jeder LED kann einzeln mit einem 8-Bit Wert (0-255)
eingestellt werden. Ein Wert von 0 deaktiviert die LED und ein Wert von 255
aktiviert die LED mit voller Helligkeit.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Indicator',
'elements': [('Top Left', 'uint8', 1, 'out', {'default': 0}),
             ('Top Right', 'uint8', 1, 'out', {'default': 0}),
             ('Bottom', 'uint8', 1, 'out', {'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the indicator configuration as set by :func:`Set Indicator`.
""",
'de':
"""
Gibt die Indikatorkonfiguration zurück, wie von :func:`Set Indicator` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Motion Detected',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called after a motion was detected.
""",
'de':
"""
Dieser Callback wird aufgerufen nachdem eine Bewegung detektiert wurde.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Detection Cycle Ended',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is called when the detection cycle ended. When this
callback is called, a new motion can be detected again after approximately 2
seconds.
""",
'de':
"""
Dieser Callback wird aufgerufen wenn ein Bewegungserkennungszyklus
beendet ist. Wenn dieser Callback aufgerufen wurde kann wieder
eine weitere Bewegung erkannt werden nach ungefähr 2 Sekunden.
"""
}]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Motion Detected', 'motion detected'), [], None, 'Motion Detected'),
              ('callback', ('Detection Cycle Ended', 'detection cycle ended'), [], None, 'Detection Cycle Ended (next detection possible in ~2 seconds)')]
})

com['examples'].append({
'name': 'Indicator',
'functions': [('setter', 'Set Indicator', [('uint8', 255), ('uint8', 255), ('uint8', 255)], 'Turn blue backlight LEDs on (maximum brightness)', None)]
})


com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'params': [{
            'packet': 'Set Sensitivity',
            'element': 'Sensitivity',

            'name': 'Sensitivity',
            'type': 'integer',
            'default': 50,
            'min': 0,
            'max': 100,

            'label': 'Sensitivity',
            'description': 'The sensitivity of the PIR sensor. The range is 0-100. At full sensitivity (100), the Bricklet can detect motion in a range of approximately 12m.<br/><br/>The actual range depends on many things in the environment (e.g. reflections) and the size of the object to be detected. While a big person might be detected in a range of 10m a cat may only be detected at 2m distance with the same setting. So you will have to find a good sensitivity for your application by trial and error.'
    }],
    'init_code': "this.setSensitivity(cfg.sensitivity);",
    'channels': [
        {
            'id': 'Motion Detected',
            'label': 'Motion Detected',
            'type': 'system.trigger',

            'callbacks': [{
                'packet': 'Motion Detected',
                'transform': '""'}],

            'is_trigger_channel': True,
            'description': 'This channel is triggered after a motion was detected.'
        }, {
            'id': 'Detection Cycle Ended',
            'label': 'Detection Cycle Ended',
            'type': 'system.trigger',

            'callbacks': [{
                'packet': 'Detection Cycle Ended',
                'transform': '""'}],

            'is_trigger_channel': True,
            'description': 'This channel is triggered when the detection cycle ended. A new motion can be detected again after approximately 2 seconds.'
        },

        {
            'id': 'Top Left Indicator',
            'label': 'Top Left Indicator',
            'type': 'Indicator',

            'getters': [{
                'packet': 'Get Indicator',
                'element': 'Top Left',
                'transform': 'new QuantityType<>(value.topLeft, {unit})'}],

            'setters': [{
                'packet': 'Set Indicator',
                'element': 'Top Left',
                'packet_params': ['cmd.intValue()', 'this.getIndicator().topRight', 'this.getIndicator().bottom'],
                'command_type': 'Number',
            }],

            'java_unit': 'SmartHomeUnits.ONE'
        },{
            'id': 'Top Right Indicator',
            'label': 'Top Right Indicator',
            'type': 'Indicator',
            'getters': [{
                'packet': 'Get Indicator',
                'element': 'Top Right',
                'transform': 'new QuantityType<>(value.topRight, {unit})'}],

            'setters': [{
                'packet': 'Set Indicator',
                'element': 'Top Right',
                'packet_params': [ 'this.getIndicator().topLeft', 'cmd.intValue()', 'this.getIndicator().bottom'],
                'command_type': 'Number',
            }],

            'java_unit': 'SmartHomeUnits.ONE'
        },{
            'id': 'Bottom Indicator',
            'label': 'Bottom Indicator',
            'type': 'Indicator',
            'getters': [{
                'packet': 'Get Indicator',
                'element': 'Bottom',
                'transform': 'new QuantityType<>(value.bottom, {unit})'}],

            'setters': [{
                'packet': 'Set Indicator',
                'element': 'Bottom',
                'packet_params': ['this.getIndicator().topLeft', 'this.getIndicator().topRight', 'cmd.intValue()'],
                'command_type': 'Number',
            }],

            'java_unit': 'SmartHomeUnits.ONE'
        }
    ],
    'channel_types': [
        oh_generic_channel_type('Indicator', 'Number:Dimensionless', 'NOT USED',
                    update_style=None,
                    description='Sets one of the blue backlight LEDs of the fresnel lens. A value of 0 turns the LED off and a value of 255 turns the LED to full brightness.',
                    pattern='%d',
                    min_=0,
                    max_=255)
    ],
    'actions': ['Get Motion Detected', 'Get Sensitivity', {'fn': 'Set Indicator', 'refreshs': ['Top Left Indicator', 'Top Right Indicator', 'Bottom Indicator']}, 'Get Indicator']
}
