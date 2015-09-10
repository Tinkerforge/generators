#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tinkerforge Visual Programming Language (TVPL) Bindings Generator
Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>

generate_tvpl_bindings.py: Generator for TVPL bindings

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

sys.path.append(os.path.split(os.getcwd())[0])
import common
import tvpl_common

class TVPLBindingsDevice(tvpl_common.TVPLDevice):
    def get_tvpl_source_block(self):
        def get_source_block(packet):
            source = ''
            block_set_output = ''
            block_set_next_statement = ''
            block_set_previous_statement = ''
            block_append_field_input = ''
            block_code_header = ''
            block_code_footer = ''
            is_getter = False
            elements_in = packet.get_elements('in')
            elements_out = packet.get_elements('out')

            if len(elements_out) > 0:
                is_getter = True

            block_name = '_'.join([self.get_tvpl_block_name(), packet.get_underscore_name()])
            block_uid = '_'.join([self.get_underscore_category().upper(), self.get_underscore_name().upper(), 'UID'])
            block_host = '_'.join([self.get_underscore_category().upper(), self.get_underscore_name().upper(), 'HOST'])
            block_port = '_'.join([self.get_underscore_category().upper(), self.get_underscore_name().upper(), 'PORT'])
            block_display_device_name = self.get_long_display_name()
            block_display_function_name = packet.get_headless_camel_case_name()
            block_set_color = 'this.setColour(210);'
            block_set_tooltip = 'this.setTooltip(\'' + packet.get_tvpl_tooltip_from_doc() + '.\');'
            block_help_url = 'this.setHelpUrl(\'' + '/'.join(['http://www.tinkerforge.com/en/doc/Software',
                                                              self.get_camel_case_category() +\
                                                              's',
                                                              self.get_camel_case_name() +\
                                                              '_' +\
                                                              self.get_camel_case_category() +\
                                                              '_JavaScript.html#' +\
                                                              self.get_camel_case_category() +\
                                                              self.get_camel_case_name() +\
                                                              '.' +\
                                                              packet.get_headless_camel_case_name()]) +\
                                                              '\');'
            block_set_previous_statement = 'this.setPreviousStatement(true);'
            block_set_next_statement = 'this.setNextStatement(true);'
            block_set_output = 'this.setOutput(false);'
            block_code_header = '''Blockly.Blocks[{0}] = {{
  init: function() {{'''.format(block_name)
            block_code_footer = '''    this.setInputsInline(true);
    {0}
    {1}
    {2}
    {3}
    {4}
  }}
}};'''.format(block_set_previous_statement,
              block_set_next_statement,
              block_set_color,
              block_set_tooltip,
              block_help_url)

            if is_getter:
                block_set_previous_statement = 'this.setPreviousStatement(false);'
                block_set_next_statement = 'this.setNextStatement(false);'
                if len(elements_out) > 1:
                    block_set_output = 'this.setOutput(true, \'Array\');'
                elif len(elements_out) == 1:
                    block_set_output = 'this.setOutput(true, \'' + elements_out[0].get_tvpl_type() + '\');'
                if len(elements_in) < 1:
                    # Getter without arguments
                    block_code_body = '''
    this.appendDummyInput()
        .appendField('{0}');
    this.appendValueInput('{1}')
        .setCheck(\'String\');
    this.appendDummyInput()
        .appendField(\'at\');
    this.appendValueInput('{2}')
        .setCheck(\'String\');
    this.appendDummyInput()
        .appendField(\':\');
    this.appendValueInput('{3}')
        .setCheck(\'Number\');
'''.format(' '.join([block_display_function_name, 'of', block_display_device_name]),
           block_uid,
           block_host,
           block_port)
                    return block_code_header + block_code_body + block_code_footer + '\n'

            # Function with arguments
            constant_groups = packet.get_constant_groups()
            if len(constant_groups) > 0:
                # Create combobox with allowed input values
                block_code_body = ''
                for e in elements_in:
                    for constant_group in constant_groups:
                        combo_constants_array = ''
                        for index , constant in enumerate(constant_group.get_constants()):
                            if index == 0:
                                combo_constants_array = '['
                                combo_constants_array = combo_constants_array +\
                                                        '[\'' +\
                                                        constant.get_camel_case_name() +\
                                                        '\'' +\
                                                        ', ' +\
                                                        '\'' +\
                                                        str(constant.get_value()) +\
                                                        '\']'
                            if index == len(constant_group.get_constants()) - 1:
                                combo_constants_array = combo_constants_array + ']'
                            else:
                                combo_constants_array = combo_constants_array + ', '

                        if block_code_body == '':
                            block_code_body = '''
    this.appendDummyInput()
        .appendField('{0}');
    this.appendDummyInput()
        .appendField('{1}:');
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown({2}), {3});
'''.format(block_display_function_name,
           constant_group.get_camel_case_name(),
           combo_constants_array,
           '_'.join([self.get_underscore_category().upper(),
                     self.get_underscore_name().upper(),
                     constant.get_camel_case_name().upper()]))
                        else:
                            block_code_body = block_code_body + '''
    this.appendDummyInput()
        .appendField('{0}:');
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown({1}), {2});
'''.format(constant_group.get_camel_case_name(),
           combo_constants_array,
           '_'.join([self.get_underscore_category().upper(),
                     self.get_underscore_name().upper(),
                     constant.get_camel_case_name().upper()]))

                block_code_body = block_code_body + '''    this.appendDummyInput()
        .appendField('of {0}');
    this.appendValueInput('{1}')
        .setCheck("String");
    this.appendDummyInput()
        .appendField("at");
    this.appendValueInput('{2}')
        .setCheck("String");
    this.appendDummyInput()
        .appendField(":");
    this.appendValueInput('{3}')
        .setCheck("Number");
'''.format(block_display_device_name,
           block_uid,
           block_host,
           block_port)
                return block_code_header + block_code_body + block_code_footer
            else:
                # Create input field of specific types
                block_code_body = ''

                for e in elements_in:
                    if block_code_body == '':
                        block_code_body = '''
    this.appendDummyInput()
        .appendField('{0}');
    this.appendDummyInput()
        .appendField('{1}:');
    this.appendValueInput('{2}');
        .setCheck('{3}')
'''.format(block_display_function_name,
           e.get_headless_camel_case_name(),
           '_'.join([self.get_underscore_category().upper(), self.get_underscore_name().upper(), e.get_headless_camel_case_name().upper()]),
           e.get_tvpl_type())
                    else:
                        block_code_body = block_code_body + '''    this.appendDummyInput()
        .appendField('{0}:');
    this.appendValueInput('{1}');
        .setCheck('{2}')
'''.format(e.get_headless_camel_case_name(),
           '_'.join([self.get_underscore_category().upper(), self.get_underscore_name().upper(), e.get_headless_camel_case_name().upper()]),
           e.get_tvpl_type())


                block_code_body = block_code_body + '''    this.appendDummyInput()
        .appendField('of {0}');
    this.appendValueInput('{1}')
        .setCheck("String");
    this.appendDummyInput()
        .appendField("at");
    this.appendValueInput('{2}')
        .setCheck("String");
    this.appendDummyInput()
        .appendField(":");
    this.appendValueInput('{3}')
        .setCheck("Number");
'''.format(block_display_device_name,
           block_uid,
           block_host,
           block_port)

                return block_code_header + block_code_body + block_code_footer + '\n'

        source = ''

        for packet in self.get_packets('function'):
            # Exclude RED Brick
            if self.get_underscore_name() == 'red':
                continue

            # Exclude callbacks and thresholds
            if 'callback' in packet.get_underscore_name() or \
               'threshold' in packet.get_underscore_name():
                   continue

            # We also prepare the toolbox XML file in this loop

            source = source + get_source_block(packet)

        return source

    def get_tvpl_source_generator_javascript(self):
        return ''

    def get_tvpl_source_generator_python(self):
        return ''

class TVPLBindingsGenerator(common.BindingsGenerator):
    released_files_name_prefix = 'tvpl'

    def get_bindings_name(self):
        return 'tvpl'

    def get_device_class(self):
        return TVPLBindingsDevice

    def get_packet_class(self):
        return tvpl_common.TVPLPacket

    def get_element_class(self):
        return tvpl_common.TVPLElement

    def prepare(self):
        return common.BindingsGenerator.prepare(self)

    def generate(self, device):
        filename_tvpl_block = '{0}_{1}.block'.format(device.get_underscore_category(), device.get_underscore_name())
        filename_tvpl_code_generator_javascript = '{0}_{1}.generator.javascript'.format(device.get_underscore_category(), device.get_underscore_name())
        filename_tvpl_code_generator_python = '{0}_{1}.generator.python'.format(device.get_underscore_category(), device.get_underscore_name())

        filename_tvpl_block = open(os.path.join(self.get_bindings_root_directory(), 'bindings', filename_tvpl_block), 'wb')
        filename_tvpl_block.write(device.get_tvpl_source_block())
        filename_tvpl_block.close()

        filename_tvpl_code_generator_javascript = open(os.path.join(self.get_bindings_root_directory(), 'bindings', filename_tvpl_code_generator_javascript), 'wb')
        filename_tvpl_code_generator_javascript.write(device.get_tvpl_source_generator_javascript())
        filename_tvpl_code_generator_javascript.close()

        filename_tvpl_code_generator_python = open(os.path.join(self.get_bindings_root_directory(), 'bindings', filename_tvpl_code_generator_python), 'wb')
        filename_tvpl_code_generator_python.write(device.get_tvpl_source_generator_python())
        filename_tvpl_code_generator_python.close()

        if device.is_released():
            self.released_files.append('_'.join([device.get_underscore_category(), device.get_underscore_name()]))

    def finish(self):
        return common.BindingsGenerator.finish(self)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', TVPLBindingsGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
