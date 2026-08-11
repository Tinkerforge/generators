#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Julia Bindings Generator
Copyright (C) 2020 Jonas Schumacher <github735@jonasschumacher.de>

generate_julia_bindings.py: Generator for Julia bindings

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
from pprint import pprint

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
from generators.julia import julia_common

class JuliaBindingsDevice(julia_common.JuliaDevice):
    def get_julia_import(self):
        template = """

"""

        if not self.is_released():
            released = '\n#### __DEVICE_IS_NOT_RELEASED__ ####\n'
        else:
            released = ''

        return template.format(self.get_generator().get_header_comment('hash'),
                               released)

    def get_julia_namedtuples(self):
        tuples = ''
        template = """
export {struct_name}{name_tup}
struct {struct_name}{name_tup}
    {params}
end
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
                params.append("{0}::{1}".format(element.get_name().under, element.get_julia_type()))

            tuples += template.format(name=name.camel, name_tup=name_tup, params="\n    ".join(params), struct_name=self.get_julia_struct_name())

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
                params.append("{0}::{1}".format(element.get_name().under, element.get_julia_type()))

            tuples += template.format(name=name.camel, name_tup=name_tup, params="\n    ".join(params), struct_name=self.get_julia_struct_name())

        return tuples

    def get_julia_struct(self):
        template = """
export {0}
\"\"\"
{1}
\"\"\"
mutable struct {0} <: TinkerforgeDevice
    replaced::Bool
	uid::Union{{Integer, Missing}}
	uid_string::String
	ipcon::IPConnection
	device_identifier::Integer
	device_display_name::String
    device_url_part::String
	device_identifier_lock::Base.AbstractLock
	device_identifier_check::DeviceIdentifierCheck # protected by device_identifier_lock
	wrong_device_display_name::String # protected by device_identifier_lock
	api_version::Tuple{{Integer, Integer, Integer}}
	registered_callbacks::Dict{{Integer, Function}}
	expected_response_function_id::Union{{Symbol, Nothing}} # protected by request_lock
	expected_response_sequence_number::Union{{Integer, Nothing}} # protected by request_lock
	response_queue::DataStructures.Queue{{Symbol}}
	request_lock::Base.AbstractLock
	stream_lock::Base.AbstractLock

    callbacks::Dict{{Symbol, Integer}}
    callback_formats::Dict{{Symbol, Tuple{{Integer, String}}}}
    high_level_callbacks::Dict{{Symbol, Integer}}
    id_definitions::Dict{{Symbol, Integer}}
    constants::Dict{{Symbol, Union{Integer, String}}}
    response_expected::DefaultDict{{Symbol, ResponseExpected}} 
"""

        return template.format(self.get_julia_struct_name(),
                               common.select_lang(self.get_description()))

    def get_julia_callback_id_definitions(self):
        callback_ids = ''
        template = '        device.callbacks[:CALLBACK_{0}] = {1}\n'

        for packet in self.get_packets('callback'):
            callback_ids += template.format(packet.get_name().upper, packet.get_function_id())

        if self.get_long_display_name() == 'RS232 Bricklet':
            callback_ids += '        device.callbacks[:CALLBACK_READ_CALLBACK] = 8 # for backward compatibility\n'
            callback_ids += '        device.callbacks[:CALLBACK_ERROR_CALLBACK] = 9 # for backward compatibility\n'

        #callback_ids += '\n'

        for packet in self.get_packets('callback'):
            if packet.has_high_level():
                callback_ids += template.format(packet.get_name(skip=-2).upper, -packet.get_function_id())

        return callback_ids

    def get_julia_function_id_definitions(self):
        function_ids = '\n'
        template = '        device.id_definitions[:FUNCTION_{0}] = {1}\n'

        for packet in self.get_packets('function'):
            function_ids += template.format(packet.get_name().upper, packet.get_function_id())

        return function_ids

    def get_julia_constants(self):
        constant_format = '        device.constants[:{constant_group_name_upper}_{constant_name_upper}] = {constant_value}\n'

        return '\n' + self.get_formatted_constants(constant_format, char_format_func="\"{0}\"".format)

    def get_julia_init_method(self):
        template = """
    \"\"\"
    Creates an object with the unique device ID *uid* and adds it to
    the IP Connection *ipcon*.
    \"\"\"
    function {0}(uid::String, ipcon::IPConnection)
        replaced = false
        uid_string = uid
        device_identifier = {5}
        device_display_name = "{6}"
        device_url_part = "{7}" # internal
        device_identifier_lock = Base.ReentrantLock()
        device_identifier_check = DEVICE_IDENTIFIER_CHECK_PENDING # protected by device_identifier_lock
        wrong_device_display_name = "?" # protected by device_identifier_lock
        api_version = (0, 0, 0)
        registered_callbacks = Dict{{Integer, Function}}()
        expected_response_function_id = nothing # protected by request_lock
        expected_response_sequence_number = nothing # protected by request_lock
        response_queue = DataStructures.Queue{{Symbol}}()
        request_lock = Base.ReentrantLock()
        stream_lock = Base.ReentrantLock()

        callbacks = Dict{{Symbol, Integer}}()
        callback_formats = Dict{{Symbol, Tuple{{Integer, String}}}}()
        high_level_callbacks = Dict{{Symbol, Integer}}()
        id_definitions = Dict{{Symbol, Integer}}()
        constants = Dict{{Symbol, Union{Integer, String}}}()
        response_expected = DefaultDict{{Symbol, ResponseExpected}}(RESPONSE_EXPECTED_INVALID_FUNCTION_ID)
        
        device = new(
            replaced,
            missing,
            uid_string,
            ipcon,
            device_identifier,
            device_display_name,
            device_url_part,
            device_identifier_lock,
            device_identifier_check,
            wrong_device_display_name,
            api_version,
            registered_callbacks,
            expected_response_function_id,
            expected_response_sequence_number,
            response_queue,
            request_lock,
            stream_lock,
            callbacks,
            callback_formats,
            high_level_callbacks,
            id_definitions,
            constants,
            response_expected
        )
        _initDevice(device)

        device.api_version = ({1}, {2}, {3})
        
    {4}
        return device
    end
end
"""
        response_expected = ''

        for packet in self.get_packets('function'):
            response_expected += '        device.response_expected[:FUNCTION_{1}] = RESPONSE_EXPECTED_{2}\n' \
                                 .format(self.get_julia_struct_name(), packet.get_name().upper,
                                         packet.get_response_expected().upper())

        fillins = self.get_julia_callback_id_definitions()
        fillins += self.get_julia_function_id_definitions()
        fillins += self.get_julia_constants()+'\n'
        fillins += common.wrap_non_empty('', response_expected, '\n')
        fillins += self.get_julia_callback_formats()
        fillins += self.get_julia_high_level_callbacks()
        fillins += self.get_julia_add_device()

        return template.format(self.get_julia_struct_name(),
                               *self.get_api_version(),
                               fillins,
                               self.get_device_identifier(),
                               self.get_long_display_name(),
                               self.get_name().under)

    def get_julia_callback_formats(self):
        callback_formats = ''
        template = '        device.callback_formats[:CALLBACK_{1}] = ({2}, "{3}")\n'

        for packet in self.get_packets('callback'):
            callback_formats += template.format(self.get_julia_struct_name(),
                                                packet.get_name().upper,
                                                packet.get_response_size(),
                                                packet.get_julia_format_list('out'))

        return callback_formats + '\n'

    def get_julia_high_level_callbacks(self):
        high_level_callbacks = ''
        template = '        device.high_level_callbacks[:CALLBACK_{1}] = [{4}, Dict("fixed_length" => {2}, "single_chunk" => {3}), nothing]\n'

        for packet in self.get_packets('callback'):
            stream = packet.get_high_level('stream_*')

            if stream != None:
                roles = []

                for element in packet.get_elements(direction='out'):
                    roles.append(element.get_role())

                high_level_callbacks += template.format(self.get_julia_struct_name(),
                                                        packet.get_name(skip=-2).upper,
                                                        stream.get_fixed_length(),
                                                        stream.has_single_chunk(),
                                                        repr(tuple(roles)).replace("'", "\""))

        return high_level_callbacks

    def get_julia_add_device(self):
        return '    add_device(ipcon, device)\n'

    def get_julia_methods(self):
        m_tup = """
export {0}
\"\"\"
    $(SIGNATURES)

{10}
\"\"\"
function {0}(device::{2}{8}{4})
    {11}
    {12}
    return {1}(send_request(device, :FUNCTION_{3}, ({4}{9}), \"{5}\", {6}, \"{7}\"))
end
"""
        m_ret = """
export {0}
\"\"\"
    $(SIGNATURES)

{9}
\"\"\"
function {0}(device::{1}{7}{3})
    {10}
    {11}
    return send_request(device, :FUNCTION_{2}, ({3}{8}), \"{4}\", {5}, \"{6}\")
end
"""
        m_nor = """
export {0}
\"\"\"
    $(SIGNATURES)

{7}
\"\"\"
function {0}(device::{1}{5}{3})
    {8}
    {9}
    send_request(device, :FUNCTION_{2}, ({3}{6}), \"{4}\", 0, \"\")
end
"""
        methods = ''
        cls = self.get_julia_struct_name()

        # normal and low-level
        for packet in self.get_packets('function'):
            nb = packet.get_name().camel
            ns = packet.get_name().under
            nh = ns.upper()
            par = packet.get_julia_parameters()
            doc = packet.get_julia_formatted_doc()
            cp = ''
            ct = ''

            if par != '':
                cp = ', '

                if not ',' in par:
                    ct = ','

            in_f = packet.get_julia_format_list('in')
            out_l = packet.get_response_size()
            out_f = packet.get_julia_format_list('out')

            if packet.get_function_id() == 255: # <device>.get_identity
                check = ''
            else:
                check = 'check_validity(device)\n'

            coercions = common.wrap_non_empty('', packet.get_julia_parameter_coercions(), '\n')
            out_c = len(packet.get_elements(direction='out'))

            if out_c > 1:
                methods += m_tup.format(ns, nb, cls, nh, par, in_f, out_l, out_f, cp, ct, doc, check, coercions)
            elif out_c == 1:
                methods += m_ret.format(ns, cls, nh, par, in_f, out_l, out_f, cp, ct, doc, check, coercions)
            else:
                methods += m_nor.format(ns, cls, nh, par, in_f, cp, ct, doc, check, coercions)

        # high-level
        template_stream_in = """
export {function_name}
\"\"\"
{doc}
\"\"\"
function {function_name}(device::{struct_name}{high_level_parameters})
    {coercions}
    if length({stream_name_under}) > {stream_max_length}
        throw(TinkerforgeInvalidParameterError("{stream_name_space} can be at most {stream_max_length} items long"))
    end

    {stream_name_under}_length = length({stream_name_under})
    {stream_name_under}_chunk_offset = 0

    if {stream_name_under}_length == 0
        {stream_name_under}_chunk_data = [{chunk_padding}] * {chunk_cardinality}
        ret = {function_name}_low_level(device, {parameters})
    else
        lock(device.stream_lock) do
            while {stream_name_under}_chunk_offset < {stream_name_under}_length
                {stream_name_under}_chunk_data = create_chunk_data({stream_name_under}, {stream_name_under}_chunk_offset, {chunk_cardinality}, {chunk_padding})
                ret = {function_name}_low_level(device, {parameters})
                {stream_name_under}_chunk_offset += {chunk_cardinality}
            end
        end
    end
{result}
end
"""
        template_stream_in_fixed_length = """
export {function_name}
\"\"\"
{doc}
\"\"\"
function {function_name}(device::{struct_name}{high_level_parameters})
    {coercions}
    {stream_name_under}_length = {fixed_length}
    {stream_name_under}_chunk_offset = 0

    if length({stream_name_under}) != {stream_name_under}_length
        throw(TinkerforgeInvalidParameterError("{stream_name_space} can be at most ${stream_name_under}_length items long"))
    end

    lock(device.stream_lock) do
        while {stream_name_under}_chunk_offset < {stream_name_under}_length
            {stream_name_under}_chunk_data = create_chunk_data({stream_name_under}, {stream_name_under}_chunk_offset, {chunk_cardinality}, {chunk_padding})
            ret = {function_name}_low_level(device, {parameters})
            {stream_name_under}_chunk_offset += {chunk_cardinality}
        end
    end
{result}
end
"""
        template_stream_in_result = """
        return ret"""
        template_stream_in_namedtuple_result = """
        return {result_camel_name}(*ret)"""
        template_stream_in_short_write = """
export {function_name}
\"\"\"
{doc}
\"\"\"
function {function_name}(device::{struct_name}{high_level_parameters})
    {coercions}
    if length({stream_name_under}) > {stream_max_length}
        throw(TinkerforgeInvalidParameterError("{stream_name_space} can be at most {stream_max_length} items long"))
    end

    {stream_name_under}_length = length({stream_name_under})
    {stream_name_under}_chunk_offset = 0

    if {stream_name_under}_length == 0
        {stream_name_under}_chunk_data = [{chunk_padding}] * {chunk_cardinality}
        ret = {function_name}_low_level(device, {parameters})
        {chunk_written_0}
    else
        {stream_name_under}_written = 0

        lock(device.stream_lock) do
            while {stream_name_under}_chunk_offset < {stream_name_under}_length
                {stream_name_under}_chunk_data = create_chunk_data({stream_name_under}, {stream_name_under}_chunk_offset, {chunk_cardinality}, {chunk_padding})
                ret = {function_name}_low_level(device, {parameters})
                {chunk_written_n}

                if {chunk_written_test} < {chunk_cardinality}
                    break # either last chunk or short write
                end

                {stream_name_under}_chunk_offset += {chunk_cardinality}
            end
        end
    end
{result}
end
"""
        template_stream_in_short_write_chunk_written = ['{stream_name_under}_written = ret',
                                                        '{stream_name_under}_written += ret',
                                                        'ret']
        template_stream_in_short_write_namedtuple_chunk_written = ['{stream_name_under}_written = ret.{stream_name_under}_chunk_written',
                                                                   '{stream_name_under}_written += ret.{stream_name_under}_chunk_written',
                                                                   'ret.{stream_name_under}_chunk_written']
        template_stream_in_short_write_result = """
        return {stream_name_under}_written"""
        template_stream_in_short_write_namedtuple_result = """
        return {result_camel_name}({result_fields})"""
        template_stream_in_single_chunk = """
export {function_name}
\"\"\"
{doc}
\"\"\"
function {function_name}(device::{struct_name}{high_level_parameters})
    {coercions}
    {stream_name_under}_length = length({stream_name_under})
    {stream_name_under}_data = list({stream_name_under}) # make a copy so we can potentially extend it

    if {stream_name_under}_length > {chunk_cardinality}
        throw(TinkerforgeInvalidParameterError("{stream_name_space} can be at most {chunk_cardinality} items long"))
    end

    if {stream_name_under}_length < {chunk_cardinality}
        {stream_name_under}_data += [{chunk_padding}] * ({chunk_cardinality} - {stream_name_under}_length)
    end
{result}
end
"""
        template_stream_in_single_chunk_result = """
        return {function_name}_low_level(device, {parameters})"""
        template_stream_in_single_chunk_namedtuple_result = """
        return {result_camel_name}({function_name}_low_level(device, {parameters})...)"""
        template_stream_out = """
export {function_name}
\"\"\"
{doc}
\"\"\"
function {function_name}(device::{struct_name}{high_level_parameters})
    {coercions}{fixed_length}
    lock(device.stream_lock) do
        ret = {function_name}_low_level(device, {parameters}){dynamic_length_3}
        {chunk_offset_check}{stream_name_under}_out_of_sync = ret.{stream_name_under}_chunk_offset != 0
        {closing_end}
        {chunk_offset_check_indent}{stream_name_under}_data = ret.{stream_name_under}_chunk_data

        while !{stream_name_under}_out_of_sync && length({stream_name_under}_data) < {stream_name_under}_length
            ret = {function_name}_low_level(device, {parameters}){dynamic_length_4}
            {stream_name_under}_out_of_sync = ret.{stream_name_under}_chunk_offset != length({stream_name_under}_data)
            {stream_name_under}_data += ret.{stream_name_under}_chunk_data
        end

        if {stream_name_under}_out_of_sync # discard remaining stream to bring it back in-sync
            while ret.{stream_name_under}_chunk_offset + {chunk_cardinality} < {stream_name_under}_length
                ret = {function_name}_low_level(device, {parameters}){dynamic_length_5}
            end

            throw(TinkerforgeStreamOutOfSyncError("{stream_name_space} stream is out-of-sync"))
        end
    end
{result}
end
"""
        template_stream_out_fixed_length = """
    {stream_name_under}_length = {fixed_length}
"""
        template_stream_out_dynamic_length = """
{{indent}}{stream_name_under}_length = ret.{stream_name_under}_length"""
        template_stream_out_chunk_offset_check = """
        if ret.{stream_name_under}_chunk_offset == (1 << {shift_size}) - 1 # maximum chunk offset -> stream has no data
            {stream_name_under}_length = 0
            {stream_name_under}_out_of_sync = false
            {stream_name_under}_data = ()
        else
            """
        template_stream_out_single_chunk = """
export {function_name}
\"\"\"
{doc}
\"\"\"
function {function_name}(device::{struct_name}{high_level_parameters})
    {coercions}
    ret = {function_name}_low_level(device, {parameters})
{result}
end
"""
        template_stream_out_result = """
        return {stream_name_under}_data[:{stream_name_under}_length]"""
        template_stream_out_single_chunk_result = """
        return ret.{stream_name_under}_data[:ret.{stream_name_under}_length]"""
        template_stream_out_namedtuple_result = """
        return {result_name}({result_fields})"""

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
                        chunk_written_0 = template_stream_in_short_write_chunk_written[0].format(stream_name_under=stream_in.get_name().under)
                        chunk_written_n = template_stream_in_short_write_chunk_written[1].format(stream_name_under=stream_in.get_name().under)
                        chunk_written_test = template_stream_in_short_write_chunk_written[2].format(stream_name_under=stream_in.get_name().under)
                    else:
                        chunk_written_0 = template_stream_in_short_write_namedtuple_chunk_written[0].format(stream_name_under=stream_in.get_name().under)
                        chunk_written_n = template_stream_in_short_write_namedtuple_chunk_written[1].format(stream_name_under=stream_in.get_name().under)
                        chunk_written_test = template_stream_in_short_write_namedtuple_chunk_written[2].format(stream_name_under=stream_in.get_name().under)

                    if len(packet.get_elements(direction='out', high_level=True)) < 2:
                        if stream_in.has_single_chunk():
                            result = template_stream_in_single_chunk_result.format(function_name=packet.get_name(skip=-2).under,
                                                                                   parameters=packet.get_julia_parameters())
                        else:
                            result = template_stream_in_short_write_result.format(stream_name_under=stream_in.get_name().under)
                    else:
                        if stream_in.has_single_chunk():
                            result = template_stream_in_single_chunk_namedtuple_result.format(function_name=packet.get_name(skip=-2).under,
                                                                                              parameters=packet.get_julia_parameters(),
                                                                                              result_camel_name=packet.get_name(skip=-2).camel)
                        else:
                            fields = []

                            for element in packet.get_elements(direction='out', high_level=True):
                                if element.get_role() == 'stream_written':
                                    fields.append('{0}_written'.format(stream_in.get_name().under))
                                else:
                                    fields.append('ret.{0}'.format(element.get_name().under))

                            result = template_stream_in_short_write_namedtuple_result.format(result_camel_name=packet.get_name(skip=-2).camel,
                                                                                             result_fields=', '.join(fields))
                else:
                    chunk_written_0 = ''
                    chunk_written_n = ''
                    chunk_written_test = ''

                    if len(packet.get_elements(direction='out', high_level=True)) < 2:
                        if stream_in.has_single_chunk():
                            result = template_stream_in_single_chunk_result.format(function_name=packet.get_name(skip=-2).under,
                                                                                   parameters=packet.get_julia_parameters())
                        else:
                            result = template_stream_in_result
                    else:
                        if stream_in.has_single_chunk():
                            result = template_stream_in_single_chunk_namedtuple_result.format(function_name=packet.get_name(skip=-2).under,
                                                                                              parameters=packet.get_julia_parameters(),
                                                                                              result_camel_name=packet.get_name(skip=-2).camel)
                        else:
                            result = template_stream_in_namedtuple_result.format(result_camel_name=packet.get_name(skip=-2).camel)

                methods += template.format(doc=packet.get_julia_formatted_doc(),
                                           coercions=common.wrap_non_empty('\n        ', packet.get_julia_parameter_coercions(high_level=True), '\n'),
                                           function_name=packet.get_name(skip=-2).under,
                                           parameters=packet.get_julia_parameters(),
                                           high_level_parameters=common.wrap_non_empty(', ', packet.get_julia_parameters(high_level=True), ''),
                                           stream_name_space=stream_in.get_name().space,
                                           stream_name_under=stream_in.get_name().under,
                                           stream_max_length=abs(stream_in.get_data_element().get_cardinality()),
                                           fixed_length=stream_in.get_fixed_length(),
                                           chunk_cardinality=stream_in.get_chunk_data_element().get_cardinality(),
                                           chunk_padding=stream_in.get_chunk_data_element().get_julia_default_item_value(),
                                           chunk_written_0=chunk_written_0,
                                           chunk_written_n=chunk_written_n,
                                           chunk_written_test=chunk_written_test,
                                           struct_name=self.get_julia_struct_name(),
                                           #closing_end='end\n' if chunk_offset_check else '',
                                           result=result)
            elif stream_out != None:
                if stream_out.get_fixed_length() != None:
                    fixed_length = template_stream_out_fixed_length.format(stream_name_under=stream_out.get_name().under,
                                                                           fixed_length=stream_out.get_fixed_length())
                    dynamic_length = ''
                    shift_size = int(stream_out.get_chunk_offset_element().get_type().replace('uint', ''))
                    chunk_offset_check = template_stream_out_chunk_offset_check.format(stream_name_under=stream_out.get_name().under,
                                                                                       shift_size=shift_size)
                    chunk_offset_check_indent = ''
                else:
                    fixed_length = ''
                    dynamic_length = template_stream_out_dynamic_length.format(stream_name_under=stream_out.get_name().under)
                    chunk_offset_check = ''
                    chunk_offset_check_indent = ''

                if len(packet.get_elements(direction='out', high_level=True)) < 2:
                    if stream_out.has_single_chunk():
                        result = template_stream_out_single_chunk_result.format(stream_name_under=stream_out.get_name().under)
                    else:
                        result = template_stream_out_result.format(stream_name_under=stream_out.get_name().under)
                else:
                    fields = []

                    for element in packet.get_elements(direction='out', high_level=True):
                        if element.get_role() == 'stream_data':
                            if stream_out.has_single_chunk():
                                fields.append('ret.{0}_data[:ret.{0}_length]'.format(stream_out.get_name().under))
                            else:
                                fields.append('{0}_data[:{0}_length]'.format(stream_out.get_name().under))
                        else:
                            fields.append('ret.{0}'.format(element.get_name().under))

                    result = template_stream_out_namedtuple_result.format(result_name=packet.get_name(skip=-2).camel,
                                                                          result_fields=', '.join(fields))

                if stream_out.has_single_chunk():
                    template = template_stream_out_single_chunk
                else:
                    template = template_stream_out

                methods += template.format(doc=packet.get_julia_formatted_doc(),
                                           coercions=common.wrap_non_empty('\n        ', packet.get_julia_parameter_coercions(high_level=True), '\n'),
                                           function_name=packet.get_name(skip=-2).under,
                                           parameters=packet.get_julia_parameters(),
                                           high_level_parameters=common.wrap_non_empty(', ', packet.get_julia_parameters(high_level=True), ''),
                                           stream_name_space=stream_out.get_name().space,
                                           stream_name_under=stream_out.get_name().under,
                                           fixed_length=fixed_length,
                                           dynamic_length_3=dynamic_length.format(indent='    ' * 3),
                                           dynamic_length_4=dynamic_length.format(indent='    ' * 4),
                                           dynamic_length_5=dynamic_length.format(indent='    ' * 5),
                                           chunk_offset_check=chunk_offset_check,
                                           chunk_offset_check_indent=chunk_offset_check_indent,
                                           chunk_cardinality=stream_out.get_chunk_data_element().get_cardinality(),
                                           struct_name=self.get_julia_struct_name(),
                                           closing_end='end\n' if chunk_offset_check != '' else '',
                                           result=result)

        return methods

    def get_julia_register_callback_method(self):
        if len(self.get_packets('callback')) == 0:
            return ''

        return """
export register_callback
\"\"\"
Registers the given *function* with the given *callback_id*.
\"\"\"
function register_callback(device::{0}, callback_id, function_)
    if isnothing(function_)
        device.registered_callbacks.pop(callback_id, None)
    else
        device.registered_callbacks[callback_id] = function_
    end
end
""".format(self.get_julia_struct_name())

    def get_julia_old_name(self):
        template = """
{0} = {1} # for backward compatibility
"""

        return ""#template.format(self.get_name().camel, self.get_julia_struct_name())

    def get_julia_source(self):
        source  = self.get_julia_import()
        source += self.get_julia_namedtuples()
        source += self.get_julia_struct()
        source += self.get_julia_init_method()
        source += self.get_julia_methods()
        source += self.get_julia_register_callback_method()

        if self.is_brick() or self.is_bricklet():
            source += self.get_julia_old_name()

        return common.strip_trailing_whitespace(source)

class JuliaBindingsPacket(julia_common.JuliaPacket):
    def get_julia_formatted_doc(self):
        text = common.select_lang(self.get_doc_text())

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text).replace("\\", "\\\\").replace("$", "\\$")
        text = common.handle_rst_substitutions(text, self)
        text += common.format_since_firmware(self.get_device(), self, nbsp='\\$nbsp;')

        return '\n'.join(text.strip().split('\n'))

    def get_julia_format_list(self, io):
        forms = []

        for element in self.get_elements(direction=io):
            forms.append(element.get_julia_struct_format())

        return ' '.join(forms)

    def get_julia_parameter_coercions(self, high_level=False):
        coercions = []

        for element in self.get_elements(direction='in', high_level=high_level):
            name = element.get_name().under

            coercions.append('{0} = {1}'.format(name, element.get_julia_parameter_coercion().format(name)))

        return '\n    '.join(coercions)

class JuliaBindingsGenerator(julia_common.JuliaGeneratorTrait, common.BindingsGenerator):
    def get_device_class(self):
        return JuliaBindingsDevice

    def get_packet_class(self):
        return JuliaBindingsPacket

    def get_element_class(self):
        return julia_common.JuliaElement

    def prepare(self):
        common.BindingsGenerator.prepare(self)

        self.device_factory_all_classes = []
        self.device_factory_released_classes = []
        self.device_display_names = []

    def generate(self, device):
        filename = '{0}_{1}.jl'.format(device.get_category().under, device.get_name().under)

        with open(os.path.join(self.get_bindings_dir(), filename), 'w') as f:
            f.write(device.get_julia_source())

        self.device_factory_all_classes.append((device.get_julia_import_name(), device.get_julia_struct_name(), device.get_device_identifier()))

        if device.is_released():
            self.device_factory_released_classes.append((device.get_julia_import_name(), device.get_julia_struct_name(), device.get_device_identifier()))
            self.device_display_names.append((device.get_device_identifier(), device.get_long_display_name()))
            self.released_files.append(filename)

    def finish(self):
        template_import = """include("{0}.jl")"""
        template = """{0}
{1}

export get_device_type
function get_device_type(device_identifier::Integer)
    device_types = Dict{{Integer, String}}(
{2}
    )

    return device_types[device_identifier]
end

export create_device
function create_device(device_identifier::Integer, uid::String, ipcon::IPConnection)
    return get_device_type(device_identifier)(uid, ipcon)
end
"""
        for filename, device_factory_classes in [('device_factory_all.jl', self.device_factory_all_classes),
                                                 ('device_factory.jl', self.device_factory_released_classes)]:
            imports = []
            classes = []

            for import_name, class_name, device_identifier in sorted(device_factory_classes):
                imports.append(template_import.format(import_name, class_name))
                classes.append('        {0} => "{1}",'.format(device_identifier, class_name))

            with open(os.path.join(self.get_bindings_dir(), filename), 'w') as f:
                f.write(template.format(self.get_header_comment('hash'),
                                        '\n'.join(imports),
                                        '\n'.join(classes)))

        template = """{header}
export get_device_display_name
function get_device_display_name(device_identifier::Integer)
    device_display_names = Dict{{Integer, String}}(
    {entries}
    )
    
    try
        device_display_name = dict["d"]
    catch e
        if e isa KeyError
            device_display_name = "Unknown Device [{{device_identifier}}]"
        end
    end

    return device_display_name
end
"""

        entries = []

        for device_identifier, device_display_name in sorted(self.device_display_names):
            entries.append('    {0} => "{1}"'.format(device_identifier, device_display_name))

        with open(os.path.join(self.get_bindings_dir(), 'device_display_names.jl'), 'w') as f:
            f.write(template.format(header=self.get_header_comment('hash'),
                                    entries=',\n    '.join(entries)))

        self.released_files.append('device_display_names.jl')

        common.BindingsGenerator.finish(self)

def generate(root_dir, language, internal):
    common.generate(root_dir, language, internal, JuliaBindingsGenerator)

if __name__ == '__main__':
    args = common.dockerize('julia', __file__, add_internal_argument=True)

    generate(os.getcwd(), 'en', args.internal)
