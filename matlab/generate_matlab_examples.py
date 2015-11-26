#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MATLAB/Octave Examples Generator
Copyright (C) 2015 Matthias Bolte <matthias@tinkerforge.com>

generate_matlab_examples.py: Generator for MATLAB/Octave examples

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
from java.java_common import get_java_type

global_line_prefix = ''
global_quote = None
global_is_octave = False
global_java2int = r"""function int = java2int(value)
    if compare_versions(version(), "3.8", "<=")
        int = value.intValue();
    else
        int = value;
    end
end
"""

class MATLABFprintfFormatMixin(object):
    def get_matlab_fprintf_format(self):
        type = self.get_type()

        if type in ['char', 'string'] or ':bitmask:' in type:
            return '%s'
        elif type == 'float':
            return '%f'
        elif type.split(':')[0] != 'float' and self.get_divisor() == None:
            if global_is_octave:
                return '%d'
            else:
                return '%i'
        else:
            return '%g'

class MATLABConstant(common.Constant):
    def get_matlab_source(self):
        if global_is_octave:
            template = '{device_initial_name}.{constant_group_upper_case_name}_{constant_upper_case_name}'

            return template.format(device_initial_name=self.get_device().get_initial_name(),
                                   constant_group_upper_case_name=self.get_constant_group().get_upper_case_name(),
                                   constant_upper_case_name=self.get_upper_case_name())
        else:
            template = '{device_camel_case_category}{device_camel_case_name}.{constant_group_upper_case_name}_{constant_upper_case_name}'

            return template.format(device_camel_case_category=self.get_device().get_camel_case_category(),
                                   device_camel_case_name=self.get_device().get_camel_case_name(),
                                   constant_group_upper_case_name=self.get_constant_group().get_upper_case_name(),
                                   constant_upper_case_name=self.get_upper_case_name())

class MATLABExample(common.Example):
    def get_matlab_source(self):
        global global_quote
        global global_is_octave

        global_quote = "'"
        global_is_octave = False

        template = r"""function matlab_example_{example_underscore_name}()
    import com.tinkerforge.IPConnection;
    import com.tinkerforge.{device_camel_case_category}{device_camel_case_name};{incomplete}

    HOST = 'localhost';
    PORT = 4223;
    UID = '{dummy_uid}'; % Change to your UID

    ipcon = IPConnection(); % Create IP connection
    {device_initial_name} = handle({device_camel_case_category}{device_camel_case_name}(UID, ipcon), 'CallbackProperties'); % Create device object

    ipcon.connect(HOST, PORT); % Connect to brickd
    % Don't use device before ipcon is connected
{sources}
    input('Press key to exit\n', 's');{cleanups}
    ipcon.disconnect();
end{functions}
"""

        if self.is_incomplete():
            incomplete = '\n\n    % FIXME: This example is incomplete'
        else:
            incomplete = ''

        functions = []
        sources = []
        cleanups = []

        for function in self.get_functions():
            functions += function.get_matlab_functions()
            sources.append(function.get_matlab_source())

        for cleanup in self.get_cleanups():
            functions += cleanup.get_matlab_functions()
            cleanups.append(cleanup.get_matlab_source())

        unique_functions = []

        for function in functions:
            if function not in unique_functions:
                unique_functions.append(function)

        while None in sources:
            sources.remove(None)

        if len(sources) == 0:
            sources = ['    % TODO: Add example code here\n']

        while None in cleanups:
            cleanups.remove(None)

        return template.format(incomplete=incomplete,
                               example_underscore_name=self.get_underscore_name(),
                               device_camel_case_category=self.get_device().get_camel_case_category(),
                               device_camel_case_name=self.get_device().get_camel_case_name(),
                               device_initial_name=self.get_device().get_initial_name(),
                               dummy_uid=self.get_dummy_uid(),
                               functions=common.wrap_non_empty('\n\n', '\n'.join(unique_functions), '').rstrip('\n'),
                               sources='\n' + '\n'.join(sources).replace('\n\r', '').lstrip('\r'),
                               cleanups=common.wrap_non_empty('\n', '\n'.join(cleanups).replace('\n\r', '').lstrip('\r').rstrip('\n'), ''))

    def get_octave_source(self):
        global global_quote
        global global_is_octave

        global_quote = '"'
        global_is_octave = True

        template = r"""function octave_example_{example_underscore_name}()
    more off;{incomplete}

    HOST = "localhost";
    PORT = 4223;
    UID = "{dummy_uid}"; % Change to your UID

    ipcon = java_new("com.tinkerforge.IPConnection"); % Create IP connection
    {device_initial_name} = java_new("com.tinkerforge.{device_camel_case_category}{device_camel_case_name}", UID, ipcon); % Create device object

    ipcon.connect(HOST, PORT); % Connect to brickd
    % Don't use device before ipcon is connected
{sources}
    input("Press key to exit\n", "s");{cleanups}
    ipcon.disconnect();
end{functions}
"""

        if self.is_incomplete():
            incomplete = '\n\n    % FIXME: This example is incomplete'
        else:
            incomplete = ''

        functions = []
        sources = []
        cleanups = []

        for function in self.get_functions():
            functions += function.get_matlab_functions()
            sources.append(function.get_matlab_source())

        for cleanup in self.get_cleanups():
            functions += cleanup.get_matlab_functions()
            cleanups.append(cleanup.get_matlab_source())

        unique_functions = []

        for function in functions:
            if function not in unique_functions:
                unique_functions.append(function)

        while None in sources:
            sources.remove(None)

        if len(sources) == 0:
            sources = ['    # TODO: Add example code here\n']

        while None in cleanups:
            cleanups.remove(None)

        return template.format(incomplete=incomplete,
                               example_underscore_name=self.get_underscore_name(),
                               device_camel_case_category=self.get_device().get_camel_case_category(),
                               device_camel_case_name=self.get_device().get_camel_case_name(),
                               device_initial_name=self.get_device().get_initial_name(),
                               dummy_uid=self.get_dummy_uid(),
                               functions=common.wrap_non_empty('\n\n', '\n'.join(unique_functions), '').rstrip('\n'),
                               sources='\n' + '\n'.join(sources).replace('\n\r', '').lstrip('\r'),
                               cleanups=common.wrap_non_empty('\n', '\n'.join(cleanups).replace('\n\r', '').lstrip('\r').rstrip('\n'), ''))

class MATLABExampleArgument(common.ExampleArgument):
    def get_matlab_source(self):
        type = self.get_type()
        value = self.get_value()

        if type == 'bool':
            if value:
                return 'true'
            else:
                return 'false'
        elif type in  ['char', 'string']:
            return global_quote + value + global_quote
        elif ':bitmask:' in type:
            return common.make_c_like_bitmask(value, shift='bitshift({0}, {1})', combine='bitor({0}, {1})')
        elif type.endswith(':constant'):
            return self.get_value_constant().get_matlab_source()
        else:
            return str(value)

class MATLABExampleParameter(common.ExampleParameter, MATLABFprintfFormatMixin):
    def needs_octave_java2int(self):
        if global_is_octave:
            type = self.get_type().split(':')[0]

            if 'int' in type and get_java_type(type) != 'int':
                return True

        return False

    def get_matlab_fprintf(self):
        template = r"    fprintf({global_quote}{label_name}: {fprintf_format}{unit_final_name}\n{global_quote}, {to_binary_prefix}{java2int_prefix}e.{headless_camel_case_name}{java2int_suffix}{divisor}{to_binary_suffix});"

        if self.get_label_name() == None:
            return None

        if self.needs_octave_java2int():
            java2int_prefix = 'java2int('
            java2int_suffix = ')'
        else:
            java2int_prefix = ''
            java2int_suffix = ''

        type = self.get_type()

        # FIXME: dec2bin doesn't support leading zeros. therefore,
        #        the result is not padded to the requested number of digits
        if ':bitmask:' in type:
            to_binary_prefix = 'dec2bin('
            to_binary_suffix = ')'
        else:
            to_binary_prefix = ''
            to_binary_suffix = ''

        return template.format(global_quote=global_quote,
                               headless_camel_case_name=self.get_headless_camel_case_name(),
                               label_name=self.get_label_name().replace('%', '%%'),
                               fprintf_format=self.get_matlab_fprintf_format(),
                               divisor=self.get_formatted_divisor('/{0}'),
                               unit_final_name=self.get_unit_formatted_final_name(' {0}').replace('%', '%%'),
                               java2int_prefix=java2int_prefix,
                               java2int_suffix=java2int_suffix,
                               to_binary_prefix=to_binary_prefix,
                               to_binary_suffix=to_binary_suffix)

class MATLABExampleResult(common.ExampleResult, MATLABFprintfFormatMixin):
    def needs_octave_java2int(self):
        if global_is_octave:
            type = self.get_type().split(':')[0]

            if 'int' in type and get_java_type(type) != 'int':
                return True

        return False

    def get_matlab_variable(self):
        headless_camel_case_name = self.get_headless_camel_case_name()

        if headless_camel_case_name == self.get_device().get_initial_name():
            headless_camel_case_name += '_'

        return headless_camel_case_name

    def get_matlab_fprintf(self):
        template = r"    fprintf({global_quote}{label_name}: {fprintf_format}{unit_final_name}\n{global_quote}, {to_binary_prefix}{java2int_prefix}{object_prefix}{headless_camel_case_name}{java2int_suffix}{divisor}{to_binary_suffix});"

        if self.get_label_name() == None:
            return None

        headless_camel_case_name = self.get_headless_camel_case_name()

        if len(self.get_function().get_results()) > 1:
            object_prefix = self.get_function().get_headless_camel_case_name(skip=1) + '.'
        else:
            if headless_camel_case_name == self.get_device().get_initial_name():
                headless_camel_case_name += '_'

            object_prefix = ''

        if self.needs_octave_java2int():
            java2int_prefix = 'java2int('
            java2int_suffix = ')'
        else:
            java2int_prefix = ''
            java2int_suffix = ''

        type = self.get_type()

        # FIXME: dec2bin doesn't support leading zeros. therefore,
        #        the result is not padded to the requested number of digits
        if ':bitmask:' in type:
            to_binary_prefix = 'dec2bin('
            to_binary_suffix = ')'
        else:
            to_binary_prefix = ''
            to_binary_suffix = ''

        return template.format(global_quote=global_quote,
                               headless_camel_case_name=headless_camel_case_name,
                               label_name=self.get_label_name().replace('%', '%%'),
                               fprintf_format=self.get_matlab_fprintf_format(),
                               divisor=self.get_formatted_divisor('/{0}'),
                               unit_final_name=self.get_unit_formatted_final_name(' {0}').replace('%', '%%'),
                               object_prefix=object_prefix,
                               java2int_prefix=java2int_prefix,
                               java2int_suffix=java2int_suffix,
                               to_binary_prefix=to_binary_prefix,
                               to_binary_suffix=to_binary_suffix)

class MATLABExampleGetterFunction(common.ExampleGetterFunction):
    def get_matlab_functions(self):
        if global_is_octave:
            for result in self.get_results():
                if result.needs_octave_java2int():
                    return [global_java2int]

        return []

    def get_matlab_source(self):
        template = r"""    % Get current {function_comment_name}{comments}
    {variable} = {device_initial_name}.{function_headless_camel_case_name}({arguments});
{fprintfs}
"""
        comments = []
        variables = []
        fprintfs = []

        for result in self.get_results():
            comments.append(result.get_formatted_comment())
            variables.append(result.get_matlab_variable())
            fprintfs.append(result.get_matlab_fprintf())

        if len(comments) > 1 and len(set(comments)) == 1:
            comments = comments[:1]

        if len(variables) > 1:
            variable = self.get_headless_camel_case_name(skip=1)
        else:
            variable = variables[0]

        while None in fprintfs:
            fprintfs.remove(None)

        if len(fprintfs) > 1:
            fprintfs.insert(0, '')

        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_matlab_source())

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               function_headless_camel_case_name=self.get_headless_camel_case_name(),
                               function_comment_name=self.get_comment_name(),
                               comments=''.join(comments),
                               variable=variable,
                               fprintfs='\n'.join(fprintfs),
                               arguments=', '.join(arguments))

class MATLABExampleSetterFunction(common.ExampleSetterFunction):
    def get_matlab_functions(self):
        return []

    def get_matlab_source(self):
        template = '{comment1}{global_line_prefix}    {device_initial_name}.{function_headless_camel_case_name}({arguments});{comment2}\n'
        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_matlab_source())

        return template.format(global_line_prefix=global_line_prefix,
                               device_initial_name=self.get_device().get_initial_name(),
                               function_headless_camel_case_name=self.get_headless_camel_case_name(),
                               arguments=', '.join(arguments),
                               comment1=self.get_formatted_comment1(global_line_prefix + '    % {0}\n', '\r', '\n' + global_line_prefix + '    % '),
                               comment2=self.get_formatted_comment2(' % {0}', ''))

class MATLABExampleCallbackFunction(common.ExampleCallbackFunction):
    def get_matlab_functions(self):
        template1A = r"""% Callback function for {function_comment_name} callback{comments}
"""
        template1B = r"""{override_comment}
"""
        template2 = r"""function cb_{function_underscore_name}(e)
{fprintfs}{extra_message}
end
"""
        override_comment = self.get_formatted_override_comment('% {0}', None, '\n% ')

        if override_comment == None:
            template1 = template1A
        else:
            template1 = template1B

        comments = []
        fprintfs = []

        for parameter in self.get_parameters():
            comments.append(parameter.get_formatted_comment())
            fprintfs.append(parameter.get_matlab_fprintf())

        if len(comments) > 1 and len(set(comments)) == 1:
            comments = [comments[0].replace('parameter has', 'parameters have')]

        while None in fprintfs:
            fprintfs.remove(None)

        if len(fprintfs) > 1:
            fprintfs.append(r"    fprintf({0}\n{0});".format(global_quote))

        extra_message = self.get_formatted_extra_message(r"    fprintf({0}{{0}}\n{0});".format(global_quote)).replace('%', '%%')

        if len(extra_message) > 0 and len(fprintfs) > 0:
            extra_message = '\n' + extra_message

        functions = [template1.format(function_comment_name=self.get_comment_name(),
                                      comments=''.join(comments),
                                      override_comment=override_comment) + \
                     template2.format(function_underscore_name=self.get_underscore_name(),
                                      fprintfs='\n'.join(fprintfs),
                                      extra_message=extra_message)]

        if global_is_octave:
            for parameter in self.get_parameters():
                if parameter.needs_octave_java2int():
                    functions.append(global_java2int)
                    break

        return functions

    def get_matlab_source(self):
        templateA = r"""    % Register {function_comment_name} callback to function cb_{function_underscore_name}
    set({device_initial_name}, '{function_camel_case_name}Callback', @(h, e) cb_{function_underscore_name}(e));
"""
        templateB = r"""    % Register {function_comment_name} callback to function cb_{function_underscore_name}
    {device_initial_name}.add{function_camel_case_name}Callback(@cb_{function_underscore_name});
"""

        if not global_is_octave:
            template = templateA
        else:
            template = templateB

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               function_underscore_name=self.get_underscore_name(),
                               function_camel_case_name=self.get_camel_case_name(),
                               function_comment_name=self.get_comment_name())

class MATLABExampleCallbackPeriodFunction(common.ExampleCallbackPeriodFunction):
    def get_matlab_functions(self):
        return []

    def get_matlab_source(self):
        template = r"""    % Set period for {function_comment_name} callback to {period_sec_short} ({period_msec}ms)
    % Note: The {function_comment_name} callback is only called every {period_sec_long}
    %       if the {function_comment_name} has changed since the last call!
    {device_initial_name}.set{function_camel_case_name}{suffix}Period({arguments}{period_msec});
"""

        if self.get_device().get_underscore_name().startswith('imu'):
            suffix = '' # FIXME: special hack for IMU Brick name mismatch
        else:
            suffix = 'Callback'

        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_matlab_source())

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               function_camel_case_name=self.get_camel_case_name(),
                               function_comment_name=self.get_comment_name(),
                               suffix=suffix,
                               arguments=common.wrap_non_empty('', ', '.join(arguments), ', '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long)

class MATLABExampleCallbackThresholdMinimumMaximum(common.ExampleCallbackThresholdMinimumMaximum):
    def get_matlab_source(self):
        template = '{minimum}, {maximum}'

        return template.format(minimum=self.get_formatted_minimum(),
                               maximum=self.get_formatted_maximum())

class MATLABExampleCallbackThresholdFunction(common.ExampleCallbackThresholdFunction):
    def get_matlab_functions(self):
        return []

    def get_matlab_source(self):
        template = r"""    % Configure threshold for {function_comment_name} "{option_comment}"{mininum_maximum_unit_comments}
    {device_initial_name}.set{function_camel_case_name}CallbackThreshold({arguments}{global_quote}{option_char}{global_quote}, {mininum_maximums});
"""
        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_matlab_source())

        mininum_maximums = []
        mininum_maximum_unit_comments = []

        for mininum_maximum in self.get_minimum_maximums():
            mininum_maximums.append(mininum_maximum.get_matlab_source())
            mininum_maximum_unit_comments.append(mininum_maximum.get_unit_comment())

        if len(mininum_maximum_unit_comments) > 1 and len(set(mininum_maximum_unit_comments)) == 1:
            mininum_maximum_unit_comments = mininum_maximum_unit_comments[:1]

        return template.format(global_quote=global_quote,
                               device_initial_name=self.get_device().get_initial_name(),
                               function_camel_case_name=self.get_camel_case_name(),
                               function_comment_name=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(arguments), ', '),
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               mininum_maximums=', '.join(mininum_maximums),
                               mininum_maximum_unit_comments=''.join(mininum_maximum_unit_comments))

class MATLABExampleSpecialFunction(common.ExampleSpecialFunction):
    def get_matlab_functions(self):
        return []

    def get_matlab_source(self):
        global global_line_prefix

        type = self.get_type()

        if type == 'empty':
            return ''
        elif type == 'debounce_period':
            template = r"""    % Get threshold callbacks with a debounce time of {period_sec} ({period_msec}ms)
    {device_initial_name}.setDebouncePeriod({period_msec});
"""
            period_msec, period_sec = self.get_formatted_debounce_period()

            return template.format(device_initial_name=self.get_device().get_initial_name(),
                                   period_msec=period_msec,
                                   period_sec=period_sec)
        elif type == 'sleep':
            template = '{comment1}{global_line_prefix}    pause({duration});{comment2}\n'
            duration = self.get_sleep_duration()

            if duration % 1000 == 0:
                duration //= 1000
            else:
                duration /= 1000.0

            return template.format(global_line_prefix=global_line_prefix,
                                   duration=duration,
                                   comment1=self.get_formatted_sleep_comment1(global_line_prefix + '    % {0}\n', '\r', '\n' + global_line_prefix + '    % '),
                                   comment2=self.get_formatted_sleep_comment2(' % {0}', ''))
        elif type == 'wait':
            return None
        elif type == 'loop_header':
            template = '{comment}    for i = 0:{limit}\n'
            global_line_prefix = '    '

            return template.format(limit=self.get_loop_header_limit() - 1,
                                   comment=self.get_formatted_loop_header_comment('    % {0}\n', '', '\n    # '))
        elif type == 'loop_footer':
            global_line_prefix = ''

            return '\r    end'

class MATLABExamplesGenerator(common.ExamplesGenerator):
    def get_bindings_name(self):
        return 'matlab'

    def get_constant_class(self):
        return MATLABConstant

    def get_example_class(self):
        return MATLABExample

    def get_example_argument_class(self):
        return MATLABExampleArgument

    def get_example_parameter_class(self):
        return MATLABExampleParameter

    def get_example_result_class(self):
        return MATLABExampleResult

    def get_example_getter_function_class(self):
        return MATLABExampleGetterFunction

    def get_example_setter_function_class(self):
        return MATLABExampleSetterFunction

    def get_example_callback_function_class(self):
        return MATLABExampleCallbackFunction

    def get_example_callback_period_function_class(self):
        return MATLABExampleCallbackPeriodFunction

    def get_example_callback_threshold_minimum_maximum_class(self):
        return MATLABExampleCallbackThresholdMinimumMaximum

    def get_example_callback_threshold_function_class(self):
        return MATLABExampleCallbackThresholdFunction

    def get_example_special_function_class(self):
        return MATLABExampleSpecialFunction

    def generate(self, device):
        examples_directory = self.get_examples_directory(device)
        examples = device.get_examples()

        if len(examples) == 0:
            print('  \033[01;31m- no examples\033[0m')
            return

        if not os.path.exists(examples_directory):
            os.makedirs(examples_directory)

        # matlab
        for example in examples:
            filename = 'matlab_example_{0}.m'.format(example.get_underscore_name())
            filepath = os.path.join(examples_directory, filename)

            if example.is_incomplete():
                if os.path.exists(filepath) and self.skip_existing_incomplete_example:
                    print('  - ' + filename + ' \033[01;35m(incomplete, skipped)\033[0m')
                else:
                    print('  - ' + filename + ' \033[01;31m(incomplete)\033[0m')
            else:
                print('  - ' + filename)

            m = open(os.path.join(examples_directory, filename), 'wb')
            m.write(example.get_matlab_source())
            m.close()

        # octave
        for example in examples:
            filename = 'octave_example_{0}.m'.format(example.get_underscore_name())
            filepath = os.path.join(examples_directory, filename)

            if example.is_incomplete():
                if os.path.exists(filepath) and self.skip_existing_incomplete_example:
                    print('  - ' + filename + ' \033[01;35m(incomplete, skipped)\033[0m')
                    continue
                else:
                    print('  - ' + filename + ' \033[01;31m(incomplete)\033[0m')
            else:
                print('  - ' + filename)

            m = open(filepath, 'wb')
            m.write(example.get_octave_source())
            m.close()

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', MATLABExamplesGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
