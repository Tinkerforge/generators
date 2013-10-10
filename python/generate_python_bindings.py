#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python Bindings Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_python.py: Generator for Python bindings

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

device = None
released_files = []

def format_doc(packet):
    text = common.select_lang(packet.get_doc()[1])

    text = common.handle_rst_word(text)
    text = common.handle_rst_if(text, device)
    text += common.format_since_firmware(device, packet)

    return '\n        '.join(text.strip().split('\n'))

def make_import(version):
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
    lower_type = device.get_category().lower()

    return include.format(common.gen_text_hash.format(date, *version),
                          lower_type, device.get_underscore_name())

def make_namedtuples():
    tup = """{0} = namedtuple('{1}', [{2}])
"""

    tups = ''
    for packet in device.get_packets('function'):
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

def make_class():
    return """
class {0}{1}(Device):
    \"\"\"
    {2}
    \"\"\"

    DEVICE_IDENTIFIER = {3}

""".format(device.get_category(),
           device.get_camel_case_name(),
           device.get_description(),
           device.get_device_identifier())

def make_callback_id_definitions():
    cbs = ''
    cb = '    CALLBACK_{0} = {1}\n'
    for packet in device.get_packets('callback'):
        cbs += cb.format(packet.get_upper_case_name(), packet.get_function_id())
    return cbs

def make_function_id_definitions():
    function_ids = '\n'
    function_id = '    FUNCTION_{0} = {1}\n'
    for packet in device.get_packets('function'):
        function_ids += function_id.format(packet.get_upper_case_name(), packet.get_function_id())
    return function_ids

def make_constants():
    str_constants = '\n'
    str_constant = '    {0}_{1} = {2}\n'
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

def make_init_method():
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

    for packet in device.get_packets():
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

        response_expected += '        self.response_expected[{0}{1}.{2}{3}] = {0}{1}.{4}\n' \
            .format(device.get_category(), device.get_camel_case_name(), prefix, packet.get_upper_case_name(), flag)

    if len(response_expected) > 0:
        response_expected += '\n'

    return dev_init.format(*device.get_api_version()) + response_expected

def make_callback_formats():
    cbs = ''
    cb = "        self.callback_formats[{0}{1}.CALLBACK_{2}] = '{3}'\n"

    for packet in device.get_packets('callback'):
        cbs += cb.format(device.get_category(),
                         device.get_camel_case_name(),
                         packet.get_upper_case_name(),
                         make_format_list(packet, 'out'))

    return cbs

def make_format_from_element(element):
    forms = {
        'int8' : 'b',
        'uint8' : 'B',
        'int16' : 'h',
        'uint16' : 'H',
        'int32' : 'i',
        'uint32' : 'I',
        'int64' : 'q',
        'uint64' : 'Q',
        'float' : 'f',
        'bool' : '?',
        'string' : 's',
        'char' : 'c'
    }

    return forms[element.get_type()]

def make_format_list(packet, io):
    forms = []
    for element in packet.get_elements(io):
        num = ''
        if element.get_cardinality() > 1:
            num = element.get_cardinality()
        form = make_format_from_element(element)
        forms.append('{0}{1}'.format(num, form))
    return " ".join(forms)

def make_methods():
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

    cls = device.get_category() + device.get_camel_case_name()
    for packet in device.get_packets('function'):
        nb = packet.get_camel_case_name()
        ns = packet.get_underscore_name()
        nh = ns.upper()
        par = python_common.make_parameter_list(packet)
        doc = format_doc(packet)
        cp = ''
        ct = ''
        if par != '':
            cp = ', '
            if not ',' in par:
                ct = ','

        in_f = make_format_list(packet, 'in')
        out_f = make_format_list(packet, 'out')

        elements = len(packet.get_elements('out'))
        if elements > 1:
            methods += m_tup.format(ns, nb, cls, nh, par, in_f, out_f, cp, ct, doc)
        elif elements == 1:
            methods += m_ret.format(ns, cls, nh, par, in_f, out_f, cp, ct, doc)
        else:
            methods += m_nor.format(ns, cls, nh, par, in_f, out_f, cp, ct, doc)

    return methods

def make_register_callback_method():
    if len(device.get_packets('callback')) == 0:
        return ''

    return """
    def register_callback(self, id, callback):
        \"\"\"
        Registers a callback with ID *id* to the function *callback*.
        \"\"\"
        self.registered_callbacks[id] = callback
"""

def make_old_name():
    return """
{1} = {0}{1} # for backward compatibility
""".format(device.get_category(), device.get_camel_case_name())

def make_files(device_, directory):
    global device
    device = device_
    file_name = '{0}_{1}.py'.format(device.get_category().lower(), device.get_underscore_name())
    version = common.get_changelog_version(directory)
    directory += '/bindings'

    py = file('{0}/{1}'.format(directory, file_name), "w")
    py.write(make_import(version))
    py.write(make_namedtuples())
    py.write(make_class())
    py.write(make_callback_id_definitions())
    py.write(make_function_id_definitions())
    py.write(make_constants())
    py.write(make_init_method())
    py.write(make_callback_formats())
    py.write(make_methods())
    py.write(make_register_callback_method())
    py.write(make_old_name())

    if device.is_released():
        global released_files
        released_files.append(file_name)

class PythonBindingsGenerator(common.Generator):
    def prepare(self):
        common.recreate_directory(os.path.join(self.get_bindings_root_directory(), 'bindings'))

    def generate(self, device):
        make_files(device, self.get_bindings_root_directory())

    def finish(self):
        r = open(os.path.join(self.get_bindings_root_directory(), 'python_released_files.py'), 'wb')
        r.write('released_files = ' + repr(released_files))
        r.close()

def generate(path):
    common.generate(path, 'en', PythonBindingsGenerator, False)

if __name__ == "__main__":
    generate(os.getcwd())
