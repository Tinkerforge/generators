#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ruby Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
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
        return self.get_camel_case_category() + self.get_camel_case_name()

class RubyPacket(common.Packet):
    def get_ruby_parameters(self, high_level=False):
        params = []

        for element in self.get_elements(direction='in', high_level=high_level):
            params.append(element.get_underscore_name())

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
        'char':   'str',
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

    ruby_default_values = {
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
        'string': "'\\0'"
    }

    def get_ruby_type(self):
        t = RubyElement.ruby_types[self.get_type()]

        if self.get_cardinality() == 1 or t == 'str':
            return t

        return '[' + ', '.join([t]*self.get_cardinality()) + ']'

    def get_ruby_pack_format(self):
        return RubyElement.ruby_pack_formats[self.get_type()]

    def get_ruby_default_value(self):
        return RubyElement.ruby_default_values[self.get_type()]
