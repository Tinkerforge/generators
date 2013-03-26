#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TCP/IP Documentation Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
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

def type_to_pytype(element):
    t = element[1]

    if t == 'string':
        t = 'char'

    if element[2] == 1:
        return t

    return t + '[' + str(element[2]) + ']'

def format_doc(packet):
    text = common.select_lang(packet.get_doc()[1])
    parameter = {
    'en': 'response value',
    'de': 'Rückgabewert'
    }
    parameters = {
    'en': 'response values',
    'de': 'Rückgabewerte'
    }

    cls = device.get_camel_case_name()
    for other_packet in device.get_packets():
        name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
        if other_packet.get_type() == 'callback':
            name_upper = other_packet.get_upper_case_name()
            name_right = ':tcpip:func:`CALLBACK_{1} <{0}.CALLBACK_{1}>`'.format(cls, name_upper)
        else:
            name_right = ':tcpip:func:`{1} <{0}.{1}>`'.format(cls, other_packet.get_underscore_name())
        text = text.replace(name_false, name_right)

    text = text.replace(":word:`parameter`", common.select_lang(parameter))
    text = text.replace(":word:`parameters`", common.select_lang(parameters))

    text = common.handle_rst_if(text, device)
    text = common.handle_since_firmware(text, device, packet)

    return common.shift_right(text, 1)

def make_request_desc(packet):
    empty_payload = {
    'en': 'empty payload',
    'de': 'keine Nutzdaten'
    }
    desc = '\n'
    param = ' :request {0}: {1}\n'
    for element in packet.get_elements('in'):
        t = type_to_pytype(element)
        desc += param.format(element[0], t)

    if desc == '\n':
        desc += ' :emptyrequest: {0}\n'.format(common.select_lang(empty_payload))

    return desc

def make_response_desc(packet):
    empty_payload = {
    'en': 'empty payload',
    'de': 'keine Nutzdaten'
    }
    no_response = {
    'en': 'no response',
    'de': 'keine Antwort'
    }
    desc = '\n'
    returns = ' :response {0}: {1}\n'
    for element in packet.get_elements('out'):
        t = type_to_pytype(element)
        desc += returns.format(element[0], t)

    if desc == '\n':
        if packet.get_type() == 'callback':
            desc += ' :emptyresponse: {0}\n'.format(common.select_lang(empty_payload))
        else:
            desc += ' :noresponse: {0}\n'.format(common.select_lang(no_response))

    return desc

def make_methods(typ):
    methods = ''
    func_start = '.. tcpip:function:: '
    cls = device.get_camel_case_name()
    for packet in device.get_packets('function'):
        if packet.get_doc()[0] != typ or packet.get_function_id() < 0:
            continue
        name = packet.get_underscore_name()
        fid = '\n :functionid: {0}'.format(packet.get_function_id())
        request = make_request_desc(packet)
        response = make_response_desc(packet)
        d = format_doc(packet)
        desc = '{0}{1}{2}{3}'.format(fid, request, response, d)
        func = '{0}{1}.{2}\n{3}'.format(func_start, cls, name, desc)
        methods += func + '\n'

    return methods

def make_callbacks():
    cbs = ''
    func_start = '.. tcpip:function:: '
    cls = device.get_camel_case_name()
    for packet in device.get_packets('callback'):
        fid = '\n :functionid: {0}'.format(packet.get_function_id())
        response = make_response_desc(packet)
        desc = format_doc(packet)

        func = '{0}{1}.CALLBACK_{2}\n{3}\n{4}\n{5}'.format(func_start,
                                                           cls,
                                                           packet.get_upper_case_name(),
                                                           fid,
                                                           response,
                                                           desc)
        cbs += func + '\n'

    return cbs


def make_api():
    c_str = {
    'en': """
.. _{1}_{2}_tcpip_callbacks:

Callbacks
^^^^^^^^^

{0}
""",
    'de': """
.. _{1}_{2}_tcpip_callbacks:

Callbacks
^^^^^^^^^

{0}
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
{0}

API
---

Eine allgemeine Beschreibung der TCP/IP Protokollstruktur findet sich
:ref:`hier <llproto_tcpip>`.

{1}

{2}
"""
    }

    const_str = {
    'en' : """
Constants
^^^^^^^^^

.. tcpip:attribute:: {0}.DEVICE_IDENTIFIER

 :value: {3}

 This constant is used to identify a {0} {1}.

 The :tcpip:func:`get_identity <{0}.get_identity>` function and the
 :tcpip:func:`CALLBACK_ENUMERATE <CALLBACK_ENUMERATE>`
 callback of the IP Connection have a ``device_identifier`` parameter to specify
 the Brick's or Bricklet's type.
""",
    'de' : """
Konstanten
^^^^^^^^^^

.. tcpip:attribute:: {0}.DEVICE_IDENTIFIER

 :value: {3}

 Diese Konstante wird verwendet um {2} {0} {1} zu identifizieren.

 Die :tcpip:func:`get_identity <{0}.get_identity>` Funktion und der
 :tcpip:func:`CALLBACK_ENUMERATE <CALLBACK_ENUMERATE>`
 Callback der IP Connection haben ein ``device_identifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.
"""
    }

    bf = make_methods('bf')
    af = make_methods('af')
    ccf = make_methods('ccf')
    c = make_callbacks()
    api_str = ''
    if bf:
        api_str += common.select_lang(common.bf_str).format(bf, '')
    if af:
        api_str += common.select_lang(common.af_str).format(af)
    if ccf:
        api_str += common.select_lang(common.ccf_str).format(ccf, '')
    if c:
        api_str += common.select_lang(c_str).format(c, device.get_underscore_name(),
                                                    device.get_category().lower())

    article = 'ein'
    if device.get_category() == 'Brick':
        article = 'einen'
    api_str += common.select_lang(const_str).format(device.get_camel_case_name(),
                                                    device.get_category(),
                                                    article,
                                                    device.get_device_identifier())

    ref = '.. _{0}_{1}_tcpip_api:\n'.format(device.get_underscore_name(),
                                            device.get_category().lower())

    api_desc = ''
    if 'api' in device.com:
        api_desc = common.select_lang(device.com['api'])

    return common.select_lang(api).format(ref, api_desc, api_str)

def make_files(com_new, directory):
    global device
    device = common.Device(com_new)
    file_name = '{0}_{1}_TCPIP'.format(device.get_camel_case_name(), device.get_category())
    title = {
    'en': 'TCP/IP protocol',
    'de': 'TCP/IP Protokoll'
    }
    directory = os.path.join(directory, 'doc', common.lang)
    f = file('{0}/{1}.rst'.format(directory, file_name), "w")
    f.write(common.make_rst_header(device, 'tcpip', 'TCP/IP'))
    f.write(common.make_rst_summary(device, common.select_lang(title)))
    f.write(make_api())

if __name__ == "__main__":
    for lang in ['en', 'de']:
        print("=== Generating %s ===" % lang)
        common.generate(os.getcwd(), lang, make_files, common.prepare_doc, None, True)
