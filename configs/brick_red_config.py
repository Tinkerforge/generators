# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# RED Brick communication config

com = {
    'author': 'Matthias Bolte <matthias@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Brick',
    'device_identifier': 17,
    'name': ('RED', 'red', 'RED'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for running user programs standalone on the stack',
    'released': False,
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetObjectType', 'get_object_type'),
'elements': [('object_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('object_type', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetNextObjectTableEntry', 'get_next_object_table_entry'),
'elements': [('object_type', 'uint8', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('object_id', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('RewindObjectTable', 'rewind_object_table'),
'elements': [('object_type', 'uint8', 1, 'in'),
             ('error_code', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('AcquireString', 'acquire_string'),
'elements': [('length_to_reserve', 'uint32', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('string_id', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('ReleaseString', 'release_string'),
'elements': [('string_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('TruncateString', 'truncate_string'),
'elements': [('string_id', 'uint16', 1, 'in'),
             ('length', 'uint32', 1, 'in'),
             ('error_code', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetStringLength', 'get_string_length'),
'elements': [('string_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('length', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetStringChunk', 'set_string_chunk'),
'elements': [('string_id', 'uint16', 1, 'in'),
             ('offset', 'uint32', 1, 'in'),
             ('buffer', 'string', 58, 'in'),
             ('error_code', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetStringChunk', 'get_string_chunk'),
'elements': [('string_id', 'uint16', 1, 'in'),
             ('offset', 'uint32', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('buffer', 'string', 63, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('OpenFile', 'open_file'),
'elements': [('name_string_id', 'uint16', 1, 'in'),
             ('flags', 'uint16', 1, 'in', ('FileFlag', 'file_flag', [('ReadOnly', 'read_only', 0x0001),
                                                                     ('WriteOnly', 'write_only', 0x0002),
                                                                     ('ReadWrite', 'read_write', 0x0004),
                                                                     ('Append', 'append', 0x0008),
                                                                     ('Create', 'create', 0x0010),
                                                                     ('Truncate', 'truncate', 0x0020)])),
             ('permissions', 'uint16', 1, 'in', ('FilePermission', 'file_permission', [('UserAll', 'user_all', 00700),
                                                                                       ('UserRead', 'user_read', 00400),
                                                                                       ('UserWrite', 'user_write', 00200),
                                                                                       ('UserExecute', 'user_execute', 00100),
                                                                                       ('GroupAll', 'group_all', 00070),
                                                                                       ('GroupRead', 'group_read', 00040),
                                                                                       ('GroupWrite', 'group_write', 00020),
                                                                                       ('GroupExecute', 'group_execute', 00010),
                                                                                       ('OthersAll', 'others_all', 00007),
                                                                                       ('OthersRead', 'others_read', 00004),
                                                                                       ('OthersWrite', 'others_write', 00002),
                                                                                       ('OthersExecute', 'others_execute', 00001)])),
             ('error_code', 'uint8', 1, 'out'),
             ('file_id', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('CloseFile', 'close_file'),
'elements': [('file_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetFileName', 'get_file_name'),
'elements': [('file_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('name_string_id', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('WriteFile', 'write_file'),
'elements': [('file_id', 'uint16', 1, 'in'),
             ('buffer', 'uint8', 61, 'in'),
             ('length_to_write', 'uint8', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('length_written', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('WriteFileUnchecked', 'write_file_unchecked'),
'elements': [('file_id', 'uint16', 1, 'in'),
             ('buffer', 'uint8', 61, 'in'),
             ('length_to_write', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('WriteFileAsync', 'write_file_async'),
'elements': [('file_id', 'uint16', 1, 'in'),
             ('buffer', 'uint8', 61, 'in'),
             ('length_to_write', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('ReadFile', 'read_file'),
'elements': [('file_id', 'uint16', 1, 'in'),
             ('length_to_read', 'uint8', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('buffer', 'uint8', 62, 'out'),
             ('length_read', 'int8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('ReadFileAsync', 'read_file_async'),
'elements': [('file_id', 'uint16', 1, 'in'),
             ('length_to_read', 'uint64', 1, 'in'),
             ('error_code', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('AbortAsyncFileRead', 'abort_async_file_read'),
'elements': [('file_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetFilePosition', 'set_file_position'),
'elements': [('file_id', 'uint16', 1, 'in'),
             ('offset', 'int64', 1, 'in'),
             ('origin', 'uint8', 1, 'in', ('FileOrigin', 'file_origin', [('Set', 'set', 0),
                                                                         ('Current', 'current', 1),
                                                                         ('End', 'end', 2)])),
             ('error_code', 'uint8', 1, 'out'),
             ('position', 'uint64', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetFilePosition', 'get_file_position'),
'elements': [('file_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('position', 'uint64', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('AsyncFileWrite', 'async_file_write'),
'elements': [('file_id', 'uint16', 1, 'out'),
             ('error_code', 'uint8', 1, 'out'),
             ('length_written', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('AsyncFileRead', 'async_file_read'),
'elements': [('file_id', 'uint16', 1, 'out'),
             ('error_code', 'uint8', 1, 'out'),
             ('buffer', 'uint8', 60, 'out'),
             ('length_read', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
""",
'de':
"""
"""
}]
})
