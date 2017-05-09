#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Modbus Documentation Generator
Copyright (C) 2012-2013 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2012-2014, 2016-2017 Matthias Bolte <matthias@tinkerforge.com>

generate_modbus_doc.py: Generator for Modbus documentation

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

class ModbusDocDevice(common.Device):
    def get_modbus_name(self):
        return self.get_camel_case_category() + self.get_camel_case_name()

    def specialize_modbus_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return ':modbus:func:`CALLBACK_{1} <{0}.CALLBACK_{1}>`'.format(packet.get_device().get_modbus_name(),
                                                                               packet.get_upper_case_name())
            else:
                return ':modbus:func:`{1} <{0}.{1}>`'.format(packet.get_device().get_modbus_name(),
                                                             packet.get_underscore_name())

        return self.specialize_doc_rst_links(text, specializer, prefix='modbus')

    def get_modbus_methods(self, typ):
        methods = ''
        func_start = '.. modbus:function:: '
        cls = self.get_modbus_name()

        for packet in self.get_packets('function'):
            if packet.get_doc_type() != typ or packet.get_function_id() < 0:
                continue

            name = packet.get_underscore_name()
            fid = '\n :functionid: {0}'.format(packet.get_function_id())
            request = packet.get_modbus_request_desc()
            response = packet.get_modbus_response_desc()
            d = packet.get_modbus_formatted_doc()
            desc = '{0}{1}{2}{3}'.format(fid, request, response, d)
            func = '{0}{1}.{2}\n{3}'.format(func_start, cls, name, desc)
            methods += func + '\n'

        return methods

    def get_modbus_callbacks(self):
        cbs = ''
        func_start = '.. modbus:function:: '
        cls = self.get_modbus_name()
        for packet in self.get_packets('callback'):
            fid = '\n :functionid: {0}'.format(packet.get_function_id())
            response = packet.get_modbus_response_desc()
            desc = packet.get_modbus_formatted_doc()

            func = '{0}{1}.CALLBACK_{2}\n{3}\n{4}\n{5}'.format(func_start,
                                                               cls,
                                                               packet.get_upper_case_name(),
                                                               fid,
                                                               response,
                                                               desc)
            cbs += func + '\n'

        return cbs

    def get_modbus_api(self):
        c_str = {
        'en': """
.. _{0}_modbus_callbacks:

Callbacks
^^^^^^^^^

{1}
""",
        'de': """
.. _{0}_modbus_callbacks:

Callbacks
^^^^^^^^^

{1}
"""
        }

        api = {
        'en': """
.. _{0}_modbus_api:

API
---

A general description of the Modbus protocol structure can be found
:ref:`here <llproto_modbus>`.

{1}

{2}
""",
        'de': """
.. _{0}_modbus_api:

API
---

Eine allgemeine Beschreibung der Modbus Protokollstruktur findet sich
:ref:`hier <llproto_modbus>`.

{1}

{2}
"""
        }

        bf = self.get_modbus_methods('bf')
        af = self.get_modbus_methods('af')
        ccf = self.get_modbus_methods('ccf')
        c = self.get_modbus_callbacks()
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
                                              self.specialize_modbus_doc_function_links(common.select_lang(self.get_doc())),
                                              api_str)

    def get_modbus_doc(self):
        doc  = common.make_rst_header(self, has_device_identifier_constant=False)
        doc += common.make_rst_summary(self, is_programming_language=False)
        doc += self.get_modbus_api()

        return doc

class ModbusDocPacket(common.Packet):
    def get_modbus_formatted_doc(self):
        text = common.select_lang(self.get_doc_text())
        constants = {'en': 'meanings', 'de': 'Bedeutungen'}
        constants_intro = {
        'en': """
The following {0} are defined for the parameters of this function:

""",
        'de': """
Die folgenden {0} sind für die Parameter dieser Funktion definiert:

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

        text = self.get_device().specialize_modbus_doc_function_links(text)

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text, parameter, parameters)
        text = common.handle_rst_substitutions(text, self)
        text += common.format_since_firmware(self.get_device(), self)

        def constant_format(prefix, constant_group, constant, value):
            c = '* {0}: {1}, '.format(value, constant.get_underscore_name().replace('_', ' '))

            for_ = {
            'en': 'for',
            'de': 'für'
            }

            c += common.select_lang(for_) + ' '

            e = []
            for element in constant_group.get_elements():
                name = element.get_underscore_name()
                e.append(name)

            if len(e) > 1:
                and_ = {
                'en': 'and',
                'de': 'und'
                }

                c += ', '.join(e[:-1]) + ' ' + common.select_lang(and_) + ' ' + e[-1]
            else:
                c += e[0]

            return c + '\n'

        text += common.format_constants('', self, constants_name=constants,
                                        char_format='{0}',
                                        constant_format_func=constant_format,
                                        constants_intro=constants_intro)

        return common.shift_right(text, 1)

    def get_modbus_request_desc(self):
        empty_payload = {
        'en': 'empty payload',
        'de': 'keine Nutzdaten'
        }
        desc = '\n'
        param = ' :request {0}: {1}\n'
        for element in self.get_elements('in'):
            desc += param.format(element.get_underscore_name(), element.get_modbus_type())

        if desc == '\n':
            desc += ' :emptyrequest: {0}\n'.format(common.select_lang(empty_payload))

        return desc

    def get_modbus_response_desc(self):
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
            desc += returns.format(element.get_underscore_name(), element.get_modbus_type())

        if desc == '\n':
            if self.get_type() == 'callback':
                desc += ' :emptyresponse: {0}\n'.format(common.select_lang(empty_payload))
            else:
                desc += ' :noresponse: {0}\n'.format(common.select_lang(no_response))

        return desc

class ModbusDocElement(common.Element):
    def get_modbus_type(self):
        t = self.get_type()

        if t == 'string':
            t = 'char'

        if self.get_cardinality() == 1:
            return t

        return t + '[' + str(self.get_cardinality()) + ']'

class ModbusDocGenerator(common.DocGenerator):
    def get_bindings_name(self):
        return 'modbus'

    def get_bindings_display_name(self):
        return 'Modbus'

    def get_doc_rst_filename_part(self):
        return 'Modbus'

    def get_doc_example_regex(self):
        return None

    def get_device_class(self):
        return ModbusDocDevice

    def get_packet_class(self):
        return ModbusDocPacket

    def get_element_class(self):
        return ModbusDocElement

    def generate(self, device):
        rst = open(device.get_doc_rst_path(), 'wb')
        rst.write(device.get_modbus_doc())
        rst.close()

def generate(bindings_root_directory, language):
    common.generate(bindings_root_directory, language, ModbusDocGenerator)

if __name__ == "__main__":
    for language in ['en', 'de']:
        print("=== Generating %s ===" % language)
        generate(os.getcwd(), language)
