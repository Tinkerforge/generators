#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C# Documentation Generator
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

csharp_common.py: Common Library for generation of C# bindings and documentation

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

def make_parameter_list(packet, useOutParams=True):
    param = []
    for element in packet.get_elements():
        if (not useOutParams) and element.get_direction() == 'out':
            continue
        
        out = ''
        if element.get_direction() == 'out' and packet.get_type() == 'function':
            out = 'out '

        csharp_type = get_csharp_type(element)
        name = element.get_headless_camel_case_name()
       
        param.append('{0}{1} {2}'.format(out, csharp_type, name))
    return ', '.join(param)

def make_method_signature(packet, printFullName=False, device=None, is_doc=False):
    sig_format = "public {4}{0} {1}{2}({3})"
    ret_count = len(packet.get_elements('out'))
    params = make_parameter_list(packet, ret_count > 1)
    return_type = 'void'
    if ret_count == 1:
        return_type = get_csharp_type(packet.get_elements('out')[0])
    classPrefix = ''
    if printFullName:
        classPrefix = device.get_category() + device.get_camel_case_name() + '::'
    override = ''
    if not is_doc and packet.has_prototype_in_device():
        override = 'override '

    return sig_format.format(return_type, classPrefix, packet.get_camel_case_name(), params, override)

def get_csharp_type(element):
    types = {
        'int8'   : 'short',
        'uint8'  : 'byte',
        'int16'  : 'short',
        'uint16' : 'int',
        'int32'  : 'int',
        'uint32' : 'long',
        'int64'  : 'long',
        'uint64' : 'long',
        'float'  : 'float',
        'bool'   : 'bool',
        'string' : 'string',
        'char'   : 'char'
    }

    csharp_type = types[element.get_type()]

    if element.get_cardinality() > 1 and element.get_type() != 'string':
        csharp_type += '[]'

    return csharp_type

def get_csharp_type_for_to_convert(element):
    types = {
        'int8'   : 'byte',
        'uint8'  : 'byte',
        'int16'  : 'short',
        'uint16' : 'short',
        'int32'  : 'int',
        'uint32' : 'int',
        'int64'  : 'long',
        'uint64' : 'long',
        'float'  : 'float',
        'bool'   : 'bool',
        'string' : 'string',
        'char'   : 'char'
    }

    csharp_type = types[element.get_type()]

    if element.get_cardinality() > 1 and element.get_type() != 'string':
        csharp_type += '[]'

    return csharp_type
