#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ruby Examples Generator
Copyright (C) 2015-2018 Matthias Bolte <matthias@tinkerforge.com>

generate_ruby_examples.py: Generator for Ruby examples

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
import ruby_common

global_line_prefix = ''

class RubyConstant(common.Constant):
    def get_ruby_source(self):
        template = '{device_camel_case_category}{device_camel_case_name}::{constant_group_upper_case_name}_{constant_upper_case_name}'

        return template.format(device_camel_case_category=self.get_device().get_camel_case_category(),
                               device_camel_case_name=self.get_device().get_camel_case_name(),
                               constant_group_upper_case_name=self.get_constant_group().get_upper_case_name(),
                               constant_upper_case_name=self.get_upper_case_name())

class RubyExample(common.Example):
    def get_ruby_source(self):
        template = r"""#!/usr/bin/env ruby
# -*- ruby encoding: utf-8 -*-{incomplete}{description}

require 'tinkerforge/ip_connection'
require 'tinkerforge/{device_underscore_category}_{device_underscore_name}'

include Tinkerforge

HOST = 'localhost'
PORT = 4223
UID = '{dummy_uid}' # Change {dummy_uid} to the UID of your {device_long_display_name}

ipcon = IPConnection.new # Create IP connection
{device_initial_name} = {device_camel_case_category}{device_camel_case_name}.new UID, ipcon # Create device object

ipcon.connect HOST, PORT # Connect to brickd
# Don't use device before ipcon is connected
{sources}
puts 'Press key to exit'
$stdin.gets{cleanups}
ipcon.disconnect
"""

        if self.is_incomplete():
            incomplete = '\n\n# FIXME: This example is incomplete'
        else:
            incomplete = ''

        if self.get_description() != None:
            description = '\n\n# {0}'.format(self.get_description().replace('\n', '\n# '))
        else:
            description = ''

        sources = []

        for function in self.get_functions():
            sources.append(function.get_ruby_source())

        while None in sources:
            sources.remove(None)

        if len(sources) == 0:
            sources = ['# TODO: Add example code here\n']

        cleanups = []

        for cleanup in self.get_cleanups():
            cleanups.append(cleanup.get_ruby_source())

        while None in cleanups:
            cleanups.remove(None)

        return template.format(incomplete=incomplete,
                               description=description,
                               device_camel_case_category=self.get_device().get_camel_case_category(),
                               device_underscore_category=self.get_device().get_underscore_category(),
                               device_camel_case_name=self.get_device().get_camel_case_name(),
                               device_underscore_name=self.get_device().get_underscore_name(),
                               device_initial_name=self.get_device().get_initial_name(),
                               device_long_display_name=self.get_device().get_long_display_name(),
                               dummy_uid=self.get_dummy_uid(),
                               sources='\n' + '\n'.join(sources).replace('\n\r', '').lstrip('\r'),
                               cleanups=common.wrap_non_empty('\n', '\n'.join(cleanups).replace('\n\r', '').lstrip('\r').rstrip('\n'), ''))

class RubyExampleArgument(common.ExampleArgument):
    def get_ruby_source(self):
        type_ = self.get_type()
        value = self.get_value()

        if type_ == 'bool':
            if value:
                return 'true'
            else:
                return 'false'
        elif type_ in  ['char', 'string']:
            return "'{0}'".format(value)
        elif ':bitmask:' in type_:
            return common.make_c_like_bitmask(value)
        elif type_.endswith(':constant'):
            return self.get_value_constant().get_ruby_source()
        else:
            return str(value)

class RubyExampleArgumentsMixin(object):
    def get_ruby_arguments(self):
        return [argument.get_ruby_source() for argument in self.get_arguments()]

class RubyExampleParameter(common.ExampleParameter):
    def get_ruby_source(self):
        underscore_name = self.get_underscore_name()

        if underscore_name == self.get_device().get_initial_name():
            underscore_name += '_'

        return underscore_name

    def get_ruby_puts(self):
        template = '  puts "{label_name}: #{{{printf_prefix}{underscore_name}{index}{divisor}{printf_suffix}}}{unit_final_name}"'

        if self.get_label_name() == None:
            return []

        if self.get_cardinality() < 0:
            return [] # FIXME: streaming

        underscore_name = self.get_underscore_name()

        if underscore_name == self.get_device().get_initial_name():
            underscore_name += '_'

        type_ = self.get_type()
        divisor = self.get_formatted_divisor('/{0}')
        printf_prefix = ''
        printf_suffix = ''

        if ':bitmask:' in type_:
            printf_prefix = "'%0{0}b' % ".format(int(type_.split(':')[2]))

            if len(divisor) > 0:
                printf_prefix += '('
                printf_suffix = ')'

        result = []

        for index in range(self.get_label_count()):
            result.append(template.format(underscore_name=underscore_name,
                                          label_name=self.get_label_name(index=index),
                                          index='[{0}]'.format(index) if self.get_label_count() > 1 else '',
                                          divisor=divisor,
                                          unit_final_name=self.get_unit_formatted_final_name(' {0}'),
                                          printf_prefix=printf_prefix,
                                          printf_suffix=printf_suffix))

        return result

class RubyExampleResult(common.ExampleResult):
    def get_ruby_variable(self):
        underscore_name = self.get_underscore_name()

        if underscore_name == self.get_device().get_initial_name():
            underscore_name += '_'

        return underscore_name

    def get_ruby_puts(self):
        template = 'puts "{label_name}: #{{{printf_prefix}{array_prefix}{underscore_name}{index}{divisor}{printf_suffix}}}{unit_final_name}"'

        if self.get_label_name() == None:
            return []

        if self.get_cardinality() < 0:
            return [] # FIXME: streaming

        if len(self.get_function().get_results()) > 1:
            underscore_name = '[{0}]'.format(self.get_index())
            array_prefix = self.get_function().get_underscore_name(skip=1)
        else:
            underscore_name = self.get_underscore_name()

            if underscore_name == self.get_device().get_initial_name():
                underscore_name += '_'

            array_prefix = ''

        type_ = self.get_type()
        divisor = self.get_formatted_divisor('/{0}')
        printf_prefix = ''
        printf_suffix = ''

        if ':bitmask:' in type_:
            printf_prefix = "'%0{0}b' % ".format(int(type_.split(':')[2]))

            if len(divisor) > 0:
                printf_prefix += '('
                printf_suffix = ')'

        result = []

        for index in range(self.get_label_count()):
            result.append(template.format(underscore_name=underscore_name,
                                          label_name=self.get_label_name(index=index),
                                          array_prefix=array_prefix,
                                          index='[{0}]'.format(index) if self.get_label_count() > 1 else '',
                                          divisor=divisor,
                                          unit_final_name=self.get_unit_formatted_final_name(' {0}'),
                                          printf_prefix=printf_prefix,
                                          printf_suffix=printf_suffix))

        return result

class RubyExampleGetterFunction(common.ExampleGetterFunction, RubyExampleArgumentsMixin):
    def get_ruby_source(self):
        template = r"""# Get current {function_comment_name}{comments}
{variables} = {device_initial_name}.{function_underscore_name}{arguments}
{puts}
"""
        comments = []
        variables = []
        puts = []

        for result in self.get_results():
            comments.append(result.get_formatted_comment())
            variables.append(result.get_ruby_variable())
            puts += result.get_ruby_puts()

        if len(comments) > 1 and len(set(comments)) == 1:
            comments = comments[:1]

        if len(variables) > 1:
            comments.insert(0, ' (returned as [{0}])'.format(', '.join([variable.rstrip('_') for variable in variables])))
            variables = [self.get_underscore_name(skip=1)]

        while None in puts:
            puts.remove(None)

        if len(puts) > 1:
            puts.insert(0, '')

        arguments = common.wrap_non_empty(' ', ', '.join(self.get_ruby_arguments()), '')

        if arguments.strip().startswith('('):
            arguments = '({0})'.format(arguments.strip())

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               function_underscore_name=self.get_underscore_name(),
                               function_comment_name=self.get_comment_name(),
                               comments=''.join(comments),
                               variables=', '.join(variables),
                               puts='\n'.join(puts),
                               arguments=arguments)

class RubyExampleSetterFunction(common.ExampleSetterFunction, RubyExampleArgumentsMixin):
    def get_ruby_source(self):
        template = '{comment1}{global_line_prefix}{device_initial_name}.{function_underscore_name}{arguments}{comment2}\n'
        arguments = common.wrap_non_empty(' ', ',<BP>'.join(self.get_ruby_arguments()), '')
        marker = '.{} '

        if arguments.strip().startswith('('):
            arguments = '({0})'.format(arguments.strip())
            marker = '.{}('

        result = template.format(global_line_prefix=global_line_prefix,
                                 device_initial_name=self.get_device().get_initial_name(),
                                 function_underscore_name=self.get_underscore_name(),
                                 arguments=arguments,
                                 comment1=self.get_formatted_comment1(global_line_prefix + '# {0}\n', '\r', '\n' + global_line_prefix + '# '),
                                 comment2=self.get_formatted_comment2(' # {0}', ''))

        return common.break_string(result, marker.format(self.get_underscore_name()), continuation=' \\')

class RubyExampleCallbackFunction(common.ExampleCallbackFunction):
    def get_ruby_source(self):
        template1A = r"""# Register {function_comment_name} callback{comments}
"""
        template1B = r"""{override_comment}
"""
        template2 = r"""{device_initial_name}.register_callback({device_camel_case_category}{device_camel_case_name}::CALLBACK_{function_upper_case_name}) do{parameters}
{puts}{extra_message}
end
"""
        override_comment = self.get_formatted_override_comment('# {0}', None, '\n# ')

        if override_comment == None:
            template1 = template1A
        else:
            template1 = template1B

        comments = []
        parameters = []
        puts = []

        for parameter in self.get_parameters():
            comments.append(parameter.get_formatted_comment())
            parameters.append(parameter.get_ruby_source())
            puts += parameter.get_ruby_puts()

        if len(comments) > 1 and len(set(comments)) == 1:
            comments = [comments[0].replace('parameter has', 'parameters have')]

        while None in puts:
            puts.remove(None)

        if len(puts) > 1:
            puts.append("  puts ''")

        extra_message = self.get_formatted_extra_message("  puts '{0}'")

        if len(extra_message) > 0 and len(puts) > 0:
            extra_message = '\n' + extra_message

        result = template1.format(function_comment_name=self.get_comment_name(),
                                  comments=''.join(comments),
                                  override_comment=override_comment) + \
                 template2.format(device_camel_case_category=self.get_device().get_camel_case_category(),
                                  device_camel_case_name=self.get_device().get_camel_case_name(),
                                  device_initial_name=self.get_device().get_initial_name(),
                                  function_underscore_name=self.get_underscore_name(),
                                  function_upper_case_name=self.get_upper_case_name(),
                                  parameters=common.wrap_non_empty(' |', ',<BP>'.join(parameters), '|'),
                                  puts='\n'.join(puts),
                                  extra_message=extra_message)

        return common.break_string(result, ') do |')

class RubyExampleCallbackPeriodFunction(common.ExampleCallbackPeriodFunction, RubyExampleArgumentsMixin):
    def get_ruby_source(self):
        templateA = r"""# Set period for {function_comment_name} callback to {period_sec_short} ({period_msec}ms)
{device_initial_name}.set_{function_underscore_name}_period {arguments}{period_msec}
"""
        templateB = r"""# Set period for {function_comment_name} callback to {period_sec_short} ({period_msec}ms)
# Note: The {function_comment_name} callback is only called every {period_sec_long}
#       if the {function_comment_name} has changed since the last call!
{device_initial_name}.set_{function_underscore_name}_callback_period {arguments}{period_msec}
"""

        if self.get_device().get_underscore_name().startswith('imu'):
            template = templateA # FIXME: special hack for IMU Brick (2.0) callback behavior and name mismatch
        else:
            template = templateB

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               function_underscore_name=self.get_underscore_name(),
                               function_comment_name=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_ruby_arguments()), ', '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long)

class RubyExampleCallbackThresholdMinimumMaximum(common.ExampleCallbackThresholdMinimumMaximum):
    def get_ruby_source(self):
        template = '{minimum}, {maximum}'

        return template.format(minimum=self.get_formatted_minimum(),
                               maximum=self.get_formatted_maximum())

class RubyExampleCallbackThresholdFunction(common.ExampleCallbackThresholdFunction, RubyExampleArgumentsMixin):
    def get_ruby_source(self):
        template = r"""# Configure threshold for {function_comment_name} "{option_comment}"{mininum_maximum_unit_comments}
{device_initial_name}.set_{function_underscore_name}_callback_threshold {arguments}'{option_char}', {mininum_maximums}
"""
        mininum_maximums = []
        mininum_maximum_unit_comments = []

        for mininum_maximum in self.get_minimum_maximums():
            mininum_maximums.append(mininum_maximum.get_ruby_source())
            mininum_maximum_unit_comments.append(mininum_maximum.get_unit_comment())

        if len(mininum_maximum_unit_comments) > 1 and len(set(mininum_maximum_unit_comments)) == 1:
            mininum_maximum_unit_comments = mininum_maximum_unit_comments[:1]

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               function_underscore_name=self.get_underscore_name(),
                               function_comment_name=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_ruby_arguments()), ', '),
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               mininum_maximums=', '.join(mininum_maximums),
                               mininum_maximum_unit_comments=''.join(mininum_maximum_unit_comments))

class RubyExampleCallbackConfigurationFunction(common.ExampleCallbackConfigurationFunction, RubyExampleArgumentsMixin):
    def get_ruby_source(self):
        templateA = r"""# Set period for {function_comment_name} callback to {period_sec_short} ({period_msec}ms)
{device_initial_name}.set_{function_underscore_name}_callback_configuration {arguments}{period_msec}, false
"""
        templateB = r"""# Set period for {function_comment_name} callback to {period_sec_short} ({period_msec}ms) without a threshold
{device_initial_name}.set_{function_underscore_name}_callback_configuration {arguments}{period_msec}, false, '{option_char}', {mininum_maximums}
"""
        templateC = r"""# Configure threshold for {function_comment_name} "{option_comment}"{mininum_maximum_unit_comments}
# with a debounce period of {period_sec_short} ({period_msec}ms)
{device_initial_name}.set_{function_underscore_name}_callback_configuration {arguments}{period_msec}, false, '{option_char}', {mininum_maximums}
"""

        if self.get_option_char() == None:
            template = templateA
        elif self.get_option_char() == 'x':
            template = templateB
        else:
            template = templateC

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        mininum_maximums = []
        mininum_maximum_unit_comments = []

        for mininum_maximum in self.get_minimum_maximums():
            mininum_maximums.append(mininum_maximum.get_ruby_source())
            mininum_maximum_unit_comments.append(mininum_maximum.get_unit_comment())

        if len(mininum_maximum_unit_comments) > 1 and len(set(mininum_maximum_unit_comments)) == 1:
            mininum_maximum_unit_comments = mininum_maximum_unit_comments[:1]

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               function_underscore_name=self.get_underscore_name(),
                               function_comment_name=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_ruby_arguments()), ', '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long,
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               mininum_maximums=', '.join(mininum_maximums),
                               mininum_maximum_unit_comments=''.join(mininum_maximum_unit_comments))

class RubyExampleSpecialFunction(common.ExampleSpecialFunction):
    def get_ruby_source(self):
        global global_line_prefix

        type_ = self.get_type()

        if type_ == 'empty':
            return ''
        elif type_ == 'debounce_period':
            template = r"""# Get threshold callbacks with a debounce time of {period_sec} ({period_msec}ms)
{device_initial_name}.set_debounce_period {period_msec}
"""
            period_msec, period_sec = self.get_formatted_debounce_period()

            return template.format(device_initial_name=self.get_device().get_initial_name(),
                                   period_msec=period_msec,
                                   period_sec=period_sec)
        elif type_ == 'sleep':
            template = '{comment1}{global_line_prefix}sleep {duration}{comment2}\n'
            duration = self.get_sleep_duration()

            if duration % 1000 == 0:
                duration //= 1000
            else:
                duration /= 1000.0

            return template.format(global_line_prefix=global_line_prefix,
                                   duration=duration,
                                   comment1=self.get_formatted_sleep_comment1(global_line_prefix + '# {0}\n', '\r', '\n' + global_line_prefix + '# '),
                                   comment2=self.get_formatted_sleep_comment2(' # {0}', ''))
        elif type_ == 'wait':
            return None
        elif type_ == 'loop_header':
            template = '{comment}for _ in 0..{limit}\n'
            global_line_prefix = '  '

            return template.format(limit=self.get_loop_header_limit() - 1,
                                   comment=self.get_formatted_loop_header_comment('# {0}\n', '', '\n# '))
        elif type_ == 'loop_footer':
            global_line_prefix = ''

            return '\rend\n'

class RubyExamplesGenerator(common.ExamplesGenerator):
    def get_bindings_name(self):
        return 'ruby'

    def get_constant_class(self):
        return RubyConstant

    def get_example_class(self):
        return RubyExample

    def get_example_argument_class(self):
        return RubyExampleArgument

    def get_example_parameter_class(self):
        return RubyExampleParameter

    def get_example_result_class(self):
        return RubyExampleResult

    def get_example_getter_function_class(self):
        return RubyExampleGetterFunction

    def get_example_setter_function_class(self):
        return RubyExampleSetterFunction

    def get_example_callback_function_class(self):
        return RubyExampleCallbackFunction

    def get_example_callback_period_function_class(self):
        return RubyExampleCallbackPeriodFunction

    def get_example_callback_threshold_minimum_maximum_class(self):
        return RubyExampleCallbackThresholdMinimumMaximum

    def get_example_callback_threshold_function_class(self):
        return RubyExampleCallbackThresholdFunction

    def get_example_callback_configuration_function_class(self):
        return RubyExampleCallbackConfigurationFunction

    def get_example_special_function_class(self):
        return RubyExampleSpecialFunction

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
            filename = 'example_{0}.rb'.format(example.get_underscore_name())
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
                f.write(example.get_ruby_source())

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', RubyExamplesGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
