#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python Bindings Generator
Copyright (C) 2012-2015, 2017 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_python_bindings.py: Generator for Python bindings

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
import python_common

class PythonBindingsDevice(python_common.PythonDevice):
    def get_python_import(self):
        template = """# -*- coding: utf-8 -*-
{0}{1}
from collections import namedtuple

try:
    from .ip_connection import Device, IPConnection, Error, create_chunk_data
except ValueError:
    from ip_connection import Device, IPConnection, Error, create_chunk_data

"""

        if not self.is_released():
            released = '\n#### __DEVICE_IS_NOT_RELEASED__ ####\n'
        else:
            released = ''

        return template.format(self.get_generator().get_header_comment('hash'),
                               released)

    def get_python_namedtuples(self):
        tuples = ''
        template = """{0} = namedtuple('{1}', [{2}])
"""

        for packet in self.get_packets('function'):
            if len(packet.get_elements(direction='out')) < 2:
                continue

            name = packet.get_camel_case_name()
            name_tup = name

            if name_tup.startswith('Get'):
                name_tup = name_tup[3:]

            params = []

            for element in packet.get_elements(direction='out'):
                params.append("'{0}'".format(element.get_underscore_name()))

            tuples += template.format(name, name_tup, ", ".join(params))

        for packet in self.get_packets('function'):
            if not packet.has_high_level():
                continue

            if len(packet.get_elements(direction='out', high_level=True)) < 2:
                continue

            name = packet.get_camel_case_name(skip=-2)
            name_tup = name

            if name_tup.startswith('Get'):
                name_tup = name_tup[3:]

            params = []

            for element in packet.get_elements(direction='out', high_level=True):
                params.append("'{0}'".format(element.get_underscore_name()))

            tuples += template.format(name, name_tup, ", ".join(params))

        return tuples

    def get_python_class(self):
        template = """
class {0}(Device):
    \"\"\"
    {1}
    \"\"\"

    DEVICE_IDENTIFIER = {2}
    DEVICE_DISPLAY_NAME = '{3}'

"""

        return template.format(self.get_python_class_name(),
                               common.select_lang(self.get_description()),
                               self.get_device_identifier(),
                               self.get_long_display_name())

    def get_python_callback_id_definitions(self):
        callback_ids = ''
        template = '    CALLBACK_{0} = {1}\n'

        for packet in self.get_packets('callback'):
            callback_ids += template.format(packet.get_upper_case_name(), packet.get_function_id())

        if self.get_long_display_name() == 'RS232 Bricklet':
            callback_ids += '    CALLBACK_READ_CALLBACK = 8 # for backward compatibility\n'
            callback_ids += '    CALLBACK_ERROR_CALLBACK = 9 # for backward compatibility\n'

        callback_ids += '\n'

        for packet in self.get_packets('callback'):
            if packet.has_high_level():
                callback_ids += template.format(packet.get_upper_case_name(skip=-2), -packet.get_function_id())

        return callback_ids

    def get_python_function_id_definitions(self):
        function_ids = '\n'
        template = '    FUNCTION_{0} = {1}\n'

        for packet in self.get_packets('function'):
            function_ids += template.format(packet.get_upper_case_name(), packet.get_function_id())

        return function_ids

    def get_python_constants(self):
        constant_format = '    {constant_group_upper_case_name}_{constant_upper_case_name} = {constant_value}\n'

        return '\n' + self.get_formatted_constants(constant_format)

    def get_python_init_method(self):
        template = """
    def __init__(self, uid, ipcon):
        \"\"\"
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        \"\"\"
        Device.__init__(self, uid, ipcon)

        self.api_version = ({0}, {1}, {2})

"""
        response_expected = ''

        for packet in self.get_packets('function'):
            if len(packet.get_elements(direction='out')) > 0:
                flag = 'RESPONSE_EXPECTED_ALWAYS_TRUE'
            elif packet.get_doc_type() in ['ccf', 'llf']:
                flag = 'RESPONSE_EXPECTED_TRUE'
            else:
                flag = 'RESPONSE_EXPECTED_FALSE'

            response_expected += '        self.response_expected[{0}.FUNCTION_{1}] = {0}.{2}\n' \
                                 .format(self.get_python_class_name(), packet.get_upper_case_name(), flag)

        return template.format(*self.get_api_version()) + common.wrap_non_empty('', response_expected, '\n')

    def get_python_callback_formats(self):
        callback_formats = ''
        template = "        self.callback_formats[{0}.CALLBACK_{1}] = '{2}'\n"

        for packet in self.get_packets('callback'):
            callback_formats += template.format(self.get_python_class_name(),
                                                packet.get_upper_case_name(),
                                                packet.get_python_format_list('out'))

        return callback_formats + '\n'

    def get_python_high_level_callbacks(self):
        high_level_callbacks = ''
        template = "        self.high_level_callbacks[{0}.CALLBACK_{1}] = [{4}, {{'fixed_length': {2}, 'single_chunk': {3}}}, None]\n"

        for packet in self.get_packets('callback'):
            stream = packet.get_high_level('stream_*')

            if stream != None:
                roles = []

                for element in packet.get_elements(direction='out'):
                    roles.append(element.get_role())

                high_level_callbacks += template.format(self.get_python_class_name(),
                                                        packet.get_upper_case_name(skip=-2),
                                                        stream.get_fixed_length(),
                                                        stream.has_single_chunk(),
                                                        repr(tuple(roles)))

        return high_level_callbacks

    def get_python_methods(self):
        m_tup = """
    def {0}(self{7}{4}):
        \"\"\"
        {9}
        \"\"\"
        return {1}(*self.ipcon.send_request(self, {2}.FUNCTION_{3}, ({4}{8}), '{5}', '{6}'))
"""
        m_ret = """
    def {0}(self{6}{3}):
        \"\"\"
        {8}
        \"\"\"
        return self.ipcon.send_request(self, {1}.FUNCTION_{2}, ({3}{7}), '{4}', '{5}')
"""
        m_nor = """
    def {0}(self{6}{3}):
        \"\"\"
        {8}
        \"\"\"
        self.ipcon.send_request(self, {1}.FUNCTION_{2}, ({3}{7}), '{4}', '{5}')
"""
        methods = ''
        cls = self.get_python_class_name()

        # normal and low-level
        for packet in self.get_packets('function'):
            nb = packet.get_camel_case_name()
            ns = packet.get_underscore_name()
            nh = ns.upper()
            par = packet.get_python_parameters()
            doc = packet.get_python_formatted_doc()
            cp = ''
            ct = ''

            if par != '':
                cp = ', '
                if not ',' in par:
                    ct = ','

            in_f = packet.get_python_format_list('in')
            out_f = packet.get_python_format_list('out')

            elements = len(packet.get_elements(direction='out'))

            if elements > 1:
                methods += m_tup.format(ns, nb, cls, nh, par, in_f, out_f, cp, ct, doc)
            elif elements == 1:
                methods += m_ret.format(ns, cls, nh, par, in_f, out_f, cp, ct, doc)
            else:
                methods += m_nor.format(ns, cls, nh, par, in_f, out_f, cp, ct, doc)

        # high-level
        template_stream_in = """
    def {underscore_name}(self{high_level_parameters}):
        \"\"\"
        {doc}
        \"\"\"
        {stream_underscore_name} = list({stream_underscore_name}) # convert potential tuple to list
        {stream_underscore_name}_length = len({stream_underscore_name})
        {stream_underscore_name}_chunk_offset = 0

        if {stream_underscore_name}_length == 0:
            {stream_underscore_name}_chunk_data = [{chunk_padding}] * {chunk_cardinality}
            ret = self.{underscore_name}_low_level({parameters})
        else:
            with self.stream_lock:
                while {stream_underscore_name}_chunk_offset < {stream_underscore_name}_length:
                    {stream_underscore_name}_chunk_data = create_chunk_data({stream_underscore_name}, {stream_underscore_name}_chunk_offset, {chunk_cardinality}, {chunk_padding})
                    ret = self.{underscore_name}_low_level({parameters})
                    {stream_underscore_name}_chunk_offset += {chunk_cardinality}
{result}
"""
        template_stream_in_fixed_length = """
    def {underscore_name}(self{high_level_parameters}):
        \"\"\"
        {doc}
        \"\"\"
        {stream_underscore_name} = list({stream_underscore_name}) # convert potential tuple to list
        {stream_underscore_name}_length = {fixed_length}
        {stream_underscore_name}_chunk_offset = 0

        if len({stream_underscore_name}) != {stream_underscore_name}_length:
            raise Error(Error.INVALID_PARAMETER, '{stream_name} has to be {{0}} items long'.format({stream_underscore_name}_length))

        with self.stream_lock:
            while {stream_underscore_name}_chunk_offset < {stream_underscore_name}_length:
                {stream_underscore_name}_chunk_data = create_chunk_data({stream_underscore_name}, {stream_underscore_name}_chunk_offset, {chunk_cardinality}, {chunk_padding})
                ret = self.{underscore_name}_low_level({parameters})
                {stream_underscore_name}_chunk_offset += {chunk_cardinality}
{result}
"""
        template_stream_in_result = """
        return ret"""
        template_stream_in_namedtuple_result = """
        return {result_camel_case_name}(*ret)"""
        template_stream_in_short_write = """
    def {underscore_name}(self{high_level_parameters}):
        \"\"\"
        {doc}
        \"\"\"
        {stream_underscore_name} = list({stream_underscore_name}) # convert potential tuple to list
        {stream_underscore_name}_length = len({stream_underscore_name})
        {stream_underscore_name}_chunk_offset = 0

        if {stream_underscore_name}_length == 0:
            {stream_underscore_name}_chunk_data = [{chunk_padding}] * {chunk_cardinality}
            ret = self.{underscore_name}_low_level({parameters})
            {chunk_written_0}
        else:
            {stream_underscore_name}_written = 0

            with self.stream_lock:
                while {stream_underscore_name}_chunk_offset < {stream_underscore_name}_length:
                    {stream_underscore_name}_chunk_data = create_chunk_data({stream_underscore_name}, {stream_underscore_name}_chunk_offset, {chunk_cardinality}, {chunk_padding})
                    ret = self.{underscore_name}_low_level({parameters})
                    {chunk_written_n}

                    if {chunk_written_test} < {chunk_cardinality}:
                        break # either last chunk or short write

                    {stream_underscore_name}_chunk_offset += {chunk_cardinality}
{result}
"""
        template_stream_in_short_write_chunk_written = ['{stream_underscore_name}_written = ret',
                                                        '{stream_underscore_name}_written += ret',
                                                        'ret']
        template_stream_in_short_write_namedtuple_chunk_written = ['{stream_underscore_name}_written = ret.{stream_underscore_name}_chunk_written',
                                                                   '{stream_underscore_name}_written += ret.{stream_underscore_name}_chunk_written',
                                                                   'ret.{stream_underscore_name}_chunk_written']
        template_stream_in_short_write_result = """
        return {stream_underscore_name}_written"""
        template_stream_in_short_write_namedtuple_result = """
        return {result_camel_case_name}({result_fields})"""
        template_stream_in_single_chunk = """
    def {underscore_name}(self{high_level_parameters}):
        \"\"\"
        {doc}
        \"\"\"
        {stream_underscore_name} = list({stream_underscore_name}) # convert potential tuple to list, also makes a copy so we can potentially extend it
        {stream_underscore_name}_length = len({stream_underscore_name})
        {stream_underscore_name}_data = {stream_underscore_name}

        if {stream_underscore_name}_length > {chunk_cardinality}:
            raise Error(Error.INVALID_PARAMETER, '{stream_name} can be at most {chunk_cardinality} items long')

        if {stream_underscore_name}_length < {chunk_cardinality}:
            {stream_underscore_name}_data += [{chunk_padding}] * ({chunk_cardinality} - {stream_underscore_name}_length)
{result}
"""
        template_stream_in_single_chunk_result = """
        return self.{underscore_name}_low_level({parameters})"""
        template_stream_in_single_chunk_namedtuple_result = """
        return {result_camel_case_name}(*self.{underscore_name}_low_level({parameters}))"""
        template_stream_out = """
    def {underscore_name}(self{high_level_parameters}):
        \"\"\"
        {doc}
        \"\"\"{fixed_length}
        with self.stream_lock:
            ret = self.{underscore_name}_low_level({parameters}){dynamic_length_3}
            {chunk_offset_check}{stream_underscore_name}_out_of_sync = ret.{stream_underscore_name}_chunk_offset != 0
            {chunk_offset_check_indent}{stream_underscore_name}_data = ret.{stream_underscore_name}_chunk_data

            while not {stream_underscore_name}_out_of_sync and len({stream_underscore_name}_data) < {stream_underscore_name}_length:
                ret = self.{underscore_name}_low_level({parameters}){dynamic_length_4}
                {stream_underscore_name}_out_of_sync = ret.{stream_underscore_name}_chunk_offset != len({stream_underscore_name}_data)
                {stream_underscore_name}_data += ret.{stream_underscore_name}_chunk_data

            if {stream_underscore_name}_out_of_sync: # discard remaining stream to bring it back in-sync
                while ret.{stream_underscore_name}_chunk_offset + {chunk_cardinality} < {stream_underscore_name}_length:
                    ret = self.{underscore_name}_low_level({parameters}){dynamic_length_5}

                raise Error(Error.STREAM_OUT_OF_SYNC, '{stream_name} stream is out-of-sync')
{result}
"""
        template_stream_out_fixed_length = """
        {stream_underscore_name}_length = {fixed_length}
"""
        template_stream_out_dynamic_length = """
{{indent}}{stream_underscore_name}_length = ret.{stream_underscore_name}_length"""
        template_stream_out_chunk_offset_check = """
            if ret.{stream_underscore_name}_chunk_offset == (1 << {shift_size}) - 1: # maximum chunk offset -> stream has no data
                {stream_underscore_name}_length = 0
                {stream_underscore_name}_out_of_sync = False
                {stream_underscore_name}_data = ()
            else:
                """
        template_stream_out_single_chunk = """
    def {underscore_name}(self{high_level_parameters}):
        \"\"\"
        {doc}
        \"\"\"
        ret = self.{underscore_name}_low_level({parameters})
{result}
"""
        template_stream_out_result = """
        return {stream_underscore_name}_data[:{stream_underscore_name}_length]"""
        template_stream_out_single_chunk_result = """
        return ret.{stream_underscore_name}_data[:ret.{stream_underscore_name}_length]"""
        template_stream_out_namedtuple_result = """
        return {result_camel_case_name}({result_fields})"""

        for packet in self.get_packets('function'):
            stream_in = packet.get_high_level('stream_in')
            stream_out = packet.get_high_level('stream_out')

            if stream_in != None:
                if stream_in.get_fixed_length() != None:
                    template = template_stream_in_fixed_length
                elif stream_in.has_short_write() and stream_in.has_single_chunk():
                    # the single chunk template also covers short writes
                    template = template_stream_in_single_chunk
                elif stream_in.has_short_write():
                    template = template_stream_in_short_write
                elif stream_in.has_single_chunk():
                    template = template_stream_in_single_chunk
                else:
                    template = template_stream_in

                if stream_in.has_short_write():
                    if len(packet.get_elements(direction='out')) < 2:
                        chunk_written_0 = template_stream_in_short_write_chunk_written[0].format(stream_underscore_name=stream_in.get_underscore_name())
                        chunk_written_n = template_stream_in_short_write_chunk_written[1].format(stream_underscore_name=stream_in.get_underscore_name())
                        chunk_written_test = template_stream_in_short_write_chunk_written[2].format(stream_underscore_name=stream_in.get_underscore_name())
                    else:
                        chunk_written_0 = template_stream_in_short_write_namedtuple_chunk_written[0].format(stream_underscore_name=stream_in.get_underscore_name())
                        chunk_written_n = template_stream_in_short_write_namedtuple_chunk_written[1].format(stream_underscore_name=stream_in.get_underscore_name())
                        chunk_written_test = template_stream_in_short_write_namedtuple_chunk_written[2].format(stream_underscore_name=stream_in.get_underscore_name())

                    if len(packet.get_elements(direction='out', high_level=True)) < 2:
                        if stream_in.has_single_chunk():
                            result = template_stream_in_single_chunk_result.format(underscore_name=packet.get_underscore_name(skip=-2),
                                                                                   parameters=packet.get_python_parameters())
                        else:
                            result = template_stream_in_short_write_result.format(stream_underscore_name=stream_in.get_underscore_name())
                    else:
                        if stream_in.has_single_chunk():
                            result = template_stream_in_single_chunk_namedtuple_result.format(underscore_name=packet.get_underscore_name(skip=-2),
                                                                                              parameters=packet.get_python_parameters(),
                                                                                              result_camel_case_name=packet.get_camel_case_name(skip=-2))
                        else:
                            fields = []

                            for element in packet.get_elements(direction='out', high_level=True):
                                if element.get_role() == 'stream_written':
                                    fields.append('{0}_written'.format(stream_in.get_underscore_name()))
                                else:
                                    fields.append('ret.{0}'.format(element.get_underscore_name()))

                            result = template_stream_in_short_write_namedtuple_result.format(result_camel_case_name=packet.get_camel_case_name(skip=-2),
                                                                                             result_fields=', '.join(fields))
                else:
                    chunk_written_0 = ''
                    chunk_written_n = ''
                    chunk_written_test = ''

                    if len(packet.get_elements(direction='out', high_level=True)) < 2:
                        if stream_in.has_single_chunk():
                            result = template_stream_in_single_chunk_result.format(underscore_name=packet.get_underscore_name(skip=-2),
                                                                                   parameters=packet.get_python_parameters())
                        else:
                            result = template_stream_in_result
                    else:
                        if stream_in.has_single_chunk():
                            result = template_stream_in_single_chunk_namedtuple_result.format(underscore_name=packet.get_underscore_name(skip=-2),
                                                                                              parameters=packet.get_python_parameters(),
                                                                                              result_camel_case_name=packet.get_camel_case_name(skip=-2))
                        else:
                            result = template_stream_in_namedtuple_result.format(result_camel_case_name=packet.get_camel_case_name(skip=-2))

                methods += template.format(doc=packet.get_python_formatted_doc(),
                                           underscore_name=packet.get_underscore_name(skip=-2),
                                           parameters=packet.get_python_parameters(),
                                           high_level_parameters=common.wrap_non_empty(', ', packet.get_python_parameters(high_level=True), ''),
                                           stream_name=stream_in.get_name(),
                                           stream_underscore_name=stream_in.get_underscore_name(),
                                           fixed_length=stream_in.get_fixed_length(),
                                           chunk_cardinality=stream_in.get_chunk_data_element().get_cardinality(),
                                           chunk_padding=stream_in.get_chunk_data_element().get_python_default_item_value(),
                                           chunk_written_0=chunk_written_0,
                                           chunk_written_n=chunk_written_n,
                                           chunk_written_test=chunk_written_test,
                                           result=result)
            elif stream_out != None:
                if stream_out.get_fixed_length() != None:
                    fixed_length = template_stream_out_fixed_length.format(stream_underscore_name=stream_out.get_underscore_name(),
                                                                           fixed_length=stream_out.get_fixed_length())
                    dynamic_length = ''
                    shift_size = int(stream_out.get_chunk_offset_element().get_type().replace('uint', ''))
                    chunk_offset_check = template_stream_out_chunk_offset_check.format(stream_underscore_name=stream_out.get_underscore_name(),
                                                                                       shift_size=shift_size)
                    chunk_offset_check_indent = '    '
                else:
                    fixed_length = ''
                    dynamic_length = template_stream_out_dynamic_length.format(stream_underscore_name=stream_out.get_underscore_name())
                    chunk_offset_check = ''
                    chunk_offset_check_indent = ''

                if len(packet.get_elements(direction='out', high_level=True)) < 2:
                    if stream_out.has_single_chunk():
                        result = template_stream_out_single_chunk_result.format(stream_underscore_name=stream_out.get_underscore_name())
                    else:
                        result = template_stream_out_result.format(stream_underscore_name=stream_out.get_underscore_name())
                else:
                    fields = []

                    for element in packet.get_elements(direction='out', high_level=True):
                        if element.get_role() == 'stream_data':
                            if stream_out.has_single_chunk():
                                fields.append('ret.{0}_data[:ret.{0}_length]'.format(stream_out.get_underscore_name()))
                            else:
                                fields.append('{0}_data[:{0}_length]'.format(stream_out.get_underscore_name()))
                        else:
                            fields.append('ret.{0}'.format(element.get_underscore_name()))

                    result = template_stream_out_namedtuple_result.format(result_camel_case_name=packet.get_camel_case_name(skip=-2),
                                                                          result_fields=', '.join(fields))

                if stream_out.has_single_chunk():
                    template = template_stream_out_single_chunk
                else:
                    template = template_stream_out

                methods += template.format(doc=packet.get_python_formatted_doc(),
                                           underscore_name=packet.get_underscore_name(skip=-2),
                                           parameters=packet.get_python_parameters(),
                                           high_level_parameters=common.wrap_non_empty(', ', packet.get_python_parameters(high_level=True), ''),
                                           stream_name=stream_out.get_name(),
                                           stream_underscore_name=stream_out.get_underscore_name(),
                                           fixed_length=fixed_length,
                                           dynamic_length_3=dynamic_length.format(indent='    ' * 3),
                                           dynamic_length_4=dynamic_length.format(indent='    ' * 4),
                                           dynamic_length_5=dynamic_length.format(indent='    ' * 5),
                                           chunk_offset_check=chunk_offset_check,
                                           chunk_offset_check_indent=chunk_offset_check_indent,
                                           chunk_cardinality=stream_out.get_chunk_data_element().get_cardinality(),
                                           result=result)

        return methods

    def get_python_register_callback_method(self):
        if len(self.get_packets('callback')) == 0:
            return ''

        return """
    def register_callback(self, id_, callback):
        \"\"\"
        Registers a callback with ID *id* to the function *callback*.
        \"\"\"
        if callback is None:
            self.registered_callbacks.pop(id_, None)
        else:
            self.registered_callbacks[id_] = callback
"""

    def get_python_old_name(self):
        template = """
{0} = {1} # for backward compatibility
"""

        return template.format(self.get_camel_case_name(), self.get_python_class_name())

    def get_python_source(self):
        source  = self.get_python_import()
        source += self.get_python_namedtuples()
        source += self.get_python_class()
        source += self.get_python_callback_id_definitions()
        source += self.get_python_function_id_definitions()
        source += self.get_python_constants()
        source += self.get_python_init_method()
        source += self.get_python_callback_formats()
        source += self.get_python_high_level_callbacks()
        source += self.get_python_methods()
        source += self.get_python_register_callback_method()
        source += self.get_python_old_name()

        return common.strip_trailing_whitespace(source)

class PythonBindingsPacket(python_common.PythonPacket):
    def get_python_formatted_doc(self):
        text = common.select_lang(self.get_doc_text())

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)
        text += common.format_since_firmware(self.get_device(), self)

        return '\n        '.join(text.strip().split('\n'))

    def get_python_format_list(self, io):
        forms = []

        for element in self.get_elements(direction=io):
            forms.append(element.get_python_struct_format())

        return ' '.join(forms)

class PythonBindingsGenerator(common.BindingsGenerator):
    def get_bindings_name(self):
        return 'python'

    def get_bindings_display_name(self):
        return 'Python'

    def get_device_class(self):
        return PythonBindingsDevice

    def get_packet_class(self):
        return PythonBindingsPacket

    def get_element_class(self):
        return python_common.PythonElement

    def prepare(self):
        self.device_factory_classes = []

        return common.BindingsGenerator.prepare(self)

    def generate(self, device):
        filename = '{0}_{1}.py'.format(device.get_underscore_category(), device.get_underscore_name())

        with open(os.path.join(self.get_bindings_root_directory(), 'bindings', filename), 'w') as f:
            f.write(device.get_python_source())

        if device.is_released():
            self.device_factory_classes.append((device.get_python_import_name(), device.get_python_class_name()))
            self.released_files.append(filename)

    def finish(self):
        template_import = """try:
    from .{0} import {1}
except ValueError:
    from {0} import {1}
"""
        template = """# -*- coding: utf-8 -*-
{0}
{1}

DEVICE_CLASSES = {{
{2}
}}

def get_device_class(device_identifier):
    return DEVICE_CLASSES[device_identifier]

def get_device_display_name(device_identifier):
    return get_device_class(device_identifier).DEVICE_DISPLAY_NAME

def create_device(device_identifier, uid, ipcon):
    return get_device_class(device_identifier)(uid, ipcon)
"""
        imports = []
        classes = []

        for import_name, class_name in sorted(self.device_factory_classes):
            imports.append(template_import.format(import_name, class_name))
            classes.append('{0}.DEVICE_IDENTIFIER: {0},'.format(class_name))

        with open(os.path.join(self.get_bindings_root_directory(), 'bindings', 'device_factory.py'), 'w') as f:
            f.write(template.format(self.get_header_comment('hash'),
                                    '\n'.join(imports),
                                    '\n'.join(classes)))

        return common.BindingsGenerator.finish(self)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', PythonBindingsGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
