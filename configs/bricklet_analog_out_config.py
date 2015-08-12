# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Analog Out Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 220,
    'name': ('AnalogOut', 'analog_out', 'Analog Out', 'Analog Out Bricklet'),
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Generates configurable DC voltage between 0V and 5V',
        'de': 'Erzeugt konfigurierbare Gleichspannung zwischen 0V und 5V'
    },
    'released': True,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': ('SetVoltage', 'set_voltage'), 
'elements': [('voltage', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the voltage in mV. The possible range is 0V to 5V (0-5000).
Calling this function will set the mode to 0 (see :func:`SetMode`).

The default value is 0 (with mode 1).
""",
'de':
"""
Setzt die Spannung in mV. Der mögliche Bereich ist 0V bis 5V (0-5000).
Dieser Funktionsaufruf setzt den Modus auf 0 (siehe :func:`SetMode`).

Der Standardwert ist 0 (im Modus 1).
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
'name': ('SetMode', 'set_mode'), 
'elements': [('mode', 'uint8', 1, 'in', ('Mode', 'mode', [('AnalogValue', 'analog_value', 0),
                                                          ('1KToGround', '1k_to_ground', 1),
                                                          ('100KToGround', '100k_to_ground', 2),
                                                          ('500KToGround', '500k_to_ground', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the mode of the analog value. Possible modes:

* 0: Normal Mode (Analog value as set by :func:`SetVoltage` is applied)
* 1: 1k Ohm resistor to ground
* 2: 100k Ohm resistor to ground
* 3: 500k Ohm resistor to ground

Setting the mode to 0 will result in an output voltage of 0. You can jump
to a higher output voltage directly by calling :func:`SetVoltage`.

The default mode is 1.
""",
'de':
"""
Setzt den Modus des Analogwertes. Mögliche Modi:

* 0: normaler Modus (Analogwert, wie von :func:`SetVoltage` gesetzt, wird ausgegeben.)
* 1: 1k Ohm Widerstand gegen Masse
* 2: 100k Ohm Widerstand gegen Masse
* 3: 500k Ohm Widerstand gegen Masse

Ein setzten des Modus auf 0 resultiert in einer Ausgabespannung von 0. Es kann auf eine
höhere Ausgabespannung direkt gewechselt werden über einen Aufruf von :func:`SetVoltage`.

Der Standardmodus ist 1.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetMode', 'get_mode'), 
'elements': [('mode', 'uint8', 1, 'out', ('Mode', 'mode', [('AnalogValue', 'analog_value', 0),
                                                           ('1KToGround', '1k_to_ground', 1),
                                                           ('100KToGround', '100k_to_ground', 2),
                                                           ('500KToGround', '500k_to_ground', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the mode as set by :func:`SetMode`.
""",
'de':
"""
Gibt den Modus zurück, wie von :func:`SetMode` gesetzt.
"""
}]
})

com['examples'].append({
'type': 'setter',
'name': 'Simple',
'values': [('Set Voltage', [('uint16', 3300)], 'Set output voltage to 3.3V', None)],
'cleanups': []
})
