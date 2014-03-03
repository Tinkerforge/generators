#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TCP/IP Documentation Generator
Copyright (C) 2012-2014 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_tcpip_doc.py: Generator for TCP/IP documentation

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

class TCPIPDocDevice(common.Device):
    def get_tcpip_name(self):
        return self.get_category() + self.get_camel_case_name()

    def get_tcpip_methods(self, typ):
        methods = ''
        func_start = '.. tcpip:function:: '
        cls = self.get_tcpip_name()

        for packet in self.get_packets('function'):
            if packet.get_doc()[0] != typ or packet.get_function_id() < 0:
                continue

            name = packet.get_underscore_name()
            fid = '\n :functionid: {0}'.format(packet.get_function_id())
            request = packet.get_tcpip_request_desc()
            response = packet.get_tcpip_response_desc()
            d = packet.get_tcpip_formatted_doc()
            desc = '{0}{1}{2}{3}'.format(fid, request, response, d)
            func = '{0}{1}.{2}\n{3}'.format(func_start, cls, name, desc)
            methods += func + '\n'

        return methods

    def get_tcpip_callbacks(self):
        cbs = ''
        func_start = '.. tcpip:function:: '
        cls = self.get_tcpip_name()

        for packet in self.get_packets('callback'):
            fid = '\n :functionid: {0}'.format(packet.get_function_id())
            response = packet.get_tcpip_response_desc()
            desc = packet.get_tcpip_formatted_doc()

            func = '{0}{1}.CALLBACK_{2}\n{3}\n{4}\n{5}'.format(func_start,
                                                               cls,
                                                               packet.get_upper_case_name(),
                                                               fid,
                                                               response,
                                                               desc)
            cbs += func + '\n'

        return cbs

    def get_tcpip_api(self):
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

        bf = self.get_tcpip_methods('bf')
        af = self.get_tcpip_methods('af')
        ccf = self.get_tcpip_methods('ccf')
        c = self.get_tcpip_callbacks()
        api_str = ''
        if bf:
            api_str += common.select_lang(common.bf_str).format('', bf)
        if af:
            api_str += common.select_lang(common.af_str).format(af)
        if ccf:
            api_str += common.select_lang(common.ccf_str).format('', ccf)
        if c:
            api_str += common.select_lang(c_str).format(c, self.get_underscore_name(),
                                                        self.get_category().lower())

        ref = '.. _{0}_{1}_tcpip_api:\n'.format(self.get_underscore_name(),
                                                self.get_category().lower())

        return common.select_lang(api).format(ref, self.get_api_doc(), api_str)

    def get_tcpip_doc(self):
        title = { 'en': 'TCP/IP protocol', 'de': 'TCP/IP Protokoll' }

        doc  = common.make_rst_header(self, 'TCP/IP', has_device_identifier_constant=False)
        doc += common.make_rst_summary(self, common.select_lang(title), is_programming_language=False)
        doc += self.get_tcpip_api()

        return doc

class TCPIPDocPacket(common.Packet):
    def get_tcpip_formatted_doc(self):
        text = common.select_lang(self.get_doc()[1])
        parameter = {
        'en': 'response value',
        'de': 'Rückgabewert'
        }
        parameters = {
        'en': 'response values',
        'de': 'Rückgabewerte'
        }

        cls = self.get_device().get_tcpip_name()
        for other_packet in self.get_device().get_packets():
            name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
            if other_packet.get_type() == 'callback':
                name_upper = other_packet.get_upper_case_name()
                name_right = ':tcpip:func:`CALLBACK_{1} <{0}.CALLBACK_{1}>`'.format(cls, name_upper)
            else:
                name_right = ':tcpip:func:`{1} <{0}.{1}>`'.format(cls, other_packet.get_underscore_name())
            text = text.replace(name_false, name_right)

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text, parameter, parameters)
        text = common.handle_rst_substitutions(text, self)
        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, 1)

    def get_tcpip_request_desc(self):
        empty_payload = {
        'en': 'empty payload',
        'de': 'keine Nutzdaten'
        }
        desc = '\n'
        param = ' :request {0}: {1}\n'

        for element in self.get_elements('in'):
            desc += param.format(element.get_underscore_name(), element.get_tcpip_type())

        if desc == '\n':
            desc += ' :emptyrequest: {0}\n'.format(common.select_lang(empty_payload))

        return desc

    def get_tcpip_response_desc(self):
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

        for element in self.get_elements('out'):
            desc += returns.format(element.get_underscore_name(), element.get_tcpip_type())

        if desc == '\n':
            if self.get_type() == 'callback':
                desc += ' :emptyresponse: {0}\n'.format(common.select_lang(empty_payload))
            else:
                desc += ' :noresponse: {0}\n'.format(common.select_lang(no_response))

        return desc

class TCPIPDocElement(common.Element):
    def get_tcpip_type(self):
        t = self.get_type()

        if t == 'string':
            t = 'char'

        if self.get_cardinality() == 1:
            return t

        return t + '[' + str(self.get_cardinality()) + ']'

class TCPIPDocGenerator(common.DocGenerator):
    def get_bindings_name(self):
        return 'tcpip'

    def get_doc_rst_name(self):
        return 'TCPIP'

    def get_doc_example_regex(self):
        return None

    def get_device_class(self):
        return TCPIPDocDevice

    def get_packet_class(self):
        return TCPIPDocPacket

    def get_element_class(self):
        return TCPIPDocElement

    def generate(self, device):
        rst = open(device.get_doc_rst_path(), 'wb')
        rst.write(device.get_tcpip_doc())
        rst.close()

def generate(bindings_root_directory, language):
    common.generate(bindings_root_directory, language, TCPIPDocGenerator)

if __name__ == "__main__":
    for language in ['en', 'de']:
        print("=== Generating %s ===" % language)
        generate(os.getcwd(), language)
