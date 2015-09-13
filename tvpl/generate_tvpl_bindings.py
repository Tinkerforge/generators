#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tinkerforge Visual Programming Language (TVPL) Bindings Generator
Copyright (C) 2015 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>

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
    def get_packet_elements_as_list(self, elements):
        list_e = []

        for e in elements:
            list_e.append(e.get_underscore_name())

        return list_e

    def get_hash_value_field_variable(self, e_in):
        hash_value_to_code_variable = {}
        hash_get_field_value_variable = {}

        for e in e_in:
            hash_value_to_code_variable[e] = 'value_' + self.get_tvpl_device_name() + '_' + e
            hash_get_field_value_variable[e] = 'value_' + self.get_tvpl_device_name() + '_' + e

        return (hash_value_to_code_variable, hash_get_field_value_variable)

    def get_list_value_field_statements(self, packet, e_in, hash_value_to_code_variable, hash_get_field_value_variable):
        list_blockly_value_to_code_statements = []
        list_blockly_get_field_value_statements = []
        constant_groups = packet.get_constant_groups()

        if len(constant_groups) > 0:
            # Constants in constant group
            for e in e_in:
                for constant_group in constant_groups:
                    list_blockly_get_field_value_statements.append('''  var {0} = block.getFieldValue('{1}_{2}_{3}');'''.format(hash_get_field_value_variable[e],
                                                                                                                                  self.get_tvpl_device_name().upper(),
                                                                                                                                  packet.get_underscore_name().upper(),
                                                                                                                                  e.upper()))
        else:
            # Nothing in constant group
            for e in e_in:
                list_blockly_value_to_code_statements.append('''  var {0} = Blockly.JavaScript.valueToCode(block, '{1}_{2}', Blockly.JavaScript.ORDER_ATOMIC);'''.format(hash_value_to_code_variable[e],
                                                                                                                                                                           self.get_tvpl_device_name().upper(),
                                                                                                                                                                           e.upper()))
        return (list_blockly_value_to_code_statements, list_blockly_get_field_value_statements)

    def get_function_in_args(self, e_in, ret_get_hash_value_field_variable):
        function_in_args = ''

        for i, e in enumerate(e_in):
            if e in ret_get_hash_value_field_variable[0]:
                if function_in_args == '':
                    function_in_args = 'String(' + ret_get_hash_value_field_variable[0][e] + ')'
                    if i < len(e_in) - 1:
                        function_in_args = function_in_args + ' + \', \' + '
                else:
                    function_in_args = function_in_args + 'String(' + ret_get_hash_value_field_variable[0][e] + ')'
                    if i < len(e_in) - 1:
                        function_in_args = function_in_args + ' + \', \' + '
            elif e in ret_get_hash_value_field_variable[1]:
                if function_in_args == '':
                    function_in_args = 'String(' + ret_get_hash_value_field_variable[1][e] + ')'
                    if i < len(e_in) - 1:
                        function_in_args = function_in_args + ' + \', \' + '
                else:
                    function_in_args = function_in_args + 'String(' + ret_get_hash_value_field_variable[1][e] + ')'
                    if i < len(e_in) - 1:
                        function_in_args = function_in_args + ' + \', \' + '

        return function_in_args

    def get_tvpl_source_block(self, dir_bindings_root):
        def get_source_block(packet):
            is_getter = False
            elements_in = packet.get_elements('in')
            elements_out = packet.get_elements('out')

            if len(elements_out) > 0:
                is_getter = True

            block_name = '_'.join([self.get_tvpl_device_name(), packet.get_underscore_name()])
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
            block_code_header = '''Blockly.Blocks['{0}'] = {{
  init: function() {{'''.format(block_name)

            if is_getter:
                block_set_previous_statement = 'this.setPreviousStatement(false);'
                block_set_next_statement = 'this.setNextStatement(false);'
                if len(elements_out) > 1:
                    block_set_output = 'this.setOutput(true, \'Array\');'
                elif len(elements_out) == 1:
                    block_set_output = 'this.setOutput(true, \'' + elements_out[0].get_tvpl_type() + '\');'
                if len(elements_in) < 1:
                    # Getters without in args
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

            if not is_getter:
                if len(elements_in) < 1:
                    # Setters without in args
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

            # Getters/setters with in args
            block_code_body = ''
            for e in elements_in:
                if e.get_constant_group():
                    # Create combobox with allowed input values
                    constant_group = e.get_constant_group()
                    combo_constants_array = ''
                    constant_group_name = constant_group.get_headless_camel_case_name()
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
        .appendField(new Blockly.FieldDropdown({2}), '{3}');
'''.format(block_display_function_name,
           constant_group_name,
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
        .appendField(new Blockly.FieldDropdown({1}), '{2}');
'''.format(constant_group_name,
           combo_constants_array,
           '_'.join([self.get_underscore_category().upper(),
                     self.get_underscore_name().upper(),
                     packet.get_underscore_name().upper(),
                     e.get_underscore_name().upper()]))
                else:
                    # Create input field of specific types
                    if block_code_body == '':
                        block_code_body = '''
    this.appendDummyInput()
        .appendField('{0}');
    this.appendDummyInput()
        .appendField('{1}:');
    this.appendValueInput('{2}')
        .setCheck('{3}');
'''.format(block_display_function_name,
           e.get_headless_camel_case_name(),
           '_'.join([self.get_underscore_category().upper(),
                     self.get_underscore_name().upper(),
                     e.get_underscore_name().upper()]),
           e.get_tvpl_type())
                    else:
                        block_code_body = block_code_body + '''    this.appendDummyInput()
        .appendField('{0}:');
    this.appendValueInput('{1}')
        .setCheck('{2}');
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

        # Exclude RED Brick
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
               'threshold' in packet.get_underscore_name() or \
               'debounce' in packet.get_underscore_name() or \
               'period' in packet.get_underscore_name():
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
        file_tvpl_toolbox_part = open(os.path.join(dir_bindings_root, 'bindings', filename_tvpl_toolbox_part), 'wb')
        file_tvpl_toolbox_part.write(etree.tostring(e_device))
        file_tvpl_toolbox_part.close()

        return source

    def get_tvpl_source_generator_javascript(self):
        source = ''

        # Exclude RED Brick
        if self.get_underscore_name() == 'red':
            return ''

        for packet in self.get_packets('function'):
            # Exclude callbacks and thresholds
            if 'callback' in packet.get_underscore_name() or \
               'threshold' in packet.get_underscore_name() or \
               'debounce' in packet.get_underscore_name() or \
               'period' in packet.get_underscore_name():
                   continue

            is_getter = False
            generator_code_body = ''
            function_to_generate = ''
            index_global_variable = ''
            returned_blockly_code = ''
            elements_in = packet.get_elements('in')
            elements_out = packet.get_elements('out')
            block_name = '_'.join([self.get_tvpl_device_name(), packet.get_underscore_name()])

            generator_code_header = '''Blockly.JavaScript['{0}'] = function(block) {{
  var value_{0}_uid = Blockly.JavaScript.valueToCode(block, '{1}_UID', Blockly.JavaScript.ORDER_ATOMIC);
  var value_{0}_host = Blockly.JavaScript.valueToCode(block, '{1}_HOST', Blockly.JavaScript.ORDER_ATOMIC);
  var value_{0}_port = Blockly.JavaScript.valueToCode(block, '{1}_PORT', Blockly.JavaScript.ORDER_ATOMIC);
  var {0}_uid = value_{0}_uid.substr(1).slice(0, -1);
  var {0}_host = value_{0}_host.substr(1).slice(0, -1);
  var block_identifier = Blockly.JavaScript.tfGetUniqueNumber();
'''.format(block_name,
           self.get_tvpl_device_name().upper())

            generator_code_footer = '''  Blockly.JavaScript.definitions_['common_javascript_ipcon_connect'] = 'function _ipcon_connect(host, port) {{\\n'+
'  var ipcon;\\n'+
'  var key_ipcon_cache = host + \\':\\' + String(port);\\n'+
'\\n'+
'  if (key_ipcon_cache in _ipcon_cache) {{\\n'+
'    setTimeout(function() {{\\n'+
'      _iterator_main.next();\\n'+
'    }}, 0);\\n'+
'  }}\\n'+
'  else {{\\n'+
'     ipcon = new Tinkerforge.IPConnection();\\n'+
'     ipcon.on(Tinkerforge.IPConnection.CALLBACK_CONNECTED, function(e) {{\\n'+
'       _ipcon_cache[key_ipcon_cache] = ipcon;\\n'+
'       _iterator_main.next();\\n'+
'     }});\\n'+
'     ipcon.connect(host, port, _error_handler);\\n'+
'  }}\\n'+
'}}\\n';

  return {0};
}};

'''
            if len(elements_out) > 0:
                is_getter = True

            if is_getter:
                # Getters
                index_global_variable = '''  var index_global_variable = {0}+
'@'+
{1}+
':'+
String({2})+
'_{3}_'+
String(block_identifier);

'''.format('_'.join([block_name, 'uid']),
           '_'.join([block_name, 'host']),
           '_'.join(['value', block_name, 'port']),
           block_name)

                if len(elements_in) < 1:
                    # Getters without in args
                    returned_blockly_code = '''  var code = '(_ipcon_connect(\\''+
{0}+
'\\', '+
String({1})+
'), (yield 1), _{2}(\\''+
{0}+
'\\', '+
String({1})+
', \\''+
{3}+
'\\', \\''+
String(block_identifier)+
'\\'), (yield 1), _tf_global_variables[\\''+
index_global_variable+
'\\'])'

'''.format('_'.join([block_name, 'host']),
           '_'.join(['value', block_name, 'port']),
           block_name,
           '_'.join([block_name, 'uid']))

                    out_args_assignment = ', '.join(self.get_packet_elements_as_list(elements_out))

                    if len(elements_out) > 1:
                        out_args_assignment = '[' + ', '.join(self.get_packet_elements_as_list(elements_out)) + ']'

                    function_to_generate = '''Blockly.JavaScript.definitions_['{0}'] = 'function _{0}(host, port, uid, block_id) {{\\n'+
'  var key_ipcon_cache = host + \\':\\' + String(port);\\n'+
'  var key_device_cache = uid + \\'@\\' + key_ipcon_cache;\\n'+
'  var device = _device_cache[key_device_cache];\\n'+
'  var key_global_variable = key_device_cache + \\'_{0}_\\' + block_id;\\n'+
'\\n'+
'  if (device == null) {{\\n'+
'    device = new Tinkerforge.{1}(uid, _ipcon_cache[key_ipcon_cache]);\\n'+
'    _device_cache[key_device_cache] = device;\\n'+
'  }}\\n'+
'  device.{2}(function({3}) {{\\n'+
'    _tf_global_variables[key_global_variable] = {4};\\n'+
'    _iterator_main.next();\\n'+
'  }}, _error_handler);\\n'+
'}}\\n';

'''.format(block_name,
           self.get_camel_case_category() + self.get_camel_case_name(),
           packet.get_headless_camel_case_name(),
           ', '.join(self.get_packet_elements_as_list(elements_out)),
           out_args_assignment)

                else:
                    # Getters with in args
                    ret_get_hash_value_field_variable = self.get_hash_value_field_variable(self.get_packet_elements_as_list(elements_in))
                    ret_get_list_value_field_statements = self.get_list_value_field_statements(packet,
                                                                                          self.get_packet_elements_as_list(elements_in),
                                                                                          ret_get_hash_value_field_variable[0],
                                                                                          ret_get_hash_value_field_variable[1])

                    if len(ret_get_list_value_field_statements[0]) > 0:
                        generator_code_header = generator_code_header + '\n'.join(ret_get_list_value_field_statements[0]) + '\n'
                    elif len(ret_get_list_value_field_statements[1]) > 0:
                        generator_code_header = generator_code_header + '\n'.join(ret_get_list_value_field_statements[1]) + '\n'

                    returned_blockly_code = '''  var code = '(_ipcon_connect(\\''+
{0}+
'\\', '+
String({1})+
'), (yield 1), _{2}(\\''+
{0}+
'\\', '+
String({1})+
', \\''+
{3}+
'\\', \\''+
String(block_identifier)+
'\\', ' + {4} + '), (yield 1), _tf_global_variables[\\''+
index_global_variable+
'\\'])'

'''.format('_'.join([block_name, 'host']),
           '_'.join(['value', block_name, 'port']),
           block_name,
           '_'.join([block_name, 'uid']),
           self.get_function_in_args(self.get_packet_elements_as_list(elements_in), ret_get_hash_value_field_variable))

                    out_args_assignment = ', '.join(self.get_packet_elements_as_list(elements_out))

                    if len(elements_out) > 1:
                        out_args_assignment = '[' + ', '.join(self.get_packet_elements_as_list(elements_out)) + ']'

                    function_to_generate = '''Blockly.JavaScript.definitions_['{0}'] = 'function _{0}(host, port, uid, block_id, {1}) {{\\n'+
'  var key_ipcon_cache = host + \\':\\' + String(port);\\n'+
'  var key_device_cache = uid + \\'@\\' + key_ipcon_cache;\\n'+
'  var device = _device_cache[key_device_cache];\\n'+
'  var key_global_variable = key_device_cache + \\'_{0}_\\' + block_id;\\n'+
'\\n'+
'  if (device == null) {{\\n'+
'    device = new Tinkerforge.{2}(uid, _ipcon_cache[key_ipcon_cache]);\\n'+
'    _device_cache[key_device_cache] = device;\\n'+
'  }}\\n'+
'  device.{3}({1}, function({4}) {{\\n'+
'    _tf_global_variables[key_global_variable] = {5};\\n'+
'    _iterator_main.next();\\n'+
'  }}, _error_handler);\\n'+
'}}\\n';

'''.format(block_name,
           ', '.join(self.get_packet_elements_as_list(elements_in)),
           self.get_camel_case_category() + self.get_camel_case_name(),
           packet.get_headless_camel_case_name(),
           ', '.join(self.get_packet_elements_as_list(elements_out)),
           out_args_assignment)

                generator_code_body = index_global_variable + returned_blockly_code + function_to_generate
                source = source + generator_code_header + generator_code_body + generator_code_footer.format('[code, Blockly.JavaScript.ORDER_FUNCTION_CALL]')

                continue

            else:
                # Setters
                if len(elements_in) < 1:
                    # Setters without in args
                    returned_blockly_code = '''  var code = '(_ipcon_connect(\\''+
{0}+
'\\', '+
String({1})+
'), (yield 1), _{2}(\\''+
{0}+
'\\', '+
String({1})+
', \\''+
{3}+
'\\', \\''+
String(block_identifier)+
'\\'), (yield 1));\\n'

'''.format('_'.join([block_name, 'host']),
           '_'.join(['value', block_name, 'port']),
           block_name,
           '_'.join([block_name, 'uid']))

                    function_to_generate = '''Blockly.JavaScript.definitions_['{0}'] = 'function _{0}(host, port, uid, block_id) {{\\n'+
'  var key_ipcon_cache = host + \\':\\' + String(port);\\n'+
'  var key_device_cache = uid + \\'@\\' + key_ipcon_cache;\\n'+
'  var device = _device_cache[key_device_cache];\\n'+
'\\n'+
'  if (device == null) {{\\n'+
'    device = new Tinkerforge.{1}(uid, _ipcon_cache[key_ipcon_cache]);\\n'+
'    _device_cache[key_device_cache] = device;\\n'+
'  }}\\n'+
'  device.{2}(function(e) {{\\n'+
'    _iterator_main.next();\\n'+
'  }}, _error_handler);\\n'+
'}}\\n';

'''.format(block_name,
           self.get_camel_case_category() + self.get_camel_case_name(),
           packet.get_headless_camel_case_name())

                else:
                    # Setters with in args
                    ret_get_hash_value_field_variable = self.get_hash_value_field_variable(self.get_packet_elements_as_list(elements_in))
                    ret_get_list_value_field_statements = self.get_list_value_field_statements(packet,
                                                                                               self.get_packet_elements_as_list(elements_in),
                                                                                               ret_get_hash_value_field_variable[0],
                                                                                               ret_get_hash_value_field_variable[1])

                    if len(ret_get_list_value_field_statements[0]) > 0:
                        generator_code_header = generator_code_header + '\n'.join(ret_get_list_value_field_statements[0]) + '\n'
                    elif len(ret_get_list_value_field_statements[1]) > 0:
                        generator_code_header = generator_code_header + '\n'.join(ret_get_list_value_field_statements[1]) + '\n'

                    returned_blockly_code = '''  var code = '(_ipcon_connect(\\''+
{0}+
'\\', '+
String({1})+
'), (yield 1), _{2}(\\''+
{0}+
'\\', '+
String({1})+
', \\''+
{3}+
'\\', \\''+
String(block_identifier)+
'\\', ' + {4} + '), (yield 1));\\n'

'''.format('_'.join([block_name, 'host']),
           '_'.join(['value', block_name, 'port']),
           block_name,
           '_'.join([block_name, 'uid']),
           self.get_function_in_args(self.get_packet_elements_as_list(elements_in), ret_get_hash_value_field_variable))

                    function_to_generate = '''Blockly.JavaScript.definitions_['{0}'] = 'function _{0}(host, port, uid, block_id, {1}) {{\\n'+
'  var key_ipcon_cache = host + \\':\\' + String(port);\\n'+
'  var key_device_cache = uid + \\'@\\' + key_ipcon_cache;\\n'+
'  var device = _device_cache[key_device_cache];\\n'+
'\\n'+
'  if (device == null) {{\\n'+
'    device = new Tinkerforge.{2}(uid, _ipcon_cache[key_ipcon_cache]);\\n'+
'    _device_cache[key_device_cache] = device;\\n'+
'  }}\\n'+
'  device.{3}({1}, function({4}) {{\\n'+
'    _iterator_main.next();\\n'+
'  }}, _error_handler);\\n'+
'}}\\n';

'''.format(block_name,
           ', '.join(self.get_packet_elements_as_list(elements_in)),
           self.get_camel_case_category() + self.get_camel_case_name(),
           packet.get_headless_camel_case_name(),
           ', '.join(self.get_packet_elements_as_list(elements_out)))

                generator_code_body = returned_blockly_code + function_to_generate
                source = source + generator_code_header + generator_code_body + generator_code_footer.format('code')
                continue

        return source

    def get_tvpl_source_generator_python(self):
        # Exclude RED Brick
        if self.get_underscore_name() == 'red':
            return ''

        source = ''

        for packet in self.get_packets('function'):
            # Exclude callbacks and thresholds
            if 'callback' in packet.get_underscore_name() or \
               'threshold' in packet.get_underscore_name() or \
               'debounce' in packet.get_underscore_name() or \
               'period' in packet.get_underscore_name():
                   continue

            has_in_args = False
            elements_in = packet.get_elements('in')
            elements_out = packet.get_elements('out')
            block_name = '_'.join([self.get_tvpl_device_name(), packet.get_underscore_name()])
            generator_code_header = '''Blockly.Python['{0}'] = function(block) {{
  var value_{1}_uid = Blockly.Python.valueToCode(block, '{2}_UID', Blockly.Python.ORDER_ATOMIC);
  var value_{1}_host = Blockly.Python.valueToCode(block, '{2}_HOST', Blockly.Python.ORDER_ATOMIC);
  var value_{1}_port = Blockly.Python.valueToCode(block, '{2}_PORT', Blockly.Python.ORDER_ATOMIC);
  Blockly.Python.tfAppendCleanupCall_ = true;
'''.format(block_name,
           self.get_tvpl_device_name(),
           self.get_tvpl_device_name().upper())

            generator_code_fixed_definitions = '''  Blockly.Python.definitions_['common_python_import'] = '_ipcon_cache = {}\\n'+
'_device_cache = {}\\n'+
'\\n'+
'from tinkerforge.ip_connection import IPConnection';

  Blockly.Python.definitions_['common_python_get_ipcon'] = 'def _get_ipcon(host, port):\\n'+
'  global _ipcon_cache\\n'+
'  key = host + \\':\\' + str(port)\\n'+
'\\n'+
'  if key not in _ipcon_cache:\\n'+
'    ipcon = IPConnection()\\n'+
'    ipcon.connect(host, port)\\n'+
'    _ipcon_cache[key] = ipcon\\n'+
'\\n'+
'  return _ipcon_cache[key]';

  Blockly.Python.definitions_['common_python_get_device'] = 'def _get_device(device_class, uid, ipcon):\\n'+
'  global _device_cache\\n'+
'  key = str(device_class.DEVICE_IDENTIFIER) + \\':\\' + uid\\n'+
'\\n'+
'  if key not in _device_cache:\\n'+
'    device = device_class(uid, ipcon)\\n'+
'    _device_cache[key] = device\\n'+
'\\n'+
'  return _device_cache[key]';

  Blockly.Python.definitions_['common_python_cleanup'] = 'def _cleanup():\\n'+
'  for ipcon in _ipcon_cache.values():\\n'+
'    ipcon.disconnect()';

'''
            generator_code_device_import = '''  Blockly.Python.definitions_['import_{0}'] = 'from tinkerforge.{0} import {1}';

'''.format(self.get_tvpl_device_name(),
           self.get_camel_case_category() + self.get_camel_case_name())

            generator_code_footer = '  return [code, Blockly.Python.ORDER_FUNCTION_CALL];\n};\n\n'

            function_to_generate = ''
            returned_blockly_code = ''

            if len(elements_in) > 0:
                has_in_args = True

            if not has_in_args:
                # Function without in args
                if len(elements_out) > 0:
                    # Getters
                    function_to_generate = '''  Blockly.Python.definitions_['{0}'] = 'def {0}(HOST, PORT, UID):\\n'+
'  return get_device({1}, UID, _get_ipcon(HOST, PORT)).{2}()';

'''.format(block_name,
           self.get_camel_case_category() + self.get_camel_case_name(),
           packet.get_underscore_name())

                    returned_blockly_code = '''  var code = '{0}(' + value_{1}_host + ', ' + value_{1}_port + ', ' + value_{1}_uid + ')';
'''.format(block_name,
           self.get_tvpl_device_name())

                else:
                    # Setters
                    function_to_generate = '''  Blockly.Python.definitions_['{0}'] = 'def {0}(HOST, PORT, UID):\\n'+
'  get_device({1}, UID, _get_ipcon(HOST, PORT)).{2}()';

'''.format(block_name,
           self.get_camel_case_category() + self.get_camel_case_name(),
           packet.get_underscore_name())

                    returned_blockly_code = '''  var code = '{0}(' + value_{1}_host + ', ' + value_{1}_port + ', ' + value_{1}_uid + ')\\n';
'''.format(block_name,
           self.get_tvpl_device_name())

            else:
                # Function with in args
                ret_get_hash_value_field_variable = self.get_hash_value_field_variable(self.get_packet_elements_as_list(elements_in))
                ret_get_list_value_field_statements = self.get_list_value_field_statements(packet,
                                                                                           self.get_packet_elements_as_list(elements_in),
                                                                                           ret_get_hash_value_field_variable[0],
                                                                                           ret_get_hash_value_field_variable[1])

                if len(ret_get_list_value_field_statements[0]) > 0:
                    generator_code_header = generator_code_header + '\n'.join(ret_get_list_value_field_statements[0]) + '\n'
                elif len(ret_get_list_value_field_statements[1]) > 0:
                    generator_code_header = generator_code_header + '\n'.join(ret_get_list_value_field_statements[1]) + '\n'

                if len(elements_out) > 0:
                    # Getters
                    function_to_generate = '''  Blockly.Python.definitions_['{0}'] = 'def {0}(HOST, PORT, UID, {1}):\\n'+
'  return get_device({2}, UID, _get_ipcon(HOST, PORT)).{3}({1})';

'''.format(block_name,
           ', '.join(self.get_packet_elements_as_list(elements_in)),
           self.get_camel_case_category() + self.get_camel_case_name(),
           packet.get_underscore_name())

                    returned_blockly_code = '''  var code = '{0}(' + String(value_{1}_host) + ', ' + String(value_{1}_port) + ', ' + String(value_{1}_uid) + ', ' + {2} + ')';
'''.format(block_name,
           self.get_tvpl_device_name(),
           self.get_function_in_args(self.get_packet_elements_as_list(elements_in), ret_get_hash_value_field_variable))


                else:
                    # Setters
                    function_to_generate = '''  Blockly.Python.definitions_['{0}'] = 'def {0}(HOST, PORT, UID, {1}):\\n'+
'  get_device({2}, UID, _get_ipcon(HOST, PORT)).{3}({1})';

'''.format(block_name,
           ', '.join(self.get_packet_elements_as_list(elements_in)),
           self.get_camel_case_category() + self.get_camel_case_name(),
           packet.get_underscore_name())

                    returned_blockly_code = '''  var code = '{0}(' + String(value_{1}_host) + ', ' + String(value_{1}_port) + ', ' + String(value_{1}_uid) + ', ' + {2} + ')\\n';
'''.format(block_name,
           self.get_tvpl_device_name(),
           self.get_function_in_args(self.get_packet_elements_as_list(elements_in), ret_get_hash_value_field_variable))

            source = source + \
                     generator_code_header + \
                     generator_code_fixed_definitions + \
                     generator_code_device_import + \
                     function_to_generate + \
                     returned_blockly_code + \
                     generator_code_footer

        return source

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
        file_tvpl_block.write(device.get_tvpl_source_block(self.get_bindings_root_directory()))
        file_tvpl_block.close()

        file_tvpl_code_generator_javascript = open(os.path.join(self.bindings_root_directory, self.get_bindings_root_directory(), 'bindings', filename_tvpl_code_generator_javascript), 'wb')
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
