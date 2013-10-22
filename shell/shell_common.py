#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Shell Documentation Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011-2013 Olaf Lüke <olaf@tinkerforge.com>

shell_common.py: Common Library for generation of Shell bindings and documentation

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
    params = []
    for element in packet.get_elements('in'):
        params.append('<{0}>'.format(element.get_underscore_name().replace('_', '-')))
    return ' '.join(params)

class ShellDevice(common.Device):
    def get_shell_class_name(self):
        return self.get_camel_case_name() + self.get_category()

    def get_shell_device_name(self):
        return self.get_underscore_name().replace('_', '-') + '-' + self.get_category().lower()

class ShellElement(common.Element):
    shell_types = {
        'int8':   'int',
        'uint8':  'int',
        'int16':  'int',
        'uint16': 'int',
        'int32':  'int',
        'uint32': 'int',
        'int64':  'int',
        'uint64': 'int',
        'float':  'float',
        'bool':   'bool',
        'char':   'char',
        'string': 'string'
    }

    shell_struct_formats = {
        'int8':   'b',
        'uint8':  'B',
        'int16':  'h',
        'uint16': 'H',
        'int32':  'i',
        'uint32': 'I',
        'int64':  'q',
        'uint64': 'Q',
        'float':  'f',
        'bool':   '?',
        'char':   'c',
        'string': 's'
    }

    shell_type_converters = {
        'int8':   'convert_int',
        'uint8':  'convert_int',
        'int16':  'convert_int',
        'uint16': 'convert_int',
        'int32':  'convert_int',
        'uint32': 'convert_int',
        'int64':  'convert_int',
        'uint64': 'convert_int',
        'float':  'float',
        'bool':   'convert_bool',
        'char':   'check_char',
        'string': 'string'
    }

    def get_dash_name(self):
        return self.get_underscore_name().replace('_', '-')

    def get_shell_type(self):
        t = ShellElement.shell_types[self.get_type()]

        if self.get_cardinality() == 1 or t == 'string':
            return t

        return ','.join([t]*self.get_cardinality())

    def get_shell_struct_format(self):
        f = ShellElement.shell_struct_formats[self.get_type()]
        c = self.get_cardinality()

        if c > 1:
            f = str(c) + f

        return f

    def get_shell_help(self):
        symbols_doc = ''

        if self.has_constants():
            symbols = []

            for symbol in self.get_constants()[2]:
                symbols.append('{0}: {1}'.format(symbol[1].replace('_', '-'), symbol[2]))

            symbols_doc = ' (' + ', '.join(symbols) + ')'

        t = ShellElement.shell_types[self.get_type()]

        if self.get_cardinality() == 1 or t == 'string':
            help = "'{0}{1}'".format(t, symbols_doc)
        else:
            help = "get_array_type_name(ctx, '{0}', {1})".format(t, self.get_cardinality())

            if len(symbols_doc) > 0:
                help += "+ '{0}'".format(symbols_doc)

        return help

    def get_shell_type_converter(self):
        t = ShellElement.shell_type_converters[self.get_type()]

        if self.has_constants():
            symbols = {}

            for symbol in self.get_constants()[2]:
                symbols[symbol[1].replace('_', '-')] = symbol[2]

            if self.get_cardinality() > 1 and t != 'string':
                return 'create_array_converter(ctx, create_symbol_converter(ctx, {0}, {1}), {2})'.format(t, symbols, self.get_cardinality())
            elif t == 'string':
                return 'create_string_checker(create_symbol_converter(ctx, str, {0}), {1})'.format(symbols, self.get_cardinality())
            else:
                return 'create_symbol_converter(ctx, {0}, {1})'.format(t, symbols)
        else:
            if self.get_cardinality() > 1 and t != 'string':
                return 'create_array_converter(ctx, {0}, {1})'.format(t, self.get_cardinality())
            elif t == 'string':
                return 'create_string_checker(str, {0})'.format(self.get_cardinality())
            else:
                return t
