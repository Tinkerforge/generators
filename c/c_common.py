#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C/C++ Generator
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
    def get_c_parameters(self, signature=True, high_level=False, callback_wrapper=False, single_chunk=False):
        parameters = []

        for element in self.get_elements(high_level=high_level):
            c_type = element.get_c_type(True)
            modifier = ''
            name = element.get_name().under
            role = element.get_role()
            array = ''

            if element.get_direction() == 'out' and self.get_type() == 'function':
                if signature:
                    modifier = '*'
                    name = 'ret_{0}'.format(name)
                elif role in ['stream_length', 'stream_chunk_offset', 'stream_chunk_written']:
                    modifier = '&'
                elif role not in ['stream_chunk_data', 'stream_chunk_written']:
                    name = 'ret_{0}'.format(name)

            if element.get_role() == 'stream_data' and signature:
                if element.get_direction() == 'in' and self.get_type() == 'function':
                    c_type = 'const ' + c_type
                    modifier = '*'
                elif element.get_direction() == 'out' and self.get_type() == 'callback':
                    modifier = '*'

            if element.get_role() != 'stream_data' and element.get_cardinality() > 1:
                modifier = ''
                array = '[{0}]'.format(element.get_cardinality())

            if high_level and callback_wrapper and element.get_level() == 'high' and \
               element.get_role() == 'stream_data':
                if single_chunk:
                    parameters.append('{0}_data'.format(name))
                else:
                    parameters.append('({0} *)high_level_callback->data'.format(c_type))
            elif signature:
                parameters.append('{0} {1}{2}{3}'.format(c_type, modifier, name, array))
            else:
                parameters.append('{0}{1}'.format(modifier, name))

            length_elements = self.get_elements(role='stream_length')
            chunk_offset_elements = self.get_elements(role='stream_chunk_offset')

            if high_level and \
               element.get_level() == 'high' and \
               element.get_role() == 'stream_data' and \
               (element.get_direction() == 'out' or \
                len(length_elements) > 0):
                if signature:
                    if element.get_direction() == 'out' and self.get_type() == 'function':
                        modifier = '*'
                    else:
                        modifier = ''

                    if len(length_elements) > 0:
                        c_type = length_elements[0].get_c_type(True)
                    elif len(chunk_offset_elements) > 0:
                        c_type = chunk_offset_elements[0].get_c_type(True)
                    else:
                        raise common.GeneratorError('Malformed stream config')

                    parameters.append('{0} {1}{2}_length'.format(c_type, modifier, name))
                elif callback_wrapper and not single_chunk:
                    parameters.append('high_level_callback->length')
                else:
                    parameters.append('{0}{1}_length'.format(modifier, name))

        return ', '.join(parameters)

class CElement(common.Element):
    def get_c_type(self, signature, struct=False):
        if self.get_type() == 'string':
            if self.get_direction() == 'in' and signature:
                return 'const char'
            else:
                return 'char'
        elif self.get_type() in ('int8', 'int16', 'int32', 'int64', 'uint8', 'uint16', 'uint32', 'uint64'):
            return '{0}_t'.format(self.get_type())
        elif self.get_type() == 'bool' and struct:
            return 'uint8_t'
        else:
            return self.get_type()
