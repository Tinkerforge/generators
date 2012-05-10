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

com = None

gen_text = """# -*- coding: utf-8 -*-
#############################################################
# This file was automatically generated on {0}.      #
#                                                           #
# If you have a bugfix for this file and want to commit it, #
# please fix the bug in the generator. You can find a link  #
# to the generator git on tinkerforge.com                   #
#############################################################
"""

def make_import():
    include = """{0}
try:
    from collections import namedtuple
except ImportError:
    from ip_connection import namedtuple
from ip_connection import Device, IPConnection, Error

"""
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    lower_type = com['type'].lower()

    return include.format(gen_text.format(date), lower_type, com['name'][1])

def make_namedtuples():
    tup = """{0} = namedtuple('{1}', [{2}])
"""

    tups = ''
    for packet in com['packets']:
        elements_out = 0
        for element in packet['elements']:
            if element[3] == 'out':
                elements_out += 1
            
        if elements_out < 2 or packet['type'] != 'method':
            continue

        name = packet['name'][0]
        name_tup = name
        if name_tup.startswith('Get'):
            name_tup = name_tup[3:]
        params = []
        for element in packet['elements']:
            if element[3] == 'out':
                params.append("'{0}'".format(element[0]))

        tups += tup.format(name, name_tup, ", ".join(params))
    return tups
       
def make_class():
    return '\nclass {0}(Device):\n'.format(com['name'][0])

def make_callback_definitions():
    cbs = ''
    cb = '    CALLBACK_{0} = {1}\n'
    for i, packet in zip(range(len(com['packets'])), com['packets']):
        if packet['type'] != 'signal':
            continue
        cbs += cb.format(packet['name'][1].upper(), i+1)
    return cbs

def make_type_definitions():
    types = '\n'
    type = '    TYPE_{0} = {1}\n'
    for i, packet in zip(range(len(com['packets'])), com['packets']):
        types += type.format(packet['name'][1].upper(), i+1)
    return types

def make_init_method():
    dev_init = """
    def __init__(self, uid):
        Device.__init__(self, uid)

        self.binding_version = {0}

"""
    return dev_init.format(str(com['version']))

def make_callbacks_format():
    cbs = ''
    cb = "        self.callbacks_format[{0}.CALLBACK_{1}] = '{2}'\n"
    for i, packet in zip(range(len(com['packets'])), com['packets']):
        if packet['type'] != 'signal':
            continue
        form = make_format_list(packet, 'out')
        cbs += cb.format(com['name'][0], packet['name'][1].upper(), form)
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
    for element in packet['elements']:
        if element[3] != io:
            continue
        num = ''
        if element[2] > 1:
            num = element[2]
        form = make_format_from_element(element)
        forms.append('{0}{1}'.format(num, form))
    return " ".join(forms)

def make_parameter_list(packet):
    params = []
    for element in packet['elements']:
        if element[3] != 'in':
            continue
        params.append(element[0])
    return ", ".join(params)

def make_methods():
    def get_typ_elements(packet, typ):
        i = 0
        for element in packet['elements']:
            if element[3] == typ:
                i += 1
        return i
            
    m_tup = """
    def {0}(self{7}{4}):
        return {1}(*self.ipcon.write(self, {2}.TYPE_{3}, ({4}{8}), '{5}', '{6}'))
"""
    m_ret = """
    def {0}(self{6}{3}):
        return self.ipcon.write(self, {1}.TYPE_{2}, ({3}{7}), '{4}', '{5}')
"""
    m_nor = """
    def {0}(self{6}{3}):
        self.ipcon.write(self, {1}.TYPE_{2}, ({3}{7}), '{4}', '{5}')
"""
    methods = ''

    cls = com['name'][0]
    for packet in com['packets']:
        if packet['type'] != 'method':
            continue

        nb = packet['name'][0]
        ns = packet['name'][1]
        nh = ns.upper()
        par = make_parameter_list(packet)
        cp = ''
        ct = ''
        if par != '':
            cp = ', '
            if not ',' in par:
                ct = ','

        in_f = make_format_list(packet, 'in')
        out_f = make_format_list(packet, 'out')

        elements =  get_typ_elements(packet, 'out')
        if elements > 1:
            methods += m_tup.format(ns, nb, cls, nh, par, in_f, out_f, cp, ct)
        elif elements == 1:
            methods += m_ret.format(ns, cls, nh, par, in_f, out_f, cp, ct)
        else:
            methods += m_nor.format(ns, cls, nh, par, in_f, out_f, cp, ct)

    return methods

def make_register_callback_method():
    signal_count = 0
    for packet in com['packets']:
        if packet['type'] == 'signal':
            signal_count += 1

    if signal_count == 0:
        return ''

    return """
    def register_callback(self, cb, func):
        self.callbacks[cb] = func
"""

def make_files(com_new, directory):
    global com
    com = com_new

    file_name = '{0}_{1}'.format(com['type'].lower(), com['name'][1])
    
    directory += '/bindings'
    if not os.path.exists(directory):
        os.makedirs(directory)

    py = file('{0}/{1}.py'.format(directory, file_name), "w")
    py.write(make_import())
    py.write(make_namedtuples())
    py.write(make_class())
    py.write(make_callback_definitions())
    py.write(make_type_definitions())
    py.write(make_init_method())
    py.write(make_callbacks_format())
    py.write(make_methods())
    py.write(make_register_callback_method())

def generate(path):
    path_list = path.split('/')
    path_list[-1] = 'configs'
    path_config = '/'.join(path_list)
    sys.path.append(path_config)
    configs = os.listdir(path_config)

    for config in configs:
        if config.endswith('_config.py'):
            module = __import__(config[:-3])
            print(" * {0}".format(config[:-10]))            
            make_files(module.com, path)

if __name__ == "__main__":
    generate(os.getcwd())
