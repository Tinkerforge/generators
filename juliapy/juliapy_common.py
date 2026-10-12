# -*- coding: utf-8 -*-

"""
JuliaPy Generator
Copyright (C) 2012-2013, 2017, 2019-2020 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011-2013 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>

juliapy_common.py: Common library for generation of JuliaPy bindings and documentation

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

from generators import common

class JuliaPyDevice(common.Device):
    def get_juliapy_import_name(self):
        return self.get_category().under + '_' + self.get_name().under

    def get_juliapy_struct_name(self):
        return self.get_category().camel + self.get_name().camel

class JuliaPyPacket(common.Packet):
    def get_juliapy_parameters(self, high_level=False):
        parameters = []

        for element in self.get_elements(direction='in', high_level=high_level):
            parameters.append(element.get_name().under)

        return ', '.join(parameters)

class JuliaPyElement(common.Element):
    juliapy_types = {
        'int8':   'Integer',
        'uint8':  'Integer',
        'int16':  'Integer',
        'uint16': 'Integer',
        'int32':  'Integer',
        'uint32': 'Integer',
        'int64':  'Integer',
        'uint64': 'Integer',
        'float':  'Real',
        'bool':   'Bool',
        'char':   'String', # This is a bad fix for tuple depacking in identities
        'string': 'String'
    }

    juliapy_struct_formats = {
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

    juliapy_default_item_values = {
        'int8':   '0',
        'uint8':  '0',
        'int16':  '0',
        'uint16': '0',
        'int32':  '0',
        'uint32': '0',
        'int64':  '0',
        'uint64': '0',
        'float':  '0.0',
        'bool':   'False',
        'char':   "'\\0'",
        'string': "nothing"
    }

    juliapy_parameter_coercions = {
        'int8':   ('Int8({0})',          'convert(Vector{{Int8}}, {0})'),
        'uint8':  ('UInt8({0})',         'convert(Vector{{UInt8}}, {0})'),
        'int16':  ('Int16({0})',         'convert(Vector{{Int16}}, {0})'),
        'uint16': ('UInt16({0})',        'convert(Vector{{UInt16}}, {0})'),
        'int32':  ('Int32({0})',         'convert(Vector{{Int32}}, {0})'),
        'uint32': ('UInt32({0})',        'convert(Vector{{UInt32}}, {0})'),
        'int64':  ('Int64({0})',         'convert(Vector{{Int64}}, {0})'),
        'uint64': ('UInt64({0})',        'convert(Vector{{UInt64}}, {0})'),
        'float':  ('Real({0})',          'convert(Vector{{Float}}, {0})'),
        'bool':   ('Bool({0})',          'convert(Vector{{Bool}}, {0})'),
        'char':   ('String({0})',        'convert(Vector{{String}}, {0})'),
        'string': ('String({0})',        'convert(Vector{{String}}, {0})')
    }

    def format_value(self, value):
        if isinstance(value, list):
            result = []

            for subvalue in value:
                result.append(self.format_value(subvalue))

            return '[{0}]'.format(', '.join(result))

        type_ = self.get_type()

        if type_ == 'float':
            return common.format_float(value)

        if type_ == 'bool':
            return str(bool(value))

        if type_ in ['char', 'string']:
            return '"{0}"'.format(value.replace('"', '\\"'))

        return str(value)

    def get_juliapy_name(self, index=None):
        return self.get_name(index=index).under

    def get_juliapy_type(self, cardinality=None):
        assert cardinality == None or (isinstance(cardinality, int) and cardinality > 0), cardinality

        juliapy_type = JuliaPyElement.juliapy_types[self.get_type()]

        if cardinality == None:
            cardinality = self.get_cardinality()

        if cardinality == 1 or self.get_type() == 'string':
            return juliapy_type

        return 'Vector{{{0}}}'.format(juliapy_type)

    def get_juliapy_struct_format(self):
        f = JuliaPyElement.juliapy_struct_formats[self.get_type()]
        cardinality = self.get_cardinality()

        if cardinality > 1:
            f = str(cardinality) + f

        return f

    def get_juliapy_default_item_value(self):
        value = JuliaPyElement.juliapy_default_item_values[self.get_type()]

        if value == None:
            common.GeneratorError('Invalid array item type: ' + self.get_type())

        return value

    def get_juliapy_parameter_coercion(self):
        coercion = JuliaPyElement.juliapy_parameter_coercions[self.get_type()]

        if self.get_cardinality() == 1:
            return coercion[0]
        else:
            return coercion[1]

class JuliaPyGeneratorTrait:
    def get_bindings_name(self):
        return 'juliapy'

    def get_bindings_display_name(self):
        return 'JuliaPy'

    def get_doc_null_value_name(self):
        return 'nothing'

    def get_doc_formatted_param(self, element):
        return element.get_name().under

    def generates_high_level_callbacks(self):
        return True
