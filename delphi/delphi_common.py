#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Delphi Documentation Generator
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
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

def get_delphi_type(typ):
    types = {
        'int8'   : ('shortint', 'Int8'),
        'uint8'  : ('byte',     'UInt8'),
        'int16'  : ('smallint', 'Int16'),
        'uint16' : ('word',     'UInt16'),
        'int32'  : ('longint',  'Int32'),
        'uint32' : ('longword', 'UInt32'),
        'int64'  : ('int64',    'Int64'),
        'uint64' : ('uint64',   'UInt64'),
        'float'  : ('single',   'Float'),
        'bool'   : ('boolean',  'Boolean'),
        'string' : ('string',   'String'),
        'char'   : ('char',     'Char')
    }

    if typ in types:
        return types[typ]

    return ''

def get_return_type(packet, for_doc):
    if len(packet.get_elements('out')) == 1:
        for element in packet.get_elements('out'):
            delphi_type = get_delphi_type(element[1])

            if element[2] > 1:
                if for_doc:
                    final_type = 'array [0..{0}] of {1}'.format(element[2] - 1, delphi_type[0])
                else:
                    final_type = 'TArray0To{0}Of{1}'.format(element[2] - 1, delphi_type[1])
            else:
                final_type = delphi_type[0]

            return final_type
    else:
        return ''

def make_parameter_list(packet, for_doc, with_modifiers=True):
    param = []
    if len(packet.get_elements('out')) > 1 or packet.get_type() == 'callback':
        for element in packet.get_elements():
            delphi_type = get_delphi_type(element[1])

            if with_modifiers:
                if element[3] == 'in' or packet.get_type() == 'callback':
                    modifier = 'const '
                else:
                    modifier = 'out '
            else:
                modifier = ''

            if element[1] != 'string' and element[2] > 1:
                if for_doc:
                    final_type = 'array [0..{0}] of {1}'.format(element[2] - 1, delphi_type[0])
                else:
                    final_type = 'TArray0To{0}Of{1}'.format(element[2] - 1, delphi_type[1])
            else:
                final_type = delphi_type[0]

            param.append('{0}{1}: {2}'.format(modifier,
                                              common.underscore_to_headless_camel_case(element[0]),
                                              final_type))
    else:
        for element in packet.get_elements('in'):
            delphi_type = get_delphi_type(element[1])

            if with_modifiers:
                modifier = 'const '
            else:
                modifier = ''

            if element[1] != 'string' and element[2] > 1:
                if for_doc:
                    final_type = 'array [0..{0}] of {1}'.format(element[2] - 1, delphi_type[0])
                else:
                    final_type = 'TArray0To{0}Of{1}'.format(element[2] - 1, delphi_type[1])
            else:
                final_type = delphi_type[0]

            param.append('{0}{1}: {2}'.format(modifier,
                                              common.underscore_to_headless_camel_case(element[0]),
                                              final_type))
    return '; '.join(param)
