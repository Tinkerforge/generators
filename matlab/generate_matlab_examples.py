#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MATLAB/Octave Examples Generator
Copyright (C) 2015-2019 Matthias Bolte <matthias@tinkerforge.com>

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
from java.java_common import JavaDevice, get_java_type
import matlab_common

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
        type_ = self.get_type()

        if type_ in ['char', 'string'] or ':bitmask:' in type_:
            return '%s'
        elif type_ == 'float':
            return '%f'
        elif type_.split(':')[0] != 'float' and self.get_divisor() == None:
            if global_is_octave:
                return '%d'
            else:
                return '%i'
        else:
            return '%g'

class MATLABConstant(common.Constant):
    def get_matlab_source(self):
        if global_is_octave:
            template = '{device_name}.{constant_group_name}_{constant_name}'

            return template.format(device_name=self.get_device().get_initial_name(),
                                   constant_group_name=self.get_constant_group().get_name().upper,
                                   constant_name=self.get_name().upper)
        else:
            template = '{device_category}{device_name}.{constant_group_name}_{constant_name}'

            return template.format(device_category=self.get_device().get_category().camel,
                                   device_name=self.get_device().get_name().camel,
                                   constant_group_name=self.get_constant_group().get_name().upper,
                                   constant_name=self.get_name().upper)

class MATLABExample(common.Example):
    def get_matlab_source(self):
        global global_quote
        global global_is_octave

        global_quote = "'"
        global_is_octave = False

        template = r"""function matlab_example_{example_name}()
    import com.tinkerforge.IPConnection;
    import com.tinkerforge.{device_category}{device_name_camel};{incomplete}{description}

    HOST = 'localhost';
    PORT = 4223;
    UID = '{dummy_uid}'; % Change {dummy_uid} to the UID of your {device_name_long_display}

    ipcon = IPConnection(); % Create IP connection
    {device_name_initial} = handle({device_category}{device_name_camel}(UID, ipcon), 'CallbackProperties'); % Create device object

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

        if self.get_description() != None:
            description = '\n\n    % {0}'.format(self.get_description().replace('\n', '\n    % '))
        else:
            description = ''

        functions = []
        sources = []
        cleanups = []

        for function in self.get_functions():
            functions += function.get_matlab_functions(0)
            sources.append(function.get_matlab_source())

        for cleanup in self.get_cleanups():
            functions += cleanup.get_matlab_functions(0)
            cleanups.append(cleanup.get_matlab_source())

        for function in self.get_functions():
            functions += function.get_matlab_functions(1)

        for cleanup in self.get_cleanups():
            functions += cleanup.get_matlab_functions(1)

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
                               description=description,
                               example_name=self.get_name().under,
                               device_category=self.get_device().get_category().camel,
                               device_name_camel=self.get_device().get_name().camel,
                               device_name_initial=self.get_device().get_initial_name(),
                               device_name_long_display=self.get_device().get_long_display_name(),
                               dummy_uid=self.get_dummy_uid(),
                               functions=common.wrap_non_empty('\n\n', '\n'.join(unique_functions), '').rstrip('\n'),
                               sources='\n' + '\n'.join(sources).replace('\n\r', '').lstrip('\r'),
                               cleanups=common.wrap_non_empty('\n', '\n'.join(cleanups).replace('\n\r', '').lstrip('\r').rstrip('\n'), ''))

    def get_octave_source(self):
        global global_quote
        global global_is_octave

        global_quote = '"'
        global_is_octave = True

        template = r"""function octave_example_{example_name}()
    more off;{incomplete}{description}

    HOST = "localhost";
    PORT = 4223;
    UID = "{dummy_uid}"; % Change {dummy_uid} to the UID of your {device_name_long_display}

    ipcon = javaObject("com.tinkerforge.IPConnection"); % Create IP connection
    {device_name_initial} = javaObject("com.tinkerforge.{device_category}{device_name_camel}", UID, ipcon); % Create device object

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

        if self.get_description() != None:
            description = '\n\n    % {0}'.format(self.get_description().replace('\n', '\n    % '))
        else:
            description = ''

        functions = []
        sources = []
        cleanups = []

        for function in self.get_functions():
            functions += function.get_matlab_functions(0)
            sources.append(function.get_matlab_source())

        for cleanup in self.get_cleanups():
            functions += cleanup.get_matlab_functions(0)
            cleanups.append(cleanup.get_matlab_source())

        for function in self.get_functions():
            functions += function.get_matlab_functions(1)

        for cleanup in self.get_cleanups():
            functions += cleanup.get_matlab_functions(1)

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
                               description=description,
                               example_name=self.get_name().under,
                               device_category=self.get_device().get_category().camel,
                               device_name_camel=self.get_device().get_name().camel,
                               device_name_initial=self.get_device().get_initial_name(),
                               device_name_long_display=self.get_device().get_long_display_name(),
                               dummy_uid=self.get_dummy_uid(),
                               functions=common.wrap_non_empty('\n\n', '\n'.join(unique_functions), '').rstrip('\n'),
                               sources='\n' + '\n'.join(sources).replace('\n\r', '').lstrip('\r'),
                               cleanups=common.wrap_non_empty('\n', '\n'.join(cleanups).replace('\n\r', '').lstrip('\r').rstrip('\n'), ''))

class MATLABExampleArgument(common.ExampleArgument):
    def get_matlab_source(self):
        type_ = self.get_type()

        def helper(value):
            if type_ == 'bool':
                return str(bool(value)).lower()
            elif type_ in  ['char', 'string']:
                return global_quote + value.replace(global_quote, '\\' + global_quote) + global_quote
            elif ':bitmask:' in type_:
                return common.make_c_like_bitmask(value, shift='bitshift({0}, {1})', combine='bitor({0}, {1})')
            elif type_.endswith(':constant'):
                return self.get_value_constant(value).get_matlab_source()
            else:
                return str(value)

        value = self.get_value()

        if isinstance(value, list):
            return '[{0}]'.format(' '.join([helper(item) for item in value]))

        return helper(value)

class MATLABExampleArgumentsMixin(object):
    def get_matlab_arguments(self):
        return [argument.get_matlab_source() for argument in self.get_arguments()]

class MATLABExampleParameter(common.ExampleParameter, MATLABFprintfFormatMixin):
    def needs_octave_java2int(self):
        if global_is_octave:
            type_ = self.get_type().split(':')[0]

            if 'int' in type_ and get_java_type(type_, 1, legacy=self.get_device().has_java_legacy_types(), octave=True) != 'int':
                return True

        return False

    def get_matlab_fprintfs(self):
        if self.get_type().split(':')[-1] == 'constant':
            if self.get_label_name() == None:
                return []

            # FIXME: need to handle multiple labels
            assert self.get_label_count() == 1

            template = '{global_line_prefix}    {else_}if {cast_prefix}e.{name}{cast_suffix} == {constant_name}\n{global_line_prefix}        fprintf({global_quote}{label}: {constant_title}\\n{global_quote});{comment}'
            constant_group = self.get_constant_group()
            type_ = self.get_type()

            if self.needs_octave_java2int():
                cast_prefix = 'java2int('
                cast_suffix = ')'
            elif not global_is_octave and type_ == 'string':
                cast_prefix = 'char('
                cast_suffix = ')'
            else:
                cast_prefix = ''
                cast_suffix = ''

            result = []

            for constant in constant_group.get_constants():
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              global_quote=global_quote,
                                              else_='else' if len(result) > 0 else '',
                                              name=self.get_name().headless,
                                              cast_prefix=cast_prefix,
                                              cast_suffix=cast_suffix,
                                              label=self.get_label_name().replace('%', '%%'),
                                              constant_name=constant.get_value() if global_is_octave else 'com.tinkerforge.' + constant.get_matlab_source(),
                                              constant_title=constant.get_name().space,
                                              comment=self.get_formatted_comment(' % {0}')))

            result = ['\r' + '\n'.join(result) + '\n    end\r']
        else:
            template = r"{global_line_prefix}    fprintf({global_quote}{label}: {fprintf_format}{unit}\n{global_quote}, {to_binary_prefix}{cast_prefix}e.{name}{index}{cast_suffix}{divisor}{to_binary_suffix});{comment}"

            if self.get_label_name() == None:
                return []

            if self.get_cardinality() < 0:
                return [] # FIXME: streaming

            type_ = self.get_type()

            if self.needs_octave_java2int():
                cast_prefix = 'java2int('
                cast_suffix = ')'
            elif not global_is_octave and type_ == 'string':
                cast_prefix = 'char('
                cast_suffix = ')'
            else:
                cast_prefix = ''
                cast_suffix = ''

            # FIXME: dec2bin doesn't support leading zeros. therefore,
            #        the result is not padded to the requested number of digits
            if ':bitmask:' in type_:
                to_binary_prefix = 'dec2bin('
                to_binary_suffix = ')'
            else:
                to_binary_prefix = ''
                to_binary_suffix = ''

            result = []

            for index in range(self.get_label_count()):
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              global_quote=global_quote,
                                              name=self.get_name().headless,
                                              label=self.get_label_name(index=index).replace('%', '%%'),
                                              fprintf_format=self.get_matlab_fprintf_format(),
                                              index='({0})'.format(index + 1) if self.get_label_count() > 1 else '',
                                              divisor=self.get_formatted_divisor('/{0}'),
                                              unit=self.get_formatted_unit_name(' {0}').replace('%', '%%'),
                                              cast_prefix=cast_prefix,
                                              cast_suffix=cast_suffix,
                                              to_binary_prefix=to_binary_prefix,
                                              to_binary_suffix=to_binary_suffix,
                                              comment=self.get_formatted_comment(' % {0}')))

        return result

class MATLABExampleResult(common.ExampleResult, MATLABFprintfFormatMixin):
    def needs_octave_java2int(self):
        if global_is_octave:
            type_ = self.get_type().split(':')[0]

            if 'int' in type_ and get_java_type(type_, 1, legacy=self.get_device().has_java_legacy_types(), octave=True) != 'int':
                return True

        return False

    def get_matlab_variable(self):
        name = self.get_name().headless

        if name == self.get_device().get_initial_name():
            name += '_'

        return name

    def get_matlab_fprintfs(self):
        if self.get_type().split(':')[-1] == 'constant':
            # FIXME: need to handle multiple labels
            assert self.get_label_count() == 1

            template = '{global_line_prefix}    {else_}if {cast_prefix}{object_prefix}{name}{cast_suffix} == {constant_name}\n{global_line_prefix}        fprintf({global_quote}{label}: {constant_title}\\n{global_quote});{comment}'
            constant_group = self.get_constant_group()
            name = self.get_name().headless

            if len(self.get_function().get_results()) > 1:
                object_prefix = self.get_function().get_name(skip=1).headless + '.'
            else:
                if name == self.get_device().get_initial_name():
                    name += '_'

                object_prefix = ''

            type_ = self.get_type()

            if self.needs_octave_java2int():
                cast_prefix = 'java2int('
                cast_suffix = ')'
            elif not global_is_octave and type_ == 'string':
                cast_prefix = 'char('
                cast_suffix = ')'
            else:
                cast_prefix = ''
                cast_suffix = ''

            result = []

            for constant in constant_group.get_constants():
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              global_quote=global_quote,
                                              else_='else' if len(result) > 0 else '',
                                              object_prefix=object_prefix,
                                              name=name,
                                              label=self.get_label_name().replace('%', '%%'),
                                              constant_name=constant.get_value() if global_is_octave else constant.get_matlab_source(),
                                              constant_title=constant.get_name().space,
                                              cast_prefix=cast_prefix,
                                              cast_suffix=cast_suffix,
                                              comment=self.get_formatted_comment(' % {0}')))

            result = ['\r' + '\n'.join(result) + '\n    end\r']
        else:
            template = r"{global_line_prefix}    fprintf({global_quote}{label}: {fprintf_format}{unit}\n{global_quote}, {to_binary_prefix}{cast_prefix}{object_prefix}{name}{index}{cast_suffix}{divisor}{to_binary_suffix});{comment}"

            if self.get_label_name() == None:
                return []

            if self.get_cardinality() < 0:
                return [] # FIXME: streaming

            name = self.get_name().headless

            if len(self.get_function().get_results()) > 1:
                object_prefix = self.get_function().get_name(skip=1).headless + '.'
            else:
                if name == self.get_device().get_initial_name():
                    name += '_'

                object_prefix = ''

            type_ = self.get_type()

            if self.needs_octave_java2int():
                cast_prefix = 'java2int('
                cast_suffix = ')'
            elif not global_is_octave and type_ == 'string':
                cast_prefix = 'char('
                cast_suffix = ')'
            else:
                cast_prefix = ''
                cast_suffix = ''

            # FIXME: dec2bin doesn't support leading zeros. therefore,
            #        the result is not padded to the requested number of digits
            if ':bitmask:' in type_:
                to_binary_prefix = 'dec2bin('
                to_binary_suffix = ')'
            else:
                to_binary_prefix = ''
                to_binary_suffix = ''

            result = []

            for index in range(self.get_label_count()):
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              global_quote=global_quote,
                                              object_prefix=object_prefix,
                                              name=name,
                                              label=self.get_label_name(index=index).replace('%', '%%'),
                                              fprintf_format=self.get_matlab_fprintf_format(),
                                              index='({0})'.format(index + 1) if self.get_label_count() > 1 else '',
                                              divisor=self.get_formatted_divisor('/{0}'),
                                              unit=self.get_formatted_unit_name(' {0}').replace('%', '%%'),
                                              cast_prefix=cast_prefix,
                                              cast_suffix=cast_suffix,
                                              to_binary_prefix=to_binary_prefix,
                                              to_binary_suffix=to_binary_suffix,
                                              comment=self.get_formatted_comment(' % {0}')))

        return result

class MATLABExampleGetterFunction(common.ExampleGetterFunction, MATLABExampleArgumentsMixin):
    def get_matlab_functions(self, phase):
        if phase == 1 and global_is_octave:
            for result in self.get_results():
                if result.needs_octave_java2int():
                    return [global_java2int]

        return []

    def get_matlab_source(self):
        template = r"""{global_line_prefix}    % Get current {function_name_comment}
{global_line_prefix}    {variable} = {device_name_initial}.{function_name_headless}({arguments});
{fprintfs}
"""
        variables = []
        fprintfs = []

        for result in self.get_results():
            variables.append(result.get_matlab_variable())
            fprintfs += result.get_matlab_fprintfs()

        if len(variables) > 1:
            variable = self.get_name(skip=1).headless
        else:
            variable = variables[0]

        while None in fprintfs:
            fprintfs.remove(None)

        if len(fprintfs) > 1:
            fprintfs.insert(0, '\b')

        return template.format(global_line_prefix=global_line_prefix,
                               device_name_initial=self.get_device().get_initial_name(),
                               function_name_headless=self.get_name().headless,
                               function_name_comment=self.get_comment_name(),
                               variable=variable,
                               fprintfs='\n'.join(fprintfs).replace('\b\n\r', '\n').replace('\b', '').replace('\r\n\r', '\n\n').rstrip('\r').replace('\r', '\n'),
                               arguments=', '.join(self.get_matlab_arguments()))

class MATLABExampleSetterFunction(common.ExampleSetterFunction, MATLABExampleArgumentsMixin):
    def get_matlab_functions(self, phase):
        return []

    def get_matlab_source(self):
        template = '{comment1}{global_line_prefix}    {device_name}.{function_name}({arguments});{comment2}\n'

        result = template.format(global_line_prefix=global_line_prefix,
                                 device_name=self.get_device().get_initial_name(),
                                 function_name=self.get_name().headless,
                                 arguments=',<BP>'.join(self.get_matlab_arguments()),
                                 comment1=self.get_formatted_comment1(global_line_prefix + '    % {0}\n', '\r', '\n' + global_line_prefix + '    % '),
                                 comment2=self.get_formatted_comment2(' % {0}', ''))

        return common.break_string(result, '.{}('.format(self.get_name().headless), continuation=' ...')

class MATLABExampleCallbackFunction(common.ExampleCallbackFunction):
    def get_matlab_functions(self, phase):
        if phase == 1:
            if global_is_octave:
                for parameter in self.get_parameters():
                    if parameter.needs_octave_java2int():
                        return [global_java2int]

            return []

        template1A = r"""% Callback function for {function_name_comment} callback
"""
        template1B = r"""{override_comment}
"""
        template2 = r"""function cb_{function_name_under}(e)
{fprintfs}{extra_message}
end
"""
        override_comment = self.get_formatted_override_comment('% {0}', None, '\n% ')

        if override_comment == None:
            template1 = template1A
        else:
            template1 = template1B

        fprintfs = []

        for parameter in self.get_parameters():
            fprintfs += parameter.get_matlab_fprintfs()

        while None in fprintfs:
            fprintfs.remove(None)

        if len(fprintfs) > 1:
            fprintfs.append(r"    fprintf({0}\n{0});".format(global_quote))

        extra_message = self.get_formatted_extra_message(r"    fprintf({0}{{0}}\n{0});".format(global_quote)).replace('%', '%%')

        if len(extra_message) > 0 and len(fprintfs) > 0:
            extra_message = '\n' + extra_message

        functions = [template1.format(function_name_comment=self.get_comment_name(),
                                      override_comment=override_comment) + \
                     template2.format(function_name_under=self.get_name().under,
                                      fprintfs='\n'.join(fprintfs).replace('\r\n\r', '\n\n').strip('\r').replace('\r', '\n'),
                                      extra_message=extra_message)]

        return functions

    def get_matlab_source(self):
        template1 = r"""    % Register {function_name_comment}<BP>callback<BP>to<BP>function<BP>cb_{function_name_under}
"""
        template2A = r"""    set({device_name}, '{function_name_camel}Callback',<BP>@(h, e) cb_{function_name_under}(e));
"""
        template2B = r"""    {device_name}.add{function_name_camel}Callback(@cb_{function_name_under});
"""

        if not global_is_octave:
            template2 = template2A
        else:
            template2 = template2B

        result1 = template1.format(function_name_under=self.get_name().under,
                                   function_name_comment=self.get_comment_name())
        result2 = template2.format(device_name=self.get_device().get_initial_name(),
                                   function_name_under=self.get_name().under,
                                   function_name_camel=self.get_name().camel)

        return common.break_string(result1, '% ', indent_tail='% ') + \
               common.break_string(result2, 'set(',)

class MATLABExampleCallbackPeriodFunction(common.ExampleCallbackPeriodFunction, MATLABExampleArgumentsMixin):
    def get_matlab_functions(self, phase):
        return []

    def get_matlab_source(self):
        templateA = r"""    % Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms)
    {device_name}.set{function_name_camel}Period({arguments}{period_msec});
"""
        templateB = r"""    % Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms)
    % Note: The {function_name_comment} callback is only called every {period_sec_long}
    %       if the {function_name_comment} has changed since the last call!
    {device_name}.set{function_name_camel}CallbackPeriod({arguments}{period_msec});
"""

        if self.get_device().get_name().space.startswith('IMU'):
            template = templateA # FIXME: special hack for IMU Brick (2.0) callback behavior and name mismatch
        else:
            template = templateB

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        return template.format(device_name=self.get_device().get_initial_name(),
                               function_name_camel=self.get_name().camel,
                               function_name_comment=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_matlab_arguments()), ', '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long)

class MATLABExampleCallbackThresholdMinimumMaximum(common.ExampleCallbackThresholdMinimumMaximum):
    def get_matlab_source(self):
        template = '{minimum}, {maximum}'

        return template.format(minimum=self.get_formatted_minimum(),
                               maximum=self.get_formatted_maximum())

class MATLABExampleCallbackThresholdFunction(common.ExampleCallbackThresholdFunction, MATLABExampleArgumentsMixin):
    def get_matlab_functions(self, phase):
        return []

    def get_matlab_source(self):
        template = r"""    % Configure threshold for {function_name_comment} "{option_comment}"
    {device_name}.set{function_name_camel}CallbackThreshold({arguments}{global_quote}{option_char}{global_quote}, {minimum_maximums});
"""
        minimum_maximums = []

        for minimum_maximum in self.get_minimum_maximums():
            minimum_maximums.append(minimum_maximum.get_matlab_source())

        return template.format(global_quote=global_quote,
                               device_name=self.get_device().get_initial_name(),
                               function_name_camel=self.get_name().camel,
                               function_name_comment=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_matlab_arguments()), ', '),
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               minimum_maximums=', '.join(minimum_maximums))

class MATLABExampleCallbackConfigurationFunction(common.ExampleCallbackConfigurationFunction, MATLABExampleArgumentsMixin):
    def get_matlab_functions(self, phase):
        return []

    def get_matlab_source(self):
        templateA = r"""    % Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms)
    {device_name}.set{function_name_camel}CallbackConfiguration({arguments}{period_msec}{value_has_to_change});
"""
        templateB = r"""    % Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms) without a threshold
    {device_name}.set{function_name_camel}CallbackConfiguration({arguments}{period_msec}{value_has_to_change}, {global_quote}{option_char}{global_quote}, {minimum_maximums});
"""
        templateC = r"""    % Configure threshold for {function_name_comment} "{option_comment}"
    % with a debounce period of {period_sec_short} ({period_msec}ms)
    {device_name}.set{function_name_camel}CallbackConfiguration({arguments}{period_msec}{value_has_to_change}, {global_quote}{option_char}{global_quote}, {minimum_maximums});
"""

        if self.get_option_char() == None:
            template = templateA
        elif self.get_option_char() == 'x':
            template = templateB
        else:
            template = templateC

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        minimum_maximums = []

        for minimum_maximum in self.get_minimum_maximums():
            minimum_maximums.append(minimum_maximum.get_matlab_source())

        return template.format(global_quote=global_quote,
                               device_name=self.get_device().get_initial_name(),
                               function_name_camel=self.get_name().camel,
                               function_name_comment=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_matlab_arguments()), ', '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long,
                               value_has_to_change=common.wrap_non_empty(', ', self.get_value_has_to_change('true', 'false', ''), ''),
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               minimum_maximums=', '.join(minimum_maximums))

class MATLABExampleSpecialFunction(common.ExampleSpecialFunction):
    def get_matlab_functions(self, phase):
        return []

    def get_matlab_source(self):
        global global_line_prefix

        type_ = self.get_type()

        if type_ == 'empty':
            return ''
        elif type_ == 'debounce_period':
            template = r"""    % Get threshold callbacks with a debounce time of {period_sec} ({period_msec}ms)
    {device_name}.setDebouncePeriod({period_msec});
"""
            period_msec, period_sec = self.get_formatted_debounce_period()

            return template.format(device_name=self.get_device().get_initial_name(),
                                   period_msec=period_msec,
                                   period_sec=period_sec)
        elif type_ == 'sleep':
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
        elif type_ == 'wait':
            return None
        elif type_ == 'loop_header':
            template = '{comment}    for i = 0:{limit}\n'
            global_line_prefix = '    '

            return template.format(limit=self.get_loop_header_limit() - 1,
                                   comment=self.get_formatted_loop_header_comment('    % {0}\n', '', '\n    # '))
        elif type_ == 'loop_footer':
            global_line_prefix = ''

            return '\r    end\n'

class MATLABExamplesGenerator(matlab_common.MATLABGeneratorTrait, common.ExamplesGenerator):
    def get_bindings_name(self):
        return 'matlab'

    def get_device_class(self):
        return JavaDevice

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

    def get_example_callback_configuration_function_class(self):
        return MATLABExampleCallbackConfigurationFunction

    def get_example_special_function_class(self):
        return MATLABExampleSpecialFunction

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

        blacklist = [
            'lcd-16x2-bricklet/unicode',
            'lcd-20x4-bricklet/unicode'
        ]

        # matlab
        for example in examples:
            filename = 'matlab_example_{0}.m'.format(example.get_name().under)
            filepath = os.path.join(examples_dir, filename)

            if device.get_git_name() + '/' + example.get_name().dash in blacklist:
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

            with open(os.path.join(examples_dir, filename), 'w') as f:
                f.write(example.get_matlab_source())

        # octave
        for example in examples:
            filename = 'octave_example_{0}.m'.format(example.get_name().under)
            filepath = os.path.join(examples_dir, filename)

            if device.get_git_name() + '/' + example.get_name().dash in blacklist:
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

            with open(filepath, 'w') as f:
                f.write(example.get_octave_source())

def generate(root_dir):
    common.generate(root_dir, 'en', MATLABExamplesGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
