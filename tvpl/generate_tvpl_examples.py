#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tinkerforge Visual Programming Language (TVPL) Examples Generator
Copyright (C) 2015-2016 Matthias Bolte <matthias@tinkerforge.com>

generate_tvpl_examples.py: Generator for TVPL examples

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
import xml.etree.ElementTree as ET
import xml.dom.minidom

sys.path.append(os.path.split(os.getcwd())[0])
import common

global_line_prefix = ''

def add_tvpl_text_block(parent, text):
    block = ET.SubElement(parent, 'block', {'type': 'text'})
    field = ET.SubElement(block, 'field', {'name': 'TEXT'})
    field.text = text

def add_tvpl_text_value(parent, name, text):
    value = ET.SubElement(parent, 'value', {'name': name})
    add_tvpl_text_block(value, text)

def add_tvpl_number_block(parent, number):
    block = ET.SubElement(parent, 'block', {'type': 'math_number'})
    field = ET.SubElement(block, 'field', {'name': 'NUM'})
    field.text = str(number)

def add_tvpl_number_value(parent, name, number):
    value = ET.SubElement(parent, 'value', {'name': name})
    add_tvpl_number_block(value, number)

def add_tvpl_print_block(parent):
    block = ET.SubElement(parent, 'block', {'type': 'text_print'})
    value = ET.SubElement(block, 'value', {'name': 'TEXT'})
    next = ET.SubElement(block, 'next')
    return value, next

def add_tvpl_join_block(parent, count):
    block = ET.SubElement(parent, 'block', {'type': 'text_join'})
    ET.SubElement(block, 'mutation', {'items': str(count)})
    items = []

    for i in range(count):
        items.append(ET.SubElement(block, 'value', {'name': 'ADD{0}'.format(i)}))

    return items

def add_tvpl_set_variable_block(parent, variable):
    block = ET.SubElement(parent, 'block', {'type': 'variables_set'})
    field = ET.SubElement(block, 'field', {'name': 'VAR'})
    field.text = variable
    value = ET.SubElement(block, 'value', {'name': 'VALUE'})
    next = ET.SubElement(block, 'next')
    return value, next

def add_tvpl_get_variable_block(parent, variable):
    block = ET.SubElement(parent, 'block', {'type': 'variables_get'})
    field = ET.SubElement(block, 'field', {'name': 'VAR'})
    field.text = variable

def add_tvpl_get_list_item_block(parent, variable, index):
    block = ET.SubElement(parent, 'block', {'type': 'lists_getIndex'})
    ET.SubElement(block, 'mutation', {'statement': 'false', 'at': 'true'})
    mode_field = ET.SubElement(block, 'field', {'name': 'MODE'})
    mode_field.text = 'GET'
    where_field = ET.SubElement(block, 'field', {'name': 'WHERE'})
    where_field.text = 'FROM_START'
    value_value = ET.SubElement(block, 'value', {'name': 'VALUE'})
    value_at = ET.SubElement(block, 'value', {'name': 'AT'})
    add_tvpl_get_variable_block(value_value, variable)
    add_tvpl_number_block(value_at, index)

def add_tvpl_arithmetic_block(parent, operator):
    block = ET.SubElement(parent, 'block', {'type': 'math_arithmetic'})
    field = ET.SubElement(block, 'field', {'name': 'OP'})
    field.text = operator
    value_op0 = ET.SubElement(block, 'value', {'name': 'A'})
    value_op1 = ET.SubElement(block, 'value', {'name': 'B'})
    return value_op0, value_op1

class TVPLConstant(common.Constant):
    def get_tvpl_source(self):
        template = '{device_initial_name}.{constant_group_upper_case_name}_{constant_upper_case_name}'

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               constant_group_upper_case_name=self.get_constant_group().get_upper_case_name(),
                               constant_upper_case_name=self.get_upper_case_name())

class TVPLExample(common.Example):
    def get_tvpl_source(self):
        root = ET.Element('xml', {'xmlns': 'http://www.w3.org/1999/xhtml'})
        tvpl = ET.SubElement(root, 'tvpl')
        program = ET.SubElement(tvpl, 'program')
        gui = ET.SubElement(tvpl, 'gui')
        parent = program

        for function in self.get_functions():
            if isinstance(function, TVPLExampleGetterFunction) or \
               isinstance(function, TVPLExampleSetterFunction):
                parent = function.add_tvpl_subelement(parent)

        return xml.dom.minidom.parseString(ET.tostring(root, encoding='utf-8')).toprettyxml(indent='  ').replace('<?xml version="1.0" ?>\n', '')



        template = r"""#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
UID = "{dummy_uid}" # Change to your UID
{imports}
from tinkerforge.ip_connection import IPConnection
from tinkerforge.{device_underscore_category}_{device_underscore_name} import {device_camel_case_category}{device_camel_case_name}
{functions}
if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    {device_initial_name} = {device_camel_case_category}{device_camel_case_name}(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected
{sources}
    raw_input("Press key to exit\n") # Use input() in TVPL 3{cleanups}
    ipcon.disconnect()
"""

        if self.is_incomplete():
            template = "# FIXME: This example is incomplete\n\n" + template

        imports = []
        functions = []
        sources = []
        cleanups = []

        for function in self.get_functions():
            imports += function.get_tvpl_imports()
            functions.append(function.get_tvpl_function())
            sources.append(function.get_tvpl_source())

        for cleanup in self.get_cleanups():
            imports += cleanup.get_tvpl_imports()
            functions.append(cleanup.get_tvpl_function())
            cleanups.append(cleanup.get_tvpl_source())

        unique_imports = []

        for import_ in imports:
            if import_ not in unique_imports:
                unique_imports.append(import_)

        while None in functions:
            functions.remove(None)

        if len(sources) == 0:
            sources = ['    # TODO: Add example code here\n']

        return template.format(device_camel_case_category=self.get_device().get_camel_case_category(),
                               device_underscore_category=self.get_device().get_underscore_category(),
                               device_camel_case_name=self.get_device().get_camel_case_name(),
                               device_underscore_name=self.get_device().get_underscore_name(),
                               device_initial_name=self.get_device().get_initial_name(),
                               dummy_uid=self.get_dummy_uid(),
                               imports=common.wrap_non_empty('\n', ''.join(unique_imports), ''),
                               functions=common.wrap_non_empty('\n', '\n'.join(functions), ''),
                               sources='\n' + '\n'.join(sources).replace('\n\r', '').lstrip('\r'),
                               cleanups=common.wrap_non_empty('\n', '\n'.join(cleanups).replace('\n\r', '').lstrip('\r').rstrip('\n'), ''))

class TVPLExampleArgument(common.ExampleArgument):
    def add_tvpl_subelement(self, parent):
        upper_case_name = self.get_element().get_upper_case_name()

        if self.get_value_constant() != None:
            field = ET.SubElement(parent, 'field', {'name': upper_case_name})
            field.text = str(self.get_value())
        elif self.get_type() == 'bool':
            field = ET.SubElement(parent, 'field', {'name': upper_case_name})

            if self.get_value():
                field.text = '1'
            else:
                field.text = '0'
        else:
            value = ET.SubElement(parent, 'value', {'name': upper_case_name})
            block_type, field_name = self.get_tvpl_type()
            block = ET.SubElement(value, 'block', {'type': block_type})
            field = ET.SubElement(block, 'field', {'name': field_name})
            field.text = self.get_tvpl_value()

    def get_tvpl_type(self):
        type = self.get_type()

        if type == 'bool':
            return 'logic_boolean', 'BOOL'
        elif type in  ['char', 'string']:
            return 'text', 'TEXT'
        else:
            return 'math_number', 'NUM'

    def get_tvpl_value(self):
        type = self.get_type()
        value = self.get_value()

        if type == 'bool':
            if value:
                return 'TRUE'
            else:
                return 'FALSE'
        else:
            return str(value)

class TVPLExampleParameter(common.ExampleParameter):
    def get_tvpl_source_X(self):
        return self.get_underscore_name()

    def get_tvpl_print_X(self):
        template = '    print("{label_name}: " + {format_prefix}{underscore_name}{divisor}{format_suffix}{unit_final_name})'

        if self.get_label_name() == None:
            return None

        type = self.get_type()

        if ':bitmask:' in type:
            format_prefix = 'format('
            format_suffix = ', "0{0}b")'.format(int(type.split(':')[2]))
        elif type in ['char', 'string']:
            format_prefix = ''
            format_suffix = ''
        else:
            format_prefix = 'str('
            format_suffix = ')'

        return template.format(underscore_name=self.get_underscore_name(),
                               label_name=self.get_label_name(),
                               divisor=self.get_formatted_divisor('/{0}'),
                               unit_final_name=self.get_unit_formatted_final_name(' + " {0}"'),
                               format_prefix=format_prefix,
                               format_suffix=format_suffix)

class TVPLExampleResult(common.ExampleResult):
    def get_tvpl_variable(self):
        return self.get_name()

    def add_tvpl_print_block(self, parent, list_variable, list_index):
        print_value, print_next = add_tvpl_print_block(parent)
        unit_final_name = self.get_unit_formatted_final_name(' {0}')

        if len(unit_final_name) > 0:
            join_items = add_tvpl_join_block(print_value, 3)
        else:
            join_items = add_tvpl_join_block(print_value, 2)

        add_tvpl_text_block(join_items[0], '{0}: '.format(self.get_label_name()))

        divisor = self.get_divisor()

        if divisor != None:
            divide_op0, divide_op1 = add_tvpl_arithmetic_block(join_items[1], 'DIVIDE')

            if list_variable != None:
                add_tvpl_get_list_item_block(divide_op0, list_variable, list_index)
            else:
                add_tvpl_get_variable_block(divide_op0, self.get_name())

            add_tvpl_number_block(divide_op1, divisor)
        else:
            if list_variable != None:
                add_tvpl_get_list_item_block(join_items[1], list_variable, list_index)
            else:
                add_tvpl_get_variable_block(join_items[1], self.get_name())

        if len(unit_final_name) > 0:
            add_tvpl_text_block(join_items[2], unit_final_name.decode('utf-8'))

        return print_next

    def get_tvpl_print_X(self):
        template = '    print("{label_name}: " + {format_prefix}{underscore_name}{divisor}{format_suffix}{unit_final_name})'

        underscore_name = self.get_underscore_name()

        if underscore_name == self.get_device().get_initial_name():
            underscore_name += '_'

        type = self.get_type()

        if ':bitmask:' in type:
            format_prefix = 'format('
            format_suffix = ', "0{0}b")'.format(int(type.split(':')[2]))
        elif type in ['char', 'string']:
            format_prefix = ''
            format_suffix = ''
        else:
            format_prefix = 'str('
            format_suffix = ')'

        return template.format(underscore_name=underscore_name,
                               label_name=self.get_label_name(),
                               divisor=self.get_formatted_divisor('/{0}'),
                               unit_final_name=self.get_unit_formatted_final_name(' + " {0}"'),
                               format_prefix=format_prefix,
                               format_suffix=format_suffix)

class TVPLExampleGetterFunction(common.ExampleGetterFunction):
    def add_tvpl_subelement(self, parent):
        variables = []

        for result in self.get_results():
            variables.append(result.get_tvpl_variable())

        if len(variables) > 1:
            variable = self.get_name(skip=1)
        else:
            variable = variables[0]

        set_variable_block, set_variable_next = add_tvpl_set_variable_block(parent, variable)
        device_block = ET.SubElement(set_variable_block, 'block',
                                     {'type': '{device_underscore_category}_{device_underscore_name}_{function_underscore_name}'
                                              .format(device_underscore_category=self.get_device().get_underscore_category(),
                                                      device_underscore_name=self.get_device().get_underscore_name(),
                                                      function_underscore_name=self.get_underscore_name())})

        for argument in self.get_arguments():
            argument.add_tvpl_subelement(device_block)

        add_tvpl_text_value(device_block, '_UID', 'XYZ')
        add_tvpl_text_value(device_block, '_HOST', 'localhost')
        add_tvpl_number_value(device_block, '_PORT', 4280)

        if len(variables) > 1:
            variable = self.get_name(skip=1)
        else:
            variable = None

        result_parent = set_variable_next

        for i, result in enumerate(self.get_results()):
            result_parent = result.add_tvpl_print_block(result_parent, variable, i + 1)

        return result_parent

    def get_tvpl_source_X(self):
        template = r"""    # Get current {function_comment_name}{comments}
    {variables} = {device_initial_name}.{function_underscore_name}({arguments})
{prints}
"""
        comments = []
        variables = []
        prints = []

        for result in self.get_results():
            comments.append(result.get_formatted_comment())
            variables.append(result.get_tvpl_variable())
            prints.append(result.get_tvpl_print())

        if len(comments) > 1 and len(set(comments)) == 1:
            comments = comments[:1]

        if len(prints) > 1:
            prints.insert(0, '')

        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_tvpl_source())

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               function_underscore_name=self.get_underscore_name(),
                               function_comment_name=self.get_comment_name(),
                               comments=''.join(comments),
                               variables=', '.join(variables),
                               prints='\n'.join(prints),
                               arguments=', '.join(arguments))

class TVPLExampleSetterFunction(common.ExampleSetterFunction):
    def add_tvpl_subelement(self, parent):
        device_block = ET.SubElement(parent, 'block',
                                     {'type': '{device_underscore_category}_{device_underscore_name}_{function_underscore_name}'
                                              .format(device_underscore_category=self.get_device().get_underscore_category(),
                                                      device_underscore_name=self.get_device().get_underscore_name(),
                                                      function_underscore_name=self.get_underscore_name())})

        for argument in self.get_arguments():
            argument.add_tvpl_subelement(device_block)

        add_tvpl_text_value(device_block, '_UID', 'XYZ')
        add_tvpl_text_value(device_block, '_HOST', 'localhost')
        add_tvpl_number_value(device_block, '_PORT', 4280)

        return ET.SubElement(device_block, 'next')

    def get_tvpl_source_X(self):
        template = '{comment1}{global_line_prefix}    {device_initial_name}.{function_underscore_name}({arguments}){comment2}\n'
        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_tvpl_source())

        return template.format(global_line_prefix=global_line_prefix,
                               device_initial_name=self.get_device().get_initial_name(),
                               function_underscore_name=self.get_underscore_name(),
                               arguments=', '.join(arguments),
                               comment1=self.get_formatted_comment1(global_line_prefix + '    # {0}\n', '\r', '\n' + global_line_prefix + '    # '),
                               comment2=self.get_formatted_comment2(' # {0}', ''))

class TVPLExampleCallbackFunction(common.ExampleCallbackFunction):
    def get_tvpl_imports(self):
        return []

    def get_tvpl_function(self):
        template1A = r"""# Callback function for {function_comment_name} callback{comments}
"""
        template1B = r"""{override_comment}
"""
        template2 = r"""def cb_{function_underscore_name}({parameters}):
{prints}{extra_message}
"""
        override_comment = self.get_formatted_override_comment('# {0}', None, '\n# ')

        if override_comment == None:
            template1 = template1A
        else:
            template1 = template1B

        comments = []
        parameters = []
        prints = []

        for parameter in self.get_parameters():
            comments.append(parameter.get_formatted_comment())
            parameters.append(parameter.get_tvpl_source())
            prints.append(parameter.get_tvpl_print())

        if len(comments) > 1 and len(set(comments)) == 1:
            comments = [comments[0].replace('parameter has', 'parameters have')]

        while None in prints:
            prints.remove(None)

        if len(prints) > 1:
            prints.append('    print("")')

        extra_message = self.get_formatted_extra_message('    print("{0}")')

        if len(extra_message) > 0 and len(prints) > 0:
            extra_message = '\n' + extra_message

        return template1.format(function_comment_name=self.get_comment_name(),
                                comments=''.join(comments),
                                override_comment=override_comment) + \
               template2.format(function_underscore_name=self.get_underscore_name(),
                                parameters=', '.join(parameters),
                                prints='\n'.join(prints),
                                extra_message=extra_message)

    def get_tvpl_source(self):
        template = r"""    # Register {function_comment_name} callback to function cb_{function_underscore_name}
    {device_initial_name}.register_callback({device_initial_name}.CALLBACK_{function_upper_case_name}, cb_{function_underscore_name})
"""

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               function_underscore_name=self.get_underscore_name(),
                               function_upper_case_name=self.get_upper_case_name(),
                               function_comment_name=self.get_comment_name())

class TVPLExampleCallbackPeriodFunction(common.ExampleCallbackPeriodFunction):
    def get_tvpl_imports(self):
        return []

    def get_tvpl_function(self):
        return None

    def get_tvpl_source(self):
        templateA = r"""    # Set period for {function_comment_name} callback to {period_sec_short} ({period_msec}ms)
    {device_initial_name}.set_{function_underscore_name}{suffix}_period({arguments}{period_msec})
"""
        templateB = r"""    # Set period for {function_comment_name} callback to {period_sec_short} ({period_msec}ms)
    # Note: The {function_comment_name} callback is only called every {period_sec_long}
    #       if the {function_comment_name} has changed since the last call!
    {device_initial_name}.set_{function_underscore_name}{suffix}_period({arguments}{period_msec})
"""

        if self.get_device().get_underscore_name().startswith('imu'):
            template = templateA # FIXME: special hack for IMU Brick (2.0) callback behavior
            suffix = '' # FIXME: special hack for IMU Brick name mismatch
        else:
            template = templateB
            suffix = '_callback'

        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_tvpl_source())

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               function_underscore_name=self.get_underscore_name(),
                               function_comment_name=self.get_comment_name(),
                               suffix=suffix,
                               arguments=common.wrap_non_empty('', ', '.join(arguments), ', '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long)

class TVPLExampleCallbackThresholdMinimumMaximum(common.ExampleCallbackThresholdMinimumMaximum):
    def get_tvpl_source(self):
        template = '{minimum}, {maximum}'

        return template.format(minimum=self.get_formatted_minimum(),
                               maximum=self.get_formatted_maximum())

class TVPLExampleCallbackThresholdFunction(common.ExampleCallbackThresholdFunction):
    def get_tvpl_imports(self):
        return []

    def get_tvpl_function(self):
        return None

    def get_tvpl_source(self):
        template = r"""    # Configure threshold for {function_comment_name} "{option_comment}"{mininum_maximum_unit_comments}
    {device_initial_name}.set_{function_underscore_name}_callback_threshold({arguments}"{option_char}", {mininum_maximums})
"""
        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_tvpl_source())

        mininum_maximums = []
        mininum_maximum_unit_comments = []

        for mininum_maximum in self.get_minimum_maximums():
            mininum_maximums.append(mininum_maximum.get_tvpl_source())
            mininum_maximum_unit_comments.append(mininum_maximum.get_unit_comment())

        if len(mininum_maximum_unit_comments) > 1 and len(set(mininum_maximum_unit_comments)) == 1:
            mininum_maximum_unit_comments = mininum_maximum_unit_comments[:1]

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               function_underscore_name=self.get_underscore_name(),
                               function_comment_name=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(arguments), ', '),
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               mininum_maximums=', '.join(mininum_maximums),
                               mininum_maximum_unit_comments=''.join(mininum_maximum_unit_comments))

class TVPLExampleSpecialFunction(common.ExampleSpecialFunction):
    def get_tvpl_imports(self):
        if self.get_type() == 'sleep':
            return ['import time\n']
        else:
            return []

    def get_tvpl_function(self):
        return None

    def get_tvpl_source(self):
        global global_line_prefix

        type = self.get_type()

        if type == 'empty':
            return ''
        elif type == 'debounce_period':
            template = r"""    # Get threshold callbacks with a debounce time of {period_sec} ({period_msec}ms)
    {device_initial_name}.set_debounce_period({period_msec})
"""
            period_msec, period_sec = self.get_formatted_debounce_period()

            return template.format(device_initial_name=self.get_device().get_initial_name(),
                                   period_msec=period_msec,
                                   period_sec=period_sec)
        elif type == 'sleep':
            template = '{comment1}{global_line_prefix}    time.sleep({duration}){comment2}\n'
            duration = self.get_sleep_duration()

            if duration % 1000 == 0:
                duration //= 1000
            else:
                duration /= 1000.0

            return template.format(global_line_prefix=global_line_prefix,
                                   duration=duration,
                                   comment1=self.get_formatted_sleep_comment1(global_line_prefix + '    # {0}\n', '\r', '\n' + global_line_prefix + '    # '),
                                   comment2=self.get_formatted_sleep_comment2(' # {0}', ''))
        elif type == 'wait':
            return None
        elif type == 'loop_header':
            template = '{comment}    for i in range({limit}):\n'
            global_line_prefix = '    '

            return template.format(limit=self.get_loop_header_limit(),
                                   comment=self.get_formatted_loop_header_comment('    # {0}\n', '', '\n    # '))
        elif type == 'loop_footer':
            global_line_prefix = ''

            return '\r'

class TVPLExamplesGenerator(common.ExamplesGenerator):
    def get_bindings_name(self):
        return 'tvpl'

    def get_constant_class(self):
        return TVPLConstant

    def get_example_class(self):
        return TVPLExample

    def get_example_argument_class(self):
        return TVPLExampleArgument

    def get_example_parameter_class(self):
        return TVPLExampleParameter

    def get_example_result_class(self):
        return TVPLExampleResult

    def get_example_getter_function_class(self):
        return TVPLExampleGetterFunction

    def get_example_setter_function_class(self):
        return TVPLExampleSetterFunction

    def get_example_callback_function_class(self):
        return TVPLExampleCallbackFunction

    def get_example_callback_period_function_class(self):
        return TVPLExampleCallbackPeriodFunction

    def get_example_callback_threshold_minimum_maximum_class(self):
        return TVPLExampleCallbackThresholdMinimumMaximum

    def get_example_callback_threshold_function_class(self):
        return TVPLExampleCallbackThresholdFunction

    def get_example_special_function_class(self):
        return TVPLExampleSpecialFunction

    def generate(self, device):
        if os.getenv('TINKERFORGE_GENERATE_EXAMPLES_FOR_DEVICE', device.get_camel_case_name()) != device.get_camel_case_name():
            return

        examples_directory = self.get_examples_directory(device)
        examples = device.get_examples()

        if len(examples) == 0:
            print('  \033[01;31m- no examples\033[0m')
            return

        if not os.path.exists(examples_directory):
            os.makedirs(examples_directory)

        blacklist = [
            'lcd-16x2-bricklet/unicode',
            'lcd-20x4-bricklet/unicode'
        ]

        for example in examples:
            filename = 'example_{0}.tvpl'.format(example.get_underscore_name())
            filepath = os.path.join(examples_directory, filename)

            if device.get_git_name() + '/' + example.get_dash_name() in blacklist:
                print('  - ' + filename + ' \033[01;35m(blacklisted, skipped)\033[0m')
                continue

            has_callbacks = False

            for function in example.get_functions():
                if isinstance(function, TVPLExampleCallbackFunction):
                    has_callbacks = True

            if has_callbacks:
                print('  - ' + filename + ' \033[01;35m(callback, skipped)\033[0m')
                continue

            if example.is_incomplete():
                if os.path.exists(filepath) and self.skip_existing_incomplete_example:
                    print('  - ' + filename + ' \033[01;35m(incomplete, skipped)\033[0m')
                    continue
                else:
                    print('  - ' + filename + ' \033[01;31m(incomplete)\033[0m')
            else:
                print('  - ' + filename)

            tvpl = open(filepath, 'wb')
            tvpl.write(example.get_tvpl_source().encode('utf-8'))
            tvpl.close()

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', TVPLExamplesGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
