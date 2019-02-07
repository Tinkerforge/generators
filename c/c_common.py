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
import math

sys.path.append(os.path.split(os.getcwd())[0])
import common

class CPacket(common.Packet):
    def get_c_parameters(self, high_level=False):
        parameters = []
        packet_type = self.get_type()

        for element in self.get_elements(high_level=high_level):
            element_type = element.get_c_type('signature')
            modifier = ''
            name = element.get_name().under
            direction = element.get_direction()
            role = element.get_role()
            array = ''

            if direction == 'out' and packet_type == 'function':
                modifier = '*'
                name = 'ret_{0}'.format(name)

            if role == 'stream_data':
                if direction == 'in' and packet_type == 'function':
                    if element_type == 'char':
                        element_type = 'const ' + element_type

                    modifier = '*'
                elif direction == 'out' and packet_type == 'callback':
                    modifier = '*'

            if role != 'stream_data' and element.get_cardinality() > 1:
                modifier = ''
                array = '[{0}]'.format(element.get_cardinality())

            parameters.append('{0} {1}{2}{3}'.format(element_type, modifier, name, array))

            length_elements = self.get_elements(role='stream_length')
            chunk_offset_elements = self.get_elements(role='stream_chunk_offset')

            if role == 'stream_data' and (direction == 'out' or len(length_elements) > 0):
                if direction == 'out' and packet_type == 'function':
                    modifier = '*'
                else:
                    modifier = ''

                if len(length_elements) > 0:
                    element_type = length_elements[0].get_c_type('signature')
                elif len(chunk_offset_elements) > 0:
                    element_type = chunk_offset_elements[0].get_c_type('signature')
                else:
                    raise common.GeneratorError('Malformed stream config')

                parameters.append('{0} {1}{2}_length'.format(element_type, modifier, name))

        return ', '.join(parameters)

    def get_c_arguments(self, context, high_level=False, single_chunk=False):
        assert context in ['default', 'callback_wrapper']

        arguments = []

        for element in self.get_elements(high_level=high_level):
            modifier = ''
            name = element.get_name().under
            direction = element.get_direction()
            role = element.get_role()

            if direction == 'out' and self.get_type() == 'function':
                if role in ['stream_length', 'stream_chunk_offset', 'stream_chunk_written']:
                    modifier = '&'
                elif role not in ['stream_chunk_data', 'stream_chunk_written']:
                    name = 'ret_{0}'.format(name)

            if context == 'callback_wrapper' and role == 'stream_data':
                if single_chunk:
                    arguments.append('{0}_data'.format(name))
                else:
                    arguments.append('({0} *)high_level_callback->data'.format(element.get_c_type('signature')))
            else:
                arguments.append('{0}{1}'.format(modifier, name))

            length_elements = self.get_elements(role='stream_length')
            chunk_offset_elements = self.get_elements(role='stream_chunk_offset')

            if role == 'stream_data' and (direction == 'out' or len(length_elements) > 0):
                if context == 'callback_wrapper' and not single_chunk:
                    arguments.append('high_level_callback->length')
                else:
                    arguments.append('{0}{1}_length'.format(modifier, name))

        return ', '.join(arguments)

class CElement(common.Element):
    def get_c_type(self, context):
        assert context in ['default', 'signature', 'struct']

        type_ = self.get_type()

        if type_ == 'string':
            if self.get_direction() == 'in' and context == 'signature':
                return 'const char'

            return 'char'

        if type_ in ['int8', 'int16', 'int32', 'int64', 'uint8', 'uint16', 'uint32', 'uint64']:
            return type_ + '_t'

        if type_ == 'bool' and context == 'struct':
            return 'uint8_t'

        return type_

    def get_c_array_length(self):
        if self.get_type() == 'bool':
            return int(math.ceil(self.get_cardinality() / 8.0))

        return self.get_cardinality()
