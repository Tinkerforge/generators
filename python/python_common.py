#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python Generator
Copyright (C) 2012-2013, 2017 Matthias Bolte <matthias@tinkerforge.com>
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
        return self.get_underscore_category() + '_' + self.get_underscore_name()

    def get_python_class_name(self):
        return self.get_camel_case_category() + self.get_camel_case_name()

class PythonPacket(common.Packet):
    def get_python_parameters(self, high_level=False):
        parameters = []

        for element in self.get_elements(direction='in', high_level=high_level):
            parameters.append(element.get_underscore_name())

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
        'string': "'\\0'"
    }

    def get_python_type(self):
        python_type = PythonElement.python_types[self.get_type()]

        if self.get_cardinality() == 1 or python_type == 'str':
            return python_type
        else:
            return '[' + ', '.join([python_type] * self.get_cardinality()) + ']'

    def get_python_struct_format(self):
        f = PythonElement.python_struct_formats[self.get_type()]
        c = self.get_cardinality()

        if c > 1:
            f = str(c) + f

        return f

    def get_python_default_item_value(self):
        return PythonElement.python_default_item_values[self.get_type()]
