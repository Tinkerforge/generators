#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ruby Bindings Generator
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
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

device = None

def fix_links(text):
    link = '{0}{1}#{2}'
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

    cls = device.get_camel_case_name()
    for packet in device.get_packets():
        name_false = ':func:`{0}`'.format(packet.get_camel_case_name())
        if packet.get_type() == 'callback':
            name = packet.get_upper_case_name()
            name_right = link_c.format(name)
        else:
            name = packet.get_underscore_name()
            name_right = link.format(device.get_category(), cls, name)

        text = text.replace(name_false, name_right)

    text = text.replace(":word:`parameter`", "parameter")
    text = text.replace(":word:`parameters`", "parameters")

    return text

def make_header():
    include = """# -*- ruby encoding: utf-8 -*-
{0}
"""
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    lower_type = device.get_category().lower()

    return include.format(common.gen_text_hash.format(date),
                          lower_type, device.get_underscore_name())

def make_class():
    return """module Tinkerforge
  # {2}
  class {0}{1} < Device
""".format(device.get_category(), device.get_camel_case_name(), device.get_description())

def make_callback_id_definitions():
    cbs = ''
    cb = """
    # {2}
    CALLBACK_{0} = {1}
"""
    for packet in device.get_packets('callback'):
        doc = '\n    # '.join(fix_links(common.select_lang(packet.get_doc()[1])).strip().split('\n'))
        cbs += cb.format(packet.get_upper_case_name(), packet.get_function_id(), doc)
    return cbs

def make_function_id_definitions():
    function_ids = '\n'
    function_id = '    FUNCTION_{0} = {1} # :nodoc:\n'
    for packet in device.get_packets('function'):
        function_ids += function_id.format(packet.get_upper_case_name(), packet.get_function_id())
    return function_ids

def make_initialize_method():
    dev_init = """
    # Creates an object with the unique device ID <tt>uid</tt>. This object can
    # then be added to the IP connection.
    def initialize(uid)
      super uid

      @expected_name = '{3} {4}'

      @binding_version = [{0}, {1}, {2}]

"""
    v = device.get_version()
    return dev_init.format(v[0], v[1], v[2],
                           device.get_display_name(),
                           device.get_category())

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

    if element[1] in forms:
        return forms[element[1]]

    return '', 0

def make_format_list(packet, io):
    forms = []
    total_size = 0
    for element in packet.get_elements(io):
        num_str = ''
        num_int = 1
        if element[2] > 1:
            num_str = element[2]
            num_int = element[2]
        form, size = make_format_from_element(element)
        forms.append('{0}{1}'.format(form, num_str))
        total_size += size * num_int
    return " ".join(forms), total_size

def make_parameter_list(packet):
    params = []
    for element in packet.get_elements('in'):
        params.append(element[0])
    return ', '.join(params)

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
        parms = make_parameter_list(packet)
        doc = '\n    # '.join(fix_links(common.select_lang(packet.get_doc()[1])).strip().split('\n'))

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
    # Registers a callback with ID <tt>cb</tt> to the block <tt>block</tt>.
    def register_callback(cb, &block)
      callback = block
      @registered_callbacks[cb] = callback
    end
  end
end
"""

def make_files(com_new, directory):
    global device
    device = common.Device(com_new)

    file_name = '{0}_{1}'.format(device.get_category().lower(), device.get_underscore_name())

    directory += '/bindings'
    if not os.path.exists(directory):
        os.makedirs(directory)

    py = file('{0}/{1}.rb'.format(directory, file_name), "w")
    py.write(make_header())
    py.write(make_class())
    py.write(make_callback_id_definitions())
    py.write(make_function_id_definitions())
    py.write(make_initialize_method())
    py.write(make_callback_formats())
    py.write(make_methods())
    py.write(make_register_callback_method())

if __name__ == "__main__":
    common.generate(os.getcwd(), lang, make_files)
