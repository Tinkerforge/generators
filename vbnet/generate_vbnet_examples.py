#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Visual Basic .NET Examples Generator
Copyright (C) 2015-2017 Matthias Bolte <matthias@tinkerforge.com>

generate_vbnet_examples.py: Generator for Visual Basic .NET examples

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

sys.path.append(os.path.split(os.getcwd())[0])
import common

global_line_prefix = ''

vbnet_types = {
    'int8':   'Short',
    'uint8':  'Byte',
    'int16':  'Short',
    'uint16': 'Integer',
    'int32':  'Integer',
    'uint32': 'Long',
    'int64':  'Long',
    'uint64': 'Long',
    'float':  'Single',
    'bool':   'Boolean',
    'char':   'Char',
    'string': 'String'
}

def get_vbnet_type(type_):
     return vbnet_types[type_]

class VBNETConstant(common.Constant):
    def get_vbnet_source(self):
        template = '{device_camel_case_category}{device_camel_case_name}.{constant_group_upper_case_name}_{constant_upper_case_name}'

        return template.format(device_camel_case_category=self.get_device().get_camel_case_category(),
                               device_camel_case_name=self.get_device().get_camel_case_name(),
                               constant_group_upper_case_name=self.get_constant_group().get_upper_case_name(),
                               constant_upper_case_name=self.get_upper_case_name())

class VBNETExample(common.Example):
    def get_vbnet_source(self):
        template = r"""Imports System
{imports}Imports Tinkerforge{incomplete}{description}

Module Example{example_camel_case_name}
    Const HOST As String = "localhost"
    Const PORT As Integer = 4223
    Const UID As String = "{dummy_uid}" ' Change {dummy_uid} to the UID of your {device_long_display_name}
{subroutines}
    Sub Main()
        Dim ipcon As New IPConnection() ' Create IP connection
        Dim {device_initial_name} As New {device_camel_case_category}{device_camel_case_name}(UID, ipcon) ' Create device object

        ipcon.Connect(HOST, PORT) ' Connect to brickd
        ' Don't use device before ipcon is connected
{sources}
        Console.WriteLine("Press key to exit")
        Console.ReadLine(){cleanups}
        ipcon.Disconnect()
    End Sub
End Module
"""
        if self.is_incomplete():
            incomplete = "\n\n' FIXME: This example is incomplete"
        else:
            incomplete = ''

        if self.get_description() != None:
            description = "\n\n' {0}".format(self.get_description().replace('\n', "\n' "))
        else:
            description = ''

        imports = []
        subroutines = []
        sources = []
        cleanups = []

        for function in self.get_functions():
            imports += function.get_vbnet_imports()
            subroutines.append(function.get_vbnet_subroutine())
            sources.append(function.get_vbnet_source())

        for cleanup in self.get_cleanups():
            imports += function.get_vbnet_imports()
            subroutines.append(cleanup.get_vbnet_subroutine())
            cleanups.append(cleanup.get_vbnet_source())

        unique_imports = []

        for import_ in imports:
            if import_ not in unique_imports:
                unique_imports.append(import_)

        while None in subroutines:
            subroutines.remove(None)

        while None in sources:
            sources.remove(None)

        if len(sources) == 0:
            sources = ["        ' TODO: Add example code here\n"]

        while None in cleanups:
            cleanups.remove(None)

        return template.format(incomplete=incomplete,
                               description=description,
                               example_camel_case_name=self.get_camel_case_name(),
                               device_camel_case_category=self.get_device().get_camel_case_category(),
                               device_camel_case_name=self.get_device().get_camel_case_name(),
                               device_initial_name=self.get_device().get_initial_name(),
                               device_long_display_name=self.get_device().get_long_display_name(),
                               dummy_uid=self.get_dummy_uid(),
                               imports=''.join(unique_imports),
                               subroutines=common.wrap_non_empty('\n', '\n'.join(subroutines), ''),
                               sources='\n' + '\n'.join(sources).replace('\n\r', '').lstrip('\r'),
                               cleanups=common.wrap_non_empty('\n', '\n'.join(cleanups).replace('\n\r', '').lstrip('\r').rstrip('\n'), ''))

class VBNETExampleArgument(common.ExampleArgument):
    def get_vbnet_source(self):
        type_ = self.get_type()
        value = self.get_value()

        if type_ == 'bool':
            if value:
                return 'True'
            else:
                return 'False'
        elif type_ == 'char':
            return '"{0}"C'.format(value)
        elif type_ == 'string':
            return '"{0}"'.format(value)
        elif ':bitmask:' in type_:
            return common.make_c_like_bitmask(value, combine='({0}) or ({1})')
        elif type_.endswith(':constant'):
            return self.get_value_constant().get_vbnet_source()
        else:
            return str(value)

class VBNETExampleParameter(common.ExampleParameter):
    def get_vbnet_source(self):
        template = 'ByVal {headless_camel_case_name} As {type}'

        return template.format(type=get_vbnet_type(self.get_type().split(':')[0]),
                               headless_camel_case_name=self.get_headless_camel_case_name())

    def get_vbnet_write_line(self):
        template = '        Console.WriteLine("{label_name}: " + {to_string_prefix}{headless_camel_case_name}{divisor}{to_string_suffix}{unit_final_name})'

        if self.get_label_name() == None:
            return None

        type_ = self.get_type()
        divisor = self.get_formatted_divisor('/{0}')

        # FIXME: Convert.ToString() doesn't support leading zeros. therefore,
        #        the result is not padded to the requested number of digits
        if ':bitmask:' in self.get_type():
            to_string_prefix = 'Convert.ToString('
            to_string_suffix = ', 2)'
        elif type_ in ['char', 'string']:
            to_string_prefix = ''
            to_string_suffix = ''
        elif len(divisor) > 0:
            to_string_prefix = '('
            to_string_suffix = ').ToString()'
        else:
            to_string_prefix = ''
            to_string_suffix = '.ToString()'

        return template.format(headless_camel_case_name=self.get_headless_camel_case_name(),
                               label_name=self.get_label_name(),
                               to_string_prefix=to_string_prefix,
                               to_string_suffix=to_string_suffix,
                               divisor=divisor,
                               unit_final_name=self.get_unit_formatted_final_name(' + " {0}"'))

class VBNETExampleResult(common.ExampleResult):
    def get_vbnet_variable_declaration(self):
        template = '        Dim {headless_camel_case_name} As {type_}'
        headless_camel_case_name = self.get_headless_camel_case_name()

        if headless_camel_case_name == self.get_device().get_initial_name():
            headless_camel_case_name += '_'

        return template.format(type_=get_vbnet_type(self.get_type().split(':')[0]),
                               headless_camel_case_name=headless_camel_case_name)

    def get_vbnet_variable_reference(self):
        headless_camel_case_name = self.get_headless_camel_case_name()

        if headless_camel_case_name == self.get_device().get_initial_name():
            headless_camel_case_name += '_'

        return headless_camel_case_name

    def get_vbnet_write_line(self):
        template = '        Console.WriteLine("{label_name}: " + {to_string_prefix}{headless_camel_case_name}{divisor}{to_string_suffix}{unit_final_name})'

        if self.get_label_name() == None:
            return None

        headless_camel_case_name = self.get_headless_camel_case_name()

        if headless_camel_case_name == self.get_device().get_initial_name():
            headless_camel_case_name += '_'

        type_ = self.get_type()
        divisor = self.get_formatted_divisor('/{0}')

        # FIXME: Convert.ToString() doesn't support leading zeros. therefore,
        #        the result is not padded to the requested number of digits
        if ':bitmask:' in type_:
            to_string_prefix = 'Convert.ToString('
            to_string_suffix = ', 2)'
        elif type_ in ['char', 'string']:
            to_string_prefix = ''
            to_string_suffix = ''
        elif len(divisor) > 0:
            to_string_prefix = '('
            to_string_suffix = ').ToString()'
        else:
            to_string_prefix = ''
            to_string_suffix = '.ToString()'

        return template.format(headless_camel_case_name=headless_camel_case_name,
                               label_name=self.get_label_name(),
                               to_string_prefix=to_string_prefix,
                               to_string_suffix=to_string_suffix,
                               divisor=divisor,
                               unit_final_name=self.get_unit_formatted_final_name(' + " {0}"'))

class VBNETExampleGetterFunction(common.ExampleGetterFunction):
    def get_vbnet_imports(self):
        return []

    def get_vbnet_subroutine(self):
        return None

    def get_vbnet_source(self):
        templateA = r"""        ' Get current {function_comment_name}{comments}
{variable_declarations} = {device_initial_name}.{function_camel_case_name}({arguments})
{write_lines}
"""
        templateB = r"""        ' Get current {function_comment_name}{comments}
{variable_declarations}

        {device_initial_name}.{function_camel_case_name}({arguments})
{write_lines}
"""
        comments = []
        variable_declarations = []
        variable_references = []
        write_lines = []

        for result in self.get_results():
            comments.append(result.get_formatted_comment())
            variable_declarations.append(result.get_vbnet_variable_declaration())
            variable_references.append(result.get_vbnet_variable_reference())
            write_lines.append(result.get_vbnet_write_line())

        if len(comments) > 1 and len(set(comments)) == 1:
            comments = comments[:1]

        if len(variable_declarations) == 1:
            template = templateA
        else:
            template = templateB

        while None in write_lines:
            write_lines.remove(None)

        if len(write_lines) > 1:
            write_lines.insert(0, '')

        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_vbnet_source())

        if len(variable_references) > 1:
            arguments += variable_references

        result = template.format(device_initial_name=self.get_device().get_initial_name(),
                                 function_camel_case_name=self.get_camel_case_name(),
                                 function_headless_camel_case_name=self.get_headless_camel_case_name(),
                                 function_comment_name=self.get_comment_name(),
                                 comments=''.join(comments),
                                 variable_declarations='\n'.join(variable_declarations),
                                 write_lines='\n'.join(write_lines),
                                 arguments=',<BP>'.join(arguments))

        return common.break_string(result, '.{}('.format(self.get_camel_case_name()), continuation=' _')

class VBNETExampleSetterFunction(common.ExampleSetterFunction):
    def get_vbnet_imports(self):
        return []

    def get_vbnet_subroutine(self):
        return None

    def get_vbnet_source(self):
        template = '{comment1}{global_line_prefix}        {device_initial_name}.{function_camel_case_name}({arguments}){comment2}\n'
        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_vbnet_source())

        result = template.format(global_line_prefix=global_line_prefix,
                                 device_initial_name=self.get_device().get_initial_name(),
                                 function_camel_case_name=self.get_camel_case_name(),
                                 arguments=',<BP>'.join(arguments),
                                 comment1=self.get_formatted_comment1(global_line_prefix + "        ' {0}\n", '\r', "\n" + global_line_prefix + "        ' "),
                                 comment2=self.get_formatted_comment2(" ' {0}", ''))

        return common.break_string(result, '.{}('.format(self.get_camel_case_name()), continuation=' _')

class VBNETExampleCallbackFunction(common.ExampleCallbackFunction):
    def get_vbnet_imports(self):
        return []

    def get_vbnet_subroutine(self):
        template1A = r"""    ' Callback subroutine for {function_comment_name} callback{comments}
"""
        template1B = r"""{override_comment}
"""
        template2 = r"""    Sub {function_camel_case_name}CB(ByVal sender As {device_camel_case_category}{device_camel_case_name}{parameters})
{write_lines}{extra_message}
    End Sub
"""
        override_comment = self.get_formatted_override_comment("    ' {0}", None, "\n    ' ")

        if override_comment == None:
            template1 = template1A
        else:
            template1 = template1B

        comments = []
        parameters = []
        write_lines = []

        for parameter in self.get_parameters():
            comments.append(parameter.get_formatted_comment())
            parameters.append(parameter.get_vbnet_source())
            write_lines.append(parameter.get_vbnet_write_line())

        if len(comments) > 1 and len(set(comments)) == 1:
            comments = [comments[0].replace('parameter has', 'parameters have')]

        while None in write_lines:
            write_lines.remove(None)

        if len(write_lines) > 1:
            write_lines.append('        Console.WriteLine("")')

        extra_message = self.get_formatted_extra_message('        Console.WriteLine("{0}")')

        if len(extra_message) > 0 and len(write_lines) > 0:
            extra_message = '\n' + extra_message

        result = template1.format(function_comment_name=self.get_comment_name(),
                                  comments=''.join(comments),
                                  override_comment=override_comment) + \
                 template2.format(device_camel_case_category=self.get_device().get_camel_case_category(),
                                  device_camel_case_name=self.get_device().get_camel_case_name(),
                                  function_camel_case_name=self.get_camel_case_name(),
                                  parameters=common.wrap_non_empty(',<BP>', ',<BP>'.join(parameters), ''),
                                  write_lines='\n'.join(write_lines),
                                  extra_message=extra_message)

        return common.break_string(result, '{}CB('.format(self.get_camel_case_name()), continuation=' _')

    def get_vbnet_source(self):
        template1 = r"""        ' Register {function_comment_name} callback to<BP>subroutine {function_camel_case_name}CB
"""
        template2 = r"""        AddHandler {device_initial_name}.{function_camel_case_name}Callback,<BP>AddressOf {function_camel_case_name}CB
"""

        result1 = template1.format(function_camel_case_name=self.get_camel_case_name(),
                                   function_comment_name=self.get_comment_name())
        result2 = template2.format(device_initial_name=self.get_device().get_initial_name(),
                                   function_camel_case_name=self.get_camel_case_name())

        return common.break_string(result1, "' ", extra="' ") + \
               common.break_string(result2, 'AddHandler ', continuation=' _')

class VBNETExampleCallbackPeriodFunction(common.ExampleCallbackPeriodFunction):
    def get_vbnet_imports(self):
        return []

    def get_vbnet_subroutine(self):
        return None

    def get_vbnet_source(self):
        templateA = r"""        ' Set period for {function_comment_name} callback to {period_sec_short} ({period_msec}ms)
        {device_initial_name}.Set{function_camel_case_name}Period({arguments}{period_msec})
"""
        templateB = r"""        ' Set period for {function_comment_name} callback to {period_sec_short} ({period_msec}ms)
        ' Note: The {function_comment_name} callback is only called every {period_sec_long}
        '       if the {function_comment_name} has changed since the last call!
        {device_initial_name}.Set{function_camel_case_name}CallbackPeriod({arguments}{period_msec})
"""

        if self.get_device().get_underscore_name().startswith('imu'):
            template = templateA # FIXME: special hack for IMU Brick (2.0) callback behavior and name mismatch
        else:
            template = templateB

        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_vbnet_source())

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               function_camel_case_name=self.get_camel_case_name(),
                               function_comment_name=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(arguments), ', '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long)

class VBNETExampleCallbackThresholdMinimumMaximum(common.ExampleCallbackThresholdMinimumMaximum):
    def get_vbnet_source(self):
        template = '{minimum}, {maximum}'

        return template.format(minimum=self.get_formatted_minimum(),
                               maximum=self.get_formatted_maximum())

class VBNETExampleCallbackThresholdFunction(common.ExampleCallbackThresholdFunction):
    def get_vbnet_imports(self):
        return []

    def get_vbnet_subroutine(self):
        return None

    def get_vbnet_source(self):
        template = r"""        ' Configure threshold for {function_comment_name} "{option_comment}"{mininum_maximum_unit_comments}
        {device_initial_name}.Set{function_camel_case_name}CallbackThreshold({arguments}"{option_char}"C, {mininum_maximums})
"""
        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_vbnet_source())

        mininum_maximums = []
        mininum_maximum_unit_comments = []

        for mininum_maximum in self.get_minimum_maximums():
            mininum_maximums.append(mininum_maximum.get_vbnet_source())
            mininum_maximum_unit_comments.append(mininum_maximum.get_unit_comment())

        if len(mininum_maximum_unit_comments) > 1 and len(set(mininum_maximum_unit_comments)) == 1:
            mininum_maximum_unit_comments = mininum_maximum_unit_comments[:1]

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               function_camel_case_name=self.get_camel_case_name(),
                               function_comment_name=self.get_underscore_name(),
                               arguments=common.wrap_non_empty('', ', '.join(arguments), ', '),
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               mininum_maximums=', '.join(mininum_maximums),
                               mininum_maximum_unit_comments=''.join(mininum_maximum_unit_comments))

class VBNETExampleSpecialFunction(common.ExampleSpecialFunction):
    def get_vbnet_imports(self):
        if self.get_type() == 'sleep':
            return ['Imports System.Threading\n']
        else:
            return []

    def get_vbnet_subroutine(self):
        return None

    def get_vbnet_source(self):
        global global_line_prefix

        type_ = self.get_type()

        if type_ == 'empty':
            return ''
        elif type_ == 'debounce_period':
            template = r"""        ' Get threshold callbacks with a debounce time of {period_sec} ({period_msec}ms)
        {device_initial_name}.SetDebouncePeriod({period_msec})
"""
            period_msec, period_sec = self.get_formatted_debounce_period()

            return template.format(device_initial_name=self.get_device().get_initial_name(),
                                   period_msec=period_msec,
                                   period_sec=period_sec)
        elif type_ == 'sleep':
            template = '{comment1}{global_line_prefix}        Thread.Sleep({duration}){comment2}\n'

            return template.format(global_line_prefix=global_line_prefix,
                                   duration=self.get_sleep_duration(),
                                   comment1=self.get_formatted_sleep_comment1(global_line_prefix + "        ' {0}\n", '\r', "\n" + global_line_prefix + "        ' "),
                                   comment2=self.get_formatted_sleep_comment2(" ' {0}", ''))
        elif type_ == 'loop_header':
            template = '{comment}        Dim i As Integer\n        For i = 0 To {limit}\n'
            global_line_prefix = '    '

            return template.format(limit=self.get_loop_header_limit() - 1,
                                   comment=self.get_formatted_loop_header_comment("        ' {0}\n", '', "\n        ' "))
        elif type_ == 'loop_footer':
            global_line_prefix = ''

            return '\r        Next i\n'

class VBNETExamplesGenerator(common.ExamplesGenerator):
    def get_bindings_name(self):
        return 'vbnet'

    def get_constant_class(self):
        return VBNETConstant

    def get_example_class(self):
        return VBNETExample

    def get_example_argument_class(self):
        return VBNETExampleArgument

    def get_example_parameter_class(self):
        return VBNETExampleParameter

    def get_example_result_class(self):
        return VBNETExampleResult

    def get_example_getter_function_class(self):
        return VBNETExampleGetterFunction

    def get_example_setter_function_class(self):
        return VBNETExampleSetterFunction

    def get_example_callback_function_class(self):
        return VBNETExampleCallbackFunction

    def get_example_callback_period_function_class(self):
        return VBNETExampleCallbackPeriodFunction

    def get_example_callback_threshold_minimum_maximum_class(self):
        return VBNETExampleCallbackThresholdMinimumMaximum

    def get_example_callback_threshold_function_class(self):
        return VBNETExampleCallbackThresholdFunction

    def get_example_special_function_class(self):
        return VBNETExampleSpecialFunction

    def generate(self, device):
        if os.getenv('TINKERFORGE_GENERATE_EXAMPLES_FOR_DEVICE', device.get_camel_case_name()) != device.get_camel_case_name():
            print('  \033[01;31m- skipped\033[0m')
            return

        examples_directory = self.get_examples_directory(device)
        examples = device.get_examples()

        if len(examples) == 0:
            print('  \033[01;31m- no examples\033[0m')
            return

        if not os.path.exists(examples_directory):
            os.makedirs(examples_directory)

        for example in examples:
            filename = 'Example{0}.vb'.format(example.get_camel_case_name())
            filepath = os.path.join(examples_directory, filename)

            if example.is_incomplete():
                if os.path.exists(filepath) and self.skip_existing_incomplete_example:
                    print('  - ' + filename + ' \033[01;35m(incomplete, skipped)\033[0m')
                    continue
                else:
                    print('  - ' + filename + ' \033[01;31m(incomplete)\033[0m')
            else:
                print('  - ' + filename)

            with open(filepath, 'w') as f:
                f.write(example.get_vbnet_source())

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', VBNETExamplesGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
