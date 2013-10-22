#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C/C++ Bindings Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

c_common.py: Common Library for generation of C/C++ bindings and documentation

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

class CPacket(common.Packet):
    def get_c_parameter_list(self):
        param = ''

        for element in self.get_elements():
            c_type = element.get_c_type(True)
            name = element.get_underscore_name()
            pointer = ''
            arr = ''

            if element.get_direction() == 'out':
                pointer = '*'
                name = 'ret_{0}'.format(name)
            if element.get_cardinality() > 1:
                arr = '[{0}]'.format(element.get_cardinality())
                pointer = ''

            param += ', {0} {1}{2}{3}'.format(c_type, pointer, name, arr)

        return param

class CElement(common.Element):
    def get_c_type(self, is_in_signature):
        if self.get_type() == 'string':
            if self.get_direction() == 'in' and is_in_signature:
                return 'const char'
            else:
                return 'char'
        if self.get_type() in ('int8', 'int16', 'int32', 'int64', 'uint8', 'uint16', 'uint32', 'uint64'):
            return '{0}_t'.format(self.get_type())

        return self.get_type()
