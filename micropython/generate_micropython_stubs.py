#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MicroPython Stubs Generator
Created by René Rohner
Copyright (C) 2026 Tinkerforge GmbH

generate_micropython_stubs.py: Generator for MicroPython .pyi type stubs

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

if sys.hexversion < 0x3040000:
    print('Python >= 3.4 required')
    sys.exit(1)

import os
import importlib.util
import importlib.machinery
import shutil

def create_generators_module():
    generators_dir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]

    if sys.hexversion < 0x3050000:
        generators_module = importlib.machinery.SourceFileLoader('generators', os.path.join(generators_dir, '__init__.py')).load_module()
    else:
        generators_spec = importlib.util.spec_from_file_location('generators', os.path.join(generators_dir, '__init__.py'))
        generators_module = importlib.util.module_from_spec(generators_spec)

        generators_spec.loader.exec_module(generators_module)

    sys.modules['generators'] = generators_module

if 'generators' not in sys.modules:
    create_generators_module()

from generators import common
from generators.micropython import micropython_common

class MicroPythonStubsDevice(micropython_common.MicroPythonDevice):
    def get_stub_imports(self):
        imports = ['from typing import Optional, Callable, Sequence']
        imports.append('from collections import namedtuple')
        imports.append('from ip_connection import Device, IPConnection, Error')

        return '\n'.join(imports) + '\n'

    def get_stub_namedtuples(self):
        tuples = ''
        template = """{0} = namedtuple('{1}', [{2}])
"""

        for packet in self.get_packets('function'):
            if len(packet.get_elements(direction='out')) < 2:
                continue

            name = packet.get_name()

            if name.space.startswith('Get '):
                name_tup = name.camel[3:]
            else:
                name_tup = name.camel

            params = []

            for element in packet.get_elements(direction='out'):
                params.append("'{0}'".format(element.get_name().under))

            tuples += template.format(name.camel, name_tup, ", ".join(params))

        for packet in self.get_packets('function'):
            if not packet.has_high_level():
                continue

            if len(packet.get_elements(direction='out', high_level=True)) < 2:
                continue

            name = packet.get_name(skip=-2)

            if name.space.startswith('Get '):
                name_tup = name.camel[3:]
            else:
                name_tup = name.camel

            params = []

            for element in packet.get_elements(direction='out', high_level=True):
                params.append("'{0}'".format(element.get_name().under))

            tuples += template.format(name.camel, name_tup, ", ".join(params))

        return tuples

    def get_stub_class_header(self):
        template = """
class {0}(Device):
    r\"\"\"
    {1}
    \"\"\"

    DEVICE_IDENTIFIER: int
    DEVICE_DISPLAY_NAME: str
    DEVICE_URL_PART: str

"""

        return template.format(self.get_micropython_class_name(),
                               common.select_lang(self.get_description()))

    def get_stub_callback_id_definitions(self):
        lines = ''

        for packet in self.get_packets('callback'):
            lines += '    CALLBACK_{0}: int\n'.format(packet.get_name().upper)

        if self.get_long_display_name() == 'RS232 Bricklet':
            lines += '    CALLBACK_READ_CALLBACK: int\n'
            lines += '    CALLBACK_ERROR_CALLBACK: int\n'

        for packet in self.get_packets('callback'):
            if packet.has_high_level():
                lines += '    CALLBACK_{0}: int\n'.format(packet.get_name(skip=-2).upper)

        return lines

    def get_stub_function_id_definitions(self):
        lines = ''

        for packet in self.get_packets('function'):
            lines += '    FUNCTION_{0}: int\n'.format(packet.get_name().upper)

        return lines

    def get_stub_constants(self):
        lines = ''

        for constant_group in self.get_constant_groups():
            if constant_group.is_virtual():
                continue

            for constant in constant_group.get_constants():
                if constant_group.get_type() == 'bool':
                    lines += '    {0}_{1}: bool\n'.format(constant_group.get_name().upper, constant.get_name().upper)
                elif constant_group.get_type() in ['char', 'string']:
                    lines += '    {0}_{1}: str\n'.format(constant_group.get_name().upper, constant.get_name().upper)
                else:
                    lines += '    {0}_{1}: int\n'.format(constant_group.get_name().upper, constant.get_name().upper)

        return lines

    def get_stub_init_method(self):
        return """
    def __init__(self, uid: str, ipcon: IPConnection) -> None:
        r\"\"\"
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        \"\"\"
        ...

"""

    def get_stub_methods(self):
        methods = ''

        # normal and low-level
        for packet in self.get_packets('function'):
            methods += self._get_stub_method(packet)

        # high-level
        for packet in self.get_packets('function'):
            stream_in = packet.get_high_level('stream_in')
            stream_out = packet.get_high_level('stream_out')

            if stream_in is not None or stream_out is not None:
                methods += self._get_stub_method(packet, high_level=True)

        return methods

    def _get_stub_method(self, packet, high_level=False):
        if high_level:
            name = packet.get_name(skip=-2).under
        else:
            name = packet.get_name().under

        # Build typed parameter list
        params = self._get_typed_parameters(packet, high_level)
        param_str = ', '.join(['self'] + params)

        # Build return type
        ret_type = self._get_return_type(packet, high_level)

        # Get docstring
        doc = packet.get_stub_formatted_doc()

        method = '    def {0}({1}) -> {2}:\n'.format(name, param_str, ret_type)
        method += '        r"""\n'
        method += '        {0}\n'.format(doc)
        method += '        """\n'
        method += '        ...\n\n'

        return method

    def _get_typed_parameters(self, packet, high_level=False):
        params = []

        for element in packet.get_elements(direction='in', high_level=high_level):
            name = element.get_name().under
            type_str = self._get_element_type_hint(element, direction='in')
            params.append('{0}: {1}'.format(name, type_str))

        return params

    def _get_return_type(self, packet, high_level=False):
        out_elements = packet.get_elements(direction='out', high_level=high_level)

        if len(out_elements) == 0:
            return 'None'

        if len(out_elements) > 1:
            if high_level:
                name = packet.get_name(skip=-2)
            else:
                name = packet.get_name()
            return name.camel

        # Single return value
        element = out_elements[0]
        return self._get_element_type_hint(element, direction='out')

    def _get_element_type_hint(self, element, direction='in'):
        type_map = {
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
            'char':   'str',
            'string': 'str'
        }

        base_type = type_map[element.get_type()]
        cardinality = element.get_cardinality()

        if element.get_type() == 'string':
            return 'str'

        if cardinality == 1:
            return base_type

        if abs(cardinality) > 1:
            if direction == 'in':
                return 'Sequence[{0}]'.format(base_type)
            else:
                return 'tuple[{0}, ...]'.format(base_type)

        # variable length (negative cardinality from high-level)
        if direction == 'in':
            return 'Sequence[{0}]'.format(base_type)
        else:
            return 'list[{0}]'.format(base_type)

    def get_stub_register_callback_method(self):
        if len(self.get_packets('callback')) == 0:
            return ''

        return """    def register_callback(self, callback_id: int, function: Optional[Callable]) -> None:
        r\"\"\"
        Registers the given *function* with the given *callback_id*.
        \"\"\"
        ...

"""

    def get_stub_old_name(self):
        return '\n{0} = {1}\n'.format(self.get_name().camel, self.get_micropython_class_name())

    def get_stub_source(self):
        source  = '# -*- coding: utf-8 -*-\n'
        source += self.get_generator().get_header_comment('hash')
        source += '\n'
        source += self.get_stub_imports()
        source += '\n'
        source += self.get_stub_namedtuples()
        source += self.get_stub_class_header()
        source += self.get_stub_callback_id_definitions()
        source += self.get_stub_function_id_definitions()
        source += self.get_stub_constants()
        source += self.get_stub_init_method()
        source += self.get_stub_methods()
        source += self.get_stub_register_callback_method()

        if self.is_brick() or self.is_bricklet():
            source += self.get_stub_old_name()

        return common.strip_trailing_whitespace(source)

class MicroPythonStubsPacket(micropython_common.MicroPythonPacket):
    def get_stub_formatted_doc(self):
        text = common.select_lang(self.get_doc_text())

        def format_parameter(name):
            return '``{0}``'.format(name)

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)
        text += common.format_since_firmware(self.get_device(), self)

        return '\n        '.join(text.strip().split('\n'))

class MicroPythonStubsGenerator(micropython_common.MicroPythonGeneratorTrait, common.BindingsGenerator):
    recreate_bindings_dir = False

    def get_device_class(self):
        return MicroPythonStubsDevice

    def get_packet_class(self):
        return MicroPythonStubsPacket

    def get_element_class(self):
        return micropython_common.MicroPythonElement

    def prepare(self):
        self.stubs_dir = os.path.join(self.get_root_dir(), 'stubs')

        if os.path.exists(self.stubs_dir):
            shutil.rmtree(self.stubs_dir)

        os.makedirs(self.stubs_dir)

    def generate(self, device):
        filename = '{0}_{1}.pyi'.format(device.get_category().under, device.get_name().under)

        with open(os.path.join(self.stubs_dir, filename), 'w') as f:
            f.write(device.get_stub_source())

    def finish(self):
        # Copy the ip_connection stub
        ip_connection_stub = os.path.join(self.get_root_dir(), 'ip_connection.pyi')

        if os.path.exists(ip_connection_stub):
            shutil.copy(ip_connection_stub, self.stubs_dir)

def generate(root_dir, language, internal):
    common.generate(root_dir, language, internal, MicroPythonStubsGenerator)

if __name__ == '__main__':
    args = common.dockerize('micropython', __file__, add_internal_argument=True)

    generate(os.getcwd(), 'en', args.internal)
