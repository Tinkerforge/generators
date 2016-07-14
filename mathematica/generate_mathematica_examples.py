#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Mathematica Examples Generator
Copyright (C) 2015-2016 Matthias Bolte <matthias@tinkerforge.com>

generate_mathematica_examples.py: Generator for Mathematica examples

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
import re

sys.path.append(os.path.split(os.getcwd())[0])
import common

global_line_prefix = ''
global_line_suffix = ''

class MathematicaConstant(common.Constant):
    def get_mathematica_source(self):
        template = '{device_camel_case_category}{device_camel_case_name}`{constant_group_upper_case_name}U{constant_upper_case_name}'

        return template.format(device_camel_case_category=self.get_device().get_camel_case_category(),
                               device_camel_case_name=self.get_device().get_camel_case_name(),
                               constant_group_upper_case_name=self.get_constant_group().get_upper_case_name().replace('_', 'U'),
                               constant_upper_case_name=self.get_upper_case_name().replace('_', 'U'))

class MathematicaExample(common.Example):
    def get_mathematica_source(self):
        template = r"""Needs["NETLink`"]
LoadNETAssembly["Tinkerforge",NotebookDirectory[]<>"../../.."]{incomplete}

host="localhost"
port=4223
uid="{dummy_uid}"(*Change {dummy_uid} to the UID of your {device_long_display_name}*)

(*Create IPConnection and device object*)
ipcon=NETNew["Tinkerforge.IPConnection"]
{device_initial_name}=NETNew["Tinkerforge.{device_camel_case_category}{device_camel_case_name}",uid,ipcon]
ipcon@Connect[host,port]
{sources}
(*Clean up*){cleanups}
ipcon@Disconnect[]
ReleaseNETObject[{device_initial_name}]
ReleaseNETObject[ipcon]
"""

        if self.is_incomplete():
            incomplete = '\n\n(*FIXME: This example is incomplete*)'
        else:
            incomplete = ''

        sources = []
        add_input_call = False

        for function in self.get_functions():
            if isinstance(function, MathematicaExampleCallbackFunction):
                add_input_call = True
            elif isinstance(function, MathematicaExampleSpecialFunction) and function.get_type() == 'wait':
                add_input_call = True

            sources.append(function.get_mathematica_source())

        while None in sources:
            sources.remove(None)

        if len(sources) == 0:
            sources = ['(*TODO: Add example code here*)\n']
        elif add_input_call:
            sources.append('Input["Click OK to exit"]\n')

        cleanups = []

        for cleanup in self.get_cleanups():
            cleanups.append(cleanup.get_mathematica_source())

        while None in cleanups:
            cleanups.remove(None)

        return template.format(incomplete=incomplete,
                               device_camel_case_category=self.get_device().get_camel_case_category(),
                               device_camel_case_name=self.get_device().get_camel_case_name(),
                               device_initial_name=self.get_device().get_initial_name(),
                               device_long_display_name=self.get_device().get_long_display_name(),
                               dummy_uid=self.get_dummy_uid(),
                               sources='\n' + '\n'.join(sources).replace(';\n\n\b', '\n\n').replace('\n\r', '').lstrip('\r'),
                               cleanups=common.wrap_non_empty('\n', '\n'.join(cleanups).replace('\n\r', '').lstrip('\r').rstrip('\n'), ''))

class MathematicaExampleArgument(common.ExampleArgument):
    def get_mathematica_source(self):
        type = self.get_type()
        value = self.get_value()

        if type == 'bool':
            if value:
                return 'True'
            else:
                return 'False'
        elif type == 'char':
            return 'ToCharacterCode["{0}"][[1]]'.format(value)
        elif type == 'string':
            return '"{0}"'.format(value)
        elif ':bitmask:' in type:
            bits = []

            for i in range(64):
                if (value & (1 << i)) != 0:
                    bits = ['1'] + bits
                else:
                    bits = ['0'] + bits

            length = int(type.split(':')[2])

            return 'FromDigits[{{{0}}},2]'.format(','.join(bits[-length:]))
        elif type.endswith(':constant'):
            return self.get_value_constant().get_mathematica_source()
        else:
            return str(value)

class MathematicaExampleParameter(common.ExampleParameter):
    def get_mathematica_source(self):
        template = '{headless_camel_case_name}_'

        return template.format(headless_camel_case_name=self.get_headless_camel_case_name())

    def get_mathematica_print(self):
        templateA = ' Print["{label_name}: "<>ToString[N[Quantity[{headless_camel_case_name},"{quantity_name}"]]]]'
        templateB = ' Print["{label_name}: "<>ToString[N[{headless_camel_case_name}/{divisor}]]]'
        templateC = ' Print["{label_name}: "<>FromCharacterCode[{headless_camel_case_name}]]'
        templateD = ' Print["{label_name}: "<>StringJoin[Map[ToString,IntegerDigits[{headless_camel_case_name},2,{bitmask_length}]]]]'
        templateE = ' Print["{label_name}: "<>ToString[{headless_camel_case_name}]]'

        if self.get_label_name() == None:
            return None

        type = self.get_type()
        quantity_name = self.get_unit_formatted_final_name('{0}' + self.get_formatted_divisor('/{0}', cast=int))
        divisor = self.get_formatted_divisor('{0}')
        bitmask_length = 0

        if len(quantity_name) > 0:
            template = templateA
        elif len(divisor) > 0:
            template = templateB
        elif type == 'char':
            template = templateC
        elif ':bitmask:' in type:
            template = templateD
            bitmask_length = int(type.split(':')[2])
        else:
            template = templateE

        return template.format(headless_camel_case_name=self.get_headless_camel_case_name(),
                               label_name=self.get_label_name(),
                               quantity_name=quantity_name,
                               divisor=divisor,
                               bitmask_length=bitmask_length)

class MathematicaExampleResult(common.ExampleResult):
    def get_mathematica_variable_name(self):
        headless_camel_case_name = self.get_headless_camel_case_name()

        if headless_camel_case_name == self.get_device().get_initial_name():
            headless_camel_case_name += 'U'

        return headless_camel_case_name

    def get_mathematica_print(self, getter_call=None):
        templateA = 'Print["{label_name}: "<>ToString[N[Quantity[{value},"{quantity_name}"]]]]'
        templateB = 'Print["{label_name}: "<>ToString[N[{value}/{divisor}]]]'
        templateC = 'Print["{label_name}: "<>FromCharacterCode[{value}]]'
        templateD = 'Print["{label_name}: "<>StringJoin[Map[ToString,IntegerDigits[{value},2,{bitmask_length}]]]]'
        templateE = 'Print["{label_name}: "<>ToString[{value}]]'

        if self.get_label_name() == None:
            return None

        if getter_call != None:
            value = getter_call
        else:
            headless_camel_case_name = self.get_headless_camel_case_name()

            if headless_camel_case_name == self.get_device().get_initial_name():
                headless_camel_case_name += 'U'

            value = headless_camel_case_name

        type = self.get_type()
        quantity_name = self.get_unit_formatted_final_name('{0}' + self.get_formatted_divisor('/{0}', cast=int))
        divisor = self.get_formatted_divisor('{0}')
        bitmask_length = 0

        if len(quantity_name) > 0:
            template = templateA
        elif len(divisor) > 0:
            template = templateB
        elif type == 'char':
            template = templateC
        elif ':bitmask:' in type:
            template = templateD
            bitmask_length = int(type.split(':')[2])
        else:
            template = templateE

        return template.format(value=value,
                               label_name=self.get_label_name(),
                               quantity_name=quantity_name,
                               divisor=divisor,
                               bitmask_length=bitmask_length)

class MathematicaExampleGetterFunction(common.ExampleGetterFunction):
    def get_mathematica_source(self):
        template = '{device_initial_name}@{function_camel_case_name}[{arguments}]'
        templateA = r"""(*Get current {function_comment_name}{comments}*)
{prints}
"""
        templateB = r"""{variable_declarations}

(*Get current {function_comment_name}{comments}*)
{device_initial_name}@{function_camel_case_name}[{arguments}]
{prints}
"""
        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_mathematica_source())

        if len(self.get_results()) == 1:
            getter_call = template.format(device_initial_name=self.get_device().get_initial_name(),
                                          function_camel_case_name=self.get_camel_case_name(),
                                          arguments=','.join(arguments))
        else:
            getter_call = None

        comments = []
        variable_names = []
        prints = []

        for result in self.get_results():
            comments.append(result.get_formatted_comment())
            variable_names.append(result.get_mathematica_variable_name())
            prints.append(result.get_mathematica_print(getter_call))

        if len(comments) > 1 and len(set(comments)) == 1:
            comments = comments[:1]

        if len(variable_names) == 1:
            template = templateA
            variable_declarations = []
        else:
            template = templateB
            variable_declarations = ['{0}=0'.format(variable_name) for variable_name in variable_names]

        while None in prints:
            prints.remove(None)

        if len(prints) > 1:
            prints.insert(0, '')

        if len(variable_names) > 1:
            arguments += variable_names

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               function_camel_case_name=self.get_camel_case_name(),
                               function_headless_camel_case_name=self.get_headless_camel_case_name(),
                               function_comment_name=self.get_comment_name(),
                               comments=''.join(comments),
                               variable_names=''.join(variable_names),
                               variable_declarations=';'.join(variable_declarations),
                               prints='\n'.join(prints),
                               arguments=','.join(arguments))

class MathematicaExampleSetterFunction(common.ExampleSetterFunction):
    def get_mathematica_source(self):
        template = '{comment1}{global_line_prefix}{device_initial_name}@{function_camel_case_name}[{arguments}]{global_line_suffix}{comment2}\n'
        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_mathematica_source())

        return template.format(global_line_prefix=global_line_prefix,
                               global_line_suffix=global_line_suffix,
                               device_initial_name=self.get_device().get_initial_name(),
                               function_camel_case_name=self.get_camel_case_name(),
                               arguments=','.join(arguments),
                               comment1=re.sub('\\(\\*[ ]*\\*\\)\n', '', self.get_formatted_comment1(global_line_prefix + '(*{0}*)\n', '\r', '*)\n' + global_line_prefix + '(*')),
                               comment2=self.get_formatted_comment2('(*{0}*)', ''))

class MathematicaExampleCallbackFunction(common.ExampleCallbackFunction):
    def get_mathematica_source(self):
        template1A = r"""(*Callback function for {function_comment_name} callback{comments}*)
"""
        template1B = r"""{override_comment}
"""
        template2A = r"""{function_camel_case_name}CB[sender_{parameters}]:=
 Module[{{}},
{prints}{extra_message}
 ]

AddEventHandler[{device_initial_name}@{function_camel_case_name},{function_camel_case_name}CB]
"""
        template2B = r"""{function_camel_case_name}CB[sender_{parameters}]:=
{prints}{extra_message}
AddEventHandler[{device_initial_name}@{function_camel_case_name},{function_camel_case_name}CB]
"""
        override_comment = self.get_formatted_override_comment('(*{0}*)', None, '*)\n(*')

        if override_comment == None:
            template1 = template1A
        else:
            template1 = template1B
            override_comment = re.sub('\\(\\*[ ]+\\*\\)\n', '', override_comment)

        comments = []
        parameters = []
        prints = []

        for parameter in self.get_parameters():
            comments.append(parameter.get_formatted_comment())
            parameters.append(parameter.get_mathematica_source())
            prints.append(parameter.get_mathematica_print())

        if len(comments) > 1 and len(set(comments)) == 1:
            comments = [comments[0].replace('parameter has', 'parameters have')]

        while None in prints:
            prints.remove(None)

        extra_message = self.get_formatted_extra_message(' Print["{0}"]')

        if len(prints) > 1 or (len(prints) == 1 and len(extra_message) > 0):
            template2 = template2A
            prints = [' ' + prints for prints in prints]

            if len(extra_message) > 0:
                extra_message = ' ' + extra_message
        else:
            template2 = template2B

        if len(extra_message) > 0 and len(prints) > 0:
            extra_message = ';\n' + extra_message

        return template1.format(function_comment_name=self.get_comment_name(),
                                comments=''.join(comments),
                                override_comment=override_comment) + \
               template2.format(device_initial_name=self.get_device().get_initial_name(),
                                function_camel_case_name=self.get_camel_case_name(),
                                parameters=common.wrap_non_empty(',', ','.join(parameters), ''),
                                prints='\n'.join(prints).replace('\n', ';\n'),
                                extra_message=extra_message)

class MathematicaExampleCallbackPeriodFunction(common.ExampleCallbackPeriodFunction):
    def get_mathematica_source(self):
        template = r"""(*Set period for {function_comment_name} callback to {period_sec_short} ({period_msec}ms)*)
(*Note: The {function_comment_name} callback is only called every {period_sec_long}*)
(*if the {function_comment_name} has changed since the last call!*)
{device_initial_name}@Set{function_camel_case_name}{suffix}Period[{arguments}{period_msec}]
"""

        if self.get_device().get_underscore_name().startswith('imu'):
            suffix = '' # FIXME: special hack for IMU Brick name mismatch
        else:
            suffix = 'Callback'

        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_mathematica_source())

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               function_camel_case_name=self.get_camel_case_name(),
                               function_comment_name=self.get_comment_name(),
                               suffix=suffix,
                               arguments=common.wrap_non_empty('', ','.join(arguments), ','),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long)

class MathematicaExampleCallbackThresholdMinimumMaximum(common.ExampleCallbackThresholdMinimumMaximum):
    def get_mathematica_source(self):
        template = '{minimum},{maximum}'

        return template.format(minimum=self.get_formatted_minimum(),
                               maximum=self.get_formatted_maximum())

class MathematicaExampleCallbackThresholdFunction(common.ExampleCallbackThresholdFunction):
    def get_mathematica_source(self):
        template = r"""(*Configure threshold for {function_comment_name} "{option_comment}"{mininum_maximum_unit_comments}*)
option=Tinkerforge`{device_camel_case_category}{device_camel_case_name}`THRESHOLDUOPTIONU{option_upper_case_name}
{device_initial_name}@Set{function_camel_case_name}CallbackThreshold[{arguments}option,{mininum_maximums}]
"""
        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_mathematica_source())

        mininum_maximums = []
        mininum_maximum_unit_comments = []

        for mininum_maximum in self.get_minimum_maximums():
            mininum_maximums.append(mininum_maximum.get_mathematica_source())
            mininum_maximum_unit_comments.append(mininum_maximum.get_unit_comment())

        if len(mininum_maximum_unit_comments) > 1 and len(set(mininum_maximum_unit_comments)) == 1:
            mininum_maximum_unit_comments = mininum_maximum_unit_comments[:1]

        option_upper_case_names = {'o' : 'OUTSIDE', '<': 'SMALLER', '>': 'GREATER'}

        return template.format(device_camel_case_category=self.get_device().get_camel_case_category(),
                               device_camel_case_name=self.get_device().get_camel_case_name(),
                               device_initial_name=self.get_device().get_initial_name(),
                               function_camel_case_name=self.get_camel_case_name(),
                               function_underscore_name=self.get_underscore_name(),
                               function_comment_name=self.get_comment_name(),
                               option_upper_case_name=option_upper_case_names[self.get_option_char()],
                               option_comment=self.get_option_comment(),
                               arguments=common.wrap_non_empty('', ','.join(arguments), ','),
                               mininum_maximums=','.join(mininum_maximums),
                               mininum_maximum_unit_comments=''.join(mininum_maximum_unit_comments))

class MathematicaExampleSpecialFunction(common.ExampleSpecialFunction):
    def get_mathematica_source(self):
        global global_line_prefix
        global global_line_suffix

        type = self.get_type()

        if type == 'empty':
            return ''
        elif type == 'debounce_period':
            template = r"""(*Get threshold callbacks with a debounce time of {period_sec} ({period_msec}ms)*)
{device_initial_name}@SetDebouncePeriod[{period_msec}]
"""
            period_msec, period_sec = self.get_formatted_debounce_period()

            return template.format(device_initial_name=self.get_device().get_initial_name(),
                                   period_msec=period_msec,
                                   period_sec=period_sec)
        elif type == 'sleep':
            template = '{comment1}{global_line_prefix}Pause[{duration}]{global_line_suffix}{comment2}\n'
            duration = self.get_sleep_duration()

            if duration % 1000 == 0:
                duration //= 1000
            else:
                duration /= 1000.0

            return template.format(global_line_prefix=global_line_prefix,
                                   global_line_suffix=global_line_suffix,
                                   duration=duration,
                                   comment1=re.sub('\\(\\*[ ]*\\*\\)\n', '', self.get_formatted_sleep_comment1('(*{0}*)\n', '\r', '*)\n' + global_line_prefix + '(*')),
                                   comment2=self.get_formatted_sleep_comment2('(*{0}*)', ''))
        elif type == 'wait':
            return None
        elif type == 'loop_header':
            template = '{comment}For[i=0,i<{limit},i++,\n'
            global_line_prefix = ' '
            global_line_suffix = ';'

            return template.format(limit=self.get_loop_header_limit(),
                                   comment=re.sub('\\(\\*[ ]*\\*\\)\n', '', self.get_formatted_loop_header_comment('(*{0}*)\n', '', '*)\n' + global_line_prefix + '(*')))
        elif type == 'loop_footer':
            global_line_prefix = ''
            global_line_suffix = ''

            return '\b\r]\n'

class MathematicaExamplesGenerator(common.ExamplesGenerator):
    def get_bindings_name(self):
        return 'mathematica'

    def get_constant_class(self):
        return MathematicaConstant

    def get_example_class(self):
        return MathematicaExample

    def get_example_argument_class(self):
        return MathematicaExampleArgument

    def get_example_parameter_class(self):
        return MathematicaExampleParameter

    def get_example_result_class(self):
        return MathematicaExampleResult

    def get_example_getter_function_class(self):
        return MathematicaExampleGetterFunction

    def get_example_setter_function_class(self):
        return MathematicaExampleSetterFunction

    def get_example_callback_function_class(self):
        return MathematicaExampleCallbackFunction

    def get_example_callback_period_function_class(self):
        return MathematicaExampleCallbackPeriodFunction

    def get_example_callback_threshold_minimum_maximum_class(self):
        return MathematicaExampleCallbackThresholdMinimumMaximum

    def get_example_callback_threshold_function_class(self):
        return MathematicaExampleCallbackThresholdFunction

    def get_example_special_function_class(self):
        return MathematicaExampleSpecialFunction

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
            filename = 'Example{0}.nb.txt'.format(example.get_camel_case_name())
            filepath = os.path.join(examples_directory, filename)

            if device.get_git_name() + '/' + example.get_dash_name() in blacklist:
                print('  - ' + filename + ' \033[01;35m(blacklisted, skipped)\033[0m')
                continue

            if example.is_incomplete():
                if os.path.exists(filepath) and self.skip_existing_incomplete_example:
                    print('  - ' + filename + ' \033[01;35m(incomplete, skipped)\033[0m')
                    continue
                else:
                    print('  - ' + filename + ' \033[01;31m(incomplete)\033[0m')
            else:
                print('  - ' + filename)

            txt = open(filepath, 'wb')
            txt.write(example.get_mathematica_source())
            txt.close()

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', MathematicaExamplesGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
