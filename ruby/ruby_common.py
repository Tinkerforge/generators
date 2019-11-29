#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ruby Generator
Copyright (C) 2012-2013, 2019 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

ruby_common.py: Common Library for generation of Ruby bindings and documentation

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

class RubyDevice(common.Device):
    def get_ruby_class_name(self):
        return self.get_category().camel + self.get_name().camel

class RubyPacket(common.Packet):
    def get_ruby_parameters(self, high_level=False):
        params = []

        for element in self.get_elements(direction='in', high_level=high_level):
            params.append(element.get_name().under)

        return ', '.join(params)

class RubyElement(common.Element):
    ruby_types = {
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

    ruby_pack_formats = {
        'int8':   ('c', 1),
        'uint8':  ('C', 1),
        'int16':  ('s', 2),
        'uint16': ('S', 2),
        'int32':  ('l', 4),
        'uint32': ('L', 4),
        'int64':  ('q', 8),
        'uint64': ('Q', 8),
        'float':  ('e', 4),
        'bool':   ('?', 1),
        'char':   ('k', 1),
        'string': ('Z', 1)
    }

    ruby_default_item_values = {
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

    def get_ruby_type(self):
        ruby_type = RubyElement.ruby_types[self.get_type()]
        cardinality = self.get_cardinality()

        if cardinality == 1 or self.get_type() == 'string':
            return ruby_type

        return '[{0}, ...]'.format(ruby_type)

    def get_ruby_pack_format(self):
        return RubyElement.ruby_pack_formats[self.get_type()]

    def get_ruby_default_item_value(self):
        value = RubyElement.ruby_default_item_values[self.get_type()]

        if value == None:
            common.GeneratorError('Invalid array item type: ' + self.get_type())

        return value

class RubyGeneratorTrait:
    def get_doc_null_value_name(self):
        return 'nil'

    def get_doc_formatted_param(self, element):
        return element.get_name().under
