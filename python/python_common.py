#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python Generator
Copyright (C) 2012-2013, 2017, 2019 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011-2013 Olaf Lüke <olaf@tinkerforge.com>

python_common.py: Common Library for generation of Python bindings and documentation

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

class PythonDevice(common.Device):
    def get_python_import_name(self):
        return self.get_category().under + '_' + self.get_name().under

    def get_python_class_name(self):
        return self.get_category().camel + self.get_name().camel

class PythonPacket(common.Packet):
    def get_python_parameters(self, high_level=False):
        parameters = []

        for element in self.get_elements(direction='in', high_level=high_level):
            parameters.append(element.get_name().under)

        return ', '.join(parameters)

class PythonElement(common.Element):
    python_types = {
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
        'char':   'chr',
        'string': 'str'
    }

    python_struct_formats = {
        'int8':   'b',
        'uint8':  'B',
        'int16':  'h',
        'uint16': 'H',
        'int32':  'i',
        'uint32': 'I',
        'int64':  'q',
        'uint64': 'Q',
        'float':  'f',
        'bool':   '!',
        'char':   'c',
        'string': 's'
    }

    python_default_item_values = {
        'int8':   '0',
        'uint8':  '0',
        'int16':  '0',
        'uint16': '0',
        'int32':  '0',
        'uint32': '0',
        'int64':  '0',
        'uint64': '0',
        'float':  '0.0',
        'bool':   'False',
        'char':   "'\\0'",
        'string': None
    }

    python_parameter_coercions = {
        'int8':   ('int({0})',           'list(map(int, {0}))'),
        'uint8':  ('int({0})',           'list(map(int, {0}))'),
        'int16':  ('int({0})',           'list(map(int, {0}))'),
        'uint16': ('int({0})',           'list(map(int, {0}))'),
        'int32':  ('int({0})',           'list(map(int, {0}))'),
        'uint32': ('int({0})',           'list(map(int, {0}))'),
        'int64':  ('int({0})',           'list(map(int, {0}))'),
        'uint64': ('int({0})',           'list(map(int, {0}))'),
        'float':  ('float({0})',         'list(map(float, {0}))'),
        'bool':   ('bool({0})',          'list(map(bool, {0}))'),
        'char':   ('create_char({0})',   'create_char_list({0})'),
        'string': ('create_string({0})', 'create_string({0})')
    }

    def format_value(self, value):
        if isinstance(value, list):
            result = []

            for subvalue in value:
                result.append(self.format_value(subvalue))

            return '[{0}]'.format(', '.join(result))

        type_ = self.get_type()

        if type_ == 'float':
            return common.format_float(value)

        if type_ == 'bool':
            return str(bool(value))

        if type_ in ['char', 'string']:
            return '"{0}"'.format(value.replace('"', '\\"'))

        return str(value)

    def get_python_name(self):
        return self.get_name().under

    def get_python_type(self, cardinality=None):
        assert cardinality == None or (isinstance(cardinality, int) and cardinality > 0), cardinality

        python_type = PythonElement.python_types[self.get_type()]

        if cardinality == None:
            cardinality = self.get_cardinality()

        if cardinality == 1 or self.get_type() == 'string':
            return python_type

        return '[{0}, ...]'.format(python_type)

    def get_python_struct_format(self):
        f = PythonElement.python_struct_formats[self.get_type()]
        cardinality = self.get_cardinality()

        if cardinality > 1:
            f = str(cardinality) + f

        return f

    def get_python_default_item_value(self):
        value = PythonElement.python_default_item_values[self.get_type()]

        if value == None:
            common.GeneratorError('Invalid array item type: ' + self.get_type())

        return value

    def get_python_parameter_coercion(self):
        coercion = PythonElement.python_parameter_coercions[self.get_type()]

        if self.get_cardinality() == 1:
            return coercion[0]
        else:
            return coercion[1]

class PythonGeneratorTrait:
    def get_doc_null_value_name(self):
        return 'None'

    def get_doc_formatted_param(self, element):
        return element.get_name().under
