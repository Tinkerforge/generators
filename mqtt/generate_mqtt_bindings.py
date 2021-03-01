#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MQTT Bindings Generator
Copyright (C) 2019 Erik Fleckstein <erik@tinkerforge.com>
Copyright (C) 2020 Matthias Bolte <matthias@tinkerforge.com>

generate_mqtt_bindings.py: Generator for MQTT bindings

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
from generators.mqtt import mqtt_common

class MQTTBindingsPacket(mqtt_common.MQTTPacket):
    def get_mqtt_format_list(self, direction):
        formats = []

        for element in self.get_elements(direction=direction):
            formats.append(element.get_mqtt_struct_format())

        return ' '.join(formats)

class MQTTBindingsDevice(mqtt_common.MQTTDevice):
    def get_mqtt_class(self):
        template = """
class {0}(MQTTCallbackDevice):
"""

        return template.format(self.get_python_class_name())

    def get_mqtt_init_method(self):
        template = """
	def __init__(self, uid, ipcon, device_class_name, device_class, mqttc):
		MQTTCallbackDevice.__init__(self, uid, ipcon, {1}, device_names[{1}], device_class_name, device_class, mqttc)

{0}

		ipcon.add_device(self)
"""
        response_expected = []
        mapping = {'always_true': 1, 'true': 2, 'false': 3}

        for packet in self.get_packets('function'):
            response_expected.append('re[{0}] = {1}'.format(packet.get_function_id(),
                                                            mapping[packet.get_response_expected()]))

        if len(response_expected) > 0:
            return template.format('\t\tre = self.response_expected\n\t\t' + '; '.join(response_expected),
                                   self.get_device_identifier())
        else:
            return template.format('',
                                   self.get_device_identifier())

    def get_mqtt_function_map(self):
        template = "\tfunctions = {{\n\t\t{entries}\n\t}}\n"
        entries = []
        for packet in self.get_packets('function'):
            entries.append("'{mqtt_name}': FunctionInfo({id}, {arg_names}, {arg_types}, [{arg_symbols}], '{payload_fmt}', {result_names}, {result_types}, [{result_symbols}], {response_size}, '{response_fmt}')".format(
                 mqtt_name=packet.get_mqtt_name(),
                 id=packet.get_function_id(),
                 arg_names=[elem.get_name().under for elem in packet.get_elements(direction='in')],
                 arg_types=[elem.get_mqtt_type() for elem in packet.get_elements(direction='in')],
                 arg_symbols=', '.join([elem.get_symbols() for elem in packet.get_elements(direction='in')]),
                 result_names=[elem.get_name().under for elem in packet.get_elements(direction='out')],
                 result_types=[elem.get_mqtt_type() for elem in packet.get_elements(direction='out')],
                 result_symbols=', '.join([elem.get_symbols() for elem in packet.get_elements(direction='out')]),
                 payload_fmt=packet.get_mqtt_format_list('in'),
                 response_size=packet.get_response_size(),
                 response_fmt=packet.get_mqtt_format_list('out')))

            if packet.has_high_level():
                stream_in = packet.get_high_level('stream_in')
                stream_out = packet.get_high_level('stream_out')

                if stream_in == None and stream_out == None:
                    continue

                if stream_in != None:
                    direction = 'in'
                else:
                    direction = 'out'

                input_names = []
                input_types = []
                input_symbols = []
                high_level_roles_in = []
                low_level_roles_in = []

                for element in packet.get_elements(direction='in', high_level=True):
                    input_names.append('{0}'.format(element.get_name().under))
                    input_types.append(element.get_mqtt_type())
                    high_level_roles_in.append(element.get_role())
                    constant_group = element.get_constant_group()

                    symbols = {}

                    if constant_group != None:
                        for constant in constant_group.get_constants():
                            symbols[constant.get_value()] = constant.get_name().under

                    input_symbols.append(symbols)

                for element in packet.get_elements(direction='in'):
                    low_level_roles_in.append(element.get_role())

                output_names = []
                output_types = []
                output_symbols = []
                high_level_roles_out = []
                low_level_roles_out = []

                for element in packet.get_elements(direction='out', high_level=True):
                    output_names.append('{0}'.format(element.get_name().dash))
                    output_types.append(element.get_type())
                    high_level_roles_out.append(element.get_role())
                    constant_group = element.get_constant_group()

                    symbols = {}

                    if constant_group != None:
                        for constant in constant_group.get_constants():
                            symbols[constant.get_value()] =  constant.get_name().under

                    output_symbols.append(symbols)

                for element in packet.get_elements(direction='out'):
                    low_level_roles_out.append(element.get_role())

                if stream_in != None:
                    chunk_padding = "'0'"
                    chunk_cardinality = stream_in.get_chunk_data_element().get_cardinality()

                    if stream_in.get_fixed_length() != None:
                        chunk_max_offset = (1 << int(stream_in.get_chunk_offset_element().get_type().replace('uint', ''))) - 1
                    else:
                        chunk_max_offset = None

                    short_write = stream_in.has_short_write()
                    single_read = False
                    fixed_length = stream_in.get_fixed_length()
                else:
                    chunk_padding = None
                    chunk_cardinality = stream_out.get_chunk_data_element().get_cardinality()

                    if stream_out.get_fixed_length() != None:
                        chunk_max_offset = (1 << int(stream_out.get_chunk_offset_element().get_type().replace('uint', ''))) - 1
                    else:
                        chunk_max_offset = None

                    short_write = False
                    single_read = stream_out.has_single_chunk()
                    fixed_length = stream_out.get_fixed_length()

                entries.append("'{mqtt_name}': HighLevelFunctionInfo({low_level_id}, '{direction}', {high_level_roles_in}, {high_level_roles_out}, {low_level_roles_in}, {low_level_roles_out}, {arg_names}, {arg_types}, {arg_symbols}, '{format_in}', {result_names}, {result_types}, {result_symbols}, {response_size}, '{format_out}',{chunk_padding}, {chunk_cardinality}, {chunk_max_offset},{short_write}, {single_read}, {fixed_length})".format(
                    mqtt_name=packet.get_mqtt_name(skip=-2),
                    low_level_id=packet.get_function_id(),
                    direction=direction,
                    high_level_roles_in=high_level_roles_in,
                    high_level_roles_out=high_level_roles_out,
                    low_level_roles_in=low_level_roles_in,
                    low_level_roles_out=low_level_roles_out,
                    arg_names=input_names,
                    arg_types=input_types,
                    arg_symbols=input_symbols,
                    format_in=packet.get_mqtt_format_list('in'),
                    result_names=output_names,
                    result_types=output_types,
                    result_symbols=output_symbols,
                    response_size=packet.get_response_size(),
                    format_out=packet.get_mqtt_format_list('out'),
                    chunk_padding=chunk_padding,
                    chunk_cardinality=chunk_cardinality,
                    chunk_max_offset=chunk_max_offset,
                    short_write=short_write,
                    single_read=single_read,
                    fixed_length=fixed_length
                ))
        return template.format(entries = ",\n\t\t".join(entries))

    def get_mqtt_callback_map(self):
        template = "\tcallbacks = {{\n\t\t{entries}\n\t}}\n"
        entry_template = "'{mqtt_name}': CallbackInfo({id}, {names}, {types}, [{symbols}], ({response_size}, '{fmt}'), {hl_info})"
        hl_template = "[{2}, {{'fixed_length': {0}, 'single_chunk': {1}}}, None]"

        entries = []

        for packet in self.get_packets('callback'):
            hl_info="None"
            callback_id=packet.get_function_id()
            stream = packet.get_high_level('stream_*')
            skip=0
            if stream != None:
                roles = []

                for element in packet.get_elements(direction='out'):
                    roles.append(element.get_role())
                skip=-2
                hl_info = hl_template.format(stream.get_fixed_length(),
                                            stream.has_single_chunk(),
                                            repr(tuple(roles)))
            entries.append(entry_template.format(mqtt_name=packet.get_mqtt_name(skip),
                                                id=callback_id,
                                                names=[elem.get_name().under for elem in packet.get_elements(direction='out', high_level=True)],
                                                types=[elem.get_type() for elem in packet.get_elements(direction='out', high_level=True)],
                                                symbols=', '.join([elem.get_symbols() for elem in packet.get_elements(direction='out', high_level=True)]),
                                                fmt=packet.get_mqtt_format_list('out'),
                                                response_size=packet.get_response_size(),
                                                hl_info=hl_info))
        return template.format(entries=",\n\t\t".join(entries))

    def get_mqtt_source(self):
        source  = self.get_mqtt_class()
        source += self.get_mqtt_function_map()
        source += self.get_mqtt_callback_map()
        source += self.get_mqtt_init_method()
        return source

class MQTTBindingsGenerator(mqtt_common.MQTTGeneratorTrait, common.BindingsGenerator):
    def get_device_class(self):
        return MQTTBindingsDevice

    def get_packet_class(self):
        return MQTTBindingsPacket

    def get_element_class(self):
        return mqtt_common.MQTTElement

    def prepare(self):
        common.BindingsGenerator.prepare(self)

        self.part_files = []
        self.devices = []
        self.device_mqtt_names = []
        self.device_display_names = []

    def generate(self, device):
        filename = '{0}.part'.format(device.get_mqtt_device_name())

        with open(os.path.join(self.get_bindings_dir(), filename), 'w') as f:
            f.write(device.get_mqtt_source())

        if device.is_released():
            self.devices.append("'{mqtt_dev_name}': {py_dev_name}".format(mqtt_dev_name=device.get_mqtt_device_name(), py_dev_name=device.get_python_class_name()))
            self.device_mqtt_names.append((device.get_device_identifier(), device.get_mqtt_device_name()))
            self.device_display_names.append((device.get_device_identifier(), device.get_long_display_name()))
            self.part_files.append(filename)

    def finish(self):
        root_dir = self.get_root_dir()
        bindings_dir = self.get_bindings_dir()
        version = self.get_changelog_version()
        mqtt = open(os.path.join(bindings_dir, '{}_mqtt'.format(self.get_config_name().under)), 'w')

        with open(os.path.join(root_dir, 'tinkerforge.header'), 'r') as f:
            header = f.read().replace('<<VERSION>>', '.'.join(version))

        with open(os.path.join(root_dir, 'tinkerforge.middle'), 'r') as f:
            middle = f.read().replace('<<VERSION>>', '.'.join(version))

        with open(os.path.join(root_dir, 'tinkerforge.footer'), 'r') as f:
            footer = (f.read().replace('<<VERSION>>', '.'.join(version))
                              .replace('<<CONFIG_NAME_SPACE>>', self.get_config_name().space)
                              .replace('<<CONFIG_NAME_UNDER>>', self.get_config_name().under))

        mqtt.write(header)

        template = """

device_names = {{
    0: '',
	{entries}
}}

def get_device_display_name(device_identifier):
	device_display_name = device_names.get(device_identifier)

	if device_display_name == None:
		device_display_name = 'Unknown Device [{{0}}]'.format(device_identifier)

	return device_display_name
"""
        entries = []

        for device_identifier, device_name in sorted(self.device_display_names):
            entries.append("\t{0}: '{1}'".format(device_identifier, device_name))

        mqtt.write(template.format(entries=',\n\t'.join(entries)))

        with open(os.path.join(root_dir, '..', 'python', 'ip_connection.py'), 'r') as f:
            ipcon = f.read()

        mqtt.write('\n\n\n' + ipcon + '\n\n\n')
        mqtt.write(middle + '\n\n\n')

        for filename in sorted(self.part_files):
            if filename.endswith('.part'):
                with open(os.path.join(bindings_dir, filename), 'r') as f:
                    mqtt.write(f.read())

        mqtt.write('\n\n\ndevices = {\n\t' + ',\n\t'.join(sorted(self.devices)) + '\n}\n')

        mqtt_names = []

        for device_identifier, mqtt_name in sorted(self.device_mqtt_names):
            mqtt_names.append("\t{0}: '{1}'".format(device_identifier, mqtt_name))

        mqtt.write('\n\nmqtt_names = {\n' + ',\n'.join(mqtt_names) + '\n}\n')

        mqtt.write(footer)
        mqtt.close()

        os.system('chmod +x {0}/{1}_mqtt'.format(bindings_dir, self.get_config_name().under))

        common.BindingsGenerator.finish(self)

def generate(root_dir, language):
    common.generate(root_dir, language, MQTTBindingsGenerator)

if __name__ == '__main__':
    common.dockerize('mqtt', __file__)

    generate(os.getcwd(), 'en')
