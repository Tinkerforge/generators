#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tinkerforge Visual Programming Language (TVPL) Documentation Generator
Copyright (C) 2015 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2015, 2017-2018 Matthias Bolte <matthias@tinkerforge.com>

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

if sys.hexversion < 0x3040000:
    print('Python >= 3.4 required')
    sys.exit(1)

import os
import importlib.util
import importlib.machinery

def create_generators_module():
    generators_dir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]

    if sys.hexversion < 0x3050000:
        generators_module = importlib.machinery.SourceFileLoader('generators', os.path.join(generators_dir, '__init__.py')).load_module()
    else:
        generators_spec = importlib.util.spec_from_file_location('generators', os.path.join(generators_dir, '__init__.py'))
        generators_module = importlib.util.module_from_spec(generators_spec)

        generators_spec.loader.exec_module(generators_module)

    sys.modules['generators'] = generators_module

if 'generators' not in sys.modules:
    create_generators_module()

from generators import common
from generators.tvpl import tvpl_common

class TVPLDocDevice(tvpl_common.TVPLDevice):
    # FIXME: this also filters out all paragraphs that reference callbacks or
    #        callback configuration function. this is not perfect and might
    #        filter too much, but for now it is a reasonable hack
    def replace_tvpl_function_links(self, text):
        all_blocks = [[]]

        for line in text.split('\n'):
            if len(line.strip()) == 0:
                all_blocks.append([])

            all_blocks[-1].append(line)

        device_name = self.get_long_display_name()
        filtered_blocks = []

        for block in all_blocks:
            skip_block = False
            filtered_block = []

            for line in block:
                for other_packet in self.get_packets():
                    name_false = ':func:`{0}`'.format(other_packet.get_name().camel)
                    name_right = ':tvpl:func:`{0} <{0} of {1}>`'.format(other_packet.get_name().space, device_name)
                    replaced_line = line.replace(name_false, name_right)

                    if line != replaced_line:
                        if other_packet.get_doc_type() not in ['bf', 'af']:
                            skip_block = True

                    line = replaced_line

                filtered_block.append(line)

            if not skip_block:
                filtered_blocks.append(filtered_block)

        lines = []

        for filtered_block in filtered_blocks:
            lines += filtered_block

        text = '\n'.join(lines)

        return text

    def get_tvpl_examples(self): # FIXME
        def title_from_filename(filename):
            filename = filename.replace('example_', '').replace('.tvpl', '')
            return common.under_to_space(filename)

        def language_from_filename(filename):
            return 'xml'

        return common.make_rst_examples(title_from_filename, self,
                                        language_from_filename=language_from_filename,
                                        add_tvpl_test_link=True)

    def get_tvpl_methods(self, typ):
        methods = ''
        device_name = self.get_long_display_name().replace(' ', '_')

        for packet in self.get_packets('function'):
            if packet.is_virtual():
                continue

            if packet.get_doc_type() != typ:
                continue

            name = packet.get_name().space.replace(' ', '_')
            params = packet.get_tvpl_parameter_list()
            returns = packet.get_tvpl_return_list()
            pd = packet.get_tvpl_parameter_desc()
            r = packet.get_tvpl_return_desc()
            d = packet.get_tvpl_formatted_doc()
            desc = '{0}{1}{2}'.format(pd, r, d)
            func = '.. tvpl:function:: N{0}{1} Aof P{2}{3}\n{4}'.format(name, params, device_name, returns, desc)
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
                                              self.replace_tvpl_function_links(common.select_lang(self.get_doc())),
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

        def format_element_name(element, index):
            if index == None:
                return element.get_name().space

            return '{0} [{1}]'.format(element.get_name().space, index)

        text += common.format_constants('', self, format_element_name, constants_name=constants)
        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, 1)

    def get_tvpl_parameter_list(self):
        params = []

        for element in self.get_elements(direction='in'):
            params.append('L{0}'.format(element.get_name().space.replace(' ', '_')))

        if len(params) > 1:
            params.insert(len(params) - 1, 'Aand')

        if len(params) > 0:
            if len(self.get_elements(direction='out')) > 0:
                params.insert(0, 'Awith')
            else:
                params.insert(0, 'Ato')

        return common.wrap_non_empty(' ', ' '.join(params), '')

    def get_tvpl_return_list(self):
        ret = ' R{0}'
        ret_list = []
        and_ = {
            'en': '_and_',
            'de': '_und_'
        }
        list_of = {
            'en': 'List_of_',
            'de': 'Liste_mit_'
        }

        for element in self.get_elements(direction='out'):
            ret_list.append(element.get_name().space.replace(' ', '_'))

        if len(ret_list) == 0:
            return ''
        elif len(ret_list) == 1:
            return ret.format(ret_list[0])

        return ret.format(common.select_lang(list_of) + ',_'.join(ret_list[:-1]) + common.select_lang(and_) + ret_list[-1])

    def get_tvpl_parameter_desc(self):
        desc = '\n'
        param = ' :param {0}: {1}'
        has_symbols = {
            'en': 'has symbols',
            'de': 'hat Symbole'
        }

        for element in self.get_elements(direction='in'):
            t = element.get_tvpl_doc_type()
            desc += param.format(element.get_name().space.replace(' ', '$nbsp;'), t)

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
        elements = self.get_elements(direction='out')

        if len(elements) == 0:
            return '\n :noreturn: {0}\n'.format(common.select_lang(nothing))

        ret = '\n'
        for element in elements:
            t = element.get_tvpl_doc_type()
            ret += ' :returns {0}: {1}'.format(element.get_name().space.replace(' ', '$nbsp;'), t)

            if element.get_constant_group() is not None or \
               self.get_function_id() == 255 and element.get_name().space == 'Device Identifier':
                ret += ' ({0})'.format(common.select_lang(has_symbols))

            ret += '\n'

        return ret

class TVPLDocGenerator(tvpl_common.TVPLGeneratorTrait, common.DocGenerator):
    def get_doc_rst_filename_part(self):
        return 'TVPL'

    def get_doc_example_regex(self):
        return r'^example_.*\.tvpl$'

    def get_device_class(self):
        return TVPLDocDevice

    def get_packet_class(self):
        return TVPLDocPacket

    def get_element_class(self):
        return tvpl_common.TVPLElement

    def generate(self, device):
        with open(device.get_doc_rst_path(), 'w') as f:
            f.write(device.get_tvpl_doc())

def generate(root_dir, language):
    common.generate(root_dir, language, TVPLDocGenerator)

if __name__ == '__main__':
    for language in ['en', 'de']:
        print('=== Generating %s ===' % language)
        generate(os.getcwd(), language)
