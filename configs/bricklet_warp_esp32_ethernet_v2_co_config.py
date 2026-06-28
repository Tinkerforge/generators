# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# WARP ESP32 Ethernet 2.0 Co communication config

from generators.configs.commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from generators.configs.commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2184,
    'name': 'WARP ESP32 Ethernet V2 Co',
    'display_name': 'WARP ESP32 Ethernet 2.0 Co',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Real-time clock, temperature sensor and status LED for the WARP ESP32 Ethernet 2.0',
        'de': 'Echtzeituhr, Temperatursensor und Status-LED für das WARP ESP32 Ethernet 2.0'
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
'name': 'Data Status',
'type': 'uint8',
'constants': [('OK', 0),
              ('SD Error', 1),
              ('LFS Error', 2),
              ('Queue Full', 3),
              ('Date Out Of Range', 4)]
})

com['constant_groups'].append({
'name': 'Format Status',
'type': 'uint8',
'constants': [('OK', 0),
              ('Password Error', 1),
              ('Format Error', 2)]
})

com['constant_groups'].append({
'name': 'LED State',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Auto', 2)]
})

com['packets'].append({
'type': 'function',
'name': 'Set LED',
'elements': [('State', 'uint8', 1, 'in', {'constant_group': 'LED State'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the state of the status LED. *Off* turns the LED off, *On* turns it on and
*Auto* lets it blink at about 1 Hz.
""",
'de':
"""
Setzt den Zustand der Status-LED. *Off* schaltet die LED aus, *On* schaltet sie
ein und *Auto* lässt sie mit etwa 1 Hz blinken.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get LED',
'elements': [('State', 'uint8', 1, 'out', {'constant_group': 'LED State'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the state of the status LED as set by :func:`Set LED`.
""",
'de':
"""
Gibt den Zustand der Status-LED zurück, wie von :func:`Set LED` gesetzt.
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Get Temperature',
'elements': [('Temperature', 'int16', 1, 'out')], # Returns 0 in EVSE V2
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the temperature measured by the on-board sensor in 1/100 °C.
""",
'de':
"""
Gibt die vom On-Board-Sensor gemessene Temperatur in 1/100 °C zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Date Time',
'elements': [('Seconds', 'uint8', 1, 'in', {'range': (0, 59)}),
             ('Minutes', 'uint8', 1, 'in', {'range': (0, 59)}),
             ('Hours', 'uint8', 1, 'in', {'range': (0, 23)}),
             ('Days', 'uint8', 1, 'in', {'range': (0, 31)}),
             ('Days Of Week', 'uint8', 1, 'in', {'range': (0, 6)}), # 0 = Sunday, 1 = Monday, ...
             ('Month', 'uint8', 1, 'in', {'range': (0, 11)}),
             ('Year', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the date and time of the internal real-time clock. The day of the week is
0 for Sunday, 1 for Monday and so on.
""",
'de':
"""
Setzt das Datum und die Uhrzeit der internen Echtzeituhr. Der Wochentag ist
0 für Sonntag, 1 für Montag und so weiter.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Date Time',
'elements': [('Seconds', 'uint8', 1, 'out', {'range': (0, 59)}),
             ('Minutes', 'uint8', 1, 'out', {'range': (0, 59)}),
             ('Hours', 'uint8', 1, 'out', {'range': (0, 23)}),
             ('Days', 'uint8', 1, 'out', {'range': (0, 31)}),
             ('Days Of Week', 'uint8', 1, 'out', {'range': (0, 6)}), # 0 = Sunday, 1 = Monday, ...
             ('Month', 'uint8', 1, 'out', {'range': (0, 11)}),
             ('Year', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the date and time of the internal real-time clock as set by
:func:`Set Date Time`.
""",
'de':
"""
Gibt das Datum und die Uhrzeit der internen Echtzeituhr zurück, wie von
:func:`Set Date Time` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Uptime',
'elements': [('Uptime', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the uptime of the Bricklet in milliseconds.
""",
'de':
"""
Gibt die Uptime des Bricklets in Millisekunden zurück.
"""
}]
})

com['packets'].append({ # unused
'type': 'function',
'name': 'Format SD',
'elements': [('Password', 'uint32', 1, 'in'), # Password: 0x4223ABCD
             ('Format Status', 'uint8', 1, 'out', {'constant_group': 'Format Status'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Not supported by current hardware version.
""",
'de':
"""
Wird von der aktuellen Hardware-Version nicht unterstützt.
"""
}]
})

com['packets'].append({ # unused
'type': 'function',
'name': 'Get SD Information',
'elements': [('SD Status', 'uint32', 1, 'out'),
             ('LFS Status', 'uint32', 1, 'out'),
             ('Sector Size', 'uint16', 1, 'out'),
             ('Sector Count', 'uint32', 1, 'out'),
             ('Card Type', 'uint32', 1, 'out'),
             ('Product Rev', 'uint8', 1, 'out'),
             ('Product Name', 'char', 5, 'out'),
             ('Manufacturer ID', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Not supported by current hardware version.
""",
'de':
"""
Wird von der aktuellen Hardware-Version nicht unterstützt.
"""
}]
})


com['packets'].append({
'type': 'callback',
'name': 'RMMI Interrupt',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered when an interrupt is signaled on the RMII interrupt
line of the Ethernet PHY. The callback is debounced and triggered at most once
every 250 ms.
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn auf der RMII-Interrupt-Leitung des
Ethernet-PHY ein Interrupt signalisiert wird. Der Callback ist entprellt und
wird höchstens einmal alle 250 ms ausgelöst.
"""
}]
})
