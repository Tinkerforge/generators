#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PHP Documentation Generator
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

php_common.py: Common Library for generation of PHP bindings and documentation

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

def get_php_type(typ):
    forms = {
        'int8' : 'int',
        'uint8' : 'int',
        'int16' : 'int',
        'uint16' : 'int',
        'int32' : 'int',
        'uint32' : 'int',
        'int64' : 'int',
        'uint64' : 'int',
        'float' : 'float',
        'bool' : 'bool',
        'string' : 'string',
        'char' : 'string'
    }

    if typ in forms:
        return forms[typ]

    return ''

def get_return_type(packet):
    if len(packet.get_elements('out')) == 0:
        return 'void'
    if len(packet.get_elements('out')) > 1:
        return 'array'

    for element in packet.get_elements('out'):
        if element.get_cardinality() > 1 and element.get_type() != 'string':
            return 'array'
        else:
            return get_php_type(element.get_type())

def make_parameter_list(packet, for_doc=False):
    param = []
    for element in packet.get_elements():
        if element.get_direction() == 'out' and packet.get_type() == 'function':
            continue
        name = element.get_underscore_name()
        if for_doc:
            php_type = get_php_type(element.get_type())
            if element.get_cardinality() > 1 and element.get_type() != 'string':
                php_type = 'array'

            param.append('{0} ${1}'.format(php_type, name))
        else:
            param.append('${0}'.format(name))
    return ', '.join(param)
