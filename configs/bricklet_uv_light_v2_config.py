# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# UV Light Bricklet 2.0 communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

com = {
    'author': 'Ishraq Ibne Ashraf <ishraq@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2118,
    'name': 'UV Light V2',
    'display_name': 'UV Light 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures UV light',
        'de': 'Misst UV-Licht'
    },
    'comcu': True,
    'released': True,
    'documented': True,
    'discontinued': False,
    'packets': [],
    'examples': []
}

uva_doc = {
'en':
"""
Returns the UVA intensity of the sensor, the intensity is given
in 1/10 mW/m². The sensor has not weighted the intensity with the erythemal
action spectrum to get the skin-affecting irradiation. Therefore, you cannot
just divide the value by 250 to get the UVA index. To get the UV index use
:func:`Get UVI`.

If the sensor is saturated, then -1 is returned, see :func:`Set Configuration`.

If you want to get the intensity periodically, it is recommended to use the
:cb:`UVA` callback and set the period with
:func:`Set UVA Callback Configuration`.
""",
'de':
"""
Gibt die UVA Intensität des Sensors zurück. Die Intensität wird in der Einheit
1/10 mW/m² gegeben. Der Sensor hat die Intensität nicht mit dem
Erythem-Wirkungsspektrum gewichtet, daher handelt es sich nicht um die
hautbeeinflussende Bestrahlungsstärke. Der Wert kann nicht einfach durch 250
geteilt werden, um den UVA Index zu bestimmen. Um den UV Index zu bestimmen kann
:func:`Get UVI` verwendet werden.

Falls der Sensor gesättigt (saturated) ist, dann wird -1 zurückgegeben,
siehe :func:`Set Configuration`.

Wenn die Intensität periodisch abgefragt werden soll, wird empfohlen
den :cb:`UVA` Callback zu nutzen und die Periode mit
:func:`Set UVA Callback Configuration` vorzugeben.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get UVA',
    data_name = 'UVA',
    data_type = 'int32',
    doc       = uva_doc
)

uvb_doc = {
'en':
"""
Returns the UVB intensity of the sensor, the intensity is given
in 1/10 mW/m². The sensor has not weighted the intensity with the erythemal
action spectrum to get the skin-affecting irradiation. Therefore, you cannot
just divide the value by 250 to get the UVB index. To get the UV index use
:func:`Get UVI`.

If the sensor is saturated, then -1 is returned, see :func:`Set Configuration`.

If you want to get the intensity periodically, it is recommended to use the
:cb:`UVB` callback and set the period with
:func:`Set UVB Callback Configuration`.
""",
'de':
"""
Gibt die UVB Intensität des Sensors zurück. Die Intensität wird in der Einheit
1/10 mW/m² gegeben. Der Sensor hat die Intensität nicht mit dem
Erythem-Wirkungsspektrum gewichtet, daher handelt es sich nicht um die
hautbeeinflussende Bestrahlungsstärke. Der Wert kann nicht einfach durch 250
geteilt werde, um den UVB Index zu bestimmen. Um den UV Index zu bestimmen kann
:func:`Get UVI` verwendet werden.

Falls der Sensor gesättigt (saturated) ist, dann wird -1 zurückgegeben,
siehe :func:`Set Configuration`.

Wenn die Intensität periodisch abgefragt werden soll, wird empfohlen
den :cb:`UVB` Callback zu nutzen und die Periode mit
:func:`Set UVB Callback Configuration` vorzugeben.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get UVB',
    data_name = 'UVB',
    data_type = 'int32',
    doc       = uvb_doc
)

uvi_doc = {
'en':
"""
Returns the UV index of the sensor, the index is given in 1/10.

If the sensor is saturated, then -1 is returned, see :func:`Set Configuration`.

If you want to get the intensity periodically, it is recommended to use the
:cb:`UVI` callback and set the period with
:func:`Set UVI Callback Configuration`.
""",
'de':
"""
Gibt den UV Index des Sensors in 1/10 zurück.

Falls der Sensor gesättigt (saturated) ist, dann wird -1 zurückgegeben,
siehe :func:`Set Configuration`.

Wenn die Intensität periodisch abgefragt werden soll, wird empfohlen
den :cb:`UVI` Callback zu nutzen und die Periode mit
:func:`Set UVI Callback Configuration` vorzugeben.
"""
}

add_callback_value_function(
    packets   = com['packets'],
    name      = 'Get UVI',
    data_name = 'UVI',
    data_type = 'int32',
    doc       = uvi_doc
)

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('Integration Time', 'uint8', 1, 'in', ('Integration Time', [('50ms', 0),
                                                                          ('100ms', 1),
                                                                          ('200ms', 2),
                                                                          ('400ms', 3),
                                                                          ('800ms', 4)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the configuration of the sensor. The integration time can be configured
between 50 and 800 ms. With a shorter integration time the sensor reading updates
more often but contains more noise. With a longer integration the sensor reading
contains less noise but updates less often.

With a longer integration time (especially 800 ms) and a higher UV intensity the
sensor can be saturated. If this happens the UVA/UVB/UVI readings are all -1.
In this case you need to choose a shorter integration time.

Default value: 400 ms.
""",
'de':
"""
Setzt die Konfiguration des Sensors. Die Integrationszeit kann zwischen 50 und
800 ms eingestellt werden. Mit einer kürzeren Integrationszeit wird der Sensorwert
öfter aktualisiert, beinhaltet aber mehr Rauschen. Mit einer längeren
Integrationszeit wird das Rauschen verringert aber der Sensorwert wird nicht so
oft aktualisiert.

Mit einer längeren Integrationszeit (ins besondere 800 ms) und einer höheren UV
Intensität kann der Sensor gesättigt (saturated) sein. Falls dies auftritt dann
sind die UVA/UVB/UVI Messwerte alle -1. In diesem Fall muss eine kürzere
Integrationszeit gewählt werden.

Standardwert: 400 ms.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Integration Time', 'uint8', 1, 'out', ('Integration Time', [('50ms', 0),
                                                                           ('100ms', 1),
                                                                           ('200ms', 2),
                                                                           ('400ms', 3),
                                                                           ('800ms', 4)]))],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the configuration as set by :func:`Set Configuration`.
""",
'de':
"""
Gibt die Konfiguration zurück, wie von :func:`Set Configuration`
gesetzt.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get UVA', 'UV-A'), [(('UVA', 'UV-A'), 'int32', 1, 10.0, 'mW/m²', None)], []),
              ('getter', ('Get UVB', 'UV-B'), [(('UVB', 'UV-B'), 'int32', 1, 10.0, 'mW/m²', None)], []),
              ('getter', ('Get UVI', 'UV index'), [(('UVI', 'UV Index'), 'int32', 1, 10.0, None, None)], [])]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('UVI', 'UV index'), [(('UVI', 'UV Index'), 'int32', 1, 10.0, None, None)], None, None),
              ('callback_configuration', ('UVI', 'UVI'), [], 1000, False, 'x', [(0, 0)])]
})

com['examples'].append({
'name': 'Threshold',
'functions': [('callback', ('UVI', 'UV index'), [(('UVI', 'UV Index'), 'int32', 1, 10.0, None, None)], None, 'UV index > 3. Use sunscreen!'),
              ('callback_configuration', ('UVI', 'UV index'), [], 1000, False, '>', [(3, 0)])]
})
