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

def to_camel_case(name):
    names = name.split('_')
    ret = names[0]
    for n in names[1:]:
        ret += n[0].upper() + n[1:]
    return ret

def make_parameter_list(packet, useOutParams=True):
    param = []
    for element in packet['elements']:
        if (not useOutParams) and element[3] == 'out':
            continue
        
        out = ''
        if element[3] == 'out' and packet['type'] == 'method':
            out = 'out '

        csharp_type = get_csharp_type(element)
        name = to_camel_case(element[0])
       
        param.append('{0}{1} {2}'.format(out, csharp_type, name))
    return ', '.join(param)

def make_method_signature(packet, printFullName=False, com=None):
    sig_format = "public {0} {1}{2}({3})"
    ret_count = count_return_values(packet['elements'])
    params = make_parameter_list(packet, ret_count > 1)
    return_type = 'void'
    if ret_count == 1:
        return_type = get_csharp_type(filter(lambda e: e[3] == 'out', packet['elements'])[0])
    classPrefix = ''
    if printFullName:
        classPrefix = com['type'] + com['name'][0] + '::'

    return sig_format.format(return_type, classPrefix, packet['name'][0], params)

def get_csharp_type(element):
    forms = {
        'int8' : 'sbyte',
        'uint8' : 'byte',
        'int16' : 'short',
        'uint16' : 'ushort',
        'int32' : 'int',
        'uint32' : 'uint',
        'int64' : 'long',
        'uint64' : 'ulong',
        'float' : 'float',
        'bool' : 'bool',
        'string' : 'string',
        'char' : 'char'
    }
    
    sharpType = ''
    if element[1] in forms:
        sharpType = forms[element[1]]
    else:
        return ''

    if element[2] > 1 and element[1] != 'string':
        sharpType += '[]'
    return sharpType

def count_return_values(elements):
    count = 0
    for element in elements:
        if element[3] == 'out':
            count += 1
    return count
