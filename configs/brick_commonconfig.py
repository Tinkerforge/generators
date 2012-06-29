# -*- coding: utf-8 -*-

# Common communication config

common_packets = []

common_packets.append({
'type': 'function', 
'function_id': 243,
'name': ('Reset', 'reset'), 
'elements': [], 
'doc': ['am', {
'en':
"""
Calling this function will reset the Brick. Calling this function 
on a Brick inside of a stack will reset the whole stack.

After a reset you have to create new device objects, 
calling functions on the existing ones will result in 
undefined behavior!
""",
'de':
"""
"""
}]
})

common_packets.append({
'type': 'function',
'function_id': 242,
'name': ('GetChipTemperature', 'get_chip_temperature'), 
'elements': [('temperature', 'int16', 1, 'out')], 
'doc': ['am', {
'en':
"""
Returns the temperature in °C/10 as measured inside the microcontroller. The
value returned is not the ambient temperature! Under normal conditions
the microcontroller should have a temperature of about 35-45°C

The temperature has an accuracy of +-15%.
""",
'de':
"""
"""
}]
})
