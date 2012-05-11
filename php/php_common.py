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

def get_num_return(elements): 
    num = 0
    for element in elements:
        if element[3] == 'out':
            num += 1

    return num
    
def get_return_type(packet):
    if get_num_return(packet['elements']) == 0:
        return 'void'
    if get_num_return(packet['elements']) > 1:
        return 'array'
    
    for element in packet['elements']:
        if element[3] == 'out':
            if element[2] > 1:
                return 'array'
            else:
                return get_php_type(element[1])
