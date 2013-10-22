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

def make_parameter_list(packet):
    param = ''
    for element in packet.get_elements():
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

class CPacket(common.Packet):
    def get_c_struct_list(self):
        struct_list = ''
        needs_i = False

        for element in self.get_elements('in'):
            sf = 'request'

            if element.get_type() == 'string':
                temp = '\n\tstrncpy({0}.{1}, {1}, {2});\n'
                struct_list += temp.format(sf, element.get_underscore_name(), element.get_cardinality())
            elif element.get_cardinality() > 1:
                if element.get_item_size() > 1:
                    needs_i = True
                    struct_list += '\n\tfor (i = 0; i < {3}; i++) {0}.{1}[i] = leconvert_{2}_to({1}[i]);' \
                                   .format(sf, element.get_underscore_name(), element.get_type(), element.get_cardinality())
                else:
                    temp = '\n\tmemcpy({0}.{1}, {1}, {2} * sizeof({3}));'
                    struct_list += temp.format(sf,
                                               element.get_underscore_name(),
                                               element.get_cardinality(),
                                               element.get_c_type(False))
            elif element.get_item_size() > 1:
                struct_list += '\n\t{0}.{1} = leconvert_{2}_to({1});'.format(sf, element.get_underscore_name(), element.get_type())
            else:
                struct_list += '\n\t{0}.{1} = {1};'.format(sf, element.get_underscore_name())

        return struct_list, needs_i

    def get_c_return_list(self):
        return_list = ''
        needs_i = False

        for element in self.get_elements('out'):
            sf = 'response'

            if element.get_type() == 'string':
                temp = '\tstrncpy(ret_{0}, {1}.{0}, {2});\n'
                return_list += temp.format(element.get_underscore_name(), sf, element.get_cardinality())
            elif element.get_cardinality() > 1:
                if element.get_item_size() > 1:
                    needs_i = True
                    return_list += '\tfor (i = 0; i < {3}; i++) ret_{0}[i] = leconvert_{2}_from({1}.{0}[i]);\n' \
                                   .format(element.get_underscore_name(), sf, element.get_type(), element.get_cardinality())
                else:
                    temp = '\tmemcpy(ret_{0}, {1}.{0}, {2} * sizeof({3}));\n'
                    return_list += temp.format(element.get_underscore_name(),
                                               sf,
                                               element.get_cardinality(),
                                               element.get_c_type(False))
            elif element.get_item_size() > 1:
                return_list += '\t*ret_{0} = leconvert_{2}_from({1}.{0});\n'.format(element.get_underscore_name(), sf, element.get_type())
            else:
                return_list += '\t*ret_{0} = {1}.{0};\n'.format(element.get_underscore_name(), sf)

        return return_list, needs_i

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
