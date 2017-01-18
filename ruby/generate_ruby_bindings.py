#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ruby Bindings Generator
Copyright (C) 2012-2015 Matthias Bolte <matthias@tinkerforge.com>
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
        def specializer(packet):
            if packet.get_type() == 'callback':
                return 'CALLBACK_{0}'.format(packet.get_upper_case_name())
            else:
                return '{0}#{1}'.format(packet.get_device().get_ruby_class_name(),
                                        packet.get_underscore_name())

        return self.specialize_doc_function_links(text, specializer)

    def get_ruby_header(self):
        include = """# -*- ruby encoding: utf-8 -*-
{0}
"""

        return include.format(self.get_generator().get_header_comment('hash'),
                              self.get_underscore_category(),
                              self.get_underscore_name())

    def get_ruby_class(self):
        return """module Tinkerforge
  # {1}
  class {0} < Device
    DEVICE_IDENTIFIER = {2} # :nodoc:
    DEVICE_DISPLAY_NAME = '{3}' # :nodoc:
""".format(self.get_ruby_class_name(),
           common.select_lang(self.get_description()),
           self.get_device_identifier(),
           self.get_long_display_name())

    def get_ruby_callback_id_definitions(self):
        cbs = ''
        cb = """
    # {2}
    CALLBACK_{0} = {1}
"""
        for packet in self.get_packets('callback'):
            doc = packet.get_ruby_formatted_doc()
            cbs += cb.format(packet.get_upper_case_name(), packet.get_function_id(), doc)
        return cbs

    def get_ruby_function_id_definitions(self):
        function_ids = '\n'
        function_id = '    FUNCTION_{0} = {1} # :nodoc:\n'

        for packet in self.get_packets('function'):
            function_ids += function_id.format(packet.get_upper_case_name(), packet.get_function_id())

        return function_ids

    def get_ruby_constants(self):
        constant_format = '    {constant_group_upper_case_name}_{constant_upper_case_name} = {constant_value} # :nodoc:\n'

        return '\n' + self.get_formatted_constants(constant_format)

    def get_ruby_initialize_method(self):
        dev_init = """
    # Creates an object with the unique device ID <tt>uid</tt> and adds it to
    # the IP Connection <tt>ipcon</tt>.
    def initialize(uid, ipcon)
      super uid, ipcon

      @api_version = [{0}, {1}, {2}]

"""
        return dev_init.format(*self.get_api_version())

    def get_ruby_response_expected(self):
        response_expected = ''

        for packet in self.get_packets():
            if packet.get_type() == 'callback':
                prefix = 'CALLBACK'
                flag = 'RESPONSE_EXPECTED_ALWAYS_FALSE'
            elif len(packet.get_elements('out')) > 0:
                prefix = 'FUNCTION'
                flag = 'RESPONSE_EXPECTED_ALWAYS_TRUE'
            elif packet.get_doc_type() == 'ccf':
                prefix = 'FUNCTION'
                flag = 'RESPONSE_EXPECTED_TRUE'
            else:
                prefix = 'FUNCTION'
                flag = 'RESPONSE_EXPECTED_FALSE'

            response_expected += '      @response_expected[{0}_{1}] = {2}\n' \
                .format(prefix, packet.get_upper_case_name(), flag)

        return response_expected + '\n'

    def get_ruby_callback_formats(self):
        cbs = ''
        cb = "      @callback_formats[CALLBACK_{0}] = '{1}'\n"
        for packet in self.get_packets('callback'):
            form, _ = packet.get_ruby_format_list('out')
            cbs += cb.format(packet.get_upper_case_name(), form)
        return cbs + '    end\n'

    def get_ruby_methods(self):
        method0 = """
    # {4}
    def {0}
      send_request(FUNCTION_{1}, [], '', {2}, '{3}')
    end
"""
        method1 = """
    # {6}
    def {0}({1})
      send_request(FUNCTION_{2}, [{1}], '{3}', {4}, '{5}')
    end
"""
        methods = ''

        for packet in self.get_packets('function'):
            name = packet.get_underscore_name()
            fid = packet.get_upper_case_name()
            parms = packet.get_ruby_parameter_list()
            doc = packet.get_ruby_formatted_doc()

            in_format, _ = packet.get_ruby_format_list('in')
            out_format, out_size = packet.get_ruby_format_list('out')

            if len(parms) > 0:
                methods += method1.format(name, parms, fid, in_format, out_size, out_format, doc)
            else:
                methods += method0.format(name, fid, out_size, out_format, doc)

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

    def get_ruby_format_list(self, io):
        forms = []
        total_size = 0

        for element in self.get_elements(io):
            num_str = ''
            num_int = 1

            if element.get_cardinality() > 1:
                num_str = element.get_cardinality()
                num_int = element.get_cardinality()

            form, size = element.get_ruby_pack_format()
            forms.append('{0}{1}'.format(form, num_str))
            total_size += size * num_int

        return " ".join(forms), total_size

class RubyBindingsGenerator(common.BindingsGenerator):
    def get_bindings_name(self):
        return 'ruby'

    def get_bindings_display_name(self):
        return 'Ruby'

    def get_device_class(self):
        return RubyBindingsDevice

    def get_packet_class(self):
        return RubyBindingsPacket

    def get_element_class(self):
        return ruby_common.RubyElement

    def generate(self, device):
        filename = '{0}_{1}.rb'.format(device.get_underscore_category(), device.get_underscore_name())

        rb = open(os.path.join(self.get_bindings_root_directory(), 'bindings', filename), 'wb')
        rb.write(device.get_ruby_source())
        rb.close()

        if device.is_released():
            self.released_files.append(filename)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', RubyBindingsGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
