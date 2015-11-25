#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tinkerforge Visual Programming Language (TVPL) Documentation Generator
Copyright (C) 2015 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2015 Matthias Bolte <matthias@tinkerforge.com>

generate_tvpl_doc.py: Generator for TVPL documentation

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
import glob
import re

sys.path.append(os.path.split(os.getcwd())[0])
import common
import tvpl_common

class TVPLDocDevice(tvpl_common.TVPLDevice):
    def replace_tvpl_function_links(self, text):
        device_name = self.get_long_display_name()
        for other_packet in self.get_packets():
            name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
            name_right = ':tvpl:func:`{0} <{0} of {1}>`'.format(other_packet.get_name(), device_name)
            text = text.replace(name_false, name_right)

        return text

    def get_tvpl_examples(self): # FIXME
        def title_from_filename(filename):
            filename = filename.replace('example_', '').replace('.tvpl', '')
            return common.underscore_to_space(filename)

        def language_from_filename(filename):
            return 'xml'

        return common.make_rst_examples(title_from_filename, self,
                                        language_from_filename=language_from_filename)

    def get_tvpl_methods(self, typ):
        methods = ''
        device_name = self.get_long_display_name().replace(' ', '_')

        for packet in self.get_packets('function'):
            if packet.is_virtual():
                continue

            if packet.get_doc_type() != typ:
                continue

            name = packet.get_name().replace(' ', '_')
            params = packet.get_tvpl_parameter_list()
            pd = packet.get_tvpl_parameter_desc()
            r = packet.get_tvpl_return_desc()
            d = packet.get_tvpl_formatted_doc()
            desc = '{0}{1}{2}'.format(pd, r, d)
            func = '.. tvpl:function:: N{0}{1} Aof P{2}\n{3}'.format(name, params, device_name, desc)
            methods += func + '\n'

        return methods

    def get_tvpl_api(self):
        api = {
        'en': """
.. _{0}_tvpl_api:

API
---

{1}

{2}
""",
        'de': """
.. _{0}_tvpl_api:

API
---

{1}

{2}
"""
        }

        bf = self.get_tvpl_methods('bf')
        af = self.get_tvpl_methods('af')
        api_str = ''
        if bf:
            api_str += common.select_lang(common.bf_str).format('', bf)
        if af:
            api_str += common.select_lang(common.af_str).format(af)

        return common.select_lang(api).format(self.get_doc_rst_ref_name(),
                                              self.replace_tvpl_function_links(self.get_api_doc()),
                                              api_str)

    def get_tvpl_doc(self):
        doc  = common.make_rst_header(self, has_device_identifier_constant=False)
        doc += common.make_rst_summary(self)
        doc += self.get_tvpl_examples()
        doc += self.get_tvpl_api()

        return doc

class TVPLDocPacket(tvpl_common.TVPLPacket):
    def get_tvpl_formatted_doc(self):
        text = common.select_lang(self.get_doc_text())
        constants = {'en': 'symbols', 'de': 'Symbole'}

        text = self.get_device().replace_tvpl_function_links(text)

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)

        def constant_format(prefix, constant_group, constant, value):
            c = '* ``{0}`` = {1}, '.format(constant.get_dash_name(), value)

            for_ = {
            'en': 'for',
            'de': 'für'
            }

            c += common.select_lang(for_) + ' '

            e = []
            for element in constant_group.get_elements():
                name = element.get_dash_name()
                if element.get_direction() == 'in':
                    e.append('<{0}>'.format(name))
                else:
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
                                        constant_format_func=constant_format)

        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, 1)

    def get_tvpl_parameter_list(self):
        params = []

        for element in self.get_elements('in'):
            params.append('L{0}'.format(element.get_name().replace(' ', '_')))

        if len(params) > 1:
            params.insert(len(params) - 1, 'Aand')

        if len(params) > 0:
            params.insert(0, 'Ato')

        return common.wrap_non_empty(' ', ' '.join(params), '')

    def get_tvpl_parameter_desc(self):
        desc = '\n'
        param = ' :param <{0}>: {1}'
        has_symbols = {
        'en': 'has symbols',
        'de': 'hat Symbole'
        }

        for element in self.get_elements('in'):
            t = element.get_tvpl_type()
            desc += param.format(element.get_dash_name(), t)

            if element.get_constant_group() is not None:
                desc += ' ({0})'.format(common.select_lang(has_symbols))

            desc += '\n'

        return desc

    def get_tvpl_return_desc(self):
        nothing = {
        'en': 'no output',
        'de': 'keine Ausgabe'
        }
        has_symbols = {
        'en': 'has symbols',
        'de': 'hat Symbole'
        }
        elements = self.get_elements('out')

        if len(elements) == 0:
            return '\n :noreturn: {0}\n'.format(common.select_lang(nothing))

        ret = '\n'
        for element in elements:
            t = element.get_tvpl_type()
            ret += ' :returns {0}: {1}'.format(element.get_dash_name(), t)

            if element.get_constant_group() is not None or \
               self.get_function_id() == 255 and element.get_underscore_name() == 'device_identifier':
                ret += ' ({0})'.format(common.select_lang(has_symbols))

            ret += '\n'

        return ret

class TVPLDocGenerator(common.DocGenerator):
    def get_bindings_name(self):
        return 'tvpl'

    def get_bindings_display_name(self):
        return 'Tinkerforge Visual Programming Language (TVPL)'

    def get_doc_rst_filename_part(self):
        return 'TVPL'

    def get_doc_example_regex(self):
        return '^example_.*\.tvpl$'

    def get_device_class(self):
        return TVPLDocDevice

    def get_packet_class(self):
        return TVPLDocPacket

    def get_element_class(self):
        return tvpl_common.TVPLElement

    def generate(self, device):
        rst = open(device.get_doc_rst_path(), 'wb')
        rst.write(device.get_tvpl_doc())
        rst.close()

def generate(bindings_root_directory, language):
    common.generate(bindings_root_directory, language, TVPLDocGenerator)

if __name__ == "__main__":
    for language in ['en', 'de']:
        print("=== Generating %s ===" % language)
        generate(os.getcwd(), language)
