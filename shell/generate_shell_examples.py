#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Shell Examples Generator
Copyright (C) 2015-2017 Matthias Bolte <matthias@tinkerforge.com>

generate_shell_examples.py: Generator for Shell examples

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

class ShellExample(common.Example):
    def get_shell_source(self):
        template = r"""#!/bin/sh
# Connects to localhost:4223 by default, use --host and --port to change this{incomplete}{description}

uid={dummy_uid} # Change {dummy_uid} to the UID of your {device_long_display_name}
{sources}{cleanups}"""

        if self.is_incomplete():
            incomplete = '\n\n# FIXME: This example is incomplete'
        else:
            incomplete = ''

        if self.get_description() != None:
            description = '\n\n# {0}'.format(self.get_description().replace('\n', '\n# '))
        else:
            description = ''

        sources = []
        add_read_call = False
        add_kill_call = False

        for function in self.get_functions():
            if isinstance(function, ShellExampleCallbackFunction):
                add_read_call = True
                add_kill_call = True

            if isinstance(function, ShellExampleSpecialFunction) and function.get_type() == 'wait':
                add_read_call = True

            sources.append(function.get_shell_source())

        while None in sources:
            sources.remove(None)

        if len(sources) == 0:
            sources = ['# TODO: Add example code here\n']
        elif add_read_call:
            sources.append('echo "Press key to exit"; read dummy\n')

        cleanups = []

        for cleanup in self.get_cleanups():
            cleanups.append(cleanup.get_shell_source())

        while None in cleanups:
            cleanups.remove(None)

        if add_kill_call:
            cleanups.append('kill -- -$$ # Stop callback dispatch in background\n')

        return template.format(incomplete=incomplete,
                               description=description,
                               device_long_display_name=self.get_device().get_long_display_name(),
                               dummy_uid=self.get_dummy_uid(),
                               sources='\n' + '\n'.join(sources).replace('\n\r', '').lstrip('\r'),
                               cleanups=common.wrap_non_empty('\n', '\n'.join(cleanups).replace('\n\r', '').lstrip('\r').rstrip('\n'), '')).rstrip('\n') + '\n'

class ShellExampleArgument(common.ExampleArgument):
    def get_shell_bitmask_comment(self):
        if ':bitmask:' in self.get_type():
            value = self.get_value()
            return '{0} = {1}'.format(common.make_c_like_bitmask(value), value)
        else:
            return None

    def get_shell_source(self):
        constant = self.get_value_constant()

        if constant != None:
            return '{0}-{1}'.format(constant.get_constant_group().get_dash_name(), constant.get_dash_name())

        type_ = self.get_type()
        value = self.get_value()

        if type_ == 'bool':
            if value:
                return 'true'
            else:
                return 'false'
        elif type_ == 'char':
            return '{0}'.format(value)
        elif type_ == 'string':
            return '"{0}"'.format(value)
        elif ':bitmask:' in type_:
            return str(value)
        else:
            return str(value)

class ShellExampleArgumentsMixin(object):
    def get_shell_arguments(self):
        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_shell_source())

        return arguments

class ShellExampleParameter(common.ExampleParameter):
    def get_shell_source(self):
        template = '{label_name}: {{{{{underscore_name}}}}}{divisor}{unit_name}'

        if self.get_label_name() == None:
            return None

        return template.format(underscore_name=self.get_underscore_name(),
                               label_name=self.get_label_name(),
                               divisor=self.get_formatted_divisor('/{0}', cast=int),
                               unit_name=self.get_formatted_unit_name(' {0}'))

class ShellExampleResult(common.ExampleResult):
    pass

class ShellExampleGetterFunction(common.ExampleGetterFunction, ShellExampleArgumentsMixin):
    def get_shell_source(self):
        template = r"""# Get current {function_comment_name}
tinkerforge call {device_dash_name}-{device_dash_category} $uid {function_dash_name}{arguments}
"""

        return template.format(device_dash_name=self.get_device().get_dash_name(),
                               device_dash_category=self.get_device().get_dash_category(),
                               function_comment_name=self.get_comment_name(),
                               function_dash_name=self.get_dash_name(),
                               arguments=common.wrap_non_empty(' ', ' '.join(self.get_shell_arguments()), ''))

class ShellExampleSetterFunction(common.ExampleSetterFunction, ShellExampleArgumentsMixin):
    def get_shell_source(self):
        template = '{comment1}{global_line_prefix}tinkerforge call {device_dash_name}-{device_dash_category} $uid {function_dash_name}{arguments}{comment2}\n'
        bitmask_comments = []

        for argument in self.get_arguments():
            bitmask_comments.append(argument.get_shell_bitmask_comment())

        while None in bitmask_comments:
            bitmask_comments.remove(None)

        comment1 = self.get_formatted_comment1(global_line_prefix + '# {0}\n', '\r', '\n' + global_line_prefix + '# ')
        comment2 = self.get_formatted_comment2(' # {0}', '')

        if len(bitmask_comments) > 0:
            if comment1 == '\r':
                if len(comment2) == 0:
                    comment2 = ' # ' + ', '.join(bitmask_comments)
                else:
                    comment2 += ': ' + ', '.join(bitmask_comments)
            else:
                comment1 = comment1.rstrip('\n') + ': ' + ', '.join(bitmask_comments) + '\n'

        return template.format(global_line_prefix=global_line_prefix,
                               device_dash_name=self.get_device().get_dash_name(),
                               device_dash_category=self.get_device().get_dash_category(),
                               function_dash_name=self.get_dash_name(),
                               arguments=common.wrap_non_empty(' ', ' '.join(self.get_shell_arguments()), ''),
                               comment1=comment1,
                               comment2=comment2)

class ShellExampleCallbackFunction(common.ExampleCallbackFunction):
    def get_shell_source(self):
        template1A = r"""# Handle incoming {function_comment_name} callbacks
"""
        template1B = r"""{override_comment}
"""
        template2 = r"""tinkerforge dispatch {device_dash_name}-{device_dash_category} $uid {function_dash_name}{extra_message} &
"""
        override_comment = self.get_formatted_override_comment('# {0}', None, '\n# ')

        if override_comment == None:
            template1 = template1A
        else:
            template1 = template1B

        parameters = []

        for parameter in self.get_parameters():
            parameters.append(parameter.get_shell_source())

        while None in parameters:
            parameters.remove(None)

        extra_message = self.get_formatted_extra_message('\\\n --execute "echo {parameters}{{0}}"'.format(parameters=common.wrap_non_empty('', '. '.join(parameters), '. ')))

        return template1.format(function_comment_name=self.get_comment_name(),
                                override_comment=override_comment) + \
               template2.format(device_dash_name=self.get_device().get_dash_name(),
                                device_dash_category=self.get_device().get_dash_category(),
                                function_dash_name=self.get_dash_name(),
                                extra_message=extra_message)

class ShellExampleCallbackPeriodFunction(common.ExampleCallbackPeriodFunction, ShellExampleArgumentsMixin):
    def get_shell_source(self):
        templateA = r"""# Set period for {function_comment_name} callback to {period_sec_short} ({period_msec}ms)
tinkerforge call {device_dash_name}-{device_dash_category} $uid set-{function_dash_name}-period {arguments}{period_msec}
"""
        templateB = r"""# Set period for {function_comment_name} callback to {period_sec_short} ({period_msec}ms)
# Note: The {function_comment_name} callback is only called every {period_sec_long}
#       if the {function_comment_name} has changed since the last call!
tinkerforge call {device_dash_name}-{device_dash_category} $uid set-{function_dash_name}-callback-period {arguments}{period_msec}
"""

        if self.get_device().get_underscore_name().startswith('imu'):
            template = templateA # FIXME: special hack for IMU Brick (2.0) callback behavior and name mismatch
        else:
            template = templateB

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        return template.format(device_dash_name=self.get_device().get_dash_name(),
                               device_dash_category=self.get_device().get_dash_category(),
                               function_dash_name=self.get_dash_name(),
                               function_comment_name=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ' '.join(self.get_shell_arguments()), ' '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long)

class ShellExampleCallbackThresholdMinimumMaximum(common.ExampleCallbackThresholdMinimumMaximum):
    def get_shell_source(self):
        template = '{minimum} {maximum}'

        return template.format(minimum=self.get_formatted_minimum(template='{result}'),
                               maximum=self.get_formatted_maximum(template='{result}'))

class ShellExampleCallbackThresholdFunction(common.ExampleCallbackThresholdFunction, ShellExampleArgumentsMixin):
    def get_shell_source(self):
        template = r"""# Configure threshold for {function_comment_name} "{option_comment}"
tinkerforge call {device_dash_name}-{device_dash_category} $uid set-{function_dash_name}-callback-threshold {arguments}{option_dash_name} {mininum_maximums}
"""
        mininum_maximums = []

        for mininum_maximum in self.get_minimum_maximums():
            mininum_maximums.append(mininum_maximum.get_shell_source())

        option_dash_names = {'o' : 'threshold-option-outside', '<': 'threshold-option-smaller', '>': 'threshold-option-greater'}

        return template.format(device_dash_name=self.get_device().get_dash_name(),
                               device_dash_category=self.get_device().get_dash_category(),
                               function_dash_name=self.get_dash_name(),
                               function_comment_name=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ' '.join(self.get_shell_arguments()), ' '),
                               option_dash_name=option_dash_names[self.get_option_char()],
                               option_comment=self.get_option_comment(),
                               mininum_maximums=' '.join(mininum_maximums))

class ShellExampleCallbackConfigurationFunction(common.ExampleCallbackConfigurationFunction, ShellExampleArgumentsMixin):
    def get_shell_source(self):
        templateA = r"""# Set period for {function_comment_name} callback to {period_sec_short} ({period_msec}ms)
tinkerforge call {device_dash_name}-{device_dash_category} $uid set-{function_dash_name}-callback-configuration {arguments}{period_msec} false
"""
        templateB = r"""# Set period for {function_comment_name} callback to {period_sec_short} ({period_msec}ms) without a threshold
tinkerforge call {device_dash_name}-{device_dash_category} $uid set-{function_dash_name}-callback-configuration {arguments}{period_msec} false {option_dash_name} {mininum_maximums}
"""
        templateC = r"""# Configure threshold for {function_comment_name} "{option_comment}"
# with a debounce period of {period_sec_short} ({period_msec}ms)
tinkerforge call {device_dash_name}-{device_dash_category} $uid set-{function_dash_name}-callback-configuration {arguments}{period_msec} false {option_dash_name} {mininum_maximums}
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
            mininum_maximums.append(mininum_maximum.get_shell_source())

        option_dash_names = {None: '', 'x' : 'threshold-option-off', 'o' : 'threshold-option-outside', '<': 'threshold-option-smaller', '>': 'threshold-option-greater'}

        return template.format(device_dash_name=self.get_device().get_dash_name(),
                               device_dash_category=self.get_device().get_dash_category(),
                               function_dash_name=self.get_dash_name(),
                               function_comment_name=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ' '.join(self.get_shell_arguments()), ' '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long,
                               option_dash_name=option_dash_names[self.get_option_char()],
                               option_comment=self.get_option_comment(),
                               mininum_maximums=' '.join(mininum_maximums))

class ShellExampleSpecialFunction(common.ExampleSpecialFunction):
    def get_shell_defines(self):
        if self.get_type() == 'sleep':
            return ['#define IPCON_EXPOSE_MILLISLEEP\n']
        else:
            return []

    def get_shell_function(self):
        return None

    def get_shell_source(self):
        global global_line_prefix

        type_ = self.get_type()

        if type_ == 'empty':
            return ''
        elif type_ == 'debounce_period':
            template = r"""# Get threshold callbacks with a debounce time of {period_sec} ({period_msec}ms)
tinkerforge call {device_dash_name}-{device_dash_category} $uid set-debounce-period {period_msec}
"""
            period_msec, period_sec = self.get_formatted_debounce_period()

            return template.format(device_dash_name=self.get_device().get_dash_name(),
                                   device_dash_category=self.get_device().get_dash_category(),
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
            template = '{comment}for i in {limit}; do\n'
            global_line_prefix = '\t'

            return template.format(limit=' '.join(map(str, range(self.get_loop_header_limit()))),
                                   comment=self.get_formatted_loop_header_comment('# {0}\n', '', '\n# '))
        elif type_ == 'loop_footer':
            global_line_prefix = ''

            return '\rdone\n'

class ShellExamplesGenerator(common.ExamplesGenerator):
    def get_bindings_name(self):
        return 'shell'

    def get_example_class(self):
        return ShellExample

    def get_example_argument_class(self):
        return ShellExampleArgument

    def get_example_parameter_class(self):
        return ShellExampleParameter

    def get_example_result_class(self):
        return ShellExampleResult

    def get_example_getter_function_class(self):
        return ShellExampleGetterFunction

    def get_example_setter_function_class(self):
        return ShellExampleSetterFunction

    def get_example_callback_function_class(self):
        return ShellExampleCallbackFunction

    def get_example_callback_period_function_class(self):
        return ShellExampleCallbackPeriodFunction

    def get_example_callback_threshold_minimum_maximum_class(self):
        return ShellExampleCallbackThresholdMinimumMaximum

    def get_example_callback_threshold_function_class(self):
        return ShellExampleCallbackThresholdFunction

    def get_example_callback_configuration_function_class(self):
        return ShellExampleCallbackConfigurationFunction

    def get_example_special_function_class(self):
        return ShellExampleSpecialFunction

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

        blacklist = [
            'led-strip-bricklet/callback',
            'nfc-rfid-bricklet/write-read-type2'
        ]

        for example in examples:
            filename = 'example-{0}.sh'.format(example.get_dash_name())
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

            with open(filepath, 'w') as f:
                f.write(example.get_shell_source())

            os.chmod(filepath, 0o755)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', ShellExamplesGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
