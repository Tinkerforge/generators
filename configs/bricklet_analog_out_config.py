# -*- coding: utf-8 -*-

# Analog Out Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'version': [1, 0, 0],
    'category': 'Bricklet',
    'name': ('AnalogOut', 'analog_out', 'Analog Out'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for output of voltage between 0 and 5V',
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('SetVoltage', 'set_voltage'), 
'elements': [('voltage', 'uint16', 1, 'in')],
'doc': ['bm', {
'en':
"""
Sets the voltage in mV. The possible range is 0V to 5V (0-5000).
Calling this function will set the mode to 0 (see `:func:SetMode`).

The default value is 0 (with mode 1).
""",
'de':
"""
Setzt die Spannung in mV. Der mögliche Bereich ist 0V bis 5V (0-5000).
Dieser Funktionsaufruf setzt den Modus auf 0 (siehe `:func:SetMode`).

Der Standardwert ist 0 (im Modus 1).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetVoltage', 'get_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')],
'doc': ['bm', {
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
'elements': [('mode', 'uint8', 1, 'in')],
'doc': ['bm', {
'en':
"""
Sets the mode of the analog value. Possible modes:

* 0: Normal Mode (Analog value as set by :func:`SetVoltage` is applied
* 1: 1k Ohm resistor to ground
* 2: 100k Ohm resistor to ground
* 3: 500k Ohm resistor to ground

Setting the mode to 0 will result in an output voltage of 0. You can jump
to a higher output voltage directly by calling :func:`SetVoltage`.

The default mode is 1.
""",
'de':
"""
Setzt die Modus des Analogwertes. Mögliche Modi:

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
'elements': [('mode', 'uint8', 1, 'out')],
'doc': ['bm', {
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
