# -*- coding: utf-8 -*-

# Servo Brick communication config

com = {
    'author': 'Olaf Lüke (olaf@tinkerforge.com)',
    'version': [1, 1, 0],
    'type': 'Brick',
    'name': ('Master', 'master'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for controlling Stacks and four Bricklets',
    'packets': []
}

com['packets'].append({
'type': 'method', 
'name': ('GetStackVoltage', 'get_stack_voltage'), 
'elements': [('voltage', 'uint16', 1, 'out')], 
'doc': ['bm', {
'en':
"""
Returns the stack voltage in mV. The stack voltage is the
voltage that is supplied via the stack, i.e. it is given by a 
Step-Down or Step-Up power supply Brick.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetStackCurrent', 'get_stack_current'), 
'elements': [('current', 'uint16', 1, 'out')], 
'doc': ['bm', {
'en':
"""
Returns the stack current in mA. The stack current is the
current that is drawn via the stack, i.e. it is given by a
Step-Down or Step-Up power supply Brick.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('SetExtensionType', 'set_extension_type'), 
'elements': [('extension', 'uint8', 1, 'in'),
             ('exttype', 'uint32', 1, 'in')], 
'doc': ['am', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetExtensionType', 'get_extension_type'), 
'elements': [('extension', 'uint8', 1, 'in'),
             ('exttype', 'uint32', 1, 'out')], 
'doc': ['am', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('IsChibiPresent', 'is_chibi_present'), 
'elements': [('present', 'bool', 1, 'out')], 
'doc': ['am', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('SetChibiAddress', 'set_chibi_address'), 
'elements': [('address', 'uint8', 1, 'in')], 
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetChibiAddress', 'get_chibi_address'), 
'elements': [('address', 'uint8', 1, 'out')], 
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('SetChibiMasterAddress', 'set_chibi_master_address'), 
'elements': [('address', 'uint8', 1, 'in')], 
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetChibiMasterAddress', 'get_chibi_master_address'), 
'elements': [('address', 'uint8', 1, 'out')], 
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('SetChibiSlaveAddress', 'set_chibi_slave_address'), 
'elements': [('num', 'uint8', 1, 'in'),
             ('address', 'uint8', 1, 'in')], 
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetChibiSlaveAddress', 'get_chibi_slave_address'), 
'elements': [('num', 'uint8', 1, 'in'),
             ('address', 'uint8', 1, 'out')], 
'doc': ['bm', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetChibiSignalStrength', 'get_chibi_signal_strength'), 
'elements': [('signal_strength', 'uint8', 1, 'out')], 
'doc': ['am', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'method', 
'name': ('GetChibiErrorLog', 'get_chibi_error_log'), 
'elements': [('underrun', 'uint16', 1, 'out'),
             ('crc_error', 'uint16', 1, 'out'),
             ('no_ack', 'uint16', 1, 'out'),
             ('overflow', 'uint16', 1, 'out')], 
'doc': ['am', {
'en':
"""
""",
'de':
"""
"""
}]
})
