#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MQTT Bindings Generator
Copyright (C) 2019 Erik Fleckstein <erik@tinkerforge.com>

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
import os

sys.path.append(os.path.split(os.getcwd())[0])
import common
import mqtt_common

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
	def __init__(self, uid, ipcon, device_class, mqttc):
		MQTTCallbackDevice.__init__(self, uid, ipcon, device_class, mqttc)

{0}
"""
        response_expected = []
        mapping = {'always_true': 1, 'true': 2, 'false': 3}

        for packet in self.get_packets('function'):
            response_expected.append('re[{0}] = {1}'.format(packet.get_function_id(),
                                                            mapping[packet.get_response_expected()]))

        if len(response_expected) > 0:
            return template.format('\t\tre = self.response_expected\n\t\t' + '; '.join(response_expected))
        else:
            return template.format('')

    def get_mqtt_function_map(self):
        template = "\tfunctions = {{\n\t\t{entries}\n\t}}\n"
        entries = []
        for packet in self.get_packets('function'):
            entries.append("'{mqtt_name}': FunctionInfo({id}, {arg_names}, {arg_types}, [{arg_symbols}], '{payload_fmt}', {result_names}, [{result_symbols}], '{response_fmt}')".format(
                 mqtt_name=packet.get_mqtt_name(),
                 id=packet.get_function_id(),
                 arg_names=[elem.get_name().under for elem in packet.get_elements(direction='in')],
                 arg_types=[elem.get_mqtt_type() for elem in packet.get_elements(direction='in')],
                 arg_symbols=', '.join([elem.get_symbols() for elem in packet.get_elements(direction='in')]),
                 result_names=[elem.get_name().under for elem in packet.get_elements(direction='out')],
                 result_symbols=', '.join([elem.get_symbols() for elem in packet.get_elements(direction='out')]),
                 payload_fmt=packet.get_mqtt_format_list('in'),
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
                output_symbols = []
                high_level_roles_out = []
                low_level_roles_out = []

                for element in packet.get_elements(direction='out', high_level=True):
                    output_names.append('{0}'.format(element.get_name().dash))
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

                entries.append("'{mqtt_name}': HighLevelFunctionInfo({low_level_id}, '{direction}', {high_level_roles_in}, {high_level_roles_out}, {low_level_roles_in}, {low_level_roles_out}, {arg_names}, {arg_types}, {arg_symbols}, '{format_in}', {result_names}, {result_symbols}, '{format_out}',{chunk_padding}, {chunk_cardinality}, {chunk_max_offset},{short_write}, {single_read}, {fixed_length})".format(
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
                    result_symbols=output_symbols,
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
        entry_template = "'{mqtt_name}': CallbackInfo({id}, {names}, [{symbols}], '{fmt}', {hl_info})"
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
                                                symbols=', '.join([elem.get_symbols() for elem in packet.get_elements(direction='out', high_level=True)]),
                                                fmt=packet.get_mqtt_format_list('out'),
                                                hl_info=hl_info))
        return template.format(entries=",\n\t\t".join(entries))

    def get_mqtt_source(self):
        source  = self.get_mqtt_class()
        source += self.get_mqtt_function_map()
        source += self.get_mqtt_callback_map()
        source += self.get_mqtt_init_method()
        return source

class MQTTBindingsGenerator(mqtt_common.MQTTGeneratorTrait, common.BindingsGenerator):
    def __init__(self, *args, **kwargs):
        common.BindingsGenerator.__init__(self, *args, **kwargs)

        self.part_files = []
        self.devices = []
        self.device_mqtt_names = []
        self.device_display_names = []

    def get_bindings_name(self):
        return 'mqtt'

    def get_bindings_display_name(self):
        return 'MQTT'

    def get_device_class(self):
        return MQTTBindingsDevice

    def get_packet_class(self):
        return MQTTBindingsPacket

    def get_element_class(self):
        return mqtt_common.MQTTElement

    def generate(self, device):
        filename = '{0}.part'.format(device.get_mqtt_device_name())

        with open(os.path.join(self.get_bindings_dir(), filename), 'w') as f:
            f.write(device.get_mqtt_source())

        if device.is_released():
            self.devices.append("'{mqtt_dev_name}': {py_dev_name}".format(mqtt_dev_name=device.get_mqtt_device_name(), py_dev_name=device.get_python_class_name()))
            self.device_mqtt_names.append("{dev_id} : '{mqtt_dev_name}'".format(dev_id = device.get_device_identifier(), mqtt_dev_name=device.get_mqtt_device_name()))
            self.device_display_names.append("{dev_id} : '{display_name}'".format(dev_id = device.get_device_identifier(), display_name=device.get_long_display_name()))
            self.part_files.append(filename)

    def finish(self):
        common.BindingsGenerator.finish(self)

        root_dir = self.get_root_dir()
        bindings_dir = self.get_bindings_dir()
        version = self.get_changelog_version()
        mqtt = open(os.path.join(bindings_dir, 'tinkerforge_mqtt'), 'w')

        with open(os.path.join(root_dir, 'tinkerforge.header'), 'r') as f:
            header = f.read().replace('<<VERSION>>', '.'.join(version))

        with open(os.path.join(root_dir, 'tinkerforge.middle'), 'r') as f:
            middle = f.read().replace('<<VERSION>>', '.'.join(version))

        with open(os.path.join(root_dir, 'tinkerforge.footer'), 'r') as f:
            footer = f.read().replace('<<VERSION>>', '.'.join(version))

        mqtt.write(header)

        with open(os.path.join(root_dir, '..', 'python', 'ip_connection.py'), 'r') as f:
            ipcon = f.read()

        mqtt.write('\n\n\n' + ipcon + '\n\n\n')
        mqtt.write(middle + '\n\n\n')

        for filename in sorted(self.part_files):
            if filename.endswith('.part'):
                with open(os.path.join(bindings_dir, filename), 'r') as f:
                    mqtt.write(f.read())

        mqtt.write('\n\n\ndevices = {\n\t' + ',\n\t'.join(self.devices) + '\n}\n\n\n')
        mqtt.write('\n\n\nmqtt_names = {\n\t' + ',\n\t'.join(self.device_mqtt_names) + '\n}\n\n\n')
        mqtt.write('\n\n\ndisplay_names = {\n\t' + ',\n\t'.join(self.device_display_names) + '\n}\n\n\n')
        mqtt.write(footer)
        mqtt.close()

def generate(root_dir):
    common.generate(root_dir, 'en', MQTTBindingsGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
