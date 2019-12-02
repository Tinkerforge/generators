#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Perl Generator
Copyright (C) 2013-2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2014, 2019 Matthias Bolte <matthias@tinkerforge.com>

perl_common.py: Common Library for generation of Perl bindings and documentation

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

class PerlDevice(common.Device):
    def get_perl_class_name(self):
        return self.get_category().camel + self.get_name().camel

class PerlElement(common.Element):
    perl_types = {
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
        'char':   'char',
        'string': 'string'
    }

    perl_pack_formats = {
        'int8':   'c',
        'uint8':  'C',
        'int16':  's',
        'uint16': 'S',
        'int32':  'l',
        'uint32': 'L',
        'int64':  'q',
        'uint64': 'Q',
        'float':  'f',
        'bool':   '?',
        'char':   'a',
        'string': 'Z'
    }

    perl_default_item_values = {
        'int8':   '0',
        'uint8':  '0',
        'int16':  '0',
        'uint16': '0',
        'int32':  '0',
        'uint32': '0',
        'int64':  '0',
        'uint64': '0',
        'float':  '0.0',
        'bool':   '0',
        'char':   "'\\0'",
        'string': None
    }

    def format_value(self, value):
        if isinstance(value, list):
            result = []

            for subvalue in value:
                result.append(self.format_value(subvalue))

            return '({0})'.format(', '.join(result))

        type_ = self.get_type()

        if type_ == 'float':
            return common.format_float(value)

        if type_ == 'bool':
            return str(int(bool(value)))

        if type_ == 'char':
            return "'{0}'".format(value.replace("'", "\\'"))

        if type_ == 'string':
            return '"{0}"'.format(value.replace('"', '\\"'))

        return str(value)

    def get_perl_type(self, cardinality=None):
        assert cardinality == None or (isinstance(cardinality, int) and cardinality > 0), cardinality

        perl_type = PerlElement.perl_types[self.get_type()]

        if cardinality == None:
            cardinality = self.get_cardinality()

        if cardinality == 1 or self.get_type() == 'string':
            return perl_type

        return '[{0}, ...]'.format(perl_type)

    def get_perl_doc_name(self):
        name = self.get_name().under

        if self.get_cardinality() == 1 or self.get_type() == 'string':
            prefix = '$'
        else:
            prefix = '@'

        return prefix + name

    def get_perl_pack_format(self):
        f = PerlElement.perl_pack_formats[self.get_type()]
        cardinality = self.get_cardinality()

        if cardinality > 1:
            f += str(cardinality)

        return f

    def get_perl_default_item_value(self):
        value = PerlElement.perl_default_item_values[self.get_type()]

        if value == None:
            common.GeneratorError('Invalid array item type: ' + self.get_type())

        return value

class PerlGeneratorTrait:
    def get_doc_null_value_name(self):
        return 'undef'

    def get_doc_formatted_param(self, element):
        return element.get_name().under
