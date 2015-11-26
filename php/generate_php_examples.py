#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PHP Examples Generator
Copyright (C) 2015 Matthias Bolte <matthias@tinkerforge.com>

generate_php_examples.py: Generator for PHP examples

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

class PHPConstant(common.Constant):
    def get_php_source(self):
        template = '{device_camel_case_category}{device_camel_case_name}::{constant_group_upper_case_name}_{constant_upper_case_name}'

        return template.format(device_camel_case_category=self.get_device().get_camel_case_category(),
                               device_camel_case_name=self.get_device().get_camel_case_name(),
                               constant_group_upper_case_name=self.get_constant_group().get_upper_case_name(),
                               constant_upper_case_name=self.get_upper_case_name())

class PHPExample(common.Example):
    def get_php_source(self):
        template = r"""<?php{incomplete}

require_once('Tinkerforge/IPConnection.php');
require_once('Tinkerforge/{device_camel_case_category}{device_camel_case_name}.php');

use Tinkerforge\IPConnection;
use Tinkerforge\{device_camel_case_category}{device_camel_case_name};

const HOST = 'localhost';
const PORT = 4223;
const UID = '{dummy_uid}'; // Change to your UID
{subroutines}
$ipcon = new IPConnection(); // Create IP connection
${device_initial_name} = new {device_camel_case_category}{device_camel_case_name}(UID, $ipcon); // Create device object

$ipcon->connect(HOST, PORT); // Connect to brickd
// Don't use device before ipcon is connected
{sources}
{footer}
?>
"""
        wait = r"""echo "Press key to exit\n";
fgetc(fopen('php://stdin', 'r'));{cleanups}
$ipcon->disconnect();
"""
        dispatch = r"""echo "Press ctrl+c to exit\n";
$ipcon->dispatchCallbacks(-1); // Dispatch callbacks forever
"""

        if self.is_incomplete():
            incomplete = '\n\n// FIXME: This example is incomplete'
        else:
            incomplete = ''

        subroutines = []
        sources = []
        cleanups = []
        footer = wait

        for function in self.get_functions():
            if isinstance(function, PHPExampleCallbackFunction):
                footer = dispatch

            subroutines.append(function.get_php_subroutine())
            sources.append(function.get_php_source())

        for cleanup in self.get_cleanups():
            subroutines.append(cleanup.get_php_subroutine())
            cleanups.append(cleanup.get_php_source())

        while None in subroutines:
            subroutines.remove(None)

        while None in sources:
            sources.remove(None)

        if len(sources) == 0:
            sources = ['// TODO: Add example code here\n']

        while None in cleanups:
            cleanups.remove(None)

        return template.format(incomplete=incomplete,
                               device_camel_case_category=self.get_device().get_camel_case_category(),
                               device_camel_case_name=self.get_device().get_camel_case_name(),
                               device_initial_name=self.get_device().get_initial_name(),
                               dummy_uid=self.get_dummy_uid(),
                               subroutines=common.wrap_non_empty('\n', '\n'.join(subroutines), ''),
                               sources='\n' + '\n'.join(sources).replace('\n\r', '').lstrip('\r'),
                               footer=footer.format(cleanups=common.wrap_non_empty('\n', '\n'.join(cleanups).replace('\n\r', '').lstrip('\r').rstrip('\n'), '')))

class PHPExampleArgument(common.ExampleArgument):
    def get_php_source(self):
        type = self.get_type()
        value = self.get_value()

        if type == 'bool':
            if value:
                return 'TRUE'
            else:
                return 'FALSE'
        elif type in ['char', 'string']:
            return "'{0}'".format(value)
        elif ':bitmask:' in type:
            return common.make_c_like_bitmask(value)
        elif type.endswith(':constant'):
            return self.get_value_constant().get_php_source()
        else:
            return str(value)

class PHPExampleParameter(common.ExampleParameter):
    def get_php_source(self):
        template = '${underscore_name}'

        return template.format(underscore_name=self.get_underscore_name())

    def get_php_echo(self):
        templateA = '    echo "{label_name}: " . {sprintf_prefix}${underscore_name}{divisor}{sprintf_suffix} . "{unit_final_name}\\n";'
        templateB = '    echo "{label_name}: ${underscore_name}{unit_final_name}\\n";'

        if self.get_label_name() == None:
            return None

        type = self.get_type()
        divisor = self.get_formatted_divisor('/{0}')
        sprintf_prefix = ''
        sprintf_suffix = ''

        if ':bitmask:' in type:
            template = templateA
            sprintf_prefix = 'sprintf("%0{0}b", '.format(int(type.split(':')[2]))
            sprintf_suffix = ')'
        elif len(divisor) > 0:
            template = templateA
        else:
            template = templateB

        return template.format(underscore_name=self.get_underscore_name(),
                               label_name=self.get_label_name(),
                               divisor=divisor,
                               unit_final_name=self.get_unit_formatted_final_name(' {0}'),
                               sprintf_prefix=sprintf_prefix,
                               sprintf_suffix=sprintf_suffix)

class PHPExampleResult(common.ExampleResult):
    def get_php_variable(self):
        template = '${underscore_name}'
        underscore_name = self.get_underscore_name()

        if underscore_name == self.get_device().get_initial_name():
            underscore_name += '_'

        return template.format(underscore_name=underscore_name)

    def get_php_echo(self):
        templateA = 'echo "{label_name}: " . {sprintf_prefix}${underscore_name}{divisor}{sprintf_suffix} . "{unit_final_name}\\n";'
        templateB = 'echo "{label_name}: ${underscore_name}{unit_final_name}\\n";'

        if self.get_label_name() == None:
            return None

        underscore_name = self.get_underscore_name()
        divisor = self.get_formatted_divisor('/{0}')

        if len(self.get_function().get_results()) > 1:
            underscore_name = "{0}['{1}']".format(self.get_function().get_underscore_name(skip=1), self.get_underscore_name())
            template = templateA
        else:
            if underscore_name == self.get_device().get_initial_name():
                underscore_name += '_'

            if len(divisor) > 0:
                template = templateA
            else:
                template = templateB

        type = self.get_type()

        if ':bitmask:' in type:
            template = templateA
            sprintf_prefix = 'sprintf("%0{0}b", '.format(int(type.split(':')[2]))
            sprintf_suffix = ')'
        else:
            sprintf_prefix = ''
            sprintf_suffix = ''

        return template.format(underscore_name=underscore_name,
                               label_name=self.get_label_name(),
                               divisor=divisor,
                               unit_final_name=self.get_unit_formatted_final_name(' {0}'),
                               sprintf_prefix=sprintf_prefix,
                               sprintf_suffix=sprintf_suffix)

class PHPExampleGetterFunction(common.ExampleGetterFunction):
    def get_php_subroutine(self):
        return None

    def get_php_source(self):
        template = r"""// Get current {function_comment_name}{comments}
{variables} = ${device_initial_name}->{function_headless_camel_case_name}({arguments});
{echos}
"""
        comments = []
        variables = []
        echos = []

        for result in self.get_results():
            comments.append(result.get_formatted_comment())
            variables.append(result.get_php_variable())
            echos.append(result.get_php_echo())

        if len(comments) > 1 and len(set(comments)) == 1:
            comments = comments[:1]

        if len(variables) > 1:
            variables = '$' + self.get_underscore_name(skip=1)
        else:
            variables = variables[0]

        while None in echos:
            echos.remove(None)

        if len(echos) > 1:
            echos.insert(0, '')

        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_php_source())

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               function_headless_camel_case_name=self.get_headless_camel_case_name(),
                               function_comment_name=self.get_comment_name(),
                               comments=''.join(comments),
                               variables=variables,
                               echos='\n'.join(echos),
                               arguments=', '.join(arguments))

class PHPExampleSetterFunction(common.ExampleSetterFunction):
    def get_php_subroutine(self):
        return None

    def get_php_source(self):
        template = '{comment1}{global_line_prefix}${device_initial_name}->{function_headless_camel_case_name}({arguments});{comment2}\n'
        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_php_source())

        return template.format(global_line_prefix=global_line_prefix,
                               device_initial_name=self.get_device().get_initial_name(),
                               function_headless_camel_case_name=self.get_headless_camel_case_name(),
                               arguments=', '.join(arguments),
                               comment1=self.get_formatted_comment1(global_line_prefix + '// {0}\n', '\r', '\n' + global_line_prefix + '// '),
                               comment2=self.get_formatted_comment2(' // {0}', ''))

class PHPExampleCallbackFunction(common.ExampleCallbackFunction):
    def get_php_subroutine(self):
        template1A = r"""// Callback function for {function_comment_name} callback{comments}
"""
        template1B = r"""{override_comment}
"""
        template2 = r"""function cb_{function_headless_camel_case_name}({parameters})
{{
{echos}{extra_message}
}}
"""
        override_comment = self.get_formatted_override_comment('// {0}', None, '\n// ')

        if override_comment == None:
            template1 = template1A
        else:
            template1 = template1B

        comments = []
        parameters = []
        echos = []

        for parameter in self.get_parameters():
            comments.append(parameter.get_formatted_comment())
            parameters.append(parameter.get_php_source())
            echos.append(parameter.get_php_echo())

        if len(comments) > 1 and len(set(comments)) == 1:
            comments = [comments[0].replace('parameter has', 'parameters have')]

        while None in echos:
            echos.remove(None)

        if len(echos) > 1:
            echos.append('    echo "\\n";')

        extra_message = self.get_formatted_extra_message('    echo "{0}\\n";')

        if len(extra_message) > 0 and len(echos) > 0:
            extra_message = '\n' + extra_message

        return template1.format(function_comment_name=self.get_comment_name(),
                                comments=''.join(comments),
                                override_comment=override_comment) + \
               template2.format(function_headless_camel_case_name=self.get_headless_camel_case_name(),
                                parameters=', '.join(parameters),
                                echos='\n'.join(echos),
                                extra_message=extra_message)

    def get_php_source(self):
        template = r"""// Register {function_comment_name} callback to function cb_{function_headless_camel_case_name}
${device_initial_name}->registerCallback({device_camel_case_category}{device_camel_case_name}::CALLBACK_{function_upper_case_name}, 'cb_{function_headless_camel_case_name}');
"""

        return template.format(device_camel_case_category=self.get_device().get_camel_case_category(),
                               device_camel_case_name=self.get_device().get_camel_case_name(),
                               device_initial_name=self.get_device().get_initial_name(),
                               function_headless_camel_case_name=self.get_headless_camel_case_name(),
                               function_upper_case_name=self.get_upper_case_name(),
                               function_comment_name=self.get_comment_name())

class PHPExampleCallbackPeriodFunction(common.ExampleCallbackPeriodFunction):
    def get_php_subroutine(self):
        return None

    def get_php_source(self):
        template = r"""// Set period for {function_comment_name} callback to {period_sec_short} ({period_msec}ms)
// Note: The {function_comment_name} callback is only called every {period_sec_long}
//       if the {function_comment_name} has changed since the last call!
${device_initial_name}->set{function_camel_case_name}{suffix}Period({arguments}{period_msec});
"""

        if self.get_device().get_underscore_name().startswith('imu'):
            suffix = '' # FIXME: special hack for IMU Brick name mismatch
        else:
            suffix = 'Callback'

        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_php_source())

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               function_camel_case_name=self.get_camel_case_name(),
                               function_comment_name=self.get_comment_name(),
                               suffix=suffix,
                               arguments=common.wrap_non_empty('', ', '.join(arguments), ', '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long)

class PHPExampleCallbackThresholdMinimumMaximum(common.ExampleCallbackThresholdMinimumMaximum):
    def get_php_source(self):
        template = '{minimum}, {maximum}'

        return template.format(minimum=self.get_formatted_minimum(),
                               maximum=self.get_formatted_maximum())

class PHPExampleCallbackThresholdFunction(common.ExampleCallbackThresholdFunction):
    def get_php_subroutine(self):
        return None

    def get_php_source(self):
        template = r"""// Configure threshold for {function_comment_name} "{option_comment}"{mininum_maximum_unit_comments}
${device_initial_name}->set{function_camel_case_name}CallbackThreshold({arguments}'{option_char}', {mininum_maximums});
"""
        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_php_source())

        mininum_maximums = []
        mininum_maximum_unit_comments = []

        for mininum_maximum in self.get_minimum_maximums():
            mininum_maximums.append(mininum_maximum.get_php_source())
            mininum_maximum_unit_comments.append(mininum_maximum.get_unit_comment())

        if len(mininum_maximum_unit_comments) > 1 and len(set(mininum_maximum_unit_comments)) == 1:
            mininum_maximum_unit_comments = mininum_maximum_unit_comments[:1]

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               function_camel_case_name=self.get_camel_case_name(),
                               function_comment_name=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(arguments), ', '),
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               mininum_maximums=', '.join(mininum_maximums),
                               mininum_maximum_unit_comments=''.join(mininum_maximum_unit_comments))

class PHPExampleSpecialFunction(common.ExampleSpecialFunction):
    def get_php_subroutine(self):
        return None

    def get_php_source(self):
        global global_line_prefix

        type = self.get_type()

        if type == 'empty':
            return ''
        elif type == 'debounce_period':
            template = r"""// Get threshold callbacks with a debounce time of {period_sec} ({period_msec}ms)
${device_initial_name}->setDebouncePeriod({period_msec});
"""
            period_msec, period_sec = self.get_formatted_debounce_period()

            return template.format(device_initial_name=self.get_device().get_initial_name(),
                                   period_msec=period_msec,
                                   period_sec=period_sec)
        elif type == 'sleep':
            templateA = '{comment1}{global_line_prefix}sleep({duration});{comment2}\n'
            templateB = '{comment1}{global_line_prefix}usleep({duration}*1000);{comment2}\n'
            duration = self.get_sleep_duration()

            if duration % 1000 == 0:
                duration /= 1000
                template = templateA
            else:
                template = templateB

            return template.format(global_line_prefix=global_line_prefix,
                                   duration=duration,
                                   comment1=self.get_formatted_sleep_comment1(global_line_prefix + '// {0}\n', '\r', '\n' + global_line_prefix + '// '),
                                   comment2=self.get_formatted_sleep_comment2(' // {0}', ''))
        elif type == 'wait':
            return None
        elif type == 'loop_header':
            template = '{comment}for($i = 0; $i < {limit}; $i++) {{\n'
            global_line_prefix = '    '

            return template.format(limit=self.get_loop_header_limit(),
                                   comment=self.get_formatted_loop_header_comment('// {0}\n', '', '\n// '))
        elif type == 'loop_footer':
            global_line_prefix = ''
            return '\r}\n'

class PHPExamplesGenerator(common.ExamplesGenerator):
    def get_bindings_name(self):
        return 'php'

    def get_constant_class(self):
        return PHPConstant

    def get_example_class(self):
        return PHPExample

    def get_example_argument_class(self):
        return PHPExampleArgument

    def get_example_parameter_class(self):
        return PHPExampleParameter

    def get_example_result_class(self):
        return PHPExampleResult

    def get_example_getter_function_class(self):
        return PHPExampleGetterFunction

    def get_example_setter_function_class(self):
        return PHPExampleSetterFunction

    def get_example_callback_function_class(self):
        return PHPExampleCallbackFunction

    def get_example_callback_period_function_class(self):
        return PHPExampleCallbackPeriodFunction

    def get_example_callback_threshold_minimum_maximum_class(self):
        return PHPExampleCallbackThresholdMinimumMaximum

    def get_example_callback_threshold_function_class(self):
        return PHPExampleCallbackThresholdFunction

    def get_example_special_function_class(self):
        return PHPExampleSpecialFunction

    def generate(self, device):
        examples_directory = self.get_examples_directory(device)
        examples = device.get_examples()

        if len(examples) == 0:
            print('  \033[01;31m- no examples\033[0m')
            return

        if not os.path.exists(examples_directory):
            os.makedirs(examples_directory)

        for example in examples:
            filename = 'Example{0}.php'.format(example.get_camel_case_name())
            filepath = os.path.join(examples_directory, filename)

            if example.is_incomplete():
                if os.path.exists(filepath) and self.skip_existing_incomplete_example:
                    print('  - ' + filename + ' \033[01;35m(incomplete, skipped)\033[0m')
                else:
                    print('  - ' + filename + ' \033[01;31m(incomplete)\033[0m')
            else:
                print('  - ' + filename)

            php = open(filepath, 'wb')
            php.write(example.get_php_source())
            php.close()

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', PHPExamplesGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
