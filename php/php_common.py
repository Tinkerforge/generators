#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PHP Generator
Copyright (C) 2012, 2014 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

php_common.py: Common Library for generation of PHP bindings and documentation

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the
Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
"""

import sys
import os

sys.path.append(os.path.split(os.getcwd())[0])
import common

class PHPDevice(common.Device):
    def get_php_class_name(self):
        return self.get_category() + self.get_camel_case_name()

class PHPPacket(common.Packet):
    def get_php_return_type(self):
        if len(self.get_elements('out')) == 0:
            return 'void'
        if len(self.get_elements('out')) > 1:
            return 'array'

        for element in self.get_elements('out'):
            if element.get_cardinality() > 1 and element.get_type() != 'string':
                return 'array'
            else:
                return element.get_php_type()

    def get_php_parameter_list(self, for_doc=False):
        param = []

        for element in self.get_elements():
            if element.get_direction() == 'out' and self.get_type() == 'function':
                continue
            name = element.get_underscore_name()
            if for_doc:
                php_type = element.get_php_type()
                if element.get_cardinality() > 1 and element.get_type() != 'string':
                    php_type = 'array'

                param.append('{0} ${1}'.format(php_type, name))
            else:
                param.append('${0}'.format(name))

        return ', '.join(param)

class PHPElement(common.Element):
    php_type = {
        'int8':   'int',
        'uint8':  'int',
        'int16':  'int',
        'uint16': 'int',
        'int32':  'int',
        'uint32': 'int',
        'int64':  'int',
        'uint64': 'int',
        'float':  'float',
        'bool':   'bool',
        'char':   'string',
        'string': 'string'
    }

    php_pack_format = {
        'int8':   'c',
        'uint8':  'C',
        'int16':  'v',
        'uint16': 'v',
        'int32':  'V',
        'uint32': 'V',
        'int64':  'C8', # needs special handling
        'uint64': 'C8', # needs special handling
        'float':  'f',
        'bool':   'C',
        'char':   'c',
        'string': 'c'
    }

    def get_php_type(self):
        return PHPElement.php_type[self.get_type()]

    def get_php_pack_format(self):
        return PHPElement.php_pack_format[self.get_type()]

    def get_php_unpack_format(self):
        cardinality = self.get_cardinality()
        underscore_name = self.get_underscore_name()

        if self.get_type() in ['int64', 'uint64']:
            if cardinality > 1:
                unpack_format = []

                for i in range(0, cardinality):
                    unpack_format.append('C8{0}{1}'.format(underscore_name, chr(ord('A') + i)))

                return '/'.join(unpack_format)
            else:
                return 'C8{0}'.format(underscore_name)
        else:
            return'{0}{1}{2}'.format(PHPElement.php_pack_format[self.get_type()], cardinality, underscore_name)

    def get_php_unpack_fix(self):
        if self.get_cardinality() > 1:
            if self.get_type() == 'int16':
                return ('IPConnection::collectUnpackedInt16Array(', ')', ', ', '')
            elif self.get_type() == 'int32':
                return ('IPConnection::collectUnpackedInt32Array(', ')', ', ', '')
            elif self.get_type() == 'uint32':
                return ('IPConnection::collectUnpackedUInt32Array(', ')', ', ', '')
            elif self.get_type() == 'int64':
                return ('IPConnection::collectUnpackedInt64Array(', ')', ', ', '')
            elif self.get_type() == 'uint64':
                return ('IPConnection::collectUnpackedUInt64Array(', ')', ', ', '')
            elif self.get_type() == 'bool':
                return ('IPConnection::collectUnpackedBoolArray(', ')', ', ', '')
            elif self.get_type() == 'string':
                return ('IPConnection::implodeUnpackedString(', ')', ', ', '')
            elif self.get_type() == 'char':
                return ('IPConnection::collectUnpackedCharArray(', ')', ', ', '')
            else:
                return ('IPConnection::collectUnpackedArray(', ')', ', ', '')
        else:
            if self.get_type() == 'int16':
                return ('IPConnection::fixUnpackedInt16(', ')', ', ', '')
            elif self.get_type() == 'int32':
                return ('IPConnection::fixUnpackedInt32(', ')', ', ', '')
            elif self.get_type() == 'uint32':
                return ('IPConnection::fixUnpackedUInt32(', ')', ', ', '')
            elif self.get_type() == 'int64':
                return ('IPConnection::fixUnpackedInt64(', ')', ', ', '')
            elif self.get_type() == 'uint64':
                return ('IPConnection::fixUnpackedUInt64(', ')', ', ', '')
            elif self.get_type() == 'bool':
                return ('(bool)', '', '[', ']')
            elif self.get_type() == 'string':
                return ('chr(', ')', '[', ']')
            elif self.get_type() == 'char':
                return ('chr(', ')', '[', ']')
            else:
                return ('', '', '[', ']')
