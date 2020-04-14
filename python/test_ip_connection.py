# -*- coding: utf-8 -*-

import sys
from ip_connection import create_char, create_char_list, create_string, pack_payload, unpack_payload

def b(value):
    if sys.hexversion < 0x03000000:
        return value
    else:
        return bytes(map(ord, value))

#
# char
#

assert(create_char('a') == 'a') # str

if sys.hexversion < 0x03000000:
    assert(create_char(u'a') == 'a') # unicode
else:
    assert(create_char(b'a') == 'a') # bytes

assert(create_char(bytearray([97])) == 'a') # bytearray
assert(create_char(97) == 'a') # int

for c in range(256):
    k = (c + 1) % 256

    assert(create_char(chr(c)) == chr(c)) # str
    assert(create_char(chr(c)) != chr(k)) # str

    if sys.hexversion < 0x03000000:
        assert(create_char(unichr(c)) == chr(c)) # unicode
        assert(create_char(unichr(c)) != chr(k))
    else:
        assert(create_char(bytes([c])) == chr(c)) # bytes
        assert(create_char(bytes([c])) != chr(k)) # bytes

    assert(create_char(bytearray([c])) == chr(c)) # bytearray
    assert(create_char(bytearray([c])) != chr(k)) # bytearray
    assert(create_char(c) == chr(c)) # int
    assert(create_char(c) != chr(k)) # int

try:
    create_char('ab') # str
    assert(False)
except:
    pass

if sys.hexversion < 0x03000000:
    try:
        create_char(u'ab') # unicode
        assert(False)
    except:
        pass
else:
    try:
        create_char(b'ab') # bytes
        assert(False)
    except:
        pass

try:
    create_char(bytearray([42, 17])) # bytearray
    assert(False)
except:
    pass

try:
    create_char([42, 17]) # int
    assert(False)
except:
    pass

try:
    create_char(256) # int
    assert(False)
except:
    pass

#
# char list
#

assert(create_char_list('') == []) # str
assert(create_char_list('a') == ['a']) # str
assert(create_char_list('ab') == ['a', 'b']) # str
assert(create_char_list([]) == [])
assert(create_char_list(['a']) == ['a']) # str
assert(create_char_list(['a', 'b']) == ['a', 'b']) # str

if sys.hexversion < 0x03000000:
    assert(create_char_list(u'') == []) # unicode
    assert(create_char_list(u'a') == ['a']) # unicode
    assert(create_char_list(u'ab') == ['a', 'b']) # unicode
    assert(create_char_list([u'a']) == ['a']) # unicode
    assert(create_char_list([u'a', u'b']) == ['a', 'b']) # unicode
else:
    assert(create_char_list(b'') == []) # bytes
    assert(create_char_list(b'a') == ['a']) # bytes
    assert(create_char_list(b'ab') == ['a', 'b']) # bytes
    assert(create_char_list([b'a']) == ['a']) # bytes
    assert(create_char_list([b'a', b'b']) == ['a', 'b']) # bytes

assert(create_char_list(bytearray([])) == []) # bytearray
assert(create_char_list(bytearray([97])) == ['a']) # bytearray
assert(create_char_list(bytearray([97, 98])) == ['a', 'b']) # bytearray
assert(create_char_list([97]) == ['a']) # int
assert(create_char_list([97, 98]) == ['a', 'b']) # int

#
# string
#

assert(create_string('') == '') # str
assert(create_string('a') == 'a') # str
assert(create_string('ab') == 'ab') # str
assert(create_string([]) == '')
assert(create_string(['a']) == 'a') # str
assert(create_string(['a', 'b']) == 'ab') # str

if sys.hexversion < 0x03000000:
    assert(create_string(u'') == '') # unicode
    assert(create_string(u'a') == 'a') # unicode
    assert(create_string(u'ab') == 'ab') # unicode
    assert(create_string([u'a']) == 'a') # unicode
    assert(create_string([u'a', u'b']) == 'ab') # unicode
else:
    assert(create_string(b'') == '') # bytes
    assert(create_string(b'a') == 'a') # bytes
    assert(create_string(b'ab') == 'ab') # bytes
    assert(create_string([b'a']) == 'a') # bytes
    assert(create_string([b'a', b'b']) == 'ab') # bytes

assert(create_string(bytearray([])) == '') # bytearray
assert(create_string(bytearray([97])) == 'a') # bytearray
assert(create_string(bytearray([97, 98])) == 'ab') # bytearray
assert(create_string([97]) == 'a') # int
assert(create_string([97, 98]) == 'ab') # int

#
# pack_payload
#

assert(pack_payload(('a',), 's') == b('a'))
assert(pack_payload(('abc',), '5s') == b('abc\0\0'))
assert(pack_payload(('abc\xff',), '5s') == b('abc\xff\0'))
assert(pack_payload(('a',), 'c') == b('a'))
assert(pack_payload((['a', 'b', 'c'],), '3c') == b('abc'))

#
# unpack_payload
#

assert(unpack_payload(b('a'), 's') == 'a')
assert(unpack_payload(b('abc'), '3s') == 'abc')
assert(unpack_payload(b('abc\xff\0'), '5s') == 'abc\xff')
assert(unpack_payload(b('a'), 'c') == 'a')
assert(unpack_payload(b('abc'), '3c') == ('a', 'b', 'c'))
assert(unpack_payload(b('a\xff\0'), '3c') == ('a', '\xff', '\0'))
