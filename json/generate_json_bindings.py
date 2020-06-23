#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JSON Bindings Generator
Copyright (C) 2017-2020 Matthias Bolte <matthias@tinkerforge.com>

generate_json_bindings.py: Generator for JSON bindings

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

if sys.hexversion < 0x3050000:
    print('Python >= 3.5 required')
    sys.exit(1)

import os
import json
from collections import OrderedDict
import importlib.util

def create_generators_module():
    generators_dir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
    generators_spec = importlib.util.spec_from_file_location('generators', os.path.join(generators_dir, '__init__.py'))
    generators_module = importlib.util.module_from_spec(generators_spec)

    generators_spec.loader.exec_module(generators_module)

    sys.modules['generators'] = generators_module

if 'generators' not in sys.modules:
    create_generators_module()

from generators import common

class JSONBindingsDevice(common.Device):
    def get_json_source(self):
        members = OrderedDict()

        members['author'] = self.get_author()
        members['api_version'] = self.get_api_version()
        members['category'] = self.get_category().space
        members['device_identifier'] = self.get_device_identifier()
        members['name'] = self.get_name().space
        members['display_name'] = OrderedDict()
        members['display_name']['short'] = self.get_short_display_name()
        members['display_name']['long'] = self.get_long_display_name()
        members['manufacturer'] = self.get_manufacturer()
        members['description'] = OrderedDict()
        members['description']['en'] = self.get_description()['en']
        members['description']['de'] = self.get_description()['de']
        members['released'] = self.is_released()
        members['documented'] = self.is_documented()
        members['doc'] = OrderedDict()
        members['doc']['en'] = self.get_doc()['en']
        members['doc']['de'] = self.get_doc()['de']
        members['packets'] = []
        #members['examples'] = [] # FIXME

        for packet in self.get_packets():
            members['packets'].append(packet.get_json_members())

            if packet.has_high_level():
                members['packets'].append(packet.get_json_members(high_level=True))

        return json.dumps(members, indent=2)

class JSONBindingsPacket(common.Packet):
    def get_json_members(self, high_level=False):
        members = OrderedDict()

        if high_level:
            members['level'] = 'high'
        elif self.has_high_level():
            members['level'] = 'low'
        else:
            members['level'] = 'normal'

        members['type'] = self.get_type()
        members['name'] = self.get_name(skip=-2 if high_level else 0).space
        members['function_id'] = self.get_function_id()
        members['since_firmware'] = self.get_since_firmware()
        members['doc'] = OrderedDict()
        members['doc']['type'] = self.get_doc_type()
        members['doc']['text'] = OrderedDict()
        members['doc']['text']['en'] = self.get_doc_text()['en']
        members['doc']['text']['de'] = self.get_doc_text()['de']
        members['elements'] = []

        for element in self.get_elements(high_level=high_level):
            members['elements'].append(element.get_json_members())

        return members

class JSONBindingsElement(common.Element):
    def get_json_members(self):
        members = OrderedDict()

        members['level'] = self.get_level()
        members['name'] = self.get_name().space
        members['type'] = self.get_type()
        members['cardinality'] = self.get_cardinality()
        members['direction'] = self.get_direction()
        members['role'] = self.get_role()
        members['extra'] = []

        for index in self.get_indices():
            extra = OrderedDict()
            extra['index'] = index
            extra['name'] = self.get_name(index=index).space

            scale = self.get_scale(index=index)

            if scale in [None, 'dynamic']:
                extra['scale'] = scale
            else:
                extra['scale'] = OrderedDict()
                extra['scale']['numerator'] = scale[0]
                extra['scale']['denominator'] = scale[1]

            unit = self.get_unit(index=index)

            if unit in [None, 'dynamic']:
                extra['unit'] = unit
            else:
                extra['unit'] = OrderedDict()
                extra['unit']['title'] = OrderedDict()
                extra['unit']['title']['en'] = unit.get_title(language='en')
                extra['unit']['title']['de'] = unit.get_title(language='de')
                extra['unit']['symbol'] = unit.get_symbol()
                extra['unit']['usage'] = OrderedDict()
                extra['unit']['usage']['en'] = unit.get_usage(language='en')
                extra['unit']['usage']['de'] = unit.get_usage(language='de')
                extra['unit']['sequence'] = OrderedDict()
                extra['unit']['sequence']['en'] = unit.get_sequence(language='en')
                extra['unit']['sequence']['de'] = unit.get_sequence(language='de')

            range_ = self.get_range(index=index)

            if not isinstance(range_, list):
                extra['range'] = range_
            else:
                extra['range'] = []

                for subrange in range_:
                    extra['range'].append(OrderedDict([('minimum', subrange[0]), ('maximum', subrange[1])]))

            extra['default'] = self.get_default(index=index)

            constant_group = self.get_constant_group(index=index)

            if constant_group == None:
                extra['constant_group'] = None
            else:
                extra['constant_group'] = OrderedDict()
                extra['constant_group']['name'] = constant_group.get_name().space
                extra['constant_group']['constants'] = []

                for constant in constant_group.get_constants():
                    extra['constant_group']['constants'].append(OrderedDict([
                        ('name', constant.get_name().space),
                        ('value', constant.get_value())
                    ]))

            members['extra'].append(extra)

        return members

class JSONGeneratorTrait:
    def get_bindings_name(self):
        return 'json'

    def get_bindings_display_name(self):
        return 'JSON'

    def get_doc_null_value_name(self):
        return 'null'

    def get_doc_formatted_param(self, element):
        return element.get_name().space

class JSONBindingsGenerator(JSONGeneratorTrait, common.BindingsGenerator):
    def get_device_class(self):
        return JSONBindingsDevice

    def get_packet_class(self):
        return JSONBindingsPacket

    def get_element_class(self):
        return JSONBindingsElement

    def generate(self, device):
        filename = '{0}_{1}.json'.format(device.get_category().under, device.get_name().under)

        with open(os.path.join(self.get_bindings_dir(), filename), 'w') as f:
            f.write(device.get_json_source())

        if device.is_released():
            self.released_files.append(filename)

def generate(root_dir):
    common.generate(root_dir, 'en', JSONBindingsGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
