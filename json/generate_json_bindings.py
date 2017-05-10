#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JSON Bindings Generator
Copyright (C) 2017 Matthias Bolte <matthias@tinkerforge.com>

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
import os
import json

sys.path.append(os.path.split(os.getcwd())[0])
import common

class JSONBindingsDevice(common.Device):
    def get_json_source(self):
        members = {}

        members['author'] = self.get_author()
        members['api_version'] = self.get_api_version()
        members['category'] = self.get_category()
        members['device_identifier'] = self.get_device_identifier()
        members['name'] = self.get_name()
        members['display_name'] = {'short': self.get_short_display_name(), 'long': self.get_long_display_name()}
        members['manufacturer'] = self.get_manufacturer()
        members['description'] = self.get_description()
        members['released'] = self.is_released()
        members['documented'] = self.is_documented()
        members['doc'] = self.get_doc()
        members['packets'] = []
        #members['examples'] = [] # FIXME

        for packet in self.get_packets():
            members['packets'].append(packet.get_json_members())

        return json.dumps(members, indent=2)

class JSONBindingsPacket(common.Packet):
    def get_json_members(self):
        members = {}

        members['type'] = self.get_type()
        members['name'] = self.get_name()
        members['function_id'] = self.get_function_id()
        members['since_firmware'] = self.get_since_firmware()
        members['doc'] = {'type': self.get_doc_type(), 'text': self.get_doc_text()}
        members['elements'] = []

        for element in self.get_elements():
            members['elements'].append(element.get_json_members())

        return members

class JSONBindingsElement(common.Element):
    def get_json_members(self):
        members = {}

        members['name'] = self.get_name()
        members['type'] = self.get_type()
        members['cardinality'] = self.get_cardinality()
        members['direction'] = self.get_direction()

        constant_group = self.get_constant_group()

        if constant_group != None:
            members['constant_group'] = {}

            members['constant_group']['name'] = constant_group.get_name()
            members['constant_group']['constants'] = []

            for constant in constant_group.get_constants():
                members['constant_group']['constants'].append({
                'name': constant.get_name(),
                'value': constant.get_value()
                })

        else:
            members['constant_group'] = None

        return members

class JSONBindingsGenerator(common.BindingsGenerator):
    def get_bindings_name(self):
        return 'json'

    def get_bindings_display_name(self):
        return 'JSON'

    def get_device_class(self):
        return JSONBindingsDevice

    def get_packet_class(self):
        return JSONBindingsPacket

    def get_element_class(self):
        return JSONBindingsElement

    def generate(self, device):
        filename = '{0}_{1}.json'.format(device.get_underscore_category(), device.get_underscore_name())

        with open(os.path.join(self.get_bindings_root_directory(), 'bindings', filename), 'wb') as f:
            f.write(device.get_json_source())

        if device.is_released():
            self.released_files.append(filename)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', JSONBindingsGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
