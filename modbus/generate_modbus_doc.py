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

if sys.hexversion < 0x3040000:
    print('Python >= 3.4 required')
    sys.exit(1)

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

    def get_modbus_functions(self, type_):
        functions = []
        template = '.. modbus:function:: {0}.{1}\n\n{2}{3}\n'
        cls = self.get_modbus_name()

        for packet in self.get_packets('function'):
            if packet.get_doc_type() != type_ or packet.is_virtual():
                continue

            name = packet.get_name().under
            meta = packet.get_formatted_element_meta(lambda element, cardinality=None: element.get_modbus_type(cardinality=cardinality),
                                                     lambda element, index=None: element.get_name(index=index).under,
                                                     parameter_label_override={'en': 'Request', 'de': 'Anfrage'},
                                                     return_label_override={'en': 'Response', 'de': 'Antwort'},
                                                     constants_hint_override={'en': ('See meanings', 'with meanings'), 'de': ('Siehe Bedeutungen', 'mit Bedeutungen')},
                                                     no_in_value={'en': 'empty payload', 'de': 'keine Nutzdaten'},
                                                     no_out_value={'en': 'no response', 'de': 'keine Antwort'},
                                                     include_function_id=True)
            meta_table = common.make_rst_meta_table(meta)
            desc = packet.get_modbus_formatted_doc()

            functions.append(template.format(cls, name, meta_table, desc))

        return ''.join(functions)

    def get_modbus_callbacks(self):
        callbacks = []
        template = '.. modbus:function:: {0}.CALLBACK_{1}\n\n{2}{3}\n'
        cls = self.get_modbus_name()

        for packet in self.get_packets('callback'):
            meta = packet.get_formatted_element_meta(lambda element, cardinality=None: element.get_modbus_type(cardinality=cardinality),
                                                     lambda element, index=None: element.get_name(index=index).under,
                                                     parameter_label_override={'en': 'Request', 'de': 'Anfrage'},
                                                     return_label_override={'en': 'Response', 'de': 'Antwort'},
                                                     callback_parameter_label_override={'en': 'Response', 'de': 'Antwort'},
                                                     constants_hint_override={'en': ('See meanings', 'with meanings'), 'de': ('Siehe Bedeutungen', 'mit Bedeutungen')},
                                                     no_out_value={'en': 'empty payload', 'de': 'keine Nutzdaten'},
                                                     include_function_id=True)
            meta_table = common.make_rst_meta_table(meta)
            desc = packet.get_modbus_formatted_doc()

            callbacks.append(template.format(cls, packet.get_name().upper, meta_table, desc))

        return ''.join(callbacks)

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

        bf = self.get_modbus_functions('bf')
        af = self.get_modbus_functions('af')
        ccf = self.get_modbus_functions('ccf')
        c = self.get_modbus_callbacks()
        if_ = self.get_modbus_functions('if')
        api_str = ''

        if bf:
            api_str += common.select_lang(common.bf_str).format('', bf)

        if af:
            api_str += common.select_lang(common.af_str).format(af)

        if c:
            if ccf:
                api_str += common.select_lang(common.ccf_str).format('', ccf)

            api_str += common.select_lang(c_str).format(self.get_doc_rst_ref_name(),
                                                        c)

        if if_:
            api_str += common.select_lang(common.if_str).format(if_)

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
The following **{0}** are defined for the elements of this function:

""",
        'de': """
Die folgenden **{0}** sind für die Elemente dieser Funktion definiert:

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

        def format_element_name(element, index):
            if index == None:
                return element.get_name().under

            return '{0}[{1}]'.format(element.get_name().under, index)

        def format_constant(prefix, constant_group, constant, value):
            text = ''

            for word in constant.get_name().space.split(' '):
                if len(text) > 0:
                    if word[0] in '0123456789' and text[-1] in '0123456789':
                        text += common.select_lang({'en': '.', 'de': ','})
                    else:
                        text += ' '

                text += word

            return '* {0} = {1}\n'.format(value, text)

        text += common.format_constants('', self, format_element_name,
                                        constants_intro=constants_intro,
                                        constants_name=constants,
                                        constant_format_func=format_constant)

        return common.shift_right(text, 1)

class ModbusDocElement(common.Element):
    def format_value(self, value):
        if isinstance(value, list):
            result = []

            for subvalue in value:
                result.append(self.format_value(subvalue))

            return '[{0}]'.format(', '.join(result))

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

    def get_modbus_type(self, cardinality=None):
        assert cardinality == None or (isinstance(cardinality, int) and cardinality > 0), cardinality

        modbus_type = self.get_type()

        if cardinality == None:
            cardinality = self.get_cardinality()

        if modbus_type == 'string':
            modbus_type = 'char'

        if cardinality == 1:
            return modbus_type

        return modbus_type + '[' + str(cardinality) + ']'

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
