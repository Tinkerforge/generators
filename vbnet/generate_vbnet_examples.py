#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Visual Basic .NET Examples Generator
Copyright (C) 2015-2018 Matthias Bolte <matthias@tinkerforge.com>

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
        template = '{device_category}{device_name}.{constant_group_name}_{constant_name}'

        return template.format(device_category=self.get_device().get_category().camel,
                               device_name=self.get_device().get_name().camel,
                               constant_group_name=self.get_constant_group().get_name().upper,
                               constant_name=self.get_name().upper)

class VBNETExample(common.Example):
    def get_vbnet_source(self):
        template = r"""Imports System
{imports}Imports Tinkerforge{incomplete}{description}

Module Example{example_name}
    Const HOST As String = "localhost"
    Const PORT As Integer = 4223
    Const UID As String = "{dummy_uid}" ' Change {dummy_uid} to the UID of your {device_name_long_display}
{subroutines}
    Sub Main()
        Dim ipcon As New IPConnection() ' Create IP connection
        Dim {device_name_initial} As New {device_category}{device_name_camel}(UID, ipcon) ' Create device object

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
                               example_name=self.get_name().camel,
                               device_category=self.get_device().get_category().camel,
                               device_name_camel=self.get_device().get_name().camel,
                               device_name_initial=self.get_device().get_initial_name(),
                               device_name_long_display=self.get_device().get_long_display_name(),
                               dummy_uid=self.get_dummy_uid(),
                               imports=''.join(unique_imports),
                               subroutines=common.wrap_non_empty('\n', '\n'.join(subroutines), ''),
                               sources='\n' + '\n'.join(sources).replace('\n\r', '').lstrip('\r'),
                               cleanups=common.wrap_non_empty('\n', '\n'.join(cleanups).replace('\n\r', '').lstrip('\r').rstrip('\n'), ''))

class VBNETExampleArgument(common.ExampleArgument):
    def get_vbnet_source(self):
        type_ = self.get_type()

        def helper(value):
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
                return self.get_value_constant(value).get_vbnet_source()
            else:
                return str(value)

        value = self.get_value()

        if isinstance(value, list):
            return 'new {0}(){{{1}}}'.format(get_vbnet_type(self.get_type().split(':')[0]), ', '.join([helper(item) for item in value]))

        return helper(value)

class VBNETExampleArgumentsMixin(object):
    def get_vbnet_arguments(self):
        return [argument.get_vbnet_source() for argument in self.get_arguments()]

class VBNETExampleParameter(common.ExampleParameter):
    def get_vbnet_source(self):
        templateA = 'ByVal {name} As {type_}'
        templateB = 'ByVal {name} As {type_}()'

        if self.get_cardinality() == 1:
            template = templateA
        else:
            template = templateB

        return template.format(type_=get_vbnet_type(self.get_type().split(':')[0]),
                               name=self.get_name().headless)

    def get_vbnet_write_lines(self):
        if self.get_type().split(':')[-1] == 'constant':
            # FIXME: need to handle multiple labels
            assert self.get_label_count() == 1

            template = '{global_line_prefix}        {else_}If {name} = {constant_name} Then\n{global_line_prefix}            Console.WriteLine("{label}: {constant_title}"){comment}'
            constant_group = self.get_constant_group()
            name = self.get_name().headless

            if name == self.get_device().get_initial_name():
                name += '_'

            result = []

            for constant in constant_group.get_constants():
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              else_='Else ' if len(result) > 0 else '',
                                              name=name,
                                              label=self.get_label_name(),
                                              constant_name=constant.get_vbnet_source(),
                                              constant_title=constant.get_name().space,
                                              comment=self.get_formatted_comment(" ' {0}")))

            result = ['\r' + '\n'.join(result) + '\n        End If\r']
        else:
            template = '{global_line_prefix}        Console.WriteLine("{label}: " + {to_string_prefix}{name}{index}{divisor}{to_string_suffix}{unit}){comment}'

            if self.get_label_name() == None:
                return []

            if self.get_cardinality() < 0:
                return [] # FIXME: streaming

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

            result = []

            for index in range(self.get_label_count()):
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              name=self.get_name().headless,
                                              label=self.get_label_name(index=index),
                                              index='({0})'.format(index) if self.get_label_count() > 1 else '',
                                              to_string_prefix=to_string_prefix,
                                              to_string_suffix=to_string_suffix,
                                              divisor=divisor,
                                              unit=self.get_formatted_unit_name(' + " {0}"'),
                                              comment=self.get_formatted_comment(" ' {0}")))

        return result

class VBNETExampleResult(common.ExampleResult):
    def get_vbnet_variable_declaration(self):
        template = '        Dim {name_headless} As {type_}'
        name = self.get_name().headless

        if name == self.get_device().get_initial_name():
            name += '_'

        type_ = get_vbnet_type(self.get_type().split(':')[0])

        if self.get_cardinality() > 1:
            type_ += '()'

        return type_, name

    def get_vbnet_variable_reference(self):
        name = self.get_name().headless

        if name == self.get_device().get_initial_name():
            name += '_'

        return name

    def get_vbnet_write_lines(self):
        if self.get_type().split(':')[-1] == 'constant':
            # FIXME: need to handle multiple labels
            assert self.get_label_count() == 1

            template = '{global_line_prefix}        {else_}If {name} = {constant_name} Then\n{global_line_prefix}            Console.WriteLine("{label}: {constant_title}"){comment}'
            constant_group = self.get_constant_group()
            name = self.get_name().headless

            if name == self.get_device().get_initial_name():
                name += '_'

            result = []

            for constant in constant_group.get_constants():
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              else_='Else ' if len(result) > 0 else '',
                                              name=name,
                                              label=self.get_label_name(),
                                              constant_name=constant.get_vbnet_source(),
                                              constant_title=constant.get_name().space,
                                              comment=self.get_formatted_comment(" ' {0}")))

            result = ['\r' + '\n'.join(result) + '\n        End If\r']
        else:
            template = '{global_line_prefix}        Console.WriteLine("{label}: " + {to_string_prefix}{name}{index}{divisor}{to_string_suffix}{unit}){comment}'

            if self.get_label_name() == None:
                return []

            if self.get_cardinality() < 0:
                return [] # FIXME: streaming

            name = self.get_name().headless

            if name == self.get_device().get_initial_name():
                name += '_'

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

            result = []

            for index in range(self.get_label_count()):
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              name=name,
                                              label=self.get_label_name(index=index),
                                              index='({0})'.format(index) if self.get_label_count() > 1 else '',
                                              to_string_prefix=to_string_prefix,
                                              to_string_suffix=to_string_suffix,
                                              divisor=divisor,
                                              unit=self.get_formatted_unit_name(' + " {0}"'),
                                              comment=self.get_formatted_comment(" ' {0}")))

        return result

class VBNETExampleGetterFunction(common.ExampleGetterFunction, VBNETExampleArgumentsMixin):
    def get_vbnet_imports(self):
        return []

    def get_vbnet_subroutine(self):
        return None

    def get_vbnet_source(self):
        templateA = r"""{global_line_prefix}        ' Get current {function_name_comment}
{global_line_prefix}{variable_declarations} = {device_name}.{function_name_camel}({arguments})
{write_lines}
"""
        templateB = r"""{global_line_prefix}        ' Get current {function_name_comment}
{global_line_prefix}{variable_declarations}

{global_line_prefix}        {device_name}.{function_name_camel}({arguments})
{write_lines}
"""
        variable_declarations = []
        variable_references = []
        write_lines = []

        for result in self.get_results():
            variable_declarations.append(result.get_vbnet_variable_declaration())
            variable_references.append(result.get_vbnet_variable_reference())
            write_lines += result.get_vbnet_write_lines()

        if len(variable_declarations) == 1:
            template = templateA
        else:
            template = templateB

        merged_variable_declarations = []

        for variable_declaration in variable_declarations:
            merged = False

            for merged_variable_declaration in merged_variable_declarations:
                if merged_variable_declaration[0] == variable_declaration[0]:
                    merged_variable_declaration[1].append(variable_declaration[1])
                    merged = True
                    break

            if not merged:
                merged_variable_declarations.append([variable_declaration[0], [variable_declaration[1]]])

        variable_declarations = []

        for merged_variable_declaration in merged_variable_declarations:
            variable_declarations.append(common.break_string('        Dim {0} As {1}'.format(',<BP>'.join(merged_variable_declaration[1]),
                                                                                             merged_variable_declaration[0]), 'Dim '))

        while None in write_lines:
            write_lines.remove(None)

        if len(write_lines) > 1:
            write_lines.insert(0, '\b')

        arguments = self.get_vbnet_arguments()

        if len(variable_references) > 1:
            arguments += variable_references

        result = template.format(global_line_prefix=global_line_prefix,
                                 device_name=self.get_device().get_initial_name(),
                                 function_name_camel=self.get_name().camel,
                                 function_name_headless=self.get_name().headless,
                                 function_name_comment=self.get_comment_name(),
                                 variable_declarations='\n'.join(variable_declarations),
                                 write_lines='\n'.join(write_lines).replace('\b\n\r', '\n').replace('\b', '').replace('\r\n\r', '\n\n').rstrip('\r').replace('\r', '\n'),
                                 arguments=',<BP>'.join(arguments))

        return common.break_string(result, '.{}('.format(self.get_name().camel), continuation=' _')

class VBNETExampleSetterFunction(common.ExampleSetterFunction, VBNETExampleArgumentsMixin):
    def get_vbnet_imports(self):
        return []

    def get_vbnet_subroutine(self):
        return None

    def get_vbnet_source(self):
        template = '{comment1}{global_line_prefix}        {device_name}.{function_name}({arguments}){comment2}\n'

        result = template.format(global_line_prefix=global_line_prefix,
                                 device_name=self.get_device().get_initial_name(),
                                 function_name=self.get_name().camel,
                                 arguments=',<BP>'.join(self.get_vbnet_arguments()),
                                 comment1=self.get_formatted_comment1(global_line_prefix + "        ' {0}\n", '\r', "\n" + global_line_prefix + "        ' "),
                                 comment2=self.get_formatted_comment2(" ' {0}", ''))

        return common.break_string(result, '.{}('.format(self.get_name().camel), continuation=' _')

class VBNETExampleCallbackFunction(common.ExampleCallbackFunction):
    def get_vbnet_imports(self):
        return []

    def get_vbnet_subroutine(self):
        template1A = r"""    ' Callback subroutine for {function_name_comment} callback
"""
        template1B = r"""{override_comment}
"""
        template2 = r"""    Sub {function_name_camel}CB(ByVal sender As {device_category}{device_name}{parameters})
{write_lines}{extra_message}
    End Sub
"""
        override_comment = self.get_formatted_override_comment("    ' {0}", None, "\n    ' ")

        if override_comment == None:
            template1 = template1A
        else:
            template1 = template1B

        parameters = []
        write_lines = []

        for parameter in self.get_parameters():
            parameters.append(parameter.get_vbnet_source())
            write_lines += parameter.get_vbnet_write_lines()

        while None in write_lines:
            write_lines.remove(None)

        if len(write_lines) > 1:
            write_lines.append('        Console.WriteLine("")')

        extra_message = self.get_formatted_extra_message('        Console.WriteLine("{0}")')

        if len(extra_message) > 0 and len(write_lines) > 0:
            extra_message = '\n' + extra_message

        result = template1.format(function_name_comment=self.get_comment_name(),
                                  override_comment=override_comment) + \
                 template2.format(device_category=self.get_device().get_category().camel,
                                  device_name=self.get_device().get_name().camel,
                                  function_name_camel=self.get_name().camel,
                                  parameters=common.wrap_non_empty(',<BP>', ',<BP>'.join(parameters), ''),
                                  write_lines='\n'.join(write_lines).replace('\r\n\r', '\n\n').strip('\r').replace('\r', '\n'),
                                  extra_message=extra_message)

        return common.break_string(result, '{}CB('.format(self.get_name().camel), continuation=' _')

    def get_vbnet_source(self):
        template1 = r"""        ' Register {function_name_comment}<BP>callback<BP>to<BP>subroutine<BP>{function_name_camel}CB
"""
        template2 = r"""        AddHandler {device_name}.{function_name_camel}Callback,<BP>AddressOf {function_name_camel}CB
"""

        result1 = template1.format(function_name_camel=self.get_name().camel,
                                   function_name_comment=self.get_comment_name())
        result2 = template2.format(device_name=self.get_device().get_initial_name(),
                                   function_name_camel=self.get_name().camel)

        return common.break_string(result1, "' ", indent_tail="' ") + \
               common.break_string(result2, 'AddHandler ', continuation=' _')

class VBNETExampleCallbackPeriodFunction(common.ExampleCallbackPeriodFunction, VBNETExampleArgumentsMixin):
    def get_vbnet_imports(self):
        return []

    def get_vbnet_subroutine(self):
        return None

    def get_vbnet_source(self):
        templateA = r"""        ' Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms)
        {device_name}.Set{function_name_camel}Period({arguments}{period_msec})
"""
        templateB = r"""        ' Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms)
        ' Note: The {function_name_comment} callback is only called every {period_sec_long}
        '       if the {function_name_comment} has changed since the last call!
        {device_name}.Set{function_name_camel}CallbackPeriod({arguments}{period_msec})
"""

        if self.get_device().get_name().space.startswith('IMU'):
            template = templateA # FIXME: special hack for IMU Brick (2.0) callback behavior and name mismatch
        else:
            template = templateB

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        return template.format(device_name=self.get_device().get_initial_name(),
                               function_name_camel=self.get_name().camel,
                               function_name_comment=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_vbnet_arguments()), ', '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long)

class VBNETExampleCallbackThresholdMinimumMaximum(common.ExampleCallbackThresholdMinimumMaximum):
    def get_vbnet_source(self):
        template = '{minimum}, {maximum}'

        return template.format(minimum=self.get_formatted_minimum(),
                               maximum=self.get_formatted_maximum())

class VBNETExampleCallbackThresholdFunction(common.ExampleCallbackThresholdFunction, VBNETExampleArgumentsMixin):
    def get_vbnet_imports(self):
        return []

    def get_vbnet_subroutine(self):
        return None

    def get_vbnet_source(self):
        template = r"""        ' Configure threshold for {function_name_comment} "{option_comment}"
        {device_name}.Set{function_name_camel}CallbackThreshold({arguments}"{option_char}"C, {mininum_maximums})
"""
        mininum_maximums = []

        for mininum_maximum in self.get_minimum_maximums():
            mininum_maximums.append(mininum_maximum.get_vbnet_source())

        return template.format(device_name=self.get_device().get_initial_name(),
                               function_name_camel=self.get_name().camel,
                               function_name_comment=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_vbnet_arguments()), ', '),
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               mininum_maximums=', '.join(mininum_maximums))

class VBNETExampleCallbackConfigurationFunction(common.ExampleCallbackConfigurationFunction, VBNETExampleArgumentsMixin):
    def get_vbnet_imports(self):
        return []

    def get_vbnet_subroutine(self):
        return None

    def get_vbnet_source(self):
        templateA = r"""        ' Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms)
        {device_name}.Set{function_name_camel}CallbackConfiguration({arguments}{period_msec}{value_has_to_change})
"""
        templateB = r"""        ' Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms) without a threshold
        {device_name}.Set{function_name_camel}CallbackConfiguration({arguments}{period_msec}{value_has_to_change}, "{option_char}"C, {mininum_maximums})
"""
        templateC = r"""        ' Configure threshold for {function_name_comment} "{option_comment}"
        ' with a debounce period of {period_sec_short} ({period_msec}ms)
        {device_name}.Set{function_name_camel}CallbackConfiguration({arguments}{period_msec}{value_has_to_change}, "{option_char}"C, {mininum_maximums})
"""

        if self.get_option_char() == None:
            template = templateA
        elif self.get_option_char() == 'x':
            template = templateB
        else:
            template = templateC

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        mininum_maximums = []

        for mininum_maximum in self.get_minimum_maximums():
            mininum_maximums.append(mininum_maximum.get_vbnet_source())

        return template.format(device_name=self.get_device().get_initial_name(),
                               function_name_camel=self.get_name().camel,
                               function_name_comment=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_vbnet_arguments()), ', '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long,
                               value_has_to_change=common.wrap_non_empty(', ', self.get_value_has_to_change('True', 'False', ''), ''),
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               mininum_maximums=', '.join(mininum_maximums))

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
        {device_name_initial}.SetDebouncePeriod({period_msec})
"""
            period_msec, period_sec = self.get_formatted_debounce_period()

            return template.format(device_name_initial=self.get_device().get_initial_name(),
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

    def get_example_callback_configuration_function_class(self):
        return VBNETExampleCallbackConfigurationFunction

    def get_example_special_function_class(self):
        return VBNETExampleSpecialFunction

    def generate(self, device):
        if os.getenv('TINKERFORGE_GENERATE_EXAMPLES_FOR_DEVICE', device.get_name().camel) != device.get_name().camel:
            print('  \033[01;31m- skipped\033[0m')
            return

        examples_dir = self.get_examples_dir(device)
        examples = device.get_examples()

        if len(examples) == 0:
            print('  \033[01;31m- no examples\033[0m')
            return

        if not os.path.exists(examples_dir):
            os.makedirs(examples_dir)

        for example in examples:
            filename = 'Example{0}.vb'.format(example.get_name().camel)
            filepath = os.path.join(examples_dir, filename)

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

def generate(root_dir):
    common.generate(root_dir, 'en', VBNETExamplesGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
