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
    def get_c_parameters(self, signature=True, high_level=False, callback_wrapper=False):
        parameters = []

        for element in self.get_elements(high_level=high_level):
            c_type = element.get_c_type(True)
            modifier = ''
            name = element.get_underscore_name()
            array = ''

            if name == 'stream_chunk_written':
                if high_level:
                    c_type = 'uint16_t' # FIXME: uint16_t is not always the correct type
                    name = 'written'
                elif not signature:
                    modifier = '&'

            if element.get_direction() == 'out' and self.get_type() == 'function':
                if signature:
                    modifier = '*'
                    name = 'ret_{0}'.format(name)
                elif name in ['stream_total_length', 'stream_chunk_offset']:
                    modifier = '&'
                elif name not in ['stream_chunk_data', 'stream_chunk_written']:
                    name = 'ret_{0}'.format(name)

            if element.get_cardinality() < 0 and signature and \
               ((element.get_direction() == 'in' and self.get_type() == 'function') or \
                (element.get_direction() == 'out' and self.get_type() == 'callback')):
                modifier = '*'

            if element.get_cardinality() > 1:
                modifier = ''
                array = '[{0}]'.format(element.get_cardinality())

            if high_level and callback_wrapper and element.is_high_level() and element.get_cardinality() < 0:
                name = 'low_level_callback->data'

                parameters.append('({0} *){1}'.format(element.get_c_type(False), name))
            elif signature:
                parameters.append('{0} {1}{2}{3}'.format(c_type, modifier, name, array))
            else:
                parameters.append('{0}{1}'.format(modifier, name))

            if high_level and element.is_high_level() and element.get_cardinality() < 0:
                if signature:
                    if element.get_direction() == 'out' and self.get_type() == 'function':
                        modifier = '*'
                    else:
                        modifier = ''

                    parameters.append('uint16_t {0}{1}_length'.format(modifier, name)) # FIXME: uint16_t is not always the correct type
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
