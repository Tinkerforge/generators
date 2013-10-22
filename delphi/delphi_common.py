#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Delphi Documentation Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

delphi_common.py: Common Library for generation of Delphi bindings and documentation

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

def get_return_type(packet, for_doc):
    elements = packet.get_elements('out')

    if len(elements) != 1:
        return ''

    first = elements[0]
    delphi_type = first.get_delphi_type()

    if first.get_cardinality() > 1 and first.get_type() != 'string':
        if for_doc:
            final_type = 'array [0..{0}] of {1}'.format(first.get_cardinality() - 1, delphi_type[0])
        else:
            final_type = 'TArray0To{0}Of{1}'.format(first.get_cardinality() - 1, delphi_type[1])
    else:
        final_type = delphi_type[0]

    return final_type

def make_parameter_list(packet, for_doc, with_modifiers=True):
    param = []
    if len(packet.get_elements('out')) > 1 or packet.get_type() == 'callback':
        for element in packet.get_elements():
            delphi_type = element.get_delphi_type()

            if with_modifiers:
                if element.get_direction() == 'in' or packet.get_type() == 'callback':
                    modifier = 'const '
                else:
                    modifier = 'out '
            else:
                modifier = ''

            if element.get_cardinality() > 1 and element.get_type() != 'string':
                if for_doc:
                    final_type = 'array [0..{0}] of {1}'.format(element.get_cardinality() - 1, delphi_type[0])
                else:
                    final_type = 'TArray0To{0}Of{1}'.format(element.get_cardinality() - 1, delphi_type[1])

                    # special case for GetIdentity to avoid redefinition of TArray0To2OfUInt8 and signature mismatch
                    if packet.get_camel_case_name() == 'GetIdentity' and final_type == 'TArray0To2OfUInt8':
                        final_type = 'TVersionNumber'
            else:
                final_type = delphi_type[0]

            param.append('{0}{1}: {2}'.format(modifier,
                                              element.get_headless_camel_case_name(),
                                              final_type))
    else:
        for element in packet.get_elements('in'):
            delphi_type = element.get_delphi_type()

            if with_modifiers:
                modifier = 'const '
            else:
                modifier = ''

            if element.get_cardinality() > 1 and element.get_type() != 'string':
                if for_doc:
                    final_type = 'array [0..{0}] of {1}'.format(element.get_cardinality() - 1, delphi_type[0])
                else:
                    final_type = 'TArray0To{0}Of{1}'.format(element.get_cardinality() - 1, delphi_type[1])
            else:
                final_type = delphi_type[0]

            param.append('{0}{1}: {2}'.format(modifier,
                                              element.get_headless_camel_case_name(),
                                              final_type))
    return '; '.join(param)

class DelphiDevice(common.Device):
    def get_delphi_class_name(self):
        return 'T' + self.get_category() + self.get_camel_case_name()

class DelphiElement(common.Element):
    delphi_types = {
        'int8':   ('shortint', 'Int8'),
        'uint8':  ('byte',     'UInt8'),
        'int16':  ('smallint', 'Int16'),
        'uint16': ('word',     'UInt16'),
        'int32':  ('longint',  'Int32'),
        'uint32': ('longword', 'UInt32'),
        'int64':  ('int64',    'Int64'),
        'uint64': ('uint64',   'UInt64'),
        'float':  ('single',   'Float'),
        'bool':   ('boolean',  'Boolean'),
        'char':   ('char',     'Char'),
        'string': ('string',   'String')
    }

    delphi_le_convert_types = {
        'int8':   'Int8',
        'uint8':  'UInt8',
        'int16':  'Int16',
        'uint16': 'UInt16',
        'int32':  'Int32',
        'uint32': 'UInt32',
        'int64':  'Int64',
        'uint64': 'UInt64',
        'float':  'Float',
        'bool':   'Boolean',
        'char':   'Char',
        'string': 'String'
    }

    def get_delphi_type(self):
        return DelphiElement.delphi_types[self.get_type()]

    def get_delphi_le_convert_type(self):
        return DelphiElement.delphi_le_convert_types[self.get_type()]
