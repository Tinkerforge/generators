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
import xml.etree.ElementTree as etree

sys.path.append(os.path.split(os.getcwd())[0])
import common
import tvpl_common

class TVPLBindingsDevice(tvpl_common.TVPLDevice):
    def get_tvpl_source_block(self):
        def get_source_block(packet):
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

                    block_code_footer = '''    this.setInputsInline(true);
    {0}
    {1}
    {2}
    {3}
    {4}
  }}
}};
'''.format(block_set_output,
           block_set_previous_statement,
           block_set_next_statement,
           block_set_color,
           block_help_url)
                    return block_code_header + block_code_body + block_code_footer

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
        .appendField(new Blockly.FieldDropdown({2}), {3});'''.format(block_display_function_name,
                                                                     e.get_headless_camel_case_name(),
                                                                     combo_constants_array,
                                                                     '_'.join([self.get_underscore_category().upper(),
                                                                               self.get_underscore_name().upper(),
                                                                               packet.get_underscore_name().upper(),
                                                                               e.get_underscore_name().upper()]))
                        else:
                            block_code_body = block_code_body + '''
    this.appendDummyInput()
        .appendField('{0}:');
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown({1}), {2});
'''.format(e.get_headless_camel_case_name(),
           combo_constants_array,
           '_'.join([self.get_underscore_category().upper(),
                     self.get_underscore_name().upper(),
                     packet.get_underscore_name().upper(),
                     e.get_underscore_name().upper()]))

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

                block_code_footer = '''    this.setInputsInline(true);
    {0}
    {1}
    {2}
    {3}
    {4}
  }}
}};
'''.format(block_set_output,
           block_set_previous_statement,
           block_set_next_statement,
           block_set_color,
           block_help_url)

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
           '_'.join([self.get_underscore_category().upper(),
                     self.get_underscore_name().upper(),
                     e.get_underscore_name().upper()]),
           e.get_tvpl_type())
                    else:
                        block_code_body = block_code_body + '''    this.appendDummyInput()
        .appendField('{0}:');
    this.appendValueInput('{1}');
        .setCheck('{2}')
'''.format(e.get_headless_camel_case_name(),
           '_'.join([self.get_underscore_category().upper(),
                     self.get_underscore_name().upper(),
                     e.get_underscore_name().upper()]),
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

                block_code_footer = '''    this.setInputsInline(true);
    {0}
    {1}
    {2}
    {3}
    {4}
  }}
}};
'''.format(block_set_output,
           block_set_previous_statement,
           block_set_next_statement,
           block_set_color,
           block_help_url)

                return block_code_header + block_code_body + block_code_footer

        # Ignore RED Brick
        if self.get_underscore_name() == 'red':
            return ''

        source = ''
        device = '_'.join([self.get_underscore_category(),
                           self.get_underscore_name()]).upper()
        xml_toolbox_uid = '_'.join([device, 'UID'])
        xml_toolbox_host = '_'.join([device, 'HOST'])
        xml_toolbox_port = '_'.join([device, 'PORT'])
        xml_toolbox_part_function = ''

        e_device = etree.Element('category')
        e_device.set('name', self.get_short_display_name())

        for packet in self.get_packets('function'):
            # Exclude callbacks and thresholds
            if 'callback' in packet.get_underscore_name() or \
               'threshold' in packet.get_underscore_name():
                   continue

            source = source + get_source_block(packet)

            e_block_function = etree.Element('block')
            e_block_function.set('type', '_'.join([self.get_underscore_category(),
                                          self.get_underscore_name(),
                                          packet.get_underscore_name()]))
            e_value_uid = etree.Element('value')
            e_block_uid = etree.Element('block')
            e_field_uid = etree.Element('field')
            e_value_uid.set('name', xml_toolbox_uid)
            e_block_uid.set('type', 'text')
            e_field_uid.set('name', 'TEXT')
            e_block_uid.append(e_field_uid)
            e_value_uid.append(e_block_uid)

            e_value_host = etree.Element('value')
            e_block_host = etree.Element('block')
            e_field_host = etree.Element('field')
            e_value_host.set('name', xml_toolbox_host)
            e_block_host.set('type', 'text')
            e_field_host.set('name', 'TEXT')
            e_field_host.text = 'localhost'
            e_block_host.append(e_field_host)
            e_value_host.append(e_block_host)

            e_value_port = etree.Element('value')
            e_block_port = etree.Element('block')
            e_field_port = etree.Element('field')
            e_value_port.set('name', xml_toolbox_port)
            e_block_port.set('type', 'math_number')
            e_field_port.set('name', 'NUM')
            e_field_port.text = '4223'
            e_block_port.append(e_field_port)
            e_value_port.append(e_block_port)

            e_block_function.append(e_value_uid)
            e_block_function.append(e_value_host)
            e_block_function.append(e_value_port)

            e_device.append(e_block_function)

        # Generated partial XML toolbox file contains the category of each brick and bricklet
        # having all the getters and setter as blocks in sub-elements
        filename_tvpl_toolbox_part = '_'.join([self.get_underscore_category(),
                                               self.get_underscore_name()]) + '.toolbox.part'
        file_tvpl_toolbox_part = open(os.path.join('bindings', filename_tvpl_toolbox_part), 'wb')
        file_tvpl_toolbox_part.write(etree.tostring(e_device))
        file_tvpl_toolbox_part.close()

        return source

    def get_tvpl_source_generator_javascript(self):
        for packet in self.get_packets('function'):
            pass
        return ''

    def get_tvpl_source_generator_python(self):
        for packet in self.get_packets('function'):
            pass
        return ''

class TVPLBindingsGenerator(common.BindingsGenerator):
    released_files_name_prefix = 'tvpl'

    def get_bindings_name(self):
        return 'tvpl'

    def get_device_class(self):
        return TVPLBindingsDevice

    def get_packet_class(self):
        return common.Packet

    def get_element_class(self):
        return tvpl_common.TVPLElement

    def prepare(self):
        return common.BindingsGenerator.prepare(self)

    def generate(self, device):
        filename_tvpl_block = '{0}_{1}.block'.format(device.get_underscore_category(), device.get_underscore_name())
        filename_tvpl_code_generator_javascript = '{0}_{1}.generator.javascript'.format(device.get_underscore_category(), device.get_underscore_name())
        filename_tvpl_code_generator_python = '{0}_{1}.generator.python'.format(device.get_underscore_category(), device.get_underscore_name())

        file_tvpl_block = open(os.path.join(self.get_bindings_root_directory(), 'bindings', filename_tvpl_block), 'wb')
        file_tvpl_block.write(device.get_tvpl_source_block())
        file_tvpl_block.close()

        file_tvpl_code_generator_javascript = open(os.path.join(self.get_bindings_root_directory(), 'bindings', filename_tvpl_code_generator_javascript), 'wb')
        file_tvpl_code_generator_javascript.write(device.get_tvpl_source_generator_javascript())
        file_tvpl_code_generator_javascript.close()

        file_tvpl_code_generator_python = open(os.path.join(self.get_bindings_root_directory(), 'bindings', filename_tvpl_code_generator_python), 'wb')
        file_tvpl_code_generator_python.write(device.get_tvpl_source_generator_python())
        file_tvpl_code_generator_python.close()

        if device.is_released():
            self.released_files.append('_'.join([device.get_underscore_category(), device.get_underscore_name()]))

    def finish(self):
        return common.BindingsGenerator.finish(self)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', TVPLBindingsGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
