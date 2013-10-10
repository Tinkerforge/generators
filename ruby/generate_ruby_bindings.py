#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ruby Bindings Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_ruby.py: Generator for Ruby bindings

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

import datetime
import sys
import os

sys.path.append(os.path.split(os.getcwd())[0])
import common
import ruby_common

device = None

def format_doc(packet):
    text = common.select_lang(packet.get_doc()[1])
    link = '{0}#{1}'
    link_c = 'CALLBACK_{0}'

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

    cls = device.get_ruby_class_name()
    for other_packet in device.get_packets():
        name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
        if other_packet.get_type() == 'callback':
            name = other_packet.get_upper_case_name()
            name_right = link_c.format(name)
        else:
            name = other_packet.get_underscore_name()
            name_right = link.format(cls, name)

        text = text.replace(name_false, name_right)

    text = common.handle_rst_word(text)
    text = common.handle_rst_if(text, device)
    text += common.format_since_firmware(device, packet)

    return '\n    # '.join(text.strip().split('\n'))

def make_header(version):
    include = """# -*- ruby encoding: utf-8 -*-
{0}
"""
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    lower_type = device.get_category().lower()

    return include.format(common.gen_text_hash.format(date, *version),
                          lower_type, device.get_underscore_name())

def make_class():
    return """module Tinkerforge
  # {1}
  class {0} < Device
    DEVICE_IDENTIFIER = {2} # :nodoc:
""".format(device.get_ruby_class_name(), device.get_description(), device.get_device_identifier())

def make_callback_id_definitions():
    cbs = ''
    cb = """
    # {2}
    CALLBACK_{0} = {1}
"""
    for packet in device.get_packets('callback'):
        doc = format_doc(packet)
        cbs += cb.format(packet.get_upper_case_name(), packet.get_function_id(), doc)
    return cbs

def make_function_id_definitions():
    function_ids = '\n'
    function_id = '    FUNCTION_{0} = {1} # :nodoc:\n'
    for packet in device.get_packets('function'):
        function_ids += function_id.format(packet.get_upper_case_name(), packet.get_function_id())
    return function_ids

def make_constants():
    str_constants = '\n'
    str_constant = '    {0}_{1} = {2} # :nodoc:\n'
    constants = device.get_constants()
    for constant in constants:
        for definition in constant.definitions:
            if constant.type == 'char':
                value = "'{0}'".format(definition.value)
            else:
                value = str(definition.value)

            str_constants += str_constant.format(constant.name_uppercase,
                                                 definition.name_uppercase,
                                                 value)
    return str_constants

def make_initialize_method():
    dev_init = """
    # Creates an object with the unique device ID <tt>uid</tt> and adds it to
    # the IP Connection <tt>ipcon</tt>.
    def initialize(uid, ipcon)
      super uid, ipcon

      @api_version = [{0}, {1}, {2}]

"""
    return dev_init.format(*device.get_api_version())

def make_response_expected():
    response_expected = ''

    for packet in device.get_packets():
        if packet.get_type() == 'callback':
            prefix = 'CALLBACK'
            flag = 'RESPONSE_EXPECTED_ALWAYS_FALSE'
        elif len(packet.get_elements('out')) > 0:
            prefix = 'FUNCTION'
            flag = 'RESPONSE_EXPECTED_ALWAYS_TRUE'
        elif packet.get_doc()[0] == 'ccf':
            prefix = 'FUNCTION'
            flag = 'RESPONSE_EXPECTED_TRUE'
        else:
            prefix = 'FUNCTION'
            flag = 'RESPONSE_EXPECTED_FALSE'

        response_expected += '      @response_expected[{0}_{1}] = {2}\n' \
            .format(prefix, packet.get_upper_case_name(), flag)

    return response_expected + '\n'

def make_callback_formats():
    cbs = ''
    cb = "      @callback_formats[CALLBACK_{0}] = '{1}'\n"
    for packet in device.get_packets('callback'):
        form, _ = make_format_list(packet, 'out')
        cbs += cb.format(packet.get_upper_case_name(), form)
    return cbs + '    end\n'

def make_format_from_element(element):
    forms = {
        'int8'   : ('c', 1),
        'uint8'  : ('C', 1),
        'int16'  : ('s', 2),
        'uint16' : ('S', 2),
        'int32'  : ('l', 4),
        'uint32' : ('L', 4),
        'int64'  : ('q', 8),
        'uint64' : ('Q', 8),
        'float'  : ('e', 4),
        'bool'   : ('?', 1),
        'string' : ('Z', 1),
        'char'   : ('k', 1)
    }

    return forms[element.get_type()]

def make_format_list(packet, io):
    forms = []
    total_size = 0
    for element in packet.get_elements(io):
        num_str = ''
        num_int = 1
        if element.get_cardinality() > 1:
            num_str = element.get_cardinality()
            num_int = element.get_cardinality()
        form, size = make_format_from_element(element)
        forms.append('{0}{1}'.format(form, num_str))
        total_size += size * num_int
    return " ".join(forms), total_size

def make_methods():
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

    for packet in device.get_packets('function'):
        name = packet.get_underscore_name()
        fid = packet.get_upper_case_name()
        parms = ruby_common.make_parameter_list(packet)
        doc = format_doc(packet)

        in_format, _ = make_format_list(packet, 'in')
        out_format, out_size = make_format_list(packet, 'out')

        if len(parms) > 0:
            methods += method1.format(name, parms, fid, in_format, out_size, out_format, doc)
        else:
            methods += method0.format(name, fid, out_size, out_format, doc)

    return methods

def make_register_callback_method():
    if device.get_callback_count() == 0:
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

class RubyBindingsGenerator(common.BindingsGenerator):
    def __init__(self, *args, **kwargs):
        common.BindingsGenerator.__init__(self, *args, **kwargs)

        self.released_files_name_prefix = 'ruby'

    def get_device_class(self):
        return ruby_common.RubyDevice

    def generate(self, device_):
        global device
        device = device_

        version = common.get_changelog_version(self.get_bindings_root_directory())
        file_name = '{0}_{1}.rb'.format(device.get_category().lower(), device.get_underscore_name())

        rb = open(os.path.join(self.get_bindings_root_directory(), 'bindings', file_name), 'wb')
        rb.write(make_header(version))
        rb.write(make_class())
        rb.write(make_callback_id_definitions())
        rb.write(make_function_id_definitions())
        rb.write(make_constants())
        rb.write(make_initialize_method())
        rb.write(make_response_expected())
        rb.write(make_callback_formats())
        rb.write(make_methods())
        rb.write(make_register_callback_method())
        rb.close()

        if device.is_released():
            self.released_files.append(file_name)

def generate(path):
    common.generate(path, 'en', RubyBindingsGenerator, False)

if __name__ == "__main__":
    generate(os.getcwd())
