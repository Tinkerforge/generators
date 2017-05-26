#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C# Generator
Copyright (C) 2012-2015 Matthias Bolte <matthias@tinkerforge.com>
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
        return self.get_camel_case_category() + self.get_camel_case_name()

class CSharpPacket(common.Packet):
    def get_csharp_parameters(self, context='signature', high_level=False, callback_wrapper=False):
        parameters = []
        out_count = len(self.get_elements(direction='out', high_level=high_level))

        for element in self.get_elements(high_level=high_level):
            if element.get_direction() == 'out' and self.get_type() == 'function':
                if out_count == 1:
                    continue
                else:
                    out = 'out '
            else:
                out = ''

            if context == 'call':
                csharp_type = ''
            else: # signature
                csharp_type = element.get_csharp_type() + ' '

            if high_level and callback_wrapper and element.get_level() == 'high' and element.get_cardinality() < 0:
                name = '({0})highLevelCallback.data'.format(element.get_csharp_type())
            else:
                name = element.get_headless_camel_case_name()

            parameters.append(''.join([out, csharp_type, name]))

        return ', '.join(parameters)

    def get_csharp_return_element(self, high_level=False):
        elements = self.get_elements(direction='out', high_level=high_level)

        if len(elements) == 1:
            return elements[0]
        else:
            return None

    def get_csharp_method_signature(self, print_full_name=False, is_doc=False):
        sig_format = "public {4}{0} {1}{2}({3})"
        ret_count = len(self.get_elements(direction='out'))
        params = self.get_csharp_parameters()
        return_type = 'void'

        if ret_count == 1:
            return_type = self.get_elements(direction='out')[0].get_csharp_type()

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

def get_csharp_type(type_, cardinality):
    csharp_type = csharp_types[type_]

    if (cardinality > 1 and type_ != 'string') or cardinality < 0:
        csharp_type += '[]'

    return csharp_type

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

    csharp_default_item_values = {
        'int8':   '0',
        'uint8':  '0',
        'int16':  '0',
        'uint16': '0',
        'int32':  '0',
        'uint32': '0',
        'int64':  '0',
        'uint64': '0',
        'float':  '0.0',
        'bool':   'false',
        'char':   "'\\0'",
        'string': None
    }

    def get_csharp_type(self):
        return get_csharp_type(self.get_type(), self.get_cardinality())

    def get_csharp_le_converter_type(self):
        converter_type = CSharpElement.csharp_le_converter_types[self.get_type()]

        if self.get_cardinality() > 1 and self.get_type() != 'string':
            converter_type += '[]'

        return converter_type

    def get_csharp_le_converter_from_method(self):
        from_method = CSharpElement.csharp_le_converter_from_methods[self.get_type()]

        if from_method != 'StringFrom' and self.get_cardinality() > 1:
            from_method = from_method.replace('From', 'ArrayFrom')

        return from_method

    def get_csharp_new(self, cardinality=None):
        if cardinality == None:
            return 'new {0}[{1}]'.format(csharp_types[self.get_type()], self.get_cardinality())
        else:
            return 'new {0}[{1}]'.format(csharp_types[self.get_type()], cardinality)

    def get_csharp_default_value(self):
        if self.get_cardinality() != 1:
            return 'null'
        else:
            value = CSharpElement.csharp_default_item_values[self.get_type()]

            if value == None:
                common.GeneratorError('Invalid array item type: ' + self.get_type())

            return value
