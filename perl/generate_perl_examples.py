#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Perl Examples Generator
Copyright (C) 2015-2018 Matthias Bolte <matthias@tinkerforge.com>

generate_perl_examples.py: Generator for Perl examples

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

class PerlConstant(common.Constant):
    def get_perl_source(self):
        template = '${device_name}->{constant_group_name}_{constant_name}'

        return template.format(device_name=self.get_device().get_initial_name(),
                               constant_group_name=self.get_constant_group().get_name().upper,
                               constant_name=self.get_name().upper)

class PerlExample(common.Example):
    def get_perl_source(self):
        template = r"""#!/usr/bin/perl{incomplete}{description}

use Tinkerforge::IPConnection;
use Tinkerforge::{device_category}{device_name_camel};

use constant HOST => 'localhost';
use constant PORT => 4223;
use constant UID => '{dummy_uid}'; # Change {dummy_uid} to the UID of your {device_name_long_display}
{subroutines}
my $ipcon = Tinkerforge::IPConnection->new(); # Create IP connection
my ${device_name_initial} = Tinkerforge::{device_category}{device_name_camel}->new(&UID, $ipcon); # Create device object

$ipcon->connect(&HOST, &PORT); # Connect to brickd
# Don't use device before ipcon is connected
{sources}
print "Press key to exit\n";
<STDIN>;{cleanups}
$ipcon->disconnect();
"""

        if self.is_incomplete():
            incomplete = '\n\n# FIXME: This example is incomplete'
        else:
            incomplete = ''

        if self.get_description() != None:
            description = '\n\n# {0}'.format(self.get_description().replace('\n', '\n# '))
        else:
            description = ''

        subroutines = []
        sources = []
        cleanups = []

        for function in self.get_functions():
            subroutines.append(function.get_perl_subroutine())
            sources.append(function.get_perl_source())

        for cleanup in self.get_cleanups():
            subroutines.append(cleanup.get_perl_subroutine())
            cleanups.append(cleanup.get_perl_source())

        while None in subroutines:
            subroutines.remove(None)

        while None in sources:
            sources.remove(None)

        if len(sources) == 0:
            sources = ['# TODO: Add example code here\n']

        while None in cleanups:
            cleanups.remove(None)

        return template.format(incomplete=incomplete,
                               description=description,
                               device_category=self.get_device().get_category().camel,
                               device_name_camel=self.get_device().get_name().camel,
                               device_name_initial=self.get_device().get_initial_name(),
                               device_name_long_display=self.get_device().get_long_display_name(),
                               dummy_uid=self.get_dummy_uid(),
                               subroutines=common.wrap_non_empty('\n', '\n'.join(subroutines), ''),
                               sources='\n' + '\n'.join(sources).replace('\n\r', '').lstrip('\r'),
                               cleanups=common.wrap_non_empty('\n', '\n'.join(cleanups).replace('\n\r', '').lstrip('\r').rstrip('\n'), ''))

class PerlExampleArgument(common.ExampleArgument):
    def get_perl_source(self):
        type_ = self.get_type()
        value = self.get_value()

        if type_ == 'bool':
            if value:
                return '1'
            else:
                return '0'
        elif type_ == 'char':
            return "'{0}'".format(value)
        elif type_ == 'string':
            return '"{0}"'.format(value)
        elif ':bitmask:' in type_:
            return common.make_c_like_bitmask(value)
        elif type_.endswith(':constant'):
            return self.get_value_constant().get_perl_source()
        else:
            return str(value)

class PerlExampleArgumentsMixin(object):
    def get_perl_arguments(self):
        return [argument.get_perl_source() for argument in self.get_arguments()]

class PerlExampleParameter(common.ExampleParameter):
    def get_perl_source(self):
        template = '${name}'

        return template.format(name=self.get_name().under)

    def get_perl_prints(self):
        templateA = '    print "{label}: " . {sprintf_prefix}{index_prefix}${name}{index_suffix}{divisor}{sprintf_suffix} . "{unit}\\n";{comment}'
        templateB = '    print "{label}: ${name}{unit}\\n";{comment}'

        if self.get_label_name() == None:
            return []

        if self.get_cardinality() < 0:
            return [] # FIXME: streaming

        type_ = self.get_type()
        divisor = self.get_formatted_divisor('/{0}')
        sprintf_prefix = ''
        sprintf_suffix = ''
        index_prefix = ''

        if ':bitmask:' in type_:
            template = templateA
            sprintf_prefix = "sprintf('%0{0}b', ".format(int(type_.split(':')[2]))
            sprintf_suffix = ')'
        elif len(divisor) > 0 or self.get_label_count() > 1:
            template = templateA

            if self.get_label_count() > 1:
                index_prefix = '@{'
        else:
            template = templateB

        result = []

        for index in range(self.get_label_count()):
            result.append(template.format(name=self.get_name().under,
                                          label=self.get_label_name(index=index),
                                          index_prefix=index_prefix,
                                          index_suffix='}}[{0}]'.format(index) if self.get_label_count() > 1 else '',
                                          divisor=divisor,
                                          unit=self.get_formatted_unit_name(' {0}'),
                                          sprintf_prefix=sprintf_prefix,
                                          sprintf_suffix=sprintf_suffix,
                                          comment=self.get_formatted_comment(' # {0}')))

        return result

class PerlExampleResult(common.ExampleResult):
    def get_perl_variable(self):
        template = '${name}'
        name = self.get_name().under

        if name == self.get_device().get_initial_name():
            name += '_'

        return template.format(name=name)

    def get_perl_prints(self):
        templateA = 'print "{label}: " . {sprintf_prefix}{index_prefix}${name}{index_suffix}{divisor}{sprintf_suffix} . "{unit}\\n";{comment}'
        templateB = 'print "{label}: ${name}{name}\\n";{comment}'

        if self.get_label_name() == None:
            return []

        if self.get_cardinality() < 0:
            return [] # FIXME: streaming

        name = self.get_name().under

        if name == self.get_device().get_initial_name():
            name += '_'

        type_ = self.get_type()
        divisor = self.get_formatted_divisor('/{0}')
        sprintf_prefix = ''
        sprintf_suffix = ''
        index_prefix = ''

        if ':bitmask:' in type_:
            template = templateA
            sprintf_prefix = "sprintf('%0{0}b', ".format(int(type_.split(':')[2]))
            sprintf_suffix = ')'
        elif len(divisor) > 0 or self.get_label_count() > 1:
            template = templateA

            if self.get_label_count() > 1:
                index_prefix = '@{'
        else:
            template = templateB

        result = []

        for index in range(self.get_label_count()):
            result.append(template.format(name=name,
                                          label=self.get_label_name(index=index),
                                          index_prefix=index_prefix,
                                          index_suffix='}}[{0}]'.format(index) if self.get_label_count() > 1 else '',
                                          divisor=divisor,
                                          unit=self.get_formatted_unit_name(' {0}'),
                                          sprintf_prefix=sprintf_prefix,
                                          sprintf_suffix=sprintf_suffix,
                                          comment=self.get_formatted_comment(' # {0}')))

        return result

class PerlExampleGetterFunction(common.ExampleGetterFunction, PerlExampleArgumentsMixin):
    def get_perl_subroutine(self):
        return None

    def get_perl_source(self):
        template = r"""# Get current {function_name_comment}
{variables} = ${device_name}->{function_name_under}({arguments});
{prints}
"""
        variables = []
        prints = []

        for result in self.get_results():
            variables.append(result.get_perl_variable())
            prints += result.get_perl_prints()

        if len(variables) > 1:
            variables = common.break_string('my (' + ',<BP>'.join(variables) + ')', 'my (')
        else:
            variables = 'my ' + variables[0]

        while None in prints:
            prints.remove(None)

        if len(prints) > 1:
            prints.insert(0, '')

        return template.format(device_name=self.get_device().get_initial_name(),
                               function_name_under=self.get_name().under,
                               function_name_comment=self.get_comment_name(),
                               variables=variables,
                               prints='\n'.join(prints),
                               arguments=', '.join(self.get_perl_arguments()))

class PerlExampleSetterFunction(common.ExampleSetterFunction, PerlExampleArgumentsMixin):
    def get_perl_subroutine(self):
        return None

    def get_perl_source(self):
        template = '{comment1}{global_line_prefix}${device_name}->{function_name}({arguments});{comment2}\n'
        marker = '->{}('

        result = template.format(global_line_prefix=global_line_prefix,
                                 device_name=self.get_device().get_initial_name(),
                                 function_name=self.get_name().under,
                                 arguments=',<BP>'.join(self.get_perl_arguments()),
                                 comment1=self.get_formatted_comment1(global_line_prefix + '# {0}\n', '\r', '\n' + global_line_prefix + '# '),
                                 comment2=self.get_formatted_comment2(' # {0}', ''))

        return common.break_string(result, marker.format(self.get_name().under))

class PerlExampleCallbackFunction(common.ExampleCallbackFunction):
    def get_perl_subroutine(self):
        template1A = r"""# Callback subroutine for {function_name_comment} callback
"""
        template1B = r"""{override_comment}
"""
        template2 = r"""sub cb_{function_name_under}
{{
{parameters}{prints}{extra_message}
}}
"""
        override_comment = self.get_formatted_override_comment('# {0}', None, '\n# ')

        if override_comment == None:
            template1 = template1A
        else:
            template1 = template1B

        parameters = []
        prints = []

        for parameter in self.get_parameters():
            parameters.append(parameter.get_perl_source())
            prints += parameter.get_perl_prints()

        while None in prints:
            prints.remove(None)

        if len(prints) > 1:
            prints.append('    print "\\n";')

        extra_message = self.get_formatted_extra_message('    print "{0}\\n";')

        if len(extra_message) > 0 and len(prints) > 0:
            extra_message = '\n' + extra_message

        result = template1.format(function_name_comment=self.get_comment_name(),
                                  override_comment=override_comment) + \
                 template2.format(function_name_under=self.get_name().under,
                                  parameters=common.wrap_non_empty('    my (', ',<BP>'.join(parameters), ') = @_;\n\n'),
                                  prints='\n'.join(prints),
                                  extra_message=extra_message)

        return common.break_string(result, 'my (')

    def get_perl_source(self):
        template1 = r"""# Register {function_name_comment}<BP>callback<BP>to<BP>subroutine<BP>cb_{function_name_under}
"""
        template2 = r"""${device_name}->register_callback(${device_name}->CALLBACK_{function_name_upper},<BP>'cb_{function_name_under}');
"""

        result1 = template1.format(function_name_under=self.get_name().under,
                                   function_name_comment=self.get_comment_name())
        result2 = template2.format(device_name=self.get_device().get_initial_name(),
                                   function_name_under=self.get_name().under,
                                   function_name_upper=self.get_name().upper)

        return common.break_string(result1, '# ', indent_tail='# ') + \
               common.break_string(result2, 'register_callback(')

class PerlExampleCallbackPeriodFunction(common.ExampleCallbackPeriodFunction, PerlExampleArgumentsMixin):
    def get_perl_subroutine(self):
        return None

    def get_perl_source(self):
        templateA = r"""# Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms)
${device_name}->set_{function_name_under}_period({arguments}{period_msec});
"""
        templateB = r"""# Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms)
# Note: The {function_name_comment} callback is only called every {period_sec_long}
#       if the {function_name_comment} has changed since the last call!
${device_name}->set_{function_name_under}_callback_period({arguments}{period_msec});
"""

        if self.get_device().get_name().space.startswith('IMU '):
            template = templateA # FIXME: special hack for IMU Brick (2.0) callback behavior and name mismatch
        else:
            template = templateB

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        return template.format(device_name=self.get_device().get_initial_name(),
                               function_name_under=self.get_name().under,
                               function_name_comment=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_perl_arguments()), ', '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long)

class PerlExampleCallbackThresholdMinimumMaximum(common.ExampleCallbackThresholdMinimumMaximum):
    def get_perl_source(self):
        template = '{minimum}, {maximum}'

        return template.format(minimum=self.get_formatted_minimum(),
                               maximum=self.get_formatted_maximum())

class PerlExampleCallbackThresholdFunction(common.ExampleCallbackThresholdFunction, PerlExampleArgumentsMixin):
    def get_perl_subroutine(self):
        return None

    def get_perl_source(self):
        template = r"""# Configure threshold for {function_name_comment} "{option_comment}"
${device_name}->set_{function_name_under}_callback_threshold({arguments}'{option_char}', {mininum_maximums});
"""
        mininum_maximums = []

        for mininum_maximum in self.get_minimum_maximums():
            mininum_maximums.append(mininum_maximum.get_perl_source())

        return template.format(device_name=self.get_device().get_initial_name(),
                               function_name_under=self.get_name().under,
                               function_name_comment=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_perl_arguments()), ', '),
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               mininum_maximums=', '.join(mininum_maximums))

class PerlExampleCallbackConfigurationFunction(common.ExampleCallbackConfigurationFunction, PerlExampleArgumentsMixin):
    def get_perl_subroutine(self):
        return None

    def get_perl_source(self):
        templateA = r"""# Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms)
${device_name}->set_{function_name_under}_callback_configuration({arguments}{period_msec}, 0);
"""
        templateB = r"""# Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms) without a threshold
${device_name}->set_{function_name_under}_callback_configuration({arguments}{period_msec}, 0, '{option_char}', {mininum_maximums});
"""
        templateC = r"""# Configure threshold for {function_name_comment} "{option_comment}"
# with a debounce period of {period_sec_short} ({period_msec}ms)
${device_name}->set_{function_name_under}_callback_configuration({arguments}{period_msec}, 0, '{option_char}', {mininum_maximums});
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
            mininum_maximums.append(mininum_maximum.get_perl_source())

        return template.format(device_name=self.get_device().get_initial_name(),
                               function_name_under=self.get_name().under,
                               function_name_comment=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_perl_arguments()), ', '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long,
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               mininum_maximums=', '.join(mininum_maximums))

class PerlExampleSpecialFunction(common.ExampleSpecialFunction):
    def get_perl_subroutine(self):
        return None

    def get_perl_source(self):
        global global_line_prefix

        type_ = self.get_type()

        if type_ == 'empty':
            return ''
        elif type_ == 'debounce_period':
            template = r"""# Get threshold callbacks with a debounce time of {period_sec} ({period_msec}ms)
${device_name}->set_debounce_period({period_msec});
"""
            period_msec, period_sec = self.get_formatted_debounce_period()

            return template.format(device_name=self.get_device().get_initial_name(),
                                   period_msec=period_msec,
                                   period_sec=period_sec)
        elif type_ == 'sleep':
            templateA = '{comment1}{global_line_prefix}sleep({duration});{comment2}\n'
            templateB = '{comment1}{global_line_prefix}select(undef, undef, undef, {duration});{comment2}\n'
            duration = self.get_sleep_duration()

            if duration % 1000 == 0:
                duration //= 1000
                template = templateA
            else:
                duration /= 1000.0
                template = templateB

            return template.format(global_line_prefix=global_line_prefix,
                                   duration=duration,
                                   comment1=self.get_formatted_sleep_comment1(global_line_prefix + '# {0}\n', '\r', '\n' + global_line_prefix + '# '),
                                   comment2=self.get_formatted_sleep_comment2(' # {0}', ''))
        elif type_ == 'wait':
            return None
        elif type_ == 'loop_header':
            template = '{comment}for (my $i = 0; $i < {limit}; $i++)\n{{\n'
            global_line_prefix = '    '

            return template.format(limit=self.get_loop_header_limit(),
                                   comment=self.get_formatted_loop_header_comment('# {0}\n', '', '\n# '))
        elif type_ == 'loop_footer':
            global_line_prefix = ''

            return '\r}\n'

class PerlExamplesGenerator(common.ExamplesGenerator):
    def get_bindings_name(self):
        return 'perl'

    def get_constant_class(self):
        return PerlConstant

    def get_example_class(self):
        return PerlExample

    def get_example_argument_class(self):
        return PerlExampleArgument

    def get_example_parameter_class(self):
        return PerlExampleParameter

    def get_example_result_class(self):
        return PerlExampleResult

    def get_example_getter_function_class(self):
        return PerlExampleGetterFunction

    def get_example_setter_function_class(self):
        return PerlExampleSetterFunction

    def get_example_callback_function_class(self):
        return PerlExampleCallbackFunction

    def get_example_callback_period_function_class(self):
        return PerlExampleCallbackPeriodFunction

    def get_example_callback_threshold_minimum_maximum_class(self):
        return PerlExampleCallbackThresholdMinimumMaximum

    def get_example_callback_threshold_function_class(self):
        return PerlExampleCallbackThresholdFunction

    def get_example_callback_configuration_function_class(self):
        return PerlExampleCallbackConfigurationFunction

    def get_example_special_function_class(self):
        return PerlExampleSpecialFunction

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

        for example in examples:
            filename = 'example_{0}.pl'.format(example.get_name().under)
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
                f.write(example.get_perl_source())

def generate(root_dir):
    common.generate(root_dir, 'en', PerlExamplesGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
