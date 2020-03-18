# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Temperature IR Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from commonconstants import add_callback_value_function

from openhab_commonconfig import *

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

com['constant_groups'].append(THRESHOLD_OPTION_CONSTANT_GROUP)

ambient_temperature_doc = {
'en':
"""
Returns the ambient temperature of the sensor.
""",
'de':
"""
Gibt die Umgebungstemperatur des Sensors zurück.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Ambient Temperature',
    data_name = 'Temperature',
    data_type = 'int16',
    doc       = ambient_temperature_doc,
    scale     = (1, 10),
    unit      = 'Degree Celsius',
    range_    = (-400, 1250)
)

object_temperature_doc = {
'en':
"""
Returns the object temperature of the sensor, i.e. the temperature
of the surface of the object the sensor is aimed at.

The temperature of different materials is dependent on their `emissivity
<https://en.wikipedia.org/wiki/Emissivity>`__. The emissivity of the material
can be set with :func:`Set Emissivity`.
""",
'de':
"""
Gibt die Objekttemperatur des Sensors zurück, z.B. die Temperatur
der Oberfläche auf welche der Sensor zielt.

Die Temperatur von unterschiedlichen Materialien ist abhängig von ihrem
`Emissionsgrad <https://de.wikipedia.org/wiki/Emissionsgrad>`__. Der
Emissionsgrad des Materials kann mit :func:`Set Emissivity` gesetzt werden.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get Object Temperature',
    data_name = 'Temperature',
    data_type = 'int16',
    doc       = object_temperature_doc,
    scale     = (1, 10),
    unit      = 'Degree Celsius',
    range_    = (-700, 3800)
)

com['packets'].append({
'type': 'function',
'name': 'Set Emissivity',
'elements': [('Emissivity', 'uint16', 1, 'in', {'scale': (1, 65535), 'range': (6553, None), 'default': 65535})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the `emissivity <https://en.wikipedia.org/wiki/Emissivity>`__ that is
used to calculate the surface temperature as returned by
:func:`Get Object Temperature`.

The emissivity is usually given as a value between 0.0 and 1.0. A list of
emissivities of different materials can be found
`here <https://www.infrared-thermography.com/material.htm>`__.

The parameter of :func:`Set Emissivity` has to be given with a factor of
65535 (16-bit). For example: An emissivity of 0.1 can be set with the
value 6553, an emissivity of 0.5 with the value 32767 and so on.

.. note::
 If you need a precise measurement for the object temperature, it is
 absolutely crucial that you also provide a precise emissivity.

The emissivity is stored in non-volatile memory and will still be
used after a restart or power cycle of the Bricklet.
""",
'de':
"""
Setzt den `Emissionsgrad <https://de.wikipedia.org/wiki/Emissionsgrad>`__,
welcher zur Berechnung der Oberflächentemperatur benutzt wird, wie von
:func:`Get Object Temperature` zurückgegeben.

Der Emissionsgrad wird normalerweise als Wert zwischen 0,0 und 1,0 angegeben.
Eine Liste von Emissionsgraden unterschiedlicher Materialien ist
`hier <https://www.infrared-thermography.com/material.htm>`__ zu finden.

Der Parameter von :func:`Set Emissivity` muss mit eine Faktor von 65535 (16-Bit)
vorgegeben werden. Beispiel: Ein Emissionsgrad von 0,1 kann mit dem Wert
6553 gesetzt werden, ein Emissionsgrad von 0,5 mit dem Wert 32767 und so weiter.

.. note::
 Wenn eine exakte Messung der Objekttemperatur notwendig ist, ist es entscheidend
 eine exakten Emissionsgrad anzugeben.

Der Emissionsgrad wird in nicht-flüchtigem Speicher gespeichert und wird
auch noch einem Neustart weiter genutzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Emissivity',
'elements': [('Emissivity', 'uint16', 1, 'out', {'scale': (1, 65535), 'range': (6553, None), 'default': 65535})],
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

ambient_temp_channel = oh_generic_channel('Ambient Temperature', 'Ambient Temperature', element_name='Temperature')
ambient_temp_channel['callbacks'][0]['transform'] = 'new {number_type}(temperature{divisor}{unit})'

object_temp_channel = oh_generic_channel('Object Temperature', 'Object Temperature', element_name='Temperature')
object_temp_channel['callbacks'][0]['transform'] = 'new {number_type}(temperature{divisor}{unit})'

com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'channels': [
        ambient_temp_channel,
        object_temp_channel
    ],
    'channel_types': [
        oh_generic_channel_type('Ambient Temperature', 'Number', 'Ambient Temperature',
                    update_style='Callback Configuration',
                    description='Measured ambient temperature'),
        oh_generic_channel_type('Object Temperature', 'Number', 'Object Temperature',
                    update_style='Callback Configuration',
                    description='Measured object temperature, i.e. the temperature of the surface of the object the sensor is aimed at. The temperature of different materials is dependent on their <a href=https://en.wikipedia.org/wiki/Emissivity>emissivity</a>.')
    ],
    'actions': ['Get Ambient Temperature', 'Get Object Temperature', 'Get Emissivity']
}
