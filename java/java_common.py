#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Java Documentation Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011-2013 Olaf Lüke <olaf@tinkerforge.com>

java_common.py: Common Library for generation of Java bindings and documentation

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

def get_java_type(typ):
    forms = {
        'int8' : 'byte',
        'uint8' : 'short',
        'int16' : 'short',
        'uint16' : 'int',
        'int32' : 'int',
        'uint32' : 'long',
        'int64' : 'long',
        'uint64' : 'long',
        'float' : 'float',
        'bool' : 'boolean',
        'string' : 'String',
        'char' : 'char'
    }

    if typ in forms:
        return forms[typ]

    return ''

def get_object_name(packet):
    name = packet.get_camel_case_name()
    if name.startswith('Get'):
        name = name[3:]

    return name

def get_return_type(packet, for_doc=False):
    elements = packet.get_elements('out')

    if len(elements) == 0:
        return 'void'

    if len(elements) > 1:
        if for_doc:
            return packet.get_device().get_category() + packet.get_device().get_camel_case_name() + '.' + get_object_name(packet)
        else:
            return get_object_name(packet)

    return_type = get_java_type(elements[0][1])

    if elements[0][2] > 1 and elements[0][1] != 'string':
        return_type += '[]'

    return return_type

def make_parameter_list(packet, just_types=False):
    param = []
    for element in packet.get_elements():
        if element[3] == 'out' and packet.get_type() == 'function':
            continue
        java_type = get_java_type(element[1])
        name = common.underscore_to_headless_camel_case(element[0])
        arr = ''
        if element[2] > 1 and element[1] != 'string':
            arr = '[]'

        if just_types:
            param.append('{0}{1}'.format(java_type, arr))
        else:
            param.append('{0}{1} {2}'.format(java_type, arr, name))
    return ', '.join(param)
