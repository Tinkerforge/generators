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
    'name': ('IndustrialAnalogOut', 'industrial_analog_out', 'Industrial Analog Out', 'Industrial Analog Out Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Generates configurable DC voltage and current, 0V to 10V and 4mA to 20mA',
        'de': 'Erzeugt konfigurierbare Gleichspannung und -strom, 0V bis 10V und 4mA bis 20mA'
    },
    'released': False,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('Enable', 'enable'), 
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
'name': ('Disable', 'disable'), 
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
'name': ('IsEnabled', 'is_enabled'), 
'elements': [('enabled', 'bool', 1, 'out')],
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
'name': ('SetVoltage', 'set_voltage'), 
'elements': [('voltage', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the output voltage in mV.
""",
'de':
"""
Setzt die Ausgabespannung in mV.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetVoltage', 'get_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the voltage as set by :func:`SetVoltage`.
""",
'de':
"""
Gibt die Spannung zurück, wie von :func:`SetVoltage`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetCurrent', 'set_current'), 
'elements': [('current', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the output current in µA.
""",
'de':
"""
Setzt den Ausgabestrom in µA.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetCurrent', 'get_current'), 
'elements': [('current', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current as set by :func:`SetCurrent`.
""",
'de':
"""
Gibt die Spannung zurück, wie von :func:`SetCurrent`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetConfiguration', 'set_configuration'), 
'elements': [('voltage_range', 'uint8', 1, 'in', ('VoltageRange', 'voltage_range', [('0To5V', '0_to_5v', 0),
                                                                                    ('0To10V', '0_to_10v', 1)])),
             ('current_range', 'uint8', 1, 'in', ('CurrentRange', 'current_range', [('4To20mA', '4_to_20ma', 0),
                                                                                    ('0To20mA', '0_to_20ma', 1),
                                                                                    ('0To24mA', '0_to_24ma', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Configures the voltage and current range.

Possible voltage ranges are:

* 0V - 5V
* 0V - 10V

Possible current ranges are:

* 4mA to 20mA
* 0mA to 20mA
* 0mA to 24mA

The resolution will always be 12 bit. This means, that the
precision is higher with a smaller range.
""",
'de':
"""
Konfiguriert die Spannungs- und Stromwertebereiche.

Einstellbare Spannungswertebereiche sind:

* 0V - 5V
* 0V - 10V

Einstellbare Stromwertebereiche sind:

* 4mA to 20mA
* 0mA to 20mA
* 0mA to 24mA

Die Auflösung ist immer 12 Bit. D.h., die Genauigkeit erhöht
sich bei kleineren Wertebereichen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetConfiguration', 'get_configuration'), 
'elements': [('voltage_range', 'uint8', 1, 'out', ('VoltageRange', 'voltage_range', [('0To5V', '0_to_5v', 0),
                                                                                     ('0To10V', '0_to_10v', 1)])),
             ('current_range', 'uint8', 1, 'out', ('CurrentRange', 'current_range', [('4To20mA', '4_to_20ma', 0),
                                                                                     ('0To20mA', '0_to_20ma', 1),
                                                                                     ('0To24mA', '0_to_24ma', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`SetConfiguration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`SetConfiguration`
gesetzt.
"""
}]
})
