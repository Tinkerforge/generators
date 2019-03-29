# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Distance IR Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'api_version_extra': 1, # +1 for "Break API to fix wrong moving-average-length type [ec51349]"
    'category': 'Bricklet',
    'device_identifier': 2125,
    'name': 'Distance IR V2',
    'display_name': 'Distance IR 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures distance up to 150cm with infrared light',
        'de': 'Misst Entfernung bis zu 150cm mit Infrarot-Licht'
    },
    'released': True,
    'documented': True,
    'discontinued': False,
    'features': [
        'comcu_bricklet',
        'bricklet_get_identity'
    ],
    'packets': [],
    'examples': []
}

distance_doc = {
'en':
"""
Returns the distance measured by the sensor. The value is in mm and possible
distance ranges are 40 to 300, 100 to 800 and 200 to 1500, depending on the
selected IR sensor.
""",
'de':
"""
Gibt die gemessene Entfernung des Sensors zurück. Der Wert ist in mm und die möglichen
Entfernungsbereiche sind 40 bis 300, 100 bis 800 und 200 bis 1500, in Abhängigkeit vom
gewählten IR Sensor.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Distance',
    data_name = 'Distance',
    data_type = 'uint16',
    doc       = distance_doc
)

analog_value_doc = {
'en':
"""
Returns the analog value as read by a analog-to-digital converter.
The value has 21 bit with a range of 0 to 2097151.

This is unfiltered raw data. We made sure that the integration time
of the ADC is shorter then the measurement interval of the sensor
(10ms vs 16.5ms). So there is no information lost.

If you want to do your own calibration or create your own lookup table
you can use this value.
""",
'de':
"""
Gibt den Analogwert des Analog/Digital-Wandler zurück.
Der Wert hat 21 Bit und einen Wertebereich von 0 bis 2097151.

Dieser Wert ist ein unverarbeiteter Rohwert. Wir haben sichergestellt,
dass die Integrationszeit des ADCs kleiner ist als das Messintervall des
Sensors (10ms vs 16,5ms). Dadurch ist sichergestellt das keine Informationen
verloren gehen können.

Der Analogwert kann genutzt werden wenn eine eigene Kalibrierung oder
Lookup-Tabelle benötigt wird.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Analog Value',
    data_name = 'Analog Value',
    data_type = 'uint32',
    doc       = analog_value_doc
)

com['packets'].append({
'type': 'function',
'name': 'Set Moving Average Configuration',
'elements': [('Moving Average Length', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
for the resistance and temperature.

Setting the length to 1 will turn the averaging off. With less averaging, there
is more noise on the data.

The range for the averaging is 1-1000.

New data is gathered every ~10ms. With a moving average of length 1000 the
resulting averaging window has a length of approximately 10s. If you want to do
long term measurements the longest moving average will give the cleanest results.

The default value is 25.
""",
'de':
"""
Setzt die Länge eines `gleitenden Mittelwerts <https://de.wikipedia.org/wiki/Gleitender_Mittelwert>`__
für den Widerstand und die Temperatur.

Wenn die Länge auf 1 gesetzt wird, ist die Mittelwertbildung deaktiviert.
Desto kürzer die Länge des Mittelwerts ist, desto mehr Rauschen ist auf den Daten.

Der Wertebereich liegt bei 1-1000.

Einer neue Wert wird alle ~10ms gemessen. Mit einer Mittelwerts-Länge von 1000 hat das
resultierende gleitende Fenster eine Zeitspanne von ca. 10s. Bei Langzeitmessungen gibt
ein langer Mittelwert die saubersten Resultate.

Der Standardwert ist 25.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Moving Average Configuration',
'elements': [('Moving Average Length', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the moving average configuration as set by :func:`Set Moving Average Configuration`.
""",
'de':
"""
Gibt die Moving Average-Konfiguration zurück, wie von :func:`Set Moving Average Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Distance LED Config',
'elements': [('Config', 'uint8', 1, 'in', ('Distance LED Config', [('Off', 0),
                                                                   ('On', 1),
                                                                   ('Show Heartbeat', 2),
                                                                   ('Show Distance', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Configures the distance LED to be either turned off, turned on, blink in
heartbeat mode or show the distance (brighter = object is nearer).

The default value is 3 (show distance).
""",
'de':
"""
Konfiguriert die Distanz-LED. Die LED kann ausgeschaltet, eingeschaltet,
im Herzschlagmodus betrieben werden. Zusätzlich gibt es die Option
mit der LED die Distanz anzuzeigen (heller = Objekt näher).

Der Standardwert ist 3 (Distanzanzeige).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Distance LED Config',
'elements': [('Config', 'uint8', 1, 'out', ('Distance LED Config', [('Off', 0),
                                                                    ('On', 1),
                                                                    ('Show Heartbeat', 2),
                                                                    ('Show Distance', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the LED configuration as set by :func:`Set Distance LED Config`
""",
'de':
"""
Gibt die LED-Konfiguration zurück, wie von :func:`Set Distance LED Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Sensor Type',
'elements': [('Sensor', 'uint8', 1, 'in', ('Sensor Type', [('2Y0A41', 0),
                                                           ('2Y0A21', 1),
                                                           ('2Y0A02', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the sensor type.

The Bricklet comes configured with the correct sensor type
and the type is saved in flash (i.e. the Bricklet retains the information if
power is lost).

If you want to change the sensor you can set the type in Brick Viewer,
you will likely never need to call this function from your program.
""",
'de':
"""
Setzt den Sensor-Typ.

Das Bricklet kommt vorkonfiguriert mit dem korrektem Sensor und der
Sensor-Typ wird im Flash gespeichert (d.h. das Bricklet behält die Einstellung
auch wenn es vom Strom getrennt wird).

Die Einstellung kann im Brick Viewer vorgenommen werden. Diese Funktion
sollte in einem externen Programm also nicht ausgeführt werden müssen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Sensor Type',
'elements': [('Sensor', 'uint8', 1, 'out', ('Sensor Type', [('2Y0A41', 0),
                                                            ('2Y0A21', 1),
                                                            ('2Y0A02', 2)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the sensor type as set by :func:`Set Sensor Type`.
""",
'de':
"""
Gibt den Sensor-Typ zurück, wie von :func:`Set Sensor Type` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Distance', 'distance'), [(('Distance', 'Distance'), 'uint16', 1, 10.0, 'cm', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Distance', 'distance'), [(('Distance', 'Distance'), 'uint16', 1, 10.0, 'cm', None)], None, None),
              ('callback_configuration', ('Distance', 'distance'), [], 1000, False, 'x', [(0, 0)])]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('callback', ('Distance', 'distance'), [(('Distance', 'Distance'), 'uint16', 1, 10.0, 'cm', None)], None, None),
              ('callback_configuration', ('Distance', 'distance'), [], 1000, False, '<', [(30, 0)])]
})
