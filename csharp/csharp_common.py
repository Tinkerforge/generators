#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C# Documentation Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

csharp_common.py: Common Library for generation of C# bindings and documentation

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

import os
import sys

sys.path.append(os.path.split(os.getcwd())[0])
import common

class CSharpDevice(common.Device):
    def get_csharp_class_name(self):
        return self.get_category() + self.get_camel_case_name()

class CSharpPacket(common.Packet):
    def get_csharp_parameter_list(self, use_out_params=True):
        param = []

        for element in self.get_elements():
            if (not use_out_params) and element.get_direction() == 'out':
                continue

            out = ''
            if element.get_direction() == 'out' and self.get_type() == 'function':
                out = 'out '

            csharp_type = element.get_csharp_type()
            name = element.get_headless_camel_case_name()

            param.append('{0}{1} {2}'.format(out, csharp_type, name))

        return ', '.join(param)

    def get_csharp_method_signature(self, print_full_name=False, is_doc=False):
        sig_format = "public {4}{0} {1}{2}({3})"
        ret_count = len(self.get_elements('out'))
        params = self.get_csharp_parameter_list(ret_count > 1)
        return_type = 'void'

        if ret_count == 1:
            return_type = self.get_elements('out')[0].get_csharp_type()

        class_prefix = ''

        if print_full_name:
            class_prefix = self.get_device().get_csharp_class_name() + '::'

        override = ''

        if not is_doc and self.has_prototype_in_device():
            override = 'override '

        return sig_format.format(return_type, class_prefix, self.get_camel_case_name(), params, override)

csharp_types = {
    'int8':   'short',
    'uint8':  'byte',
    'int16':  'short',
    'uint16': 'int',
    'int32':  'int',
    'uint32': 'long',
    'int64':  'long',
    'uint64': 'long',
    'float':  'float',
    'bool':   'bool',
    'char':   'char',
    'string': 'string'
}

def get_csharp_type(type, cardinality):
    t = csharp_types[type]

    if cardinality > 1 and type != 'string':
        t += '[]'

    return t

class CSharpElement(common.Element):
    csharp_le_converter_types = {
        'int8':   'byte',
        'uint8':  'byte',
        'int16':  'short',
        'uint16': 'short',
        'int32':  'int',
        'uint32': 'int',
        'int64':  'long',
        'uint64': 'long',
        'float':  'float',
        'bool':   'bool',
        'char':   'char',
        'string': 'string'
    }

    csharp_le_converter_from_methods = {
        'int8':   'SByteFrom',
        'uint8':  'ByteFrom',
        'int16':  'ShortFrom',
        'uint16': 'UShortFrom',
        'int32':  'IntFrom',
        'uint32': 'UIntFrom',
        'int64':  'LongFrom',
        'uint64': 'ULongFrom',
        'float':  'FloatFrom',
        'bool':   'BoolFrom',
        'char':   'CharFrom',
        'string': 'StringFrom'
    }

    def get_csharp_type(self):
        return get_csharp_type(self.get_type(), self.get_cardinality())

    def get_csharp_le_converter_type(self):
        t = CSharpElement.csharp_le_converter_types[self.get_type()]

        if self.get_cardinality() > 1 and self.get_type() != 'string':
            t += '[]'

        return t

    def get_csharp_le_converter_from_method(self):
        m =  CSharpElement.csharp_le_converter_from_methods[self.get_type()]

        if m != 'StringFrom' and self.get_cardinality() > 1:
            m = m.replace('From', 'ArrayFrom')

        return m
