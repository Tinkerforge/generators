# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Temperature IR Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 1],
    'api_version_extra': 1, # +1 for "Fix min/max types in add_callback_value_function logic [aff5bfc]"
    'category': 'Bricklet',
    'device_identifier': 291,
    'name': 'Temperature IR V2',
    'display_name': 'Temperature IR 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures contactless object temperature between -70°C and +380°C',
        'de': 'Kontaktlose Objekttemperaturmessung zwischen -70°C und +380°C'
    },
    'comcu': True,
    'released': True,
    'documented': True,
    'discontinued': False,
    'packets': [],
    'examples': []
}

ambient_temperature_doc = {
'en':
"""
Returns the ambient temperature of the sensor. The value
has a range of -400 to 1250 and is given in °C/10,
e.g. a value of 423 means that an ambient temperature of 42.3 °C is
measured.

If you want to get the ambient temperature periodically, it is recommended
to use the :cb:`Ambient Temperature` callback and set the period with
:func:`Set Ambient Temperature Callback Configuration`.
""",
'de':
"""
Gibt die Umgebungstemperatur des Sensors zurück. Der Wertebereich ist von
-400 bis 1250 und wird in °C/10 angegeben, z.B. bedeutet
ein Wert von 423 eine gemessene Umgebungstemperatur von 42,3 °C.

Wenn die Umgebungstemperatur periodisch abgefragt werden soll, wird empfohlen
den :cb:`Ambient Temperature` Callback zu nutzen und die Periode mit
:func:`Set Ambient Temperature Callback Configuration` vorzugeben.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Ambient Temperature',
    data_name = 'Temperature',
    data_type = 'int16',
    doc       = ambient_temperature_doc
)

object_temperature_doc = {
'en':
"""
Returns the object temperature of the sensor, i.e. the temperature
of the surface of the object the sensor is aimed at. The value
has a range of -700 to 3800 and is given in °C/10,
e.g. a value of 3001 means that a temperature of 300.1 °C is measured
on the surface of the object.

The temperature of different materials is dependent on their `emissivity
<https://en.wikipedia.org/wiki/Emissivity>`__. The emissivity of the material
can be set with :func:`Set Emissivity`.

If you want to get the object temperature periodically, it is recommended
to use the :cb:`Object Temperature` callback and set the period with
:func:`Set Object Temperature Callback Configuration`.
""",
'de':
"""
Gibt die Objekttemperatur des Sensors zurück, z.B. die Temperatur
der Oberfläche auf welche der Sensor zielt. Der Wertebereich ist von
-700 bis 3800 und wird in °C/10 angegeben, z.B. bedeutet
ein Wert von 3001 eine gemessene Temperatur von 300,1 °C auf der Oberfläche
des Objektes.

Die Temperatur von unterschiedlichen Materialien ist abhängig von ihrem
`Emissionsgrad <https://de.wikipedia.org/wiki/Emissionsgrad>`__. Der
Emissionsgrad des Materials kann mit :func:`Set Emissivity` gesetzt werden.

Wenn die Objekttemperatur periodisch abgefragt werden soll, wird empfohlen
den :cb:`Object Temperature` Callback zu nutzen und die Periode mit
:func:`Set Object Temperature Callback Configuration` vorzugeben.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Object Temperature',
    data_name = 'Temperature',
    data_type = 'int16',
    doc       = object_temperature_doc
)

com['packets'].append({
'type': 'function',
'name': 'Set Emissivity',
'elements': [('Emissivity', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the `emissivity <https://en.wikipedia.org/wiki/Emissivity>`__ that is
used to calculate the surface temperature as returned by
:func:`Get Object Temperature`.

The emissivity is usually given as a value between 0.0 and 1.0. A list of
emissivities of different materials can be found
`here <http://www.infrared-thermography.com/material.htm>`__.

The parameter of :func:`Set Emissivity` has to be given with a factor of
65535 (16-bit). For example: An emissivity of 0.1 can be set with the
value 6553, an emissivity of 0.5 with the value 32767 and so on.

.. note::
 If you need a precise measurement for the object temperature, it is
 absolutely crucial that you also provide a precise emissivity.

The default emissivity is 1.0 (value of 65535) and the minimum emissivity the
sensor can handle is 0.1 (value of 6553).
""",
'de':
"""
Setzt den `Emissionsgrad <https://de.wikipedia.org/wiki/Emissionsgrad>`__,
welcher zur Berechnung der Oberflächentemperatur benutzt wird, wie von
:func:`Get Object Temperature` zurückgegeben.

Der Emissionsgrad wird normalerweise als Wert zwischen 0,0 und 1,0 angegeben.
Eine Liste von Emissionsgraden unterschiedlicher Materialien ist
`hier <http://www.infrared-thermography.com/material.htm>`__ zu finden.

Der Parameter von :func:`Set Emissivity` muss mit eine Faktor von 65535 (16-Bit)
vorgegeben werden. Beispiel: Ein Emissionsgrad von 0,1 kann mit dem Wert
6553 gesetzt werden, ein Emissionsgrad von 0,5 mit dem Wert 32767 und so weiter.

.. note::
 Wenn eine exakte Messung der Objekttemperatur notwendig ist, ist es entscheidend
 eine exakten Emissionsgrad anzugeben.

Der Standard Emissionsgrad ist 1,0 (Wert von 65535) und der minimale
Emissionsgrad welcher der Sensor verarbeiten kann ist 0,1 (Wert von 6553).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Emissivity',
'elements': [('Emissivity', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the emissivity as set by :func:`Set Emissivity`.
""",
'de':
"""
Gibt den Emissionsgrad zurück, wie von :func:`Set Emissivity` gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Ambient Temperature', 'ambient temperature'), [(('Ambient Temperature', 'Ambient Temperature'), 'int16', 1, 10.0, '°C', None)], []),
              ('getter', ('Get Object Temperature', 'object temperature'), [(('Object Temperature', 'Object Temperature'), 'int16', 1, 10.0, '°C', None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Object Temperature', 'object temperature'), [(('Temperature', 'Object Temperature'), 'int16', 1, 10.0, '°C', None)], None, None),
              ('callback_configuration', ('Object Temperature', 'object temperature'), [], 1000, False, 'x', [(0, 0)])]
})

com['examples'].append({
'name': 'Water Boiling',
'functions': [('setter', 'Set Emissivity', [('uint16', 64224)], 'Set emissivity to 0.98 (emissivity of water, 65535 * 0.98 = 64224.299)', None),
              ('callback', ('Object Temperature', 'object temperature reached'), [(('Temperature', 'Object Temperature'), 'int16', 1, 10.0, '°C', None)], None, 'The water is boiling!'),
              ('callback_configuration', ('Object Temperature', 'object temperature'), [], 10000, False, '>', [(100, 0)])]
})
