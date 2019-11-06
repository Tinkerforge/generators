#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TCP/IP Documentation Generator
Copyright (C) 2012-2014, 2016-2019 Matthias Bolte <matthias@tinkerforge.com>
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
        return self.get_category().camel + self.get_name().camel

    def specialize_tcpip_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return ':tcpip:func:`CALLBACK_{1} <{0}.CALLBACK_{1}>`'.format(packet.get_device().get_tcpip_name(),
                                                                              packet.get_name().upper)
            else:
                return ':tcpip:func:`{1} <{0}.{1}>`'.format(packet.get_device().get_tcpip_name(),
                                                            packet.get_name().under)

        return self.specialize_doc_rst_links(text, specializer, prefix='tcpip')

    def get_tcpip_methods(self, typ):
        methods = ''
        cls = self.get_tcpip_name()

        for packet in self.get_packets('function'):
            if packet.get_doc_type() != typ or packet.get_function_id() < 0:
                continue

            name = packet.get_name().under
            meta = packet.get_formatted_element_meta(lambda element: element.get_tcpip_type(),
                                                     lambda element: element.get_name().under,
                                                     lambda constant_group: constant_group.get_name().upper,
                                                     parameter_title_override={'en': 'Request', 'de': 'Anfrage'},
                                                     return_title_override={'en': 'Response', 'de': 'Antwort'},
                                                     no_in_value={'en': 'empty payload', 'de': 'keine Nutzdaten'},
                                                     no_out_value={'en': 'no response', 'de': 'keine Antwort'},
                                                     include_function_id=True,
                                                     include_constants=False)
            meta_table = common.make_rst_meta_table(meta)
            desc = packet.get_tcpip_formatted_doc()
            func = '.. tcpip:function:: {0}.{1}\n\n{2}{3}'.format(cls, name, meta_table, desc)
            methods += func + '\n'

        return methods

    def get_tcpip_callbacks(self):
        cbs = ''
        func_start = '.. tcpip:function:: '
        cls = self.get_tcpip_name()

        for packet in self.get_packets('callback'):
            meta = packet.get_formatted_element_meta(lambda element: element.get_tcpip_type(),
                                                     lambda element: element.get_name().under,
                                                     lambda constant_group: constant_group.get_name().upper,
                                                     parameter_title_override={'en': 'Request', 'de': 'Anfrage'},
                                                     return_title_override={'en': 'Response', 'de': 'Antwort'},
                                                     callback_parameter_title_override={'en': 'Response', 'de': 'Antwort'},
                                                     no_out_value={'en': 'empty payload', 'de': 'keine Nutzdaten'},
                                                     include_function_id=True,
                                                     include_constants=False)
            meta_table = common.make_rst_meta_table(meta)
            desc = packet.get_tcpip_formatted_doc()
            func = '.. tcpip:function:: {0}.CALLBACK_{1}\n\n{2}{3}'.format(cls,
                                                                           packet.get_name().upper,
                                                                           meta_table,
                                                                           desc)
            cbs += func + '\n'

        return cbs

    def get_tcpip_api(self):
        c_str = {
        'en': """
.. _{0}_tcpip_callbacks:

Callbacks
^^^^^^^^^

{1}
""",
        'de': """
.. _{0}_tcpip_callbacks:

Callbacks
^^^^^^^^^

{1}
"""
        }

        api = {
        'en': """
.. _{0}_tcpip_api:

API
---

A general description of the TCP/IP protocol structure can be found
:ref:`here <llproto_tcpip>`.

{1}

{2}
""",
        'de': """
.. _{0}_tcpip_api:

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
            api_str += common.select_lang(c_str).format(self.get_doc_rst_ref_name(),
                                                        c)

        return common.select_lang(api).format(self.get_doc_rst_ref_name(),
                                              self.specialize_tcpip_doc_function_links(common.select_lang(self.get_doc())),
                                              api_str)

    def get_tcpip_doc(self):
        doc  = common.make_rst_header(self, has_device_identifier_constant=False)
        doc += common.make_rst_summary(self, is_programming_language=False)
        doc += self.get_tcpip_api()

        return doc

class TCPIPDocPacket(common.Packet):
    # There are no high level callbacks here.
    def add_high_level_callback_note(self):
        pass

    def get_tcpip_formatted_doc(self):
        text = common.select_lang(self.get_doc_text())
        constants = {'en': 'meanings', 'de': 'Bedeutungen'}
        constants_intro = {
        'en': """
The following {0} are defined for the elements of this function:

""",
        'de': """
Die folgenden {0} sind für die Elemente dieser Funktion definiert:

"""
        }
        parameter = {
        'en': 'response value',
        'de': 'Rückgabewert'
        }
        parameters = {
        'en': 'response values',
        'de': 'Rückgabewerte'
        }

        text = self.get_device().specialize_tcpip_doc_function_links(text)

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text, parameter, parameters)
        text = common.handle_rst_substitutions(text, self)

        def element_format(element):
            return common.select_lang({'en': '\nFor **{0}** element:\n\n', 'de': '\nFor **{0}** Element:\n\n'}).format(element.get_name().under)

        def constant_format(prefix, constant_group, constant, value):
            text = ''

            for word in constant.get_name().space.split(' '):
                if len(text) > 0:
                    if word[0] in '0123456789' and text[-1] in '0123456789':
                        text += common.select_lang({'en': '.', 'de': ','})
                    else:
                        text += ' '

                text += word

            return '* {0} = {1}\n'.format(value, text)

        text += common.format_constants('', self,
                                        constants_intro=constants_intro,
                                        constants_name=constants,
                                        element_format_func=element_format,
                                        constant_format_func=constant_format)

        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, 1)

class TCPIPDocElement(common.Element):
    def format_value(self, value):
        type_ = self.get_type()

        if type_ == 'float':
            return common.format_float(value)

        if type_ == 'bool':
            return str(bool(value)).lower()

        if type_ == 'char':
            return "'{0}'".format(value.replace("'", "\\'"))

        if type_ == 'string':
            return '"{0}"'.format(value.replace('"', '\\"'))

        return str(value)

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

    def get_bindings_display_name(self):
        return 'TCP/IP'

    def get_doc_rst_filename_part(self):
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
        with open(device.get_doc_rst_path(), 'w') as f:
            f.write(device.get_tcpip_doc())

def generate(root_dir, language):
    common.generate(root_dir, language, TCPIPDocGenerator)

if __name__ == '__main__':
    for language in ['en', 'de']:
        print('=== Generating %s ===' % language)
        generate(os.getcwd(), language)
