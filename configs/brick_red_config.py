# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# RED Brick communication config

OBJECT_TYPE_CONSTANTS = ('ObjectType', 'object_type', [('String', 'string', 0),
                                                       ('List', 'list', 1),
                                                       ('File', 'file', 2),
                                                       ('Directory', 'directory', 3),
                                                       ('Process', 'process', 4),
                                                       ('Program', 'program', 5)])

FILE_TYPE_CONSTANTS = ('FileType', 'file_type', [('Unknown', 'unknown', 0),
                                                 ('Regular', 'regular', 1),
                                                 ('Directory', 'directory', 2),
                                                 ('Character', 'character', 3),
                                                 ('Block', 'block', 4),
                                                 ('FIFO', 'fifo', 5),
                                                 ('Symlink', 'symlink', 6),
                                                 ('Socket', 'socket', 7),
                                                 ('Pipe', 'pipe', 8)])

FILE_FLAG_CONSTANTS = ('FileFlag', 'file_flag', [('ReadOnly', 'read_only', 0x0001),
                                                 ('WriteOnly', 'write_only', 0x0002),
                                                 ('ReadWrite', 'read_write', 0x0004),
                                                 ('Append', 'append', 0x0008),
                                                 ('Create', 'create', 0x0010),
                                                 ('Exclusive', 'exclusive', 0x0020),
                                                 ('NonBlocking', 'non_blocking', 0x0040),
                                                 ('Truncate', 'truncate', 0x0080),
                                                 ('Temporary', 'temporary', 0x0100)])

PIPE_FLAG_CONSTANTS = ('PipeFlag', 'pipe_flag', [('NonBlockingRead', 'non_blocking_read', 0x0001),
                                                 ('NonBlockingWrite', 'non_blocking_write', 0x0002)])

# the permission bit values match the UNIX permission bit values, this allows
# to use the normal octal way to write them, e.g. 0755
FILE_PERMISSION_CONSTANTS = ('FilePermission', 'file_permission', [('UserAll', 'user_all', 00700),
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
                                                                   ('OthersExecute', 'others_execute', 00001)])

FILE_ORIGIN_CONSTANTS = ('FileOrigin', 'file_origin', [('Beginning', 'beginning', 0),
                                                       ('Current', 'current', 1),
                                                       ('End', 'end', 2)])

DIRECTORY_FLAG_CONSTANTS = ('DirectoryFlag', 'directory_flag', [('Recursive', 'recursive', 0x0001),
                                                                ('Exclusive', 'exclusive', 0x0002)])

# the signal numbers match the UNIX signal numbers on purpose
PROCESS_SIGNAL_CONSTANTS = ('ProcessSignal', 'process_signal', [('Interrupt', 'interrupt', 2),
                                                                ('Quit', 'quit', 3),
                                                                ('Abort', 'abort', 6),
                                                                ('Kill', 'kill', 9),
                                                                ('User1', 'user1', 10),
                                                                ('User2', 'user2', 12),
                                                                ('Terminate', 'terminate', 15),
                                                                ('Continue', 'continue', 18),
                                                                ('Stop', 'stop', 19)])

PROCESS_STATE_CONSTANTS = ('ProcessState', 'process_state', [('Unknown', 'unknown', 0),
                                                             ('Running', 'running', 1),
                                                             ('Error', 'error', 2),
                                                             ('Exited', 'exited', 3),
                                                             ('Killed', 'killed', 4),
                                                             ('Stopped', 'stopped', 5)])

PROGRAM_STDIO_REDIRECTION_CONSTANTS = ('ProgramStdioRedirection', 'program_stdio_redirection', [('DevNull', 'dev_null', 0),
                                                                                                ('Pipe', 'pipe', 1),
                                                                                                ('File', 'file', 2),
                                                                                                ('Stdout', 'stdout', 3),
                                                                                                ('Log', 'log', 4)])

PROGRAM_START_CONDITION_CONSTANTS = ('ProgramStartCondition', 'program_start_condition', [('Never', 'never', 0),
                                                                                          ('Now', 'now', 1),
                                                                                          ('Reboot', 'reboot', 2),
                                                                                          ('Timestamp', 'timestamp', 3)])

PROGRAM_REPEAT_MODE_CONSTANTS = ('ProgramRepeatMode', 'program_repeat_mode', [('Never', 'never', 0),
                                                                              ('Interval', 'interval', 1),
                                                                              ('Selection', 'selection', 2)])

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

com['api'] = {
'en':
"""
The RED Brick API operates on reference counted objects (strings, lists, files,
directories, processes and programs) that are identified by their 16bit object
ID. Functions that allocate or return an object ID (e.g. :func:`AllocateString`
and :func:`GetNextDirectoryEntry`) increase the reference count of the returned
object. If the object is no longer needed then :func:`ReleaseObject` has to
be called to decrease the reference count of the object again. In contrast to
allocation and getter functions, the reference count for an object returned by
a callback is not increased and :func:`ReleaseObject` must not be called for
such an object in response to a callback.

There are functions (e.g. :func:`GetFileInfo`) that only return valid objects
under certain conditions. This conditions are documented for the specific
functions. For invalid objects :func:`ReleaseObject` must not be called.

There are also function (e.g. :func:`SetProcessStdioRedirection`) that have
conditionally unused object parameters. Under which conditions an object
parameter is unused is documented for the specific functions. For unused
object parameters 0 has to be passed as object ID.

The RED Brick API is more complex then the typical Brick API and requires more
elaborate error reporting than the :ref:`TCP/IP protocol <llproto_tcpip>`
can provide with its 2bit error code. Therefore, almost all functions of the
RED Brick API return an 8bit error code. Possible error codes are:

* Success = 0
* UnknownError = 1
* InvalidOperation = 2
* OperationAborted = 3
* InternalError = 4
* UnknownObjectID = 5
* NoFreeObjectID = 6
* ObjectIsLocked = 7
* NoMoreData = 8
* WrongListItemType = 9
* MalformedProgramConfig = 10
* InvalidParameter = 128 (EINVAL)
* NoFreeMemory = 129 (ENOMEM)
* NoFreeSpace = 130 (ENOSPC)
* AccessDenied = 131 (EACCES)
* AlreadyExists = 132 (EEXIST)
* DoesNotExist = 133 (ENOENT)
* Interrupted = 134 (EINTR)
* IsDirectory = 135 (EISDIR)
* NotADirectory = 136 (ENOTDIR)
* WouldBlock = 137 (EWOULDBLOCK)
* Overflow = 138 (EOVERFLOW)
* BadFileDescriptor = 139 (EBADF)
* OutOfRange = 140 (ERANGE)
* NameTooLong = 141 (ENAMETOOLONG)
* InvalidSeek = 142 (ESPIPE)
* NotSupported = 143 (ENOTSUP)

If a function returns an error code other than *Success* then its other
return values (if any) are invalid and must not be used.

The error code *InvalidOperation* is returned if the requested operation cannot
be performed because the current state of the object does not allow it. For
example, trying to append an item to a full list object or trying to undefine
an already undefined program.

The error code *NotSupported* is returned if the requested operation can never
be performed. For example, trying to append a list object to itself, trying to
get the name of a file object with type *Pipe* or trying to create a directory
non-recursively with more than the last part of the directory name referring
to non-existing directories.
""",
'de':
"""
"""
}

#
# object
#

com['packets'].append({
'type': 'function',
'name': ('ReleaseObject', 'release_object'),
'elements': [('object_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Decreases the reference count of an object by one and returns the resulting
error code. If the reference count reaches zero the object gets destroyed.
""",
'de':
"""
"""
}]
})

#
# string
#

com['packets'].append({
'type': 'function',
'name': ('AllocateString', 'allocate_string'),
'elements': [('length_to_reserve', 'uint32', 1, 'in'),
             ('buffer', 'string', 60, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('string_id', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Allocates a new string object, reserves ``length_to_reserve`` bytes memory
for it and sets up to the first 60 bytes. Set ``length_to_reserve`` to the
length of the string that should be stored in the string object.

Returns the object ID of the new string object and the resulting error code.
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
Truncates a string object to ``length`` bytes and returns the resulting
error code.
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
Returns the length of a string object in bytes and the resulting error code.
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
Sets a chunk of up to 58 bytes in a string object beginning at ``offset``.

Returns the resulting error code.
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
Returns a chunk up to 63 bytes from a string object beginning at ``offset`` and
returns the resulting error code.
""",
'de':
"""
"""
}]
})

#
# list
#

com['packets'].append({
'type': 'function',
'name': ('AllocateList', 'allocate_list'),
'elements': [('length_to_reserve', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('list_id', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Allocates a new list object and reserves memory for ``length_to_reserve``
items. Set ``length_to_reserve`` to the number of items that should be stored
in the list object.

Returns the object ID of the new list object and the resulting error code.

When a list object gets destroyed then the reference count of each object in
the list object is decreased by one.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetListLength', 'get_list_length'),
'elements': [('list_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('length', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the length of a list object in items and the resulting error code.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetListItem', 'get_list_item'),
'elements': [('list_id', 'uint16', 1, 'in'),
             ('index', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('item_object_id', 'uint16', 1, 'out'),
             ('type', 'uint8', 1, 'out', OBJECT_TYPE_CONSTANTS)],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the object ID and type of the object stored at ``index`` in a list
object and returns the resulting error code.

Possible object types are:

* String = 0
* List = 1
* File = 2
* Directory = 3
* Process = 4
* Program = 5
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('AppendToList', 'append_to_list'),
'elements': [('list_id', 'uint16', 1, 'in'),
             ('item_object_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Appends an object to a list object and increases the reference count of the
appended object by one.

Returns the resulting error code.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('RemoveFromList', 'remove_from_list'),
'elements': [('list_id', 'uint16', 1, 'in'),
             ('index', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Removes the object stored at ``index`` from a list object and decreases the
reference count of the removed object by one.

Returns the resulting error code.
""",
'de':
"""
"""
}]
})

#
# file
#

com['packets'].append({
'type': 'function',
'name': ('OpenFile', 'open_file'),
'elements': [('name_string_id', 'uint16', 1, 'in'),
             ('flags', 'uint16', 1, 'in', FILE_FLAG_CONSTANTS),
             ('permissions', 'uint16', 1, 'in', FILE_PERMISSION_CONSTANTS),
             ('uid', 'uint32', 1, 'in'),
             ('gid', 'uint32', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('file_id', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Opens an existing file or creates a new file and allocates a new file object
for it.

FIXME: name has to be absolute

The reference count of the name string object is increased by one. When the
file object gets destroyed then the reference count of the name string object is
decreased by one. Also the name string object is locked and cannot be modified
while the file object holds a reference to it.

The ``flags`` parameter takes a ORed combination of the following possible file
flags (in hexadecimal notation):

* ReadOnly = 0x0001 (O_RDONLY)
* WriteOnly = 0x0002 (O_WRONLY)
* ReadWrite = 0x0004 (O_RDWR)
* Append = 0x0008 (O_APPEND)
* Create = 0x0010 (O_CREAT)
* Exclusive = 0x0020 (O_EXCL)
* NonBlocking = 0x0040 (O_NONBLOCK)
* Truncate = 0x0080 (O_TRUNC)
* Temporary = 0x0100

FIXME: explain *Temporary* flag

The ``permissions`` parameter takes a ORed combination of the following
possible file permissions (in octal notation) that match the common UNIX
permission bits:

* UserRead = 00400
* UserWrite = 00200
* UserExecute = 00100
* GroupRead = 00040
* GroupWrite = 00020
* GroupExecute = 00010
* OthersRead = 00004
* OthersWrite = 00002
* OthersExecute = 00001

Returns the object ID of the new file object and the resulting error code.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('CreatePipe', 'create_pipe'),
'elements': [('flags', 'uint16', 1, 'in', PIPE_FLAG_CONSTANTS),
             ('error_code', 'uint8', 1, 'out'),
             ('file_id', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Creates a new pipe and allocates a new file object for it.

The ``flags`` parameter takes a ORed combination of the following possible
pipe flags (in hexadecimal notation):

* NonBlockingRead = 0x0001
* NonBlockingWrite = 0x0002

Returns the object ID of the new file object and the resulting error code.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetFileInfo', 'get_file_info'),
'elements': [('file_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('type', 'uint8', 1, 'out', FILE_TYPE_CONSTANTS),
             ('name_string_id', 'uint16', 1, 'out'),
             ('flags', 'uint16', 1, 'out'),
             ('permissions', 'uint16', 1, 'out', FILE_PERMISSION_CONSTANTS),
             ('uid', 'uint32', 1, 'out'),
             ('gid', 'uint32', 1, 'out'),
             ('length', 'uint64', 1, 'out'),
             ('access_timestamp', 'uint64', 1, 'out'),
             ('modification_timestamp', 'uint64', 1, 'out'),
             ('status_change_timestamp', 'uint64', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns various information about a file and the resulting error code.

Possible file types are:

* Unknown = 0
* Regular = 1
* Directory = 2
* Character = 3
* Block = 4
* FIFO = 5
* Symlink = 6
* Socket = 7
* Pipe = 8

If the file type is *Pipe* then the returned name string object is invalid,
because a pipe has no name. Otherwise the returned name string object was used
to open or create the file object, as passed to :func:`OpenFile`.

The returned flags were used to open or create the file object, as passed to
:func:`OpenFile` or :func:`CreatePipe`. See the respective function for a list
of possible file and pipe flags.

FIXME: everything except flags is invalid if file type is *Pipe*
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
             ('length_read', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Reads up to 62 bytes from a file object.

Returns the read bytes and the resulting error code.

If the file object was created by :func:`OpenFile` without the *NonBlocking*
flag or by :func:`CreatePipe` without the *NonBlockingRead* flag then the
error code *NotSupported* is returned.
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
Reads up to 2\ :sup:`63`\  - 1 bytes from a file object asynchronously. The
minimum asynchronous read length is 1 byte.

Returns the resulting error code.

The read bytes in 60 byte chunks and the resulting error codes of the read
operations are reported via the :func:`AsyncFileRead` callback.

If the file object was created by :func:`OpenFile` without the *NonBlocking*
flag or by :func:`CreatePipe` without the *NonBlockingRead* flag then the error
code *NotSupported* is reported via the :func:`AsyncFileRead` callback.
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
Aborts a :func:`ReadFileAsync` operation in progress.

Returns the resulting error code.
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
Writes up to 61 bytes to a file object.

Returns the actual number of bytes written and the resulting error code.

If the file object was created by :func:`OpenFile` without the *NonBlocking*
flag or by :func:`CreatePipe` without the *NonBlockingWrite* flag then the
error code *NotSupported* is returned.
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
Writes up to 61 bytes to a file object.

Does neither report the actual number of bytes written nor the resulting error
code.

If the file object was created by :func:`OpenFile` without the *NonBlocking*
flag or by :func:`CreatePipe` without the *NonBlockingWrite* flag then the
write operation will fail silently.
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
Writes up to 61 bytes to a file object.

Reports the actual number of bytes written and the resulting error code via the
:func:`AsyncFileWrite` callback.

If the file object was created by :func:`OpenFile` without the *NonBlocking*
flag or by :func:`CreatePipe` without the *NonBlockingWrite* flag then the
error code *NotSupported* is reported via the :func:`AsyncFileWrite` callback.
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
             ('origin', 'uint8', 1, 'in', FILE_ORIGIN_CONSTANTS),
             ('error_code', 'uint8', 1, 'out'),
             ('position', 'uint64', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Set the current seek position of a file object in bytes relative to ``origin``.

Possible file origins are:

* Beginning = 0
* Current = 1
* End = 2

Returns the resulting absolute seek position and error code.

If the file object was created by :func:`CreatePipe` then it has no seek
position and the error code *InvalidSeek* is returned.
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
Returns the current seek position of a file object in bytes and returns the
resulting error code.

If the file object was created by :func:`CreatePipe` then it has no seek
position and the error code *InvalidSeek* is returned.
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
This callback reports the result of a call to the :func:`ReadFileAsync`
function.
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
This callback reports the result of a call to the :func:`WriteFileAsync`
function.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('LookupFileInfo', 'lookup_file_info'),
'elements': [('name_string_id', 'uint16', 1, 'in'),
             ('follow_symlink', 'bool', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('type', 'uint8', 1, 'out', FILE_TYPE_CONSTANTS),
             ('permissions', 'uint16', 1, 'out', FILE_PERMISSION_CONSTANTS),
             ('uid', 'uint32', 1, 'out'),
             ('gid', 'uint32', 1, 'out'),
             ('length', 'uint64', 1, 'out'),
             ('access_timestamp', 'uint64', 1, 'out'),
             ('modification_timestamp', 'uint64', 1, 'out'),
             ('status_change_timestamp', 'uint64', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns various information about a file and the resulting error code.

FIXME: name has to be absolute

The information is obtained via the
`stat() <http://pubs.opengroup.org/onlinepubs/9699919799/functions/stat.html>`__
function. If ``follow_symlink`` is *false* then the
`lstat() <http://pubs.opengroup.org/onlinepubs/9699919799/functions/stat.html>`__
function is used instead.

See :func:`GetFileInfo` for a list of possible file types and see
:func:`OpenFile` for a list of possible file permissions.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('LookupSymlinkTarget', 'lookup_symlink_target'),
'elements': [('name_string_id', 'uint16', 1, 'in'),
             ('canonicalize', 'bool', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('target_string_id', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the target of a symbolic link and the resulting error code.

FIXME: name has to be absolute

If ``canonicalize`` is *false* then the target of the symbolic link is resolved
one level via the
`readlink() <http://pubs.opengroup.org/onlinepubs/9699919799/functions/readlink.html>`__
function, otherwise it is fully resolved using the
`realpath() <http://pubs.opengroup.org/onlinepubs/9699919799/functions/realpath.html>`__
function.
""",
'de':
"""
"""
}]
})

#
# directory
#

com['packets'].append({
'type': 'function',
'name': ('OpenDirectory', 'open_directory'),
'elements': [('name_string_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('directory_id', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Opens an existing directory and allocates a new directory object for it.

FIXME: name has to be absolute

The reference count of the name string object is increased by one. When the
directory object is destroyed then the reference count of the name string
object is decreased by one. Also the name string object is locked and cannot be
modified while the directory object holds a reference to it.

Returns the object ID of the new directory object and the resulting error code.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetDirectoryName', 'get_directory_name'),
'elements': [('directory_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('name_string_id', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the name of a directory object, as passed to :func:`OpenDirectory`, and
the resulting error code.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetNextDirectoryEntry', 'get_next_directory_entry'),
'elements': [('directory_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('name_string_id', 'uint16', 1, 'out'),
             ('type', 'uint8', 1, 'out', FILE_TYPE_CONSTANTS)],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the next entry in a directory object and the resulting error code.

If there is not next entry then error code *NoMoreData* is returned. To rewind
a directory object call :func:`RewindDirectory`.

See :func:`GetFileType` for a list of possible file types.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('RewindDirectory', 'rewind_directory'),
'elements': [('directory_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Rewinds a directory object and returns the resulting error code.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('CreateDirectory', 'create_directory'),
'elements': [('name_string_id', 'uint16', 1, 'in'),
             ('flags', 'uint16', 1, 'in', DIRECTORY_FLAG_CONSTANTS),
             ('permissions', 'uint16', 1, 'in', FILE_PERMISSION_CONSTANTS),
             ('uid', 'uint32', 1, 'in'),
             ('gid', 'uint32', 1, 'in'),
             ('error_code', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
FIXME: name has to be absolute
""",
'de':
"""
"""
}]
})

#
# process
#

com['packets'].append({
'type': 'function',
'name': ('GetProcesses', 'get_processes'),
'elements': [('error_code', 'uint8', 1, 'out'),
             ('processes_list_id', 'uint16', 1, 'out')],
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
'name': ('SpawnProcess', 'spawn_process'),
'elements': [('executable_string_id', 'uint16', 1, 'in'),
             ('arguments_list_id', 'uint16', 1, 'in'),
             ('environment_list_id', 'uint16', 1, 'in'),
             ('working_directory_string_id', 'uint16', 1, 'in'),
             ('uid', 'uint32', 1, 'in'),
             ('gid', 'uint32', 1, 'in'),
             ('stdin_file_id', 'uint16', 1, 'in'),
             ('stdout_file_id', 'uint16', 1, 'in'),
             ('stderr_file_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('process_id', 'uint16', 1, 'out')],
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
'name': ('KillProcess', 'kill_process'),
'elements': [('process_id', 'uint16', 1, 'in'),
             ('signal', 'uint8', 1, 'in', PROCESS_SIGNAL_CONSTANTS),
             ('error_code', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sends a UNIX signal to a process object and returns the resulting error code.

Possible UNIX signals are:

* Interrupt = 2
* Quit = 3
* Abort = 6
* Kill = 9
* User1 = 10
* User2 = 12
* Terminate = 15
* Continue =  18
* Stop = 19
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetProcessCommand', 'get_process_command'),
'elements': [('process_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('executable_string_id', 'uint16', 1, 'out'),
             ('arguments_list_id', 'uint16', 1, 'out'),
             ('environment_list_id', 'uint16', 1, 'out'),
             ('working_directory_string_id', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the executable, arguments, environment and working directory used to
spawn a process object, as passed to :func:`SpawnProcess`, and the resulting
error code.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetProcessIdentity', 'get_process_identity'),
'elements': [('process_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('uid', 'uint32', 1, 'out'),
             ('gid', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the user and group ID used to spawn a process object, as passed to
:func:`SpawnProcess`, and the resulting error code.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetProcessStdio', 'get_process_stdio'),
'elements': [('process_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('stdin_file_id', 'uint16', 1, 'out'),
             ('stdout_file_id', 'uint16', 1, 'out'),
             ('stderr_file_id', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the stdin, stdout and stderr files used to spawn a process object, as
passed to :func:`SpawnProcess`, and the resulting error code.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetProcessState', 'get_process_state'),
'elements': [('process_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('state', 'uint8', 1, 'out', PROCESS_STATE_CONSTANTS),
             ('timestamp', 'uint64', 1, 'out'),
             ('pid', 'uint32', 1, 'out'),
             ('exit_code', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the current state, timestamp, process ID and exit code of a process
object, and the resulting error code.

Possible process states are:

* Unknown = 0
* Running = 1
* Error = 2
* Exited = 3
* Killed = 4
* Stopped = 5

The timestamp represents the UNIX time since the process is in its current
state.

The process ID is only valid if the state is *Running* or *Stopped*.

The exit code is only valid if the state is *Error*, *Exited*, *Killed* or
*Stopped* and has different meanings depending on the state:

* Error: error code for error occurred while spawning the process (see below)
* Exited: exit status of the process
* Killed: UNIX signal number used to kill the process
* Stopped: UNIX signal number used to stop the process

Possible exit/error codes in *Error* state are:

* InternalError = 125
* CannotExecute = 126
* DoesNotExist = 127
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('ProcessStateChanged', 'process_state_changed'),
'elements': [('process_id', 'uint16', 1, 'out'),
             ('state', 'uint8', 1, 'out', PROCESS_STATE_CONSTANTS),
             ('timestamp', 'uint64', 1, 'out'),
             ('pid', 'uint32', 1, 'out'),
             ('exit_code', 'uint8', 1, 'out')],
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

#
# program
#

com['packets'].append({
'type': 'function',
'name': ('GetDefinedPrograms', 'get_defined_programs'),
'elements': [('error_code', 'uint8', 1, 'out'),
             ('programs_list_id', 'uint16', 1, 'out')],
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
'name': ('DefineProgram', 'define_program'),
'elements': [('identifier_string_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('program_id', 'uint16', 1, 'out')],
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
'name': ('UndefineProgram', 'undefine_program'),
'elements': [('program_id', 'uint16', 1, 'in'),
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
'name': ('GetProgramIdentifier', 'get_program_identifier'),
'elements': [('program_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('identifier_string_id', 'uint16', 1, 'out')],
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
'name': ('GetProgramDirectory', 'get_program_directory'),
'elements': [('program_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('directory_string_id', 'uint16', 1, 'out')],
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
'name': ('SetProgramCommand', 'set_program_command'),
'elements': [('program_id', 'uint16', 1, 'in'),
             ('executable_string_id', 'uint16', 1, 'in'),
             ('arguments_list_id', 'uint16', 1, 'in'),
             ('environment_list_id', 'uint16', 1, 'in'),
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
'name': ('GetProgramCommand', 'get_program_command'),
'elements': [('program_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('executable_string_id', 'uint16', 1, 'out'),
             ('arguments_list_id', 'uint16', 1, 'out'),
             ('environment_list_id', 'uint16', 1, 'out')],
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
'name': ('SetProgramStdioRedirection', 'set_program_stdio_redirection'),
'elements': [('program_id', 'uint16', 1, 'in'),
             ('stdin_redirection', 'uint8', 1, 'in', PROGRAM_STDIO_REDIRECTION_CONSTANTS),
             ('stdin_file_name_string_id', 'uint16', 1, 'in'),
             ('stdout_redirection', 'uint8', 1, 'in', PROGRAM_STDIO_REDIRECTION_CONSTANTS),
             ('stdout_file_name_string_id', 'uint16', 1, 'in'),
             ('stderr_redirection', 'uint8', 1, 'in', PROGRAM_STDIO_REDIRECTION_CONSTANTS),
             ('stderr_file_name_string_id', 'uint16', 1, 'in'),
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
'name': ('GetProgramStdioRedirection', 'get_program_stdio_redirection'),
'elements': [('program_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('stdin_redirection', 'uint8', 1, 'out', PROGRAM_STDIO_REDIRECTION_CONSTANTS),
             ('stdin_file_name_string_id', 'uint16', 1, 'out'),
             ('stdout_redirection', 'uint8', 1, 'out', PROGRAM_STDIO_REDIRECTION_CONSTANTS),
             ('stdout_file_name_string_id', 'uint16', 1, 'out'),
             ('stderr_redirection', 'uint8', 1, 'out', PROGRAM_STDIO_REDIRECTION_CONSTANTS),
             ('stderr_file_name_string_id', 'uint16', 1, 'out')],
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
'name': ('SetProgramSchedule', 'set_program_schedule'),
'elements': [('program_id', 'uint16', 1, 'in'),
             ('start_condition', 'uint8', 1, 'in', PROGRAM_START_CONDITION_CONSTANTS),
             ('start_timestamp', 'uint64', 1, 'in'),
             ('start_delay', 'uint32', 1, 'in'),
             ('repeat_mode', 'uint8', 1, 'in', PROGRAM_REPEAT_MODE_CONSTANTS),
             ('repeat_interval', 'uint32', 1, 'in'),
             ('repeat_second_mask', 'uint64', 1, 'in'),
             ('repeat_minute_mask', 'uint64', 1, 'in'),
             ('repeat_hour_mask', 'uint32', 1, 'in'),
             ('repeat_day_mask', 'uint32', 1, 'in'),
             ('repeat_month_mask', 'uint16', 1, 'in'),
             ('repeat_weekday_mask', 'uint8', 1, 'in'),
             ('error_code', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
FIXME: week starts on monday
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetProgramSchedule', 'get_program_schedule'),
'elements': [('program_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('start_condition', 'uint8', 1, 'out', PROGRAM_START_CONDITION_CONSTANTS),
             ('start_timestamp', 'uint64', 1, 'out'),
             ('start_delay', 'uint32', 1, 'out'),
             ('repeat_mode', 'uint8', 1, 'out', PROGRAM_REPEAT_MODE_CONSTANTS),
             ('repeat_interval', 'uint32', 1, 'out'),
             ('repeat_second_mask', 'uint64', 1, 'out'),
             ('repeat_minute_mask', 'uint64', 1, 'out'),
             ('repeat_hour_mask', 'uint32', 1, 'out'),
             ('repeat_day_mask', 'uint32', 1, 'out'),
             ('repeat_month_mask', 'uint16', 1, 'out'),
             ('repeat_weekday_mask', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
FIXME: week starts on monday
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetLastSpawnedProgramProcess', 'get_last_spawned_program_process'),
'elements': [('program_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('process_id', 'uint16', 1, 'out')],
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
'name': ('GetLastProgramSchedulerError', 'get_last_program_scheduler_error'),
'elements': [('program_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('timestamp', 'uint64', 1, 'out'),
             ('message_string_id', 'uint16', 1, 'out')],
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
'name': ('GetCustomProgramOptionNames', 'get_custom_program_option_names'),
'elements': [('program_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('names_list_id', 'uint16', 1, 'out')],
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
'name': ('SetCustomProgramOptionValue', 'set_custom_program_option_value'),
'elements': [('program_id', 'uint16', 1, 'in'),
             ('name_string_id', 'uint16', 1, 'in'),
             ('value_string_id', 'uint16', 1, 'in'),
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
'name': ('GetCustomProgramOptionValue', 'get_custom_program_option_value'),
'elements': [('program_id', 'uint16', 1, 'in'),
             ('name_string_id', 'uint16', 1, 'in'),
             ('error_code', 'uint8', 1, 'out'),
             ('value_string_id', 'uint16', 1, 'out')],
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
'name': ('RemoveCustomProgramOption', 'remove_custom_program_option'),
'elements': [('program_id', 'uint16', 1, 'in'),
             ('name_string_id', 'uint16', 1, 'in'),
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
'type': 'callback',
'name': ('ProgramProcessSpawned', 'program_process_spawned'),
'elements': [('program_id', 'uint16', 1, 'out')],
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
'name': ('ProgramSchedulerErrorOccurred', 'program_scheduler_error_occurred'),
'elements': [('program_id', 'uint16', 1, 'out')],
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
