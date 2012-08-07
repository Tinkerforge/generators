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

import sys
import os
import shutil
import subprocess

sys.path.append(os.path.split(os.getcwd())[0])
import common

device = None
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
    parameter = {
    'en': 'response value',
    'de': 'Rückgabewert'
    }
    parameters = {
    'en': 'response values',
    'de': 'Rückgabewerte'
    }

    cls = device.get_camel_case_name()
    for packet in device.get_packets():
        name_false = ':func:`{0}`'.format(packet.get_camel_case_name())
        if packet.get_type() == 'callback':
            name_upper = packet.get_upper_case_name()
            name_right = ':tcpip:func:`CALLBACK_{1} <{0}.CALLBACK_{1}>`'.format(cls, name_upper)
        else:
            name_right = ':tcpip:func:`{1} <{0}.{1}>`'.format(cls, packet.get_underscore_name())
        text = text.replace(name_false, name_right)

    text = text.replace(":word:`parameter`", parameter[lang])
    text = text.replace(":word:`parameters`", parameters[lang])

    return text

def make_request_desc(packet):
    empty_payload = {
    'en': 'empty payload',
    'de': ''
    }
    desc = '\n'
    param = ' :request {0}: {1}\n'
    for element in packet.get_elements('in'):
        t = type_to_pytype(element)
        desc += param.format(element[0], t)

    if desc == '\n':
        desc += ' :emptyrequest: {0}\n'.format(empty_payload[lang])

    return desc

def make_response_desc(packet):
    empty_payload = {
    'en': 'empty payload',
    'de': ''
    }
    no_response = {
    'en': 'no response',
    'de': ''
    }
    desc = '\n'
    returns = ' :response {0}: {1}\n'
    for element in packet.get_elements('out'):
        t = type_to_pytype(element)
        desc += returns.format(element[0], t)

    if desc == '\n':
        if packet.get_type() == 'callback':
            desc += ' :emptyresponse: {0}\n'.format(empty_payload[lang])
        else:
            desc += ' :noresponse: {0}\n'.format(no_response[lang])

    return desc

def make_methods(typ):
    methods = ''
    func_start = '.. tcpip:function:: '
    cls = device.get_camel_case_name()
    for packet in device.get_packets('function'):
        if packet.get_doc()[0] != typ:
            continue
        name = packet.get_underscore_name()
        fid = '\n :functionid: {0}'.format(packet.get_function_id())
        request = make_request_desc(packet)
        response = make_response_desc(packet)
        d = fix_links(common.shift_right(packet.get_doc()[1][lang], 1))
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
    cls = device.get_camel_case_name()
    for packet in device.get_packets('callback'):
        fid = '\n :functionid: {0}'.format(packet.get_function_id())
        response = make_response_desc(packet)
        desc = fix_links(common.shift_right(packet.get_doc()[1][lang], 1))

        func = '{0}{1}.CALLBACK_{2}\n{3}\n{4}\n{5}'.format(func_start,
                                                      cls,
                                                      packet.get_upper_case_name(),
                                                      fid,
                                                      response,
                                                      desc)
        cbs += func + '\n'

    return cbs


def make_api():
    bm_str = {
    'en': """
Basic Methods
^^^^^^^^^^^^^

{0}
""",
    'de': """
"""
    }

    am_str = {
    'en': """
Advanced Methods
^^^^^^^^^^^^^^^^

{0}
""",
    'de': """
"""
    }

    ccm_str = {
    'en': """
Callback Configuration Methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

{0}
""",
    'de': """
"""
    }

    c_str = {
    'en': """
.. _{1}_{2}_tcpip_callbacks:

Callbacks
^^^^^^^^^

{0}
""",
    'de': """
"""
    }

    api = {
    'en': """
{0}

API
---

A general description of the TCP/IP protocol structure can be found
:ref:`here <llproto_tcpip>`.

{1}

{2}
""",
    'de': """
"""
    }

    bm = make_methods('bm')
    am = make_methods('am')
    ccm = make_methods('ccm')
    c = make_callbacks()
    api_str = ''
    if bm:
        api_str += bm_str[lang].format(bm)
    if am:
        api_str += am_str[lang].format(am)
    if c:
        api_str += ccm_str[lang].format(ccm)
        api_str += c_str[lang].format(c, device.get_underscore_name(),
                                      device.get_category().lower())

    ref = '.. _{0}_{1}_tcpip_api:\n'.format(device.get_underscore_name(),
                                            device.get_category().lower())

    api_desc = ''
    try:
        api_desc = device.com['api'][lang]
    except KeyError:
        pass

    return api[lang].format(ref, api_desc, api_str)

def make_files(com_new, directory):
    global device
    device = common.Device(com_new)
    file_name = '{0}_{1}_TCPIP'.format(device.get_camel_case_name(), device.get_category())
    title = {
    'en': 'TCP/IP protocol',
    'de': 'TCP/IP Protokoll'
    }

    directory += '/doc'
    if not os.path.exists(directory):
        os.makedirs(directory)

    f = file('{0}/{1}.rst'.format(directory, file_name), "w")
    f.write(common.make_rst_header(device, 'tcpip', 'TCP/IP'))
    f.write(common.make_rst_summary(device, title[lang]))
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
