# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Analog Out Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 258,
    'name': 'Industrial Analog Out',
    'display_name': 'Industrial Analog Out',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Generates configurable DC voltage and current, 0V to 10V and 4mA to 20mA',
        'de': 'Erzeugt konfigurierbare Gleichspannung und -strom, 0V bis 10V und 4mA bis 20mA'
    },
    'released': True,
    'documented': True,
    'discontinued': False, # selling remaining stock, replaced by Industrial Analog Out Bricklet 2.0
    'features': [
        'bricklet_get_identity'
    ],
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Enable',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Enables the output of voltage and current.

The default is disabled.
""",
'de':
"""
Aktiviert die Ausgabe von Spannung und Strom.

Der Standardwert ist deaktiviert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Disable',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Disables the output of voltage and current.

The default is disabled.
""",
'de':
"""
Deaktiviert die Ausgabe von Spannung und Strom.

Der Standardwert ist deaktiviert.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Is Enabled',
'elements': [('Enabled', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns *true* if output of voltage and current is enabled, *false* otherwise.
""",
'de':
"""
Gibt *true* zurück falls die Ausgabe von Spannung und Strom aktiviert ist,
*false* sonst.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Voltage',
'elements': [('Voltage', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the output voltage in mV.

The output voltage and output current are linked. Changing the output voltage
also changes the output current.
""",
'de':
"""
Setzt die Ausgangsspannung in mV.

Die Ausgangsspannung und der Ausgangsstrom sind gekoppelt. Eine Änderung der
Ausgangsspannung führt auch zu einer Änderung des Ausgangsstroms.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Voltage',
'elements': [('Voltage', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the voltage as set by :func:`Set Voltage`.
""",
'de':
"""
Gibt die Spannung zurück, wie von :func:`Set Voltage` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Current',
'elements': [('Current', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the output current in µA.

The output current and output voltage are linked. Changing the output current
also changes the output voltage.
""",
'de':
"""
Setzt den Ausgangsstrom in µA.

Der Ausgangsstrom und die Ausgangsspannung sind gekoppelt. Eine Änderung des
Ausgangsstroms führt auch zu einer Änderung der Ausgangsspannung.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Current',
'elements': [('Current', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current as set by :func:`Set Current`.
""",
'de':
"""
Gibt die Spannung zurück, wie von :func:`Set Current` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('Voltage Range', 'uint8', 1, 'in', ('Voltage Range', [('0 To 5V', 0),
                                                                    ('0 To 10V', 1)])),
             ('Current Range', 'uint8', 1, 'in', ('Current Range', [('4 To 20mA', 0),
                                                                    ('0 To 20mA', 1),
                                                                    ('0 To 24ma', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Configures the voltage and current range.

Possible voltage ranges are:

* 0V to 5V
* 0V to 10V (default)

Possible current ranges are:

* 4mA to 20mA (default)
* 0mA to 20mA
* 0mA to 24mA

The resolution will always be 12 bit. This means, that the
precision is higher with a smaller range.
""",
'de':
"""
Konfiguriert die Spannungs- und Stromwertebereiche.

Einstellbare Spannungswertebereiche sind:

* 0V bis 5V
* 0V bis 10V (Standard)

Einstellbare Stromwertebereiche sind:

* 4mA bis 20mA (Standard)
* 0mA bis 20mA
* 0mA bis 24mA

Die Auflösung ist immer 12 Bit. Dass heißt, die Genauigkeit erhöht
sich bei kleineren Wertebereichen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Voltage Range', 'uint8', 1, 'out', ('Voltage Range', [('0 To 5V', 0),
                                                                     ('0 To 10V', 1)])),
             ('Current Range', 'uint8', 1, 'out', ('Current Range', [('4 To 20mA', 0),
                                                                     ('0 To 20mA', 1),
                                                                     ('0 To 24ma', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Configuration` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple Voltage',
'functions': [('setter', 'Set Voltage', [('uint16', 3300)], 'Set output voltage to 3.3V', None),
              ('setter', 'Enable', [], None, None),
              ('wait',)],
'cleanups': [('setter', 'Disable', [], None, None)]
})

com['examples'].append({
'name': 'Simple Current',
'functions': [('setter', 'Set Current', [('uint16', 4500)], 'Set output current to 4.5mA', None),
              ('setter', 'Enable', [], None, None),
              ('wait',)],
'cleanups': [('setter', 'Disable', [], None, None)]
})
