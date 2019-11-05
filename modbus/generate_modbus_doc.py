#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Modbus Documentation Generator
Copyright (C) 2012-2013 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2012-2014, 2016-2019 Matthias Bolte <matthias@tinkerforge.com>

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
        return self.get_category().camel + self.get_name().camel

    def specialize_modbus_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return ':modbus:func:`CALLBACK_{1} <{0}.CALLBACK_{1}>`'.format(packet.get_device().get_modbus_name(),
                                                                               packet.get_name().upper)
            else:
                return ':modbus:func:`{1} <{0}.{1}>`'.format(packet.get_device().get_modbus_name(),
                                                             packet.get_name().under)

        return self.specialize_doc_rst_links(text, specializer, prefix='modbus')

    def get_modbus_methods(self, typ):
        methods = ''
        cls = self.get_modbus_name()

        for packet in self.get_packets('function'):
            if packet.get_doc_type() != typ or packet.get_function_id() < 0:
                continue

            name = packet.get_name().under
            meta = packet.get_formatted_element_meta(lambda element: element.get_modbus_type(),
                                                     lambda element: element.get_name().under,
                                                     lambda constant_group: constant_group.get_name().upper,
                                                     parameter_title_override={'en': 'Request', 'de': 'Anfrage'},
                                                     return_title_override={'en': 'Response', 'de': 'Antwort'},
                                                     no_in_value={'en': 'empty payload', 'de': 'keine Nutzdaten'},
                                                     no_out_value={'en': 'no response', 'de': 'keine Antwort'},
                                                     include_function_id=True)
            meta_table = common.make_rst_meta_table(meta)
            desc = packet.get_modbus_formatted_doc()
            func = '.. modbus:function:: {0}.{1}\n\n{2}{3}'.format(cls, name, meta_table, desc)
            methods += func + '\n'

        return methods

    def get_modbus_callbacks(self):
        cbs = ''
        cls = self.get_modbus_name()

        for packet in self.get_packets('callback'):
            meta = packet.get_formatted_element_meta(lambda element: element.get_modbus_type(),
                                                     lambda element: element.get_name().under,
                                                     lambda constant_group: constant_group.get_name().upper,
                                                     parameter_title_override={'en': 'Request', 'de': 'Anfrage'},
                                                     return_title_override={'en': 'Response', 'de': 'Antwort'},
                                                     callback_parameter_title_override={'en': 'Response', 'de': 'Antwort'},
                                                     no_out_value={'en': 'empty payload', 'de': 'keine Nutzdaten'},
                                                     include_function_id=True)
            meta_table = common.make_rst_meta_table(meta)
            desc = packet.get_modbus_formatted_doc()
            func = '.. modbus:function:: {0}.CALLBACK_{1}\n\n{2}{3}'.format(cls,
                                                                            packet.get_name().upper,
                                                                            meta_table,
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
    # There are no high level callbacks here.
    def add_high_level_callback_note(self):
        pass

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
            c = '* {0}: {1}, '.format(value, constant.get_name().lower)

            for_ = {
            'en': 'for',
            'de': 'für'
            }

            c += common.select_lang(for_) + ' '

            e = []

            for element in constant_group.get_elements(self):
                name = element.get_name().under
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
                                        char_format_func=str,
                                        bool_format_func=lambda value: str(int(value)),
                                        constant_format_func=constant_format,
                                        constants_intro=constants_intro)

        return common.shift_right(text, 1)

class ModbusDocElement(common.Element):
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

    def get_doc_null_value_name(self):
        return 'null'

    def get_doc_formatted_param(self, element):
        return element.get_name().headless

    def generate(self, device):
        with open(device.get_doc_rst_path(), 'w') as f:
            f.write(device.get_modbus_doc())

def generate(root_dir, language):
    common.generate(root_dir, language, ModbusDocGenerator)

if __name__ == '__main__':
    for language in ['en', 'de']:
        print('=== Generating %s ===' % language)
        generate(os.getcwd(), language)
