# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

THRESHOLD_OPTION_CONSTANTS = ('Threshold Option', [('Off', 'x'),
                                                   ('Outside', 'o'),
                                                   ('Inside', 'i'),
                                                   ('Smaller', '<'),
                                                   ('Greater', '>')])

def add_callback_value_function(packets, name, data_name, data_type, doc, since_firmware = [1, 0, 0]):
    # TODO: Add hint of callback function to getter doc
    getter = {
'type': 'function',
'name': name,
'elements': [(data_name, data_type, 1, 'out')],
'since_firmware': since_firmware,
'doc': ['bf', doc]
}

    callback_config_setter = {
'type': 'function',
'name': (name + ' Callback Configuration').replace('Get ', 'Set '),
'corresponding_getter': name,
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in'),
             ('Option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint16', 1, 'in'),
             ('Max', 'uint16', 1, 'in')],
'since_firmware': since_firmware,
'doc': ['ccf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
}

    callback_config_getter = {
'type': 'function',
'name': (name + ' Callback Configuration'),
'corresponding_getter': name,
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out'),
             ('Option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint16', 1, 'out'),
             ('Max', 'uint16', 1, 'out')],
'since_firmware': since_firmware,
'doc': ['ccf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
}

    callback = {
'type': 'callback',
'name': name.replace('Get ', ''),
'corresponding_getter': name,
'elements': [(data_name, data_type, 1, 'out')],
'since_firmware': since_firmware,
'doc': ['c', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
}

    packets.append(getter)
    packets.append(callback_config_setter)
    packets.append(callback_config_getter)
    packets.append(callback)
