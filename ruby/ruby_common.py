#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ruby Documentation Generator
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

def make_parameter_list(packet):
    params = []
    for element in packet.get_elements('in'):
        params.append(element.get_underscore_name())
    return ", ".join(params)

class RubyDevice(common.Device):
    def get_ruby_class_name(self):
        return self.get_category() + self.get_camel_case_name()

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
        'bool':   'bool',
        'char':   'str',
        'string': 'str',
        'float':  'float'
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
        'string': ('Z', 1),
        'char':   ('k', 1)
    }

    def get_ruby_type(self):
        t = RubyElement.ruby_types[self.get_type()]

        if self.get_cardinality() == 1 or t == 'str':
            return t

        return '[' + ', '.join([t]*self.get_cardinality()) + ']'

    def get_ruby_pack_format(self):
        return RubyElement.ruby_pack_formats[self.get_type()]
