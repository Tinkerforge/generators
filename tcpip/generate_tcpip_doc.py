#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TCP/IP Documentation Generator
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_tcpip_doc.py: Generator for TCP/IP documentation

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
import shutil
import subprocess

sys.path.append(os.path.split(os.getcwd())[0])
import common

com = None
lang = 'en'
file_path = ''

def type_to_pytype(element):
    t = element[1]

    if t == 'string':
        t = 'char'

    if element[2] == 1:
        return t

    return t + '[' + str(element[2]) + ']'

def fix_links(text):
    cls = com['name'][0]
    for packet in com['packets']:
        name_false = ':func:`{0}`'.format(packet['name'][0])
        if packet['type'] == 'callback':
            name_upper = packet['name'][1].upper()
            name_right = ':tcpip:func:`{0}.CALLBACK_{1}`'.format(cls, name_upper)
        else:
            name_right = ':tcpip:func:`{0}.{1}`'.format(cls, packet['name'][1])
        text = text.replace(name_false, name_right)

    text = text.replace(":word:`parameter`", "response value")
    text = text.replace(":word:`parameters`", "response values")

    return text

def make_header():
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    ref = '.. _{0}_{1}_tcpip:\n'.format(com['name'][1], com['type'].lower())
    name = common.camel_case_to_space(com['name'][0])
    title = 'TCP/IP - {0} {1}'.format(name, com['type'])
    title_under = '='*len(title)
    return '{0}\n{1}\n{2}\n{3}\n'.format(common.gen_text_rst.format(date),
                                         ref,
                                         title,
                                         title_under)

def make_summary():
    su = """
This is the API site for the TCP/IP protocol of the {0} {1}. General information
on what this device does and the technical specifications can be found
:ref:`here <{2}>`.

A tutorial on how to test the {0} {1} and get the first examples running
can be found :ref:`here <{3}>`.
"""

    hw_link = com['name'][1] + '_' + com['type'].lower()
    hw_test = hw_link + '_test'
    name = common.camel_case_to_space(com['name'][0])
    su = su.format(name, com['type'], hw_link, hw_test)
    return su

def make_request_desc(packet):
    desc = '\n'
    param = ' :request {0}: {1}\n'
    for element in packet['elements']:
        if element[3] != 'in':
            continue
        t = type_to_pytype(element)
        desc += param.format(element[0], t)

    if desc == '\n':
        desc += ' :emptyrequest: empty payload\n'

    return desc

def make_response_desc(packet):
    desc = '\n'
    returns = ' :response {0}: {1}\n'
    for element in packet['elements']:
        if element[3] != 'out':
            continue
        t = type_to_pytype(element)
        desc += returns.format(element[0], t)

    if desc == '\n':
        if packet['type'] == 'callback':
            desc += ' :emptyresponse: empty payload\n'
        else:
            desc += ' :noresponse: no response\n'

    return desc

def make_methods(typ):
    methods = ''
    func_start = '.. tcpip:function:: '
    cls = com['name'][0]
    for packet in com['packets']:
        if packet['type'] != 'function' or packet['doc'][0] != typ:
            continue
        name = packet['name'][1]
        fid = '\n :functionid: {0}'.format(packet['function_id'])
        request = make_request_desc(packet)
        response = make_response_desc(packet)
        d = fix_links(common.shift_right(packet['doc'][1][lang], 1))
        desc = '{0}{1}{2}{3}'.format(fid, request, response, d)
        func = '{0}{1}.{2}\n{3}'.format(func_start,
                                             cls,
                                             name,
                                             desc)
        methods += func + '\n'

    return methods

def make_callbacks():
    cbs = ''
    func_start = '.. tcpip:function:: '
    cls = com['name'][0]
    pt = 1
    for packet in com['packets']:
        pt += 1
        if packet['type'] != 'callback':
            continue

        fid = '\n :functionid: {0}'.format(packet['function_id'])
        response = make_response_desc(packet)
        desc = fix_links(common.shift_right(packet['doc'][1][lang], 1))

        func = '{0}{1}.CALLBACK_{2}\n{3}\n{4}\n{5}'.format(func_start,
                                                      cls,
                                                      packet['name'][1].upper(),
                                                      fid,
                                                      response,
                                                      desc)
        cbs += func + '\n'

    return cbs


def make_api():
    bm_str = """
Basic Methods
^^^^^^^^^^^^^

{0}
"""

    am_str = """
Advanced Methods
^^^^^^^^^^^^^^^^

{0}
"""

    ccm_str = """
Callback Configuration Methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

{0}
"""

    c_str = """
.. _{1}_{2}_tcpip_callbacks:

Callbacks
^^^^^^^^^

{0}
"""

    api = """
{0}

API
---

A general description of the TCP/IP protocol structure can be found
:ref:`here <ipcon_tcpip_protocol>`.

{1}

{2}
"""

    bm = make_methods('bm')
    am = make_methods('am')
    ccm = make_methods('ccm')
    c = make_callbacks()
    api_str = ''
    if bm:
        api_str += bm_str.format(bm)
    if am:
        api_str += am_str.format(am)
    if c:
        api_str += ccm_str.format(ccm)
        api_str += c_str.format(c, com['name'][1], com['type'].lower())

    ref = '.. _{0}_{1}_tcpip_api:\n'.format(com['name'][1],
                                            com['type'].lower())

    api_desc = ''
    try:
        api_desc = com['api']
    except:
        pass

    return api.format(ref, api_desc, api_str)

def make_files(com_new, directory):
    global com
    com = com_new

    for i, packet in zip(range(len(com['packets'])), com['packets']):
        packet['function_id'] = i + 1

    file_name = '{0}_{1}_TCPIP'.format(com['name'][0], com['type'])

    directory += '/doc'
    if not os.path.exists(directory):
        os.makedirs(directory)

    f = file('{0}/{1}.rst'.format(directory, file_name), "w")
    f.write(make_header())
    f.write(make_summary())
    f.write(make_api())

def generate(path):
    global file_path
    file_path = path
    path_list = path.split('/')
    path_list[-1] = 'configs'
    path_config = '/'.join(path_list)
    sys.path.append(path_config)
    configs = os.listdir(path_config)

    # Make temporary generator directory
    if os.path.exists('/tmp/generator'):
        shutil.rmtree('/tmp/generator/')
    os.makedirs('/tmp/generator')
    os.chdir('/tmp/generator')

    for config in configs:
        if config.endswith('_config.py'):
            module = __import__(config[:-3])
            print(" * {0}".format(config[:-10]))
            make_files(module.com, path)

if __name__ == "__main__":
    generate(os.getcwd())
