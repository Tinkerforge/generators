# -*- coding: utf-8 -*-

"""
Tinkerforge Visual Programming Language (TVPL) Generator
Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>

tvpl_common.py: Common library for generation of TVPL bindings and documentation

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

class TVPLDevice(common.Device):
    def get_tvpl_device_name(self):
        return '_'.join([self.get_category().under, self.get_name().under])

class TVPLPacket(common.Packet):
    def get_packet_elements_name_as_list(self, elements):
        list_e = []

        for e in elements:
            list_e.append(e.get_name().under)

        return list_e

class TVPLElement(common.Element):
    tvpl_types = {
        'int8':   'Number',
        'uint8':  'Number',
        'int16':  'Number',
        'uint16': 'Number',
        'int32':  'Number',
        'uint32': 'Number',
        'int64':  'Number',
        'uint64': 'Number',
        'float':  'Number',
        'bool':   'Boolean',
        'char':   'String',
        'string': 'String'
    }

    tvpl_doc_types = {
        'en': {
            'int8':   ('Number', 'Numbers'),
            'uint8':  ('Number', 'Numbers'),
            'int16':  ('Number', 'Numbers'),
            'uint16': ('Number', 'Numbers'),
            'int32':  ('Number', 'Numbers'),
            'uint32': ('Number', 'Numbers'),
            'int64':  ('Number', 'Numbers'),
            'uint64': ('Number', 'Numbers'),
            'float':  ('Number', 'Numbers'),
            'bool':   ('Boolean', 'Booleans'),
            'char':   ('Letter', 'Letters'),
            'string': ('Text' 'Texts'),
        },
        'de': {
            'int8':   ('Zahl', 'Zahlen'),
            'uint8':  ('Zahl', 'Zahlen'),
            'int16':  ('Zahl', 'Zahlen'),
            'uint16': ('Zahl', 'Zahlen'),
            'int32':  ('Zahl', 'Zahlen'),
            'uint32': ('Zahl', 'Zahlen'),
            'int64':  ('Zahl', 'Zahlen'),
            'uint64': ('Zahl', 'Zahlen'),
            'float':  ('Zahl', 'Zahlen'),
            'bool':   ('Boolescher Wert', 'Booleschen Werten'),
            'char':   ('Buchstabe', 'Buchstaben'),
            'string': ('Text', 'Texten')
        }
    }

    def get_tvpl_type(self):
        return self.tvpl_types[self.get_type()]

    def get_tvpl_doc_type(self):
        t = common.select_lang(self.tvpl_doc_types)[self.get_type()]
        c = self.get_cardinality()
        list_of = {
            'en': 'List of ',
            'de': 'Liste von '
        }

        if c == 1 or self.get_type() == 'string':
            return t[0]

        return '{0}{1} {2}'.format(common.select_lang(list_of), c, t[0 if c == 1 else 1])

class TVPLGeneratorTrait:
    def get_doc_null_value_name(self):
        return 'null'

    def get_doc_formatted_param(self, element):
        return element.get_name().space
