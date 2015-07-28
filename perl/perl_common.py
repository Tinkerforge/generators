#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Perl Generator
Copyright (C) 2013-2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2014 Matthias Bolte <matthias@tinkerforge.com>

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
        return self.get_camel_case_category() + self.get_camel_case_name()

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
        'bool':   'C',
        'char':   'a',
        'string': 'Z'
    }

    def get_perl_type(self):
        t = PerlElement.perl_types[self.get_type()]

        if self.get_cardinality() == 1 or t == 'string':
            return t

        return '[' + ', '.join([t]*self.get_cardinality()) + ']'

    def get_perl_doc_name(self):
        name = self.get_underscore_name()

        if self.get_cardinality() == 1 or self.get_type() == 'string':
            prefix = '$'
        else:
            prefix = '@'

        return prefix + name

    def get_perl_pack_format(self):
        f = PerlElement.perl_pack_formats[self.get_type()]
        c = self.get_cardinality()

        if c > 1:
            f += str(c)

        return f
