# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# RED Brick communication config

from openhab_common import *

com = {
    'author': 'Matthias Bolte <matthias@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Brick',
    'device_identifier': 17,
    'name': 'RED',
    'display_name': 'RED',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Executes user programs and controls other Bricks/Bricklets standalone',
        'de': 'Führt Programme aus und steuert andere Bricks/Bricklets selbständig'
    },
    'released': True,
    'documented': True,
    'discontinued': False,
    'features': [
        'brick_get_identity'
     ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append({
'name': 'Error Code',
'type': 'uint8',
'constants': [('Success', 0),
              ('Unknown Error', 1),
              ('Invalid Operation', 2),
              ('Operation Aborted', 3),
              ('Internal Error', 4),
              ('Unknown Session Id', 5),
              ('No Free Session Id', 6),
              ('Unknown Object Id', 7),
              ('No Free Object Id', 8),
              ('Object Is Locked', 9),
              ('No More Data', 10),
              ('Wrong List Item Type', 11),
              ('Program Is Purged', 12),
              ('Invalid Parameter', 128),
              ('No Free Memory', 129),
              ('No Free Space', 130),
              ('Access Denied', 121),
              ('Already Exists', 132),
              ('Does Not Exist', 133),
              ('Interrupted', 134),
              ('Is Directory', 135),
              ('Not A Directory', 136),
              ('Would Block', 137),
              ('Overflow', 138),
              ('Bad File Descriptor', 139),
              ('Out Of Range', 140),
              ('Name Too Long', 141),
              ('Invalid Seek', 142),
              ('Not Supported', 143),
              ('Too Many Open Files', 144)]
})

com['constant_groups'].append({
'name': 'Object Type',
'type': 'uint8',
'constants': [('String', 0),
              ('List', 1),
              ('File', 2),
              ('Directory', 3),
              ('Process', 4),
              ('Program', 5)]
})

com['constant_groups'].append({
'name': 'File Flag',
'type': 'uint32',
'constants': [('Read Only', 0x0001),
              ('Write Only', 0x0002),
              ('Read Write', 0x0004),
              ('Append', 0x0008),
              ('Create', 0x0010),
              ('Exclusive', 0x0020),
              ('Non Blocking', 0x0040),
              ('Truncate', 0x0080),
              ('Temporary', 0x0100),
              ('Replace', 0x0200)]
})

# the permission bit values match the UNIX permission bit values, this allows
# to use the normal octal way to write them, e.g. 0755
com['constant_groups'].append({
'name': 'File Permission',
'type': 'uint16',
'constants': [('User All', 0o0700),
              ('User Read', 0o0400),
              ('User Write', 0o0200),
              ('User Execute', 0o0100),
              ('Group All', 0o0070),
              ('Group Read', 0o0040),
              ('Group Write', 0o0020),
              ('Group Execute', 0o0010),
              ('Others All', 0o0007),
              ('Others Read', 0o0004),
              ('Others Write', 0o0002),
              ('Others Execute', 0o0001)]
})

com['constant_groups'].append({
'name': 'Pipe Flag',
'type': 'uint32',
'constants': [('Non Blocking Read', 0x0001),
              ('Non Blocking Write', 0x0002)]
})

com['constant_groups'].append({
'name': 'File Type',
'type': 'uint8',
'constants': [('Unknown', 0),
              ('Regular', 1),
              ('Directory', 2),
              ('Character', 3),
              ('Block', 4),
              ('FIFO', 5),
              ('Symlink', 6),
              ('Socket', 7),
              ('Pipe', 8)]
})

com['constant_groups'].append({
'name': 'File Origin',
'type': 'uint8',
'constants': [('Beginning', 0),
              ('Current', 1),
              ('End', 2)]
})

com['constant_groups'].append({
'name': 'File Event',
'type': 'uint16',
'constants': [('Readable', 0x0001),
              ('Writable', 0x0002)]
})

com['constant_groups'].append({
'name': 'Directory Entry Type',
'type': 'uint8',
'constants': [('Unknown', 0),
              ('Regular', 1),
              ('Directory', 2),
              ('Character', 3),
              ('Block', 4),
              ('FIFO', 5),
              ('Symlink', 6),
              ('Socket', 7)]
})

com['constant_groups'].append({
'name': 'Directory Flag',
'type': 'uint32',
'constants': [('Recursive', 0x0001),
              ('Exclusive', 0x0002)]
})

# the signal numbers match the UNIX signal numbers on purpose
com['constant_groups'].append({
'name': 'Process Signal',
'type': 'uint8',
'constants': [('Interrupt', 2),
              ('Quit', 3),
              ('Abort', 6),
              ('Kill', 9),
              ('User1', 10),
              ('User2', 12),
              ('Terminate', 15),
              ('Continue', 18),
              ('Stop', 19)]
})

com['constant_groups'].append({
'name': 'Process State',
'type': 'uint8',
'constants': [('Unknown', 0),
              ('Running', 1),
              ('Error', 2),
              ('Exited', 3),
              ('Killed', 4),
              ('Stopped', 5)]
})

com['constant_groups'].append({
'name': 'Program Stdio Redirection',
'type': 'uint8',
'constants': [('Dev Null', 0),
              ('Pipe', 1),
              ('File', 2),
              ('Individual Log', 3),
              ('Continuous Log', 4),
              ('Stdout', 5)]
})

com['constant_groups'].append({
'name': 'Program Start Mode',
'type': 'uint8',
'constants': [('Never', 0),
              ('Always', 1),
              ('Interval', 2),
              ('Cron', 3)]
})

com['constant_groups'].append({
'name': 'Program Scheduler State',
'type': 'uint8',
'constants': [('Stopped', 0),
              ('Running', 1)]
})

com['doc'] = {
'en':
"""
.. note::
 The API documentation for the RED Brick is currently incomplete.

The RED Brick API is meant to be used by the Brick Viewer to implement the
offered  functionality (getting status information, managing programs etc.).
Normal users will not need to use this API, it may only be interesting for
power users.

FIXME: explain sessions

The RED Brick API operates on reference counted objects (strings, lists, files,
directories, processes and programs) that are identified by their 16bit object
ID. Functions that allocate or return an object ID (e.g. :func:`Allocate String`
and :func:`Get Next Directory Entry`) increase the reference count of the returned
object. If the object is no longer needed then :func:`Release Object` has to
be called to decrease the reference count of the object again. In contrast to
allocation and getter functions, the reference count for an object returned by
a callback is not increased and :func:`Release Object` must not be called for
such an object in response to a callback.

There are functions (e.g. :func:`Get File Info`) that only return valid objects
under certain conditions. This conditions are documented for the specific
functions. For invalid objects :func:`Release Object` must not be called.

There are also function (e.g. :func:`Set Program Stdio Redirection`) that have
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
* UnknownSessionID = 5
* NoFreeSessionID = 6
* UnknownObjectID = 7
* NoFreeObjectID = 8
* ObjectIsLocked = 9
* NoMoreData = 10
* WrongListItemType = 11
* ProgramIsPurged = 12
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
* TooManyOpenFiles = 144 (EMFILE)

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

String objects store UTF-8 encoded data.
""",
'de':
"""
.. note::
 Die API Dokumentation für den RED Brick ist noch nicht vollständig.
"""
}

#
# session
#

com['packets'].append({
'type': 'function',
'name': 'Create Session',
'elements': [('Lifetime', 'uint32', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Session Id', 'uint16', 1, 'out', {})],
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
'name': 'Expire Session',
'elements': [('Session Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'})],
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
'name': 'Expire Session Unchecked',
'elements': [('Session Id', 'uint16', 1, 'in', {})],
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
'name': 'Keep Session Alive',
'elements': [('Session Id', 'uint16', 1, 'in', {}),
             ('Lifetime', 'uint32', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'})],
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

#
# object
#

com['packets'].append({
'type': 'function',
'name': 'Release Object',
'elements': [('Object Id', 'uint16', 1, 'in', {}),
             ('Session Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'})],
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

com['packets'].append({
'type': 'function',
'name': 'Release Object Unchecked',
'elements': [('Object Id', 'uint16', 1, 'in', {}),
             ('Session Id', 'uint16', 1, 'in', {})],
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

#
# string
#

com['packets'].append({
'type': 'function',
'name': 'Allocate String',
'elements': [('Length To Reserve', 'uint32', 1, 'in', {'unit': 'Byte'}),
             ('Buffer', 'string', 58, 'in', {}),
             ('Session Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('String Id', 'uint16', 1, 'out', {})],
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
'name': 'Truncate String',
'elements': [('String Id', 'uint16', 1, 'in', {}),
             ('Length', 'uint32', 1, 'in', {'unit': 'Byte'}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'})],
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
'name': 'Get String Length',
'elements': [('String Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Length', 'uint32', 1, 'out', {'unit': 'Byte'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the length of a string object and the resulting error code.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set String Chunk',
'elements': [('String Id', 'uint16', 1, 'in', {}),
             ('Offset', 'uint32', 1, 'in', {'unit': 'Byte'}),
             ('Buffer', 'string', 58, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'})],
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
'name': 'Get String Chunk',
'elements': [('String Id', 'uint16', 1, 'in', {}),
             ('Offset', 'uint32', 1, 'in', {'unit': 'Byte'}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Buffer', 'string', 63, 'out', {})],
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
'name': 'Allocate List',
'elements': [('Length To Reserve', 'uint16', 1, 'in', {}),
             ('Session Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('List Id', 'uint16', 1, 'out', {})],
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
'name': 'Get List Length',
'elements': [('List Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Length', 'uint16', 1, 'out', {})],
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
'name': 'Get List Item',
'elements': [('List Id', 'uint16', 1, 'in', {}),
             ('Index', 'uint16', 1, 'in', {}),
             ('Session Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Item Object Id', 'uint16', 1, 'out', {}),
             ('Type', 'uint8', 1, 'out', {'constant_group': 'Object Type'})],
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
'name': 'Append To List',
'elements': [('List Id', 'uint16', 1, 'in', {}),
             ('Item Object Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'})],
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
'name': 'Remove From List',
'elements': [('List Id', 'uint16', 1, 'in', {}),
             ('Index', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'})],
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
'name': 'Open File',
'elements': [('Name String Id', 'uint16', 1, 'in', {}),
             ('Flags', 'uint32', 1, 'in', {'constant_group': 'File Flag'}),
             ('Permissions', 'uint16', 1, 'in', {'constant_group': 'File Permission'}),
             ('UID', 'uint32', 1, 'in', {}),
             ('GID', 'uint32', 1, 'in', {}),
             ('Session Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('File Id', 'uint16', 1, 'out', {})],
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
* Replace = 0x0200

FIXME: explain *Temporary* and *Replace* flag

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
'name': 'Create Pipe',
'elements': [('Flags', 'uint32', 1, 'in', {'constant_group': 'Pipe Flag'}),
             ('Length', 'uint64', 1, 'in', {'unit': 'Byte'}),
             ('Session Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('File Id', 'uint16', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Creates a new pipe and allocates a new file object for it.

The ``flags`` parameter takes a ORed combination of the following possible
pipe flags (in hexadecimal notation):

* NonBlockingRead = 0x0001
* NonBlockingWrite = 0x0002

The length of the pipe buffer can be specified with the ``length`` parameter
in bytes. If length is set to zero, then the default pipe buffer length is used.

Returns the object ID of the new file object and the resulting error code.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get File Info',
'elements': [('File Id', 'uint16', 1, 'in', {}),
             ('Session Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Type', 'uint8', 1, 'out', {'constant_group': 'File Type'}),
             ('Name String Id', 'uint16', 1, 'out', {}),
             ('Flags', 'uint32', 1, 'out', {'constant_group': 'File Flag'}),
             ('Permissions', 'uint16', 1, 'out', {'constant_group': 'File Permission'}),
             ('UID', 'uint32', 1, 'out', {}),
             ('GID', 'uint32', 1, 'out', {}),
             ('Length', 'uint64', 1, 'out', {'unit': 'Byte'}),
             ('Access Timestamp', 'uint64', 1, 'out', {}),
             ('Modification Timestamp', 'uint64', 1, 'out', {}),
             ('Status Change Timestamp', 'uint64', 1, 'out', {})],
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
to open or create the file object, as passed to :func:`Open File`.

The returned flags were used to open or create the file object, as passed to
:func:`Open File` or :func:`Create Pipe`. See the respective function for a list
of possible file and pipe flags.

FIXME: everything except flags and length is invalid if file type is *Pipe*
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Read File',
'elements': [('File Id', 'uint16', 1, 'in', {}),
             ('Length To Read', 'uint8', 1, 'in', {'unit': 'Byte'}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Buffer', 'uint8', 62, 'out', {}),
             ('Length Read', 'uint8', 1, 'out', {'unit': 'Byte'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Reads up to 62 bytes from a file object.

Returns the bytes read, the actual number of bytes read and the resulting
error code.

If there is not data to be read, either because the file position reached
end-of-file or because there is not data in the pipe, then zero bytes are
returned.

If the file object was created by :func:`Open File` without the *NonBlocking*
flag or by :func:`Create Pipe` without the *NonBlockingRead* flag then the
error code *NotSupported* is returned.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Read File Async',
'elements': [('File Id', 'uint16', 1, 'in', {}),
             ('Length To Read', 'uint64', 1, 'in', {'unit': 'Byte'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Reads up to 2\ :sup:`63`\  - 1 bytes from a file object asynchronously.

Reports the bytes read (in 60 byte chunks), the actual number of bytes read and
the resulting error code via the :cb:`Async File Read` callback.

If there is not data to be read, either because the file position reached
end-of-file or because there is not data in the pipe, then zero bytes are
reported.

If the file object was created by :func:`Open File` without the *NonBlocking*
flag or by :func:`Create Pipe` without the *NonBlockingRead* flag then the error
code *NotSupported* is reported via the :cb:`Async File Read` callback.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Abort Async File Read',
'elements': [('File Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Aborts a :func:`Read File Async` operation in progress.

Returns the resulting error code.

On success the :cb:`Async File Read` callback will report *OperationAborted*.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Write File',
'elements': [('File Id', 'uint16', 1, 'in', {}),
             ('Buffer', 'uint8', 61, 'in', {}),
             ('Length To Write', 'uint8', 1, 'in', {'unit': 'Byte'}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Length Written', 'uint8', 1, 'out', {'unit': 'Byte'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Writes up to 61 bytes to a file object.

Returns the actual number of bytes written and the resulting error code.

If the file object was created by :func:`Open File` without the *NonBlocking*
flag or by :func:`Create Pipe` without the *NonBlockingWrite* flag then the
error code *NotSupported* is returned.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Write File Unchecked',
'elements': [('File Id', 'uint16', 1, 'in', {}),
             ('Buffer', 'uint8', 61, 'in', {}),
             ('Length To Write', 'uint8', 1, 'in', {'unit': 'Byte'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Writes up to 61 bytes to a file object.

Does neither report the actual number of bytes written nor the resulting error
code.

If the file object was created by :func:`Open File` without the *NonBlocking*
flag or by :func:`Create Pipe` without the *NonBlockingWrite* flag then the
write operation will fail silently.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Write File Async',
'elements': [('File Id', 'uint16', 1, 'in', {}),
             ('Buffer', 'uint8', 61, 'in', {}),
             ('Length To Write', 'uint8', 1, 'in', {'unit': 'Byte'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Writes up to 61 bytes to a file object.

Reports the actual number of bytes written and the resulting error code via the
:cb:`Async File Write` callback.

If the file object was created by :func:`Open File` without the *NonBlocking*
flag or by :func:`Create Pipe` without the *NonBlockingWrite* flag then the
error code *NotSupported* is reported via the :cb:`Async File Write` callback.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set File Position',
'elements': [('File Id', 'uint16', 1, 'in', {}),
             ('Offset', 'int64', 1, 'in', {'unit': 'Byte'}),
             ('Origin', 'uint8', 1, 'in', {'constant_group': 'File Origin'}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Position', 'uint64', 1, 'out', {'unit': 'Byte'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Set the current seek position of a file object relative to ``origin``.

Possible file origins are:

* Beginning = 0
* Current = 1
* End = 2

Returns the resulting absolute seek position and error code.

If the file object was created by :func:`Create Pipe` then it has no seek
position and the error code *InvalidSeek* is returned.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get File Position',
'elements': [('File Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Position', 'uint64', 1, 'out', {'unit': 'Byte'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the current seek position of a file object and returns the
resulting error code.

If the file object was created by :func:`Create Pipe` then it has no seek
position and the error code *InvalidSeek* is returned.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set File Events',
'elements': [('File Id', 'uint16', 1, 'in', {}),
             ('Events', 'uint16', 1, 'in', {'constant_group': 'File Event'}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'})],
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
'name': 'Get File Events',
'elements': [('File Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Events', 'uint16', 1, 'out', {'constant_group': 'File Event'})],
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
'name': 'Async File Read',
'elements': [('File Id', 'uint16', 1, 'out', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Buffer', 'uint8', 60, 'out', {}),
             ('Length Read', 'uint8', 1, 'out', {'unit': 'Byte'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback reports the result of a call to the :func:`Read File Async`
function.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Async File Write',
'elements': [('File Id', 'uint16', 1, 'out', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Length Written', 'uint8', 1, 'out', {'unit': 'Byte'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback reports the result of a call to the :func:`Write File Async`
function.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'File Events Occurred',
'elements': [('File Id', 'uint16', 1, 'out', {}),
             ('Events', 'uint16', 1, 'out', {'constant_group': 'File Event'})],
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
# directory
#

com['packets'].append({
'type': 'function',
'name': 'Open Directory',
'elements': [('Name String Id', 'uint16', 1, 'in', {}),
             ('Session Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Directory Id', 'uint16', 1, 'out', {})],
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
'name': 'Get Directory Name',
'elements': [('Directory Id', 'uint16', 1, 'in', {}),
             ('Session Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Name String Id', 'uint16', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the name of a directory object, as passed to :func:`Open Directory`, and
the resulting error code.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Next Directory Entry',
'elements': [('Directory Id', 'uint16', 1, 'in', {}),
             ('Session Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Name String Id', 'uint16', 1, 'out', {}),
             ('Type', 'uint8', 1, 'out', {'constant_group': 'Directory Entry Type'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the next entry in a directory object and the resulting error code.

If there is not next entry then error code *NoMoreData* is returned. To rewind
a directory object call :func:`Rewind Directory`.

Possible directory entry types are:

* Unknown = 0
* Regular = 1
* Directory = 2
* Character = 3
* Block = 4
* FIFO = 5
* Symlink = 6
* Socket = 7
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Rewind Directory',
'elements': [('Directory Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'})],
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
'name': 'Create Directory',
'elements': [('Name String Id', 'uint16', 1, 'in', {}),
             ('Flags', 'uint32', 1, 'in', {'constant_group': 'Directory Flag'}),
             ('Permissions', 'uint16', 1, 'in', {'constant_group': 'File Permission'}),
             ('UID', 'uint32', 1, 'in', {}),
             ('GID', 'uint32', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'})],
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
'name': 'Get Processes',
'elements': [('Session Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Processes List Id', 'uint16', 1, 'out', {})],
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
'name': 'Spawn Process',
'elements': [('Executable String Id', 'uint16', 1, 'in', {}),
             ('Arguments List Id', 'uint16', 1, 'in', {}),
             ('Environment List Id', 'uint16', 1, 'in', {}),
             ('Working Directory String Id', 'uint16', 1, 'in', {}),
             ('UID', 'uint32', 1, 'in', {}),
             ('GID', 'uint32', 1, 'in', {}),
             ('Stdin File Id', 'uint16', 1, 'in', {}),
             ('Stdout File Id', 'uint16', 1, 'in', {}),
             ('Stderr File Id', 'uint16', 1, 'in', {}),
             ('Session Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Process Id', 'uint16', 1, 'out', {})],
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
'name': 'Kill Process',
'elements': [('Process Id', 'uint16', 1, 'in', {}),
             ('Signal', 'uint8', 1, 'in', {'constant_group': 'Process Signal'}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'})],
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
'name': 'Get Process Command',
'elements': [('Process Id', 'uint16', 1, 'in', {}),
             ('Session Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Executable String Id', 'uint16', 1, 'out', {}),
             ('Arguments List Id', 'uint16', 1, 'out', {}),
             ('Environment List Id', 'uint16', 1, 'out', {}),
             ('Working Directory String Id', 'uint16', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the executable, arguments, environment and working directory used to
spawn a process object, as passed to :func:`Spawn Process`, and the resulting
error code.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Process Identity',
'elements': [('Process Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('PID', 'uint32', 1, 'out', {}),
             ('UID', 'uint32', 1, 'out', {}),
             ('GID', 'uint32', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the process ID and the user and group ID used to spawn a process object,
as passed to :func:`Spawn Process`, and the resulting error code.

The process ID is only valid if the state is *Running* or *Stopped*, see
:func:`Get Process State`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Process Stdio',
'elements': [('Process Id', 'uint16', 1, 'in', {}),
             ('Session Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Stdin File Id', 'uint16', 1, 'out', {}),
             ('Stdout File Id', 'uint16', 1, 'out', {}),
             ('Stderr File Id', 'uint16', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the stdin, stdout and stderr files used to spawn a process object, as
passed to :func:`Spawn Process`, and the resulting error code.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Process State',
'elements': [('Process Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('State', 'uint8', 1, 'out', {'constant_group': 'Process State'}),
             ('Timestamp', 'uint64', 1, 'out', {}),
             ('Exit Code', 'uint8', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the current state, timestamp and exit code of a process object, and
the resulting error code.

Possible process states are:

* Unknown = 0
* Running = 1
* Error = 2
* Exited = 3
* Killed = 4
* Stopped = 5

The timestamp represents the UNIX time since when the process is in its current
state.

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

The *CannotExecute* error can be caused by the executable being opened for
writing.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Process State Changed',
'elements': [('Process Id', 'uint16', 1, 'out', {}),
             ('State', 'uint8', 1, 'out', {'constant_group': 'Process State'}),
             ('Timestamp', 'uint64', 1, 'out', {}),
             ('Exit Code', 'uint8', 1, 'out', {})],
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
'name': 'Get Programs',
'elements': [('Session Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Programs List Id', 'uint16', 1, 'out', {})],
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
'name': 'Define Program',
'elements': [('Identifier String Id', 'uint16', 1, 'in', {}),
             ('Session Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Program Id', 'uint16', 1, 'out', {})],
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
'name': 'Purge Program',
'elements': [('Program Id', 'uint16', 1, 'in', {}),
             ('Cookie', 'uint32', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'})],
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
'name': 'Get Program Identifier',
'elements': [('Program Id', 'uint16', 1, 'in'),
             ('Session Id', 'uint16', 1, 'in'),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Identifier String Id', 'uint16', 1, 'out', {})],
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
'name': 'Get Program Root Directory',
'elements': [('Program Id', 'uint16', 1, 'in', {}),
             ('Session Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Root Directory String Id', 'uint16', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
FIXME: root directory is absolute: <home>/programs/<identifier>
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Program Command',
'elements': [('Program Id', 'uint16', 1, 'in', {}),
             ('Executable String Id', 'uint16', 1, 'in', {}),
             ('Arguments List Id', 'uint16', 1, 'in', {}),
             ('Environment List Id', 'uint16', 1, 'in', {}),
             ('Working Directory String Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
FIXME: working directory is relative to <home>/programs/<identifier>/bin
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Program Command',
'elements': [('Program Id', 'uint16', 1, 'in', {}),
             ('Session Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Executable String Id', 'uint16', 1, 'out', {}),
             ('Arguments List Id', 'uint16', 1, 'out', {}),
             ('Environment List Id', 'uint16', 1, 'out', {}),
             ('Working Directory String Id', 'uint16', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
FIXME: working directory is relative to <home>/programs/<identifier>/bin
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Program Stdio Redirection',
'elements': [('Program Id', 'uint16', 1, 'in', {}),
             ('Stdin Redirection', 'uint8', 1, 'in', {'constant_group': 'Program Stdio Redirection'}),
             ('Stdin File Name String Id', 'uint16', 1, 'in', {}),
             ('Stdout Redirection', 'uint8', 1, 'in', {'constant_group': 'Program Stdio Redirection'}),
             ('Stdout File Name String Id', 'uint16', 1, 'in', {}),
             ('Stderr Redirection', 'uint8', 1, 'in', {'constant_group': 'Program Stdio Redirection'}),
             ('Stderr File Name String Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
FIXME: stdio file names are relative to <home>/programs/<identifier>/bin
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Program Stdio Redirection',
'elements': [('Program Id', 'uint16', 1, 'in', {}),
             ('Session Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Stdin Redirection', 'uint8', 1, 'out', {'constant_group': 'Program Stdio Redirection'}),
             ('Stdin File Name String Id', 'uint16', 1, 'out', {}),
             ('Stdout Redirection', 'uint8', 1, 'out', {'constant_group': 'Program Stdio Redirection'}),
             ('Stdout File Name String Id', 'uint16', 1, 'out', {}),
             ('Stderr Redirection', 'uint8', 1, 'out', {'constant_group': 'Program Stdio Redirection'}),
             ('Stderr File Name String Id', 'uint16', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
FIXME: stdio file names are relative to <home>/programs/<identifier>/bin
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Program Schedule',
'elements': [('Program Id', 'uint16', 1, 'in', {}),
             ('Start Mode', 'uint8', 1, 'in', {'constant_group': 'Program Start Mode'}),
             ('Continue After Error', 'bool', 1, 'in', {}),
             ('Start Interval', 'uint32', 1, 'in', {}),
             ('Start Fields String Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'})],
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
'name': 'Get Program Schedule',
'elements': [('Program Id', 'uint16', 1, 'in', {}),
             ('Session Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Start Mode', 'uint8', 1, 'out', {'constant_group': 'Program Start Mode'}),
             ('Continue After Error', 'bool', 1, 'out', {}),
             ('Start Interval', 'uint32', 1, 'out', {}),
             ('Start Fields String Id', 'uint16', 1, 'out', {})],
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
'name': 'Get Program Scheduler State',
'elements': [('Program Id', 'uint16', 1, 'in', {}),
             ('Session Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('State', 'uint8', 1, 'out', {'constant_group': 'Program Scheduler State'}),
             ('Timestamp', 'uint64', 1, 'out', {}),
             ('Message String Id', 'uint16', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
FIXME: message is currently valid in error-occurred state only
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Continue Program Schedule',
'elements': [('Program Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'})],
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
'name': 'Start Program',
'elements': [('Program Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'})],
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
'name': 'Get Last Spawned Program Process',
'elements': [('Program Id', 'uint16', 1, 'in', {}),
             ('Session Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Process Id', 'uint16', 1, 'out', {}),
             ('Timestamp', 'uint64', 1, 'out', {})],
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
'name': 'Get Custom Program Option Names',
'elements': [('Program Id', 'uint16', 1, 'in', {}),
             ('Session Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Names List Id', 'uint16', 1, 'out', {})],
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
'name': 'Set Custom Program Option Value',
'elements': [('Program Id', 'uint16', 1, 'in', {}),
             ('Name String Id', 'uint16', 1, 'in', {}),
             ('Value String Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'})],
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
'name': 'Get Custom Program Option Value',
'elements': [('Program Id', 'uint16', 1, 'in', {}),
             ('Name String Id', 'uint16', 1, 'in', {}),
             ('Session Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'}),
             ('Value String Id', 'uint16', 1, 'out', {})],
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
'name': 'Remove Custom Program Option',
'elements': [('Program Id', 'uint16', 1, 'in', {}),
             ('Name String Id', 'uint16', 1, 'in', {}),
             ('Error Code', 'uint8', 1, 'out', {'constant_group': 'Error Code'})],
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
'name': 'Program Scheduler State Changed',
'elements': [('Program Id', 'uint16', 1, 'out', {})],
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
'name': 'Program Process Spawned',
'elements': [('Program Id', 'uint16', 1, 'out', {})],
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

com['openhab'] = {
    'imports': oh_generic_channel_imports(),
    'param_groups': oh_generic_channel_param_groups(),
    'params': [],
    'channels': [],
    'channel_types': [],
    'actions': [
        'Create Session', 'Expire Session', 'Expire Session Unchecked', 'Keep Session Alive',
        'Release Object', 'Release Object Unchecked',
        'Allocate String', 'Truncate String', 'Get String Length', 'Set String Chunk', 'Get String Chunk',
        'Allocate List', 'Get List Length', 'Get List Item', 'Append To List', 'Remove From List',
        'Open File', 'Create Pipe', 'Get File Info', 'Read File', 'Write File', 'Write File Unchecked',
        'Set File Position', 'Get File Position', 'Set File Events', 'Get File Events',
        'Open Directory', 'Get Directory Name', 'Get Next Directory Entry', 'Rewind Directory', 'Create Directory',
        'Get Processes', 'Spawn Process', 'Kill Process', 'Get Process Command', 'Get Process Identity', 'Get Process Stdio', 'Get Process State',
        'Get Programs', 'Define Program', 'Purge Program', 'Get Program Identifier', 'Get Program Root Directory',
        'Set Program Command', 'Get Program Command', 'Set Program Stdio Redirection', 'Get Program Stdio Redirection',
        'Set Program Schedule', 'Get Program Schedule', 'Get Program Scheduler State', 'Continue Program Schedule', 'Start Program', 'Get Last Spawned Program Process',
        'Get Custom Program Option Names', 'Set Custom Program Option Value', 'Get Custom Program Option Value', 'Remove Custom Program Option'
    ]
}
