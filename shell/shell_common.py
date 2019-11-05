#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Shell Generator
Copyright (C) 2012-2013, 2019 Matthias Bolte <matthias@tinkerforge.com>
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

class ShellDevice(common.Device):
    def get_shell_class_name(self):
        if self.is_tng():
            return self.get_category().camel + self.get_name().camel

        return self.get_name().camel + self.get_category().camel

    def get_shell_device_name(self):
        if self.is_tng():
            return self.get_category().dash + '-' + self.get_name().dash

        return self.get_name().dash + '-' + self.get_category().dash

class ShellPacket(common.Packet):
    def get_shell_parameter_list(self, high_level=False):
        params = []

        for element in self.get_elements(direction='in', high_level=high_level):
            params.append('<{0}>'.format(element.get_name().dash))

        return ' '.join(params)

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
        'bool':   '!',
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
        'char':   'create_char_converter(ctx)',
        'string': 'string'
    }

    shell_default_items = {
        'int8':   "'0'",
        'uint8':  "'0'",
        'int16':  "'0'",
        'uint16': "'0'",
        'int32':  "'0'",
        'uint32': "'0'",
        'int64':  "'0'",
        'uint64': "'0'",
        'float':  "'0.0'",
        'bool':   "'false'",
        'char':   "'\\0'",
        'string': None
    }

    def format_value(self, value):
        type_ = self.get_type()

        if type_ == 'float':
            return common.format_float(value)

        if type_ == 'bool':
            return str(bool(value)).lower()

        if type_ == 'char':
            return '{0}'.format(value) # FIXME: how to escape a single quote?

        if type_ == 'string':
            return '"{0}"'.format(value) # FIXME: how to escape a double quote?

        return str(value)

    def get_shell_doc_type(self):
        shell_type = ShellElement.shell_types[self.get_type()].capitalize()
        cardinality = self.get_cardinality()

        if cardinality == 1 or self.get_type() == 'string':
            return shell_type

        return '{0} Array'.format(shell_type)

    def get_shell_struct_format(self):
        f = ShellElement.shell_struct_formats[self.get_type()]
        cardinality = self.get_cardinality()

        if cardinality > 1:
            f = str(cardinality) + f

        return f

    def get_shell_help(self):
        symbols_doc = ''
        constant_group = self.get_constant_group()

        if constant_group != None:
            symbols = []

            for constant in constant_group.get_constants():
                if constant_group.get_type() == 'bool':
                    value = str(constant.get_value()).lower()
                else:
                    value = constant.get_value()

                symbols.append('{0}-{1}: {2}'.format(constant_group.get_name().dash, constant.get_name().dash, value))

            symbols_doc = ' (' + ', '.join(symbols) + ')'

        t = ShellElement.shell_types[self.get_type()]

        if self.get_cardinality() == 1 or t == 'string':
            help_ = "'{0}{1}'".format(t, symbols_doc)
        else:
            help_ = "get_array_type_name(ctx, '{0}', {1})".format(t, self.get_cardinality())

            if len(symbols_doc) > 0:
                help_ += "+ '{0}'".format(symbols_doc)

        return help_

    def get_shell_type_converter(self):
        type_converter = ShellElement.shell_type_converters[self.get_type()]
        default_item = ShellElement.shell_default_items[self.get_type()]
        constant_group = self.get_constant_group()

        if constant_group != None:
            symbols = {}

            for constant in constant_group.get_constants():
                symbols['{0}-{1}'.format(constant_group.get_name().dash, constant.get_name().dash)] = constant.get_value()

            if self.get_cardinality() != 1 and type_converter != 'string':
                if self.get_cardinality() < 0:
                    default_item = None

                return 'create_array_converter(ctx, create_symbol_converter(ctx, {0}, {1}), {2}, {3})'.format(type_converter, symbols, default_item, self.get_cardinality())
            elif type_converter == 'string':
                return 'create_string_converter(ctx, create_symbol_converter(ctx, str, {0}), {1})'.format(symbols, self.get_cardinality())
            else:
                return 'create_symbol_converter(ctx, {0}, {1})'.format(type_converter, symbols)
        else:
            if self.get_cardinality() != 1 and type_converter != 'string':
                if self.get_cardinality() < 0:
                    default_item = None

                return 'create_array_converter(ctx, {0}, {1}, {2})'.format(type_converter, default_item, self.get_cardinality())
            elif type_converter == 'string':
                return 'create_string_converter(ctx, str, {0})'.format(self.get_cardinality())
            else:
                return type_converter

    def get_shell_default_item_value(self):
        value = ShellElement.shell_default_items[self.get_type()]

        if value == None:
            common.GeneratorError('Invalid array item type: ' + self.get_type())

        return value

class ShellGeneratorTrait:
    def get_doc_null_value_name(self):
        return 'None'

    def get_doc_formatted_param(self, element):
        return element.get_name().dash
