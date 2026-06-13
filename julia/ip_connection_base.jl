# Copyright (C) 2012-2015, 2017, 2019-2020 Matthias Bolte <matthias@tinkerforge.com>
# Copyright (C) 2011-2012 Olaf Lüke <olaf@tinkerforge.com>
#
# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

py"""
import struct
import socket
import sys
import time
import os
import math
import hmac
import hashlib
import errno
import threading

try:
    import queue # Python 3
except ImportError:
    import Queue as queue # Python 2

def pack_struct(format, data):
    #format = bytearray(format.encode())
    print("bla")
    print(data)
    print("bla")
    return struct.pack(format, *data)

def unpack_struct(format, data):
    #format = bytearray(format.encode())
    return struct.unpack(format, *data)

def urandom(size):
    return os.urandom(size)

# internal
def get_uid_from_data(data):
    return struct.unpack('<I', data[0:4])[0]

# internal
def get_length_from_data(data):
    return struct.unpack('<B', data[4:5])[0]

# internal
def get_function_id_from_data(data):
    return struct.unpack('<B', data[5:6])[0]

# internal
def get_sequence_number_from_data(data):
    return (struct.unpack('<B', data[6:7])[0] >> 4) & 0x0F

# internal
def get_error_code_from_data(data):
    return (struct.unpack('<B', data[7:8])[0] >> 6) & 0x03

BASE58 = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'

# internal
def base58encode(value):
    encoded = ''

    while value >= 58:
        div, mod = divmod(value, 58)
        encoded = BASE58[mod] + encoded
        value = div

    return BASE58[value] + encoded

# internal
def base58decode(encoded):
    value = 0
    column_multiplier = 1

    for c in encoded[::-1]:
        try:
            column = BASE58.index(c)
        except ValueError:
            raise Error(Error.INVALID_UID, 'UID "{0}" contains invalid character'.format(encoded), suppress_context=True)

        value += column * column_multiplier
        column_multiplier *= 58

    return value

# internal
def uid64_to_uid32(uid64):
    value1 = uid64 & 0xFFFFFFFF
    value2 = (uid64 >> 32) & 0xFFFFFFFF

    uid32  = (value1 & 0x00000FFF)
    uid32 |= (value1 & 0x0F000000) >> 12
    uid32 |= (value2 & 0x0000003F) << 16
    uid32 |= (value2 & 0x000F0000) << 6
    uid32 |= (value2 & 0x3F000000) << 2

    return uid32

# internal
def create_chunk_data(data, chunk_offset, chunk_length, chunk_padding):
    chunk_data = data[chunk_offset:chunk_offset + chunk_length]

    if len(chunk_data) < chunk_length:
        chunk_data += [chunk_padding] * (chunk_length - len(chunk_data))

    return chunk_data

if sys.hexversion < 0x03000000:
    # internal
    def create_char(value): # return str with len() == 1 and ord() <= 255
        if isinstance(value, str) and len(value) == 1: # Python2 str satisfies ord() <= 255 by default
            return value
        elif isinstance(value, unicode) and len(value) == 1: # pylint: disable=undefined-variable
            code_point = ord(value)

            if code_point <= 255:
                return chr(code_point)
            else:
                raise ValueError('Invalid char value: ' + repr(value))
        elif isinstance(value, bytearray) and len(value) == 1: # Python2 bytearray satisfies item <= 255 by default
            return chr(value[0])
        elif isinstance(value, int) and value >= 0 and value <= 255:
            return chr(value)
        else:
            raise ValueError('Invalid char value: ' + repr(value))
else:
    # internal
    def create_char(value): # return str with len() == 1 and ord() <= 255
        if isinstance(value, str) and len(value) == 1 and ord(value) <= 255:
            return value
        elif isinstance(value, (bytes, bytearray)) and len(value) == 1: # Python3 bytes/bytearray satisfies item <= 255 by default
            return chr(value[0])
        elif isinstance(value, int) and value >= 0 and value <= 255:
            return chr(value)
        else:
            raise ValueError('Invalid char value: ' + repr(value))

if sys.hexversion < 0x03000000:
    # internal
    def create_char_list(value, expected_type='char list'): # return list of str with len() == 1 and ord() <= 255 for all items
        if isinstance(value, list):
            return map(create_char, value)
        elif isinstance(value, str): # Python2 str satisfies ord() <= 255 by default
            return list(value)
        elif isinstance(value, unicode): # pylint: disable=undefined-variable
            chars = []

            for char in value:
                code_point = ord(char)

                if code_point <= 255:
                    chars.append(chr(code_point))
                else:
                    raise ValueError('Invalid {0} value: {1}'.format(expected_type, repr(value)))

            return chars
        elif isinstance(value, bytearray): # Python2 bytearray satisfies item <= 255 by default
            return map(chr, value)
        else:
            raise ValueError('Invalid {0} value: {1}'.format(expected_type, repr(value)))
else:
    # internal
    def create_char_list(value, expected_type='char list'): # return list of str with len() == 1 and ord() <= 255 for all items
        if isinstance(value, list):
            return list(map(create_char, value))
        elif isinstance(value, str):
            chars = list(value)

            for char in chars:
                if ord(char) > 255:
                    raise ValueError('Invalid {0} value: {1}'.format(expected_type, repr(value)))

            return chars
        elif isinstance(value, (bytes, bytearray)): # Python3 bytes/bytearray satisfies item <= 255 by default
            return list(map(chr, value))
        else:
            raise ValueError('Invalid {0} value: {1}'.format(expected_type, repr(value)))

if sys.hexversion < 0x03000000:
    # internal
    def create_string(value): # return str with ord() <= 255 for all chars
        if isinstance(value, str): # Python2 str satisfies ord() <= 255 by default
            return value
        elif isinstance(value, unicode): # pylint: disable=undefined-variable
            chars = []

            for char in value:
                code_point = ord(char)

                if code_point <= 255:
                    chars.append(chr(code_point))
                else:
                    raise ValueError('Invalid string value: {0}'.format(repr(value)))

            return ''.join(chars)
        elif isinstance(value, bytearray): # Python2 bytearray satisfies item <= 255 by default
            chars = []

            for byte in value:
                chars.append(chr(byte))

            return ''.join(chars)
        else:
            return ''.join(create_char_list(value, expected_type='string'))
else:
    # internal
    def create_string(value): # return str with ord() <= 255 for all chars
        if isinstance(value, str):
            for char in value:
                if ord(char) > 255:
                    raise ValueError('Invalid string value: {0}'.format(repr(value)))

            return value
        elif isinstance(value, (bytes, bytearray)): # Python3 bytes/bytearray satisfies item <= 255 by default
            chars = []

            for byte in value:
                chars.append(chr(byte))

            return ''.join(chars)
        else:
            return ''.join(create_char_list(value, expected_type='string'))

# internal
def pack_payload(data, form):
    if sys.hexversion < 0x03000000:
        packed = ''
    else:
        packed = b''

    for f, d in zip(form.split(' '), data):
        if '!' in f:
            if len(f) > 1:
                if int(f.replace('!', '')) != len(d):
                    raise ValueError('Incorrect bool list length')

                p = [0] * int(math.ceil(len(d) / 8.0))

                for i, b in enumerate(d):
                    if b:
                        p[i // 8] |= 1 << (i % 8)

                packed += struct.pack('<{0}B'.format(len(p)), *p)
            else:
                packed += struct.pack('<?', d)
        elif 'c' in f:
            if sys.hexversion < 0x03000000:
                if len(f) > 1:
                    packed += struct.pack('<' + f, *d)
                else:
                    packed += struct.pack('<' + f, d)
            else:
                if len(f) > 1:
                    packed += struct.pack('<' + f, *list(map(lambda char: bytes([ord(char)]), d)))
                else:
                    packed += struct.pack('<' + f, bytes([ord(d)]))
        elif 's' in f:
            if sys.hexversion < 0x03000000:
                packed += struct.pack('<' + f, d)
            else:
                packed += struct.pack('<' + f, bytes(map(ord, d)))
        elif len(f) > 1:
            packed += struct.pack('<' + f, *d)
        else:
            packed += struct.pack('<' + f, d)

    return packed

# Mark start and end of the unpack_payload funtion, so that the
# saleae bindings can extract it
# UNPACK_PAYLOAD_CUT_HERE
# internal
def unpack_payload(data, form):
    ret = []

    for f in form.split(' '):
        o = f

        if '!' in f:
            if len(f) > 1:
                f = '{0}B'.format(int(math.ceil(int(f.replace('!', '')) / 8.0)))
            else:
                f = 'B'

        f = '<' + f
        length = struct.calcsize(f)
        x = struct.unpack(f, data[:length])

        if '!' in o:
            y = []

            if len(o) > 1:
                for i in range(int(o.replace('!', ''))):
                    y.append(x[i // 8] & (1 << (i % 8)) != 0)
            else:
                y.append(x[0] != 0)

            x = tuple(y)

        if 'c' in f:
            if sys.hexversion < 0x03000000:
                if len(x) > 1:
                    ret.append(x)
                else:
                    ret.append(x[0])
            else:
                if len(x) > 1:
                    ret.append(tuple(map(lambda item: chr(ord(item)), x)))
                else:
                    ret.append(chr(ord(x[0])))
        elif 's' in f:
            if sys.hexversion < 0x03000000:
                s = x[0]
            else:
                s = ''.join(map(chr, x[0]))

            i = s.find('\x00')

            if i >= 0:
                s = s[:i]

            ret.append(s)
        elif len(x) > 1:
            ret.append(x)
        else:
            ret.append(x[0])

        data = data[length:]

    if len(ret) == 1:
        return ret[0]
    else:
        return ret
		
"""