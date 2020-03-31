#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ruby Bindings Generator
Copyright (C) 2012-2015, 2017-2018, 2020 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_ruby.py: Generator for Ruby bindings

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
import ruby_common

class RubyBindingsDevice(ruby_common.RubyDevice):
    def specialize_ruby_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return 'CALLBACK_{0}'.format(packet.get_name(skip=-2 if high_level else 0).upper)
            else:
                return '{0}#{1}'.format(packet.get_device().get_ruby_class_name(),
                                        packet.get_name(skip=-2 if high_level else 0).under)

        return self.specialize_doc_rst_links(text, specializer)

    def get_ruby_header(self):
        template = """# -*- ruby encoding: utf-8 -*-
{0}
"""

        return template.format(self.get_generator().get_header_comment('hash'),
                               self.get_category().under,
                               self.get_name().under)

    def get_ruby_class(self):
        template = """require_relative './ip_connection'

module Tinkerforge
  # {1}
  class {0} < Device
    DEVICE_IDENTIFIER = {2} # :nodoc:
    DEVICE_DISPLAY_NAME = '{3}' # :nodoc:
"""

        return template.format(self.get_ruby_class_name(),
                               common.select_lang(self.get_description()),
                               self.get_device_identifier(),
                               self.get_long_display_name())

    def get_ruby_callback_id_definitions(self):
        callback_ids = ''
        template = """
    # {2}
    CALLBACK_{0} = {1}
"""

        for packet in self.get_packets('callback'):
            if packet.has_high_level():
                doc = 'See CALLBACK_{}'.format(packet.get_name(skip=-2).upper)
            else:
                doc = packet.get_ruby_formatted_doc()
            callback_ids += template.format(packet.get_name().upper, packet.get_function_id(), doc)

        if self.get_long_display_name() == 'RS232 Bricklet':
            callback_ids += '\n'
            callback_ids += '    CALLBACK_READ_CALLBACK = 8 # :nodoc: for backward compatibility\n'
            callback_ids += '    CALLBACK_ERROR_CALLBACK = 9 # :nodoc: for backward compatibility\n'

        for packet in self.get_packets('callback'):
            if packet.has_high_level():
                doc = packet.get_ruby_formatted_doc()
                callback_ids += template.format(packet.get_name(skip=-2).upper, -packet.get_function_id(), doc)

        return callback_ids

    def get_ruby_function_id_definitions(self):
        function_ids = '\n'
        template = '    FUNCTION_{0} = {1} # :nodoc:\n'

        for packet in self.get_packets('function'):
            function_ids += template.format(packet.get_name().upper, packet.get_function_id())

        return function_ids

    def get_ruby_constants(self):
        constant_format = '    {constant_group_name_upper}_{constant_name_upper} = {constant_value} # :nodoc:\n'

        return '\n' + self.get_formatted_constants(constant_format, bool_format_func=lambda value: str(value).lower())

    def get_ruby_initialize_method(self):
        template = """
    # Creates an object with the unique device ID <tt>uid</tt> and adds it to
    # the IP Connection <tt>ipcon</tt>.
    def initialize(uid, ipcon)
      super uid, ipcon, DEVICE_IDENTIFIER, DEVICE_DISPLAY_NAME

      @api_version = [{0}, {1}, {2}]

"""

        return template.format(*self.get_api_version())

    def get_ruby_response_expected(self):
        result = []
        template = '      @response_expected[FUNCTION_{name}] = RESPONSE_EXPECTED_{flag}\n'

        for packet in self.get_packets('function'):
            result.append(template.format(name=packet.get_name().upper,
                                          flag=packet.get_response_expected().upper()))

        return ''.join(result) + '\n'

    def get_ruby_callback_formats(self):
        callback_formats = ''
        template = "      @callback_formats[CALLBACK_{0}] = [{1}, '{2}']\n"

        for packet in self.get_packets('callback'):
            form = packet.get_ruby_format_list('out')
            callback_formats += template.format(packet.get_name().upper, packet.get_response_size(), form)

        return callback_formats

    def get_ruby_high_level_callbacks(self):
        high_level_callbacks = '\n'
        template = "      @high_level_callbacks[CALLBACK_{0}] = [[{3}], {{'fixed_length' => {1}, 'single_chunk' => {2}}}, nil]\n"

        for packet in self.get_packets('callback'):
            stream = packet.get_high_level('stream_*')

            if stream != None:
                roles = []

                for element in packet.get_elements(direction='out'):
                    roles.append(element.get_role())

                high_level_callbacks += template.format(packet.get_name(skip=-2).upper,
                                                        stream.get_fixed_length(default='nil'),
                                                        'true' if stream.has_single_chunk() else 'false',
                                                        ', '.join(map(lambda role: "'{0}'".format(role) if role != None else 'nil', roles)))

        return high_level_callbacks + '      @ipcon.add_device self\n     end\n'

    def get_ruby_methods(self):
        methods = ''

        # normal and low-level
        method0 = """
    # {4}
    def {0}{5}
      send_request FUNCTION_{1}, [], '', {2}, '{3}'
    end
"""
        method1 = """
    # {6}
    def {0}({1}){7}
      send_request FUNCTION_{2}, [{1}], '{3}', {4}, '{5}'
    end
"""

        for packet in self.get_packets('function'):
            name = packet.get_name().under
            fid = packet.get_name().upper
            parms = packet.get_ruby_parameters()
            doc = packet.get_ruby_formatted_doc()
            in_format = packet.get_ruby_format_list('in')
            out_size = packet.get_response_size()
            out_format = packet.get_ruby_format_list('out')

            if packet.get_function_id() == 255: # <device>.get_identity
                check = ''
            else:
                check = '\n      check_validity\n'

            if len(parms) > 0:
                methods += method1.format(name, parms, fid, in_format, out_size, out_format, doc, check)
            else:
                methods += method0.format(name, fid, out_size, out_format, doc, check)

        # high-level
        template_stream_in = """
    # {doc}
    def {function_name}{high_level_parameters}
      if {stream_name_under}.length > {stream_max_length}
        raise ArgumentError, '{stream_name_space} can be at most {stream_max_length} items long'
      end

      {stream_name_under}_length = {stream_name_under}.length
      {stream_name_under}_chunk_offset = 0

      if {stream_name_under}_length == 0
        {stream_name_under}_chunk_data = [{chunk_padding}] * {chunk_cardinality}
        ret = {function_name}_low_level{parameters}
      else
        ret = nil # assigned in block

        @stream_mutex.synchronize {{
          while {stream_name_under}_chunk_offset < {stream_name_under}_length
            {stream_name_under}_chunk_data = {stream_name_under}[{stream_name_under}_chunk_offset, {chunk_cardinality}]

            if {stream_name_under}_chunk_data.length < {chunk_cardinality}
              {stream_name_under}_chunk_data += [{chunk_padding}] * ({chunk_cardinality} - {stream_name_under}_chunk_data.length)
            end

            ret = {function_name}_low_level{parameters}
            {stream_name_under}_chunk_offset += {chunk_cardinality}
          end
        }}
      end

      ret
    end
"""
        template_stream_in_fixed_length = """
    # {doc}
    def {function_name}{high_level_parameters}
      {stream_name_under}_length = {fixed_length}
      {stream_name_under}_chunk_offset = 0
      ret = nil # assigned in block

      if {stream_name_under}.length != {stream_name_under}_length
        raise ArgumentError, "{stream_name_space} has to be exactly #{{{stream_name_under}_length}} items long"
      end

      @stream_mutex.synchronize {{
        while {stream_name_under}_chunk_offset < {stream_name_under}_length
          {stream_name_under}_chunk_data = {stream_name_under}[{stream_name_under}_chunk_offset, {chunk_cardinality}]

          if {stream_name_under}_chunk_data.length < {chunk_cardinality}
            {stream_name_under}_chunk_data += [{chunk_padding}] * ({chunk_cardinality} - {stream_name_under}_chunk_data.length)
          end

          ret = {function_name}_low_level{parameters}
          {stream_name_under}_chunk_offset += {chunk_cardinality}
        end
      }}

      ret
    end
"""
        template_stream_in_short_write = """
    # {doc}
    def {function_name}{high_level_parameters}
      if {stream_name_under}.length > {stream_max_length}
        raise ArgumentError, '{stream_name_space} can be at most {stream_max_length} items long'
      end

      {stream_name_under}_length = {stream_name_under}.length
      {stream_name_under}_chunk_offset = 0

      if {stream_name_under}_length == 0
        {stream_name_under}_chunk_data = [{chunk_padding}] * {chunk_cardinality}
        ret = {function_name}_low_level{parameters}
        {chunk_written_0}
      else{chunk_result_predefinition}
        {stream_name_under}_written = 0 # assigned in block

        @stream_mutex.synchronize {{
          while {stream_name_under}_chunk_offset < {stream_name_under}_length
            {stream_name_under}_chunk_data = {stream_name_under}[{stream_name_under}_chunk_offset, {chunk_cardinality}]

            if {stream_name_under}_chunk_data.length < {chunk_cardinality}
              {stream_name_under}_chunk_data += [{chunk_padding}] * ({chunk_cardinality} - {stream_name_under}_chunk_data.length)
            end

            ret = {function_name}_low_level{parameters}
            {chunk_written_n}

            if {chunk_written_test} < {chunk_cardinality}
              break # either last chunk or short write
            end

            {stream_name_under}_chunk_offset += {chunk_cardinality}
          end
        }}
      end
{result}
    end
"""
        template_stream_in_short_write_chunk_result_predefinition = """
        ret = nil # assigned in block"""
        template_stream_in_short_write_chunk_written = ['{stream_name_under}_written = ret',
                                                        '{stream_name_under}_written += ret',
                                                        'ret']
        template_stream_in_short_write_namedtuple_chunk_written = ['{stream_name_under}_written = ret[{chunk_written_index}]',
                                                                   '{stream_name_under}_written += ret[{chunk_written_index}]',
                                                                   'ret[{chunk_written_index}]']
        template_stream_in_short_write_result = """
      {stream_name_under}_written"""
        template_stream_in_short_write_namedtuple_result = """
      [{result_fields}]"""
        template_stream_in_single_chunk = """
    # {doc}
    def {function_name}{high_level_parameters}
      {stream_name_under} = {stream_name_under}.clone # clone so we can potentially extend it
      {stream_name_under}_length = {stream_name_under}.length
      {stream_name_under}_data = {stream_name_under}

      if {stream_name_under}_length > {chunk_cardinality}
        raise ArgumentError, '{stream_name_space} can be at most {chunk_cardinality} items long'
      end

      if {stream_name_under}_length < {chunk_cardinality}
        {stream_name_under}_data += [{chunk_padding}] * ({chunk_cardinality} - {stream_name_under}_length)
      end

      {function_name}_low_level{parameters}
    end
"""
        template_stream_out = """
    # {doc}
    def {function_name}{high_level_parameters}{chunk_result_predefinition}
      {stream_name_under}_length = {fixed_length}
      {stream_name_under}_data = nil # assigned in block

      @stream_mutex.synchronize {{
        ret = {function_name}_low_level{parameters}{dynamic_length_4}
        {stream_name_under}_chunk_offset = ret[{chunk_offset_index}]
{chunk_offset_check}{stream_name_under}_out_of_sync = {stream_name_under}_chunk_offset != 0
        {chunk_offset_check_indent}{stream_name_under}_data = ret[{chunk_data_index}]{chunk_offset_check_end}

        while not {stream_name_under}_out_of_sync and {stream_name_under}_data.length < {stream_name_under}_length
          ret = {function_name}_low_level{parameters}{dynamic_length_5}
          {stream_name_under}_chunk_offset = ret[{chunk_offset_index}]
          {stream_name_under}_out_of_sync = {stream_name_under}_chunk_offset != {stream_name_under}_data.length
          {stream_name_under}_data += ret[{chunk_data_index}]
        end

        if {stream_name_under}_out_of_sync # discard remaining stream to bring it back in-sync
          while {stream_name_under}_chunk_offset + {chunk_cardinality} < {stream_name_under}_length
            ret = {function_name}_low_level{parameters}{dynamic_length_6}
            {stream_name_under}_chunk_offset = ret[{chunk_offset_index}]
          end

          raise StreamOutOfSyncException, '{stream_name_space} stream is out-of-sync'
        end
      }}
{result}
    end
"""
        template_stream_out_chunk_result_predefinition = """
      ret = nil # assigned in block"""
        template_stream_out_dynamic_length = """
{{indent}}{stream_name_under}_length = ret[{length_index}]"""
        template_stream_out_chunk_offset_check = """
        if {stream_name_under}_chunk_offset == (1 << {shift_size}) - 1 # maximum chunk offset -> stream has no data
          {stream_name_under}_length = 0
          {stream_name_under}_chunk_offset = 0
          {stream_name_under}_out_of_sync = false
          {stream_name_under}_data = []
        else
          """
        template_stream_out_single_chunk = """
    # {doc}
    def {function_name}{high_level_parameters}
      ret = {function_name}_low_level{parameters}
{result}
    end
"""
        template_stream_out_result = """
      {stream_name_under}_data[0, {stream_name_under}_length]"""
        template_stream_out_single_chunk_result = """
      ret[{chunk_data_index}][0, ret[{length_index}]]"""
        template_stream_out_namedtuple_result = """
      [{result_fields}]"""

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
                        chunk_written_index = None

                        for i, element in enumerate(packet.get_elements(direction='out')):
                            if element.get_role() == 'stream_chunk_written':
                                chunk_written_index = i
                                break

                        chunk_written_0 = template_stream_in_short_write_namedtuple_chunk_written[0].format(stream_name_under=stream_in.get_name().under,
                                                                                                            chunk_written_index=chunk_written_index)
                        chunk_written_n = template_stream_in_short_write_namedtuple_chunk_written[1].format(stream_name_under=stream_in.get_name().under,
                                                                                                            chunk_written_index=chunk_written_index)
                        chunk_written_test = template_stream_in_short_write_namedtuple_chunk_written[2].format(stream_name_under=stream_in.get_name().under,
                                                                                                               chunk_written_index=chunk_written_index)

                    if len(packet.get_elements(direction='out', high_level=True)) < 2:
                        chunk_result_predefinition = ''
                        result = template_stream_in_short_write_result.format(stream_name_under=stream_in.get_name().under)
                    else:
                        chunk_result_predefinition = template_stream_in_short_write_chunk_result_predefinition.format(stream_name_under=stream_in.get_name().under)
                        fields = []

                        for element in packet.get_elements(direction='out', high_level=True):
                            if element.get_role() == 'stream_written':
                                fields.append('{0}_written'.format(stream_in.get_name().under))
                            else:
                                index = None

                                for i, other in enumerate(packet.get_elements(direction='out')):
                                    if other.get_name().space == element.get_name().space:
                                        index = i
                                        break

                                fields.append('ret[{0}]'.format(index))

                        result = template_stream_in_short_write_namedtuple_result.format(result_fields=', '.join(fields))
                else:
                    chunk_written_0 = ''
                    chunk_written_n = ''
                    chunk_written_test = ''
                    chunk_result_predefinition = ''
                    result = ''

                methods += template.format(doc=packet.get_ruby_formatted_doc(),
                                           function_name=packet.get_name(skip=-2).under,
                                           parameters=common.wrap_non_empty(' ', packet.get_ruby_parameters(), ''),
                                           high_level_parameters=common.wrap_non_empty('(', packet.get_ruby_parameters(high_level=True), ')'),
                                           stream_name_space=stream_in.get_name().space,
                                           stream_name_under=stream_in.get_name().under,
                                           stream_max_length=abs(stream_in.get_data_element().get_cardinality()),
                                           fixed_length=stream_in.get_fixed_length(default='nil'),
                                           chunk_result_predefinition=chunk_result_predefinition,
                                           chunk_cardinality=stream_in.get_chunk_data_element().get_cardinality(),
                                           chunk_padding=stream_in.get_chunk_data_element().get_ruby_default_item_value(),
                                           chunk_written_0=chunk_written_0,
                                           chunk_written_n=chunk_written_n,
                                           chunk_written_test=chunk_written_test,
                                           result=result)
            elif stream_out != None:
                length_index = None
                chunk_offset_index = None
                chunk_data_index = None

                for i, element in enumerate(packet.get_elements(direction='out')):
                    if element.get_role() == 'stream_length':
                        length_index = i
                    elif element.get_role() == 'stream_chunk_offset':
                        chunk_offset_index = i
                    elif element.get_role() == 'stream_chunk_data':
                        chunk_data_index = i

                if stream_out.get_fixed_length() != None:
                    dynamic_length = ''
                    shift_size = int(stream_out.get_chunk_offset_element().get_type().replace('uint', ''))
                    chunk_offset_check = template_stream_out_chunk_offset_check.format(stream_name_under=stream_out.get_name().under,
                                                                                       shift_size=shift_size)
                    chunk_offset_check_indent = '  '
                    chunk_offset_check_end = '\n        end'
                else:
                    dynamic_length = template_stream_out_dynamic_length.format(stream_name_under=stream_out.get_name().under,
                                                                               length_index=length_index)
                    chunk_offset_check = '        '
                    chunk_offset_check_indent = ''
                    chunk_offset_check_end = ''

                if len(packet.get_elements(direction='out', high_level=True)) < 2:
                    chunk_result_predefinition = ''

                    if stream_out.has_single_chunk():
                        result = template_stream_out_single_chunk_result.format(chunk_data_index=chunk_data_index,
                                                                                length_index=length_index)
                    else:
                        result = template_stream_out_result.format(stream_name_under=stream_out.get_name().under)
                else:
                    chunk_result_predefinition = template_stream_out_chunk_result_predefinition.format(stream_name_under=stream_out.get_name().under)
                    fields = []

                    for element in packet.get_elements(direction='out', high_level=True):
                        if element.get_role() == 'stream_data':
                            if stream_out.has_single_chunk():
                                fields.append('ret[{0}][0, ret[{1}]]'.format(chunk_data_index, length_index))
                            else:
                                fields.append('{0}_data[0, {0}_length]'.format(stream_out.get_name().under))
                        else:
                            index = None

                            for i, other in enumerate(packet.get_elements(direction='out')):
                                if other.get_name().space == element.get_name().space:
                                    index = i
                                    break

                            fields.append('ret[{0}]'.format(index))

                    result = template_stream_out_namedtuple_result.format(result_fields=', '.join(fields))

                if stream_out.has_single_chunk():
                    template = template_stream_out_single_chunk
                else:
                    template = template_stream_out

                methods += template.format(doc=packet.get_ruby_formatted_doc(),
                                           function_name=packet.get_name(skip=-2).under,
                                           parameters=common.wrap_non_empty(' ', packet.get_ruby_parameters(), ''),
                                           high_level_parameters=common.wrap_non_empty('(', packet.get_ruby_parameters(high_level=True), ')'),
                                           stream_name_space=stream_out.get_name().space,
                                           stream_name_under=stream_out.get_name().under,
                                           fixed_length=stream_out.get_fixed_length(default='nil # assigned in block'),
                                           dynamic_length_4=dynamic_length.format(indent='  ' * 4),
                                           dynamic_length_5=dynamic_length.format(indent='  ' * 5),
                                           dynamic_length_6=dynamic_length.format(indent='  ' * 6),
                                           chunk_result_predefinition=chunk_result_predefinition,
                                           chunk_offset_check=chunk_offset_check,
                                           chunk_offset_check_indent=chunk_offset_check_indent,
                                           chunk_offset_check_end=chunk_offset_check_end,
                                           chunk_cardinality=stream_out.get_chunk_data_element().get_cardinality(),
                                           length_index=length_index,
                                           chunk_offset_index=chunk_offset_index,
                                           chunk_data_index=chunk_data_index,
                                           result=result)

        return methods


    def get_ruby_register_callback_method(self):
        if self.get_callback_count() == 0:
            return """
  end
end
"""

        return """
    # Registers a callback with ID <tt>id</tt> to the block <tt>block</tt>.
    def register_callback(id, &block)
      callback = block
      @registered_callbacks[id] = callback
    end
  end
end
"""

    def get_ruby_source(self):
        source  = self.get_ruby_header()
        source += self.get_ruby_class()
        source += self.get_ruby_callback_id_definitions()
        source += self.get_ruby_function_id_definitions()
        source += self.get_ruby_constants()
        source += self.get_ruby_initialize_method()
        source += self.get_ruby_response_expected()
        source += self.get_ruby_callback_formats()
        source += self.get_ruby_high_level_callbacks()
        source += self.get_ruby_methods()
        source += self.get_ruby_register_callback_method()

        return source

class RubyBindingsPacket(ruby_common.RubyPacket):
    def get_ruby_formatted_doc(self):
        text = common.select_lang(self.get_doc_text())

        # handle tables
        lines = text.split('\n')
        replaced_lines = []
        in_table_head = False
        in_table_body = False

        for line in lines:
            if line.strip() == '.. csv-table::':
                in_table_head = True
            elif line.strip().startswith(':header: ') and in_table_head:
                replaced_lines.append(line[len(':header: '):])
            elif line.strip().startswith(':widths:') and in_table_head:
                pass
            elif len(line.strip()) == 0 and in_table_head:
                in_table_head = False
                in_table_body = True

                replaced_lines.append('')
            elif len(line.strip()) == 0 and in_table_body:
                in_table_body = False
                replaced_lines.append('')
            else:
                replaced_lines.append(line)

        text = '\n'.join(replaced_lines)
        text = self.get_device().specialize_ruby_doc_function_links(text)

        def format_parameter(name):
            return name # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)
        text += common.format_since_firmware(self.get_device(), self)

        return '\n    # '.join(text.strip().split('\n'))

    def get_ruby_format_list(self, direction):
        forms = []

        for element in self.get_elements(direction=direction):
            cardinality = element.get_cardinality()

            if cardinality == 1:
                cardinality = ''

            forms.append('{0}{1}'.format(element.get_ruby_pack_format(), cardinality))

        return ' '.join(forms)

class RubyBindingsGenerator(ruby_common.RubyGeneratorTrait, common.BindingsGenerator):
    def get_device_class(self):
        return RubyBindingsDevice

    def get_packet_class(self):
        return RubyBindingsPacket

    def get_element_class(self):
        return ruby_common.RubyElement

    def prepare(self):
        common.BindingsGenerator.prepare(self)

        self.device_display_names = []

    def generate(self, device):
        filename = '{0}_{1}.rb'.format(device.get_category().under, device.get_name().under)

        with open(os.path.join(self.get_bindings_dir(), filename), 'w') as f:
            f.write(device.get_ruby_source())

        if device.is_released():
            self.device_display_names.append((device.get_device_identifier(), device.get_long_display_name()))
            self.released_files.append(filename)

    def finish(self):
        template = """# -*- ruby encoding: utf-8 -*-
{header}
module Tinkerforge
  DEVICE_DISPLAY_NAMES = {{
    {entries}
  }}

  # internal
  def get_device_display_name(device_identifier)
    device_display_name = DEVICE_DISPLAY_NAMES[device_identifier]

    if device_display_name == nil
      device_display_name = "Unknown Device [#{{device_identifier}}]"
    end

    device_display_name
  end
end
"""

        entries = []

        for device_identifier, device_display_name in sorted(self.device_display_names):
            entries.append("{0} => '{1}'".format(device_identifier, device_display_name))

        with open(os.path.join(self.get_bindings_dir(), 'device_display_names.rb'), 'w') as f:
            f.write(template.format(header=self.get_header_comment('hash'),
                                    entries=',\n    '.join(entries)))

        self.released_files.append('device_display_names.rb')

        common.BindingsGenerator.finish(self)

def generate(root_dir):
    common.generate(root_dir, 'en', RubyBindingsGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
