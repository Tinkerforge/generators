#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python Bindings Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
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

import datetime
import sys
import os

sys.path.append(os.path.split(os.getcwd())[0])
import common
import python_common

class PythonBindingsDevice(python_common.PythonDevice):
    def get_python_import(self):
        include = """# -*- coding: utf-8 -*-
{0}
try:
    from collections import namedtuple
except ImportError:
    try:
        from .ip_connection import namedtuple
    except ValueError:
        from ip_connection import namedtuple

try:
    from .ip_connection import Device, IPConnection, Error
except ValueError:
    from ip_connection import Device, IPConnection, Error

"""
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        version = common.get_changelog_version(self.get_generator().get_bindings_root_directory())
        lower_type = self.get_category().lower()

        return include.format(common.gen_text_hash.format(date, *version),
                              lower_type, self.get_underscore_name())

    def get_python_namedtuples(self):
        tup = """{0} = namedtuple('{1}', [{2}])
"""

        tups = ''
        for packet in self.get_packets('function'):
            if len(packet.get_elements('out')) < 2:
                continue

            name = packet.get_camel_case_name()
            name_tup = name
            if name_tup.startswith('Get'):
                name_tup = name_tup[3:]
            params = []
            for element in packet.get_elements('out'):
                params.append("'{0}'".format(element.get_underscore_name()))

            tups += tup.format(name, name_tup, ", ".join(params))
        return tups

    def get_python_class(self):
        return """
class {0}(Device):
    \"\"\"
    {1}
    \"\"\"

    DEVICE_IDENTIFIER = {2}

""".format(self.get_python_class_name(),
           self.get_description(),
           self.get_device_identifier())

    def get_python_callback_id_definitions(self):
        cbs = ''
        cb = '    CALLBACK_{0} = {1}\n'
        for packet in self.get_packets('callback'):
            cbs += cb.format(packet.get_upper_case_name(), packet.get_function_id())
        return cbs

    def get_python_function_id_definitions(self):
        function_ids = '\n'
        function_id = '    FUNCTION_{0} = {1}\n'
        for packet in self.get_packets('function'):
            function_ids += function_id.format(packet.get_upper_case_name(), packet.get_function_id())
        return function_ids

    def get_python_constants(self):
        constant_format = '    {constant_group_upper_case_name}_{constant_item_upper_case_name} = {constant_item_value}\n'

        return '\n' + self.get_formatted_constants(constant_format)

    def get_python_init_method(self):
        dev_init = """
    def __init__(self, uid, ipcon):
        \"\"\"
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        \"\"\"
        Device.__init__(self, uid, ipcon)

        self.api_version = ({0}, {1}, {2})

"""
        response_expected = ''

        for packet in self.get_packets():
            if packet.get_type() == 'callback':
                prefix = 'CALLBACK_'
                flag = 'RESPONSE_EXPECTED_ALWAYS_FALSE'
            elif len(packet.get_elements('out')) > 0:
                prefix = 'FUNCTION_'
                flag = 'RESPONSE_EXPECTED_ALWAYS_TRUE'
            elif packet.get_doc()[0] == 'ccf':
                prefix = 'FUNCTION_'
                flag = 'RESPONSE_EXPECTED_TRUE'
            else:
                prefix = 'FUNCTION_'
                flag = 'RESPONSE_EXPECTED_FALSE'

            response_expected += '        self.response_expected[{0}.{1}{2}] = {0}.{3}\n' \
                .format(self.get_python_class_name(), prefix, packet.get_upper_case_name(), flag)

        if len(response_expected) > 0:
            response_expected += '\n'

        return dev_init.format(*self.get_api_version()) + response_expected

    def get_python_callback_formats(self):
        cbs = ''
        cb = "        self.callback_formats[{0}.CALLBACK_{1}] = '{2}'\n"

        for packet in self.get_packets('callback'):
            cbs += cb.format(self.get_python_class_name(),
                             packet.get_upper_case_name(),
                             packet.get_python_format_list('out'))

        return cbs

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
        for packet in self.get_packets('function'):
            nb = packet.get_camel_case_name()
            ns = packet.get_underscore_name()
            nh = ns.upper()
            par = packet.get_python_parameter_list()
            doc = packet.get_python_formatted_doc()
            cp = ''
            ct = ''
            if par != '':
                cp = ', '
                if not ',' in par:
                    ct = ','

            in_f = packet.get_python_format_list('in')
            out_f = packet.get_python_format_list('out')

            elements = len(packet.get_elements('out'))
            if elements > 1:
                methods += m_tup.format(ns, nb, cls, nh, par, in_f, out_f, cp, ct, doc)
            elif elements == 1:
                methods += m_ret.format(ns, cls, nh, par, in_f, out_f, cp, ct, doc)
            else:
                methods += m_nor.format(ns, cls, nh, par, in_f, out_f, cp, ct, doc)

        return methods

    def get_python_register_callback_method(self):
        if len(self.get_packets('callback')) == 0:
            return ''

        return """
    def register_callback(self, id, callback):
        \"\"\"
        Registers a callback with ID *id* to the function *callback*.
        \"\"\"
        self.registered_callbacks[id] = callback
"""

    def get_python_old_name(self):
        return """
{0} = {1} # for backward compatibility
""".format(self.get_camel_case_name(), self.get_python_class_name())

    def get_python_source(self):
        source  = self.get_python_import()
        source += self.get_python_namedtuples()
        source += self.get_python_class()
        source += self.get_python_callback_id_definitions()
        source += self.get_python_function_id_definitions()
        source += self.get_python_constants()
        source += self.get_python_init_method()
        source += self.get_python_callback_formats()
        source += self.get_python_methods()
        source += self.get_python_register_callback_method()
        source += self.get_python_old_name()

        return source

class PythonBindingsPacket(python_common.PythonPacket):
    def get_python_formatted_doc(self):
        text = common.select_lang(self.get_doc()[1])

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)
        text += common.format_since_firmware(self.get_device(), self)

        return '\n        '.join(text.strip().split('\n'))

    def get_python_format_list(self, io):
        forms = []

        for element in self.get_elements(io):
            forms.append(element.get_python_struct_format())

        return ' '.join(forms)

class PythonBindingsGenerator(common.BindingsGenerator):
    released_files_name_prefix = 'python'

    def get_bindings_name(self):
        return 'python'

    def get_device_class(self):
        return PythonBindingsDevice

    def get_packet_class(self):
        return PythonBindingsPacket

    def get_element_class(self):
        return python_common.PythonElement

    def generate(self, device):
        filename = '{0}_{1}.py'.format(device.get_category().lower(), device.get_underscore_name())

        py = open(os.path.join(self.get_bindings_root_directory(), 'bindings', filename), 'wb')
        py.write(device.get_python_source())
        py.close()

        if device.is_released():
            self.released_files.append(filename)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', PythonBindingsGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
