# -*- coding: utf-8 -*-

"""
C/C++ Generator
Copyright (C) 2012-2013, 2019-2020 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>

c_common.py: Common library for generation of C/C++ bindings and documentation

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

import math

from generators import common

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
                    modifier = '*'
                elif direction == 'out' and packet_type == 'callback':
                    modifier = '*'

            if role != 'stream_data' and element.get_cardinality() > 1:
                if element.get_type() == 'string' and direction == 'in':
                    modifier = '*'
                else:
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
    def format_value(self, value):
        if isinstance(value, list):
            result = []

            for subvalue in value:
                result.append(self.format_value(subvalue))

            return '{{{0}}}'.format(', '.join(result))

        type_ = self.get_type()

        if type_ == 'float':
            return common.format_float(value) + 'f'

        if type_ == 'bool':
            return str(bool(value)).lower()

        if type_ == 'char':
            return "'{0}'".format(value.replace("'", "\\'"))

        if type_ == 'string':
            return '"{0}"'.format(value.replace('"', '\\"'))

        return str(value)

    def get_c_name(self, index=None):
        name = self.get_name(index=index).under

        if self.get_direction() == 'out' and self.get_packet().get_type() == 'function' and index == None:
            name = 'ret_' + name

        return name

    def get_c_type(self, context, cardinality=None):
        assert context in ['default', 'signature', 'struct', 'meta']
        assert cardinality == None or (isinstance(cardinality, int) and cardinality > 0), cardinality

        type_ = self.get_type()

        if cardinality == None:
            cardinality = self.get_cardinality()

        if type_ == 'string':
            if self.get_direction() == 'in' and context in ['signature', 'meta']:
                type_ = 'const char'
            else:
                type_ = 'char'
        elif type_ == 'char':
            if self.get_direction() == 'in' and self.get_role() == 'stream_data' and context in ['signature', 'meta']:
                type_ = 'const char'
            else:
                type_ = 'char'
        elif type_ in ['int8', 'int16', 'int32', 'int64', 'uint8', 'uint16', 'uint32', 'uint64']:
            type_ = type_ + '_t'
        elif type_ == 'bool' and context == 'struct':
            type_ = 'uint8_t'

        if context == 'meta':
            if cardinality > 1:
                if type_ == 'string' and self.get_direction() == 'in':
                    type_ += ' *'
                else:
                    type_ += '[{}]'.format(cardinality)
            elif cardinality < 0:
                type_ += ' *'

        return type_

    def get_c_array_length(self):
        if self.get_type() == 'bool':
            return int(math.ceil(self.get_cardinality() / 8.0))

        return self.get_cardinality()

class CGeneratorTrait:
    def get_bindings_name(self):
        return 'c'

    def get_bindings_display_name(self):
        return 'C/C++'

    def get_doc_null_value_name(self):
        return 'NULL'

    def get_doc_formatted_param(self, element):
        return element.get_name().under

    def generates_high_level_callbacks(self):
        return True
