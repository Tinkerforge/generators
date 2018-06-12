# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Voltage/Current Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2105,
    'name': 'Voltage Current V2',
    'display_name': 'Voltage/Current 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures power, DC voltage and DC current up to 720W/36V/20A',
        'de': 'Misst Leistung, Gleichspannung und Gleichstrom bis zu 720W/36V/20A'
    },
    'comcu': True,
    'released': True,
    'documented': True,
    'discontinued': False,
    'packets': [],
    'examples': []
}

current_doc = {
'en':
"""
Returns the current. The value is in mA
and between -20000mA and 20000mA.
""",
'de':
"""
Gibt die gemessenen Stromstärke zurück. Der Wert ist in mA und im
Bereich von -20000mA bis 20000mA.
"""
}

add_callback_value_function(
    packets   = com['packets'], 
    name      = 'Get Current', 
    data_name = 'Current',
    data_type = 'int32',
    doc       = current_doc
)

voltage_doc = {
'en':
"""
Returns the voltage. The value is in mV
and between 0mV and 36000mV.
""",
'de':
"""
Gibt die gemessenen Spannung zurück. Der Wert ist in mV und im
Bereich von 0mV bis 36000mV.
"""
}

add_callback_value_function(
    packets   = com['packets'], 
    name      = 'Get Voltage', 
    data_name = 'Voltage',
    data_type = 'int32',
    doc       = voltage_doc
)

power_doc = {
'en':
"""
Returns the power. The value is in mW
and between 0mV and 720000mW.
""",
'de':
"""
Gibt die gemessenen Leistung zurück. Der Wert ist in mW und im
Bereich von 0mW bis 720000mW.
"""
}

add_callback_value_function(
    packets   = com['packets'], 
    name      = 'Get Power', 
    data_name = 'Power',
    data_type = 'int32',
    doc       = power_doc
)

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('Averaging', 'uint8', 1, 'in', ('Averaging', [('1', 0),
                                                            ('4', 1),
                                                            ('16', 2),
                                                            ('64', 3),
                                                            ('128', 4),
                                                            ('256', 5),
                                                            ('512', 6),
                                                            ('1024', 7)])),
             ('Voltage Conversion Time', 'uint8', 1, 'in'),
             ('Current Conversion Time', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the configuration of the Voltage/Current Bricklet 2.0. It is
possible to configure number of averages as well as
voltage and current conversion time.

Averaging:

.. csv-table::
 :header: "Value", "Number of Averages"
 :widths: 20, 20

 "0",    "1"
 "1",    "4"
 "2",    "16"
 "3",    "64"
 "4",    "128"
 "5",    "256"
 "6",    "512"
 ">=7",  "1024"

Voltage/Current conversion:

.. csv-table::
 :header: "Value", "Conversion time"
 :widths: 20, 20

 "0",    "140µs"
 "1",    "204µs"
 "2",    "332µs"
 "3",    "588µs"
 "4",    "1.1ms"
 "5",    "2.116ms"
 "6",    "4.156ms"
 ">=7",  "8.244ms"

The default values are 3, 4 and 4 (64, 1.1ms, 1.1ms) for averaging, voltage
conversion and current conversion.
""",
'de':
"""
Setzt die Konfiguration des Voltage/Current Bricklet 2.0. Es ist
möglich die Anzahl für die Durchschnittsbildung, und die
Wandlungszeit für Spannung und Stromstärke zu definieren.

Durchschnittsbildung:

.. csv-table::
 :header: "Wert", "Anzahl"
 :widths: 20, 20

 "0",    "1"
 "1",    "4"
 "2",    "16"
 "3",    "64"
 "4",    "128"
 "5",    "256"
 "6",    "512"
 ">=7",  "1024"

Wandlungszeit für Spannung/Stromstärke:

.. csv-table::
 :header: "Wert", "Wandlungszeit"
 :widths: 20, 20

 "0",    "140µs"
 "1",    "204µs"
 "2",    "332µs"
 "3",    "588µs"
 "4",    "1.1ms"
 "5",    "2.116ms"
 "6",    "4.156ms"
 ">=7",  "8.244ms"

Die Standardwerte sind 3, 4 und 4 (64, 1.1ms, 1.1ms) für die
Durchschnittsbildung und die Spannungs/Stromstärkenwandlungszeit.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Averaging', 'uint8', 1, 'out', ('Averaging', [('1', 0),
                                                             ('4', 1),
                                                             ('16', 2),
                                                             ('64', 3),
                                                             ('128', 4),
                                                             ('256', 5),
                                                             ('512', 6),
                                                             ('1024', 7)])),
             ('Voltage Conversion Time', 'uint8', 1, 'out'),
             ('Current Conversion Time', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
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

com['packets'].append({
'type': 'function',
'name': 'Set Calibration',
'elements': [('Voltage Multiplier', 'uint16', 1, 'in'),
             ('Voltage Divisor', 'uint16', 1, 'in'),
             ('Current Multiplier', 'uint16', 1, 'in'),
             ('Current Divisor', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Since the ADC and the shunt resistor used for the measurements
are not perfect they need to be calibrated by a multiplier and
a divisor if a very precise reading is needed.

For example, if you are expecting a current of 1000mA and you
are measuring 1023mA, you can calibrate the Voltage/Current Bricklet
by setting the current multiplier to 1000 and the divisor to 1023.
The same applies for the voltage.
""",
'de':
"""
Da der ADC und der Shunt-Widerstand für die Messungen verwendet
werden nicht perfekt sind, ist es nötig einen Multiplikator und
einen Divisor zu setzen falls sehr genaue Messwerte nötig sind.

Zum Beispiel: Wenn eine Messung von 1000mA erwartet wird, das
Voltage/Current Bricklet 2.0 aber 1023mA zurück gibt, sollte
der Multiplikator auf 1000 und der Divisor auf 1023 gesetzt
werden. Das gleiches gilt für die Spannung.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Calibration',
'elements': [('Voltage Multiplier', 'uint16', 1, 'out'),
             ('Voltage Divisor', 'uint16', 1, 'out'),
             ('Current Multiplier', 'uint16', 1, 'out'),
             ('Current Divisor', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the calibration as set by :func:`Set Calibration`.
""",
'de':
"""
Gibt die Kalibrierung zurück, wie von :func:`Set Calibration` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Voltage', 'voltage'), [(('Voltage', 'Voltage'), 'int32', 1, 1000.0, 'V', None)], []),
              ('getter', ('Get Current', 'current'), [(('Current', 'Current'), 'int32', 1, 1000.0, 'A', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Current', 'current'), [(('Current', 'Current'), 'int32', 1, 1000.0, 'A', None)], None, None),
              ('callback_configuration', ('Current', 'current'), [], 1000, False, 'x', [(0, 0)])]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('callback', ('Power', 'power'), [(('Power', 'power'), 'int32', 1, 1000.0, 'W', None)], None, None),
              ('callback_configuration', ('Power', 'power'), [], 1000, False, '>', [(10, 0)])]
})
