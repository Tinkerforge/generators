#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Saleae High Level Analyzer Generator
Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>

generate_saleae_bindings.py: Generator for Saleae bindings

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
from collections import OrderedDict

sys.path.append(os.path.split(os.getcwd())[0])
sys.path.append(os.path.join(os.path.split(os.getcwd())[0], 'python'))
import common
from python.generate_python_bindings import PythonBindingsPacket
from python.python_common import PythonElement
import saleae_common

class SaleaeBindingsDevice(common.Device):
    def get_info_dict(self):
        packets = [packet.get_info_dict() for packet in self.get_packets()]

        enumerate_packet = """253: {
            'function_id': 253,
            'name': 'Enumerate',
            'elements': [
                {
                    'name': 'Uid',
                    'type': 'string',
                    'cardinality': '8',
                    'direction': 'out'
                },
                {
                    'name': 'Connected Uid',
                    'type': 'string',
                    'cardinality': '8',
                    'direction': 'out'
                },
                {
                    'name': 'Position',
                    'type': 'char',
                    'cardinality': '1',
                    'direction': 'out'
                },
                {
                    'name': 'Hardware Version',
                    'type': 'uint8',
                    'cardinality': '3',
                    'direction': 'out'
                },
                {
                    'name': 'Firmware Version',
                    'type': 'uint8',
                    'cardinality': '3',
                    'direction': 'out'
                },
                {
                    'name': 'Device Identifier',
                    'type': 'uint16',
                    'cardinality': '1',
                    'direction': 'out'
                },
                {
                    'name': 'Enumeration Type',
                    'type': 'uint8',
                    'cardinality': '1',
                    'direction': 'out'
                }
            ],
            'in_struct_format': '',
            'out_struct_format': '8s 8s c 3B 3B H B'
        }"""

        packets += [enumerate_packet]

        return """{dev_id}: {{
    'device_identifier': {dev_id},
    'name': '{long_display_name}',
    'packets': {{
        {packets}
    }}
}}""".format(dev_id=self.get_device_identifier(),
             long_display_name=self.get_long_display_name(),
             packets=',\n        '.join(packets))

class SaleaeBindingsPacket(PythonBindingsPacket):
    def get_info_dict(self):
        elements = [element.get_info_dict() for element in self.get_elements()]

        return """{fid}: {{
            'function_id': {fid},
            'name': '{name}',
            'elements': [
                {elements}
            ],
            'in_struct_format': '{in_struct_format}',
            'out_struct_format': '{out_struct_format}',
        }}""".format(fid=self.get_function_id(),
                     name=self.get_name().space,
                     elements=',\n                '.join(elements),
                     in_struct_format=self.get_python_format_list('in'),
                     out_struct_format=self.get_python_format_list('out'))

class SaleaeBindingsElement(PythonElement):
    def get_info_dict(self):
        return """{{
                    'name': '{name}',
                    'type': '{type}',
                    'cardinality': '{cardinality}',
                    'direction': '{direction}'
                }}""".format(name=self.get_name().space,
                             type=self.get_type(),
                             cardinality=self.get_cardinality(),
                             direction=self.get_direction())


class SaleaeBindingsGenerator(saleae_common.SaleaeGeneratorTrait, common.BindingsGenerator):
    def get_device_class(self):
        return SaleaeBindingsDevice

    def get_packet_class(self):
        return SaleaeBindingsPacket

    def get_element_class(self):
        return SaleaeBindingsElement

    def generate(self, device):
        if not device.has_comcu():
            return
        filename = '{0}_{1}.txt'.format(device.get_category().under, device.get_name().under)

        with open(os.path.join(self.get_bindings_dir(), filename), 'w') as f:
            f.write(device.get_info_dict())

        if device.is_released():
            self.released_files.append(filename)

    def finish(self):
        infos = []
        for filename in self.released_files:
            with open(os.path.join(self.get_bindings_dir(), filename), 'r') as f:
                infos.append(f.read())

        with open(os.path.join(self.get_root_dir(), '..', 'python', 'ip_connection.py'), 'r') as f:
            content = f.read()
        unpack_payload_impl = content.split('# UNPACK_PAYLOAD_CUT_HERE\n')[1]

        common.specialize_template(
            os.path.join(self.get_root_dir(), 'HighLevelAnalyzer.py.template'),
            os.path.join(self.get_bindings_dir(),  'HighLevelAnalyzer.py'), {
            '{{infos}}': ',\n'.join(infos),
            '{{unpack_payload}}': unpack_payload_impl,
            '{{header}}': self.get_header_comment('hash')
        })

        common.specialize_template(
            os.path.join(self.get_root_dir(), 'extension.json.template'),
            os.path.join(self.get_bindings_dir(),  'extension.json'), {
            '{{version}}': '{}.{}.{}'.format(*self.get_changelog_version())
        })


def generate(root_dir):
    common.generate(root_dir, 'en', SaleaeBindingsGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
