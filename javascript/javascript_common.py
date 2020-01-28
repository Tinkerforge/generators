#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JavaScript Generator
Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2014-2015, 2019-2020 Matthias Bolte <matthias@tinkerforge.com>

javascript_common.py: Common Library for generation of JavaScript bindings and documentation

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

class JavaScriptDevice(common.Device):
    def get_javascript_class_name(self):
        return self.get_category().camel + self.get_name().camel

class JavaScriptPacket(common.Packet):
    def get_javascript_parameter_list(self, high_level=False):
        params = []

        for element in self.get_elements(direction='in', high_level=high_level):
            params.append(element.get_name().headless)

        return ', '.join(params)

class JavaScriptElement(common.Element):
    javascript_types = {
        'int8':   'int',
        'uint8':  'int',
        'int16':  'int',
        'uint16': 'int',
        'int32':  'int',
        'uint32': 'int',
        'int64':  'int',
        'uint64': 'int',
        'float':  'float',
        'bool':   'boolean',
        'char':   'char',
        'string': 'string'
    }

    javascript_struct_formats = {
        'int8':   'b',
        'uint8':  'B',
        'int16':  'h',
        'uint16': 'H',
        'int32':  'i',
        'uint32': 'I',
        'int64':  'q',
        'uint64': 'Q',
        'float':  'f',
        'bool':   '?',
        'char':   'c',
        'string': 's'
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
            return str(bool(value)).lower()

        if type_ in ['char', 'string']:
            return "'{0}'".format(value.replace("'", "\\'"))

        return str(value)

    def get_javascript_type(self, cardinality=None):
        assert cardinality == None or (isinstance(cardinality, int) and cardinality > 0), cardinality

        javascript_type = JavaScriptElement.javascript_types[self.get_type()]

        if cardinality == None:
            cardinality = self.get_cardinality()

        if cardinality == 1 or self.get_type() == 'string':
            return javascript_type

        return '[{0}, ...]'.format(javascript_type)

    def get_javascript_struct_format(self):
        f = JavaScriptElement.javascript_struct_formats[self.get_type()]
        cardinality = self.get_cardinality()

        if cardinality > 1:
            f = f + str(cardinality)

        return f

class JavascriptGeneratorTrait:
    def get_bindings_name(self):
        return 'javascript'

    def get_bindings_display_name(self):
        return 'JavaScript'

    def get_doc_null_value_name(self):
        return 'null'

    def get_doc_formatted_param(self, element):
        return element.get_name().headless
