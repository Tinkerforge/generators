#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python Bindings Generator
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
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

device = None

def fix_links(text):
    text = text.replace(":word:`parameter`", "parameter")
    text = text.replace(":word:`parameters`", "parameters")

    return text

def make_import():
    include = """# -*- coding: utf-8 -*-
{0}
try:
    from collections import namedtuple
except ImportError:
    from .ip_connection import namedtuple
from .ip_connection import Device, IPConnection, Error

"""
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    lower_type = device.get_category().lower()

    return include.format(common.gen_text_hash.format(date),
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
            params.append("'{0}'".format(element[0]))

        tups += tup.format(name, name_tup, ", ".join(params))
    return tups
       
def make_class():
    return """
class {0}(Device):
    \"\"\"
    {1}
    \"\"\"

""".format(device.get_camel_case_name(), device.get_description())

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

def make_init_method():
    dev_init = """
    def __init__(self, uid):
        \"\"\"
        Creates an object with the unique device ID *uid*. This object can
        then be added to the IP connection.
        \"\"\"
        Device.__init__(self, uid)

        self.expected_name = '{1} {2}'

        self.binding_version = {0}

"""
    return dev_init.format(str(device.get_version()),
                           device.get_display_name(),
                           device.get_category())

def make_callback_formats():
    cbs = ''
    cb = "        self.callback_formats[{0}.CALLBACK_{1}] = '{2}'\n"
    for packet in device.get_packets('callback'):
        form = make_format_list(packet, 'out')
        cbs += cb.format(device.get_camel_case_name(), packet.get_upper_case_name(), form)
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

    if element[1] in forms:
        return forms[element[1]]

    return ''

def make_format_list(packet, io):
    forms = []
    for element in packet.get_elements(io):
        num = ''
        if element[2] > 1:
            num = element[2]
        form = make_format_from_element(element)
        forms.append('{0}{1}'.format(num, form))
    return " ".join(forms)

def make_parameter_list(packet):
    params = []
    for element in packet.get_elements('in'):
        params.append(element[0])
    return ", ".join(params)

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

    cls = device.get_camel_case_name()
    for packet in device.get_packets('function'):
        nb = packet.get_camel_case_name()
        ns = packet.get_underscore_name()
        nh = ns.upper()
        par = make_parameter_list(packet)
        doc = '\n        '.join(fix_links(common.select_lang(packet.get_doc()[1])).strip().split('\n'))
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
        Registers a callback with ID id to the function callback.
        \"\"\"
        self.registered_callbacks[id] = callback
"""

def make_files(com_new, directory):
    global device
    device = common.Device(com_new)
    file_name = '{0}_{1}'.format(device.get_category().lower(), device.get_underscore_name())
    directory += '/bindings'
    py = file('{0}/{1}.py'.format(directory, file_name), "w")
    py.write(make_import())
    py.write(make_namedtuples())
    py.write(make_class())
    py.write(make_callback_id_definitions())
    py.write(make_function_id_definitions())
    py.write(make_init_method())
    py.write(make_callback_formats())
    py.write(make_methods())
    py.write(make_register_callback_method())

if __name__ == "__main__":
    common.generate(os.getcwd(), 'en', make_files, common.prepare_bindings, False)
