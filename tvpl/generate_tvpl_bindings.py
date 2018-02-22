#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tinkerforge Visual Programming Language (TVPL) Bindings Generator
Copyright (C) 2015, 2018 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>

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
            elements_in = packet.get_elements(direction='in')
            elements_out = packet.get_elements(direction='out')

            if len(elements_out) > 0:
                is_getter = True

            block_name = '_'.join([self.get_tvpl_device_name(), packet.get_name().under])
            block_uid = '_UID'
            block_host = '_HOST'
            block_port = '_PORT'
            block_display_device_name = self.get_long_display_name()
            block_display_function_name = packet.get_name().space

            if self.is_brick():
                block_set_color = 'this.setColour(195);'
            else:
                block_set_color = 'this.setColour(297);'

            block_help_url = 'this.setHelpUrl(\'' + '/'.join(['http://www.tinkerforge.com/en/doc/Software',
                                                              self.get_category().camel +\
                                                              's',
                                                              self.get_name().camel +\
                                                              '_' +\
                                                              self.get_category().camel +\
                                                              '_JavaScript.html#' +\
                                                              self.get_category().camel +\
                                                              self.get_name().camel +\
                                                              '.' +\
                                                              packet.get_name().headless]) +\
                                                              '\');'
            block_set_previous_statement = 'this.setPreviousStatement(true);'
            block_set_next_statement = 'this.setNextStatement(true);'
            block_set_output = 'this.setOutput(false);'
            block_code_header = '''Blockly.Blocks['{blockname}'] = {{
  init: function() {{'''.format(blockname=block_name)

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
        .appendField('{function_name}')
    this.appendValueInput('{uid}')
        .setCheck(\'String\')
        .appendField('of {device_name}')
    this.appendValueInput('{host}')
        .setCheck(\'String\')
        .appendField(\'at\')
    this.appendValueInput('{port}')
        .setCheck(\'Number\')
        .appendField(\':\')
'''.format(function_name=block_display_function_name,
           device_name=block_display_device_name,
           uid=block_uid,
           host=block_host,
           port=block_port)

                    block_code_footer = '''    this.setInputsInline(true);
    {setoutput}
    {previousstatement}
    {nextstatement}
    {color}
    {helpurl}
  }}
}};
'''.format(setoutput=block_set_output,
           previousstatement=block_set_previous_statement,
           nextstatement=block_set_next_statement,
           color=block_set_color,
           helpurl=block_help_url)
                    return block_code_header + block_code_body + block_code_footer

            if not is_getter:
                if len(elements_in) < 1:
                    # Setters without in args
                    block_code_body = '''
    this.appendDummyInput()
        .appendField('{function_name}')
    this.appendValueInput('{uid}')
        .setCheck(\'String\')
        .appendField('of {device_name}')
    this.appendValueInput('{host}')
        .setCheck(\'String\')
        .appendField(\'at\')
    this.appendValueInput('{port}')
        .setCheck(\'Number\')
        .appendField(\':\')
'''.format(function_name=block_display_function_name,
           device_name=block_display_device_name,
           uid=block_uid,
           host=block_host,
           port=block_port)

                    block_code_footer = '''    this.setInputsInline(true);
    {setoutput}
    {previousstatement}
    {nextstatement}
    {color}
    {helpurl}
  }}
}};
'''.format(setoutput=block_set_output,
           previousstatement=block_set_previous_statement,
           nextstatement=block_set_next_statement,
           color=block_set_color,
           helpurl=block_help_url)
                    return block_code_header + block_code_body + block_code_footer

            # Getters/setters with in args
            block_code_body = ''

            if len(elements_out) < 1:
                block_code_body = '''
    this.appendDummyInput()
        .appendField('{functionname} to')
'''.format(functionname=block_display_function_name)
            else:
                block_code_body = '''
    this.appendDummyInput()
        .appendField('{functionname} with')
'''.format(functionname=block_display_function_name)

            for i, e in enumerate(elements_in):
                if e.get_constant_group():
                    # Create combobox with allowed input values
                    constant_group = e.get_constant_group()
                    combo_constants_array = ''

                    for index, constant in enumerate(constant_group.get_constants()):
                        if index == 0:
                            combo_constants_array = '['

                        combo_constants_array = combo_constants_array +\
                                                '[\'' +\
                                                constant.get_name().space +\
                                                '\'' +\
                                                ', ' +\
                                                '\'' +\
                                                str(constant.get_value()) +\
                                                '\']'

                        if index == len(constant_group.get_constants()) - 1:
                            combo_constants_array = combo_constants_array + ']'
                        else:
                            combo_constants_array = combo_constants_array + ', '

                    block_code_body = block_code_body + '''    this.appendDummyInput()
        .appendField('{ename}')
        .appendField(new Blockly.FieldDropdown({constantsarray}), '{fieldname}')
'''.format(ename=('and ' if len(elements_in) > 1 and i == len(elements_in) - 1 else '') + e.get_name().space,
           constantsarray=combo_constants_array,
           fieldname=e.get_name().upper)

                elif e.get_tvpl_type() == 'Boolean':
                    # Create combobox with boolean values
                    block_code_body = block_code_body + '''    this.appendDummyInput()
        .appendField('{ename}')
        .appendField(new Blockly.FieldDropdown([['True', '1'], ['False', '0']]), '{fieldname}')
'''.format(ename=('and ' if len(elements_in) > 1 and i == len(elements_in) - 1 else '') + e.get_name().space,
           fieldname=e.get_name().upper)

                elif e.get_tvpl_type() != 'Boolean':
                    # Create input field of specific types
                    block_code_body = block_code_body + '''    this.appendValueInput('{variablename}')
        .setCheck('{etvpltype}')
        .appendField('{ename}')
'''.format(ename=('and ' if len(elements_in) > 1 and i == len(elements_in) - 1 else '') + e.get_name().space,
           variablename=e.get_name().upper,
           etvpltype=e.get_tvpl_type())

            block_code_body += '''    this.appendValueInput('{uid}')
        .setCheck("String")
        .appendField('of {devicename}')
    this.appendValueInput('{host}')
        .setCheck("String")
        .appendField("at")
    this.appendValueInput('{port}')
        .setCheck("Number")
        .appendField(":")
'''.format(devicename=block_display_device_name,
           uid=block_uid,
           host=block_host,
           port=block_port)

            block_code_footer = '''    this.setInputsInline(true);
    {output}
    {previousstatement}
    {nextstatement}
    {color}
    {helpurl}
  }}
}};
'''.format(output=block_set_output,
           previousstatement=block_set_previous_statement,
           nextstatement=block_set_next_statement,
           color=block_set_color,
           helpurl=block_help_url)

            return block_code_header + block_code_body + block_code_footer

        # Exclude RED Brick
        if self.get_device_identifier() == 17:
            return ''

        source = ''
        xml_toolbox_uid = '_UID'
        xml_toolbox_host = '_HOST'
        xml_toolbox_port = '_PORT'

        e_device = etree.Element('category')
        e_device.set('name', self.get_short_display_name())

        if self.get_category().under == 'brick':
            e_device.set('colour', '195')
        elif self.get_category().under == 'bricklet':
            e_device.set('colour', '297')

        for packet in self.get_packets('function'):
            # Exclude unrelated functions

            if packet.get_doc_type() != 'af' and \
               packet.get_doc_type() != 'bf':
                continue

            if packet.is_virtual():
                continue

            source = source + get_source_block(packet)

            e_block_function = etree.Element('block')
            e_block_function.set('type', '_'.join([self.get_category().under,
                                                   self.get_name().under,
                                                   packet.get_name().under]))
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
            e_field_port.text = '4280'
            e_block_port.append(e_field_port)
            e_value_port.append(e_block_port)

            e_block_function.append(e_value_uid)
            e_block_function.append(e_value_host)
            e_block_function.append(e_value_port)

            e_device.append(e_block_function)

        # Generated partial XML toolbox file contains the category of each brick and bricklet
        # having all the getters and setter as blocks in sub-elements
        filename_tvpl_toolbox_part = '_'.join([self.get_category().under,
                                               self.get_name().under]) + '.toolbox.part'

        with open(os.path.join(self.get_generator().get_bindings_dir(), filename_tvpl_toolbox_part), 'wb') as f:
            f.write(etree.tostring(e_device))

        return source

    def get_tvpl_source_generator_javascript(self):
        source = ''

        # Exclude RED Brick
        if self.get_device_identifier() == 17:
            return ''

        for packet in self.get_packets('function'):
           # Exclude unrelated functions
            if packet.get_doc_type() != 'af' and \
               packet.get_doc_type() != 'bf':
                continue

            if packet.is_virtual():
                continue

            is_getter = False
            generator_code_body = ''
            function_to_generate = ''
            returned_blockly_code = ''
            elements_in = packet.get_elements(direction='in')
            elements_out = packet.get_elements(direction='out')
            block_name = '_'.join([self.get_tvpl_device_name(), packet.get_name().under])

            generator_code_header = '''Blockly.JavaScript['{blockname}'] = function(block) {{
  var value_{blockname}_ipcon_uid = Blockly.JavaScript.valueToCode(block, '_UID', Blockly.JavaScript.ORDER_ATOMIC);
  var value_{blockname}_ipcon_host = Blockly.JavaScript.valueToCode(block, '_HOST', Blockly.JavaScript.ORDER_ATOMIC);
  var value_{blockname}_ipcon_port = Blockly.JavaScript.valueToCode(block, '_PORT', Blockly.JavaScript.ORDER_ATOMIC);
'''.format(blockname=block_name)

            generator_code_footer = '''return {returncode};
}};

'''
            if len(elements_out) > 0:
                is_getter = True

            if is_getter:
                if len(elements_in) < 1:
                    # Getters without in args
                    returned_blockly_code = '''  var code = '(yield *_{blockname}(' + {host} + ', ' + {port} + ', ' + {uid} + '))'

'''.format(blockname=block_name,
           host='_'.join(['value', block_name, 'ipcon_host']),
           port='_'.join(['value', block_name, 'ipcon_port']),
           uid='_'.join(['value', block_name, 'ipcon_uid']))

                    out_args_assignment = ', '.join(packet.get_packet_elements_name_as_list(elements_out))

                    if len(elements_out) > 1:
                        out_args_assignment = '[' + ', '.join(packet.get_packet_elements_name_as_list(elements_out)) + ']'

                    function_to_generate = '''Blockly.JavaScript.definitions_['{blockname}'] = 'function *_{blockname}(host, port_ip, uid) {{\\n'+
'  var dict_tf_function_call = {{}};\\n'+
'  dict_tf_function_call.worker_id = String(_worker_id);\\n'+
'  dict_tf_function_call.host = String(host);\\n'+
'  dict_tf_function_call.port = Number(port_ip);\\n'+
'  dict_tf_function_call.uid = String(uid);\\n'+
'  dict_tf_function_call.device_class_name = \\'{categoryname}\\';\\n'+
'  dict_tf_function_call.device_function_name = \\'{packetname}\\';\\n'+
'  dict_tf_function_call.device_function_input_args = null;\\n'+
'  dict_tf_function_call.device_function_output_args = \\'{eoutargs}\\';\\n'+
'  dict_tf_function_call.device_function_output_assignment = \\'{eoutassignment}\\';\\n'+
'  postMessage(workerProtocol.getMessage(_worker_id, workerProtocol._TYPE_RES_FUNCTION_TF_CALL, dict_tf_function_call));\\n'+
'  yield 1;\\n'+
'  return _return_value;\\n'+
'}}\\n';

'''.format(blockname=block_name,
           categoryname=self.get_category().camel + self.get_name().camel,
           packetname=packet.get_name().headless,
           eoutargs=', '.join(packet.get_packet_elements_name_as_list(elements_out)),
           eoutassignment=out_args_assignment)

                else:
                    # Getters with in args
                    ret_get_hash_of_value_and_field_variables = packet.get_hash_of_value_and_field_variables(packet.get_packet_elements_name_as_list(elements_in),
                                                                                                             self.get_tvpl_device_name())
                    ret_get_list_of_value_field_statements_from_hash = packet.get_list_of_value_field_statements_from_hash(elements_in,
                                                                                                                           ret_get_hash_of_value_and_field_variables[0],
                                                                                                                           ret_get_hash_of_value_and_field_variables[1])

                    if len(ret_get_list_of_value_field_statements_from_hash[0]) > 0:
                        generator_code_header = generator_code_header + '\n'.join(ret_get_list_of_value_field_statements_from_hash[0]) + '\n'
                    if len(ret_get_list_of_value_field_statements_from_hash[1]) > 0:
                        generator_code_header = generator_code_header + '\n'.join(ret_get_list_of_value_field_statements_from_hash[1]) + '\n'

                    returned_blockly_code = '''  var code = '(yield *_{blockname}(' + {host} + ', ' + {port} + ', ' + {uid} + ', ' + {einargs} + '))'

'''.format(blockname=block_name,
           host='_'.join(['value', block_name, 'ipcon_host']),
           port='_'.join(['value', block_name, 'ipcon_port']),
           uid='_'.join(['value', block_name, 'ipcon_uid']),
           einargs=packet.get_caller_generation_arguments_from_value_and_field_hash(elements_in,
                                                                                    packet.get_packet_elements_name_as_list(elements_in),
                                                                                    ret_get_hash_of_value_and_field_variables))

                    out_args_assignment = ', '.join(packet.get_packet_elements_name_as_list(elements_out))

                    if len(elements_out) > 1:
                        out_args_assignment = '[' + ', '.join(packet.get_packet_elements_name_as_list(elements_out)) + ']'

                    statements_string_inputs = ''

                    for e in elements_in:
                        if e.get_tvpl_type() == 'String':
                            statements_string_inputs += e.get_name().under + ' = JSON.stringify(' + e.get_name().under + ');'

                    function_to_generate = '''Blockly.JavaScript.definitions_['{blockname}'] = 'function *_{blockname}(host, port_ip, uid, {einargs}) {{\\n'+
'  var dict_tf_function_call = {{}};\\n'+
'  dict_tf_function_call.worker_id = String(_worker_id);\\n'+
'  dict_tf_function_call.host = String(host);\\n'+
'  dict_tf_function_call.port = Number(port_ip);\\n'+
'  dict_tf_function_call.uid = String(uid);\\n'+
'  {ssi}\\n'+
'  dict_tf_function_call.device_class_name = \\'{categoryname}\\';\\n'+
'  dict_tf_function_call.device_function_name = \\'{packetname}\\';\\n'+
'  dict_tf_function_call.device_function_input_args = [{einargs}].join(\\', \\');\\n'+
'  dict_tf_function_call.device_function_output_args = \\'{eoutargs}\\';\\n'+
'  dict_tf_function_call.device_function_output_assignment = \\'{eoutassignment}\\';\\n'+
'  postMessage(workerProtocol.getMessage(_worker_id, workerProtocol._TYPE_RES_FUNCTION_TF_CALL, dict_tf_function_call));\\n'+
'  yield 1;\\n'+
'  return _return_value;\\n'+
'}}\\n';

'''.format(blockname=block_name,
           categoryname=self.get_category().camel + self.get_name().camel,
           packetname=packet.get_name().headless,
           einargs=', '.join(packet.get_packet_elements_name_as_list(elements_in)),
           eoutargs=', '.join(packet.get_packet_elements_name_as_list(elements_out)),
           eoutassignment=out_args_assignment,
           ssi=statements_string_inputs)

                generator_code_body = returned_blockly_code + function_to_generate

                source = source + \
                         generator_code_header + \
                         generator_code_body + \
                         generator_code_footer.format(returncode='[code, Blockly.JavaScript.ORDER_FUNCTION_CALL]')

                continue

            else:
                # Setters
                if len(elements_in) < 1:
                    # Setters without in args
                    returned_blockly_code = '''  var code = 'yield *_{blockname}(' + {host} + ', ' + {port} + ', ' + {uid} + ');\\n'

'''.format(blockname=block_name,
           host='_'.join(['value', block_name, 'ipcon_host']),
           port='_'.join(['value', block_name, 'ipcon_port']),
           uid='_'.join(['value', block_name, 'ipcon_uid']))

                    function_to_generate = '''Blockly.JavaScript.definitions_['{blockname}'] = 'function *_{blockname}(host, port_ip, uid) {{\\n'+
'  var dict_tf_function_call = {{}};\\n'+
'  dict_tf_function_call.worker_id = String(_worker_id);\\n'+
'  dict_tf_function_call.host = String(host);\\n'+
'  dict_tf_function_call.port = Number(port_ip);\\n'+
'  dict_tf_function_call.uid = String(uid);\\n'+
'  dict_tf_function_call.device_class_name = \\'{categoryname}\\';\\n'+
'  dict_tf_function_call.device_function_name = \\'{packetname}\\';\\n'+
'  dict_tf_function_call.device_function_input_args = null;\\n'+
'  dict_tf_function_call.device_function_output_args = null;\\n'+
'  dict_tf_function_call.device_function_output_assignment = null;\\n'+
'  postMessage(workerProtocol.getMessage(_worker_id, workerProtocol._TYPE_RES_FUNCTION_TF_CALL, dict_tf_function_call));\\n'+
'  yield 1;\\n'+
'  return _return_value;\\n'+
'}}\\n';

'''.format(blockname=block_name,
           categoryname=self.get_category().camel + self.get_name().camel,
           packetname=packet.get_name().headless)

                else:
                    # Setters with in args
                    ret_get_hash_of_value_and_field_variables = packet.get_hash_of_value_and_field_variables(packet.get_packet_elements_name_as_list(elements_in),
                                                                                                             self.get_tvpl_device_name())
                    ret_get_list_of_value_field_statements_from_hash = packet.get_list_of_value_field_statements_from_hash(elements_in,
                                                                                                                           ret_get_hash_of_value_and_field_variables[0],
                                                                                                                           ret_get_hash_of_value_and_field_variables[1])

                    if len(ret_get_list_of_value_field_statements_from_hash[0]) > 0:
                        generator_code_header = generator_code_header + '\n'.join(ret_get_list_of_value_field_statements_from_hash[0]) + '\n'
                    if len(ret_get_list_of_value_field_statements_from_hash[1]) > 0:
                        generator_code_header = generator_code_header + '\n'.join(ret_get_list_of_value_field_statements_from_hash[1]) + '\n'

                    returned_blockly_code = '''  var code = 'yield *_{blockname}(' + {host} + ', ' + {port} + ', ' + {uid} + ', ' + {einargs} + ');\\n'

'''.format(blockname=block_name,
           host='_'.join(['value', block_name, 'ipcon_host']),
           port='_'.join(['value', block_name, 'ipcon_port']),
           uid='_'.join(['value', block_name, 'ipcon_uid']),
           einargs=packet.get_caller_generation_arguments_from_value_and_field_hash(elements_in,
                                                                                    packet.get_packet_elements_name_as_list(elements_in),
                                                                                    ret_get_hash_of_value_and_field_variables))

                    statements_string_inputs = ''

                    for e in elements_in:
                        if e.get_tvpl_type() == 'String':
                            statements_string_inputs += e.get_name().under + ' = JSON.stringify(' + e.get_name().under + ');'

                    function_to_generate = '''Blockly.JavaScript.definitions_['{blockname}'] = 'function *_{blockname}(host, port_ip, uid, {einargs}) {{\\n'+
'  var dict_tf_function_call = {{}};\\n'+
'  dict_tf_function_call.worker_id = String(_worker_id);\\n'+
'  dict_tf_function_call.host = String(host);\\n'+
'  dict_tf_function_call.port = Number(port_ip);\\n'+
'  dict_tf_function_call.uid = String(uid);\\n'+
'  {ssi}\\n'+
'  dict_tf_function_call.device_class_name = \\'{categoryname}\\';\\n'+
'  dict_tf_function_call.device_function_name = \\'{packetname}\\';\\n'+
'  dict_tf_function_call.device_function_input_args = [{einargs}].join(\\', \\');\\n'+
'  dict_tf_function_call.device_function_output_args = null;\\n'+
'  dict_tf_function_call.device_function_output_assignment = null;\\n'+
'  postMessage(workerProtocol.getMessage(_worker_id, workerProtocol._TYPE_RES_FUNCTION_TF_CALL, dict_tf_function_call));\\n'+
'  yield 1;\\n'+
'  return _return_value;\\n'+
'}}\\n';

'''.format(blockname=block_name,
           einargs=', '.join(packet.get_packet_elements_name_as_list(elements_in)),
           categoryname=self.get_category().camel + self.get_name().camel,
           packetname=packet.get_name().headless,
           ssi=statements_string_inputs)

                generator_code_body = returned_blockly_code + function_to_generate
                source = source + generator_code_header + generator_code_body + generator_code_footer.format(returncode='code')
                continue

        return source

    def get_tvpl_source_generator_python(self):
        # Exclude RED Brick
        if self.get_device_identifier() == 17:
            return ''

        source = ''

        for packet in self.get_packets('function'):
            # Exclude unrelated functions
            if packet.get_doc_type() != 'af' and \
               packet.get_doc_type() != 'bf':
                continue

            if packet.is_virtual():
                continue

            has_in_args = False
            elements_in = packet.get_elements(direction='in')
            elements_out = packet.get_elements(direction='out')
            block_name = '_'.join([self.get_tvpl_device_name(), packet.get_name().under])
            generator_code_header = '''Blockly.Python['{blockname}'] = function(block) {{
  var value_{devicename}_ipcon_uid = Blockly.Python.valueToCode(block, '_UID', Blockly.Python.ORDER_ATOMIC);
  var value_{devicename}_ipcon_host = Blockly.Python.valueToCode(block, '_HOST', Blockly.Python.ORDER_ATOMIC);
  var value_{devicename}_ipcon_port = Blockly.Python.valueToCode(block, '_PORT', Blockly.Python.ORDER_ATOMIC);
  Blockly.Python.tfAppendCleanupCall_ = true;

  if (value_{devicename}_ipcon_port === '4280') {{
    value_{devicename}_ipcon_port = 4223;
  }}
'''.format(blockname=block_name,
           devicename=self.get_tvpl_device_name())

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
'    device.set_response_expected_all(True)\\n'+
'    _device_cache[key] = device\\n'+
'\\n'+
'  return _device_cache[key]';

  Blockly.Python.definitions_['common_python_cleanup'] = 'def _cleanup():\\n'+
'  for ipcon in _ipcon_cache.values():\\n'+
'    ipcon.disconnect()';

'''
            generator_code_device_import = '''  Blockly.Python.definitions_['import_{devicename}'] = 'from tinkerforge.{devicename} import {categoryname}';

'''.format(devicename=self.get_tvpl_device_name(),
           categoryname=self.get_category().camel + self.get_name().camel)

            if len(elements_out) > 0:
                generator_code_footer = '  return [code, Blockly.Python.ORDER_FUNCTION_CALL];\n};\n\n'
            else:
                generator_code_footer = '  return code;\n};\n\n'

            function_to_generate = ''
            returned_blockly_code = ''

            if len(elements_in) > 0:
                has_in_args = True

            if not has_in_args:
                # Function without in args
                if len(elements_out) > 0:
                    # Getters
                    function_to_generate = '''  Blockly.Python.definitions_['{blockname}'] = 'def _{blockname}(host, port_ip, uid):\\n'+
'  return _get_device({categoryname}, uid, _get_ipcon(host, port)).{packetname}()';

'''.format(blockname=block_name,
           categoryname=self.get_category().camel + self.get_name().camel,
           packetname=packet.get_name().under)

                    returned_blockly_code = '''  var code = '_{blockname}(' + value_{devicename}_ipcon_host + ', ' + value_{devicename}_ipcon_port + ', ' + value_{devicename}_ipcon_uid + ')';
'''.format(blockname=block_name,
           devicename=self.get_tvpl_device_name())

                else:
                    # Setters
                    function_to_generate = '''  Blockly.Python.definitions_['{blockname}'] = 'def _{blockname}(host, port_ip, uid):\\n'+
'  _get_device({categoryname}, uid, _get_ipcon(host, port)).{packetname}()';

'''.format(blockname=block_name,
           categoryname=self.get_category().camel + self.get_name().camel,
           packetname=packet.get_name().under)

                    returned_blockly_code = '''  var code = '_{blockname}(' + value_{devicename}_ipcon_host + ', ' + value_{devicename}_ipcon_port + ', ' + value_{devicename}_ipcon_uid + ')\\n';
'''.format(blockname=block_name,
           devicename=self.get_tvpl_device_name())

            else:
                # Function with in args
                ret_get_hash_of_value_and_field_variables = packet.get_hash_of_value_and_field_variables(packet.get_packet_elements_name_as_list(elements_in),
                                                                                                         self.get_tvpl_device_name())
                ret_get_list_of_value_field_statements_from_hash = packet.get_list_of_value_field_statements_from_hash(elements_in,
                                                                                                                       ret_get_hash_of_value_and_field_variables[0],
                                                                                                                       ret_get_hash_of_value_and_field_variables[1])

                if len(ret_get_list_of_value_field_statements_from_hash[0]) > 0:
                    generator_code_header = generator_code_header + '\n'.join(ret_get_list_of_value_field_statements_from_hash[0]) + '\n'
                if len(ret_get_list_of_value_field_statements_from_hash[1]) > 0:
                    generator_code_header = generator_code_header + '\n'.join(ret_get_list_of_value_field_statements_from_hash[1]) + '\n'

                if len(elements_out) > 0:
                    # Getters
                    function_to_generate = '''  Blockly.Python.definitions_['{blockname}'] = 'def _{blockname}(host, port_ip, uid, {einargs}):\\n'+
'  return _get_device({categoryname}, uid, _get_ipcon(host, port)).{packetname}({einargs})';

'''.format(blockname=block_name,
           einargs=', '.join(packet.get_packet_elements_name_as_list(elements_in)),
           categoryname=self.get_category().camel + self.get_name().camel,
           packetname=packet.get_name().under)

                    returned_blockly_code = '''  var code = '_{blockname}(' + String(value_{devicename}_ipcon_host) + ', ' + String(value_{devicename}_ipcon_port) + ', ' + String(value_{devicename}_ipcon_uid) + ', ' + {einargs} + ')';
'''.format(blockname=block_name,
           devicename=self.get_tvpl_device_name(),
           einargs=packet.get_caller_generation_arguments_from_value_and_field_hash(elements_in,
                                                                                    packet.get_packet_elements_name_as_list(elements_in),
                                                                                    ret_get_hash_of_value_and_field_variables))

                else:
                    # Setters
                    function_to_generate = '''  Blockly.Python.definitions_['{blockname}'] = 'def _{blockname}(host, port_ip, uid, {einargs}):\\n'+
'  _get_device({categoryname}, uid, _get_ipcon(host, port)).{packetname}({einargs})';

'''.format(blockname=block_name,
           einargs=', '.join(packet.get_packet_elements_name_as_list(elements_in)),
           categoryname=self.get_category().camel + self.get_name().camel,
           packetname=packet.get_name().under)

                    returned_blockly_code = '''  var code = '_{blockname}(' + String(value_{devicename}_ipcon_host) + ', ' + String(value_{devicename}_ipcon_port) + ', ' + String(value_{devicename}_ipcon_uid) + ', ' + {einargs} + ')\\n';
'''.format(blockname=block_name,
           devicename=self.get_tvpl_device_name(),
           einargs=packet.get_caller_generation_arguments_from_value_and_field_hash(elements_in,
                                                                                    packet.get_packet_elements_name_as_list(elements_in),
                                                                                    ret_get_hash_of_value_and_field_variables))

            source = source + \
                     generator_code_header + \
                     generator_code_fixed_definitions + \
                     generator_code_device_import + \
                     function_to_generate + \
                     returned_blockly_code + \
                     generator_code_footer

        return source

class TVPLBindingsPacket(tvpl_common.TVPLPacket):
    def get_hash_of_value_and_field_variables(self, elements, device_name):
        hash_value_to_code_variable = {}
        hash_get_field_value_variable = {}

        for e in elements:
            hash_value_to_code_variable[e] = 'value_' + device_name + '_' + e
            hash_get_field_value_variable[e] = 'value_' + device_name + '_' + e

        return (hash_value_to_code_variable, hash_get_field_value_variable)

    def get_list_of_value_field_statements_from_hash(self,
                                                     elements,
                                                     hash_value_to_code_variable,
                                                     hash_get_field_value_variable):
        list_blockly_value_to_code_statements = []
        list_blockly_get_field_value_statements = []

        for e in elements:
            if e.get_constant_group() or e.get_tvpl_type() == 'Boolean':
                list_blockly_get_field_value_statements.append('''  var {fieldvaluevariable} = block.getFieldValue('{eupper}');'''.format(fieldvaluevariable=hash_get_field_value_variable[e.get_name().under],
                                                                                                                                          eupper=e.get_name().upper))
            else:
                list_blockly_value_to_code_statements.append('''  var {valuetocodevariable} = Blockly.JavaScript.valueToCode(block, '{eupper}', Blockly.JavaScript.ORDER_ATOMIC);'''.format(valuetocodevariable=hash_value_to_code_variable[e.get_name().under],
                                                                                                                                                                                            eupper=e.get_name().upper))
        return (list_blockly_value_to_code_statements, list_blockly_get_field_value_statements)

    def get_caller_generation_arguments_from_value_and_field_hash(self,
                                                                  ein,
                                                                  under_names,
                                                                  ret_get_hash_of_value_and_field_variables):
        function_in_args = ''
        is_input_type_string = False

        for i, e in enumerate(under_names):
            for ein_e in ein:
                if ein_e.get_name().under == e and ein_e.get_tvpl_type() == 'String':
                    is_input_type_string = True

            if e in ret_get_hash_of_value_and_field_variables[0]:
                if function_in_args == '':
                    if is_input_type_string:
                        function_in_args = '\'String(\' + ' + 'String(' + ret_get_hash_of_value_and_field_variables[0][e] + ')' + ' + \')\''
                    else:
                        function_in_args = 'String(' + ret_get_hash_of_value_and_field_variables[0][e] + ')'

                    if i < len(under_names) - 1:
                        function_in_args = function_in_args + ' + \', \' + '
                else:
                    if is_input_type_string:
                        function_in_args = function_in_args + '\'String(\' + ' + 'String(' + ret_get_hash_of_value_and_field_variables[0][e] + ')' + ' + \')\''
                    else:
                        function_in_args = function_in_args + 'String(' + ret_get_hash_of_value_and_field_variables[0][e] + ')'

                    if i < len(under_names) - 1:
                        function_in_args = function_in_args + ' + \', \' + '
            elif e in ret_get_hash_of_value_and_field_variables[1]:
                if function_in_args == '':
                    if is_input_type_string:
                        function_in_args = '\'String(\' + ' + 'String(' + ret_get_hash_of_value_and_field_variables[1][e] + ')' + ' + \')\''
                    else:
                        function_in_args = 'String(' + ret_get_hash_of_value_and_field_variables[1][e] + ')'

                    if i < len(under_names) - 1:
                        function_in_args = function_in_args + ' + \', \' + '
                else:
                    if is_input_type_string:
                        function_in_args = function_in_args + '\'String(\' + ' + 'String(' + ret_get_hash_of_value_and_field_variables[1][e] + ')' + ' + \')\''
                    else:
                        function_in_args = function_in_args + 'String(' + ret_get_hash_of_value_and_field_variables[1][e] + ')'

                    if i < len(under_names) - 1:
                        function_in_args = function_in_args + ' + \', \' + '

        return function_in_args

class TVPLBindingsGenerator(common.BindingsGenerator):
    def get_bindings_name(self):
        return 'tvpl'

    def get_bindings_display_name(self):
        return 'Tinkerforge Visual Programming Language (TVPL)'

    def get_device_class(self):
        return TVPLBindingsDevice

    def get_packet_class(self):
        return TVPLBindingsPacket

    def get_element_class(self):
        return tvpl_common.TVPLElement

    def prepare(self):
        return common.BindingsGenerator.prepare(self)

    def generate(self, device):
        filename_tvpl_block = '{devicecategory}_{devicename}.block'.format(devicecategory=device.get_category().under,
                                                                           devicename=device.get_name().under)
        filename_tvpl_code_generator_javascript = '{devicecategory}_{devicename}.generator.javascript'.format(devicecategory=device.get_category().under,
                                                                                                              devicename=device.get_name().under)
        filename_tvpl_code_generator_python = '{devicecategory}_{devicename}.generator.python'.format(devicecategory=device.get_category().under,
                                                                                                      devicename=device.get_name().under)

        with open(os.path.join(self.get_bindings_dir(), filename_tvpl_block), 'w') as f:
            f.write(device.get_tvpl_source_block())

        with open(os.path.join(self.get_bindings_dir(), filename_tvpl_code_generator_javascript), 'w') as f:
            f.write(device.get_tvpl_source_generator_javascript())

        with open(os.path.join(self.get_bindings_dir(), filename_tvpl_code_generator_python), 'w') as f:
            f.write(device.get_tvpl_source_generator_python())

        if device.is_released():
            self.released_files.append('_'.join([device.get_category().under, device.get_name().under]))

    def finish(self):
        return common.BindingsGenerator.finish(self)

def generate(root_dir):
    common.generate(root_dir, 'en', TVPLBindingsGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
