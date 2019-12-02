#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Delphi/Lazarus Generator
Copyright (C) 2012-2015, 2019 Matthias Bolte <matthias@tinkerforge.com>
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

class DelphiDevice(common.Device):
    def get_delphi_class_name(self):
        return 'T' + self.get_category().camel + self.get_name().camel

class DelphiPacket(common.Packet):
    def get_delphi_return_type(self, context, high_level=False):
        assert context in ['signature', 'doc']

        elements = self.get_elements(direction='out', high_level=high_level)

        if len(elements) != 1:
            return ''

        first = elements[0]
        delphi_type = first.get_delphi_type()

        if first.get_cardinality() < 0:
            if context == 'doc':
                final_type = 'array of {0}'.format(delphi_type[0])
            else:
                final_type = 'TArrayOf{0}'.format(delphi_type[1])
        elif first.get_cardinality() > 1 and first.get_type() != 'string':
            if context == 'doc':
                final_type = 'array [0..{0}] of {1}'.format(first.get_cardinality() - 1, delphi_type[0])
            else:
                final_type = 'TArray0To{0}Of{1}'.format(first.get_cardinality() - 1, delphi_type[1])
        else:
            final_type = delphi_type[0]

        return final_type

    def get_delphi_parameters(self, context, high_level=False):
        assert context in ['signature', 'variables', 'doc']

        param = []

        if len(self.get_elements(direction='out', high_level=high_level)) > 1 or self.get_type() == 'callback':
            for element in self.get_elements(high_level=high_level):
                delphi_type = element.get_delphi_type()

                if context.endswith('variables'):
                    modifier = ''
                else:
                    if element.get_direction() == 'in' or self.get_type() == 'callback':
                        modifier = 'const '
                    else:
                        modifier = 'out '

                if element.get_cardinality() != 1 and element.get_type() != 'string':
                    if context == 'signature':
                        if element.get_direction() == 'in' and element.get_level() != 'low':
                            final_type = 'array of {0}'.format(delphi_type[0])
                        elif element.get_cardinality() > 0:
                            final_type = 'TArray0To{0}Of{1}'.format(element.get_cardinality() - 1, delphi_type[1])

                            # special case for GetIdentity to avoid redefinition of TArray0To2OfUInt8 and signature mismatch
                            if self.get_name().camel == 'GetIdentity' and final_type == 'TArray0To2OfUInt8':
                                final_type = 'TVersionNumber'
                        else:
                            final_type = 'TArrayOf{0}'.format(delphi_type[1])
                    elif context == 'variables':
                        if element.get_cardinality() > 0:
                            final_type = 'TArray0To{0}Of{1}'.format(element.get_cardinality() - 1, delphi_type[1])
                        else:
                            final_type = 'TArrayOf{0}'.format(delphi_type[1])
                    else: # doc
                        if element.get_cardinality() > 0:
                            final_type = 'array [0..{0}] of {1}'.format(element.get_cardinality() - 1, delphi_type[0])
                        else:
                            final_type = 'array of {0}'.format(delphi_type[0])
                else:
                    final_type = delphi_type[0]

                param.append('{0}{1}: {2}'.format(modifier, element.get_name().headless, final_type))
        else:
            for element in self.get_elements(direction='in', high_level=high_level):
                delphi_type = element.get_delphi_type()

                if context.endswith('variables'):
                    modifier = ''
                else:
                    modifier = 'const '

                if element.get_cardinality() != 1 and element.get_type() != 'string':
                    if context == 'signature':
                        if element.get_level() != 'low':
                            final_type = 'array of {0}'.format(delphi_type[0])
                        elif element.get_cardinality() > 0:
                            final_type = 'TArray0To{0}Of{1}'.format(element.get_cardinality() - 1, delphi_type[1])
                        else:
                            final_type = 'TArrayOf{0}'.format(delphi_type[1])
                    elif context == 'variables':
                        if element.get_cardinality() > 0:
                            final_type = 'TArray0To{0}Of{1}'.format(element.get_cardinality() - 1, delphi_type[1])
                        else:
                            final_type = 'TArrayOf{0}'.format(delphi_type[1])
                    else: # doc
                        if element.get_cardinality() > 0:
                            final_type = 'array [0..{0}] of {1}'.format(element.get_cardinality() - 1, delphi_type[0])
                        else:
                            final_type = 'array of {0}'.format(delphi_type[0])
                else:
                    final_type = delphi_type[0]

                param.append('{0}{1}: {2}'.format(modifier, element.get_name().headless, final_type))

        return param

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

def get_delphi_type(type_, cardinality, context='default'):
    assert context in ['default', 'meta'], context

    delphi_type = delphi_types[type_]

    if context == 'default':
        return delphi_type

    if cardinality != 1 and type_ != 'string':
        if cardinality > 0:
            return 'array [0..{0}] of {1}'.format(cardinality - 1, delphi_type[0]) # FIXME: this is frond for fixed-length streams, should also be array of XYZ
        else:
            return 'array of {0}'.format(delphi_type[0])

    return delphi_type[0]

class DelphiElement(common.Element):
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
            return str(bool(value)).lower()

        if type_ in ['char', 'string']:
            return "'{0}'".format(value.replace("'", "''"))

        return str(value)

    def get_delphi_type(self, context='default', cardinality=None):
        assert cardinality == None or (isinstance(cardinality, int) and cardinality > 0), cardinality

        if cardinality == None:
            cardinality = self.get_cardinality()

        return get_delphi_type(self.get_type(), cardinality, context=context)

    def get_delphi_le_convert_type(self):
        return DelphiElement.delphi_le_convert_types[self.get_type()]

class DelphiGeneratorTrait:
    def get_doc_null_value_name(self):
        return 'nil'

    def get_doc_formatted_param(self, element):
        return element.get_name().headless
